import random

#les cas possible de maintenance pour 1 & 2
groupe1 = ['1100','0110','0011']
#les cas possible de maintenance pour 3 & 4 & 5 & 6 & 7
groupe2 = ['1000','0100','0010','0001']

capacite_maximum = 150
#capacité de chaque centrale electrique
capacite = [20,15,35,40,15,15,10]
#demande dans les 4 intervalles de l'année
intervalle = [80,90,65,70]

max_iteration = 100     # nombre d'iterations
taille_tabou = 5        # taille de la liste tabou


#pour creer une solution au hasard
def creation_individu():
    individu = []
    for i in range(7):
        if i < 2:
            individu.append(random.choice(groupe1))
        else:
            individu.append(random.choice(groupe2))
    return individu


#fonction objectif : la plus petite reserve des 4 intervalles
def reserve(individu):
    plus_petite = 1000
    for k in range(4):                      # pour chaque intervalle
        perdue = 0
        for j in range(7):                  # pour chaque centrale
            perdue += int(individu[j][k]) * capacite[j]
        r = capacite_maximum - perdue - intervalle[k]
        if r < plus_petite:
            plus_petite = r
    if plus_petite < 0:                     # reserve negative -> performance 0
        return 0
    return plus_petite


#pour avoir tous les voisins : on change la maintenance d'une seule centrale
#chaque voisin est accompagne de son mouvement (centrale, nouvelle valeur)
def tous_les_voisins(individu):
    liste = []
    for j in range(7):
        if j < 2:
            valeurs = groupe1
        else:
            valeurs = groupe2
        for v in valeurs:
            if v != individu[j]:
                nouveau = individu[:]
                nouveau[j] = v
                liste.append((nouveau, (j, v)))
    return liste


# ---------- PROGRAMME PRINCIPAL ----------
courant = creation_individu()
meilleur = courant[:]
liste_tabou = []        # mouvements interdits

for iteration in range(max_iteration):
    meilleur_voisin = None
    meilleur_mouvement = None
    meilleur_score = -1

    for nouveau, mouvement in tous_les_voisins(courant):
        score = reserve(nouveau)
        # un mouvement tabou est interdit sauf s'il bat le meilleur resultat
        if mouvement in liste_tabou and score <= reserve(meilleur):
            continue
        if score > meilleur_score:
            meilleur_score = score
            meilleur_voisin = nouveau
            meilleur_mouvement = mouvement

    if meilleur_voisin is None:     # tous les voisins sont interdits
        break

    # on interdit de revenir a l'ancienne valeur de la centrale
    j = meilleur_mouvement[0]
    liste_tabou.append((j, courant[j]))
    if len(liste_tabou) > taille_tabou:
        liste_tabou.pop(0)

    courant = meilleur_voisin
    if reserve(courant) > reserve(meilleur):
        meilleur = courant[:]

print('le meilleur individu est :', meilleur)
print('le meilleur score est :', reserve(meilleur))