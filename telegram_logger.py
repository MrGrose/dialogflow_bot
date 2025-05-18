import logging


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id) -> None:
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record) -> None:
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)