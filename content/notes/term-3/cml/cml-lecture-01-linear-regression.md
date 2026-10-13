# Linear Regression & Gradient Descent Optimization
**Term:** Term 3 | **Subject:** CML | **Note ID:** `cml-lecture-01-linear-regression`
**Last Updated:** 2026-10-07T10:30:00Z

## Abstract & Summary
Mathematical principles of linear regression, parameter estimation via Ordinary Least Squares (OLS), and numerical optimization with Gradient Descent variants.

## Learning Objectives
- Derive the Mean Squared Error (MSE) objective function.
- Formulate Ordinary Least Squares (OLS) closed-form normal equations.
- Understand batch, stochastic, and mini-batch gradient descent update rules.

## Key Takeaways
- Hypothesis function: h_theta(x) = theta^T x.
- Cost function MSE: J(theta) = 1/(2m) sum (h_theta(x_i) - y_i)^2.
- Analytical solution (Normal Equation): theta = (X^T X)^(-1) X^T y.
- Gradient Descent iteratively steps along the negative gradient: theta := theta - alpha * grad(J).

---

## 1. Linear Regression Model Formulation
In supervised linear regression, given a dataset $\{(x^{(i)}, y^{(i)})\}_{i=1}^m$ where each input feature vector $x^{(i)} \in \mathbb{R}^n$, we model the target as a linear combination of inputs:

$$h_\theta(x) = \theta_0 + \theta_1 x_1 + \dots + \theta_n x_n = \theta^T x$$

To find optimal parameters $\theta$, we minimize the **Mean Squared Error (MSE)** cost function:

$$J(\theta) = \frac{1}{2m} \sum_{i=1}^m \left(h_\theta(x^{(i)}) - y^{(i)}\right)^2$$

**Citations & References:**
- Pattern Recognition and Machine Learning - Christopher Bishop, Chapter 3

---

## 2. Gradient Descent Algorithm
Gradient descent is a first-order iterative optimization algorithm for finding a local minimum of a differentiable function.

### Update Rule
At each iteration, we update all parameters simultaneously:

$$\theta_j := \theta_j - \alpha \frac{\partial}{\partial \theta_j} J(\theta)$$

Computing the partial derivative gives:

$$\frac{\partial}{\partial \theta_j} J(\theta) = \frac{1}{m} \sum_{i=1}^m \left(h_\theta(x^{(i)}) - y^{(i)}\right) x_j^{(i)}$$

Where $\alpha$ represents the learning rate hyperparameter. A learning rate that is too high causes divergence; one that is too low causes slow convergence.

**Citations & References:**
- Andrew Ng - CS229 Lecture Notes on Supervised Learning

---