from .application_schemas import APPLICATION_SCHEMAS_TEMPLATE
from .application_web_cases import (
    APPLICATION_WEB_CASE_TEMPLATE,
    APPLICATION_WEB_CASE_TEMPLATE_INIT,
)
from .domain_entities import DOMAIN_ENTITIES_TEMPLATE
from .domain_exceptions import DOMAIN_EXCEPTIONS_TEMPLATE
from .domain_repository import DOMAIN_REPOSITORY_TEMPLATE
from .domain_unit_of_work import DOMAIN_UNIT_OF_WORK_TEMPLATE
from .infrastructure_database import (
    INFRASTRUCTURE_DATABASE_TEMPLATE,
)
from .infrastructure_exception_handlers import (
    INFRASTRUCTURE_EXCEPTION_HANDLERS_TEMPLATE,
)
from .infrastructure_models import INFRASTRUCTURE_MODELS_TEMPLATE
from .infrastructure_unit_of_work import INFRASTRUCTURE_UNIT_OF_WORK_TEMPLATE
from .infrastructure_web import INFRASTRUCTURE_WEB_TEMPLATE


routes = [
    ("infrastructure/web.py", INFRASTRUCTURE_WEB_TEMPLATE),
    ("infrastructure/database.py", INFRASTRUCTURE_DATABASE_TEMPLATE),
    ("infrastructure/models.py", INFRASTRUCTURE_MODELS_TEMPLATE),
    ("infrastructure/unit_of_work.py", INFRASTRUCTURE_UNIT_OF_WORK_TEMPLATE),
    ("infrastructure/exception_handlers.py", INFRASTRUCTURE_EXCEPTION_HANDLERS_TEMPLATE),
    ("domain/entities.py", DOMAIN_ENTITIES_TEMPLATE),
    ("domain/exceptions.py", DOMAIN_EXCEPTIONS_TEMPLATE),
    ("domain/repository.py", DOMAIN_REPOSITORY_TEMPLATE),
    ("domain/unit_of_work.py", DOMAIN_UNIT_OF_WORK_TEMPLATE),
    ("application/schemas.py", APPLICATION_SCHEMAS_TEMPLATE),
]

dirs = [
    "",
    "application",
    "domain",
    "infrastructure",
    "application/use_cases",
]
