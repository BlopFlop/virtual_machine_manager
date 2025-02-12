from typing import Any
from abc import ABC, abstractmethod

from asyncpg import Pool
from asyncpg.connection import Connection


from schemas import (
    VirtualMachineSchemaCreate,
    VirtualMachineSchemaUpdate,
    VirtualMachineSchemaDB,
    HardDriveSchemaDB,
    HardDriveSchemaUpdate,
    HardDriveSchemaCreate,
)
from server.schedules import (
    GET_VM_FOR_KEY,
    GET_ALL_VM,
    CREATE_VM,
    UPDATE_VM,
    DELETE_VM,

    GET_HD_FOR_KEY,
    GET_ALL_HD,
    CREATE_HD,
    UPDATE_HD,
    DELETE_HD,
)


class ReposiotryBase(ABC):

    @abstractmethod
    async def get(self, obj_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_multi(self):
        raise NotImplementedError

    @abstractmethod
    async def create(self, create_schema):
        raise NotImplementedError

    @abstractmethod
    async def update(self, obj_id: int, update_schema):
        raise NotImplementedError

    @abstractmethod
    async def remove(self, obj_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_obj_for_field_arg(self, field: str, arg: Any, many: bool):
        raise NotImplementedError


class HDRepository(ReposiotryBase):
    def __init__(self, session: Connection):
        self.session = session

    async def get(self, obj_id: int):
        return await self.get_obj_for_field_arg("id", obj_id, False)

    async def get_multi(self) -> list[HardDriveSchemaDB]:
        hd_objs = await self.session.fetch(GET_ALL_HD)
        if not hd_objs:
            return None
        return [HardDriveSchemaDB(**hd_obj) for hd_obj in hd_objs]

    async def create(
        self,
        create_schema: HardDriveSchemaCreate
    ) -> HardDriveSchemaDB:
        hd_obj = await self.session.fetchrow(
            CREATE_HD, create_schema.vm_id, create_schema.rom_amount
        )
        return HardDriveSchemaDB(**hd_obj)

    async def update(
        self,
        db_obj: HardDriveSchemaDB,
        update_schema: HardDriveSchemaUpdate
    ) -> HardDriveSchemaDB:
        db_data = db_obj.model_dump()
        update_data = update_schema.model_dump(exclude_unset=True)
        for field in db_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        await self.session.execute(
            UPDATE_HD, db_obj.vm_id, db_obj.rom_amount, db_obj.id
        )
        return db_obj

    async def remove(
        self,
        db_obj: HardDriveSchemaDB
    ) -> HardDriveSchemaDB:
        await self.session.execute(DELETE_HD, db_obj.id)
        return db_obj

    async def get_obj_for_field_arg(
        self, field: str, arg: Any, many: bool = False
    ) -> HardDriveSchemaDB | list[HardDriveSchemaDB]:
        items = await self.session.fetch(GET_HD_FOR_KEY, field, arg)
        if not items:
            return None
        if many:
            return [HardDriveSchemaDB(**item) for item in items]
        return HardDriveSchemaDB(**items[0])


class VirtualMachineRepository(ReposiotryBase):

    def __init__(self, session: Connection):
        self.session = session

    async def __create_vm_schema(self, vm_object: dict[str: Any]):
        hd_repo = HDRepository(self.session)
        hard_dirves = await hd_repo.get_obj_for_field_arg(
            HardDriveSchemaDB.vm_id.__name__,
            vm_object["id"],
            True
        )
        hard_dirves = hard_dirves if hard_dirves else []
        return VirtualMachineSchemaDB(**vm_object, hard_drives=hard_dirves)

    async def get(self, obj_id: int) -> VirtualMachineSchemaDB:
        return await self.get_obj_for_field_arg("id", obj_id, False)

    async def get_multi(self) -> list[VirtualMachineSchemaDB]:
        vm_objects = await self.session.fetch(GET_ALL_VM)

        if not vm_objects:
            return None

        return [self.__create_vm_schema(vm_object) for vm_object in vm_objects]

    async def create(self, create_schema: VirtualMachineSchemaCreate):
        vm_obj = await self.session.fetchrow(
            CREATE_VM,
            create_schema.ram_amount,
            create_schema.cpu_amount,
            create_schema.token
        )
        return await self.__create_vm_schema(vm_obj)

    async def update(
        self,
        db_obj: VirtualMachineSchemaDB,
        update_schema: VirtualMachineSchemaUpdate
    ) -> VirtualMachineSchemaDB:
        db_data = db_obj.model_dump()
        update_data = update_schema.model_dump(exclude_unset=True)
        for field in db_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        await self.session.execute(
            UPDATE_VM, db_obj.ram_amount, db_obj.cpu_amount, db_obj.token, db_obj.id
        )
        return db_obj

    async def remove(
        self,
        db_obj: VirtualMachineSchemaDB
    ) -> VirtualMachineSchemaDB:
        await self.session.execute(DELETE_VM, db_obj.id)
        return db_obj

    async def get_obj_for_field_arg(
        self,
        field: str,
        arg: Any,
        many: bool = False
    ) -> VirtualMachineSchemaDB | list[VirtualMachineSchemaDB]:
        vm_objects = await self.session.fetch(GET_VM_FOR_KEY, field, arg)
        if not vm_objects:
            return None

        if many:
            return [self.__create_vm_schema(vm_object) for vm_object in vm_objects]
        return self.__create_vm_schema(vm_objects[0])
