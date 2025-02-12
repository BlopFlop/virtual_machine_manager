from asyncpg import Pool
import asyncpg


async def create_pool(database_url: str) -> Pool:
    return await asyncpg.create_pool(dsn=database_url)
