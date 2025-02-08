from prisma.actions import sessionActions
from prisma.models import session, analysis
from prisma import Prisma

def get_session_repository(db: Prisma) -> sessionActions[session]:
    """
    Retrieves the session repository for interacting with the session data in the database.

    This function returns the repository for performing CRUD operations on session entities.
    
    :param db: The Prisma database connection instance.
    :return: The session repository to interact with session data.
    """
    return db.session

def get_analysis_repository(db: Prisma) -> sessionActions[analysis]:
    """
    Retrieves the analysis repository for interacting with the analysis data in the database.

    This function returns the repository for performing CRUD operations on analysis entities.
    
    :param db: The Prisma database connection instance.
    :return: The analysis repository to interact with analysis data.
    """
    return db.analysis
