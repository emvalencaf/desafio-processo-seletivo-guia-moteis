from typing import Tuple
from langchain_core.prompts import ChatPromptTemplate


from ia.templates.prompt_template import user_prompt, system_role

def get_system_prompt() -> Tuple[str, str]:
    """
    Returns the system prompt for the AI assistant.

    :return: A tuple representing the system role and its corresponding instruction.
    """
    return ("system", system_role)


def get_prompt_template() -> ChatPromptTemplate:
    """
    Creates a chat prompt template by combining the system prompt and user instructions.

    :return: A ChatPromptTemplate object containing system and user messages.
    """
    system_prompt = get_system_prompt()
    
    return ChatPromptTemplate.from_messages([system_prompt, ("human", user_prompt)])
