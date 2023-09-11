import cv2
import numpy as np
import pytesseract
import pyautogui
import time
import difflib
import sqlite3
from random import random

# Définir la zone initiale à capturer
x, y, width, height = 0, 0, 1500, 1000
scalex,scaley = 1,1
bool = True

pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"

# Fonction de rappel pour la détection de clic de souris
def mouse_callback(event, x_new, y_new, flags, param):
    global x, y, width, height,scalex,scaley

    # Si l'utilisateur a cliqué avec le bouton gauche de la souris, enregistrer la position de départ
    if event == cv2.EVENT_LBUTTONDOWN:
        x, y = x_new*scalex, y_new*scaley

    # Si l'utilisateur a relâché le bouton gauche de la souris, enregistrer la position finale et lancer la boucle de reconnaissance
    elif event == cv2.EVENT_LBUTTONUP:
        width, height = x_new*scalex - x, y_new*scaley - y
        cv2.destroyWindow('Selection')
        global bool
        bool = False
        return 

# Afficher une fenêtre pour la sélection de la zone de l'écran
cv2.namedWindow('Selection')



# Attacher la fonction de rappel à la fenêtre
cv2.setMouseCallback('Selection', mouse_callback)

# Boucle pour attendre que l'utilisateur sélectionne la zone de l'écran
while bool:
    # Capturer une image de l'écran
    screenshot = np.array(pyautogui.screenshot())
    scalex = len(screenshot)/720
    scaley = len(screenshot[0])/1280
    # Afficher la capture en temps réel dans la fenêtre OpenCV
    cv2.imshow('Selection', cv2.resize(screenshot,(1280,720)))

    # Attendre la touche 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fermer la fenêtre OpenCV pour la sélection de la zone de l'écran
cv2.destroyAllWindows()



with open("liste_archi.txt",'r',encoding='utf8') as f:

    possibilities = f.read().split("\n")
    n = 1
    cutoff = 0.7
    print(possibilities)

    compilation = dict.fromkeys(possibilities)
    # Boucle infinie pour effectuer la capture en continu sur la zone sélectionnée
    while True:
        pyautogui.press('pagedown')
        # Capturer la zone de l'écran définie
        screenshot = np.array(pyautogui.screenshot(region=(x, y, width, height)))

        # Convertir l'image capturée en noir et blanc pour améliorer la reconnaissance de texte
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Utiliser Tesseract pour effectuer la reconnaissance de texte en français
        text = pytesseract.image_to_string(screenshot_gray, lang='fra',config="--psm 1")

        groupes = list(filter(None, text.split('\n')))
        nombre_objet = len(groupes)//3
        names = groupes [:nombre_objet]
        prix = groupes[nombre_objet*2:]
        for i in range(len(names)):
            name = difflib.get_close_matches(names[i], possibilities, n, cutoff)
            if not name :
                continue
            name = name[0]
            try : 
                tp_prix = int(prix[i].replace(" ",''))
                if tp_prix == 8 :
                    continue
                if compilation[name] == None :
                    compilation[name] = tp_prix

                elif compilation[name] > tp_prix :
                    compilation[name] = tp_prix
            except ValueError:
                pass   
           
        # Afficher la capture en temps réel dans la fenêtre OpenCV
        cv2.imshow('Capture', screenshot)

        # Attendre la touche 'q' pour quitter
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Fermer la fenêtre OpenCV et terminer le programme
    cv2.destroyAllWindows()
print(compilation)

print("\n1.Sauvegrader les donnees")
choice = input("2. Annuler \n")
# Le dictionnaire que nous allons utiliser pour créer la base de données

# Nom de fichier pour la base de données
db_filename = "Archi_prix.db"

if choice == "1" :
    # Connexion à la base de données
    conn = sqlite3.connect(db_filename)

    # Création d'une table pour stocker les données
    conn.execute("""
    CREATE TABLE IF NOT EXISTS data_archi (
        archi TEXT NOT NULL,
        date DATE NOT NULL,
        prix int,
        PRIMARY KEY(archi,date)
    )
    """)

    # Ajout des données dans la base de données
    for key, value in compilation.items():
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        if value :
            conn.execute("""INSERT INTO data_archi (archi, date, prix) VALUES (?, ?, ?)""", (key, date, value))

    # Sauvegarde des modifications et fermeture de la connexion à la base de données
    conn.commit()
    conn.close()

    print("\n1. Créer les graphes")
    choice = input("2. Quitter \n")

    if choice =='1':
        import graph
        import multi_graph

if choice =='3' :
        # Connexion à la base de données
    conn = sqlite3.connect("db_test.db")

    # Création d'une table pour stocker les données
    conn.execute("""
    CREATE TABLE IF NOT EXISTS data_archi (
        archi TEXT NOT NULL,
        date DATE NOT NULL,
        prix int,
        PRIMARY KEY(archi,date)
    )
    """)

    # Ajout des données dans la base de données
    for key, value in compilation.items():
        date = time.strftime('%Y-%m-%d %H %M', time.localtime())
        if value :
            conn.execute("""INSERT INTO data_archi (archi, date, prix) VALUES (?, ?, ?)""", (key, date, value))

    # Sauvegarde des modifications et fermeture de la connexion à la base de données
    conn.commit()
    conn.close()