
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from typing import Final

TOKEN: Final = '6555863588:AAEqAL3MGTNkuuyGQ7fd_sQXPO8F8dpS_8E'
Bot_username: Final = '@voicereg_bot'


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me. I am a voice bot')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please type something so i can respond')


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command')


def handle_response(text: str):
    processed: str = text.lower()
    if 'hello' in processed or 'hey' in processed:
        return 'hey there'
    elif 'how are you' in processed:
        return 'I am good'
    elif 'i am sick' in processed:
        return 'You can talk to me'
    elif 'bye' in processed:
        return "Bye"
    else:
        return 'Sorry I dont understand what you are saying'


async def handle_message(update: Update, context:ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if Bot_username in text:
            new_text: str = text.replace(Bot_username, '').strip()
            response: str = handle_response(new_text)
            print('Bot', response)
            await update.message.reply_text(response)
        else:
            return
    elif message_type == 'private':
        response: str = handle_response(text)
        print(response)
        await update.message.reply_text(response)


async def error(update: Update, context:ContextTypes.DEFAULT_TYPE):
    print(f'{update} caused the following error{context.error}')


def main():
    print('Starting.........')
    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))


    #message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #error
    app.add_error_handler(error)

    #polls the bot
    print('Polling')
    app.run_polling(poll_interval=3)


if __name__ == '__main__':
    main()

