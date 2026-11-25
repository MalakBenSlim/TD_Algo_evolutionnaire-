# TD4 - Exercice 3
import random

c1 = random.uniform(0.4, 0.9)    # inertie
c2 = random.uniform(1, 2.5)      # cognitif
c3 = random.uniform(1, 2.5)      # social
a = random.randint(-10, 1)       # borne inférieure
b = random.randint(3, 10)        # borne supérieure

print("c1 =", round(c1, 2), "c2 =", round(c2, 2), "c3 =", round(c3, 2))
print("intervalle = [", a, ",", b, "]")


def f(x):
    return -x ** 2 + 4 * x


def borner(x):
    return max(a, min(b, x))


# Question 1 : première itération (r1 = r2 = 1)
print("\n=== Question 1 ===")
x = [round(random.uniform(a, b), 2) for i in range(3)]
v = [0, 0, 0]
pbest = x[:]
gbest = max(pbest, key=f)
print("x0 =", x, " gbest =", gbest)

for i in range(3):
    v[i] = c1 * v[i] + c2 * (pbest[i] - x[i]) + c3 * (gbest - x[i])
    x[i] = borner(x[i] + v[i])
    if f(x[i]) > f(pbest[i]):
        pbest[i] = x[i]
gbest = max(pbest, key=f)
print("v1 =", v)
print("x1 =", x)
print("pbest1 =", pbest, " gbest1 =", gbest)


#Question 2 : PSO complet 
print("\n=== Question 2 ===")
n = random.randint(10, 30)        # particules
t_max = random.randint(50, 150)   # itérations
vmax = (b - a) / 5

x = [random.uniform(a, b) for i in range(n)]
v = [random.uniform(-vmax, vmax) for i in range(n)]
pbest = x[:]
gbest = max(pbest, key=f)

for t in range(t_max):
    for i in range(n):
        r1 = random.random()
        r2 = random.random()
        v[i] = c1 * v[i] + c2 * r1 * (pbest[i] - x[i]) + c3 * r2 * (gbest - x[i])
        v[i] = max(-vmax, min(vmax, v[i]))
        x[i] = borner(x[i] + v[i])
        if f(x[i]) > f(pbest[i]):
            pbest[i] = x[i]
    gbest = max(pbest, key=f)

print("n =", n, " t_max =", t_max)
print("gbest =", round(gbest, 4), " f(gbest) =", round(f(gbest), 4))
print("Optimum théorique : x = 2, f = 4")