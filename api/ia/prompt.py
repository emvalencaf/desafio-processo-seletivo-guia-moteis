from langchain_core.prompts import ChatPromptTemplate


from ia.templates.prompt_template import user_prompt, system_role

def get_system_prompt():
    """
    """
    
    return ( "system", system_role )

def get_prompt_template():
    """
    """
    system_prompt = get_system_prompt()
    
    return ChatPromptTemplate.from_messages([system_prompt,
                                             ("human", user_prompt)])