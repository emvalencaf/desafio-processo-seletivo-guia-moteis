from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable

from ia.schema import AnalyseSchema
from helpers.parser_output import parser_output
from ia.prompt import get_prompt_template
from config import global_settings

def get_settings_llm_model():
    """
    Retrieves the settings for the LLM model.

    This function fetches the global configuration for the LLM model, including its URI, temperature, and max token limit.

    :return: Dictionary containing the model settings
    """
    return {
        "model": global_settings.LLM_MODEL_URI,
        "temperature": global_settings.LLM_MODEL_TEMPERATURE,
        "max_tokens": global_settings.LLM_MODEL_MAX_TOKENS,
    }

def get_llm_model():
    """
    Initializes and returns an instance of the ChatOpenAI model.

    This function retrieves the model settings and uses them to instantiate a ChatOpenAI instance.

    :return: Instance of ChatOpenAI initialized with the retrieved settings
    """
    settings = get_settings_llm_model()
    
    return ChatOpenAI(**settings)

def get_ai_model(prompt_template: ChatPromptTemplate, llm: ChatOpenAI):
    """
    Combines a prompt template with an LLM model.

    This function pipes the provided prompt template into the LLM model, creating a configured AI model ready for inference.

    :param prompt_template: The chat prompt template to be used
    :param llm: The ChatOpenAI model instance
    :return: A configured AI model combining the prompt template and LLM model
    """
    return prompt_template | llm

async def ainvoke(input: str) -> AnalyseSchema:
    """
    Asynchronously invokes the AI model and retrieves the response.

    This function initializes an AI model using a predefined prompt template and LLM model,
    then asynchronously invokes the model with the given input. The function also extracts
    the response metadata, such as token usage and model details.

    :param input: The input string that will be processed by the AI model.
    :return: An instance of AnalyseSchema containing the response from the AI model, 
             including analysis results and metadata.
    """
    prompt_template = get_prompt_template()
    
    llm = get_llm_model()
    
    ai_model = get_ai_model(prompt_template=prompt_template,
                            llm=llm)
    
    response = await ai_model.ainvoke(input={ "session_chat_history" : input })

    return parser_output(response, schema=AnalyseSchema)


