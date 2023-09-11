import sqlite3
from datetime import datetime

# Ouverture de la connexion à la base de données
conn = sqlite3.connect('Archi_prix.db')

# Création d'un curseur pour exécuter des requêtes SQL
cur = conn.cursor()


# # Requête SQL pour modifier la colonne date
# Sélection de toutes les dates de la table à modifier
# cur.execute("SELECT date FROM data_archi")

# # Parcourir les résultats de la requête SQL
# for row in cur.fetchall():
#     # Convertir la date en objet datetime
#     try :
#         date = datetime.strptime(row[0], '%Y-%m-%d %H:%M')  # Si les secondes ne sont pas incluses
#     except ValueError:
#         continue
#     # Vérifier si les secondes sont déjà incluses
#     if date.second == 0:
#         # Ajouter les secondes à l'objet datetime
#         date = date.replace(second=0)

#         # Convertir l'objet datetime en une chaîne de caractères avec le format final
#         formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')

#         # Mettre à jour la date dans la base de données
#         cur.execute("UPDATE data_archi SET date = ? WHERE date = ?", (formatted_date, row[0]))

# # Enregistrer les modifications dans la base de données
# conn.commit()


# cur.execute('DELETE FROM data_archi WHERE DATE LIKE "2023-04-02"')
# Exécution d'une requête pour sélectionner tous les enregistrements de la table
# cur.execute("Update data_archi SET prix = REPLACE(prix, 'NULL', NULL) Where prix LIKE '%NULL%'")




# cur.execute("SELECT * from data_archi group by archi,date order by archi,date")

# # Récupération des résultats de la requête
# rows = cur.fetchall()

# # Parcours des enregistrements et affichage de leurs valeurs
# for row in rows:
#     print(row)

print("\nPrix moyen des Archi-monstres par dateTime :")
cur.execute("SELECT date,AVG(prix) from data_archi group by date")
rows = cur.fetchall()
for row in rows:
    print(row)


print("\nPrix du total par dateTime :")
cur.execute("SELECT date,SUM(prix) from data_archi group by date")
rows = cur.fetchall()
for row in rows:
    print(row)


print("\nArchi-monstres non présent en HDV par dateTime :")
cur.execute("SELECT * from data_archi GROUP BY archi,date HAVING prix is NULL order by archi,date ASC")
rows = cur.fetchall()
for row in rows:
    print(row)
# Fermeture de la connexion à la base de données

print("\nnombre d'Archi-monstres dans l'HDV par dateTime :")
cur.execute("SELECT date,count(archi) from data_archi group by date")
rows = cur.fetchall()
for row in rows:
    print(row)


cur.execute("SELECT DISTINCT archi from data_archi WHERE date = ( SELECT max(date) from data_archi) group by archi,date")
rows = cur.fetchall()

for i in range(len(rows)):
    rows[i] = rows[i][0]

print("\nArchi-monstres pas dans l'HDV au dernier scan:")
with open("liste_archi.txt",'r',encoding='utf8') as f:

    possibilities = f.read().split("\n")
    for elt in possibilities :
        if elt not in rows :
            print(elt)



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
with open("liste_poss.txt",'r',encoding='utf-8') as f :
    archis = f.read().split('\n')
    for archi in data :
        if archi not in archis :
            cout += int(data[archi][-1][1])
            num += 1
        else:
            print(archi)
            archis.remove(archi)
            got += 1
    print(archis)
print("\nEtat quête Dofus Ocre :")
print("Kamas pour finir: "+str(cout))
print("Nombre Archi-monstres manquant : "+str(num))
print("Nombre Archi-monstres possédé : "+str(got))

conn.commit()
conn.close()
