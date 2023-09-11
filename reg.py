import re
with open('Hôtel de vente & Statistiques _ Vulbis.mhtml',encoding='utf8') as file :

    html = file.read()
    # Utilisation de la regex pour récupérer le contenu de la balise <tbody></tbody>
    reg = r"<tbody>([\s\S]*?)<\/tbody>"
    resultat =   re.findall(reg,html)

    pattern = r'<p.*?>(.*?)</p>'
    content = re.findall(pattern, resultat[0])
    print(content)

    # Affichage du résultat
    for elt in content :
        print(re.split(r'<span.*?>.*?</span>',elt))
        
    # for elt in content :
    #     print(elt)
