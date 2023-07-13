import sqlite3 

# This file is to start the database and add a starting link if it wasn't yet started 

link = input("Please enter a valid wikipedia link:\t")

conn = sqlite3.connect("data.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS wiki (id INTEGER PRIMARY KEY AUTOINCREMENT, link VARCHAR(100) UNIQUE, page TEXT DEFAULT(NULL));")
conn.commit()
cur.execute("INSERT OR IGNORE INTO wiki (link) VALUES (?)", (link,))
conn.commit()