APPLICATION_SERVICE_TEMPLATE = """
from src.{{ model_snake_case }}.application.interfaces import {{ model_pascal_case }}ServiceInterface

class {{ model_pascal_case }}Service({{ model_pascal_case }}ServiceInterface):
    # TODO:
    def my_method(self, *, my_param: None) -> None: ...
"""
