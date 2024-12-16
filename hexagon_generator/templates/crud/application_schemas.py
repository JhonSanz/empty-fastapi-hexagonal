APPLICATION_SCHEMAS_TEMPLATE = """
from pydantic import BaseModel


class {{ model_pascal_case }}InDBBase(BaseModel):
    # TODO:
    pass


class Create{{ model_pascal_case }}Request(BaseModel):
    # TODO:
    pass

    
class Update{{ model_pascal_case }}Request(BaseModel):
    # TODO:
    pass


class FilterParams(BaseModel):
    skip: int = 0
    limit: int = 10

"""