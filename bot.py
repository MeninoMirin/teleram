import telebot
from telebot import types
import os

# Substitua pelo seu token do bot
token = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(token)

def greet_user(messages):
    for message in messages:
        for new_member in message.new_chat_members:
            bot.send_message(message.chat.id, f'Bem-vindo(a) {new_member.first_name} ao grupo!')
            print(f"Novo membro adicionado: {new_member.first_name}")

# Configura o listener para eventos
bot.set_update_listener(greet_user)

# Inicia o bot
if __name__ == '__main__':
    bot.infinity_polling()
