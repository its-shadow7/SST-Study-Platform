"""
Data definition for Term 5 CML Lecture 3:
Linear Regression Deep Dive: Ordinary Least Squares, Normal Equations & Optimization
"""

L3_DATA = {
    "schema_version": 1,
    "note_id": "cml-t5-l03",
    "term": "Term 5",
    "subject_code": "CML",
    "topic_title": "3. Linear Regression Deep Dive: Ordinary Least Squares, Normal Equations & Optimization",
    "tags": [
        "Linear Regression",
        "Ordinary Least Squares",
        "Normal Equation",
        "Gradient Descent",
        "Cost Functions",
        "Evaluation Metrics",
        "R-squared",
        "Residuals"
    ],
    "learning_objectives": [
        "1. Master the mathematical formulation of linear regression using vector dot products and the intercept trick.",
        "2. Formulate the Ordinary Least Squares (OLS) objective function J(theta) and understand its convex quadratic geometry.",
        "3. Derive the closed-form Normal Equation theta = (X^T X)^(-1) X^T y via matrix calculus and geometric projection.",
        "4. Differentiate Batch Gradient Descent, Stochastic Gradient Descent (SGD), and Mini-Batch Gradient Descent update rules.",
        "5. Explain how feature scaling spherizes the loss surface contours to accelerate gradient descent convergence.",
        "6. Compute, interpret, and compare evaluation metrics: MAE, MSE, RMSE, R^2, and Adjusted R^2 on unseen holdout datasets.",
        "7. Interpret regression weights as partial slopes under ceteris paribus conditions, distinguishing association from causation."
    ],
    "summary": "An exhaustive, mathematically rigorous deep dive into Linear Regression. Covers vector formulation with the intercept trick, geometric projection in column space, calculus derivation of the Normal Equation, Batch vs. Stochastic Gradient Descent dynamics, feature scaling condition numbers, comprehensive holdout evaluation metrics (MAE, MSE, RMSE, R^2, Adjusted R^2), coefficient interpretation pitfalls, and complete scikit-learn pipeline implementations.",
    "key_takeaways": [
        "1. The intercept trick packs the bias parameter theta_0 and feature weights theta_1...theta_d into a single compact dot product theta^T x by appending a constant feature x_0 = 1.",
        "2. Ordinary Least Squares minimizes the sum of squared vertical residuals, forming a strictly convex quadratic bowl J(theta) with a unique global minimum.",
        "3. Geometrically, OLS projects target vector y orthogonally onto the column space Col(X), ensuring the residual vector e = y - X theta is strictly orthogonal to every feature column.",
        "4. The Normal Equation theta = (X^T X)^(-1) X^T y yields an exact one-shot solution when X has full column rank; for large-scale data (n, d >> 10^5), gradient descent is computationally superior.",
        "5. Batch GD uses all m samples to compute smooth gradients; SGD updates per single sample introducing stochastic noise; Mini-Batch balances vectorization and stability.",
        "6. R^2 quantifies the proportion of variance explained by the model relative to the horizontal mean baseline y_bar; Adjusted R^2 penalizes superfluous features.",
        "7. Regression coefficients represent partial associations holding all other model variables fixed; they do not establish causal mechanisms without experimental designs."
    ],
    "last_updated": "2026-10-16T00:00:00Z",
    "approval_status": "approved",
    "sections": [
        {
            "section_id": "cml-l03-sec01",
            "heading": "1. Mathematical Formulation & Geometric Projections of Linear Regression",
            "citations": [
                "Strang, G. (2016). Introduction to Linear Algebra (5th ed.). Wellesley-Cambridge Press, Chapter 4.",
                "Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer, Chapter 3.",
                "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). Springer."
            ],
            "body": r"""### 1.1 The Supervised Learning Framework

In supervised regression, the learner is supplied with an empirical training dataset $\\mathcal{D} = \\{(\\mathbf{x}^{(i)}, y^{(i)})\\}_{i=1}^m$, where:
- $\\mathbf{x}^{(i)} \\in \\mathbb{R}^d$ represents the $i$-th input feature vector (e.g., median income, housing age, total rooms).
- $y^{(i)} \\in \\mathbb{R}$ represents the continuous target response (e.g., house price in dollars).
- $m$ denotes the total number of training instances (rows).
- $d$ denotes the number of raw features (columns).

The fundamental hypothesis of Linear Regression asserts that the target variable $y$ can be modeled as a linear combination of input features plus an unobserved additive error term $\\varepsilon$:

$$y = \\theta_0 + \\theta_1 x_1 + \\theta_2 x_2 + \\dots + \\theta_d x_d + \\varepsilon$$

Where:
- $\\theta_0 \\in \\mathbb{R}$ is the **intercept** (bias term), representing the expected value of $y$ when all input features equal zero ($x_1 = x_2 = \\dots = x_d = 0$).
- $\\theta_j \\in \\mathbb{R}$ ($j \\in \\{1, \\dots, d\\}$) are the **regression coefficients** (feature weights), representing the marginal change in $y$ per unit increase in feature $x_j$, holding all other features strictly constant (*ceteris paribus*).
- $\\varepsilon \\sim \\mathcal{N}(0, \\sigma^2)$ is the irreducible random noise representing unmodeled latent factors and measurement stochasticity.

---

### 1.2 The Intercept Trick & Compact Matrix Notation

To eliminate separate handling of the intercept $\\theta_0$, we introduce a constant dummy feature $x_0 = 1$ to every observation vector. This mathematical formulation packs the entire hypothesis into a single vector inner product:

$$\\mathbf{x} = \\begin{bmatrix} x_0 \\\\ x_1 \\\\ x_2 \\\\ \\vdots \\\\ x_d \\end{bmatrix} = \\begin{bmatrix} 1 \\\\ x_1 \\\\ x_2 \\\\ \\vdots \\\\ x_d \\end{bmatrix} \\in \\mathbb{R}^{d+1}, \\quad \\boldsymbol{\\theta} = \\begin{bmatrix} \\theta_0 \\\\ \\theta_1 \\\\ \\theta_2 \\\\ \\vdots \\\\ \\theta_d \\end{bmatrix} \\in \\mathbb{R}^{d+1}$$

$$h_{\\boldsymbol{\\theta}}(\\mathbf{x}) = \\boldsymbol{\\theta}^T \\mathbf{x} = \\theta_0 x_0 + \\theta_1 x_1 + \\dots + \\theta_d x_d = \\sum_{j=0}^d \\theta_j x_j$$

For the entire training dataset of $m$ observations, we assemble the design matrix $\\mathbf{X} \\in \\mathbb{R}^{m \\times (d+1)}$ by prepending a column of ones:

$$\\mathbf{X} = \\begin{bmatrix} 1 & x_{1,1} & x_{1,2} & \\cdots & x_{1,d} \\\\ 1 & x_{2,1} & x_{2,2} & \\cdots & x_{2,d} \\\\ \\vdots & \\vdots & \\vdots & \\ddots & \\vdots \\\\ 1 & x_{m,1} & x_{m,2} & \\cdots & x_{m,d} \\end{bmatrix} = \\begin{bmatrix} (\\mathbf{x}^{(1)})^T \\\\ (\\mathbf{x}^{(2)})^T \\\\ \\vdots \\\\ (\\mathbf{x}^{(m)})^T \\end{bmatrix}, \\quad \\mathbf{y} = \\begin{bmatrix} y^{(1)} \\\\ y^{(2)} \\\\ \\vdots \\\\ y^{(m)} \\end{bmatrix} \\in \\mathbb{R}^m$$

The vector of all $m$ model predictions $\\hat{\\mathbf{y}} \\in \\mathbb{R}^m$ is expressed as a single matrix-vector multiplication:

$$\\hat{\\mathbf{y}} = \\mathbf{X} \\boldsymbol{\\theta}$$

---

### 1.3 Geometric Interpretation: Projection onto Column Space

Linear regression possesses a geometric interpretation in linear algebra. The target vector $\\mathbf{y} \\in \\mathbb{R}^m$ lives in an $m$-dimensional observation space. 

The columns of design matrix $\\mathbf{X} = [\\mathbf{1}, \\mathbf{x}_1, \\mathbf{x}_2, \\dots, \\mathbf{x}_d]$ span a $(d+1)$-dimensional subspace $\\text{Col}(\\mathbf{X}) \\subset \\mathbb{R}^m$. In real-world data where $m \\gg d$, the vector $\\mathbf{y}$ does **not** lie within $\\text{Col}(\\mathbf{X})$ due to noise $\\varepsilon$. 

```
Geometry of Ordinary Least Squares (m-dimensional Observation Space):
              y (True target vector)
              ^
              | \
              |  \
              |   \\  e = y - X theta (Residual vector, orthogonal to Col(X))
              |    \
              |     v
              +------> y_hat = X theta  (Orthogonal Projection of y onto Col(X))
             /       /
            / Col(X)/  Subspace spanned by columns of design matrix X
           +-------+
```

1. Any prediction $\\hat{\\mathbf{y}} = \\mathbf{X} \\boldsymbol{\\theta}$ is a linear combination of the column vectors of $\\mathbf{X}$, meaning $\\hat{\\mathbf{y}}$ is constrained to lie inside $\\text{Col}(\\mathbf{X})$.
2. The Ordinary Least Squares solution finds the specific point $\\hat{\\mathbf{y}} \\in \\text{Col}(\\mathbf{X})$ that is **closest in Euclidean distance** to the true vector $\\mathbf{y}$.
3. By the Projection Theorem, the shortest distance from a point to a subspace is achieved when the error vector (residual vector) $\\mathbf{e} = \\mathbf{y} - \\hat{\\mathbf{y}} = \\mathbf{y} - \\mathbf{X}\\boldsymbol{\\theta}$ is **strictly orthogonal (perpendicular)** to every column vector spanning $\\text{Col}(\\mathbf{X})$:

$$\\mathbf{X}^T (\\mathbf{y} - \\mathbf{X}\\boldsymbol{\\theta}) = \\mathbf{0}$$

This orthogonality condition yields the Normal Equation directly."""
        },
        {
            "section_id": "cml-l03-sec02",
            "heading": "2. The Ordinary Least Squares (OLS) Objective & Cost Function J(theta)",
            "citations": [
                "Gauss, C. F. (1809). Theoria motus corporum coelestium in sectionibus conicis solem ambientium.",
                "Nocedal, J., & Wright, S. J. (2006). Numerical Optimization (2nd ed.). Springer."
            ],
            "body": r"""### 2.1 Formulation of the Least Squares Objective

To estimate the optimal parameter vector $\\boldsymbol{\\theta}^*$, we establish a mathematical loss function quantifying the discrepancy between model predictions $h_{\\boldsymbol{\\theta}}(\\mathbf{x}^{(i)})$ and ground-truth observations $y^{(i)}$.

The **residual error** for the $i$-th training observation is:
$$e^{(i)} = y^{(i)} - h_{\\boldsymbol{\\theta}}(\\mathbf{x}^{(i)}) = y^{(i)} - \\boldsymbol{\\theta}^T \\mathbf{x}^{(i)}$$

The **Ordinary Least Squares (OLS) Cost Function** $J(\\boldsymbol{\\theta})$ sums the squared residual errors across all $m$ training samples:

$$J(\\boldsymbol{\\theta}) = \\frac{1}{2} \\sum_{i=1}^m \\left( h_{\\boldsymbol{\\theta}}(\\mathbf{x}^{(i)}) - y^{(i)} \\right)^2 = \\frac{1}{2} \\sum_{i=1}^m \\left( \\boldsymbol{\\theta}^T \\mathbf{x}^{(i)} - y^{(i)} \\right)^2$$

*(Note: The leading constant $\\frac{1}{2}$ is introduced purely for algebraic convenience to cancel the factor of $2$ when computing partial derivatives).*

In vector-matrix notation, $J(\\boldsymbol{\\theta})$ is written as the squared Euclidean norm of the residual vector $\\mathbf{e} = \\mathbf{X}\\boldsymbol{\\theta} - \\mathbf{y}$:

$$J(\\boldsymbol{\\theta}) = \\frac{1}{2} \\| \\mathbf{X}\\boldsymbol{\\theta} - \\mathbf{y} \\|_2^2 = \\frac{1}{2} (\\mathbf{X}\\boldsymbol{\\theta} - \\mathbf{y})^T (\\mathbf{X}\\boldsymbol{\\theta} - \\mathbf{y})$$

---

### 2.2 Why Squared Residuals? (Gauss-Markov & Maximum Likelihood)

Why do we minimize squared errors $\\sum (y^{(i)} - \\hat{y}^{(i)})^2$ rather than absolute errors $\\sum |y^{(i)} - \\hat{y}^{(i)}|$ or higher powers?

1. **Strict Convexity & Uniqueness**: For linear models with linearly independent features, $J(\\boldsymbol{\\theta})$ is a quadratic function of $\\boldsymbol{\\theta}$. The Hessian matrix $\\nabla^2 J(\\boldsymbol{\\theta}) = \\mathbf{X}^T \\mathbf{X}$ is positive definite. This guarantees that $J(\\boldsymbol{\\theta})$ forms a smooth, convex bowl with **exactly one global minimum and zero local minima**.
2. **Maximum Likelihood Equivalence**: Under the assumption that observational errors $\\varepsilon^{(i)} \\overset{\\text{iid}}{\\sim} \\mathcal{N}(0, \\sigma^2)$ are normally distributed:
   $$p(y^{(i)} \\mid \\mathbf{x}^{(i)}; \\boldsymbol{\\theta}) = \\frac{1}{\\sqrt{2\\pi\\sigma^2}} \\exp\\left( -\\frac{(y^{(i)} - \\boldsymbol{\\theta}^T \\mathbf{x}^{(i)})^2}{2\\sigma^2} \\right)$$
   Maximizing the log-likelihood function $\\log L(\\boldsymbol{\\theta})$ across all $m$ independent samples is mathematically equivalent to minimizing the sum of squared errors $J(\\boldsymbol{\\theta})$.
3. **Continuous Differentiability**: Unlike absolute error $|e|$, squared error $e^2$ is everywhere continuously differentiable ($\\mathcal{C}^\\infty$), enabling exact analytical solutions and smooth gradient descent convergence.

```
Residual Errors in Least Squares (Vertical Distances):
       y ^
         |              * (x3, y3)
         |             /|
         |            / | e3 = y3 - y_hat3
         |           /  v
         |          /---o--  Fitted Line: y_hat = theta0 + theta1 * x
         |         /|
         |        / | e2
         |       /  v
         |      * (x2, y2)
         |     /
         +----+------------------------------------> x
   OLS minimizes sum(e_i^2) strictly along the VERTICAL y-axis!
```

> **Pedagogical Warning**: Least Squares minimizes **vertical** errors $(y^{(i)} - \\hat{y}^{(i)})$, assuming input features $x$ are measured without error. This is fundamentally distinct from Total Least Squares (Orthogonal Regression), which minimizes perpendicular Euclidean distances to the regression line."""
        },
        {
            "section_id": "cml-l03-sec03",
            "heading": "3. Closed-Form Analytical Solution: Derivation of the Normal Equation",
            "citations": [
                "Boyd, S., & Vandenberghe, L. (2004). Convex Optimization. Cambridge University Press.",
                "Petersen, K. B., & Pedersen, M. S. (2012). The Matrix Cookbook. Technical University of Denmark."
            ],
            "body": r"""### 3.1 Step-by-Step Matrix Calculus Derivation

Because $J(\\boldsymbol{\\theta})$ is a convex quadratic function, its global minimum occurs where the gradient vector $\\nabla_{\\boldsymbol{\\theta}} J(\\boldsymbol{\\theta})$ is identically equal to the zero vector $\\mathbf{0} \\in \\mathbb{R}^{d+1}$.

#### Step 1: Expand the Matrix Cost Function
$$J(\\boldsymbol{\\theta}) = \\frac{1}{2} (\\mathbf{X}\\boldsymbol{\\theta} - \\mathbf{y})^T (\\mathbf{X}\\boldsymbol{\\theta} - \\mathbf{y})$$
$$J(\\boldsymbol{\\theta}) = \\frac{1}{2} \\left( (\\mathbf{X}\\boldsymbol{\\theta})^T - \\mathbf{y}^T \\right) (\\mathbf{X}\\boldsymbol{\\theta} - \\mathbf{y})$$
$$J(\\boldsymbol{\\theta}) = \\frac{1}{2} \\left( \\boldsymbol{\\theta}^T \\mathbf{X}^T \\mathbf{X} \\boldsymbol{\\theta} - \\boldsymbol{\\theta}^T \\mathbf{X}^T \\mathbf{y} - \\mathbf{y}^T \\mathbf{X} \\boldsymbol{\\theta} + \\mathbf{y}^T \\mathbf{y} \\right)$$

Note that $\\boldsymbol{\\theta}^T \\mathbf{X}^T \\mathbf{y}$ is a scalar ($1 \\times 1$). The transpose of a scalar equals itself:
$$(\\boldsymbol{\\theta}^T \\mathbf{X}^T \\mathbf{y})^T = \\mathbf{y}^T \\mathbf{X} \\boldsymbol{\\theta}$$

Therefore, the two middle cross-terms combine:
$$J(\\boldsymbol{\\theta}) = \\frac{1}{2} \\left( \\boldsymbol{\\theta}^T \\mathbf{X}^T \\mathbf{X} \\boldsymbol{\\theta} - 2 \\mathbf{y}^T \\mathbf{X} \\boldsymbol{\\theta} + \\mathbf{y}^T \\mathbf{y} \\right)$$

---

#### Step 2: Compute the Matrix Gradient $\\nabla_{\\boldsymbol{\\theta}} J(\\boldsymbol{\\theta})$
Using fundamental matrix derivative identities from The Matrix Cookbook:
- $\\nabla_{\\mathbf{w}} (\\mathbf{a}^T \\mathbf{w}) = \\mathbf{a}$
- $\\nabla_{\\mathbf{w}} (\\mathbf{w}^T \\mathbf{A} \\mathbf{w}) = (\\mathbf{A} + \\mathbf{A}^T)\\mathbf{w} = 2\\mathbf{A}\\mathbf{w}$ (when $\\mathbf{A}$ is symmetric; $\\mathbf{X}^T\\mathbf{X}$ is symmetric).

Differentiating $J(\\boldsymbol{\\theta})$ with respect to $\\boldsymbol{\\theta}$:
$$\\nabla_{\\boldsymbol{\\theta}} J(\\boldsymbol{\\theta}) = \\frac{1}{2} \\left( 2 \\mathbf{X}^T \\mathbf{X} \\boldsymbol{\\theta} - 2 \\mathbf{X}^T \\mathbf{y} + \\mathbf{0} \\right) = \\mathbf{X}^T \\mathbf{X} \\boldsymbol{\\theta} - \\mathbf{X}^T \\mathbf{y}$$

---

#### Step 3: Set Gradient to Zero and Solve for $\\boldsymbol{\\theta}^*$
Setting the gradient equal to zero yields the **Normal Equation**:
$$\\mathbf{X}^T \\mathbf{X} \\boldsymbol{\\theta} - \\mathbf{X}^T \\mathbf{y} = \\mathbf{0}$$
$$\\mathbf{X}^T \\mathbf{X} \\boldsymbol{\\theta} = \\mathbf{X}^T \\mathbf{y}$$

Assuming the square matrix $(\\mathbf{X}^T \\mathbf{X}) \\in \\mathbb{R}^{(d+1) \\times (d+1)}$ is non-singular and invertible, pre-multiplying both sides by $(\\mathbf{X}^T \\mathbf{X})^{-1}$ yields the closed-form analytical OLS solution:

$$\\boldsymbol{\\theta}^* = (\\mathbf{X}^T \\mathbf{X})^{-1} \\mathbf{X}^T \\mathbf{y}$$

---

### 3.2 Invertibility & The Pseudo-Inverse

When is $(\\mathbf{X}^T \\mathbf{X})$ invertible?
1. **Full Column Rank**: The matrix $(\\mathbf{X}^T \\mathbf{X})$ is invertible if and only if $\\mathbf{X}$ has full column rank, meaning $\\text{rank}(\\mathbf{X}) = d + 1$. This requires:
   - $m \\ge d + 1$ (strictly more observations than parameters).
   - No feature column is an exact linear combination of other feature columns (zero perfect multicollinearity).
2. **Singularity Remedies**: If $(\\mathbf{X}^T \\mathbf{X})$ is non-invertible (e.g., $d > m$ or redundant columns):
   - Compute the Moore-Penrose Pseudoinverse via Singular Value Decomposition (SVD): $\\boldsymbol{\\theta}^* = \\mathbf{X}^+ \\mathbf{y}$.
   - Add $L_2$ regularization (Ridge Regression): $(\\mathbf{X}^T \\mathbf{X} + \\lambda \\mathbf{I})^{-1} \\mathbf{X}^T \\mathbf{y}$, which guarantees non-singularity for any $\\lambda > 0$."""
        },
        {
            "section_id": "cml-l03-sec04",
            "heading": "4. Gradient Descent Optimization: Batch GD, Stochastic GD & Mini-Batch GD",
            "citations": [
                "Robbins, H., & Monro, S. (1951). A stochastic approximation method. The Annals of Mathematical Statistics, 22(3), 400-407.",
                "Bottou, L. (2010). Large-scale machine learning with stochastic gradient descent. COMPSTAT."
            ],
            "body": r"""### 4.1 When the Normal Equation Fails: The Scaling Problem

Computing the closed-form Normal Equation requires inverting the $(d+1) \\times (d+1)$ matrix $(\\mathbf{X}^T \\mathbf{X})$. Matrix inversion has a computational complexity of approximately $\\mathcal{O}(d^3)$ (or $\\mathcal{O}(d^{2.807})$ via Strassen's algorithm).
- If $d = 100$: $(d+1)^3 \\approx 10^6$ operations (instantaneous, $< 1$ millisecond).
- If $d = 100,000$ (e.g., text NLP embeddings or genomic data): $(10^5)^3 = 10^{15}$ operations (impossible in RAM, hours/days of compute).

When feature dimensionality $d$ or sample size $m$ is large, or when data arrives in streaming batches, we deploy **iterative optimization algorithms: Gradient Descent**.

---

### 4.2 The Gradient Descent Update Rule

Gradient Descent starts with an initial parameter guess $\\boldsymbol{\\theta}^{(0)}$ (typically zeros or small random Gaussian values) and iteratively steps in the direction of steepest descent (opposite to the gradient vector $\\nabla J(\\boldsymbol{\\theta})$):

$$\\boldsymbol{\\theta} \\leftarrow \\boldsymbol{\\theta} - \\alpha \\nabla_{\\boldsymbol{\\theta}} J(\\boldsymbol{\\theta})$$

Where $\\alpha > 0$ represents the **learning rate** (step size).

For an individual parameter $\\theta_j$, the component-wise update is:
$$\\theta_j \\leftarrow \\theta_j - \\alpha \\frac{\\partial J(\\boldsymbol{\\theta})}{\\partial \\theta_j}$$

> **The Simultaneous Update Requirement**:
> All parameters $\\theta_0, \\theta_1, \\dots, \\theta_d$ must be updated **simultaneously** at each iteration. That is, all partial derivatives $\\frac{\\partial J(\\boldsymbol{\\theta})}{\\partial \\theta_j}$ must be calculated using the identical, frozen parameter vector $\\boldsymbol{\\theta}^{\\text{old}}$ before any parameter values are overwritten.

---

### 4.3 The Three Gradient Descent Variants

```
Comparison of Optimization Trajectories on Contour Surface:
         Batch Gradient Descent                     Stochastic Gradient Descent (SGD)
              w_2 ^                                      w_2 ^
                  |      /-----\\                             |      /-----\\
                  |     /   |   \\                            |     / *--*  \\  (Noisy,
                  |    | <--+--* | (Smooth direct path)      |    | /  / \\* |  erratic
                  |     \\   |   /                            |     \\*--*  /   walk)
                  |      \\-----/                             |      \\-----/
                  +------------------> w_1                   +------------------> w_1
```

| Parameter | Batch Gradient Descent (BGD) | Stochastic Gradient Descent (SGD) | Mini-Batch Gradient Descent (MBGD) |
| :--- | :--- | :--- | :--- |
| **Samples per Update** | **All $m$ samples** (full dataset). | **1 single sample** ($m=1$). | **$B$ samples** ($32 \\le B \\le 512$). |
| **Gradient Formula** | $\\sum_{i=1}^m (h_{\\boldsymbol{\\theta}}(\\mathbf{x}^{(i)}) - y^{(i)}) x_j^{(i)}$ | $(h_{\\boldsymbol{\\theta}}(\\mathbf{x}^{(i)}) - y^{(i)}) x_j^{(i)}$ | $\\frac{1}{B} \\sum_{i \\in \\mathcal{B}} (h_{\\boldsymbol{\\theta}}(\\mathbf{x}^{(i)}) - y^{(i)}) x_j^{(i)}$ |
| **Gradient Variance** | Zero (Exact true gradient). | High (Noisy stochastic gradient). | Moderate (Controlled variance). |
| **Path to Minimum** | Smooth, direct, monotonic. | Oscillatory, erratic, jagged. | Smooth with mild stochasticity. |
| **Computational Cost** | $\\mathcal{O}(m \\cdot d)$ per step. Very slow for large $m$. | $\\mathcal{O}(d)$ per step. Extremely fast. | $\\mathcal{O}(B \\cdot d)$ per step. Highly parallelizable on GPUs. |
| **Memory Requirement** | Entire dataset must reside in RAM. | One sample in RAM (Streaming). | Small batch in RAM. |
| **Industrial Usage** | Small-to-medium tabular datasets. | Online/streaming learning. | **Standard default for modern deep learning and large-scale ML**. |"""
        },
        {
            "section_id": "cml-l03-sec05",
            "heading": "5. Feature Scaling Dynamics & Condition Numbers in Optimization",
            "citations": [
                "LeCun, Y. et al. (2012). Efficient BackProp. Neural Networks: Tricks of the Trade, Springer.",
                "Trefethen, L. N., & Bau, D. (1997). Numerical Linear Algebra. SIAM."
            ],
            "body": r"""### 5.1 The Mathematical Mechanism of Scaling in Optimization

In Lecture 2, we observed that unscaled features distort distance-based models. In Linear Regression, feature scaling dictates the **geometry of the quadratic loss bowl** and the condition number of the Hessian matrix.

The Hessian of the OLS cost function is:
$$\\mathbf{H} = \\nabla^2 J(\\boldsymbol{\\theta}) = \\mathbf{X}^T \\mathbf{X}$$

The eigenvalues $\\lambda_1 \\ge \\lambda_2 \\ge \\dots \\ge \\lambda_{d+1} > 0$ of $\\mathbf{X}^T \\mathbf{X}$ determine the curvature of $J(\\boldsymbol{\\theta})$ along the principal coordinate axes.
The **condition number** $\\kappa$ measures the ratio of maximum to minimum curvature:

$$\\kappa = \\frac{\\lambda_{\\max}(\\mathbf{X}^T \\mathbf{X})}{\\lambda_{\\min}(\\mathbf{X}^T \\mathbf{X})}$$

```
Loss Surface Geometries:
Ill-Conditioned (kappa >> 1, Unscaled Data):       Well-Conditioned (kappa approx 1, Scaled Data):
             w_2 ^                                             w_2 ^
                 |    /-----------------------\\                    |       /-----\\
                 |   /           |             \\                   |      /   |   \\
                 |  | <----------+----------->  |                  |     | <--+--> |
                 |   \\           |             /                   |      \\   |   /
                 |    \\-----------------------/                    |       \\-----/
                 +------------------------------> w_1              +--------------------> w_1
             Extreme oscillation, tiny learning rate             Direct radial descent, fast convergence
```

1. **Ill-Conditioned Landscape ($\\kappa \\gg 1$)**: When feature $x_1$ has variance $\\sigma_1^2 = 1,000,000$ (e.g., total rooms) and feature $x_2$ has variance $\\sigma_2^2 = 1$ (e.g., median income), the level curves form extremely compressed ellipses.
   - The gradient vector $\\nabla J(\\boldsymbol{\\theta})$ points nearly perpendicular to the direction of the true minimum.
   - Updates oscillate wildly along the steep $w_1$ dimension while making negligible progress along the flat $w_2$ dimension.
   - To prevent numerical divergence, the learning rate $\\alpha$ must be set exceptionally small: $\\alpha < \\frac{2}{\\lambda_{\\max}}$.
2. **Well-Conditioned Landscape ($\\kappa \\approx 1$)**: Applying Z-score standardization ($z = \\frac{x - \\mu}{\\sigma}$) scales all features to unit variance $\\sigma^2 = 1$. The eigenvalues become nearly equal, transforming elliptical contours into circular hyperspheres.
   - Gradients point directly toward the global minimum.
   - Large, stable learning rates can be deployed, accelerating convergence by orders of magnitude.

---

### 5.2 Normal Equation vs. Gradient Descent Comparison

| Engineering Criterion | Normal Equation ($\text{OLS Closed Form}$) | Gradient Descent (Iterative Solver) |
| :--- | :--- | :--- |
| **Hyperparameter Tuning** | **None**. Zero learning rate or iteration count to configure. | Requires tuning learning rate $\\alpha$, batch size $B$, and convergence epochs. |
| **Feature Scaling** | Not mathematically necessary for parameter values, though helpful for interpretation. | **Mandatory**. Unscaled features severely impair convergence speed. |
| **Computational Complexity** | $\\mathcal{O}(d^3)$ inversion of $(\\mathbf{X}^T \\mathbf{X})$. | $\\mathcal{O}(k \\cdot m \\cdot d)$ for $k$ iterations. |
| **Memory Scalability** | Requires storing $(d+1) \\times (d+1)$ matrix in RAM. | Highly scalable via mini-batch streaming from disk. |
| **Suitability Threshold** | Ideal when $d < 10,000$ and all data fits in memory. | Ideal when $d > 10,000$ or sample size $m > 1,000,000$. |
| **Scikit-Learn Implementation** | `LinearRegression()` | `SGDRegressor()` |"""
        },
        {
            "section_id": "cml-l03-sec06",
            "heading": "6. Model Evaluation Metrics: MAE, MSE, RMSE, R-squared & Adjusted R-squared",
            "citations": [
                "Willmott, C. J., & Matsuura, K. (2005). Advantages of the mean absolute error (MAE) over the root mean squared error (RMSE) in assessing average model performance. Climate Research.",
                "Chai, T., & Draxler, R. R. (2014). Root mean square error (RMSE) or mean absolute error (MAE)? Geoscientific Model Development."
            ],
            "body": r"""### 6.1 Point Residual Metrics

Once parameters $\\boldsymbol{\\theta}$ are fitted on training data $\\mathbf{X}_{\\text{train}}$, the model is evaluated on held-out test data $\\mathbf{X}_{\\text{test}}, \\mathbf{y}_{\\text{test}}$. We define test residual error for sample $i$ as:

$$e_i = y_i - \\hat{y}_i$$

#### 1. Mean Absolute Error (MAE)
$$\\text{MAE} = \\frac{1}{m} \\sum_{i=1}^m |y_i - \\hat{y}_i|$$
- **Interpretation**: The average expected absolute magnitude of error in natural target units (e.g., dollars).
- **Outlier Robustness**: High. Errors are penalized linearly ($L_1$), preventing isolated outliers from distorting the metric.

#### 2. Mean Squared Error (MSE)
$$\\text{MSE} = \\frac{1}{m} \\sum_{i=1}^m (y_i - \\hat{y}_i)^2$$
- **Interpretation**: Mean of squared deviations ($L_2$). Highly sensitive to outliers due to quadratic penalty $e_i^2$.
- **Unit Drawback**: Units are squared (e.g., $\\text{dollars}^2$), making business communication counter-intuitive.

#### 3. Root Mean Squared Error (RMSE)
$$\\text{RMSE} = \\sqrt{\\frac{1}{m} \\sum_{i=1}^m (y_i - \\hat{y}_i)^2} = \\sqrt{\\text{MSE}}$$
- **Interpretation**: Standard deviation of the unexplained residuals, measured in identical physical units to $y$.
- **Mathematical Property**: $\\text{RMSE} \\ge \\text{MAE}$. The difference $\\text{RMSE} - \\text{MAE}$ directly reflects the variance in error magnitudes across the test sample.

---

### 6.2 Relative Goodness-of-Fit: $R^2$ & Adjusted $R^2$

Absolute metrics (RMSE, MAE) depend on target scale ($10,000 RMSE is disastrous for predicting car age, but outstanding for predicting aircraft cost). We require a scale-independent metric comparing the model against a naive baseline.

#### The Horizontal Baseline Predictor
The simplest possible prediction for any unseen observation is the mean of the training target:
$$\\hat{y}_{\\text{baseline}} = \\bar{y} = \\frac{1}{m} \\sum_{i=1}^m y_i$$

We partition total variation into Sum of Squares components:
- **Total Sum of Squares (SST)**: Total variance inherent in the ground-truth target:
  $$\\text{SST} = \\sum_{i=1}^m (y_i - \\bar{y})^2$$
- **Residual Sum of Squares (SSE or SSR)**: Unexplained variance remaining after regression fit:
  $$\\text{SSE} = \\sum_{i=1}^m (y_i - \\hat{y}_i)^2$$

#### The Coefficient of Determination ($R^2$)
$$R^2 = 1 - \\frac{\\text{SSE}}{\\text{SST}} = 1 - \\frac{\\sum_{i=1}^m (y_i - \\hat{y}_i)^2}{\\sum_{i=1}^m (y_i - \\bar{y})^2}$$

```
Interpreting R^2 Values on Test Data:
   R^2 = 1.0  --> Perfect model: SSE = 0, every prediction exactly matches ground truth.
   R^2 = 0.8  --> Model explains 80% of the total variance in the target variable.
   R^2 = 0.0  --> Model performs identically to predicting the horizontal mean baseline y_bar.
   R^2 < 0.0  --> Model performs WORSE than predicting y_bar! (Indicates severe overfitting/breakdown).
```

#### The Fatal Flaw of $R^2$ & The Adjusted $R^2$ Solution
**Mathematical Flaw**: Adding a completely random, useless feature column to design matrix $\\mathbf{X}$ will **never decrease training $R^2$**. It will either marginally increase $R^2$ or keep it identical, because Ordinary Least Squares can always assign a near-zero weight to the useless feature.

To penalize model complexity and prevent feature bloating, **Adjusted $R^2$** incorporates degrees of freedom:

$$R^2_{\\text{adj}} = 1 - \\left( \\frac{\\text{SSE} / (m - d - 1)}{\\text{SST} / (m - 1)} \\right) = 1 - (1 - R^2) \\frac{m - 1}{m - d - 1}$$

Where:
- $m$ is sample size.
- $d$ is number of features (excluding intercept).
- $R^2_{\\text{adj}}$ increases **only if** a newly added feature reduces SSE by an amount greater than what would be expected by pure random chance."""
        },
        {
            "section_id": "cml-l03-sec07",
            "heading": "7. Coefficient Interpretation: Partial Slopes, Association vs. Causation",
            "citations": [
                "Pearl, J. (2009). Causality: Models, Reasoning, and Inference (2nd ed.). Cambridge University Press.",
                "Angrist, J. D., & Pischke, J. S. (2009). Mostly Harmless Econometrics. Princeton University Press."
            ],
            "body": r"""### 7.1 Interpreting Regression Weights as Partial Slopes

In multiple linear regression, each coefficient $\\theta_j$ ($j \\ge 1$) represents a **partial slope**:

$$\\theta_j = \\frac{\\partial h_{\\boldsymbol{\\theta}}(\\mathbf{x})}{\\partial x_j}$$

> **The Ceteris Paribus Principle**:
> Coefficient $\\theta_j$ quantifies the expected change in target $y$ when feature $x_j$ increases by exactly one unit, **holding all other $d-1$ features strictly constant**.

#### The Intercept $\\theta_0$
$\\theta_0$ represents the expected baseline prediction when every input feature equals zero: $h_{\\boldsymbol{\\theta}}(\\mathbf{0}) = \\theta_0$.
- In many domains, $\\mathbf{x} = \\mathbf{0}$ is physically impossible (e.g., a house with 0 square feet, 0 rooms, and 0 income).
- Centering features around their means ($x_j - \\bar{x}_j$) shifts the intercept such that $\\theta_0 = \\bar{y}$, providing immediate physical meaning as the average expected outcome for an average subject.

---

### 7.2 Scaled vs. Unscaled Coefficients

When comparing features to determine which attribute has the greatest predictive influence, comparing raw unscaled coefficients $\\theta_j$ is misleading:

$$\\hat{y} = 250,000 + 0.05 \\cdot (\\text{Annual Income in INR}) + 80,000 \\cdot (\\text{Number of Bedrooms})$$

At first glance, $\\theta_{\\text{bedrooms}} = 80,000$ appears $1,600,000$ times more influential than $\\theta_{\\text{income}} = 0.05$. 
However, annual income varies by $500,000$ INR, while bedrooms vary by $1$ or $2$. 
- **Standardized Coefficients**: When features are standardized via Z-score scaling ($x_j' = \\frac{x_j - \\mu_j}{\\sigma_j}$), each standardized coefficient $\\beta_j$ represents the expected standard deviation change in $y$ per one-standard-deviation change in $x_j$.
- In the California housing lab: The standardized coefficient for `median_income` ($\approx +82,000$) dominates all other features, proving that median district wealth is the primary linear driver of parcel value.

---

### 7.3 The Iron Boundary: Association $\\neq$ Causation

A foundational error in machine learning applications is confusing statistical regression weights with causal real-world levers:

```
Observed Empirical Correlation:
   High Ice Cream Sales <-------------------- Correlation --------------------> High Drowning Deaths
          ^                                                                             ^
          |                                                                             |
          +----------------------------- Hot Summer Sun --------------------------------+
                                       (Confounding Variable Z)
   Fitting OLS: Drowning = theta0 + theta1 * IceCreamSales yields a large positive theta1!
   Causal Fallacy: "Banning ice cream sales will prevent drownings." (Completely false).
```

1. **The Confounder Problem**: In observational tabular data, omitted variables (confounders) simultaneously influence both $x_j$ and $y$. Regression coefficients absorb these confounding paths.
2. **Reverse Causality**: The regression model treats $x \\to y$ as directional, but observational data cannot rule out $y \\to x$ or bidirectional feedback loops.
3. **The Executive Statement**:
   - **Correct Engineering Phrasing**: *"In this fitted model, a 1-standard-deviation increase in median income is associated with an estimated $82,000 increase in median house value, holding all other features in the dataset constant."*
   - **Incorrect Causal Claim**: *"Raising district income by $10,000 will cause house prices to rise by $82,000."*"""
        },
        {
            "section_id": "cml-l03-sec08",
            "heading": "8. End-to-End California Housing Pipeline Implementation & Residual Analysis",
            "citations": [
                "Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python.",
                "Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn. O'Reilly Media."
            ],
            "body": r"""### 8.1 Industrial Code Walkthrough

We assemble the complete California housing linear regression pipeline, adhering strictly to the train/test hygiene rules established in Lecture 2:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 1. Ingest Data and Separate Features
df = pd.read_csv("data/california_housing.csv")
X = df.drop(columns=["median_house_value"])
y = df["median_house_value"]

# 2. Strict Partitioning First (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# 3. Define Column Categories
num_cols = ["median_income", "housing_median_age", "total_rooms", 
            "total_bedrooms", "population", "households", "latitude", "longitude"]
cat_cols = ["ocean_proximity"]

# 4. Construct Sub-Pipelines
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_pipeline, num_cols),
    ("cat", categorical_pipeline, cat_cols)
])

# 5. Assemble Master Pipeline with OLS Solver
model_pipeline = Pipeline([
    ("prep", preprocessor),
    ("ols", LinearRegression())
])

# 6. Fit Once on Train; Evaluate on Held-Out Test
model_pipeline.fit(X_train, y_train)
y_pred = model_pipeline.predict(X_test)

# 7. Compute Test Performance Metrics
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

n_test = len(y_test)
p_features = len(model_pipeline.named_steps["ols"].coef_)
adj_r2 = 1 - (1 - r2) * ((n_test - 1) / (n_test - p_features - 1))

print(f"Test RMSE:     ${rmse:,.2f}")
print(f"Test MAE:      ${mae:,.2f}")
print(f"Test R^2:      {r2:.4f}")
print(f"Adjusted R^2:  {adj_r2:.4f}")
```

---

### 8.2 Inspecting Standardized Regression Weights

```python
# Extract feature names after transformation
ohe_feature_names = model_pipeline.named_steps["prep"].named_transformers_["cat"].named_steps["onehot"].get_feature_names_out(cat_cols)
all_feature_names = num_cols + list(ohe_feature_names)
coefficients = model_pipeline.named_steps["ols"].coef_

coef_df = pd.DataFrame({
    "Feature": all_feature_names,
    "Standardized_Coefficient": coefficients
}).sort_values(by="Standardized_Coefficient", ascending=False)

print("\nTop Positive & Negative Features by Influence:")
print(coef_df.to_string(index=False))
```

---

### 8.3 Core Diagnostic Visualizations

```python
residuals = y_test - y_pred

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Predicted vs. Actual
axes[0].scatter(y_test, y_pred, alpha=0.25, color="teal", edgecolors="none")
axes[0].plot([y.min(), y.max()], [y.min(), y.max()], "r--", linewidth=2, label="Perfect Fit (y = x)")
axes[0].set_xlabel("Actual Median House Value ($)")
axes[0].set_ylabel("Predicted Median House Value ($)")
axes[0].set_title(f"Predicted vs. Actual (R^2 = {r2:.3f})")
axes[0].legend()
axes[0].grid(True, linestyle=":", alpha=0.6)

# Plot 2: Residuals vs. Fitted Values
axes[1].scatter(y_pred, residuals, alpha=0.25, color="purple", edgecolors="none")
axes[1].axhline(0, color="black", linestyle="--", linewidth=2)
axes[1].set_xlabel("Fitted Values y_hat ($)")
axes[1].set_ylabel("Residuals e = y - y_hat ($)")
axes[1].set_title("Residuals vs. Fitted Values (Checking Homoscedasticity)")
axes[1].grid(True, linestyle=":", alpha=0.6)

plt.tight_layout()
plt.show()
```

#### Diagnostic Takeaway
In Plot 2, observe the horizontal ceiling cap at $y = 500,001$ present in the California housing dataset (censored data). Furthermore, notice the widening fan shape as $\\hat{y}$ increases, signaling **heteroscedasticity**—the exact statistical violation explored in Lecture 4."""
        }
    ],
    "quiz": {
        "title": "Comprehensive Examination: Linear Regression Deep Dive & Optimization",
        "description": "25-question examination testing vector dot product formulation, OLS derivation, Normal Equations, Batch vs. Stochastic Gradient Descent, feature scaling condition numbers, evaluation metrics, and coefficient interpretation.",
        "time_limit": "30 mins",
        "questions": [
            {
                "id": "q-cml-l03-01",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "The Intercept Trick",
                "question": "In linear regression mathematical notation, what is the purpose of the 'intercept trick' (introducing a dummy feature x_0 = 1)?",
                "options": [
                    {"id": "opt-1", "text": "To convert the hypothesis into a non-linear quadratic polynomial.", "is_correct": False},
                    {"id": "opt-2", "text": "To pack both the intercept theta_0 and feature weights theta_1...theta_d into a single compact vector dot product theta^T x.", "is_correct": True},
                    {"id": "opt-3", "text": "To eliminate the need for training labels y.", "is_correct": False},
                    {"id": "opt-4", "text": "To ensure that the residual error is identically equal to zero.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "By defining x_0 = 1 and appending it to feature vector x, the linear hypothesis h_theta(x) = theta_0 + theta_1 x_1 + ... + theta_d x_d simplifies to the vector dot product theta^T x, enabling vectorized matrix operations."
            },
            {
                "id": "q-cml-l03-02",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "OLS Objective Function",
                "question": "What is the mathematical cost function J(theta) minimized by Ordinary Least Squares linear regression?",
                "options": [
                    {"id": "opt-1", "text": "J(theta) = sum |y_i - h_theta(x_i)|", "is_correct": False},
                    {"id": "opt-2", "text": "J(theta) = (1/2) sum (h_theta(x_i) - y_i)^2", "is_correct": True},
                    {"id": "opt-3", "text": "J(theta) = - sum [y_i log(h_theta(x_i))]", "is_correct": False},
                    {"id": "opt-4", "text": "J(theta) = max |y_i - h_theta(x_i)|", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Ordinary Least Squares minimizes the sum of squared differences between predictions and true labels: J(theta) = (1/2) sum (h_theta(x_i) - y_i)^2. The factor (1/2) is introduced for convenience when differentiating."
            },
            {
                "id": "q-cml-l03-03",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Normal Equation Matrix Formula",
                "question": "What is the closed-form analytical solution (the Normal Equation) for the optimal parameter vector theta in Ordinary Least Squares?",
                "options": [
                    {"id": "opt-1", "text": "theta = (X X^T)^(-1) X y", "is_correct": False},
                    {"id": "opt-2", "text": "theta = (X^T X)^(-1) X^T y", "is_correct": True},
                    {"id": "opt-3", "text": "theta = X^T (X X^T)^(-1) y", "is_correct": False},
                    {"id": "opt-4", "text": "theta = X^T y / (X^T X)", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Setting the matrix gradient of J(theta) to zero yields X^T X theta = X^T y. Assuming X^T X is invertible, pre-multiplying by (X^T X)^(-1) gives theta = (X^T X)^(-1) X^T y."
            },
            {
                "id": "q-cml-l03-04",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Gradient Descent Learning Rate",
                "question": "In gradient descent optimization, what occurs if the learning rate alpha is set excessively large?",
                "options": [
                    {"id": "opt-1", "text": "The algorithm will converge instantaneously in a single iteration.", "is_correct": False},
                    {"id": "opt-2", "text": "The cost function J(theta) may oscillate wildly, overshoot the minimum, and diverge to infinity.", "is_correct": True},
                    {"id": "opt-3", "text": "The algorithm will convert into closed-form OLS.", "is_correct": False},
                    {"id": "opt-4", "text": "The feature weights will all become strictly zero.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "If alpha is too large, the parameter updates overshoot the bottom of the convex bowl, stepping across to regions of higher cost and causing the optimization trajectory to diverge."
            },
            {
                "id": "q-cml-l03-05",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Simultaneous Parameter Updates",
                "question": "In batch gradient descent for linear regression, why must all parameters theta_0, theta_1, ..., theta_d be updated SIMULTANEOUSLY?",
                "options": [
                    {"id": "opt-1", "text": "To prevent Scikit-Learn from throwing a threading exception.", "is_correct": False},
                    {"id": "opt-2", "text": "To ensure that every partial derivative is computed using the identical old parameter state theta before any parameter is overwritten.", "is_correct": True},
                    {"id": "opt-3", "text": "Because simultaneous updates make J(theta) non-convex.", "is_correct": False},
                    {"id": "opt-4", "text": "To ensure that all features receive identical weights.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Simultaneous updating ensures that the gradient vector represents the true slope of the loss surface at the current point theta_old. Updating parameters sequentially would evaluate subsequent derivatives at altered parameter locations."
            },
            {
                "id": "q-cml-l03-06",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Holdout Metric Units",
                "question": "Which of the following regression evaluation metrics is expressed in the EXACT SAME physical measurement units as the target variable y?",
                "options": [
                    {"id": "opt-1", "text": "Mean Squared Error (MSE)", "is_correct": False},
                    {"id": "opt-2", "text": "Root Mean Squared Error (RMSE)", "is_correct": True},
                    {"id": "opt-3", "text": "Coefficient of Determination (R-squared)", "is_correct": False},
                    {"id": "opt-4", "text": "Variance Inflation Factor (VIF)", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "RMSE takes the square root of MSE, returning the metric back to the original units of y (e.g., dollars, meters, degrees). MSE is in squared units, while R^2 is a dimensionless ratio."
            },
            {
                "id": "q-cml-l03-07",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Coefficient Interpretation Basics",
                "question": "In an unstandardized multiple linear regression model predicting house prices, the coefficient on 'median_income' (measured in tens of thousands of dollars) is +40,000. How is this interpreted?",
                "options": [
                    {"id": "opt-1", "text": "Raising a neighborhood's income by $10,000 will directly cause house prices to rise by $40,000.", "is_correct": False},
                    {"id": "opt-2", "text": "Holding all other features in the model fixed, a 1-unit ($10,000) increase in median income is associated with an expected $40,000 increase in predicted house price.", "is_correct": True},
                    {"id": "opt-3", "text": "Income explains exactly 40% of the total variance in house prices.", "is_correct": False},
                    {"id": "opt-4", "text": "The model has an RMSE of $40,000.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Regression coefficients represent partial slopes under ceteris paribus ('holding other variables constant'). They indicate associative correlation within the model, not proven physical causation."
            },
            {
                "id": "q-cml-l03-08",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "R-squared Baseline Definition",
                "question": "What is the reference baseline model against which R^2 compares the fitted regression model?",
                "options": [
                    {"id": "opt-1", "text": "A baseline predicting zero (y_hat = 0) for all observations.", "is_correct": False},
                    {"id": "opt-2", "text": "A horizontal baseline predicting the sample mean of the target variable (y_hat = y_bar) for all observations.", "is_correct": True},
                    {"id": "opt-3", "text": "A random uniform number generator.", "is_correct": False},
                    {"id": "opt-4", "text": "A Decision Tree with unlimited depth.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "R^2 = 1 - (SSE / SST). SST measures the squared dispersion around the horizontal mean baseline y_bar. An R^2 of 0 indicates the model performs no better than predicting y_bar for every sample."
            },
            {
                "id": "q-cml-l03-09",
                "type": "multiple_choice",
                "difficulty": "medium",
                "subtopic": "Convexity of OLS Cost",
                "question": "Which of the following statements correctly describe the mathematical properties of the OLS cost function J(theta)? (Select all that apply)",
                "options": [
                    {"id": "opt-1", "text": "For linear models, J(theta) is a strictly convex quadratic bowl if X^T X is positive definite.", "is_correct": True},
                    {"id": "opt-2", "text": "J(theta) contains numerous saddle points and local minima that trap gradient descent.", "is_correct": False},
                    {"id": "opt-3", "text": "At the global minimum of J(theta), the gradient vector nabla J(theta) is equal to zero.", "is_correct": True},
                    {"id": "opt-4", "text": "The Hessian matrix of J(theta) is given by X^T X.", "is_correct": True}
                ],
                "correctOptionIds": ["opt-1", "opt-3", "opt-4"],
                "explanation": "The OLS cost function is a quadratic form in theta whose Hessian is X^T X. When X has full column rank, X^T X is positive definite, making J(theta) strictly convex with a single unique global minimum and zero local minima (Option 2 is false)."
            },
            {
                "id": "q-cml-l03-10",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Normal Equation vs Gradient Descent Trade-off",
                "question": "When would a machine learning engineer choose Gradient Descent (e.g., SGDRegressor) over the closed-form Normal Equation (LinearRegression)?",
                "options": [
                    {"id": "opt-1", "text": "When the feature dimensionality d is very large (e.g., d > 50,000) or data arrives in a continuous stream.", "is_correct": True},
                    {"id": "opt-2", "text": "Only when the target variable y is discrete.", "is_correct": False},
                    {"id": "opt-3", "text": "Whenever R^2 is below 0.50.", "is_correct": False},
                    {"id": "opt-4", "text": "When we refuse to perform feature scaling.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "Inverting the (d+1) x (d+1) matrix in the Normal Equation requires O(d^3) operations, which becomes computationally prohibitive when d is large. Gradient descent scales linearly in d per iteration and supports out-of-core streaming."
            },
            {
                "id": "q-cml-l03-11",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Feature Scaling for Optimization",
                "question": "Why does Z-score feature standardization accelerate the convergence rate of Gradient Descent in linear regression?",
                "options": [
                    {"id": "opt-1", "text": "It eliminates the need to compute partial derivatives.", "is_correct": False},
                    {"id": "opt-2", "text": "It spherizes the elliptical loss contours of J(theta), reducing the condition number and allowing gradients to point directly toward the minimum without oscillation.", "is_correct": True},
                    {"id": "opt-3", "text": "It guarantees that the model will achieve an R^2 of 1.0.", "is_correct": False},
                    {"id": "opt-4", "text": "It forces all parameters to update sequentially.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "When feature scales are disparate, level curves of J(theta) are elongated ellipses with high condition numbers, causing gradients to oscillate wildly perpendicular to the valley. Scaling makes contours circular, enabling direct descent."
            },
            {
                "id": "q-cml-l03-12",
                "type": "multiple_choice",
                "difficulty": "medium",
                "subtopic": "Batch GD vs SGD vs Mini-Batch",
                "question": "Which of the following statements correctly compare Gradient Descent variants? (Select all that apply)",
                "options": [
                    {"id": "opt-1", "text": "Batch GD computes exact gradients using all m samples, producing a smooth monotonic trajectory toward the minimum.", "is_correct": True},
                    {"id": "opt-2", "text": "Stochastic GD (SGD) updates parameters using 1 sample per step, introducing noisy oscillations that can help escape shallow local plateaus.", "is_correct": True},
                    {"id": "opt-3", "text": "Mini-Batch GD balances vectorization hardware efficiency (GPUs) with gradient stability by using small sample batches (e.g., 32-256).", "is_correct": True},
                    {"id": "opt-4", "text": "SGD requires significantly more memory than Batch GD because it stores multiple gradient matrices.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-1", "opt-2", "opt-3"],
                "explanation": "Options 1, 2, and 3 are correct. Option 4 is false: SGD processes one sample at a time and has minimal memory overhead compared to full-batch GD."
            },
            {
                "id": "q-cml-l03-13",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "MAE vs RMSE Comparison",
                "question": "An environmental agency is predicting atmospheric pollutant levels. In evaluating two models, Model A has MAE = 12, RMSE = 14. Model B has MAE = 11, RMSE = 28. What does the large gap between MAE and RMSE in Model B indicate?",
                "options": [
                    {"id": "opt-1", "text": "Model B has lower overall variance than Model A.", "is_correct": False},
                    {"id": "opt-2", "text": "Model B makes occasional severe, large-magnitude outlier errors that are heavily penalized by the squared term in RMSE.", "is_correct": True},
                    {"id": "opt-3", "text": "Model B was trained without an intercept term.", "is_correct": False},
                    {"id": "opt-4", "text": "Model A has perfect correlation.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "RMSE squares errors before averaging. When a model has a low MAE but a high RMSE, it indicates that while most errors are small, the model produces occasional extreme outlier errors that heavily inflate RMSE."
            },
            {
                "id": "q-cml-l03-14",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Adjusted R-squared Role",
                "question": "An analyst adds 50 completely random noise variables into a linear regression model. What will happen to the training R^2 and the Adjusted R^2?",
                "options": [
                    {"id": "opt-1", "text": "Both R^2 and Adjusted R^2 will increase substantially.", "is_correct": False},
                    {"id": "opt-2", "text": "R^2 will increase (or stay constant), while Adjusted R^2 will decrease.", "is_correct": True},
                    {"id": "opt-3", "text": "Both R^2 and Adjusted R^2 will automatically drop to 0.", "is_correct": False},
                    {"id": "opt-4", "text": "Adjusted R^2 will become exactly equal to MAE.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Standard R^2 never decreases when adding features because OLS can always assign small weights to reduce training SSE. Adjusted R^2 penalizes the loss of degrees of freedom (m - d - 1) and will decrease if the new features do not add predictive value."
            },
            {
                "id": "q-cml-l03-15",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Geometric Orthogonality of Residuals",
                "question": "In the geometric vector space formulation of Ordinary Least Squares, what is the geometric relationship between the residual error vector e = y - X theta and the column space Col(X)?",
                "options": [
                    {"id": "opt-1", "text": "The residual vector e lies strictly inside the column space Col(X).", "is_correct": False},
                    {"id": "opt-2", "text": "The residual vector e is orthogonal (perpendicular) to every column vector in X, meaning X^T e = 0.", "is_correct": True},
                    {"id": "opt-3", "text": "The residual vector e is parallel to the target vector y.", "is_correct": False},
                    {"id": "opt-4", "text": "The angle between e and Col(X) is exactly 45 degrees.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "By the Orthogonal Projection Theorem, the minimum distance from y to the subspace Col(X) occurs when the error vector e is orthogonal to the subspace, which mathematically yields the condition X^T e = X^T (y - X theta) = 0."
            },
            {
                "id": "q-cml-l03-16",
                "type": "multiple_choice",
                "difficulty": "medium",
                "subtopic": "Negative R-squared Conditions",
                "question": "Under which of the following conditions can R^2 be mathematically NEGATIVE? (Select all that apply)",
                "options": [
                    {"id": "opt-1", "text": "When evaluated on an unseen test set where the model's predictions have larger residual error than simply predicting the training target mean y_bar.", "is_correct": True},
                    {"id": "opt-2", "text": "When fitting an unconstrained linear regression without an intercept term on non-centered data.", "is_correct": True},
                    {"id": "opt-3", "text": "When training an ordinary linear regression with an intercept on the training set using an exact OLS solver.", "is_correct": False},
                    {"id": "opt-4", "text": "When the model is heavily overfitted to training noise and fails to generalize to test data.", "is_correct": True}
                ],
                "correctOptionIds": ["opt-1", "opt-2", "opt-4"],
                "explanation": "On unseen test data, an overfitted model can produce predictions with SSE > SST, resulting in R^2 < 0. Similarly, fitting without an intercept on training data can yield negative R^2. On training data with an intercept, OLS guarantees 0 <= R^2 <= 1 (Option 3 is false)."
            },
            {
                "id": "q-cml-l03-17",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Standardized vs Unstandardized Weights",
                "question": "A model predicts customer spending y: y_hat = 150 + 0.02 * income + 50 * visits. Income has mean $50,000, std $15,000. Visits has mean 3, std 1. Why is comparing 0.02 to 50 misleading for assessing feature importance?",
                "options": [
                    {"id": "opt-1", "text": "Because visits has a higher p-value.", "is_correct": False},
                    {"id": "opt-2", "text": "Because raw coefficients depend on measurement units; a 1-std shift in income ($15,000 * 0.02 = $300) actually affects predictions six times more than a 1-std shift in visits (1 * 50 = $50).", "is_correct": True},
                    {"id": "opt-3", "text": "Because the intercept term absorbs the effect of income.", "is_correct": False},
                    {"id": "opt-4", "text": "Because linear regression cannot accept two features simultaneously.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Raw coefficients reflect measurement scales (dollars vs count). To compare feature importance fairly, one must inspect standardized coefficients, which scale the weights by feature standard deviations."
            },
            {
                "id": "q-cml-l03-18",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Matrix Rank & Singularity",
                "question": "Suppose a design matrix X has dimensions 1,000 x 5 (1,000 rows, 4 features + intercept). Feature column 4 is exactly equal to 3 * column 2 - 2 * column 3. What is the mathematical consequence when attempting to solve theta = (X^T X)^(-1) X^T y?",
                "options": [
                    {"id": "opt-1", "text": "The matrix X^T X is strictly singular (determinant = 0) and non-invertible, causing the analytical OLS solver to fail.", "is_correct": True},
                    {"id": "opt-2", "text": "The learning rate automatically increases by a factor of 3.", "is_correct": False},
                    {"id": "opt-3", "text": "The model's R^2 becomes 1.0.", "is_correct": False},
                    {"id": "opt-4", "text": "Gradient descent will converge in exactly 1 iteration.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "Because column 4 is an exact linear combination of columns 2 and 3, X does not have full column rank (rank = 4 instead of 5). Consequently, X^T X has a zero eigenvalue, determinant 0, and is non-invertible."
            },
            {
                "id": "q-cml-l03-19",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Hessian Condition Number Bounds",
                "question": "In optimizing linear regression via Batch Gradient Descent, if the maximum eigenvalue of the Hessian matrix H = X^T X is lambda_max = 500, what is the theoretical upper bound on learning rate alpha to ensure convergence?",
                "options": [
                    {"id": "opt-1", "text": "alpha < 2 / lambda_max = 0.004", "is_correct": True},
                    {"id": "opt-2", "text": "alpha < 500", "is_correct": False},
                    {"id": "opt-3", "text": "alpha > 1 / 500", "is_correct": False},
                    {"id": "opt-4", "text": "alpha = 1.0", "is_correct": False}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "In convex quadratic optimization, the spectral radius of the iteration matrix (I - alpha H) must be strictly less than 1 for convergence, which mandates 0 < alpha < 2 / lambda_max. Here, 2 / 500 = 0.004."
            },
            {
                "id": "q-cml-l03-20",
                "type": "multiple_choice",
                "difficulty": "hard",
                "subtopic": "Gauss-Markov Theorem Conditions",
                "question": "According to the Gauss-Markov Theorem, under what conditions is the Ordinary Least Squares estimator theta_hat the Best Linear Unbiased Estimator (BLUE)? (Select all that apply)",
                "options": [
                    {"id": "opt-1", "text": "The error terms have an expected value of zero: E[epsilon | X] = 0.", "is_correct": True},
                    {"id": "opt-2", "text": "The error terms are homoscedastic: Var(epsilon_i | X) = sigma^2 for all i.", "is_correct": True},
                    {"id": "opt-3", "text": "The error terms are uncorrelated: Cov(epsilon_i, epsilon_j | X) = 0 for all i != j.", "is_correct": True},
                    {"id": "opt-4", "text": "The error terms must follow a strictly Gaussian distribution for OLS to be BLUE.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-1", "opt-2", "opt-3"],
                "explanation": "The Gauss-Markov theorem states that OLS is BLUE (minimum variance among linear unbiased estimators) under zero conditional mean, homoscedasticity, and no autocorrelation. Crucially, normality is NOT required for BLUE (it is only needed for exact hypothesis tests and CIs). Option 4 is false."
            },
            {
                "id": "q-cml-l03-21",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Omitted Variable Bias Derivation",
                "question": "Suppose the true data-generating process is y = beta_1 x_1 + beta_2 x_2 + epsilon. An analyst omits x_2 and fits the simple regression y = alpha_1 x_1 + u. What is the expected value of the estimated coefficient alpha_hat_1?",
                "options": [
                    {"id": "opt-1", "text": "E[alpha_hat_1] = beta_1 + beta_2 * Cov(x_1, x_2) / Var(x_1)", "is_correct": True},
                    {"id": "opt-2", "text": "E[alpha_hat_1] = beta_1", "is_correct": False},
                    {"id": "opt-3", "text": "E[alpha_hat_1] = beta_1 * beta_2", "is_correct": False},
                    {"id": "opt-4", "text": "E[alpha_hat_1] = 0", "is_correct": False}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "This is the classic Omitted Variable Bias formula: E[alpha_hat_1] = beta_1 + beta_2 * (Cov(x_1, x_2) / Var(x_1)). The omitted variable biases the estimated coefficient unless beta_2 = 0 or x_1 and x_2 are uncorrelated."
            },
            {
                "id": "q-cml-l03-22",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Adjusted R-squared Calculation",
                "question": "A model evaluated on a test set of m = 101 samples with d = 10 features achieves an R^2 of 0.80. What is the Adjusted R^2 for this test set?",
                "options": [
                    {"id": "opt-1", "text": "0.7778", "is_correct": True},
                    {"id": "opt-2", "text": "0.8000", "is_correct": False},
                    {"id": "opt-3", "text": "0.7200", "is_correct": False},
                    {"id": "opt-4", "text": "0.8222", "is_correct": False}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "Formula: Adj R^2 = 1 - (1 - R^2) * [(m - 1) / (m - d - 1)]. Here, m = 101, d = 10, so m - 1 = 100, and m - d - 1 = 101 - 10 - 1 = 90. Adj R^2 = 1 - (1 - 0.80) * (100 / 90) = 1 - 0.20 * 1.1111 = 1 - 0.2222 = 0.7778."
            },
            {
                "id": "q-cml-l03-23",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Hat Matrix & Leverage",
                "question": "In linear regression matrix algebra, the 'Hat Matrix' H is defined as H = X (X^T X)^(-1) X^T, mapping y to predictions y_hat = H y. What mathematical properties characterize the Hat Matrix?",
                "options": [
                    {"id": "opt-1", "text": "H is symmetric (H^T = H) and idempotent (H^2 = H).", "is_correct": True},
                    {"id": "opt-2", "text": "H is an upper triangular matrix with zero trace.", "is_correct": False},
                    {"id": "opt-3", "text": "H is always an invertible matrix of full rank m.", "is_correct": False},
                    {"id": "opt-4", "text": "H has eigenvalues strictly equal to 2.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "As an orthogonal projection operator, the Hat Matrix H satisfies symmetry H^T = H and idempotence H^2 = H * H = H (projecting an already projected vector changes nothing). Its rank equals trace(H) = d + 1."
            },
            {
                "id": "q-cml-l03-24",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "LMS Stochastic Gradient Derivation",
                "question": "For a single observation (x, y) with cost J_i(theta) = (1/2) (h_theta(x) - y)^2, what is the exact gradient update rule for parameter theta_j?",
                "options": [
                    {"id": "opt-1", "text": "theta_j := theta_j + alpha * (y - h_theta(x)) * x_j", "is_correct": True},
                    {"id": "opt-2", "text": "theta_j := theta_j - alpha * (y - h_theta(x)) * x_j", "is_correct": False},
                    {"id": "opt-3", "text": "theta_j := theta_j - alpha * (h_theta(x) - y)^2", "is_correct": False},
                    {"id": "opt-4", "text": "theta_j := theta_j + alpha * x_j", "is_correct": False}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "By chain rule, dJ_i/dtheta_j = (h_theta(x) - y) * x_j. The descent step is theta_j := theta_j - alpha * (h_theta(x) - y) * x_j = theta_j + alpha * (y - h_theta(x)) * x_j. This is the Widrow-Hoff / LMS update rule."
            },
            {
                "id": "q-cml-l03-25",
                "type": "multiple_choice",
                "difficulty": "hard",
                "subtopic": "Scikit-Learn OLS Solver Architecture",
                "question": "How does Scikit-Learn's LinearRegression class compute optimal coefficients under the hood? (Select all that apply)",
                "options": [
                    {"id": "opt-1", "text": "It uses scipy.linalg.lstsq, which computes the solution via Singular Value Decomposition (SVD) of matrix X rather than explicitly inverting X^T X.", "is_correct": True},
                    {"id": "opt-2", "text": "It executes an iterative from-scratch batch gradient descent loop with learning rate 0.01.", "is_correct": False},
                    {"id": "opt-3", "text": "Using SVD avoids numerical instability and handles rank-deficient matrices via the pseudoinverse.", "is_correct": True},
                    {"id": "opt-4", "text": "It computes parameter estimates using closed-form analytical least squares.", "is_correct": True}
                ],
                "correctOptionIds": ["opt-1", "opt-3", "opt-4"],
                "explanation": "Scikit-Learn's LinearRegression wraps scipy.linalg.lstsq, which uses LAPACK's DGELSD driver based on SVD of X. This analytical solver avoids explicitly computing the ill-conditioned product X^T X and handles singularities gracefully. It does NOT use gradient descent (Option 2 is false; SGDRegressor does)."
            }
        ]
    }
}
