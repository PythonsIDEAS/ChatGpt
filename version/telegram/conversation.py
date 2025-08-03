import ssl
import certifi
from functools import partial


ssl.default_ca_certs = certifi.where()
ssl.create_default_context = partial(
    ssl.create_default_context,
    cafile=certifi.where()
)

import telebot
from g4f.client import Client
import g4f
from main import save_message, get_history, clear_history  # Import database functions

TOKENBOT = "7214383095:AAG9qffJQuM4oxTM89CwFXFGfP0J8vYV5w0"
bot = telebot.TeleBot(TOKENBOT)
client = Client()

@bot.message_handler(commands=['clear'])
def clear_conversation(message):
    user_id = message.chat.id
    clear_history(user_id)
    bot.send_message(user_id, "Conversation history cleared!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user_message = message.text

    if user_message:
        try:
            # Retrieve user history from database
            chat_history = get_history(user_id)

            # Append new user message to history
            chat_history.append({"role": "user", "content": user_message})

            # Get response from GPT
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=chat_history,
                web_search=False,
                provider=g4f.Provider.DDG
            )

            # Extract AI response
            chat_gpt_response = response.choices[0].message.content

            # Save both user and AI messages to the database
            save_message(user_id, "user", user_message)
            save_message(user_id, "assistant", chat_gpt_response)

            # Send response to user
            bot.send_message(user_id, chat_gpt_response)

        except Exception as e:
            bot.send_message(user_id, f"Error: {str(e)}")

# Start polling for messages
bot.infinity_polling()