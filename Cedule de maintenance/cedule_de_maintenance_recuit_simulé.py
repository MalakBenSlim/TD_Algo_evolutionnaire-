import random
import math

#les cas possible de maintenance pour 1 & 2
groupe1 = ['1100','0110','0011']
#les cas possible de maintenance pour 3 & 4 & 5 & 6 & 7
groupe2 = ['1000','0100','0010','0001']

capacite_maximum = 150
#capacité de chaque centrale electrique
capacite = [20,15,35,40,15,15,10]
#demande dans les 4 intervalles de l'année
intervalle = [80,90,65,70]

#parametres du recuit simule
temperature = 50        # temperature de depart
temperature_min = 0.01  # temperature d'arret
alpha = 0.95            # coefficient de refroidissement
nombre_essai = 20       # nombre d'essais pour chaque temperature


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


#pour creer un voisin : on change la maintenance d'une seule centrale
def voisin(individu):
    nouveau = individu[:]
    position = random.randint(0, 6)
    if position < 2:
        nouveau[position] = random.choice(groupe1)
    else:
        nouveau[position] = random.choice(groupe2)
    return nouveau


# ---------- PROGRAMME PRINCIPAL ----------
courant = creation_individu()
meilleur = courant[:]

while temperature > temperature_min:
    for i in range(nombre_essai):
        nouveau = voisin(courant)
        difference = reserve(nouveau) - reserve(courant)
        # on accepte si c'est meilleur
        # sinon on accepte avec une probabilite exp(difference / temperature)
        if difference >= 0 or random.random() < math.exp(difference / temperature):
            courant = nouveau
            if reserve(courant) > reserve(meilleur):
                meilleur = courant[:]
    temperature = temperature * alpha       # refroidissement

print('le meilleur individu est :', meilleur)
print('le meilleur score est :', reserve(meilleur))