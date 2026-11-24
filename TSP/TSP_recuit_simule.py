from typing import List
import random
import math


def voyageur_de_commerce(distances: List[List[int]], n: int, temperature: float, temperature_min: float, alpha: float, nombre_essai: int) -> List[int]:
    # solution de depart au hasard
    solution = generate_random_solution(n)
    distance = calculate_distance(solution, distances)
    # la meilleure solution trouvee jusqu'a present
    best_solution = solution[:]
    best_distance = distance  # on veut DIMINUER la distance

    while temperature > temperature_min:
        for i in range(nombre_essai):
            # creer un voisin : on echange deux villes
            voisin = generate_voisin(solution)
            distance_voisin = calculate_distance(voisin, distances)
            difference = distance_voisin - distance

            # on accepte si la distance diminue
            # sinon on accepte avec une probabilite exp(-difference / temperature)
            if difference <= 0 or random.random() < math.exp(-difference / temperature):
                solution = voisin
                distance = distance_voisin
                if distance < best_distance:
                    best_solution = solution[:]
                    best_distance = distance
        # refroidissement
        temperature = temperature * alpha

    return best_solution


def generate_random_solution(n: int) -> List[int]:
    # Générer une solution aléatoire en mélangeant les villes
    cities = list(range(n))
    random.shuffle(cities)
    return cities


def generate_voisin(solution: List[int]) -> List[int]:
    # on echange deux villes au hasard
    voisin = solution[:]
    i, j = random.sample(range(len(solution)), 2)
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin


def calculate_distance(solution: List[int], distances: List[List[int]]) -> int:
    # Calculer la distance totale de la solution en parcourant chaque ville
    distance = 0
    for i in range(len(solution) - 1):
        distance += distances[solution[i]][solution[i + 1]]
    return distance


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

resultat = voyageur_de_commerce(distances, 12, 100, 0.01, 0.95, 50)
print("meilleur solution trouvee:", resultat)
print("distance :", calculate_distance(resultat, distances))