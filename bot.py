import telebot
from config import TOKEN
from config import PGSQL_DATABASE
from config import PGSQL_HOST
from config import PGSQL_PORT
from config import PGSQL_PASSWORD
from config import PGSQL_USER
from payout import payout
from platforms import platforms

from psycopg2 import OperationalError
import psycopg2
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection
bot = telebot.TeleBot(token=TOKEN, parse_mode=None)

is_order = 0
conn = create_connection(PGSQL_DATABASE, PGSQL_USER, PGSQL_PASSWORD, PGSQL_HOST, PGSQL_PORT)
cursor = conn.cursor()

def create_main_page(username, id, balance): 
    return (f'{username} \n 
                id: {id} \n 
                Баланс: {balance}')

def create_main_keyboard(chat_id, message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    find_offer = telebot.types.KeyboardButton(text="Найти заказ")
    keyboard.add(find_offer)
    payout = telebot.types.KeyboardButton(text="Вывод")
    keyboard.add(payout)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)

def create_order_keyboard(chat_id, message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    getOffer = telebot.types.KeyboardButton(text="Взять заказ")
    keyboard.add(getOffer)
    findNext = telebot.types.KeyboardButton(text="Искать еще")
    keyboard.add(findNext)
    mainMenu = telebot.types.KeyboardButton(text="Главное меню")
    keyboard.add(mainMenu)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)

def create_payout_keyboard(chat_id, message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    for i in payout: 
        keyboard.add(telebot.types.KeyboardButton(text=i))
    mainMenu = telebot.types.KeyboardButton(text="Главное меню")
    keyboard.add(mainMenu)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)

def create_platforms_keyboard(chat_id, message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    for i in platforms: 
        keyboard.add(telebot.types.KeyboardButton(text=i))
    mainMenu = telebot.types.KeyboardButton(text="Главное меню")
    keyboard.add(mainMenu)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    cursor.execute(f"SELECT * FROM users WHERE user_id={message.from_user.id}")
    user = cursor.fetchall()
    if (user == 0):
        postgres_insert_query = """ INSERT INTO users (user_name, user_id, balance)
                                        VALUES (%s,%s,%s)"""
        record_to_insert = (message.from_user.username, message.from_user.id, 0)
        cursor.execute(postgres_insert_query, record_to_insert)    
        conn.commit()
        create_main_keyboard(chat_id = message.chat.id, message = 'Здесь будет инструкция')
    else:
        create_main_keyboard(chat_id = message.chat.id, message = create_main_page(user[0][1], user[0][2], user[0][0]))
def help(message):
    bot.reply_to(message, text='Здесь будет помощь')

@bot.message_handler(func=lambda message: message.text=='Найти заказ')
def find_orders(message): 
    create_platforms_keyboard(chat_id = message.chat.id, message = 'Выберите платформу')
@bot.message_handler(content_types=['text'])
def find_order(message): 
    print(is_order)
    cursor.execute(f"SELECT * FROM orderd WHERE platform={message.text}")
    orders = cursor.fetchall()
    if (orders):
        cursor.execute(f"SELECT * FROM orderd WHERE platform={message.text} AND location='Location'")
        orders = cursor.fetchall()
    if(is_order == 1):
        match(message.text):
            case 'Яндекс':
                bot.reply_to(message, text='Яндекс')
            case 'Google':
                bot.reply_to(message, text='Google')
            case 'Авито':
                bot.reply_to(message, text='Авито')
            case 'Прочее':
                bot.reply_to(message, text='Прочее')
    create_order_keyboard(chat_id = message.chat.id, message = 'Здесь будет заказ какой-то')
@bot.message_handler(func=lambda message: message.text=='Вывод')
def payout_f(message): 
    create_payout_keyboard(chat_id = message.chat.id, message = 'Выберите способ выплаты')
@bot.message_handler(func=lambda message: message.text=='Главное меню')
def main_menu(message): 
    create_main_keyboard(chat_id = message.chat.id, message = 'Главное меню')


bot.infinity_polling()