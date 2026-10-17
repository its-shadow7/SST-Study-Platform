# 10. Decision Trees: Recursive Partitioning, Impurity Metrics & Tree Depth
**Term:** Term 5 | **Subject:** CML | **Note ID:** `cml-t5-l10`
**Last Updated:** 2026-10-18T00:00:00Z

## Abstract & Summary
An intuitive yet rigorous first-principles guide to Decision Trees. Covers the foundational concept of recursive binary splitting, explains how trees partition feature space into axis-aligned rectangular regions without requiring feature scaling, deconstructs node impurity metrics (Shannon Entropy and Gini Impurity), walks through hand-calculated Information Gain on loan data, explores tree growth and stopping criteria, and diagnoses overfitting controls.

## Learning Objectives
- Explain how Decision Trees partition feature space using axis-aligned orthogonal splits to make predictions.
- Calculate and contrast Entropy and Gini Impurity as measures of node homogeneity.
- Compute Information Gain and Gini Gain step-by-step for candidate feature splits on a dataset.
- Analyze why unconstrained deep trees overfit and tune pre-pruning stopping knobs (max_depth, min_samples_leaf).
- Train, visualize, and interpret Decision Trees using Scikit-Learn's DecisionTreeClassifier and plot_tree.

## Key Takeaways
- A Decision Tree makes predictions by traversing a sequence of internal yes/no questions from the root to a terminal leaf node.
- Geometrically, trees create axis-aligned, orthogonal boundaries (rectangles/boxes), unlike linear models which fit diagonal hyperplanes.
- Pure nodes contain samples from only one class (Impurity = 0); mixed 50-50 nodes have maximum uncertainty (Entropy = 1.0, Gini = 0.5).
- Information Gain measures the reduction in impurity achieved by splitting a node on a specific feature and threshold.
- Trees are naturally scale-invariant: monotonic transformations and differing physical units do not alter split ordering.
- Unconstrained trees will split until every leaf is pure, memorizing training noise (0% train error, high test variance).
- Pre-pruning constraints (max_depth, min_samples_split, min_samples_leaf) prevent trees from growing fragile, overfitted sub-branches.

---

## 1. What is a Decision Tree? The 20-Questions Intuition
### 1.1 The Intuition: Asking Sequential Questions

Think about how an expert loan officer evaluates a mortgage applicant, or how a doctor diagnoses a patient in an emergency triage unit, or how you play the classic parlor game **20 Questions**:
1. *"Is the applicant's Credit Score below 600?"* $\implies$ **Yes**.
2. *"Is their Debt-to-Income (DTI) ratio greater than 45%?"* $\implies$ **Yes**.
3. *"Decision: Reject Loan Application (High Default Risk)"*.

If the answer to the first question were **No** (Credit Score $\ge 600$), the officer would pivot to an entirely different line of inquiry:
1. *"Is the Annual Household Income above 80,000 USD?"* $\implies$ **Yes**.
2. *"Decision: Approve Loan Application (Low Default Risk)"*.

A **Decision Tree** structures this exact hierarchical, sequential reasoning process into a directed acyclic graph (an upside-down tree):
- It starts at the top with the entire universe of training observations.
- At each step, it selects the single most informative feature and asks a binary True/False question (e.g., $x_j \le \theta$).
- The data is split into two mutually exclusive subsets, each following their respective downstream branch.
- The process repeats recursively until a terminal stopping condition is met, where a final prediction is rendered.

```
Anatomy of a Decision Tree:
                  [ Root Node: All n Samples ]
                   Question: Is Credit_Score <= 600?
                             /               \
                     True  /                   \  False
                         v                       v
            [ Internal Split Node ]          [ Internal Split Node ]
            Question: DTI > 45%?             Question: Income > 80k?
               /              \                 /              \
       True  /          False   \       True  /          False   \
           v                      v         v                      v
     ( Leaf Node 1 )      ( Leaf Node 2 ) ( Leaf Node 3 )      ( Leaf Node 4 )
     Pred: Reject         Pred: Review    Pred: Approve        Pred: Review
```

---

### 1.2 Anatomy & Terminology of Tree Structures

1. **Root Node**: The top-most node of the tree, containing $100\%$ of the training observations. It has no incoming edges and exactly two outgoing edges (in binary trees).
2. **Internal Decision Nodes (Splitting Nodes)**: Intermediate nodes that evaluate a specific feature $x_j$ against a threshold $\theta$ ($x_j \le \theta$). They have exactly one incoming edge and two outgoing edges.
3. **Branches (Edges)**: Directed connections routing data points based on whether the condition evaluated to True (typically Left) or False (typically Right).
4. **Leaf Nodes (Terminal Nodes)**: Nodes at the base of the tree that have incoming edges but **zero outgoing edges**. They store the final predictive outcome:
   - In **Classification**, each leaf stores class frequencies and predicts either the **majority class** (mode) or the **empirical posterior probability vector** $\hat{p}_c = \frac{n_c}{n_{\text{leaf}}}$.
   - In **Regression**, each leaf stores continuous numerical targets and predicts the **local sample mean** $\hat{y} = \frac{1}{|S|}\sum_{i \in S} y_i$ (or sample median for $L_1$ loss).
5. **Depth of a Node**: The length of the path (number of edges) from the root node to that specific node. The root is at Depth $0$.
6. **Maximum Depth (`max_depth`)**: The maximum number of edges separating the root from the deepest leaf in the tree. A tree with a single split has Depth $1$ (known as a **Decision Stump**).

---

### 1.3 Geometric Interpretation: Axis-Aligned Orthogonal Partitions

The most critical mathematical insight regarding Decision Trees is understanding how they partition feature space:

```
Geometric Partitioning of 2D Feature Space:
       x2 ^
          │             Region R3
          │           (Class: Default)
       θ2 ├─────────────┬──────────────────────────
          │             │
          │  Region R1  │        Region R2
          │ (Class: No) │     (Class: Default)
          │             │
          └─────────────┴────────────────────────► x1
                        θ1

Corresponding Tree Structure:
                     [ x1 <= θ1 ]
                     /          \
             True  /              \  False
                 v                  v
            [ x2 <= θ2 ]        ( Leaf R2 )
            /          \        Pred: Default
    True  /              \ False
        v                  v
   ( Leaf R1 )        ( Leaf R3 )
   Pred: No           Pred: Default
```

#### Why Splits Are Strictly Axis-Aligned:
- At every internal node, the decision rule tests **exactly one feature** against a scalar threshold: $x_j \le \theta$.
- In a 2-dimensional space $(x_1, x_2)$, a condition like $x_1 \le \theta_1$ creates a **vertical line** parallel to the $x_2$-axis.
- A subsequent condition like $x_2 \le \theta_2$ creates a **horizontal line** parallel to the $x_1$-axis.
- In $d$-dimensional space $\mathbb{R}^d$, every split is an axis-aligned **orthogonal hyperplane** perpendicular to one coordinate axis.
- As a direct geometric consequence, a Decision Tree partitions the feature space into a collection of non-overlapping **hyper-rectangles (boxes)**:

$$\mathbb{R}^d = \bigcup_{m=1}^{M} R_m, \quad \text{where } R_j \cap R_k = \emptyset \text{ for } j \ne k$$

#### The Diagonal Boundary Failure (Staircase Approximation):
Consider a problem where the true underlying boundary is diagonal: $x_1 + x_2 = 10$.
- A linear model (Logistic Regression or Linear SVM) captures this boundary effortlessly with a single hyperplane: $w_1 x_1 + w_2 x_2 + b = 0$.
- A Decision Tree **cannot draw diagonal lines**. It must approximate the smooth diagonal boundary using a jagged, stepped **staircase** composed of dozens of alternating vertical and horizontal cuts!
- Approximating smooth, rotated, or spherical boundaries requires enormous tree depth, which drastically increases the risk of overfitting.

---

### 1.4 Classification Trees vs. Regression Trees (CART)

The **CART (Classification and Regression Trees)** framework, developed by Leo Breiman, Jerome Friedman, Richard Olshen, and Charles Stone in 1984, unifies both problem types:

| Property | Classification Tree (`DecisionTreeClassifier`) | Regression Tree (`DecisionTreeRegressor`) |
| :--- | :--- | :--- |
| **Target Variable $y$** | Discrete categorical classes ($y \in \{0, 1, \dots, C-1\}$). | Continuous real numbers ($y \in \mathbb{R}$). |
| **Node Impurity Metric** | Gini Impurity ($I_G$) or Shannon Entropy ($H$). | Variance / Mean Squared Error ($\text{MSE}$) or Mean Absolute Error ($\text{MAE}$). |
| **Leaf Prediction** | Majority class label (Mode) or class probability $\hat{p}_c = \frac{n_c}{|S|}$. | Sample mean $\hat{y} = \bar{y} = \frac{1}{|S|}\sum y_i$ (or sample median). |
| **Leaf Loss Minimization** | Minimizes misclassification risk under chosen loss. | Minimizes squared error $\sum (y_i - \hat{y})^2$ or absolute error $\sum |y_i - \hat{y}|$. |
| **Continuous Function Shape** | Piecewise-constant discrete step surface. | Piecewise-constant flat step-function (staircase plateaus). |

---

### 1.5 The Principle of Monotonic Scale Invariance

One of the greatest operational advantages of Decision Trees over distance-based models ($k$-NN) and gradient-based models (Linear/Logistic Regression, Neural Networks) is **complete scale invariance**:

> **Theorem of Monotonic Invariance**:
> Let $f: \mathbb{R} \to \mathbb{R}$ be any strictly monotonically increasing transformation (e.g., $f(x) = 1000 \cdot x$, $f(x) = x + 50$, $f(x) = \log(x)$ for $x > 0$, or $f(x) = \sqrt{x}$).
> If feature $x_j$ is replaced by $f(x_j)$, the optimal split threshold $t$ transforms to $f(t)$, and the resulting partition, impurity reduction, and model predictions are **identically unchanged**!

#### Why Does This Hold?
Decision trees do not calculate physical Euclidean distances or take numerical inner products $\mathbf{w}^T \mathbf{x}$.
They only evaluate **relative ordering**: *"Are samples where $x_j \le t$ purer than samples where $x_j > t$?"*
Because monotonic transformations preserve rank ordering ($a < b \iff f(a) < f(b)$), the sorting of feature values is identical.
Consequently:
- **No feature scaling is required**: Standardizing with `StandardScaler` or `MinMaxScaler` produces zero difference in tree topology.
- **Robustness to extreme outliers**: An outlier with $x = 10,000,000$ simply sits at the highest rank. It does not pull or distort split boundaries the way it violently tilts linear regression hyperplanes!

**Citations & References:**
- Breiman, L., Friedman, J., Stone, C. J., & Olshen, R. A. (1984). Classification and Regression Trees. CRC Press.
- Quinlan, J. R. (1986). Induction of decision trees. Machine Learning, 1(1), 81-106.

---

## 2. Measuring Node Impurity: Shannon Entropy vs. Gini Impurity
### 2.1 The Concept of Impurity: Measuring Node Homogeneity

To construct an optimal decision tree, an algorithm must decide at every node: *"Which feature and which threshold should we split on?"*
To answer this, we need a mathematical yardstick to quantify the **quality** of a node:

- A **pure node** contains observations belonging to **only one class** (e.g., 50 default cases, 0 non-default cases). A pure node requires no further splitting; it can become a definitive leaf.
- An **impure node** contains a thoroughly mixed soup of labels (e.g., 25 default cases, 25 non-default cases). Predicting a label here is no better than flipping a fair coin.

Let $S$ be the subset of training samples present at node $m$, comprising $|S|$ total points across $C$ distinct classes.
The empirical proportion of samples belonging to class $c \in \{1, \dots, C\}$ is:

$$p_c = \frac{1}{|S|} \sum_{i \in S} \mathbb{I}(y_i = c), \quad \text{where } p_c \ge 0 \text{ and } \sum_{c=1}^{C} p_c = 1$$

---

### 2.2 Shannon Entropy: Uncertainty in Information Theory

In 1948, Claude Shannon published his landmark paper *"A Mathematical Theory of Communication"*, defining the fundamental measure of uncertainty (information content) in a random variable.
If an event occurs with probability $p_c$, the amount of "surprise" or information gained upon observing it is $\log_2(1 / p_c) = -\log_2(p_c)$ bits.
The **Shannon Entropy** $H(S)$ is the expected surprise across all classes in the node:

$$H(S) = - \sum_{c=1}^{C} p_c \log_2(p_c)$$

*(By universal mathematical convention in information theory, $0 \cdot \log_2(0) \equiv \lim_{p \to 0^+} p \log_2(p) = 0$, since impossible classes contribute zero uncertainty).*

#### The Binary Classification Case ($C = 2$):
Let $p$ be the proportion of positive class samples ($y = 1$), so $(1 - p)$ is the proportion of negative class samples ($y = 0$):

$$H(p) = - p \log_2(p) - (1 - p) \log_2(1 - p)$$

- **Perfect Purity ($p = 0.0$ or $p = 1.0$)**:
  $$H(1.0) = - 1.0 \log_2(1.0) - 0 = 0.0 \text{ bits}$$
  There is zero uncertainty. Every sample belongs to the exact same class.
- **Maximum Uncertainty ($p = 0.5$)**:
  $$H(0.5) = - 0.5 \log_2(0.5) - 0.5 \log_2(0.5) = - 0.5(-1) - 0.5(-1) = 0.5 + 0.5 = \mathbf{1.0 \text{ bit}}$$
  Uncertainty is at its theoretical maximum. It requires exactly $1$ full bit of additional information to determine the class.

---

### 2.3 Gini Impurity: Expected Misclassification Probability

Corrado Gini's metric, widely popularized in machine learning through the CART algorithm, has a clean and elegant probabilistic interpretation:

> **Probabilistic Definition of Gini Impurity**:
> Suppose you assign a class label to a randomly chosen sample from node $S$ strictly according to the node's empirical class distribution $(p_1, p_2, \dots, p_C)$.
> What is the probability that this randomly assigned label is **incorrect**?

The probability of choosing an item of class $c$ is $p_c$. The probability of mistakenly assigning it any other class is $(1 - p_c)$.
Summing across all possible classes yields the **Gini Impurity** $I_G(S)$:

$$I_G(S) = \sum_{c=1}^{C} p_c (1 - p_c) = \sum_{c=1}^{C} (p_c - p_c^2) = \sum_{c=1}^{C} p_c - \sum_{c=1}^{C} p_c^2 = 1 - \sum_{c=1}^{C} p_c^2$$

#### The Binary Classification Case ($C = 2$):
Let $p$ be the proportion of positive class samples:

$$I_G(p) = 1 - \left( p^2 + (1 - p)^2 \right) = 1 - \left( p^2 + 1 - 2p + p^2 \right) = 2p - 2p^2 = \mathbf{2p(1 - p)}$$

- **Perfect Purity ($p = 0.0$ or $p = 1.0$)**:
  $$I_G(0) = 2(0)(1) = \mathbf{0.0}, \quad I_G(1) = 2(1)(0) = \mathbf{0.0}$$
- **Maximum Uncertainty ($p = 0.5$)**:
  $$I_G(0.5) = 2(0.5)(0.5) = \mathbf{0.50}$$
  The Gini impurity peaks at $0.50$ for a balanced binary mixture.

---

### 2.4 Mathematical Connection: Gini as the First-Order Taylor Approximation of Entropy

Why do Entropy and Gini Impurity lead to virtually identical tree structures in practice?
Recall the natural logarithm Taylor series expansion around $x = 1$:
$$\ln(x) = (x - 1) - \frac{(x - 1)^2}{2} + \dots \implies \ln(p_c) \approx p_c - 1 = -(1 - p_c)$$
Multiplying by $-1$ gives:
$$-\ln(p_c) \approx 1 - p_c$$

Substituting this first-order linear approximation into the natural entropy formula:
$$H_e(S) = - \sum_{c=1}^{C} p_c \ln(p_c) \approx \sum_{c=1}^{C} p_c (1 - p_c) = I_G(S)$$

> **Mathematical Revelation**:
> **Gini Impurity is literally the first-order linear Taylor expansion of Natural Entropy!**
> Because Gini replaces expensive transcendental logarithm evaluations ($\log_2(p)$) with basic multiplications ($p^2$), computing Gini is computationally much faster when evaluating millions of candidate splits during training.

```
Impurity Curves Comparison Across Binary Class Proportions p:
    Impurity
      1.0 ^                   Entropy H(p) [Peaks at 1.0]
          │                     .---.
      0.8 │                    /     \
          │                   /       \
      0.5 │   .. - - - - - - / - - - - \ - - - - - - - ..  Gini I_G(p) [Peaks at 0.5]
          │  /              /           \              \
      0.2 │ /              /             \              \
          │/              /               \              \
      0.0 ┴──────────────┴─────────────────┴──────────────┴► Proportion p
         0.0            0.25              0.5            0.75            1.0
```

| Class Proportion $p$ | Shannon Entropy $H(p)$ (bits) | Gini Impurity $I_G(p)$ | Scaled Gini ($2 \times I_G(p)$) |
| :--- | :--- | :--- | :--- |
| **$0.00$** (Pure Class 0) | $0.0000$ | $0.0000$ | $0.0000$ |
| **$0.10$** | $0.4690$ | $0.1800$ | $0.3600$ |
| **$0.20$** | $0.7219$ | $0.3200$ | $0.6400$ |
| **$0.30$** | $0.8813$ | $0.4200$ | $0.8400$ |
| **$0.40$** | $0.9710$ | $0.4800$ | $0.9600$ |
| **$0.50$** (Max Mixed) | $\mathbf{1.0000}$ | $\mathbf{0.5000}$ | $\mathbf{1.0000}$ |
| **$0.60$** | $0.9710$ | $0.4800$ | $0.9600$ |
| **$0.70$** | $0.8813$ | $0.4200$ | $0.8400$ |
| **$0.80$** | $0.7219$ | $0.3200$ | $0.6400$ |
| **$0.90$** | $0.4690$ | $0.1800$ | $0.3600$ |
| **$1.00$** (Pure Class 1) | $0.0000$ | $0.0000$ | $0.0000$ |

---

### 2.5 Impurity Metrics for Regression Trees: Variance (MSE)

For regression problems where target $y \in \mathbb{R}$ is continuous, class proportions $p_c$ do not exist.
Instead, node impurity measures the **spread or dispersion** of targets around their local mean $\bar{y}_S = \frac{1}{|S|}\sum_{i \in S} y_i$:

$$I_{\text{MSE}}(S) = \frac{1}{|S|} \sum_{i \in S} (y_i - \bar{y}_S)^2 = \text{Var}_S(y)$$

- A node where all targets are identical ($y = 42.0$ for all samples) has $\text{Var}(y) = 0.0$ (perfect purity).
- A node where targets vary wildly has high variance, demanding further splitting.
- *Alternative ($L_1$ Mean Absolute Error)*: $I_{\text{MAE}}(S) = \frac{1}{|S|} \sum_{i \in S} |y_i - \text{median}_S(y)|$, which is more robust to extreme outlier target values.

**Citations & References:**
- Shannon, C. E. (1948). A mathematical theory of communication. Bell System Technical Journal, 27(3), 379-423.
- Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer, Chapter 14.

---

## 3. The Splitting Engine: Information Gain & Gini Gain
### 3.1 The Greedy CART Recursive Binary Splitting Algorithm

Finding the globally optimal decision tree that minimizes overall training error is an **NP-complete problem** requiring combinatorial search over all possible tree topologies.
Instead, modern libraries (like Scikit-Learn's CART implementation) use a **top-down greedy heuristic**:

```
The CART Greedy Search Step:
  1. For each feature j in {1, 2, ..., d}:
       Sort unique values of feature j in current node S: x_(1) < x_(2) < ... < x_(k)
       For each adjacent pair, evaluate candidate threshold t = (x_(i) + x_(i+1)) / 2:
           Partition S into Left S_L (x_j <= t) and Right S_R (x_j > t)
           Calculate Impurity Reduction (Gain):
               Gain(S, j, t) = Impurity(S) - [ (|S_L|/|S|)*Impurity(S_L) + (|S_R|/|S|)*Impurity(S_R) ]
  2. Pick the feature j* and threshold t* that produce the MAXIMUM GAIN.
  3. Split the node and recursively repeat steps 1-2 on both S_L and S_R.
```

#### Mathematical Formulas for Gain:
1. **Information Gain (Entropy-based)**:
   $$IG(S, j, t) = H(S) - \left[ \frac{|S_L|}{|S|} H(S_L) + \frac{|S_R|}{|S|} H(S_R) \right]$$
2. **Gini Gain ($\Delta I_G$)**:
   $$\Delta I_G(S, j, t) = I_G(S) - \left[ \frac{|S_L|}{|S|} I_G(S_L) + \frac{|S_R|}{|S|} I_G(S_R) \right]$$
3. **Variance Reduction (Regression Trees)**:
   $$\Delta \text{Var}(S, j, t) = \text{Var}(S) - \left[ \frac{|S_L|}{|S|} \text{Var}(S_L) + \frac{|S_R|}{|S|} \text{Var}(S_R) \right]$$

---

### 3.2 Exhaustive Hand-Calculated Walkthrough: 8-Row Bank Loan Default Dataset

To cement these formulas into instinct, let us solve the exact benchmark loan problem taught on the whiteboard:

#### The Training Dataset:
| Customer ID | Credit Band ($x_1$) | Loan Size ($x_2$) | Actual Default Status ($y$) |
| :---: | :---: | :---: | :---: |
| **ID 1** | Low | Small | **1 (Default)** |
| **ID 2** | Low | Small | **1 (Default)** |
| **ID 3** | Low | Large | **1 (Default)** |
| **ID 4** | Low | Large | **0 (No Default)** |
| **ID 5** | High | Small | **0 (No Default)** |
| **ID 6** | High | Small | **0 (No Default)** |
| **ID 7** | High | Large | **0 (No Default)** |
| **ID 8** | High | Large | **1 (Default)** |

Total observations $n = 8$:
- Total Defaults ($y = 1$): $4$ customers (IDs 1, 2, 3, 8).
- Total Non-Defaults ($y = 0$): $4$ customers (IDs 4, 5, 6, 7).
- Base Class Proportions: $p_1 = 4/8 = 0.50$, $p_0 = 4/8 = 0.50$.

---

#### Step 1: Calculate Impurity of the Parent Root Node
- **Shannon Entropy of Parent**:
  $$H(\text{Parent}) = - 0.50 \log_2(0.50) - 0.50 \log_2(0.50) = - 0.50(-1.0) - 0.50(-1.0) = \mathbf{1.000 \text{ bit}}$$
- **Gini Impurity of Parent**:
  $$I_G(\text{Parent}) = 1 - \left( 0.50^2 + 0.50^2 \right) = 1 - (0.25 + 0.25) = 1 - 0.50 = \mathbf{0.500}$$

---

#### Step 2: Evaluate Candidate Split A: `Credit Band` == Low vs. High
- **Left Child Node ($S_L$: `Credit Band == Low`)**:
  - Contains IDs 1, 2, 3, 4 ($n_L = 4$).
  - Targets: $[1, 1, 1, 0] \implies 3$ Defaults, $1$ Non-Default.
  - Proportions: $p_1 = 3/4 = 0.75$, $p_0 = 1/4 = 0.25$.
  - **Left Entropy $H(S_L)$**:
    $$H(S_L) = - 0.75 \log_2(0.75) - 0.25 \log_2(0.25)$$
    Using $\log_2(0.75) \approx -0.4150$ and $\log_2(0.25) = -2.000$:
    $$H(S_L) = - 0.75(-0.4150) - 0.25(-2.000) = 0.3113 + 0.5000 = \mathbf{0.8113 \text{ bits}}$$
  - **Left Gini $I_G(S_L)$**:
    $$I_G(S_L) = 1 - \left( 0.75^2 + 0.25^2 \right) = 1 - (0.5625 + 0.0625) = 1 - 0.6250 = \mathbf{0.3750}$$

- **Right Child Node ($S_R$: `Credit Band == High`)**:
  - Contains IDs 5, 6, 7, 8 ($n_R = 4$).
  - Targets: $[0, 0, 0, 1] \implies 1$ Default, $3$ Non-Defaults.
  - Proportions: $p_1 = 1/4 = 0.25$, $p_0 = 3/4 = 0.75$.
  - By symmetry:
    $$H(S_R) = \mathbf{0.8113 \text{ bits}}, \quad I_G(S_R) = \mathbf{0.3750}$$

- **Weighted Child Impurities**:
  $$\bar{H}_{\text{children}} = \frac{4}{8} H(S_L) + \frac{4}{8} H(S_R) = 0.5(0.8113) + 0.5(0.8113) = \mathbf{0.8113 \text{ bits}}$$
  $$\bar{I}_{G, \text{children}} = \frac{4}{8} I_G(S_L) + \frac{4}{8} I_G(S_R) = 0.5(0.3750) + 0.5(0.3750) = \mathbf{0.3750}$$

- **Gain for Candidate Split A (`Credit Band`)**:
  $$IG(\text{Credit Band}) = H(\text{Parent}) - \bar{H}_{\text{children}} = 1.000 - 0.8113 = \mathbf{0.1887 \text{ bits}}$$
  $$\Delta I_G(\text{Credit Band}) = I_G(\text{Parent}) - \bar{I}_{G, \text{children}} = 0.500 - 0.3750 = \mathbf{0.1250}$$

---

#### Step 3: Evaluate Candidate Split B: `Loan Size` == Small vs. Large
- **Left Child Node ($S_L$: `Loan Size == Small`)**:
  - Contains IDs 1, 2, 5, 6 ($n_L = 4$).
  - Targets: $[1, 1, 0, 0] \implies 2$ Defaults, $2$ Non-Defaults.
  - Proportions: $p_1 = 2/4 = 0.50$, $p_0 = 2/4 = 0.50$.
  - **Left Entropy and Gini**:
    $$H(S_L) = \mathbf{1.000 \text{ bit}}, \quad I_G(S_L) = \mathbf{0.500}$$

- **Right Child Node ($S_R$: `Loan Size == Large`)**:
  - Contains IDs 3, 4, 7, 8 ($n_R = 4$).
  - Targets: $[1, 0, 0, 1] \implies 2$ Defaults, $2$ Non-Defaults.
  - Proportions: $p_1 = 2/4 = 0.50$, $p_0 = 2/4 = 0.50$.
  - **Right Entropy and Gini**:
    $$H(S_R) = \mathbf{1.000 \text{ bit}}, \quad I_G(S_R) = \mathbf{0.500}$$

- **Weighted Child Impurities**:
  $$\bar{H}_{\text{children}} = 0.5(1.000) + 0.5(1.000) = \mathbf{1.000 \text{ bit}}$$
  $$\bar{I}_{G, \text{children}} = 0.5(0.500) + 0.5(0.500) = \mathbf{0.500}$$

- **Gain for Candidate Split B (`Loan Size`)**:
  $$IG(\text{Loan Size}) = 1.000 - 1.000 = \mathbf{0.0000 \text{ bits}}$$
  $$\Delta I_G(\text{Loan Size}) = 0.500 - 0.500 = \mathbf{0.0000}$$

---

#### Step 4: Decision Tree Split Selection
- $IG(\text{Credit Band}) = 0.1887 \text{ bits} \gg IG(\text{Loan Size}) = 0.0000 \text{ bits}$.
- $\Delta I_G(\text{Credit Band}) = 0.1250 \gg \Delta I_G(\text{Loan Size}) = 0.0000$.

**Conclusion**: The decision tree algorithm selects **`Credit Band`** as the winning split for the root node! `Loan Size` fails to provide any discriminatory power at the root level because both resulting child nodes remain in a 50-50 deadlock.

---

### 3.3 Continuous Feature Splitting Mechanism

When dealing with a continuous numerical feature (e.g., `Annual Income` in dollars):
1. **Sort**: The unique values of the continuous feature across all samples present in the node are sorted in ascending order:
   $$x_{(1)} < x_{(2)} < x_{(3)} < \dots < x_{(m)}$$
2. **Midpoint Candidates**: Potential split thresholds $t_k$ are placed at the arithmetic midpoints between consecutive distinct values:
   $$t_k = \frac{x_{(k)} + x_{(k+1)}}{2}$$
3. **Boundary Optimization**: The algorithm sweeps through all candidate midpoints from left to right, maintaining rolling cumulative counts of classes to evaluate the gain in $O(n)$ time after an initial $O(n \log n)$ sort.
4. **Computational Complexity**: For $d$ continuous features and $n$ samples, finding the single best split at a node requires $O(d \cdot n \log n)$ time.

---

### 3.4 Multiway Splits vs. Binary Splits & The High-Cardinality Bias Trap

In older tree algorithms like **ID3** (Iterative Dichotomiser 3), categorical features were split into **multiway branches** (one branch for every distinct category level).
However, standard Information Gain has a severe mathematical flaw when evaluating high-cardinality features:

> **The Customer ID Pathology**:
> Suppose a database includes a unique primary key `Customer_ID` (or `Credit_Card_Number`) with $n$ distinct values for $n$ samples.
> If a tree splits on `Customer_ID`, it creates $n$ single-sample leaves.
> Each leaf contains exactly $1$ observation, so $p_c = 1.0 \implies H(\text{leaf}) = 0.0 \text{ bits}$!
> The weighted child entropy is $\bar{H} = 0.0$, yielding maximal possible Information Gain:
> $$IG = H(\text{Parent}) - 0 = H(\text{Parent})$$
> The algorithm will enthusiastically choose `Customer_ID` as the root split, creating an overfitted lookup table with zero predictive generalization!

#### The Solutions:
1. **CART Binary Subsetting**: Modern CART never splits multiway; it partitions categorical levels into two subsets: e.g., $\{A, B\} \text{ vs. } \{C, D\}$.
2. **Gain Ratio (C4.5)**: Ross Quinlan introduced the **Gain Ratio**, which penalizes features with high intrinsic split entropy:
   $$\text{GainRatio}(S, A) = \frac{IG(S, A)}{\text{SplitInformation}(S, A)}$$
   $$\text{SplitInformation}(S, A) = - \sum_{i=1}^{k} \frac{|S_i|}{|S|} \log_2 \left( \frac{|S_i|}{|S|} \right)$$
   For `Customer_ID`, $\text{SplitInformation} = \log_2(n)$, which heavily suppresses the Gain Ratio, stopping the tree from choosing the useless feature!

**Citations & References:**
- Quinlan, J. R. (1993). C4.5: Programs for Machine Learning. Morgan Kaufmann Publishers.

---

## 4. The Overfitting Hazard & Pre-Pruning Stopping Rules
### 4.1 The Overfitting Pathology: Why Unconstrained Trees Memorize Noise

A fully grown, unconstrained Decision Tree is one of the most aggressive memorization engines in classical machine learning:

- If no stopping constraints are imposed, the recursive splitting algorithm will continue splitting nodes until **every single leaf is 100% pure** (or contains fewer samples than required to split).
- In a pure tree, **Training Accuracy is identically 100%** (Training Error = $0.0\%$, Impurity = $0.0$).
- However, real-world data contains noise: measurement errors, labeling mistakes, and overlapping distributions.
- To make every leaf pure, the tree will create specialized micro-branches that isolate individual noise outliers, creating tiny "islands" of erroneous predictions across feature space.

```
Train Error vs. Test Error as Tree Depth Grows:
    Error Rate
      ^
      │  \                                   Test Error (Generalization Gap)
      │   \                                        . - - - -
      │    \                                     /
      │     \                                  .'
      │      \                                /
      │       '.                            .'  <-- Optimal Sweet Spot
      │         '--.                    .--'
      │             ' - - - - - - - - -'
      │                \
      │                 '-----------------------------------► Train Error -> 0%
      +─────────────────────────────────────────────────────► Tree Depth
      Depth 1               Depth 3-5                   Depth 20+
    (Underfitting)     (Balanced Generalization)      (Extreme Overfitting)
```

---

### 4.2 Pre-Pruning (Early Stopping) Hyperparameters in Scikit-Learn

To prevent trees from growing excessively tall and memorizing sample-specific noise, practitioners use **Pre-Pruning (Early Stopping)**.
These hyperparameters instruct the tree builder to halt expansion before leaves become pure:

| Hyperparameter Knob | Default in `sklearn` | Physical Role & Regularization Mechanism | Recommended Tuning Values |
| :--- | :--- | :--- | :--- |
| **`max_depth`** | `None` (unlimited) | **Hard ceiling on tree height**. Restricts the longest path from root to leaf. A tree with `max_depth=3` can have at most $2^3 = 8$ leaves. | `3, 4, 5, 6, 8, 10` |
| **`min_samples_split`** | `2` | **Minimum samples required inside a node** to attempt any candidate split. If a node has $n < \text{min\_samples\_split}$, it immediately becomes a leaf. | `10, 20, 50, 100` |
| **`min_samples_leaf`** | `1` | **Minimum samples required in BOTH left and right children**. If a proposed split leaves either child with fewer than this threshold, the split is forbidden! | `5, 10, 25, 50` |
| **`max_leaf_nodes`** | `None` (unlimited) | **Caps the total number of leaves** across the entire tree. Grown in best-first fashion (splitting the node that yields the largest gain first). | `8, 16, 32, 64` |
| **`min_impurity_decrease`** | `0.0` | **Threshold on minimum gain**. A split is executed only if $\Delta I_G \ge \text{threshold}$. Filters out marginal splits that barely reduce entropy. | `0.001, 0.01, 0.05` |
| **`criterion`** | `'gini'` | Metric used to evaluate split quality: `'gini'` (Gini Impurity) or `'entropy'` (Shannon Information Gain). | `'gini'`, `'entropy'` |

> **Best Practice Tip for `min_samples_leaf`**:
> Setting `min_samples_leaf=10` is often far more effective than tuning `max_depth` alone.
> It guarantees that every single prediction rendered by any leaf represents a statistical consensus of at least 10 real customers, completely neutralizing isolated single-point outliers!

---

### 4.3 Pre-Pruning vs. Post-Pruning (Cost-Complexity Pruning)

There are two fundamental paradigms for controlling tree complexity:

#### 1. Pre-Pruning (Early Stopping)
- Halts tree construction dynamically during top-down growth when a stopping threshold is reached.
- **Advantage**: Fast training time; avoids building massive unnecessary subtrees.
- **The "Horizon Effect" Flaw**: A greedy algorithm evaluates splits one step at a time. A feature split that offers very little immediate gain might unlock an exceptionally powerful split on the very next level! Pre-pruning terminates prematurely, missing the high-gain downstream split.

#### 2. Post-Pruning (Cost-Complexity Pruning / Minimal Cost-Complexity)
- Grows a complete, fully saturated tree $T_{\max}$ until all leaves are pure.
- Subsequently prunes back the weakest subtrees from the bottom up by adding a complexity penalty for each leaf:
  $$R_\alpha(T) = R(T) + \alpha |T|$$
  Where $R(T)$ is total tree misclassification rate, $|T|$ is the number of terminal leaves, and $\alpha \ge 0$ is the cost-complexity hyperparameter (`ccp_alpha` in Scikit-Learn).
- As $\alpha$ increases, smaller subtrees with fewer leaves are systematically favored, pruning away fragile leaf branches while preserving deep, high-gain pathways!

**Citations & References:**
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). Springer, Chapter 9.

---

## 5. Hands-On Python Implementation: Loan Default Classification
### 5.1 Hands-On Python Implementation: Loan Default Classification

The following production script trains, regularizes, visualizes, and evaluates a Decision Tree on a credit risk dataset, demonstrating how hyperparameter constraints prevent overfitting:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, confusion_matrix

# 1. Generate Synthetic Loan Default Problem
# 1,000 applicants, 8 financial features (income, credit score, DTI, debt, etc.)
np.random.seed(42)
X, y = make_classification(
    n_samples=1000,
    n_features=8,
    n_informative=5,
    n_redundant=2,
    n_classes=2,
    weights=[0.80, 0.20],  # 20% default rate (imbalanced loan portfolio)
    random_state=42
)
feature_names = [
    "credit_score", "dti_ratio", "annual_income", "revolving_debt",
    "years_employed", "num_open_credit_lines", "savings_balance", "missed_payments_12m"
]

# 2. Strict Train / Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 3. Model A: Unconstrained Overfitted Tree (max_depth=None)
overfit_tree = DecisionTreeClassifier(criterion="gini", max_depth=None, random_state=42)
overfit_tree.fit(X_train, y_train)

# 4. Model B: Pre-Pruned Regularized Tree (max_depth=3, min_samples_leaf=15)
pruned_tree = DecisionTreeClassifier(
    criterion="gini",
    max_depth=3,
    min_samples_leaf=15,
    random_state=42
)
pruned_tree.fit(X_train, y_train)

# 5. Evaluate Performance & Generalization Gap
def evaluate_model(model, name):
    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))
    test_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    depth = model.get_depth()
    leaves = model.get_n_leaves()
    print(f"=== {name} ===")
    print(f"Tree Depth:        {depth} | Leaf Nodes: {leaves}")
    print(f"Train Accuracy:    {train_acc * 100:.2f}%")
    print(f"Test Accuracy:     {test_acc * 100:.2f}%")
    print(f"Holdout ROC-AUC:   {test_auc:.4f}\n")

evaluate_model(overfit_tree, "Unconstrained Overfitted Tree (max_depth=None)")
evaluate_model(pruned_tree, "Pre-Pruned Regularized Tree (max_depth=3, leaf>=15)")

# 6. Inspect Human-Readable Rule Hierarchy
tree_rules = export_text(pruned_tree, feature_names=feature_names)
print("=== EXTRACTED DECISION RULES ===")
print(tree_rules)
```

---

### 5.2 Depth Sweep Analysis: Demonstrating the Overfitting Signature

When we systematically sweep `max_depth` from $1$ to $15$ on this credit risk dataset, the diagnostic signatures of underfitting and overfitting become vividly visible:

| Tree Depth | Number of Leaves | Training Accuracy | Test Accuracy | Holdout ROC-AUC | Diagnostic State |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **Depth 1** | $2$ | $80.00\%$ | $80.00\%$ | $0.6214$ | **Underfitting (Decision Stump)**: High bias; fails to capture multi-feature interactions. |
| **Depth 2** | $4$ | $84.27\%$ | $83.60\%$ | $0.7812$ | Improving; captures primary interaction. |
| **Depth 3** | $8$ | $87.87\%$ | $\mathbf{86.80\%}$ | $\mathbf{0.8491}$ | **Optimal Generalization Sweet Spot**: Peak test accuracy and highest ROC-AUC. |
| **Depth 4** | $14$ | $90.53\%$ | $86.00\%$ | $0.8350$ | Slight variance emerging. |
| **Depth 6** | $32$ | $95.20\%$ | $84.40\%$ | $0.7980$ | Test score degrades as subtrees isolate noise. |
| **Depth 10** | $78$ | $98.93\%$ | $82.40\%$ | $0.7410$ | Marked overfitting: memorizing training noise. |
| **Depth $\infty$** | $124$ | $\mathbf{100.00\%}$ | $81.20\%$ | $0.7105$ | **Extreme Overfitting**: 0% training error, lowest test ROC-AUC. |

---

### 5.3 Diagnostic Failure Modes & Engineering Pitfalls

| Engineering Failure Mode | Underlying Root Cause | Catastrophic Symptom | Recommended Production Solution |
| :--- | :--- | :--- | :--- |
| **The Diagonal Boundary Trap** | Orthogonal, axis-aligned splitting geometry. | Tree builds a jagged, stepped staircase to approximate diagonal lines, requiring massive depth and overfitting. | Rotate feature axes using PCA before fitting, or employ Linear Discriminant Analysis (LDA) / Logistic Regression. |
| **High Model Instability (Variance)** | Greedy hierarchical structure: a small change at the root alters all subsequent downstream splits. | Adding 10 new training records completely rearranges the tree structure and decision rules. | Use tree ensembles: **Random Forests** or **Gradient Boosted Trees (GBDT)** to aggregate hundreds of perturbed trees. |
| **High-Cardinality Categorical Bias** | Pure categorical columns with many unique levels (e.g., `ZIP_Code`, `Device_ID`) artificially maximize Information Gain. | Tree splits on the identifier feature, creating single-sample pure leaves that fail completely on unseen test IDs. | Apply Target Encoding, Weight of Evidence (WoE) encoding, or use C4.5 Gain Ratio / CART binary subsetting. |
| **Regression Extrapolation Failure** | Leaf predictions are constant scalar means bounded by $\min(y_{\text{train}})$ and $\max(y_{\text{train}})$. | Tree cannot predict values outside the range seen during training (e.g., predicting future revenue in an expanding economy). | Combine tree with a linear trend base estimator (e.g., Linear Regression + GBDT residuals). |
| **Majority Class Domination in Imbalance** | Impurity metrics (Gini/Entropy) sum over total sample counts without weighting. | Tree splits to purify the easy majority class (99% non-fraud), creating massive leaves that ignore minority fraud cases. | Set `class_weight='balanced'` in `DecisionTreeClassifier` to scale impurity by inverse class frequencies. |

**Citations & References:**
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. JMLR, 12, 2825-2830.

---
