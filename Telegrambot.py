import telebot
from telebot import types
from currency_converter import CurrencyConverter
from datetime import date, datetime
import os

mount = 0
username = None
datime = date.today()
datimetime = datetime.today()
bot = telebot.TeleBot('5438302448:AAH3I_VRAM8LAqayTXvKF4y_TUiEKbr-cYw')
currency = CurrencyConverter()
admchatid = ''


@bot.message_handler(commands=['start'])
def start(message):
    global username
    loglist = open('/home/krechet/work/python/LogTelegBot/loglist.txt', 'w')
    log = open(f'/home/krechet/work/python/LogTelegBot/Log{message.from_user.first_name}{message.from_user.last_name}.txt', 'a+')
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name} {message.from_user.last_name} - это бот который поможет '
                     f'узнать курс валют')
    bot.send_message(message.chat.id, 'Если хотите ознакомится со списком доступных валют введите /help')
    bot.send_message(message.chat.id, 'Введите количество валюты')
    username = message.from_user.username
    log.close()
    # assign directory
    directory = '/home/krechet/work/python/LogTelegBot'

    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        fi = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(fi):
            loglist.writelines(f'{fi}\n'[38::])


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Вот список поддерживаемых валют')
    bot.send_message(message.chat.id, 'USD-Американский доллар JPY-японская йена BGN-Болгарский лев CYP-Кипрский фунт CZK-Чешская крона DKK-Датская крона EEK-Эстонская крона GBP-Фунт стерлингов HUF-Венгерский форинт LTL-Литовский лит LVL-Латвийский лат MTL-Молдавский лей PLN-Польский злотый RON-Румынский лей SEK-Шведская крона SIT-Словенский толар SKK-Словацкая крона CHF-Швейцарский франк ISK-Исландская крона NOK-Норвежская крона HRK-Хорватская куна RUB-Российский рубль TRL-Турецкая лира AUD-Австралийский доллар BRL-Бразильский реал CAD-Канадский доллар CNY-Китайский юань HKD-Гонконгский доллар IDR-Индонезийская рупия ILS-Израильский шекель INR-Индийская рупия KRW-Южнокорейская вона MXN-Мексиканское песо MYR-Малайзийский ринггит NZD-Новозеландский доллар PHP-Филиппинский песо SGD-Сингапурский доллар THB-Тайский бат ZAR-Южноафриканский рэнд')


@bot.message_handler(content_types=['text'])
def amount(message):
    if message.text != 'admincommand':
        log = open(f'/home/krechet/work/python/LogTelegBot/Log{message.from_user.first_name}{message.from_user.last_name}.txt', 'a+')
        global mount
        global username
        global admchatid
        username = message.from_user.username
        try:
            mount = int(message.text.strip())
        except ValueError:
            log.writelines(f'First_name:{message.from_user.first_name} Last_name:{message.from_user.last_name} Username:{username} Message:{message.text}\n')
            bot.reply_to(message, 'Вы ввели некорректное значение попробуйте снова')
            bot.register_next_step_handler(message, amount)
            return
        if mount > 0:
            markup = types.InlineKeyboardMarkup(row_width=3)
            btn1 = types.InlineKeyboardButton('USD/RUB', callback_data='usd/rub')
            btn2 = types.InlineKeyboardButton('EUR/RUB', callback_data='eur/rub')
            btn3 = types.InlineKeyboardButton('JPY/RUB', callback_data='jpy/rub')
            btn4 = types.InlineKeyboardButton('RUB/USD', callback_data='RUB/USD')
            btn5 = types.InlineKeyboardButton('RUB/EUR', callback_data='RUB/EUR')
            btn6 = types.InlineKeyboardButton('RUB/JPY', callback_data='RUB/JPY')
            btn7 = types.InlineKeyboardButton('Изменить количество', callback_data='change')
            btn8 = types.InlineKeyboardButton('Другая валюта', callback_data='else')
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn8, btn7)
            bot.send_message(message.chat.id, "Выберите валюту", reply_markup=markup)
        else:
            bot.reply_to(message, 'Вы ввели некорректное значение попробуйте снова')
        log.writelines(f'First_name:{message.from_user.first_name} Last_name:{message.from_user.last_name} Username:{username} Message:{message.text} date:{datimetime}\n')
        log.close()
    else:
        if message.text == 'admincommand':
            bot.delete_message(message.chat.id, message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton('admincommand_message', callback_data='admmess')
            btn2 = types.InlineKeyboardButton('admincommand_loglist', callback_data='admll')
            btn3 = types.InlineKeyboardButton('admincommand_logfiles', callback_data='admlf')
            btn4 = types.InlineKeyboardButton('Exit', callback_data='Exit')
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, "Добро пожаловать в панели админа", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    log = open(f'/home/krechet/work/python/LogTelegBot/Log{call.message.from_user.first_name}{call.message.from_user.last_name}.txt', 'a+')
    global mount
    global admchatid
    username = call.message.from_user.username
    if call.data != 'else' and call.data != 'change' and call.data != 'admmess' and call.data != 'admll' and call.data != 'admlf' and call.data != 'Exit':
        val = call.data.upper().split('/')
        res = round(currency.convert(mount, val[0], val[1], date=date(2022, 3, 1)), 5)
        bot.send_message(call.message.chat.id, f'В {mount} {val[0]}: {res} {val[1]}')
        bot.send_message(call.message.chat.id, 'Курс представлен согласно 2022 03 01')
        bot.send_message(call.message.chat.id, 'Введите количество валюты')
    elif call.data == 'else':
        bot.send_message(call.message.chat.id, "Введите  значение в формате: USD/RUB")
        bot.register_next_step_handler(call.message, esle)
    elif call.data == 'admmess':
        bot.send_message(call.message.chat.id, call.message)
    elif call.data == 'admll':
        fi = [i[0:-1] for i in open('/home/krechet/work/python/LogTelegBot/loglist.txt')]
        for i in fi:
            bot.send_message(call.message.chat.id, i)
    elif call.data == 'admlf':
        bot.send_message(call.message.chat.id,  'Enter name')
        bot.register_next_step_handler(call.message, admlogfile)
    elif call.data == 'Exit':
        bot.delete_message(call.message.chat.id, call.message.message_id)

    else:
        bot.send_message(call.message.chat.id, 'Введите количество валюты')
    log.writelines(f'First_name:{call.message.from_user.first_name} Last_name:{call.message.from_user.last_name} Username:{username} Message:{call.message.text} date:{datimetime}\n')
    log.close()


def admlogfile(message):
    try:
        bot.send_document(message.chat.id, open(f'/home/krechet/work/python/LogTelegBot/{message.text}'))
    except:
        bot.send_message(message.chat.id, 'Такого нету')


def esle(message):
    log = open(f'/home/krechet/work/python/LogTelegBot/Log{message.from_user.first_name}{message.from_user.last_name}.txt', 'a+')
    username = message.from_user.username
    val = message.text.upper().split('/')
    try:
        res = round(currency.convert(mount, val[0], val[1]), 5)
        bot.send_message(message.chat.id, f'В {mount} {val[0]}: {res} {val[1]}')
        bot.send_message(message.chat.id, 'Введите количество валюты')
    except:
        try:
            res = round(currency.convert(mount, val[0], val[1], date=date(2022, 3, 1)), 5)
            bot.send_message(message.chat.id, f'В {mount} {val[0]}: {res} {val[1]}')
            bot.send_message(message.chat.id, 'Курс представлен согласно 2022 03 01')
            bot.send_message(message.chat.id, 'Введите количество валюты')
        except:
            bot.reply_to(message, 'Вы ввели некорректное значение попробуйте снова')
            bot.register_next_step_handler(message, esle)

    log.writelines(f'First_name:{message.from_user.first_name} Last_name:{message.from_user.last_name} Username:{username} Message:{message.text} date:{datimetime}\n')

    log.close()


bot.polling(none_stop=True)
