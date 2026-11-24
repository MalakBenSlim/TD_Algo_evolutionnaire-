from typing import List
import random
import math

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


def containers(couts: List[List[int]], stock: List[int], demande: List[int], temperature: float, temperature_min: float, alpha: float, nombre_essai: int) -> List[int]:
    n = len(destination)
    # solution de depart au hasard
    solution = generate_random_solution(n)
    cout = calculate_cout(solution, couts)
    # la meilleure solution trouvee jusqu'a present
    best_solution = solution[:]
    best_cout = cout  # on veut DIMINUER le cout

    while temperature > temperature_min:
        for i in range(nombre_essai):
            # creer un voisin : on echange le depot de deux containers
            voisin = generate_voisin(solution)
            cout_voisin = calculate_cout(voisin, couts)
            difference = cout_voisin - cout

            # on accepte si le cout diminue
            # sinon on accepte avec une probabilite exp(-difference / temperature)
            if difference <= 0 or random.random() < math.exp(-difference / temperature):
                solution = voisin
                cout = cout_voisin
                if cout < best_cout:
                    best_solution = solution[:]
                    best_cout = cout
        # refroidissement
        temperature = temperature * alpha

    return best_solution


def generate_random_solution(n: int) -> List[int]:
    # solution[k] = depot (0 ou 1) qui livre le container k
    # 8 containers viennent de D1 et 9 de D2 : les stocks sont toujours respectes
    solution = [0] * stock[0] + [1] * stock[1]
    random.shuffle(solution)
    return solution


def generate_voisin(solution: List[int]) -> List[int]:
    # on echange deux containers qui viennent de depots differents
    voisin = solution[:]
    i = random.choice([k for k in range(len(voisin)) if voisin[k] == 0])
    j = random.choice([k for k in range(len(voisin)) if voisin[k] == 1])
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin


def calculate_cout(solution: List[int], couts: List[List[int]]) -> int:
    # cout total de transport
    cout = 0
    for k in range(len(solution)):
        cout += couts[solution[k]][destination[k]]
    return cout


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


resultat = containers(couts, stock, demande, 50, 0.01, 0.95, 20)
print("meilleure solution trouvee :", resultat)
affiche_livraison(resultat)
print("cout total :", calculate_cout(resultat, couts))