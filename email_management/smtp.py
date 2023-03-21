import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

logger = logging.getLogger(__name__)


class SmtpManager:
    def __init__(
            self,
            smtp_address: str,
            port=587,
            username="",
            password=""
    ):
        """
        :param smtp_address (str): Server address like smtp.google.com
        :param port (int): The port of the service, default 578
        :param username (str): The username to login the email_management service
        :param password (str): The password to login the email_management service
        """
        self.smtp_address = smtp_address
        self.port = port
        self.__username = username
        self.__password = password
        self.__connection: SMTP or None = None
        self.is_connected = False

    def connect(self):
        if not self.is_connected:
            self.__connection = SMTP(self.smtp_address, self.port)
            logger.debug(self.__connection.ehlo())
            logger.debug(self.__connection.starttls())
            logger.debug(self.__connection.login(self.__username, self.__password))
            self.is_connected = True

    def disconnect(self):
        if self.is_connected:
            logger.debug(self.__connection.quit())
            self.is_connected = False

    def send_mail(self, to, subject, body):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        return self.__connection.sendmail(
            from_addr=self.__username,
            to_addrs=to,
            msg=msg.as_string()
        )

    def __enter__(self) -> 'SmtpManager':
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
