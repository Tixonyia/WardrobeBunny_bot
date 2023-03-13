"""Фаил 'ручной' работы с DB. Создание первой таблицы 'users'."""

import sqlite3

def conn(creator):
    connect = sqlite3.connect('banybase.db')
    cursor = connect.cursor()
    cursor.execute(creator)
    connect.commit()
    cursor.close()

def drop_tables(tables):
    for table in tables:
        creator = f'DROP TABLE IF EXISTS {table};'
        conn(creator)
def users_table_creator():
    creator = "CREATE TABLE if not exists users(id_telegram INTEGER  NOT NULL " \
              " UNIQUE ,name_user TEXT, location_default TEXT DEFAULT " \
              "'0.0, 0.0', PRIMARY KEY (id_telegram));"
    conn(creator)
def show_tables():
    connect = sqlite3.connect('banybase.db')
    cursor = connect.cursor()
    creator = "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
    tables = cursor.execute(creator)
    list_names = list(map(list, tables))
    list_names = sum(list_names, [])
    connect.commit()
    cursor.close()
    print(list_names)
    return list_names

def create_users_table():
    creator = "CREATE TABLE if not exists users(id_telegram INTEGER  NOT NULL " \
              " UNIQUE ,name_user TEXT, location_default TEXT DEFAULT " \
              "'0.0, 0.0', PRIMARY KEY (id_telegram));"
    conn(creator)

def create_location_table():
    creator = "CREATE TABLE if not exists location_table(id INTEGER NOT NULL , location_name" \
              " TEXT , location_coordinates TEXT , " \
              "FOREIGN KEY (id)  REFERENCES users(id_telegram) ON UPDATE CASCADE" \
              " ON DELETE CASCADE);"
    conn(creator)

def cleare_table(table_name):
    creator = f'DELETE FROM {table_name};'
    conn(creator)

comand = input('Comand: ')

match comand:
    case 'drop':
        tables = show_tables()
        drop_tables(tables)

    case 'show_tables':
        show_tables()

    case 'create_tables':
        create_users_table()
        #create_location_table()

    case 'clear':
        name = input("Название таблицы: ")
        cleare_table(name)