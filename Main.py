import telebot
from config import token

bot = telebot.TeleBot(token)
users = {}
flag_name_surname = 0

# Приветствие и запросить имя
@bot.message_handler(commands=['start'])
def welcome(message):
    global flag_name_surname
    flag_name_surname = 0
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет, это бот! Давай познакомимся")
    bot.send_message(chat_id,"Введи свое имя")
    users[chat_id] = {}
    bot.register_next_step_handler(message, username)

# Сохранить имя и запросить фамилию
def username(message):
    chat_id = message.chat.id
    name = message.text
    users[chat_id]["name"] = name
    bot.send_message(chat_id, "Отлично, теперь введи свою фамилию")
    bot.register_next_step_handler(message, surname)

# Сохранить фамилию
def surname(message):
    chat_id = message.chat.id
    sur_name = message.text
    users[chat_id]["surname"] = sur_name
    saving(message)

# Проверка имени и фамилии
def saving(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Имя: {users[chat_id]["name"]}\nФамилия: {users[chat_id]["surname"]}")
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text="Да")
    button2 = telebot.types.KeyboardButton(text="Изменить имя")
    button3 = telebot.types.KeyboardButton(text="Изменить фамилию")
    keyboard.add(button1)
    keyboard.add(button2, button3)
    bot.send_message(chat_id, "Данные верны?", reply_markup=keyboard)

# Подтвердить имя и фамилию
@bot.message_handler(func=lambda message: message.text == "Да")
def func1(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardRemove()
    bot.send_message(chat_id, "Отлично", reply_markup=keyboard)
    where_from(message)

# Изменить имя
@bot.message_handler(func=lambda message: message.text == "Изменить имя")
def reg_new_name(message):
    keyboard = telebot.types.ReplyKeyboardRemove()
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введи свое имя еще раз", reply_markup=keyboard)
    bot.register_next_step_handler(message, change_name)

# Сохранение измененного имени
def change_name(message):
    global flag_name_surname
    chat_id = message.chat.id
    name = message.text
    users[chat_id]["name"] = name
    bot.send_message(chat_id, "Давай проверим данные")
    if flag_name_surname == 1: next_step(message)
    else: saving(message)

# Изменить фамилию
@bot.message_handler(func=lambda message: message.text == "Изменить фамилию")
def reg_new_surname(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardRemove()
    bot.send_message(chat_id, "Введите свою фамилию еще раз", reply_markup=keyboard)
    bot.register_next_step_handler(message, change_surname)

# Сохранение измененной фамилии
def change_surname(message):
    chat_id = message.chat.id
    sur_name = message.text
    users[chat_id]["surname"] = sur_name
    bot.send_message(chat_id, "Давай проверим данные")
    if flag_name_surname == 1: next_step(message)
    else: saving(message)

# Запросить страну
@bot.message_handler(func=lambda message: message.text == "Изменить страну")
def where_from(message):
    global flag_name_surname
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text="Россия 🇷🇺", callback_data="Россия")
    button2 = telebot.types.InlineKeyboardButton(text="Грузия 🇬🇪", callback_data="Грузия")
    button3 = telebot.types.InlineKeyboardButton(text="Сербия 🇷🇸", callback_data="Сербия")
    button4 = telebot.types.InlineKeyboardButton(text="Армения 🇦🇲", callback_data="Армения")
    button5 = telebot.types.InlineKeyboardButton(text="Латвия 🇱🇻", callback_data="Латвия")
    button6 = telebot.types.InlineKeyboardButton(text="Литва 🇱🇹", callback_data="Литва")
    button7 = telebot.types.InlineKeyboardButton(text="Другое...", callback_data="ani_more")
    keyboard.add(button2, button1)
    keyboard.add(button3, button4)
    keyboard.add(button5, button6)
    keyboard.add(button7)
    bot.send_message(chat_id, "Из какой ты страны?", reply_markup=keyboard)
    flag_name_surname = 1

# Сохранение перечневой страны
@bot.callback_query_handler(func=lambda call: call.data in ["Россия", "Грузия", "Сербия", "Армения", "Латвия", "Литва"])
def save_from(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Принято!")
    users[chat_id]['from'] = call.data
    next_step(message)

# Другая страна
@bot.callback_query_handler(func=lambda call: call.data == "ani_more")
def from_more(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Введи название своей страны")
    bot.register_next_step_handler(message, save_from_more)

# Сохранение другой страны
def save_from_more(message):
    chat_id = message.chat.id
    country = message.text
    users[chat_id]["from"] = country
    next_step(message)

# Проверка всех данных
def next_step(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text="Все верно")
    button2 = telebot.types.KeyboardButton(text="Изменить имя")
    button3 = telebot.types.KeyboardButton(text="Изменить фамилию")
    button4 = telebot.types.KeyboardButton(text="Изменить страну")
    keyboard.add(button1)
    keyboard.add(button2, button3, button4)
    bot.send_message(chat_id, f"Итак, Ты {users[chat_id]["name"]} {users[chat_id]["surname"]}. Твоя страна: {users[chat_id]["from"]}", reply_markup= keyboard)

# Подтверждение всех данных
@bot.message_handler(func= lambda message: message.text == "Все верно")
def all_right(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardRemove()
    bot.send_message(chat_id, "Вы прошли регистрацию, поздравляю!", reply_markup=keyboard)

if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()