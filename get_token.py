import sqlite3

conn = sqlite3.connect('critical.db')
c = conn.cursor()
c.execute("SELECT token FROM token WHERE name='teamgen'")
tg_token = c.fetchone()[0]
conn.commit()
conn.close()
