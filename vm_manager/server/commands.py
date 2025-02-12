from asyncpg import Pool
from asyncpg.connection import Connection

from server.repository import VirtualMachineRepository, VirtualMachineSchemaCreate
from server.utils import generate_token


async def create_virtual_machine(
    pool: Pool, ram_amount: int, cpu_amount: int, auth_token: str
) -> str:
    async with pool.acquire() as connection:
        create_schema = VirtualMachineSchemaCreate(ram_amount, cpu_amount, generate_token())
        repo = VirtualMachineRepository(connection)
        db_schema = await repo.create(create_schema)
        return db_schema


async def authenticate_vm(pool: Pool, auth_token: str):
    async with pool.acquire() as connection:
        connection: Connection
        return await connection.fetchrow(
            "SELECT * FROM virtual_machines WHERE auth_token = $1", auth_token
        )