from fastapi import APIRouter, Depends
from prisma import Prisma
from dependencies import get_session_db
from repositories import get_analysis_repository
router = APIRouter(tags=["chatbot-analysis"])

@router.get("/")
async def get_all_analysis(db: Prisma = Depends(get_session_db)) -> list:
    """
    Fetches all analysis data, including session and motel information.

    This endpoint performs an SQL query that retrieves analysis-related data 
    by joining the `analysis`, `session`, and `motel` tables in the database. 
    The result includes analysis information such as satisfaction, improvement, 
    tokens, and cost data along with session and motel details.

    :param db: The Prisma client used to interact with the database. It's injected via FastAPI's dependency injection system.
    :return: A list of analysis data with details about the analysis, session, and motel.
    """
    result = await db.query_raw("""
                                SELECT
                                    a.id as analysis_id,
                                    a.satisfaction,
                                    a.improvement,
                                    a.summary,
                                    a.output_tokens,
                                    a.input_tokens,
                                    a.input_tokens_price,
                                    a.output_tokens_price,
                                    a.llm_model,
                                    a.created_at as analysis_created_at,
                                    s.id as session_id,
                                    s.created_at as session_created_at,
                                    m.id as motel_id,
                                    m.name as motel_name
                                FROM
                                    analysis a
                                    INNER JOIN session s ON s.id = a.session_id
                                    INNER JOIN motel m ON m.id = s.motel_id
                                """)
    
    return result
    

