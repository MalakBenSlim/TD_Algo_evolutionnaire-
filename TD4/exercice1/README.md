# Exercice 1 : Théorème des schémas

## Énoncé

Une population contient à la génération 0 les chaînes et les valeurs d'adaptation suivantes :

| N | Chaîne | Adaptation |
|---|--------|-----------|
| 1 | 10001 | 20 |
| 2 | 11100 | 10 |
| 3 | 00011 | 05 |
| 4 | 01110 | 15 |

La probabilité de mutation est `pm = 0.01` et la probabilité de croisement est `pc = 0.1`.

a) Calculer le nombre attendu de schémas de la forme `H1 = 1****` à la génération 1.
b) Estimer le nombre attendu de schémas de la forme `H2 = 0**10` à la génération 1.

---

## Correction

### 1. Rappel théorique

Un **schéma** H est un modèle de chaînes sur l'alphabet {0, 1, \*}, où \* signifie « 0 ou 1 ».

- `m(H,t)` : nombre d'instances de H à la génération t
- `o(H)` : ordre, c'est-à-dire le nombre de positions fixées
- `δ(H)` : longueur utile, c'est-à-dire la distance entre la première et la dernière position fixée

Théorème fondamental des algorithmes génétiques (Holland), pour une sélection proportionnelle, un croisement à un point et une mutation bit à bit :

```
m(H,t+1) >= m(H,t) * f(H)/f_moy * [ 1 - pc * δ(H)/(l-1) - o(H) * pm ]
```

- `f(H)/f_moy` : effet de la **sélection**
- `pc * δ(H)/(l-1)` : probabilité maximale de destruction par **croisement**
- `o(H) * pm` : probabilité approchée de destruction par **mutation**

### 2. Données

- Taille de la population N = 4, longueur des chaînes l = 5
- Somme des adaptations : 20 + 10 + 5 + 15 = 50
- Adaptation moyenne : **f_moy = 50 / 4 = 12.5**

### 3. Question a) : H1 = 1\*\*\*\*

1. **Instances** : 10001 et 11100, donc `m(H1,0) = 2`.
2. **Adaptation du schéma** : `f(H1) = (20 + 10) / 2 = 15`, donc `f(H1)/f_moy = 1.2`.
3. **Ordre et longueur utile** : `o(H1) = 1` et `δ(H1) = 0`.
4. **Facteur de survie** :
   - croisement : `0.1 × 0/4 = 0`
   - mutation : `1 × 0.01 = 0.01`
   - facteur = `1 - 0 - 0.01 = 0.99`
5. **Résultat** :

```
m(H1,1) >= 2 × 1.2 × 0.99 = 2.376
```

**Le nombre attendu d'instances de H1 à la génération 1 est ≈ 2.38.**

### 4. Question b) : H2 = 0\*\*10

1. **Instances** : il faut 0 en position 1, 1 en position 4 et 0 en position 5. Seule 01110 convient, donc `m(H2,0) = 1`.
2. **Adaptation du schéma** : `f(H2) = 15`, donc `f(H2)/f_moy = 1.2`.
3. **Ordre et longueur utile** : `o(H2) = 3` et `δ(H2) = 5 - 1 = 4`.
4. **Facteur de survie** :
   - croisement : `0.1 × 4/4 = 0.1`
   - mutation : `3 × 0.01 = 0.03`
   - facteur = `1 - 0.1 - 0.03 = 0.87`
5. **Résultat** :

```
m(H2,1) >= 1 × 1.2 × 0.87 = 1.044
```

**Le nombre attendu d'instances de H2 à la génération 1 est ≈ 1.04.** Il s'agit d'une borne inférieure, d'où le terme « estimer » dans l'énoncé.

### 5. Comparaison

| Schéma | m(H,0) | f(H) | f(H)/f_moy | δ | o | Survie | m(H,1) |
|---|---|---|---|---|---|---|---|
| `1****` | 2 | 15 | 1.2 | 0 | 1 | 0.99 | **≈ 2.38** |
| `0**10` | 1 | 15 | 1.2 | 4 | 3 | 0.87 | **≈ 1.04** |

Les deux schémas ont la même adaptation moyenne, donc le même avantage de sélection. H1 est court et d'ordre faible, donc il résiste bien au croisement et à la mutation. H2 est long et d'ordre plus élevé, donc sa croissance est freinée. Cela illustre l'hypothèse des **blocs de construction** : les schémas courts, d'ordre faible et d'adaptation supérieure à la moyenne se propagent de façon exponentielle.

---

## Code

[`schemas.py`](schemas.py) calcule la borne du théorème des schémas pour `1****` et `0**10` 
