from prisma.models import session
import asyncio
import logging
from prisma import Prisma

from ia.schema import CreateAnalysisSchema
from helpers.format_message import format_messages
from ia.ia import ainvoke
from repositories import get_analysis_repository, get_session_repository
from dependencies import get_session_db

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def process_session(session: session):
    """
    Processes a single session and returns the analysis result.

    This function takes a session, formats the messages, and invokes the AI model 
    to analyze the conversation. If successful, it returns the analysis as an instance 
    of CreateAnalysisSchema.

    :param session: The session object containing messages to be analyzed.
    :return: A CreateAnalysisSchema instance containing the session analysis, or None if there is an error.
    """
    try:
        messages = session.message

        # Format messages
        formatted_messages = format_messages(messages=messages)
        formatted_messages = '\n'.join(formatted_messages)

        # Asynchronous call to AI/Model/API
        response = await ainvoke(input=formatted_messages)

        logging.info(response)
        
        return CreateAnalysisSchema.from_analyse(
            session_id=session.id,
            analyse=response
        )
    except Exception as e:
        logging.error(f"Error processing session {session.id}: {e}")
        return None  # Return None for sessions with errors

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

def run_analysis_job():
    """
    Runs the chatbot analysis cron job.

    This function invokes the cron job to analyze the chatbot sessions by calling the
    `analysis_chatbot_cron_job` function in an asynchronous manner.

    :return: None
    """
    asyncio.run(analysis_chatbot_cron_job())