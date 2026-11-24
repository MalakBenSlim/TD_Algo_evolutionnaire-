# Voyageur de commerce (TSP) : tabou, recuit simulé et algorithme génétique

Ce dossier contient trois solutions au même problème du voyageur de commerce.

## Le problème

On a 12 villes (numérotées de 0 à 11) et une matrice de distances entre elles. Le voyageur doit visiter chaque ville une seule fois. On veut trouver l'ordre de visite qui **minimise la distance totale**.

## Encodage (commun aux trois méthodes)

Une solution est une liste qui contient chaque ville une seule fois, dans l'ordre de visite.

Exemple : `[3, 0, 5, 1, 2, 4, 6, 7, 8, 9, 10, 11]` veut dire qu'on part de la ville 3, puis 0, puis 5, etc.

## Fonction objectif (commune)

La fonction `calculate_distance(solution, distances)` additionne les distances entre deux villes consécutives de la liste. Plus la distance est **petite**, meilleure est la solution (contrairement au sac à dos où on augmente la valeur).

Remarque : le calcul ne ramène pas le voyageur à la ville de départ (pas de retour). C'est le calcul du code de départ, repris dans les trois programmes.

## Les fichiers

| Fichier | Méthode |
|---------|---------|
| `voyageur_de_commerce_tabou.py` | Recherche tabou |
| `voyageur_de_commerce_recuit_simule.py` | Recuit simulé |
| `voyageur_de_commerce_genetique.py` | Algorithme génétique |

### 1. Recherche tabou (`voyageur_de_commerce_tabou.py`)

- On génère des solutions (villes mélangées) et on garde la meilleure trouvée (`best_solution`).
- La liste tabou garde les dernières solutions. Quand elle est pleine, on retire la plus ancienne.
- Paramètres : `tabou_length` (taille de la liste tabou) et `max_iter` (nombre d'itérations).

Remarque : dans cette version, chaque solution est générée au hasard et la liste tabou n'est jamais consultée pour interdire une solution. Pour une recherche tabou complète, il faut partir d'une solution, évaluer ses voisins (échanger deux villes) et choisir le meilleur voisin qui n'est pas dans la liste tabou.

### 2. Recuit simulé (`voyageur_de_commerce_recuit_simule.py`)

On travaille avec **une seule solution**.

- Un voisin s'obtient en échangeant deux villes au hasard.
- Si la distance diminue, on accepte le voisin. Sinon, on l'accepte avec la probabilité `exp(-différence / température)`.
- La température baisse à chaque palier (`température = température * alpha`). À la fin, on n'accepte presque plus de mauvaises solutions.
- Paramètres : `temperature`, `temperature_min`, `alpha`, `nombre_essai`.

### 3. Algorithme génétique (`voyageur_de_commerce_genetique.py`)

On travaille avec une **population** de solutions (30 individus, 300 générations).

- **Croisement** : on garde le début du parent 1 jusqu'à un point de coupure, puis on complète avec les villes manquantes dans l'ordre du parent 2. Ainsi, chaque ville apparaît une seule fois (un croisement simple donnerait des villes en double).
- **Mutation** : on échange deux villes.
- **Sélection** : on garde les 30 individus avec la plus petite distance.
- Paramètres : `nombre_individu`, `max_generation`.

## Exécution

Il faut Python 3 (aucune bibliothèque externe). Dans le dossier :

```
python voyageur_de_commerce_tabou.py
python voyageur_de_commerce_recuit_simule.py
python voyageur_de_commerce_genetique.py
```

Chaque programme affiche la meilleure solution trouvée et sa distance.

## Captures d'exécution

### Recherche tabou

![Exécution de la recherche tabou](../Images/tsp_tabou.png)

### Recuit simulé

![Exécution du recuit simulé](../Images/tsp_recuit_simule.png)

### Algorithme génétique

![Exécution de l'algorithme génétique](../Images/tsp_genetique.png)

## Résultat attendu

Avec cette matrice et ce calcul de distance (sans retour), la meilleure distance possible est **193** (calculée de façon exacte). Dans nos essais, le recuit simulé et l'algorithme génétique donnent des distances proches, entre 193 et 210 environ. La recherche tabou de départ, qui est une recherche aléatoire, donne en général de moins bons résultats.

## Remarques

- Ces méthodes utilisent le hasard, donc les résultats changent d'une exécution à l'autre. Il est conseillé de lancer chaque programme plusieurs fois.
- La matrice contient des valeurs qui semblent être des fautes de frappe (331, 261 et 221 dans la dernière colonne, alors que les valeurs symétriques sont 33, 26 et 22). Les programmes utilisent la matrice telle quelle.
- Il faut essayer plusieurs valeurs des paramètres plutôt que de se limiter à une seule.
