from pydantic import BaseModel


class BaseModelWithNoneCheck(BaseModel):
    def is_empty(self) -> bool:
        return all(value is None for value in self.model_dump().values())
