import requests
from selenium import webdriver
import re
import data_cursor
import datetime

def get_api_key_google():
    # Получение токена из файла.
    with open('/home/tixonyia/Рабочий стол/API key/Google', 'r') as file:
        str_key = file.read(46)
        return str_key


def add_user(message):
    try:
        data_cursor.add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    except Exception as err:
        print('functions.->data_cursor.add_user: ', err)
def add_user_clothes(message, dict_columns):
    # добавление одежды
    try:
        proprty_list = dict_columns['proprty_thing'].split(' ')
        proprty_names = ['wind', 'rain', 'cold', 'warmly', 'sun']
        proprty_dict = dict(zip(proprty_names, proprty_list))
        dict_columns.update(proprty_dict)
        del dict_columns['proprty_thing']
        data_cursor.add_user_clothes(message.from_user.id, dict_columns)
        return 'Добавлено'

    except Exception as err:
        print('functions.add_user_clothes: ', err)
        return 'Не могу добавить'

def create_table_clothes(message):
    # Необходимые таблицы
    try:
        data_cursor.create_clothes_table(message.from_user.id)
    except Exception as err:
        print('functions->data_cursor.create_clothes_table: ', err)



def add_user_location(id_telegram, location_name, location_coordinates):
    # вставка данных локации
    try:
        data_cursor.add_user_location(id_telegram, location_name, location_coordinates)
    except Exception as err:
        print('functions->data_cursor.add_table_location: ', err)
def create_table_location(message):
    # Необходимые таблицы
    try:
        data_cursor.create_location_table(message.from_user.id)
    except Exception as err:
        print('functions->data_cursor.create_location_table: ', err)

def add_weather_table(id_telegram, weather_data):
    try:
        data_cursor.add_weather_table(id_telegram, weather_data)
    except Exception as err:
        print('functions->addd_cursor.weather_table: ', err)


def get_coordinates(message_location):
    # Формирование окончания url для запроса в яндекс-погоду.
    lat = re.search(r'-?\d+\.\d+', message_location).group(0)
    lon = re.findall(r'-?\d+\.\d+', message_location)[-1]
    return lat, lon

def get_weather(loc='latitude=59.931181&longitude=30.418557'):
    # Получение всех html данных с Яндекс-погода
        now = datetime.datetime.now()
        now_time = now.hour
        url = f'https://api.open-meteo.com/v1/forecast?{loc}&hourly=temperature_2m,apparent_temperature,weathercode,relativehumidity_2m,surface_pressure,windspeed_10m,windgusts_10m&timezone=Europe%2FMoscow'
        req = requests.get(url)
        data_js = req.json()
        data = {}
        for key, val in data_js['hourly'].items():
            data[key] = val[now_time]
        weathercodes = {0: 'Чистое небо.',
                        1:'Преимущественно ясно.',
                        2:'Преимущественно ясно, переменная облачность.',
                        3:'Преимущественно ясно, переменная облачность.',
                        45:'Туман.', 48:'Изморозь.',
                        51:'Легкая морось.', 53:'Умеренная морось.',
                        55:'Морось плотной интенсивности.',
                        56:'Легкая ледяная морось.',
                        57:'Ледяная морось плотной интенсивности.',
                        61:'Слабый дождь.', 63:'Умеренный дождь.', 65:'Сильный дождь.',
                        66:'Легкий ледяной дождь.', 67:'Сильный ледяной дождь',
                        71:'Легкий снегопад.', 73:'Умеренный снегопад.',
                        75:'Сильный снегопад.', 77:'Снежные зерна',
                        80:'Слабый ливень.', 81:'Умеренный ливень.', 82:'Сильный ливень.',
                        85:'Слабый снег.', 86:'Сильный снег.',
                        95:'Гроза', 96:'Гроза со слабым градом', 99:'Гроза со сильным градом'
                        }
        data['weathercode'] = weathercodes[data['weathercode']]
        press = float(data['surface_pressure'])
        data['surface_pressure'] = int(press*0.750062)

        return data


def get_location_now():
    # Данные по геолокации. Название и тд. из html_data
    loc = get_weather.__defaults__[0]
    loc = re.findall(r'-?\d+\.\d+', loc)
    lat = loc[0]
    lon = loc[-1]
    now = datetime.datetime.now()
    now_time = now.time()
    key = get_api_key_google()
    req = requests.get(
        f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}2&key={key}&language=ru&result_type=street_address')
    req_j = req.json()
    if req_j['results'] != []:
        loc_now = {'loc_name': req_j['results'][0]['formatted_address'], 'loc_time': now_time}
    elif req_j['results'] == []:
        loc_now = {'loc_name': req_j['plus_code']['compound_code'], 'loc_time': now_time}
    else:
        print("Что-то с респом погоды.")

    if loc_now['loc_name'][0].isdigit():
        loc_now['loc_name'] = loc_now['loc_name'][8:]

    return loc_now

def driver_chrom_respons_after_load(text):
    url = text.split('\n')[-1]
    driver = webdriver.Chrome()
    driver.set_window_rect(x=0, y=0, width=0, height=0)
    driver.get(url)
    req = driver.page_source
    driver.close()
    return req

def get_url(message):
    try:
        if re.findall(r'https://yandex.ru/maps/', message.text):
            if re.findall(r'-?\d+\.\d+%2C-?\d+\.\d+', message.text):
                coordinates_mix = re.findall(r'-?\d+\.\d+%2C-?\d+\.\d+', message.text)
                coordinates_mix = coordinates_mix[0].split('%2C')
            else:
                req = driver_chrom_respons_after_load(message.text)
                coordinates_mix = re.search(r'-?\d+\.\d+%2C-?\d+\.\d+', req)
                coordinates_mix = coordinates_mix[0].split('%2C')
            print("Yandex")

        elif re.findall(r'https://maps.app.goo.gl', message.text) \
                or re.findall(r'https://goo.gl/maps', message.text) \
                or re.findall(r'https://www.google.ru/maps/', message.text) \
                or re.findall(r'https://www.google.com/maps/', message.text):
            print("GOOGLE")
            req = driver_chrom_respons_after_load(message.text)


            if re.findall(r'https://goo.gl/maps', message.text):
                req = driver_chrom_respons_after_load(message.text)
                start_url = re.findall(r'content=("https://\S*")', req)[0]
                coordinates_mix = re.findall(r'-?\d+\.\d+%2C-?\d+\.\d+', start_url)
                coordinates_mix = coordinates_mix[0].split('%2C')

            else:
                coordinats_dog = re.findall(r'@-?\d+\.\d+,? ?-?\d+\.\d+', req)
                coordinates_mix = re.findall('-?\d+\.\d+', coordinats_dog[0])
            coordinates_mix[0], coordinates_mix[1] = coordinates_mix[1], coordinates_mix[0]

        elif re.findall(r'https://2gis.ru/', message.text) or \
                re.findall(r'https://go.2gis.com/', message.text):
                req = driver_chrom_respons_after_load(message.text)
                start_url = re.findall(r'content=("https://\S*")', req)[0]
                coordinates_mix = re.findall(r'-?\d+\.\d+%2C-?\d+\.\d+', start_url)
                coordinates_mix = coordinates_mix[0].split('%2C')
                print("2GIS")


        elif re.findall(r'-?\d+\.\d+,? ?-?\d+\.\d+', message.text):
            coordinates_mix = re.search(r'-?\d+\.\d+,? ?-?\d+\.\d+', message.text)
            coordinates_mix = re.findall(r'-?\d+\.\d+', str(coordinates_mix))
            coordinates_mix[0], coordinates_mix[1] = coordinates_mix[1], coordinates_mix[0]

        lat = coordinates_mix[1]
        lon = coordinates_mix[0]
        loc = f'latitude={lat}&longitude={lon}'
        return loc

    except Exception:
        return 'Не могу вычеслить координаты.'

def near_val(hot, cold, temp):
    if not cold and not hot:
        raise TypeError('OOPS CLEARS DATAS!!!!')
    elif not cold:
        return hot
    elif not hot:
        return cold

    if (temp - cold[0][4]) < (hot[0][4] - temp):
        return cold
    elif (temp - cold[0][4]) == (hot[0][4] - temp):
        return cold
    else:
        return hot

def what_to_wear(id_telegram, weather):
    try:
        if not weather ['apparent_temperature']:
            return 'Не с чем сравнивать ('
        apparent_temperature = weather['apparent_temperature']
        table_name = f"weather_table_{id_telegram}"
        columns = 'id_weather, weather_name, things_description, comments, apparent_temperature, time'
        where_cold = f"WHERE apparent_temperature BETWEEN {apparent_temperature - 3} AND {apparent_temperature + 0.05}"
        where_hot = f"WHERE apparent_temperature BETWEEN {apparent_temperature} AND {apparent_temperature+3}"
        order_by = f"ORDER BY apparent_temperature"
        data_cold = data_cursor.conn_select(table_name, columns, where=where_cold, order_by=order_by, limit='DESC LIMIT 1')
        data_hot = data_cursor.conn_select(table_name, columns, where=where_hot, order_by=order_by, limit='LIMIT 1')
        near = near_val(data_hot, data_cold, apparent_temperature)
        res = dict(zip(columns.split(', '), near[0]))
        return res

    except Exception as err:
        print('function what_to_wear: ', err)
        return 'Ааааа не чего надеть!!! Ты ж тян-обожян!!! (нет схожей погоды)'



