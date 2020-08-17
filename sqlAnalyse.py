import sqlite3

db = sqlite3.connect("Monster.db")

c = db.cursor()

c.execute("SELECT DISTINCT Source FROM Monster")
result = c.fetchall()
print(result)