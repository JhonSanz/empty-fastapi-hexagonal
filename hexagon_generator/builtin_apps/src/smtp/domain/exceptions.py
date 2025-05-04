from fastapi import Request, status

from src.common.std_response import StandardResponse, std_response


class SMTPNotFoundException(Exception):
    pass


class ErrorSendingEmailException(Exception):
    pass


async def smtp_not_found_handler(request: Request, exc: SMTPNotFoundException):
    return std_response(
        status_code=status.HTTP_404_NOT_FOUND,
        ok=False,
        msg=str(exc),
        data=None,
    )


async def error_sending_email_handler(
    request: Request, exc: ErrorSendingEmailException
):
    return std_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        ok=False,
        msg=str(exc),
        data=None,
    )


EXCEPTIONS_SMTP_MAPPING = [
    (smtp_not_found_handler, SMTPNotFoundException),
    (error_sending_email_handler, ErrorSendingEmailException),
]
