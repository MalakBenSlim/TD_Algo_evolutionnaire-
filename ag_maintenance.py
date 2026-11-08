"""
Problème d'ordonnancement de la maintenance de centrales électriques
résolu par Algorithme Génétique.

Encodage      : chromosome = 7 gènes de 4 bits (1 gène par unité, 1 bit par intervalle)
Fitness       : plus petite réserve sur les 4 intervalles (0 si réserve négative)
Sélection     : loterie (roulette proportionnelle à la fitness)
Croisement    : 1 point, uniquement aux frontières de gènes (blocs de 4 bits)
Mutation      : "inversion" (miroir d'un ou plusieurs blocs de 4 bits)
                ou "remplacement" (autre type, pour comparaison)
"""
import random

# ----------------------------------------------------------------- Données
CAPACITE = [20, 15, 35, 40, 15, 15, 10]      # MW par unité
DUREE = [2, 2, 1, 1, 1, 1, 1]                # nb d'intervalles de maintenance
DEMANDE = [80, 90, 65, 70]                   # MW par intervalle
N_UNITES, N_INTERV = len(CAPACITE), len(DEMANDE)
CAP_TOTALE = sum(CAPACITE)                   # 150 MW


def motifs_possibles(d, n=N_INTERV):
    """Blocs de n bits avec d '1' consécutifs (maintenance contiguë)."""
    return [tuple([0] * s + [1] * d + [0] * (n - s - d)) for s in range(n - d + 1)]


MOTIFS = [motifs_possibles(d) for d in DUREE]   # ex. unité 1 : 1100, 0110, 0011


# ----------------------------------------------------------- Chromosome
def individu_aleatoire():
    return [random.choice(MOTIFS[u]) for u in range(N_UNITES)]


def reserves(chrom):
    res = []
    for t in range(N_INTERV):
        perdue = sum(chrom[u][t] * CAPACITE[u] for u in range(N_UNITES))
        res.append(CAP_TOTALE - perdue - DEMANDE[t])
    return res


def fitness(chrom):
    return max(0, min(reserves(chrom)))


# ------------------------------------------------------------ Sélection
def selection_loterie(pop, fits):
    """Roulette : probabilité de tirage proportionnelle à la fitness."""
    total = sum(fits)
    if total == 0:                       # tous à 0 -> tirage uniforme
        return random.choice(pop)
    r = random.uniform(0, total)
    cumul = 0
    for ind, f in zip(pop, fits):
        cumul += f
        if cumul >= r:
            return ind
    return pop[-1]


# ----------------------------------------------------------- Croisement
def croisement(p1, p2, pc):
    if random.random() < pc:
        pt = random.randint(1, N_UNITES - 1)     # point entre deux gènes
        return p1[:pt] + p2[pt:], p2[:pt] + p1[pt:]
    return p1[:], p2[:]


# ------------------------------------------------------------- Mutations
def mutation_inversion(chrom, pm):
    """Inversion : on choisit un segment de gènes [i..j] et on inverse l'ordre
    des bits (effet miroir dans le temps) de chaque bloc du segment.
    1100 -> 0011, 0110 -> 0110, 1000 -> 0001 : les blocs restent valides."""
    c = chrom[:]
    if random.random() < pm:
        i = random.randrange(N_UNITES)
        j = random.randrange(i, N_UNITES)
        for u in range(i, j + 1):
            c[u] = tuple(reversed(c[u]))
    return c


def mutation_remplacement(chrom, pm):
    """Autre type : remplace le bloc d'une unité par un autre bloc valide."""
    c = chrom[:]
    if random.random() < pm:
        u = random.randrange(N_UNITES)
        c[u] = random.choice(MOTIFS[u])
    return c


# --------------------------------------------------------- Algorithme AG
def ag(taille_pop=50, generations=100, pc=0.8, pm=0.2,
       mutation="inversion", elitisme=True, graine=None):
    if graine is not None:
        random.seed(graine)
    mut = mutation_inversion if mutation == "inversion" else mutation_remplacement
    pop = [individu_aleatoire() for _ in range(taille_pop)]
    meilleur, hist = None, []

    for g in range(generations):
        fits = [fitness(i) for i in pop]
        k = max(range(taille_pop), key=lambda x: fits[x])
        if meilleur is None or fits[k] > fitness(meilleur):
            meilleur = pop[k][:]
        hist.append(fits[k])

        nouvelle = [meilleur[:]] if elitisme else []
        while len(nouvelle) < taille_pop:
            p1 = selection_loterie(pop, fits)
            p2 = selection_loterie(pop, fits)
            e1, e2 = croisement(p1, p2, pc)
            nouvelle += [mut(e1, pm), mut(e2, pm)]
        pop = nouvelle[:taille_pop]

    return meilleur, hist


def afficher(chrom):
    print("Chromosome :", " ".join("".join(map(str, g)) for g in chrom))
    for u, g in enumerate(chrom, 1):
        ints = [t + 1 for t, b in enumerate(g) if b]
        print(f"  Unité {u} ({CAPACITE[u-1]:>2} MW) : maintenance aux intervalles {ints}")
    r = reserves(chrom)
    print("Réserves par intervalle :", r)
    print("Fitness (réserve minimale) :", fitness(chrom))


if __name__ == "__main__":
    for type_mut in ("inversion", "remplacement"):
        print(f"\n=== Mutation : {type_mut} ===")
        best, hist = ag(mutation=type_mut, graine=42)
        afficher(best)
        print("Fitness du meilleur par génération (début -> fin):",
              hist[0], "->", hist[-1])
