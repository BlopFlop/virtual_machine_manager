from typing import List, Optional

from pydantic import BaseModel, Field, PositiveInt


class HDSchemaCreate(BaseModel):
    """Hard drives create schema."""

    vm_id: Optional[int] = Field(
        None, title="Virtual machine Id", description="Id виртуальной машины."
    )
    rom_amount: PositiveInt = Field(
        ..., title="ROM amount", description="Количество памяти у HD."
    )


class HDSchemaUpdate(BaseModel):
    """Hard drives update schema."""

    vm_id: Optional[int] = Field(
        ..., title="Virtual machine Id", description="Id виртуальной машины."
    )
    rom_amount: Optional[PositiveInt] = Field(
        ..., title="ROM amount", description="Количество памяти у HD."
    )


class HDSchemaDB(HDSchemaCreate):
    """Hard drives database schema."""

    id: int = Field(..., title="Id", description="Id в базе данных.")


class VMSchemaCreate(BaseModel):
    """Virtual Machine create schema."""

    ram_amount: PositiveInt = Field(
        ...,
        title="RAM amount",
        description="Количетво оперативной памяти у VM.",
    )
    cpu_amount: PositiveInt = Field(
        ..., title="CPU amount", description="Количество выделеных CPU."
    )
    is_online: bool = Field(
        True, title="Is online", description="Флаг подключения."
    )
    is_auth: bool = Field(
        True, title="Is auth", description="Флаг аунтефикации подключения."
    )


class VMSchemaUpdate(BaseModel):
    """Virtual Machine update schema."""

    ram_amount: Optional[PositiveInt] = Field(
        None,
        title="RAM amount",
        description="Количетво оперативной памяти у VM.",
    )
    cpu_amount: Optional[PositiveInt] = Field(
        None, title="CPU amount", description="Количество выделеных CPU."
    )
    is_online: Optional[bool] = Field(
        None, title="Is online", description="Флаг подключения."
    )
    is_auth: Optional[bool] = Field(
        None, title="Is auth", description="Флаг аунтефикации подключения."
    )


class VMSchemaDB(VMSchemaCreate):
    """Virtual Machine database schema."""

    id: int = Field(..., title="Id", description="Id в базе данных.")
    hard_drives: List[HDSchemaDB] = []
