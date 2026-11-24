from typing import List
import random


def sac_a_dos(valeurs: List[int], poids: List[int], capacite: int, tabou_length: int, max_iter: int) -> List[int]:
    # Initialiser la liste tabou et la meilleure solution trouvée jusqu'à présent
    tabou_list = []
    best_solution = []
    best_valeur = 0  # on veut AUGMENTER la valeur (dans le voyageur on diminuait la distance)
    iter_count = 0
    n = len(valeurs)

    while True:
        # Générer une solution aléatoire (exemple : [0, 1, 1, 0, 1])
        solution = generate_random_solution(n)
        # Calculer la valeur de la solution
        valeur = calculate_valeur(solution, valeurs, poids, capacite)

        # Si la valeur est meilleure que la meilleure trouvée, mettre à jour
        if valeur > best_valeur:
            best_solution = solution
            best_valeur = valeur

        # Ajouter la solution à la liste tabou
        tabou_list.append(solution)
        # Si la liste tabou est pleine, retirer le premier élément
        if len(tabou_list) > tabou_length:
            tabou_list.pop(0)

        # Incrémenter le compteur d'itérations
        iter_count += 1
        if iter_count >= max_iter:
            break

    return best_solution


def generate_random_solution(n: int) -> List[int]:
    # 1 = objet pris, 0 = objet non pris
    solution = []
    for i in range(n):
        choix = random.randint(0, 1)
        solution.append(choix)
    return solution


def calculate_valeur(solution: List[int], valeurs: List[int], poids: List[int], capacite: int) -> int:
    valeur = 0
    poids_total = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            valeur += valeurs[i]
            poids_total += poids[i]
    # Si le sac est trop lourd, la solution est refusée (valeur 0)
    if poids_total > capacite:
        return 0
    return valeur


# Données de l'image
valeurs = [4, 2, 2, 1, 10]
poids = [12, 2, 1, 1, 4]
capacite = 15

print("meilleure solution trouvee :", sac_a_dos(valeurs, poids, capacite, 5, 1000))