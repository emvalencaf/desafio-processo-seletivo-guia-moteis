from os import getenv
from typing import Literal
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')

class GlobalConfig(BaseSettings):
    V_STR:str = getenv("V_STR", 'v1')
    
    ENVIRONMENT: Literal["DEVELOPMENT",
                         "TEST",
                         "PRODUCTION",] = getenv("ENVIRONMENT", 'DEVELOPMENT')
    
    OPENAI_API_KEY: str = getenv("OPENAI_API_KEY")
    
    LLM_MODEL_URI: str = getenv("LLM_MODEL_URI",
                                "gpt-4o-mini")
    
    LLM_MODEL_TEMPERATURE: float = float(getenv("LLM_MODEL_TEMPERATURE", "0"))
    
    LLM_MODEL_MAX_TOKENS: int = int(getenv("LLM_MODEL_MAX_TOKENS",
                                           "280"))
    
    if not OPENAI_API_KEY:
        raise ValueError("You must pass a openai key as a environment variable (OPENAI_KEY) to run this project.")
    
    DATABASE_URL: str = getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        raise ValueError("You must pass a url database as a environment variable (DATABASE_URL) to run this project.")
    
    DASHBOARD_URL: str = str(getenv("DASHBOARD_URL",
                                    "http://localhost:8501"))
    
    CRONTAB: str = str(getenv("CRONTAB",
                              "* * * * *"))
    
    class Config:
        case_sensitive = True
        
global_settings: GlobalConfig = GlobalConfig()