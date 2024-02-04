import logging
import os
from . import handlers
from telegram.ext import CommandHandler, Application

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler(["whoami"], handlers.whoami_handler))
    application.add_handler(CommandHandler(["start"], handlers.start_handler))
    application.add_handler(CommandHandler(["topup5", "t5"], handlers.topup5_handler))
    application.add_handler(CommandHandler(["topup1", "t1"], handlers.topup1_handler))
    application.add_handler(CommandHandler(["topup", "t"], handlers.topup10_handler))
    application.add_handler(CommandHandler(["imagine", "i"], handlers.imagine_handler))
    application.add_handler(CommandHandler(["credits", "c"], handlers.credits_handler))

    application.run_polling()

if __name__ == '__main__':
    main()