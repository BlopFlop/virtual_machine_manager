import asyncio
import asyncpg

from config import database_config


async def run_migration():
    conn = await asyncpg.connect(
        user=database_config.user,
        password=database_config.password,
        database=database_config.db,
        host=database_config.host,
        port=database_config.port
    )

    with open("migrations/init.sql", "r") as f:
        sql_script = f.read()

    try:
        await conn.execute(sql_script)
        print("Миграция успешно выполнена!")
    except Exception as e:
        print(f"Ошибка при выполнении миграции: {e}")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(run_migration())
