"""Фаил запросов к DB."""
import sqlite3


def conn_create(creator):
    connect = sqlite3.connect('banybase.db')
    cursor = connect.cursor()
    cursor.execute(creator)
    connect.commit()
    cursor.close()

def conn_insert(table_name, colomns_name, colomns_value):
    connect = sqlite3.connect('banybase.db')
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO {table_name} ({colomns_name}) VALUES ({colomns_value})")
    connect.commit()
    cursor.close()

def conn_select(table_name, columns, where='', order_by='', limit=''):
    connect = sqlite3.connect('banybase.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT {columns} FROM {table_name} {where} {order_by} {limit}")
    res = cursor.fetchall()
    connect.commit()
    cursor.close()
    return res


def create_location_table(id_telegram):
    creator = f'CREATE TABLE if not exists location_table_{id_telegram} (id_telegram INTEGER NOT NULL , id_location INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,' \
              f'location_name TEXT UNIQUE DEFAULT "home", location_coordinates TEXT DEFAULT "lat=0.0&lon=0.0" , ' \
              f'FOREIGN KEY (id_telegram) REFERENCES users(id_telegram) ON UPDATE CASCADE ON DELETE CASCADE);'
    conn_create(creator)

def create_clothes_table(id_telegram):
    creator = f'CREATE TABLE if not exists clothes_table_{id_telegram} (id_thing INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, id_telegram INTEGER NOT NULL , ' \
              f'clothes_name TEXT DEFAULT "thing", description TEXT , type_of_the_thing TEXT, photo TEXT NOT NULL DEFAULT "default_photo.png",' \
              f'wind INTEGER NOT NULL DEFAULT 0, rain INTEGER NOT NULL DEFAULT 0,' \
              f'cold INTEGER NOT NULL DEFAULT 0, warmly INTEGER NOT NULL DEFAULT 0,' \
              f'sun INTEGER NOT NULL DEFAULT 0,' \
              f'FOREIGN KEY (id_telegram)  REFERENCES users(id_telegram) ON UPDATE CASCADE ON DELETE CASCADE);'
    conn_create(creator)

def create_weather_table(id_telegram):
    creator = f'CREATE TABLE if not exists weather_table_{id_telegram} ' \
              f'(id_weather INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, id_telegram INTEGER NOT NULL, weather_description TEXT,' \
              f' weather_name TEXT,' \
              f'things_description TEXT, comments TEXT, time TEXT, temperature_2m INTEGER, apparent_temperature INTEGER,' \
              f'weathercode TEXT, relativehumidity INTEGER, surface_pressure INTEGER,' \
              f'windspeed_10m INTEGER, windgusts INTEGER,' \
              f'FOREIGN KEY (id_telegram)  REFERENCES users(id_telegram) ON UPDATE CASCADE ON DELETE CASCADE);'
    conn_create(creator)

def add_weather_table(id_telegram, weather_data):
    table_name = f"weather_table_{id_telegram}"
    colomns_name = 'id_telegram, weather_name, weather_description, things_description, comments, time,' \
                   ' temperature_2m, apparent_temperature, weathercode, relativehumidity,' \
                   ' surface_pressure, windspeed_10m, windgusts'
    quotes = list(map(lambda x: f"'{x}'", weather_data.values()))
    str_value = ', '.join(quotes)
    colomns_value = f"{id_telegram}, {str_value}"
    conn_insert(table_name, colomns_name, colomns_value)


def add_user(id_telegram, first_name, last_name):
    table_name = 'users'
    colomns_name = 'id_telegram, name_user'
    colomns_value = f"{id_telegram}, '{first_name} {last_name}'"
    conn_insert(table_name, colomns_name, colomns_value)

def add_user_location(id_telegram, location_name, location_coordinates):
    table_name = f"location_table_{id_telegram}"
    colomns_name = 'id_telegram, location_name, location_coordinates'
    colomns_value = f"{id_telegram}, '{location_name}', '{location_coordinates}'"
    conn_insert(table_name, colomns_name, colomns_value)

def add_user_clothes(id_telegram, dict_columns):
    table_name = f"clothes_table_{id_telegram}"
    colomns_name = 'id_telegram, clothes_name, description, type_of_the_thing, photo, wind, rain, cold, warmly, sun'
    quotes = list(map(lambda x: f"'{x}'", dict_columns.values()))
    str_value = ', '.join(quotes)
    colomns_value = f"{id_telegram}, {str_value}"
    conn_insert(table_name, colomns_name, colomns_value)

def get_user_things(id_telegramm, thing):
    things = {'мои места':{'table_name':'location', 'columns':'id_location, location_name', 'thing':'Ваши места'},
              'моя одежда':{'table_name':'clothes', 'columns':'id_thing, clothes_name, description', 'thing':'Ваша одежда'},
              'моя погода':{'table_name':'weather', 'columns':'id_weather, weather_name, apparent_temperature', 'thing':'Погода в списке'}}
    table_name = f"{things[thing]['table_name']}_table_{id_telegramm}"
    columns = things[thing]['columns']
    res = conn_select(table_name, columns)
    res = [list(map(str, item)) for item in res]
    res = ['   '.join(item) for item in res]
    res.insert(0, things[thing]['columns'].replace(', ', '   '))
    thing  = things[thing]['thing']
    return res, thing


def change_user_things(id_telegramm, thing):
    pass



if __name__ == '__main__':
    print(get_user_things(708055024, 'мои места'))


