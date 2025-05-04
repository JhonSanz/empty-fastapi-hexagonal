import smtplib
import socket
import ssl
from email.mime.text import MIMEText

from src.common.loggin_config import setup_logger
from src.smtp.application.interfaces import SMTPProviderInterface
from src.smtp.application.schemas import SMTPBase
from src.smtp.domain.exceptions import ErrorSendingEmailException
from src.smtp.domain.repository import SMTPRepository
from src.smtp.utils.smtp_config_base import SMTPConfigBase

logger = setup_logger()


class SMTPHostinger(SMTPProviderInterface, SMTPConfigBase):
    def __init__(self, *, smtp_repository: SMTPRepository):
        super().__init__(smtp_repository=smtp_repository)

        self.smtp_credentials: SMTPBase = None
        self.conn = None

    @classmethod
    async def create(cls, smtp_repository: SMTPRepository):
        instance = cls(smtp_repository=smtp_repository)
        instance.smtp_credentials = await instance.generate_smtp_credentials()
        return instance

    async def auth(self):
        context = ssl.create_default_context()
        try:
            self.conn = smtplib.SMTP_SSL(
                self.smtp_credentials.host, self.smtp_credentials.port, context=context
            )
        except socket.gaierror as e:
            logger.error(e)
            raise ErrorSendingEmailException(f"Error enviando mensaje, error SMTP")
        except smtplib.SMTPException as e:
            logger.error(e)
            raise ErrorSendingEmailException(f"Error enviando mensaje, error SMTP")

        self.conn.set_debuglevel(self.smtp_credentials.debug)

        try:
            self.conn.login(self.smtp_credentials.user, self.smtp_credentials.password)
        except smtplib.SMTPAuthenticationError as e:
            logger.info(e)
            raise ErrorSendingEmailException(f"Error sending email")
        except Exception as e:
            logger.info(e)
            raise ErrorSendingEmailException(f"Error sending email")

    async def send(
        self, *, recipient: str | list[str], sender: str, subject: str, message: str
    ):
        raw = MIMEText(message, "html")
        raw["Subject"] = subject
        raw["From"] = sender
        raw["To"] = ", ".join(recipient) if type(recipient) == list else recipient

        if self.conn:
            try:
                self.conn.sendmail(sender, recipient, raw.as_string())
                logger.info(f"Enviando mensaje {sender}, {recipient}")
            except Exception as e:
                logger.error(f"Error enviando el mensaje {e}")
                raise ErrorSendingEmailException(f"Error sending email")
            return True
        else:
            logger.error(f"Error enviando el mensaje, no se estableció la conexión")
            raise ErrorSendingEmailException(f"Error sending email")

    async def get_smtp_credentials(self) -> SMTPBase:
        return self.smtp_credentials
