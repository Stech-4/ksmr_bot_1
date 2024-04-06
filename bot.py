import telebot
from config import TOKEN
from payout import payout
from platforms import platforms
from api import getUser, updateUsers
from state import State

bot = telebot.TeleBot(token=TOKEN, parse_mode=None)

def create_main_page(username, id, balance): 
    return (f'{username} 
            \nid: {id} 
            \nБаланс: {balance}')
state = State()
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
    user = getUser(message)
    print(user)
    if (len(user) == 0):
        updateUsers(message)
        create_main_keyboard(chat_id = message.chat.id, message = 'Здесь будет инструкция')
    else:
        create_main_keyboard(chat_id = message.chat.id, message = create_main_page(user[0][1], user[0][2], user[0][0]))
def help(message):
    bot.reply_to(message, text='Здесь будет помощь')

@bot.message_handler(func=lambda message: message.text=='Найти заказ')
def find_orders(message): 
    state.setOrder(True)
    create_platforms_keyboard(chat_id = message.chat.id, message = 'Выберите платформу')
@bot.message_handler(content_types=['text'])
def find_order(message): 
    # cursor.execute(f"SELECT * FROM orderd WHERE platform={message.text}")
    # orders = cursor.fetchall()
    # if (orders):
    #     cursor.execute(f"SELECT * FROM orderd WHERE platform={message.text} AND location='Location'")
    #     orders = cursor.fetchall()
    if(state.getState()['in_order']):
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