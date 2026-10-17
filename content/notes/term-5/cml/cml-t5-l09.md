# 9. K-Nearest Neighbours (k-NN), Distance Metrics & The Curse of Dimensionality
**Term:** Term 5 | **Subject:** CML | **Note ID:** `cml-t5-l09`
**Last Updated:** 2026-10-18T00:00:00Z

## Abstract & Summary
A comprehensive, intuitive masterclass on K-Nearest Neighbours (k-NN) and metric-space learning. Explores the non-parametric, instance-based paradigm where 'training' consists of memorizing data and inference computes local neighborhood majorities. Deconstructs Euclidean, Manhattan, and Minkowski distances, demonstrates why unscaled features blind the algorithm, maps the Bias-Variance tradeoff as k shifts from 1 to n, and proves why high-dimensional feature spaces suffer from distance concentration.

## Learning Objectives
- Understand instance-based (lazy) learning and contrast k-NN with parametric models (Linear and Logistic Regression).
- Calculate and contrast distance metrics (Euclidean, Manhattan, Minkowski) and explain why feature scaling is strictly mandatory.
- Analyze how hyperparameter k governs the Bias-Variance tradeoff from k=1 (high variance) to k=n (high bias).
- Explain the geometric reality of the Curse of Dimensionality and the distance concentration phenomenon.
- Implement production k-NN classification and regression pipelines using Scikit-Learn, KD-Trees, and BallTrees.

## Key Takeaways
- k-NN is a non-parametric, lazy learner: it learns no explicit mathematical formula (no weights w); training stores the dataset, and all computation occurs at query time.
- Classification predicts via local majority vote; Regression predicts via the arithmetic mean (or median) of the k nearest neighbors.
- Distance metrics (Euclidean L2, Manhattan L1) depend entirely on feature units; failing to standardize features allows wide-scale features to completely dominate distance calculations.
- Small k (k = 1) yields complex, fragmented decision boundaries with zero training error (High Variance / Overfitting); Large k (k = n) yields flat, rigid predictions equal to the global majority (High Bias / Underfitting).
- In binary classification, choose an odd integer for k to naturally prevent 50-50 voting deadlocks.
- The Curse of Dimensionality causes hyperspace volume to concentrate in outer shells; as dimension d grows, all pairwise distances converge to the same value, rendering distance discrimination useless.
- KD-Trees and BallTrees accelerate neighbor queries in low-to-moderate dimensions (d < 20), but degrade to O(n) brute-force linear scans in high dimensions.

---

## 1. Instance-Based Learning: The Lazy Paradigm of k-NN
### 1.1 The Lazy Learning Paradigm: Zero Training, Heavy Inference

Most machine learning algorithms we study (Linear Regression, Logistic Regression, Decision Trees, Support Vector Machines) belong to the family of **Eager Learners**:
- During the training phase, they analyze the training dataset, solve an optimization problem, extract abstract parameters (weights $\mathbf{w}$, split rules), and then **discard the raw training data**.
- At inference time, predicting a new observation requires only evaluating a compact mathematical formula: $\hat{y} = \sigma(\mathbf{w}^T \mathbf{x} + w_0)$ or traversing a pre-built tree.
- Inference is instantaneous ($O(d)$ or $O(\text{depth})$), and the model footprint in RAM is tiny (just the weights).

In stark contrast, **$k$-Nearest Neighbors ($k$-NN)** is a classic **Lazy Learner (Instance-Based Learner / Memory-Based Learner)**:
- **Training Phase ($O(1)$ Time)**: The algorithm does virtually zero computation during training. It simply memorizes and stores the training feature vectors $\mathbf{X} \in \mathbb{R}^{n \times d}$ and targets $\mathbf{y} \in \mathbb{R}^n$ directly in memory (or organizes them into spatial index trees).
- **Inference Phase ($O(n \cdot d)$ Time)**: When a query point $\mathbf{x}_q$ arrives, the algorithm computes distances between $\mathbf{x}_q$ and **every single stored training point**, finds the $k$ closest observations, and aggregates their labels.
- **Memory Footprint**: The model **is** the entire training dataset. For a dataset with $n = 1,000,000$ rows and $d = 300$ dense embedding features (float64), storing the model in RAM requires $10^6 \times 300 \times 8 \text{ bytes} \approx 2.4 \text{ GB}$ of physical memory just to serve predictions!

```
Eager Learning vs. Lazy Learning Workflow:
   Eager Learning (e.g., Logistic Regression / Neural Net):
      [ Training Data ] ──► [ Intensive Optimization (GD / Adam) ] ──► [ Model Weights w ]
                                                                                │
      Query Point x_q ──────────────────────────────────────────────────────────┴─► Instant Pred: O(d)

   Lazy Learning (k-NN):
      [ Training Data ] ──► [ Zero Optimization! Store in RAM ] ──► Stored Database in Memory (O(n*d) RAM)
                                                                                │
      Query Point x_q ──► [ Compute Distances to ALL n Points ] ────────────────┴─► Query Time: O(n*d)
```

---

### 1.2 Algorithmic Formulation: Classification & Regression Rules

#### 1. Classification (Majority Voting)
Given a query point $\mathbf{x}_q$, identify the set $\mathcal{N}_k(\mathbf{x}_q)$ containing the indices of the $k$ closest training points under chosen metric $D(\cdot, \cdot)$.
The predicted class $\hat{y}$ is determined by the mode (plurality / majority vote):

$$\hat{y}(\mathbf{x}_q) = \operatorname{mode}\left(\{y^{(i)} \mid i \in \mathcal{N}_k(\mathbf{x}_q)\}\right)$$

The estimated posterior class probability for class $c$ is the local empirical proportion:
$$\hat{P}(Y = c \mid \mathbf{x}_q) = \frac{1}{k} \sum_{i \in \mathcal{N}_k(\mathbf{x}_q)} \mathbb{I}(y^{(i)} = c)$$

#### 2. Regression (Neighborhood Averaging)
In regression, targets $y \in \mathbb{R}$ are continuous quantities (e.g., house prices, hospital length of stay):

$$\hat{y}(\mathbf{x}_q) = \frac{1}{k} \sum_{i \in \mathcal{N}_k(\mathbf{x}_q)} y^{(i)}$$

*Robust Variant*: Instead of the arithmetic mean, we can compute the **median** of the $k$ neighbors to insulate the prediction from local extreme outliers or recording anomalies.

---

### 1.3 Concrete Hand-Calculated Regression Walkthrough: Uniform vs. Distance Weighting

Suppose an automated valuation model predicts house price for a query home $Q$. Its $k = 5$ nearest neighbors in feature space have the following actual selling prices and distances:
- Neighbor 1: Price $y_1 = 320{,}000\text{ USD}$, Distance $d_1 = 1.0$ km
- Neighbor 2: Price $y_2 = 340{,}000\text{ USD}$, Distance $d_2 = 1.5$ km
- Neighbor 3: Price $y_3 = 350{,}000\text{ USD}$, Distance $d_3 = 2.0$ km
- Neighbor 4: Price $y_4 = 390{,}000\text{ USD}$, Distance $d_4 = 3.0$ km
- Neighbor 5: Price $y_5 = 450{,}000\text{ USD}$, Distance $d_5 = 5.0$ km

#### Method A: Uniform Average ($k = 5$)
Every neighbor gets equal weight $w_i = \frac{1}{5} = 0.20$:
$$\hat{y}_{\text{uniform}} = \frac{320 + 340 + 350 + 390 + 450}{5} = \frac{1{,}850}{5} = \mathbf{370{,}000\text{ USD}}$$

#### Method B: Inverse Distance Weighting ($w_i = 1 / d_i$)
Points that are geographically and architecturally closer should exert stronger influence on the predicted valuation:
- $w_1 = 1 / 1.0 = 1.0000$
- $w_2 = 1 / 1.5 \approx 0.6667$
- $w_3 = 1 / 2.0 = 0.5000$
- $w_4 = 1 / 3.0 \approx 0.3333$
- $w_5 = 1 / 5.0 = 0.2000$
- Sum of weights $\sum_{i=1}^5 w_i = 1.0000 + 0.6667 + 0.5000 + 0.3333 + 0.2000 = \mathbf{2.7000}$

Normalized weights $\tilde{w}_i = w_i / \sum w_j$:
- $\tilde{w}_1 = 1.0000 / 2.7000 \approx 0.3704$ ($37.0\%$ of total vote)
- $\tilde{w}_2 = 0.6667 / 2.7000 \approx 0.2469$ ($24.7\%$ of total vote)
- $\tilde{w}_3 = 0.5000 / 2.7000 \approx 0.1852$ ($18.5\%$ of total vote)
- $\tilde{w}_4 = 0.3333 / 2.7000 \approx 0.1235$ ($12.3\%$ of total vote)
- $\tilde{w}_5 = 0.2000 / 2.7000 \approx 0.0741$ ($7.4\%$ of total vote)

$$\hat{y}_{\text{weighted}} = 0.3704(320,000) + 0.2469(340,000) + 0.1852(350,000) + 0.1235(390,000) + 0.0741(450,000)$$
$$\hat{y}_{\text{weighted}} = 118,528 + 83,946 + 64,820 + 48,165 + 33,345 = \mathbf{348{,}804\text{ USD}}$$

#### Method C: Gaussian Radial Basis Function (RBF) Kernel Weighting
Instead of inverse distance, standard kernel regression uses a smooth Gaussian decay:
$$w_i = \exp\left(-\frac{d_i^2}{2\sigma^2}\right)$$
Where bandwidth parameter $\sigma$ dictates the radius of neighborhood influence:
Suppose $\sigma = 2.0$ km ($\implies 2\sigma^2 = 8.0$):
- $w_1 = \exp(-1.0^2 / 8.0) = \exp(-0.125) \approx \mathbf{0.8825}$
- $w_2 = \exp(-1.5^2 / 8.0) = \exp(-0.28125) \approx \mathbf{0.7548}$
- $w_3 = \exp(-2.0^2 / 8.0) = \exp(-0.500) \approx \mathbf{0.6065}$
- $w_4 = \exp(-3.0^2 / 8.0) = \exp(-1.125) \approx \mathbf{0.3247}$
- $w_5 = \exp(-5.0^2 / 8.0) = \exp(-3.125) \approx \mathbf{0.0439}$
- Total sum: $\sum w_i = 0.8825 + 0.7548 + 0.6065 + 0.3247 + 0.0439 = \mathbf{2.6124}$

Notice how the distant neighbor at $5.0$ km receives only a tiny $0.0439$ weight under the Gaussian kernel ($1.7\%$ of influence), naturally filtering out distant noise!

---

### 1.4 Voronoi Tessellation & The Cover-Hart Asymptotic Theoretical Bound

When $k = 1$, the feature space is partitioned into convex polyhedral cells called a **Voronoi Diagram (Voronoi Tessellation)**:
For each training point $\mathbf{x}^{(i)}$, its Voronoi cell $V(\mathbf{x}^{(i)})$ contains all query locations in $\mathbb{R}^d$ closer to $\mathbf{x}^{(i)}$ than to any other training sample:
$$V(\mathbf{x}^{(i)}) = \left\{ \mathbf{x} \in \mathbb{R}^d \mid \|\mathbf{x} - \mathbf{x}^{(i)}\| \le \|\mathbf{x} - \mathbf{x}^{(j)}\| \; \forall j \ne i \right\}$$

```
Voronoi Tessellation (k = 1 Partitioning of Feature Space):
        x2 ^
           │      \      /             * = Class 1 (Positive)
           │       \ *  /              o = Class 0 (Negative)
           │   *    \  /      *
           │  ───────┼───────────────
           │   o    / \        o
           │       /   \   o
           │      /  o  \
           +─────/───────\──────────► x1
```

#### The Celebrated Cover & Hart (1967) Theorem:
One of the most foundational mathematical proofs in statistical pattern recognition demonstrates that the humble 1-NN rule has extraordinary asymptotic guarantees:
Let $R^*$ denote the **Bayes Optimal Error Rate** (the absolute theoretical lower bound on classification error achievable by an omniscient observer with perfect knowledge of the true posterior probability distributions $P(Y \mid X)$).
As sample size $n \to \infty$, the asymptotic error rate of the 1-NN classifier $R_{\text{1-NN}}$ satisfies:

$$R^* \le R_{\text{1-NN}} \le 2R^*(1 - R^*) \le 2R^*$$

> **Theoretical Milestone**:
> No matter how arbitrarily complex or non-linear the underlying probability distributions are, given enough training data, **the error rate of the nearest neighbor classifier is bounded above by at most twice the optimal Bayes error**!
> Formally, if the optimal Bayes error is $5\%$, the 1-NN classifier will never exceed $2(0.05)(0.95) = 9.5\%$ error as $n \to \infty$. Half of all classification information resides in the single nearest neighbor.

**Citations & References:**
- Cover, T., & Hart, P. (1967). Nearest neighbor pattern classification. IEEE Transactions on Information Theory, 13(1), 21-27.
- Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer, Chapter 2.

---

## 2. Distance Metrics: Euclidean, Manhattan & The Minkowski Family
### 2.1 The Minkowski Distance Family

Distance is the fundamental yardstick of $k$-NN. The general mathematical formulation for vector distance between $\mathbf{x}, \mathbf{z} \in \mathbb{R}^d$ is the **Minkowski Distance** of order $p$:

$$D_p(\mathbf{x}, \mathbf{z}) = \|\mathbf{x} - \mathbf{z}\|_p = \left( \sum_{j=1}^d |x_j - z_j|^p \right)^{1/p}$$

```
Unit Circles (Points at Distance = 1.0 from Origin) Across Minkowski Orders:
     Manhattan (p = 1)          Euclidean (p = 2)          Chebyshev (p -> inf)
           x2 ^                       x2 ^                       x2 ^
            1 |    /\                  1 |   .---.                1 | ┌───────┐
              |   /  \                   |  /     \                 | │       │
      -1 -----+----+----+ 1      -1 -----+--+-----+--+ 1    -1 -----+─┼───────┼─ 1
              |   \  /                   |  \     /                 | │       │
           -1 |    \/                 -1 |   '---'               -1 | └───────┘
              +---------> x1             +---------> x1             +---------> x1
             Diamond                     Circle                     Square
```

#### 1. Manhattan Distance ($p = 1$, City Block / Taxicab Distance)
$$D_1(\mathbf{x}, \mathbf{z}) = \sum_{j=1}^d |x_j - z_j|$$
- Measures movement strictly along orthogonal coordinate axes (like a taxi navigating the grid layout of Manhattan).
- **Outlier Robustness**: Because coordinate differences are not squared, a massive anomaly along one single feature does not disproportionately dominate the overall metric.
- Recommended when working in higher dimensions or when data has heavy-tailed noise.

#### 2. Euclidean Distance ($p = 2$, Ruler / L2 Distance)
$$D_2(\mathbf{x}, \mathbf{z}) = \sqrt{\sum_{j=1}^d (x_j - z_j)^2}$$
- The standard straight-line distance in Euclidean geometry.
- **Isotropic**: Rotationally invariant; distances do not depend on the orientation of the coordinate axes.
- Highly sensitive to extreme single-feature deviations because coordinate errors are squared before summing.

#### 3. Chebyshev Distance ($p \to \infty$, Chessboard / L-Infinity Distance)
$$D_\infty(\mathbf{x}, \mathbf{z}) = \lim_{p \to \infty} \left( \sum_{j=1}^d |x_j - z_j|^p \right)^{1/p} = \max_{j \in \{1, \dots, d\}} |x_j - z_j|$$
- Measures the number of moves a King needs to travel between two squares on an $8 \times 8$ chessboard (since the King can move diagonally, horizontally, or vertically in 1 step).
- Reflects the single worst-case dimensional difference between two feature vectors.

#### 4. Cosine Similarity & Cosine Distance
When vector magnitude is irrelevant and only the **angular orientation** carries meaning (e.g., text document classification where document length varies, or facial recognition embeddings):

$$\text{Cosine Similarity} = \cos(\theta) = \frac{\mathbf{x} \cdot \mathbf{z}}{\|\mathbf{x}\|_2 \|\mathbf{z}\|_2} = \frac{\sum x_j z_j}{\sqrt{\sum x_j^2}\sqrt{\sum z_j^2}} \in [-1, 1]$$
$$\text{Cosine Distance} = 1 - \cos(\theta) \in [0, 2]$$

#### 5. Mahalanobis Distance (Covariance-Aware Distance)
Standard Euclidean distance implicitly assumes that all features are uncorrelated and have equal variance ($\mathbf{\Sigma} = \mathbf{I}$). When features are strongly correlated (e.g., Height and Weight), Euclidean distance distorts true statistical similarity.
The **Mahalanobis Distance** scales differences by the inverse covariance matrix $\mathbf{\Sigma}^{-1}$:

$$D_M(\mathbf{x}, \mathbf{z}) = \sqrt{(\mathbf{x} - \mathbf{z})^T \mathbf{\Sigma}^{-1} (\mathbf{x} - \mathbf{z})}$$

- Warps space so that level curves of equal distance are ellipsoids aligned with the principal axes of data spread.
- Statistically equivalent to standardizing features and decorrelating them via PCA whitening before calculating Euclidean distance!

---

### 2.2 Concrete Hand-Calculated Walkthrough: 2D Neighbor Ranking Reversal

Suppose a query point arrives at $\mathbf{x}_q = (3.0, 4.0)$, and we have three candidate training samples in the database:
- Point $A = (1.0, 2.0)$ with Class 1
- Point $B = (4.0, 7.0)$ with Class 0
- Point $C = (6.0, 4.0)$ with Class 1

Let us compute the exact distances under Manhattan ($L_1$), Euclidean ($L_2$), and Chebyshev ($L_\infty$) metrics:

| Candidate Point | Coordinate $(x_1, x_2)$ | Coordinate Differences $(\Delta x_1, \Delta x_2)$ | Manhattan Distance ($L_1$) | Euclidean Distance ($L_2$) | Chebyshev Distance ($L_\infty$) | Class Label |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Point A** | $(1.0, 2.0)$ | $|3 - 1| = 2.0, \; |4 - 2| = 2.0$ | $2.0 + 2.0 = \mathbf{4.00}$ | $\sqrt{2^2 + 2^2} = \sqrt{8} \approx \mathbf{2.828}$ | Class 1 |
| **Point B** | $(4.0, 7.0)$ | $|3 - 4| = 1.0, \; |4 - 7| = 3.0$ | $1.0 + 3.0 = \mathbf{4.00}$ | $\sqrt{1^2 + 3^2} = \sqrt{10} \approx \mathbf{3.162}$ | Class 0 |
| **Point C** | $(6.0, 4.0)$ | $|3 - 6| = 3.0, \; |4 - 4| = 0.0$ | $3.0 + 0.0 = \mathbf{3.00}$ | $\sqrt{3^2 + 0^2} = \sqrt{9} = \mathbf{3.000}$ | Class 1 |

#### Neighbor Ranking Comparison:
- Under **Manhattan ($L_1$)**:
  1. Rank 1: **Point C** ($D_1 = 3.00$) $\implies$ Prediction for $k=1$ is **Class 1**.
  2. Rank 2: **Point A & Point B Tied!** ($D_1 = 4.00$)
- Under **Euclidean ($L_2$)**:
  1. Rank 1: **Point A** ($D_2 = 2.828$) $\implies$ Prediction for $k=1$ is **Class 1**.
  2. Rank 2: **Point C** ($D_2 = 3.000$)
  3. Rank 3: **Point B** ($D_2 = 3.162$)
- Under **Chebyshev ($L_\infty$)**:
  1. Rank 1: **Point A** ($\max(2, 2) = \mathbf{2.00}$)
  2. Rank 2: **Point B & Point C Tied!** ($\max(1, 3) = \mathbf{3.00}$ vs $\max(3, 0) = \mathbf{3.00}$)

> **Crucial Pedagogical Takeaway**:
> The choice of distance metric **alters the neighbor ranking**!
> Under Euclidean distance, Point $A$ is closest ($2.828 < 3.000$); under Manhattan distance, Point $C$ is closest ($3.00 < 4.00$). Metric selection is a critical hyperparameter that dictates which geometric patterns the algorithm prioritizes.

**Citations & References:**
- Deza, M. M., & Deza, E. (2009). Encyclopedia of Distances. Springer.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). Springer.

---

## 3. The Scaling Imperative: Why Unscaled Features Blind k-NN
### 3.1 The Feature Magnitude Catastrophe

Imagine building a loan default classifier with two features:
- $x_1$ = `Annual Salary` in dollars (ranges from 20,000 USD to 200,000 USD).
- $x_2$ = `Age` in years (ranges from $18$ to $75$).

Suppose we have two applicants compared to query applicant $Q = (60{,}000, 30)$: 
- Applicant $A_1 = (61{,}000, 30)$: Salary differs by 1,000 USD, Age is identical.
- Applicant $A_2 = (60{,}000, 70)$: Salary is identical, Age differs by 40 years (an entire generation!).

Let us compute Euclidean distance to query applicant $Q$:
$$D(Q, A_1) = \sqrt{(60000 - 61000)^2 + (30 - 30)^2} = \sqrt{(-1{,}000)^2 + 0^2} = \sqrt{1{,}000{,}000} = \mathbf{1{,}000.0}$$
$$D(Q, A_2) = \sqrt{(60000 - 60000)^2 + (30 - 70)^2} = \sqrt{0^2 + (-40)^2} = \sqrt{1{,}600} = \mathbf{40.0}$$

#### The Disastrous Illusion:
The algorithm declares that $A_2$ (a 70-year-old pensioner) is **25 times closer** to a 30-year-old millennial than $A_1$ (another 30-year-old who makes 1,000 USD more)!
Because Salary is measured in tens of thousands while Age is measured in tens, squared salary differences completely overpower age differences by factors of millions.
The algorithm is **completely blind to Age**! Distance metrics calculate isotropic geometry; they cannot know that 1,000 USD is a negligible salary increment while 40 years is a massive biological span.

---

### 3.2 Standardization vs. MinMax Normalization

To ensure every feature contributes equitably to geometric distance, features must be transformed to a shared numerical scale:

```
Feature Scaling Comparison:
┌─────────────────────┬────────────────────────────────────┬────────────────────────────────────┐
│ Attribute           │ StandardScaler (Z-Score)           │ MinMaxScaler                       │
├─────────────────────┼────────────────────────────────────┼────────────────────────────────────┤
│ Mathematical Formula│ z = (x - μ) / σ                    │ x_norm = (x - x_min)/(x_max - x_min│
│ Output Range        │ Unbounded, centered at 0 (σ = 1)   │ Strictly bounded in [0, 1]         │
│ Outlier Handling    │ Robust: preserves relative spread  │ Fragile: an extreme outlier squashes│
│                     │ without compressing normal points  │ all normal data into a tiny cluster│
│ Recommended Regime  │ Default for k-NN, SVM, Ridge/Lasso │ Bounded coordinates, image pixels  │
└─────────────────────┴────────────────────────────────────┴────────────────────────────────────┘
```

#### Re-evaluating the Loan Applicants After Z-Score Standardization:
Suppose in the population:
- Salary has mean $\mu_{\text{sal}} = 60{,}000\text{ USD}$ and std $\sigma_{\text{sal}} = 20{,}000\text{ USD}$.
- Age has mean $\mu_{\text{age}} = 35$ and std $\sigma_{\text{age}} = 10$.

Let us transform query $Q$ and candidate applicants $A_1, A_2$:
- Query $Q = (60k, 30) \implies z_Q = \left(\frac{60k - 60k}{20k}, \frac{30 - 35}{10}\right) = (0.00, -0.50)$
- Applicant $A_1 = (61k, 30) \implies z_{A_1} = \left(\frac{61k - 60k}{20k}, \frac{30 - 35}{10}\right) = (+0.05, -0.50)$
- Applicant $A_2 = (60k, 70) \implies z_{A_2} = \left(\frac{60k - 60k}{20k}, \frac{70 - 35}{10}\right) = (0.00, +3.50)$

Now compute standardized Euclidean distances:
$$D(z_Q, z_{A_1}) = \sqrt{(0.00 - 0.05)^2 + (-0.50 - (-0.50))^2} = \sqrt{0.0025 + 0} = \mathbf{0.050}$$
$$D(z_Q, z_{A_2}) = \sqrt{(0.00 - 0.00)^2 + (-0.50 - 3.50)^2} = \sqrt{0 + (-4.0)^2} = \mathbf{4.000}$$

Now, applicant $A_1$ is **80 times closer** to query $Q$ than $A_2$ ($0.050 \ll 4.000$), perfectly aligning model geometry with true financial and demographic reality!

---

### 3.3 Handling Categorical Features & Gower's Distance

What happens when data contains a mix of numerical features and categorical features (e.g., `City: [Delhi, Mumbai, Bengaluru]` or `Education: [High School, Bachelors, Masters]`)?
- **The One-Hot Encoding Trap**:
  If a nominal feature with 10 categories is one-hot encoded into 10 binary columns ($0$ or $1$), two samples differing in that category have squared Euclidean distance $(\Delta x)^2 = 1^2 + 1^2 = 2.0$ (distance $\sqrt{2} \approx 1.414$).
  If numerical features are standardized to variance $1.0$, a single categorical discrepancy can overpower several numerical features!
- **Gower's General Distance**:
  For mixed datasets, Gower's metric defines pairwise distance between observations $\mathbf{x}_i, \mathbf{x}_j$ as:
  $$S_{ij} = \frac{\sum_{k=1}^p w_k s_{ijk}}{\sum_{k=1}^p w_k}$$
  Where for numerical feature $k$, $s_{ijk} = 1 - \frac{|x_{ik} - x_{jk}|}{R_k}$ ($R_k$ is the feature range), and for categorical feature $k$, $s_{ijk} = 1$ if $x_{ik} == x_{jk}$ else $0$. Gower's distance is then $D_G = 1 - S_{ij} \in [0, 1]$.

**Citations & References:**
- Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (3rd ed.). O'Reilly Media, Chapter 2.

---

## 4. Choosing k: Navigating the Bias-Variance Spectrum
### 4.1 The Bias-Variance Trade-Off Across $k$

The number of neighbors $k$ is the master hyperparameter controlling model complexity:

```
The Spectrum of k:
  k = 1                                k = Optimal Sweet Spot                      k = n
  ├──────────────────────────────────────────────┼────────────────────────────────────┤
  High Variance (Overfitting)          Balanced Generalization            High Bias (Underfitting)
  Complex, jagged boundaries           Smooth boundary separating signal  Flat boundary everywhere
  Train Error = 0.0!                   Optimal test set performance       Predicts majority class
```

| Hyperparameter Setting | Effective Degrees of Freedom | Model Complexity | Behavior on Outliers & Noise |
| :--- | :--- | :--- | :--- |
| **$k = 1$ (Minimum $k$)** | Maximum ($n$ parameters) | **Extreme Overfitting** (High Variance). Training error is identically $0.0\%$. | A single mislabeled training point creates an isolated "island" in feature space that misclassifies nearby test points. |
| **$k$ Small ($3 - 7$)** | High | Flexible, localized decision boundaries. | Captures subtle non-linear boundaries while averaging out isolated noise spikes. |
| **$k$ Moderate ($11 - 25$)** | Balanced | **Optimal Trade-off**. Low generalization error. | Broad statistical consensus; filters out measurement noise. |
| **$k = n$ (Maximum $k$)** | Minimum ($1$ parameter) | **Extreme Underfitting** (High Bias). | Evaluates all $n$ samples in the dataset for every query, predicting the global majority class everywhere. |

---

### 4.2 Non-Linear Decision Boundaries: Comparing Logistic Regression vs. $k$-NN

In class, we visualized a synthetic dataset with 400 observations across two features ($F_1, F_2$) where classes overlap in non-linear curved geometries:

```
Boundary Geometry Comparison:
   Logistic Regression (Parametric Linear):       k-NN (Non-Parametric Local):
        F2 ^                                           F2 ^
           │         /  Straight Line                     │        .---.  Flexible Local Contour
           │  +  +  /   (Cannot bend!)                    │  +  + /     \
           │   +   /  +                                   │   +  |   +   |
           │  ────/─────────                              │  ────+───────+──
           │  o  /   o                                    │  o  o \     / o
           │    /  o                                      │        '---'
           +───/────────────────► F1                      +─────────────────► F1
```

1. **Why Logistic Regression Struggles**:
   Logistic regression can only construct straight lines ($w_1 F_1 + w_2 F_2 + w_0 = 0$) or flat hyperplanes. If the true class boundary is circular, crescent-shaped, or interleaved, a straight line will inevitably misclassify large clusters of points.
2. **Why $k$-NN Excels on Non-Linear Geometries**:
   Because $k$-NN makes zero assumptions about the functional form of the boundary, it organically flexes and bends around complex geometric clusters, forming circular, winding, or multi-modal boundary enclosures.

---

### 4.3 Tie-Breaking Rules & Distance-Weighted Voting

#### 1. Why $k$ Should Be Odd for Binary Classification
If $k = 4$ in binary classification, a query point might find 2 neighbors of Class 0 and 2 neighbors of Class 1 ($2 - 2$ tie).
To prevent arbitrary tie-breaking, **always select odd values of $k$** ($k \in \{3, 5, 7, 9, \dots\}$) when solving binary classification problems.
For multi-class problems ($C > 2$), ties can still occur even with odd $k$ (e.g., $k=5$ with 2 votes for Class A, 2 votes for Class B, 1 vote for Class C). Common tie-breaking strategies include:
1. Fall back to 1-NN (pick the class of the single closest neighbor).
2. Weight votes by inverse distance.
3. Randomly break ties (non-deterministic).

#### 2. Distance-Weighted Voting (`weights='distance'`)
In standard uniform voting (`weights='uniform'`), a neighbor located $0.001$ units away has the exact same voting weight as a neighbor located $9.999$ units away.
Under **Distance-Weighted Voting**, each neighbor's vote is weighted inversely by its distance:

$$w_i = \frac{1}{D(\mathbf{x}_q, \mathbf{x}^{(i)}) + \epsilon}$$

Where $\epsilon$ is a tiny positive constant (e.g., $10^{-5}$) to prevent division by zero if a query point coincides with a training point.
- Nearby neighbors exert a massive gravitational pull on the prediction.
- Distant background points on the periphery of the neighborhood have negligible impact.

**Citations & References:**
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). Springer, Chapter 2.
- James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). An Introduction to Statistical Learning. Springer, Chapter 2.

---

## 5. The Curse of Dimensionality & Metric Collapse
### 5.1 The Geometry of High Dimensions: Space Becomes Exponentially Empty

Human intuition is calibrated in 2D and 3D space, where volume is compact. In high-dimensional machine learning ($d = 50, 100, 1000$), geometry behaves in bizarre, counter-intuitive ways:

> **The Unit Hypercube Paradox**:
> Suppose observations are uniformly distributed in a $d$-dimensional unit hypercube $[0, 1]^d$.
> To capture a fraction $r$ of the data points in a localized neighborhood, we must construct a hypercube of edge length $s$:
> $$\text{Volume} = s^d = r \implies s = r^{1/d}$$

Let us calculate the required neighborhood edge length $s$ to capture just **10% of the data ($r = 0.10$)**:
- In $d = 1$ dimension: $s = (0.10)^{1/1} = \mathbf{0.10}$ (Requires only 10% of the axis length).
- In $d = 2$ dimensions: $s = (0.10)^{1/2} \approx \mathbf{0.32}$ (Requires 32% of each axis).
- In $d = 10$ dimensions: $s = (0.10)^{1/10} \approx \mathbf{0.794}$ (Must span nearly 80% of each feature's entire range!).
- In $d = 100$ dimensions: $s = (0.10)^{1/100} \approx \mathbf{0.977}$ (Must span 98% of each feature's range!).

To find even 10% of your nearest neighbors in 100-dimensional space, your "local neighborhood" must stretch across **almost the entire breadth of the universe**!
Neighbors are no longer "local" in high dimensions.

---

### 5.2 The Inscribed Hypersphere Volume Vanishing Theorem

Consider a $d$-dimensional hypercube $[-1, 1]^d$ with side length $2$, whose total volume is:
$$V_{\text{cube}}(d) = 2^d$$
Inside this hypercube, inscribe a $d$-dimensional hypersphere of radius $R = 1$. The volume of a $d$-dimensional sphere is given by:
$$V_{\text{sphere}}(d) = \frac{\pi^{d/2}}{\Gamma\left(\frac{d}{2} + 1\right)}$$

Let us compute the ratio of the volume of the inscribed sphere to the surrounding cube as dimension $d$ grows:
$$\text{Ratio}(d) = \frac{V_{\text{sphere}}(d)}{V_{\text{cube}}(d)} = \frac{\pi^{d/2}}{2^d \cdot \Gamma\left(\frac{d}{2} + 1\right)}$$

| Dimension $d$ | Hypercube Volume $2^d$ | Inscribed Hypersphere Volume | Sphere / Cube Volume Ratio | Physical Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **$d = 1$** | $2^1 = 2$ | $2.000$ | $1.0000$ ($100.0\%$) | The sphere (line segment) fills the entire box. |
| **$d = 2$** | $2^2 = 4$ | $\pi \approx 3.1416$ | $\frac{\pi}{4} \approx 0.7854$ ($78.5\%$) | A circle occupies most of the square. |
| **$d = 3$** | $2^3 = 8$ | $\frac{4}{3}\pi \approx 4.1888$ | $\frac{\pi}{6} \approx 0.5236$ ($52.4\%$) | A ball fills over half the cube. |
| **$d = 5$** | $2^5 = 32$ | $\frac{8\pi^2}{15} \approx 5.2638$ | $0.1645$ ($16.5\%$) | Most volume is now outside the sphere. |
| **$d = 10$** | $2^{10} = 1,024$ | $\frac{\pi^5}{120} \approx 2.5502$ | $0.00249$ ($\mathbf{0.25\%}$) | Over $99.7\%$ of volume is in the corners! |
| **$d = 20$** | $2^{20} \approx 1.05 \times 10^6$ | $\approx 0.0258$ | $2.46 \times 10^{-8}$ ($\mathbf{0.000002\%}$) | The sphere volume is virtually zero. |

$$\lim_{d \to \infty} \frac{V_{\text{sphere}}(d)}{V_{\text{cube}}(d)} = 0$$

> **Geometrical Consequence**:
> In high dimensions, the interior volume of the hypersphere completely vanishes!
> **Almost 100% of the volume in high-dimensional space is concentrated in the spiky "corners" of the hypercube.**
> Points do not cluster in the interior; they all lie along the outer shell!

---

### 5.3 Metric Collapse: The Distance Concentration Phenomenon

In 1999, Beyer et al. proved a mathematically devastating property of high-dimensional metrics:
Under broad distributional assumptions, as dimensionality $d \to \infty$, the distance to the **farthest point** and the distance to the **nearest point** converge to the same value:

$$\lim_{d \to \infty} \frac{D_{\max} - D_{\min}}{D_{\min}} = 0$$

```
Distance Concentration Ratio as Dimensionality Increases:
   (D_max - D_min) / D_min
      ^
      │  \
      │   \
      │    '.
      │      '--.
      │          '───────────────────► 0.0 (All points become equidistant!)
      +────────────────────────────────► Dimension d
      d = 2         d = 20        d = 100
```

#### The Engineering Disaster:
If the nearest neighbor is at distance $10.00$ and the farthest neighbor is at distance $10.01$, all data points are virtually equidistant from the query point.
The concept of a "nearest neighbor" completely collapses, and $k$-NN degrades into **random neighbor selection**.

#### Practical Remedies for the Curse of Dimensionality:
1. **Dimensionality Reduction**: Apply **PCA** or UMAP to compress $100$ features down to the $10-15$ principal axes carrying $95\%$ of variance.
2. **Feature Selection**: Use **Lasso (L1)** or Mutual Information to delete uninformative noise features before computing distances.
3. **Domain Metrics**: Use Manhattan ($L_1$) distance, which degrades much more gracefully in high dimensions than Euclidean ($L_2$) distance.

**Citations & References:**
- Bellman, R. (1957). Dynamic Programming. Princeton University Press.
- Beyer, K., Goldstein, J., Ramakrishnan, R., & Shaft, U. (1999). When is 'nearest neighbor' meaningful? ICDT 1999, 217-235.

---

## 6. Hands-On Python Implementations & Algorithmic Indexing
### 6.1 Computational Complexity: Brute Force vs. KD-Trees vs. Ball-Trees

Evaluating distances against all $n$ training points for every query requires $O(n \cdot d)$ operations. For real-time applications (e.g., search engines, fraud scoring with $n = 10^7$), brute-force search is far too slow.

```
Spatial Indexing Strategies:
┌─────────────────┬──────────────────┬──────────────────┬──────────────────┬────────────────────────────────────┐
│ Algorithm       │ Training Build   │ Query Time       │ Space Complexity │ Optimal Operational Regime         │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┼────────────────────────────────────┤
│ **Brute Force** │ $O(1)$           │ $O(n \cdot d)$   │ $O(n \cdot d)$   │ Small datasets ($n < 1,000$) or    │
│                 │ (Instant)        │ (Slowest)        │                  │ very high dimensions ($d > 50$).   │
│ **KD-Tree**     │ $O(d \cdot n\log n│ $O(\log n)$      │ $O(n \cdot d)$   │ Low dimensions ($d < 20$) with     │
│                 │                  │ (Fastest)        │                  │ Euclidean/Manhattan metrics.       │
│ **Ball-Tree**   │ $O(d \cdot n\log n│ $O(\log n)$      │ $O(n \cdot d)$   │ Moderate dimensions ($d \le 40$)   │
│                 │                  │                  │                  │ and arbitrary distance metrics.    │
└─────────────────┴──────────────────┴──────────────────┴──────────────────┴────────────────────────────────────┘
```

#### Detailed KD-Tree Construction & Search Walkthrough:
A $k$-d tree (short for $k$-dimensional tree) recursively bisects feature space using axis-aligned orthogonal hyperplanes:
1. **Cycle Dimensions**: At depth 0, split along axis $x_1$ at the median value. All points with $x_1 < \text{median}$ go to the left child; points with $x_1 \ge \text{median}$ go to the right child.
2. At depth 1, split each subset along axis $x_2$ at their respective medians.
3. At depth $m$, split along axis $x_{(m \bmod d) + 1}$.
4. **Query & Branch Pruning**:
   - Descend the tree to find the leaf containing query point $\mathbf{x}_q$ (candidate best neighbor at distance $r$).
   - Backtrack up the tree. For each parent node, check if a sphere of radius $r$ centered at $\mathbf{x}_q$ crosses the splitting hyperplane:
     $$|\mathbf{x}_{q, \text{split\_axis}} - \text{split\_val}| < r$$
   - If the sphere crosses the hyperplane, the other subtree **must** be searched; if it does not cross, the entire opposite branch is **pruned**, saving millions of calculations!
   - In high dimensions ($d > 20$), the hypersphere almost always intersects every dividing hyperplane, forcing the algorithm to visit virtually every node ($O(n)$ collapse).

---

### 6.2 Production Scikit-Learn Pipeline: Hyperparameter Grid Search

```python
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# 1. Load benchmark medical diagnostic dataset (30 continuous features)
data = load_breast_cancer()
X, y = data.data, data.target

# 2. Strict Stratified Train / Test Partition (Prevent leakage)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 3. Encapsulate in Leak-Free Pipeline
# StandardScaler fits ONLY on training folds during CV to prevent data leakage!
knn_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(algorithm="auto"))
])

# 4. Hyperparameter Search Grid
param_grid = {
    "knn__n_neighbors": [1, 3, 5, 7, 9, 11, 15, 21, 29],
    "knn__weights": ["uniform", "distance"],
    "knn__metric": ["euclidean", "manhattan"]
}

# 5. Execute Stratified 5-Fold Cross-Validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid_search = GridSearchCV(
    knn_pipeline,
    param_grid,
    cv=cv,
    scoring="roc_auc",
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

# 6. Evaluate Best Tuned Model on Untouched Test Set
best_model = grid_search.best_estimator_
y_probs = best_model.predict_proba(X_test)[:, 1]
y_preds = best_model.predict(X_test)

test_auc = roc_auc_score(y_test, y_probs)

print("=== BEST HYPERPARAMETER CONFIGURATION ===")
print(f"Optimal Parameters: {grid_search.best_params_}")
print(f"Best CV ROC-AUC:    {grid_search.best_score_:.4f}")
print(f"Holdout Test AUC:   {test_auc:.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_preds))
print("\nClassification Report:")
print(classification_report(y_test, y_preds, target_names=data.target_names))
```

---

### 6.3 Diagnostic Failure Modes & Engineering Pitfalls

| Engineering Pitfall | Root Mechanism | Catastrophic Consequence | Production Solution |
| :--- | :--- | :--- | :--- |
| **Omitting Feature Scaling** | Features with large numerical spans dominate Euclidean sum of squares. | Small-scale features (e.g., Age) are completely ignored; distance geometry corrupted. | Enforce `StandardScaler` inside a Scikit-Learn `Pipeline`. |
| **Choosing Even $k$ in Binary Problems** | Equal neighbor voting counts split 50/50. | Arbitrary tie-breaking introduces non-deterministic random predictions. | Always select odd $k$ values ($k \in \{3, 5, 7, \dots\}$). |
| **Deploying Brute-Force in Latency-Critical APIs** | $O(n \cdot d)$ linear scan over millions of stored records per query. | Inference latency exceeds SLA limits (500ms+ per API call). | Use spatial indexing (`algorithm='ball_tree'`) or approximate nearest neighbors (FAISS/HNSW). |
| **Running $k$-NN on $d > 100$ Features** | Distance concentration phenomenon: $D_{\max} \approx D_{\min}$. | All points become equidistant; algorithm degrades to random coin flips. | Precede $k$-NN with PCA or Lasso feature selection to reduce dimensions below 20. |
| **Scaling Categorical One-Hot Columns Inappropriately** | One-hot binary columns span $0$ to $1$, creating artificial Euclidean leaps. | Distance metric is distorted by arbitrary category card. | Use Gower's distance or target encoding, or standardize continuous features appropriately. |
| **Data Leakage in Normalization** | Normalizing the entire dataset before train-test split. | Test distribution information leaks into train scaling params ($\mu, \sigma$), giving optimistic validation metrics. | Fit scalers exclusively on training splits inside `Pipeline`. |

**Citations & References:**
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. JMLR, 12, 2825-2830.

---
