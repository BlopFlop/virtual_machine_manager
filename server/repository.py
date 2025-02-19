from typing import Any

from asyncpg.connection import Connection
from core.repository import AbstractRepository
from models import (
    HDSchemaCreate,
    HDSchemaDB,
    HDSchemaUpdate,
    VMSchemaCreate,
    VMSchemaDB,
    VMSchemaUpdate,
)
from queries import (
    CREATE_HD,
    CREATE_VM,
    DELETE_HD,
    DELETE_VM,
    GET_ALL_HD,
    GET_ALL_VM,
    GET_HD_FOR_KEY,
    GET_VM_FOR_KEY,
    SET_NULL_HD_VM_ID,
    UPDATE_HD,
    UPDATE_VM,
)


class HDRepository(AbstractRepository):
    def __init__(self, session: Connection):
        self.session = session

    async def get(self, obj_id: int):
        """Get obj for id."""
        return await self.get_obj_for_field_arg("id", obj_id, False)

    async def get_multi(self) -> list[HDSchemaDB]:
        """Get all obj in db."""
        hd_objs = await self.session.fetch(GET_ALL_HD)
        if not hd_objs:
            return []
        return [HDSchemaDB(**hd_obj) for hd_obj in hd_objs]

    async def create(self, create_schema: HDSchemaCreate) -> HDSchemaDB:
        """Create obj in db."""
        hd_obj = await self.session.fetchrow(
            CREATE_HD, create_schema.vm_id, create_schema.rom_amount
        )
        return HDSchemaDB(**hd_obj)

    async def update(
        self, db_obj: HDSchemaDB, update_schema: HDSchemaUpdate
    ) -> HDSchemaDB:
        """Update obj in db."""
        db_data = db_obj.model_dump()
        update_data = update_schema.model_dump(exclude_unset=True)
        for field in db_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        await self.session.execute(
            UPDATE_HD, db_obj.vm_id, db_obj.rom_amount, db_obj.id
        )
        return db_obj

    async def remove(self, db_obj: HDSchemaDB) -> HDSchemaDB:
        """Delete boj in db."""
        await self.session.execute(DELETE_HD, db_obj.id)
        return db_obj

    async def get_obj_for_field_arg(
        self, field: str, arg: Any, many: bool = False
    ) -> HDSchemaDB | list[HDSchemaDB]:
        """Get obj or objs for field arguments."""
        items = await self.session.fetch(GET_HD_FOR_KEY.format(field), arg)
        if not items:
            return None
        if many:
            return [HDSchemaDB(**item) for item in items]
        return HDSchemaDB(**items[0])


class VMRepository(AbstractRepository):

    def __init__(self, session: Connection):
        self.session = session

    async def __get_hd_for_vm_id(self, vm_id: int) -> list[HDSchemaDB]:
        hd_repo = HDRepository(self.session)
        hd_objs = await hd_repo.get_obj_for_field_arg("vm_id", vm_id, True)
        return hd_objs if hd_objs else []

    async def __create_vm_schema(self, vm_object: dict[str:Any]):
        hard_dirves = await self.__get_hd_for_vm_id(vm_object["id"])
        vm_object = dict(vm_object)
        return VMSchemaDB(**vm_object, hard_drives=hard_dirves)

    async def get(self, obj_id: int) -> VMSchemaDB:
        """Get obj for id."""
        return await self.get_obj_for_field_arg("id", obj_id, False)

    async def get_multi(self) -> list[VMSchemaDB]:
        """Get all obj in db."""
        vm_objects = await self.session.fetch(GET_ALL_VM)

        if not vm_objects:
            return []

        return [
            await self.__create_vm_schema(vm_object)
            for vm_object in vm_objects
        ]

    async def create(self, create_schema: VMSchemaCreate):
        """Create obj in db."""
        vm_obj = await self.session.fetchrow(
            CREATE_VM,
            create_schema.ram_amount,
            create_schema.cpu_amount,
        )
        return await self.__create_vm_schema(vm_obj)

    async def update(
        self,
        db_obj: VMSchemaDB,
        update_schema: VMSchemaUpdate,
    ) -> VMSchemaDB:
        """Update obj in db."""
        db_data = db_obj.model_dump()
        update_data = update_schema.model_dump(exclude_unset=True)
        for field in db_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        await self.session.execute(
            UPDATE_VM,
            db_obj.ram_amount,
            db_obj.cpu_amount,
            db_obj.is_online,
            db_obj.is_auth,
            db_obj.id,
        )
        return db_obj

    async def remove(self, db_obj: VMSchemaDB) -> VMSchemaDB:
        """Delete boj in db."""
        await self.session.fetch(SET_NULL_HD_VM_ID, db_obj.id)
        await self.session.execute(DELETE_VM, db_obj.id)
        return db_obj

    async def get_obj_for_field_arg(
        self, field: str, arg: Any, many: bool = False
    ) -> VMSchemaDB | list[VMSchemaDB]:
        """Get obj or objs for field arguments."""
        vm_objects = await self.session.fetch(
            GET_VM_FOR_KEY.format(field), arg
        )
        if not vm_objects:
            if many:
                return []
            return None

        if not many:
            return await self.__create_vm_schema(vm_objects[0])
        return [
            await self.__create_vm_schema(vm_object)
            for vm_object in vm_objects
        ]
