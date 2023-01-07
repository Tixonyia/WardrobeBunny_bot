from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
import telebot
import requests
import data_cursor
from selenium import webdriver
import time


def token():
    with open('/home/tixonyia/Рабочий стол/Bunny/Token', 'r') as file:
        str_token = file.read(46)
    return str_token

bot = telebot.TeleBot(token(), threaded=False)


def get_coordinates(message_location):
        lat = re.search(r'-?\d+\.\d+', message_location).group(0)  # широта
        lon = re.findall(r'-?\d+\.\d+', message_location)[-1]
        print(lat, lon)
        loc= f"lat={lat}&lon={lon}"
        loc =loc.replace(' ', '')
        print(loc)
        return loc

def get_data(loc="lat=59.931193608737843&lon=30.418711071833968"):
    print(loc)
    page_data = requests.get(f'https://yandex.ru/pogoda/?{loc}')
    html_data = BeautifulSoup(page_data.text, "html.parser")
    return html_data


def get_temperature_now(html_data):
    div_temperature = html_data.find('div', "fact__temp-wrap")
    temperature_thermometer = div_temperature.findAll('span', 'temp__value_with-unit')[0].text
    day_anchor = div_temperature.find('div', 'day-anchor').text
    temperature_feeling = div_temperature.findAll('span', 'temp__value_with-unit')[1].text
    temperature_now = {"temperature_thermometer" : temperature_thermometer,
              "day_anchor" : day_anchor,
              "temperature_feeling" : temperature_feeling}
    return temperature_now


def get_weather_now(html_data):
    div_weather = html_data.find('div', "fact__props")
    wind = div_weather.findAll('span', "a11y-hidden")[0].text
    humidity = div_weather.findAll('span', "a11y-hidden")[1].text
    pressure = div_weather.findAll('span', "a11y-hidden")[2].text
    weather_now = {'wind': wind, 'humidity': humidity, 'pressure': pressure}
    return weather_now


def get_location_now(html_data):
    div_location = html_data.find('div', "fact__title")
    loc_name = div_location.find('h1', "title_level_1").text
    loc_time = div_location.find('time', "fact__time").text
    loc_now = {'loc_name': loc_name, 'loc_time': loc_time}
    return loc_now

def create_table(message):
    try:
        data_cursor.add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    except Exception as err:
        print('add_user: ', err)
    try:
        data_cursor.create_location_table(message.from_user.id)
    except Exception as err:
        print('create_location_table: ', err)
    try:
        data_cursor.create_clothes_table(message.from_user.id)
    except Exception as err:
        print('create_clothes_table: ', err)
    try:
        data_cursor.add_user_location(message.from_user.id, location_name='home', location_coordinates='0.0, 0.0')
        print("I happy because you are with us")
    except Exception as err:
        print('add_user: ', err)
@bot.message_handler(content_types=['text', 'photo'])
def get_text_messages(message):
    create_table(message)
    if message.text.lower() == 'бжя':
        bot.send_message(message.from_user.id, "Бжя")
    elif message.text.lower() == 'лагмань' :
        bot.send_message(message.from_user.id, "логмань, позжалуйста")
    elif message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, "Привет)")
        bot.send_message(message.from_user.id, "Я только создан, но уже"
                                               " могу рассказать о погоде: \n"
                                               "Просто набери 'погода' или 'ветер.'")

    elif message.text.lower() == 'погода':
        html_data = get_data()
        location = get_location_now(html_data)
        temperature = get_temperature_now(html_data)
        text = f"{location['loc_name']}. {location['loc_time']} \n"\
               f"На улице {temperature['temperature_thermometer']}°C. " \
               f"{temperature['day_anchor']}. " \
               f"Ощущается как {temperature['temperature_feeling']}°C."
        bot.send_message(message.from_user.id, text)

    elif message.text.lower() == 'ветер':
        html_data = get_data()
        weather = get_weather_now(html_data)
        text = f"За бортом: \n" \
               f"{weather['wind']} \n" \
               f"{weather['humidity']} \n" \
               f"{weather['pressure']}"
        bot.send_message(message.from_user.id, text)


    elif re.findall(r'https://yandex.ru/maps/', message.text):
        if re.findall(r'-?\d+\.\d+%2C-?\d+\.\d+', message.text):
            print(message.text)
            coordinates_mix = re.findall(r'-?\d+\.\d+%2C-?\d+\.\d+', message.text)
            coordinates_mix = coordinates_mix[0].split('%2C')
        else:
            url = message.text
            url = message.text.split('\n')[-1]
            driver = webdriver.Chrome()
            driver.get(url)
            req = driver.page_source
            coordinates_mix = re.search(r'-?\d+\.\d+%2C-?\d+\.\d+', req)
            coordinates_mix = coordinates_mix[0].split('%2C')
        lat = coordinates_mix[1]
        lon = coordinates_mix[0]
        get_data.__defaults__ = (f"lat={lat}&lon={lon}",)
        mess = get_data.__defaults__
        bot.send_message(message.from_user.id, mess)
        print("Yandex")
        #bot.send_message(message.from_user.id, 'Yandex даёт говно ссылку с проверкой ботов. Дай тогда координаты в формате "Yandex: координаты"')

    elif re.findall(r'https://maps.app.goo.gl', message.text) \
            or re.findall('https://goo.gl/maps', message.text) \
            or re.findall('https://www.google.ru/maps/', message.text):
        url = message.text.split('\n')[-1]
        driver = webdriver.Chrome()
        driver.get(url)
        req = driver.page_source
        coordinats_dog = re.findall(r'@-?\d+\.\d+,? ?-?\d+\.\d+', req)
        coordinates_mix = re.findall('-?\d+\.\d+', coordinats_dog[0])
        lon = coordinates_mix[1]
        lat = coordinates_mix[0]
        get_data.__defaults__ = (f"lat={lat}&lon={lon}",)
        mess = get_data.__defaults__
        bot.send_message(message.from_user.id, mess)
        print("GOOGLE")

    elif re.findall('https://2gis.ru/', message.text) or \
            re.findall('https://go.2gis.com/', message.text):
        try:
            url = message.text.split('\n')[-1]
            driver = webdriver.Chrome()
            driver.get(url)
            req = driver.page_source
            start_url = re.findall(r'"startURL":("https://\S*")', req)[0]
            coordinates_mix = re.findall(r'-?\d+\.\d+%2C-?\d+\.\d+', start_url)
            coordinates_mix = coordinates_mix[0].split('%2C')
            lat = coordinates_mix[1]
            lon = coordinates_mix[0]
            get_data.__defaults__ = (f"lat={lat}&lon={lon}",)
            mess = get_data.__defaults__
            bot.send_message(message.from_user.id, mess)
            print("2GIS")

        except Exception as err:
            print(err)
            bot.send_message(message.from_user.id, 'Error 2gis')

    elif re.findall(r'-?\d+\.\d+,? ?-?\d+\.\d+', message.text):  # координаты=числа
        print('number')
        coordinates = get_coordinates(message.text)
        get_data.__defaults__ = (coordinates,)
        bot.send_message(message.from_user.id, get_data.__defaults__)

    elif message.text.lower() == 'добавить отметку':
        bot.send_message(message.from_user.id, 'Название?')

    else:
        print('else')
        print(message.text)
        bot.send_message(message.from_user.id, 'else')

bot.infinity_polling()
