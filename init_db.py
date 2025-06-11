import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO hotspots (call_number, phone_number, is_disabled) VALUES (?,?,?)", ('ECPL 56B', '1234', False))
cur.execute("INSERT INTO hotspots (call_number, phone_number, is_disabled) VALUES (?,?,?)", ('ECPL 70', '4321', True))

connection.commit()
connection.close()