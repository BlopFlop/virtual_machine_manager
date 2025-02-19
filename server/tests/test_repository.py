from uuid import uuid4

import pytest
from core.config import database_config
from core.db import create_pool
from fixtures.hard_drivers import (
    correct_data1_hd,
    correct_data2_hd,
    correct_data3_hd,
)
from fixtures.virtual_machines import (
    correct_data1,
    correct_data2,
    correct_data3,
)
from models import (
    HDSchemaCreate,
    HDSchemaUpdate,
    VMSchemaCreate,
    VMSchemaDB,
    VMSchemaUpdate,
)
from repository import HDRepository, VMRepository


@pytest.mark.parametrize("data", (correct_data1, correct_data2, correct_data3))
@pytest.mark.asyncio
async def test_create_vm(db_connection, data: dict):
    repo = VMRepository(db_connection)
    schema_create = VMSchemaCreate(**data)
    vm_ojb = await repo.create(schema_create)

    assert vm_ojb, "Создание виртуальной машины не создало объект в бд."


@pytest.mark.asyncio
async def test_get_vm(db_connection):
    repo = VMRepository(db_connection)
    vm_ojb = await repo.get_multi()

    assert (
        len(vm_ojb) > 0
    ), "При получении объектов из бд должно вернуться несколько объектов."


@pytest.mark.asyncio
async def test_get_vm_for_id(db_connection):
    repo = VMRepository(db_connection)
    vm_ojbs = await repo.get_multi()

    for obj in vm_ojbs:
        obj_get = await repo.get(obj.id)
        assert (
            obj_get
        ), "При получении объектов из бд по id должен вернуться объект"
        assert obj_get.id == obj.id, (
            "Id полученного объекта должен быть равен id по которому он "
            "полчался"
        )


@pytest.mark.asyncio
async def test_update_vm_for_id(db_connection):
    repo = VMRepository(db_connection)
    vm_ojbs = await repo.get_multi()

    for obj in vm_ojbs:
        update_schema = VMSchemaUpdate(
            ram_amount=100,
            cpu_amount=1,
            token=str(uuid4()),
            is_online=True,
            is_auth=False,
        )
        obj_update = await repo.update(obj, update_schema)
        obj_update = await repo.get(obj_update.id)
        obj_update = obj_update.model_dump()
        obj_update.pop("id")
        obj_update.pop("hard_drives")
        assert (
            obj_update == update_schema.model_dump()
        ), "При получении объектов из бд по id должен вернуться объект"


@pytest.mark.parametrize(
    "data", (correct_data1_hd, correct_data2_hd, correct_data3_hd)
)
@pytest.mark.asyncio
async def test_create_hd(db_connection, data: dict):
    repo = HDRepository(db_connection)
    schema_create = HDSchemaCreate(**data)
    vm_ojb = await repo.create(schema_create)

    assert vm_ojb, "Создание жесткого диска не создало объект в бд."


@pytest.mark.asyncio
async def test_get_hd(db_connection):
    repo = HDRepository(db_connection)
    hd_ojb = await repo.get_multi()

    assert (
        len(hd_ojb) > 0
    ), "При получении объектов из бд должно вернуться несколько объектов."


@pytest.mark.asyncio
async def test_get_hd_for_id(db_connection):
    repo = HDRepository(db_connection)
    hd_obj = await repo.get_multi()

    for obj in hd_obj:
        obj_get = await repo.get(obj.id)
        assert (
            obj_get
        ), "При получении объектов из бд по id должен вернуться объект"
        assert obj_get.id == obj.id, (
            "Id полученного объекта должен быть равен id по которому он "
            "полчался"
        )


@pytest.mark.asyncio
async def test_update_hd_for_id(db_connection):
    repo = VMRepository(db_connection)
    vm_obj = await repo.get_multi()
    vm_obj = vm_obj[0]

    repo = HDRepository(db_connection)
    hd_ojbs = await repo.get_multi()

    for obj in hd_ojbs:
        update_schema = HDSchemaUpdate(rom_amount=100, vm_id=vm_obj.id)
        obj_update = await repo.update(obj, update_schema)
        obj_update = obj_update.model_dump()
        obj_update.pop("id")
        assert (
            obj_update == update_schema.model_dump()
        ), "При получении объектов из бд по id должен вернуться объект"

    repo = VMRepository(db_connection)
    vm_obj: VMSchemaDB = await repo.get(vm_obj.id)

    assert len(vm_obj.hard_drives) > 0, (
        "После добавления объектов в бд у виртуальной машины должны"
        "отобразится жесткие диски"
    )


@pytest.mark.asyncio
async def test_delete_vm_for_id(db_connection):
    repo = VMRepository(db_connection)
    vm_ojbs = await repo.get_multi()

    for obj in vm_ojbs:
        await repo.remove(obj)
        delete_obj = await repo.get(obj.id)
        assert (
            delete_obj is None
        ), "При получении объектов из бд по id должен вернуться объект"

    repo = HDRepository(db_connection)
    hd_objs = await repo.get_multi()

    for hd_obj in hd_objs:
        assert (
            hd_obj.vm_id is None
        ), "После удаления виртуальной машины у ее жд должны удалится айди"


@pytest.mark.asyncio
async def test_delete_hd_for_id(db_connection):
    repo = HDRepository(db_connection)
    hd_ojbs = await repo.get_multi()

    for obj in hd_ojbs:
        await repo.remove(obj)
        delete_obj = await repo.get(obj.id)
        assert delete_obj is None, (
            "При получении удаленных объектов из бд по id не должно "
            "возвращаться объектов."
        )
