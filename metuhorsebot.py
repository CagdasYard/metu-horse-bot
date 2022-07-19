from flask import Flask, request
import telebot
import os
import time

app = Flask(__name__)

TOKEN = os.environ["METU_HORSE_BOT_API_TOKEN"]
bot = telebot.TeleBot(TOKEN)


@app.route('/')
@app.route('/home')
def home():
    return "Success v48"


@bot.message_handler(func=lambda message: message.chat.type == 'private', content_types=['text'])
def echo_message(message):
    bot.reply_to(message, 'private ' + message.text)
    # print(message.chat.type == 'private')


@bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'], content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.chat.type + ' ' + message.text)
    # print(message)


@bot.message_handler(func=lambda message: message['chat']['type'] == 'private', content_types=['text'])
def private_message(message):
    bot.reply_to(message, "private " + message.text)


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://metu-horse-bot.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.secret_key = "It is a secret"
    app.debug = True
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

    # Polling for testing
    # bot.remove_webhook()
    # while True:
    #     try:
    #         bot.polling()
    #     except:
    #         time.sleep(15)
