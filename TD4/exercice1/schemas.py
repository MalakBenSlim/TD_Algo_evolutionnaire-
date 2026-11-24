# TD4 - Exercice 1 : Théorème des schémas
#
# m(H,t+1) >= m(H,t) * f(H)/f_moy * [1 - pc*delta/(l-1) - o*pm]

population = ["10001", "11100", "00011", "01110"]
adaptation = [20, 10, 5, 15]
pc = 0.1
pm = 0.01

l = 5                                        # longueur des chaînes
f_moy = sum(adaptation) / len(adaptation)    # adaptation moyenne = 12.5


def est_instance(chaine, schema):
    # une chaîne est une instance si chaque bit fixé du schéma est identique
    for i in range(len(schema)):
        if schema[i] != "*" and schema[i] != chaine[i]:
            return False
    return True


def calcul(schema):
    # 1) instances du schéma et leur adaptation
    somme = 0
    m = 0
    for i in range(len(population)):
        if est_instance(population[i], schema):
            m = m + 1
            somme = somme + adaptation[i]
    f_H = somme / m

    # 2) ordre o = nombre de bits fixés
    positions = []
    for i in range(len(schema)):
        if schema[i] != "*":
            positions.append(i)
    o = len(positions)

    # 3) longueur utile delta = dernière position fixée - première position fixée
    delta = positions[-1] - positions[0]

    # 4) formule du théorème des schémas
    survie = 1 - pc * delta / (l - 1) - o * pm
    attendu = m * (f_H / f_moy) * survie

    print("Schéma", schema)
    print("  m =", m, " f(H) =", f_H, " f_moy =", f_moy)
    print("  ordre =", o, " longueur utile =", delta)
    print("  facteur de survie =", round(survie, 3))
    print("  nombre attendu à la génération 1 =", round(attendu, 3))
    print()


calcul("1****")   # question a)
calcul("0**10")   # question b)
