"""
Data definition for Term 5 CML Lecture 1:
Foundations of Machine Learning, Paradigms & Problem Formulation
"""

L1_DATA = {
    "schema_version": 1,
    "note_id": "cml-t5-l01",
    "term": "Term 5",
    "subject_code": "CML",
    "topic_title": "1. Foundations of Machine Learning, Paradigms & Problem Formulation",
    "tags": [
        "Machine Learning",
        "Mitchell Framework",
        "Supervised Learning",
        "Unsupervised Learning",
        "Classification",
        "Regression",
        "Mathematical Foundations",
        "EDA"
    ],
    "learning_objectives": [
        "Master the transition from classical deterministic programming to empirical machine learning.",
        "Formalize learning problems using Tom Mitchell's Task-Experience-Performance (T-E-P) framework.",
        "Differentiate classification and regression tasks based on target topology, loss functions, and evaluation metrics.",
        "Distinguish supervised, unsupervised, semi-supervised, and reinforcement learning paradigms.",
        "Select optimal visualization techniques (histograms, bar plots, scatter plots, line charts) for exploratory feature analysis."
    ],
    "summary": "An exhaustive, rigorous foundation for Classical Machine Learning. Covers the fundamental paradigm shift from rule-based software engineering to statistical learning, Tom Mitchell's formal ETP framework, the mathematical boundary between classification and regression, a complete taxonomy of machine learning paradigms, exploratory data analysis foundations, and concrete synthetic implementations.",
    "key_takeaways": [
        "Classical programming maps Inputs + Handcrafted Rules -> Outputs, whereas Machine Learning maps Inputs + Outputs/Structure -> Learned Mapping.",
        "A well-defined machine learning problem requires an unambiguous triplet: Task T, Experience E, and Performance Measure P.",
        "The classification vs. regression distinction is governed strictly by the target space Y (discrete classes vs. continuous real values), not the input features X.",
        "Posterior class probabilities P(Y=k|X) provide soft confidence scores, but the operational decision requires a threshold tau to produce discrete class assignments.",
        "Clustering is unsupervised and discovers emergent geometric grouping in X; classification is supervised and predicts pre-existing ground-truth labels Y.",
        "Histograms bin continuous distributions to reveal skewness and modality; scatter plots inspect bivariate relationships; bar charts compare discrete categorical frequencies."
    ],
    "last_updated": "2026-10-16T00:00:00Z",
    "approval_status": "approved",
    "sections": [
        {
            "section_id": "cml-l01-sec01",
            "heading": "1. The DSML Base Layer: Linear Algebra, Probability & Exploratory Visualization",
            "citations": [
                "Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer, Chapter 1.",
                "Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley.",
                "Strang, G. (2016). Introduction to Linear Algebra (5th ed.). Wellesley-Cambridge Press."
            ],
            "body": """### 1.1 Mathematical Representation of Tabular Data

In Classical Machine Learning, empirical reality is digitized into mathematical objects. A structured dataset is represented as a design matrix $\\mathbf{X} \\in \\mathbb{R}^{n \\times d}$ and a corresponding target vector $\\mathbf{y} \\in \\mathcal{Y}^n$, where:
- $n$ denotes the number of observations (samples, rows, or instances).
- $d$ denotes the feature dimensionality (variables, attributes, or columns).

$$\\mathbf{X} = \\begin{bmatrix} x_{1,1} & x_{1,2} & \\cdots & x_{1,d} \\\\ x_{2,1} & x_{2,2} & \\cdots & x_{2,d} \\\\ \\vdots & \\vdots & \\ddots & \\vdots \\\\ x_{n,1} & x_{n,2} & \\cdots & x_{n,d} \\end{bmatrix} = \\begin{bmatrix} \\mathbf{x}_1^T \\\\ \\mathbf{x}_2^T \\\\ \\vdots \\\\ \\mathbf{x}_n^T \\end{bmatrix}, \\quad \\mathbf{y} = \\begin{bmatrix} y_1 \\\\ y_2 \\\\ \\vdots \\\\ y_n \\end{bmatrix}$$

Each individual row $\\mathbf{x}_i \\in \\mathbb{R}^d$ is a feature vector residing in a $d$-dimensional coordinate space $\\mathcal{X} \\subseteq \\mathbb{R}^d$. The fundamental objective of classical machine learning is to identify a parameterized mapping function $f: \\mathcal{X} \\to \\mathcal{Y}$ within a chosen hypothesis space $\\mathcal{H}$ that maps input features to target responses with minimal expected loss.

```
Feature Space Geometry (d = 2):
       x_2 ^
           |             * Class A (y = 1)
           |         *  *  *
           |            *
           |     -------------------  Decision Boundary: w^T x + b = 0
           |        o    o
           |      o   o    o   o  Class B (y = 0)
           +------------------------------------> x_1
```

#### Linear Algebra Foundations
1. **Dot Products & Projections**: The inner product $\\langle \\mathbf{w}, \\mathbf{x} \\rangle = \\mathbf{w}^T \\mathbf{x} = \\sum_{j=1}^d w_j x_j = \\|\\mathbf{w}\\| \\|\\mathbf{x}\\| \\cos(\\theta)$ measures geometric alignment and forms the core computational primitive for linear classifiers, hyperplanes, and kernel methods.
2. **Norms as Lengths**: The Euclidean ($L_2$) norm $\\|\\mathbf{x}\\|_2 = \\sqrt{\\sum_{j=1}^d x_j^2}$ dictates distances in metric algorithms (KNN, K-Means), while the Manhattan ($L_1$) norm $\\|\\mathbf{x}\\|_1 = \\sum_{j=1}^d |x_j|$ induces sparsity in regularization.
3. **Hyperplanes**: A linear decision surface in $\\mathbb{R}^d$ is parameterized by a normal vector $\\mathbf{w} \\in \\mathbb{R}^d$ and bias $b \\in \\mathbb{R}$ such that $\\{ \\mathbf{x} \\in \\mathbb{R}^d \\mid \\mathbf{w}^T \\mathbf{x} + b = 0 \\}$.

#### Probability Foundations
1. **Expected Value & Variance**: For a random variable $X$, expectation $\\mathbb{E}[X] = \\int x p(x) dx$ captures central tendency, whereas variance $\\text{Var}(X) = \\mathbb{E}[(X - \\mathbb{E}[X])^2] = \\mathbb{E}[X^2] - (\\mathbb{E}[X])^2$ quantifies dispersion.
2. **Covariance Matrix**: For vector $\\mathbf{x}$, $\\mathbf{\\Sigma} = \\mathbb{E}[(\\mathbf{x} - \\boldsymbol{\\mu})(\\mathbf{x} - \\boldsymbol{\\mu})^T] \\in \\mathbb{R}^{d \\times d}$ encodes pairwise linear dependencies, critical for Multicollinearity diagnosis and Principal Component Analysis.
3. **Bayes' Theorem**: Provides the foundation for probabilistic prediction:
   $$P(Y = k \\mid \\mathbf{X} = \\mathbf{x}) = \\frac{P(\\mathbf{X} = \\mathbf{x} \\mid Y = k) P(Y = k)}{P(\\mathbf{X} = \\mathbf{x})} = \\frac{P(\\mathbf{X} = \\mathbf{x} \\mid Y = k) P(Y = k)}{\\sum_{c=1}^K P(\\mathbf{X} = \\mathbf{x} \\mid Y = c) P(Y = c)}$$

---

### 1.2 Exploratory Visualization Taxonomy

Before formulating an ML model, an engineer must diagnose the underlying geometric and statistical distribution of features using Exploratory Data Analysis (EDA). Selecting the wrong visualization tool obscures critical data anomalies.

| Analytical Objective | Primary Tool | Secondary / Advanced Tool | Key Diagnostic Signals |
| :--- | :--- | :--- | :--- |
| **Univariate Shape & Modality** | **Histogram** | Kernel Density Estimation (KDE) | Skewness, heavy tails, bimodality, outlier detection, zero-inflation |
| **Categorical Frequency Comparison** | **Bar Plot** | Count Plot | Class imbalance, cardinality, rare category presence |
| **Bivariate Continuous Association** | **Scatter Plot** | Hexbin / 2D Density Plot | Non-linear relationships, heteroscedasticity, clustering tendencies |
| **Ordered / Temporal Progression** | **Line Plot** | Rolling Average Ribbon | Trends, seasonal cycles, non-stationarity, concept drift |
| **Multi-Group Distribution Comparison** | **Box Plot** | Violin Plot | Interquartile range (IQR), median shifts, outlier density |

```
Distribution Types Visible in Histograms:
   Unimodal (Gaussian-like)        Bimodal (Sub-populations)         Right-Skewed (Income/Prices)
           _/\_                            _/\_      _/\_                 _/\_
         /      \\                        /    \\    /    \\               /    \\___
        /        \\                      /      \\__/      \\             /          \\______
     --+----------+-->               --+--------------------+-->       --+------------------->
```

> **Pedagogical Insight (Exam Scores Scenario)**: If given exam scores for 200 students to determine whether the cohort is centered around 70 or split into distinct high/low subgroups (bimodal), a **Histogram** (or KDE) answers the question immediately by partitioning continuous scores into bins and displaying frequency density. A scatter plot lacks density aggregation without a second variable, and a bar plot treats continuous scores as disjoint categories, fragmenting the distribution."""
        },
        {
            "section_id": "cml-l01-sec02",
            "heading": "2. The Paradigm Shift: Software Engineering (SDE) vs. Machine Learning (ML)",
            "citations": [
                "Domingos, P. (2012). A few useful things to know about machine learning. Communications of the ACM, 55(10), 78-87.",
                "Mitchell, T. M. (1997). Machine Learning. McGraw-Hill Education."
            ],
            "body": """### 2.1 Rule-Based Programming vs. Statistical Learning

The defining distinction between classical software engineering and machine learning lies in **where the algorithmic logic originates**:

```
Classical Software Engineering:
   [Data / Inputs] -----+
                        |---> [ Handcrafted Program / If-Else Rules ] ---> [ Outputs / Decisions ]
   [Explicit Rules] ----+

Machine Learning:
   [Data / Inputs] -----+
                        |---> [ Learning Algorithm / Optimizer ] --------> [ Learned Program / Model ]
   [Ground-Truth Labels]+                                                         |
                                                                                  v
   [New Unseen Data] --------------------------------------------------> [ Predictions ]
```

#### The Classical (SDE) Architecture
- **Paradigm**: Deductive reasoning. Humans analyze business requirements, formulate deterministic business rules, and translate them into control structures (`if/else`, loops, deterministic state machines).
- **Failure Mode**: When the underlying phenomenon exhibits high dimensionality, perceptual complexity (computer vision, natural language), or noisy statistical variance, human rule-authoring collapses under combinatorial explosion.
- **Example**: Constructing a spam filter by hardcoding rules like `if "Viagra" in email and "click here" in email: return SPAM`. Spammers immediately mutate strings (`V!agra`, `V-i-a-g-r-a`), requiring endless manual patching.

#### The Machine Learning (ML) Architecture
- **Paradigm**: Inductive inference. The human provides a parameterized model family (e.g., Logistic Regression, Decision Tree, Support Vector Machine) and an optimization criterion (loss function). The learning algorithm parses labeled historical examples and autonomously tunes internal parameters to minimize prediction error.
- **Maintenance**: When patterns shift (concept drift), an ML system adapts not by rewriting thousands of lines of code, but by **retraining the model pipeline on fresh empirical data**.

---

### 2.2 Deep Comparative Lifecycle Matrix

| Architectural Dimension | Classical Software Engineering (SDE) | Machine Learning Engineering (MLE) |
| :--- | :--- | :--- |
| **Logic Origin** | Human engineer explicitly writes every logical branch. | Optimization algorithm infers weights from empirical data. |
| **Specification Complexity** | Clear, deterministic, rule-based specifications. | Fuzzy, perceptual, probabilistic, or complex patterns. |
| **Data Dependency** | Minimal; small test fixtures suffice for validation. | Massive; performance scales directly with sample size and data quality. |
| **Verification & Testing** | Unit tests, integration tests, deterministic assertions. | Holdout validation, cross-validation, statistical significance tests. |
| **Failure Modes** | Logic bugs, syntax errors, uncaught runtime exceptions. | Generalization error, overfitting, underfitting, data leakage, distribution drift. |
| **Change Management** | Refactor source code, deploy code patch. | Re-collect data, retrain pipeline, validate on fresh holdout. |
| **Best Deployed When** | Business logic is stable, deterministic, and fully known. | The mathematical function mapping $X \\to Y$ is too complex to write by hand. |

---

### 2.3 The Pragmatic Heuristic: When to Use ML

An engineer should never deploy machine learning when a simple, deterministic rule suffices:

$$\\text{Decision Framework} = \\begin{cases} \\text{Classical SDE Code} & \\text{if rules are } < 20 \\text{ branches and domain is static} \\\\ \\text{Heuristic / Lookup} & \\text{if 100\\% determinism and zero tolerance for statistical error} \\\\ \\text{Machine Learning} & \\text{if inputs are high-dimensional, relationships noisy, and labeled data exists} \\end{cases}$$

> **Core Rule of Thumb**: If you can write a compact, robust `if/else` block that solves the problem with 100% compliance, do not train a model. If listing all rules requires thousands of fragile conditions, reach for Machine Learning."""
        },
        {
            "section_id": "cml-l01-sec03",
            "heading": "3. Tom Mitchell's Mathematical Framework for Well-Defined Learning",
            "citations": [
                "Mitchell, T. M. (1997). Machine Learning. McGraw-Hill Education, Section 1.2.",
                "Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.). Pearson."
            ],
            "body": """### 3.1 The Canonical Definition

In his seminal 1997 textbook, computer scientist Tom M. Mitchell formulated the foundational, universally accepted mathematical definition of machine learning:

> **Mitchell's Learning Criterion**:
> *"A computer program is said to **learn** from experience $\\mathcal{E}$ with respect to some class of tasks $\\mathcal{T}$ and performance measure $\\mathcal{P}$, if its performance at tasks in $\\mathcal{T}$, as measured by $\\mathcal{P}$, improves with experience $\\mathcal{E}$."*

```
         +-------------------------------------------------------+
         |              Tom Mitchell's ETP Triad                 |
         +-------------------------------------------------------+
         |                                                       |
         |   [Task T] <------------ Defines What To Do           |
         |      ^                   (Mapping f: X -> Y)          |
         |      |                                                |
         |   [Performance P] <----- Defines How Success Is Scored|
         |      ^                   (Metric evaluated on holdout)|
         |      |                                                |
         |   [Experience E] <------ Defines The Training Fuel    |
         |                          (Data samples, interactions) |
         |                                                       |
         +-------------------------------------------------------+
```

An engineering initiative cannot be classified as a machine learning project without a rigorous, unambiguous specification of all three constituents:

$$\\text{Well-Defined Learning Task} = \\langle \\mathcal{T}, \\mathcal{E}, \\mathcal{P} \\rangle$$

---

### 3.2 Formal Dissection of the ETP Components

#### 1. Task ($\\mathcal{T}$)
The task is not the learning process itself; the task is the **operational execution** that the system must perform on inputs. Formally, it defines the functional domain and codomain:
$$f: \\mathcal{X} \\to \\mathcal{Y}$$
- **Spam Filtering**: Classify an incoming raw email document $\\mathbf{x} \\in \\mathcal{X}$ into $\\mathcal{Y} \\in \\{\\text{Spam}, \\text{Ham}\\}$.
- **Autonomous Driving**: Predict instantaneous steering angle $\\theta \\in [-180^\\circ, +180^\\circ]$ and braking force $b \\in [0, 1]$ given LiDAR point clouds and camera frames.
- **Property Valuation**: Estimate fair market valuation $\\hat{y} \\in \\mathbb{R}^+$ given district census features.

#### 2. Experience ($\\mathcal{E}$)
Experience represents the information corpus exposed to the algorithm from which it extracts statistical regularities. Experience varies across learning paradigms:
- **Supervised Experience**: Labeled historical observations $\\mathcal{D} = \\{(\\mathbf{x}_i, y_i)\\}_{i=1}^n \\sim p_{\\text{data}}(\\mathbf{x}, y)$.
- **Unsupervised Experience**: Unlabeled sensory observations $\\mathcal{D} = \\{\\mathbf{x}_i\\}_{i=1}^n \\sim p_{\\text{data}}(\\mathbf{x})$.
- **Reinforcement Experience**: Trajectories of state-action-reward sequences $\\tau = (s_0, a_0, r_0, s_1, a_1, r_1, \\dots)$ gathered via interactive policy execution in an environment.

#### 3. Performance Measure ($\\mathcal{P}$)
Performance provides the objective quantitative metric to evaluate how effectively the program executes task $\\mathcal{T}$.
- **Critical Requirement**: $\\mathcal{P}$ must be evaluated on an independent, unseen **holdout dataset** $\\mathcal{D}_{\\text{test}}$ drawn from the same data-generating distribution:
  $$\\mathcal{P} = \\mathbb{E}_{(\\mathbf{x}, y) \\sim \\mathcal{D}_{\\text{test}}} [ \\mathcal{M}(f(\\mathbf{x}), y) ]$$
- Selecting $\\mathcal{P}$ requires alignment with business cost matrices: in cancer screening, False Negatives (missing a tumor) carry fatal costs compared to False Positives, mandating High Recall over raw Accuracy.

---

### 3.3 Concrete Industrial ETP Formulations

| Problem Domain | Task ($\\mathcal{T}$) | Experience ($\\mathcal{E}$) | Performance Measure ($\\mathcal{P}$) |
| :--- | :--- | :--- | :--- |
| **Email Spam Classification** | Classify an incoming email message as spam or non-spam. | Historical corpus of 500,000 human-annotated emails with spam/ham flags. | $F_1$-Score and Precision at 99% Recall on a held-out test mailbox. |
| **California Real Estate Valuation** | Predict the continuous median sale price of a residential parcel. | Tabular transaction records from 1990–2020 containing physical and geographic attributes. | Root Mean Squared Error (RMSE) and $R^2$ score on post-2020 holdout transactions. |
| **Credit Card Fraud Detection** | Flag incoming card transactions as fraudulent or legitimate in real time. | Logged transaction streams with terminal IDs, amounts, and bank fraud dispute chargebacks. | Area Under the Precision-Recall Curve (PR-AUC) and False Positive Rate at 95% Recall. |
| **Autonomous Vehicle Navigation** | Determine continuous steering torque and throttle commands per video frame. | 100,000 hours of human driving telemetry, forward video feeds, and LiDAR point clouds. | Mean squared trajectory deviation from expert driver paths and collision rate per 1,000 km. |"""
        },
        {
            "section_id": "cml-l01-sec04",
            "heading": "4. Supervised Learning Taxonomy: Classification vs. Regression",
            "citations": [
                "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). Springer, Chapters 2 & 7.",
                "Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press."
            ],
            "body": """### 4.1 The Fundamental Boundary: Target Topology

In Supervised Machine Learning, the learner is supplied with labeled pairs $\\mathcal{D} = \\{(\\mathbf{x}_i, y_i)\\}_{i=1}^n$. The division between **Classification** and **Regression** is dictated exclusively by the mathematical nature of the **target space $\\mathcal{Y}$**:

$$\\text{Supervised Task} = \\begin{cases} \\text{Classification} & \\iff \\mathcal{Y} \\text{ is a discrete, categorical set } \\{C_1, C_2, \\dots, C_K\\} \\\\ \\text{Regression} & \\iff \\mathcal{Y} \\text{ is a continuous metric space } \\mathbb{R} \\text{ (or } \\mathbb{R}^k \\text{)} \\end{cases}$$

> **Crucial Rule on Feature Types**: Inputs $\\mathbf{x}$ can be continuous, discrete, ordinal, categorical, or mixed in **both** classification and regression. The input feature types do not determine the problem class; **only the target $y$ determines the problem class**.

```
Classification (Discrete Decision Regions):       Regression (Continuous Response Surface):
         x_2 ^                                             y ^
             |  Class 0     /    Class 1                     |            *   *  *  f(x)
             |      o      /        *                        |       *   *  *
             |    o   o   /       *   *                      |     *   *
             |   o   o   /         *                         |   *
             +----------/-------------> x_1                  +----------------------------> x
```

---

### 4.2 Comprehensive Classification vs. Regression Matrix

| Property | Classification | Regression |
| :--- | :--- | :--- |
| **Target Space $\\mathcal{Y}$** | Qualitative / Discrete labels: $\\mathcal{Y} \\in \\{0, 1\\}$ or $\\{1, \\dots, K\\}$ | Quantitative / Continuous: $\\mathcal{Y} \\subseteq \\mathbb{R}$ |
| **Model Output** | Class index $k$, or posterior probability vector $\\hat{\\mathbf{p}} \\in [0, 1]^K$ | Continuous scalar estimate $\\hat{y} \\in \\mathbb{R}$ |
| **Canonical Loss Functions** | - 0-1 Loss: $\\mathbb{I}(y \\neq \\hat{y})$<br>- Binary Cross-Entropy / Log-Loss:<br>  $\\mathcal{L}_{\\text{BCE}} = -[y \\log \\hat{p} + (1-y) \\log(1-\\hat{p})]$<br>- Categorical Cross-Entropy | - Mean Squared Error (MSE): $\\frac{1}{n} \\sum (y_i - \\hat{y}_i)^2$<br>- Mean Absolute Error (MAE): $\\frac{1}{n} \\sum |y_i - \\hat{y}_i|$<br>- Huber Loss: Quadratic for small $|e|$, linear for large $|e|$ |
| **Standard Evaluation Metrics** | Accuracy, Precision, Recall, $F_1$-Score, Specificity, ROC-AUC, PR-AUC | MAE, MSE, RMSE, Mean Absolute Percentage Error (MAPE), $R^2$ |
| **Geometric Interpretation** | Partitions $\\mathcal{X}$ into $K$ decision regions separated by boundaries. | Constructs a continuous hypersurface spanning feature space $\\mathcal{X}$. |
| **Industrial Examples** | - Loan default prediction (Default / Repay)<br>- Medical diagnosis (Malignant / Benign)<br>- Optical character recognition (Digits 0–9) | - Real estate price appraisal (INR/USD)<br>- Next-day stock closing price<br>- Delivery duration estimation (Minutes) |

---

### 4.3 The Probability Nuance: Posterior Probabilities vs. Continuous Targets

A frequent source of beginner confusion: *Many classification algorithms (Logistic Regression, Softmax, Random Forest) output continuous probabilities $\\hat{p} \\in [0, 1]$. Does this convert classification into regression?*

**Mathematical Reality**: **No.** 
1. Posterior probabilities $\\hat{p} = P(Y = 1 \\mid \\mathbf{X} = \\mathbf{x})$ are internal model confidence estimates, constrained strictly to the unit interval $[0, 1]$ and summing to 1 across classes.
2. The operational task remains discrete assignment. A decision rule parameterized by a threshold $\\tau \\in (0, 1)$ maps continuous probability back to the discrete label space:
   $$\\hat{y} = \\begin{cases} 1 & \\text{if } P(Y = 1 \\mid \\mathbf{x}) \\ge \\tau \\\\ 0 & \\text{if } P(Y = 1 \\mid \\mathbf{x}) < \\tau \\end{cases}$$
3. Regression models, by contrast, predict an unbounded or metric continuous quantity $\\hat{y} \\in \\mathbb{R}$ evaluated via residuals $(y - \\hat{y})$, where standard distance metrics have physical meaning ($10 error in house pricing carries monetary meaning; an error between class 1 and class 2 in categorical space has no natural Euclidean distance).

---

### 4.4 Subtle Boundary Cases in Practice
- **Count Data (e.g., number of hospital admissions, number of clicks)**: Target $y \\in \\{0, 1, 2, \\dots\\}$ is discrete, but ordered and metric. Usually formulated as **Poisson / Negative-Binomial Regression**, not classification, because the numeric difference between 5 and 6 has the same scale as between 100 and 101.
- **Ordinal Targets (e.g., Credit Rating: AAA, AA, A, BBB, Default)**: Discrete classes with strict order. Can be framed as multi-class classification (losing order) or **Ordinal Regression** (preserving order constraints)."""
        },
        {
            "section_id": "cml-l01-sec05",
            "heading": "5. The Full Taxonomy of Machine Learning Paradigms",
            "citations": [
                "Murphy, K. P. (2022). Probabilistic Machine Learning: An Introduction. MIT Press, Chapter 1.",
                "Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction (2nd ed.). MIT Press."
            ],
            "body": """### 5.1 Beyond Supervised Learning

Machine learning paradigms are categorized by the **nature of supervisory feedback** provided during the training phase:

```
                            +-----------------------------------------------+
                            |          Machine Learning Paradigms           |
                            +-----------------------------------------------+
                                    |               |               |
             +----------------------+               |               +----------------------+
             |                                      |                                      |
             v                                      v                                      v
   [ Supervised Learning ]               [ Unsupervised Learning ]              [ Reinforcement Learning ]
   Labeled pairs (x_i, y_i)              Unlabeled data {x_i}                   Agent-Environment Interaction
   - Classification                      - Clustering (K-Means, GMM)            - Markov Decision Process
   - Regression                          - Dimensionality Reduction (PCA)       - State, Action, Reward
                                         - Density Estimation                   - Policy Optimization
```

---

### 5.2 Supervised vs. Unsupervised Learning

#### Supervised Learning
- **Input Corpus**: Labeled pairs $\\mathcal{D} = \\{(\\mathbf{x}_i, y_i)\\}_{i=1}^n$.
- **Goal**: Infer an underlying function $f: \\mathcal{X} \\to \\mathcal{Y}$ such that generalized risk $\\mathbb{E}[\\mathcal{L}(f(\\mathbf{x}), y)]$ is minimized on future unseen data.
- **Evaluation**: Clear ground-truth targets exist on holdout sets; error is directly measurable via metrics (RMSE, Accuracy, Log Loss).

#### Unsupervised Learning
- **Input Corpus**: Unlabeled instances $\\mathcal{D} = \\{\\mathbf{x}_i\\}_{i=1}^n$.
- **Goal**: Uncover intrinsic structural properties, probability densities $p(\\mathbf{x})$, geometric manifolds, or latent cluster assignments $z_i \\in \\{1, \\dots, K\\}$.
- **Core Branches**:
  1. **Clustering**: Grouping instances such that intra-cluster similarity is maximized and inter-cluster similarity is minimized (e.g., K-Means, Agglomerative Hierarchical, DBSCAN).
  2. **Dimensionality Reduction**: Projecting $d$-dimensional data into $k \\ll d$ dimensions while preserving variance or topological neighborhood geometry (e.g., PCA, t-SNE, UMAP).
  3. **Density Estimation**: Estimating continuous probability density functions $p(\\mathbf{x})$ to identify rare anomalous anomalies (e.g., Gaussian Mixture Models, Isolation Forests).
- **Evaluation**: Inherently difficult and often subjective. Utilizes internal geometric criteria (Silhouette Coefficient, Davies-Bouldin Index, Explained Variance Ratio) combined with qualitative human domain inspection.

---

### 5.3 The Critical Trap: Clustering $\\neq$ Classification

A frequent industrial error is attempting to solve a classification problem using clustering, or vice versa:

| Dimension | Classification (Supervised) | Clustering (Unsupervised) |
| :--- | :--- | :--- |
| **Ground-Truth Labels** | **Mandatory**. Pre-defined class names must exist in training data. | **Zero**. Operates purely on unannotated feature geometry. |
| **Cluster / Class Origin** | Classes represent pre-determined real-world categories (e.g., Fraud, Tumor). | Clusters are emergent geometric groupings discovered by distance algorithms. |
| **Output Semantics** | Assigns new sample to a known semantic label: $P(\\text{Spam} \\mid \\mathbf{x})$. | Assigns new sample to an arbitrary cluster index: $\\text{Cluster } 2$. |
| **Alignment Risk** | None; explicitly optimizes to predict the target label. | Discovered clusters rarely align cleanly with human-desired business categories. |

> **Real-World Scenarios from Class**:
> 1. **HR Candidate Screening**: An HR director asks to categorize applicants into pre-existing job tiers (`Junior Engineer`, `Senior Engineer`, `Tech Lead`).
>    - *Correct Solution*: **Supervised Classification**. Clustering will merely cluster candidates by arbitrary geometry (e.g., word count or university names), which will not match HR's official tiers.
> 2. **Customer Segmentation for New Marketing Campaigns**: An e-commerce company has 2 million customer transaction records without any pre-existing group tags and wants to discover natural spending personas.
>    - *Correct Solution*: **Unsupervised Clustering**. Since no ground-truth persona labels exist, the algorithm discovers emergent behavioral segments.
> 3. **Raw Customer Feedback Topics**: Given 50,000 unlabelled open-text reviews, identify what themes customers discuss.
>    - *Correct Solution*: **Unsupervised Topic Modeling / Clustering**. Once clusters are reviewed and named by human analysts, they can be used to train a supervised text classifier.

---

### 5.4 Extended Paradigms: Semi-Supervised, Self-Supervised & RL

1. **Semi-Supervised Learning**: Bridges the gap when labeling data is prohibitively expensive (e.g., medical pathology slides). Combines a small labeled corpus $\\mathcal{D}_L = \\{(\\mathbf{x}_i, y_i)\\}_{i=1}^{n_L}$ with a vast unlabeled corpus $\\mathcal{D}_U = \\{\\mathbf{x}_j\\}_{j=1}^{n_U}$ ($n_U \\gg n_L$). Exploits manifold continuity assumptions to propagate labels.
2. **Self-Supervised Learning**: Generates pseudo-labels directly from unlabeled data structure (e.g., masking words in a sentence and predicting the masked token in BERT/GPT, or predicting spatial rotation of image patches).
3. **Reinforcement Learning (RL)**: Learning via trial-and-error interaction with a dynamic environment formalized as a Markov Decision Process (MDP): $\\langle \\mathcal{S}, \\mathcal{A}, \\mathcal{P}, \\mathcal{R}, \\gamma \\rangle$. An agent observes state $s_t$, takes action $a_t$, receives scalar reward $r_t$, and transitions to $s_{t+1}$, optimizing cumulative discounted future return $G_t = \\sum_{k=0}^\\infty \\gamma^k r_{t+k}$."""
        },
        {
            "section_id": "cml-l01-sec06",
            "heading": "6. Hands-On Synthetic Demonstration: Toy Classification vs. Regression",
            "citations": [
                "Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830.",
                "Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95."
            ],
            "body": """### 6.1 Practical Implementation Architecture

To solidify the conceptual boundaries, we construct an end-to-end Python implementation demonstrating the mathematical contrast between a 2D Classification problem (partitioning feature space into discrete decision regions) and a 1D Regression problem (fitting a continuous response function to noisy metric targets).

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score

# Set deterministic pseudorandom seed
rng = np.random.default_rng(42)

# =====================================================================
# 1. SYNTHETIC CLASSIFICATION: Discrete Classes in 2D Feature Space
# =====================================================================
n_samples = 100
# Generate Class 0: Centered at [-1.2, -0.8]
X_class0 = rng.normal(loc=[-1.2, -0.8], scale=0.55, size=(n_samples, 2))
y_class0 = np.zeros(n_samples, dtype=int)

# Generate Class 1: Centered at [1.2, 0.8]
X_class1 = rng.normal(loc=[1.2, 0.8], scale=0.55, size=(n_samples, 2))
y_class1 = np.ones(n_samples, dtype=int)

X_clf = np.vstack([X_class0, X_class1])
y_clf = np.concatenate([y_class0, y_class1])

# Fit Linear Classifier (Logistic Regression)
clf = LogisticRegression()
clf.fit(X_clf, y_clf)
y_clf_pred = clf.predict(X_clf)
clf_acc = accuracy_score(y_clf, y_clf_pred)

# =====================================================================
# 2. SYNTHETIC REGRESSION: Continuous Response Surface in 1D Space
# =====================================================================
x_reg = np.linspace(-3.0, 3.0, 120).reshape(-1, 1)
# True underlying function: y = 2.5 * x + 1.2 + Gaussian noise N(0, 1.2)
noise = rng.normal(loc=0.0, scale=1.2, size=x_reg.shape)
y_reg = 2.5 * x_reg + 1.2 + noise

# Fit Ordinary Least Squares Linear Regression
reg = LinearRegression()
reg.fit(x_reg, y_reg)
y_reg_pred = reg.predict(x_reg)

mse_val = mean_squared_error(y_reg, y_reg_pred)
r2_val = r2_score(y_reg, y_reg_pred)

print(f"Classification Training Accuracy: {clf_acc * 100:.2f}%")
print(f"Regression Mean Squared Error (MSE): {mse_val:.4f}")
print(f"Regression Coefficient of Determination (R^2): {r2_val:.4f}")
```

---

### 6.2 Visualizing the Dual Paradigms

```python
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel 1: Classification Decision Surface
xx, yy = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
grid = np.c_[xx.ravel(), yy.ravel()]
probs = clf.predict_proba(grid)[:, 1].reshape(xx.shape)

axes[0].contourf(xx, yy, probs, levels=20, cmap="RdBu_r", alpha=0.3)
axes[0].contour(xx, yy, probs, levels=[0.5], colors="black", linestyles="--", linewidths=2)
axes[0].scatter(X_class0[:, 0], X_class0[:, 1], color="blue", edgecolors="k", label="Class 0 (y=0)")
axes[0].scatter(X_class1[:, 0], X_class1[:, 1], color="red", edgecolors="k", label="Class 1 (y=1)")
axes[0].set_title(f"Classification: Decision Boundary (Acc = {clf_acc*100:.1f}%)")
axes[0].set_xlabel("Feature $x_1$")
axes[0].set_ylabel("Feature $x_2$")
axes[0].legend()
axes[0].grid(True, linestyle=":", alpha=0.6)

# Panel 2: Regression Response Curve
axes[1].scatter(x_reg, y_reg, color="darkgreen", alpha=0.6, edgecolors="k", label="Observations $(x_i, y_i)$")
axes[1].plot(x_reg, y_reg_pred, color="black", linewidth=2.5, label=f"Fit: $\\hat{{y}} = {reg.coef_[0][0]:.2f}x + {reg.intercept_[0]:.2f}$")
axes[1].fill_between(x_reg.ravel(), (y_reg_pred - np.sqrt(mse_val)).ravel(), (y_reg_pred + np.sqrt(mse_val)).ravel(), color="green", alpha=0.15, label="$\\pm 1$ RMSE Residual Band")
axes[1].set_title(f"Regression: Continuous Surface ($R^2 = {r2_val:.3f}$)")
axes[1].set_xlabel("Feature $x$")
axes[1].set_ylabel("Target $y$ (Continuous)")
axes[1].legend()
axes[1].grid(True, linestyle=":", alpha=0.6)

plt.tight_layout()
plt.show()
```

---

### 6.3 Diagnostic Summary Table

| Operational Aspect | Panel 1 (Classification) | Panel 2 (Regression) |
| :--- | :--- | :--- |
| **Output Topology** | Discrete partition (Blue vs. Red separated by dashed 0.5 probability line). | Continuous slope $\\hat{y} = w x + b$ spanning the real number line. |
| **Residual Meaning** | Cross-entropy distance between predicted probability distribution and one-hot label. | Metric vertical distance $(y_i - \\hat{y}_i)$ in measurement units (e.g., dollars, meters). |
| **Evaluation Criterion** | Percentage of samples placed on correct side of boundary (Accuracy). | Variance explained by fitted hyper-plane relative to horizontal baseline ($R^2$). |"""
        }
    ],
    "quiz": {
        "title": "Comprehensive Examination: Foundations of Classical Machine Learning",
        "description": "25-question examination testing linear algebra and probability foundations, classical SDE vs ML paradigms, Tom Mitchell's ETP framework, classification vs regression nuances, and machine learning taxonomy.",
        "time_limit": "30 mins",
        "questions": [
            {
                "id": "q-cml-l01-01",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "DSML Visualization Foundations",
                "question": "An analytics engineer is examining exam scores for 200 students to determine whether the distribution is unimodal around 70 or split into distinct bimodal cohorts. Which plot answers this question most directly?",
                "options": [
                    {"id": "opt-1", "text": "Bar Plot", "is_correct": False},
                    {"id": "opt-2", "text": "Histogram (or KDE Plot)", "is_correct": True},
                    {"id": "opt-3", "text": "Scatter Plot", "is_correct": False},
                    {"id": "opt-4", "text": "Line Plot", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "A Histogram partitions continuous values into discrete bins and computes frequency counts, directly revealing distribution shape, skewness, and modality (e.g., unimodal vs bimodal). Bar plots are for categorical counts, scatter plots require two continuous variables, and line plots display ordered/temporal trends."
            },
            {
                "id": "q-cml-l01-02",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "ML Paradigm Shift",
                "question": "Which of the following statements provides the most accurate and foundational definition of Machine Learning?",
                "options": [
                    {"id": "opt-1", "text": "Machine Learning is the science of programming computers with exhaustive expert rules.", "is_correct": False},
                    {"id": "opt-2", "text": "Machine Learning refers strictly to algorithms that learn from manually labeled categorical data.", "is_correct": False},
                    {"id": "opt-3", "text": "Machine Learning is the field of study that gives computers the ability to learn mappings from empirical data without being explicitly programmed with hand-crafted rules.", "is_correct": True},
                    {"id": "opt-4", "text": "Machine Learning is exclusively focused on controlling physical robotic systems.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-3"],
                "explanation": "Arthur Samuel's classic definition states that Machine Learning gives computers the ability to learn without being explicitly programmed. Rather than hand-authoring deterministic rules, an algorithm infers functional mappings from empirical data."
            },
            {
                "id": "q-cml-l01-03",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Tom Mitchell Framework",
                "question": "In Tom Mitchell's formal framework for a well-defined learning task, what do the symbols T, E, and P represent?",
                "options": [
                    {"id": "opt-1", "text": "T = Training, E = Evaluation, P = Prediction", "is_correct": False},
                    {"id": "opt-2", "text": "T = Task, E = Experience, P = Performance Measure", "is_correct": True},
                    {"id": "opt-3", "text": "T = Target, E = Error, P = Probability", "is_correct": False},
                    {"id": "opt-4", "text": "T = Topology, E = Epochs, P = Precision", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Tom Mitchell's formal learning triplet consists of Task (T), Experience (E), and Performance Measure (P). A computer program learns if its measured performance P at task T improves with experience E."
            },
            {
                "id": "q-cml-l01-04",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Regression Fundamentals",
                "question": "What is the primary objective of regression analysis in machine learning?",
                "options": [
                    {"id": "opt-1", "text": "To classify observations into discrete mutually exclusive categories.", "is_correct": False},
                    {"id": "opt-2", "text": "To discover emergent cluster groupings without any target labels.", "is_correct": False},
                    {"id": "opt-3", "text": "To predict a continuous quantitative outcome or real-valued scalar target.", "is_correct": True},
                    {"id": "opt-4", "text": "To project high-dimensional data onto lower-dimensional manifolds for visualization.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-3"],
                "explanation": "Regression algorithms map input features to continuous numerical responses Y in R (such as real estate valuation, temperature, or travel duration)."
            },
            {
                "id": "q-cml-l01-05",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Classification Fundamentals",
                "question": "A real estate brokerage builds a system to predict whether a prospective home buyer will purchase an 'Apartment', 'Villa', or 'Agricultural Plot'. What kind of machine learning task is this?",
                "options": [
                    {"id": "opt-1", "text": "Continuous Regression", "is_correct": False},
                    {"id": "opt-2", "text": "Multi-class Classification", "is_correct": True},
                    {"id": "opt-3", "text": "Unsupervised Dimensionality Reduction", "is_correct": False},
                    {"id": "opt-4", "text": "Density Estimation", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "The target variable consists of three discrete, qualitative categories ('Apartment', 'Villa', 'Plot'). Predicting qualitative classes is multi-class classification."
            },
            {
                "id": "q-cml-l01-06",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Supervised vs Unsupervised",
                "question": "You possess a dataset of 500,000 unlabelled customer transaction logs and want to identify natural spending personas without any pre-existing group tags. Is this supervised or unsupervised learning?",
                "options": [
                    {"id": "opt-1", "text": "Supervised Learning", "is_correct": False},
                    {"id": "opt-2", "text": "Unsupervised Learning", "is_correct": True},
                    {"id": "opt-3", "text": "Reinforcement Learning", "is_correct": False},
                    {"id": "opt-4", "text": "Semi-Supervised Learning", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Because no pre-existing ground-truth labels Y are provided in the training data, discovering natural patterns or groups in X is an unsupervised learning task (clustering)."
            },
            {
                "id": "q-cml-l01-07",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Supervised Learning Scenarios",
                "question": "An algorithm is trained on 10 years of historical stock market data (prices, volumes, moving averages) to predict the closing price of Apple Inc. stock tomorrow. Is this supervised or unsupervised learning?",
                "options": [
                    {"id": "opt-1", "text": "Supervised Learning", "is_correct": True},
                    {"id": "opt-2", "text": "Unsupervised Learning", "is_correct": False},
                    {"id": "opt-3", "text": "Pure Clustering", "is_correct": False},
                    {"id": "opt-4", "text": "Self-Organizing Mapping", "is_correct": False}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "The training dataset contains historical input features paired with a known ground-truth numerical target (tomorrow's closing price). This is supervised regression."
            },
            {
                "id": "q-cml-l01-08",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Clustering vs Classification",
                "question": "An HR director asks you to build an ML system to categorize job applicants into the company's pre-existing, official job levels (Level 1, Level 2, Level 3). Which approach should you recommend?",
                "options": [
                    {"id": "opt-1", "text": "An unsupervised K-Means clustering algorithm that creates emergent candidate clusters.", "is_correct": False},
                    {"id": "opt-2", "text": "A supervised classification model trained on historically labeled applicant records.", "is_correct": True},
                    {"id": "opt-3", "text": "An unsupervised Principal Component Analysis system without labels.", "is_correct": False},
                    {"id": "opt-4", "text": "A reinforcement learning agent operating without an environment.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "The business objective requires assigning candidates to predefined, established organizational tiers (Level 1, 2, 3). Supervised classification trains explicitly to predict these known classes, whereas unsupervised clustering invents arbitrary geometric clusters that do not correspond to HR's official tiers."
            },
            {
                "id": "q-cml-l01-09",
                "type": "multiple_choice",
                "difficulty": "medium",
                "subtopic": "Classification Probabilities",
                "question": "Which of the following statements regarding classification algorithms and output probabilities are TRUE? (Select all that apply)",
                "options": [
                    {"id": "opt-1", "text": "Classification models map input features to discrete categorical classes.", "is_correct": True},
                    {"id": "opt-2", "text": "Predicting class probabilities turns a classification model into a continuous regression model.", "is_correct": False},
                    {"id": "opt-3", "text": "A classification algorithm can accept both continuous and discrete input features simultaneously.", "is_correct": True},
                    {"id": "opt-4", "text": "Class probabilities can be converted to discrete predictions using a decision threshold tau.", "is_correct": True}
                ],
                "correctOptionIds": ["opt-1", "opt-3", "opt-4"],
                "explanation": "Classification targets discrete qualitative classes. Inputs X can be continuous, discrete, or mixed. While algorithms output posterior probabilities P(Y=1|X) in [0, 1], this represents internal model confidence, which a threshold tau converts into discrete labels; it does NOT turn classification into regression. Option 2 is false."
            },
            {
                "id": "q-cml-l01-10",
                "type": "multiple_choice",
                "difficulty": "medium",
                "subtopic": "SDE vs ML Architecture",
                "question": "In software engineering versus machine learning architecture, which statements correctly characterize their operational differences? (Select all that apply)",
                "options": [
                    {"id": "opt-1", "text": "Classical SDE systems rely on human engineers explicitly writing logic rules, whereas ML systems learn mappings from data.", "is_correct": True},
                    {"id": "opt-2", "text": "When business patterns shift, classical code is updated by retraining, while ML is updated by manual rule edits.", "is_correct": False},
                    {"id": "opt-3", "text": "If a problem domain can be completely solved by a simple, static 5-line if/else block, classical code is preferred over ML.", "is_correct": True},
                    {"id": "opt-4", "text": "ML systems are fundamentally inductive, deriving generalized patterns from empirical sample datasets.", "is_correct": True}
                ],
                "correctOptionIds": ["opt-1", "opt-3", "opt-4"],
                "explanation": "Option 2 is inverted: classical code requires manual rule edits, while ML systems are retrained on fresh empirical data. Options 1, 3, and 4 are fundamental tenets of the SDE vs ML paradigm shift."
            },
            {
                "id": "q-cml-l01-11",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Tom Mitchell Framework Formulation",
                "question": "A team builds an automated credit card fraud detection system. Which of the following provides the most rigorous and complete formulation of Tom Mitchell's ETP triad?",
                "options": [
                    {"id": "opt-1", "text": "T = Train Logistic Regression; E = Python scikit-learn library; P = Fast execution time", "is_correct": False},
                    {"id": "opt-2", "text": "T = Predict whether a transaction is fraudulent or legitimate; E = Historical transaction logs with confirmed chargebacks; P = Area Under the Precision-Recall Curve (PR-AUC) on unseen holdout transactions", "is_correct": True},
                    {"id": "opt-3", "text": "T = Calculate mean transaction volume; E = Unsupervised customer clustering; P = High silhouette score", "is_correct": False},
                    {"id": "opt-4", "text": "T = Detect credit card numbers; E = Regex pattern matching; P = 100% unit test coverage", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Option 2 correctly defines: Task T as operational fraud classification on transactions; Experience E as historical transactions with verified chargeback ground truth; Performance P as PR-AUC on an independent holdout dataset. Option 1 confuses the learning tool with ETP components."
            },
            {
                "id": "q-cml-l01-12",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Target Topology & Boundary Cases",
                "question": "An emergency department builds a model to predict the 'number of hours a patient will wait before triage' (a continuous positive number) and another model to predict 'triage acuity level' (1-Immediate, 2-Emergency, 3-Urgent, 4-Semi-Urgent, 5-Non-Urgent). How should these two tasks be formulated?",
                "options": [
                    {"id": "opt-1", "text": "Both tasks are multi-class classification.", "is_correct": False},
                    {"id": "opt-2", "text": "Wait time is Regression; Triage acuity is Multi-class / Ordinal Classification.", "is_correct": True},
                    {"id": "opt-3", "text": "Wait time is Unsupervised Clustering; Triage acuity is Binary Classification.", "is_correct": False},
                    {"id": "opt-4", "text": "Both tasks are Continuous Regression.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Waiting time in hours is a continuous real-valued measurement in R+, requiring Regression. Triage acuity level consists of 5 discrete ordered priority buckets, requiring Multi-class or Ordinal Classification."
            },
            {
                "id": "q-cml-l01-13",
                "type": "multiple_choice",
                "difficulty": "medium",
                "subtopic": "Evaluation Metrics by Task",
                "question": "Which of the following evaluation metrics are strictly designed for REGRESSION tasks, rather than classification? (Select all that apply)",
                "options": [
                    {"id": "opt-1", "text": "Mean Absolute Error (MAE)", "is_correct": True},
                    {"id": "opt-2", "text": "Area Under the ROC Curve (ROC-AUC)", "is_correct": False},
                    {"id": "opt-3", "text": "Root Mean Squared Error (RMSE)", "is_correct": True},
                    {"id": "opt-4", "text": "Coefficient of Determination (R-squared)", "is_correct": True}
                ],
                "correctOptionIds": ["opt-1", "opt-3", "opt-4"],
                "explanation": "MAE, RMSE, and R-squared evaluate numerical residual differences (y - y_hat) in continuous space and are regression metrics. ROC-AUC evaluates the trade-off between True Positive Rate and False Positive Rate across classification thresholds."
            },
            {
                "id": "q-cml-l01-14",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Exploratory Visualization Scenarios",
                "question": "A data scientist wants to inspect the relationship between 'Years of Experience' (continuous numeric) and 'Annual Salary' (continuous numeric) across 5,000 engineers. Which plot is best suited for this task?",
                "options": [
                    {"id": "opt-1", "text": "Bar Plot", "is_correct": False},
                    {"id": "opt-2", "text": "Histogram", "is_correct": False},
                    {"id": "opt-3", "text": "Scatter Plot", "is_correct": True},
                    {"id": "opt-4", "text": "Pie Chart", "is_correct": False}
                ],
                "correctOptionIds": ["opt-3"],
                "explanation": "A scatter plot plots two continuous variables against orthogonal Cartesian axes, revealing linear or non-linear correlation, clustering, and heteroscedasticity. Histograms are univariate; bar plots compare discrete categorical aggregations."
            },
            {
                "id": "q-cml-l01-15",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Linear Algebra in Feature Spaces",
                "question": "In a d-dimensional feature space, what geometric object represents the decision boundary of a standard linear classifier such as Logistic Regression or a Linear SVM?",
                "options": [
                    {"id": "opt-1", "text": "A (d - 1)-dimensional affine hyperplane defined by w^T x + b = 0.", "is_correct": True},
                    {"id": "opt-2", "text": "A closed hypersphere centered at the origin.", "is_correct": False},
                    {"id": "opt-3", "text": "A non-linear parabolic manifold.", "is_correct": False},
                    {"id": "opt-4", "text": "A 1-dimensional discrete scalar point.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "In R^d, a linear equation w^T x + b = 0 defines a flat (d-1)-dimensional hyperplane that divides the feature space into two half-spaces corresponding to the predicted classes."
            },
            {
                "id": "q-cml-l01-16",
                "type": "multiple_choice",
                "difficulty": "medium",
                "subtopic": "Learning Paradigms",
                "question": "Which of the following problem statements fall into the UNSUPERVISED learning paradigm? (Select all that apply)",
                "options": [
                    {"id": "opt-1", "text": "Compressing 100 gene expression features into 5 principal components using PCA.", "is_correct": True},
                    {"id": "opt-2", "text": "Predicting whether a credit applicant will default using historical loan repayment labels.", "is_correct": False},
                    {"id": "opt-3", "text": "Clustering online news articles into emergent story clusters using text embeddings without tags.", "is_correct": True},
                    {"id": "opt-4", "text": "Detecting rare anomalies in server telemetry data using Gaussian density estimation.", "is_correct": True}
                ],
                "correctOptionIds": ["opt-1", "opt-3", "opt-4"],
                "explanation": "Options 1 (PCA dimensionality reduction), 3 (clustering articles), and 4 (density estimation for anomaly detection) operate purely on unannotated feature distributions X without ground-truth labels Y, making them unsupervised. Option 2 has explicit default labels and is supervised."
            },
            {
                "id": "q-cml-l01-17",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Loss Functions in Regression",
                "question": "Why is Mean Absolute Error (MAE) considered more robust to extreme dataset outliers than Mean Squared Error (MSE)?",
                "options": [
                    {"id": "opt-1", "text": "MAE squares the residual errors, diminishing the influence of large deviations.", "is_correct": False},
                    {"id": "opt-2", "text": "MSE penalizes residuals quadratically (e_i^2), disproportionately weighting extreme outliers, while MAE penalizes residuals linearly (|e_i|).", "is_correct": True},
                    {"id": "opt-3", "text": "MAE is differentiable at zero, allowing faster gradient descent convergence.", "is_correct": False},
                    {"id": "opt-4", "text": "MSE can only be computed on datasets with fewer than 100 observations.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "In MSE, squaring residuals (y - y_hat)^2 heavily inflates the penalty for large errors, pulling the fitted model toward extreme outliers. MAE applies a linear penalty |y - y_hat|, ensuring that outlier influence remains proportional to magnitude."
            },
            {
                "id": "q-cml-l01-18",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Decision Threshold Dynamics",
                "question": "A binary classification model for rare disease detection outputs posterior probability P(Disease = 1 | x). The clinical cost of a False Negative (missing a sick patient) is 50 times greater than a False Positive (subjecting a healthy person to a secondary blood test). How should the decision threshold tau be adjusted away from the default 0.50?",
                "options": [
                    {"id": "opt-1", "text": "Increase tau significantly (e.g., tau = 0.85) to ensure only highly certain disease cases are flagged.", "is_correct": False},
                    {"id": "opt-2", "text": "Decrease tau significantly (e.g., tau = 0.05) to maximize Recall and minimize fatal False Negatives.", "is_correct": True},
                    {"id": "opt-3", "text": "Leave tau strictly at 0.50 because mathematical probability axioms forbid shifting decision thresholds.", "is_correct": False},
                    {"id": "opt-4", "text": "Switch the task to an unsupervised K-Means clustering algorithm to eliminate thresholding.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "When False Negatives carry devastating asymmetric costs, the system must prioritize High Recall. Lowering the decision threshold tau (e.g., to 0.05 or 0.10) ensures that any patient with even a slight suspicion of disease is flagged for follow-up testing, minimizing missed cases."
            },
            {
                "id": "q-cml-l01-19",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "R-squared Mathematical Intuition",
                "question": "In a regression problem, an engineer calculates the Coefficient of Determination R^2 on an unseen test set and obtains R^2 = -0.42. What does a negative R^2 value mathematically signify?",
                "options": [
                    {"id": "opt-1", "text": "The model has achieved perfect correlation with inverted polarity.", "is_correct": False},
                    {"id": "opt-2", "text": "A negative R^2 is mathematically impossible because the metric is squared.", "is_correct": False},
                    {"id": "opt-3", "text": "The model's residual sum of squares is worse than simply predicting the mean of the training target (y_bar) for all test samples.", "is_correct": True},
                    {"id": "opt-4", "text": "The dataset contains negative eigenvalues in its covariance matrix.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-3"],
                "explanation": "R^2 = 1 - (SS_res / SS_tot). If the model's predictions have larger residual variance than the horizontal baseline predicting y_bar (SS_res > SS_tot), the ratio exceeds 1, resulting in a negative R^2. This indicates a severely flawed or heavily overfitted model."
            },
            {
                "id": "q-cml-l01-20",
                "type": "multiple_choice",
                "difficulty": "hard",
                "subtopic": "Mitchell Framework Nuances",
                "question": "Which of the following scenarios violate Tom Mitchell's requirement for a well-defined learning task? (Select all that apply)",
                "options": [
                    {"id": "opt-1", "text": "Evaluating performance measure P exclusively on the exact same dataset used for experience E.", "is_correct": True},
                    {"id": "opt-2", "text": "Failing to define an objective mathematical scoring metric P, relying solely on undefined human intuition.", "is_correct": True},
                    {"id": "opt-3", "text": "Using an experience dataset E where labels are continuous while task T requires assigning discrete categories.", "is_correct": False},
                    {"id": "opt-4", "text": "Declaring task T as 'making the company more innovative' without a concrete functional mapping from inputs to outputs.", "is_correct": True}
                ],
                "correctOptionIds": ["opt-1", "opt-2", "opt-4"],
                "explanation": "Option 1 violates Mitchell's intent because memorizing training data without generalization is not learning. Option 2 violates the requirement for an explicit performance measure P. Option 4 lacks an operational, well-specified task T. Option 3 is valid (e.g., thresholding continuous blood pressure labels into discrete hypertensive categories)."
            },
            {
                "id": "q-cml-l01-21",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Cross-Entropy vs 0-1 Loss",
                "question": "In training classification models via numerical optimization (gradient descent), why is Cross-Entropy / Log Loss utilized as the loss function instead of 0-1 Classification Loss (Accuracy)?",
                "options": [
                    {"id": "opt-1", "text": "0-1 Loss produces non-convex step functions with zero gradients almost everywhere, preventing gradient-based weight updates.", "is_correct": True},
                    {"id": "opt-2", "text": "0-1 Loss is non-deterministic and varies with random seed initialization.", "is_correct": False},
                    {"id": "opt-3", "text": "Cross-Entropy is bounded strictly between 0 and 1, whereas 0-1 Loss is unbounded.", "is_correct": False},
                    {"id": "opt-4", "text": "Scikit-learn documentation forbids the use of accuracy during training.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "0-1 loss assigns 0 for correct and 1 for incorrect predictions. Its derivative is zero wherever it is flat and undefined at the threshold boundary. This piecewise-constant step surface provides zero gradient signal for gradient descent. Cross-Entropy is smooth, convex, and differentiable, providing steep gradients when predictions are wrong."
            },
            {
                "id": "q-cml-l01-22",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Metric Selection in Imbalanced Classification",
                "question": "A fraud detection dataset has 99,900 legitimate transactions and 100 fraudulent transactions (0.1% fraud prevalence). A naive dummy classifier predicts 'Legitimate' for every single transaction. What are the Accuracy and Recall of this dummy classifier on the fraudulent class?",
                "options": [
                    {"id": "opt-1", "text": "Accuracy = 99.9%, Recall = 99.9%", "is_correct": False},
                    {"id": "opt-2", "text": "Accuracy = 99.9%, Recall = 0.0%", "is_correct": True},
                    {"id": "opt-3", "text": "Accuracy = 50.0%, Recall = 50.0%", "is_correct": False},
                    {"id": "opt-4", "text": "Accuracy = 0.1%, Recall = 0.0%", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Accuracy is (TP + TN) / Total = (0 + 99,900) / 100,000 = 99.9%. However, Recall on fraud is TP / (TP + FN) = 0 / (0 + 100) = 0.0%. This illustrates why raw accuracy is a fatally misleading metric for highly imbalanced classification problems."
            },
            {
                "id": "q-cml-l01-23",
                "type": "multiple_choice",
                "difficulty": "hard",
                "subtopic": "Statistical Foundations of ML",
                "question": "Which of the following statements correctly describe the statistical and probabilistic assumptions underpinning classical linear models? (Select all that apply)",
                "options": [
                    {"id": "opt-1", "text": "Ordinary Least Squares (OLS) regression minimizes the sum of squared residuals, which corresponds to Maximum Likelihood Estimation under the assumption of independent, identically distributed Gaussian noise.", "is_correct": True},
                    {"id": "opt-2", "text": "Linear regression models strictly require that input features X follow a normal distribution.", "is_correct": False},
                    {"id": "opt-3", "text": "The covariance matrix Sigma of feature matrix X is symmetric and positive semi-definite.", "is_correct": True},
                    {"id": "opt-4", "text": "Logistic regression models the log-odds (logit) of the positive class as a linear combination of input features.", "is_correct": True}
                ],
                "correctOptionIds": ["opt-1", "opt-3", "opt-4"],
                "explanation": "Option 1 is correct (Gauss-Markov & MLE). Option 2 is false: linear regression assumes the residual errors are Gaussian, not the input features X. Option 3 is true (covariances are symmetric, variances non-negative). Option 4 is the mathematical definition of logistic regression: ln(p / (1-p)) = w^T x + b."
            },
            {
                "id": "q-cml-l01-24",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Multi-label vs Multi-class",
                "question": "A diagnostic imaging system inspects chest X-rays. A single patient's X-ray can simultaneously exhibit 'Pneumonia', 'Cardiomegaly', and 'Pleural Effusion'. How is this problem mathematically structured?",
                "options": [
                    {"id": "opt-1", "text": "Multi-class Classification with Softmax activation.", "is_correct": False},
                    {"id": "opt-2", "text": "Multi-label Classification with independent binary sigmoid outputs per pathology.", "is_correct": True},
                    {"id": "opt-3", "text": "Unsupervised Gaussian Mixture Modeling.", "is_correct": False},
                    {"id": "opt-4", "text": "Univariate Poisson Regression.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "In Multi-class classification, classes are mutually exclusive (sum of probabilities = 1 via Softmax). When an instance can simultaneously possess multiple active labels, the problem is Multi-label classification, where each pathology is modeled as an independent binary classification target using Sigmoidal activations."
            },
            {
                "id": "q-cml-l01-25",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Reinforcement Learning Boundary",
                "question": "How does Reinforcement Learning fundamentally differ from both Supervised and Unsupervised Learning regarding its feedback signal and data collection?",
                "options": [
                    {"id": "opt-1", "text": "RL does not use any mathematical optimization functions.", "is_correct": False},
                    {"id": "opt-2", "text": "RL receives instantaneous ground-truth labels for every action from an oracle supervisor.", "is_correct": False},
                    {"id": "opt-3", "text": "RL learns from delayed evaluative scalar rewards through active trial-and-error interaction, where current actions influence future states and data distribution.", "is_correct": True},
                    {"id": "opt-4", "text": "RL operates strictly on static offline CSV tables without temporal sequencing.", "is_correct": False}
                ],
                "correctOptionIds": ["opt-3"],
                "explanation": "Unlike supervised learning (which receives prescriptive ground-truth targets y) and unsupervised learning (which finds static patterns in fixed X), Reinforcement Learning receives evaluative, often delayed scalar rewards. Crucially, the agent's actions alter the environment state, dynamically dictating future data experiences (closed-loop interaction)."
            }
        ]
    }
}
