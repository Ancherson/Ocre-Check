# Importer les modules nécessaires
import sqlite3
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots


fig = make_subplots(rows=2, cols=1)

# Connecter à la base de données
conn = sqlite3.connect('Archi_prix.db')

cur = conn.cursor()

# Récupération des données de la table
cur.execute("SELECT * FROM data_archi order by archi")
rows = cur.fetchall()

# Création d'un dictionnaire pour stocker les données de chaque architecture
data = {}
for row in rows:
    archi, date, prix = row
    if archi not in data:
        data[archi] = {'dates': [], 'prix': []}
    data[archi]['dates'].append(date)
    data[archi]['prix'].append(prix)


# Création du subplot pour chaque architecture
fig = make_subplots(rows=len(data)+2, cols=1, subplot_titles= ["Pack_archi"]+list(data.keys()))

# Ajout du prix total en premier

cur.execute("SELECT date,SUM(prix) from data_archi group by date")
rows = cur.fetchall()

prix_tot = []
date = []
for elt in rows:
    prix_tot.append(elt[1])
    date.append(elt[0])

tot = go.Scatter(
        x = date,
        y = prix_tot,
        name = "Total",
        mode = 'lines+markers'
    )
fig.add_trace(tot, row=1, col=1)


row = 2
for archi in data:
    # Création d'une trace pour chaque architecture
    trace = go.Scatter(
        x = data[archi]['dates'],
        y = data[archi]['prix'],
        name = archi,
        mode = 'lines+markers'
    )
    fig.add_trace(trace, row=row, col=1)
    row += 1

# Création du layout du graphique
fig.update_layout(
    title = 'Evolution des prix en fonction du temps pour chaque architecture',
    yaxis = {'title': 'Prix'},
    height=80000, 
)




# Création de la figure et génération du fichier HTML
plot(fig, filename='evo_prix_multi.html')
