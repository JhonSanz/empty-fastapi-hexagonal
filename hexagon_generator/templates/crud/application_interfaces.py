APPLICATION_INTERFACES_TEMPLATE = """
from abc import ABC, abstractmethod


class {{ model_pascal_case }}ServiceInterface(ABC):
    @abstractmethod
    def my_method(self, my_param: None) -> None: ...
"""
