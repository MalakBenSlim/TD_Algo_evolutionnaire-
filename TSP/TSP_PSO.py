import random

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

n = 12
nombre_particule = 30
max_iteration = 300
w, c1, c2 = 0.3, 0.3, 0.3


def distance_totale(tournee):
    total = 0
    for i in range(n - 1):
        total += distances[tournee[i]][tournee[i + 1]]
    return total


def echanges_vers(a, b):
    # liste des echanges (i, j) qui transforment la tournee a en la tournee b
    a = a[:]
    echanges = []
    for i in range(n):
        if a[i] != b[i]:
            j = a.index(b[i])
            a[i], a[j] = a[j], a[i]
            echanges.append((i, j))
    return echanges


def appliquer(tournee, echanges):
    tournee = tournee[:]
    for i, j in echanges:
        tournee[i], tournee[j] = tournee[j], tournee[i]
    return tournee


# creation des particules
positions = []
vitesses = []
for i in range(nombre_particule):
    tournee = list(range(n))
    random.shuffle(tournee)
    positions.append(tournee)
    vitesses.append([])

# pbest = meilleure position de chaque particule, gbest = meilleure du groupe
pbest = [p[:] for p in positions]
pbest_dist = [distance_totale(p) for p in positions]
gbest = pbest[pbest_dist.index(min(pbest_dist))][:]
gbest_dist = min(pbest_dist)

for iteration in range(max_iteration):
    for i in range(nombre_particule):
        # nouvelle vitesse : on garde chaque ancien echange avec la probabilite w,
        # puis on ajoute ceux vers pbest (probabilite c1) et vers gbest (probabilite c2)
        nouvelle = [e for e in vitesses[i] if random.random() < w]
        nouvelle += [e for e in echanges_vers(positions[i], pbest[i]) if random.random() < c1]
        nouvelle += [e for e in echanges_vers(positions[i], gbest) if random.random() < c2]
        vitesses[i] = nouvelle

        # nouvelle position
        positions[i] = appliquer(positions[i], vitesses[i])

        # mise a jour de pbest et gbest (on veut diminuer la distance)
        d = distance_totale(positions[i])
        if d < pbest_dist[i]:
            pbest[i] = positions[i][:]
            pbest_dist[i] = d
            if d < gbest_dist:
                gbest = positions[i][:]
                gbest_dist = d

print("meilleure solution trouvee :", gbest)
print("distance :", gbest_dist)