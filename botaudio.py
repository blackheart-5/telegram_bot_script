import pyttsx3
import os
import time
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from typing import Final
import tracemalloc



TOKEN: Final = '6555863588:AAEqAL3MGTNkuuyGQ7fd_sQXPO8F8dpS_8E'
Bot_username: Final = '@voicereg_bot'

tracemalloc.start()


async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text('Hello! Thanks for chatting with me. I am a voice bot')


async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text('Please type something so I can respond')


async def custom_command(update: Update, context: CallbackContext):
    await update.message.reply_text('This is a custom command')


def save_and_send_audio(bot_id, text, context):
    engine = pyttsx3.init()
    engine.save_to_file(text, f'audio_response.mp3')
    engine.runAndWait()

    return context.bot.send_audio(chat_id=bot_id, audio=open(f'audio_response.mp3', 'rb'))


def handle_response(update: Update, text: str, context: CallbackContext):
    processed: str = text.lower()
    bot_id = update.effective_user.id

    if processed in ['hi', 'hello', 'hi there', 'hello there', 'hey there', 'hey']:
        audio_text = 'Hello! I am a voice bo.  what can I help you with'
        return save_and_send_audio(bot_id, audio_text, context)

    elif 'how are you' == processed:
        audio_text = "I am doing good"  # Change this text as per your requirement
        return save_and_send_audio(bot_id, audio_text, context)
    elif 'i am sick' == processed:
        audio_text = "You can talk to me"  # Change this text as per your requirement
        return save_and_send_audio(bot_id, audio_text, context)
    elif 'bye' == processed:
        audio_text = "Goodbye"  # Change this text as per your requirement
        return save_and_send_audio(bot_id, audio_text, context)
    else:
        audio_text = "Sorry, I don't understand what you are saying"  # Change this text as per your requirement
        return save_and_send_audio(bot_id, audio_text, context)


async def handle_message(update: Update, context: CallbackContext):
    message_type = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'private':
        response = await handle_response(update, text, context)
        os.remove('audio_response.mp3')
        return response


async def error(update: Update, context: CallbackContext):
    print(f'{update} caused the following error {context.error}')


def main():
    print('Starting building.........')
    app_builder = Application.builder().token(TOKEN)
    app = app_builder.read_timeout(200).write_timeout(200).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    print('Polling started')
    try:
        app.add_handler(MessageHandler(filters.TEXT, handle_message))
        app.add_error_handler(error)
        app.run_polling(poll_interval=10, timeout=120)
    except RuntimeError as e:
        print("Error during polling:", e)


if __name__ == '__main__':
    main()