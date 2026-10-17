# 14. Unsupervised Learning: K-Means Clustering & Hierarchical Clustering
**Term:** Term 5 | **Subject:** CML | **Note ID:** `cml-t5-l14`
**Last Updated:** 2026-10-18T00:00:00Z

## Abstract & Summary
An exhaustive, first-principles journey through Unsupervised Learning and Clustering. Explores why learning without labels requires internal geometrical validation, walks through Lloyd's K-Means algorithm and the mathematical proof of inertia convergence, solves the local minima trap with k-means++ initialization, and rigorously deconstructs the Elbow method and Silhouette coefficients. Unpacks Hierarchical Agglomerative Clustering, compares linkage metrics, decodes dendrograms, and demonstrates production customer segmentation in Scikit-Learn.

## Learning Objectives
- Contrast supervised learning against unsupervised learning and define cluster homogeneity via Euclidean distance.
- Execute Lloyd's K-Means algorithm step-by-step: nearest-centroid assignment and centroid mean update.
- Analyze the K-Means objective function (Inertia/WCSS), explain local minima convergence, and evaluate k-means++ seeding.
- Determine the optimal number of clusters k using the Elbow heuristic and Silhouette analysis (cohesion a vs separation b).
- Construct Hierarchical Agglomerative Clustering trees, evaluate linkage criteria (Single, Complete, Average, Ward), and cut dendrograms.
- Implement end-to-end customer segmentation in Scikit-Learn, profile cluster personas, and diagnose geometric failure modes.

## Key Takeaways
- Unsupervised learning uncovers latent structure in feature space X without target labels y; cluster IDs are arbitrary and require domain profiling.
- Because clustering algorithms depend heavily on Euclidean distance, feature scaling (StandardScaler) is strictly mandatory.
- Lloyd's K-Means alternates between two simple steps: Assign each point to its nearest centroid, then Update each centroid to the mean of its points.
- Inertia (Within-Cluster Sum of Squares, WCSS) monotonically decreases during K-Means iterations, guaranteeing convergence to a local minimum.
- k-means++ initialization selects spread-out starting seeds with probability proportional to squared distance D(x)^2, avoiding bad local minima.
- Inertia always decreases as k increases; therefore, k must be selected using the Elbow knee heuristic paired with the Silhouette score.
- Hierarchical Agglomerative Clustering builds a bottom-up merge tree without requiring k upfront; cutting the dendrogram at the largest vertical gap yields stable clusters.
- Ward linkage minimizes total within-cluster variance (producing spherical clusters), while Single linkage connects closest pairs (capable of finding non-convex moons but prone to chaining).

---

## 1. The Unsupervised Paradigm: Finding Structure Without Labels
### 1.1 The Hook: Finding Hidden Structure Without Ground Truth Labels

Imagine examining a retail database containing transaction histories for 10,000 customers:
- There is no target variable $y$. No column indicates *"Good Customer"* or *"Bad Customer"*.
- The machine learning model is given only the feature matrix $\mathbf{X} \in \mathbb{R}^{n \times d}$ (e.g., Annual Income, Spending Score, Age, Visit Frequency).
- Yet, when plotted in feature space, the observations are not uniformly scattered. They naturally coalesce into dense geometric islands separated by sparse valleys.

**Clustering** is the foundational task of **Unsupervised Learning**:
Its objective is to discover natural, coherent groupings (clusters) within data such that:
1. **High Intra-Cluster Cohesion**: Observations within the same cluster are as geometrically similar (close) to each other as possible.
2. **High Inter-Cluster Separation**: Observations in different clusters are as geometrically distinct (distant) from each other as possible.

```
Supervised vs. Unsupervised Learning Paradigms:
   Supervised Learning (Classification):
      Feature Matrix X + Ground Truth Labels y ──► [ Learn Mapping f(X) -> y ] ──► Evaluate on y_test

   Unsupervised Learning (Clustering):
      Feature Matrix X (No Labels!) ──────────► [ Discover Latent Structure ] ──► Geometric Cohesion & Separation
```

---

### 1.2 Comparison: Supervised vs. Unsupervised Learning

| Dimension | Supervised Learning (Regression / Classification) | Unsupervised Learning (Clustering / PCA) |
| :--- | :--- | :--- |
| **Data Requirements** | Feature matrix $\mathbf{X}$ and target vector $\mathbf{y}$. | Feature matrix $\mathbf{X}$ **only**. No target $y$ exists. |
| **Objective** | Learn a predictive mapping $f: \mathbf{x} \mapsto y$ that generalizes to unseen $\mathbf{x}_{\text{test}}$. | Partition feature space $\mathbb{R}^d$ into $K$ meaningful clusters or low-dimensional manifolds. |
| **Evaluation** | Concrete external ground truth: Accuracy, ROC-AUC, Mean Squared Error. | Internal geometric metrics: Inertia, Silhouette Score, Davies-Bouldin Index. |
| **Cluster Label Meaning** | Class names have fixed semantic meaning (e.g., $1 = \text{Default}$). | Cluster IDs (`0, 1, 2`) are completely arbitrary and require human domain profiling. |
| **Primary Failure Risk** | Overfitting to training labels; data leakage. | Finding meaningless patterns in pure noise (clustering algorithms will happily partition random uniform noise into $K$ clusters!). |

---

### 1.3 The Non-Negotiable Imperative of Feature Scaling

Because virtually all clustering algorithms rely directly on **Euclidean Distance**:
$$D(\mathbf{x}_i, \mathbf{x}_j) = \sqrt{\sum_{k=1}^d (x_{ik} - x_{jk})^2}$$

Features with large numerical ranges (e.g., `Annual Income` ranging from 20,000 USD to 200,000 USD) produce squared differences of $(10,000)^2 = 100,000,000$, while features with small numerical ranges (e.g., `Age` ranging from $18$ to $70$) produce squared differences of $(20)^2 = 400$.
- The algorithm will compute distances based almost exclusively on Income, **completely blinding itself to Age**.
- **Rule of Thumb**: Always standardize features with `StandardScaler` ($z = \frac{x - \mu}{\sigma}$) before clustering, unless features share identical physical units.

**Citations & References:**
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). Springer, Chapter 14.
- Jain, A. K. (2010). Data clustering: 50 years beyond K-means. Pattern Recognition Letters, 31(8), 651-666.

---

## 2. K-Means Algorithm: Lloyd's Assign-Update Cycle
### 2.1 The K-Means Objective Function: Within-Cluster Sum of Squares (Inertia)

Let $\mathcal{D} = \{\mathbf{x}_1, \dots, \mathbf{x}_n\} \subset \mathbb{R}^d$ be our dataset.
We wish to partition the $n$ points into $K$ mutually disjoint subsets $C_1, C_2, \dots, C_K$ such that each cluster has a prototype center (centroid) $\boldsymbol{\mu}_k \in \mathbb{R}^d$.

The **K-Means Objective Function**, formally known as the **Within-Cluster Sum of Squares (WCSS)** or **Inertia** $J(C, \boldsymbol{\mu})$, is defined as:

$$J(C, \boldsymbol{\mu}) = \sum_{k=1}^{K} \sum_{i \in C_k} \|\mathbf{x}_i - \boldsymbol{\mu}_k\|_2^2$$

Finding the global minimum of $J(C, \boldsymbol{\mu})$ is an **NP-hard combinatorial problem**, as there are approximately $K^n / K!$ possible ways to assign $n$ points into $K$ clusters.
Instead, we solve it using **Lloyd's Algorithm (1957)**, an alternating greedy optimization heuristic.

---

### 2.2 Lloyd's Algorithm: The Two-Step Dance

Lloyd's algorithm alternates between two complementary optimization steps until convergence:

```
Lloyd's K-Means Algorithm:
  Initialize K centroids: μ_1, μ_2, ..., μ_K
  Repeat until centroids stop moving (convergence):
     1. Assignment Step (Fix centroids μ, optimize cluster assignments C):
           Assign each observation x_i to its nearest centroid:
           C_k = { x_i : || x_i - μ_k ||^2 <= || x_i - μ_j ||^2   for all j in {1, ..., K} }
     2. Update Step (Fix cluster assignments C, optimize centroids μ):
           Recompute each centroid as the center of mass (mean) of its assigned points:
           μ_k = (1 / |C_k|) * sum_{x_i in C_k} x_i
```

#### Mathematical Proof of Monotonic Inertia Convergence:
1. **In the Assignment Step**: Holding centroids $\boldsymbol{\mu}$ constant, assigning each point $\mathbf{x}_i$ to its nearest centroid strictly minimizes $\sum_k \sum_{i \in C_k} \|\mathbf{x}_i - \boldsymbol{\mu}_k\|^2$. Therefore, $J(C^{(t+1)}, \boldsymbol{\mu}^{(t)}) \le J(C^{(t)}, \boldsymbol{\mu}^{(t)})$.
2. **In the Update Step**: Holding assignments $C$ constant, the point that minimizes the sum of squared distances to a set of points is the arithmetic mean $\boldsymbol{\mu}_k = \frac{1}{|C_k|}\sum_{i \in C_k}\mathbf{x}_i$. (Setting $\frac{\partial J}{\partial \boldsymbol{\mu}_k} = 0 \implies -2\sum_{i \in C_k}(\mathbf{x}_i - \boldsymbol{\mu}_k) = 0 \implies \boldsymbol{\mu}_k = \bar{\mathbf{x}}_{C_k}$). Therefore, $J(C^{(t+1)}, \boldsymbol{\mu}^{(t+1)}) \le J(C^{(t+1)}, \boldsymbol{\mu}^{(t)})$.
3. Because $J$ monotonically decreases at every step and there are a finite number of partitions ($K^n$), **Lloyd's algorithm is mathematically guaranteed to converge in a finite number of iterations** to a local minimum!

---

### 2.3 Comprehensive Hand-Calculated Walkthrough: Whiteboard 1 (6 Points in 2D)

Let us trace Lloyd's algorithm by hand on the exact 6-point dataset from class whiteboard 1, using a deliberately poor initialization:

#### The Dataset ($n = 6$ points in $\mathbb{R}^2$):
- $A = (1.0, 1.0)$
- $B = (1.0, 2.0)$
- $C = (2.0, 1.0)$
- $D = (5.0, 4.0)$
- $E = (5.0, 5.0)$
- $F = (6.0, 5.0)$

We want $K = 2$ clusters.
**Deliberately Poor Initialization**:
- Centroid 1: $\boldsymbol{\mu}_1 = A = (1.0, 1.0)$
- Centroid 2: $\boldsymbol{\mu}_2 = B = (1.0, 2.0)$

---

#### Iteration 1 — Step 1: Distance Calculation & Cluster Assignment
Compute squared Euclidean distance from each point to $\boldsymbol{\mu}_1(1, 1)$ and $\boldsymbol{\mu}_2(1, 2)$:

| Point | $(x_1, x_2)$ | $\|\mathbf{x} - \boldsymbol{\mu}_1\|^2 = (x_1-1)^2 + (x_2-1)^2$ | $\|\mathbf{x} - \boldsymbol{\mu}_2\|^2 = (x_1-1)^2 + (x_2-2)^2$ | Assigned Cluster |
| :---: | :---: | :---: | :---: | :---: |
| **A** | $(1.0, 1.0)$ | $(0)^2 + (0)^2 = \mathbf{0.0}$ | $(0)^2 + (-1)^2 = 1.0$ | **Cluster 1** |
| **B** | $(1.0, 2.0)$ | $(0)^2 + (1)^2 = 1.0$ | $(0)^2 + (0)^2 = \mathbf{0.0}$ | **Cluster 2** |
| **C** | $(2.0, 1.0)$ | $(1)^2 + (0)^2 = \mathbf{1.0}$ | $(1)^2 + (-1)^2 = 2.0$ | **Cluster 1** |
| **D** | $(5.0, 4.0)$ | $(4)^2 + (3)^2 = 25.0$ | $(4)^2 + (2)^2 = \mathbf{20.0}$ | **Cluster 2** |
| **E** | $(5.0, 5.0)$ | $(4)^2 + (4)^2 = 32.0$ | $(4)^2 + (3)^2 = \mathbf{25.0}$ | **Cluster 2** |
| **F** | $(6.0, 5.0)$ | $(5)^2 + (4)^2 = 41.0$ | $(5)^2 + (3)^2 = \mathbf{34.0}$ | **Cluster 2** |

- **Cluster 1**: $\{A, C\}$
- **Cluster 2**: $\{B, D, E, F\}$
- **Iteration 1 Initial Inertia**: $J = (0 + 1) + (0 + 20 + 25 + 34) = 1 + 79 = \mathbf{80.0}$

---

#### Iteration 1 — Step 2: Update Centroids
Recompute centroids as the mean of assigned points:
- $\boldsymbol{\mu}_1^{(1)} = \text{mean}(A, C) = \left( \frac{1+2}{2}, \frac{1+1}{2} \right) = \mathbf{(1.5, 1.0)}$
- $\boldsymbol{\mu}_2^{(1)} = \text{mean}(B, D, E, F) = \left( \frac{1+5+5+6}{4}, \frac{2+4+5+5}{4} \right) = \left( \frac{17}{4}, \frac{16}{4} \right) = \mathbf{(4.25, 4.0)}$

---

#### Iteration 2 — Step 1: Re-assign Points to Updated Centroids
Compute distances to $\boldsymbol{\mu}_1(1.5, 1.0)$ and $\boldsymbol{\mu}_2(4.25, 4.0)$:

| Point | $(x_1, x_2)$ | $\|\mathbf{x} - \boldsymbol{\mu}_1\|^2 = (x_1-1.5)^2 + (x_2-1.0)^2$ | $\|\mathbf{x} - \boldsymbol{\mu}_2\|^2 = (x_1-4.25)^2 + (x_2-4.0)^2$ | New Assigned Cluster |
| :---: | :---: | :---: | :---: | :---: |
| **A** | $(1.0, 1.0)$ | $(-0.5)^2 + 0^2 = \mathbf{0.25}$ | $(-3.25)^2 + (-3)^2 = 19.56$ | **Cluster 1** |
| **B** | $(1.0, 2.0)$ | $(-0.5)^2 + (1)^2 = \mathbf{1.25}$ | $(-3.25)^2 + (-2)^2 = 14.56$ | **Cluster 1 (FLIPPED!)** |
| **C** | $(2.0, 1.0)$ | $(0.5)^2 + 0^2 = \mathbf{0.25}$ | $(-2.25)^2 + (-3)^2 = 14.06$ | **Cluster 1** |
| **D** | $(5.0, 4.0)$ | $(3.5)^2 + (3)^2 = 21.25$ | $(0.75)^2 + 0^2 = \mathbf{0.56}$ | **Cluster 2** |
| **E** | $(5.0, 5.0)$ | $(3.5)^2 + (4)^2 = 28.25$ | $(0.75)^2 + (1)^2 = \mathbf{1.56}$ | **Cluster 2** |
| **F** | $(6.0, 5.0)$ | $(4.5)^2 + (4)^2 = 36.25$ | $(1.75)^2 + (1)^2 = \mathbf{4.06}$ | **Cluster 2** |

Notice that **Point B flipped from Cluster 2 to Cluster 1**!
- **New Cluster 1**: $\{A, B, C\}$
- **New Cluster 2**: $\{D, E, F\}$

---

#### Iteration 2 — Step 2: Recompute Centroids
- $\boldsymbol{\mu}_1^{(2)} = \text{mean}(A, B, C) = \left( \frac{1+1+2}{3}, \frac{1+2+1}{3} \right) = \left( \frac{4}{3}, \frac{4}{3} \right) \approx \mathbf{(1.333, 1.333)}$
- $\boldsymbol{\mu}_2^{(2)} = \text{mean}(D, E, F) = \left( \frac{5+5+6}{3}, \frac{4+5+5}{3} \right) = \left( \frac{16}{3}, \frac{14}{3} \right) \approx \mathbf{(5.333, 4.667)}$

---

#### Iteration 3: Convergence Check
If we compute distances to these new centroids, no point changes assignment.
The algorithm terminates!
Final Converged Inertia:
$$J = \|\mathbf{x}_A - \boldsymbol{\mu}_1\|^2 + \dots + \|\mathbf{x}_F - \boldsymbol{\mu}_2\|^2 = \mathbf{4.000}$$
Inertia plunged from $80.0 \to 4.000$, achieving the globally optimal clustering!

---

### 2.4 Voronoi Cell Geometry: The Linear Boundary Theorem

A fundamental geometric property of K-Means is that it partitions space into convex polyhedral cells called a **Voronoi Diagram**:

> **Theorem of Voronoi Boundaries**:
> For any two centroids $\boldsymbol{\mu}_j$ and $\boldsymbol{\mu}_k$, the decision boundary between them is the set of points equidistant from both:
> $$\|\mathbf{x} - \boldsymbol{\mu}_j\|^2 = \|\mathbf{x} - \boldsymbol{\mu}_k\|^2$$
> Expanding the Euclidean norms:
> $$\mathbf{x}^T \mathbf{x} - 2\boldsymbol{\mu}_j^T \mathbf{x} + \|\boldsymbol{\mu}_j\|^2 = \mathbf{x}^T \mathbf{x} - 2\boldsymbol{\mu}_k^T \mathbf{x} + \|\boldsymbol{\mu}_k\|^2$$
> Cancelling $\mathbf{x}^T \mathbf{x}$ and rearranging yields a **strictly linear hyperplane equation**:
> $$2(\boldsymbol{\mu}_k - \boldsymbol{\mu}_j)^T \mathbf{x} + (\|\boldsymbol{\mu}_j\|^2 - \|\boldsymbol{\mu}_k\|^2) = 0$$
> $$(\boldsymbol{\mu}_k - \boldsymbol{\mu}_j)^T \left( \mathbf{x} - \frac{\boldsymbol{\mu}_j + \boldsymbol{\mu}_k}{2} \right) = 0$$

```
Voronoi Linear Boundary Geometry:
       x2 ^
          │      \                     /
          │       \   Cluster 1       /   Cluster 2
          │        \     * μ1        /       * μ2
          │         \               /
          │  ────────┼─────────────┼──────────────
          │           \           /
          │   Cluster 3\         /   Cluster 4
          │      * μ3   \       /       * μ4
          │              \     /
          └───────────────┴───┴──────────────────► x1
```

#### Why K-Means Cannot Learn Non-Convex Geometries:
Because every cell boundary is formed by the intersection of flat linear hyperplanes, **every K-Means cluster is mathematically guaranteed to be a convex polyhedron**!
If your real-world data contains non-convex manifolds (such as concentric circles or interlocking crescents), K-Means will inevitably slice them into arbitrary straight-edged pieces!

**Citations & References:**
- Lloyd, S. (1982). Least squares quantization in PCM. IEEE Transactions on Information Theory, 28(2), 129-137.

---

## 3. Inertia (WCSS) & The k-means++ Seeding Advantage
### 3.1 The Initialization Trap & The K-Means++ Breakthrough

Because Lloyd's algorithm is a greedy gradient descent method on non-convex surfaces, **random initialization frequently gets trapped in terrible local minima**:
- If two initial centroids land in the same dense cluster, that cluster gets artificially split in half.
- Meanwhile, two distant distinct clusters are forced to share a single centroid!
- In Scikit-Learn, the brute-force workaround was `n_init=10` (running 10 times with different random seeds and keeping the lowest inertia run).

In 2007, David Arthur and Sergei Vassilvitskii revolutionized clustering with **k-means++**:

```
The k-means++ Initialization Algorithm:
  1. Choose the first centroid μ_1 uniformly at random from the dataset D.
  2. For each remaining point x_i in D:
        Compute D(x_i) = shortest distance from x_i to the closest already chosen centroid.
  3. Select the next centroid μ_k from D with probability proportional to SQUARED distance:
        P(x_i) = [ D(x_i) ]^2 / sum_{j} [ D(x_j) ]^2
  4. Repeat steps 2-3 until K centroids are chosen.
  5. Proceed with standard Lloyd's iterations.
```

> **The Arthur-Vassilvitskii Theorem (2007)**:
> The k-means++ initialization algorithm is mathematically guaranteed to be **$O(\log K)$-competitive in expectation** with the optimal clustering:
> $$\mathbb{E}[J_{\text{k-means++}}] \le 8(\ln K + 2) J_{\text{optimal}}$$
> By forcing new centroids to be picked far away from existing ones ($D(x)^2$ sampling), k-means++ avoids seeding multiple centroids into the same cluster!

---

### 3.2 Determining the Optimal Number of Clusters $K$

Because clustering is unsupervised, how do we know whether the data contains $K = 2, 3, 5,$ or $10$ clusters?

#### 1. The Fatal Flaw of "Lowest Inertia":
Inertia $J$ **strictly decreases** as $K$ increases:
- When $K = n$, every point is its own centroid ($\boldsymbol{\mu}_i = \mathbf{x}_i$), and Inertia is identically **$0.0$**!
- Therefore, **you can never pick $K$ by minimizing inertia**.

#### 2. The Elbow Method (Knee Point Heuristic):
We plot Inertia $J$ as a function of $K \in \{1, 2, \dots, 10\}$:
- Initially, as $K$ increases, inertia drops steeply because real clusters are being separated.
- Beyond the true number of clusters $K^*$, adding more centroids merely splits existing tight clusters, producing only marginal inertia reductions.
- The optimal $K^*$ sits at the **"Elbow"** (the point of maximum curvature / knee).

```
The Elbow Curve:
    Inertia J
      ^
      │  \
      │   \
      │    \  <-- Rapid drop (Real structure uncovered)
      │     \
      │      '.  <-- THE ELBOW (Optimal K = 3)
      │        ' - - - - - - - - - - - - - -► Marginal drop (Splitting real clusters)
      +──────────────┴────────────────────────► Number of Clusters K
      K = 1        K = 3                    K = 10
```

---

### 3.3 Silhouette Analysis: Quantifying Cohesion vs. Separation

To mathematically validate cluster quality without subjective visual inspection, Rousseeuw (1987) introduced the **Silhouette Coefficient**:

For each individual observation $i$:
1. **Intra-Cluster Cohesion ($a(i)$)**:
   The mean distance between observation $i$ and all other points belonging to the **same cluster**:
   $$a(i) = \frac{1}{|C_I| - 1} \sum_{j \in C_I, j \ne i} \|\mathbf{x}_i - \mathbf{x}_j\|$$
2. **Nearest-Cluster Separation ($b(i)$)**:
   The mean distance between observation $i$ and all points in the **closest neighboring cluster**:
   $$b(i) = \min_{J \ne I} \left[ \frac{1}{|C_J|} \sum_{j \in C_J} \|\mathbf{x}_i - \mathbf{x}_j\| \right]$$
3. **Silhouette Score ($s(i)$)**:
   $$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))} \in [-1, +1]$$

#### Interpreting the Silhouette Value:
- **$s(i) \approx +1$ (Strong Clustering)**: $a(i) \ll b(i)$. The point is tightly nestled inside its own cluster and far away from any other cluster.
- **$s(i) \approx 0$ (Boundary Ambiguity)**: $a(i) \approx b(i)$. The point sits directly on the decision border between two clusters.
- **$s(i) < 0$ (Misassigned Point)**: $a(i) > b(i)$. The point is closer to the neighboring cluster than to its own! It should be moved.

#### Hand-Check from Whiteboard 1:
For Point $A(1, 1)$ in Cluster 1 $\{A, B, C\}$:
- Distance to $B(1, 2)$: $1.000$
- Distance to $C(2, 1)$: $1.000$
- Cohesion $a(A) = \frac{1.0 + 1.0}{2} = \mathbf{1.000}$
- Nearest Cluster is Cluster 2 $\{D(5,4), E(5,5), F(6,5)\}$:
  - Distance to $D$: $\sqrt{4^2 + 3^2} = 5.000$
  - Distance to $E$: $\sqrt{4^2 + 4^2} = \sqrt{32} \approx 5.657$
  - Distance to $F$: $\sqrt{5^2 + 4^2} = \sqrt{41} \approx 6.403$
  - Separation $b(A) = \frac{5.000 + 5.657 + 6.403}{3} = \frac{17.060}{3} \approx \mathbf{5.687}$
- Silhouette Coefficient:
  $$s(A) = \frac{5.687 - 1.000}{\max(1.000, 5.687)} = \frac{4.687}{5.687} \approx \mathbf{0.824}$$
  *(Matches the whiteboard lecture value $s(A) \approx 0.82$ exactly!)*

---

### 3.4 Additional Validation Metrics: Davies-Bouldin & Calinski-Harabasz

In automated machine learning pipelines where human engineers cannot visually inspect elbow plots, two additional metrics provide programmatic cluster evaluation:

#### 1. Davies-Bouldin Index (DBI):
Measures the average similarity between each cluster and its most similar peer:
$$R_{ij} = \frac{s_i + s_j}{d(\boldsymbol{\mu}_i, \boldsymbol{\mu}_j)}$$
Where $s_i$ is the average distance of points in cluster $i$ to centroid $\boldsymbol{\mu}_i$, and $d(\boldsymbol{\mu}_i, \boldsymbol{\mu}_j)$ is the distance between centroids.
$$\text{DBI} = \frac{1}{K} \sum_{i=1}^{K} \max_{j \ne i} R_{ij}$$
- **Lower DBI is better**: Indicates clusters that are internally tight ($s_i$ small) and widely separated ($d(\boldsymbol{\mu}_i, \boldsymbol{\mu}_j)$ large).

#### 2. Calinski-Harabasz Index (Variance Ratio Criterion):
The ratio of between-cluster dispersion to within-cluster dispersion:
$$\text{CH} = \frac{\text{Tr}(\mathbf{B}_K) / (K - 1)}{\text{Tr}(\mathbf{W}_K) / (n - K)}$$
Where $\mathbf{B}_K$ is the between-cluster scatter matrix and $\mathbf{W}_K$ is the within-cluster scatter matrix.
- **Higher CH is better**: Reflects dense, well-separated clusters with fast $O(1)$ computation time.

**Citations & References:**
- Arthur, D., & Vassilvitskii, S. (2007). k-means++: The advantages of careful seeding. SODA, 1027-1035.

---

## 4. Selecting k: The Elbow Method, Silhouette Analysis & Failure Modes
### 4.1 Hierarchical Agglomerative Clustering: The Bottom-Up Tree

Unlike K-Means, which requires choosing $K$ upfront and flattens data into Voronoi cells, **Hierarchical Agglomerative Clustering (HAC)** builds a rich, nested hierarchy of clusters:

```
The Agglomerative Algorithm:
  1. Start with n clusters (each data point is its own cluster of size 1).
  2. Compute pairwise distance matrix D between all clusters.
  3. Repeat until only 1 master cluster remains:
        a. Identify the two closest clusters (A, B) according to Linkage Criterion.
        b. Merge them into a single cluster (A U B).
        c. Record the merge height (distance) in the linkage matrix Z.
```

---

### 4.2 The Four Linkage Criteria

How do we measure the distance between two clusters of points $A$ and $B$?

```
Linkage Criteria Visualized:
   Single Linkage (Min)        Complete Linkage (Max)       Average Linkage (Mean)
      (Nearest pair)               (Farthest pair)             (All pairs mean)
     A           B                A           B               A           B
    (o)───────(o)                (o)                         (o)═══╤═══(o)
     │         │                  │           │                │   │   │
     │         │                  │           │                │   │   │
    (o)       (o)                 └──(o)─────(o)──┘           (o)═══╧═══(o)
```

| Linkage Metric | Mathematical Definition | Geometric Behavior | Critical Failure Mode |
| :--- | :--- | :--- | :--- |
| **Single Linkage** | $d(A, B) = \min_{u \in A, v \in B} \|\mathbf{u} - \mathbf{v}\|$ | Connects closest points; can trace non-linear, curved manifolds (moons, spirals). | **Chaining**: A single line of noise points bridges two distinct clusters into one giant chain. |
| **Complete Linkage** | $d(A, B) = \max_{u \in A, v \in B} \|\mathbf{u} - \mathbf{v}\|$ | Considers the farthest points; enforces compact, equal-diameter spherical clusters. | **Outlier Sensitivity**: A single extreme outlier violently inflates merge height. |
| **Average Linkage (UPGMA)**| $d(A, B) = \frac{1}{|A||B|}\sum_{u \in A}\sum_{v \in B} \|\mathbf{u} - \mathbf{v}\|$ | Robust compromise between Single and Complete; balances cluster variances. | Computationally slower ($O(n^2 \log n)$). |
| **Ward's Linkage** | $\Delta \text{ESS} = \frac{|A||B|}{|A|+|B|}\|\boldsymbol{\mu}_A - \boldsymbol{\mu}_B\|^2$ | Minimizes increase in total within-cluster variance; produces clean, balanced clusters. | Assumes spherical, Gaussian-distributed clusters (like K-Means). |

---

### 4.3 Hand-Calculated Walkthrough: Whiteboard 2 (1D Points: 1, 2, 5, 7.5, 12)

Let us trace agglomerative merges by hand on the 1D dataset from class whiteboard 2:
Five points on the real number line: $\{1.0, 2.0, 5.0, 7.5, 12.0\}$.

#### Initial Pairwise Distances:
- $|1 - 2| = \mathbf{1.0}$
- $|2 - 5| = 3.0$
- $|5 - 7.5| = 2.5$
- $|7.5 - 12| = 4.5$

#### Step 1: Smallest Distance is between 1 and 2 ($d = 1.0$)
- Merge $\{1\}$ and $\{2\}$ into cluster $C_{12} = \{1, 2\}$.
- Merge Height = **$1.0$**.
- Remaining clusters: $\{1, 2\}, \{5\}, \{7.5\}, \{12\}$.

#### Step 2: Compare Distances to $\{5\}$
- Single Linkage: $d(\{1, 2\}, \{5\}) = \min(|1-5|, |2-5|) = |2-5| = 3.0$.
- Distance between $\{5\}$ and $\{7.5\}$ is $|5 - 7.5| = \mathbf{2.5}$.
- Smallest distance is $2.5 \implies$ Merge $\{5\}$ and $\{7.5\}$ into cluster $C_{5,7.5} = \{5, 7.5\}$.
- Merge Height = **$2.5$**.
- Remaining clusters: $\{1, 2\}, \{5, 7.5\}, \{12\}$.

#### Step 3: Compare Remaining Clusters
- Single Linkage between $C_{12}$ and $C_{5,7.5}$: $\min(|2-5|) = \mathbf{3.0}$.
- Distance between $C_{5,7.5}$ and $\{12\}$: $|7.5 - 12| = 4.5$.
- Smallest distance is $3.0 \implies$ Merge $\{1, 2\}$ and $\{5, 7.5\}$.
- Merge Height = **$3.0$**.
- Remaining clusters: $\{1, 2, 5, 7.5\}$ and $\{12\}$.

#### Step 4: Final Merge with Outlier $\{12\}$
- Merge Height = $|7.5 - 12| = \mathbf{4.5}$.

```
Dendrogram Structure for 1D Whiteboard Points:
    Height ^
       5.0 │                                   ┌────────── 12.0
           │               ┌───────────────────┴──────────┐
       4.0 │               │                              │
       3.0 │       ┌───────┴───────┐                      │
           │       │               │                      │  <-- CUT AT HEIGHT 4.0:
       2.0 │       │          ┌────┴────┐                 │      Yields 2 Clusters:
           │   ┌───┴───┐      │         │                 │      {1, 2, 5, 7.5} and {12}
       1.0 │   │       │      │         │                 │
       0.0 ┴───┴───────┴──────┴─────────┴─────────────────┴► Points
              1.0     2.0    5.0       7.5               12.0
```

> **Cutting the Dendrogram**:
> If we draw a horizontal cut line across the dendrogram at **Height = 4.0**:
> It crosses exactly **2 vertical branches**, yielding:
> - Cluster A: $\{1.0, 2.0, 5.0, 7.5\}$
> - Cluster B: $\{12.0\}$ (the isolated outlier!).

---

### 4.4 The Lance-Williams Recurrence Formula

In 1967, Lance and Williams unified all hierarchical clustering algorithms into a single generalized recurrence formula:
When two clusters $A$ and $B$ merge into $A \cup B$, the distance from the new merged cluster to any remaining cluster $C$ is computed in $O(1)$ time without examining raw points:

$$d(A \cup B, C) = \alpha_A d(A, C) + \alpha_B d(B, C) + \beta d(A, B) + \gamma |d(A, C) - d(B, C)|$$

```
Lance-Williams Parameter Values:
┌─────────────────────┬──────────────────┬──────────────────┬──────────────────┬────────────────────────────────────┐
│ Linkage Method      │ α_A              │ α_B              │ β                │ γ                                  │
├─────────────────────┼──────────────────┼──────────────────┼──────────────────┼────────────────────────────────────┤
│ **Single Linkage**  │ 1/2              │ 1/2              │ 0                │ -1/2                               │
│ **Complete Linkage**│ 1/2              │ 1/2              │ 0                │ +1/2                               │
│ **Average Linkage** │ |A| / (|A| + |B|)│ |B| / (|A| + |B|)│ 0                │ 0                                  │
│ **Ward's Linkage**  │ (|A|+|C|)/(|A|+|B|+|C|) │ (|B|+|C|)/(|A|+|B|+|C|) │ -|C|/(|A|+|B|+|C|) │ 0                  │
└─────────────────────┴──────────────────┴──────────────────┴──────────────────┴────────────────────────────────────┘
```

This brilliant formula allows SciPy and Scikit-Learn to build dendrograms in $O(n^2)$ time instead of recomputing distances from scratch!

**Citations & References:**
- Rousseeuw, P. J. (1987). Silhouettes: a graphical aid to the interpretation and validation of cluster analysis. CAM, 20, 53-65.

---

## 5. Hierarchical Agglomerative Clustering & Dendrograms
### 5.1 Hands-On Python Implementation: End-to-End Customer Segmentation

The following production script implements, tunes, and diagnoses customer segmentation using both K-Means and Hierarchical Agglomerative Clustering on a mall customer dataset:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, silhouette_samples

# 1. Synthesize Mall Customer Dataset (400 shoppers, 4 continuous features)
np.random.seed(42)
n_shoppers = 400

age = np.random.normal(38, 12, n_shoppers).clip(18, 70)
annual_income_lakh = np.concatenate([
    np.random.normal(3.5, 0.8, 100),   # Low Income
    np.random.normal(7.5, 1.2, 200),   # Moderate Income
    np.random.normal(14.0, 2.0, 100)   # High Income
]).clip(1.5, 25.0)

spending_score = np.concatenate([
    np.random.normal(25, 8, 120),      # Conservative Spenders
    np.random.normal(55, 10, 160),     # Moderate Spenders
    np.random.normal(85, 6, 120)       # VIP High Spenders
]).clip(1, 100)

visits_per_month = np.random.poisson(4, n_shoppers).clip(1, 15)

df = pd.DataFrame({
    "age": age,
    "annual_income_lakh": annual_income_lakh,
    "spending_score": spending_score,
    "visits_per_month": visits_per_month
})

# 2. Strict Standardization (Mandatory for Euclidean Distance!)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# 3. Determine Optimal K via Elbow Method and Silhouette Analysis
k_range = range(2, 11)
inertias = []
sil_scores = []

for k in k_range:
    km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    sil_scores.append(silhouette_score(X_scaled, km.labels_))

best_k = k_range[np.argmax(sil_scores)]
print(f"Optimal K selected by Peak Silhouette Score: K = {best_k} (Score: {max(sil_scores):.4f})")

# 4. Fit Final K-Means Model
final_km = KMeans(n_clusters=best_k, init="k-means++", n_init=10, random_state=42)
df["Cluster_KM"] = final_km.fit_predict(X_scaled)

# 5. Profile Customer Segments for Business Stakeholders
segment_profiles = df.groupby("Cluster_KM").mean().round(2)
segment_profiles["Shopper_Count"] = df["Cluster_KM"].value_counts()
print("\n=== CUSTOMER SEGMENT PERSONAS ===")
print(segment_profiles)

# 6. Fit Agglomerative Clustering with Ward Linkage for Validation
hac_ward = AgglomerativeClustering(n_clusters=best_k, linkage="ward")
df["Cluster_HAC"] = hac_ward.fit_predict(X_scaled)
print(f"\nHAC (Ward) Silhouette Score: {silhouette_score(X_scaled, df['Cluster_HAC']):.4f}")
```

---

### 5.2 Diagnostic Failure Modes & Geometric Blind Spots

| Geometric Blind Spot | Underlying Mechanism | Catastrophic Symptom | Recommended Alternative Algorithm |
| :--- | :--- | :--- | :--- |
| **Non-Convex Manifolds (Moons, Spirals, Rings)** | K-Means partitions space using flat linear Voronoi hyperplanes. | Cuts concentric rings or interlocking moons in half, assigning points across boundaries. | **DBSCAN** (density-based), **Single-Linkage HAC**, or **Spectral Clustering**. |
| **Unequal Cluster Variances (Density Mismatch)** | K-Means objective $J$ minimizes sum of squared Euclidean errors isotropically. | Splits large diffuse clusters into artificial pieces; merges small dense clusters together. | **Gaussian Mixture Models (GMM)** with unconstrained covariance matrices. |
| **Anisotropic (Elongated / Correlated) Clusters** | Euclidean distance implicitly assumes spherical, uncorrelated clusters ($\mathbf{\Sigma} = \mathbf{I}$). | Misclassifies points along the principal axis of spread. | **GMM with Full Covariance** or Mahalanobis distance whitening. |
| **Unscaled Physical Dimensions** | Large numerical features overwhelm smaller ones in Euclidean squared sum. | Algorithm completely ignores vital demographic features (e.g. Age). | Enforce `StandardScaler` inside an automated preprocessing pipeline. |
| **Extreme Outliers** | Squared distance $\|\mathbf{x} - \boldsymbol{\mu}\|^2$ penalizes distant anomalies severely. | A single extreme outlier drags a centroid far away from real clusters, creating a useless 1-point cluster. | **K-Medoids (PAM)** or **DBSCAN** (which flags outliers as noise label `-1`). |

---

### 5.3 Production Code: Plotting Per-Sample Silhouette Diagrams

A single scalar average silhouette score can hide localized cluster collapse.
A **Silhouette Diagram** visualizes the distribution of silhouette values within each cluster:

```python
# Compute per-sample silhouette scores
sample_sil_values = silhouette_samples(X_scaled, df["Cluster_KM"])

for cluster_id in range(best_k):
    cluster_scores = sample_sil_values[df["Cluster_KM"] == cluster_id]
    cluster_scores.sort()
    
    avg_score = cluster_scores.mean()
    negative_ratio = (cluster_scores < 0).mean()
    
    print(f"Cluster {cluster_id}: Count = {len(cluster_scores):3d} | "
          f"Avg Silhouette = {avg_score:.3f} | "
          f"Misclustered Points (< 0) = {negative_ratio * 100:.1f}%")
```

If any cluster displays a wide band of negative silhouette scores ($s(i) < 0$), it indicates that points in that cluster are closer to a neighboring cluster, signaling that $K$ should be adjusted or that cluster shapes are non-spherical!

**Citations & References:**
- Ward, J. H. (1963). Hierarchical grouping to optimize an objective function. JASA, 58(301), 236-244.
- Müllner, D. (2011). Modern hierarchical, agglomerative clustering algorithms. arXiv:1109.2378.

---
