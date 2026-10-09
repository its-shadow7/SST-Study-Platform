# Lecture 1: Introduction to Classical Machine Learning
## Student Notes — SST Classical Machine Learning

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Explain the fundamental paradigm shift from **Classical Rule-Based Software Engineering** to **Data-Driven Machine Learning**.
- Apply **Tom Mitchell’s formal definition of a learning problem** ($\text{Task } T, \text{Experience } E, \text{Performance Metric } P$) to mathematically frame any real-world engineering problem.
- Categorize machine learning paradigms rigorously into **Supervised**, **Unsupervised**, **Semi-Supervised**, and **Reinforcement Learning**.
- Differentiate between **Classification** (discrete target space) and **Regression** (continuous target space), understanding why predicting probabilities does not convert classification into arbitrary regression.
- Trace the **8-stage End-to-End Machine Learning Lifecycle**, specifically analyzing the critical failure modes in the two stages most beginners skip.
- Formulate the concept of **Generalization Error** and explain why minimizing empirical training error alone leads to catastrophic real-world failure.

---

## 1. The Paradigm Shift: Software 1.0 vs. Software 2.0

### Classical Programming (Rule-Based Engineering)
In traditional computer science (Software 1.0), human software engineers manually craft deterministic business logic. We design explicit rules, algorithms, conditional branches, and state machines that take structured inputs and yield outputs.

$$\text{Data} + \text{Handcrafted Rules} \longrightarrow \text{Output}$$

This paradigm excels when the underlying problem domain is well-understood, fully specifiable, and governed by strict mathematical or business axioms (e.g., calculating tax brackets, payroll processing, sorting arrays, compiling source code).

```
   Traditional Programming:
   ┌──────────┐
   │   Data   │──────┐
   └──────────┘      ▼
                 ┌───────────────┐        ┌──────────┐
                 │ Computer (CPU)│───────►│  Output  │
                 └───────────────┘        └──────────┘
   ┌──────────┐      ▲
   │  Rules   │──────┘
   └──────────┘
```

### Machine Learning (Data-Driven Induction)
In many real-world domains, formulating exhaustive deterministic rules is mathematically intractable or humanly impossible. Consider spam detection, predicting real estate valuations, identifying fraudulent credit card transactions, or facial recognition. A human cannot write a million `if/else` statements that reliably cover every syntactic permutation of an incoming phishing email.

Machine Learning flips the computational equation:

$$\text{Data} + \text{Observed Outputs (Labels)} \longrightarrow \text{Learned Rules (Model)}$$

```
   Machine Learning Paradigm:
   ┌──────────┐
   │   Data   │──────┐
   └──────────┘      ▼
                 ┌───────────────┐        ┌──────────────────┐
                 │ ML Algorithm  │───────►│ Learned Rules    │
                 └───────────────┘        │ (Trained Model)  │
   ┌──────────┐      ▲                    └──────────────────┘
   │  Output  │──────┘
   └──────────┘
```

### The Engineering Decision Matrix

| Dimension | Classical Programming | Machine Learning |
| :--- | :--- | :--- |
| **Origin of Rules** | Explicitly designed by human engineers | Statistically learned from observed data |
| **Data Requirement** | Often requires zero or minimal training data | Strictly dependent on statistical volume and quality |
| **Adaptability** | Requires manual code changes and redeployment | Retrain or fine-tune weights on fresh distribution data |
| **Determinism** | 100% deterministic (same input $\to$ same output) | Probabilistic / stochastic approximations |
| **Best Applied When** | Rules are unambiguous, clear, and stable | The underlying pattern is complex, noisy, or humanly unspecifiable |

> [!TIP]
> **Rule of Thumb for Systems Architects**: If you can write a short, deterministic, maintainable unit test or regex that cleanly solves your problem with $>99\%$ reliability, **never use Machine Learning**. Reach for ML only when the underlying mapping $f: \mathcal{X} \to \mathcal{Y}$ is fuzzy, non-linear, high-dimensional, and continuously evolving.

---

## 2. Tom Mitchell’s Formal Definition of Learning (E, T, P)

In his seminal 1997 textbook *Machine Learning*, computer scientist Tom Mitchell provided the foundational mathematical definition of an inductive learning agent:

> **Mitchell's Definition**:  
> A computer program is said to **learn** from experience $\mathbf{E}$ with respect to some class of tasks $\mathbf{T}$ and performance measure $\mathbf{P}$, if its performance at tasks in $\mathbf{T}$, as measured by $\mathbf{P}$, improves with experience $\mathbf{E}$.

$$\lim_{E \to \infty} P(T \mid E) > P(T \mid E_{\text{initial}})$$

Any vaguely defined ML initiative fails unless the engineering team explicitly formalizes all three components before writing a single line of training code.

```
   ┌──────────────────────────────────────────────────────────────┐
   │                    TOM MITCHELL'S TRIAD                      │
   ├──────────────────┬───────────────────────────────────────────┤
   │ Task (T)         │ The formal operational goal the system    │
   │                  │ executes (e.g. classify, rank, predict).   │
   ├──────────────────┼───────────────────────────────────────────┤
   │ Experience (E)   │ The empirical data / interactions fed to  │
   │                  │ the learning algorithm over time.         │
   ├──────────────────┼───────────────────────────────────────────┤
   │ Performance (P)  │ The quantitative metric evaluating the    │
   │                  │ quality of execution on unseen instances. │
   └──────────────────┴───────────────────────────────────────────┘
```

### Case Studies in Problem Formulation

#### 1. Automated Email Spam Classification
- **Task ($T$)**: Classify an incoming raw email message $x \in \mathcal{X}$ into one of two discrete classes: $y \in \{0, 1\}$ ($\text{Ham} = 0, \text{Spam} = 1$).
- **Experience ($E$)**: A historical dataset of $N$ emails labeled by users or security analysts: $\mathcal{D} = \{(x^{(i)}, y^{(i)})\}_{i=1}^N$.
- **Performance ($P$)**: $F_{\beta}$-Score or Precision on held-out test mailboxes (prioritizing Precision so legitimate emails are almost never sent to the Spam folder).

#### 2. Real Estate Price Prediction
- **Task ($T$)**: Estimate the continuous market clearing price $\hat{y} \in \mathbb{R}^+$ of a residential property given structural and geographical attributes $\mathbf{x} = [x_1, x_2, \dots, x_d]^T$.
- **Experience ($E$)**: Historical registry of executed transactions with verified sale prices over the past 24 months.
- **Performance ($P$)**: Root Mean Squared Error ($\text{RMSE}$) or Mean Absolute Percentage Error ($\text{MAPE}$) evaluated on recent, out-of-time transactions.

#### 3. Autonomous Lane Keeping
- **Task ($T$)**: Output a steering angle adjustment $\theta \in [-45^\circ, +45^\circ]$ at 60 Hz given camera sensor streams and LiDAR point clouds.
- **Experience ($E$)**: Telemetry logs of expert human driving across diverse road conditions and simulated trajectories.
- **Performance ($P$)**: Mean squared error relative to human driver trajectories, and rate of lane departure interventions per 1,000 km.

---

## 3. High-Level Taxonomy of Machine Learning

Machine Learning is a subset of the broader discipline of **Artificial Intelligence**. Within ML, we distinguish between **Classical (Statistical) Machine Learning** and **Deep Learning**:

```
   ┌────────────────────────────────────────────────────────┐
   │             ARTIFICIAL INTELLIGENCE (AI)               │
   │   ┌────────────────────────────────────────────────┐   │
   │   │            MACHINE LEARNING (ML)               │   │
   │   │   ┌───────────────────────┬────────────────┐   │   │
   │   │   │ Classical ML          │ Deep Learning  │   │   │
   │   │   │ (Linear, Trees, SVMs, │ (Multi-layer   │   │   │
   │   │   │  k-NN, Clustering)    │  Neural Nets)  │   │   │
   │   │   └───────────────────────┴────────────────┘   │   │
   │   └────────────────────────────────────────────────┘   │
   └────────────────────────────────────────────────────────┘
```

The four core learning paradigms are differentiated by the nature of the training signal and feedback mechanism:

```
                                  Machine Learning Paradigms
                                              │
         ┌───────────────────┬────────────────┴───────────────────┬────────────────────┐
         ▼                   ▼                                    ▼                    ▼
   Supervised           Unsupervised                       Semi-Supervised        Reinforcement
   Learning             Learning                              Learning               Learning
  (Labelled data:    (No target labels:                   (Small labeled set +     (Agent, Environment,
   x ↦ y)             discover geometry)                   massive unlabeled)       Reward signal)
         │                   │
   ┌─────┴─────┐       ┌─────┴─────┐
   ▼           ▼       ▼           ▼
Classif-    Regress- Cluster-   Dim.
ication      ion      ing     Reduction
```

### 1. Supervised Learning
The learning algorithm is provided with a training set of input-output pairs:

$$\mathcal{D} = \{(\mathbf{x}^{(i)}, y^{(i)})\}_{i=1}^N \quad \text{where } \mathbf{x}^{(i)} \in \mathbb{R}^d, \; y^{(i)} \in \mathcal{Y}$$

The objective is to learn a mapping function $f: \mathcal{X} \to \mathcal{Y}$ that minimizes a chosen loss function $\mathcal{L}(y, f(\mathbf{x}))$ on unseen test data.

### 2. Unsupervised Learning
The dataset contains only features without supervisory ground-truth annotations:

$$\mathcal{D} = \{\mathbf{x}^{(i)}\}_{i=1}^N$$

The goal is to infer the intrinsic probability distribution $p(\mathbf{x})$, discover low-dimensional latent manifolds, or partition data into coherent clusters:
- **Clustering**: Grouping customers with similar purchasing behavior (e.g., $K$-Means, DBSCAN).
- **Dimensionality Reduction**: Projecting a 1,000-dimensional genomics dataset onto 2 principal orthogonal axes while preserving maximum variance (e.g., PCA, t-SNE).
- **Density Estimation & Anomaly Detection**: Identifying fraudulent transactions as low-probability outliers under a learned distribution (e.g., Isolation Forests, Gaussian Mixture Models).

> [!WARNING]
> **Clustering $\ne$ Classification!**  
> Beginners frequently conflate clustering and classification. **Classification** predicts predefined, human-labeled categories for an unseen query. **Clustering** invents mathematical partitions based on geometric distance metrics in feature space; it has no awareness of human semantics or pre-existing business classes.

### 3. Semi-Supervised Learning
In many industry applications (e.g., medical pathology imagery, speech transcription), obtaining unlabeled data $\mathbf{x}$ is trivial, but acquiring ground-truth labels $y$ requires expensive human specialist labor. Semi-supervised algorithms leverage a small set of labeled points alongside a massive pool of unlabeled data by enforcing assumptions such as the **cluster assumption** (points in the same cluster share the same label) or the **smoothness assumption**.

### 4. Reinforcement Learning (RL)
An autonomous agent interacts sequentially with an external environment. Rather than being told the correct action at each step, the agent receives scalar reward signals $r_t \in \mathbb{R}$ and optimizes a policy $\pi(a \mid s)$ to maximize the expected cumulative discounted return:

$$G_t = \sum_{k=0}^{\infty} \gamma^k r_{t+k+1}, \quad \gamma \in [0, 1)$$

---

## 4. Supervised Learning: Classification vs. Regression

Within Supervised Learning, tasks are categorized by the mathematical topology of the target space $\mathcal{Y}$.

```
                 SUPERVISED LEARNING TARGET TOPOLOGY
       ┌───────────────────────────────┬───────────────────────────────┐
       │        CLASSIFICATION         │          REGRESSION           │
       ├───────────────────────────────┼───────────────────────────────┤
       │ Target: Discrete Set          │ Target: Continuous Metric     │
       │   y ∈ {0, 1} (Binary)         │   y ∈ ℝ                       │
       │   y ∈ {1, 2, ..., K} (Multi)  │   y ∈ [0, ∞)                  │
       ├───────────────────────────────┼───────────────────────────────┤
       │ Boundary: Decision Surfaces   │ Boundary: Regression Surface  │
       │ that partition feature space  │ fitting the conditional mean  │
       ├───────────────────────────────┼───────────────────────────────┤
       │ Metrics: Accuracy, F1, AUC,   │ Metrics: MSE, RMSE, MAE, R²,  │
       │ Precision, Recall, Log-Loss   │ MAPE, Huber Loss              │
       └───────────────────────────────┴───────────────────────────────┘
```

### The Probability Nuance
Consider a logistic regression model outputting $\hat{p} = \sigma(\mathbf{w}^T \mathbf{x}) = 0.84$. 
- Even though the numerical probability $\hat{p} \in [0, 1]$ is continuous, **the task remains classification**. 
- The probability represents the model's epistemic confidence in a Bernoulli trial ($P(y=1 \mid \mathbf{x})$). 
- Applying a threshold (e.g., $\tau = 0.5$) projects this probability back into the discrete category space $\{0, 1\}$.

---

## 5. The End-to-End Machine Learning Pipeline

Building production-grade machine learning systems involves a continuous feedback loop across 8 discrete engineering phases:

```
 ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
 │ 1. Problem      │──────►│ 2. Data Sourcing│──────►│ 3. Exploratory  │
 │    Framing      │       │    & Ingestion  │       │    Data Analysis│
 └─────────────────┘       └─────────────────┘       └─────────────────┘
                                                              │
                                                              ▼
 ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
 │ 6. Offline      │◄──────│ 5. Model        │◄──────│ 4. Preprocessing│
 │    Evaluation   │       │    Training     │       │    & Features   │
 └─────────────────┘       └─────────────────┘       └─────────────────┘
         │
         ▼
 ┌─────────────────┐       ┌─────────────────┐
 │ 7. Serving &    │──────►│ 8. Continuous   │
 │    Deployment   │       │    Monitoring   │
 └─────────────────┘       └─────────────────┘
```

1. **Problem Formulation**: Translating an ambiguous business need into a mathematically sound machine learning task ($T, E, P$). Defining acceptable trade-offs (e.g., latency budget $< 15\text{ms}$ vs. $1\%$ F1 improvement).
2. **Data Sourcing & Ingestion**: Extracting records from transactional databases (PostgreSQL), event streams (Kafka), or data lakes (S3/Parquet). Ensuring cryptographic data provenance.
3. **Exploratory Data Analysis (EDA)**: Profiling missingness, skewness, kurtosis, class imbalance, multi-collinearity, and feature distributions.
4. **Data Cleaning & Preprocessing**: Imputing missing entries, encoding categorical vectors, and scaling numerical continuous features strictly within a non-leaking pipeline.
5. **Model Training & Optimization**: Selecting algorithmic inductive biases (OLS, Ridge, Lasso, Logistic Regression, Trees, KNN), running hyperparameter tuning using cross-validation.
6. **Offline Validation & Error Analysis**: Evaluating performance against baselines on strictly separated test sets. Conducting stratified subgroup performance audits.
7. **Production Deployment**: Exposing inference endpoints via REST/gRPC microservices, batch inference pipelines, or embedded edge runtimes (ONNX).
8. **Monitoring & Drift Detection**: Tracking operational metrics (CPU, RAM, p99 latency) alongside statistical metrics (**Data Drift**, **Concept Drift**, and **Prediction Distribution Shift**).

---

## 6. The Two Boxes Beginners Skip

Ninety percent of ML tutorials start at **Step 5 (Model Training)** and end at **Step 6 (Evaluation)**. In production engineering, the greatest system failures occur in the two neglected bookends:

```
      ╔═════════════════════════════╗                ╔═════════════════════════════╗
      ║     BOX 1 (UPSTREAM)        ║                ║     BOX 2 (DOWNSTREAM)      ║
      ║  Precise Problem Framing    ║                ║  Monitoring & Concept Drift ║
      ║  & Cost-Matrix Alignment    ║   ═════════►   ║  Detection in Production    ║
      ╚═════════════════════════════╝                ╚═════════════════════════════╝
          Failure: Building the                          Failure: Model decays silently
          wrong model perfectly                          as world distributions change
```

### Box 1: Upstream Framing & Metric Misalignment
Engineers frequently jump into model fitting using default `accuracy` without analyzing the asymmetric costs of errors.
- **Example**: In cancer screening, a False Negative (telling a sick patient they are healthy) is catastrophic, whereas a False Positive (requiring a secondary confirmation biopsy) is merely inconvenient. A model with $99.2\%$ accuracy that achieves high score by guessing "healthy" for every edge case is lethal in production.
- **Remedy**: Construct a formal **Cost Matrix** weighting $\text{Cost}(FN) \gg \text{Cost}(FP)$ and optimize expected financial/clinical loss rather than raw mathematical accuracy.

### Box 2: Downstream Monitoring & Distribution Drift
A model is not a compiled C++ binary; its performance deteriorates over time because the real world is non-stationary:
1. **Covariate Shift (Data Drift)**: $P(\mathbf{x})$ changes while $P(y \mid \mathbf{x})$ remains static. (e.g., camera sensors degrade, or an e-commerce platform attracts a younger demographic whose browsing features look completely different).
2. **Concept Drift**: $P(y \mid \mathbf{x})$ changes while $P(\mathbf{x})$ appears unchanged. (e.g., during inflation or macroeconomic shifts, a customer with historical salary $\mathbf{x}$ who previously qualified for a loan default now defaults).

---

## 7. The Core Objective: Generalization vs. Memorization

The fundamental mathematical paradox of machine learning is:
> We train a model by minimizing error on historical data $\mathcal{D}_{\text{train}}$, but we do not care how well the model performs on $\mathcal{D}_{\text{train}}$. We only care how well it generalizes to unseen future data $\mathcal{D}_{\text{test}} \sim \mathcal{P}(\mathcal{X}, \mathcal{Y})$.

### Empirical Risk vs. True Risk
Let $\mathcal{L}(y, f(\mathbf{x}))$ denote the loss incurred when predicting $f(\mathbf{x})$ while the true value is $y$.
- **Empirical Risk (Training Loss)**:

  $$R_{\text{emp}}(f) = \frac{1}{N} \sum_{i=1}^N \mathcal{L}\left(y^{(i)}, f(\mathbf{x}^{(i)})\right)$$

- **True Risk (Expected Generalization Loss)**:

  $$R(f) = \mathbb{E}_{(\mathbf{x}, y) \sim \mathcal{P}}\left[\mathcal{L}(y, f(\mathbf{x}))\right] = \int_{\mathcal{X} \times \mathcal{Y}} \mathcal{L}(y, f(\mathbf{x})) \, d\mathcal{P}(\mathbf{x}, y)$$

Since the joint distribution $\mathcal{P}(\mathbf{x}, y)$ is unknown, we cannot compute $R(f)$ directly. A model with infinite capacity (such as a lookup table or a 50-degree polynomial) can achieve $R_{\text{emp}}(f) = 0$ by simply memorizing every point in $\mathcal{D}_{\text{train}}$, yet suffer catastrophic error $R(f) \to \infty$.

```
   Error
     ▲
     │       \                                 /  Test Error: R(f)
     │        \      Generalization Gap       /   (Expected Out-of-Sample Risk)
     │         \     ┌─────────────────┐     /
     │          \    │                 │    /
     │           \───▼─────────────────▼───/ ◄── Sweet Spot (Optimal Complexity)
     │            \                       /
     │             \─────────────────────/
     │              \                   /
     │               \                 /
     │────────────────\───────────────/──────── Train Error: R_emp(f)
     │                 \             /
     │                  \           /
     └───────────────────▼─────────▼────────────────────────► Model Complexity
                        Underfitting         Overfitting
                        (High Bias)         (High Variance)
```

---

## 8. Clean Scikit-Learn Pipeline Implementation

The following complete Python script establishes the standard, production-grade template for building a supervised classical machine learning model.

```python
"""
Classical Machine Learning: End-to-End Baseline Template
Demonstrates proper train/test split, column transformations, and pipeline encapsulation.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 1. Ingestion: Load raw data
raw_data = fetch_california_housing(as_frame=True)
df = raw_data.frame

# Feature Matrix (X) and Continuous Target Vector (y)
X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]

# 2. Strict Train-Test Hygiene: Split BEFORE any data transformation!
# Test size = 20%, fixed random_state ensures deterministic reproducibility.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# 3. Preprocessing Definition
numeric_features = X.columns.tolist()
preprocessor = ColumnTransformer(
    transformers=[
        ("num_scaler", StandardScaler(), numeric_features)
    ],
    remainder="passthrough"
)

# 4. Pipeline Encapsulation: Prevents preprocessing data leakage
full_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

# 5. Model Fitting: Fit parameters solely on Training partition
full_pipeline.fit(X_train, y_train)

# 6. Evaluation: Predict on unseen Test partition
y_pred_train = full_pipeline.predict(X_train)
y_pred_test = full_pipeline.predict(X_test)

# 7. Compute Formal Performance Metrics (P)
train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
test_r2 = r2_score(y_test, y_pred_test)

print("=" * 50)
print(f"Train RMSE: {train_rmse:.4f}")
print(f"Test RMSE:  {test_rmse:.4f}")
print(f"Test R²:    {test_r2:.4f}")
print("=" * 50)
```

---

## 9. Common Pitfalls & Interview-Grade Questions

### Q1: An intern states: "My logistic regression model outputs probabilities between 0 and 1, so it is actually performing regression, not classification." How do you evaluate this statement?
**Answer**:  
The statement is technically incorrect. The fundamental distinction between regression and classification is the topological nature of the label space $\mathcal{Y}$, not the mathematical form of the intermediate activation. In binary classification, ground truth is discrete: $\mathcal{Y} = \{0, 1\}$. Logistic regression models the parameter of a Bernoulli distribution $P(Y=1 \mid \mathbf{x}) = \pi(\mathbf{x})$. While $\pi(\mathbf{x}) \in [0, 1]$ is continuous, the operational task is deciding class membership by applying a threshold $\tau \in (0, 1)$. True regression models predict unbounded continuous properties (e.g., price, temperature, velocity).

### Q2: You are designing a machine learning system to route customer support tickets to one of 10 specialized engineering teams. Your colleague suggests using K-Means clustering. Is this a sound design?
**Answer**:  
No. K-Means is an unsupervised clustering algorithm that groups instances based on geometric proximity in feature space. It creates cluster identifiers (Cluster 0, Cluster 1, etc.) that have no inherent semantic correspondence to your 10 actual engineering teams. What the organization requires is **Supervised Multi-Class Classification**, trained on historical tickets that were manually resolved and tagged with the ground-truth destination team.

### Q3: Why is achieving 0% training error on a complex real-world dataset almost always a critical red flag in production engineering?
**Answer**:  
Real-world datasets contain aleatoric noise (irreducible error $\sigma^2$ caused by unmeasured variables, label noise, or measurement imprecision). A model that achieves $0\%$ training error has exhausted its parametric capacity memorizing noise, outliers, and idiosyncratic artifacts in $\mathcal{D}_{\text{train}}$. This constitutes severe **overfitting** (high variance), guaranteeing that when exposed to unseen test data from the true distribution, its prediction error will explode.

---

## 10. Summary & Key Takeaways

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                     SESSION 1 KEY TAKEAWAYS                            │
   ├────────────────────────────────────────────────────────────────────────┤
   │ 1. Classical Code vs. ML: Classical programming hardcodes human rules; │
   │    ML induces rules statistically from historical data mappings.       │
   │ 2. Mitchell's Triad (E, T, P): A problem is well-defined only when the │
   │    Task (T), Experience (E), and Performance Metric (P) are explicit.  │
   │ 3. Supervised vs. Unsupervised: Supervised learns x ↦ y mappings;     │
   │    Unsupervised discovers intrinsic structure in x without labels.     │
   │ 4. Classification vs. Regression: Split by target topology (discrete   │
   │    classes vs. continuous manifold), not feature types or probabilities│
   │ 5. Upstream & Downstream Traps: Pay extreme attention to business cost │
   │    matrices (Box 1) and continuous production drift monitoring (Box 2).│
   │ 6. Generalization is the Goal: Empirical training error is merely an   │
   │    optimization proxy; minimizing out-of-sample risk is the real goal. │
   └────────────────────────────────────────────────────────────────────────┘
```
