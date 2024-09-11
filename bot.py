import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Função de boas-vindas
async def welcome(update: Update, context) -> None:
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"Bem-vindo(a), {member.first_name}! :)")
        print(f"Novo membro adicionado: {member.first_name}")

# Função de despedida
async def goodbye(update: Update, context) -> None:
    if update.message.left_chat_member:
        await update.message.reply_text(f"Volte sempre, {update.message.left_chat_member.first_name}!")
        print(f"Membro saiu: {update.message.left_chat_member.first_name}")

# Função que responde "Oi"
async def respond_oi(update: Update, context) -> None:
    if update.message and update.message.text:  # Verifica se a mensagem não é None
        message = update.message.text.lower()
        if message == "oi":
            await update.message.reply_text("Oi! Como vai?")

# Função que responde ao comando /start
async def start(update: Update, context) -> None:
    await update.message.reply_text("Bot está funcionando e pronto para interagir!")
    print("Bot respondeu ao comando /start")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    application = Application.builder().token(token).build()

    # Manipulador para membros entrando no grupo
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    # Manipulador para membros saindo do grupo
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, goodbye))

    # Manipulador para responder "Oi"
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)\boi\b'), respond_oi))

    # Manipulador para o comando /start
    application.add_handler(CommandHandler('start', start))

    # Log de inicialização
    print("Bot iniciado com sucesso! Aguardando interações...")

    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main()
