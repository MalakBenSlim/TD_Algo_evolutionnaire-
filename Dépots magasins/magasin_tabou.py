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


def containers(couts: List[List[int]], stock: List[int], demande: List[int], tabou_length: int, max_iter: int) -> List[int]:
    n = len(destination)
    # Initialiser la liste tabou et la meilleure solution trouvée jusqu'à présent
    tabou_list = []
    solution = generate_random_solution(n)
    best_solution = solution[:]
    best_cout = calculate_cout(solution, couts)  # on veut DIMINUER le cout
    iter_count = 0

    while iter_count < max_iter:
        meilleur_voisin = None
        meilleur_mouvement = None
        meilleur_cout = float("inf")

        # regarder tous les voisins : echanger un container de D1 avec un container de D2
        for i in range(n):
            for j in range(n):
                if solution[i] == 0 and solution[j] == 1:
                    voisin = solution[:]
                    voisin[i], voisin[j] = voisin[j], voisin[i]
                    cout = calculate_cout(voisin, couts)
                    mouvement = (i, j)
                    # un mouvement tabou est interdit sauf s'il bat la meilleure solution
                    if mouvement in tabou_list and cout >= best_cout:
                        continue
                    if cout < meilleur_cout:
                        meilleur_cout = cout
                        meilleur_voisin = voisin
                        meilleur_mouvement = mouvement

        if meilleur_voisin is None:   # tous les voisins sont interdits
            break

        # on se deplace vers le meilleur voisin (meme s'il est moins bon)
        solution = meilleur_voisin
        # Ajouter le mouvement a la liste tabou (on interdit de l'annuler)
        tabou_list.append(meilleur_mouvement)
        # Si la liste tabou est pleine, retirer le premier élément
        if len(tabou_list) > tabou_length:
            tabou_list.pop(0)

        # Si le cout est meilleur que le meilleur trouvé, mettre à jour
        if meilleur_cout < best_cout:
            best_solution = solution[:]
            best_cout = meilleur_cout

        iter_count += 1

    return best_solution


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


resultat = containers(couts, stock, demande, 5, 100)
print("meilleure solution trouvee :", resultat)
affiche_livraison(resultat)
print("cout total :", calculate_cout(resultat, couts))