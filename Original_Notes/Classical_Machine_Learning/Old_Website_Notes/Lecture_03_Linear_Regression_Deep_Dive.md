# Lecture 3: Linear Regression — Deep Dive
## Student Notes — SST Classical Machine Learning

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Formulate the **multivariate linear regression hypothesis** using vector notation and the **intercept trick** ($x_0 = 1$).
- Derive the **Ordinary Least Squares (OLS)** cost function $J(\boldsymbol{\theta})$ from two foundational mathematical perspectives: **Conditional Expectation Minimization** and **Maximum Likelihood Estimation (MLE)** under Gaussian noise.
- Derive the **Normal Equation** $\boldsymbol{\theta}^* = (X^T X)^{-1} X^T \mathbf{y}$ in closed matrix form and explain the geometric interpretation of predictions as an **orthogonal projection** via the Hat Matrix $H$.
- Analyze the computational complexity of the Normal Equation ($\mathcal{O}(n d^2 + d^3)$) and determine when to transition to iterative gradient optimization.
- Calculate and evaluate regression metrics: **MAE**, **MSE**, **RMSE**, and **$R^2$ (Coefficient of Determination)**, including why $R^2$ can be negative on test sets.
- Interpret standardized regression coefficients rigorously as **partial linear associations** holding other covariates fixed, avoiding invalid causal claims.

---

## 1. The Supervised Regression Formulation

In supervised regression, we observe $n$ independent training examples:

$$\mathcal{D} = \{(\mathbf{x}^{(i)}, y^{(i)})\}_{i=1}^n$$

where each input instance $\mathbf{x}^{(i)} \in \mathbb{R}^d$ is a $d$-dimensional feature vector, and $y^{(i)} \in \mathbb{R}$ is a continuous target response.

### The Linear Hypothesis
We model the target as an affine linear combination of the features:

$$h_{\boldsymbol{\theta}}(\mathbf{x}) = \theta_0 + \theta_1 x_1 + \theta_2 x_2 + \dots + \theta_d x_d$$

### The Intercept Trick
To simplify notation, we define a dummy bias feature $x_0 \equiv 1$ for every observation:

$$\mathbf{x} = \begin{bmatrix} x_0 \\ x_1 \\ \vdots \\ x_d \end{bmatrix} \in \mathbb{R}^{d+1}, \quad \boldsymbol{\theta} = \begin{bmatrix} \theta_0 \\ \theta_1 \\ \vdots \\ \theta_d \end{bmatrix} \in \mathbb{R}^{d+1}$$

This allows the entire hypothesis to be expressed compactly as an inner product:

$$h_{\boldsymbol{\theta}}(\mathbf{x}) = \boldsymbol{\theta}^T \mathbf{x} = \mathbf{x}^T \boldsymbol{\theta}$$

```
   Single Data Point Representation:
   ┌────────┐   ┌──────────────────────────────┐
   │ x₀ = 1 │──►│ Dummy intercept multiplier   │
   ├────────┤   ├──────────────────────────────┤
   │ x₁     │──►│ Feature 1 (e.g., Square Feet)│     h_θ(x) = θ₀(1) + θ₁x₁ + ... + θ_d x_d
   ├────────┤   ├──────────────────────────────┤            = θᵀx
   │ ...    │──►│ ...                          │
   ├────────┤   ├──────────────────────────────┤
   │ x_d    │──►│ Feature d (e.g., Bedrooms)   │
   └────────┘   └──────────────────────────────┘
```

---

## 2. The Cost Function: Why Squared Errors?

To identify the optimal parameter vector $\boldsymbol{\theta}$, we define the **Ordinary Least Squares (OLS)** cost function:

$$J(\boldsymbol{\theta}) = \frac{1}{2n} \sum_{i=1}^n \left( h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) - y^{(i)} \right)^2$$

*(Note: The factor of $\frac{1}{2}$ is an algebraic convenience that cancels cleanly when differentiating.)*

Why do we minimize squared errors rather than absolute errors $|h_{\boldsymbol{\theta}}(\mathbf{x}) - y|$ or fourth powers $(h_{\boldsymbol{\theta}}(\mathbf{x}) - y)^4$? There are three rigorous mathematical justifications:

### Justification 1: The Conditional Mean Minimizes Squared Error
From statistical decision theory, if we seek a single scalar predictor $c$ that minimizes expected squared loss $\mathbb{E}[(Y - c)^2]$, calculus proves that the optimal predictor is the **expected value**:

$$\frac{\partial}{\partial c} \mathbb{E}[(Y - c)^2] = -2\mathbb{E}[Y - c] = 0 \implies c^* = \mathbb{E}[Y]$$

When conditioned on feature vector $\mathbf{X}$, minimizing squared error estimates the **conditional expectation**:

$$h^*(\mathbf{x}) = \mathbb{E}[Y \mid \mathbf{X} = \mathbf{x}]$$

### Justification 2: Maximum Likelihood Estimation (MLE) under Gaussian Noise
Assume the true data-generating process is linear with additive, independent and identically distributed (i.i.d.) Gaussian error:

$$y^{(i)} = \boldsymbol{\theta}^T \mathbf{x}^{(i)} + \epsilon^{(i)}, \quad \text{where } \epsilon^{(i)} \sim \mathcal{N}(0, \sigma^2)$$

The probability density of observing target $y^{(i)}$ given input $\mathbf{x}^{(i)}$ is:

$$p(y^{(i)} \mid \mathbf{x}^{(i)}; \boldsymbol{\theta}, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(y^{(i)} - \boldsymbol{\theta}^T \mathbf{x}^{(i)})^2}{2\sigma^2} \right)$$

Under the i.i.d. assumption, the Likelihood $L(\boldsymbol{\theta})$ across all $n$ points is the product of densities:

$$L(\boldsymbol{\theta}) = \prod_{i=1}^n p(y^{(i)} \mid \mathbf{x}^{(i)}; \boldsymbol{\theta}) = \left(\frac{1}{\sqrt{2\pi\sigma^2}}\right)^n \exp\left( -\frac{1}{2\sigma^2} \sum_{i=1}^n (y^{(i)} - \boldsymbol{\theta}^T \mathbf{x}^{(i)})^2 \right)$$

Taking the Natural Logarithm yields the **Log-Likelihood** $\ell(\boldsymbol{\theta})$:

$$\ell(\boldsymbol{\theta}) = \ln L(\boldsymbol{\theta}) = -n \ln(\sqrt{2\pi}\sigma) - \frac{1}{2\sigma^2} \sum_{i=1}^n (y^{(i)} - \boldsymbol{\theta}^T \mathbf{x}^{(i)})^2$$

To maximize $\ell(\boldsymbol{\theta})$ with respect to $\boldsymbol{\theta}$, we drop constant terms and invert the negative sign:

$$\arg\max_{\boldsymbol{\theta}} \ell(\boldsymbol{\theta}) \equiv \arg\min_{\boldsymbol{\theta}} \frac{1}{2} \sum_{i=1}^n (h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) - y^{(i)})^2 \equiv \arg\min_{\boldsymbol{\theta}} J(\boldsymbol{\theta})$$

> **Fundamental Theorem**: Maximizing the log-likelihood of a linear model with i.i.d. Gaussian noise is mathematically equivalent to minimizing the Ordinary Least Squares objective.

### Justification 3: Convexity and Smoothness
The squared error function is everywhere infinitely differentiable ($C^\infty$) and strictly convex. Its Hessian matrix is positive semi-definite, guaranteeing that any stationary point ($\nabla J = \mathbf{0}$) is a **global minimum**.

---

## 3. The Closed-Form Solution: The Normal Equation

### Matrix-Vector Formulation
Let the training dataset be assembled into a **Design Matrix** $X \in \mathbb{R}^{n \times (d+1)}$ and a target vector $\mathbf{y} \in \mathbb{R}^n$:

$$X = \begin{bmatrix} (\mathbf{x}^{(1)})^T \\ (\mathbf{x}^{(2)})^T \\ \vdots \\ (\mathbf{x}^{(n)})^T \end{bmatrix} = \begin{bmatrix} 1 & x_1^{(1)} & \dots & x_d^{(1)} \\ 1 & x_1^{(2)} & \dots & x_d^{(2)} \\ \vdots & \vdots & \ddots & \vdots \\ 1 & x_1^{(n)} & \dots & x_d^{(n)} \end{bmatrix}, \quad \mathbf{y} = \begin{bmatrix} y^{(1)} \\ y^{(2)} \\ \vdots \\ y^{(n)} \end{bmatrix}$$

The vector of model predictions across all $n$ training instances is:

$$\hat{\mathbf{y}} = X \boldsymbol{\theta}$$

The residual error vector is:

$$\mathbf{e} = \hat{\mathbf{y}} - \mathbf{y} = X \boldsymbol{\theta} - \mathbf{y}$$

The sum of squared residuals can be expressed as a matrix quadratic form:

$$J(\boldsymbol{\theta}) = \frac{1}{2} \|\mathbf{e}\|_2^2 = \frac{1}{2} (X \boldsymbol{\theta} - \mathbf{y})^T (X \boldsymbol{\theta} - \mathbf{y})$$

Expanding the quadratic form:

$$J(\boldsymbol{\theta}) = \frac{1}{2} \left( \boldsymbol{\theta}^T X^T X \boldsymbol{\theta} - \boldsymbol{\theta}^T X^T \mathbf{y} - \mathbf{y}^T X \boldsymbol{\theta} + \mathbf{y}^T \mathbf{y} \right)$$

Since $\boldsymbol{\theta}^T X^T \mathbf{y}$ is a scalar, it equals its transpose $\mathbf{y}^T X \boldsymbol{\theta}$:

$$J(\boldsymbol{\theta}) = \frac{1}{2} \boldsymbol{\theta}^T (X^T X) \boldsymbol{\theta} - (X^T \mathbf{y})^T \boldsymbol{\theta} + \frac{1}{2} \mathbf{y}^T \mathbf{y}$$

### Matrix Calculus Derivation
Using standard matrix derivative identities ($\nabla_{\mathbf{u}} (\mathbf{u}^T A \mathbf{u}) = (A + A^T)\mathbf{u}$ and $\nabla_{\mathbf{u}} (\mathbf{b}^T \mathbf{u}) = \mathbf{b}$):

$$\nabla_{\boldsymbol{\theta}} J(\boldsymbol{\theta}) = X^T X \boldsymbol{\theta} - X^T \mathbf{y}$$

Setting the gradient vector identically to zero:

$$X^T X \boldsymbol{\theta} - X^T \mathbf{y} = \mathbf{0} \implies X^T X \boldsymbol{\theta} = X^T \mathbf{y}$$

Assuming the Gram matrix $X^T X$ is invertible (full column rank), multiplying by $(X^T X)^{-1}$ yields the celebrated **Normal Equation**:

$$\boldsymbol{\theta}^* = (X^T X)^{-1} X^T \mathbf{y}$$

---

## 4. Geometric Interpretation: Prediction as an Orthogonal Projection

Why is the equation called the *Normal* Equation?

Notice that the prediction vector $\hat{\mathbf{y}} = X \boldsymbol{\theta}$ is a linear combination of the columns of the design matrix $X$. Therefore, $\hat{\mathbf{y}}$ must reside strictly inside the **column space** of $X$, denoted $\text{col}(X) \subset \mathbb{R}^n$.

```
                     Geometric Projection in ℝⁿ
                               y (True target vector)
                              ▲
                             /│
                            / │
               Residual e  /  │  e = y - ŷ
                 (y - Xθ) /   │  e ⟂ col(X)
                         /    │
                        /     ▼
                       /──────•─────────────────► col(X)
                      0       ŷ = Xθ* (Orthogonal Projection)
```

1. The true target vector $\mathbf{y}$ generally lies outside $\text{col}(X)$ due to random noise and unmodeled non-linearities.
2. The vector in $\text{col}(X)$ closest in Euclidean distance to $\mathbf{y}$ is the **orthogonal projection** of $\mathbf{y}$ onto $\text{col}(X)$.
3. At the point of orthogonal projection, the residual vector $\mathbf{e} = \mathbf{y} - \hat{\mathbf{y}}$ is perpendicular (**normal**) to every column of $X$:

   $$X^T (\mathbf{y} - X\boldsymbol{\theta}) = \mathbf{0} \iff X^T X \boldsymbol{\theta} = X^T \mathbf{y}$$

4. Substituting $\boldsymbol{\theta}^*$ into $\hat{\mathbf{y}} = X \boldsymbol{\theta}^*$:

   $$\hat{\mathbf{y}} = X (X^T X)^{-1} X^T \mathbf{y} = H \mathbf{y}$$

   where $H = X(X^T X)^{-1} X^T \in \mathbb{R}^{n \times n}$ is the famous **Hat Matrix** (it puts the "hat" on $\mathbf{y}$). $H$ is symmetric ($H = H^T$) and idempotent ($H^2 = H$).

---

## 5. Computational Complexity: Normal Equation vs. Gradient Descent

When should you use the analytical Normal Equation, and when should you use iterative Gradient Descent?

| Criterion | Normal Equation ($\boldsymbol{\theta}^* = (X^T X)^{-1} X^T \mathbf{y}$) | Gradient Descent ($\boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \alpha \nabla J$) |
| :--- | :--- | :--- |
| **Computational Complexity** | $\mathcal{O}(n d^2 + d^3)$ (matrix multiplication + inversion) | $\mathcal{O}(k \cdot n d)$ for $k$ iterations |
| **Hyperparameter Tuning** | **Zero** hyperparameters (exact analytical solution) | Requires tuning learning rate $\alpha$, batch size, and epochs |
| **Feature Scaling** | **Not strictly required** for the math to invert | **Crucial**; unscaled features cause severe oscillation |
| **Performance on Huge $d$** | Breaks if $d > 10,000$ (inverting a $10^4 \times 10^4$ matrix is prohibitive) | Scales gracefully to millions of features |
| **Singularity Vulnerability** | Fails if $X^T X$ is non-invertible ($d > n$ or collinear features) | Still converges (though to non-unique solutions) |

---

## 6. Evaluation Metrics for Continuous Targets

Once a linear model is trained, performance must be evaluated on an unseen holdout test set using standardized metrics.

```
       ┌────────┬──────────────────────────────────────────┬─────────────────────────────┐
       │ Metric │ Mathematical Formula                     │ Key Properties              │
       ├────────┼──────────────────────────────────────────┼─────────────────────────────┤
       │  MAE   │ MAE = (1/n) Σ |yᵢ - ŷᵢ|                  │ Robust to outliers; in same │
       │        │                                          │ physical units as target y  │
       ├────────┼──────────────────────────────────────────┼─────────────────────────────┤
       │  MSE   │ MSE = (1/n) Σ (yᵢ - ŷᵢ)²                 │ Differentiable; heavily     │
       │        │                                          │ penalizes large misses      │
       ├────────┼──────────────────────────────────────────┼─────────────────────────────┤
       │  RMSE  │ RMSE = √[ (1/n) Σ (yᵢ - ŷᵢ)² ]           │ Same units as y; standard   │
       │        │                                          │ benchmark metric            │
       ├────────┼──────────────────────────────────────────┼─────────────────────────────┤
       │   R²   │ R² = 1 - [ Σ (yᵢ - ŷᵢ)² / Σ (yᵢ - ȳ)² ]  │ Normalized scale (-∞ to 1]; │
       │        │    = 1 - (SS_res / SS_tot)               │ % variance explained        │
       └────────┴──────────────────────────────────────────┴─────────────────────────────┘
```

### Can $R^2$ be Negative?
Yes! 
- On the training set of an OLS model with an intercept, $R^2 \in [0, 1]$.
- However, on a **held-out test set**, if the model predicts worse than the simple horizontal baseline $\hat{y} = \bar{y}_{\text{train}}$, then $\text{SS}_{\text{res}} > \text{SS}_{\text{tot}}$, driving $R^2 < 0$. A negative $R^2$ is an immediate indicator of catastrophic failure or severe overfitting.

---

## 7. Coefficient Interpretation: Association vs. Causation

Consider a fitted model for house prices (in dollars):

$$\widehat{\text{Price}} = 50,000 + 120 \cdot (\text{SqFt}) - 8,000 \cdot (\text{Bedrooms}) + 45,000 \cdot (\text{MedianIncome})$$

### The "Holding All Else Equal" Principle
- The slope $\theta_1 = +120$ states: *For two houses that have identical numbers of bedrooms and identical median neighborhood incomes, each additional square foot is associated with an estimated $\$120$ increase in price.*
- Why is the coefficient for `Bedrooms` negative ($-8,000$)? Does adding a bedroom reduce property value?
  - **No!** If square footage is held constant, adding another bedroom means **every room must be smaller**. The negative coefficient reflects the penalty for cramped room layouts, not a causal destruction of value.

> [!WARNING]
> **Regression Coefficients are NOT Causal Effects!**  
> $\theta_j$ measures the observational linear association between $x_j$ and $y$ *conditional on all other covariates included in the model*. It does not imply that intervening on $x_j$ will cause $y$ to change by $\theta_j$. Omitted variable bias, reverse causality, and confounders make observational coefficients non-causal.

---

## 8. Complete Scikit-Learn Implementation: California Housing

```python
"""
Multivariate Linear Regression with OLS
California Housing Dataset: Complete Pipeline with Metrics and Diagnostics
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 1. Load Data
housing = fetch_california_housing(as_frame=True)
X = housing.data
y = housing.target  # Median house value in $100,000s

# 2. Train-Test Split (Hygiene: 80-20 Split)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# 3. Assemble Scaled OLS Pipeline
# Note: While OLS predictions are invariant to feature scaling, scaling is essential
# for comparing coefficient magnitudes!
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("ols", LinearRegression(fit_intercept=True))
])

# 4. Fit Model
pipeline.fit(X_train, y_train)

# 5. Evaluate on Holdout Test Set
y_pred_test = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, y_pred_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
r2 = r2_score(y_test, y_pred_test)

print("=" * 45)
print(f"Test MAE:  ${mae * 100000:,.2f}")
print(f"Test RMSE: ${rmse * 100000:,.2f}")
print(f"Test R²:   {r2:.4f}")
print("=" * 45)

# 6. Inspect Standardized Coefficients
coefs = pd.Series(
    pipeline.named_steps["ols"].coef_,
    index=X.columns
).sort_values(ascending=False)

print("\nStandardized Coefficients:")
for feat, val in coefs.items():
    print(f"{feat:15s}: {val:+.4f}")
```

---

## 9. Common Pitfalls & Interview-Grade Questions

### Q1: Prove why the Gram matrix $X^T X$ is singular (non-invertible) when the number of features $d$ exceeds the number of observations $n$ ($d > n$).
**Answer**:  
The design matrix $X \in \mathbb{R}^{n \times (d+1)}$ has rank at most $\min(n, d+1)$. If $n < d+1$, the rank of $X$ is at most $n$. By Sylvester’s rank inequality and properties of matrix multiplication:

$$\text{rank}(X^T X) = \text{rank}(X) \le n < d+1$$

The Gram matrix $X^T X$ is a square matrix of dimension $(d+1) \times (d+1)$ with rank strictly less than its dimension. Hence, $\det(X^T X) = 0$, making $X^T X$ singular and non-invertible. The system has infinitely many solutions that achieve zero training error. To solve this, one must apply **L2 Regularization (Ridge Regression)**: $(X^T X + \lambda I)^{-1}$, which is strictly positive definite and invertible.

### Q2: An engineer adds 10 random noise features (pure Gaussian noise completely uncorrelated with $y$) to a linear regression model. What happens to the training $R^2$? What happens to Adjusted $R^2$?
**Answer**:  
The standard training $R^2 = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}}$ will **monotonically increase** (or at worst remain unchanged). Adding any feature provides the hyperplane extra degrees of freedom to fit incidental noise in the training set, reducing $\text{SS}_{\text{res}}$. Conversely, the **Adjusted $R^2$**:

$$R_{\text{adj}}^2 = 1 - \left[ \frac{\text{SS}_{\text{res}} / (n - d - 1)}{\text{SS}_{\text{tot}} / (n - 1)} \right]$$

penalizes the loss of degrees of freedom ($n - d - 1$). If the noise features do not reduce $\text{SS}_{\text{res}}$ by more than the penalty factor $\frac{n-1}{n-d-1}$, Adjusted $R^2$ will **decrease**, correctly signaling that the additional complexity is harmful.

### Q3: What is the geometric meaning of the Hat Matrix $H = X(X^T X)^{-1} X^T$, and what does the trace $\text{Tr}(H)$ represent?
**Answer**:  
The Hat Matrix $H$ is the orthogonal projection operator from $\mathbb{R}^n$ onto the column space $\text{col}(X)$. It maps the observed target vector $\mathbf{y}$ directly to the fitted prediction vector $\hat{\mathbf{y}} = H\mathbf{y}$.  
Using the cyclic property of the matrix trace $\text{Tr}(AB) = \text{Tr}(BA)$:

$$\text{Tr}(H) = \text{Tr}\left( X(X^T X)^{-1} X^T \right) = \text{Tr}\left( (X^T X)^{-1} (X^T X) \right) = \text{Tr}(I_{d+1}) = d+1$$

The trace of the Hat Matrix equals the **effective degrees of freedom** of the linear model (the number of fitted parameters including the intercept). The diagonal entries $h_{ii}$ represent the **statistical leverage** of the $i$-th observation.

---

## 10. Summary & Key Takeaways

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                     SESSION 3 KEY TAKEAWAYS                            │
   ├────────────────────────────────────────────────────────────────────────┤
   │ 1. Hypothesis Formulation: h_θ(x) = θᵀx incorporates the bias term     │
   │    via the intercept trick x₀ = 1.                                     │
   │ 2. Dual Justifications of OLS: Minimizing squared error simultaneously │
   │    estimates the conditional mean E[Y|X] and achieves MLE under        │
   │    Gaussian i.i.d. observation noise.                                  │
   │ 3. The Normal Equation: θ* = (XᵀX)⁻¹ Xᵀy finds the global minimum      │
   │    in one step by orthogonally projecting y onto the column space of X.│
   │ 4. Complexity Bottleneck: Normal equation requires O(d³); use Gradient │
   │    Descent when feature dimensionality d exceeds ~10,000.              │
   │ 5. Metric Selection: MAE for robust dollar errors; RMSE to heavily     │
   │    penalize extreme misses; R² for variance explained.                 │
   │ 6. Observational vs Causal: Standardized coefficients measure partial  │
   │    associations holding other features constant; they do not prove     │
   │    causal mechanisms.                                                  │
   └────────────────────────────────────────────────────────────────────────┘
```
