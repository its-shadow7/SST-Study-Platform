# Lecture 9: K-Nearest Neighbours & The Curse of Dimensionality
## Student Notes — SST Classical Machine Learning

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Contrast **Lazy (Instance-Based) Learning** against **Eager Learning**, analyzing their time and memory complexities during training versus inference ($\mathcal{O}(1)$ training vs. $\mathcal{O}(n d)$ inference).
- Formulate the **Minkowski Distance Family** ($L_p$ norm) and prove how **Manhattan ($L_1$)**, **Euclidean ($L_2$)**, and **Chebyshev ($L_\infty$)** distances emerge as specific parameterizations of $p$.
- Explain geometrically and algebraically why **Feature Standardization is strictly mandatory** for distance-based learners.
- Formulate $k$-NN for both **Classification** (majority voting, inverse-distance weighting) and **Regression** (local conditional mean).
- Analyze the **Bias–Variance Tradeoff as a function of $k$**, proving why $k = 1$ maximizes variance (Voronoi tessellation) while $k = n$ maximizes bias.
- Mathematically formulate the **Curse of Dimensionality**: the **Empty Space Phenomenon** (hypercube volume growth) and the **Distance Concentration Phenomenon** ($\frac{d_{\max} - d_{\min}}{d_{\min}} \to 0$).

---

## 1. Lazy vs. Eager Learning: The Computational Inversion

All parametric models studied so far (Linear Regression, Ridge, Lasso, Logistic Regression) are **Eager Learners**:
- They invest significant compute during training to condense the training dataset $\mathcal{D}$ into a compact parameter vector $\mathbf{w}^* \in \mathbb{R}^{d+1}$.
- Once trained, the dataset $\mathcal{D}$ can be completely discarded. Inference takes $\mathcal{O}(d)$ floating-point operations ($\hat{y} = \mathbf{w}^T \mathbf{x}$).

In contrast, **$K$-Nearest Neighbours ($k$-NN)** is a **Lazy (Instance-Based / Non-Parametric) Learner**:
- There is **no training phase** in the conventional sense. "Training" simply means loading the dataset into memory: $\mathcal{O}(1)$ training time!
- There are **no learned mathematical weights** $\mathbf{w}$. The entire training dataset *is* the model.
- **The Computational Burden is Shifted to Inference**: To predict for a single query point $\mathbf{x}^*$, the algorithm must scan all $n$ training instances, compute $n$ Euclidean distance metrics in $d$ dimensions, and sort them:

  $$\text{Inference Complexity (Brute Force)} = \mathcal{O}(n \cdot d + n \log k)$$

```
   Eager Learner (Logistic / Linear Regression):
   Training (Expensive):   Dataset ──► [ Gradient Descent / OLS ] ──► Parameters w*
   Inference (Instant):    Query x* ──► [ w*ᵀ x* ] ──► ŷ (O(d) time; fast & lightweight)

   Lazy Learner (k-NN):
   Training (Free):        Dataset ──► [ Store in RAM ] (O(1) time)
   Inference (Expensive):  Query x* ──► [ Compute distances to all n points ] ──► ŷ (O(nd) time)
```

> [!TIP]
> **Scaling $k$-NN in Production**:  
> For large datasets ($n > 100,000$), brute-force search is too slow for real-time APIs ($>50\text{ms}$).  
> Engineers deploy spatial tree indexing data structures (**KD-Trees**, **Ball-Trees**) or vector search engines (**HNSW / FAISS**) which reduce search complexity to $\mathcal{O}(d \log n)$.

---

## 2. The Algorithm Step-by-Step

Given a labeled training set $\mathcal{D} = \{(\mathbf{x}^{(i)}, y^{(i)})\}_{i=1}^n$ and an unseen query vector $\mathbf{x}^*$:

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                       THE k-NN INFERENCE PIPELINE                      │
   ├────────────────────────────────────────────────────────────────────────┤
   │ 1. Distance Calculation: Compute distance d(x*, x⁽ⁱ⁾) to all n points. │
   │ 2. Sorting & Filtering: Sort distances ascending; select the k         │
   │    closest training points: 𝒩_k(x*).                                  │
   │ 3. Aggregation:                                                        │
   │    • Classification: Majority vote among the k labels.                 │
   │    • Regression: Compute the arithmetic mean of the k target values.   │
   └────────────────────────────────────────────────────────────────────────┘
```

### Classification Aggregation

$$\hat{y}(\mathbf{x}^*) = \arg\max_{c \in \mathcal{Y}} \sum_{i \in \mathcal{N}_k(\mathbf{x}^*)} \mathbb{I}(y^{(i)} = c)$$

#### Weighted Majority Voting
Instead of giving equal democratic weight to all $k$ neighbors, we weight votes inversely by their distance:

$$w_i = \frac{1}{d(\mathbf{x}^*, \mathbf{x}^{(i)})^2 + \epsilon}$$
$$\hat{y}(\mathbf{x}^*) = \arg\max_{c \in \mathcal{Y}} \sum_{i \in \mathcal{N}_k(\mathbf{x}^*)} w_i \cdot \mathbb{I}(y^{(i)} = c)$$

A neighbor right next to $\mathbf{x}^*$ exerts vastly greater influence than a neighbor barely inside the $k$-boundary.

### Regression Aggregation

$$h(\mathbf{x}^*) = \frac{1}{k} \sum_{i \in \mathcal{N}_k(\mathbf{x}^*)} y^{(i)}$$

---

## 3. Distance Metrics: The Minkowski Family

The definition of "nearest" depends entirely on the mathematical metric space chosen. Most metrics belong to the **Minkowski Distance Family** ($L_p$ norm):

$$D_p(\mathbf{x}, \mathbf{z}) = \|\mathbf{x} - \mathbf{z}\|_p = \left( \sum_{j=1}^d |x_j - z_j|^p \right)^{\frac{1}{p}}$$

```
   ┌─────────┬──────────────────────┬────────────────────────────────────┬────────────────────────┐
   │ Norm    │ Metric Name          │ Formula                            │ Geometry / Physical    │
   ├─────────┼──────────────────────┼────────────────────────────────────┼────────────────────────┤
   │ p = 1   │ Manhattan (L₁)       │ d₁ = Σ |xⱼ - zⱼ|                   │ Grid / City-Block path │
   ├─────────┼──────────────────────┼────────────────────────────────────┼────────────────────────┤
   │ p = 2   │ Euclidean (L₂)       │ d₂ = √[ Σ (xⱼ - zⱼ)² ]             │ Straight-line ruler    │
   ├─────────┼──────────────────────┼────────────────────────────────────┼────────────────────────┤
   │ p → ∞   │ Chebyshev (L_∞)      │ d_∞ = maxⱼ |xⱼ - zⱼ|               │ Chessboard King move   │
   └─────────┴──────────────────────┴────────────────────────────────────┴────────────────────────┘
```

```
   Geometric Comparison in 2D:
   z = (4, 4)
   ▲          Euclidean (Straight line: d₂ = 4.24)
   │         /
   │        / 
   │       /  Manhattan (Grid path: d₁ = 3 + 3 = 6.00)
   │  ┌───┴───┐
   │  │       │
   └──•───────┴────────►
   x = (1, 1)
   Always: d₁ ≥ d₂ ≥ d_∞
```

### Worked Numerical Example
Let $\mathbf{x} = [1, 1]^T$ and $\mathbf{z} = [4, 5]^T$:
- **Euclidean ($L_2$)**:

  $$d_2 = \sqrt{(4 - 1)^2 + (5 - 1)^2} = \sqrt{3^2 + 4^2} = \sqrt{9 + 16} = \sqrt{25} = \mathbf{5.0}$$

- **Manhattan ($L_1$)**:

  $$d_1 = |4 - 1| + |5 - 1| = 3 + 4 = \mathbf{7.0}$$

- **Chebyshev ($L_\infty$)**:

  $$d_\infty = \max(|4 - 1|, |5 - 1|) = \max(3, 4) = \mathbf{4.0}$$

### Cosine Distance (For High-Dimensional Embeddings)
In text vectorization and deep learning embeddings, vector magnitude is often irrelevant compared to directional orientation:

$$\text{Cosine Similarity} = \cos(\theta) = \frac{\mathbf{x} \cdot \mathbf{z}}{\|\mathbf{x}\|_2 \|\mathbf{z}\|_2}$$
$$\text{Cosine Distance} = 1 - \text{Cosine Similarity} = 1 - \frac{\mathbf{x} \cdot \mathbf{z}}{\|\mathbf{x}\|_2 \|\mathbf{z}\|_2}$$

---

## 4. Why Feature Standardization is Strictly Mandatory

In $k$-NN, distances across all feature dimensions are pooled into a single scalar sum:

$$d_2(\mathbf{x}, \mathbf{z}) = \sqrt{ (x_{\text{income}} - z_{\text{income}})^2 + (x_{\text{age}} - z_{\text{age}})^2 }$$

Suppose:
- Annual Income varies from $\$20,000$ to $\$200,000$ ($\Delta \approx \$10,000$).
- Age varies from $18$ to $65$ ($\Delta \approx 5$ years).

Squaring the differences:
- $\Delta_{\text{income}}^2 \approx (10,000)^2 = \mathbf{100,000,000}$
- $\Delta_{\text{age}}^2 \approx (5)^2 = \mathbf{25}$

$$\text{Distance} = \sqrt{100,000,000 + 25} \approx 10,000.0012$$

**The age feature is completely annihilated!** The nearest neighbors will simply be individuals with identical salaries, even if one is 19 years old and the other is 64 years old. Standardizing all features to $\mu = 0, \sigma = 1$ ensures every feature exerts equitable geometric influence.

---

## 5. Choosing $k$ and the Bias–Variance Tradeoff

The hyperparameter $k$ controls the effective capacity and smoothness of the decision boundary:

```
   k = 1 (Overfitting / High Variance):        k = 15 (Balanced Decision Surface):         k = n (Underfitting / High Bias):
   x₂                                          x₂                                          x₂
   ▲                                           ▲                                           ▲
   │    ╭─╮                                    │           ╭───────────╮                   │  ═══════════════════════════════
   │   │ • │  Island of Class 1                │          │  Class 1   │                   │   Predicts Majority Class
   │    ╰─╯                                    │           ╰───────────╯                   │   Everywhere!
   │   Voronoi Polygonal Cells                 │   Smooth, robust boundary                 │
   └──────────────────────────► x₁             └──────────────────────────► x₁             └──────────────────────────► x₁
   Train Error = 0%; Test Error explodes!      Optimal Generalization                      Flat horizontal decision; 0 capacity
```

### The Extremes of $k$

| Hyperparameter Setting | Decision Boundary Topology | Bias–Variance State | Practical Consequence |
| :--- | :--- | :--- | :--- |
| **$k = 1$** | Voronoi tessellation cells surrounding every training point | **Minimum Bias, Maximum Variance** | Memorizes training noise and label errors; zero training error, collapses on test. |
| **$k = \text{Optimal } k^*$** | Smooth, locally adaptive non-linear surface | **Balanced Bias and Variance** | Filters random label noise while capturing local class clusters. |
| **$k = n$** | Entire feature space assigned to the global dataset majority class | **Maximum Bias, Minimum Variance** | Completely ignores input query $\mathbf{x}^*$; outputs static global mode. |

> [!IMPORTANT]
> **Why Odd Values of $k$ for Binary Classification?**  
> If $k$ is even (e.g., $k = 4$), a query point can easily receive an exact $2 - 2$ tie vote. Choosing an odd integer ($k = 3, 5, 7, 9, \dots$) mathematically prevents ties in two-class problems.

---

## 6. The Curse of Dimensionality

$k$-NN relies fundamentally on the **Local Constant Assumption**:  
> Points close to each other in feature space share similar target labels: $f(\mathbf{x}^*) \approx f(\mathbf{x}^{(i)})$ when $\|\mathbf{x}^* - \mathbf{x}^{(i)}\| \ll 1$.

In high-dimensional space ($d > 50$), **this assumption shatters completely** due to two counter-intuitive geometric phenomena:

### Phenomenon 1: The Empty Space Phenomenon (Hypercube Volume)
Consider a $d$-dimensional unit hypercube $[0, 1]^d$ with volume $V = 1^d = 1$.  
Suppose we wish to capture a tiny local sub-cube centered at the origin that contains just **$10\%$ of the data** ($\text{Volume } V_{\text{sub}} = 0.10$).  
What must the edge length $s$ of this sub-cube be?

$$V_{\text{sub}} = s^d = 0.10 \implies s = (0.10)^{\frac{1}{d}}$$

```
   Dimension (d)       Edge Length (s) required to capture 10% volume
   d = 1               s = (0.10)¹      = 0.10  (Local: spans 10% of axis)
   d = 2               s = (0.10)¹ᐟ²    = 0.32  (Spans 32% of each axis)
   d = 10              s = (0.10)¹ᐟ¹⁰   = 0.79  (Spans 79% of each axis!)
   d = 100             s = (0.10)¹ᐟ¹⁰⁰  = 0.98  (Spans 98% of the ENTIRE space!)
```
To capture a mere $10\%$ of data in 100 dimensions, your neighborhood must span **$98\%$ of the entire universe**! The concept of a "local neighborhood" ceases to exist.

### Phenomenon 2: Distance Concentration
In high dimensions, the contrast between the nearest point and the farthest point vanishes.
Let $\mathbf{x}$ and $\mathbf{z}$ be $d$-dimensional random vectors with independent coordinates. By the Central Limit Theorem, the Euclidean distance $\|\mathbf{x} - \mathbf{z}\|_2 = \sqrt{\sum_{j=1}^d (x_j - z_j)^2}$ has mean scaling as $\mathcal{O}(\sqrt{d})$, while its standard deviation remains constant $\mathcal{O}(1)$.

$$\lim_{d \to \infty} \frac{d_{\max} - d_{\min}}{d_{\min}} \longrightarrow 0$$

```
   Distance Distribution Concentration in High Dimensions:
   Probability Density
    ▲
    │                     d = 500 Dimensions
    │                        ╭───╮  All pairwise distances
    │                       │     │ concentrate tightly around √d!
    │                      │       │
    │   d = 2             │         │
    │   ╭────────╮       │           │
    │  │          │     │             │
    └──┴──────────┴─────┴─────────────┴──────────► Pairwise Distance
       Wide spread:     d_max ≈ d_min!
       Nearest is clear Nearest neighbor is barely closer than farthest!
```
When the nearest neighbor is $99.9\%$ as far away as the most distant point in the dataset, **distance loses all discriminatory meaning**.

---

## 7. Complete Scikit-Learn Implementation: KNN Classification & Hyperparameter Search

```python
"""
K-Nearest Neighbours with Scikit-Learn
Demonstrates Pipeline scaling, GridSearchCV for k and metric, and decision boundaries.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# 1. Generate Non-Linear 2D Dataset (Two Intertwined Moons)
X, y = make_moons(n_samples=600, noise=0.25, random_state=42)

# 2. Strict Train-Test Hygiene
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# 3. Assemble Pipeline (Mandatory StandardScaler + KNN)
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier())
])

# 4. Hyperparameter Optimization via 5-Fold Cross-Validation
param_grid = {
    "knn__n_neighbors": np.arange(1, 31, 2), # Odd k to avoid ties
    "knn__weights": ["uniform", "distance"], # Test inverse-distance weighting
    "knn__p": [1, 2]                         # 1 = Manhattan, 2 = Euclidean
}

grid_search = GridSearchCV(
    pipe, param_grid, cv=5, scoring="accuracy", n_jobs=-1
)
grid_search.fit(X_train, y_train)

# 5. Best Hyperparameter Extraction
best_model = grid_search.best_estimator_
best_params = grid_search.best_params_

print("=" * 55)
print("OPTIMAL k-NN HYPERPARAMETERS:")
print(f"Optimal k:       {best_params['knn__n_neighbors']}")
print(f"Weighting:       {best_params['knn__weights']}")
print(f"Distance Metric: {'Manhattan (L1)' if best_params['knn__p'] == 1 else 'Euclidean (L2)'}")
print(f"Best CV Score:   {grid_search.best_score_:.4f}")
print("=" * 55)

# 6. Evaluate on Final Holdout Test Set
y_pred_test = best_model.predict(X_test)
test_acc = accuracy_score(y_test, y_pred_test)
print(f"\nFinal Unseen Test Accuracy: {test_acc:.4f}")
print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred_test, target_names=["Moon 0", "Moon 1"]))
```

---

## 8. Common Pitfalls & Interview-Grade Questions

### Q1: An intern trains a 1-NN model on a dataset with no duplicate points and reports 100% accuracy on the training set. Is the model broken or is this mathematically guaranteed?
**Answer**:  
This is **mathematically guaranteed for unique training instances**. When evaluating a 1-NN model on a training instance $\mathbf{x}^{(i)}$, the algorithm searches $\mathcal{D}_{\text{train}}$ for the closest point. The point closest to $\mathbf{x}^{(i)}$ in Euclidean distance is $\mathbf{x}^{(i)}$ itself ($d(\mathbf{x}^{(i)}, \mathbf{x}^{(i)}) = 0$). It retrieves its own ground-truth label $y^{(i)}$, resulting in a trivial $100\%$ training accuracy. This is a classic hallmark of high variance / severe memorization. The training accuracy of 1-NN provides zero diagnostic value regarding out-of-sample generalization.

### Q2: Why does K-Nearest Neighbours fail catastrophically when applied directly to raw 1024-dimensional pixel arrays for image classification?
**Answer**:  
Raw pixel spaces suffer intensely from the **Curse of Dimensionality** and the failure of pixel-level Euclidean distance to reflect semantic meaning. Two identical images of a cat—one shifted by 3 pixels to the right—will have huge pixel-by-pixel Euclidean distance, appearing farther apart than a dark cat and a black dog. Furthermore, in 1024 dimensions, distance concentration collapses pairwise distances into a uniform band ($\frac{d_{\max}-d_{\min}}{d_{\min}} \approx 0$). $k$-NN should only be applied to images after passing them through a convolutional feature extractor or autoencoder to obtain low-dimensional, semantically dense embeddings.

### Q3: What is the computational complexity of predicting a single query point in a dataset of $n = 1,000,000$ instances with $d = 100$ features using brute-force $k$-NN?
**Answer**:  
Computing the Euclidean distance between the query and a single training point requires $d$ subtractions, $d$ squarings, and $d-1$ additions ($\approx 3d$ FLOPs). Across $n$ instances, computing all distances takes $\mathcal{O}(n \cdot d) = 1,000,000 \times 100 = 10^8$ operations. Finding the $k$ smallest distances requires an $\mathcal{O}(n \log k)$ partial selection heap. For $k = 10$, this takes an additional $\approx 3.3 \times 10^6$ operations. A single query requires roughly $100\text{M}$ floating-point operations! For an API serving 1,000 requests per second, brute-force $k$-NN is completely unviable without KD-Trees or Approximate Nearest Neighbor (ANN) indexers.

---

## 9. Summary & Key Takeaways

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                     SESSION 9 KEY TAKEAWAYS                            │
   ├────────────────────────────────────────────────────────────────────────┤
   │ 1. Lazy vs. Eager: k-NN has zero training time O(1); all compute is    │
   │    deferred to inference time: O(nd + n log k).                        │
   │ 2. Minkowski Family: Unified metric D_p(x, z). p=1 gives Manhattan;    │
   │    p=2 gives Euclidean; p=∞ gives Chebyshev.                           │
   │ 3. Mandatory Scaling: Because distance sums over all dimensions,       │
   │    features with large numerical magnitudes completely swamp others.   │
   │ 4. Bias-Variance Tradeoff: Small k (k=1) creates complex Voronoi cells │
   │    (high variance); large k (k=n) predicts the global majority (bias). │
   │ 5. Odd k for Binary: Selecting odd values for k mathematically prevents│
   │    tie-breaking deadlocks in binary classification.                    │
   │ 6. Curse of Dimensionality: In high dimensions, neighborhoods must span│
   │    nearly the entire volume, and pairwise distances concentrate.       │
   └────────────────────────────────────────────────────────────────────────┘
```
