import json
import logging

from environs import Env
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialogflow_bot import detect_intent_texts
from telegram_logger import TelegramLogsHandler

logger = logging.getLogger('Logger')


def start_tg_message(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f"Hi {user.first_name}!")


def send_tg_message(update: Update, context: CallbackContext) -> None:
    if update.message.text:
        user_message = update.message.text
        session_id = f"tg-{update.message.chat_id}"
        project_id = context.bot_data.get("project_id")
        try:
            response_text = detect_intent_texts(project_id, session_id, [user_message], "ru-RU")
            if response_text:
                update.message.reply_text(response_text)
            else:
                update.message.reply_text("Я не понимаю, о чём речь.")
        except Exception as error:
            logger.exception(f"TG бот упал с ошибкой:{error}")


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

    dispatcher.add_handler(CommandHandler("start", start_tg_message))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_tg_message))

    logging.basicConfig(
        format="[%(asctime)s] - %(levelname)s - %(funcName)s - %(message)s",
        level=logging.INFO
    )

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(updater.bot, tg_chat_id))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
