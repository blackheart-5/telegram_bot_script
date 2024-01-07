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


def handle_response(update: Update, text: str, context: CallbackContext):
    processed: str = text.lower()
    if processed in ['hello', 'hey']:
        bot_id = update.effective_user.id
        return context.bot.send_voice(chat_id=bot_id, voice=open('Jahmiel - We Alone.mp3', 'rb'))
    elif 'how are you' == processed:
        bot_id = update.effective_user.id
        return context.bot.send_photo(chat_id=bot_id, photo=open('iamgood.png', 'rb+'))
    elif 'i am sick' == processed:
        bot_id = update.effective_user.id
        return context.bot.send_message(chat_id=bot_id, text='You can talk to me')

    elif 'bye' == processed:
        bot_id = update.effective_user.id
        return context.bot.send_message(chat_id=bot_id, text="Bye")
    else:
        bot_id = update.effective_user.id
        return context.bot.send_message(chat_id=bot_id, text='Sorry, I don\'t understand what you are saying')


async def handle_message(update: Update, context: CallbackContext):
    message_type = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'private':
        response = await handle_response(update, text, context)
        print('Bot', response)
        #if not isinstance(response, coroutine):
         #   await update.message.reply_text(response)
        #else:
        print(type(response))
        #response = await handle_response(update, text, context)
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





def handle_response(update: Update, text: str, context: CallbackContext):
    processed: str = text.lower()
    bot_id = update.effective_user.id

    if 'how are you' == processed:
        # Use Google Text-to-Speech to convert text to audio
        audio_text = "I am good"  # Change this text as per your requirement
        tts = gTTS(audio_text)
        tts.save('audio_response.mp3')

        # Send the audio file
        return context.bot.send_voice(chat_id=bot_id, voice=open('audio_response.mp3', 'rb'))

    elif 'i am sick' == processed:
        # Use Google Text-to-Speech to convert text to audio
        audio_text = "You can talk to me"  # Change this text as per your requirement
        tts = gTTS(audio_text)
        tts.save('audio_response.mp3')

        # Send the audio file
        return context.bot.send_voice(chat_id=bot_id, voice=open('audio_response.mp3', 'rb'))

    elif 'bye' == processed:
        # Use Google Text-to-Speech to convert text to audio
        audio_text = "Goodbye"  # Change this text as per your requirement
        tts = gTTS(audio_text)
        tts.save('audio_response.mp3')

        # Send the audio file
        return context.bot.send_voice(chat_id=bot_id, voice=open('audio_response.mp3', 'rb'))

    else:
        # Use Google Text-to-Speech to convert text to audio
        audio_text = "Sorry, I don't understand what you are saying"  # Change this text as per your requirement
        tts = gTTS(audio_text)
        tts.save('audio_response.mp3')

        # Send the audio file
        return context.bot.send_voice(chat_id=bot_id, voice=open('audio_response.mp3', 'rb'))
import pyttsx3
from telegram import Update
from telegram.ext import CallbackContext