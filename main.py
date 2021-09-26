import constants as keys
from telegram.ext import *
import responses as R
import logging

print('Bot Started...')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start_command(update, context):
    update.message.reply_text("Hi! I am your trading bot! Type /help to see commands")


def help_command(update, context):
    update.message.reply_text(
        """
        **Useful Commands**
         **/start** 
         Starts the Bot 
         **/trade [ticker][order_id][order_type][amount]**  
         For executing trades (without quotes) 
         **/price [symbol]**
         gives you the current trading price of the symbol  
         **/orderbook [order_type][ticker][depth]**
         Gives the orderbook depth
         **/help**
         Shows commands list
        """,
    )


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.greet_response(text)
    update.message.reply_text(response)


def error(update, context):
    print(f"Update {update} caused error {context.error} ")


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(keys.API_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
