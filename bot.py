import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext

# Função de boas-vindas
def welcome(update: Update, context: CallbackContext) -> None:
    for member in update.message.new_chat_members:
        update.message.reply_text(f"Bem-vindo(a), {member.first_name}! :)")

# Função de despedida
def goodbye(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"Volte sempre, {update.message.left_chat_member.first_name}!")

# Função que responde "Oi"
def respond_oi(update: Update, context: CallbackContext) -> None:
    message = update.message.text.lower()
    if message == "oi":
        update.message.reply_text("Oi! Como vai?")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(token)

    dispatcher = updater.dispatcher

    # Manipulador para membros entrando no grupo
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    # Manipulador para membros saindo do grupo
    dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, goodbye))

    # Manipulador para responder "Oi"
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'(?i)\boi\b'), respond_oi))

    # Inicia o bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
