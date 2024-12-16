from .application_handlers import (
    APPLICATION_HANDLERS_TEMPLATE,
)
from .application_schemas import APPLICATION_SCHEMAS_TEMPLATE
from .application_service import APPLICATION_SERVICE_TEMPLATE
from .domain_exceptions import DOMAIN_EXCEPTIONS_TEMPLATE
from .domain_repository import DOMAIN_REPOSITORY_TEMPLATE
from .infrastructure_database import (
    INFRASTRUCTURE_DATABASE_TEMPLATE,
)
from .infrastructure_web import INFRASTRUCTURE_WEB_TEMPLATE
from .dependencies_get_user import DEPENDENCIES_GET_USER_TEMPLATE

routes = [
    ("infrastructure/web.py", INFRASTRUCTURE_WEB_TEMPLATE),
    (
        "infrastructure/database.py",
        INFRASTRUCTURE_DATABASE_TEMPLATE,
    ),
    ("domain/exceptions.py", DOMAIN_EXCEPTIONS_TEMPLATE),
    ("domain/repository.py", DOMAIN_REPOSITORY_TEMPLATE),
    ("application/service.py", APPLICATION_SERVICE_TEMPLATE),
    ("application/schemas.py", APPLICATION_SCHEMAS_TEMPLATE),
    ("application/handlers.py", APPLICATION_HANDLERS_TEMPLATE),
    ("dependencies/get_user_with_permissions.py", DEPENDENCIES_GET_USER_TEMPLATE),
]

dirs = [
    "",
    "dependencies",
    "application",
    "domain",
    "infrastructure",
    "application/use_cases",
]
