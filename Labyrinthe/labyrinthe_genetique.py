import random

# le labyrinthe : 0 = case blanche (libre), 1 = case tramee (mur)
# l'entree est la case (1,1) en haut a gauche, la sortie est la case (10,10) en bas a droite
labyrinthe = [
    "0100100000",
    "0100101111",
    "0000100000",
    "1110101010",
    "0000001010",
    "0011101010",
    "0100000010",
    "0101010000",
    "0101010111",
    "0101010000"]

entree = (0, 0)
sortie = (9, 9)

#les 4 deplacements possibles (un gene = 2 bits)
mouvements = {'00': (-1, 0),    # haut
              '01': (1, 0),     # bas
              '10': (0, -1),    # gauche
              '11': (0, 1)}     # droite
genes = ['00', '01', '10', '11']

nombre_individu = 100      # nombre d'individus dans une generation
max_generation = 500       # nombre de generations
nombre_genes = 30          # nombre de deplacements dans un individu


#distance reelle de chaque case jusqu'a la sortie (en tenant compte des murs)
#on part de la sortie et on avance case par case
def calcul_distances():
    distances = {sortie: 0}
    a_traiter = [sortie]
    while len(a_traiter) > 0:
        case = a_traiter.pop(0)
        for mouvement in mouvements.values():
            ligne = case[0] + mouvement[0]
            colonne = case[1] + mouvement[1]
            if 0 <= ligne <= 9 and 0 <= colonne <= 9:
                if labyrinthe[ligne][colonne] == '0' and (ligne, colonne) not in distances:
                    distances[(ligne, colonne)] = distances[case] + 1
                    a_traiter.append((ligne, colonne))
    return distances


distances = calcul_distances()
distance_max = distances[entree]     # distance entre l'entree et la sortie (18)


#pour creer un individu : une suite de 30 deplacements au hasard
def creation_individu():
    individu = []
    for i in range(nombre_genes):
        individu.append(random.choice(genes))
    return individu


#pour creer une generation
def createGeneration():
    generation = []
    for i in range(nombre_individu):
        generation.append(creation_individu())
    return generation


#le robot suit les deplacements de l'individu
#il s'arrete s'il se cogne contre un mur (ou sort du labyrinthe),
#s'il revient sur une case deja visitee, ou s'il atteint la sortie
def parcours(individu):
    position = entree
    visitees = [entree]
    pas = 0
    for gene in individu:
        ligne = position[0] + mouvements[gene][0]
        colonne = position[1] + mouvements[gene][1]
        if ligne < 0 or ligne > 9 or colonne < 0 or colonne > 9:
            break                                   # sort du labyrinthe
        if labyrinthe[ligne][colonne] == '1':
            break                                   # se cogne contre un mur
        if (ligne, colonne) in visitees:
            break                                   # revient sur une case deja visitee
        position = (ligne, colonne)
        visitees.append(position)
        pas += 1
        if position == sortie:
            break                                   # sortie atteinte
    return position, pas, visitees


#fonction fitness : plus elle est grande, meilleur est l'individu
def fitness(individu):
    position, pas, visitees = parcours(individu)
    if position == sortie:
        # sortie atteinte : on prefere le chemin le plus court
        return 100 + (nombre_genes - pas)
    # sinon : plus la case finale est proche de la sortie, meilleur est l'individu
    return distance_max - distances[position]


#pour faire croisement
def croisement_point(parent1, parent2, position):
    enfant1 = parent1[:position] + parent2[position:]
    enfant2 = parent2[:position] + parent1[position:]
    return enfant1, enfant2


#pour faire mutation : on remplace un deplacement par un autre au hasard
def mutation(individu, position):
    individu[position] = random.choice(genes)
    return individu


#pour developper une generation (ajouter des enfants)
def developpement_generation(generation):
    for i in range(10):
        # on choisit 2 parents au hasard dans la generation
        parent1, parent2 = random.sample(generation, 2)
        position_croisement = random.randint(1, nombre_genes - 1)
        enfant1, enfant2 = croisement_point(parent1, parent2, position_croisement)
        generation.append(enfant1)
        generation.append(enfant2)
    for i in range(20):
        # mutation sur la copie d'un individu au hasard
        parent = random.choice(generation)
        # on mute un deplacement que le robot a execute, ou celui qui l'a arrete
        # (les deplacements apres l'arret ne servent a rien)
        position, pas, visitees = parcours(parent)
        position_mutation = random.randint(0, min(pas, nombre_genes - 1))
        generation.append(mutation(parent[:], position_mutation))
    # quelques nouveaux individus au hasard pour garder de la diversite
    for i in range(5):
        generation.append(creation_individu())


#pour faire selection : garder les meilleurs
def selection(generation):
    generation.sort(key=fitness, reverse=True)
    return generation[:nombre_individu]


def afficheGeneration(generation, nombreGeneration):
    print("Generation", nombreGeneration)
    nombre = 1
    for individu in generation[:5]:         # on affiche les 5 meilleurs
        position, pas, visitees = parcours(individu)
        print(nombre, ')', ''.join(individu), 'fitness :', fitness(individu), '| pas :', pas)
        nombre += 1
    print()


#pour afficher le chemin du robot dans le labyrinthe
def afficheChemin(individu):
    position, pas, visitees = parcours(individu)
    for i in range(10):
        ligne = ''
        for j in range(10):
            if (i, j) in visitees:
                ligne += ' o'
            elif labyrinthe[i][j] == '1':
                ligne += ' #'
            else:
                ligne += ' .'
        print(ligne)
    print()


# ---------- PROGRAMME PRINCIPAL ----------
nombre_generation = 1
generation = createGeneration()
generation = selection(generation)          # trier du meilleur au pire
afficheGeneration(generation, nombre_generation)

while nombre_generation < max_generation:
    developpement_generation(generation)
    generation = selection(generation)
    nombre_generation += 1
    if fitness(generation[0]) > 100:        # sortie trouvee : on peut s'arreter
        break

afficheGeneration(generation, nombre_generation)
meilleur = generation[0]
position, pas, visitees = parcours(meilleur)
print('le meilleur individu est :', ''.join(meilleur))
print('le meilleur score est :', fitness(meilleur))
print('position finale :', (position[0] + 1, position[1] + 1), '| nombre de pas :', pas)
if position == sortie:
    print('le robot a atteint la sortie !')
else:
    print("le robot n'a pas atteint la sortie")
print()
afficheChemin(meilleur)