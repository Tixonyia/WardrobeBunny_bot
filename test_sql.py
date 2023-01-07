import sqlite3

def conn(creator):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(creator)
    connect.commit()
    cursor.close()


def create_new_table():
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
def add_data():
    creator = "INSERT INTO users (id_telegram, name_user) VALUES (7080550299, 'Artem Vasilev');"
    conn(creator)

def select_data(id_telegram):
    creator = "SELECT id_telegram FROM users" # => обьект с кортежами типа "tuple" (12321,), (21312,)
    conn(creator)
if __name__ == '__main__':
    #add_data()
    create_new_table()
    #select_data()
    create_location_table()
    pass