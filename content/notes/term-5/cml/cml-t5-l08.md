# 8. Logistic Regression, Classification Metrics & Class Imbalance
**Term:** Term 5 | **Subject:** CML | **Note ID:** `cml-t5-l08`
**Last Updated:** 2026-10-18T00:00:00Z

## Abstract & Summary
An exhaustive, intuitive masterclass on Binary Classification using Logistic Regression. Contrasts lines of best fit with hyperplanes of best separation, demystifies the Sigmoid function, Logit, and Odds, formalizes the convex Binary Cross-Entropy loss surface, and delivers a rigorous breakdown of the Confusion Matrix. Explores threshold tuning dynamics, shows why ROC curves deceive on imbalanced data while Precision-Recall curves tell the truth, and details production remediation for class imbalance.

## Learning Objectives
- Understand why linear regression fails for binary classification and formulate the Sigmoid activation and Log-Odds representation.
- Derive and interpret the Binary Cross-Entropy (Log-Loss) objective function and explain why MSE is mathematically unsuitable.
- Compute and diagnose all primary classification metrics (Accuracy, Precision, Recall, Specificity, F1-Score) from a confusion matrix.
- Analyze operating threshold trade-offs and evaluate models using ROC-AUC and Precision-Recall (PR) curves.
- Diagnose the 'Accuracy Trap' in severely imbalanced datasets and deploy industry solutions (class weighting, threshold tuning, and PR-AUC optimization).

## Key Takeaways
- Linear regression predicts continuous real values that exceed [0, 1] and is sensitive to extreme outliers; Logistic Regression applies the Sigmoid function to map unbounded scores to valid probabilities.
- The decision boundary is the linear hyperplane where w^T x + w_0 = 0, corresponding to probability P(y=1|x) = 0.5. Points deeper into positive space have higher confidence.
- MSE with Sigmoid produces a non-convex loss surface with flat plateaus; Log-Loss (Binary Cross-Entropy) guarantees a strictly convex bowl with a unique global minimum.
- Accuracy is fatally deceptive on imbalanced datasets: a dummy model predicting majority class on 99% non-fraud data achieves 99% accuracy while catching zero fraud.
- Precision measures exactness (low false alarms); Recall measures completeness (low false negatives). The F1-score balances them via the harmonic mean.
- ROC-AUC measures ranking ability across all thresholds but is insensitive to false positives when negatives dominate; Precision-Recall (PR-AUC) is the gold standard for rare positive classes.
- Remediating class imbalance requires class-weighted loss functions (class_weight='balanced'), threshold shifting based on business costs, and leak-free resampling inside CV folds.

---

## 1. Classification Foundations: Why Linear Regression Fails for Binary Outcomes
### 1.1 The Telco Churn Case Study: The Business Imperative of Binary Classification

Consider a major telecom provider (such as Bharti Airtel or AT&T).
Every month, the company tracks millions of active mobile subscribers. A fundamental business challenge is **Customer Churn**:
- $y = 0$: **Retained Customer** (Continues using the service, paying monthly bills).
- $y = 1$: **Churned Customer** (Ported their SIM to a competitor, canceled subscription, or ceased recharges).

```
Customer Churn Timeline:
   Month t-1: Active Subscriber ──► Month t: Evaluates Competitor Offers ──► Month t+1: Decision
                                            │                                        │
                                            ├── Network issues in local area?       ├── Stays (y = 0)
                                            ├── Better data tariff elsewhere?       └── Churns (y = 1)
                                            └── High volume of support calls?
```

#### Why Early Predictive Identification is Worth Millions
Acquiring a new customer in the telecom sector costs between **5 to 25 times more** than retaining an existing customer.
If the company can predict that high-value subscriber $U$ has an $85\%$ probability of churning next month:
1. **Targeted Incentives**: The business can proactively offer a 20 USD bill credit, 50% recharge discount, or bonus 5G data pack.
2. **Infrastructure Root-Cause Resolution**: If multiple customers churning in an IT corridor (e.g., Electronic City) cite call drops, network engineers can deploy localized micro-cell towers before thousands more churn.
3. **Optimized Retention Spend**: Offering discounts to customers who were never going to leave wastes valuable marketing budget. Predicting accurate probabilities ensures retention capital is deployed only where it moves the needle.

---

### 1.2 Why Linear Regression Fails Catastrophically for Classification

A natural first instinct of a student might be: *"We already know Ordinary Least Squares Linear Regression ($\hat{y} = \mathbf{w}^T \mathbf{x} + w_0$). Can we not simply train a line on the binary targets $\{0, 1\}$ and predict Class 1 whenever $\hat{y} \ge 0.5$?"*

The answer is an emphatic **NO**. Linear regression fails for binary classification due to two fatal geometric and statistical flaws:

```
Why Linear Regression Fails for Binary Targets:
       y (Target)
         ^
       1 |           *  *  *  *  *  *  *  * (Class 1)                 * (Extreme Outlier x = 50)
         |                                                           /
         |                                                          /
     0.5 |------------------ Threshold ----------------------------/-----------------
         |                                                        /
         |                                                       / (Fitted Line shifted right!)
       0 |   *  *  *  *  *  * (Class 0)                         /
         +----------------------------------------------------> x
                    Unbounded: y_hat can be -0.4 or +2.8!
```

#### Flaw 1: Nonsensical, Unbounded Output Ranges
Ordinary Least Squares is designed for continuous unbounded target spaces $\mathcal{Y} = (-\infty, +\infty)$.
For extreme values of feature $x$ (e.g., very high monthly usage), linear regression outputs values like $\hat{y} = 2.45$ or $\hat{y} = -0.38$.
In classification, we require outputs to represent **posterior probabilities** $P(Y = 1 \mid \mathbf{x})$.
A probability of $-0.38$ or $+2.45$ violates the fundamental Kolmogorov axioms of probability ($0 \le P(E) \le 1$) and cannot be interpreted as risk or confidence.

#### Flaw 2: The Outlier Sensitivity Disaster (The Tilting Boundary)
In Ordinary Least Squares, the loss function minimizes squared vertical residuals $\sum (y^{(i)} - \hat{y}^{(i)})^2$.
Suppose we have well-separated clusters for Class 0 ($x \in [1, 5]$) and Class 1 ($x \in [7, 12]$). The linear threshold $\hat{y} = 0.5$ falls cleanly at $x = 6.0$.
Now introduce a single extreme outlier: a heavy enterprise customer at $x = 50$ who also belongs to Class 1 ($y = 1$).
- Because OLS squares the error $(1 - (w \cdot 50 + w_0))^2$, this distant point exerts an enormous lever-arm torque on the regression line.
- The fitted line pivots and flattens out to reduce the squared residual on this distant point.
- As the line pivots, the point where it crosses $\hat{y} = 0.5$ **shifts drastically to the right** (e.g., from $x = 6.0$ to $x = 8.5$).
- Consequently, dozens of genuine Class 1 customers between $x = 7.0$ and $x = 8.5$ are now falsely classified as Class 0!
- *Irony*: An observation that was **extremely positive** caused other positive observations to be misclassified as negative!

---

### 1.3 Geometric Foundations: Line of Best Fit vs. Hyperplane of Separation

| Architectural Dimension | Linear Regression | Logistic Regression |
| :--- | :--- | :--- |
| **Fundamental Nature** | Function Approximation / Curve Fitting | Pattern Classification / Space Partitioning |
| **Geometric Objective** | Finds the **line of best fit** that passes through the spatial center of data points. | Finds the **decision hyperplane** that separates points of Class 0 from Class 1. |
| **Target Variable Space** | Continuous scalar $y \in \mathbb{R}$ | Discrete categorical class label $y \in \{0, 1\}$ |
| **Hypothesis Output** | Real-valued numerical estimate $\hat{y} \in (-\infty, +\infty)$ | Calibrated probability estimate $\hat{p} = P(Y=1 \mid \mathbf{x}) \in (0, 1)$ |
| **Loss Function** | Convex Mean Squared Error (MSE) | Convex Binary Cross-Entropy (Log-Loss / NLL) |
| **Response to Outliers** | Highly vulnerable: line pivots to chase distant points. | Exceptionally robust: points far from boundary saturate at $p \approx 0$ or $1$. |

**Citations & References:**
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). Springer, Chapter 4.
- James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). An Introduction to Statistical Learning. Springer, Chapter 4.

---

## 2. The Sigmoid Activation, Odds & The Logit Function
### 2.1 The Two-Step Prediction Pipeline

To resolve the unbounded range problem, Logistic Regression constructs a two-stage hypothesis:
1. First, compute a standard linear combination of the input features (the **Logit / Linear Score** $z$).
2. Second, pass this continuous score $z$ through a non-linear squashing function that maps $(-\infty, +\infty)$ strictly into the open interval $(0, 1)$.

```
The Logistic Regression Feedforward Flow:
   Features x = [x1, x2, ..., xd]^T
            │
            ▼
   ┌────────────────────────────────────────────────────────┐
   │ Step 1: Linear Combination (Dot Product + Bias)        │
   │ z = w^T x + w0 = w0 + w1*x1 + w2*x2 + ... + wd*xd      │
   │ Output Range: z in (-inf, +inf)                        │
   └────────────────────────────────────────────────────────┘
            │
            ▼
   ┌────────────────────────────────────────────────────────┐
   │ Step 2: Non-Linear Activation (Standard Sigmoid / GLM) │
   │ p_hat = sigma(z) = 1 / (1 + e^(-z))                    │
   │ Output Range: p_hat in (0, 1)                          │
   └────────────────────────────────────────────────────────┘
            │
            ▼
   Predicted Class Posterior Probability: P(Y = 1 | x)
```

---

### 2.2 The Sigmoid (Logistic) Function & Its Mathematical Elegance

The squashing function used is the **Standard Sigmoid Function** $\sigma(z)$:

$$\sigma(z) = \frac{1}{1 + e^{-z}} = \frac{e^z}{1 + e^z}$$

```
The S-Shaped Sigmoid Curve:
       sigma(z) ^
            1.0 |                              .-------- (Asymptote at 1.0)
                |                           .-'
            0.5 |------------------------.-' (z = 0, p = 0.5)
                |                     .-'
            0.0 | --------'                                (Asymptote at 0.0)
                +-------------------------+-------------------------> z
                                         0
```

#### Core Mathematical Properties:
1. **Strictly Bounded**: For all $z \in \mathbb{R}$, $0 < \sigma(z) < 1$. It never reaches 0 or 1 at any finite $z$, acting as asymptotic probability bounds.
2. **Symmetry About the Origin**:
   $$\sigma(-z) = \frac{1}{1 + e^z} = \frac{1 + e^z - e^z}{1 + e^z} = 1 - \frac{e^z}{1 + e^z} = 1 - \sigma(z)$$
3. **Midpoint Anchor at $z = 0$**:
   $$\sigma(0) = \frac{1}{1 + e^0} = \frac{1}{1 + 1} = \mathbf{0.5}$$
4. **Asymptotic Limits**:
   $$\lim_{z \to +\infty} \sigma(z) = 1.0, \qquad \lim_{z \to -\infty} \sigma(z) = 0.0$$
5. **The Magical Derivative Property**:
   The derivative of $\sigma(z)$ with respect to $z$ can be written entirely in terms of its own output:
   $$\frac{d\sigma}{dz} = \frac{d}{dz}(1 + e^{-z})^{-1} = -(1 + e^{-z})^{-2} \cdot (-e^{-z}) = \frac{1}{1 + e^{-z}} \cdot \frac{e^{-z}}{1 + e^{-z}} = \sigma(z) \cdot (1 - \sigma(z))$$
   This property allows neural networks and gradient descent optimizers to compute derivatives with extreme computational efficiency.

---

### 2.3 Odds and Log-Odds (The Logit Transformation)

To understand where the Sigmoid comes from, we view Logistic Regression through the lens of **Odds**:

$$\text{Odds} = \frac{P(Y = 1 \mid \mathbf{x})}{P(Y = 0 \mid \mathbf{x})} = \frac{p}{1 - p} \in [0, \infty)$$

- If the probability of rain is $p = 0.80$, the odds are $\frac{0.80}{0.20} = 4.0$ (spoken as "4 to 1 in favor of rain").
- If the probability is $p = 0.50$, the odds are $\frac{0.50}{0.50} = 1.0$ ("even odds").
- If the probability is $p = 0.10$, the odds are $\frac{0.10}{0.90} \approx 0.111$ ("1 to 9 against rain").

While probability $p$ is constrained to $[0, 1]$, the Odds ratio ranges from $0$ to $+\infty$.
Taking the natural logarithm of the odds maps it across the entire real number line $(-\infty, +\infty)$:

$$\text{Logit}(p) = \ln(\text{Odds}) = \ln\left(\frac{p}{1 - p}\right) \in (-\infty, +\infty)$$

In Logistic Regression, we model this **Log-Odds (Logit)** as a linear function of features:

$$\ln\left(\frac{p}{1 - p}\right) = \mathbf{w}^T \mathbf{x} + w_0$$

Solving for probability $p$ by exponentiating both sides:
$$\frac{p}{1 - p} = e^{\mathbf{w}^T \mathbf{x} + w_0} \implies p = e^{\mathbf{w}^T \mathbf{x} + w_0}(1 - p) \implies p(1 + e^{\mathbf{w}^T \mathbf{x} + w_0}) = e^{\mathbf{w}^T \mathbf{x} + w_0}$$
$$p = \frac{e^{\mathbf{w}^T \mathbf{x} + w_0}}{1 + e^{\mathbf{w}^T \mathbf{x} + w_0}} = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + w_0)}} = \sigma(\mathbf{w}^T \mathbf{x} + w_0)$$

> **The Fundamental Definition**:
> **Logistic Regression is a linear model for the log-odds of the positive class.**
> When feature $x_j$ increases by $1$ unit (holding all other features fixed), the log-odds increase by $w_j$, and the **odds are multiplied by $e^{w_j}$**.

---

### 2.4 The Decision Boundary Geometry & Confidence

When we apply the standard classification threshold $\tau = 0.50$:
$$\hat{y} = 1 \iff \hat{p} \ge 0.50 \iff \sigma(z) \ge 0.50 \iff z \ge 0$$
$$\hat{y} = 1 \iff \mathbf{w}^T \mathbf{x} + w_0 \ge 0$$

The **Decision Boundary** is the exact set of points where the model is maximally uncertain ($\hat{p} = 0.50$):

$$\mathbf{w}^T \mathbf{x} + w_0 = 0$$

```
Decision Boundary Geometry in 2D Feature Space:
         x2 ^
            │       + (Positive class, p_hat > 0.5)
            │      +      +
            │         +   * (Perpendicular distance d indicates high confidence!)
            │            /
            │           /  Decision Boundary: w1*x1 + w2*x2 + w0 = 0
            │          /   (On the line: p_hat = 0.50)
            │         /
            │  o     /       o (Negative class, p_hat < 0.5)
            │    o  /    o
            │      /  o
            +─────/─────────────────────────► x1
```

1. The decision boundary is an **affine hyperplane** of dimension $d-1$ in $d$-dimensional space (a line in 2D, a flat plane in 3D).
2. The parameter vector $\mathbf{w}$ is the **normal vector orthogonal** to the decision boundary, pointing in the direction of increasing Class 1 probability.
3. The signed perpendicular distance from any observation $\mathbf{x}^{(i)}$ to the boundary is:
   $$\text{dist}(\mathbf{x}^{(i)}) = \frac{\mathbf{w}^T \mathbf{x}^{(i)} + w_0}{\|\mathbf{w}\|_2}$$
4. Points located far from the boundary have large $|z|$, producing $\hat{p} \approx 0.999$ or $\hat{p} \approx 0.001$ (**High Confidence**).
5. Points hovering right beside the boundary have $z \approx 0$, producing $\hat{p} \approx 0.51$ (**Low Confidence / Hesitant**).

**Citations & References:**
- Cox, D. R. (1958). The regression analysis of binary sequences. Journal of the Royal Statistical Society: Series B, 20(2), 215-232.
- Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer, Chapter 4.

---

## 3. The Optimization Objective: Binary Cross-Entropy (Log-Loss)
### 3.1 Why Mean Squared Error (MSE) Breaks with Sigmoid

If we attempted to train Logistic Regression using MSE:

$$J_{\text{MSE}}(\mathbf{w}) = \frac{1}{n} \sum_{i=1}^n \left(y^{(i)} - \sigma(\mathbf{w}^T \mathbf{x}^{(i)})\right)^2$$

Because $\sigma(z)$ is non-linear and saturates at both ends, the resulting loss surface $J_{\text{MSE}}$ is **non-convex**. It possesses severe local plateaus where gradients vanish ($\sigma'(z) \to 0$), causing gradient descent to get trapped in terrible sub-optimal states.

---

### 3.2 Derivation of Log-Loss via Maximum Likelihood Estimation

For a single binary observation $(x^{(i)}, y^{(i)})$ where $y^{(i)} \in \{0, 1\}$, the probability of observing the label is modeled as a Bernoulli random variable:

$$P(Y = y^{(i)} \mid \mathbf{x}^{(i)}) = (\hat{p}_i)^{y^{(i)}} (1 - \hat{p}_i)^{1 - y^{(i)}}$$

Where $\hat{p}_i = \sigma(\mathbf{w}^T \mathbf{x}^{(i)})$.

Assuming independent observations, the likelihood of the entire training dataset is the product of individual probabilities:

$$L(\mathbf{w}) = \prod_{i=1}^n (\hat{p}_i)^{y^{(i)}} (1 - \hat{p}_i)^{1 - y^{(i)}}$$

To maximize this likelihood without multiplying tiny probabilities (which causes numerical underflow), we take the natural logarithm to get the log-likelihood:

$$\ln L(\mathbf{w}) = \sum_{i=1}^n \left[ y^{(i)} \ln(\hat{p}_i) + (1 - y^{(i)}) \ln(1 - \hat{p}_i) \right]$$

To convert this maximization into a standard loss minimization, we negate it and divide by $n$. This defines **Binary Cross-Entropy (Log-Loss)**:

$$J(\mathbf{w}) = -\frac{1}{n} \sum_{i=1}^n \left[ y^{(i)} \ln(\hat{p}_i) + (1 - y^{(i)}) \ln(1 - \hat{p}_i) \right]$$

```
Behavior of Log-Loss Penalty:
   When True Label y = 1:                    When True Label y = 0:
   Loss = -ln(p_hat)                         Loss = -ln(1 - p_hat)
      Loss ^                                    Loss ^
           | \                                       |          /
           |  \                                      |         /
           |   \                                     |        /
           |    '--.                                 |   .--'
         0 +---------> p_hat                       0 +---------> p_hat
           0        1                                0        1
       p_hat -> 1: Loss -> 0                     p_hat -> 0: Loss -> 0
       p_hat -> 0: Loss -> +inf!                 p_hat -> 1: Loss -> +inf!
```

> **The Penalty Intuition**:
> - If true label is $y = 1$ and model predicts $\hat{p} = 0.99$, Loss $= -\ln(0.99) \approx 0.01$ (Virtually zero penalty).
> - If true label is $y = 1$ and model confidently predicts $\hat{p} = 0.001$, Loss $= -\ln(0.001) \approx 6.91$ (Severe penalty tending to infinity).

### 3.3 Concrete Hand-Calculated Log-Loss Walkthrough

Let us evaluate the Log-Loss across 5 representative patient predictions to see how confident mistakes are penalized:

| Patient ($i$) | True Label ($y_i$) | Predicted Probability ($\hat{p}_i$) | Loss Formula Applied | Loss $\ell_i$ | Diagnostic Behavior |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Patient 1** | $y = 1$ | $\hat{p} = 0.90$ | $-\ln(0.90)$ | **$0.105$** | Confident correct detection (tiny loss). |
| **Patient 2** | $y = 0$ | $\hat{p} = 0.10$ | $-\ln(1 - 0.10) = -\ln(0.90)$ | **$0.105$** | Confident correct rejection (tiny loss). |
| **Patient 3** | $y = 1$ | $\hat{p} = 0.60$ | $-\ln(0.60)$ | **$0.511$** | Hesitant correct detection (moderate loss). |
| **Patient 4** | $y = 0$ | $\hat{p} = 0.40$ | $-\ln(1 - 0.40) = -\ln(0.60)$ | **$0.511$** | Hesitant correct rejection (moderate loss). |
| **Patient 5** | $y = 1$ | $\hat{p} = 0.05$ | $-\ln(0.05)$ | **$2.996$** | **Confident Blunder!** (Severe exponential blowup). |

#### Dataset Average Log-Loss:
$$J(\mathbf{w}) = \frac{1}{5}(0.105 + 0.105 + 0.511 + 0.511 + 2.996) = \frac{4.228}{5} = \mathbf{0.846}$$

Notice that Patient 5 accounts for over **70% of the entire dataset loss** ($2.996 / 4.228 = 70.9\%$)! Log-Loss relentlessly forces optimization away from confident false assurances.

---

### 3.4 The Gradient Update Rule

Taking the derivative of the Log-Loss with respect to weight vector $\mathbf{w}$ yields an extraordinarily elegant result:

$$\nabla_{\mathbf{w}} J(\mathbf{w}) = \frac{1}{n} \mathbf{X}^T (\hat{\mathbf{p}} - \mathbf{y})$$

> **The Mathematical Parallel**:
> Notice that the gradient of Logistic Regression has the **exact same functional form** as the gradient of Ordinary Least Squares Linear Regression! The only difference is that $\hat{\mathbf{p}} = \sigma(\mathbf{Xw})$ instead of $\hat{\mathbf{y}} = \mathbf{Xw}$.

**Citations & References:**
- Good, I. J. (1952). Rational decisions. Journal of the Royal Statistical Society: Series B, 14(1), 107-114.
- McCullagh, P., & Nelder, J. A. (1989). Generalized Linear Models (2nd ed.). Chapman and Hall/CRC.

---

## 4. The Confusion Matrix & Primary Classification Metrics
### 4.1 The Confusion Matrix Anatomy

To convert continuous probabilities $\hat{p} \in (0, 1)$ into actionable operational decisions, we compare them against a decision threshold $\tau \in [0, 1]$ (default $\tau = 0.50$):

$$\hat{y} = \begin{cases} 1 & \text{if } \hat{p} \ge \tau \\ 0 & \text{if } \hat{p} < \tau \end{cases}$$

Every single prediction falls into one of four mutually exclusive quadrants in the **Confusion Matrix**:

```
The 2x2 Confusion Matrix:
                         Predicted Negative (0)         Predicted Positive (1)
                   ┌──────────────────────────────┬──────────────────────────────┐
    Actual         │      TRUE NEGATIVE (TN)      │     FALSE POSITIVE (FP)      │
    Negative (0)   │   Healthy patient cleared.   │   Healthy patient panicked.  │
                   │   Correct Rejection.         │   Type I Error (False Alarm) │
                   ├──────────────────────────────┼──────────────────────────────┤
    Actual         │     FALSE NEGATIVE (FN)      │      TRUE POSITIVE (TP)      │
    Positive (1)   │   Sick patient sent home!    │   Sick patient diagnosed.    │
                   │   Type II Error (Missed Hit) │   Correct Hit.               │
                   └──────────────────────────────┴──────────────────────────────┘
```

---

### 4.2 Comprehensive Metric Formulas & Hand-Calculated 1,000-Patient Example

Suppose an oncology clinic evaluates a diagnostic AI model on $N = 1,000$ patients:
- Actual Sick Patients ($y = 1$): $100$
- Actual Healthy Patients ($y = 0$): $900$

The model produces the following Confusion Matrix:
- $\text{TP} = 80$ (Caught 80 sick patients)
- $\text{FN} = 20$ (Missed 20 sick patients)
- $\text{FP} = 50$ (Falsely flagged 50 healthy people)
- $\text{TN} = 850$ (Correctly cleared 850 healthy people)

#### 1. Accuracy
$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} = \frac{80 + 850}{1000} = \frac{930}{1000} = \mathbf{93.0\%}$$
- *Limitation*: If a doctor simply guessed "Healthy" for all 1,000 patients without even seeing them, they would achieve $90.0\%$ accuracy! Accuracy masks poor minority detection.

#### 2. Precision (Positive Predictive Value)
$$\text{Precision} = \frac{TP}{TP + FP} = \frac{80}{80 + 50} = \frac{80}{130} \approx \mathbf{61.5\%}$$
- *Meaning*: When the model fires an alarm and says "Patient is Positive", there is a $61.5\%$ chance they actually have the disease. (The other $38.5\%$ are false alarms).

#### 3. Recall (Sensitivity / True Positive Rate / Hit Rate)
$$\text{Recall} = \frac{TP}{TP + FN} = \frac{80}{80 + 20} = \frac{80}{100} = \mathbf{80.0\%}$$
- *Meaning*: Out of all people who genuinely have the disease in reality, the model successfully catches $80\%$. (It missed $20\%$ of cancer patients!).

#### 4. Specificity (True Negative Rate / Selectivity)
$$\text{Specificity} = \frac{TN}{TN + FP} = \frac{850}{850 + 50} = \frac{850}{900} \approx \mathbf{94.4\%}$$
- *Meaning*: Out of all healthy people, $94.4\%$ were correctly cleared.
- *False Positive Rate (Fall-out)*: $\text{FPR} = 1 - \text{Specificity} = \frac{50}{900} \approx \mathbf{5.6\%}$.

#### 5. F1-Score (The Harmonic Mean)
$$\text{F}_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}} = 2 \cdot \frac{0.6154 \cdot 0.8000}{0.6154 + 0.8000} = \frac{0.9846}{1.4154} \approx \mathbf{0.696}$$

---

### 4.3 Type I vs. Type II Errors: The Real-World Asymmetry

In pure mathematics, all errors have equal cost. In the real world, the costs of Type I and Type II errors are wildly asymmetric:

| Industry Domain | Positive Event ($y=1$) | Type I Error (False Positive) | Type II Error (False Negative) | Critical Priority |
| :--- | :--- | :--- | :--- | :--- |
| **Oncology Diagnosis** | Malignant Tumor Present | Healthy patient undergoes follow-up biopsy. Stressful, but non-fatal. | Cancer missed; patient sent home without treatment. **Fatal outcome!** | **MAXIMIZE RECALL** (Drive False Negatives to 0). |
| **Email Spam Filtering** | Unsolicited Phishing Spam | Legitimate job offer or urgent bank notice sent to Spam folder. Catastrophic disruption. | Spam email slips into inbox. Mild annoyance to user. | **MAXIMIZE PRECISION** (Ensure flagged emails are 99.9% true spam). |
| **Credit Card Fraud** | Stolen Card Transaction | Cardholder declined at dinner; mild embarrassment, quick SMS confirmation. | 5,000 USD fraudulent charge approved; bank suffers financial loss. | **BALANCED F1 / HIGH RECALL** |
| **Telecom Churn Retention** | Customer Will Churn | Loyal customer given an unneeded 500 USD retention voucher. Direct revenue loss. | Customer churns to competitor; lifetime value lost. | **CALIBRATED PRECISION** (Spend retention bonus only when sure). |

**Citations & References:**
- Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters, 27(8), 861-874.
- Powers, D. M. (2020). Evaluation: from precision, recall and F-measure to ROC, informedness, markedness and correlation. arXiv:2010.16061.

---

## 5. Operating Thresholds & Diagnostic Curves: ROC-AUC vs. Precision-Recall
### 5.1 The Threshold Lever: Balancing Precision and Recall

The decision threshold $\tau$ is an external business knob, **not** a fixed mathematical law:

```
Threshold Dynamic:
   Lower Threshold (tau = 0.2):
     --> Model predicts Positive much more aggressively.
     --> Catches almost all positives: RECALL INCREASES.
     --> Generates more false alarms: PRECISION DECREASES.

   Raise Threshold (tau = 0.8):
     --> Model predicts Positive only when extremely confident.
     --> Low false alarms: PRECISION INCREASES.
     --> Misses borderline positive cases: RECALL DECREASES.
```

---

### 5.2 The ROC Curve and Area Under the Curve (ROC-AUC)

The **Receiver Operating Characteristic (ROC)** curve plots the trade-off across all possible thresholds $\tau \in [0, 1]$:
- **Y-axis**: True Positive Rate ($\text{TPR} = \text{Recall}$)
- **X-axis**: False Positive Rate ($\text{FPR} = 1 - \text{Specificity}$)

```
ROC Curve Interpretation:
       TPR (Recall) ^
                1.0 |               .------------ (Perfect Classifier: AUC = 1.0)
                    |            .-'
                    |         .-'
                    |      .-'   AUC = 0.85
                    |   .-'
                    |.-' (Diagonal line: Random Guessing, AUC = 0.5)
                0.0 +-------------------------------------------> FPR
                    0.0                                       1.0
```

#### Meaning of ROC-AUC:
The Area Under the ROC Curve (ROC-AUC) has a concrete probabilistic interpretation:
> *ROC-AUC is the probability that the classifier will rank a randomly chosen positive sample higher than a randomly chosen negative sample.*
- $\text{AUC} = 0.5$: Worthless coin flip.
- $\text{AUC} = 0.85$: Strong discrimination ability.
- $\text{AUC} = 1.0$: Perfect class separation.

---

### 5.3 Worked Whiteboard Example: Calculating ROC-AUC by Hand

Suppose your model scores 5 website browsing sessions predicting whether the visitor will make a purchase ($y = 1$).
Two sessions bought ($A, B$) and three did not ($C, D, E$):

| Session | Actually Bought? ($y$) | Model Predicted Score ($\hat{p}$) |
| :--- | :--- | :--- |
| **A** | **Yes ($y = 1$)** | **0.90** |
| **C** | No ($y = 0$) | 0.70 |
| **B** | **Yes ($y = 1$)** | **0.40** |
| **D** | No ($y = 0$) | 0.30 |
| **E** | No ($y = 0$) | 0.10 |

#### Step 1: Pairwise Ranking (Concordant Pairs)
There are $N_{\text{pos}} \times N_{\text{neg}} = 2 \times 3 = \mathbf{6}$ possible buyer–non-buyer pairs.
Let us test every single pair to check if the buyer received a strictly higher score than the non-buyer:
1. **$A$ (0.90) vs $C$ (0.70)**: $A$ scores higher $\implies$ **Win (+1)**
2. **$A$ (0.90) vs $D$ (0.30)**: $A$ scores higher $\implies$ **Win (+1)**
3. **$A$ (0.90) vs $E$ (0.10)**: $A$ scores higher $\implies$ **Win (+1)**
4. **$B$ (0.40) vs $C$ (0.70)**: $B$ scores lower ($0.40 < 0.70$) $\implies$ **Loss (0)**
5. **$B$ (0.40) vs $D$ (0.30)**: $B$ scores higher $\implies$ **Win (+1)**
6. **$B$ (0.40) vs $E$ (0.10)**: $B$ scores higher $\implies$ **Win (+1)**

Total buyer wins across all pairs: $3 + 2 = \mathbf{5}$.
$$\text{ROC-AUC} = \frac{\text{Concordant Pairs}}{\text{Total Pairs}} = \frac{5}{6} \approx \mathbf{0.833}$$

#### Step 2: Step-by-Step Threshold Sweep
If we sweep decision threshold $\tau$ across the scores, we generate the empirical ROC coordinates:

| Threshold ($\tau$) | Predicted Positives | True Positives ($TP$) | False Positives ($FP$) | $\text{TPR} = \frac{TP}{2}$ | $\text{FPR} = \frac{FP}{3}$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $\tau > 0.90$ | None | 0 | 0 | **0.0** | **0.0** |
| $\tau = 0.90$ | {A} | 1 | 0 | **0.5** | **0.0** |
| $\tau = 0.70$ | {A, C} | 1 | 1 | **0.5** | **0.333** |
| $\tau = 0.40$ | {A, C, B} | 2 | 1 | **1.0** | **0.333** |
| $\tau = 0.30$ | {A, C, B, D} | 2 | 2 | **1.0** | **0.667** |
| $\tau = 0.10$ | All 5 | 2 | 3 | **1.0** | **1.0** |

Calculating the area under these stepped rectangular blocks gives:
$$\text{Area} = (0.333 - 0.0) \times 0.5 + (1.0 - 0.333) \times 1.0 = 0.1667 + 0.6667 = \mathbf{0.833}$$
Both the pairwise ranking count and the geometric integral match with 100% mathematical precision!

---

### 5.4 Why ROC Deceives on Imbalanced Data (And Why PR Curves Rule)

Consider a fraud detection dataset with 100,000 transactions:
- 99,000 legitimate ($y = 0$)
- 1,000 fraudulent ($y = 1$)

Suppose a model produces **990 False Positives** ($FP = 990$) while catching 800 frauds ($TP = 800$):
- $\text{False Positive Rate} = \frac{FP}{TN + FP} = \frac{990}{98,010 + 990} = \frac{990}{99,000} = 0.01$ (Only 1%! The ROC curve looks stunning!).
- But look at **Precision**: $\text{Precision} = \frac{TP}{TP + FP} = \frac{800}{800 + 990} = \frac{800}{1790} \approx 44.7\%$! More than half of all flagged transactions are false alarms!

> **The Golden Production Rule**:
> - Use **ROC-AUC** when classes are roughly balanced.
> - Use the **Precision-Recall Curve (PR-AUC)** whenever positive events are rare (< 10%). The PR curve ignores True Negatives ($TN$), exposing false alarm dilution immediately.

**Citations & References:**
- Saito, T., & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. PloS ONE, 10(3), e0118432.

---

## 6. Class Imbalance Remediation & Production Scikit-Learn Pipeline
### 6.1 The Accuracy Paradox in Imbalanced Regimes

If $99\%$ of credit card transactions are legitimate and $1\%$ are fraudulent, a trivial model that outputs `Legitimate` for every single query achieves:

$$\text{Accuracy} = \frac{99,000 + 0}{100,000} = \mathbf{99.0\%}$$

The model has a 99% accuracy score, yet it stops **zero fraud** and is completely worthless.
In real-world ML systems with imbalanced targets, **Accuracy is a toxic metric**.

---

### 6.2 Industry Remediation Strategies

```
Remediation Strategy Spectrum:
   ┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
   │ 1. Cost-Sensitive Learning      │ 2. Data Resampling (SMOTE)      │ 3. Threshold Tuning             │
   ├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
   │ Multiplies minority loss by     │ Synthesizes artificial minority │ Optimizes decision threshold τ  │
   │ class weight factor.            │ samples using k-NN vectors.     │ on validation PR curve.         │
   │ Zero data duplication.          │ Balances training distribution. │ Direct alignment to business $. │
   └─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
```

#### Strategy 1: Cost-Sensitive Loss Weighting (`class_weight='balanced'`)
Instead of treating all errors equally, we scale the loss of each sample by its class weight:

$$J_{\text{weighted}}(\mathbf{w}) = -\frac{1}{n} \sum_{i=1}^n w_{y^{(i)}} \left[ y^{(i)} \ln(\hat{p}_i) + (1 - y^{(i)}) \ln(1 - \hat{p}_i) \right]$$

In Scikit-Learn, `class_weight='balanced'` computes weights inversely proportional to class frequencies:

$$w_c = \frac{n_{\text{samples}}}{k \cdot n_c}$$

For 1,000 samples with 950 Class 0 and 50 Class 1 ($k=2$):
$$w_0 = \frac{1000}{2 \times 950} \approx 0.526, \qquad w_1 = \frac{1000}{2 \times 50} = \mathbf{10.000}$$
Missing a single Class 1 sample is penalized **19 times more severely** than missing a Class 0 sample! The optimizer shifts the decision boundary to protect the minority class.

#### Strategy 2: SMOTE (Synthetic Minority Over-sampling Technique)
Instead of simply duplicating existing minority points (which causes overfitting), SMOTE synthesizes new plausible feature vectors along the line segments connecting $k$-nearest minority neighbors:

$$\mathbf{x}_{\text{new}} = \mathbf{x}_i + \lambda \cdot (\mathbf{x}_{zi} - \mathbf{x}_i), \qquad \lambda \sim \text{Uniform}(0, 1)$$

```
SMOTE Geometric Synthesis:
         x2 ^
            │            x_zi (Minority Neighbor)
            │           /
            │          * (x_new synthesized on line segment!)
            │         /
            │        x_i (Minority Sample)
            +────────────────────────► x1
```

*Critical Anti-Leakage Rule*: Never run SMOTE on the whole dataset before cross-validation! SMOTE must be performed **strictly inside each training fold**.

---

### 6.3 End-to-End Scikit-Learn Production Pipeline

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score,
    precision_recall_curve
)

# 1. Generate imbalanced binary problem: 2,500 samples, 95% Class 0 (Retain), 5% Class 1 (Churn)
X, y = make_classification(
    n_samples=2500,
    n_features=12,
    n_informative=6,
    weights=[0.95, 0.05],
    random_state=42
)

# 2. Stratified Train / Test Split (Guarantees 5% positive class in both partitions)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 3. Cost-Sensitive Logistic Pipeline (Leak-free scaling + balanced loss weights)
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(
        class_weight="balanced",  # Multiplies minority loss by n / (2 * n_pos)
        solver="lbfgs",
        C=1.0,                    # Inverse regularization strength (C = 1 / lambda)
        random_state=42
    ))
])
pipeline.fit(X_train, y_train)

# 4. Predict Raw Probabilities on Unseen Test Partition
y_probs = pipeline.predict_proba(X_test)[:, 1]

# 5. Business Threshold Optimization (Default tau = 0.50 vs Custom tau = 0.35)
default_preds = pipeline.predict(X_test)
custom_tau = 0.35
custom_preds = (y_probs >= custom_tau).astype(int)

# 6. Comprehensive Metric Reporting
roc_auc = roc_auc_score(y_test, y_probs)
pr_auc = average_precision_score(y_test, y_probs)

print("=== IMBALANCE-AWARE PERFORMANCE REPORT ===")
print(f"ROC-AUC Score:                 {roc_auc:.4f}")
print(f"PR-AUC (Average Precision):    {pr_auc:.4f}")
print("\nConfusion Matrix at Custom Threshold (tau = 0.35):")
print(confusion_matrix(y_test, custom_preds))
print("\nDetailed Classification Report (tau = 0.35):")
print(classification_report(y_test, custom_preds, target_names=["Retain", "Churn"]))
```

---

### 6.4 Key Diagnostic Summary & Engineering Pitfalls

| Diagnostic Pitfall | Why It Happens | Severe Consequence | Production Solution |
| :--- | :--- | :--- | :--- |
| **Evaluating Imbalanced Data with Accuracy** | Majority class dominates sample counts. | Model predicts majority class everywhere and passes evaluation while completely failing in production. | Ban accuracy; evaluate strictly with **PR-AUC, F1-Score, and Recall**. |
| **Applying SMOTE Before Cross-Validation Split** | Synthetic points created from test fold distribution leak into training fold. | Optimistic validation metrics; massive performance collapse in production. | Run SMOTE strictly inside training folds using `imblearn.pipeline.Pipeline`. |
| **Treating 0.50 as an Inviolable Threshold** | Blindly using `.predict()` without tuning $\tau$. | Fails business objectives when False Negatives cost 50x more than False Positives. | Use `.predict_proba()` and select threshold $\tau$ from validation PR curve. |
| **Unstandardized Features Before Logistic Regression** | Features have different numerical ranges (e.g. Salary vs Age). | L2 regularization (`C` parameter) penalizes small-scale features unfairly; gradient descent oscillates. | Always wrap `StandardScaler` and `LogisticRegression` inside a `Pipeline`. |

**Citations & References:**
- Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: synthetic minority over-sampling technique. JAIR, 16, 321-357.
- He, H., & Garcia, E. A. (2009). Learning from imbalanced data. IEEE TKDE, 21(9), 1263-1284.

---
