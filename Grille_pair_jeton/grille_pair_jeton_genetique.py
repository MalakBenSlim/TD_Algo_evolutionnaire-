import random

n = 5                      # la grille a n lignes et n colonnes
k = 10                     # nombre de jetons a placer (k < n*n)

nombre_individu = 50       # nombre d'individus dans une generation
max_generation = 300       # nombre de generations
fitness_max = 2 * n        # fitness d'une solution faisable (toutes les lignes et colonnes paires)


#pour creer un individu : une grille de n*n cases (1 = jeton, 0 = vide)
#avec exactement k jetons, a des positions au hasard
def creation_individu():
    individu = [0] * (n * n)
    for case in random.sample(range(n * n), k):
        individu[case] = 1
    return individu


#pour creer une generation
def createGeneration():
    generation = []
    for i in range(nombre_individu):
        generation.append(creation_individu())
    return generation


#fonction fitness : on compte les lignes et les colonnes qui ont un nombre impair de jetons
#fitness = 2n - (nombre de lignes impaires + nombre de colonnes impaires)
#plus elle est grande, meilleur est l'individu ; 2n veut dire solution faisable
def fitness(individu):
    impaires = 0
    for i in range(n):
        if sum(individu[i * n:(i + 1) * n]) % 2 == 1:        # ligne i
            impaires += 1
    for j in range(n):
        if sum(individu[j::n]) % 2 == 1:                       # colonne j
            impaires += 1
    return fitness_max - impaires


#apres un croisement, le nombre de jetons peut etre different de k
#on corrige pour avoir exactement k jetons
def reparer(individu):
    while sum(individu) > k:
        case = random.choice([c for c in range(n * n) if individu[c] == 1])
        individu[case] = 0
    while sum(individu) < k:
        case = random.choice([c for c in range(n * n) if individu[c] == 0])
        individu[case] = 1
    return individu


#pour faire croisement : le point de croisement est entre deux lignes de la grille
def croisement_point(parent1, parent2, position):
    enfant1 = reparer(parent1[:position * n] + parent2[position * n:])
    enfant2 = reparer(parent2[:position * n] + parent1[position * n:])
    return enfant1, enfant2


#pour faire mutation : on deplace un jeton vers une case vide
def mutation(individu):
    jeton = random.choice([c for c in range(n * n) if individu[c] == 1])
    vide = random.choice([c for c in range(n * n) if individu[c] == 0])
    individu[jeton] = 0
    individu[vide] = 1
    return individu


#pour developper une generation (ajouter des enfants)
def developpement_generation(generation):
    for i in range(10):
        # on choisit 2 parents au hasard dans la generation
        parent1, parent2 = random.sample(generation, 2)
        position_croisement = random.randint(1, n - 1)
        enfant1, enfant2 = croisement_point(parent1, parent2, position_croisement)
        generation.append(enfant1)
        generation.append(enfant2)
    for i in range(20):
        # mutation sur la copie d'un individu au hasard
        parent = random.choice(generation)
        generation.append(mutation(parent[:]))


#pour faire selection : garder les meilleurs
def selection(generation):
    generation.sort(key=fitness, reverse=True)
    return generation[:nombre_individu]


#pour afficher une grille
def afficheGrille(individu):
    for i in range(n):
        ligne = ''
        for j in range(n):
            if individu[i * n + j] == 1:
                ligne += ' o'
            else:
                ligne += ' .'
        print(ligne, '  jetons :', sum(individu[i * n:(i + 1) * n]))
    print('colonnes :', [sum(individu[j::n]) for j in range(n)])
    print()


def afficheGeneration(generation, nombreGeneration):
    print("Generation", nombreGeneration)
    nombre = 1
    for individu in generation[:5]:         # on affiche les 5 meilleurs
        print(nombre, ')', ''.join(str(b) for b in individu), 'fitness :', fitness(individu))
        nombre += 1
    print()


# ---------- PROGRAMME PRINCIPAL ----------
if k % 2 == 1:
    # la somme des jetons des lignes est k : si chaque ligne est paire, k est pair
    print("pas de solution : k doit etre pair")
else:
    nombre_generation = 1
    generation = createGeneration()
    generation = selection(generation)          # trier du meilleur au pire
    afficheGeneration(generation, nombre_generation)

    while nombre_generation < max_generation and fitness(generation[0]) < fitness_max:
        developpement_generation(generation)
        generation = selection(generation)
        nombre_generation += 1

    afficheGeneration(generation, nombre_generation)
    meilleur = generation[0]
    print('le meilleur individu est :', ''.join(str(b) for b in meilleur))
    print('le meilleur score est :', fitness(meilleur), 'sur', fitness_max)
    if fitness(meilleur) == fitness_max:
        print('solution faisable trouvee en', nombre_generation, 'generations')
    else:
        print('pas de solution faisable trouvee')
    print()
    afficheGrille(meilleur)