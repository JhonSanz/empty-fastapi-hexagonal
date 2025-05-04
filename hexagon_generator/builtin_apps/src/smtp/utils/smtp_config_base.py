from src.common.loggin_config import setup_logger
from src.smtp.application.schemas import FilterParams, SMTPBase
from src.smtp.domain.exceptions import SMTPNotFoundException
from src.smtp.domain.repository import SMTPRepository

logger = setup_logger()


class SMTPConfigBase:
    def __init__(self, *, smtp_repository: SMTPRepository):
        self.smtp_repository = smtp_repository

    async def generate_smtp_credentials(self) -> SMTPBase:
        filter_params = FilterParams()
        credentials, count = await self.smtp_repository.get(filter_params=filter_params)
        if count == 0:
            logger.error("Configuración SMTP no encontrada")
            return
        credentials = credentials[0]
        result = SMTPBase(
            host=credentials.server,
            port=credentials.port,
            user=credentials.user,
            password=credentials.password,
            debug=True,
        )
        return result
