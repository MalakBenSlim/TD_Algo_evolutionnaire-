from typing import List
import random


def sac_a_dos(valeurs: List[int], poids: List[int], capacite: int, nombre_individu: int, max_generation: int) -> List[int]:
    n = len(valeurs)
    # creer la premiere generation
    generation = []
    for i in range(nombre_individu):
        generation.append(generate_random_solution(n))
    generation = selection(generation, valeurs, poids, capacite, nombre_individu)

    nombre_generation = 1
    while nombre_generation < max_generation:
        developpement_generation(generation)
        generation = selection(generation, valeurs, poids, capacite, nombre_individu)
        nombre_generation += 1

    # le meilleur est au debut apres la selection
    return generation[0]


def generate_random_solution(n: int) -> List[int]:
    # 1 = objet pris, 0 = objet non pris
    solution = []
    for i in range(n):
        solution.append(random.randint(0, 1))
    return solution


def calculate_valeur(solution: List[int], valeurs: List[int], poids: List[int], capacite: int) -> int:
    valeur = 0
    poids_total = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            valeur += valeurs[i]
            poids_total += poids[i]
    # Si le sac est trop lourd, la solution est refusee (valeur 0)
    if poids_total > capacite:
        return 0
    return valeur


#pour faire croisement
def croisement_point(parent1: List[int], parent2: List[int], position: int):
    enfant1 = parent1[:position] + parent2[position:]
    enfant2 = parent2[:position] + parent1[position:]
    return enfant1, enfant2


#pour faire mutation : on change un objet (pris <-> pas pris)
def mutation(solution: List[int], position: int) -> List[int]:
    solution[position] = 1 - solution[position]
    return solution


#pour developper une generation (ajouter des enfants)
def developpement_generation(generation: List[List[int]]):
    n = len(generation[0])
    position_croisement = random.randint(1, n - 1)
    position_mutation = random.randint(0, n - 1)
    enfant1, enfant2 = croisement_point(generation[0], generation[1], position_croisement)
    enfant3, enfant4 = croisement_point(generation[2], generation[3], position_croisement)
    generation.append(enfant1)
    generation.append(enfant2)
    generation.append(enfant3)
    generation.append(enfant4)
    generation.append(mutation(generation[0][:], position_mutation))


#pour faire selection : garder les meilleurs
def selection(generation, valeurs, poids, capacite, nombre_individu):
    generation.sort(key=lambda s: calculate_valeur(s, valeurs, poids, capacite), reverse=True)
    return generation[:nombre_individu]


# Données de l'image
valeurs = [4, 2, 2, 1, 10]
poids = [12, 2, 1, 1, 4]
capacite = 15

resultat = sac_a_dos(valeurs, poids, capacite, 10, 30)
print("meilleure solution trouvee :", resultat)
print("valeur :", calculate_valeur(resultat, valeurs, poids, capacite))