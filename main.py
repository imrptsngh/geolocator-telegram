from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
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

GENDER, PHOTO, LOCATION = range(3)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Boy or Girl?'
        ),
    )

    return GENDER


def gender(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'I see! Please send me the photo , ',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('photo1.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'photo1.jpg')
    update.message.reply_text(
        'Gorgeous! Now, send me your location please'
    )

    return LOCATION


def location(update: Update, context: CallbackContext) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    name = str(user.first_name)
    latitude = str(user_location.latitude)
    longitude = str(user_location.longitude)
    update.message.reply_text(
        'Got it! Maybe I can visit you sometime!'
    )
    update.message.reply_text(
       "Thanks " + name + "!!" + "Longitude & Latitude are " + longitude + " " + latitude
    )

    return LOCATION


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def help_command(update, context):
    update.message.reply_text(
        """
        **Useful Commands**
         **/start** 
         Starts the Bot 
         ** time **  
         Fetches the current time
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

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],
            PHOTO: [MessageHandler(Filters.photo, photo)],
            LOCATION: [
                MessageHandler(Filters.location, location),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    print(GENDER, PHOTO, LOCATION)


if __name__ == '__main__':
    main()
