APPLICATION_MAPPERS_TEMPLATE = """
\"\"\"
Mappers for converting between application schemas (Pydantic) and domain DTOs.

This layer handles the conversion between external (API) representations
and internal (domain) representations.
\"\"\"

from src.{{ model_snake_case }}.application.schemas import (
    Create{{ model_pascal_case }}Request,
    Update{{ model_pascal_case }}Request,
    FilterParams,
)
from src.{{ model_snake_case }}.domain.dtos import (
    Create{{ model_pascal_case }}DTO,
    Update{{ model_pascal_case }}DTO,
    {{ model_pascal_case }}FilterDTO,
)


class {{ model_pascal_case }}Mapper:
    \"\"\"Mapper for {{ model_pascal_case }} conversions between layers.\"\"\"

    @staticmethod
    def to_create_dto(request: Create{{ model_pascal_case }}Request) -> Create{{ model_pascal_case }}DTO:
        \"\"\"
        Convert a Create request schema to a domain DTO.

        Args:
            request: Pydantic schema from API

        Returns:
            Domain DTO
        \"\"\"
        data = request.model_dump()
        return Create{{ model_pascal_case }}DTO(**data)

    @staticmethod
    def to_update_dto(request: Update{{ model_pascal_case }}Request) -> Update{{ model_pascal_case }}DTO:
        \"\"\"
        Convert an Update request schema to a domain DTO.

        Args:
            request: Pydantic schema from API

        Returns:
            Domain DTO
        \"\"\"
        data = request.model_dump(exclude_none=True)
        return Update{{ model_pascal_case }}DTO(**data)

    @staticmethod
    def to_filter_dto(params: FilterParams) -> {{ model_pascal_case }}FilterDTO:
        \"\"\"
        Convert filter parameters to a domain DTO.

        Args:
            params: Pydantic schema from API

        Returns:
            Domain DTO
        \"\"\"
        return {{ model_pascal_case }}FilterDTO(
            skip=params.skip,
            limit=params.limit,
            order_by=params.order_by,
            search=params.search,
            # TODO: Map additional filters
        )
"""
