from django.conf import settings
import traceback
import requests
from telegraph import Telegraph
from datetime import datetime


class TelegramLoggerMiddleware:
    """
    Middleware for logging errors to a Telegram chat.

    Attributes:
        get_response (Callable): The next middleware or view in the Django request chain.
        bot_token (str): The Telegram bot token.
        chat_id (str): The Telegram chat ID.
        is_logger_on (bool): Flag to enable/disable logging.
        message (str): The message to be sent.
        error (str): The error message.
        bot_api (str): The Telegram API URL for sending messages.
        error_page (str): URL to the detailed error page created on Telegraph.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.bot_token = settings.LOGGER_BOT_TOKEN
        self.logger_name = settings.LOGGER_NAME
        self.chat_id = settings.LOGGER_CHAT_ID
        self.is_logger_on = settings.LOGGER_ON
        self.message = "LOGGER"
        self.error = "ERROR"
        self.bot_api = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        self.error_page = None

    def __call__(self, request):
        """
        Processes the request and returns the response.

        Args:
            request (HttpRequest): The Django HTTP request object.

        Returns:
            HttpResponse: The Django HTTP response object.
        """
        return self.get_response(request)

    def create_error_page(self):
        """
        Creates a detailed error page on Telegraph.

        Returns:
            str: URL of the created Telegraph page, or None if creation failed.
        """
        telegraph = Telegraph()
        telegraph.create_account(short_name=self.chat_id)
        try:
            response = telegraph.create_page(title=self.error, html_content=self.message)
            return response.get("url")
        except Exception as e:
            print(f"Error creating Telegraph page: {e}")
            return None

    def send_message(self):
        """
        Sends the error message to the configured Telegram chat.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        text = f"🌐{self.logger_name}"
        text += f"\n⏰ Time: {timestamp}"
        text += self.message[:2000]
        if self.error_page:
            text += f"\n\nFOR MORE: {self.error_page}"

        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'disable_web_page_preview': True,
            'parse_mode': 'markdown'
        }

        try:
            requests.post(self.bot_api, json=payload)
            self.error_page = None
        except Exception as e:
            print(f"Error while sending message: {e}")

    def process_exception(self, request, exception):
        """
        Processes exceptions and logs them to Telegram.

        Args:
            request (HttpRequest): The Django HTTP request object.
            exception (Exception): The exception that was raised.
        """
        if exception and self.is_logger_on:
            self.error = repr(exception)
            self.message = f"\n🔗HOST: {request.build_absolute_uri()}\n💥nERROR: {self.error}\n\n```python3\n{traceback.format_exc()}```"

            if len(self.message) > 2000:
                self.error_page = self.create_error_page()

            self.send_message()
