from typing import List
import random

# Données de l'énoncé
couts = [[5, 3, 4],      # cout de transport de D1 vers M1, M2, M3
         [6, 7, 2]]      # cout de transport de D2 vers M1, M2, M3
stock = [8, 9]           # nombre de containers dans D1 et D2
demande = [4, 5, 8]      # demande de M1, M2, M3

# Chaque container demandé a un magasin de destination :
# [0,0,0,0, 1,1,1,1,1, 2,2,2,2,2,2,2,2]  (4 pour M1, 5 pour M2, 8 pour M3)
destination = []
for j in range(len(demande)):
    for k in range(demande[j]):
        destination.append(j)


def containers(couts: List[List[int]], stock: List[int], demande: List[int], nombre_individu: int, max_generation: int) -> List[int]:
    n = len(destination)
    # creer la premiere generation
    generation = []
    for i in range(nombre_individu):
        generation.append(generate_random_solution(n))
    generation = selection(generation, couts, nombre_individu)

    nombre_generation = 1
    while nombre_generation < max_generation:
        developpement_generation(generation)
        generation = selection(generation, couts, nombre_individu)
        nombre_generation += 1

    # le meilleur est au debut apres la selection
    return generation[0]


def generate_random_solution(n: int) -> List[int]:
    # solution[k] = depot (0 ou 1) qui livre le container k
    # 8 containers viennent de D1 et 9 de D2 : les stocks sont toujours respectes
    solution = [0] * stock[0] + [1] * stock[1]
    random.shuffle(solution)
    return solution


def calculate_cout(solution: List[int], couts: List[List[int]]) -> int:
    # cout total de transport
    cout = 0
    for k in range(len(solution)):
        cout += couts[solution[k]][destination[k]]
    return cout


#apres un croisement, le nombre de containers de D1 peut etre different de 8
#on corrige pour respecter les stocks
def reparer(solution: List[int]) -> List[int]:
    while solution.count(0) > stock[0]:
        k = random.choice([i for i in range(len(solution)) if solution[i] == 0])
        solution[k] = 1
    while solution.count(0) < stock[0]:
        k = random.choice([i for i in range(len(solution)) if solution[i] == 1])
        solution[k] = 0
    return solution


#pour faire croisement
def croisement_point(parent1: List[int], parent2: List[int], position: int):
    enfant1 = reparer(parent1[:position] + parent2[position:])
    enfant2 = reparer(parent2[:position] + parent1[position:])
    return enfant1, enfant2


#pour faire mutation : on echange deux containers de depots differents
def mutation(solution: List[int]) -> List[int]:
    i = random.choice([k for k in range(len(solution)) if solution[k] == 0])
    j = random.choice([k for k in range(len(solution)) if solution[k] == 1])
    solution[i], solution[j] = solution[j], solution[i]
    return solution


#pour developper une generation (ajouter des enfants)
def developpement_generation(generation: List[List[int]]):
    n = len(generation[0])
    # on choisit 4 parents au hasard dans la generation
    p1, p2, p3, p4 = random.sample(generation, 4)
    position_croisement = random.randint(1, n - 1)
    enfant1, enfant2 = croisement_point(p1, p2, position_croisement)
    enfant3, enfant4 = croisement_point(p3, p4, position_croisement)
    generation.append(enfant1)
    generation.append(enfant2)
    generation.append(enfant3)
    generation.append(enfant4)
    # mutation sur des copies de 4 individus au hasard
    for parent in random.sample(generation, 4):
        generation.append(mutation(parent[:]))


#pour faire selection : garder les meilleurs (cout le plus petit)
def selection(generation, couts, nombre_individu):
    generation.sort(key=lambda s: calculate_cout(s, couts))
    return generation[:nombre_individu]


def affiche_livraison(solution: List[int]):
    # tableau : nombre de containers livres de chaque depot a chaque magasin
    for i in range(2):
        ligne = []
        for j in range(3):
            nb = 0
            for k in range(len(solution)):
                if solution[k] == i and destination[k] == j:
                    nb += 1
            ligne.append(nb)
        print("D" + str(i + 1), "->", ligne, "(M1, M2, M3)")


resultat = containers(couts, stock, demande, 20, 50)
print("meilleure solution trouvee :", resultat)
affiche_livraison(resultat)
print("cout total :", calculate_cout(resultat, couts))