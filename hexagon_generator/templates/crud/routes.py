from .application_handlers import (
    APPLICATION_HANDLERS_TEMPLATE,
)
from .application_interfaces import (
    APPLICATION_INTERFACES_TEMPLATE,
)
from .application_schemas import APPLICATION_SCHEMAS_TEMPLATE
from .application_service import APPLICATION_SERVICE_TEMPLATE
from .application_web_cases import (
    APPLICATION_WEB_CASE_TEMPLATE,
    APPLICATION_WEB_CASE_TEMPLATE_INIT,
)
from .domain_exceptions import DOMAIN_EXCEPTIONS_TEMPLATE
from .domain_models import DOMAIN_MODELS_TEMPLATE
from .domain_repository import DOMAIN_REPOSITORY_TEMPLATE
from .infrastructure_database import (
    INFRASTRUCTURE_DATABASE_TEMPLATE,
)
from .infrastructure_web import INFRASTRUCTURE_WEB_TEMPLATE


routes = [
    ("infrastructure/web.py", INFRASTRUCTURE_WEB_TEMPLATE),
    (
        "infrastructure/database.py",
        INFRASTRUCTURE_DATABASE_TEMPLATE,
    ),
    ("domain/exceptions.py", DOMAIN_EXCEPTIONS_TEMPLATE),
    ("domain/models.py", DOMAIN_MODELS_TEMPLATE),
    ("domain/repository.py", DOMAIN_REPOSITORY_TEMPLATE),
    ("application/service.py", APPLICATION_SERVICE_TEMPLATE),
    ("application/schemas.py", APPLICATION_SCHEMAS_TEMPLATE),
    ("application/handlers.py", APPLICATION_HANDLERS_TEMPLATE),
    (
        "application/interfaces.py",
        APPLICATION_INTERFACES_TEMPLATE,
    ),
]

dirs = [
    "",
    "application",
    "domain",
    "infrastructure",
    "application/use_cases",
]
