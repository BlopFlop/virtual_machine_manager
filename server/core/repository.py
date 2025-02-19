from abc import ABC, abstractmethod
from typing import Any


class AbstractRepository(ABC):
    """Abstract CRUD operation."""

    @abstractmethod
    async def get(self, obj_id: int):
        """Get obj for id."""
        raise NotImplementedError

    @abstractmethod
    async def get_multi(self):
        """Get all obj in db."""
        raise NotImplementedError

    @abstractmethod
    async def create(self, create_schema):
        """Create obj in db."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, obj_id: int, update_schema):
        """Update obj in db."""
        raise NotImplementedError

    @abstractmethod
    async def remove(self, obj_id: int):
        """Delete boj in db."""
        raise NotImplementedError

    @abstractmethod
    async def get_obj_for_field_arg(self, field: str, arg: Any, many: bool):
        """Get obj or objs for field arguments."""
        raise NotImplementedError
