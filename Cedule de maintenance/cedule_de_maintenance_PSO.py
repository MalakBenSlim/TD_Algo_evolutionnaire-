import random

#les cas possible de maintenance pour 1 & 2
groupe1 = ['1100','0110','0011']
#les cas possible de maintenance pour 3 & 4 & 5 & 6 & 7
groupe2 = ['1000','0100','0010','0001']

nombre_particule = 20      # nombre de particules
max_iteration = 50         # nombre d'iterations
w = 0.7                    # inertie
c1 = 1.5                   # confiance en sa meilleure position (pbest)
c2 = 1.5                   # confiance en la meilleure position du groupe (gbest)

capacite_maximum = 150
#capacité de chaque centrale electrique
capacite = [20,15,35,40,15,15,10]
#demande dans les 4 intervalles de l'année
intervalle = [80,90,65,70]


#nombre de choix possibles pour chaque centrale
def nombre_choix(j):
    if j < 2:
        return len(groupe1)
    return len(groupe2)


#une particule a 7 positions (une par centrale) : chaque position est un nombre
#entre 0 et (nombre de choix - 1) ; on l'arrondit pour trouver le cas de maintenance
#ex : position 1.7 -> arrondi 2 -> troisieme cas possible
def decoder(position):
    individu = []
    for j in range(7):
        indice = int(round(position[j]))
        if j < 2:
            individu.append(groupe1[indice])
        else:
            individu.append(groupe2[indice])
    return individu


#fonction objectif : la plus petite reserve des 4 intervalles
def reserve(position):
    individu = decoder(position)
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


#pour creer une particule : position et vitesse au hasard
def creation_particule():
    position = []
    vitesse = []
    for j in range(7):
        position.append(random.uniform(0, nombre_choix(j) - 1))
        vitesse.append(random.uniform(-1, 1))
    return position, vitesse


# ---------- PROGRAMME PRINCIPAL ----------
positions = []
vitesses = []
for i in range(nombre_particule):
    position, vitesse = creation_particule()
    positions.append(position)
    vitesses.append(vitesse)

# la meilleure position de chaque particule (pbest) et la meilleure du groupe (gbest)
pbest = [p[:] for p in positions]
pbest_valeur = [reserve(p) for p in positions]
meilleur = pbest_valeur.index(max(pbest_valeur))
gbest = pbest[meilleur][:]
gbest_valeur = pbest_valeur[meilleur]

for iteration in range(1, max_iteration + 1):
    for i in range(nombre_particule):
        for j in range(7):
            r1 = random.random()
            r2 = random.random()
            # mise a jour de la vitesse
            vitesses[i][j] = (w * vitesses[i][j]
                              + c1 * r1 * (pbest[i][j] - positions[i][j])
                              + c2 * r2 * (gbest[j] - positions[i][j]))
            # mise a jour de la position
            positions[i][j] = positions[i][j] + vitesses[i][j]
            # on reste dans les limites (0 .. nombre de choix - 1)
            if positions[i][j] < 0:
                positions[i][j] = 0
                vitesses[i][j] = 0
            if positions[i][j] > nombre_choix(j) - 1:
                positions[i][j] = nombre_choix(j) - 1
                vitesses[i][j] = 0

        valeur = reserve(positions[i])
        # mise a jour de pbest (on veut AUGMENTER la reserve)
        if valeur > pbest_valeur[i]:
            pbest[i] = positions[i][:]
            pbest_valeur[i] = valeur
            # mise a jour de gbest
            if valeur > gbest_valeur:
                gbest = positions[i][:]
                gbest_valeur = valeur

    if iteration % 10 == 0:
        print('iteration', iteration, ': meilleure reserve =', gbest_valeur)

print()
print('le meilleur individu est :', decoder(gbest))
print('le meilleur score est :', gbest_valeur)