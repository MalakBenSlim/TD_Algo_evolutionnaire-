# TD4 - Exercice 4 : sac à dos résolu par colonie de fourmis (ACO)
import random

# ---- Données du problème (à modifier) ----
valeurs = [60, 100, 120, 80, 30, 50, 90, 40]
poids = [10, 20, 30, 15, 5, 12, 25, 8]
C = 60
n = len(valeurs)

# ---- Paramètres de l'algorithme ----
m = 10        # nombre de fourmis
T = 100       # nombre d'itérations
alpha = 1     # importance de la phéromone
beta = 2      # importance de l'heuristique V/p
rho = 0.1     # taux d'évaporation
Q = 1         # quantité de phéromone déposée

# ---- Initialisation ----
tau = [1.0] * n                                   # phéromone de chaque objet
eta = [valeurs[i] / poids[i] for i in range(n)]   # visibilité = valeur / poids
meilleure = [0] * n
meilleure_val = 0

random.seed(1)

for t in range(T):
    solutions = []
    valeurs_sol = []

    # ---- Construction : chaque fourmi construit un sac ----
    for k in range(m):
        sol = [0] * n
        W = 0
        while True:
            # objets pas encore pris et qui rentrent dans le sac
            candidats = []
            for j in range(n):
                if sol[j] == 0 and W + poids[j] <= C:
                    candidats.append(j)
            if len(candidats) == 0:
                break

            # probabilité de choix proportionnelle à tau^alpha * eta^beta
            scores = []
            for j in candidats:
                scores.append(tau[j] ** alpha * eta[j] ** beta)

            # tirage à la roulette
            tirage = random.random() * sum(scores)
            cumul = 0
            choix = candidats[-1]
            for idx in range(len(candidats)):
                cumul = cumul + scores[idx]
                if cumul >= tirage:
                    choix = candidats[idx]
                    break

            sol[choix] = 1
            W = W + poids[choix]

        # valeur totale du sac
        Z = 0
        for j in range(n):
            if sol[j] == 1:
                Z = Z + valeurs[j]
        solutions.append(sol)
        valeurs_sol.append(Z)

        if Z > meilleure_val:
            meilleure_val = Z
            meilleure = sol[:]

    # ---- Évaporation ----
    for j in range(n):
        tau[j] = (1 - rho) * tau[j]

    # ---- Dépôt de phéromone ----
    for k in range(m):
        for j in range(n):
            if solutions[k][j] == 1:
                tau[j] = tau[j] + Q * valeurs_sol[k] / meilleure_val

# ---- Résultat ----
poids_total = 0
for j in range(n):
    if meilleure[j] == 1:
        poids_total = poids_total + poids[j]

print("Solution ACO   :", meilleure)
print("Objets choisis :", [j + 1 for j in range(n) if meilleure[j] == 1])
print("Valeur =", meilleure_val, " Poids =", poids_total, " (capacité", C, ")")

# ---- Vérification : énumération des 2^n solutions ----
optimum = 0
for code in range(2 ** n):
    V = 0
    P = 0
    for j in range(n):
        if (code >> j) & 1:
            V = V + valeurs[j]
            P = P + poids[j]
    if P <= C and V > optimum:
        optimum = V
print("Optimum exact (énumération) :", optimum)
