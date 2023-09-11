import sqlite3
from datetime import datetime

# Ouverture de la connexion à la base de données
conn = sqlite3.connect('Archi_prix.db')

# Création d'un curseur pour exécuter des requêtes SQL
cur = conn.cursor()



cur.execute("SELECT * FROM data_archi order by archi")
rows = cur.fetchall()

data = {}
cout = 0
num = 0
got = 0
for row in rows:
    archi, date, prix = row
    if archi not in data:
        data[archi] = []
    data[archi].append((date,prix))
with open("archi_count",'r',encoding='utf-8') as f :
    archis = f.read().split('\n')
    for archi in data :
        if archi not in archis :
            cout += int(data[archi][-1][1])
            num += 1
        else:
            got += 1

print("\nEtat quête Dofus Ocre :")
print("Kamas pour finir: "+str(cout))
print("Nombre Archi-monstres manquant : "+str(num))
print("Nombre Archi-monstres possédé : "+str(got))

cur.close()