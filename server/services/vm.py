import json
import logging

from core.config import database_config
from core.db import create_pool
from models import HDSchemaCreate, VMSchemaCreate, VMSchemaUpdate
from outputs import pretty_vm_output
from repository import HDRepository, VMRepository


async def add_vm(vm_data: str) -> int:
    """Add vm to database."""
    vm_data = json.loads(vm_data)

    pool = await create_pool(database_config.database_url)
    async with pool as session:
        ram_amount = vm_data["ram_amount"]
        cpu_amount = vm_data["cpu_amount"]

        vm_repo = VMRepository(session)
        hd_repo = HDRepository(session)
        create_schema = VMSchemaCreate(
            ram_amount=ram_amount,
            cpu_amount=cpu_amount,
        )
        vm_obj = await vm_repo.create(create_schema)

        for hd in vm_data["hd"]:
            rom_amount = hd["rom_amount"]
            hd_create_schema = HDSchemaCreate(
                vm_id=vm_obj.id, rom_amount=rom_amount
            )
            await hd_repo.create(hd_create_schema)
        logging.info(f"ВМ добавлена в бд id {vm_obj.id}")
        return vm_obj.id


async def auth_vm(vm_id: int):
    """Autentificate vm to database."""
    pool = await create_pool(database_config.database_url)
    async with pool as session:
        vm_repo = VMRepository(session)
        vm_obj = await vm_repo.get(vm_id)
        vm_update = VMSchemaUpdate(is_auth=True)
        vm_obj = await vm_repo.update(vm_obj, vm_update)
    logging.info(f"ВМ id {vm_obj.id} залогинена.")


async def logout_vm(vm_id: int):
    """Logout vm into database."""
    pool = await create_pool(database_config.database_url)
    async with pool as session:
        vm_repo = VMRepository(session)
        vm_obj = await vm_repo.get(vm_id)
        vm_update = VMSchemaUpdate(is_auth=False)
        vm_obj = await vm_repo.update(vm_obj, vm_update)
    logging.info(f"ВМ id {vm_obj.id} вышла из системы.")


async def offline_vm(vm_id: int):
    """Vm has offline into db."""
    pool = await create_pool(database_config.database_url)
    async with pool as session:
        vm_repo = VMRepository(session)
        vm_obj = await vm_repo.get(vm_id)
        vm_update = VMSchemaUpdate(is_auth=False, is_online=False)
        vm_obj = await vm_repo.update(vm_obj, vm_update)
    logging.info(f"ВМ id {vm_obj.id} Оффлайн.")


async def get_vm():
    """Get all vm in db."""
    pool = await create_pool(database_config.database_url)
    async with pool as session:
        repo = VMRepository(session)
        vm_objs = await repo.get_multi()
        pretty_vm_output(vm_objs)


async def get_online_vm():
    """Get online vm in db."""
    pool = await create_pool(database_config.database_url)
    async with pool as session:
        repo = VMRepository(session)
        vm_objs = await repo.get_obj_for_field_arg("is_online", True, True)
        pretty_vm_output(vm_objs)


async def get_auth_vm():
    """Get auth vm in db."""
    pool = await create_pool(database_config.database_url)
    async with pool as session:
        repo = VMRepository(session)
        vm_objs = await repo.get_obj_for_field_arg("is_auth", True, True)
        pretty_vm_output(vm_objs)


async def update_auth_vm(vm_id: int, vm_data: str):
    """Update vm."""
    vm_data = json.loads(vm_data)

    pool = await create_pool(database_config.database_url)
    async with pool as session:
        ram_amount = vm_data["ram_amount"]
        cpu_amount = vm_data["cpu_amount"]

        vm_repo = VMRepository(session)
        hd_repo = HDRepository(session)

        vm_obj = await vm_repo.get(vm_id)
        for hd in vm_obj.hard_drives:
            await hd_repo.remove(hd)

        update_schema = VMSchemaUpdate(
            ram_amount=ram_amount,
            cpu_amount=cpu_amount,
        )
        vm_obj = await vm_repo.update(vm_obj, update_schema)

        for hd in vm_data["hd"]:
            rom_amount = hd["rom_amount"]
            hd_create_schema = HDSchemaCreate(
                vm_id=vm_obj.id, rom_amount=rom_amount
            )
            await hd_repo.create(hd_create_schema)
            logging.info(f"VM id {vm_obj.id} update")
        return vm_obj.id
