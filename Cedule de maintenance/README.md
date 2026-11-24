# Cédule de maintenance : algorithme génétique, recuit simulé et recherche tabou

Ce dossier contient trois solutions au même problème d'ordonnancement de la maintenance de centrales électriques.

## Le problème

On a 7 unités (centrales) et l'année est divisée en 4 intervalles. Chaque unité doit être en maintenance pendant un certain nombre d'intervalles :

| Unité | Capacité (MW) | Intervalles de maintenance requis |
|-------|---------------|-----------------------------------|
| 1     | 20            | 2                                 |
| 2     | 15            | 2                                 |
| 3     | 35            | 1                                 |
| 4     | 40            | 1                                 |
| 5     | 15            | 1                                 |
| 6     | 15            | 1                                 |
| 7     | 10            | 1                                 |

- Capacité totale : 150 MW
- Demande pendant les 4 intervalles : 80, 90, 65 et 70 MW
- La maintenance d'une unité commence au début d'un intervalle et finit à la fin de l'intervalle.
- La réserve de puissance doit toujours être plus grande que la demande.

**Objectif** : trouver la cédule qui maximise la plus petite réserve de l'année.

```
Réserve (intervalle) = Capacité totale - Puissance perdue en maintenance - Demande
```

## Encodage (commun aux trois méthodes)

Une solution (individu) est une liste de 7 gènes de 4 bits, un gène par unité. Chaque bit correspond à un intervalle : `1` = maintenance, `0` = pas de maintenance.

- Unités 1 et 2 : `1100`, `0110` ou `0011`
- Unités 3 à 7 : `1000`, `0100`, `0010` ou `0001`

Exemple : `1100` pour l'unité 1 veut dire maintenance pendant les intervalles 1 et 2.

## Fonction objectif (commune)

La fonction `reserve(individu)` calcule la réserve de chaque intervalle et retourne la **plus petite**. Si elle est négative, la performance est 0. Plus la valeur est grande, meilleure est la solution.

## Les fichiers

| Fichier | Méthode |
|---------|---------|
| `cedule_genetique.py` | Algorithme génétique (population de 10 individus, 30 générations) |
| `cedule_recuit.py` | Recuit simulé |
| `cedule_tabou.py` | Recherche tabou |

### 1. Algorithme génétique

Il travaille avec une **population** d'individus.

- **Croisement** : on échange la fin de deux parents à un point de coupure (sur des blocs de 4 bits).
- **Mutation** : on remplace le gène d'une unité par une autre valeur possible.
- **Sélection** : on garde les 10 meilleurs individus à chaque génération.

### 2. Recuit simulé

Il travaille avec **une seule solution**.

- On crée un voisin en changeant la maintenance d'une seule unité.
- S'il est meilleur, on l'accepte. Sinon, on l'accepte avec la probabilité `exp(différence / température)`.
- La température baisse à chaque palier (`température = température * alpha`). À la fin, on n'accepte presque plus de mauvaises solutions.

Paramètres : `temperature`, `temperature_min`, `alpha`, `nombre_essai`.

### 3. Recherche tabou

Il travaille aussi avec **une seule solution**.

- À chaque itération, on évalue tous les voisins et on prend le meilleur, même s'il est moins bon que la solution courante.
- La liste tabou garde les derniers mouvements (unité, ancienne valeur) pour interdire de revenir en arrière.
- Un mouvement tabou est permis s'il bat le meilleur résultat trouvé jusque-là (critère d'aspiration).

Paramètres : `max_iteration`, `taille_tabou`.

## Exécution

Il faut Python 3 (aucune bibliothèque externe). Dans le dossier :

```
python cedule_genetique.py
python cedule_recuit.py
python cedule_tabou.py
```

Chaque programme affiche le meilleur individu et son score (la plus petite réserve, en MW).

## Remarques

- Les méthodes utilisent le hasard, donc les résultats peuvent changer d'une exécution à l'autre. Il est conseillé de lancer chaque programme plusieurs fois.
- Dans nos essais, le recuit simulé et la recherche tabou ont donné une réserve de 25 MW à chaque exécution.
- Il faut essayer plusieurs valeurs des paramètres plutôt que de se limiter à une seule.
