from database import get_database_client

async def get_session_db():
    """
    Dependency that manages the Prisma database connection.

    This function ensures that the database is connected before yielding the Prisma instance.
    After usage, it disconnects the database to prevent connection leaks.

    :return: Prisma database instance
    """
    db = get_database_client()
    
    if not db.is_connected():
        await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()