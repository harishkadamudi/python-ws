import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table_sql = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY  , username text, password text)"
cursor.execute(create_table_sql)

create_table_sql = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table_sql)

#cursor.execute("INSERT INTO items values('test',0.99)")

connection.commit()
connection.close()
