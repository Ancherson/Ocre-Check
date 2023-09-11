import sqlite3
import statistics

conn = sqlite3.connect('Archi_prix.db')

# Création d'un curseur pour exécuter des requêtes SQL
cur = conn.cursor()

with open("archi_étape.txt",'r',encoding='utf-8') as f:
    texte = f.read().split('\n')
    dic = {elt[:-3]:elt[-2:] for elt in texte}

cur.execute("SELECT DISTINCT archi,prix from data_archi WHERE date = ( SELECT max(date) from data_archi)")
rows = cur.fetchall()

dic2 = {i : [] for i in range(20,35) }

for elt in rows :
    dic2[int(dic[elt[0]])].append(int(elt[1]))

for i in range(20,35) :
    print(f"Etape {i}:   {statistics.mean(dic2[i])}")

cur.execute("SELECT AVG(prix) from data_archi WHERE date = ( SELECT max(date) from data_archi) group by date")
rows = cur.fetchall()
print(f"Total AVG:  {rows[0][0]}")

cur.close()
    