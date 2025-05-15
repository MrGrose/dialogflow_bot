import json
import logging

from environs import Env
from telegram import Bot, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialog_flow_bot import detect_intent_texts


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot: Bot, chat_id: int) -> None:
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record: logging.LogRecord) -> None:
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f"Hi {user.first_name}!")


def echo(update: Update, context: CallbackContext) -> None:
    if update.message.text:
        user_message = update.message.text
        user_chat_id = update.message.chat_id
        project_id = context.bot_data.get("project_id")

        response_text = detect_intent_texts(project_id, user_chat_id, [user_message], "ru-RU")
        if response_text:
            update.message.reply_text(response_text)


def main() -> None:
    env = Env()
    env.read_env()
    tg_token = env.str("TG_TOKEN")
    tg_chat_id = env.int("TG_CHAT_ID")
    application_credentials = env.str("GOOGLE_APPLICATION_CREDENTIALS")

    with open(application_credentials, "r", encoding="UTF-8") as file:
        data = json.loads(file.read())
        project_id = data.get("project_id")

    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data["project_id"] = project_id

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    logging.basicConfig(
        format="[%(asctime)s] - %(levelname)s - %(funcName)s - %(message)s",
        level=logging.INFO
    )

    logger = logging.getLogger('Logger')
    logger.setLevel(logging.INFO)

    logger.addHandler(TelegramLogsHandler(updater.bot, tg_chat_id))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
