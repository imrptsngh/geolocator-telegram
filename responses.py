from datetime import datetime


def greet_response(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hi", "hello", "what's up"):
        res = "Hey! How it's going ? Type /start to start the bot"
        return res

    elif user_message in ('time', 'time?'):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%y, %H:%M:%S")
        return str(date_time)

    return "I am sorry I didn't understand. See /help for help"
