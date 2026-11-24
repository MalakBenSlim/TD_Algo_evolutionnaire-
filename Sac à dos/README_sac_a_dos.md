# Problème du sac à dos : tabou, recuit simulé et algorithme génétique

Ce dossier contient trois solutions au même problème du sac à dos.

## Le problème

On a des objets, chacun avec une **valeur** et un **poids**. Le sac a une **capacité** maximale. On veut choisir les objets à mettre dans le sac pour **maximiser la valeur totale** sans dépasser la capacité.

Données utilisées dans les programmes :

| Objet | Valeur | Poids |
|-------|--------|-------|
| 1     | 4      | 12    |
| 2     | 2      | 2     |
| 3     | 2      | 1     |
| 4     | 1      | 1     |
| 5     | 10     | 4     |

Capacité du sac : 15

## Encodage (commun aux trois méthodes)

Une solution est une liste de 0 et de 1, un bit par objet : `1` = objet pris, `0` = objet non pris.

Exemple : `[0, 1, 1, 1, 1]` veut dire qu'on prend les objets 2, 3, 4 et 5.

## Fonction objectif (commune)

La fonction `calculate_valeur(solution, valeurs, poids, capacite)` fait la somme des valeurs et des poids des objets pris.

- Si le poids total dépasse la capacité, la solution est refusée et sa valeur est **0**.
- Sinon, sa valeur est la somme des valeurs des objets pris.

On cherche à **augmenter** la valeur (contrairement au voyageur de commerce où on diminue la distance).

## Les fichiers

| Fichier | Méthode |
|---------|---------|
| `sac_a_dos_tabou.py` | Recherche tabou |
| `sac_a_dos_recuit_simule.py` | Recuit simulé |
| `sac_a_dos_genetique.py` | Algorithme génétique |

### 1. Recherche tabou (`sac_a_dos_tabou.py`)

- On génère des solutions et on garde la meilleure trouvée (`best_solution`).
- La liste tabou garde les dernières solutions. Quand elle est pleine, on retire la plus ancienne.
- Paramètres : `tabou_length` (taille de la liste tabou) et `max_iter` (nombre d'itérations).

Remarque : dans cette version, chaque solution est générée au hasard et la liste tabou n'est jamais consultée pour interdire une solution. Pour une recherche tabou complète, il faut partir d'une solution, évaluer ses voisins (changer un seul objet) et choisir le meilleur voisin qui n'est pas dans la liste tabou.

### 2. Recuit simulé (`sac_a_dos_recuit_simule.py`)

On travaille avec **une seule solution**.

- Un voisin s'obtient en changeant un seul objet (pris devient pas pris, ou l'inverse).
- Si le voisin est meilleur, on l'accepte. Sinon, on l'accepte avec la probabilité `exp(différence / température)`.
- La température baisse à chaque palier (`température = température * alpha`). À la fin, on n'accepte presque plus de mauvaises solutions.
- Paramètres : `temperature`, `temperature_min`, `alpha`, `nombre_essai`.

### 3. Algorithme génétique (`sac_a_dos_genetique.py`)

On travaille avec une **population** de solutions (10 individus, 30 générations).

- **Croisement** : on échange la fin de deux parents à un point de coupure.
- **Mutation** : on change un objet de pris à pas pris, ou l'inverse.
- **Sélection** : on garde les 10 meilleurs individus à chaque génération.
- Paramètres : `nombre_individu`, `max_generation`.

## Exécution

Il faut Python 3 (aucune bibliothèque externe). Dans le dossier :

```
python sac_a_dos_tabou.py
python sac_a_dos_recuit_simule.py
python sac_a_dos_genetique.py
```

Chaque programme affiche la meilleure solution trouvée.

## Résultat attendu

Pour ces données, la meilleure solution est `[0, 1, 1, 1, 1]` : poids total 8 (capacité 15) et valeur totale **15**. L'objet 1 est trop lourd (poids 12) pour entrer avec l'objet 5, qui a la plus grande valeur. Dans nos essais, le recuit simulé et l'algorithme génétique ont trouvé cette valeur à chaque exécution.

## Captures d'exécution

### Recherche tabou

![Exécution de la recherche tabou](Images/sac_a_dos_tabou.png)

### Recuit simulé

![Exécution du recuit simulé](Images/sac_a_dos_recuit_simule.png)

### Algorithme génétique

![Exécution de l'algorithme génétique](Images/sac_a_dos_genetique.png)

## Remarques

- Ces méthodes utilisent le hasard, donc les résultats peuvent changer d'une exécution à l'autre. Il est conseillé de lancer chaque programme plusieurs fois.
- Il faut essayer plusieurs valeurs des paramètres plutôt que de se limiter à une seule.