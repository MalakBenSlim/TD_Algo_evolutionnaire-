# Exercice 3 : Optimisation par essaim de particules (PSO)

## Énoncé

On se propose d'appliquer l'optimisation par essaim de particules « PSO » pour rechercher le **maximum** de la fonction `f` à une variable réelle `x` définie par :

```
f(x) = -x² + 4x    tel que x ∈ [-5, +5]
```

**1)** En partant, dans la phase d'initialisation, par les trois particules `x1 = 2 ; x2 = 4 ; x3 = -1` avec les vélocités initiales `v1 = v2 = v3 = 0` et en utilisant une inertie `c1 = 0.8` et des accélérations `c2 = c3 = 2` :

- a) Calculer la meilleure position `pbest_i` (i = 1..3) pour chaque particule.
- b) Calculer la meilleure position globale de l'essaim `gbest`.
- c) Calculer les nouvelles valeurs `x_i¹ ; v_i¹ ; pbest_i (i = 1..3)` et `gbest¹` à la première itération.

**2)** Afin d'implémenter cet algorithme, on prendra `n` particules, et en utilisant les mêmes paramètres qu'en (1).

- a) Écrire l'algorithme permettant de générer une population initiale de `n` particules aléatoires `x_i` avec des vélocités aléatoires `v_i`, i = 1..n et de calculer les `pbest_i` et `gbest`.
- b) Évaluer la complexité de l'algorithme d'initialisation.
- c) Écrire l'algorithme PSO intégral pour ce problème.

---

## Correction

### Rappel théorique

Chaque particule i possède une position `x_i`, une vitesse `v_i`, sa meilleure position personnelle `pbest_i`, et connaît la meilleure position de l'essaim `gbest`.

```
v_i(t+1) = c1·v_i(t) + c2·r1·(pbest_i - x_i(t)) + c3·r2·(gbest - x_i(t))
x_i(t+1) = x_i(t) + v_i(t+1)
```

- `c1·v_i` : inertie (exploration)
- `c2·r1·(pbest_i - x_i)` : composante cognitive
- `c3·r2·(gbest - x_i)` : composante sociale
- `r1, r2` : nombres aléatoires dans [0,1]

Comme on cherche un maximum, une position est meilleure si `f` est plus grande.

**Vérification analytique** : `f'(x) = -2x + 4 = 0` donne `x* = 2`, et `f''(x) = -2 < 0` donc c'est un maximum, avec **f(x\*) = 4**.

### Question 1 : application à la main

L'énoncé ne donne pas `r1` et `r2`. On prend **r1 = r2 = 1** pour avoir des valeurs numériques.

**a) pbest_i** : à l'initialisation, `pbest_i = x_i`.

| Particule | x_i | f(x_i) | pbest_i |
|---|---|---|---|
| 1 | 2 | 4 | 2 |
| 2 | 4 | 0 | 4 |
| 3 | -1 | -5 | -1 |

**b) gbest** = 2 (particule 1, f = 4).

**c) Première itération.** Comme `pbest_i = x_i`, le terme cognitif est nul, donc `v_i¹ = 2·(2 - x_i)`.

| Particule | v_i¹ | x_i¹ | f(x_i¹) | pbest_i après |
|---|---|---|---|---|
| 1 | 2·(2-2) = **0** | **2** | 4 | 2 |
| 2 | 2·(2-4) = **-4** | **0** | 0 | 4 (égalité, pas d'amélioration stricte) |
| 3 | 2·(2+1) = **6** | **5** | -5 | -1 (égalité, pas d'amélioration stricte) |

**gbest¹ = 2.**

Cas général (r2 quelconque) : `x2¹ = 4 - 4·r2` et `x3¹ = -1 + 6·r2`.

### Question 2 : implémentation

**a) Algorithme d'initialisation**

```
Algorithme Initialisation(n)
Début
  Pour i de 1 à n faire
      x[i]     <- a + rand(0,1) × (b - a)         // a = -5, b = 5
      v[i]     <- -vmax + rand(0,1) × 2·vmax
      pbest[i] <- x[i]
      fp[i]    <- f(x[i])
  Fin Pour
  gbest <- pbest[1] ; fg <- fp[1]
  Pour i de 2 à n faire
      Si fp[i] > fg alors gbest <- pbest[i] ; fg <- fp[i]
  Fin Pour
Fin
```

**b) Complexité** : la boucle d'initialisation coûte O(n) (chaque itération est en O(1)) et la recherche de `gbest` coûte O(n). Au total **O(n)** en temps et **O(n)** en mémoire.

**c) PSO complet**

```
Algorithme PSO
Paramètres : n, Tmax, c1 = 0.8, c2 = 2, c3 = 2, [a,b] = [-5,5], vmax
Début
  Initialisation(n)
  t <- 0
  Tant que t < Tmax faire
      Pour i de 1 à n faire
          r1 <- rand(0,1) ; r2 <- rand(0,1)
          v[i] <- c1·v[i] + c2·r1·(pbest[i] - x[i]) + c3·r2·(gbest - x[i])
          v[i] <- borner(v[i], -vmax, vmax)
          x[i] <- borner(x[i] + v[i], a, b)
          Si f(x[i]) > f(pbest[i]) alors pbest[i] <- x[i]
          Si f(pbest[i]) > f(gbest) alors gbest <- pbest[i]
      Fin Pour
      t <- t + 1
  Fin Tant que
  Retourner gbest, f(gbest)
Fin
```

Complexité totale : **O(Tmax · n)**. Résultat attendu : `gbest → 2` et `f(gbest) → 4`.

---

## Code

[`pso.py`](pso.py) contient :

- la vérification de la **première itération à la main** (question 1),
- l'implémentation complète du **PSO** avec `n = 20` particules (question 2).
