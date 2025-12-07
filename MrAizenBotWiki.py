from telebot import TeleBot, types
import requests

import wikipedia
wikipedia.set_lang("ru")

bot = TeleBot('8241650196:AAEtj_LFfENQopDGyB5DNl5ImeYt6K_RJDo')

def random_duck():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.message_handler(commands = ['duck'])
def duck(message):
    url = random_duck()
    bot.send_message(message.chat.id, url)

@bot.message_handler(commands = ['wiki'])
def wiki(message):
    text = ' '.join(message.text.split(' ')[1:])
    results = wikipedia.search(text)
    markup = types.InlineKeyboardMarkup()
    for res in results:
        markup.add(types.InlineKeyboardButton(res, callback_data=res))
    bot.send_message(message.chat.id, text='Смотри что нашёл!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data)
def answer(call):
    page = wikipedia.page(call.data)
    bot.send_message(call.message.chat.id, text=page.title)
    bot.send_message(call.message.chat.id, text=page.summary)
    bot.send_message(call.message.chat.id, text=page.url)


USERNAME = "MrAizen"
WEBHOOK_URL = f"https://{USERNAME}.pythonanywhere.com/" + TOKEN

bot = TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# Удаление старого вебхука и установка нового
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)


@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200


@app.route('/')
def index():
    return 'Бот работает!'