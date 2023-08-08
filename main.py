import telebot
from extensions import APIException, CurrencyConverter
from config import TOKEN, exchanges
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handler_start_help(message:telebot.types.Message):
    text = f'Приветствую, {message.chat.username}!\n Чтобы начать работу введите команду боту в следующем формате:\n \
<имя валюты> <валюта, в которую хотите перевести>  <количество переводимой валюты>.\n  \
Увидить список всех доступных валют: /values.'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')
        
        answer = CurrencyConverter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}" )
    else:
        bot.reply_to(message,answer)

bot.polling()
