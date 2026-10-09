# Lecture 5: Gradient Descent — Optimization Foundations
## Student Notes — SST Classical Machine Learning

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Explain why iterative first-order optimization is necessary when the analytical closed form ($\mathcal{O}(d^3)$) fails or does not exist (e.g., Logistic Regression, Neural Networks).
- Derive the exact gradient $\nabla_{\boldsymbol{\theta}} J(\boldsymbol{\theta})$ for Ordinary Least Squares and prove that **$\text{Gradient} = \text{Error} \times \text{Feature}$**.
- Explain how the algorithm **naturally brakes itself** as it approaches stationary points without requiring manual step-size reductions.
- Formulate the **vectorized update rule** $\boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \frac{\alpha}{n} X^T (X\boldsymbol{\theta} - \mathbf{y})$ and verify matrix dimensional compatibility.
- Prove that the OLS cost function is **strictly convex** by analyzing its Hessian matrix $\nabla^2 J(\boldsymbol{\theta})$.
- Diagnose learning rate problems by reading **Loss vs. Iteration curves** (detecting crawling convergence, healthy decay, oscillation, and catastrophic divergence to `NaN`).
- Compare **Batch Gradient Descent**, **Stochastic Gradient Descent (SGD)**, and **Mini-Batch Gradient Descent** across computation time, memory footprints, and convergence paths.
- Explain geometrically and algebraically why **Feature Standardization** converts narrow elliptical loss ravines into spherical bowls, drastically accelerating convergence.

---

## 1. The Foggy Mountain Metaphor: Why Optimization?

Imagine you are hiking on a mountain engulfed in dense fog:
- You cannot see the valley floor (the global minimum of cost $J$).
- However, you can **feel the slope of the ground** under your boots at your current coordinates.
- To descend, you feel the direction of steepest upward incline, turn $180^\circ$ around, and take a step downward.
- By repeating this local greedy strategy, you eventually reach the bottom of the basin.

```
       Descending a Hill in the Fog:
       J(θ)
        ▲
        │           \  Start: High Cost
        │            \ ◄── Slope is steep! Step is large.
        │             \
        │              \
        │               \___
        │                   \___ ◄── Slope flattens! Step automatically brakes.
        │                       \___•─── Global Minimum: ∇J = 0
        └────────────────────────────────────────► θ
```

### Why Not Always Use the Normal Equation?
1. **Computational Bottleneck**: The closed-form Normal Equation requires inverting the matrix $(X^T X)$, costing $\mathcal{O}(d^3)$ operations. If $d = 100,000$ (e.g., bag-of-words text features), inverting this matrix requires millions of gigabytes of RAM and days of compute.
2. **Non-Existent Closed Forms**: In Logistic Regression, Support Vector Machines, and Deep Neural Networks, no analytical closed-form solution exists. **Iterative numerical optimization is the universal workhorse of modern AI.**

---

## 2. Deriving the Gradient: Error $\times$ Feature

Recall the Mean Squared Error cost function:

$$J(\boldsymbol{\theta}) = \frac{1}{2n} \sum_{i=1}^n \left( h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) - y^{(i)} \right)^2 = \frac{1}{2n} \sum_{i=1}^n \left( \sum_{j=0}^d \theta_j x_j^{(i)} - y^{(i)} \right)^2$$

### Differentiating with Respect to $\theta_j$
Applying the chain rule of calculus:

$$\frac{\partial J(\boldsymbol{\theta})}{\partial \theta_j} = \frac{1}{2n} \sum_{i=1}^n 2 \left( h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) - y^{(i)} \right) \cdot \frac{\partial}{\partial \theta_j}\left( \sum_{k=0}^d \theta_k x_k^{(i)} - y^{(i)} \right)$$
$$\frac{\partial J(\boldsymbol{\theta})}{\partial \theta_j} = \frac{1}{n} \sum_{i=1}^n \underbrace{\left( h_{\boldsymbol{\theta}}(\mathbf{x}^{(i)}) - y^{(i)} \right)}_{\text{Scalar Error on Example } i} \cdot \underbrace{x_j^{(i)}}_{\text{Value of Feature } j}$$

> [!IMPORTANT]
> **The Universal Pattern to Memorize**:  
> The gradient component for parameter $j$ is the average product of the **model error** and the **$j$-th feature value**:
> $$\nabla_{\theta_j} J = \frac{1}{n} \sum_{i=1}^n (\hat{y}^{(i)} - y^{(i)}) x_j^{(i)}$$
> *Notice: This exact mathematical structure reappears unchanged in Logistic Regression (Lecture 8) and Neural Network Backpropagation!*

### The Parameter Update Rule
Because the gradient $\nabla J$ points in the direction of **steepest ascent**, we update parameters in the opposite direction:

$$\theta_j \leftarrow \theta_j - \alpha \frac{\partial J(\boldsymbol{\theta})}{\partial \theta_j}$$

where $\alpha > 0$ is the **learning rate** (step size).

### Why the Algorithm Brakes Itself
Notice that the step magnitude taken in parameter space is:

$$\Delta \theta_j = \alpha \left| \frac{\partial J}{\partial \theta_j} \right|$$

As $\boldsymbol{\theta}$ approaches the stationary minimum, the slope $\frac{\partial J}{\partial \theta_j} \to 0$. Therefore, **the parameter updates automatically shrink to zero without needing to reduce $\alpha$**.

---

## 3. Vectorized Formulation & Convexity

### Vectorizing the Gradient Across All $n$ Examples
Stacking all partial derivatives into the full gradient vector $\nabla_{\boldsymbol{\theta}} J \in \mathbb{R}^{d+1}$:

$$\nabla_{\boldsymbol{\theta}} J(\boldsymbol{\theta}) = \begin{bmatrix} \frac{\partial J}{\partial \theta_0} \\ \frac{\partial J}{\partial \theta_1} \\ \vdots \\ \frac{\partial J}{\partial \theta_d} \end{bmatrix} = \frac{1}{n} X^T \left( X \boldsymbol{\theta} - \mathbf{y} \right)$$

#### Dimensionality Verification:
- $X \in \mathbb{R}^{n \times (d+1)}$
- $\boldsymbol{\theta} \in \mathbb{R}^{(d+1) \times 1} \implies X\boldsymbol{\theta} \in \mathbb{R}^{n \times 1}$
- $(X\boldsymbol{\theta} - \mathbf{y}) \in \mathbb{R}^{n \times 1}$ (The error vector $\mathbf{e}$)
- $X^T \in \mathbb{R}^{(d+1) \times n}$
- $X^T \mathbf{e} \in \mathbb{R}^{(d+1) \times 1}$ (Matches dimension of $\boldsymbol{\theta}$ exactly!)

### The Full Vectorized Update Equation

$$\boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \frac{\alpha}{n} X^T \left( X \boldsymbol{\theta} - \mathbf{y} \right)$$

### Mathematical Proof of Convexity
A function is strictly convex if its Hessian matrix $H = \nabla^2 J(\boldsymbol{\theta})$ is positive semi-definite ($H \succeq 0$).

$$H_{jk} = \frac{\partial^2 J}{\partial \theta_j \partial \theta_k} = \frac{1}{n} \sum_{i=1}^n x_j^{(i)} x_k^{(i)} \implies H = \frac{1}{n} X^T X$$

For any arbitrary non-zero vector $\mathbf{v} \in \mathbb{R}^{d+1}$:

$$\mathbf{v}^T H \mathbf{v} = \mathbf{v}^T \left( \frac{1}{n} X^T X \right) \mathbf{v} = \frac{1}{n} (X\mathbf{v})^T (X\mathbf{v}) = \frac{1}{n} \|X\mathbf{v}\|_2^2 \ge 0$$

Since $\|X\mathbf{v}\|_2^2 \ge 0$ for all $\mathbf{v}$, the Hessian is **positive semi-definite**.  
**Conclusion**: For linear regression, $J(\boldsymbol{\theta})$ is a global quadratic bowl. There are **zero local minima**, zero saddle points, and no deceptive ravines. Gradient descent is mathematically guaranteed to converge to the unique global minimum (provided $\alpha$ is bounded).

---

## 4. Hand-Worked Example: One Full Iteration by Hand

To demystify the linear algebra, consider a minimal toy dataset with $n = 2$ points and $d = 1$ feature:

$$\text{Point 1: } (x^{(1)}, y^{(1)}) = (1, 2), \quad \text{Point 2: } (x^{(2)}, y^{(2)}) = (2, 3)$$

Let initial weights be $\theta_0 = 0, \theta_1 = 0$, and learning rate $\alpha = 0.1$.

```
   Step 0: Initial Predictions (h_θ(x) = 0 + 0·x = 0)
   - Point 1: ŷ₁ = 0  ──►  Error e₁ = (0 - 2) = -2
   - Point 2: ŷ₂ = 0  ──►  Error e₂ = (0 - 3) = -3
   - Initial Cost J(0, 0) = (1 / 4) * [ (-2)² + (-3)² ] = (4 + 9)/4 = 3.25

   Step 1: Compute Gradients
   - ∂J / ∂θ₀ = (1 / 2) * [ e₁·1 + e₂·1 ] = (1 / 2) * [ -2(1) + -3(1) ] = -2.5
   - ∂J / ∂θ₁ = (1 / 2) * [ e₁·x₁ + e₂·x₂ ] = (1 / 2) * [ -2(1) + -3(2) ] = (1 / 2) * [ -2 - 6 ] = -4.0

   Step 2: Update Parameters
   - θ₀_new = 0 - (0.1) * (-2.5) = +0.25
   - θ₁_new = 0 - (0.1) * (-4.0) = +0.40

   Step 3: Check Cost After One Step
   - New Hypothesis: h_θ(x) = 0.25 + 0.40·x
   - New Predictions: ŷ₁ = 0.25 + 0.4(1) = 0.65;  ŷ₂ = 0.25 + 0.4(2) = 1.05
   - New Errors: e₁ = (0.65 - 2) = -1.35;  e₂ = (1.05 - 3) = -1.95
   - New Cost J(0.25, 0.40) = (1 / 4) * [ (-1.35)² + (-1.95)² ] = (1.8225 + 3.8025)/4 = 1.406
```
The cost dropped dramatically from **$3.25 \to 1.41$** in a single update step!

---

## 5. The Learning Rate ($\alpha$): Reading the Loss Curve

In practical machine learning engineering, **always plot Cost $J(\boldsymbol{\theta})$ versus Iteration (Epoch)**:

```
   DIAGNOSING LEARNING RATES FROM LOSS CURVES:
   J(θ)
    ▲
    │   \  α too large (Divergence / Exploding to NaN)
    │    \           /
    │     \  /\  /\ /
    │      \/  \/  \  α moderately too large (Oscillates endlessly)
    │
    │  ═════════════════════════════ α too small (Crawls, flatlines before optimum)
    │
    │   \
    │    \___
    │        \________ α well-tuned (Smooth asymptotic exponential decay)
    └────────────────────────────────────────► Iteration
```

1. **$\alpha$ Too Small**: Loss curve decreases at a glacial pace; appears horizontal. The model exhausts its computational epoch budget long before reaching the valley floor.
2. **$\alpha$ Well-Tuned**: Rapid initial descent that smoothly transitions into an asymptote, settling cleanly at the global minimum.
3. **$\alpha$ Moderately Too Large**: The update step overshoots the valley floor, oscillating back and forth across the opposing walls of the bowl.
4. **$\alpha$ Catastrophically Too Large ($\alpha > \frac{2}{\lambda_{\max}}$)**: The step overshoots the valley so severely that the new point lands higher up the opposite wall than where it started. Loss expands exponentially ($10^2 \to 10^8 \to 10^{35} \to \texttt{NaN}$ / floating-point overflow).

---

## 6. The Three Variants of Gradient Descent

```
   ┌────────────────────────────────────────────────────────────────────────────────┐
   │                       GRADIENT DESCENT TAXONOMY                                │
   ├───────────────────┬───────────────────┬────────────────────────────────────────┤
   │ Variant           │ Batch Size (B)    │ Trajectory on Loss Contour             │
   ├───────────────────┼───────────────────┼────────────────────────────────────────┤
   │ Batch GD          │ B = n (All points)│ Direct, deterministic, ultra-smooth    │
   ├───────────────────┼───────────────────┼────────────────────────────────────────┤
   │ Stochastic (SGD)  │ B = 1 (One point) │ Highly erratic, noisy, stochastic walk │
   ├───────────────────┼───────────────────┼────────────────────────────────────────┤
   │ Mini-Batch GD     │ 32 ≤ B ≤ 256      │ Balanced, mildly noisy, GPU-accelerated│
   └───────────────────┴───────────────────┴────────────────────────────────────────┘
```

```
   Convergence Trajectories on Level Set Contours:
         Batch GD (B = n):            Stochastic GD (B = 1):         Mini-Batch GD (B = 64):
         ╭────────────────╮            ╭────────────────╮            ╭────────────────╮
         │   ╭────────╮   │            │   ╭────────╮   │            │   ╭────────╮   │
         │  │    •    │  │            │  │  /\ •   │  │            │  │   / •  │  │
         │   ╰───▲────╯   │            │   ╰─/\─▼───╯   │            │   ╰──\─▲───╯   │
         │       │        │            │     \ /        │            │       \│       │
         │       • Start  │            │      • Start   │            │        • Start │
         ╰────────────────╯            ╰────────────────╯            ╰────────────────╯
         Smooth & direct               Erratic random walk           The golden industry
         O(nd) per step                Escapes bad plateaus          compromise
```

### Why Noise is Not a Flaw in SGD
While Batch GD computes the mathematically exact gradient, SGD's stochastic noise offers two hidden advantages:
1. **Computational Speed**: In massive datasets ($n = 10,000,000$), Batch GD takes 20 minutes to perform a single weight update. SGD performs $10,000,000$ updates in the same time.
2. **Regularization & Basin Escapes**: The stochastic jitter prevents the optimizer from getting trapped in shallow local troughs or saddle points in non-convex architectures.

---

## 7. Why Feature Scaling Accelerates Descent

Geometrically, the contours of $J(\boldsymbol{\theta})$ are level sets of the quadratic form $\boldsymbol{\theta}^T (X^T X) \boldsymbol{\theta}$.

- When feature $x_1$ has range $[0, 1]$ and feature $x_2$ has range $[0, 1,000,000]$, the Hessian matrix $X^T X$ has an extreme **condition number** ($\kappa = \frac{\lambda_{\max}}{\lambda_{\min}} \gg 10,000$).
- The loss surface becomes a **hyper-elongated elliptical canyon**.
- Because the gradient is orthogonal to the contour lines, the gradient vector points almost perpendicular to the direction of the true minimum. The optimizer wastes $99\%$ of its energy ricocheting violently between the steep canyon walls!

```
   Unscaled Feature Space (Canyon Ravine):       Scaled Feature Space (Spherical Bowl):
              θ₂                                            θ₂
              ▲                                             ▲
              │   ╭───────────────────────╮                 │       ╭─────╮
              │  │           •             │                │      │   •   │
              │   ╰──/\──/\──/\───────────╯                 │       ╰──▲──╯
              │     /  \/  \/  \                            │          │
              └───────────────────────────► θ₁              └──────────┴──► θ₁
              Wild oscillations across ravine;              Marches radially straight
              requires tiny α; takes 5,000 steps            to center; converges in 20 steps
```

Standardizing features ($\mu = 0, \sigma = 1$) conditions the Hessian so $\kappa \approx 1$. The elliptical contours become **concentric spheres**. The negative gradient points directly at the global minimum!

---

## 8. Complete From-Scratch Python Implementation

```python
"""
From-Scratch Vectorized Batch Gradient Descent vs. Scikit-Learn SGDRegressor
Demonstrates loss curve tracking and convergence verification.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor

# 1. Generate Synthetic Regression Problem
X_raw, y = make_regression(n_samples=500, n_features=2, noise=15.0, random_state=42)

# 2. Mandatory Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)

# Add dummy column x₀ = 1 for intercept
n_samples = X_scaled.shape[0]
X_design = np.hstack([np.ones((n_samples, 1)), X_scaled])

# 3. Vectorized Batch Gradient Descent Function
def batch_gradient_descent(X, y, alpha=0.05, max_epochs=200):
    n, d = X.shape
    theta = np.zeros(d) # Initialize weights to zeros
    cost_history = []
    
    for epoch in range(max_epochs):
        # Forward prediction
        y_pred = X @ theta
        error = y_pred - y
        
        # Mean Squared Error Cost: (1 / 2n) * ||e||²
        cost = (1.0 / (2.0 * n)) * np.dot(error, error)
        cost_history.append(cost)
        
        # Vectorized Gradient: (1 / n) * Xᵀ e
        gradient = (1.0 / n) * (X.T @ error)
        
        # Simultaneous Parameter Update
        theta = theta - alpha * gradient
        
    return theta, cost_history

# 4. Train Scratch Model
theta_scratch, loss_history = batch_gradient_descent(X_design, y, alpha=0.05, max_epochs=150)

# 5. Compare with Scikit-Learn SGDRegressor
sgd = SGDRegressor(max_iter=150, eta0=0.05, learning_rate="constant", penalty=None, random_state=42)
sgd.fit(X_scaled, y)

print("=" * 45)
print("PARAMETER RECOVERY VERIFICATION:")
print(f"Scratch Intercept (θ₀):   {theta_scratch[0]:.4f}")
print(f"Sklearn Intercept:        {sgd.intercept_[0]:.4f}")
print(f"Scratch Slopes (θ₁, θ₂):  {theta_scratch[1]:.4f}, {theta_scratch[2]:.4f}")
print(f"Sklearn Slopes:           {sgd.coef_[0]:.4f}, {sgd.coef_[1]:.4f}")
print("=" * 45)
print(f"Final Scratch Cost J(θ):  {loss_history[-1]:.4f}")
```

---

## 9. Common Pitfalls & Interview-Grade Questions

### Q1: In Batch Gradient Descent for linear regression, why is it mandatory that all parameters $\theta_0, \theta_1, \dots, \theta_d$ are updated *simultaneously*?
**Answer**:  
The gradient vector $\nabla_{\boldsymbol{\theta}} J(\boldsymbol{\theta})$ is mathematically defined at a specific coordinates vector $\boldsymbol{\theta}^{(t)}$ in parameter space. If an engineer updates $\theta_0$ first, and then calculates the partial derivative $\frac{\partial J}{\partial \theta_1}$ using the *new* $\theta_0^{(t+1)}$, they are no longer descending along the true gradient of $J$ at $\boldsymbol{\theta}^{(t)}$. Updating parameters sequentially using freshly updated coordinates alters the algorithm into **Gauss-Seidel / Coordinate Descent**, which follows an axis-aligned zigzag trajectory rather than the path of steepest gradient descent.

### Q2: Why does an excessively high learning rate ($\alpha$) cause the cost function to explode to `NaN` or positive infinity?
**Answer**:  
For a quadratic cost surface with maximum Hessian eigenvalue $\lambda_{\max}$, the step taken in parameter space is $\Delta \boldsymbol{\theta} = -\alpha \nabla J$. If $\alpha > \frac{2}{\lambda_{\max}}$, the step overshoots the valley floor so excessively that the new distance to the minimum $\|\boldsymbol{\theta}^{(t+1)} - \boldsymbol{\theta}^*\|$ is strictly greater than the initial distance $\|\boldsymbol{\theta}^{(t)} - \boldsymbol{\theta}^*\|$. With each successive iteration, the overshoot magnifies geometrically by a factor $(\alpha \lambda_{\max} - 1) > 1$. The error grows exponentially until the float64 IEEE-754 mantissa overflows into `+inf` and subsequently `NaN`.

### Q3: What is the primary operational trade-off between Stochastic Gradient Descent (SGD) and Mini-Batch Gradient Descent in modern computing hardware?
**Answer**:  
Pure SGD (batch size $B = 1$) evaluates memory row-by-row, which completely fails to utilize the **SIMD (Single Instruction, Multiple Data) matrix vectorization** engines in modern multi-core CPUs and GPUs. The arithmetic intensity (FLOPs per byte of memory bandwidth) is extremely low. **Mini-Batch GD** (batch sizes $B = 32, 64, 128$) bundles observations into matrix blocks, enabling BLAS Level-3 GEMM (General Matrix Multiply) operations that saturate GPU tensor cores while retaining the regularizing, noise-driven optimization benefits of SGD.

---

## 10. Summary & Key Takeaways

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                     SESSION 5 KEY TAKEAWAYS                            │
   ├────────────────────────────────────────────────────────────────────────┤
   │ 1. Optimization Necessity: Iterative gradient descent scales to        │
   │    millions of features where the O(d³) matrix inversion fails.        │
   │ 2. The Core Gradient Rule: ∇_θ J = (1/n) Xᵀ(Xθ - y). The gradient      │
   │    is always the average of (Error × Feature).                         │
   │ 3. Self-Braking Property: As the model nears the stationary minimum,   │
   │    the gradient flattens (∇J → 0), naturally shrinking step sizes.     │
   │ 4. Strictly Convex: The OLS Hessian is H = (1/n) XᵀX ≥ 0, guaranteeing │
   │    zero local minima traps.                                            │
   │ 5. Feature Scaling is Essential: Standardizing features transforms     │
   │    hyper-elongated canyon ravines into symmetric spherical bowls.      │
   │ 6. Loss Curve Diagnostics: Always inspect Cost vs. Epoch. Rising loss  │
   │    demands immediate learning rate reduction.                          │
   └────────────────────────────────────────────────────────────────────────┘
```
