# TD4 - Exercice 3 : PSO pour maximiser f(x) = -x^2 + 4x sur [-5, 5]
import random

c1 = 0.8    # inertie
c2 = 2      # accélération cognitive
c3 = 2      # accélération sociale
a, b = -5, 5


def f(x):
    return -x ** 2 + 4 * x


def borner(x):
    # garder x dans [-5, 5]
    if x < a:
        return a
    if x > b:
        return b
    return x


# ---------------------------------------------------------------
# Question 1 : première itération à la main (avec r1 = r2 = 1)
# ---------------------------------------------------------------
print("=== Question 1 ===")
x = [2, 4, -1]
v = [0, 0, 0]

pbest = x[:]                 # a) pbest_i = x_i au départ
gbest = pbest[0]
for p in pbest:
    if f(p) > f(gbest):
        gbest = p            # b) meilleur pbest
print("pbest =", pbest)
print("gbest =", gbest)

for i in range(3):
    v[i] = c1 * v[i] + c2 * 1 * (pbest[i] - x[i]) + c3 * 1 * (gbest - x[i])
    x[i] = borner(x[i] + v[i])
    if f(x[i]) > f(pbest[i]):
        pbest[i] = x[i]
for p in pbest:
    if f(p) > f(gbest):
        gbest = p
print("v1 =", v)
print("x1 =", x)
print("pbest1 =", pbest)
print("gbest1 =", gbest)


# ---------------------------------------------------------------
# Question 2 : PSO complet avec n particules
# ---------------------------------------------------------------
print()
print("=== Question 2 ===")
n = 20          # nombre de particules
t_max = 100     # nombre d'itérations
vmax = 2

# Initialisation : positions et vitesses aléatoires
x = []
v = []
for i in range(n):
    x.append(random.uniform(a, b))
    v.append(random.uniform(-vmax, vmax))
pbest = x[:]
gbest = pbest[0]
for p in pbest:
    if f(p) > f(gbest):
        gbest = p

# Boucle principale
for t in range(t_max):
    for i in range(n):
        r1 = random.random()
        r2 = random.random()
        # mise à jour de la vitesse puis de la position
        v[i] = c1 * v[i] + c2 * r1 * (pbest[i] - x[i]) + c3 * r2 * (gbest - x[i])
        if v[i] > vmax:
            v[i] = vmax
        if v[i] < -vmax:
            v[i] = -vmax
        x[i] = borner(x[i] + v[i])
        # mise à jour de pbest et gbest
        if f(x[i]) > f(pbest[i]):
            pbest[i] = x[i]
        if f(pbest[i]) > f(gbest):
            gbest = pbest[i]

print("gbest =", round(gbest, 4), " f(gbest) =", round(f(gbest), 4))
print("Optimum théorique : x = 2, f = 4")
