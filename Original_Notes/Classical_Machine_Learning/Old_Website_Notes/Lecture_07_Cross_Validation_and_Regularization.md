# Lecture 7: Regularization & Cross-Validation
## Student Notes — SST Classical Machine Learning

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Explain why over-parameterized models develop wildly exploding coefficients and how regularization constrains model capacity.
- Formulate the **L2 Regularization (Ridge)** objective and derive its closed-form analytical solution: $\mathbf{w}^* = (X^T X + \lambda I)^{-1} X^T \mathbf{y}$, proving that Ridge guarantees invertibility even when $d > n$.
- Formulate the **L1 Regularization (Lasso)** objective, derive its subgradient behavior, and geometrically prove why Lasso induces **parameter sparsity** (exact zero weights) while Ridge merely shrinks weights.
- Formulate **ElasticNet** and explain why it outperforms Lasso when features exhibit strong group multicollinearity.
- Prove why **Feature Scaling is strictly mandatory** prior to regularized regression.
- Differentiate between **Model Parameters** (learned via optimization) and **Hyperparameters** (tuned via validation).
- Implement **$K$-Fold Cross-Validation** without data leakage using `RidgeCV`, `LassoCV`, and Scikit-Learn `Pipeline`.

---

## 1. Motivation: The Exploding Weight Problem

In Lecture 6, we saw that high-degree polynomial models overfit by wiggling violently to pass through every individual training point.

If you inspect the raw numerical values of the fitted weights $\hat{\boldsymbol{\theta}}$ in an overfit model, you discover a striking mathematical symptom:

$$\hat{y} = 1.2 + 84,200 \cdot x - 186,400 \cdot x^2 + 104,100 \cdot x^3 + \dots$$

The coefficients explode into **massive positive and negative numbers that cancel each other out**:
- At training coordinates $x^{(i)}$, the massive numbers cancel out with razor-thin precision.
- However, if you evaluate the model at an unseen test point $x^* = x^{(i)} + 0.001$, the delicate balance collapses, and $\hat{y}$ swings wildly by hundreds of thousands of units!

```
   Overfitting Exploding Weights:              Regularized Stable Weights:
   y                                           y
   ▲    /\                                     ▲
   │   /  \   /\                               │         ╭────────╮
   │  /    \ /  \                              │       ╭─╯        ╰─╮
   │ /      •    \                             │     ╭─╯     •      ╰─╮
   │/             \                            │   ╭─╯                ╰─╮
   └────────────────► x                        └────────────────────────► x
   Coefficients: θ ~ ±100,000                  Coefficients: θ ~ ±1.5
   Extreme sensitivity to tiny input shifts    Smooth, resilient, generalizable
```

> **The Core Idea of Regularization**:  
> If an overfit model requires enormous weights to wiggle through noise, **penalize the magnitude of the weights in the loss function**. We force the optimizer to balance fitting the training data against keeping weights small.

---

## 2. L2 Regularization: Ridge Regression (Tikhonov)

In **Ridge Regression**, we augment the Mean Squared Error loss with an $L_2$ norm penalty on the weight vector:

$$J_{\text{Ridge}}(\mathbf{w}) = \frac{1}{n} \sum_{i=1}^n \left( y^{(i)} - \mathbf{w}^T \mathbf{x}^{(i)} \right)^2 + \lambda \sum_{j=1}^d w_j^2 = \text{MSE} + \lambda \|\mathbf{w}\|_2^2$$

*(Note: We never penalize the bias intercept $w_0$! Penalizing $w_0$ would make model predictions dependent on arbitrary shifts in the origin of the target variable).*

### The Regularization Hyperparameter ($\lambda$ or $\alpha$)
- **$\lambda = 0$**: The penalty vanishes. The objective reduces to unconstrained Ordinary Least Squares (vulnerable to high variance and multicollinearity).
- **$\lambda \to \infty$**: The penalty dominates. All non-intercept weights are crushed to zero: $w_1, w_2, \dots, w_d \to 0$. The model collapses to a horizontal line predicting the mean: $\hat{y} = \bar{y}$ (extreme high bias).
- **$0 < \lambda < \infty$**: The **optimal sweet spot** balancing bias and variance.

```
                  THE REGULARIZATION TRADE-OFF
       λ = 0                   Optimal λ*                 λ → ∞
   ◄───────────────────────────────┼───────────────────────────────►
     Plain OLS                       Sweet Spot                     All w_j → 0
     High Variance                   Low Error                      High Bias
     Overfitting                     Generalizes                    Underfitting
```

### Analytical Solution of Ridge Regression
Expressing the Ridge cost function in matrix notation:

$$J_{\text{Ridge}}(\mathbf{w}) = \frac{1}{n} (X\mathbf{w} - \mathbf{y})^T (X\mathbf{w} - \mathbf{y}) + \lambda \mathbf{w}^T \mathbf{w}$$

Differentiating with respect to $\mathbf{w}$ and setting to zero:

$$\nabla_{\mathbf{w}} J_{\text{Ridge}} = \frac{2}{n} X^T (X\mathbf{w} - \mathbf{y}) + 2\lambda \mathbf{w} = \mathbf{0}$$
$$X^T X \mathbf{w} - X^T \mathbf{y} + n\lambda \mathbf{w} = \mathbf{0}$$
$$\left( X^T X + n\lambda I \right) \mathbf{w} = X^T \mathbf{y}$$
$$\mathbf{w}^*_{\text{Ridge}} = \left( X^T X + n\lambda I \right)^{-1} X^T \mathbf{y}$$

> [!TIP]
> **Why Ridge Regression ALWAYS Inverts!**  
> In standard OLS, if $d > n$ or if features are perfectly collinear, the matrix $X^T X$ is singular ($\det(X^T X) = 0$).  
> However, $X^T X$ is symmetric positive semi-definite (all eigenvalues $\mu_i \ge 0$).  
> Adding $n\lambda I$ shifts every single eigenvalue strictly upward: $\mu_i \to \mu_i + n\lambda > 0$.  
> The matrix $(X^T X + n\lambda I)$ is **strictly positive definite and mathematically guaranteed to be invertible for any $\lambda > 0$**!

---

## 3. L1 Regularization: Lasso (Feature Selection)

In **Lasso (Least Absolute Shrinkage and Selection Operator)**, we replace the squared $L_2$ penalty with the sum of absolute values ($L_1$ norm):

$$J_{\text{Lasso}}(\mathbf{w}) = \frac{1}{n} \sum_{i=1}^n \left( y^{(i)} - \mathbf{w}^T \mathbf{x}^{(i)} \right)^2 + \lambda \sum_{j=1}^d |w_j| = \text{MSE} + \lambda \|\mathbf{w}\|_1$$

### Why Lasso Produces Exact Sparsity ($w_j = 0$)
Why does Lasso drive weights to **exact zero** (performing automatic feature selection), while Ridge only shrinks them to small non-zero numbers?

#### Perspective 1: Subgradient Analysis
Consider the derivative of each penalty term with respect to a single weight $w_j$:
- **Ridge ($L_2$)**: $\frac{\partial}{\partial w_j} (\lambda w_j^2) = 2\lambda w_j$.  
  As $w_j \to 0$, the penalty force shrinks proportionally. It becomes infinitesimal near zero, so the weight asymptotically approaches zero but rarely hits zero.
- **Lasso ($L_1$)**: $\frac{\partial}{\partial w_j} (\lambda |w_j|) = \lambda \cdot \text{sign}(w_j)$ for $w_j \ne 0$.  
  The subgradient at $w_j = 0$ is the set interval $[-\lambda, +\lambda]$. The penalty force is a **constant push** of magnitude $\lambda$ regardless of how tiny $w_j$ is. It drives the parameter directly into zero and traps it there.

#### Perspective 2: Geometric Duality (Constraint Surfaces)
By Lagrange multiplier theory, optimizing an objective with a penalty is equivalent to minimizing MSE subject to a hard budget constraint:

$$\text{Ridge: } \min_{\mathbf{w}} \text{MSE} \quad \text{s.t. } w_1^2 + w_2^2 \le C \quad \text{(Disk)}$$
$$\text{Lasso: } \min_{\mathbf{w}} \text{MSE} \quad \text{s.t. } |w_1| + |w_2| \le C \quad \text{(Diamond / Polytope)}$$

```
   RIDGE (L2): Smooth Circular Boundary        LASSO (L1): Diamond Boundary with Sharp Vertices
              w₂                                           w₂
              ▲     Contours of MSE                        ▲   \  Contours of MSE
              │     ╭────────╮                             │    \  ╭────────╮
              │    │    •     │                            │     \│    •     │
              │   ╭───╮╰─────╯                             │    ◆─╯╰────────╯
              │  │  •  │                                   │   /│\
              │   ╰───╯                                    │  / │ \  Touches sharp vertex
   ───────────┼───────────────► w₁              ───────────┼─◆──┴──◆────────► w₁
              │                                            │  \ │ /  w₂ = 0! (Exact Sparsity)
              │                                            │   \│/
              Tangency occurs at an arbitrary point;       Tangency naturally occurs at sharp
              both w₁ and w₂ remain non-zero.              axis corners, setting weights to 0!
```
Because the $L_1$ ball has sharp vertices lying directly on the coordinate axes ($w_1 = 0$ or $w_2 = 0$), the expanding elliptical contours of the MSE loss function are geometrically most likely to first touch the constraint boundary at a vertex.

---

## 4. ElasticNet: The Best of Both Worlds

While Lasso is excellent for feature selection, it suffers two critical limitations:
1. When $d > n$, Lasso can select at most $n$ features.
2. When features are **heavily correlated** (e.g., gene expression data where 20 genes act as a single pathway), Lasso arbitrarily picks one feature from the group and zeros out the other 19.

**ElasticNet** resolves this by blending both penalties:

$$J_{\text{ElasticNet}}(\mathbf{w}) = \text{MSE} + \alpha \left[ \rho \|\mathbf{w}\|_1 + \frac{1 - \rho}{2} \|\mathbf{w}\|_2^2 \right]$$

where $\alpha$ is total regularization strength, and $\rho \in [0, 1]$ is the `l1_ratio`.
- $\rho = 1 \implies$ Pure Lasso.
- $\rho = 0 \implies$ Pure Ridge.
- $0 < \rho < 1 \implies$ ElasticNet: The $L_1$ component drives sparse feature selection, while the $L_2$ component enforces the **grouping effect** (retaining correlated features together).

---

## 5. Why Feature Scaling is Mandatory for Regularization

Consider two features:
- $x_1$: Annual Salary in Rupees (Range: $300,000$ to $5,000,000$)
- $x_2$: Years of Experience (Range: $1$ to $30$)

Because $x_1$ has huge numerical values, an OLS model assigns it a tiny coefficient: $w_1 \approx 0.00004$.  
Because $x_2$ has small values, it requires a large coefficient: $w_2 \approx 8,500$.

Now look at the Ridge penalty $\lambda (w_1^2 + w_2^2)$:
- Penalty on $w_1$: $\lambda (0.00004)^2 \approx 1.6 \times 10^{-9} \cdot \lambda$ (Virtually zero!)
- Penalty on $w_2$: $\lambda (8500)^2 \approx 72,250,000 \cdot \lambda$ (Brutal destruction!)

The model obliterates Years of Experience while letting Salary escape unregularized simply because of unit scaling!  
> **Mandatory Rule**: Always standardize features ($\mu = 0, \sigma = 1$) before fitting Ridge, Lasso, or ElasticNet.

---

## 6. Parameters vs. Hyperparameters

```
       ┌───────────────────────────────┬───────────────────────────────┐
       │       MODEL PARAMETERS        │     MODEL HYPERPARAMETERS     │
       ├───────────────────────────────┼───────────────────────────────┤
       │ Weights and biases (w, b)     │ Polynomial degree d, penalty  │
       │                               │ strength λ, learning rate α   │
       ├───────────────────────────────┼───────────────────────────────┤
       │ Learned automatically from    │ Set by the machine learning   │
       │ training data via Gradient    │ engineer prior to fitting;    │
       │ Descent or Normal Equation    │ governs algorithm behavior    │
       ├───────────────────────────────┼───────────────────────────────┤
       │ Optimized on: Training Set    │ Optimized on: Validation Set  │
       └───────────────────────────────┴───────────────────────────────┘
```

---

## 7. Model Selection & Cross-Validation: Avoiding the Holdout Trap

### The Holdout Trap: Peeking at the Test Set
A fatal methodology error in ML engineering is tuning $\lambda$ directly on the test set:
```
   ❌ THE HOLDOUT TRAP:
   Train Model on Train Set ──► Evaluate on Test Set ──► Tweak λ ──► Repeat
```
If you iterate on $\lambda$ to maximize test performance, **the test set has leaked into your decision process**. The test set is no longer an unbiased estimate of future generalization!

### The Three-Way Partition

$$\mathcal{D} \longrightarrow \mathcal{D}_{\text{train}} \; (60\%) + \mathcal{D}_{\text{validation}} \; (20\%) + \mathcal{D}_{\text{test}} \; (20\%)$$

1. **Train Set**: Used to learn weights $\mathbf{w}$.
2. **Validation Set**: Used to evaluate multiple $\lambda$ candidates and select $\lambda^*$.
3. **Test Set**: Kept in a cryptographic vault. Evaluated **exactly once** at the very end of the project to report final expected generalization risk.

### $K$-Fold Cross-Validation
When sample size $n$ is small, a single validation split is high-variance. $K$-Fold Cross-Validation partitions data into $K$ equal subsets (folds):

```
   Iteration 1: [ Fold 1 (Val) ] [ Fold 2 (Train) ] [ Fold 3 (Train) ] [ Fold 4 (Train) ] [ Fold 5 (Train) ]
   Iteration 2: [ Fold 1 (Train) ] [ Fold 2 (Val) ] [ Fold 3 (Train) ] [ Fold 4 (Train) ] [ Fold 5 (Train) ]
   Iteration 3: [ Fold 1 (Train) ] [ Fold 2 (Train) ] [ Fold 3 (Val) ] [ Fold 4 (Train) ] [ Fold 5 (Train) ]
   Iteration 4: [ Fold 1 (Train) ] [ Fold 2 (Train) ] [ Fold 3 (Train) ] [ Fold 4 (Val) ] [ Fold 5 (Train) ]
   Iteration 5: [ Fold 1 (Train) ] [ Fold 2 (Train) ] [ Fold 3 (Train) ] [ Fold 4 (Train) ] [ Fold 5 (Val) ]
```
The overall CV performance metric is the average across all $K$ validation folds:

$$\text{CV}_{(K)} = \frac{1}{K} \sum_{k=1}^K \text{Metric}_k$$

---

## 8. Complete Scikit-Learn Implementation: RidgeCV & LassoCV

```python
"""
Regularized Regression with Cross-Validation
Demonstrates RidgeCV, LassoCV, and feature sparsity verification.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV, LassoCV, LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. Load Data
diabetes = load_diabetes(as_frame=True)
X, y = diabetes.data, diabetes.target

# 2. Strict Train-Test Split (Hygiene: 80% Train, 20% Final Holdout Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# 3. Standardize Features (Mandatory!)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# 4. Fit Baseline Unregularized OLS
ols = LinearRegression()
ols.fit(X_train_scaled, y_train)

# 5. Fit RidgeCV (Sweeping alphas across log-space with 5-Fold CV)
alphas = np.logspace(-3, 3, 50)
ridge_cv = RidgeCV(alphas=alphas, cv=5)
ridge_cv.fit(X_train_scaled, y_train)

# 6. Fit LassoCV (Automatic coordinate descent with 5-Fold CV)
lasso_cv = LassoCV(alphas=alphas, cv=5, max_iter=5000, random_state=42)
lasso_cv.fit(X_train_scaled, y_train)

# 7. Evaluate on Final Unseen Test Partition
models = {
    "OLS (Unregularized)": ols,
    f"RidgeCV (α={ridge_cv.alpha_:.4f})": ridge_cv,
    f"LassoCV (α={lasso_cv.alpha_:.4f})": lasso_cv
}

print("=" * 65)
print(f"{'Model':35s} | {'Test RMSE':10s} | {'Test R²':8s} | {'Zero Coefs':10s}")
print("-" * 65)
for name, m in models.items():
    pred = m.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred)
    zero_count = np.sum(np.isclose(m.coef_, 0, atol=1e-3))
    print(f"{name:35s} | {rmse:10.2f} | {r2:8.4f} | {zero_count:10d}/{X.shape[1]}")
print("=" * 65)
```

---

## 9. Common Pitfalls & Interview-Grade Questions

### Q1: Prove why adding an L2 penalty ($\lambda \|\mathbf{w}\|_2^2$) makes the OLS optimization problem strictly convex, even if the original design matrix $X$ has linearly dependent columns ($X^T X$ is singular).
**Answer**:  
The Hessian of unregularized OLS is $H_{\text{OLS}} = \frac{2}{n} X^T X$, which is positive semi-definite ($H \succeq 0$). When columns are collinear, $\det(X^T X) = 0$, meaning at least one eigenvalue $\mu_{\min} = 0$, resulting in a flat trough with infinitely many solutions.  
The Hessian of Ridge Regression is:

$$H_{\text{Ridge}} = \nabla^2 \left( \frac{1}{n} \|X\mathbf{w} - \mathbf{y}\|_2^2 + \lambda \|\mathbf{w}\|_2^2 \right) = \frac{2}{n} X^T X + 2\lambda I$$

For any non-zero vector $\mathbf{v} \ne \mathbf{0}$:

$$\mathbf{v}^T H_{\text{Ridge}} \mathbf{v} = \frac{2}{n} \|X\mathbf{v}\|_2^2 + 2\lambda \|\mathbf{v}\|_2^2 \ge 0 + 2\lambda \|\mathbf{v}\|_2^2 > 0$$

Since $\mathbf{v}^T H_{\text{Ridge}} \mathbf{v} > 0$ for all $\mathbf{v} \ne \mathbf{0}$, the Hessian is **strictly positive definite** for any $\lambda > 0$. The objective function is **strictly convex**, guaranteeing a single, unique global minimum with zero flat troughs.

### Q2: What is the "Grouping Effect" of ElasticNet, and why does Lasso fail to exhibit it?
**Answer**:  
When two features $x_1$ and $x_2$ are highly collinear ($r_{x_1, x_2} \approx 1$), their gradient directions are nearly identical. In Lasso ($L_1$), the constraint boundary is a diamond polytope. The loss contour touches one sharp corner first, setting $w_1 \ne 0$ and driving $w_2 = 0$. Which feature is selected and which is zeroed out is completely arbitrary and unstable under small dataset shifts.  
In ElasticNet, the strictly convex $L_2$ term forces the coefficients of identical features to be equal ($|w_1^* - w_2^*| \le \frac{1}{\lambda_2} \sqrt{2(1 - r)}$). It forces correlated features to enter or leave the model **as a group**, distributing weight evenly across the cluster.

### Q3: An engineer performs 5-fold cross-validation. Inside each fold, they compute training RMSE and validation RMSE. As $\lambda$ increases from $10^{-4}$ to $10^4$, what happens to training RMSE? What happens to validation RMSE?
**Answer**:  
- **Training RMSE**: Will **monotonically increase** (or remain flat). At $\lambda = 10^{-4}$, the model has maximum parametric flexibility to minimize empirical training error. As $\lambda$ increases, the penalty forces weights closer to zero, restricting flexibility and monotonically worsening the fit on $\mathcal{D}_{\text{train}}$.
- **Validation RMSE**: Will follow a **U-shaped curve**. Initially, as $\lambda$ increases, it penalizes overfit noise weights, shrinking variance and causing validation RMSE to decrease toward a minimum. Beyond the optimal $\lambda^*$, excessive regularization induces severe bias, causing validation RMSE to climb steeply as the model underfits.

---

## 10. Summary & Key Takeaways

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                     SESSION 7 KEY TAKEAWAYS                            │
   ├────────────────────────────────────────────────────────────────────────┤
   │ 1. Exploding Weights: Overfitting manifests as gigantic cancelling     │
   │    coefficients; regularization restricts parameter magnitude.        │
   │ 2. Ridge (L2): Adds λ||w||₂². Shrinks weights continuously; guarantees │
   │    matrix invertibility (XᵀX + λI)⁻¹ even when d > n.                  │
   │ 3. Lasso (L1): Adds λ||w||₁. Constant subgradient force drives weights │
   │    to exact zero, performing automatic sparse feature selection.       │
   │ 4. ElasticNet: Combines L1 + L2; preserves group selection on highly   │
   │    correlated covariate clusters.                                      │
   │ 5. Mandatory Scaling: Without standardizing features, features with    │
   │    small numeric ranges are unfairly destroyed by regularization.      │
   │ 6. Three-Way Split & CV: Never tune λ on test data. Use K-Fold CV on   │
   │    training folds; evaluate the final holdout test set exactly once.    │
   └────────────────────────────────────────────────────────────────────────┘
```
