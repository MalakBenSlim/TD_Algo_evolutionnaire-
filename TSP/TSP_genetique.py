from typing import List
import random


def voyageur_de_commerce(distances: List[List[int]], n: int, nombre_individu: int, max_generation: int) -> List[int]:
    # creer la premiere generation
    generation = []
    for i in range(nombre_individu):
        generation.append(generate_random_solution(n))
    generation = selection(generation, distances, nombre_individu)

    nombre_generation = 1
    while nombre_generation < max_generation:
        developpement_generation(generation)
        generation = selection(generation, distances, nombre_individu)
        nombre_generation += 1

    # le meilleur est au debut apres la selection
    return generation[0]


def generate_random_solution(n: int) -> List[int]:
    # Générer une solution aléatoire en mélangeant les villes
    cities = list(range(n))
    random.shuffle(cities)
    return cities


def calculate_distance(solution: List[int], distances: List[List[int]]) -> int:
    # Calculer la distance totale de la solution en parcourant chaque ville
    distance = 0
    for i in range(len(solution) - 1):
        distance += distances[solution[i]][solution[i + 1]]
    return distance


#pour faire croisement : on garde le debut du parent 1
#et on complete avec les villes qui manquent dans l'ordre du parent 2
#(comme ca chaque ville apparait une seule fois)
def croisement_point(parent1: List[int], parent2: List[int], position: int):
    enfant1 = parent1[:position]
    for ville in parent2:
        if ville not in enfant1:
            enfant1.append(ville)
    enfant2 = parent2[:position]
    for ville in parent1:
        if ville not in enfant2:
            enfant2.append(ville)
    return enfant1, enfant2


#pour faire mutation : on echange deux villes
def mutation(solution: List[int]) -> List[int]:
    i, j = random.sample(range(len(solution)), 2)
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
    # mutation sur des copies de 10 individus au hasard
    for parent in random.sample(generation, 10):
        generation.append(mutation(parent[:]))


#pour faire selection : garder les meilleurs (distance la plus petite)
def selection(generation, distances, nombre_individu):
    generation.sort(key=lambda s: calculate_distance(s, distances))
    return generation[:nombre_individu]


# Créer la matrice de distances à partir des données fournies
distances = [
[0, 12, 13, 15, 23, 25, 56, 27, 38, 29, 60, 32],
[12, 0, 23, 22, 34, 56, 24, 78, 79, 34, 23, 24],
[13, 23, 0, 25, 23, 19, 18, 42, 25, 23, 26, 331],
[15, 22, 25, 0, 12, 24, 38, 27, 38, 49, 69, 29],
[23, 34, 23, 12, 0, 54, 36, 71, 81, 19, 100, 22],
[25, 56, 19, 24, 54, 0, 16, 27, 26, 37, 105, 72],
[56, 24, 18, 38, 36, 16, 0, 18, 23, 24, 25, 261],
[27, 78, 42, 27, 71, 27, 18, 0, 18, 19, 30, 53],
[38, 79, 25, 38, 81, 26, 23, 18, 0, 29, 23, 221],
[29, 34, 23, 49, 19, 37, 24, 19, 29, 0, 22, 42],
[60, 23, 26, 69, 100, 105, 25, 30, 23, 22, 0, 36],
[32, 24, 33, 29, 22, 72, 26, 53, 22, 42, 36, 0]]

resultat = voyageur_de_commerce(distances, 12, 50, 500)
print("meilleur solution trouvee:", resultat)
print("distance :", calculate_distance(resultat, distances))