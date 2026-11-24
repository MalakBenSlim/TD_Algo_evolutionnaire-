from typing import List
import random
import math


def sac_a_dos(valeurs: List[int], poids: List[int], capacite: int, temperature: float, temperature_min: float, alpha: float, nombre_essai: int) -> List[int]:
    n = len(valeurs)
    # solution de depart au hasard
    solution = generate_random_solution(n)
    valeur = calculate_valeur(solution, valeurs, poids, capacite)
    # la meilleure solution trouvee jusqu'a present
    best_solution = solution[:]
    best_valeur = valeur

    while temperature > temperature_min:
        for i in range(nombre_essai):
            # creer un voisin : on change un seul objet (pris <-> pas pris)
            voisin = generate_voisin(solution)
            valeur_voisin = calculate_valeur(voisin, valeurs, poids, capacite)
            difference = valeur_voisin - valeur   # on veut AUGMENTER la valeur

            # on accepte si c'est meilleur
            # sinon on accepte avec une probabilite exp(difference / temperature)
            if difference >= 0 or random.random() < math.exp(difference / temperature):
                solution = voisin
                valeur = valeur_voisin
                if valeur > best_valeur:
                    best_solution = solution[:]
                    best_valeur = valeur
        # refroidissement
        temperature = temperature * alpha

    return best_solution


def generate_random_solution(n: int) -> List[int]:
    # 1 = objet pris, 0 = objet non pris
    solution = []
    for i in range(n):
        solution.append(random.randint(0, 1))
    return solution


def generate_voisin(solution: List[int]) -> List[int]:
    voisin = solution[:]
    i = random.randint(0, len(solution) - 1)
    voisin[i] = 1 - voisin[i]
    return voisin


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


# Données de l'image
valeurs = [4, 2, 2, 1, 10]
poids = [12, 2, 1, 1, 4]
capacite = 15

resultat = sac_a_dos(valeurs, poids, capacite, 50, 0.01, 0.95, 20)
print("meilleure solution trouvee :", resultat)
print("valeur :", calculate_valeur(resultat, valeurs, poids, capacite))