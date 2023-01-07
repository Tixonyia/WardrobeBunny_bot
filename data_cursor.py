import sqlite3

def conn(creator):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(creator)
    connect.commit()
    cursor.close()

def create_location_table(user_id):
    creator = f'CREATE TABLE if not exists location_table_{user_id} (id INTEGER NOT NULL , ' \
              f'location_name TEXT UNIQUE, location_coordinates TEXT , ' \
              f'FOREIGN KEY (id)  REFERENCES users(id_telegram) ON UPDATE CASCADE ON DELETE CASCADE);'
    conn(creator)

def create_clothes_table(user_id):
    creator = f'CREATE TABLE if not exists clothes_{user_id} (id_thing INTEGER AUTO_INCREMENT, id INTEGER NOT NULL , ' \
              f'clothes_name TEXT DEFAULT "thing", description TEXT , parts_of_the_body TEXT, photo TEXT NOT NULL DEFAULT "default_photo.png",' \
              f'wind INTEGER NOT NULL DEFAULT 0, rain INTEGER NOT NULL DEFAULT 0,' \
              f'cold INTEGER NOT NULL DEFAULT 0, warmly INTEGER NOT NULL DEFAULT 0,' \
              f'sun INTEGER NOT NULL DEFAULT 0,' \
              f'FOREIGN KEY (id)  REFERENCES users(id_telegram) ON UPDATE CASCADE ON DELETE CASCADE);'
    conn(creator)
def add_user(id_telegram, first_name, last_name):
    creator = f"INSERT INTO users (id_telegram, name_user) VALUES ({id_telegram}, '{first_name} {last_name}')"
    conn(creator)

def add_user_location(id_telegram, location_name, location_coordinates):
    creator = f"INSERT INTO location_table_{id_telegram} (id, location_name, location_coordinates) VALUES ({id_telegram}, '{location_name}', '{location_coordinates}');"
    conn(creator)

