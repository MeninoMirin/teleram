import os
import nest_asyncio
nest_asyncio.apply()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
import logging
import requests
import random
from datetime import datetime

# Configure o logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para encurtar links usando a API TinyURL
async def encurtar_link(update: Update, context: CallbackContext) -> None:
    if context.args:
        url = context.args[0]
        api_url = f"http://tinyurl.com/api-create.php?url={url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            await update.message.reply_text(f"Link encurtado: {response.text}")
        else:
            await update.message.reply_text("Houve um erro ao encurtar o link.")
    else:
        await update.message.reply_text("Por favor, forneça o link após o comando. Exemplo: /encurtar https://www.google.com")

# Função para obter a previsão do tempo usando uma API pública
async def previsao_tempo(update: Update, context: CallbackContext) -> None:
    if context.args:
        cidade = " ".join(context.args)
        api_key = os.getenv("OPENWEATHER_API_KEY")  # A chave da API será obtida da variável de ambiente
        api_url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&lang=pt_br&units=metric"
        response = requests.get(api_url)
        if response.status_code == 200:
            weather_data = response.json()
            temperatura = weather_data['main']['temp']
            descricao = weather_data['weather'][0]['description']
            await update.message.reply_text(f"Previsão do tempo para {cidade}:\n{descricao}, {temperatura}°C")
        else:
            await update.message.reply_text("Houve um erro ao obter a previsão do tempo. Verifique se a cidade está correta.")
    else:
        await update.message.reply_text("Por favor, forneça o nome da cidade após o comando. Exemplo: /tempo São Paulo")

# Função para consultar a "Bola de Cristal"
async def bola_cristal(update: Update, context: CallbackContext) -> None:
    api_url = "https://api.find-ip.net/ip"  # API para obter informações do IP
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        ip_info = f"IP: {data.get('ip')}\nPaís: {data.get('country_name')}\nRegião: {data.get('region_name')}\nCidade: {data.get('city')}"
        await update.message.reply_text(f"A Bola de Cristal revela...\n{ip_info}")
    else:
        await update.message.reply_text("A Bola de Cristal está nebulosa... Tente novamente mais tarde.")

# Funções extras e perguntas
FAQ = {
    "1": "Eu sou um bot criado para ajudar você!",
    "2": "Eu uso a API do Telegram para receber e responder mensagens.",
    "3": "Eu estou disponível 24/7!",
    "4": "Eu posso encurtar links. Para encurtar um link, use o comando: /encurtar <link>.",
    "5": "Eu posso fornecer a previsão do tempo. Para obter a previsão, use o comando: /tempo <cidade>.",
    "6": "Eu posso contar piadas. Para ouvir uma piada, use o comando: /piada.",
    "7": "Eu posso compartilhar fatos interessantes. Para ouvir um fato, use o comando: /fato.",
    "8": "Eu posso informar a data atual. Use o comando: /data.",
    "9": "Eu posso informar a hora atual. Use o comando: /hora.",
    "10": "Eu posso consultar a Bola de Cristal. Para ver o futuro, use o comando: /bola.",
}

# Função para exibir um menu de perguntas
async def show_menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("1. Qual é o seu propósito?", callback_data='1')],
        [InlineKeyboardButton("2. Como você funciona?", callback_data='2')],
        [InlineKeyboardButton("3. Qual é o horário de atendimento?", callback_data='3')],
        [InlineKeyboardButton("4. Como encurtar um link?", callback_data='4')],
        [InlineKeyboardButton("5. Como obter a previsão do tempo?", callback_data='5')],
        [InlineKeyboardButton("6. Como ouvir uma piada?", callback_data='6')],
        [InlineKeyboardButton("7. Como aprender um fato interessante?", callback_data='7')],
        [InlineKeyboardButton("8. Como saber a data atual?", callback_data='8')],
        [InlineKeyboardButton("9. Como saber a hora atual?", callback_data='9')],
        [InlineKeyboardButton("10. Como consultar a Bola de Cristal?", callback_data='10')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Escolha uma opção:', reply_markup=reply_markup)

# Função para lidar com as respostas do menu
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    question_number = query.data
    response = FAQ.get(question_number, "Desculpe, não entendi sua pergunta. Pode reformular?")
    await query.edit_message_text(text=f"Resposta: {response}")

# Função para iniciar o menu quando alguém enviar uma mensagem
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text.lower()
    if "oi" in text or "/start" in text:
        await show_menu(update, context)

# Funções para comandos específicos
async def piada(update: Update, context: CallbackContext) -> None:
    piadas = ["Por que o livro de matemática se suicidou? Porque tinha muitos problemas!", "O que é um pontinho amarelo no céu? Um Fanta-sema!"]
    await update.message.reply_text(random.choice(piadas))

async def fato_interessante(update: Update, context: CallbackContext) -> None:
    fatos = ["Os gatos dormem em média 13 a 16 horas por dia!", "O Oceano Atlântico está ficando mais largo a cada ano."]
    await update.message.reply_text(random.choice(fatos))

async def data_atual(update: Update, context: CallbackContext) -> None:
    data = datetime.now().strftime("%d/%m/%Y")
    await update.message.reply_text(f"Data de hoje: {data}")

async def hora_atual(update: Update, context: CallbackContext) -> None:
    hora = datetime.now().strftime("%H:%M:%S")
    await update.message.reply_text(f"Hora atual: {hora}")

# Função principal para iniciar o bot
def main():
    token = os.getenv("TELEGRAM_TOKEN")  # O token será obtido da variável de ambiente
    application = Application.builder().token(token).build()

    # Adicione handlers para mensagens e respostas de botões
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button))

    # Handlers para comandos específicos
    application.add_handler(CommandHandler("encurtar", encurtar_link))
    application.add_handler(CommandHandler("tempo", previsao_tempo))
    application.add_handler(CommandHandler("piada", piada))
    application.add_handler(CommandHandler("fato", fato_interessante))
    application.add_handler(CommandHandler("data", data_atual))
    application.add_handler(CommandHandler("hora", hora_atual))
    application.add_handler(CommandHandler("bola", bola_cristal))

    # Inicie o bot
    application.run_polling()

# Execute o bot
if __name__ == '__main__':
    main()
