from typing import Optional, List

from pydantic import BaseModel, Field, PositiveInt


class HardDriveSchemaCreate(BaseModel):
    vm_id: Optional[int] = Field(
        None, title="Virtual machine Id", description="Id виртуальной машины."
    )
    rom_amount: PositiveInt = Field(
        ..., title="ROM amount", description="Количество памяти у HD."
    )


class HardDriveSchemaUpdate(BaseModel):
    vm_id: Optional[int] = Field(
        ..., title="Virtual machine Id", description="Id виртуальной машины."
    )
    rom_amount: Optional[PositiveInt] = Field(
        ..., title="ROM amount", description="Количество памяти у HD."
    )


class HardDriveSchemaDB(HardDriveSchemaCreate):
    id: int = Field(..., title="Id", description="Id в базе данных.")


class VirtualMachineSchemaCreate(BaseModel):
    ram_amount: PositiveInt = Field(
        ..., title="RAM amount", description="Количетво оперативной памяти у VM."
    )
    cpu_amount: PositiveInt = Field(
        ..., title="CPU amount", description="Количество выделеных CPU."
    )
    token: str = Field(..., title="Auth token", description="Токен авторизации.")
    is_online: bool = Field(False, title="Is online", description="Флаг подключения.")


class VirtualMachineSchemaUpdate(BaseModel):
    ram_amount: Optional[PositiveInt] = Field(
        None, title="RAM amount", description="Количетво оперативной памяти у VM."
    )
    cpu_amount: Optional[PositiveInt] = Field(
        None, title="CPU amount", description="Количество выделеных CPU."
    )
    token: Optional[str] = Field(
        None, title="Auth token", description="Токен авторизации."
    )
    is_online: Optional[bool] = Field(
        None, title="Is online", description="Флаг подключения."
    )


class VirtualMachineSchemaDB(VirtualMachineSchemaCreate):
    id: int = Field(..., title="Id", description="Id в базе данных.")
    hard_drives: List[HardDriveSchemaDB] = []
