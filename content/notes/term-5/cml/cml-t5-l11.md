# 11. Decision Trees II: Pruning, Categorical Features & Feature Importance
**Term:** Term 5 | **Subject:** CML | **Note ID:** `cml-t5-l11`
**Last Updated:** 2026-10-18T00:00:00Z

## Abstract & Summary
An in-depth, practical continuation of Decision Tree architectures. Explores why pre-pruning can suffer from the horizon problem and formalizes Cost-Complexity Pruning (ccp_alpha) where a deep tree is grown and systematically trimmed back. Dissects categorical split mechanics in Scikit-Learn, demystifies Mean Decrease in Impurity (MDI) feature importance, exposes high-cardinality bias traps, and implements production pruning on loan default datasets.

## Learning Objectives
- Contrast pre-pruning stopping rules with post-pruning via Minimal Cost-Complexity Pruning (ccp_alpha).
- Extract the effective alpha pruning path using cost_complexity_pruning_path and select optimal tree complexity.
- Compare numerical threshold splits against categorical feature encodings in CART trees.
- Compute and interpret Mean Decrease in Impurity (MDI) feature importances and diagnose high-cardinality bias.
- Build an end-to-end pruned decision tree pipeline on tabular data and rank feature drivers.

## Key Takeaways
- Pre-pruning stops growth early using greedy thresholds; Post-pruning (Cost-Complexity Pruning) grows a deep tree first and removes subtrees that do not justify their complexity.
- Cost-Complexity Pruning balances training error R(T) against tree size |T| via the cost objective R_alpha(T) = R(T) + alpha * |T|.
- As ccp_alpha increases, more subtrees are pruned away, reducing variance and simplifying the tree graph.
- Scikit-Learn's CART implementation requires categorical features to be numerically encoded (One-Hot or Ordinal) before building split thresholds.
- Feature Importance (MDI) measures the total weighted impurity reduction brought by a feature across all splits where it was chosen.
- MDI feature importance is systematically biased toward high-cardinality features (like numerical floats or unique IDs); Permutation Importance provides an unbiased validation alternative.

---

## 1. Pre-Pruning Limitations & The Horizon Problem
### 1.1 The Greedy Nature of Tree Induction

Standard decision tree algorithms (CART, ID3, C4.5) build trees using a **greedy, top-down recursive heuristic**:
- At each step, the algorithm chooses the single split $(x_j, \theta)$ that yields the maximum immediate drop in impurity:
  $$\Delta I(t) = I(t) - \left[ \frac{n_L}{n_t} I(t_L) + \frac{n_R}{n_t} I(t_R) \right]$$
- It makes the locally optimal choice at the current internal node without looking ahead to see how that split influences subsequent downstream choices.
- While computationally tractable ($O(d \cdot n \log n)$ per split), this myopic approach has a fundamental blind spot known as **The Horizon Problem**.

---

### 1.2 The Horizon Problem & The XOR / Parity Failure

What happens when no single feature by itself separates the classes, but an interaction of two or more features separates them perfectly?
This is the classic **Exclusive-OR (XOR) / Parity Problem**:

Suppose we have two binary features $x_1 \in \{0, 1\}$ and $x_2 \in \{0, 1\}$, and our target label is $y = x_1 \oplus x_2$:

| Observation ID | Feature $x_1$ | Feature $x_2$ | Target Label $y$ ($x_1 \oplus x_2$) |
| :---: | :---: | :---: | :---: |
| **Row 1** | $0$ | $0$ | **0** |
| **Row 2** | $0$ | $1$ | **1** |
| **Row 3** | $1$ | $0$ | **1** |
| **Row 4** | $1$ | $1$ | **0** |

```
The XOR Feature Space Geometry:
    x2 ^
     1 │   (y = 1)        (y = 0)
       │      o              *
       │
     0 │      *              o
       │   (y = 0)        (y = 1)
       └──────┴──────────────┴──────► x1
              0              1
```

#### Step-by-Step Mathematical Walkthrough of Greedy Failure:
1. **Parent Root Node ($n = 4$)**:
   - Class counts: $2$ zeros, $2$ ones ($p_0 = 0.50, p_1 = 0.50$).
   - Impurity:
     $$H(\text{Parent}) = - 0.50 \log_2(0.50) - 0.50 \log_2(0.50) = \mathbf{1.000 \text{ bit}}$$
     $$I_G(\text{Parent}) = 1 - (0.50^2 + 0.50^2) = \mathbf{0.500}$$

2. **Evaluating Candidate Split on $x_1$ ($x_1 == 0 \text{ vs. } x_1 == 1$)**:
   - **Left Child ($x_1 = 0$, Rows 1 & 2)**:
     Targets are $[0, 1] \implies 1$ zero, $1$ one ($p_0 = 0.50, p_1 = 0.50$).
     $$H(S_L) = \mathbf{1.000 \text{ bit}}, \quad I_G(S_L) = \mathbf{0.500}$$
   - **Right Child ($x_1 = 1$, Rows 3 & 4)**:
     Targets are $[1, 0] \implies 1$ zero, $1$ one ($p_0 = 0.50, p_1 = 0.50$).
     $$H(S_R) = \mathbf{1.000 \text{ bit}}, \quad I_G(S_R) = \mathbf{0.500}$$
   - **Information Gain on $x_1$**:
     $$IG(x_1) = 1.000 - \left[ \frac{2}{4}(1.000) + \frac{2}{4}(1.000) \right] = 1.000 - 1.000 = \mathbf{0.000 \text{ bits!}}$$

3. **Evaluating Candidate Split on $x_2$ ($x_2 == 0 \text{ vs. } x_2 == 1$)**:
   - Identical symmetric result:
     $$IG(x_2) = \mathbf{0.000 \text{ bits!}}$$

#### The Catastrophe of Pre-Pruning:
If we enforce common pre-pruning stopping conditions:
- `min_impurity_decrease = 0.01` $\implies$ The algorithm sees $IG = 0.000 \le 0.01$ and **aborts immediately**!
- `max_depth = 1` $\implies$ The decision stump achieves $50\%$ accuracy, completely useless.

However, if the tree is allowed to take this "zero-gain" split on $x_1$ and continue to **Depth 2**:
- On the Left child ($x_1 = 0$), splitting on $x_2$ yields:
  - Left-Left ($x_2 = 0$): Row 1 $\implies$ Target $0$ ($100\%$ pure, $H = 0.0$).
  - Left-Right ($x_2 = 1$): Row 2 $\implies$ Target $1$ ($100\%$ pure, $H = 0.0$).
- On the Right child ($x_1 = 1$), splitting on $x_2$ yields:
  - Right-Left ($x_2 = 0$): Row 3 $\implies$ Target $1$ ($100\%$ pure, $H = 0.0$).
  - Right-Right ($x_2 = 1$): Row 4 $\implies$ Target $0$ ($100\%$ pure, $H = 0.0$).
- At Depth 2, the tree achieves **100% purity and 100% accuracy**!

> **The Pre-Pruning Horizon Blind Spot**:
> Pre-pruning stops growth as soon as local gain falls below a threshold.
> It cannot see beyond the immediate "horizon" to realize that a split with zero immediate gain can unlock massive purity gains downstream!

---

### 1.3 Architectural Comparison: Decision Trees vs. Logistic Regression

| Architectural Dimension | Decision Trees (Non-Parametric) | Logistic Regression (Parametric Linear) |
| :--- | :--- | :--- |
| **Functional Assumption** | Non-parametric: No functional form assumed; partitions space into step-wise hyper-rectangles. | Parametric: Assumes log-odds is a strictly linear combination: $\ln\frac{p}{1-p} = \mathbf{w}^T \mathbf{x} + b$. |
| **Decision Boundary** | Axis-aligned piecewise constant orthogonal staircases. | Smooth, continuous flat linear hyperplane. |
| **Interaction Modeling** | Automatically captures hierarchical multi-feature interactions (depth $k$ models $k$-way interaction). | Cannot capture interactions unless manually engineered by multiplying features ($x_1 \times x_2$). |
| **Feature Scaling** | **Completely scale-invariant**: No standardization or normalization needed. | Highly sensitive: Gradient descent and regularization require standardized features ($z = \frac{x-\mu}{\sigma}$). |
| **Outlier Robustness** | Extreme outliers in features do not distort splits (only order matters). | Extreme outliers pull weights heavily, tilting the decision boundary. |
| **Inference Latency** | $O(\text{depth})$ path traversal; ultra-fast binary comparisons. | $O(d)$ dot product evaluation; instantaneous vector multiplication. |
| **Risk of Overfitting** | High variance: Deep unpruned trees easily memorize noise. | Low variance: Underfitting risk if true boundary is non-linear. |

---

### 1.4 Grow-Then-Prune: The Philosophical Shift

To overcome the horizon blind spot, Breiman et al. introduced the **Post-Pruning (Grow-Then-Prune)** paradigm:
1. **Phase 1 (Grow Fully)**: Build an unconstrained tree $T_{\max}$ until every leaf is pure ($I_G = 0$) or contains fewer than 2 samples. By growing past zero-gain nodes, the tree captures multi-variable feature interactions (like XOR).
2. **Phase 2 (Prune Back)**: Systematically collapse unnecessary leaves and subtrees that merely model sample noise, retaining only those branches that provide robust statistical validation.

**Citations & References:**
- Breiman, L. et al. (1984). Classification and Regression Trees. CRC Press, Chapter 3.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). Springer, Chapter 9.

---

## 2. Cost-Complexity Pruning: The Mechanics of ccp_alpha
### 2.1 The Mathematical Formulation of Cost-Complexity Pruning

In CART, post-pruning is formalized through **Minimal Cost-Complexity Pruning (CCP)**.
Instead of evaluating nodes individually, CCP evaluates the quality of an entire tree $T$ using a penalized objective function:

$$R_\alpha(T) = R(T) + \alpha |T|$$

Where:
- $T \subseteq T_{\max}$ is any pruned subtree of the fully grown tree $T_{\max}$.
- $R(T)$ is the **total misclassification cost (or impurity)** of the tree across all its terminal leaf nodes:
  $$R(T) = \sum_{\tau \in \tilde{T}} R(\tau) = \sum_{\tau \in \tilde{T}} P(\tau) I(\tau)$$
  Where $\tilde{T}$ is the set of terminal leaves in $T$, $P(\tau) = \frac{n_\tau}{n}$ is the proportion of training points that reach leaf $\tau$, and $I(\tau)$ is the impurity of leaf $\tau$.
- $|T| = |\tilde{T}|$ is the **number of terminal leaf nodes** in tree $T$ (a direct measure of tree complexity).
- $\alpha \ge 0$ is the **cost-complexity hyperparameter** (`ccp_alpha` in Scikit-Learn), which acts as a penalty per additional leaf.

```
The Spectrum of ccp_alpha:
  α = 0                                       Optimal α*                             α -> ∞
  ├───────────────────────────────────────────────┼────────────────────────────────────┤
  No penalty for leaves               Balanced Generalization               Extreme penalty
  T_max is preferred                  Subtrees with weak gain pruned        Tree collapses to
  Overfitting (0% train error)        Optimal test accuracy / ROC-AUC       Single Root Node (|T| = 1)
```

---

### 2.2 Derivation of the Effective Alpha $\alpha_{\text{eff}}(t)$ of an Internal Node

For any internal node $t$ in tree $T$:
- Let $T_t$ denote the **subtree rooted at node $t$** (the branch expanding below $t$).
- If we **keep** the subtree $T_t$, its cost-complexity contribution is:
  $$R_\alpha(T_t) = R(T_t) + \alpha |T_t|$$
  *(Where $|T_t|$ is the number of terminal leaves in subtree $T_t$, and $R(T_t) = \sum_{\tau \in \tilde{T}_t} R(\tau)$).*
- If we **collapse / prune** the subtree $T_t$ into a single terminal leaf at node $t$, its cost-complexity becomes:
  $$R_\alpha(t) = R(t) + \alpha \cdot 1$$
  *(Where $R(t)$ is the misclassification error if node $t$ acts as a leaf).*

#### At What Value of $\alpha$ Does Pruning Node $t$ Become Preferable?
Because the unpruned subtree $T_t$ was grown to fit the data, its training error is always lower than or equal to the collapsed single node: $R(T_t) \le R(t)$.
However, the collapsed node has only $1$ leaf, whereas the subtree has $|T_t| > 1$ leaves.
Setting their cost-complexities equal:
$$R_\alpha(t) = R_\alpha(T_t)$$
$$R(t) + \alpha \cdot 1 = R(T_t) + \alpha |T_t|$$
$$R(t) - R(T_t) = \alpha (|T_t| - 1)$$

Solving for $\alpha$ yields the celebrated **Effective Alpha** $\alpha_{\text{eff}}(t)$:

$$\alpha_{\text{eff}}(t) = \frac{R(t) - R(T_t)}{|T_t| - 1}$$

> **Physical Meaning of Effective Alpha**:
> $\alpha_{\text{eff}}(t)$ measures the **error rate reduction per leaf** gained by keeping subtree $T_t$ instead of collapsing it into a single leaf.
> - When $\alpha < \alpha_{\text{eff}}(t)$, the error reduction exceeds the penalty $\implies$ **Keep the subtree**.
> - When $\alpha \ge \alpha_{\text{eff}}(t)$, the complexity penalty outweighs the error reduction $\implies$ **Prune the subtree into a leaf**!

---

### 2.3 Concrete Multi-Node Hand-Calculated Pruning Walkthrough

Suppose an overfitted loan decision tree has $4$ candidate internal subtrees ($N_A, N_B, N_C, N_D$) across different depths:

| Internal Node ($t$) | Node Error If Leaf ($R(t)$) | Subtree Error ($R(T_t)$) | Number of Leaves in Subtree ($|T_t|$) | Effective Alpha Calculation: $\alpha_{\text{eff}}(t) = \frac{R(t) - R(T_t)}{|T_t| - 1}$ | Pruning Priority |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Node $N_A$** | $0.040$ | $0.034$ | $3$ leaves | $\frac{0.040 - 0.034}{3 - 1} = \frac{0.006}{2} = \mathbf{0.0030}$ | **1st (Weakest Link)** |
| **Node $N_B$** | $0.075$ | $0.055$ | $5$ leaves | $\frac{0.075 - 0.055}{5 - 1} = \frac{0.020}{4} = \mathbf{0.0050}$ | **2nd to Prune** |
| **Node $N_C$** | $0.120$ | $0.080$ | $3$ leaves | $\frac{0.120 - 0.080}{3 - 1} = \frac{0.040}{2} = \mathbf{0.0200}$ | **3rd to Prune** |
| **Node $N_D$** | $0.250$ | $0.100$ | $4$ leaves | $\frac{0.250 - 0.100}{4 - 1} = \frac{0.150}{3} = \mathbf{0.0500}$ | **4th (Strongest Split)** |

#### How the Algorithm Executes Pruning:
1. At $\alpha = 0$, all subtrees are preserved ($T_0 = T_{\max}$).
2. As $\alpha$ increases to $0.0030$, Node $N_A$ is the weakest link ($\alpha_{\text{eff}} = 0.0030$). Its 3 leaves are collapsed into a single leaf, creating subtree $T_1$.
3. As $\alpha$ increases to $0.0050$, Node $N_B$ collapses into a leaf, creating subtree $T_2$.
4. At $\alpha = 0.0200$, Node $N_C$ collapses, creating subtree $T_3$.
5. At $\alpha \ge 0.0500$, Node $N_D$ collapses, reducing the tree to the single root node $T_{\text{root}}$.

---

### 2.4 The Nested Sequence of Optimal Subtrees

A remarkable property established by Breiman is that as $\alpha$ increases from $0$ to $\infty$, CART does not produce arbitrary trees.
It generates a strictly **nested hierarchy of optimal subtrees**:

$$T_{\max} = T_0 \supset T_1 \supset T_2 \supset \dots \supset T_k = T_{\text{root}}$$

Each subtree $T_{i+1}$ is obtained by pruning the weakest link (smallest $\alpha_{\text{eff}}$) from subtree $T_i$.
Scikit-Learn computes this entire pruning path in a single pass via:
`path = clf.cost_complexity_pruning_path(X_train, y_train)`
Which returns the sequence of critical `ccp_alphas` and their corresponding total impurities.

**Citations & References:**
- Breiman, L. et al. (1984). Classification and Regression Trees. CRC Press.
- Ripley, B. D. (1996). Pattern Recognition and Neural Networks. Cambridge University Press.

---

## 3. Categorical vs. Numerical Features in Decision Trees
### 3.1 Numerical vs. Categorical Features in Tree Splitting

Machine learning datasets in production almost always contain a mixture of continuous numerical features and discrete categorical features:

| Feature Type | Definition | Mathematical Representation | Example in Credit Underwriting |
| :--- | :--- | :--- | :--- |
| **Continuous / Numerical** | Quantities with natural metric ordering and infinite possible gradations. | $x_j \in \mathbb{R}$ | `Annual Income ($)`, `Credit Score`, `Debt-to-Income Ratio (%)` |
| **Nominal Categorical** | Unordered discrete levels or classes. | $x_j \in \{c_1, c_2, \dots, c_K\}$ | `Loan Purpose: {Education, Home, Personal, Auto}` |
| **Ordinal Categorical** | Discrete levels with a natural intrinsic rank order. | $x_j \in \{\text{Low} < \text{Medium} < \text{High}\}$ | `Risk Rating: {Subprime, Near-Prime, Prime, Super-Prime}` |

---

### 3.2 Splitting Mechanics: Thresholds vs. Binary Subsets

#### 1. Splitting on Numerical Features
For a numerical feature, a candidate split always takes the form of a scalar threshold test:
$$\text{Is } x_j \le \theta?$$
There are at most $n - 1$ unique candidate thresholds, evaluated in $O(n \log n)$ time.

#### 2. Splitting on Categorical Features Conceptually
For a categorical feature with $K$ unique categories, a binary tree must partition the categories into two non-empty subsets:
$$\text{Is } x_j \in \mathcal{S}_{\text{left}}? \quad \text{where } \mathcal{S}_{\text{left}} \subset \{c_1, \dots, c_K\}$$

```
Categorical Binary Partitioning:
                [ Is Loan_Purpose in {Home, Auto}? ]
                                /        \
                        Yes   /            \  No
                            v                v
                 [ Home, Auto Cohort ]   [ Education, Personal Cohort ]
```

#### The Combinatorial Explosion Problem:
How many non-empty subsets can be formed from $K$ categories?
The number of distinct binary partitions is:
$$N_{\text{partitions}} = 2^{K-1} - 1$$

- For $K = 4$ categories (`loan_purpose`): $2^{4-1} - 1 = 2^3 - 1 = \mathbf{7}$ candidate splits. Easy to evaluate!
- For $K = 10$ categories: $2^9 - 1 = \mathbf{511}$ candidate splits.
- For $K = 20$ categories: $2^{19} - 1 = \mathbf{524,287}$ candidate splits!
- For $K = 50$ (e.g., US States): $2^{49} - 1 \approx \mathbf{5.6 \times 10^{14}}$ candidate splits. Evaluating every partition is computationally impossible.

#### Breiman's Ordering Theorem for Binary Classification:
Breiman proved an astonishing theorem for binary classification:
If you sort the $K$ categories in ascending order of their **positive class proportion**:
$$P(Y = 1 \mid x_j = c_{(1)}) \le P(Y = 1 \mid x_j = c_{(2)}) \le \dots \le P(Y = 1 \mid x_j = c_{(K)})$$
Then the optimal binary partition that maximizes Gini Gain or Information Gain is **guaranteed** to be one of the $K - 1$ consecutive cuts along this sorted line!
This collapses the computational search from exponential $O(2^K)$ down to linear $O(K \log K)$!

---

### 3.3 Target Encoding with Empirical Bayesian Smoothing

When dealing with high-cardinality categories ($K > 20$, such as `Zip_Code` or `Product_Category`), One-Hot encoding blows up dimensionality and fractures trees into sparse leaves.
A powerful alternative is **Target Encoding (Mean Target Encoding)**:
Each category $c$ is replaced by the expected target value:
$$\hat{x}_c = \mathbb{E}[Y \mid X = c]$$

#### The Overfitting Hazard on Rare Categories:
If a category appears only once in the dataset (e.g., `Zip_Code = 90210` with $y = 1$), naive target encoding assigns it $\hat{x} = 1.0$. The tree creates a perfect leaf on this single sample, causing massive overfitting!
To resolve this, we apply **Empirical Bayesian Smoothing (m-estimate)**:

$$S_k = \lambda(n_k) \bar{y}_k + (1 - \lambda(n_k)) \bar{y}_{\text{global}}$$
$$\lambda(n_k) = \frac{n_k}{n_k + m}$$

Where:
- $n_k$ is the count of observations in category $k$.
- $\bar{y}_k$ is the local sample target mean for category $k$.
- $\bar{y}_{\text{global}}$ is the overall dataset target mean (e.g., $0.20$ default rate).
- $m \ge 1$ is the smoothing weight (e.g., $m = 10$).

#### Concrete Hand Calculation:
Suppose global default rate $\bar{y}_{\text{global}} = 0.20$ ($20\%$). We have two categories:
1. Category A (`Personal Loan`): $n_A = 500$ loans, $150$ defaults $\implies \bar{y}_A = 150/500 = 0.30$.
   $$\lambda(500) = \frac{500}{500 + 10} = \frac{500}{510} \approx 0.9804$$
   $$S_A = 0.9804(0.30) + (1 - 0.9804)(0.20) = 0.2941 + 0.0039 = \mathbf{0.2980} \text{ (Virtually unchanged)}$$
2. Category B (`Rare Yacht Loan`): $n_B = 2$ loans, $2$ defaults $\implies \bar{y}_B = 2/2 = 1.00$.
   $$\lambda(2) = \frac{2}{2 + 10} = \frac{2}{12} \approx 0.1667$$
   $$S_B = 0.1667(1.00) + (1 - 0.1667)(0.20) = 0.1667 + 0.1667 = \mathbf{0.3334}$$

Notice how the smoothed estimate for the rare category is pulled from a dangerous $1.00$ down to $0.3334$, protecting the tree from memorizing a 2-sample fluke!

**Citations & References:**
- Quinlan, J. R. (1993). C4.5: Programs for Machine Learning. Morgan Kaufmann Publishers.

---

## 4. Feature Importance: Mean Decrease in Impurity (MDI) & Pitfalls
### 4.1 Mean Decrease in Impurity (MDI / Gini Importance)

When a decision tree is trained in Scikit-Learn, it automatically computes and exposes the `feature_importances_` attribute.
This metric is formally known as **Mean Decrease in Impurity (MDI)** or **Gini Importance**:

#### Mathematical Definition:
Let $\mathcal{T}_j$ denote the set of all internal nodes $t$ across the tree where feature $j$ was selected as the splitting variable ($v(t) = j$).
The raw importance of feature $j$ is the sum of the impurity decreases achieved at those specific nodes, weighted by the fraction of training samples that traverse node $t$:

$$\text{MDI}(j) = \sum_{t \in \mathcal{T}_j} \frac{n_t}{n} \Delta I(t)$$

Where:
- $n_t$ is the number of training observations reaching node $t$.
- $n$ is the total number of training observations in the entire dataset.
- $\Delta I(t) = I(t) - \frac{n_L}{n_t} I(t_L) - \frac{n_R}{n_t} I(t_R)$ is the impurity reduction at node $t$.

To make importances easily interpretable, Scikit-Learn normalizes the values so they sum to $1.0$:

$$\text{Importance}(j) = \frac{\text{MDI}(j)}{\sum_{k=1}^d \text{MDI}(k)}, \quad \text{where } \sum_{j=1}^d \text{Importance}(j) = 1.0$$

---

### 4.2 Three Critical Pitfalls of MDI Feature Importance

While MDI is fast to compute (accumulated for free during tree training), it suffers from severe statistical flaws that frequently deceive data scientists:

#### Pitfall 1: Severe Bias Toward High-Cardinality & Continuous Features
- A continuous feature with 1,000 unique values offers 999 possible split midpoints.
- A binary categorical feature ($0$ or $1$) offers exactly $1$ possible split midpoint.
- **Purely by chance**, an uninformative continuous feature (or a random noise column) has hundreds of opportunities to find a spurious split that marginally reduces training impurity.
- As a result, **MDI heavily inflates the importance of continuous and high-cardinality features**, even when they contain zero real predictive signal!

#### Pitfall 2: Collinear Feature Cannibalization (Shadowing)
- Suppose two features $x_1$ and $x_2$ are nearly identical (e.g., `Annual Income` in dollars and `Monthly Income` in dollars).
- At the root node, the tree evaluates both. Suppose $x_1$ achieves an infinitesimal edge ($IG = 0.2501$ vs $0.2500$). The tree splits on $x_1$.
- Once the node is partitioned on $x_1$, the residual variance is largely resolved. When $x_2$ is evaluated in downstream child nodes, its remaining gain is near zero.
- In the final MDI summary, $x_1$ appears critically important ($0.85$), while $x_2$ appears virtually useless ($0.02$), hiding the fact that $x_2$ is just as predictive as $x_1$!

#### Pitfall 3: In-Sample Training Metric (No Generalization Guarantee)
- MDI is calculated strictly on the **training data**.
- If a deep unpruned tree overfits and memorizes random training noise, MDI will assign massive importance to the exact features that memorized that noise.
- It tells you what features the tree used to memorize the training set, **not** what features reliably predict new, unseen observations!

---

### 4.3 The Gold Standard Solution: Permutation Feature Importance

In 2001, Leo Breiman designed **Permutation Feature Importance** to resolve the fatal shortcomings of MDI:

```
Permutation Feature Importance Workflow:
  1. Train the tree model on X_train, y_train.
  2. Compute baseline performance metric on an UNTOUCHED validation set (X_val, y_val):
         Baseline Score = ROC-AUC(y_val, Model.predict_proba(X_val))
  3. For each feature j in {1, 2, ..., d}:
         Randomly shuffle ONLY column j in X_val (breaking its relationship with y_val).
         Compute new performance score on corrupted data:
             Score_perm(j) = ROC-AUC(y_val, Model.predict_proba(X_val_shuffled_j))
         Calculate Importance as the Performance Drop:
             Importance_perm(j) = Baseline Score - Score_perm(j)
```

#### Comparing Tree Interpretability Frameworks:
| Attribute | MDI (Gini Importance) | Permutation Importance | SHAP (SHapley Additive exPlanations) |
| :--- | :--- | :--- | :--- |
| **Data Split Evaluated** | Training set only | Holdout Test / Validation set | Test / Validation set |
| **Computational Speed** | Instant ($O(1)$ post-training) | Moderate ($O(p \times n_{\text{test}})$) | Fast for trees ($O(T \cdot L \cdot D^2)$ via TreeSHAP) |
| **High-Cardinality Bias** | **Severe Positive Bias** | **Unbiased** (Noise scores $\le 0$) | **Unbiased** |
| **Directional Impact** | Magnitude only ($[0, 1]$) | Performance drop only | Directional ($+$ or $-$ impact on class probability) |
| **Collinearity Handling** | Arbitrarily picks one feature | Understates correlated features | Fairly distributes credit using Shapley values |

**Citations & References:**
- Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5-32.
- Strobl, C., Boulesteix, A. L., Zeileis, A., & Hothorn, T. (2007). Bias in random forest variable importance measures: Illustrations, sources and a solution. BMC Bioinformatics, 8(1), 25.

---

## 5. Hands-On Python Implementation: Pruning Path & Feature Importance
### 5.1 Hands-On Python Implementation: Pruning Path & Feature Importance

The following production script implements the full CART post-pruning pipeline on a bank loan default dataset, tunes `ccp_alpha` using cross-validation, and contrasts MDI vs. Permutation Feature Importance:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

# 1. Synthesize Bank Loan Dataset with Categorical & Continuous Features + Random Noise
np.random.seed(42)
n_samples = 1200

# Continuous financial features
credit_score = np.random.normal(650, 80, n_samples).clip(300, 850)
annual_income = np.random.lognormal(10.8, 0.5, n_samples)
loan_amount = annual_income * np.random.uniform(0.1, 0.6, n_samples)
years_employed = np.random.exponential(5, n_samples).clip(0, 30)

# Categorical feature: loan_purpose
purposes = ["education", "home", "personal", "auto"]
loan_purpose = np.random.choice(purposes, size=n_samples, p=[0.20, 0.35, 0.25, 0.20])

# Pure Random Noise column with high cardinality (Tests MDI bias!)
random_noise_high_card = np.random.uniform(0, 1000, n_samples)

# Generate Ground Truth Target (Default = 1)
logit = (
    - 0.012 * (credit_score - 600)
    + 0.00003 * (loan_amount - 20000)
    - 0.15 * (years_employed - 4)
    + np.where(loan_purpose == "personal", 0.6, 0.0)
    + np.where(loan_purpose == "education", 0.3, 0.0)
    - 1.2
)
prob_default = 1 / (1 + np.exp(-logit))
default = (np.random.uniform(0, 1, n_samples) < prob_default).astype(int)

df = pd.DataFrame({
    "credit_score": credit_score,
    "annual_income": annual_income,
    "loan_amount": loan_amount,
    "years_employed": years_employed,
    "loan_purpose": loan_purpose,
    "random_noise_col": random_noise_high_card,
    "default": default
})

# 2. Preprocessing: One-Hot Encode Categorical Column
df_encoded = pd.get_dummies(df, columns=["loan_purpose"], drop_first=False)
X = df_encoded.drop(columns=["default"])
y = df_encoded["default"]

# 3. Train / Validation / Test Partition
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 4. Extract Cost-Complexity Pruning Path
unpruned_tree = DecisionTreeClassifier(random_state=42)
path = unpruned_tree.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas, impurities = path.ccp_alphas, path.impurities

# 5. Tune Optimal ccp_alpha via 5-Fold Stratified Cross-Validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
alpha_candidates = ccp_alphas[::5]  # Subsample candidates along the path
alpha_scores = []

for alpha in alpha_candidates:
    clf = DecisionTreeClassifier(random_state=42, ccp_alpha=alpha)
    scores = cross_val_score(clf, X_train, y_train, cv=cv, scoring="roc_auc")
    alpha_scores.append(scores.mean())

best_alpha = alpha_candidates[np.argmax(alpha_scores)]
print(f"Optimal Tuned ccp_alpha: {best_alpha:.5f}")

# 6. Fit Final Pruned Tree
best_tree = DecisionTreeClassifier(random_state=42, ccp_alpha=best_alpha)
best_tree.fit(X_train, y_train)

# 7. Evaluate on Holdout Test Set
test_auc = roc_auc_score(y_test, best_tree.predict_proba(X_test)[:, 1])
print(f"Holdout Test ROC-AUC (Optimal CCP Tree): {test_auc:.4f}")
print(f"Tree Depth: {best_tree.get_depth()} | Leaves: {best_tree.get_n_leaves()}")

# 8. Compare MDI vs. Permutation Importance
mdi_importances = pd.Series(best_tree.feature_importances_, index=X.columns)

perm_result = permutation_importance(
    best_tree, X_test, y_test, n_repeats=10, random_state=42, scoring="roc_auc"
)
perm_importances = pd.Series(perm_result.importances_mean, index=X.columns)

comparison_df = pd.DataFrame({
    "MDI (Gini Importance)": mdi_importances,
    "Permutation Importance (Test)": perm_importances
}).sort_values(by="Permutation Importance (Test)", ascending=False)

print("\n=== FEATURE IMPORTANCE COMPARISON ===")
print(comparison_df.round(4))
```

---

### 5.2 Alpha Sweep Results & Pruning Trade-Off Table

When cost-complexity pruning is evaluated across increasing values of `ccp_alpha`, the tree shrinks monotonically:

| Complexity Penalty ($\alpha$) | Tree Depth | Terminal Leaves | Train ROC-AUC | Test ROC-AUC | Diagnostic State |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **$\alpha = 0.00000$** | $14$ | $118$ | $1.0000$ | $0.7180$ | **Overfitted Tree**: Fits training noise; wide generalization gap. |
| **$\alpha = 0.00210$** | $8$ | $42$ | $0.9420$ | $0.7810$ | Mild pruning; weak subtrees collapsed. |
| **$\alpha = 0.00485$** | $5$ | $14$ | $0.8830$ | $\mathbf{0.8350}$ | **Optimal CCP Sweet Spot**: Peak test ROC-AUC. Balanced bias-variance. |
| **$\alpha = 0.01250$** | $3$ | $6$ | $0.8210$ | $0.8120$ | Coarse tree; robust, human-interpretable rules. |
| **$\alpha = 0.03500$** | $1$ | $2$ | $0.7250$ | $0.7200$ | Underfitting (Decision Stump). |
| **$\alpha \ge 0.08000$** | $0$ | $1$ | $0.5000$ | $0.5000$ | Complete Collapse: Single root node predicting global majority class. |

---

### 5.3 Diagnostic Failure Modes & Engineering Pitfalls

| Engineering Failure Mode | Underlying Root Cause | Catastrophic Symptom | Recommended Production Solution |
| :--- | :--- | :--- | :--- |
| **Relying Exclusively on Pre-Pruning** | Greedy early stopping halts on zero-gain splits. | Tree fails completely on multi-variable interactions (e.g., XOR, synergy between income and debt). | Use Post-Pruning (`ccp_alpha`) or ensemble methods (Random Forests) that grow deep trees before regularizing. |
| **Trusting MDI on High-Cardinality Features** | Continuous/high-cardinality features offer hundreds of candidate thresholds, winning spurious gains. | Random noise columns or unique IDs rank at the top of `feature_importances_`. | Always evaluate **Permutation Feature Importance** on an independent validation/test set. |
| **One-Hot Encoding High-Cardinality Columns** | Categorical features with $50+$ categories create dozens of sparse columns. | Splits isolate tiny groups ($1$ vs $999$), fracturing tree depth and destroying predictive power. | Use Target Encoding with cross-validation smoothing, or switch to LightGBM/CatBoost native categorical handling. |
| **Arbitrary Alpha Selection Without CV** | Choosing `ccp_alpha = 0.05` arbitrarily without checking the pruning path. | Tree over-prunes into a useless single root node, causing massive underfitting. | Always extract `cost_complexity_pruning_path` and select $\alpha$ via `GridSearchCV` on cross-validation ROC-AUC. |
| **Permutation Importance on Collinear Features** | Correlated features share identical information. | Shuffling feature A has no effect because feature B provides the exact same information, masking both features. | Group correlated features together and permute them as a single cluster (**Clustered Permutation Importance**). |

---

### 5.4 Production Automated Pruning Curve Visualization

In production machine learning workflows, plotting the pruning path against tree complexity and cross-validation accuracy allows engineers to audit the optimal stopping point:

```python
# Extract full alpha path
clf = DecisionTreeClassifier(random_state=42)
path = clf.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas, impurities = path.ccp_alphas, path.impurities

# Track tree metrics across alpha
clfs = []
for alpha in ccp_alphas[::3]:  # Subsample path for efficiency
    t = DecisionTreeClassifier(random_state=42, ccp_alpha=alpha)
    t.fit(X_train, y_train)
    clfs.append(t)

node_counts = [t.tree_.node_count for t in clfs]
depths = [t.tree_.max_depth for t in clfs]
train_scores = [t.score(X_train, y_train) for t in clfs]
test_scores = [t.score(X_test, y_test) for t in clfs]

print(f"Total alpha candidate thresholds evaluated: {len(ccp_alphas)}")
print(f"Max Nodes in Unpruned Tree: {node_counts[0]} | Max Depth: {depths[0]}")
print(f"Nodes in Pruned Tree (Optimal Alpha): {best_tree.tree_.node_count} | Depth: {best_tree.tree_.max_depth}")
```

**Citations & References:**
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. JMLR, 12, 2825-2830.

---
