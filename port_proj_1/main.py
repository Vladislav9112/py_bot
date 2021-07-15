import telebot
from telebot import types

bot = telebot.TeleBot('1670174822:AAEl1Oo0RTA7hvQZ3pNxFOqYqrVEt5HCSV8')

dr_a = {}
dr_b = {}
dr_c = {}

name = ''
surname = ''
data = ''
doc = ''

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Доктор А', 'Доктор Б', 'Доктор В')

keyboard3 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard3.row('Привет')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Добрый день', reply_markup=keyboard3)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Как ваше имя?')
        bot.register_next_step_handler(message, reg_name)


def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Как ваша фамилия?')
    bot.register_next_step_handler(message, reg_surname)


def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Выберите доктора', reply_markup=keyboard1)
    bot.register_next_step_handler(message, reg_doc)


def reg_doc(message):
    global doc
    doc = message.text
    bot.send_message(message.from_user.id, 'Выберите дату. "Пример - 1.01.2001"')
    bot.register_next_step_handler(message, reg_data)


def reg_data(message):
    global data
    data = message.text

    keyboard2 = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='да', callback_data='yes')
    keyboard2.add(key_yes)
    key_no = types.InlineKeyboardButton(text='нет', callback_data='no')
    keyboard2.add(key_no)

    question = 'Вас зовут' + ' ' + name + ' ' + surname + ' ' + 'и вы записались к' + ' ' + doc + ' ' + 'на' + ' ' + data + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard2)


@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    if call.data == 'yes':
        if doc.lower() == 'доктор а':
            if data not in dr_a:
                dr_a[data] = name + ' ' + surname
                bot.send_message(call.message.chat.id, 'Заявка принята')
                with open('C:\\Users\\shino\\Desktop\\test_bot.txt', 'w') as i:
                    for key, val in dr_a.items():
                        i.write('{}:{}\n'.format(key, val))

            else:
                bot.send_message(call.message.chat.id, 'Эта дата занета попробуйте снова')
                bot.register_next_step_handler(call.message, reg_name)
        elif doc.lower() == 'доктор б':
            if data not in dr_b:
                dr_b[data] = name + ' ' + surname
                bot.send_message(call.message.chat.id, 'Заявка принята')
            else:
                bot.send_message(call.message.chat.id, 'Эта дата занета попробуйте снова')
                bot.register_next_step_handler(call.message, reg_name)

        elif doc.lower() == 'доктор в':
            if data not in dr_c:
                dr_c[data] = name + ' ' + surname
                bot.send_message(call.message.chat.id, 'Заявка принята')
            else:
                bot.send_message(call.message.chat.id, 'Эта дата занета попробуйте снова')
                bot.register_next_step_handler(call.message, reg_name)
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Попробуйте снова')
        bot.send_message(call.message.chat.id, 'Как вас зовут')
        bot.register_next_step_handler(call.message, reg_name)

        # litr = open('C:\\Users\\shino\Desktop\\test_bot.txt', 'w' )
        # litr.write('some text\n')
        # litr.write(str())
        # litr.close()


bot.polling()
