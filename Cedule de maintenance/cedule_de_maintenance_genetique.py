import random

#les cas possible de maintenance pour 1 & 2
groupe1 = ['1100','0110','0011']
#les cas possible de maintenance pour 3 & 4 & 5 & 6 & 7
groupe2 = ['1000','0100','0010','0001']

nombre_individu = 10       # nombre d'individus dans une generation
max_generation = 30        # nombre de generations
capacite_maximum = 150
#capacité de chaque centrale electrique
capacite = [20,15,35,40,15,15,10]
#demande dans les 4 intervalles de l'année
intervalle = [80,90,65,70]


#pour creer un individu
def creation_individu():
    individu = []
    for i in range(7):
        if i < 2:
            individu.append(random.choice(groupe1))
        else:
            individu.append(random.choice(groupe2))
    return individu


#pour creer une generation
def createGeneration():
    generation = []
    for i in range(nombre_individu):
        generation.append(creation_individu())
    return generation


#fonction objectif : la plus petite reserve des 4 intervalles
def reserve(individu):
    plus_petite = 1000
    for k in range(4):                      # pour chaque intervalle
        perdue = 0
        for j in range(7):                  # pour chaque centrale
            perdue += int(individu[j][k]) * capacite[j]
        r = capacite_maximum - perdue - intervalle[k]
        if r < plus_petite:
            plus_petite = r
    if plus_petite < 0:                     # reserve negative -> performance 0
        return 0
    return plus_petite


#pour faire croisement
def croisement_point(parent1, parent2, position):
    enfant1 = parent1[:position] + parent2[position:]
    enfant2 = parent2[:position] + parent1[position:]
    return enfant1, enfant2


#pour faire mutation
def mutation(individu, position):
    if position < 2:
        individu[position] = random.choice(groupe1)
    else:
        individu[position] = random.choice(groupe2)
    return individu


#pour developper une generation (ajouter des enfants)
def developpement_generation(generation):
    position_croisement = random.randint(1, 6)
    position_mutation = random.randint(0, 6)
    enfant1, enfant2 = croisement_point(generation[0], generation[1], position_croisement)
    enfant3, enfant4 = croisement_point(generation[2], generation[3], position_croisement)
    generation.append(enfant1)
    generation.append(enfant2)
    generation.append(enfant3)
    generation.append(enfant4)
    generation.append(mutation(generation[0][:], position_mutation))


#pour faire selection : garder les meilleurs
def selection(generation):
    generation.sort(key=reserve, reverse=True)
    return generation[:nombre_individu]


def afficheGeneration(generation, nombreGeneration):
    print("Generation", nombreGeneration)
    nombre = 1
    for individu in generation:
        print(nombre, ')', individu, 'reserve :', reserve(individu))
        nombre += 1
    print()


# ---------- PROGRAMME PRINCIPAL ----------
nombre_generation = 1
generation = createGeneration()
generation = selection(generation)          # trier du meilleur au pire
afficheGeneration(generation, nombre_generation)

while nombre_generation < max_generation:
    developpement_generation(generation)
    generation = selection(generation)
    nombre_generation += 1

afficheGeneration(generation, nombre_generation)
print('le meilleur individu est :', generation[0])
print('le meilleur score est :', reserve(generation[0]))