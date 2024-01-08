import os
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

botTimeWeb = telebot.TeleBot('6782691562:AAFOUfac0eiFvfZVH_mCGoa1Oaej0g54DEk')


def game_start():
    global chemical_elements, chemical_elements_old, chemical_old, polymers_game, fields, flag_a, flag_b, flag_g
    chemical_elements = {}  # Пустой словарь химических элементов
    chemical_elements_old = {}  # Пустой словарь химических элементов, которе игрок использовал
    chemical_old = []  # Массив из названий собранных полимеров

    with open('polymers.txt', 'r', encoding="utf-8") as file:
        lines = file.readlines()
        polymers_game = {}
        fields = {}
        for line in lines:
            composition_dict = {}
            polymer, field, *composition = line.split()
            field = field.split('-')[0]
            composition = [i.split(":") for i in composition[1:]]
            for each in composition:
                composition_dict[each[0]] = int(each[1])
            if field in fields:
                fields[field] += 1
            else:
                fields[field] = 1
            polymers_game[polymer] = composition_dict

    fields['beta'] += fields['alpha']
    fields['gamma'] += fields['beta']
    flag_a = False
    flag_b = False
    flag_g = False


game_start()


# начальное окно спрашивает о действиях после команды /start
@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    markup = types.InlineKeyboardMarkup()
    button_begin = types.InlineKeyboardButton(text='Начать игру', callback_data='game_begin')
    button_rules = types.InlineKeyboardButton(text='Правила игры', callback_data='game_rules')
    button_rules_bot = types.InlineKeyboardButton(text='Работа бота', callback_data='game_rules_bot')
    markup.row(button_begin)
    markup.row(button_rules, button_rules_bot)
    botTimeWeb.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


# Правила игры
@botTimeWeb.callback_query_handler(func=lambda call: call.data == 'game_rules')
def gameRules(call):
    botTimeWeb.send_photo(call.message.chat.id, photo=open('image/rules.png', 'rb'),
                          caption='''В начале игры перед вами лежат некоторые предметы:
    1. Карточка полимеров для сбора;
    2. СФ - структурные фрагменты для сбора структурных формул;
    3. Планшет для сбора полимеров.''')

    keyboard = types.InlineKeyboardMarkup()
    next_button = types.InlineKeyboardButton("Далее", callback_data='game_rules1')
    keyboard.add(next_button)

    botTimeWeb.send_message(call.message.chat.id, "Выберите действие:", reply_markup=keyboard)


@botTimeWeb.callback_query_handler(func=lambda call: call.data == 'game_rules1')
def gameRules(call):
    botTimeWeb.send_photo(call.message.chat.id, photo=open('image/rules_1.png', 'rb'),
                          caption='''Ведущий будет доставать из мешочка СФ и проговаривать.
Вам нужно их ставить перед собой для последующей сборки.
Так же вам нужно отмечать их в данном боте.''')
    botTimeWeb.send_message(call.message.chat.id, '''Цель игры: как можно быстрее собрать 3 полимера на планшете.
Но стоит учитывать, что другие игроки тоже хотят победить!
Возможно быстрая сборка окажется не самой эффективной для победы... ''')

    keyboard = types.InlineKeyboardMarkup()
    next_button = types.InlineKeyboardButton("Начать игру", callback_data='game_begin')
    next_button1 = types.InlineKeyboardButton("Работа с ботом", callback_data='game_rules_bot')
    keyboard.add(next_button, next_button1)

    botTimeWeb.send_message(call.message.chat.id, "Выберите действие:", reply_markup=keyboard)


# Правила игры bot
@botTimeWeb.callback_query_handler(func=lambda call: call.data == 'game_rules_bot')
def gameRulesBot(call):
    botTimeWeb.send_message(call.message.chat.id, "Правила по работе с ботом")
    botTimeWeb.send_photo(call.message.chat.id, photo=open('image/bot_1.png', 'rb'),
                          caption='''В начале игры перед вами появятся определенные кнопки:
    1 и 2 строка - СФ для сбора полимеров;
    Использованные СФ - после сбора определенного полимера СФ попадут в данный список;
    Полимеры - открывает подсказку всех полимеров;
    Закончить - сбрасывает игру.''')

    keyboard = types.InlineKeyboardMarkup()
    next_button = types.InlineKeyboardButton("Далее", callback_data='next')
    keyboard.add(next_button)
    botTimeWeb.send_message(call.message.chat.id, "Выберите действие:", reply_markup=keyboard)


@botTimeWeb.callback_query_handler(func=lambda call: call.data == 'next')
def gameRules(call):
    botTimeWeb.send_message(call.message.chat.id,
                            '''Вам могут встречаться как обычные названия полимеров, так и нет.
  Пример:
      Полистирол и Полистирол_1СН.
      Полистирол - тот самый, который показан в карточке полимеров.
      Полистирол_1СН - полимер с одной заменой СН.''')
    botTimeWeb.send_message(call.message.chat.id,
                            '''У вас могут встречаться разные полимеры, и все они помогут вам сделать замену и быстрее победить!''')

    keyboard = types.InlineKeyboardMarkup()
    next_button = types.InlineKeyboardButton("Начать игру", callback_data='game_begin')
    next_button1 = types.InlineKeyboardButton("Правила игры", callback_data='game_rules')
    keyboard.add(next_button, next_button1)

    botTimeWeb.send_message(call.message.chat.id, "Выберите действие:", reply_markup=keyboard)


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

    button_used_sf = types.KeyboardButton(text='Использованные СФ')
    markup.add(button_used_sf)

    button_polymer = types.KeyboardButton(text='Полимеры')
    button_finish = types.KeyboardButton(text='Закончить')
    markup.add(button_polymer, button_finish)

    botTimeWeb.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)


@botTimeWeb.message_handler(func=lambda message: message.text == 'Использованные СФ')
def used_SF(message):
    elements = '\n'.join([f"{key}: {value}" for key, value in chemical_elements_old.items()])
    botTimeWeb.send_message(message.chat.id, f"Вот все СФ, что вы уже использовали:\n{elements}")


@botTimeWeb.message_handler(func=lambda message: message.text == 'Закончить')
def finish(message):
    game_start()
    botTimeWeb.send_message(message.chat.id, "Программа сброшена, но вы можете начать заново. \n/start")


# Отобразить доску правил сбора полимеров
@botTimeWeb.message_handler(
    func=lambda message: message.text in ['Полимеры'])
def polim(message):
    botTimeWeb.send_photo(message.chat.id, photo=open('image/khimloto.png', 'rb'),
                          caption="Вы можете ознакомиться со всеми полимерами, которые бывают!")


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
        botTimeWeb.send_message(message.chat.id, "Хотите собрать что-нибудь?", reply_markup=markup)


# Проверка нажатости на кнопки Да и Нет
@botTimeWeb.callback_query_handler(func=lambda call: True)
def callback_handler(callback_query):
    handle_button_click(callback_query)


def get_polymer_image_filename(polymer_name):
    return f"{polymer_name}.png"


# Проверка на Да - вывод возможно собранных элементов
def handle_button_click(callback_query):
    polymers = get_ready_polymers()

    if callback_query.data == 'yes':
        if polymers:
            buttons = []
            but = {}
            i = 1
            for polymer, elements in polymers.items():
                but[i] = polymer
                button = InlineKeyboardButton(i, callback_data=polymer)
                buttons.append(button)
                i += 1

            but_i = '\n'.join([f"{key} -  {value}" for key, value in but.items()])

            num_buttons = len(buttons)
            num_rows = (num_buttons + 7) // 8
            rows = [buttons[i:i + 8] for i in range(0, num_buttons, 8)]

            reply_markup = InlineKeyboardMarkup(rows)
            botTimeWeb.send_message(callback_query.message.chat.id,
                                    f"Выберете номер полимера для сбора: \n{but_i}",
                                    reply_markup=reply_markup)


    else:
        global flag_a, flag_b, flag_g
        for element, count in polymers[callback_query.data].items():
            if element in chemical_elements_old:
                chemical_elements_old[element] += count
            else:
                chemical_elements_old[element] = count
            chemical_elements[element] -= count
        chemical_old.append(callback_query.data)
        keys_list = list(polymers_game.keys())
        index_in_array = keys_list.index(callback_query.data)

        # Получение имени файла изображения полимера
        image_filename = get_polymer_image_filename(callback_query.data)
        image_path = f'image/polimers/{image_filename}'

        if os.path.isfile(image_path):
            botTimeWeb.send_photo(callback_query.message.chat.id, photo=open(image_path, 'rb'))
        else:
            none_image_path = 'image/polimers/None.png'
            botTimeWeb.send_photo(callback_query.message.chat.id, photo=open(none_image_path, 'rb'),
                                  caption='''Эхх... Но не огорчайся, всё ещё впереди! 
                                  \n Просто разработчики ещё не успели всё доработать((''')

        if index_in_array <= fields['alpha']:
            for i in range(0, fields['alpha']):
                del polymers_game[keys_list[i]]
            flag_a = True
            if flag_b and flag_g:
                botTimeWeb.send_message(callback_query.message.chat.id, "Вы собрали поле alpha.")
            elif flag_b:
                fields['gamma'] -= fields['beta']
                botTimeWeb.send_message(callback_query.message.chat.id, "Вы собрали поле alpha, осталось gamma.")
            elif flag_g:
                fields['beta'] -= fields['alpha']
                botTimeWeb.send_message(callback_query.message.chat.id, "Вы собрали поле alpha, осталось beta.")
            else:
                fields['beta'] -= fields['alpha']
                fields['gamma'] -= fields['alpha']
                botTimeWeb.send_message(callback_query.message.chat.id, "Вы собрали поле alpha, осталось beta и gamma.")
            fields['alpha'] = -1
        elif (index_in_array > fields['alpha']) and (index_in_array <= fields['beta']):
            for i in range(fields['alpha'] + 1, fields['beta']):
                del polymers_game[keys_list[i]]
            flag_b = True
            if flag_a and flag_g:
                botTimeWeb.send_message(callback_query.message.chat.id, "Вы собрали поле beta.")
            elif flag_a:
                fields['gamma'] -= fields['beta']
                botTimeWeb.send_message(callback_query.message.chat.id, "Вы собрали поле beta, осталось gamma.")
            elif flag_g:
                botTimeWeb.send_message(callback_query.message.chat.id, "Вы собрали поле beta, осталось alpha.")
            else:
                fields['gamma'] = - fields['beta'] + fields['alpha']
                botTimeWeb.send_message(callback_query.message.chat.id, "Вы собрали поле beta, осталось alpha и gamma.")
            fields['beta'] = -1
        else:
            for i in range(fields['beta'] + 1, fields['gamma']):
                del polymers_game[keys_list[i]]
            flag_g = True
            if flag_a and flag_b:
                botTimeWeb.send_message(callback_query.message.chat.id, "Вы собрали поле gamma.")
            elif flag_a:
                botTimeWeb.send_message(callback_query.message.chat.id, "Вы собрали поле gamma, осталось beta.")
            elif flag_b:
                botTimeWeb.send_message(callback_query.message.chat.id, "Вы собрали поле gamma, осталось alpha.")
            else:
                botTimeWeb.send_message(callback_query.message.chat.id, "Вы собрали поле gamma, осталось alpha и beta.")
            fields['gamma'] = -1
        if not (flag_a and flag_b and flag_g):
            botTimeWeb.send_message(callback_query.message.chat.id, "Химические элементы добавлены в использованные.")
            elements = '\n'.join([f"{key}: {value}" for key, value in chemical_elements.items()])
            botTimeWeb.send_message(callback_query.message.chat.id,
                                    f"Элементы, которые есть на данный момент:\n{elements}")
        else:
            botTimeWeb.send_message(callback_query.message.chat.id, "Вы собрали все поля. Поздравляем!")


@botTimeWeb.callback_query_handler(func=lambda call: True)
def callback_handler(callback_query):
    assemblePoly(callback_query)


def assemblePoly(callback_query):
    for element, count in chemical_elements.items():
        if element in chemical_elements_old:
            chemical_elements_old[element] += count
        else:
            chemical_elements_old[element] = count
    chemical_elements.clear()
    botTimeWeb.send_message(callback_query.message.chat.id, "Химические элементы добавлены в использованные.")


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
