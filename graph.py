# Importer les modules nécessaires
import sqlite3
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots

# Connecter à la base de données
conn = sqlite3.connect('Archi_prix.db')

cur = conn.cursor()


# Création de la courbe avec le prix total du pack
traces = []
cur.execute("SELECT date,SUM(prix) from data_archi group by date ")
rows = cur.fetchall()
prix_tot = []
date = []
for elt in rows:
    prix_tot.append(elt[1])
    date.append(elt[0])

trace = go.Scatter(
        x = date,
        y = prix_tot,
        name = "Total",
        mode = 'lines+markers'
    )
traces.append(trace)

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

# Création d'une trace pour chaque architecture
for archi in data:
    trace = go.Scatter(
        x = data[archi]['dates'],
        y = data[archi]['prix'],
        name = archi,
        mode = 'lines+markers'
    )
    traces.append(trace)



# Création de la figure et génération du fichier HTML
fig = go.Figure(traces)
plot(fig, filename='evo_prix_mono.html')
