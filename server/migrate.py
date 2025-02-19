import asyncio
from pathlib import Path

import asyncpg
from core.config import database_config
from core.constants import MG_SCRIPT


async def run_migration(sql_script_file: Path):
    """Run migration script."""
    conn = await asyncpg.connect(
        user=database_config.user,
        password=database_config.password,
        database=database_config.db,
        host=database_config.host,
        port=database_config.port,
    )

    with open(sql_script_file, "r") as f:
        sql_script = f.read()

    try:
        await conn.execute(sql_script)
        print("Миграция успешно выполнена!")
    except Exception as e:
        print(f"Ошибка при выполнении миграции: {e}")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(run_migration(MG_SCRIPT))
