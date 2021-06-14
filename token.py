import sqlite3

conn = sqlite3.connect('critical.db')
c = conn.cursor()
c.execute("SELECT token FROM tokens WHERE key=1")
games_token = c.fetchone()[0]
conn.commit()
conn.close()
