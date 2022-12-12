from bs4 import BeautifulSoup
import re

import telebot
import requests
bot = telebot.TeleBot('Token_for_bot', threaded=False)


def get_coordinates(message_location):
        list_loc = re.findall('\d+\.\d+\,\d+\.\d+', message_location)
        lat = list_loc[0].split(',')[1]
        lon = list_loc[0].split(',')[0]
        loc= f"lat={lat}&lon={lon}"
        return loc
                    #"""if re.findall('\d+\.\d+\,\d+\.\d+', message.text):
                    #loc = localtion_now(message.text)
                        #bot.send_message(message.from_user.id, f'Kоординаты заданы: {loc}')"""

def get_data(loc="lat=59.931193608737843&lon=30.418711071833968"):
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


@bot.message_handler(content_types=['text', 'photo'])
def get_text_messages(message):
    if message.text.lower() == 'бжя':
        bot.send_message(message.from_user.id, "Бжя")
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

    elif re.findall('\d+\.\d+\,\d+\.\d+', message.text) :
        coordinates = get_coordinates(message.text)
        get_data.__defaults__ = (coordinates,)
        bot.send_message(message.from_user.id, re.findall('\d+\.\d+\,\d+\.\d+', message.text))

    elif re.findall('https://maps.app.goo.gl', message.text):
        url = message.text.split('\n')[1]
        req = requests.get(url)
        coordinates_mix = re.findall('\d+\.\d+', req.url)
        lon = coordinates_mix[1]
        lat = coordinates_mix[0]
        get_data.__defaults__ = (f"lat={lat}&lon={lon}",)
    else:
        print('else')
        print(message.text)
        bot.send_message(message.from_user.id, 'else')


bot.infinity_polling()
