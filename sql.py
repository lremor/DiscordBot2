import sqlite3

conn = sqlite3.connect('logs.db')

cursor = conn.cursor()
cursor.execute('''SELECT user, COUNT(*) as count
             FROM logs
             WHERE content LIKE '%https://gamersclub.com.br/%'
             GROUP BY user
             ORDER BY count DESC''')

rows = cursor.fetchall()
print("TOP LOBBYS MASTER:")
for row in rows:
    print(f'Nick: {row[0]}, Lobbys: {row[1]}')

conn.close()