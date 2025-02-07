from prisma import Prisma

def get_database_client():
    """
    Returns a Prisma Client
    
    :return: a prisma client
    """
    return Prisma()