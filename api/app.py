from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lifespan import lifespan
from router import api_router
from config import global_settings

app = FastAPI(title="ChatInsight",
              version='0.0.1',
              description="end-to-end LLM app para analisar as mensagens de interação entre IA (chatbot) e humano de forma assíncrona em lotes (batches) e possibilitar a auditoria (humana) tanto do processo de iteração IA-Humano (chatbot) quanto da própria avaliação da IA.",
              lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[global_settings.DASHBOARD_URL,],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)

app.include_router(api_router,
                   prefix=f"/api/{global_settings.V_STR}")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:app",
                log_level='info',
                reload=True)