# 4. Linear Regression Assumptions, Residual Diagnostics & Multicollinearity
**Term:** Term 5 | **Subject:** CML | **Note ID:** `cml-t5-l04`
**Last Updated:** 2026-10-16T00:00:00Z

## Abstract & Summary
An exhaustive, rigorous masterclass on Linear Regression assumptions and diagnostic validation. Covers the crucial divide between predictive accuracy and statistical inference, the full LINE+ Gauss-Markov framework, residual analysis geometry, statistical hypothesis tests (Breusch-Pagan, Durbin-Watson, Jarque-Bera), mathematical derivation and interpretation of Variance Inflation Factor (VIF), influential observation analysis (Leverage and Cook's Distance), and complete hands-on diagnostic workflows in Python.

## Learning Objectives
- 1. Differentiate pure predictive performance (holdout RMSE) from inferential validity and coefficient interpretability.
- 2. Formulate and verify all five classical Gauss-Markov and regression assumptions using the LINE+ framework.
- 3. Conduct comprehensive residual diagnostics using Residuals vs. Fitted, Normal Q-Q, Scale-Location, and Cook's Distance plots.
- 4. Diagnose and remediate non-linearity through feature transformations, splines, and polynomial expansion.
- 5. Detect heteroscedasticity via the Breusch-Pagan test and resolve it using log-target transformations and White robust standard errors.
- 6. Evaluate error autocorrelation in sequential data using the Durbin-Watson statistic.
- 7. Derive the Variance Inflation Factor (VIF) mathematically, quantify multicollinearity inflation on standard errors, and deploy engineering remedies.

## Key Takeaways
- 1. High R^2 or low holdout RMSE does not imply that regression coefficients, p-values, or confidence intervals are valid or trustworthy.
- 2. Classical regression assumptions live on the unobservable population error terms epsilon; we verify them through empirical sample residuals e_i = y_i - y_hat_i.
- 3. The LINE framework mandates: Linearity in parameters, Independence of errors, Normality of residuals, and Equal variance (Homoscedasticity), plus No Multicollinearity.
- 4. Heteroscedasticity (fan-shaped residual variance) does not bias OLS coefficients, but severely biases standard errors, invalidating hypothesis tests; log-transforming y is the primary remediation.
- 5. Under the Central Limit Theorem, normality of residuals is less critical for parameter point estimates in large samples (m > 500), but essential for exact prediction intervals.
- 6. Multicollinearity inflates coefficient variance by factor VIF_j = 1 / (1 - R_j^2); VIF > 5-10 indicates unstable coefficients with erratic signs.
- 7. A single high-leverage outlier can completely pivot an Ordinary Least Squares hyperplane; Cook's Distance D_i quantifies overall parameter shift upon deleting observation i.

---

## 1. Statistical Inference vs. Pure Prediction: Why Assumptions Dictate Model Trust
### 1.1 The Two Operational Objectives of Linear Models

In Lecture 3, we observed that fitting an Ordinary Least Squares (OLS) model produces a set of weights $\\hat{\\boldsymbol{\\theta}}$ that minimize training Mean Squared Error. In machine learning engineering, a model is deployed for one of two distinct objectives:

```
                            +-----------------------------------------------+
                            |          Two Objectives of Modeling           |
                            +-----------------------------------------------+
                                    |                               |
             +----------------------+                               +----------------------+
             |                                                                             |
             v                                                                             v
   [ Pure Predictive Engineering ]                                             [ Statistical Inference & Policy ]
   - Goal: Minimize holdout RMSE / MAE.                                        - Goal: Accurately estimate true beta_j.
   - Question: "What will house price be?"                                     - Question: "How much does income affect price?"
   - Evaluated on unseen test sets.                                            - Evaluated via standard errors, p-values, CIs.
   - Tolerates mild assumption violations                                      - CRUSHED if Gauss-Markov assumptions
     if generalization error is low.                                             are violated (biased SEs, flipped signs).
```

1. **Pure Prediction**: The sole objective is producing accurate point estimates $\\hat{y}$ on unseen holdout observations. If a non-linear or heteroscedastic model achieves low test RMSE, the engineer may accept it for prediction, though diagnostic sanity checks are still recommended.
2. **Statistical Inference & Decision Policy**: The objective is interpreting the learned coefficients $\\hat{\\theta}_j$, conducting hypothesis tests ($H_0: \\theta_j = 0$), constructing $95\\%$ confidence intervals, or making corporate investment decisions based on feature impacts.

---

### 1.2 The Illusion of a High $R^2$

> **The Dangerous Engineering Trap**:
> *"Our model achieved an $R^2$ of $0.85$ on the test set, so the feature coefficients must accurately reflect reality."*
> 
> **Mathematical Reality**: **Completely False.**
> An OLS model can produce an $R^2$ of $0.90$ while suffering from severe heteroscedasticity, omitted variable bias, or multicollinearity. In such cases:
> - True standard errors are underestimated by $200\\% - 500\\%$.
> - Stated $p$-values are statistically meaningless, falsely labeling irrelevant features as 'statistically significant' ($p < 0.001$).
> - Key coefficient signs can invert (e.g., predicting that more bedrooms *decrease* home price due to collinearity with square footage).

---

### 1.3 The Epistemic Core: Errors vs. Residuals

All classical regression assumptions are formulated on the **unobservable true population disturbances** $\\varepsilon_i$:

$$y_i = \\mathbf{x}_i^T \\boldsymbol{\\theta}^* + \\varepsilon_i, \\quad \\varepsilon_i \\sim \\mathcal{N}(0, \\sigma^2)$$

Because the true parameter vector $\\boldsymbol{\\theta}^*$ is forever hidden, we can never directly measure the true errors $\\varepsilon_i$. Instead, we inspect the empirical **sample residuals** $e_i$:

$$e_i = y_i - \\hat{y}_i = y_i - \\mathbf{x}_i^T \\hat{\\boldsymbol{\\theta}}$$

Sample residuals $e_i$ serve as our only observable window into the behavior of the unobservable population errors $\\varepsilon_i$. Residual analysis is the diagnostic language through which we audit model validity.

**Citations & References:**
- Breiman, L. (2001). Statistical modeling: The two cultures. Statistical Science, 16(3), 199-231.
- Shmueli, G. (2010). To explain or to predict? Statistical Science, 25(3), 289-310.
- Greene, W. H. (2018). Econometric Analysis (8th ed.). Pearson.

---

## 2. The LINE Framework & Classical Gauss-Markov Assumptions
### 2.1 The LINE Mnemonic Framework

To verify that an Ordinary Least Squares estimator is theoretically sound, econometricians and machine learning practitioners audit the model against five core assumptions, remembered via the **LINE+** mnemonic:

| Letter | Assumption Name | Mathematical Formulation | Core Meaning in Plain English |
| :---: | :--- | :--- | :--- |
| **L** | **Linearity in Parameters** | $\\mathbb{E}[y \\mid \\mathbf{X}] = \\mathbf{X}\\boldsymbol{\\theta}$ | The true relationship between input features and target expectation is linear in weights $\\boldsymbol{\\theta}$. |
| **I** | **Independence of Errors** | $\\text{Cov}(\\varepsilon_i, \\varepsilon_j \\mid \\mathbf{X}) = 0, \\quad \\forall i \\neq j$ | Observations are independent. No autocorrelation across time, space, or clustered entity groups. |
| **N** | **Normality of Residuals** | $\\varepsilon \\mid \\mathbf{X} \\sim \\mathcal{N}(\\mathbf{0}, \\sigma^2 \\mathbf{I})$ | Error terms are normally distributed. Mandatory for exact small-sample hypothesis tests ($t, F$) and prediction intervals. |
| **E** | **Equal Variance (Homoscedasticity)** | $\\text{Var}(\\varepsilon_i \\mid \\mathbf{X}) = \\sigma^2, \\quad \\forall i$ | Residual dispersion remains constant across all fitted values $\\hat{y}$ and across all feature ranges. |
| **+** | **No Perfect Multicollinearity** | $\\text{rank}(\\mathbf{X}) = d + 1$ | No explanatory feature column is an exact or near-exact linear combination of other feature columns. |

---

### 2.2 The Gauss-Markov Theorem & BLUE Properties

Why are these assumptions revered in mathematical statistics? The answer is formulated in the **Gauss-Markov Theorem**:

> **The Gauss-Markov Theorem**:
> Under the conditions of:
> 1. Linearity: $\\mathbf{y} = \\mathbf{X}\\boldsymbol{\\theta} + \\boldsymbol{\\varepsilon}$
> 2. Zero conditional mean: $\\mathbb{E}[\\boldsymbol{\\varepsilon} \\mid \\mathbf{X}] = \\mathbf{0}$
> 3. Spherical error variance (Homoscedasticity and No Autocorrelation): $\\text{Var}(\\boldsymbol{\\varepsilon} \\mid \\mathbf{X}) = \\sigma^2 \\mathbf{I}_m$
> 4. Full column rank: $\\text{rank}(\\mathbf{X}) = d + 1$
> 
> The Ordinary Least Squares estimator $\\hat{\\boldsymbol{\\theta}} = (\\mathbf{X}^T \\mathbf{X})^{-1} \\mathbf{X}^T \\mathbf{y}$ is the **Best Linear Unbiased Estimator (BLUE)**.

```
What BLUE Mathematically Guarantees:
   - Best: Has the MINIMUM possible sampling variance among all linear estimators.
   - Linear: Parameter estimator is a linear function of target values: theta_hat = C * y.
   - Unbiased: Expected value of theta_hat equals true population parameter: E[theta_hat] = theta*.
   - Estimator: A valid statistical method for approximating ground truth.
```

> **Critical Theoretical Nuance**: Notice that the Gauss-Markov Theorem does **NOT** require Normality (N). OLS is BLUE even if the error distribution is Uniform, Exponential, or Bimodal! Normality is required strictly for computing exact $t$-statistics, $F$-statistics, $p$-values, and confidence intervals.

**Citations & References:**
- Gauss, C. F. (1823). Theoria combinationis observationum erroribus minimis obnoxiae.
- Markov, A. A. (1912). Wahrscheinlichkeitsrechnung. Teubner.

---

## 3. Residual Analysis: The Diagnostic Language of Regression
### 3.1 The Failure of Simple 'Predicted vs. Actual' Plots

A common mistake is evaluating a regression model exclusively by plotting actual targets $y$ against predicted targets $\\hat{y}$. While this plot reveals gross correlation, it **hides severe systematic structural failures**:
- A curved non-linear trend can look deceptively tight around the $y = x$ diagonal.
- Heteroscedastic fan spreads are compressed visually at high values.
- Mild outliers blend into dense point clusters.

```
Predicted vs Actual (Deceptively Acceptable):     Residuals vs Fitted (Reveals Severe U-Shaped Defect):
         y ^                                              e ^
           |             *                                  |      *              *
           |           *                                    |        *          *
           |         *                                      |   ------+---*----+---*--------+--> y_hat
           |       *                                        |           *    *
           |     *                                          |             **
           +----------------------> y_hat                   +----------------------------->
```

---

### 3.2 The Four Core Residual Diagnostic Plots

#### 1. Residuals vs. Fitted Values ($e_i$ vs. $\\hat{y}_i$)
- **What it audits**: Linearity and Equal Variance (Homoscedasticity).
- **Ideal Pattern**: A completely uniform, random horizontal cloud of points scattered symmetrically around the zero line $e = 0$, with constant vertical spread across the entire horizontal range of $\\hat{y}$.
- **Warning Signals**:
  - *Curved parabolic or U-shape*: Violates Linearity.
  - *Funnel / Megaphone shape*: Violates Homoscedasticity.

#### 2. Normal Quantile-Quantile (Q-Q) Plot
- **What it audits**: Normality of residuals.
- **Ideal Pattern**: Residual sample quantiles fall precisely along the 45-degree diagonal reference line.
- **Warning Signals**:
  - *S-shaped curve with ends peeling away from diagonal*: Heavy tails (leptokurtic distribution / outliers).
  - *Systematic upward or downward bow*: Skewed residuals.

#### 3. Scale-Location Plot ($\\sqrt{|\\text{Standardized Residuals}|}$ vs. $\\hat{y}_i$)
- **What it audits**: Homoscedasticity across the fitted range.
- **Ideal Pattern**: A flat, horizontal trend line with randomly scattered points of equal vertical density.
- **Warning Signal**: A steep upward sloping trend line proves that residual spread increases systematically with prediction magnitude.

#### 4. Residuals vs. Leverage / Cook's Distance Plot
- **What it audits**: Identifying highly influential outlier observations that disproportionately dictate model parameters.

**Citations & References:**
- Anscombe, F. J. (1973). Graphs in statistical analysis. The American Statistician, 27(1), 17-21.
- Cook, R. D., & Weisberg, S. (1982). Residuals and Influence in Regression. Chapman & Hall.

---

## 4. Assumption 1 (Linearity): Detection, Polynomial Spanning & Transformations
### 4.1 What Linearity Truly Means in OLS

A frequent point of confusion is the definition of 'linear'. Linear regression requires the model to be **linear in the parameters $\\boldsymbol{\\theta}$**, **not** necessarily linear in the raw input features $\\mathbf{x}$.

$$\\text{Linear Model} \\iff h_{\\boldsymbol{\\theta}}(\\mathbf{x}) = \\sum_{j=0}^d \\theta_j \\phi_j(\\mathbf{x})$$

Where $\\phi_j(\\mathbf{x})$ can be any arbitrary non-linear basis transformation of raw features (e.g., $x_1^2$, $\\log(x_2)$, $\\sin(x_3)$, $x_1 x_2$). As long as the relationship between the transformed features $\\phi(\\mathbf{x})$ and prediction $\\hat{y}$ is additive with scalar weights $\\theta_j$, the optimization problem remains Ordinary Least Squares!

---

### 4.2 Diagnosing Non-Linearity

When the true relationship between an input feature and the target is non-linear (e.g., diminishing returns of income, exponential growth of population), fitting a straight line $y = \\theta_0 + \\theta_1 x$ introduces **systematic structural bias**:

```
Diagnosing Non-Linearity in Residual Plots:
   Fitted Straight Line on Parabolic Data:         Residual Plot Shows Distinct Downward U-Curve:
         y ^                                              e ^
           |             *                                  |          *   *   *
           |          *     *                               |       *             *
           |       *   Line   *                             |   ----+---------------+----+----> y_hat
           |    *        /      *                           |   *                       *
           |  *         /         *                         | *                           *
           +-----------/-------------> x                    +----------------------------->
```

1. **Residuals vs. Fitted**: If the mean residual curve bends in a smooth U-shape or inverted U-shape, the model is failing to capture a non-linear curvature.
2. **Component-Plus-Residual (Partial Residual) Plots**: Plots $e_i + \\hat{\\theta}_j x_{ij}$ against $x_j$. This isolates the specific non-linear shape of feature $x_j$ independent of other model variables.

---

### 4.3 Engineering Remediation Strategies

When non-linearity is detected, an engineer has three primary options:

1. **Non-Linear Feature Transformations**:
   - Logarithmic: $x' = \\log(x)$ (for diminishing returns, power-law features, or exponential decay).
   - Square Root: $x' = \\sqrt{x}$ (for count features or Poisson-like variances).
   - Reciprocal: $x' = 1 / x$ (for rates, speed vs. time).
2. **Polynomial Feature Expansion**:
   $$h_{\\boldsymbol{\\theta}}(x) = \\theta_0 + \\theta_1 x + \\theta_2 x^2 + \\theta_3 x^3$$
   Implemented via Scikit-Learn's `PolynomialFeatures(degree=2, include_bias=False)`.
3. **Spline Transformations / Generalized Additive Models (GAMs)**:
   Dividing the feature domain into intervals via knots and fitting piecewise polynomial splines (`SplineTransformer`).

**Citations & References:**
- Box, G. E., & Cox, D. R. (1964). An analysis of transformations. Journal of the Royal Statistical Society: Series B, 26(2), 211-252.
- Harrell, F. E. (2015). Regression Modeling Strategies (2nd ed.). Springer.

---

## 5. Assumption 2 (Homoscedasticity): The Heteroscedastic Fan, Breusch-Pagan Test & Log Transforms
### 5.1 The Nature of Heteroscedasticity

**Homoscedasticity** (equal scatter) requires that the variance of the error term $\\varepsilon_i$ is constant across all observations, regardless of the values of the input features:

$$\\text{Var}(\\varepsilon_i \\mid \\mathbf{X} = \\mathbf{x}_i) = \\sigma^2 = \\text{constant}, \\quad \\forall i \\in \\{1, \\dots, m\\}$$

**Heteroscedasticity** occurs when error variance is a function of input variables or predicted magnitude: $\\text{Var}(\\varepsilon_i \\mid \\mathbf{X} = \\mathbf{x}_i) = \\sigma_i^2 = f(\\mathbf{x}_i)$.

```
Homoscedasticity (Healthy Constant Band):          Heteroscedasticity (Classic Fan / Megaphone):
         e ^                                              e ^
           |   *   *   *   *   *   *                        |                 *     *     *
           |     *   *   *   *   *                          |            *       *       *
        ---+-----------------------+--> y_hat            ---+-------*-----------*-----+---> y_hat
           |     *   *   *   *   *                          |            *       *       *
           |   *   *   *   *   *   *                        |                 *     *     *
           +--------------------------->                    +----------------------------->
         Constant vertical width: sigma^2                 Variance explodes as y_hat increases
```

#### Why Heteroscedasticity Occurs in Practice
- **Real Estate**: For modest $100,000 homes, pricing variation is small ($\\pm $10,000$). For luxury $5,000,000 estates, unique architectural features and bidder wealth create massive variance ($\\pm $1,000,000$).
- **Income & Expenditure**: Low-income households spend predictable fractions of income on food; wealthy households have immense discretionary choice, creating widening expenditure variance.

#### Consequences on OLS
1. **Coefficients Remain Unbiased**: $\\mathbb{E}[\\hat{\\boldsymbol{\\theta}}] = \\boldsymbol{\\theta}^*$. The line still passes through the center of the cloud.
2. **Standard Errors Are Biased**: OLS standard error formulas assume $\\sigma^2$ is constant. Under heteroscedasticity, standard errors are systematically underestimated.
3. **Hypothesis Tests Collapse**: Computed $t$-scores $\\frac{\\hat{\\theta}_j}{\\text{SE}(\\hat{\\theta}_j)}$ are artificially inflated, generating false positive statistical discoveries ($p$-value spam).

---

### 5.2 Formal Hypothesis Testing: The Breusch-Pagan Test

To statistically confirm whether a residual fan represents true heteroscedasticity rather than random noise, we deploy the **Breusch-Pagan Test**:

1. Fit the primary OLS model and obtain squared residuals $e_i^2 = (y_i - \\hat{y}_i)^2$.
2. Fit an auxiliary regression predicting squared residuals from the original features:
   $$e_i^2 = \\gamma_0 + \\gamma_1 x_{i,1} + \\dots + \\gamma_d x_{i,d} + v_i$$
3. Compute the test statistic:
   $$\\text{LM} = m \\cdot R_{\\text{aux}}^2 \\sim \\chi^2(d)$$
4. **Decision Rule**: If $p < 0.05$, reject the null hypothesis of homoscedasticity; heteroscedasticity is statistically verified.

---

### 5.3 Remediation Strategies

#### Strategy 1: Log-Transformation of Target ($\log(y)$)
When error spread grows proportionally with $y$, transforming $y \\to \\log(y)$ stabilizes variance across orders of magnitude:

$$\\log(y) = \\theta_0 + \\theta_1 x_1 + \\dots + \\theta_d x_d + \\varepsilon$$

- **Coefficient Interpretation After Log-y**:
  $$\\theta_j = \\frac{\\partial \\log(y)}{\\partial x_j} = \\frac{1}{y} \\frac{\\partial y}{\\partial x_j} \\implies \\% \\Delta y \\approx 100 \\cdot \\theta_j \\quad (\\text{for a 1-unit increase in } x_j)$$
  A coefficient of $\\theta_{\\text{income}} = 0.08$ means each additional unit of income associates with approximately an **$8\\%$ increase** in house price, rather than a fixed dollar amount.

#### Strategy 2: Heteroscedasticity-Consistent (White / Huber-White) Standard Errors
If transforming $y$ is undesirable or fails to fully resolve heteroscedasticity, compute robust standard errors via the 'sandwich' covariance estimator:

$$\\text{Var}_{\\text{robust}}(\\hat{\\boldsymbol{\\theta}}) = (\\mathbf{X}^T \\mathbf{X})^{-1} \\left( \\sum_{i=1}^m e_i^2 \\mathbf{x}_i \\mathbf{x}_i^T \\right) (\\mathbf{X}^T \\mathbf{X})^{-1}$$

This adjusts standard errors and $p$-values to be asymptotically valid without modifying the point estimates $\\hat{\\boldsymbol{\\theta}}$.

**Citations & References:**
- Breusch, T. S., & Pagan, A. R. (1979). A simple test for heteroscedasticity and random coefficient variation. Econometrica, 47(5), 1287-1294.
- White, H. (1980). A heteroskedasticity-consistent covariance matrix estimator and a direct test for heteroskedasticity. Econometrica, 48(4), 817-838.

---

## 6. Assumption 3 (Normality of Residuals): Q-Q Plots, Jarque-Bera Test & Outliers
### 6.1 The Role of Normal Errors in OLS

Assumption 3 specifies that the population disturbances follow a Gaussian bell curve:
$$\\varepsilon_i \\overset{\\text{iid}}{\\sim} \\mathcal{N}(0, \\sigma^2)$$

#### Why Normality Matters
1. **Hypothesis Testing**: Formulating confidence intervals ($\\hat{\\theta}_j \\pm 1.96 \\cdot \\text{SE}$) and computing exact $t$-tests and $F$-tests requires that sampling distributions of $\\hat{\\boldsymbol{\\theta}}$ are strictly Gaussian.
2. **Prediction Intervals**: Forecasting future individual outcomes $y_{\\text{new}} = \\hat{y}_{\\text{new}} \\pm t_{\\alpha/2} \\sqrt{\\sigma^2 + \\text{SE}^2}$ depends directly on Gaussian tail probabilities.

#### The Central Limit Theorem (CLT) Salvation for Large $m$
By the Central Limit Theorem, the distribution of the estimated parameters $\\hat{\\boldsymbol{\\theta}} = (\\mathbf{X}^T \\mathbf{X})^{-1} \\mathbf{X}^T \\mathbf{y}$ converges asymptotically to a Multivariate Normal distribution as sample size $m \\to \\infty$, **regardless of the distribution of $\\varepsilon_i$**, provided errors have finite variance.
- For datasets with $m > 500$, non-normal residuals have negligible impact on point estimates or large-sample $Z$-tests.
- However, for individual prediction intervals and small sample inference ($m < 100$), non-normality remains a critical failure mode.

---

### 6.2 Visual Diagnosis: The Quantile-Quantile (Q-Q) Plot

The Normal Q-Q plot compares the ordered sample residuals against theoretical standard normal quantiles:

```
Normal Q-Q Plot Diagnostic Patterns:
   Healthy Gaussian Residuals:                  Heavy Tails (Leptokurtic / Outliers):
         Sample ^                                     Sample ^
         Quant  |          /                          Quant  |            /--* (Extreme high)
                |        /                                   |          /
                |      /                                     |        /
                |    /                                       |      /
                |  /                                         | *--/ (Extreme low)
                +------------------->                         +------------------->
                   Theoretical Quant                             Theoretical Quant
             Points hug 45-degree line                      Points lift up and drop off line
```

- **S-Shape with Ends Peeling Away**: Signals heavy tails (leptokurtosis) and high outlier frequency.
- **Upward Convex Bow**: Signals right-skewed residuals (model systematically underpredicts high values).
- **Downward Concave Bow**: Signals left-skewed residuals.

---

### 6.3 Influential Points, Leverage & Cook's Distance

Not all outliers are created equal. In linear regression, we distinguish three concepts:

```
Outliers vs. High-Leverage vs. Influential Observations:
       y ^                                               y ^
         |                                                 |
         |         *                                       |                               * [High Leverage +
         |       *   *  o [Outlier in y, Low Leverage]     |                          *      Large Residual =
         |     *   *                                       |                     *           INFLUENTIAL!]
         |   *                                             |                *
         |                                                 |           *
         +-----------------------------> x                 +-----------------------------> x
      (Minimal impact on slope)                         (Pivots the entire regression line!)
```

1. **Vertical Outlier**: Observation with an extreme residual $|e_i|$, but typical feature values $x_i$. Has minimal leverage to tilt the regression line.
2. **High Leverage Point**: Observation with extreme, unusual feature values $x_i$, far from the centroid $\\bar{\\mathbf{x}}$. Measured by the diagonal elements $h_{ii}$ of the Hat Matrix $\\mathbf{H} = \\mathbf{X}(\\mathbf{X}^T \\mathbf{X})^{-1} \\mathbf{X}^T$.
3. **Influential Point**: An observation that possesses **both** high leverage and a large residual. Deleting this single point drastically changes the parameter vector $\\hat{\\boldsymbol{\\theta}}$.

#### Cook's Distance ($D_i$)
Cook's Distance quantifies the overall displacement of all model predictions when observation $i$ is omitted:

$$D_i = \\frac{\\sum_{j=1}^m (\\hat{y}_j - \\hat{y}_{j(-i)})^2}{(d+1) \\cdot \\text{MSE}} = \\frac{e_i^2}{(d+1) \\cdot \\text{MSE}} \\left[ \\frac{h_{ii}}{(1 - h_{ii})^2} \\right]$$

- **Threshold**: Any observation with $D_i > 0.5$ or $D_i > \\frac{4}{m}$ warrants manual inspection. Never blindly delete outliers; investigate whether they represent measurement error or genuine rare phenomena.

**Citations & References:**
- Shapiro, S. S., & Wilk, M. B. (1965). An analysis of variance test for normality. Biometrika, 52(3-4), 591-611.
- Jarque, C. M., & Bera, A. K. (1987). A test for normality of observations and regression residuals. International Statistical Review, 163-172.

---

## 7. Assumption 4 (Independence of Errors): Autocorrelation, Durbin-Watson & Clustered Errors
### 7.1 The Independence Assumption

Assumption 4 dictates that error terms across distinct observations are statistically uncorrelated:

$$\\text{Cov}(\\varepsilon_i, \\varepsilon_j \\mid \\mathbf{X}) = 0, \\quad \\forall i \\neq j$$

When this assumption is violated, the error covariance matrix is non-diagonal:
$$\\text{Var}(\\boldsymbol{\\varepsilon} \\mid \\mathbf{X}) = \\sigma^2 \\boldsymbol{\\Omega}, \\quad \\boldsymbol{\\Omega} \\neq \\mathbf{I}$$

---

### 7.2 Manifestations of Autocorrelation

1. **Temporal Serial Correlation**: In sequential data (daily stock prices, hourly temperature, quarterly GDP), the residual at time $t$ is correlated with the residual at time $t-1$:
   $$\\varepsilon_t = \\rho \\varepsilon_{t-1} + u_t, \\quad |\\rho| < 1$$
   - Positive serial correlation ($\\rho > 0$): Consecutive errors have identical signs, producing long waves above and below the regression line.
2. **Spatial Autocorrelation**: Geographic proximity induces dependency (e.g., California housing parcel prices where neighboring parcels share unmeasured school district and ocean proximity amenities).
3. **Clustered / Grouped Dependency**: Multiple observations collected from the same user, patient, or school classroom.

#### Consequences on OLS
Under positive autocorrelation ($\\rho > 0$), OLS standard error formulas vastly underestimate true parameter uncertainty. The true variance can be **10 to 50 times larger** than reported by OLS, creating false claims of statistical significance.

---

### 7.3 Testing Autocorrelation: The Durbin-Watson Statistic

The **Durbin-Watson ($d$) test** evaluates first-order serial correlation in sequential residuals:

$$d = \\frac{\\sum_{t=2}^m (e_t - e_{t-1})^2}{\\sum_{t=1}^m e_t^2} \\approx 2(1 - \\hat{\\rho})$$

Where $\\hat{\\rho} = \\frac{\\sum e_t e_{t-1}}{\\sum e_t^2}$ is the sample first-order autocorrelation of residuals.

```
Interpreting the Durbin-Watson Statistic:
     d = 0.0                     d = 2.0                     d = 4.0
       |----------------------------|----------------------------|
   rho = +1.0                   rho = 0.0                   rho = -1.0
   Severe Positive              IDEAL: ZERO                 Severe Negative
   Serial Correlation           AUTOCORRELATION             Serial Correlation
```

- **$d \\approx 2.0$**: Ideal. Zero serial correlation.
- **$d < 1.5$**: Serious positive autocorrelation. Standard errors are severely underestimated.
- **$d > 2.5$**: Negative autocorrelation (alternating residual signs).

---

### 7.4 Remediation Strategies
1. **Time-Series Lags & Differencing**: Include autoregressive lag terms $y_{t-1}$ or regress on first differences: $\\Delta y_t = y_t - y_{t-1}$.
2. **Cluster-Robust Standard Errors (Huber-White-Liang-Zeger)**: Group observations by entity ID (e.g., patient or district), allowing arbitrary internal correlation within clusters while maintaining independence across clusters.
3. **Generalized Least Squares (GLS / Prais-Winsten)**: Pre-whiten data by multiplying by $\\boldsymbol{\\Omega}^{-1/2}$.

**Citations & References:**
- Durbin, J., & Watson, G. S. (1950). Testing for serial correlation in least squares regression: I. Biometrika, 37(3-4), 409-428.
- Wooldridge, J. M. (2010). Econometric Analysis of Cross Section and Panel Data. MIT Press.

---

## 8. Assumption 5 (No Multicollinearity): Variance Inflation Factor (VIF) Derivation & Matrix Conditioning
### 8.1 The Multicollinearity Problem

Multicollinearity arises when two or more explanatory features in design matrix $\\mathbf{X}$ are highly correlated, meaning one feature can be linearly predicted from the others with substantial accuracy.

- **Perfect Multicollinearity**: One column is an exact linear combination of others (e.g., including both `height_in_inches` and `height_in_centimeters`, or failing to drop one level in One-Hot Encoding). $\\mathbf{X}^T \\mathbf{X}$ is singular, determinant equals 0, and Normal Equations cannot be inverted.
- **Imperfect (High) Multicollinearity**: Features are strongly correlated (e.g., in California housing, `total_rooms`, `total_bedrooms`, `population`, and `households` have pairwise correlations $r > 0.90$). $\\mathbf{X}^T \\mathbf{X}$ is invertible, but near-singular with tiny eigenvalues.

---

### 8.2 Consequences of High Multicollinearity

1. **Prediction Remains Unaffected**: Multicollinearity does **not** degrade overall predictive accuracy or $R^2$ within the training distribution. The hyperplane fits the data well.
2. **Coefficients Become Wildly Unstable**: The model cannot disentangle the individual marginal contribution of $x_1$ versus $x_2$. Small perturbations in training data cause massive swings in coefficient magnitudes and signs.
3. **Standard Errors Explode**: Confidence intervals become excessively wide, and $t$-statistics drop to zero. A model can have an overall $F$-test with $p < 0.0001$ and $R^2 = 0.85$, yet **every single individual feature has $p > 0.50$**!

---

### 8.3 Mathematical Derivation of Variance Inflation Factor (VIF)

The variance of an individual estimated regression coefficient $\\hat{\\theta}_j$ in multiple regression is given by:

$$\\text{Var}(\\hat{\\theta}_j) = \\frac{\\sigma^2}{(m - 1) s_{x_j}^2} \\cdot \\frac{1}{1 - R_j^2}$$

Where:
- $\\sigma^2$ is error variance.
- $s_{x_j}^2$ is the sample variance of feature $x_j$.
- $R_j^2$ is the Coefficient of Determination obtained by **regressing feature $x_j$ on all other $d-1$ features**.

The term $\\frac{1}{1 - R_j^2}$ is defined as the **Variance Inflation Factor (VIF)**:

$$\\text{VIF}_j = \\frac{1}{1 - R_j^2}$$

```
VIF Growth as Auxiliary R_j^2 Increases:
   R_j^2 = 0.00  -->  VIF = 1.0   (Completely orthogonal feature; zero variance inflation)
   R_j^2 = 0.80  -->  VIF = 5.0   (Standard error inflated by sqrt(5) = 2.23x)
   R_j^2 = 0.90  -->  VIF = 10.0  (Standard error inflated by sqrt(10) = 3.16x)
   R_j^2 = 0.99  -->  VIF = 100.0 (Standard error inflated by sqrt(100) = 10.0x!)
```

#### Diagnostic Decision Rules
- $\\text{VIF} = 1$: Ideal. Completely orthogonal.
- $1 < \\text{VIF} < 5$: Acceptable moderate correlation. No remediation needed.
- $\\text{VIF} > 5$: High collinearity. Investigate feature relationships.
- $\\text{VIF} > 10$: Severe multicollinearity. Coefficients are untrustworthy and require remediation.

---

### 8.4 Engineering Remediation for Multicollinearity

1. **Feature Pruning**: Delete redundant features that provide duplicate signals (e.g., between `total_rooms` and `total_bedrooms`, keep only one).
2. **Feature Engineering (Ratios)**: Create composite ratios that represent distinct physical concepts:
   $$\\text{rooms\\_per\\_household} = \\frac{\\text{total\\_rooms}}{\\text{households}}, \\quad \\text{bedrooms\\_per\\_room} = \\frac{\\text{total\\_bedrooms}}{\\text{total\\_rooms}}$$
   This breaks linear dependency and yields highly interpretable features.
3. **Principal Component Analysis (PCA)**: Orthogonalize the correlated features into uncorrelated principal components.
4. **$L_2$ Regularization (Ridge Regression)**: Adding $\\lambda \\mathbf{I}$ to $\\mathbf{X}^T \\mathbf{X}$ shifts eigenvalues away from zero, conditioning the matrix and stabilizing coefficient variances.

**Citations & References:**
- Belsley, D. A., Kuh, E., & Welsch, R. E. (1980). Regression Diagnostics: Identifying Influential Data and Sources of Collinearity. John Wiley & Sons.
- Marquardt, D. W. (1970). Generalized inverses, ridge regression, biased linear estimation, and nonlinear estimation. Technometrics, 12(3), 591-612.

---

## 9. Comprehensive Diagnostic Lab on California Housing & Remediation Strategies
### 9.1 Industrial Diagnostic Implementation in Python

We conduct a full econometric and machine learning diagnostic audit of the California Housing dataset using `statsmodels` and `scikit-learn`:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Load Data
df = pd.read_csv("data/california_housing.csv").dropna()
features = ["median_income", "housing_median_age", "total_rooms", 
            "total_bedrooms", "population", "households", "latitude", "longitude"]
X = df[features]
y = df["median_house_value"]

# 2. Strict Partitioning First
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# 3. Standardize and Prepend Constant Intercept
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=features, index=X_train.index)
X_train_const = sm.add_constant(X_train_scaled)

# 4. Fit OLS Model via Statsmodels for Inferential Diagnostics
ols_model = sm.OLS(y_train, X_train_const).fit()
print(ols_model.summary())
```

---

### 9.2 Computing Variance Inflation Factors (VIF)

```python
# Compute VIF for all numeric features
vif_data = pd.DataFrame()
vif_data["Feature"] = features
vif_data["VIF"] = [
    variance_inflation_factor(X_train_scaled.values, i) 
    for i in range(len(features))
]
print("\nMulticollinearity Audit (VIF):")
print(vif_data.sort_values(by="VIF", ascending=False).to_string(index=False))
```

#### Diagnostic Output on California Housing
- `households`: $\\text{VIF} \\approx 13.5$ (Severe Multicollinearity!)
- `total_bedrooms`: $\\text{VIF} \\approx 10.2$ (Severe Multicollinearity!)
- `total_rooms`: $\\text{VIF} \\approx 8.9$ (High Collinearity!)
- `population`: $\\text{VIF} \\approx 6.4$ (High Collinearity!)

The four census volume variables are heavily intercorrelated. In our pipeline, replacing them with `rooms_per_household`, `bedrooms_per_room`, and `population_per_household` reduces all VIFs below $2.5$.

---

### 9.3 Statistical Tests & Remediation via Log-Target Transformation

```python
# 1. Extract Training Residuals
residuals = ols_model.resid
fitted_values = ols_model.fittedvalues

# 2. Durbin-Watson Test for Independence
dw_stat = durbin_watson(residuals)
print(f"\nDurbin-Watson Statistic: {dw_stat:.4f} (Ideal ~ 2.0)")

# 3. Breusch-Pagan Test for Homoscedasticity
bp_test = het_breuschpagan(residuals, X_train_const)
print(f"Breusch-Pagan LM p-value: {bp_test[1]:.4e} (p < 0.05 verifies Heteroscedasticity!)")

# 4. REMEDIATION: Log-Transform the Target
y_train_log = np.log(y_train)
ols_log_model = sm.OLS(y_train_log, X_train_const).fit()

# Re-test Breusch-Pagan on Log Model
bp_log_test = het_breuschpagan(ols_log_model.resid, X_train_const)
print(f"Breusch-Pagan p-value after log(y): {bp_log_test[1]:.4e}")
```

---

### 9.4 The Complete 4-Panel Diagnostic Dashboard

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Residuals vs Fitted
axes[0, 0].scatter(fitted_values, residuals, alpha=0.15, color="darkblue")
axes[0, 0].axhline(0, color="red", linestyle="--", linewidth=2)
axes[0, 0].set_title("1. Residuals vs. Fitted (Checking Linearity & Heteroscedasticity)")
axes[0, 0].set_xlabel("Fitted Values y_hat")
axes[0, 0].set_ylabel("Residuals e")

# Panel 2: Normal Q-Q Plot
sm.qqplot(residuals, line="45", fit=True, ax=axes[0, 1])
axes[0, 1].set_title("2. Normal Q-Q Plot (Checking Normality)")

# Panel 3: Scale-Location Plot
std_residuals = ols_model.get_influence().resid_studentized_internal
axes[1, 0].scatter(fitted_values, np.sqrt(np.abs(std_residuals)), alpha=0.15, color="purple")
axes[1, 0].set_title("3. Scale-Location (Checking Equal Spread)")
axes[1, 0].set_xlabel("Fitted Values y_hat")
axes[1, 0].set_ylabel("sqrt(|Standardized Residuals|)")

# Panel 4: Cook's Distance
cooks_d = ols_model.get_influence().cooks_distance[0]
axes[1, 1].stem(np.arange(len(cooks_d)), cooks_d, markerfmt=",")
axes[1, 1].axhline(4 / len(X_train), color="red", linestyle="--", label="Threshold 4/m")
axes[1, 1].set_title("4. Cook's Distance (Identifying Influential Points)")
axes[1, 1].set_xlabel("Observation Index")
axes[1, 1].legend()

plt.tight_layout()
plt.show()
```

**Citations & References:**
- Seabold, S., & Perktold, J. (2010). statsmodels: Econometric and statistical modeling with python. Proceedings of the 9th Python in Science Conference.
- Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python.

---
