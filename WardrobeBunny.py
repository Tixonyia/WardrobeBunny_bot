""" Main. Непосредственная связь с API бота.
    Работа с DB осуществляется в data_cursor.py
    Функционал питона в functions.py"""

import re
import random
import telebot

import data_cursor
import functions

def token():
    # Получение токена из файла.
    with open('/home/tixonyia/Рабочий стол/Bunny/Token', 'r') as file:
        str_token = file.read(46)
    return str_token

# Подключение к боту.
bot = telebot.TeleBot(token(), threaded=False)

@bot.message_handler(content_types=['text', 'photo'])
# работа с message от пользователя
def get_text_messages(message):
    functions.add_user(message)
    if message.text.lower() == 'бжя' or message.text.lower() == 'любля':
        bot.send_message(message.from_user.id, message.text)
    elif message.text.lower() == 'лагмань' :
        bot.send_message(message.from_user.id, "логмань, позжалуйста")
    elif message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, "Привет)")
        bot.send_message(message.from_user.id, "Я только создан, но уже"
                                               " могу рассказать о погоде: \n"
                                               "Просто набери 'погода' или 'ветер.'")

    elif message.text.lower() == 'погода':
        location = functions.get_location_now()
        weather = functions.get_weather()
        text = f"{location['loc_name']}. {location['loc_time']} \n"\
               f"На улице {weather['temperature_2m']}°C. " \
               f"{weather['weathercode']}. " \
               f"Ощущается как {weather['apparent_temperature']}°C." \
               f"\n За бортом: \n" \
               f"Ветер {weather['windspeed_10m']} м\с . С порывами до {weather['windgusts_10m']} м\с .\n" \
               f"Относительная влажность состовляет {weather['relativehumidity_2m']} %.\n" \
               f"Атмосферное давление: {weather['surface_pressure']}мм.рт.ст."
        bot.send_message(message.from_user.id, text)

    elif message.text.lower() == 'что надеть':
        weather = functions.get_weather()
        res = functions.what_to_wear(message.from_user.id, weather)
        if isinstance(res, str):
            bot.send_message(message.from_user.id, res)
        else:
            [bot.send_message(message.from_user.id, f'{val} -> {key}') for val, key in res.items()]

    elif message.text.lower() == 'добавить место':
        def loc_name(message):
            msg = bot.send_message(message.from_user.id, 'Название?')
            bot.register_next_step_handler(msg, loc_coord)

        def loc_coord(message):
            msg = bot.send_message(message.from_user.id, 'Координаты?')
            bot.register_next_step_handler(msg, add_in_db_loc, message.text)

        def add_in_db_loc(message, name_loc):
            # Добавить место в DB
            functions.create_table_location(message)
            coord_loc = functions.get_url(message)
            if coord_loc == 'Не могу вычеслить координаты.':
                bot.send_message(message.from_user.id, coord_loc)
            else:
                functions.add_user_location(message.from_user.id, name_loc, coord_loc)
                bot.send_message(message.from_user.id, coord_loc)
        loc_name(message)

    elif message.text.lower() == 'добавить одежду':
        # Добавить одежду в DB
        dict_columns = {'clothes_name': 'Название', 'description': 'Описание',
                        'type_of_the_thing': 'тип одежы(головняк, штаны, футболка, обувь)',
                        'photo': 'Фото', 'proprty_thing': 'Оцени защиту в формате 0-10. В порядке: '
                                                    'ветер, дождь, от холода, от жары, от солнца.'
                                                    'Например: 0 3 4 7 0'}
        iter_dict = iter(dict_columns.keys())
        list_answer = []

        def colomn(message):
            # сохранение ряда ответов для данных в таблицу
            try:
                next_iter = next(iter_dict)
                msg = bot.send_message(message.from_user.id, dict_columns[next_iter])
                list_answer.append(message.text)
                bot.register_next_step_handler(msg, colomn)

            except StopIteration:
                # смещение ответов на один вверх.
                list_answer.append(message.text)
                list_answer.pop(0)
                ind = 0
                for key in dict_columns.keys():
                    dict_columns[key] = list_answer[ind]
                    ind += 1
                functions.create_table_clothes(message)
                res = functions.add_user_clothes(message, dict_columns)
                bot.send_message(message.from_user.id, res)

        colomn(message)


    elif re.findall("r'https://www.google.ru/maps/|https://maps.app.goo.gl"
                    "|https://goo.gl/maps|https://2gis.ru/|https://go.2gis.com/"
                    "|https://yandex.ru/maps/|-?\d+\.\d+,? ?-?\d+\.\d+", message.text):
        coord_str = functions.get_url(message)
        if coord_str == 'except':
            bot.send_message(message.from_user.id, 'Координаты не в том формате.')
        else:
            functions.get_weather.__defaults__ = (coord_str,)
            bot.send_message(message.from_user.id, coord_str,)

    elif message.text.lower() == "добавить погоду":
        weather_data = functions.get_weather()
        dict_columns = {'weather_name': 'Дайте название погоде', 'weather_description': 'Дайте описание погоде',
                        'things_description': 'Что было надето', 'coments': 'Комментарии.'}
        iter_dict = iter(dict_columns.keys())
        list_answer = []

        def colomn(message):
            # сохранение ряда ответов для данных в таблицу
            try:
                next_iter = next(iter_dict)
                msg = bot.send_message(message.from_user.id, dict_columns[next_iter])
                list_answer.append(message.text)
                bot.register_next_step_handler(msg, colomn)

            except StopIteration:
                # смещение ответов на один вверх.
                list_answer.append(message.text)
                list_answer.pop(0)
                ind = 0
                for key in dict_columns.keys():
                    dict_columns[key] = list_answer[ind]
                    ind += 1
                weather = dict_columns|weather_data
                data_cursor.create_weather_table(message.from_user.id)
                functions.add_weather_table(message.from_user.id, weather)
                bot.send_message(message.from_user.id, 'Погода добавлена.')
        colomn(message)


    elif message.text.lower() in ['мои места', 'моя одежда', 'моя погода']:
        res, thing = data_cursor.get_user_things(message.from_user.id, message.text.lower())
        bot.send_message(message.from_user.id, f"{thing}:")
        [bot.send_message(message.from_user.id, item) for item in res]

    elif message.text.lower() in ['изменить место', 'изменить одежду', 'изменить погоду']:
        res, thing = data_cursor.change_user_things(message.from_user.id, message.text.lower())
        bot.send_message(message.from_user.id, f"{thing}:")
        [bot.send_message(message.from_user.id, item) for item in res]

    elif message.from_user.id == 187814413:
        bja = ['Любля', 'Супер-дупер любля', 'Мега БЖЯ', 'Цыпленочек',
               'Ты ж моя радость', 'Тефтелька вторниковая', 'Рыбонька лучистая'
               'Зайка моя', 'Любля любля любля']
        mess = lambda x: random.choice(bja)
        bot.send_message(message.from_user.id, mess(bja))

    else:
        print('else')
        bot.send_message(message.from_user.id, 'else')

bot.infinity_polling()
