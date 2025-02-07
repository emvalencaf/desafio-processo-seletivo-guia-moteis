from fastapi import APIRouter, Depends
from cron.analysis_job import analysis_chatbot_cron_job, run_analysis_job
from repositories import get_session_repository
from dependencies import get_session_db
from prisma.actions import sessionActions
from prisma.models import session
from langchain_core.runnables import RunnableSerializable
from pydantic import BaseModel
from prisma import Prisma

from ia.ia import ainvoke, get_ai_model, get_llm_model
from ia.prompt import get_prompt_template
from helpers.format_message import format_messages

api_router = APIRouter()


class AIModelInputSchema(BaseModel):
    input: str

@api_router.post("/llm")
async def hello_world(input: AIModelInputSchema,):
    """
    """
    ai_model = get_ai_model(prompt_template=get_prompt_template(),
                            llm=get_llm_model())
    
    return await ai_model.ainvoke(input=input)

@api_router.get("/{id}/messages")
async def get_session_messages(id: int,
                               db: Prisma = Depends(get_session_db)):
  
    await analysis_chatbot_cron_job(db=db)
    return { "result" : "ok" }

@api_router.get("/all-analysis")
async def get_all_analysis(db: Prisma = Depends(get_session_db)):
    return await db.analysis.find_many()