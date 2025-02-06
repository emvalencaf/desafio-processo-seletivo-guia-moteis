# Solução - Desafio de Análise de Conversas com OpenAI

## Autor

| Edson Mota Valença Filho|
|-|
| (81) 9.9633-9891 |
| edsomvf@hotmail.com |
| linkedin.com/in/emvalencaf |
| github.com/emvalencaf |

## Sobre a solução proposta ao desafio

A proposta é criar uma *end-to-end LLM app* para analisar as mensagens de iteração entre IA (chatbot) e humano de forma assíncrona em lote (*batches*) e possibilitar a auditoria (humana) tanto do processo de iteração IA-Humano (chatbot) quanto da própria avaliação da IA.

![Diagrama da Arquitetura Geral](/docs/diagrams/general_architecture.png)

### Estrutura do projeto
```plaintext
|__ api/
|
|
|__ prisma/
|
|
|__ dashboard/
```

As *features* são:
- **Visualizar as métricas de satisfação**
- **Avaliações**
- **Monitoramento da Gen AI**

### Escolha das bibliotecas e linguagem de programação

Como o desafio não explicitou qual linguagem devo usar, optei por escolher a linguagem de `python` porque é a qual estou mais acostumado para desenvolver programas baseados em inteligência artificial. Embora, para as especificações `nodejs` também poderia ser usado.

- **Framework**: Streamlit (WEB frontend), FastAPI (para WEB backend) e LangChain (para GenAI).
- **ORM**: Prisma (escolhido pelo avaliador).
- **Arquitetura**: microsserviços.
- **Padrão de Projeto**: em camadas.

Como o desafio não impediu de usar *frameworks* optei por utilizá-los para acelerar a entrega. 

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

