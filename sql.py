import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('logs.db')
cursor = conn.cursor()

# Executar uma consulta
cursor.execute("SELECT * FROM logs")

# Obter os resultados
rows = cursor.fetchall()
for row in rows:
    print(row)

# Fechar a conexão
conn.close()
