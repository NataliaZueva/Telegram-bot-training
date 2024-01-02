import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

botTimeWeb = telebot.TeleBot('6782691562:AAFOUfac0eiFvfZVH_mCGoa1Oaej0g54DEk')
chemical_elements = {}  # Пустой словарь химических элементов
chemical_elements_old = {}  # Пустой словарь химических элементов, которе игрок использовал
chemical_old = []  # Массив из названий собранных полимеров

polymers_game = {
    'glycine': {'O': 2, 'H': 5, 'N': 1, 'C': 2},
    'kvskm': {'O': 2},
    'sgrthe': {'N': 2}
}


# начальное окно спрашивает о действиях после команды /start
@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    markup = types.InlineKeyboardMarkup()
    button_begin = types.InlineKeyboardButton(text='Начать игру', callback_data='game_begin')
    button_rules = types.InlineKeyboardButton(text='Правила игры', callback_data='game_rules')
    button_exit = types.InlineKeyboardButton(text='Выйти', callback_data='exit')
    markup.row(button_begin)
    markup.row(button_rules, button_exit)
    botTimeWeb.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


# Правила игры
@botTimeWeb.callback_query_handler(func=lambda call: call.data == 'game_rules')
def gameRules(call):
    botTimeWeb.send_message(call.message.chat.id, "Вот правила игры:")
    botTimeWeb.send_photo(call.message.chat.id, photo=open('khimloto.png', 'rb'))
    botTimeWeb.send_message(call.message.chat.id, "Чтобы вернуться назад, нажмите /start")


# После начала начинается игра с кнопками
@botTimeWeb.callback_query_handler(func=lambda call: call.data == 'game_begin')
def gameBegin(call):
    markup = types.ReplyKeyboardMarkup(row_width=5)
    button_c = types.KeyboardButton(text='C')
    button_h = types.KeyboardButton(text='H')
    button_o = types.KeyboardButton(text='O')
    button_n = types.KeyboardButton(text='N')
    button_cl = types.KeyboardButton(text='Cl')
    markup.add(button_c, button_h, button_o, button_n, button_cl)

    button_ch = types.KeyboardButton(text='CH')
    button_ch2 = types.KeyboardButton(text='CH2')
    button_ch3 = types.KeyboardButton(text='CH3')
    button_c6h4 = types.KeyboardButton(text='C6H4')
    button_c6h5 = types.KeyboardButton(text='C6H5')
    markup.add(button_ch, button_ch2, button_ch3, button_c6h4, button_c6h5)

    button_rules = types.KeyboardButton(text='Правила')
    button_polymer = types.KeyboardButton(text='Полимеры ')
    markup.add(button_rules, button_polymer)

    button_used_sf = types.KeyboardButton(text='Использованные СФ')
    button_finish = types.KeyboardButton(text='Закончить')
    markup.add(button_used_sf, button_finish)

    botTimeWeb.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)


# проверка нажатия на кнопки хим элементов
@botTimeWeb.message_handler(
    func=lambda message: message.text in ['C', 'H', 'O', 'N', 'Cl', 'CH', 'CH2', 'CH3', 'C6H4', 'C6H5'])
def add_element(message):
    # Если элемент нажат прибавить его в словарь
    element = message.text
    if element in chemical_elements:
        chemical_elements[element] += 1
    else:
        chemical_elements[element] = 1
    # Вывод элементов на руках
    elements = '\n'.join([f"{key}: {value}" for key, value in chemical_elements.items()])
    botTimeWeb.send_message(message.chat.id, f"Элементы, которые есть на данный момент:\n{elements}")

    polymers = get_ready_polymers()
    # Проверка наличия достаточного количества элементов для полимеров
    if polymers != {}:
        poly = []
        for polymer, elements in polymers.items():
            elements_str = ', '.join([f"{key}: {value}" for key, value in elements.items()])
            poly.append(f"Название: {polymer}, его состав: {elements_str}")
        poly_message = "\n".join(poly)
        botTimeWeb.send_message(message.chat.id, f"Можно собрать следующие полимеры: \n{poly_message}")

        # создание кнопок Да и Нет для выбора
        markup = types.InlineKeyboardMarkup()
        button_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        button_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        markup.row(button_yes, button_no)
        botTimeWeb.send_message(message.chat.id, "Хотите собрать что-нибудь??", reply_markup=markup)


# Проверка нажатости на кнопки Да и Нет
@botTimeWeb.callback_query_handler(func=lambda call: True)
def callback_handler(callback_query):
    handle_button_click(callback_query)


# Проверка на Да - вывод возможно собранных элементов
def handle_button_click(callback_query):
    if callback_query.data == 'yes':
        polymers = get_ready_polymers()
        if polymers:
            buttons = []
            for polymer, elements in polymers.items():
                button_text = f"{polymer}"
                button = InlineKeyboardButton(button_text, callback_data=polymer)
                buttons.append(button)
            reply_markup = InlineKeyboardMarkup([buttons])
            botTimeWeb.send_message(callback_query.message.chat.id,
                                    "Соберите следующие полимеры прямо сейчас:",
                                    reply_markup=reply_markup)


# Проверка на то если ли возможность уже что-то собрать
def get_ready_polymers():
    ready_polymers = {}
    for polymer, elements in polymers_game.items():
        if all(element in chemical_elements and chemical_elements[element] >= count for element, count in
               elements.items()):
            ready_polymers[polymer] = elements

    return ready_polymers


def get_confirmation_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button_yes = types.KeyboardButton(text='Да')
    button_no = types.KeyboardButton(text='Нет')
    markup.add(button_yes, button_no)
    return markup


@botTimeWeb.message_handler(func=lambda message: message.text in ['Да', 'Нет'])
def handle_confirmation(message):
    if message.text == 'Да':
        for element, count in chemical_elements.items():
            if element in chemical_elements_old:
                chemical_elements_old[element] += count
            else:
                chemical_elements_old[element] = count
        chemical_elements.clear()
        botTimeWeb.send_message(message.chat.id, "Химические элементы добавлены в использованные.")
    else:
        botTimeWeb.send_message(message.chat.id, "Химические элементы не добавлены в использованные.")

    elements = '\n'.join([f"{key}: {value}" for key, value in chemical_elements.items()])
    botTimeWeb.send_message(message.chat.id, f"Элементы, которые есть на данный момент:\n{elements}")


botTimeWeb.polling()
