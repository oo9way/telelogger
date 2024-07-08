# Telegram Logger Middleware

`TelegramLoggerMiddleware` is a Django middleware that logs errors to a specified Telegram chat. It sends a message to a Telegram bot with the details of any exceptions that occur during the request processing.

## Installation

Install the required packages:
   ```sh
   git clone https://github.com/oo9way/telelogger.git
   pip install requests telegraph
```
## Configuration

Add the following settings to your Django project's settings.py file:

```python
# Telegram bot token for sending messages
LOGGER_BOT_TOKEN = 'your-telegram-bot-token'

# Telegram chat ID where the messages will be sent
LOGGER_CHAT_ID = 'your-telegram-chat-id'

# Flag to enable or disable the logger
LOGGER_ON = True

# Logger name to identify the logger in messages
LOGGER_NAME = 'Your Logger Name'
```

## Usage

Add TelegramLoggerMiddleware to your MIDDLEWARE list in settings.py:

```python
MIDDLEWARE = [
    ...,
    'telelogger.middleware.TelegramLoggerMiddleware',
    ...,
]
```
Ensure that the necessary settings are correctly configured in settings.py.