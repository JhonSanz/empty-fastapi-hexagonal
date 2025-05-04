from src.common.loggin_config import setup_logger
from src.smtp.application.interfaces import SMTPProviderInterface
from src.smtp.application.schemas import FilterParams
from src.smtp.dependencies.hostinger_smtp import SMTPHostinger
from src.smtp.infrastructure.database import ORMSMTPRepository

logger = setup_logger()


async def wrapped_send_email(
    smtp_provider: SMTPProviderInterface,
    subject: str,
    message: str,
    email: str | list[str] = None,
):
    await smtp_provider.auth()
    credentials = await smtp_provider.get_smtp_credentials()
    await smtp_provider.send(
        recipient=email,
        sender=credentials.user,
        subject=subject,
        message=message,
    )


async def send_email(
    db,
    subject: str,
    message: str,
    email: str = None,
):
    smtp_repository = ORMSMTPRepository(db=db)
    hostinger_smtp_provider = await SMTPHostinger.create(
        smtp_repository=smtp_repository
    )
    filter_params = FilterParams()
    smtp_config, _ = await smtp_repository.get(filter_params=filter_params)
    if not smtp_config:
        logger.error("Configuración SMTP no encontrada")
        return (False, "Configuración SMTP no encontrada")

    if not email:
        receivers = smtp_config[0].receivers
        if not receivers:
            logger.error("No se encontraron correos para recibir el mensaje")
            return (False, "No se encontraron correos para recibir el mensaje")
        email = smtp_config[0].receivers

    await wrapped_send_email(
        smtp_provider=hostinger_smtp_provider,
        subject=subject,
        message=message,
        email=email,
    )
    return True, None
