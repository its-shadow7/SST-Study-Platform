# Lecture 8: Logistic Regression, Classification Metrics & Class Imbalance
## Student Notes — SST Classical Machine Learning

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Formulate binary classification and explain why Ordinary Least Squares regression fails when applied to bounded discrete targets $y \in \{0, 1\}$.
- Derive the **Sigmoid (Logistic) Function** $\sigma(z) = \frac{1}{1 + e^{-z}}$ and formulate the relationship between **Probabilities**, **Odds**, and **Log-Odds (Logits)**.
- Prove geometrically that the decision boundary of logistic regression is a flat **hyperplane** in feature space ($\mathbf{w}^T \mathbf{x} + w_0 = 0$) and interpret the logit $z$ as a signed distance metric.
- Derive the **Binary Cross-Entropy (Log-Loss)** cost function via Maximum Likelihood Estimation and prove that its gradient preserves the universal **$\text{Error} \times \text{Feature}$** structure.
- Construct and analyze a **Confusion Matrix**, defining **Precision**, **Recall (Sensitivity)**, **Specificity**, **$F_1$-Score**, and **$F_\beta$-Score**.
- Explain the **Accuracy Paradox** in severe class imbalance and evaluate models using **ROC-AUC** versus **Precision-Recall (PR) Curves**.
- Calibrate the operational **Decision Threshold ($\tau$)** to align with asymmetric business cost matrices.

---

## 1. Why Linear Regression Fails on Classification

Suppose you want to predict whether a customer will churn ($y = 1$) or stay ($y = 0$).

If you fit an ordinary linear regression model $h_{\boldsymbol{\theta}}(\mathbf{x}) = \boldsymbol{\theta}^T \mathbf{x}$:
1. **Unbounded Output Space**: Linear regression outputs real values $\hat{y} \in (-\infty, +\infty)$. Predicting a probability of $\hat{y} = +2.4$ or $\hat{y} = -0.7$ is mathematically nonsensical.
2. **Sensitivity to Outliers**: Adding extreme, legitimate positive examples far to the right pulls the regression line upward and pivots the decision boundary, damaging classification accuracy on points near the threshold.
3. **Heteroscedasticity by Design**: Because $y \in \{0, 1\}$, the error variance $\text{Var}(y \mid \mathbf{x}) = p(\mathbf{x})(1 - p(\mathbf{x}))$ varies with $\mathbf{x}$, violating OLS assumptions.

```
   Linear Regression on Binary Data:           Logistic Regression (Sigmoid S-Curve):
   y                                           P(y=1)
   ▲                                           ▲
   1 ┼   •  •  •  •  •  •                      1 ┼─────────╭─────────•──•──•
     │              /                            │       ╭─╯
     │             /  Threshold = 0.5            │     ╭─╯  Threshold = 0.5
 0.5 ┼────────────/───────────────           0.5 ┼────•─────────────────────
     │           /                               │  ╭─╯
   0 ┼  •  •  • /                              0 ┼──╯•──•──•─────────────────
     └─────────/──────────────────► x            └──────────────────────────► x
     Predictions exceed [0, 1]!                  Strictly bounded: σ(z) ∈ (0, 1)
```

---

## 2. The Sigmoid Function, Odds, and Logits

To guarantee predictions lie strictly within valid probability bounds $\hat{p} \in (0, 1)$, we pass the linear score $z = \mathbf{w}^T \mathbf{x} + w_0$ through the **Standard Logistic (Sigmoid) Function**:

$$\sigma(z) = \frac{1}{1 + e^{-z}} = \frac{e^z}{1 + e^z}$$

### Key Mathematical Properties of Sigmoid
- $\lim_{z \to +\infty} \sigma(z) = 1$
- $\lim_{z \to -\infty} \sigma(z) = 0$
- $\sigma(0) = \frac{1}{1 + 1} = 0.5$
- **Symmetry**: $\sigma(-z) = 1 - \sigma(z)$
- **Clean Derivative**:

  $$\frac{d\sigma(z)}{dz} = \frac{e^{-z}}{(1 + e^{-z})^2} = \left(\frac{1}{1 + e^{-z}}\right) \left(\frac{e^{-z}}{1 + e^{-z}}\right) = \sigma(z)(1 - \sigma(z))$$

### From Probabilities to Odds and Logits
Let $p = P(y = 1 \mid \mathbf{x}) = \sigma(z)$.
1. **The Odds Ratio**: The ratio of the probability of an event occurring to the probability of it not occurring:

   $$\text{Odds} = \frac{p}{1 - p} = \frac{\frac{1}{1 + e^{-z}}}{1 - \frac{1}{1 + e^{-z}}} = \frac{\frac{1}{1 + e^{-z}}}{\frac{e^{-z}}{1 + e^{-z}}} = \frac{1}{e^{-z}} = e^z$$

2. **The Log-Odds (Logit)**: Taking the natural logarithm of the odds:

   $$\text{Logit}(p) = \ln\left( \frac{p}{1 - p} \right) = \ln(e^z) = z = \mathbf{w}^T \mathbf{x} + w_0$$

> [!IMPORTANT]
> **What Logistic Regression Actually Models**:  
> Logistic regression is not linear in probabilities; **it is strictly linear in the log-odds of the positive class**:
> $$\ln\left( \frac{P(y=1 \mid \mathbf{x})}{1 - P(y=1 \mid \mathbf{x})} \right) = w_0 + w_1 x_1 + \dots + w_d x_d$$
> Each weight $w_j$ represents the **change in log-odds per 1-unit increase in $x_j$**, holding other covariates constant. Exponentiating $e^{w_j}$ yields the **multiplicative Odds Ratio (OR)**.

---

## 3. The Geometry of the Decision Boundary

The default operational rule classifies an observation as positive if:

$$\hat{p} = \sigma(z) \ge 0.5 \iff z = \mathbf{w}^T \mathbf{x} + w_0 \ge 0$$

The **Decision Boundary** is the set of all points where the model is maximally uncertain ($\hat{p} = 0.5$):

$$\mathbf{w}^T \mathbf{x} + w_0 = 0$$

```
                         Geometry in 2D Feature Space
              x₂
              ▲
              │          P(y=1) > 0.9           w (Normal vector pointing toward Class 1)
              │       •      •                 ▲
              │    •     •     •              /
              │                         Class 1 (y = 1)
              │───────────────────────/───────────────── Decision Surface: wᵀx + w₀ = 0
              │                      /                  (p̂ = 0.5)
              │       ▲  ▲  ▲       /
              │       ▲    ▲       /            Class 0 (y = 0)
              │          ▲        /
              │      P(y=1) < 0.1
              └────────────────────────────────────────► x₁
```

1. In $d$-dimensional feature space, the decision boundary is a **flat $(d-1)$-dimensional affine hyperplane**.
2. The weight vector $\mathbf{w}$ is the **normal vector** perpendicular to the decision hyperplane, pointing in the direction of increasing positive class probability.
3. The scalar value $z^{(i)} = \mathbf{w}^T \mathbf{x}^{(i)} + w_0$ is proportional to the **signed Euclidean distance** from instance $\mathbf{x}^{(i)}$ to the decision boundary:

   $$\text{Distance} = \frac{\mathbf{w}^T \mathbf{x}^{(i)} + w_0}{\|\mathbf{w}\|_2}$$

---

## 4. The Loss Function: Binary Cross-Entropy (Log-Loss)

Why can't we use Mean Squared Error $J(\mathbf{w}) = \frac{1}{n} \sum (y - \sigma(\mathbf{w}^T \mathbf{x}))^2$?  
Because plugging the non-linear sigmoid $\sigma(z)$ into a squared error function creates a **non-convex optimization landscape** riddled with local minima and flat plateaus where gradients vanish!

### Maximum Likelihood Derivation
For binary labels $y \in \{0, 1\}$, each observation is modeled as a Bernoulli random variable:

$$P(Y = y \mid \mathbf{x}) = p^y (1 - p)^{1 - y} \quad \text{where } p = \sigma(\mathbf{w}^T \mathbf{x})$$

Assuming independent observations, the Likelihood function is:

$$L(\mathbf{w}) = \prod_{i=1}^n \left( \hat{p}^{(i)} \right)^{y^{(i)}} \left( 1 - \hat{p}^{(i)} \right)^{1 - y^{(i)}}$$

Taking the natural logarithm yields the **Log-Likelihood**:

$$\ell(\mathbf{w}) = \sum_{i=1}^n \left[ y^{(i)} \ln \hat{p}^{(i)} + (1 - y^{(i)}) \ln(1 - \hat{p}^{(i)}) \right]$$

To convert maximization into minimization, we multiply by $-\frac{1}{n}$, giving the **Binary Cross-Entropy (Log-Loss)** cost function:

$$J(\mathbf{w}) = -\frac{1}{n} \sum_{i=1}^n \left[ y^{(i)} \ln \hat{p}^{(i)} + (1 - y^{(i)}) \ln(1 - \hat{p}^{(i)}) \right]$$

### Intuition of Log-Loss
- If true label $y = 1$: Loss is $-\ln(\hat{p})$. As $\hat{p} \to 1$, loss $\to 0$. As $\hat{p} \to 0$ (confident and wrong), loss $\to +\infty$.
- If true label $y = 0$: Loss is $-\ln(1 - \hat{p})$. As $\hat{p} \to 0$, loss $\to 0$. As $\hat{p} \to 1$, loss $\to +\infty$.

### Deriving the Gradient
Applying the chain rule:

$$\frac{\partial J(\mathbf{w})}{\partial w_j} = \frac{1}{n} \sum_{i=1}^n \left( \hat{p}^{(i)} - y^{(i)} \right) x_j^{(i)}$$

In vectorized form:

$$\nabla_{\mathbf{w}} J(\mathbf{w}) = \frac{1}{n} X^T (\hat{\mathbf{p}} - \mathbf{y})$$

> **The Universal Convergence**: The gradient of Logistic Regression under Log-Loss has the **identical mathematical form** as Linear Regression under OLS: $\frac{1}{n} X^T (\text{Predictions} - \text{Actuals})$!

---

## 5. The Confusion Matrix and Core Classification Metrics

In classification, raw accuracy is rarely sufficient. We evaluate models using the **Confusion Matrix**:

```
                              PREDICTED CLASS
                         Predicted 0       Predicted 1
                      ┌─────────────────┬─────────────────┐
           Actual 0   │ True Negative   │ False Positive  │
   ACTUAL             │ (TN)            │ (FP) [Type I]   │
   CLASS              ├─────────────────┼─────────────────┤
           Actual 1   │ False Negative  │ True Positive   │
                      │ (FN) [Type II]  │ (TP)            │
                      └─────────────────┴─────────────────┘
```

### Key Performance Formulas

| Metric | Formula | Business Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | $$\frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}}$$ | Overall fraction of correct predictions across all classes. |
| **Precision** | $$\frac{\text{TP}}{\text{TP} + \text{FP}}$$ | Out of all instances the model labeled positive, how many were truly positive? *(Minimizes False Alarms)* |
| **Recall (Sensitivity)** | $$\frac{\text{TP}}{\text{TP} + \text{FN}}$$ | Out of all actual positive instances in reality, how many did the model find? *(Minimizes Misses)* |
| **Specificity** | $$\frac{\text{TN}}{\text{TN} + \text{FP}}$$ | True Negative Rate: ability to correctly identify genuine negatives. |
| **$F_1$-Score** | $$2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2\text{TP}}{2\text{TP} + \text{FP} + \text{FN}}$$ | Harmonic mean of Precision and Recall. Strongly punishes extreme imbalances between the two. |
| **$F_\beta$-Score** | $$(1 + \beta^2) \frac{\text{Precision} \times \text{Recall}}{\beta^2 \text{Precision} + \text{Recall}}$$ | Weights Recall $\beta$ times more heavily than Precision (e.g., $F_2$ for medical diagnostics). |

---

## 6. The Class Imbalance Problem & The Accuracy Trap

Suppose you are building a credit card fraud detection system:
- Total transactions: $100,000$
- Legitimate transactions ($y = 0$): $99,500$ ($99.5\%$)
- Fraudulent transactions ($y = 1$): $500$ ($0.5\%$)

### The Accuracy Trap
A trivial "dumb" model that predicts $\hat{y} = 0$ for every transaction achieves:

$$\text{Accuracy} = \frac{99,500 + 0}{100,000} = \mathbf{99.5\%}$$

On paper, this model appears world-class. In production, it intercepts **zero fraud cases** ($\text{Recall} = 0\%$), resulting in complete corporate insolvency.

> **Mandatory Rule for Imbalanced Data**:  
> Never use Accuracy as your primary optimization metric when class distributions are skewed. Optimize **$F_1$-Score**, **Recall**, or **Precision-Recall AUC**.

---

## 7. ROC Curves vs. Precision-Recall Curves

To evaluate a classifier independent of a single arbitrary threshold $\tau$, we sweep $\tau \in [0, 1]$ and plot curve trajectories.

```
       RECEIVER OPERATING CHARACTERISTIC (ROC)           PRECISION-RECALL (PR) CURVE
       TPR (Recall)                                      Precision
        ▲    ╭───────────────────────                    ▲  ═══════════════╮
        │   ╭╯  ROC-AUC = 0.92                           │                 ╰╮  PR-AUC = 0.84
        │  ╭╯                                            │                  ╰╮
        │ ╭╯   Random Baseline                           │                   ╰╮
        │╭╯    (AUC = 0.50)                              │                    ╰╮ Baseline = % Positives
        │/─────────────────────────                      │                     ╰─────────────────
        └──────────────────────────► FPR                 └──────────────────────────────► Recall
```

### ROC Curve (Receiver Operating Characteristic)
- **$Y$-Axis**: True Positive Rate ($\text{TPR} = \text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$)
- **$X$-Axis**: False Positive Rate ($\text{FPR} = \frac{\text{FP}}{\text{TN} + \text{FP}} = 1 - \text{Specificity}$)
- **ROC-AUC**: The probability that the classifier will rank a randomly chosen positive instance higher than a randomly chosen negative instance.

### When ROC Lies: The Case for Precision-Recall Curves
Notice the denominator of FPR: $\text{TN} + \text{FP}$.  
In fraud detection, $\text{TN} = 99,500$. If false alarms double from $50 \to 100$:

$$\text{FPR} = \frac{100}{99,500 + 100} \approx 0.001$$

The FPR barely flinches! The ROC curve continues to look spectacular ($\text{AUC} > 0.98$) even while false alarms drown human investigators.

In contrast, **Precision** explicitly includes FP in its denominator:

$$\text{Precision} = \frac{50}{50 + 100} = 33\%$$

Precision collapses from $50\% \to 33\%$, immediately exposing system degradation.
> **Production Rule**: In balanced settings, use **ROC-AUC**. In heavily skewed or rare-event settings (fraud, rare pathology, click-through prediction), **always evaluate Precision-Recall (PR) Curves**.

---

## 8. Threshold Tuning: Asymmetric Business Cost Matrices

The default threshold $\tau = 0.5$ assumes False Positives and False Negatives have identical financial costs. In industry, this is almost never true.

### Constructing an Asymmetric Cost Matrix
Suppose in customer churn prediction:
- **Cost of False Positive (FP)**: Offering an unnecessary $\$20$ retention discount to a customer who wasn't leaving $= \$20$.
- **Cost of False Negative (FN)**: Losing a customer who churns, forfeiting lifetime subscription value $= \$500$.

Because $\text{Cost}(FN) = 25 \times \text{Cost}(FP)$, we must prioritize Recall over Precision.  
By lowering the decision threshold to **$\tau = 0.15$**, the model flags any customer with $\ge 15\%$ probability of leaving. While this produces more false alarms ($\$20$), it catches the majority of churners ($\$500$), drastically minimizing total operational financial loss.

---

## 9. Complete Scikit-Learn Implementation: Metrics & Imbalance

```python
"""
Logistic Regression, Confusion Matrix, ROC-AUC, and Threshold Tuning
Demonstrates classification evaluation on an imbalanced dataset.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    confusion_matrix, classification_report,
    roc_auc_score, precision_recall_curve, auc
)

# 1. Generate Synthetic Imbalanced Dataset (95% Class 0, 5% Class 1)
X, y = make_classification(
    n_samples=5000, n_features=10, weights=[0.95, 0.05],
    flip_y=0.01, random_state=42
)

# 2. Split First (Stratified Split preserves class balance in train and test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# 3. Assemble Pipeline
model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(class_weight="balanced", random_state=42))
])

model.fit(X_train, y_train)

# 4. Predict Probabilities
y_prob = model.predict_proba(X_test)[:, 1]

# 5. Evaluate Metrics at Default Threshold (τ = 0.50)
y_pred_default = (y_prob >= 0.50).astype(int)

print("=" * 55)
print("EVALUATION AT DEFAULT THRESHOLD (τ = 0.50):")
print(classification_report(y_test, y_pred_default, target_names=["Stay", "Churn"]))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")

# Compute PR-AUC (Average Precision)
precisions, recalls, thresholds = precision_recall_curve(y_test, y_prob)
pr_auc = auc(recalls, precisions)
print(f"PR-AUC Score:  {pr_auc:.4f}")
print("=" * 55)

# 6. Tune Threshold for High Recall (τ = 0.35)
tuned_threshold = 0.35
y_pred_tuned = (y_prob >= tuned_threshold).astype(int)
cm_tuned = confusion_matrix(y_test, y_pred_tuned)

print(f"\nCONFUSION MATRIX AT TUNED THRESHOLD (τ = {tuned_threshold}):")
print(f"TN: {cm_tuned[0,0]} | FP: {cm_tuned[0,1]}")
print(f"FN: {cm_tuned[1,0]} | TP: {cm_tuned[1,1]}")
print(f"Recovered Churners (Recall): {cm_tuned[1,1] / (cm_tuned[1,0] + cm_tuned[1,1]):.2%}")
```

---

## 10. Common Pitfalls & Interview-Grade Questions

### Q1: In logistic regression, what happens to the estimated parameters $\mathbf{w}$ if the two classes are perfectly linearly separable?
**Answer**:  
If the classes are perfectly separable by a hyperplane $\mathbf{w}^T \mathbf{x} > 0$, the maximum likelihood estimation **fails to converge**; the weights diverge toward infinity ($\|\mathbf{w}\| \to \infty$). As $\|\mathbf{w}\| \to \infty$, the sigmoid output $\sigma(\mathbf{w}^T \mathbf{x})$ sharpens into a discontinuous step function ($p \to 1$ for all positive points and $p \to 0$ for all negative points), driving log-loss to zero. Standard solvers will terminate with convergence warnings. The solution is applying **L2 Regularization (Ridge penalty)**, which imposes an upper bound on weight magnitudes and restores a unique, well-behaved solution.

### Q2: Why is the harmonic mean used in the $F_1$-score instead of the simple arithmetic mean $\frac{\text{Precision} + \text{Recall}}{2}$?
**Answer**:  
The arithmetic mean is vulnerable to compensatory extremes. If a model predicts positive for every single instance, it achieves $\text{Recall} = 1.0$ and $\text{Precision} = 0.01$. The arithmetic mean would report a deceptively high score of $\frac{1.0 + 0.01}{2} = 0.505$.  
The **Harmonic Mean**:

$$F_1 = \frac{2}{\frac{1}{\text{Precision}} + \frac{1}{\text{Recall}}} = \frac{2 \cdot P \cdot R}{P + R}$$

is governed primarily by the smaller of the two terms. If either Precision or Recall collapses toward zero, the harmonic mean plummets to zero ($F_1 = \frac{2(0.01)(1.0)}{1.01} \approx 0.0198$), accurately reflecting catastrophic failure.

### Q3: How do you mathematically interpret a logistic regression coefficient of $w_1 = +0.693$ for a standardized feature $x_1$?
**Answer**:  
The log-odds change by $+0.693$ for every 1-standard-deviation increase in $x_1$, holding all other features fixed. Exponentiating this coefficient yields the **Odds Ratio**:

$$\text{OR} = e^{0.693} \approx 2.0$$

This means that holding all other covariates constant, a 1-standard-deviation increase in $x_1$ **doubles the odds** of the positive outcome occurring ($\text{Odds}_{\text{new}} = 2 \times \text{Odds}_{\text{old}}$).

---

## 11. Summary & Key Takeaways

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                     SESSION 8 KEY TAKEAWAYS                            │
   ├────────────────────────────────────────────────────────────────────────┤
   │ 1. Sigmoid Function: σ(z) = 1/(1 + e⁻ᶻ) squashes linear logit scores   │
   │    z = wᵀx + w₀ into valid class probabilities p̂ ∈ (0, 1).             │
   │ 2. Linear in Log-Odds: Logistic regression is linear in logit space:   │
   │    ln(p / (1 - p)) = wᵀx + w₀. Its decision boundary is a hyperplane.  │
   │ 3. Convex Log-Loss: Maximum likelihood under Bernoulli noise yields    │
   │    Log-Loss; its gradient is the universal Error × Feature shape.      │
   │ 4. The Accuracy Trap: High accuracy on imbalanced data is meaningless. │
   │    Always evaluate Precision, Recall, and F1 on the minority class.    │
   │ 5. ROC vs. PR Curves: ROC-AUC is appropriate for balanced data;        │
   │    Precision-Recall AUC is mandatory when positives are rare.          │
   │ 6. Threshold Tuning: Do not accept τ = 0.5 by default; tune τ on       │
   │    validation data to minimize asymmetric business cost matrices.      │
   └────────────────────────────────────────────────────────────────────────┘
```
