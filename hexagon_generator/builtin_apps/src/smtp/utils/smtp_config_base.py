from src.common.loggin_config import setup_logger
from src.smtp.application.schemas import SMTPBase
from src.smtp.domain.exceptions import SMTPNotFoundException
from src.smtp.domain.repository import SMTPRepository

logger = setup_logger()


class SMTPConfigBase:
    def __init__(self, *, smtp_repository: SMTPRepository):
        self.smtp_repository = smtp_repository

    async def generate_smtp_credentials(self) -> SMTPBase:
        credentials, count = await self.smtp_repository.get(limit=1)
        if count == 0:
            raise SMTPNotFoundException("Configuración SMTP no encontrada")

        config = credentials[0]
        return SMTPBase(
            host=config.server,
            port=config.port,
            user=config.user,
            password=config.password,
            receivers=config.receivers,
            debug=True,
        )
