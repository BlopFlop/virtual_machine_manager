import asyncpg
import pytest
from core.config import test_database_config


@pytest.fixture
@pytest.mark.asyncio
async def db_connection():
    conn = await asyncpg.connect(
        user=test_database_config.user,
        password=test_database_config.password,
        database=test_database_config.db,
        host=test_database_config.host,
        port=test_database_config.port,
    )
    yield conn
    conn.close()
