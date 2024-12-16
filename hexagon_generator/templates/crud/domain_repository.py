DOMAIN_REPOSITORY_TEMPLATE = """
from abc import ABC, abstractmethod
from src.{{ model_snake_case }}.domain.models import {{ model_pascal_case }}


class {{ model_pascal_case }}Repository(ABC):
    @abstractmethod
    async def get_by_id(self, *, id: int) -> {{ model_pascal_case }}: ...

    @abstractmethod
    async def get(self, *, id: int, filter_params) -> tuple[list[{{ model_pascal_case }}], int]: ...

    @abstractmethod
    async def create(self, *, data): ...

    @abstractmethod
    async def update(self, *, id: int, data): ...

    @abstractmethod
    async def delete(self, *, id: int): ...
"""