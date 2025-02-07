# Solução - Desafio de Análise de Conversas com OpenAI

## Autor

| Edson Mota Valença Filho|
|-|
| (81) 9.9633-9891 |
| edsomvf@hotmail.com |
| linkedin.com/in/emvalencaf |
| github.com/emvalencaf |

## Sobre a solução proposta ao desafio

A proposta é criar uma *end-to-end LLM app* para analisar as mensagens de interação entre IA (chatbot) e humano de forma assíncrona em lote (*batches*) e possibilitar a auditoria (humana) tanto do processo de iteração IA-Humano (chatbot) quanto da própria avaliação da IA.

![Diagrama da Arquitetura Geral](/docs/diagrams/general_architecture.png)

## Estrutura do projeto
```plaintext
|__ api/
|    |__ cron/  # Contains scheduled jobs for background tasks
|    |    |__ analysis_job.py  # Script for processing chatbot session analysis
|    |    |__ job.py  # General cron job management script
|    |
|    |__ helpers/  # Utility functions for formatting and parsing
|    |    |__ format_message.py  # Formats messages for chatbot analysis
|    |    |__ parser_output.py  # Parses the output from AI responses
|    |
|    |__ ia/  # AI-related logic and processing
|    |    |__ templates/  # Stores AI prompt templates
|    |    |     |__ prompt_template.py  # Defines prompt structures for AI models
|    |    |
|    |    |__ ia.py  # Main AI processing logic and invocation
|    |    |__ prompt.py  # Handles AI prompts dynamically
|    |    |__ schema.py  # Defines Pydantic schemas for AI input/output
|    |
|    |__ .dockerignore  # Specifies files to ignore when building a Docker image
|    |__ .env  # Environment variables file (not versioned)
|    |__ .env.example  # Example environment variables file
|    |__ .gitignore  # Specifies files to ignore in Git version control
|    |__ app.py  # Main application entry point
|    |__ config.py  # Configuration settings for the application
|    |__ database.py  # Database connection setup
|    |__ dependencies.py  # Dependency injection setup for FastAPI
|    |__ lifespan.py  # Manages FastAPI application startup/shutdown events
|    |__ repositories.py  # Database repository layer for handling queries
|    |__ router.py  # Defines API routes for FastAPI
|
|__ prisma/  # Prisma ORM-related files
|     |__ sql/  # Stores raw SQL queries or migrations
|     |    |__ sql.sql  # SQL script file
|     |
|     |__ schema.prisma  # Prisma schema definition for database models
|
|__ dashboard/  # Placeholder for the dashboard interface (could be frontend or admin panel)

```

As *features* são:
- **Visualizar as métricas de satisfação**
- **Avaliações**
- **Monitoramento da Gen AI**

## Escolha das bibliotecas e linguagem de programação

Como o desafio não explicitou qual linguagem devo usar, optei por escolher a linguagem de `python` porque é a qual estou mais acostumado para desenvolver programas baseados em inteligência artificial. Embora, para as especificações `nodejs` também poderia ser usado.

- **Framework**: Streamlit (WEB frontend), FastAPI (para WEB backend) e LangChain (para GenAI).
- **ORM**: Prisma (escolhido pelo avaliador).
- **Arquitetura**: microsserviços.
- **Padrão de Projeto**: em camadas.

Como o desafio não impediu de usar *frameworks* optei por utilizá-los para acelerar a entrega. 

## Módulos

### `api/`

O módulo `api/` concentra a parte lógica do servidor da aplicação WEB.

#### `api/cron/`

Esse módulo é responsável pela lógica para agendar um *cron job* que vai ser executado periodicamente enquanto o servidor estiver online. A variável de ambiente `CRONTAB` determina a periodicidade em que o *cron job* será executado.

```python
def get_cron_trigger():
    """
    Creates a cron trigger using the global CRONTAB settings.

    :return: A CronTrigger instance configured with the global CRONTAB settings.
    """
    print(global_settings.CRONTAB)
    
    return CronTrigger.from_crontab(global_settings.CRONTAB)

def get_scheduler():
    """
    Creates and returns a new instance of BackgroundScheduler.

    :return: A BackgroundScheduler instance.
    """
    return BackgroundScheduler()

def add_cron_job(fn: Callable):
    """
    Adds a function as a scheduled cron job and starts the scheduler.

    :param fn: The function to be scheduled.
    :return: A BackgroundScheduler instance.
    """
    scheduler = get_scheduler()
    
    scheduler.add_job(fn, get_cron_trigger())

    return scheduler
```

O *cron job* vai executar uma análise de todas as mensagens atreladas as sessões registradas no banco de dados, apenas as sessões que possuem mensagens e não possuem análise ligada a elas. E faz o registro de cada análise em lote.

```python
async def analysis_chatbot_cron_job():
    """
    Executes the analysis of sessions asynchronously.

    This function gathers all sessions without analysis and with at least one message,
    processes each session asynchronously, and stores the results in the database.

    It performs the following steps:
    1. Retrieves sessions that haven't been analyzed and have messages.
    2. Processes each session asynchronously.
    3. Creates analysis entries for sessions that were processed successfully.
    
    :return: None
    """
    logging.info("Starting the chatbot analysis cron job...")

    try:
        async with Prisma() as db:
            session_repository = get_session_repository(db=db)
            analysis_repository = get_analysis_repository(db=db)

            # Filter sessions with no analysis and at least one message
            sessions = await session_repository.find_many(
                where={"analysis": {"none": {}}, "message": {"some": {}}},
                include={"analysis": True, "message": True}
            )
            
            if not sessions:
                logging.info("No sessions found for analysis.")
                return

            logging.info(f"{len(sessions)} sessions found for analysis.")

            # Create tasks to process all sessions at once
            results = await asyncio.gather(*[process_session(session) for session in sessions])

            # Filter sessions that did not fail
            list_analysis = [analysis for analysis in results if analysis is not None]

            if list_analysis:
                await analysis_repository.create_many(
                    data=[analysis.model_dump() for analysis in list_analysis]
                )
                logging.info(f"{len(list_analysis)} analyses were successfully created.")
            else:
                logging.warning("No analyses were created due to failures.")

    except Exception as e:
        logging.error(f"Critical error in cron job: {e}")

    logging.info("Finishing the chatbot analysis cron job.")
```

#### `api/ia/`

Esse módulo é responsável por instanciar um `ChatOpenAI` do `langchain-openai` e `ChatPromptTemplate` e operar a lógica para invocar as inferências ao modelo da IA de forma assíncrona.

```python
async def ainvoke(input: str, ai_model = Depends(get_ai_model)):
    """
    Invokes the AI model asynchronously and retrieves the response.

    This function initializes an AI model using a predefined prompt template and LLM model,
    then asynchronously invokes it with the given input. The response metadata, including
    token usage and model details, is also extracted.

    :param input: The input string to be processed by the AI model
    :return: A tuple containing the response content and metadata with token usage details
    """
    prompt_template = get_prompt_template()
    
    llm = get_llm_model()
    
    ai_model = get_ai_model(prompt_template=prompt_template, llm=llm)
    
    response = await ai_model.ainvoke(input={ "session_chat_history" : input })

    return parser_output(response, schema=AnalyseSchema)
```
A função `parser_output` (`/api/helpers/parser_output.py`) é responsável por garantir que a resposta do modelo IA seja convertido para um JSON:
```python
def parser_to_json(content: str) -> Union[dict, list, None]:
    """
    Parses a JSON-formatted string, removing Markdown-style code blocks if present.

    This function cleans the input string by removing triple backticks and optional "json" markers,
    then attempts to parse it into a Python dictionary or list.

    :param content: A string containing JSON data, possibly wrapped in Markdown code blocks.
    :return: A dictionary or list if parsing is successful, otherwise None.
    """
    try:
        # Remove Markdown-style JSON code block markers (```json ... ```)
        cleaned_json_str = re.sub(r'^```json\n?|```$', '', content, flags=re.MULTILINE).strip()
        return json.loads(cleaned_json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def parser_output(response: BaseMessage, schema: Type[BaseModel]) -> BaseModel:
    """
    Parses the response content and metadata into a structured schema.

    :param response: The message response containing content and metadata.
    :param schema: A Pydantic model class used to validate and structure the parsed output.
    :return: An instance of the provided schema containing the parsed response data.
    """
    json_response = parser_to_json(content=response.content)
    parsed_metadata = parser_metadata(raw_metadata=response.response_metadata)

    parsed = {
        **json_response,
        "metadata": parsed_metadata
    }

    return schema(**parsed)
```
Como alternativa seria possível usar os métodos `built-in` do `langchain` (documentação: [clique aqui](https://python.langchain.com/docs/how_to/structured_output/)), entretanto, eles aumentaram a quantidade de tokens de entrada e o tempo resposta do modelo. Logo, por uma questão de performance e economia optou-se por criar uma função autônoma.

##### `api/ia/templates`

Nesse diretório está armazenado os prompts usados para aplicação.

As técnicas de engenharia de prompt utilizadas forma `chain of thought`, `role`, `few-shoot` e `output indicator`, para garantir que o modelo de IA generativa entregue como output um objeto `JSON`. Por vezes, o modelo entregará um objeto `JSOn` em *markdown*, por essa razão, é importante ter um parser.

````python
system_role = "Você é um analista de vendas sênior responsável por avaliar o comportamento de um chatbot de uma rede de motéis."

user_prompt = """
Ao receber o histórico de interação com o chatbot de uma mesma sessão, você deverá realizar:
1. Analisar o nível de satisfação e atribuir uma nota de 0 a 10.
2. Resumir os principais pontos daquela sessão em bullet-points.
3. Apontar melhorias para o comportamento do chatbot.

A saída deverá ser um objeto JSON.

Exemplo:
{{
    "satisfaction": 7,
    "summary": [
        "- O usuário tentou reservar uma suíte.",
        "- O chatbot forneceu informações detalhadas sobre os preços.",
        "- O chatbot não entendeu a solicitação de alteração no horário de check-in."
    ],
    "improvement": [
        "- Melhorar a compreensão de mudanças nos horários de check-in.",
        "- Respostas mais objetivas e diretas."
    ]
}}

Histórico da Sessão:
{session_chat_history}
"""
````

###### Melhorias

Melhorias para o futuro seria armazenar esses *prompts* em um *storage* e fazer a chamadas no código e coordenar a leitura dele com a leitura do metadados da prompt, algo como uma tabela:

|prompt_id|prompt_path|created_at|updated_at|
|-|-|-|-|

Esse ajuste permitiria uma melhor monitoramento em produção do processo de ``LLMOps``, permitindo saber em um dashboard quais prompts estão performando melhor.

#### Variáveis de ambiente do módulo `api/`

- `DB_URL`: essa variável deve conter a URL do banco de dados (ex: postgresql://{usuario}:{senha}@{host}:{porta}/{database}?schema={esquema}).
- `OPENAI_KEY`: essa variável deve conter a api key da OpenAI.
- `LLM_MODEL_URI`(***Opcional***): essa variável deve conter a uri do llm model (qual é o modelo da OpenAI). Padrão: `gpt-4o-mini`.
- `LLM_MODEL_TEMPERATURE`(***Opcional***): essa variável deve conter a temperatura que o LLM vai operar. Padrão `0`.
   - Quanto maior a temperatura maior a "criatividade" do modelo. Para trabalhos de análises é recomendável usar a temperatura baixa.
- `LLM_MODEL_MAX_TOKENS`(***Opcional***): essa variável deve conter a quantidade máxima de tokens de saída o modelo deve gerar. Padrão: `280`
   - É recomendável colocar o valor necessário para fazer o trabalho. Lembrando que os tokens de saída são mais caros que os tokens de entrada.
- `ENVIRONMENT`(***Opcional***): essa variável deve conter qual é o ambiente que o projeto vai rodar: `DEVELOPMENT`, `TEST` e `PRODUCTION`. Padrão: `DEVELOPMENT`.
- `DASHBOARD_URL`(***Opcional***): essa variável contém a URL do frontend do dashboard para fins de COORS. Padrão: `http://localhost:`
- `BACKEND_PORT`(***Opcional***): essa variável contém a porta em que o servidor vai rodar. Padrão: `8000`
- `BACKEND_HOST` (***Opcional***): essa variável contém o host do servidor. Padrão: `localhost`
- `V_STR`(***Opcional***): essa variável contém o número da versão da API. Padrão: `v1`
- `CRONTAB`(***Opcional***): essa variável contém a expressão para agendar a frequência que o cronjob vai ser executado. Padrão: ``* * * * *``(a cada 1 minuto)

## Requisitos

## Como usar


## Fontes consultadas

- [Build and deploy Python cron scheduler using APscheduler and Heroku](https://medium.com/@sauravkumarsct/build-and-deploy-python-cron-scheduler-using-apscheduler-and-heroku-8c90ce4ba069)


# Enunciado - Desafio de Análise de Conversas com OpenAI

Desenvolva uma aplicação para analisar conversas de atendimento e extrair as informações:
- **satisfaction**: nota de satisfação do cliente (0 a 10);
- **summary**: resumo da conversa;
- **improvement**: como a conversa poderia ter sido melhor.

A aplicação deve utilizar a API `https://api.openai.com/v1/chat/completions` com o modelo `gpt-4o-mini` para processar as mensagens e gravar o resultado no banco de dados. Caso outras informações sejam consideradas úteis, novas colunas podem ser adicionadas à tabela `analysis`.

## Pré-requisitos

- **Docker**  
- **Docker Compose**  
- Chave da API do OpenAI (fornecida pelo entrevistador)

## Configuração

1. Clone este repositório.
2. Edite as configurações necessárias para incluir a chave da API do OpenAI.
3. Caso queira adicionar novas colunas à tabela `analysis`, faça a alteração no modelo de dados correspondente.
4. Adicione sua aplicação no docker compose.

## Execução

1. No diretório raiz do projeto, execute:
   ```bash
   docker-compose up --build
   ```
2. A aplicação iniciará e fará a análise das conversas.

3. As informações extraídas serão gravadas no banco de dados.

## Avaliação
- A elaboração do prompt e a solução para extração de dados são os pontos principais a serem avaliados.
- A aplicação deve ser iniciada e fazer a análise das conversas ao executar o comando `docker-compose up --build`.

## Observações

- Mensagens de exemplo serão inseridas automaticamente no banco de dados.
- As conversas possuem o campo `remote` para indicar se a mensagem foi enviada pelo cliente (`true`) ou pela assistente (`false`).
- Uma boa conversa é aquela em que a assistente responde adequadamente às perguntas do usuário e finaliza a reserva.  

