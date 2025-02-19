import asyncpg
from asyncpg import Pool


async def create_pool(database_url: str) -> Pool:
    """Make connect to database."""
    return await asyncpg.create_pool(dsn=database_url)
