from queries.hard_drive import (
    CREATE_HD,
    DELETE_HD,
    GET_ALL_HD,
    GET_ALL_HD_FOR_VM,
    GET_HD_FOR_KEY,
    SET_NULL_HD_VM_ID,
    UPDATE_HD,
)
from queries.virtual_machine import (
    CREATE_VM,
    DELETE_VM,
    GET_ALL_VM,
    GET_VM_FOR_KEY,
    UPDATE_VM,
)

__all__ = (
    "CREATE_HD",
    "UPDATE_HD",
    "DELETE_HD",
    "GET_ALL_HD",
    "GET_ALL_HD_FOR_VM",
    "GET_HD_FOR_KEY",
    "SET_NULL_HD_VM_ID",
    "CREATE_VM",
    "UPDATE_VM",
    "DELETE_VM",
    "GET_VM_FOR_KEY",
    "GET_ALL_VM",
)
