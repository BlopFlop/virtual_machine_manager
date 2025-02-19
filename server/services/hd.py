from core.config import database_config
from core.db import create_pool
from outputs import pretty_hd_output
from repository import HDRepository


async def get_hd():
    """Get all hd from database."""
    pool = await create_pool(database_config.database_url)
    async with pool as session:
        repo = HDRepository(session)
        hd_objs = await repo.get_multi()
        pretty_hd_output(hd_objs)
