from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

# Função para responder "oi" com uma lista de opções
def resposta_oi(update, context):
    # Resposta com a lista de opções
    texto_resposta = (
        "Olá! Como posso te ajudar hoje?\n"
        "Aqui estão algumas opções:\n"
        "/ajuda - Ver mais informações sobre o que o bot faz.\n"
        "/comandos - Ver todos os comandos disponíveis.\n"
        "/contato - Falar com o suporte.\n"
    )
    update.message.reply_text(texto_resposta)

# Função para dar boas-vindas quando alguém entra no grupo/canal
def boas_vindas(update, context):
    for member in update.message.new_chat_members:
        update.message.reply_text(f"Bem-vindo(a), {member.first_name}! Esperamos que goste do grupo.")

# Função para dizer adeus quando alguém sai do grupo/canal
def despedida(update, context):
    if update.message.left_chat_member:
        update.message.reply_text(f"Adeus, {update.message.left_chat_member.first_name}. Volte sempre!")

def main():
    TOKEN = "7359248793:AAEOyPPaHPZvEICuHXtzlgViUO3VP-Ubv7U"  # Substitua com o token do seu bot
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    # Adiciona o handler para novas entradas no grupo/canal
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, boas_vindas))

    # Adiciona o handler para saídas do grupo/canal
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, despedida))

    # Adiciona o handler para responder quando alguém diz "oi"
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r'(?i)\boi\b'), resposta_oi))

    # Inicia o bot
    updater.start_polling()
    updater.idle()

if name == '__main__':
    main()
