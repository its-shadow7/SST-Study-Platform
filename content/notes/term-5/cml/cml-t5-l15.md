# 15. Dimensionality Reduction: Principal Component Analysis (PCA) & Variance Maximization
**Term:** Term 5 | **Subject:** CML | **Note ID:** `cml-t5-l15`
**Last Updated:** 2026-10-18T00:00:00Z

## Abstract & Summary
An intuitive yet mathematically rigorous guide to Principal Component Analysis (PCA) and Dimensionality Reduction. Establishes variance as the geometric currency of information, uses the torch-and-shadow analogy to explain projection, demystifies eigenvalues and eigenvectors as stretch factors and invariant directions of the covariance matrix, demonstrates the catastrophic 'forgot-to-scale' trap, guides component selection via scree plots, and constructs production Scikit-Learn pipelines for visualization, compression, and classification.

## Learning Objectives
- Explain why dimensionality reduction is necessary for visualization, computational speed, noise filtering, and distance metric stability.
- Articulate the geometric intuition of PCA: rotating coordinate axes to align with directions of maximum data spread (variance).
- Demonstrate why standardizing features (mean 0, variance 1) is mandatory before PCA to avoid arbitrary physical unit dominance.
- Define eigenvalues and eigenvectors in plain language and calculate explained variance ratios step-by-step.
- Select the optimal number of principal components using scree plots, cumulative variance thresholds, and cross-validated downstream models.
- Implement PCA pipelines in Scikit-Learn without data leakage for high-dimensional visualization and lossy data compression.

## Key Takeaways
- Dimensionality reduction compresses high-dimensional feature spaces into fewer informative axes to enable 2D/3D visualization, accelerate models, and eliminate multicollinearity.
- In PCA, variance equals information: a feature axis with zero variance provides zero distinguishing power, whereas directions of widest spread preserve maximum data geometry.
- Because PCA is variance-greedy, features must be standardized (StandardScaler) beforehand; otherwise, columns measured in large arbitrary units will artificially dominate PC1.
- Geometrically, PCA rotates the coordinate axes: PC1 aligns with the direction of maximal variance, and PC2 is strictly orthogonal (at 90 degrees) to PC1 capturing the next greatest spread.
- Eigenvectors of the covariance matrix define the principal component axis directions; eigenvalues represent the exact amount of variance along each direction.
- The Explained Variance Ratio is the eigenvalue divided by the sum of all eigenvalues; scree plots and cumulative variance curves determine how many components to keep.
- PCA must always be fitted strictly on the training set (e.g. inside a Pipeline) to prevent test data leakage into the principal components.

---

## 1. Why Reduce Dimensions? Variance as Information
### 1.1 The Hook: 13 Numbers or 2?

Consider the classic **Wine benchmark dataset**:
- Chemical analysis of 178 bottles of wine across 3 grape cultivars (classes).
- Each bottle is described by **13 continuous measurements**: `alcohol`, `malic_acid`, `ash`, `alcalinity`, `magnesium`, `phenols`, `flavanoids`, `nonflavanoids`, `proanthocyanins`, `color_intensity`, `hue`, `od280`, and `proline`.
- Human cognition cannot visualize 13-dimensional hyperspace. We can only look at 2D or 3D scatter plots.
- Could we somehow compress these 13 chemical features into **just 2 summary axes**, while preserving enough geometric information to clearly separate the three grape varieties?

**Principal Component Analysis (PCA)**, invented by Karl Pearson in 1901 and independently developed by Harold Hotelling in 1933, is the premier unsupervised technique for **Dimensionality Reduction**:
It projects high-dimensional data onto a smaller number of orthogonal axes that maximize data spread (variance).

```
Dimensionality Reduction Workflow:
   Raw Feature Space (d = 13 dimensions) ──► [ PCA Rotation & Projection ] ──► Compressed Space (k = 2 Principal Components)
   - High storage footprint                  - Finds orthogonal axes of         - Visualizable on a 2D scatter plot!
   - High multicollinearity                    maximum spread (variance)        - Zero correlation between PC1 and PC2!
   - Prone to Curse of Dimensionality                                           - Preserves ~55% of total variance!
```

---

### 1.2 The Four Core Motivations for Dimensionality Reduction

1. **High-Dimensional Data Visualization**:
   Compressing complex feature spaces ($d = 50, 100, 1000$) down to $k = 2$ or $3$ components enables human visual inspection of cluster clusters, class separations, and anomaly outliers.
2. **Computational Speedup & Storage Compression**:
   Training complex non-linear models on 1,000 features is orders of magnitude slower than training on 25 principal components that capture $95\%$ of the information.
3. **Elimination of Multicollinearity**:
   By mathematical construction, all principal components are **strictly orthogonal (mutually perpendicular)**. Their pairwise correlation is identically zero ($\text{Corr}(\text{PC}_i, \text{PC}_j) = 0$). Feeding uncorrelated components into linear models eliminates matrix inversion instabilities!
4. **Noise Filtering**:
   Real-world signals tend to dominate the principal directions of largest variance, while random, high-frequency measurement noise lives in the trailing components with tiny eigenvalues. Truncating trailing components acts as a natural low-pass filter!

---

### 1.3 Variance as the Currency of Information

Why does PCA prioritize variance?
- Consider a feature where every single observation has the exact same value: $x_{i} = 5.0$ for all $i$. Its variance is $\sigma^2 = 0$.
  This feature provides **zero distinguishing power**. It tells you nothing about how samples differ.
- Now consider a feature where values are widely dispersed across positive and negative values. Its high variance reflects diversity, structure, and distinguishing patterns.
- In PCA, **Variance = Information**. The direction along which data points are most spread out preserves the maximum amount of original geometric distance!

---

### 1.4 The Catastrophic "Forgot-to-Scale" Trap: The Proline Pathology

Because PCA actively seeks directions of maximum numerical variance, it is **exceptionally vulnerable to arbitrary physical units of measurement**:

Let us examine the raw variances of features in the unstandardized Wine dataset:
- `proline` is measured in milligrams per liter ($278$ to $1{,}680\text{ mg/L}$), giving an immense sample variance of:
  $$\text{Var}(\text{proline}) \approx \mathbf{99,166.7}$$
- `flavanoids` is measured in grams per liter ($0.34$ to $5.08 \text{ g/L}$), giving a tiny sample variance of:
  $$\text{Var}(\text{flavanoids}) \approx \mathbf{0.99}$$
- `nonflavanoids` has a variance of:
  $$\text{Var}(\text{nonflavanoids}) \approx \mathbf{0.015}$$

#### The Disastrous Illusion of Unscaled PCA:
When PCA is fitted directly on the raw, unscaled Wine dataset:
- **PC1 claims to explain 99.80% of total variance**!
- A naive engineer might celebrate: *"PC1 captures 99.8% of the entire dataset!"*
- But inspect the eigenvector weights (loadings) of PC1:
  $$\mathbf{v}_1 = [0.001, -0.002, 0.000, -0.005, 0.018, 0.001, 0.002, -0.000, 0.002, 0.005, 0.000, 0.001, \mathbf{0.9998}]$$
- PC1 has an loading of **$0.9998$ on Proline** and near-zero on all other 12 features!
- The algorithm did not discover a profound chemical pattern; it was simply blinded by the fact that Proline was recorded in big numbers.

```
Unscaled vs. Standardized PCA on Wine Dataset:
┌─────────────────────┬────────────────────────────────────┬────────────────────────────────────┐
│ Metric              │ Raw Unscaled PCA                   │ Standardized PCA (StandardScaler)  │
├─────────────────────┼────────────────────────────────────┼────────────────────────────────────┤
│ PC1 Variance Share  │ **99.80%** (Fake discovery!)       │ **36.20%** (Real multivariate signal│
│ PC2 Variance Share  │ **0.18%**                          │ **19.20%**                         │
│ Cumulative (PC1+PC2)│ **99.98%**                         │ **55.40%**                         │
│ PC1 Loading Focus   │ 100% Proline; 0% other 12 features │ Balanced chemical contribution     │
│ Cultivar Separation │ Poor (overlaps classes)            │ **Distinct, clear 3-class clusters│
└─────────────────────┴────────────────────────────────────┴────────────────────────────────────┘
```

> **The Non-Negotiable Rule of PCA**:
> **Always standardize features (`StandardScaler`: $\mu = 0, \sigma = 1$) before running PCA**, unless all features are already measured in the exact same physical units (such as raw image pixel intensities $\in [0, 255]$).

**Citations & References:**
- Pearson, K. (1901). On lines and planes of closest fit to systems of points in space. Philosophical Magazine, 2(11), 559-572.
- Hotelling, H. (1933). Analysis of a complex of statistical variables into principal components. Journal of Educational Psychology, 24(6), 417-441.

---

## 2. Step 0: Standardize First! (The Units Disaster)
### 2.1 The Mathematical Derivation of PCA via Variance Maximization

Let $\mathbf{X} \in \mathbb{R}^{n \times d}$ be a dataset of $n$ observations across $d$ features.
Assume without loss of generality that the data has been **mean-centered** so that the empirical column means are zero:
$$\frac{1}{n}\sum_{i=1}^n \mathbf{x}_i = \mathbf{0}$$

The empirical **Covariance Matrix** $\mathbf{\Sigma} \in \mathbb{R}^{d \times d}$ is given by:
$$\mathbf{\Sigma} = \frac{1}{n - 1} \mathbf{X}^T \mathbf{X}$$

We wish to project each $d$-dimensional observation $\mathbf{x}_i$ onto a 1-dimensional line defined by a unit direction vector $\mathbf{w} \in \mathbb{R}^d$, where:
$$\|\mathbf{w}\|_2^2 = \mathbf{w}^T \mathbf{w} = 1$$

The scalar projection (coordinate) of observation $\mathbf{x}_i$ along direction $\mathbf{w}$ is:
$$z_i = \mathbf{w}^T \mathbf{x}_i$$

#### Calculating the Variance of the Projections:
Because the data is mean-centered, the mean of the projected coordinates is also zero:
$$\bar{z} = \frac{1}{n}\sum_{i=1}^n \mathbf{w}^T \mathbf{x}_i = \mathbf{w}^T \left(\frac{1}{n}\sum_{i=1}^n \mathbf{x}_i\right) = 0$$

The empirical sample variance of the projected coordinates is:
$$\text{Var}(z) = \frac{1}{n - 1} \sum_{i=1}^n (z_i - 0)^2 = \frac{1}{n - 1} \sum_{i=1}^n (\mathbf{w}^T \mathbf{x}_i)^2 = \frac{1}{n - 1} \sum_{i=1}^n \mathbf{w}^T \mathbf{x}_i \mathbf{x}_i^T \mathbf{w}$$
$$\text{Var}(z) = \mathbf{w}^T \left( \frac{1}{n - 1} \mathbf{X}^T \mathbf{X} \right) \mathbf{w} = \mathbf{w}^T \mathbf{\Sigma} \mathbf{w}$$

---

### 2.2 Constrained Optimization via Lagrange Multipliers

To find the direction $\mathbf{w}$ that maximizes projected variance subject to the unit-norm constraint $\mathbf{w}^T \mathbf{w} = 1$, we formulate the **Lagrangian**:

$$\mathcal{L}(\mathbf{w}, \lambda) = \mathbf{w}^T \mathbf{\Sigma} \mathbf{w} - \lambda (\mathbf{w}^T \mathbf{w} - 1)$$

Taking the gradient with respect to $\mathbf{w}$:
$$\nabla_{\mathbf{w}} \mathcal{L} = 2\mathbf{\Sigma} \mathbf{w} - 2\lambda \mathbf{w} = \mathbf{0}$$
$$\mathbf{\Sigma} \mathbf{w} = \lambda \mathbf{w}$$

> **The Mathematical Revelation**:
> The condition $\mathbf{\Sigma} \mathbf{w} = \lambda \mathbf{w}$ is the fundamental **Eigenvalue Equation** of linear algebra!
> - The optimal projection directions $\mathbf{w}$ are the **Eigenvectors** of the covariance matrix $\mathbf{\Sigma}$.
> - The scalar $\lambda$ is the corresponding **Eigenvalue**.

#### What Does the Eigenvalue $\lambda$ Represent?
Multiply both sides of the eigenvalue equation on the left by $\mathbf{w}^T$:
$$\mathbf{w}^T \mathbf{\Sigma} \mathbf{w} = \mathbf{w}^T (\lambda \mathbf{w}) = \lambda (\mathbf{w}^T \mathbf{w}) = \lambda (1) = \lambda$$

Since $\text{Var}(z) = \mathbf{w}^T \mathbf{\Sigma} \mathbf{w}$, we obtain:
$$\text{Var}(z) = \lambda$$

> **Profound Geometric Insight**:
> - Each eigenvalue $\lambda_j$ is **literally the exact variance** of the data along principal component axis $\mathbf{v}_j$!
> - To maximize variance, we simply pick the eigenvector $\mathbf{v}_1$ corresponding to the **largest eigenvalue** $\lambda_1$. This is **PC1**!
> - The second principal component **PC2** is the eigenvector $\mathbf{v}_2$ corresponding to the second largest eigenvalue $\lambda_2$, and is mathematically guaranteed to be orthogonal to PC1 ($\mathbf{v}_1^T \mathbf{v}_2 = 0$).

---

### 2.3 Concrete Hand-Calculated Walkthrough: 2D Correlated System ($r = 0.8$)

Let us solve the exact 2D system taught on the whiteboard:
Suppose standardized variables $x_1$ and $x_2$ have unit variance ($\text{Var}(x_1) = 1, \text{Var}(x_2) = 1$) and correlation $r = 0.80$.
The covariance matrix is:

$$\mathbf{\Sigma} = \begin{pmatrix} 1.0 & 0.8 \\ 0.8 & 1.0 \end{pmatrix}$$

#### Step 1: Solve the Characteristic Equation $\det(\mathbf{\Sigma} - \lambda \mathbf{I}) = 0$
$$\det \begin{pmatrix} 1 - \lambda & 0.8 \\ 0.8 & 1 - \lambda \end{pmatrix} = (1 - \lambda)(1 - \lambda) - (0.8)(0.8) = 0$$
$$(1 - \lambda)^2 - 0.64 = 0$$
$$(1 - \lambda)^2 = 0.64 \implies 1 - \lambda = \pm 0.80$$

Solving for the two roots:
$$\lambda_1 = 1 + 0.80 = \mathbf{1.80}$$
$$\lambda_2 = 1 - 0.80 = \mathbf{0.20}$$

#### Total Variance Check:
$$\text{Total Variance} = \text{Tr}(\mathbf{\Sigma}) = 1.0 + 1.0 = 2.00$$
$$\lambda_1 + \lambda_2 = 1.80 + 0.20 = \mathbf{2.00} \quad (\text{Preserved perfectly!})$$

#### Explained Variance Ratios:
- **PC1**: $\frac{\lambda_1}{\lambda_1 + \lambda_2} = \frac{1.80}{2.00} = \mathbf{90.0\%}$
- **PC2**: $\frac{\lambda_2}{\lambda_1 + \lambda_2} = \frac{0.20}{2.00} = \mathbf{10.0\%}$
*(A single principal component PC1 captures 90% of all information in this 2D system!)*

---

#### Step 2: Calculate Eigenvector for $\lambda_1 = 1.80$ (PC1 Direction)
Substitute $\lambda_1 = 1.80$ into $(\mathbf{\Sigma} - \lambda_1 \mathbf{I})\mathbf{v}_1 = \mathbf{0}$:
$$\begin{pmatrix} 1.0 - 1.8 & 0.8 \\ 0.8 & 1.0 - 1.8 \end{pmatrix} \begin{pmatrix} v_{11} \\ v_{12} \end{pmatrix} = \begin{pmatrix} -0.8 & 0.8 \\ 0.8 & -0.8 \end{pmatrix} \begin{pmatrix} v_{11} \\ v_{12} \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}$$

$$-0.8 v_{11} + 0.8 v_{12} = 0 \implies v_{11} = v_{12}$$

Normalize to unit length ($v_{11}^2 + v_{12}^2 = 1 \implies 2v_{11}^2 = 1 \implies v_{11} = \frac{1}{\sqrt{2}}$):
$$\mathbf{v}_1 = \begin{pmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \end{pmatrix} \approx \begin{pmatrix} \mathbf{0.7071} \\ \mathbf{0.7071} \end{pmatrix}$$
*(This points precisely along the $45^\circ$ diagonal line $x_2 = x_1$, the direction of maximal spread!)*

---

#### Step 3: Calculate Eigenvector for $\lambda_2 = 0.20$ (PC2 Direction)
Substitute $\lambda_2 = 0.20$ into $(\mathbf{\Sigma} - \lambda_2 \mathbf{I})\mathbf{v}_2 = \mathbf{0}$:
$$\begin{pmatrix} 1.0 - 0.2 & 0.8 \\ 0.8 & 1.0 - 0.2 \end{pmatrix} \begin{pmatrix} v_{21} \\ v_{22} \end{pmatrix} = \begin{pmatrix} 0.8 & 0.8 \\ 0.8 & 0.8 \end{pmatrix} \begin{pmatrix} v_{21} \\ v_{22} \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}$$

$$0.8 v_{21} + 0.8 v_{22} = 0 \implies v_{21} = -v_{22}$$

Normalized unit vector:
$$\mathbf{v}_2 = \begin{pmatrix} -1/\sqrt{2} \\ 1/\sqrt{2} \end{pmatrix} \approx \begin{pmatrix} \mathbf{-0.7071} \\ \mathbf{0.7071} \end{pmatrix}$$
*(This points along the $135^\circ$ line, strictly orthogonal to PC1: $\mathbf{v}_1^T \mathbf{v}_2 = (0.7071)(-0.7071) + (0.7071)(0.7071) = 0$!)*

```
Geometric Visualization of Principal Axes:
       x2 ^
          │           PC1 Direction (λ1 = 1.80, 90% Variance, 45°)
          │             /
          │           .'
          │         .'  *
          │       .' * *
          │     .' * * *
    ──────┼───.'──────────────► x1
          │ .' * *
          │' *
       PC2 Direction (λ2 = 0.20, 10% Variance, 135° Orthogonal)
```

---

### 2.4 The Duality Theorem: Variance Maximization is Equivalent to Reconstruction Error Minimization

There are two completely distinct ways to derive PCA, and remarkably, both lead to the exact same mathematical solution:

#### Formulation 1: Maximum Variance Perspective (Hotelling 1933)
Find an orthogonal coordinate system that maximizes the variance of projected coordinates:
$$\max_{\mathbf{W}} \text{Tr}(\mathbf{W}^T \mathbf{\Sigma} \mathbf{W}) \quad \text{s.t. } \mathbf{W}^T \mathbf{W} = \mathbf{I}_k$$

#### Formulation 2: Minimum Reconstruction Error Perspective (Pearson 1901)
Approximate each $d$-dimensional observation $\mathbf{x}_i$ using a $k$-dimensional linear subspace ($k < d$):
$$\hat{\mathbf{x}}_i = \sum_{j=1}^k z_{ij} \mathbf{v}_j = \mathbf{V}_k \mathbf{z}_i$$
Find the orthogonal basis $\mathbf{V}_k$ that minimizes the **Mean Squared Reconstruction Error**:
$$\text{MSRE} = \frac{1}{n} \sum_{i=1}^n \|\mathbf{x}_i - \hat{\mathbf{x}}_i\|_2^2$$

#### The Fundamental Spectral Duality Proof:
By the Pythagorean theorem in Euclidean space, the squared length of vector $\mathbf{x}_i$ decomposes into preserved and discarded components:
$$\|\mathbf{x}_i\|^2 = \|\hat{\mathbf{x}}_i\|^2 + \|\mathbf{x}_i - \hat{\mathbf{x}}_i\|^2$$
Averaging over all $n$ observations:
$$\frac{1}{n}\sum_{i=1}^n \|\mathbf{x}_i\|^2 = \frac{1}{n}\sum_{i=1}^n \|\hat{\mathbf{x}}_i\|^2 + \frac{1}{n}\sum_{i=1}^n \|\mathbf{x}_i - \hat{\mathbf{x}}_i\|^2$$
$$\text{Total Variance} = \text{Preserved Projected Variance} + \text{Reconstruction Error}$$

Because Total Variance $\sum_{j=1}^d \lambda_j$ is a fixed constant determined solely by the dataset:
$$\text{Reconstruction Error} = \text{Total Variance} - \text{Preserved Variance} = \sum_{j=1}^d \lambda_j - \sum_{j=1}^k \lambda_j = \mathbf{\sum_{j=k+1}^d \lambda_j}$$

> **The Landmark Equivalence**:
> **Maximizing preserved variance is mathematically identical to minimizing reconstruction error!**
> The reconstruction error of a $k$-component PCA projection is **identically equal to the sum of the discarded eigenvalues**:
> $$\text{MSRE} = \lambda_{k+1} + \lambda_{k+2} + \dots + \lambda_d$$

**Citations & References:**
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). Springer, Chapter 14.5.

---

## 3. Geometric Intuition & Eigenvalues in Plain Language
### 3.1 Choosing the Number of Components $k$: The Scree Plot & Cumulative Variance

When reducing dimensionality from $d = 50$ down to $k$, how do we select the optimal $k$?

```
Scree Plot & Cumulative Explained Variance Curve:
    Individual Variance Ratio (%)            Cumulative Variance (%)
      40% ^ [PC1: 36%]                        100% ^                           .- - - (95% Threshold)
          │                                        │                     . - '
      20% │     [PC2: 19%]                     80% │               . - '
          │          [PC3: 11%]                    │         . - '
      10% │               [PC4: 7%]            60% │   . - ' (PC1+PC2: 55%)
          │    . . . . . . . .                 40% │ .'
        0 ┴───┴────┴────┴────┴────► Component    0 ┴─────────────────────────► Components
             PC1  PC2  PC3  PC4                   k=1   k=2   k=3   k=4   k=13
```

#### The Three Core Decision Heuristics:
1. **Cumulative Variance Threshold (The 90% or 95% Rule)**:
   Retain the smallest number of components $k$ such that their cumulative explained variance ratio reaches a pre-determined engineering threshold:
   $$\sum_{j=1}^{k} \frac{\lambda_j}{\sum_{i=1}^d \lambda_i} \ge 0.90 \quad (\text{or } 0.95)$$
   In Scikit-Learn, this can be automated directly by passing a float to `n_components`: `PCA(n_components=0.95)`.
2. **Cattell's Scree Test (Elbow Heuristic)**:
   Plot the individual eigenvalues $\lambda_j$ against component rank $j$. Look for the "elbow" where the steep drop (the cliff) flattens out into loose scree (the rubble slope at the base of the mountain). Retain all components before the elbow.
3. **The Kaiser-Guttman Criterion**:
   On standardized data (where each original feature had variance $1.0$), only retain principal components whose eigenvalue exceeds the average variance of a single feature:
   $$\lambda_j \ge 1.0$$
   *(Any component with $\lambda < 1.0$ contains less information than a single raw feature!)*

---

### 3.2 Computational Engine: Singular Value Decomposition (SVD)

In modern libraries (including Scikit-Learn), PCA is **almost never computed by explicitly forming the $d \times d$ covariance matrix $\mathbf{\Sigma} = \frac{1}{n-1}\mathbf{X}^T \mathbf{X}$**:
- Forming $\mathbf{X}^T \mathbf{X}$ costs $O(n d^2)$ operations and squares numerical rounding errors.
- If $d = 10{,}000$ features, storing $\mathbf{\Sigma}$ in RAM requires $10{,}000 \times 10{,}000 \times 8 \text{ bytes} \approx 800 \text{ MB}$.

Instead, Scikit-Learn uses **Singular Value Decomposition (SVD)** directly on the mean-centered data matrix $\mathbf{X}$:

$$\mathbf{X} = \mathbf{U} \mathbf{S} \mathbf{V}^T$$

Where:
- $\mathbf{U} \in \mathbb{R}^{n \times n}$ is an orthogonal matrix of left singular vectors.
- $\mathbf{S} \in \mathbb{R}^{n \times d}$ is a diagonal matrix of singular values $s_1 \ge s_2 \ge \dots \ge s_d \ge 0$.
- $\mathbf{V} \in \mathbb{R}^{d \times d}$ is an orthogonal matrix of right singular vectors.

#### The Beautiful Mathematical Equivalence:
$$\mathbf{X}^T \mathbf{X} = (\mathbf{U} \mathbf{S} \mathbf{V}^T)^T (\mathbf{U} \mathbf{S} \mathbf{V}^T) = \mathbf{V} \mathbf{S}^T (\mathbf{U}^T \mathbf{U}) \mathbf{S} \mathbf{V}^T = \mathbf{V} \mathbf{S}^2 \mathbf{V}^T$$
- The right singular vectors $\mathbf{V}$ are **identically the eigenvectors of the covariance matrix**!
- The singular values $s_j$ relate directly to the eigenvalues:
  $$\lambda_j = \frac{s_j^2}{n - 1}$$
- Computing SVD is numerically stable, avoids matrix inversion, and runs in $O(\min(n d^2, n^2 d))$ time.

---

### 3.3 Dimensionality Reduction Taxonomy: PCA vs. LDA vs. t-SNE vs. UMAP

Choosing the right dimensionality reduction technique depends on whether you have labels and whether your data manifold is linear or curved:

```
Dimensionality Reduction Comparison:
┌─────────────────────┬──────────────────┬──────────────────┬──────────────────┬────────────────────────────────────┐
│ Algorithm           │ Learning Paradigm│ Manifold Geometry│ Primary Objective│ Optimal Use Case                   │
├─────────────────────┼──────────────────┼──────────────────┼──────────────────┼────────────────────────────────────┤
│ **PCA**             │ **Unsupervised** │ **Linear**       │ Maximize spread /│ Compression, noise removal, model  │
│                     │ (No labels)      │ (Flat planes)    │ minimize error   │ speedup, multicollinearity fix.    │
├─────────────────────┼──────────────────┼──────────────────┼──────────────────┼────────────────────────────────────┤
│ **LDA (Linear       │ **Supervised**   │ **Linear**       │ Maximize between-│ Supervised classification when     │
│ Discriminant Anal.) │ (Uses labels $y$)│ (Flat planes)    │ to-within spread │ classes overlap along high variance│
├─────────────────────┼──────────────────┼──────────────────┼──────────────────┼────────────────────────────────────┤
│ **t-SNE**           │ **Unsupervised** │ **Non-Linear**   │ Preserves local  │ Pure 2D/3D visualization of dense, │
│                     │                  │ (Manifold curve) │ neighborhoods    │ complex clusters (e.g. single cell)│
├─────────────────────┼──────────────────┼──────────────────┼──────────────────┼────────────────────────────────────┤
│ **UMAP**            │ Unsupervised or  │ **Non-Linear**   │ Preserves local +│ Fast non-linear visualization and  │
│                     │ Semi-Supervised  │ (Riemannian geom)│ global structure │ general-purpose manifold embedding.│
└─────────────────────┴──────────────────┴──────────────────┴──────────────────┴────────────────────────────────────┘
```

#### Why PCA Differs from LDA (The Unsupervised Blind Spot):
- PCA finds axes of maximal overall data spread **without knowing class labels**.
- If two distinct classes are distributed along a narrow corridor, PCA will choose the long direction of the corridor (PC1), merging the two classes together!
- **Linear Discriminant Analysis (LDA)** uses class labels to find directions that maximize between-class variance while minimizing within-class variance (Fisher's criterion), separating the classes cleanly!

**Citations & References:**
- Strang, G. (2016). Introduction to Linear Algebra (5th ed.). Wellesley-Cambridge Press, Chapter 6 & 7.

---

## 4. Selecting k: Scree Plots & Leakage-Free Pipelines
### 4.1 The Data Leakage Hazard: Fitting PCA on Test Data

A widespread and catastrophic mistake made by junior practitioners is running PCA on the entire dataset before splitting into training and testing sets:

```python
# CATASTROPHIC DATA LEAKAGE TRAP - DO NOT DO THIS!
X_scaled = StandardScaler().fit_transform(X)
X_pca = PCA(n_components=5).fit_transform(X_scaled)  # LEAKAGE OCCURS HERE!
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.25)
```

#### Why is this Data Leakage?
- PCA learns the principal directions $\mathbf{V}$ by examining the **covariance structure of all rows**.
- If test samples are included when computing means $\boldsymbol{\mu}$, standard deviations $\boldsymbol{\sigma}$, and eigenvectors $\mathbf{V}$, **information about the test set distribution leaks directly into the training features**!
- The model's validation scores will be artificially optimistic and will degrade when deployed to real production traffic.

---

### 4.2 The Leak-Free Scikit-Learn Pipeline

To guarantee zero data leakage, PCA must be treated as an estimator that is fitted **strictly and exclusively on the training split**:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# 1. Split FIRST
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 2. Encapsulate in a Leak-Free Pipeline
pca_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("pca", PCA(n_components=0.95)),  # Retain 95% of training variance
    ("classifier", LogisticRegression(random_state=42))
])

# 3. Fit strictly on training data
pca_pipeline.fit(X_train, y_train)

# 4. Evaluate on untouched test set
test_score = pca_pipeline.score(X_test, y_test)
print(f"Holdout Test Accuracy (Leak-Free): {test_score * 100:.2f}%")
```

When `pca_pipeline.fit(X_train, y_train)` executes:
- `StandardScaler` computes $\boldsymbol{\mu}_{\text{train}}$ and $\boldsymbol{\sigma}_{\text{train}}$ from `X_train` only.
- `PCA` computes eigenvectors $\mathbf{V}_{\text{train}}$ from `X_train` only.
- When `predict(X_test)` is called, test points are transformed using the frozen training parameters:
  $$\mathbf{z}_{\text{test}} = \left( \frac{\mathbf{x}_{\text{test}} - \boldsymbol{\mu}_{\text{train}}}{\boldsymbol{\sigma}_{\text{train}}} \right) \mathbf{V}_{\text{train}}$$

**Citations & References:**
- Cattell, R. B. (1966). The scree test for the number of factors. Multivariate Behavioral Research, 1(2), 245-276.
- Pedregosa, F. et al. (2011). Scikit-learn: Machine learning in Python. JMLR, 12, 2825-2830.

---

## 5. Applications: Lossy Compression & 2D Image Visualization
### 5.1 Hands-On Python Implementation: 64-Pixel Handwritten Digit Compression

The following production script applies PCA to compress, reconstruct, and visualize the 64-dimensional Scikit-Learn `digits` dataset (8x8 pixel images of numbers 0 through 9):

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 1. Load 8x8 Grayscale Digits Dataset (1,797 images, 64 features)
digits = load_digits()
X, y = digits.data, digits.target
print(f"Original Dataset Shape: {X.shape} (1,797 images with 64 pixel features each)")

# 2. Strict Train / Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 3. Fit Full PCA to Analyze Explained Variance Spectrum
pca_full = PCA(random_state=42)
pca_full.fit(X_train)
cum_var = np.cumsum(pca_full.explained_variance_ratio_)

k_50 = np.argmax(cum_var >= 0.50) + 1
k_90 = np.argmax(cum_var >= 0.90) + 1
k_95 = np.argmax(cum_var >= 0.95) + 1

print("\n=== VARIANCE COMPONENT RETENTION ===")
print(f"Components for 50% variance: {k_50:2d} / 64 components")
print(f"Components for 90% variance: {k_90:2d} / 64 components")
print(f"Components for 95% variance: {k_95:2d} / 64 components")

# 4. Compare Compression & Classification Fidelity Across k
k_candidates = [2, 5, 10, 21, 29, 64]
comparison_records = []

for k in k_candidates:
    pca = PCA(n_components=k, random_state=42)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)

    # Reconstruct images from k components: X_hat = Z * V_k^T + mu
    X_reconstructed = pca.inverse_transform(X_test_pca)
    
    # Compute Mean Squared Reconstruction Error (MSRE)
    msre = np.mean((X_test - X_reconstructed) ** 2)

    # Evaluate Downstream Classifier
    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(X_train_pca, y_train)
    test_acc = accuracy_score(y_test, clf.predict(X_test_pca))
    
    var_preserved = np.sum(pca.explained_variance_ratio_) * 100

    comparison_records.append({
        "Components (k)": k,
        "Variance Preserved": f"{var_preserved:.1f}%",
        "Compression Ratio": f"{64 / k:.1f}x",
        "Reconstruction Error (MSRE)": f"{msre:.3f}",
        "Holdout Test Accuracy": f"{test_acc * 100:.2f}%"
    })

results_df = pd.DataFrame(comparison_records)
print("\n=== PCA COMPRESSION & ACCURACY TRADEOFF TABLE ===")
print(results_df.to_string(index=False))
```

---

### 5.2 Compression Trade-Off Table

| Number of Components ($k$) | Variance Preserved | Storage Compression | Reconstruction MSE | Test Accuracy (LogReg) | Visual Fidelity & Utility |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **$k = 2$** | $28.5\%$ | **$32.0\times$** | $8.420$ | $61.78\%$ | Blurry blobs; suitable only for 2D exploratory scatter plots. |
| **$k = 5$** | $50.3\%$ | **$12.8\times$** | $5.850$ | $85.33\%$ | Coarse digit outlines recognizable; rapid classification. |
| **$k = 10$** | $74.2\%$ | **$6.4\times$** | $3.030$ | $92.89\%$ | Sharp, readable digits; captures primary strokes. |
| **$k = 21$** | $\mathbf{90.1\%}$ | **$3.0\times$** | $1.160$ | $\mathbf{95.78\%}$ | **Optimal Compression Sweet Spot**: Indistinguishable from raw images. |
| **$k = 29$** | $\mathbf{95.0\%}$ | **$2.2\times$** | $0.580$ | $\mathbf{96.22\%}$ | Matches full model accuracy while cutting dimensions in half. |
| **$k = 64$ (Raw)** | $100.0\%$ | $1.0\times$ | $0.000$ | $96.22\%$ | Uncompressed baseline. |

---

### 5.3 Diagnostic Failure Modes & Engineering Pitfalls

| Engineering Failure Mode | Underlying Root Cause | Catastrophic Symptom | Recommended Production Solution |
| :--- | :--- | :--- | :--- |
| **The Non-Linear Manifold Trap** | PCA only searches for straight, orthogonal flat hyperplanes. | Fails completely on non-linear manifolds (e.g. Swiss roll, concentric circles). | Use **Kernel PCA** (RBF kernel), **t-SNE** (for visualization), or **UMAP**. |
| **Outlier Distortion of Covariance** | Covariance calculation sums squared differences $(x_i - \mu)^2$. | A single extreme outlier violently drags PC1 toward itself, tilting the principal axis. | Apply **Robust PCA** (using median absolute deviations) or trim outliers prior to PCA. |
| **Unsupervised Blind Spot** | PCA maximizes variance without knowing target labels $y$. | The direction of maximum variance might be completely orthogonal to the class boundary! | Use **Linear Discriminant Analysis (LDA)** or supervised feature selection (Mutual Information). |
| **Loss of Feature Interpretability** | Principal components are linear combinations of all original features. | Stakeholders cannot understand what $\text{PC1} = 0.42(\text{Income}) - 0.38(\text{Age}) + \dots$ means in business terms. | Use **Sparse PCA** (adds L1 penalty to loadings) or feature importance from Random Forests. |
| **Information Leakage via Global PCA** | Fitting PCA on combined train and test splits before modeling. | Validation accuracy is overly optimistic; model performance collapses in production. | Encapsulate PCA strictly inside a Scikit-Learn `Pipeline`. |

---

### 5.4 Production Code: PCA Biplot & Feature Loading Analysis

To understand what each principal component represents in real-world domain terms, engineers construct a **PCA Biplot**:

```python
# Inspect feature loadings on Wine dataset
from sklearn.datasets import load_wine
wine = load_wine()
X_w, y_w = wine.data, wine.target

scaler = StandardScaler()
X_w_scaled = scaler.fit_transform(X_w)

pca_w = PCA(n_components=2, random_state=42)
X_w_pca = pca_w.fit_transform(X_w_scaled)

# Loadings matrix: eigenvectors scaled by square root of eigenvalues
loadings = pd.DataFrame(
    pca_w.components_.T,
    columns=["PC1_Loading", "PC2_Loading"],
    index=wine.feature_names
)

# Sort by absolute contribution to PC1
loadings["PC1_Magnitude"] = loadings["PC1_Loading"].abs()
sorted_loadings = loadings.sort_values(by="PC1_Magnitude", ascending=False)

print("=== WINE DATASET: TOP FEATURE LOADINGS ON PC1 ===")
print(sorted_loadings[["PC1_Loading", "PC2_Loading"]].head(6).round(3))
```

This reveals that features like `flavanoids` ($+0.423$) and `phenols` ($+0.395$) strongly load onto PC1, while `color_intensity` ($-0.530$) dominates PC2, providing an interpretable chemical basis for cultivar separation!

**Citations & References:**
- Turk, M. A., & Pentland, A. P. (1991). Face recognition using eigenfaces. CVPR, 586-591.

---
