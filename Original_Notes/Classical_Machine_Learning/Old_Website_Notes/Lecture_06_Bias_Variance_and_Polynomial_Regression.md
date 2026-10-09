# Lecture 6: Bias–Variance Tradeoff & Polynomial Regression
## Student Notes — SST Classical Machine Learning

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Formulate **Polynomial Regression** as linear regression with non-linear basis feature expansion, explaining why the hypothesis remains strictly linear in its parameters $\boldsymbol{\theta}$.
- Explain why the number of polynomial interaction terms explodes combinatorially as feature dimensionality and degree increase ($\binom{d+k}{k}$).
- Differentiate between **Raw $R^2$** and **Adjusted $R^2$**, proving why training $R^2$ never decreases as polynomial terms are added.
- Apply **Occam’s Razor** to algorithmic model selection: among hypotheses with comparable generalization risk, select the minimal parameter representation.
- Derive the **Bias–Variance Decomposition** of expected test prediction error into **$\text{Bias}^2 + \text{Variance} + \text{Irreducible Noise } \sigma^2$**.
- Diagnose **High Bias (Underfitting)** versus **High Variance (Overfitting)** using both model complexity curves and **Learning Curves** (Training Size vs. Error).

---

## 1. Polynomial Regression: Fitting Curves with Linear Models

Real-world physical, biological, and economic phenomena are rarely strictly straight lines.
Consider a dataset where the true relationship is non-linear:

$$y = 0.5x^3 - 1.8x^2 + 2.4x + 1.0 + \epsilon$$

Fitting a simple straight line $h_{\boldsymbol{\theta}}(x) = \theta_0 + \theta_1 x$ yields severe systematic error. How can we model curves without abandoning the well-understood, convex mathematics of linear regression?

```
   Degree 1 (Underfitting):            Degree 3 (Balanced Fit):            Degree 25 (Overfitting):
   y                                   y                                   y
   ▲         •                         ▲         •                         ▲    /\   •
   │       •   •                       │       •   •                       │   /  \•/ \•
   │     •       •                     │     •───────•                     │  / •   \  \
   │───/───────────\───► x             │────/─────────\────► x             │─/───────\──\──► x
   │  /             \                  │   /           \                   │/         \  \
   │ /               •                 │  •             •                  │           •  \
   Straight line misses curve!         Captures the true signal            Hugs noise; wild wiggles!
   High Bias, Low Variance             Low Bias, Low Variance              Low Bias, High Variance
```

### The Basis Expansion Trick
Instead of altering the learning algorithm, we **transform the input feature space**. For a single feature $x_1$, we map it into a higher-dimensional polynomial basis vector:

$$\phi(x_1) = \begin{bmatrix} 1 & x_1 & x_1^2 & x_1^3 & \dots & x_1^d \end{bmatrix}^T$$

The hypothesis becomes:

$$h_{\boldsymbol{\theta}}(x) = \theta_0 + \theta_1 x_1 + \theta_2 x_1^2 + \theta_3 x_1^3 + \dots + \theta_d x_1^d$$

> [!IMPORTANT]
> **Why is it Still Called "Linear" Regression?**  
> Linearity in statistics is defined with respect to the **parameters $\boldsymbol{\theta}$**, NOT the inputs $x$.  
> Because the prediction $\hat{y} = \boldsymbol{\theta}^T \phi(\mathbf{x})$ is a linear combination of the weights $\theta_j$, the cost surface $J(\boldsymbol{\theta})$ remains a **strictly convex quadratic bowl**. We can solve it analytically using the Normal Equation or optimize it via Gradient Descent without local minima traps!

### Combinatorial Feature Explosion
When working with multiple features $\mathbf{x} = [x_1, x_2, \dots, x_p]^T$, polynomial expansion of degree $d$ includes all cross-product interaction terms:

$$\text{Total Features } D = \binom{p + d}{d} = \frac{(p + d)!}{p! \, d!}$$

- For $p = 10$ features and degree $d = 2$: $D = \binom{12}{2} = 66$ features.
- For $p = 10$ features and degree $d = 5$: $D = \binom{15}{5} = 3,003$ features!
- For $p = 50$ features and degree $d = 5$: $D = 3,478,761$ features!
This rapid combinatorial explosion demands rigorous regularization or dimensionality control.

---

## 2. Raw $R^2$ vs. Adjusted $R^2$

### The Trap of Raw Training $R^2$
Recall the formula for the sample coefficient of determination:

$$R^2 = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}} = 1 - \frac{\sum_{i=1}^n (y_i - \hat{y}_i)^2}{\sum_{i=1}^n (y_i - \bar{y})^2}$$

> **Mathematical Fact**: As you increase the polynomial degree $d$, **training $R^2$ can NEVER decrease**.  
> Every higher power $x^k$ grants the regression hyperplane an additional degree of freedom to bend and pass closer to existing points in $\mathcal{D}_{\text{train}}$. Even if you feed pure Gaussian white noise features, training $R^2$ will mechanically rise!

### Adjusted $R^2$: Penalizing Model Complexity
To penalize the addition of superfluous features, statisticians define **Adjusted $R^2$**:

$$R_{\text{adj}}^2 = 1 - \left[ \frac{\text{SS}_{\text{res}} / (n - p - 1)}{\text{SS}_{\text{tot}} / (n - 1)} \right] = 1 - (1 - R^2) \frac{n - 1}{n - p - 1}$$

where $n$ is sample size and $p$ is the total number of non-intercept features in the expanded space.

- If adding a feature reduces $\text{SS}_{\text{res}}$ by a smaller margin than the penalty incurred by decreasing degrees of freedom $(n - p - 1)$, **$R_{\text{adj}}^2$ drops**.
- When polynomial width $p \ge n - 1$, degrees of freedom vanish and $R_{\text{adj}}^2$ becomes mathematically undefined.

---

## 3. Occam’s Razor in Machine Learning

Formulated by Franciscan friar William of Ockham in the 14th century:
> *"Entities should not be multiplied beyond necessity."*

In modern computational learning theory:
> **Machine Learning Translation**: If two models of differing complexity achieve statistically indistinguishable generalization performance on validation data, **always select the simpler model** (lower degree, fewer parameters, less compute).

Simpler models offer:
1. **Robustness**: Far less sensitive to distribution shifts and outliers in production.
2. **Interpretability**: Easier for human auditors, regulatory bodies, and domain experts to validate.
3. **Operational Efficiency**: Lower inference latency, reduced memory footprint, and cheaper retraining budgets.

---

## 4. The Bias–Variance Decomposition

Let the true data-generating process be:

$$y = f(\mathbf{x}) + \epsilon, \quad \mathbb{E}[\epsilon] = 0, \quad \text{Var}(\epsilon) = \sigma^2$$

where $f(\mathbf{x})$ is the true target function, and $\epsilon$ is unpreventable aleatoric noise.

Suppose we draw a training set $\mathcal{D}$ from the true distribution, train an estimator $\hat{f}(\mathbf{x}; \mathcal{D})$, and evaluate its prediction at a fixed test point $\mathbf{x}$. Because $\mathcal{D}$ is random, the trained model $\hat{f}$ is itself a **random variable**.

### The Mathematical Proof
We want to calculate the Expected Out-of-Sample Prediction Error at $\mathbf{x}$, taking the expectation over all possible training datasets $\mathcal{D}$ and noise realisations $\epsilon$:

$$\mathbb{E}_{\mathcal{D}, \epsilon}\left[ (y - \hat{f}(\mathbf{x}))^2 \right]$$

Substitute $y = f(\mathbf{x}) + \epsilon$:

$$y - \hat{f}(\mathbf{x}) = (f(\mathbf{x}) + \epsilon) - \hat{f}(\mathbf{x}) = \underbrace{(f(\mathbf{x}) - \hat{f}(\mathbf{x}))}_{\text{Model estimation error}} + \underbrace{\epsilon}_{\text{Random noise}}$$

Squaring this expression:

$$(y - \hat{f}(\mathbf{x}))^2 = (f(\mathbf{x}) - \hat{f}(\mathbf{x}))^2 + 2\epsilon(f(\mathbf{x}) - \hat{f}(\mathbf{x})) + \epsilon^2$$

Taking expectations over $\mathcal{D}$ and $\epsilon$ (noting that $\epsilon$ is independent of $\hat{f}$ and has $\mathbb{E}[\epsilon] = 0$):

$$\mathbb{E}\left[ (y - \hat{f}(\mathbf{x}))^2 \right] = \mathbb{E}\left[ (f(\mathbf{x}) - \hat{f}(\mathbf{x}))^2 \right] + \sigma^2$$

Now expand the first term by adding and subtracting the expected model prediction $\mathbb{E}[\hat{f}(\mathbf{x})]$:

$$f(\mathbf{x}) - \hat{f}(\mathbf{x}) = \left( f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})] \right) + \left( \mathbb{E}[\hat{f}(\mathbf{x})] - \hat{f}(\mathbf{x}) \right)$$

Squaring both sides:

$$(f - \hat{f})^2 = (f - \mathbb{E}[\hat{f}])^2 + (\mathbb{E}[\hat{f}] - \hat{f})^2 + 2(f - \mathbb{E}[\hat{f}])(\mathbb{E}[\hat{f}] - \hat{f})$$

Taking the expectation $\mathbb{E}_{\mathcal{D}}$:
- The cross-term vanishes: $\mathbb{E}\left[ 2(f - \mathbb{E}[\hat{f}])(\mathbb{E}[\hat{f}] - \hat{f}) \right] = 2(f - \mathbb{E}[\hat{f}]) \underbrace{\mathbb{E}[\mathbb{E}[\hat{f}] - \hat{f}]}_{= 0} = 0$.
- The first term is deterministic: $\mathbb{E}[(f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2] = (f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2 = \mathbf{\text{Bias}}[\hat{f}(\mathbf{x})]^2$.
- The second term is variance: $\mathbb{E}[(\hat{f}(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2] = \mathbf{\text{Var}}[\hat{f}(\mathbf{x})]$.

### The Fundamental Decomposition

$$\mathbb{E}\left[ (y - \hat{f}(\mathbf{x}))^2 \right] = \underbrace{\left( f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})] \right)^2}_{\mathbf{\text{Bias}}^2} + \underbrace{\mathbb{E}\left[ (\hat{f}(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2 \right]}_{\mathbf{\text{Variance}}} + \underbrace{\sigma^2}_{\mathbf{\text{Irreducible Noise}}}$$

```
   ┌───────────────────────┬────────────────────────────────────────────────────────┐
   │ Error Component       │ Physical / Intuitive Meaning                           │
   ├───────────────────────┼────────────────────────────────────────────────────────┤
   │ Bias²                 │ Error from incorrect assumptions; how far the average  │
   │                       │ model prediction across all datasets is from truth.    │
   ├───────────────────────┼────────────────────────────────────────────────────────┤
   │ Variance              │ Sensitivity to training dataset fluctuations; how much │
   │                       │ the prediction swings if trained on a different fold.  │
   ├───────────────────────┼────────────────────────────────────────────────────────┤
   │ Irreducible Error σ²  │ Intrinsic aleatoric noise (unmeasured features, sensor │
   │                       │ imprecision); the theoretical lower bound on error.    │
   └───────────────────────┴────────────────────────────────────────────────────────┘
```

---

## 5. The U-Curve of Generalization Error

As model capacity (polynomial degree, tree depth, neural net parameters) increases, the two error components move in opposite directions:

```
   Error
     ▲
     │ \                                         /  Total Generalization Error
     │  \           Generalization Gap          /   (Test MSE)
     │   \          ┌─────────────────┐        /
     │    \         │                 │       /  ◄── Variance Dominates
     │     \────────▼─────────────────▼──────/       (Overfitting)
     │      \                               /
     │       \  Bias²                      /
     │        \                           /   Variance
     │─────────\─────────────────────────/──────────────────────────
     │          \                       /
     │           \                     / ◄── Training Error (R_emp)
     │            \                   /
     │             \                 /
     │              \_______________/
     │               \             /
     └────────────────▼───────────▼─────────────────────► Model Complexity
                     Underfitting        Overfitting
                     (High Bias)         (High Variance)
```

1. **Underfitting Regime (High Bias, Low Variance)**: The hypothesis class is too restricted. Training error is high, and test error is equally high. The model fails to capture underlying patterns.
2. **Overfitting Regime (Low Bias, High Variance)**: The hypothesis class is overly flexible. Training error drops toward zero, but test error diverges wildly. The model fits specific noise quirks of $\mathcal{D}_{\text{train}}$.
3. **The Sweet Spot**: The optimal capacity that balances bias reduction against variance expansion, minimizing expected out-of-sample risk.

---

## 6. Diagnosing with Learning Curves

A **Learning Curve** plots Training Error and Validation Error as a function of the **training set sample size ($n$)**.

```
   HIGH BIAS (Underfitting):                      HIGH VARIANCE (Overfitting):
   Error                                          Error
    ▲                                              ▲
    │                                              │  \ Validation Error (High)
    │  \ Validation Error                          │   \
    │   \                                          │    \_________________________
    │    \════════════════════════ (High plateau)  │
    │    /════════════════════════                 │          Wide Gap!
    │   / Training Error (High)                    │    __________________________
    │  /                                           │   / Training Error (Low)
    └─────────────────────────────► n              └─────────────────────────────► n
    More data DOES NOT help!                       More data WILL help!
    Fix: Increase model capacity.                  Fix: Collect data or regularize.
```

### How to Remediate Each Regime

| Symptom | Diagnosis | Recommended Engineering Fixes |
| :--- | :--- | :--- |
| Train Error High, Val Error High | **High Bias** (Underfitting) | • Increase polynomial degree or model capacity<br>• Add engineered domain features<br>• Reduce regularization penalty ($\lambda \downarrow$) |
| Train Error Low, Val Error High | **High Variance** (Overfitting) | • **Collect more training data** ($n \uparrow$)<br>• Apply L1/L2 Regularization ($\lambda \uparrow$)<br>• Reduce feature dimensionality (PCA, feature selection)<br>• Reduce polynomial degree |

---

## 7. Python Implementation: Polynomial Complexity & Bias-Variance

```python
"""
Polynomial Regression & Complexity Diagnostics
Simulates degree progression and plots the classic Bias-Variance U-Curve.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# 1. Synthesize Non-Linear Ground Truth
np.random.seed(42)
n_points = 120
x = np.sort(np.random.uniform(-3, 3, size=n_points))
# True function: cubic curve + Gaussian noise
y_true = 0.5 * (x ** 3) - 1.2 * (x ** 2) + 0.8 * x + 2.0
noise = np.random.normal(0, 3.5, size=n_points)
y = y_true + noise

# Reshape for scikit-learn
X = x.reshape(-1, 1)

# 2. Train-Test Split (80-20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# 3. Iterate through Degrees 1 to 15
degrees = np.arange(1, 15)
train_errors = []
test_errors = []

for deg in degrees:
    model = Pipeline([
        ("poly", PolynomialFeatures(degree=deg, include_bias=False)),
        ("scaler", StandardScaler()),
        ("linear", LinearRegression())
    ])
    
    model.fit(X_train, y_train)
    
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    train_errors.append(mean_squared_error(y_train, train_pred))
    test_errors.append(mean_squared_error(y_test, test_pred))

# 4. Display Results
results_df = pd.DataFrame({
    "Degree": degrees,
    "Train MSE": np.round(train_errors, 2),
    "Test MSE": np.round(test_errors, 2)
})
print("=" * 40)
print("POLYNOMIAL DEGREE EVALUATION:")
print(results_df.to_string(index=False))
print("=" * 40)

optimal_deg = degrees[np.argmin(test_errors)]
print(f"Optimal Degree Minimizing Test MSE: {optimal_deg}")
```

---

## 8. Common Pitfalls & Interview-Grade Questions

### Q1: An engineer notes: "My model has Train Accuracy = 91% and Test Accuracy = 90.5%. Is my model underfitting or overfitting?"
**Answer**:  
You **cannot determine underfitting vs. overfitting from these two numbers alone without knowing the human baseline or Bayes optimal error**.
- If human experts or theoretical physical limits achieve $99.5\%$ accuracy on this task, then your model is **underfitting (high bias)** because both train and test are significantly below achievable performance.
- If the Bayes optimal error rate is $90\%$ (due to irreducible noise $\sigma^2$), then your model is **virtually perfect**.
- The tiny gap between train ($91\%$) and test ($90.5\%$) only proves that the model has **low variance**; it does not diagnose the bias dimension.

### Q2: Why does adding more training observations ($n \to \infty$) reduce variance but fail to reduce bias?
**Answer**:  
Variance measures how much the fitted function $\hat{f}$ swings when trained on different random samples from the population. As $n \to \infty$, the empirical sample distribution $\hat{\mathcal{P}}_n$ converges uniformly to the true population distribution $\mathcal{P}$ by the Law of Large Numbers. Thus, parameter estimates stabilize to fixed values ($\text{Var}[\hat{f}] \to 0$). However, if the hypothesis class is fundamentally misspecified (e.g., fitting a degree-1 straight line to a parabolic curve), even an infinite dataset will not allow a straight line to bend. The structural discrepancy $\mathbb{E}[\hat{f}] - f$ (Bias) remains invariant to sample size.

### Q3: What is the dartboard analogy of the Bias-Variance tradeoff?
**Answer**:  
Imagine throwing darts at a bullseye ($f(\mathbf{x})$):
1. **Low Bias, Low Variance**: All darts cluster tightly directly in the center of the bullseye (ideal).
2. **Low Bias, High Variance**: Darts are scattered wildly all over the board, but their geometric center of mass is centered on the bullseye.
3. **High Bias, Low Variance**: All darts cluster tightly together in the top-left corner, far from the bullseye.
4. **High Bias, High Variance**: Darts are scattered all over the board, and their average is completely off-target.

---

## 9. Summary & Key Takeaways

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                     SESSION 6 KEY TAKEAWAYS                            │
   ├────────────────────────────────────────────────────────────────────────┤
   │ 1. Basis Expansion: Polynomial regression models non-linear curves     │
   │    while remaining strictly linear in parameters θ.                    │
   │ 2. Adjusted R² Penalty: Raw train R² never falls as degree increases;   │
   │    Adjusted R² incorporates a degrees-of-freedom penalty: (n-1)/(n-p-1)│
   │ 3. Occam's Razor: Between two models with similar test errors, always  │
   │    deploy the simpler, lower-capacity architecture.                    │
   │ 4. Decomposition Formula: Expected Error = Bias² + Variance + σ².      │
   │ 5. High Bias vs High Variance: High Bias fails on train and test;      │
   │    High Variance fits train noise perfectly but explodes on test.      │
   │ 6. Learning Curve Diagnostics: If curves plateau close together with   │
   │    high error, add features; if a wide gap persists, collect data.     │
   └────────────────────────────────────────────────────────────────────────┘
```
