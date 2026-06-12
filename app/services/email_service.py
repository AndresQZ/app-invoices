import logging

import aiosmtplib
from email.mime.text import MIMEText

from app.core.config import settings

logger = logging.getLogger(__name__)



class EmailService:
    async def send(self, subject: str, body: str) -> None:
        message = MIMEText(body, "html")
        message["From"] = settings.SMTP_USER
        message["To"] = settings.EMAIL_TO
        message["Subject"] = subject

        logger.info(f'send_email_to:{settings.EMAIL_TO}')

        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
