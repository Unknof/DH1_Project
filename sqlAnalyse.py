import sqlite3

db = sqlite3.connect("Monster.db")

c = db.cursor()

c.execute("SELECT Name FROM Monster WHERE CR = '1/4'")
result = c.fetchall()
print(result)