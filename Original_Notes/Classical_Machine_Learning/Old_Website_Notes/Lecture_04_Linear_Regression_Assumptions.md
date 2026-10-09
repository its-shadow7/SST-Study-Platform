# Lecture 4: Linear Regression — Assumptions & Diagnostics
## Student Notes — SST Classical Machine Learning

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Explain why a linear model can achieve a respectable holdout $R^2$ while its statistical inference, $p$-values, and coefficient signs are completely invalid.
- State and mathematically formulate the classical **LINE** assumptions + **No Multicollinearity** governing Ordinary Least Squares.
- State the **Gauss-Markov Theorem** and define what makes the OLS estimator **BLUE** (Best Linear Unbiased Estimator).
- Use the **language of residuals** ($e_i = y_i - \hat{y}_i$) to diagnose violations using **Residuals vs. Fitted**, **Q-Q (Quantile-Quantile)**, and **Lag-Residual** plots.
- Detect and rectify **Heteroscedasticity** (non-constant variance) using variance-stabilizing target transformations ($\log(y)$).
- Calculate the **Variance Inflation Factor (VIF)**, explain the geometry of near-singular matrices, and prescribe engineering solutions for severe multicollinearity.

---

## 1. The Hook: "A Model Can Fit and Still Lie"

In modern applied machine learning, engineers often fall into the **Kaggle Trap**:
> *"My holdout $R^2$ is 0.82 and RMSE is low, so my linear model is ready for decision-making."*

This is dangerous. There is a fundamental divergence between **Pure Prediction** and **Statistical Inference**:

```
                       PREDICTION VS. INFERENCE
       ┌───────────────────────────────┬───────────────────────────────┐
       │        PURE PREDICTION        │     STATISTICAL INFERENCE     │
       ├───────────────────────────────┼───────────────────────────────┤
       │ Goal: Minimize |y - ŷ| on     │ Goal: Estimate the true       │
       │ unseen instances.             │ parameters θ* and test        │
       │                               │ hypotheses (p-values, CIs).   │
       ├───────────────────────────────┼───────────────────────────────┤
       │ Tolerant of: Heteroscedastic  │ Catastrophically broken by:   │
       │ noise, non-normal residuals,  │ Correlated errors, omitted    │
       │ high multicollinearity.       │ variables, heteroscedasticity.│
       └───────────────────────────────┴───────────────────────────────┘
```

If an executive uses your model to make a multi-million-dollar policy intervention—such as cutting advertising spend because its coefficient $\theta_{\text{ads}} = -0.04$ appeared negative due to extreme collinearity with social media spend—the business suffers catastrophic damage.

---

## 2. The Classical Checklist: The LINE Framework

The true data-generating process is assumed to be:

$$y^{(i)} = \theta_0 + \theta_1 x_1^{(i)} + \dots + \theta_d x_d^{(i)} + \epsilon^{(i)}$$

The assumptions of linear regression do not govern the marginal distribution of features $X$; **they govern the behavior of the unobserved statistical error terms $\epsilon$**.

```
                   THE CLASSICAL "LINE" ASSUMPTIONS
       ┌───┬───────────────────┬──────────────────────────────────────────┐
       │ L │ Linearity         │ E[ε | X] = 0 (Linear conditional mean)   │
       ├───┼───────────────────┼──────────────────────────────────────────┤
       │ I │ Independence      │ Cov(εᵢ, εⱼ) = 0 for i ≠ j                │
       ├───┼───────────────────┼──────────────────────────────────────────┤
       │ N │ Normality         │ ε | X ~ 𝒩(0, σ²)                        │
       ├───┼───────────────────┼──────────────────────────────────────────┤
       │ E │ Equal Variance    │ Var(εᵢ | X) = σ² (Homoscedasticity)      │
       └───┴───────────────────┴──────────────────────────────────────────┘
                         + No Perfect Multicollinearity
                           rank(X) = d + 1 (Full Column Rank)
```

### The Gauss-Markov Theorem: Why OLS is "BLUE"
Under the first four structural assumptions (Linearity, Strict Exogeneity $\mathbb{E}[\epsilon \mid X] = 0$, Homoscedasticity, and Uncorrelated Errors):
> **Gauss-Markov Theorem**:  
> The Ordinary Least Squares estimator $\hat{\boldsymbol{\theta}} = (X^T X)^{-1} X^T \mathbf{y}$ is the **BLUE** (**B**est **L**inear **U**nbiased **E**stimator).

- **Linear**: $\hat{\boldsymbol{\theta}}$ is a linear combination of the observations $\mathbf{y}$: $\hat{\boldsymbol{\theta}} = C \mathbf{y}$ where $C = (X^T X)^{-1} X^T$.
- **Unbiased**: $\mathbb{E}[\hat{\boldsymbol{\theta}}] = \boldsymbol{\theta}^*$.
- **Best**: It has the **minimum sampling variance** among all possible linear unbiased estimators.

*(Note: The Normality assumption is NOT required for Gauss-Markov! Normality is only required for exact finite-sample hypothesis tests, such as $t$-tests and $F$-tests).*

---

## 3. Residuals as the Diagnostic Language

Because the true disturbance $\epsilon^{(i)}$ is an unobservable population variable, we diagnose our model using the empirical sample **residuals**:

$$e_i = y^{(i)} - \hat{y}^{(i)} = y^{(i)} - \mathbf{x}^{(i)T} \hat{\boldsymbol{\theta}}$$

```
   Healthy Residuals (Random Noise Cloud):      Violations: Non-Linearity vs Heteroscedasticity:
       e                                           e (Curvature / Non-Linear)   e (Fan / Heteroscedastic)
       ▲                                           ▲                            ▲
       │    •   •   •   •                          │         •   •              │               •   •
       │  •   •   •   •   •                        │       •       •            │            •    •
  ────┼─────────────────────► ŷ               ────┼─────•───────────•──► ŷ ───┼───•──•──•───────────► ŷ
       │    •   •   •   •                          │   •               •        │            •    •
       │  •       •   •                            │ •                   •      │               •   •
       ▼                                           ▼                            ▼
```

### The Three Workhorse Diagnostic Plots

1. **Residuals vs. Fitted Values ($\hat{y}$)**:
   - **Detects**: Linearity violations and Heteroscedasticity.
   - **Healthy Pattern**: A shapeless horizontal band centered symmetrically at zero with constant vertical spread across all values of $\hat{y}$.
2. **Normal Q-Q (Quantile-Quantile) Plot**:
   - **Detects**: Residual non-normality, skewness, and heavy fat tails.
   - **Healthy Pattern**: Residual quantiles fall tightly along the $45^\circ$ reference diagonal.
3. **Residuals vs. Individual Regressors ($x_j$)**:
   - **Detects**: Non-linear relationships specific to individual independent features.

---

## 4. Linearity: Symptoms, Diagnosis, and Remedies

### The Violation
The conditional expectation is non-linear: $\mathbb{E}[Y \mid \mathbf{X}] \ne \mathbf{X}\boldsymbol{\theta}$.

### Symptoms in Plots
- A pronounced parabolic curve, U-shape, or S-curve in the Residuals vs. Fitted plot.
- When $x_j$ increases, residuals are systematically positive, then negative, then positive again.

```
   Fitted vs Residuals showing U-Curve:
   e
   ▲
   │   •                               •
   │     •                           •
   │        •                     •
 ──┼───────────•───────•───────•────────► ŷ
   │              •         •
   │                   •
```

### Engineering Remedies
1. **Feature Transformations**: Apply monotonic non-linear mathematical functions to $x_j$ (e.g., $\log(x_j)$, $\sqrt{x_j}$, $x_j^2$).
2. **Polynomial Feature Expansion**: Introduce higher-order polynomial interaction terms ($x_1^2, x_1 x_2$) — *Note: The model remains linear in its parameters $\boldsymbol{\theta}$!*
3. **Splines / Non-Parametric Modeling**: Transition to generalized additive models (GAMs) or tree-based regressors.

---

## 5. Equal Variance: Homoscedasticity vs. Heteroscedasticity

### The Violation
Heteroscedasticity occurs when the variance of the error term depends systematically on the magnitude of the features or fitted values:

$$\text{Var}(\epsilon^{(i)} \mid \mathbf{x}^{(i)}) = \sigma_i^2 \ne \text{constant}$$

### Why It Breaks the Model
- While the OLS point estimates $\hat{\boldsymbol{\theta}}$ remain unbiased, **OLS is no longer BLUE**.
- The standard error formula $\text{SE}(\hat{\boldsymbol{\theta}}) = \sigma^2 (X^T X)^{-1}$ is mathematically invalid.
- Confidence intervals and $p$-values computed by software packages become wildly optimistic, leading to false discoveries ($p < 0.05$ when no true effect exists).

```
   The Classic Megaphone / Fan Pattern:
   e
   ▲                                 •
   │                           •   •
   │                     •   •   •
   │               •   •   •   •   •   •
 ──┼─────────•───•───•───•───•───•───•───► ŷ
   │               •   •   •   •   •   •
   │                     •   •   •
   │                           •   •
   │                                 •
```

### Engineering Remedies: The Log-Target Transformation
In financial data, real estate prices, and transaction volumes, variance naturally scales proportionally with magnitude (e.g., an error on a $\$10\text{M}$ penthouse is naturally larger in dollars than an error on a $\$100\text{k}$ studio).

$$\tilde{y} = \ln(y)$$

Fitting OLS on $\ln(y)$ stabilizes variance because:

$$\text{Var}(\ln(Y)) \approx \frac{\text{Var}(Y)}{(\mathbb{E}[Y])^2} \approx \text{constant}$$

> [!TIP]
> **Interpreting Log-Transformed Slopes**:  
> In the model $\ln(y) = \theta_0 + \theta_1 x_1$, exponentiating yields $y = e^{\theta_0} \cdot e^{\theta_1 x_1}$. For small values of $\theta_1$ ($|\theta_1| < 0.2$), a 1-unit increase in $x_1$ associates with an approximate **$100 \times \theta_1\%$ percentage change** in $y$.

---

## 6. Normality of Residuals & Independence

### Normality

$$\epsilon^{(i)} \sim \mathcal{N}(0, \sigma^2)$$

- **Why it matters**: Required for exact $t$-tests on coefficients and narrow prediction intervals.
- **Why it is less critical in big data**: By the **Central Limit Theorem (CLT)**, as sample size $n \to \infty$, the sampling distribution of the estimator $\hat{\boldsymbol{\theta}}$ asymptotically converges to multivariate Gaussian even if the raw residuals are non-normal.
- **Diagnostic Tool**: Normal Q-Q Plot. If points deviate into an "S" curve, residuals exhibit **heavy tails** (leptokurtic). Extreme outliers exert disproportionate leverage.

### Independence (No Autocorrelation)

$$\text{Cov}(\epsilon_i, \epsilon_j) = 0 \quad \forall \; i \ne j$$

- **When it fails**:
  1. **Time-Series / Longitudinal Data**: Today's error is correlated with yesterday's error ($\epsilon_t = \rho \epsilon_{t-1} + u_t$).
  2. **Spatial Clustering**: Housing prices in the same apartment block share unobserved neighborhood shocks.
- **Diagnostic Metric: Durbin-Watson Statistic ($DW$)**:

  $$DW = \frac{\sum_{i=2}^n (e_i - e_{i-1})^2}{\sum_{i=1}^n e_i^2}$$

  - $DW \approx 2$: No serial correlation (healthy).
  - $DW < 1.5$: Positive serial correlation (successive residuals cluster together; standard errors severely underestimated).
  - $DW > 2.5$: Negative serial correlation.

---

## 7. Multicollinearity and the Variance Inflation Factor (VIF)

Multicollinearity occurs when two or more independent features in the design matrix $X$ are highly linearly correlated.

```
       NO COLLINEARITY (Orthogonal):            SEVERE MULTICOLLINEARITY:
       x₂                                       x₂
       ▲                                        ▲           /  x₂ ≈ 1.8 x₁
       │                                        │          /
       │        •   •   •                       │      •  /•
       │      •   •   •                         │     •  / •
       │        •   •                           │    •  / •
       └────────────────────────► x₁            └──────/────────────────► x₁
       Information is complementary.            Information is redundant!
       θ₁ and θ₂ estimated cleanly.            Surface is an unstable trough;
                                                θ₁ and θ₂ oscillate wildly.
```

### The Mathematical Consequence of Near-Collinearity
Recall the variance of an estimated coefficient $\hat{\theta}_j$:

$$\text{Var}(\hat{\theta}_j) = \frac{\sigma^2}{(n-1) s_{x_j}^2} \times \frac{1}{1 - R_j^2} = \frac{\sigma^2}{(n-1) s_{x_j}^2} \times \text{VIF}_j$$

where $R_j^2$ is the coefficient of determination obtained by regressing feature $x_j$ on **all other remaining independent features**.

### The Variance Inflation Factor (VIF)

$$\text{VIF}_j = \frac{1}{1 - R_j^2}$$

| VIF Range | Degree of Multicollinearity | Practical Action |
| :--- | :--- | :--- |
| **$\text{VIF} = 1$** | Completely Orthogonal | Ideal scenario; zero coefficient inflation |
| **$1 < \text{VIF} < 5$** | Low to Moderate | Safe; minimal variance inflation |
| **$5 \le \text{VIF} < 10$** | High Collinearity | Investigate; standard errors inflated by $\sqrt{5} \approx 2.23\times$ |
| **$\text{VIF} \ge 10$** | Severe Multicollinearity | Critical failure; $R_j^2 > 0.90$; drop feature, merge, or apply Ridge |

### Why Correlation Matrices are Insufficient
A pairwise correlation matrix only reveals **bivariate collinearity** ($r_{x_1, x_2} > 0.9$).  
It fails completely when feature $x_3$ is a linear combination of three other features ($x_3 \approx 0.5 x_1 + 0.8 x_2 - 0.2 x_4$), where all pairwise correlations might be below $0.4$. **VIF is mandatory because it measures multivariate linear dependence across all dimensions simultaneously.**

---

## 8. Complete Diagnostic Implementation in Python

```python
"""
Comprehensive OLS Assumption Diagnostics
Generates Residuals vs Fitted, Normal Q-Q, and calculates Variance Inflation Factors (VIF).
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.datasets import fetch_california_housing
import matplotlib.pyplot as plt

# 1. Prepare Data
housing = fetch_california_housing(as_frame=True)
df = housing.frame.copy()

# Add constant for OLS intercept
X = sm.add_constant(df.drop(columns=["MedHouseVal"]))
y = df["MedHouseVal"]

# 2. Fit Statsmodels OLS
ols_model = sm.OLS(y, X).fit()
residuals = ols_model.resid
fitted_values = ols_model.fittedvalues

print(ols_model.summary())

# 3. Calculate Variance Inflation Factor (VIF)
vif_data = pd.DataFrame()
vif_data["Feature"] = X.columns
vif_data["VIF"] = [
    variance_inflation_factor(X.values, i) for i in range(X.shape[1])
]
print("\n" + "=" * 40)
print("VARIANCE INFLATION FACTORS (VIF):")
print(vif_data.sort_values(by="VIF", ascending=False).to_string(index=False))
print("=" * 40)

# 4. Diagnostic Visualizations (Code Snippet)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Residuals vs Fitted (Linearity & Homoscedasticity)
axes[0].scatter(fitted_values, residuals, alpha=0.3, edgecolors="none")
axes[0].axhline(0, color="red", linestyle="--", linewidth=1.5)
axes[0].set_title("Residuals vs. Fitted Values")
axes[0].set_xlabel("Fitted Values (ŷ)")
axes[0].set_ylabel("Residuals (e)")

# Plot 2: Normal Q-Q Plot (Normality)
sm.qqplot(residuals, line="45", fit=True, ax=axes[1])
axes[1].set_title("Normal Q-Q Plot")

plt.tight_layout()
# plt.show()
```

---

## 9. Common Pitfalls & Interview-Grade Questions

### Q1: An executive asks: "Our linear regression has a VIF of 18 on `Marketing_Spend` and `Sales_Rep_Count`. Should we immediately scrap the model if our only objective is next-quarter sales forecasting?"
**Answer**:  
**No.** Multicollinearity does not bias predictions, nor does it degrade overall out-of-sample prediction accuracy (RMSE/$R^2$), provided the joint covariance structure between the collinear features remains stable between training and testing. Multicollinearity inflates the *variance of the estimated parameters* $\text{Var}(\hat{\theta}_j)$, meaning you cannot tell whether Marketing or Sales Reps drove the revenue. If the objective is **pure prediction**, the model is acceptable. If the objective is **budget allocation (attribution/causal inference)**, the coefficients cannot be trusted and regularization (Ridge) or feature consolidation must be performed.

### Q2: You plot residuals against fitted values and discover a megaphone (fan) shape. Why does standard OLS underestimate the true uncertainty of high-value predictions?
**Answer**:  
Under heteroscedasticity, the spread of the true error expands as $\hat{y}$ grows. However, standard OLS assumes a single constant global variance $\sigma^2$ across the entire domain. Consequently, OLS computes prediction intervals of identical width everywhere. In the upper range of predictions, the actual variance $\sigma_i^2$ is much larger than the average $\sigma^2$, meaning the reported confidence/prediction intervals are unrealistically narrow. Applying a logarithmic transform $\ln(y)$ compresses the scale and restores constant variance.

### Q3: What is the Durbin-Watson statistic, and what would a value of $DW = 0.42$ indicate about your linear model's residuals?
**Answer**:  
The Durbin-Watson statistic measures first-order serial correlation among residuals in ordered observations. A value of $0.42$ is significantly below the neutral benchmark of $2.0$, indicating severe **positive autocorrelation** ($e_t \approx \rho e_{t-1}$ with $\rho > 0$). When consecutive errors are positively correlated, OLS treats each data point as fully independent when in fact it provides redundant information. This artificially inflates the effective sample size, leading to underestimated standard errors and falsely low $p$-values. The remedy is fitting an autoregressive time-series model (e.g., ARIMA or Newey-West HAC standard errors).

---

## 10. Summary & Key Takeaways

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                     SESSION 4 KEY TAKEAWAYS                            │
   ├────────────────────────────────────────────────────────────────────────┤
   │ 1. Assumptions Live on Errors: LINE applies to disturbance terms ε,    │
   │    not to raw input features X.                                        │
   │ 2. Gauss-Markov & BLUE: OLS is the Best Linear Unbiased Estimator only │
   │    when linearity, strict exogeneity, and homoscedasticity hold.       │
   │ 3. Residuals vs. Fitted: The primary diagnostic plot. Detects curvature│
   │    (non-linearity) and megaphone fans (heteroscedasticity).            │
   │ 4. Log Transform: Taking ln(y) is the primary first-line remedy for    │
   │    heteroscedastic dollar amounts and right-skewed responses.          │
   │ 5. VIF Multi-Dimensionality: Pairwise correlations miss linear combos; │
   │    VIF > 5-10 indicates dangerous variance inflation.                  │
   │ 6. Prediction vs Inference: Collinearity and non-normality barely hurt │
   │    holdout RMSE, but completely destroy coefficient interpretation.    │
   └────────────────────────────────────────────────────────────────────────┘
```
