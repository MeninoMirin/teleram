import logging
import os
from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ChatMemberHandler

# Configuração de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Lista de perguntas e respostas
perguntas_respostas = [
    {"pergunta": "Qual é a capital da França?", "resposta": "Paris"},
    {"pergunta": "Qual é o maior planeta do sistema solar?", "resposta": "Júpiter"},
    {"pergunta": "Quem escreveu 'Dom Quixote'?", "resposta": "Miguel de Cervantes"}
]

# Frases para reconhecimento de saudação
saudacoes = ['oi', 'ola', 'olá', 'bom dia', 'boa tarde', 'boa noite']

# Função para enviar saudação a novos membros
async def dar_boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_member: ChatMemberUpdated = update.chat_member
    if chat_member.new_chat_member.status == ChatMember.MEMBER:
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text=f"Bem-vindo, {chat_member.new_chat_member.user.first_name}!"
        )

# Função para enviar perguntas no privado ou quando receber uma saudação
async def enviar_perguntas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    chat_type = update.message.chat.type
    message_text = update.message.text.lower()  # Para comparar com saudações em minúsculas

    # Checar se a mensagem contém uma saudação
    if any(saudacao in message_text for saudacao in saudacoes):
        if chat_type == "private" or chat_type == "group":
            for item in perguntas_respostas:
                pergunta = item["pergunta"]
                resposta = item["resposta"]
                await update.message.reply_text(f"Pergunta: {pergunta}\nResposta: {resposta}")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Olá! Eu sou seu bot. Posso responder perguntas no privado ou dar boas-vindas em grupos.')

# Função principal do bot
def main():
    # Pegar o token da variável de ambiente
    TOKEN = os.getenv("BOT_TOKEN")

    application = ApplicationBuilder().token(TOKEN).build()

    # Handlers para comandos e eventos
    application.add_handler(CommandHandler("start", start))
    
    # Handler para enviar perguntas no privado e para saudações
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, enviar_perguntas))
    
    # Handler para monitorar novos membros no grupo/canal
    application.add_handler(ChatMemberHandler(dar_boas_vindas, ChatMemberHandler.CHAT_MEMBER))

    # Rodar o bot
    application.run_polling()

if __name__ == '__main__':
    main()
