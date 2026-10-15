"""
Lecture 6 Data: Polynomial Regression, Model Complexity & The Bias-Variance Tradeoff
Term 5 Classical Machine Learning (CML)
"""

CML_L06_DATA = {
    "slug": "cml-t5-l06",
    "title": "6. Polynomial Regression, Model Complexity & The Bias-Variance Tradeoff",
    "subject": "Classical Machine Learning",
    "subject_code": "CML",
    "term": "Term 5",
    "order": 6,
    "read_time": "60 mins",
    "status": "published",
    "prerequisites": [
        "cml-t5-l01",
        "cml-t5-l02",
        "cml-t5-l03",
        "cml-t5-l04",
        "cml-t5-l05"
    ],
    "summary": "A comprehensive, mathematically rigorous deep dive into Polynomial Regression, model generalization, and the Bias-Variance Tradeoff. Investigates how non-linear hypotheses are formulated through linear parameterizations via basis expansions, proves why raw R-squared monotonically fails as an evaluation metric on training sets, derives the exact mathematical formulation of Adjusted R-squared, formalizes Occam's Razor across the model complexity spectrum (degrees 1 through 99), delivers a complete step-by-step mathematical proof of the Bias-Variance-Noise decomposition of expected Mean Squared Error, visualizes variance dynamics using the classical dartboard analogy, analyzes numerical instability in high-degree Vandermonde design matrices, and builds robust Scikit-Learn evaluation pipelines.",
    "key_takeaways": [
        "1. Polynomial regression models non-linear relationships by creating polynomial power features (x, x^2, x^3) while remaining strictly linear in the parameter weights w; standard OLS normal equations and gradient descent apply without modification.",
        "2. In transformed polynomial space phi(x), the model is an affine hyperplane; projected back onto the original feature coordinate axis x, the prediction appears as a smooth flexible curve.",
        "3. Raw R^2 on training data is mathematically non-decreasing with respect to polynomial degree: adding higher powers (even pure random Gaussian noise) can never increase residual sum of squares. Evaluating model degree solely on training R^2 guarantees severe overfitting.",
        "4. Adjusted R^2 penalizes model complexity via the factor (m - 1) / (m - p - 1), where p is the total number of post-expansion features; it drops when an added degree fails to reduce residual variance by more than random chance.",
        "5. Occam's Razor (Lex Parsimoniae) dictates that among competing hypotheses that achieve equivalent generalization performance on holdout test data, the simplest model (lowest degree / fewest parameters) must always be selected.",
        "6. Expected out-of-sample prediction error decomposes strictly into three orthogonal components: E[(y - y_hat)^2] = Bias^2 + Variance + sigma^2 (irreducible Bayes error).",
        "7. Underfitting is characterized by high bias and low variance (model is too rigid to capture underlying signal); Overfitting is characterized by low bias and high variance (model is hypersensitive to idiosyncratic training noise).",
        "8. High-degree polynomial expansions trigger structural multicollinearity and severe ill-conditioning in the Vandermonde matrix; pipeline standardization with StandardScaler is mandatory to prevent numerical cancellation."
    ],
    "last_updated": "2026-10-16T00:00:00Z",
    "approval_status": "approved",
    "sections": [
        {
            "section_id": "cml-l06-sec01",
            "heading": "1. Non-Linear Modeling Foundations: The Motivation for Polynomial Feature Expansion",
            "citations": [
                "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). Springer.",
                "Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer."
            ],
            "body": r"""### 1.1 The Inherent Non-Linearity of Real-World Phenomena

In Lectures 3 and 4, we operated under the foundational assumption of linear regression: that the relationship between the independent input features $\mathbf{x}$ and the target response $y$ is strictly linear:
$$y = w_0 + w_1 x_1 + \dots + w_d x_d + \varepsilon$$

However, physical, economic, and industrial systems rarely adhere to straight-line trajectories:
- **Aerodynamics & Drag Resistance**: Wind resistance on an automobile or aircraft scales quadratically with velocity ($F_{\text{drag}} \propto v^2$).
- **Economics & Yield Elasticity**: Marginal returns on digital ad spend or fertilizer application exhibit diminishing marginal returns, peaking and curving downward.
- **Epidemiology & Pharmacokinetics**: Drug concentration in the bloodstream follows sharp non-linear absorption, saturation, and exponential elimination curves.
- **Real Estate Valuation**: The marginal utility of additional living space decays non-linearly with home size.

```
       Linear Model (Degree 1) on Curved Data         Polynomial Model (Degree 2) on Curved Data
              Underfitting: High Bias                          Optimal Fit: Balanced
 
        y ^                                            y ^
          |          *                                   |          *
          |       *     *                                |       * / \ *
          |     *         *                              |     *  /   \  *  <-- Quadratic curve
          |   *             *                            |   *   /     \   *    captures true trend
          |  *               *                           |  *   /       \   *
          | /------------------> Straight line misses    |     /         \
          +----------------------------> x               +----------------------------> x
```

If we restrict ourselves to fitting a straight line $\hat{y} = w_0 + w_1 x$ through intrinsically curved data, the model suffers from **underfitting**: it fundamentally lacks the functional capacity to capture the underlying signal.

---

### 1.2 The Paradigm Shift: Transforming Features, Not Algorithms

When confronted with non-linear patterns, an engineer faces two distinct design choices:
1. **Develop a Non-Linear Optimization Algorithm**: Formulate complex non-linear parameterizations where $y = f(\mathbf{x}; \mathbf{w})$ is non-linear with respect to $\mathbf{w}$. This destroys convexity, introduces intractable non-convex optimization surfaces riddled with saddle points and local minima, and invalidates closed-form solutions.
2. **Transform the Input Features (Basis Expansion)**: Maintain the mathematically proven, convex linear regression machinery ($\mathbf{w}^* = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$ and Gradient Descent), but expand the raw input features $\mathbf{x}$ into non-linear polynomial powers:
   $$\phi(x) = \begin{bmatrix} 1 & x & x^2 & x^3 & \dots & x^d \end{bmatrix}^T$$

By mapping low-dimensional non-linear inputs into a higher-dimensional feature space, we convert a non-linear regression problem into a standard linear regression problem."""
        },
        {
            "section_id": "cml-l06-sec02",
            "heading": "2. Mathematical Formulation: Polynomial Bases & The Linear-in-Parameters Property",
            "citations": [
                "Deisenroth, M. P., Faisal, A. A., & Ong, C. S. (2020). Mathematics for Machine Learning. Cambridge University Press.",
                "Montgomery, D. C., Peck, E. A., & Vining, G. G. (2021). Introduction to Linear Regression Analysis. John Wiley & Sons."
            ],
            "body": r"""### 2.1 Scalar Formulation of Polynomial Regression

Let $x \in \mathbb{R}$ be a single continuous scalar feature. A polynomial regression model of degree $d$ is formulated as:
$$\hat{y} = w_0 + w_1 x + w_2 x^2 + w_3 x^3 + \dots + w_d x^d = w_0 + \sum_{j=1}^d w_j x^j$$

where:
- $d \in \mathbb{N}$ represents the **degree of the polynomial** (the highest exponent of the feature).
- $w_0$ is the intercept parameter.
- $w_1, w_2, \dots, w_d$ are the polynomial coefficient weights.

#### Degrees of Familiar Curves:
- **Degree 1 ($d=1$)**: Linear model ($\hat{y} = w_0 + w_1 x$) — straight line.
- **Degree 2 ($d=2$)**: Quadratic model ($\hat{y} = w_0 + w_1 x + w_2 x^2$) — parabola with a single peak or valley.
- **Degree 3 ($d=3$)**: Cubic model ($\hat{y} = w_0 + w_1 x + w_2 x^2 + w_3 x^3$) — S-shaped curve with up to two inflection points.
- **Degree $d$**: Can model up to $d-1$ extrema (local peaks and valleys).

---

### 2.2 Multivariate Polynomial Expansion & Feature Combinatorics

When the dataset contains multiple independent variables $\mathbf{x} = [x_1, x_2, \dots, x_k]^T$, polynomial expansion incorporates both **pure power terms** ($x_j^p$) and **cross-feature interaction terms** ($x_j x_l$).

For example, given two features $\mathbf{x} = [x_1, x_2]^T$, a complete degree-2 polynomial expansion yields:
$$\boldsymbol{\phi}(\mathbf{x}) = \begin{bmatrix} 1 & x_1 & x_2 & x_1^2 & x_1 x_2 & x_2^2 \end{bmatrix}^T$$
and the regression equation becomes:
$$\hat{y} = w_0 + w_1 x_1 + w_2 x_2 + w_3 x_1^2 + w_4 x_1 x_2 + w_5 x_2^2$$

#### Combinatorial Explosion of Feature Dimension:
For an input vector with $k$ features expanded to degree $d$, the total number of features $p$ (including the intercept) is given by the multiset combination formula:
$$p = \binom{k + d}{d} = \frac{(k + d)!}{k! \, d!}$$

| Original Features ($k$) | Polynomial Degree ($d$) | Total Features ($p$) | Computational Impact |
| :--- | :--- | :--- | :--- |
| 1 | 2 | 3 | Trivial |
| 1 | 5 | 6 | Minimal |
| 1 | 25 | 26 | Fast, but prone to ill-conditioning |
| 10 | 2 | 66 | Modest |
| 10 | 3 | 286 | Moderate |
| 10 | 5 | 3,003 | Large memory footprint |
| 100 | 3 | 176,851 | **Explosion**: Normal equation inversion collapses |

---

### 2.3 The Core Insight: Linear in Parameters $\mathbf{w}$

The single most fundamental theoretical insight in polynomial regression is the distinction between **linearity in features** versus **linearity in parameters**:

$$\hat{y} = \mathbf{w}^T \boldsymbol{\phi}(\mathbf{x})$$

Although $\hat{y}$ is a non-linear, polynomial function of the raw input $x$, it is **strictly linear with respect to the parameter vector $\mathbf{w}$**:
$$\frac{\partial \hat{y}}{\partial w_j} = \phi_j(x) = x^j$$

Because the partial derivatives with respect to weights depend exclusively on the transformed inputs $\phi_j(x)$ and contain no parameter terms, the Mean Squared Error loss function:
$$J(\mathbf{w}) = \frac{1}{m} \|\boldsymbol{\Phi} \mathbf{w} - \mathbf{y}\|_2^2$$
remains **strictly convex quadratic** in $\mathbf{w}$.

```
                 The Geometric Duality of Polynomial Regression
 
     Original 1D Space: x                    Transformed 2D Feature Space: (x, x^2)
        y ^                                       x^2 ^
          |        *                                  |        *  *  (Hyperplane in 3D)
          |     *     *                               |     *
          |   *         *                             |   *
          |  *           *                            |  *
          +-----------------> x                       +-----------------> x
        Appears as a curved                         Appears as a flat affine
        non-linear parabola                         hyperplane
```

Consequently:
1. The loss surface has a single unique global minimum $\mathbf{w}^*$. There are zero local minima.
2. The closed-form Normal Equation remains fully valid:
   $$\mathbf{w}^* = (\boldsymbol{\Phi}^T \boldsymbol{\Phi})^{-1} \boldsymbol{\Phi}^T \mathbf{y}$$
3. All gradient descent update rules and convergence proofs derived in Lecture 5 apply directly."""
        },
        {
            "section_id": "cml-l06-sec03",
            "heading": "3. Evaluation Dilemma: The Mathematical Fallacy of Raw R-Squared & The Necessity of Adjusted R-Squared",
            "citations": [
                "Theil, H. (1961). Economic Forecasts and Policy. North-Holland Publishing Company.",
                "Kvålseth, T. O. (1985). Cautionary states about R^2. The American Statistician, 39(4), 279-285."
            ],
            "body": r"""### 3.1 The Mathematical Trap of Raw $R^2$

In Lecture 3, we defined the coefficient of determination $R^2$ as the proportion of total variance explained by the model:
$$R^2 = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}} = 1 - \frac{\sum_{i=1}^m (y_i - \hat{y}_i)^2}{\sum_{i=1}^m (y_i - \bar{y})^2}$$

In polynomial regression, a dangerous trap emerges if an engineer relies on raw $R^2$ computed on the training set to select the optimal polynomial degree.

#### Mathematical Theorem: Monotonic Non-Decreasing Property of Training $R^2$
Let $\mathcal{M}_d$ be a polynomial regression model of degree $d$, and let $\mathcal{M}_{d+1}$ be a model of degree $d+1$ trained on the identical dataset $\mathcal{D}_{\text{train}}$. Then:
$$\text{SS}_{\text{res}}(\mathcal{M}_{d+1}) \le \text{SS}_{\text{res}}(\mathcal{M}_d) \implies R^2_{\text{train}}(\mathcal{M}_{d+1}) \ge R^2_{\text{train}}(\mathcal{M}_d)$$

#### Proof Sketch:
The parameter space of model $\mathcal{M}_d$ is a strict linear subspace of model $\mathcal{M}_{d+1}$:
$$\mathbf{w}_{d} = [w_0, w_1, \dots, w_d]^T \iff \mathbf{w}_{d+1} = [w_0, w_1, \dots, w_d, 0]^T$$
When the Ordinary Least Squares optimizer minimizes $\text{SS}_{\text{res}}$ over $(d+2)$ parameters in $\mathcal{M}_{d+1}$, it can always choose to set $w_{d+1} = 0$, achieving the exact same $\text{SS}_{\text{res}}$ as $\mathcal{M}_d$. If the data permits even an infinitesimal accidental correlation with $x^{d+1}$ (even pure random Gaussian noise), the optimizer will set $w_{d+1} \neq 0$, strictly decreasing $\text{SS}_{\text{res}}$.

**Conclusion**: On training data, raw $R^2$ can **never decrease** as polynomial degree increases. A degree-50 polynomial will always have a higher training $R^2$ than a degree-2 polynomial, even when the degree-50 model is catastrophically overfitting!

---

### 3.2 The Mathematical Derivation of Adjusted $R^2$

To counteract the bias of raw $R^2$, Henri Theil (1961) introduced **Adjusted $R^2$** ($R^2_{\text{adj}}$). Instead of comparing raw sums of squares, Adjusted $R^2$ compares **unbiased sample variance estimators** by dividing each sum of squares by its respective statistical degrees of freedom:

- Unbiased error variance estimator:
  $$s_e^2 = \frac{\text{SS}_{\text{res}}}{m - p - 1}$$
  where $m$ is the number of training samples and $p$ is the number of transformed features (excluding the intercept).
- Unbiased total variance estimator:
  $$s_y^2 = \frac{\text{SS}_{\text{tot}}}{m - 1}$$

Adjusted $R^2$ is defined as:
$$R^2_{\text{adj}} = 1 - \frac{s_e^2}{s_y^2} = 1 - \frac{\text{SS}_{\text{res}} / (m - p - 1)}{\text{SS}_{\text{tot}} / (m - 1)}$$

Substituting $\frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}} = 1 - R^2$:
$$R^2_{\text{adj}} = 1 - (1 - R^2) \frac{m - 1}{m - p - 1}$$

```
                          How Adjusted R^2 Penalizes Complexity
 
   Penalty Factor: (m - 1) / (m - p - 1)
   ------------------------------------
   As degree d increases -> feature count p increases:
   -> Denominator (m - p - 1) shrinks.
   -> The penalty multiplier (m - 1) / (m - p - 1) grows strictly larger than 1.
   -> (1 - R^2) is multiplied by an increasingly heavy penalty factor.
   -> If the new polynomial power does not reduce residual error significantly,
      Adjusted R^2 actively DROPS!
```

---

### 3.3 Critical Edge Cases of Adjusted $R^2$

1. **Can Adjusted $R^2$ Be Negative?**
   Yes. If a polynomial model fits the data so poorly that $(1 - R^2) \frac{m - 1}{m - p - 1} > 1$, $R^2_{\text{adj}}$ drops below zero, signaling that the model performs worse than a simple horizontal line predicting the sample mean $\bar{y}$.
2. **The Singularity Threshold ($p \ge m - 1$)**:
   When the number of polynomial features $p$ equals or exceeds $m - 1$, the denominator $(m - p - 1) \le 0$. The model has achieved complete interpolation (zero residual degrees of freedom), and Adjusted $R^2$ becomes mathematically undefined or explodes to negative infinity."""
        },
        {
            "section_id": "cml-l06-sec04",
            "heading": "4. Generalization, Occam's Razor & The Model Complexity Spectrum",
            "citations": [
                "Thorburn, W. M. (1918). The myth of Occam's razor. Mind, 27(107), 345-353.",
                "Vapnik, V. N. (1998). Statistical Learning Theory. John Wiley & Sons."
            ],
            "body": r"""### 4.1 Generalization: The True Goal of Machine Learning

In production machine learning systems, a model is never judged by how accurately it reconstructs data it has already seen. Its sole commercial value lies in **generalization**: its capacity to output accurate predictions on unseen data sampled from the true joint data-generating distribution $\mathcal{P}_{X, Y}$.

To measure generalization, we strictly partition our data:
$$\mathcal{D} = \mathcal{D}_{\text{train}} \cup \mathcal{D}_{\text{test}}, \quad \mathcal{D}_{\text{train}} \cap \mathcal{D}_{\text{test}} = \emptyset$$
- $\mathcal{D}_{\text{train}}$: Exclusively utilized to estimate parameters $\mathbf{w}$ via optimization.
- $\mathcal{D}_{\text{test}}$: Kept in a sterile vault until model evaluation to simulate deployment on future out-of-sample data.

---

### 4.2 Occam's Razor in Machine Learning Engineering

The philosophical principle of **Occam's Razor** (*Lex Parsimoniae*, formulated by 14th-century Franciscan friar William of Ockham) states:
> *"Numquam ponenda est pluralitas sine necessitate"* — Plurality should never be posited without necessity.

In the context of statistical modeling and machine learning:
> **Among competing hypotheses that achieve comparable generalization performance on unseen test data, always select the simplest model (lowest degree, fewest parameters).**

```
                 Occam's Razor: The Model Selection Decision
 
      Model A (Degree 2 Polynomial): Test MSE = 0.042, 3 parameters
      Model B (Degree 5 Polynomial): Test MSE = 0.041, 6 parameters
      Model C (Degree 25 Polynomial): Test MSE = 0.040, 26 parameters
      
      Engineering Decision: Choose Model A!
      Why? The marginal 0.001 gain in test error is statistically insignificant,
      while Model A is dramatically more robust, interpretable, computationally cheap,
      and impervious to out-of-distribution numerical instability.
```

---

### 4.3 The Model Complexity Spectrum: Degree 1 to Degree 99

Let us trace what occurs as we sweep the polynomial degree $d$ from 1 to 99 on a dataset of $m = 50$ points generated by a noisy quintic function:

```
                            The Model Complexity Spectrum
 
    d = 1                       d = 3 to 5                    d = 20 to 99
  Underfitting                  Just Right                     Overfitting
  (High Bias)                 (Balanced Fit)                 (High Variance)
  +--------------------+      +--------------------+         +--------------------+
  | Rigid straight line|      | Flexible curve     |         | Wildly oscillating |
  | misses basic curve |      | captures true bend |         | passes thru noise  |
  +--------------------+      +--------------------+         +--------------------+
   Train Error: High           Train Error: Low               Train Error: ~0
   Test Error: High            Test Error: Low                Test Error: Catastrophic
```

- **Left Side ($d = 1$) — High Bias**: The model is fundamentally constrained. Even with infinite training data, a straight line cannot bend. Both train error and test error are large.
- **Center ($d = 2 \text{ to } 5$) — The Sweet Spot**: The model capacity matches the underlying physical process. It captures the true mathematical curvature while ignoring local random noise. Both train and test errors reach their joint global minimum.
- **Right Side ($d \ge 15$) — High Variance**: The model possesses far too many degrees of freedom. It twists, loops, and oscillates wildly to pass precisely through every single random noise spike in the training set. Training error plummets toward zero, while test error explodes exponentially."""
        },
        {
            "section_id": "cml-l06-sec05",
            "heading": "5. Underfitting vs. Overfitting: Training Error vs. Test Error Dynamics",
            "citations": [
                "Abu-Mostafa, Y. S., Magdon-Ismail, M., & Lin, H. T. (2012). Learning from Data. AMLBook.",
                "Domingos, P. (2012). A few useful things to know about machine learning. Communications of the ACM, 55(10), 78-87."
            ],
            "body": r"""### 5.1 The Divergence of Training and Test Error Curves

If we plot training error and holdout test error as a function of model complexity (polynomial degree $d$), we observe the single most iconic diagram in classical machine learning:

```
                      The Training vs. Test Error Trajectory
 
        Error
          ^
          | \                                      / Test Error (Generalization)
          |  \                                    /  Explodes due to high variance
          |   \                                  /
          |    \            Optimal Degree      /
          |     \                 v            /
          |      \            +-------+       /
          |       \           |  Min  |      /
          |        \__________+-------+_____/
          |         \...........................
          |          \
          |           \________________________  Training Error
          |                                      Monotonically approaches 0
          +---------------------------------------------> Model Complexity (Degree d)
             <--- Underfitting ---> | <--- Overfitting --->
                   (High Bias)             (High Variance)
```

#### Diagnostic Signatures:
1. **Underfitting Regime**:
   - $\text{MSE}_{\text{train}}$ is high.
   - $\text{MSE}_{\text{test}}$ is high.
   - $\text{MSE}_{\text{test}} \approx \text{MSE}_{\text{train}}$.
   - **Diagnosis**: The model family is too restrictive. Increasing sample size $m$ will not help; the hypothesis class must be enriched (e.g., increase degree $d$, add relevant features).
2. **Overfitting Regime**:
   - $\text{MSE}_{\text{train}}$ is exceptionally low ($\to 0$).
   - $\text{MSE}_{\text{test}}$ is catastrophically high.
   - $\text{MSE}_{\text{test}} \gg \text{MSE}_{\text{train}}$ (the **generalization gap** explodes).
   - **Diagnosis**: The model is memorizing sample noise. Remediation requires reducing degree $d$, applying regularization ($L_2$ Ridge or $L_1$ Lasso), or acquiring more training data.

---

### 5.2 Comparative Diagnostic Matrix

| Diagnostic Metric | Underfitted Model (Degree 1) | Optimal Model (Degree 3-4) | Overfitted Model (Degree 25) |
| :--- | :--- | :--- | :--- |
| **Training Loss ($\text{MSE}_{\text{train}}$)** | High ($> 1.5$) | Low ($\approx 0.04$) | Near Zero ($< 0.001$) |
| **Test Loss ($\text{MSE}_{\text{test}}$)** | High ($> 1.6$) | Low ($\approx 0.045$) | Massive ($> 10^3$ to $10^8$) |
| **Training $R^2$** | Low ($0.35$) | High ($0.94$) | Near Perfect ($0.999$) |
| **Test $R^2$** | Low ($0.32$) | High ($0.93$) | Highly Negative ($< -100$) |
| **Adjusted $R^2$ (Train)** | Low | High (Peaked) | Drops sharply or undefined |
| **Weight Norm $\|\mathbf{w}\|_2$** | Small | Moderate | Astonomical ($10^6$ to $10^{12}$) |
| **Sensitivity to New Points** | Rigid / Insensitive | Robust / Stable | Hyper-erratic swings |"""
        },
        {
            "section_id": "cml-l06-sec06",
            "heading": "6. The Bias-Variance Tradeoff: Analytical Decomposition of Expected Generalization Error",
            "citations": [
                "Geman, S., Bienenstock, E., & Doursat, R. (1992). Neural networks and the bias/variance dilemma. Neural Computation, 4(1), 1-58.",
                "James, G., Witten, D., Hastie, T., & Tibshirani, R. (2013). An Introduction to Statistical Learning. Springer."
            ],
            "body": r"""### 6.1 Formal Setup of the Data-Generating Process

Let the true underlying relationship between an input vector $\mathbf{x}$ and scalar target $y$ be governed by a deterministic function $f(\mathbf{x})$ contaminated with additive random noise $\varepsilon$:
$$y = f(\mathbf{x}) + \varepsilon$$

where:
- $f(\mathbf{x}) = \mathbb{E}[y \mid \mathbf{x}]$ represents the true, unobservable ground truth function.
- $\varepsilon$ is a zero-mean random noise variable representing measurement error and latent unobserved variables:
  $$\mathbb{E}[\varepsilon] = 0, \quad \text{Var}(\varepsilon) = \sigma^2$$
- The noise $\varepsilon$ is statistically independent of the input $\mathbf{x}$ and the training dataset $\mathcal{D}$.

Now, suppose we draw a specific training dataset $\mathcal{D} = \{(\mathbf{x}_i, y_i)\}_{i=1}^m$ from the universe and train an estimator $\hat{f}(\mathbf{x}; \mathcal{D})$. Because $\mathcal{D}$ is a random sample, our trained model $\hat{f}$ is itself a **random variable**.

---

### 6.2 Full Mathematical Proof of the Bias-Variance Decomposition

We evaluate the expected out-of-sample squared prediction error at a fixed test point $\mathbf{x}_0$, taking expectations over all possible training datasets $\mathcal{D}$ and noise realizations $\varepsilon$:

$$\mathbb{E}_{\mathcal{D}, \varepsilon}\left[ \left( y_0 - \hat{f}(\mathbf{x}_0; \mathcal{D}) \right)^2 \right]$$

For notational clarity, let $\hat{f} \equiv \hat{f}(\mathbf{x}_0; \mathcal{D})$ and $f \equiv f(\mathbf{x}_0)$.
Substitute $y_0 = f + \varepsilon$:
$$\mathbb{E}\left[ (y_0 - \hat{f})^2 \right] = \mathbb{E}\left[ (f + \varepsilon - \hat{f})^2 \right] = \mathbb{E}\left[ ((f - \hat{f}) + \varepsilon)^2 \right]$$

Expanding the quadratic square:
$$\mathbb{E}\left[ ((f - \hat{f}) + \varepsilon)^2 \right] = \mathbb{E}\left[ (f - \hat{f})^2 \right] + 2 \mathbb{E}[(f - \hat{f}) \varepsilon] + \mathbb{E}[\varepsilon^2]$$

Because noise $\varepsilon$ is independent of $\mathcal{D}$ (and therefore independent of $\hat{f}$), and $\mathbb{E}[\varepsilon] = 0$:
$$\mathbb{E}[(f - \hat{f}) \varepsilon] = \mathbb{E}[f - \hat{f}] \cdot \mathbb{E}[\varepsilon] = 0$$
and since $\mathbb{E}[\varepsilon^2] = \text{Var}(\varepsilon) + (\mathbb{E}[\varepsilon])^2 = \sigma^2$:
$$\mathbb{E}\left[ (y_0 - \hat{f})^2 \right] = \mathbb{E}\left[ (f - \hat{f})^2 \right] + \sigma^2$$

Now, examine the first term $\mathbb{E}[(f - \hat{f})^2]$. Add and subtract the expected model prediction $\mathbb{E}[\hat{f}]$ inside the parenthesis:
$$\mathbb{E}\left[ (f - \hat{f})^2 \right] = \mathbb{E}\left[ \left( (f - \mathbb{E}[\hat{f}]) + (\mathbb{E}[\hat{f}] - \hat{f}) \right)^2 \right]$$

Expanding this quadratic term:
$$\mathbb{E}\left[ (f - \mathbb{E}[\hat{f}])^2 \right] + 2 \mathbb{E}\left[ (f - \mathbb{E}[\hat{f}]) (\mathbb{E}[\hat{f}] - \hat{f}) \right] + \mathbb{E}\left[ (\mathbb{E}[\hat{f}] - \hat{f})^2 \right]$$

Evaluate each of the three terms:
1. $(f - \mathbb{E}[\hat{f}])$ is a deterministic constant (not a random variable). Thus:
   $$\mathbb{E}\left[ (f - \mathbb{E}[\hat{f}])^2 \right] = (f - \mathbb{E}[\hat{f}])^2 = \left( \mathbb{E}[\hat{f}] - f \right)^2 \equiv \mathbf{Bias}^2(\hat{f})$$
2. The cross-term: Pull the constant $(f - \mathbb{E}[\hat{f}])$ outside the expectation:
   $$2 (f - \mathbb{E}[\hat{f}]) \cdot \mathbb{E}[\mathbb{E}[\hat{f}] - \hat{f}] = 2 (f - \mathbb{E}[\hat{f}]) \cdot (\mathbb{E}[\hat{f}] - \mathbb{E}[\hat{f}]) = 0$$
3. The third term is the exact mathematical definition of the **Variance** of the estimator:
   $$\mathbb{E}\left[ (\hat{f} - \mathbb{E}[\hat{f}])^2 \right] \equiv \mathbf{Var}(\hat{f})$$

Assembling the terms yields the **Master Bias-Variance Equation**:
$$\mathbb{E}_{\mathcal{D}, \varepsilon}\left[ (y_0 - \hat{f}(\mathbf{x}_0))^2 \right] = \underbrace{\left( \mathbb{E}[\hat{f}(\mathbf{x}_0)] - f(\mathbf{x}_0) \right)^2}_{\mathbf{Bias}^2} + \underbrace{\mathbb{E}\left[ (\hat{f}(\mathbf{x}_0) - \mathbb{E}[\hat{f}(\mathbf{x}_0)])^2 \right]}_{\mathbf{Variance}} + \underbrace{\sigma^2}_{\mathbf{Irreducible \, Noise}}$$

---

### 6.3 Pedagogical Anatomy of the Three Components

```
                   The Three Pillars of Generalization Error
  +--------------------+---------------------+----------------------------------+
  | Squared Bias       | Model Variance      | Irreducible Bayes Noise (sigma^2)|
  +--------------------+---------------------+----------------------------------+
  | Source: Rigid or   | Source: Sensitivity | Source: Physical randomness,     |
  | erroneous model    | to random sample    | unobserved variables, sensor     |
  | assumptions        | variations in D     | imprecision                      |
  | Controllable? YES  | Controllable? YES   | Controllable? NO (Theoretical    |
  |                    |                     | error lower bound)               |
  +--------------------+---------------------+----------------------------------+
```

1. **Bias ($\text{Bias}(\hat{f})$)**:
   Measures how far the **average model prediction** across infinitely many different training datasets deviates from the true target function $f(\mathbf{x})$. A straight line fitted to a quadratic curve has massive bias because no matter how much data you feed it, its average prediction is flatly wrong.
2. **Variance ($\text{Var}(\hat{f})$)**:
   Measures how much the predictions of $\hat{f}$ **fluctuate** across different random draws of training data $\mathcal{D}$. An overfitted degree-25 polynomial has massive variance: add or delete two training points, and the fitted curve twists into a completely different shape.
3. **Irreducible Error ($\sigma^2$)**:
   The fundamental entropy of the physical universe. No model—even an all-knowing oracle with infinite capacity—can achieve an expected error lower than $\sigma^2$."""
        },
        {
            "section_id": "cml-l06-sec07",
            "heading": "7. Visualizing Bias and Variance: The Dartboard Analogy & Optimum Complexity Identification",
            "citations": [
                "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning. Springer."
            ],
            "body": r"""### 7.1 The Classical Dartboard Analogy

To build indelible mental intuition for the interplay of Bias and Variance, consider a marksman firing a sequence of darts at a target bullseye:
- The **bullseye** represents the true function value $f(\mathbf{x}_0)$.
- Each individual **dart impact** represents the prediction of a model trained on an independent dataset $\mathcal{D}_k$.

```
                              The Bias-Variance Dartboard
 
        Low Variance                     High Variance
     +--------------------------+     +--------------------------+
     |        ( )               |     |       *                  |
     |       ( * )  Low Bias    |     |      ( )   *   Low Bias  |
     |        ( )   (Ideal)     |     |     (* )*  *             |
     |                          |     |    *  ( )       *        |
     +--------------------------+     +--------------------------+
      All shots grouped tightly        Shots centered on bullseye
      inside the bullseye              on average, but wildly scattered
 
     +--------------------------+     +--------------------------+
     | * *                      |     |  *             *         |
     |* *   ( )     High Bias   |     |       ( )      High Bias |
     | *   ( * )                |     |      ( * )               |
     |      ( )                 |     |   *       *    *         |
     +--------------------------+     +--------------------------+
      All shots grouped tightly,       Shots widely scattered AND
      but systematically off-center    systematically off-target (Worst)
```

#### Mapping Models to Dartboards:
- **Low Bias, Low Variance (Top-Left)**: The Holy Grail. The optimal polynomial degree $d^*$. Every trained model lands right on target with high consistency.
- **Low Bias, High Variance (Top-Right)**: Overfitting (Degree 25). If you average 10,000 models, their mean prediction is centered near the bullseye, but any *individual* model you deploy in production is wildly off-target.
- **High Bias, Low Variance (Bottom-Left)**: Underfitting (Degree 1). The model is exceptionally consistent and repeatable, but consistently and reliably wrong.
- **High Bias, High Variance (Bottom-Right)**: Pathological failure. The model class is mis-specified and hypersensitive to noise simultaneously."""
        },
        {
            "section_id": "cml-l06-sec08",
            "heading": "8. Numerical & Practical Pitfalls: Multicollinearity in Powers, Vandermonde Ill-Conditioning & Feature Scaling",
            "citations": [
                "Golub, G. H., & Van Loan, C. F. (2013). Matrix Computations (4th ed.). Johns Hopkins University Press.",
                "Higham, N. J. (2002). Accuracy and Stability of Numerical Algorithms. SIAM."
            ],
            "body": r"""### 8.1 The Vandermonde Matrix and Catastrophic Ill-Conditioning

When we construct a polynomial design matrix for a scalar feature $x \in \mathbb{R}$, we generate a **Vandermonde Matrix** $\boldsymbol{\Phi} \in \mathbb{R}^{m \times (d+1)}$:

$$\boldsymbol{\Phi} = \begin{bmatrix}
1 & x_1 & x_1^2 & x_1^3 & \dots & x_1^d \\
1 & x_2 & x_2^2 & x_2^3 & \dots & x_2^d \\
\vdots & \vdots & \vdots & \vdots & \ddots & \vdots \\
1 & x_m & x_m^2 & x_m^3 & \dots & x_m^d
\end{bmatrix}$$

In numerical linear algebra, the Vandermonde matrix is notorious for being **exponentially ill-conditioned**:

#### 1. Dynamic Range Explosion
Suppose an input feature has values around $x = 10$.
- For degree $d = 1$, $x^1 = 10$.
- For degree $d = 8$, $x^8 = 100,000,000$.
- For degree $d = 16$, $x^{16} = 10^{16}$.
The numbers in column 16 dwarf the numbers in column 1 by sixteen orders of magnitude! In standard 64-bit IEEE 754 floating-point arithmetic (which has 53 bits of mantissa, providing roughly 15 to 17 decimal digits of precision), adding or inverting matrices with dynamic ranges exceeding $10^{16}$ results in complete loss of significance (**catastrophic cancellation**).

#### 2. Severe Structural Multicollinearity
The columns $x, x^2, x^3, \dots, x^d$ are mathematically deterministic functions of one another. On any positive interval $[a, b]$ where $a > 0$:
- Correlation $\text{Corr}(x, x^2) > 0.95$.
- Correlation $\text{Corr}(x^2, x^3) > 0.99$.
As proved in Lecture 4, near-collinear columns cause the Gram matrix $\boldsymbol{\Phi}^T \boldsymbol{\Phi}$ to have eigenvalues approaching zero ($\lambda_{\min} \to 0$). The condition number $\kappa(\boldsymbol{\Phi}^T \boldsymbol{\Phi}) = \frac{\lambda_{\max}}{\lambda_{\min}}$ explodes to $10^{14}$ or higher, making matrix inversion numerically unstable.

---

### 8.2 Production Remedy: Pipeline Standardization

To prevent numerical collapse when using polynomial features:
1. **Never fit polynomial features on raw, unscaled data**.
2. **Apply `StandardScaler` after polynomial expansion** (or use orthogonal polynomials such as Chebyshev polynomials).
3. **Caps on Degree**: Restrict polynomial degree to $d \le 3$ or $4$ in tabular production pipelines; for higher non-linearities, transition to non-linear tree ensembles (Random Forests, Gradient Boosting) or spline regression."""
        },
        {
            "section_id": "cml-l06-sec09",
            "heading": "9. Industrial Implementation: Scikit-Learn PolynomialFeatures, Pipelines & Model Selection Diagnostics",
            "citations": [
                "Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830."
            ],
            "body": r"""### 9.1 Building a Production Polynomial Pipeline in Scikit-Learn

Below is a complete, leakage-free Scikit-Learn workflow for tuning polynomial regression using `Pipeline`, `PolynomialFeatures`, `StandardScaler`, and validation curves:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# 1. Generate synthetic non-linear ground truth: y = 0.5*x^3 - 1.2*x^2 + 0.8*x + noise
np.random.seed(42)
m = 100
X = np.sort(np.random.uniform(-2, 3, size=(m, 1)), axis=0)
y_true = 0.5 * X**3 - 1.2 * X**2 + 0.8 * X + 1.0
noise = np.random.normal(0, 1.2, size=(m, 1))
y = (y_true + noise).ravel()

# 2. Strict Train-Test Partition (Leakage Prevention)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# 3. Helper: Compute Adjusted R-squared
def adjusted_r2(r2, n_samples, n_features):
    numerator = (1 - r2) * (n_samples - 1)
    denominator = n_samples - n_features - 1
    if denominator <= 0:
        return np.nan
    return 1 - (numerator / denominator)

# 4. Sweep Polynomial Degrees 1 through 15
degrees = list(range(1, 16))
train_mse_list = []
test_mse_list = []
adj_r2_train_list = []

for d in degrees:
    # Build atomic pipeline: Expansion -> Scaling -> OLS Solver
    pipe = Pipeline([
        ("poly", PolynomialFeatures(degree=d, include_bias=False)),
        ("scaler", StandardScaler()),
        ("model", LinearRegression())
    ])
    
    pipe.fit(X_train, y_train)
    
    # Evaluate
    y_pred_train = pipe.predict(X_train)
    y_pred_test = pipe.predict(X_test)
    
    train_mse = mean_squared_error(y_train, y_pred_train)
    test_mse = mean_squared_error(y_test, y_pred_test)
    r2_tr = r2_score(y_train, y_pred_train)
    
    train_mse_list.append(train_mse)
    test_mse_list.append(test_mse)
    adj_r2_train_list.append(adjusted_r2(r2_tr, len(y_train), d))

# 5. Diagnostic Summary
best_degree = degrees[np.argmin(test_mse_list)]
print(f"Optimal Degree by Holdout Test MSE: Degree {best_degree}")
print(f"Degree 1 (Underfit)  -> Train MSE: {train_mse_list[0]:.4f}, Test MSE: {test_mse_list[0]:.4f}")
print(f"Degree {best_degree} (Optimal)    -> Train MSE: {train_mse_list[best_degree-1]:.4f}, Test MSE: {test_mse_list[best_degree-1]:.4f}")
print(f"Degree 15 (Overfit)  -> Train MSE: {train_mse_list[-1]:.4f}, Test MSE: {test_mse_list[-1]:.4f}")
```

---

### 9.2 Summary Takeaways for Enterprise Practitioners

1. **Feature Engineering Supremacy**: Polynomial regression transforms non-linear relationships into linear parameter estimation without sacrificing convexity.
2. **Never Trust Raw Training $R^2$**: Raw $R^2$ is mathematically incapable of penalizing complexity; always evaluate models via Adjusted $R^2$ or holdout cross-validation.
3. **Respect Occam's Razor**: If Degree 2 and Degree 4 produce comparable test errors, deploy Degree 2.
4. **Guard Against Vandermonde Explosion**: Never use raw polynomials of high degree without standardization; for high non-linearity, prefer spline bases or ensemble trees."""
        }
    ],
    "quiz": {
        "title": "Comprehensive Examination: Polynomial Regression & The Bias-Variance Tradeoff",
        "description": "25-question examination testing polynomial bases, linear-in-parameters properties, Adjusted vs. Raw R^2, Occam's Razor, analytical Bias-Variance-Noise decomposition, underfitting/overfitting diagnostics, Vandermonde ill-conditioning, and Scikit-Learn pipelines.",
        "time_limit": "30 mins",
        "questions": [
            {
                "id": "q-cml-l06-01",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Definition of Polynomial Degree",
                "question": "In polynomial regression, what does the 'degree' of the polynomial represent?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "The total number of training observations in the dataset"
                    },
                    {
                        "id": "opt-b",
                        "text": "The highest exponent power of the input feature in the polynomial equation"
                    },
                    {
                        "id": "opt-c",
                        "text": "The number of hidden layers in the regression model"
                    },
                    {
                        "id": "opt-d",
                        "text": "The learning rate multiplier used during gradient descent"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "The degree d of a polynomial is defined as the highest power of the variable present in the mathematical formulation (e.g., in w_0 + w_1 x + w_2 x^2 + w_3 x^3, the degree is 3)."
            },
            {
                "id": "q-cml-l06-02",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Linear in Parameters",
                "question": "Why is polynomial regression categorized as a 'linear model' even though its prediction curve is non-linear in feature space?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Because it only produces straight-line predictions on the test set"
                    },
                    {
                        "id": "opt-b",
                        "text": "Because the model is strictly linear with respect to its unknown parameter weights w"
                    },
                    {
                        "id": "opt-c",
                        "text": "Because the target variable y must follow a uniform distribution"
                    },
                    {
                        "id": "opt-d",
                        "text": "Because it uses linear activation functions inside a neural network"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "A model is classified as linear if its prediction equation is a linear combination of its parameters w: y_hat = sum w_j * phi_j(x). Because the weights enter linearly, the loss function remains convex quadratic."
            },
            {
                "id": "q-cml-l06-03",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Occam's Razor Definition",
                "question": "How does Occam's Razor (Lex Parsimoniae) apply to machine learning model selection?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Always select the model with the largest number of parameters to maximize learning capacity"
                    },
                    {
                        "id": "opt-b",
                        "text": "Among competing models that achieve equivalent generalization performance, prefer the simpler model"
                    },
                    {
                        "id": "opt-c",
                        "text": "Always select the model that achieves exactly zero training error"
                    },
                    {
                        "id": "opt-d",
                        "text": "Discard half of the dataset randomly before model fitting"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "Occam's Razor dictates that entities should not be multiplied beyond necessity. In machine learning, if a degree-2 and degree-5 model achieve similar test error, the simpler degree-2 model is preferred for robustness and parsimony."
            },
            {
                "id": "q-cml-l06-04",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Symptoms of Underfitting",
                "question": "Which of the following characterizes an underfitted model?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Extremely low training error, but catastrophically high test error"
                    },
                    {
                        "id": "opt-b",
                        "text": "High training error and high test error because the model is too simple to capture the underlying pattern"
                    },
                    {
                        "id": "opt-c",
                        "text": "High variance and low bias"
                    },
                    {
                        "id": "opt-d",
                        "text": "Adjusted R^2 equal to exactly 1.0"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "Underfitting occurs when a model lacks expressive capacity (high bias), leading to poor performance (high error) on both the training set and unseen test data."
            },
            {
                "id": "q-cml-l06-05",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Symptoms of Overfitting",
                "question": "Which of the following characterizes an overfitted model?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "High training error and low test error"
                    },
                    {
                        "id": "opt-b",
                        "text": "Exceptionally low training error, but high test error because the model has memorized noise"
                    },
                    {
                        "id": "opt-c",
                        "text": "High bias and low variance"
                    },
                    {
                        "id": "opt-d",
                        "text": "The model line is a flat horizontal line at the sample mean"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "Overfitting occurs when an overly complex model fits random fluctuations and noise in the training set, causing train error to plummet while test error on new data degrades severely."
            },
            {
                "id": "q-cml-l06-06",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Bias-Variance Dartboard Analogy",
                "question": "In the classical dartboard analogy for Bias and Variance, what does an overfitted model correspond to?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "All darts grouped tightly together, but centered far away from the bullseye"
                    },
                    {
                        "id": "opt-b",
                        "text": "Darts widely scattered across the board, but centered on the bullseye on average (Low Bias, High Variance)"
                    },
                    {
                        "id": "opt-c",
                        "text": "All darts perfectly clustered inside the bullseye"
                    },
                    {
                        "id": "opt-d",
                        "text": "Zero darts hitting the board"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "An overfitted model has Low Bias (on average across infinite datasets it centers near the target) but High Variance (any single model realization scatters wildly across the target space)."
            },
            {
                "id": "q-cml-l06-07",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Irreducible Error",
                "question": "In the Bias-Variance decomposition E[(y - y_hat)^2] = Bias^2 + Variance + sigma^2, what does sigma^2 represent?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "The variance of the gradient updates during SGD"
                    },
                    {
                        "id": "opt-b",
                        "text": "The irreducible error (Bayes noise) inherent to the physical environment or unobserved latent factors"
                    },
                    {
                        "id": "opt-c",
                        "text": "The penalty hyperparameter for L1 Lasso regularization"
                    },
                    {
                        "id": "opt-d",
                        "text": "The degree of the polynomial minus one"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "sigma^2 represents the irreducible noise in the target generation process y = f(x) + epsilon. No model, regardless of capacity or data volume, can reduce error below sigma^2."
            },
            {
                "id": "q-cml-l06-08",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Scikit-Learn Class for Polynomials",
                "question": "Which Scikit-Learn transformer class is used to generate polynomial and interaction features from input arrays?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "StandardScaler"
                    },
                    {
                        "id": "opt-b",
                        "text": "PolynomialFeatures"
                    },
                    {
                        "id": "opt-c",
                        "text": "FeatureUnion"
                    },
                    {
                        "id": "opt-d",
                        "text": "VarianceThreshold"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "sklearn.preprocessing.PolynomialFeatures constructs powers (x^2, x^3) and cross-feature interaction terms (x1*x2) up to the specified degree."
            },
            {
                "id": "q-cml-l06-09",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Raw R^2 Flaw",
                "question": "Why is it mathematically flawed to select the polynomial degree based on the highest raw R^2 score on the training dataset?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Because raw R^2 is undefined for non-linear models"
                    },
                    {
                        "id": "opt-b",
                        "text": "Because raw training R^2 is monotonically non-decreasing with respect to degree, always favoring the most overfitted model"
                    },
                    {
                        "id": "opt-c",
                        "text": "Because raw R^2 can never exceed 0.5 on polynomial features"
                    },
                    {
                        "id": "opt-d",
                        "text": "Because raw R^2 measures correlation rather than mean squared error"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "Adding polynomial powers can never increase residual sum of squares on training data. Thus raw training R^2 monotonically climbs toward 1.0, invariably selecting the highest, most overfitted degree."
            },
            {
                "id": "q-cml-l06-10",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Adjusted R^2 Mechanics",
                "question": "In the formula for Adjusted R^2, R^2_{adj} = 1 - (1 - R^2) \\frac{m - 1}{m - p - 1}, what does p represent when evaluating polynomial regression?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "The p-value of the F-test"
                    },
                    {
                        "id": "opt-b",
                        "text": "The total number of transformed features used by the model (columns after polynomial expansion)"
                    },
                    {
                        "id": "opt-c",
                        "text": "The original number of raw features before transformation"
                    },
                    {
                        "id": "opt-d",
                        "text": "The proportion of test samples in train_test_split"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "In Adjusted R^2, p is the total number of explanatory features fitted in the design matrix (excluding the intercept), which corresponds to the expanded column count after PolynomialFeatures."
            },
            {
                "id": "q-cml-l06-11",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Adjusted R^2 vs Raw R^2 Behavior",
                "question": "If an extra polynomial power x^4 is added to a regression model and it explains only trivial random noise on the training set, what will happen to raw R^2 and Adjusted R^2?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Both raw R^2 and Adjusted R^2 will decrease"
                    },
                    {
                        "id": "opt-b",
                        "text": "Raw R^2 will stay constant or slightly increase, while Adjusted R^2 will actively decrease"
                    },
                    {
                        "id": "opt-c",
                        "text": "Raw R^2 will drop to zero, while Adjusted R^2 will increase"
                    },
                    {
                        "id": "opt-d",
                        "text": "Both metrics will remain completely unchanged"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "Raw R^2 will increase slightly due to fitting random noise. However, the degrees-of-freedom penalty multiplier (m-1)/(m-p-1) increases; if error reduction does not outweigh this penalty, Adjusted R^2 drops."
            },
            {
                "id": "q-cml-l06-12",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Multicollinearity in Polynomial Terms",
                "question": "Why do high-degree polynomial models (e.g., degree >= 4) naturally exhibit extreme multicollinearity?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Because polynomial features violate the Gauss-Markov linearity assumption"
                    },
                    {
                        "id": "opt-b",
                        "text": "Because powers of the same feature (x, x^2, x^3) are inherently strongly correlated with each other across positive intervals"
                    },
                    {
                        "id": "opt-c",
                        "text": "Because Scikit-Learn introduces duplicate columns during expansion"
                    },
                    {
                        "id": "opt-d",
                        "text": "Because the gradient descent learning rate is too large"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "Features x, x^2, x^3 are deterministic powers of the same variable. On positive domains, they move monotonically together, resulting in pairwise correlations often exceeding 0.95 and high VIF values."
            },
            {
                "id": "q-cml-l06-13",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Interaction Features Count",
                "question": "For a dataset with 2 continuous features x_1 and x_2, what is the exact output of PolynomialFeatures(degree=2, include_bias=True)?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "[x_1, x_2, x_1^2, x_2^2]"
                    },
                    {
                        "id": "opt-b",
                        "text": "[1, x_1, x_2, x_1^2, x_1 x_2, x_2^2] (total 6 features)"
                    },
                    {
                        "id": "opt-c",
                        "text": "[1, x_1, x_2, x_1^2, x_2^2] (total 5 features)"
                    },
                    {
                        "id": "opt-d",
                        "text": "[1, x_1 x_2]"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "A complete degree-2 expansion includes the intercept (1), linear terms (x1, x2), pure quadratic terms (x1^2, x2^2), and cross interaction term (x1*x2), totaling 6 features: (2+2)!/(2!*2!) = 6."
            },
            {
                "id": "q-cml-l06-14",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Diagnostic Performance Interpretation",
                "question": "A model evaluated on a real-world dataset yields Train MSE = 0.035 and Test MSE = 0.038. How should this model be classified?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Severely overfitted"
                    },
                    {
                        "id": "opt-b",
                        "text": "Severely underfitted"
                    },
                    {
                        "id": "opt-c",
                        "text": "Well-generalized and balanced fit"
                    },
                    {
                        "id": "opt-d",
                        "text": "Defective due to data leakage"
                    }
                ],
                "correct_answer": "opt-c",
                "explanation": "Train and test errors are both low and virtually identical (0.035 vs 0.038), indicating low bias and low variance—the hallmark of a well-generalized model."
            },
            {
                "id": "q-cml-l06-15",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Bias and Variance Trends with Complexity",
                "question": "As model complexity (polynomial degree d) increases, what are the characteristic trajectories of Bias and Variance?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Bias increases monotonically, while Variance decreases monotonically"
                    },
                    {
                        "id": "opt-b",
                        "text": "Bias decreases monotonically, while Variance increases monotonically"
                    },
                    {
                        "id": "opt-c",
                        "text": "Both Bias and Variance decrease monotonically toward zero"
                    },
                    {
                        "id": "opt-d",
                        "text": "Both Bias and Variance increase monotonically toward infinity"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "As degree increases, model capacity expands: the model can fit more complex shapes, reducing Bias. However, it becomes increasingly sensitive to training sample fluctuations, driving Variance up."
            },
            {
                "id": "q-cml-l06-16",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Adjusted R^2 Undefined Condition",
                "question": "Under what condition does Adjusted R^2 become mathematically undefined or singular?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "When the training sample size m exceeds 1,000,000"
                    },
                    {
                        "id": "opt-b",
                        "text": "When the number of features p equals or exceeds m - 1 (residual degrees of freedom <= 0)"
                    },
                    {
                        "id": "opt-c",
                        "text": "When raw R^2 is greater than 0.90"
                    },
                    {
                        "id": "opt-d",
                        "text": "When all weights w are positive"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "The denominator in Adjusted R^2 is (m - p - 1). When p >= m - 1, the denominator is zero or negative, indicating zero residual degrees of freedom (exact interpolation), making Adjusted R^2 undefined."
            },
            {
                "id": "q-cml-l06-17",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Pipeline Leakage Prevention",
                "question": "Why should PolynomialFeatures and StandardScaler always be wrapped inside a Scikit-Learn Pipeline rather than executed on the full dataset before splitting?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "To prevent data leakage by ensuring scaling statistics (mean and variance) are calculated exclusively from the training fold"
                    },
                    {
                        "id": "opt-b",
                        "text": "Because PolynomialFeatures cannot process NumPy arrays directly"
                    },
                    {
                        "id": "opt-c",
                        "text": "To automatically convert regression into classification"
                    },
                    {
                        "id": "opt-d",
                        "text": "To force the learning rate to decay exponentially"
                    }
                ],
                "correct_answer": "opt-a",
                "explanation": "Wrapping transformers in a Pipeline guarantees that StandardScaler.fit() only computes statistics from X_train, preventing out-of-sample data leakage into the evaluation folds."
            },
            {
                "id": "q-cml-l06-18",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Mathematical Proof of Cross-Terms",
                "question": "In the derivation of E[(y - y_hat)^2], why does the cross-term 2 * E[(f(x) - y_hat) * epsilon] vanish to exactly 0?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Because f(x) is assumed to be identically equal to y_hat at all points"
                    },
                    {
                        "id": "opt-b",
                        "text": "Because the noise epsilon is statistically independent of the training dataset D, and E[epsilon] = 0"
                    },
                    {
                        "id": "opt-c",
                        "text": "Because the derivative of the loss function is zero at the minimum"
                    },
                    {
                        "id": "opt-d",
                        "text": "Because the Hessian matrix is symmetric"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "By definition, the test sample noise epsilon is independent of the training dataset D that generated y_hat. Thus E[(f - y_hat)*epsilon] = E[f - y_hat] * E[epsilon]. Since E[epsilon] = 0, the entire expectation is zero."
            },
            {
                "id": "q-cml-l06-19",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Numerical Calculation of Adjusted R^2",
                "question": "A dataset contains m = 51 training samples. A model with raw features is expanded to p = 10 polynomial features, achieving raw training R^2 = 0.80. What is the value of Adjusted R^2?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "0.75"
                    },
                    {
                        "id": "opt-b",
                        "text": "0.70"
                    },
                    {
                        "id": "opt-c",
                        "text": "0.82"
                    },
                    {
                        "id": "opt-d",
                        "text": "0.65"
                    }
                ],
                "correct_answer": "opt-a",
                "explanation": "R^2_adj = 1 - (1 - R^2) * (m - 1) / (m - p - 1) = 1 - (1 - 0.80) * (51 - 1) / (51 - 10 - 1) = 1 - 0.20 * (50 / 40) = 1 - 0.20 * 1.25 = 1 - 0.25 = 0.75."
            },
            {
                "id": "q-cml-l06-20",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Vandermonde Matrix Condition Number",
                "question": "What is the primary numerical failure mechanism when inverting a high-degree Vandermonde design matrix Phi without feature scaling?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "The matrix entries become non-differentiable integers"
                    },
                    {
                        "id": "opt-b",
                        "text": "The dynamic range between column 1 (x^0) and column d (x^d) exceeds IEEE 754 float precision (10^16), causing singular condition numbers and catastrophic cancellation"
                    },
                    {
                        "id": "opt-c",
                        "text": "The eigenvalues become imaginary complex numbers"
                    },
                    {
                        "id": "opt-d",
                        "text": "The rank of the matrix permanently drops to 1"
                    }
                ],
                "correct_answer": "opt-b",
                "explanation": "Vandermonde columns grow exponentially x^d. When values exceed 10^16, float64 precision limits are exhausted, rendering (Phi^T Phi) numerically singular and generating garbage weights with magnitudes like 10^12."
            },
            {
                "id": "q-cml-l06-21",
                "type": "multi_choice",
                "difficulty": "hard",
                "subtopic": "Remediating Overfitting in High Degrees",
                "question": "Which of the following techniques are mathematically valid strategies to mitigate overfitting in polynomial regression without completely reverting to degree 1?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Applying L2 regularization (Ridge Regression) to penalize exploding weight magnitudes"
                    },
                    {
                        "id": "opt-b",
                        "text": "Applying L1 regularization (Lasso Regression) to enforce sparsity and zero out unnecessary polynomial terms"
                    },
                    {
                        "id": "opt-c",
                        "text": "Acquiring significantly more training observations (increasing m) to constrain variance"
                    },
                    {
                        "id": "opt-d",
                        "text": "Multiplying all target y values by 1,000"
                    }
                ],
                "correct_answer": ["opt-a", "opt-b", "opt-c"],
                "explanation": "L2 regularization prevents parameter explosion, L1 conducts feature selection by zeroing powers, and increasing m reduces estimator variance. Scaling target values (D) does not reduce overfitting."
            },
            {
                "id": "q-cml-l06-22",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Effect of Infinite Data on Error",
                "question": "As the training sample size m approaches infinity (m -> infinity), what happens to the Bias and Variance components of a model with a fixed, rigid hypothesis class (e.g., degree 1 on a quadratic curve)?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Variance approaches zero, but Squared Bias remains strictly positive and non-zero"
                    },
                    {
                        "id": "opt-b",
                        "text": "Both Squared Bias and Variance approach zero"
                    },
                    {
                        "id": "opt-c",
                        "text": "Variance approaches infinity, while Bias approaches zero"
                    },
                    {
                        "id": "opt-d",
                        "text": "Both Squared Bias and Variance remain unchanged"
                    }
                ],
                "correct_answer": "opt-a",
                "explanation": "With infinite data, sample variance vanishes: Var(y_hat) -> 0. However, if the model class is fundamentally misspecified (straight line on a curve), Bias^2 = (E[y_hat] - f(x))^2 remains stubbornly non-zero."
            },
            {
                "id": "q-cml-l06-23",
                "type": "multi_choice",
                "difficulty": "hard",
                "subtopic": "Adjusted R^2 Mathematical Properties",
                "question": "Which of the following statements regarding Adjusted R^2 are mathematically TRUE?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Adjusted R^2 is strictly less than or equal to raw R^2 (R^2_{adj} <= R^2) for any model with p >= 1"
                    },
                    {
                        "id": "opt-b",
                        "text": "Adjusted R^2 can take negative values if the model fits worse than the horizontal mean line"
                    },
                    {
                        "id": "opt-c",
                        "text": "Adjusted R^2 guarantees that the model will have zero out-of-sample test error"
                    },
                    {
                        "id": "opt-d",
                        "text": "Unlike raw R^2, Adjusted R^2 can decrease when a new feature is added to the model"
                    }
                ],
                "correct_answer": ["opt-a", "opt-b", "opt-d"],
                "explanation": "A is true because (m-1)/(m-p-1) > 1 when p >= 1; B is true because poor models can produce negative values; D is true because worthless features incur a penalty that outweighs error reduction. C is false."
            },
            {
                "id": "q-cml-l06-24",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Model Selection Trade-off",
                "question": "Suppose Model A has Bias^2 = 0.05, Variance = 0.08, and sigma^2 = 0.02. Model B has Bias^2 = 0.01, Variance = 0.15, and sigma^2 = 0.02. Which model achieves lower expected generalization error?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Model A (Expected Error = 0.15), which is lower than Model B (Expected Error = 0.18)"
                    },
                    {
                        "id": "opt-b",
                        "text": "Model B (Expected Error = 0.16), which is lower than Model A (Expected Error = 0.17)"
                    },
                    {
                        "id": "opt-c",
                        "text": "Both models have identical expected error"
                    },
                    {
                        "id": "opt-d",
                        "text": "Cannot be determined without knowing the training sample size"
                    }
                ],
                "correct_answer": "opt-a",
                "explanation": "Expected Error = Bias^2 + Variance + sigma^2. For Model A: 0.05 + 0.08 + 0.02 = 0.15. For Model B: 0.01 + 0.15 + 0.02 = 0.18. Model A achieves lower total expected error despite having higher bias."
            },
            {
                "id": "q-cml-l06-25",
                "type": "multi_choice",
                "difficulty": "hard",
                "subtopic": "Polynomial Expansion Risks",
                "question": "Which of the following are practical engineering hazards when deploying high-degree polynomial regression in production environments?",
                "options": [
                    {
                        "id": "opt-a",
                        "text": "Runaway feature explosion when expanding multivariate inputs (combinatorics: binom(k+d, d))"
                    },
                    {
                        "id": "opt-b",
                        "text": "Severe numerical instability and loss of floating-point precision in matrix inversion"
                    },
                    {
                        "id": "opt-c",
                        "text": "Catastrophic extrapolation errors outside the training feature range [x_min, x_max]"
                    },
                    {
                        "id": "opt-d",
                        "text": "The optimization problem becoming non-convex with millions of local minima"
                    }
                ],
                "correct_answer": ["opt-a", "opt-b", "opt-c"],
                "explanation": "A, B, and C are major hazards of high-degree polynomials (Runaway combinatorial growth, Vandermonde ill-conditioning, and wild extrapolation swings at the boundaries like Runge's phenomenon). D is FALSE: polynomial regression remains strictly convex in weights w."
            }
        ]
    }
}
