from typing import List
import random
import math


def sac_a_dos(valeurs: List[int], poids: List[int], capacite: int, nombre_particule: int, max_iteration: int, w: float, c1: float, c2: float) -> List[int]:
    n = len(valeurs)
    vitesse_max = 4

    # creer les particules : position (0/1 pour chaque objet) et vitesse
    positions = []
    vitesses = []
    for i in range(nombre_particule):
        positions.append(generate_random_solution(n))
        vitesses.append([random.uniform(-1, 1) for j in range(n)])

    # la meilleure position de chaque particule (pbest) et la meilleure du groupe (gbest)
    pbest = [p[:] for p in positions]
    pbest_valeur = [calculate_valeur(p, valeurs, poids, capacite) for p in positions]
    meilleur = pbest_valeur.index(max(pbest_valeur))
    gbest = pbest[meilleur][:]
    gbest_valeur = pbest_valeur[meilleur]

    for iteration in range(max_iteration):
        for i in range(nombre_particule):
            for d in range(n):
                r1 = random.random()
                r2 = random.random()
                # mise a jour de la vitesse
                vitesses[i][d] = (w * vitesses[i][d]
                                  + c1 * r1 * (pbest[i][d] - positions[i][d])
                                  + c2 * r2 * (gbest[d] - positions[i][d]))
                # limiter la vitesse
                vitesses[i][d] = max(-vitesse_max, min(vitesse_max, vitesses[i][d]))
                # mise a jour de la position : l'objet est pris avec la probabilite sigmoid(vitesse)
                if random.random() < sigmoid(vitesses[i][d]):
                    positions[i][d] = 1
                else:
                    positions[i][d] = 0

            valeur = calculate_valeur(positions[i], valeurs, poids, capacite)
            # mise a jour de pbest (on veut AUGMENTER la valeur)
            if valeur > pbest_valeur[i]:
                pbest[i] = positions[i][:]
                pbest_valeur[i] = valeur
                # mise a jour de gbest
                if valeur > gbest_valeur:
                    gbest = positions[i][:]
                    gbest_valeur = valeur

    return gbest


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


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


# Données de l'image
valeurs = [4, 2, 2, 1, 10]
poids = [12, 2, 1, 1, 4]
capacite = 15

resultat = sac_a_dos(valeurs, poids, capacite, 10, 50, 0.7, 1.5, 1.5)
print("meilleure solution trouvee :", resultat)
print("valeur :", calculate_valeur(resultat, valeurs, poids, capacite))