# 1. Introduction to Classical Machine Learning, Paradigms & Problem Formulation
**Term:** Term 5 | **Subject:** CML | **Note ID:** `cml-t5-l01`
**Last Updated:** 2026-10-18T00:00:00Z

## Abstract & Summary
An intuitive yet rigorous first-principles introduction to Classical Machine Learning. Covers the core DSML foundation (NumPy, Pandas, visualization taxonomy), the fundamental paradigm shift from rule-based software engineering (SDE) to statistical learning (MLE), Tom Mitchell's formal ETP framework for well-defined problems, the mathematical boundary separating classification from regression, and the operational contrast between supervised prediction and unsupervised structure discovery.

## Learning Objectives
- Understand why and when to transition from rule-based classical software engineering to machine learning.
- Formulate any machine learning problem using Tom Mitchell's Task-Experience-Performance (T-E-P) framework.
- Select the right exploratory data visualization tool (Histogram, Scatter, Bar, Line) based on data types and analytical questions.
- Differentiate classification and regression tasks based on the mathematical nature of the target variable.
- Distinguish supervised learning from unsupervised structure discovery (clustering) and know when to apply each.

## Key Takeaways
- Classical programming maps Inputs + Handcrafted Rules -> Outputs, whereas Machine Learning maps Inputs + Examples -> Learned Mapping.
- If a problem can be solved reliably with 10–20 deterministic if/else rules, stick to classical software engineering; use ML when the pattern is too complex, perceptual, or noisy to hand-code.
- Every well-defined ML project must explicitly anchor Tom Mitchell's triplet: Task T (what to do), Experience E (training data), and Performance P (how success is scored).
- Classification predicts discrete categories (even if outputting probabilities); Regression predicts continuous numbers. The boundary is governed strictly by the target space Y, not the input features X.
- Supervised learning learns a mapping X -> Y using ground-truth targets; Unsupervised learning discovers emergent geometry/clusters in X without targets.
- Histograms bin continuous values to show distribution shape and modality (unimodal vs. bimodal); scatter plots inspect bivariate relationships; bar charts compare discrete categories.

---

## 1. The DSML Base Layer: Exploratory Data Visualization & Mathematical Foundations
### 1.1 Why We Need a Solid Base Layer

Before an algorithm can learn from data, we must first be able to **see**, **manipulate**, and **model** that data. In modern data science and classical machine learning, we rely on a shared ecosystem of tools:

| Area | Industry Tools | Core Purpose in Machine Learning |
| :--- | :--- | :--- |
| **Numerics & Arrays** | **NumPy** | High-performance vector/matrix math, broadcasting, and linear algebra operations. |
| **Data Tables** | **Pandas** | Tabular data wrangling, cleaning, missing value handling, joins, and aggregations. |
| **Visual Diagnostics** | **Matplotlib & Seaborn** | Inspecting empirical distributions, relationships, correlations, and anomalies. |
| **Probability & Statistics** | Statistical primitives | Quantifying uncertainty, expected value, variance, and confidence intervals. |
| **Linear Algebra** | Vectors & Matrices | Geometric coordinate space for features, decision boundaries, and loss surfaces. |

---

### 1.2 The Data Visualization Cheat Sheet: Choosing the Right Chart

One of the most frequent beginner mistakes is picking the wrong chart for the question being asked. Visualizations are diagnostic tools. Choosing the wrong plot can completely obscure data patterns or lead to false conclusions.

```
Visual Diagnostic Flowchart:
   What do you want to explore?
     │
     ├── Continuous Variable Distribution / Shape ───────► HISTOGRAM (or KDE)
     ├── Discrete Category Frequencies / Totals ──────────► BAR PLOT
     ├── Association Between Two Continuous Variables ───► SCATTER PLOT
     └── Progression Over Time / Ordered Index ──────────► LINE PLOT
```

#### Detailed Diagnostic Matrix

| Analytical Objective | Recommended Chart | Why It Works | What Happens If You Use the Wrong Chart |
| :--- | :--- | :--- | :--- |
| **Shape & Modality of a Single Continuous Variable** | **Histogram** (or KDE) | Partitions values into contiguous numeric bins and displays frequency counts. Instantly reveals skewness, outliers, and whether data is unimodal (one peak) or bimodal (two separate clusters). | A **scatter plot** cannot aggregate density along a single axis; a **bar plot** treats every distinct floating-point number as an isolated category, creating an unreadable mess. |
| **Comparing Discrete Categories** | **Bar Plot** | Displays discrete category names on one axis and aggregate values (counts, sums, averages) on the other. | A **histogram** fails because categories have no natural continuous bin boundaries. |
| **Relationship Between Two Continuous Variables** | **Scatter Plot** | Maps each observation $(x_i, y_i)$ as a point in a 2D Cartesian plane. Reveals linear, non-linear, or clustering associations. | A **line plot** artificially connects points with lines, falsely implying sequential order or time continuity. |
| **Trend Over an Ordered Axis (Time, Steps)** | **Line Plot** | Connects sequential observations chronologically to display trajectories, trends, seasonality, and cycles. | A **scatter plot** shows points but makes it hard for the human eye to track chronological direction. |

> **The Exam Scores Scenario (Class Intuition)**:
> Imagine you are given the exam scores of 200 students. You need to answer: *"Are most students clustered around 70 marks, or is the class split into two distinct groups—struggling students at 45 and top performers at 90 (bimodal)?"*
> 
> - A **Histogram** answers this immediately: by grouping continuous marks into bins (e.g., 40-50, 50-60, 60-70), two separate peaks will visually jump out.
> - A simple **mean** or **median** would completely hide this reality by averaging out to ~68, giving the false illusion of a single average class!

---

### 1.3 Intuition of Vectors, Matrices, and Uncertainty

In classical machine learning:
1. **Each row** of your table is an observation: a vector $\mathbf{x} = [x_1, x_2, \dots, x_d]^T$ representing a point in $d$-dimensional feature space.
2. **Each column** is a feature: a geometric dimension (e.g., square footage, age, income).
3. **Dot products** measure geometric alignment and similarity: $\mathbf{w}^T \mathbf{x} = \sum_{j=1}^d w_j x_j$. When a linear model computes a score, it is projecting the feature vector onto a weight vector.
4. **Probability** is the mathematical language of uncertainty: since empirical data contains noise, our predictions represent conditional expectations $\mathbb{E}[Y \mid X]$ or posterior probabilities $P(Y=k \mid X)$ rather than absolute certainties.

**Citations & References:**
- Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley.
- Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer, Chapter 1.
- Strang, G. (2016). Introduction to Linear Algebra (5th ed.). Wellesley-Cambridge Press.

---

## 2. The Paradigm Shift: Classical Software Engineering (SDE) vs. Machine Learning (MLE)
### 2.1 Where Does the Logic Come From?

The defining difference between classical software engineering and machine learning is **who writes the rules**:

```
Classical Software Engineering (SDE):
   [ Data / Inputs ] ─────────┐
                              ├───► [ Handcrafted Rules / if-else Logic ] ───► [ Outputs / Decisions ]
   [ Human-Written Rules ] ───┘

Machine Learning Engineering (MLE):
   [ Data / Inputs ] ─────────┐
                              ├───► [ Learning Algorithm / Optimizer ] ──────► [ Learned Rules / Model ]
   [ Answers / Ground Truth ] ┘                                                       │
                                                                                      ▼
   [ New Unseen Data ] ────────────────────────────────────────────────────────► [ Predictions ]
```

#### Classical Software Engineering (Deductive Approach)
- **How it works**: A human engineer studies the requirements, figures out the logical steps, and writes explicit deterministic rules using `if`, `else`, `for`, and `switch` statements.
- **When it shines**: When business logic is clear, deterministic, and static (e.g., calculating tax slabs, authenticating passwords, processing database transactions).
- **Where it breaks**: When the problem involves perceptual complexity (recognizing faces, speech, handwritten text) or high-dimensional fuzzy patterns.

#### Machine Learning (Inductive Approach)
- **How it works**: Instead of hand-coding every condition, the engineer provides a generic model family (e.g., linear regression, decision tree) and an optimization criterion (loss function). The computer analyzes hundreds or thousands of labeled historical examples and autonomously tunes its parameters to find the best mapping rules.
- **When it shines**: When humans can easily recognize the pattern or provide examples, but cannot cleanly express the underlying mathematical rules in code.

---

### 2.2 The Spam Filter Intuition: Why Rules Collapse

Consider building an email spam filter:

```
Attempting Classical SDE:
   if "Viagra" in email_body: return SPAM
   if "Free Cash" in email_body: return SPAM
   if "Click Here Immediately" in email_body: return SPAM
```

What happens next?
1. Spammers immediately adapt: they send `V!agra`, `V-i-a-g-r-a`, `Free_Ca$h`, or embed text inside an image.
2. The engineer adds 50 more rules. Then 500 more rules.
3. Soon, valid emails get accidentally blocked (false positives), the rule base becomes an unmaintainable tangled mess of exceptions, and the system collapses under **combinatorial explosion**.

**The Machine Learning Solution**:
Feed 50,000 labeled emails (spam vs. legitimate) into a statistical learning algorithm. The algorithm automatically learns the predictive weights of thousands of word combinations simultaneously. When spammers mutate their tactics, the engineer does not rewrite code; they simply **retrain the pipeline on fresh labeled data**.

---

### 2.3 Comprehensive Comparison Matrix

| Architectural Dimension | Classical Software Engineering (SDE) | Machine Learning Engineering (MLE) |
| :--- | :--- | :--- |
| **Origin of Logic** | Human engineer explicitly writes every logical branch. | Optimization algorithm learns weights from historical data. |
| **Data Requirement** | Minimal; small unit test suites verify functionality. | High; performance scales with sample size and feature quality. |
| **Adaptation to Change (Concept Drift)** | Requires code changes, developer refactoring, and code redeployment. | Retrain the existing pipeline on newly collected empirical data. |
| **Verification & Testing** | Deterministic unit tests, assertions, and edge-case coverage. | Statistical validation: train/test split, cross-validation, precision/recall. |
| **Primary Failure Modes** | Syntax errors, logic bugs, unhandled null pointers. | Overfitting, underfitting, data leakage, distribution drift. |

---

### 2.4 Practical Rule of Thumb: When Should You Use ML?

Never use machine learning when a simple, deterministic rule suffices!

$$\text{Engineering Choice} = \begin{cases} \text{Classical SDE Code} & \text{if rules are } \le 20 \text{ branches and business domain is static} \\ \text{Lookup Table / Heuristic} & \text{if 100\% exactness is mandatory and zero statistical error is allowed} \\ \text{Machine Learning} & \text{if inputs are complex, patterns fuzzy, and labeled data is available} \end{cases}$$

> **Core Takeaway**: If you can write a clean, short `if/else` block that solves the problem reliably, write classical code. Reach for Machine Learning when the mapping function is too complex to write by hand.

**Citations & References:**
- Mitchell, T. M. (1997). Machine Learning. McGraw-Hill Education, Chapter 1.
- Domingos, P. (2012). A few useful things to know about machine learning. Communications of the ACM, 55(10), 78-87.

---

## 3. Tom Mitchell's Framework: Formulating Well-Defined Learning Problems (ETP)
### 3.1 Turning Vague Ambition into an Engineering Specification

Saying *"I want to build an AI for my company"* is a vague aspiration, not an engineering problem. In 1997, computer scientist **Tom Mitchell** provided the foundational mathematical definition that anchors all machine learning:

> **Tom Mitchell's Definition of Learning**:
> *"A computer program is said to learn from **Experience $E$** with respect to some class of **Tasks $T$** and **Performance Measure $P$**, if its performance at tasks in $T$, as measured by $P$, improves with experience $E$."*

Whenever you design an ML project, you must explicitly define these three letters before writing a single line of code:

```
Tom Mitchell's ETP Triplet:
   ┌──────────────────────────────────────────────────────────────┐
   │  T (Task)        ──► What specific operational action?       │
   │  E (Experience)  ──► What historical data / observations?    │
   │  P (Performance) ──► How do we quantitatively score success? │
   └──────────────────────────────────────────────────────────────┘
```

---

### 3.2 Breaking Down the Triplet: T, E, and P

1. **Task ($T$)**: The operational assignment the machine is executing. This is **not** the learning process itself; it is the production task the model performs on new data (e.g., classify an email, predict house price, detect credit card fraud).
2. **Experience ($E$)**: The empirical data or interaction history the system consumes to learn. Without experience, there is no learning (e.g., historical emails with user flags, past real estate transaction logs, sensor telemetry).
3. **Performance Measure ($P$)**: The quantitative metric used to judge whether the system is doing well or poorly. It must align with the real-world business objective (e.g., accuracy, precision, Root Mean Squared Error).

---

### 3.3 Concrete Industry Examples of ETP

#### Example 1: Email Spam Classifier
- **Task ($T$)**: Classify an incoming email as either `Spam` or `Not Spam`.
- **Experience ($E$)**: A dataset of 100,000 historical emails along with human-assigned labels.
- **Performance Measure ($P$)**: Classification F1-score or precision/recall on a separate held-out test mailbox.

#### Example 2: Real Estate Price Appraisal
- **Task ($T$)**: Predict the market selling price (in rupees/dollars) of a house given its features.
- **Experience ($E$)**: Historical sales records containing square footage, number of bedrooms, locality, and final sale prices.
- **Performance Measure ($P$)**: Root Mean Squared Error (RMSE) or Mean Absolute Error (MAE) on unseen house sales.

#### Example 3: Autonomous Vehicle Emergency Braking
- **Task ($T$)**: Decide whether to trigger the emergency brake system within 50 milliseconds.
- **Experience ($E$)**: Telemetry data from LiDAR, radar, front-facing cameras, and recorded driver interventions.
- **Performance Measure ($P$)**: Collision avoidance rate and false alarm rate on road-simulation test courses.

#### Example 4: Movie Recommendation Engine
- **Task ($T$)**: Recommend a list of top 5 movies a user is most likely to watch next.
- **Experience ($E$)**: Historical user viewing histories, ratings, and click-through logs.
- **Performance Measure ($P$)**: Mean Reciprocal Rank (MRR) or Click-Through Rate (CTR) on held-out user sessions.

> **Discussion Question**:
> If a system is trained on 10,000 examples and achieves 80% accuracy, but when trained on 100,000 examples its accuracy remains stuck at 80%, is it improving with experience $E$?
> Mathematically, if $P$ fails to increase as $E$ expands, the model has saturated its hypothesis capacity (underfitting) or reached the irreducible noise limit of the data.

**Citations & References:**
- Mitchell, T. M. (1997). Machine Learning. McGraw-Hill Education, Section 1.2.
- Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.). Pearson.

---

## 4. Task Taxonomy: The Fundamental Divide Between Classification and Regression
### 4.1 The Golden Rule: The Target Space Governs the Task

Once your problem is well-defined, the very first architectural question is: **What kind of target are we predicting?**

The distinction between Classification and Regression is governed **strictly by the mathematical nature of the target variable $Y$ (the output)**. It has **nothing** to do with whether the input features $X$ are continuous, discrete, or categorical!

```
Target Output Type:
   ┌──────────────────────────────────────────────────────────────┐
   │  Target Y is Discrete (Categories / Classes)  ──► CLASSIFICATION │
   │  Target Y is Continuous (Real Numbers in ℝ)  ──► REGRESSION     │
   └──────────────────────────────────────────────────────────────┘
```

---

### 4.2 Classification: Predicting Discrete Categories

In classification, the goal is to assign each input sample $\mathbf{x}$ to one of several mutually exclusive or non-mutually exclusive categories:

$$y \in \{C_1, C_2, \dots, C_K\}$$

- **Binary Classification**: Exactly two classes (e.g., `Spam` vs. `Ham`, `Fraud` vs. `Legitimate`, `Churn` vs. `Retain`).
- **Multi-Class Classification**: More than two mutually exclusive classes; each sample belongs to exactly one class (e.g., recognizing handwritten digits `0` through `9`, classifying blood types `A`, `B`, `AB`, `O`).
- **Multi-Label Classification**: Each sample can simultaneously belong to multiple classes (e.g., tagging a news article with both `Finance` and `Technology`, or a chest X-ray exhibiting both `Pneumonia` and `Cardiomegaly`).

#### The "Class Probabilities" Trap: Does Probability Make It Regression?
Beginners often ask: *"My Logistic Regression model outputs $0.85$ (85% probability of churn). Since $0.85$ is a continuous decimal number, isn't it doing regression?"*

> **No!**
> Calculating posterior probabilities $P(Y=1 \mid X)$ is merely **internal mathematical machinery** for quantifying confidence. The operational objective of the system is still to make a **discrete categorical decision**:
> 
> $$\hat{y} = \begin{cases} 1 & \text{if } P(Y=1 \mid X) \ge \tau \\ 0 & \text{if } P(Y=1 \mid X) < \tau \end{cases}$$
> 
> You cannot evaluate this system using Mean Squared Error or $R^2$; you evaluate it using Accuracy, Precision, Recall, and ROC-AUC.

---

### 4.3 Regression: Predicting Continuous Numeric Values

In regression, the target variable is a real continuous quantity:

$$y \in \mathbb{R}$$

- Examples: Predicting next month's electricity consumption in kilowatt-hours, house price in rupees, delivery time in minutes, or engine temperature in Celsius.
- The target has natural ordering and meaningful arithmetic differences: the difference between 50°C and 60°C represents the exact same physical magnitude as between 90°C and 100°C.

---

### 4.4 Comprehensive Comparison Table

| Attribute | Classification | Regression |
| :--- | :--- | :--- |
| **Target Variable ($Y$)** | **Discrete** categories / labels (nominal or ordinal). | **Continuous** real-valued scalar ($y \in \mathbb{R}$). |
| **Typical Model Output** | Predicted class label, or class probability distribution. | A single continuous numerical estimate $\hat{y}$. |
| **Standard Evaluation Metrics** | Accuracy, Precision, Recall, F1-Score, ROC-AUC, Log-Loss. | Mean Absolute Error (MAE), Mean Squared Error (MSE), RMSE, $R^2$. |
| **Input Feature Types** | Continuous, discrete, or mixed (text, numeric, categorical). | Continuous, discrete, or mixed (numerical, categorical). |
| **Example Business Questions** | *"Will this subscriber cancel their plan this month?"* | *"How many total rupees will this customer spend this year?"* |

> **Input vs. Output Clarification**:
> - Can a regression model have categorical inputs? **Yes!** For example, predicting house price ($y$, continuous) using `neighborhood` (discrete/categorical) and `bedrooms` (discrete integer).
> - Can a classification model have continuous inputs? **Yes!** For example, predicting heart disease diagnosis ($y$, discrete) using `blood_pressure` and `cholesterol` (continuous).

**Citations & References:**
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning. Springer, Chapter 2.
- James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). An Introduction to Statistical Learning. Springer.

---

## 5. Learning Paradigms: Supervised vs. Unsupervised Learning
### 5.1 The Core Distinction: Is There a Teacher?

Machine learning paradigms are classified primarily by **what kind of supervision or feedback signal** the algorithm receives during training:

```
Learning Paradigms:
   ├── SUPERVISED LEARNING   ──► Training data includes inputs X AND ground-truth targets Y (Learn X -> Y)
   ├── UNSUPERVISED LEARNING ──► Training data has ONLY inputs X (Discover emergent structure in X)
   ├── SEMI-SUPERVISED       ──► Massive unlabelled X with a small fraction of labeled (X, Y)
   └── REINFORCEMENT         ──► Active agent receives delayed scalar rewards via trial-and-error
```

---

### 5.2 Supervised Learning: Learning with a Teacher

In Supervised Learning, every single observation in the training dataset is paired with an explicit ground-truth answer:

$$\mathcal{D}_{\text{train}} = \{(\mathbf{x}_1, y_1), (\mathbf{x}_2, y_2), \dots, (\mathbf{x}_n, y_n)\}$$

The algorithm's job is to adjust its internal parameters so that its prediction $\hat{y} = f(\mathbf{x})$ matches the true target $y$ as closely as possible.
- **Both Classification and Regression belong to Supervised Learning.**
- Evaluation is straightforward: compare the model's predictions $\hat{y}$ against known true labels $y$ on holdout test data.

---

### 5.3 Unsupervised Learning: Discovering Hidden Structure

In Unsupervised Learning, there are **no target labels $y$**. The dataset consists solely of feature vectors:

$$\mathcal{D}_{\text{train}} = \{\mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_n\}$$

The algorithm receives no guidance on what the "correct" answer is. Instead, it inspects the geometric and statistical relationships among points in feature space to discover hidden structure:
1. **Clustering (e.g., K-Means, Hierarchical)**: Grouping similar data points together based on distance or density.
2. **Dimensionality Reduction (e.g., PCA, t-SNE)**: Compressing high-dimensional features into fewer dimensions while preserving variance or neighborhood structure.

---

### 5.4 The Crucial Distinction: Clustering vs. Classification

This is one of the most widely tested conceptual boundaries in machine learning interviews:

```
Clustering vs. Classification:
   [ Labeled Dataset (Pre-defined Classes) ] ──► CLASSIFICATION  ──► Predicts known labels (e.g., Cat / Dog)
   [ Unlabeled Dataset (No Prior Names) ]     ──► CLUSTERING      ──► Discovers emergent groups from geometry
```

| Dimension | Supervised Classification | Unsupervised Clustering |
| :--- | :--- | :--- |
| **Ground-Truth Labels** | **Required during training.** | **Completely absent.** |
| **Output Meaning** | Predicts pre-existing, human-defined category names. | Groups data by geometric proximity; human must interpret what each cluster represents. |
| **Evaluation** | Objective comparison against test labels (Accuracy, F1). | Internal geometric heuristics (Silhouette score) or qualitative domain inspection. |
| **Analogy** | Sorting mail into labeled mailboxes: `Billing`, `HR`, `Legal`. | Arranging pebbles on a table into piles by color and size without knowing their names. |

---

### 5.5 Four Real-World Benchmark Case Studies (From Class)

Let's walk through four classic scenarios discussed in class to see how to instantly determine the correct paradigm:

#### Case 1: The Property Dealer's Pricing Tool
- *Scenario*: A real estate broker has historical records containing property size, number of bedrooms, locality, and recorded past sale prices. A new client asks what price a 3-bedroom apartment should sell for.
- *Analysis*:
  - Are ground-truth targets available? **Yes** (past transaction prices).
  - Is the target discrete or continuous? **Continuous** (sale price in currency).
  - *Correct Paradigm*: **Supervised Regression**.

#### Case 2: Untagged Customer Feedback Reviews
- *Scenario*: A product manager receives 20,000 free-form customer feedback comments. No tags, categories, or labels have been created yet. The manager wants to discover the primary underlying themes (e.g., product defects, delivery delays, customer support).
- *Analysis*:
  - Are labels available? **No**. The system must inspect the vocabulary geometry and group similar reviews together autonomously.
  - *Correct Paradigm*: **Unsupervised Learning (Clustering / Topic Modeling)**.

#### Case 3: Stock Price Forecasting
- *Scenario*: An investment firm uses past stock price records, trading volume, and macroeconomic indicators to predict the exact closing price of a stock tomorrow.
- *Analysis*:
  - Are historical target values available? **Yes** (yesterday's and historical closing prices).
  - Is the target discrete or continuous? **Continuous** (numeric stock price).
  - *Correct Paradigm*: **Supervised Regression**.

#### Case 4: Human Resources Candidate Triage
- *Scenario*: An enterprise HR department has three pre-existing, well-defined candidate bands: `Direct Hire`, `Technical Interview`, and `Reject`. They have thousands of past resumes with their final HR decisions.
- *Analysis*:
  - The categories already exist and are clearly named (`Direct Hire`, `Interview`, `Reject`).
  - Labeled historical examples exist.
  - An unsupervised clustering algorithm would invent mathematical clusters based on resume length or font, which would **not** align with HR's business buckets!
  - *Correct Paradigm*: **Supervised Classification**.

**Citations & References:**
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning. Springer, Chapter 14.
- Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer, Section 1.1.

---

## 6. Hands-On Python Implementations & Visual Demonstrations
### 6.1 Executable Code Demonstrations

Below are three clean, self-contained Python examples demonstrating:
1. Classification with discrete labels.
2. Regression with a continuous line fit.
3. Unsupervised clustering with K-Means.

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Set random seed for reproducibility
rng = np.random.default_rng(42)

# =====================================================================
# 1. CLASSIFICATION TOY DEMO (Discrete Labels)
# =====================================================================
n_samples = 60
# Class 0: centered at (-1, -1)
X_class0 = rng.normal(loc=[-1.0, -1.0], scale=0.4, size=(n_samples, 2))
# Class 1: centered at (1, 1)
X_class1 = rng.normal(loc=[1.0, 1.0], scale=0.4, size=(n_samples, 2))

X_clf = np.vstack([X_class0, X_class1])
y_clf = np.array([0] * n_samples + [1] * n_samples)  # Discrete labels: 0 or 1

# =====================================================================
# 2. REGRESSION TOY DEMO (Continuous Numeric Target)
# =====================================================================
x_reg = np.linspace(-3, 3, 70)
# Underlying true relation: y = 2.0 * x + 0.5 + Gaussian noise
noise = rng.normal(loc=0.0, scale=0.6, size=x_reg.shape)
y_reg = 2.0 * x_reg + 0.5 + noise

# Closed-form Ordinary Least Squares slope and intercept
w1 = np.cov(x_reg, y_reg, bias=True)[0, 1] / np.var(x_reg)
w0 = y_reg.mean() - w1 * x_reg.mean()
y_pred_line = w0 + w1 * x_reg

# =====================================================================
# 3. UNSUPERVISED CLUSTERING TOY DEMO (K-Means without Labels)
# =====================================================================
# Generate 3 unlabelled spatial clusters
blob1 = rng.normal(loc=[-2.0, 0.0], scale=0.5, size=(50, 2))
blob2 = rng.normal(loc=[1.5, 2.0], scale=0.5, size=(50, 2))
blob3 = rng.normal(loc=[1.5, -2.0], scale=0.5, size=(50, 2))
X_unlabeled = np.vstack([blob1, blob2, blob3])

# Fit KMeans (Notice: fit() takes ONLY X, no target y!)
kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
cluster_assignments = kmeans.fit_predict(X_unlabeled)
centroids = kmeans.cluster_centers_

# =====================================================================
# VISUALIZATION
# =====================================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

# Plot 1: Classification
axes[0].scatter(X_clf[y_clf == 0, 0], X_clf[y_clf == 0, 1], color="royalblue", alpha=0.8, label="Class 0")
axes[0].scatter(X_clf[y_clf == 1, 0], X_clf[y_clf == 1, 1], color="crimson", alpha=0.8, label="Class 1")
axes[0].set_title("1. Classification (Discrete Targets)")
axes[0].set_xlabel("Feature x1")
axes[0].set_ylabel("Feature x2")
axes[0].legend()
axes[0].grid(True, linestyle="--", alpha=0.5)

# Plot 2: Regression
axes[1].scatter(x_reg, y_reg, color="darkorange", alpha=0.7, label="Observed (x, y)")
axes[1].plot(x_reg, y_pred_line, color="black", linewidth=2, label="Fitted Line (y_hat)")
axes[1].set_title("2. Regression (Continuous Target)")
axes[1].set_xlabel("Input Feature x")
axes[1].set_ylabel("Continuous Target y")
axes[1].legend()
axes[1].grid(True, linestyle="--", alpha=0.5)

# Plot 3: Unsupervised Clustering
scatter = axes[2].scatter(X_unlabeled[:, 0], X_unlabeled[:, 1], c=cluster_assignments, cmap="viridis", alpha=0.75)
axes[2].scatter(centroids[:, 0], centroids[:, 1], marker="X", s=150, color="red", label="Centroids")
axes[2].set_title("3. Unsupervised (K-Means Clustering)")
axes[2].set_xlabel("Feature x1")
axes[2].set_ylabel("Feature x2")
axes[2].legend()
axes[2].grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()

print("Summary Check:")
print(f"Classification Classes: {np.unique(y_clf)}")
print(f"Regression Fitted Formula: y_hat = {w1:.2f} * x + {w0:.2f}")
print(f"Discovered Cluster Sizes: {np.bincount(cluster_assignments)}")
```

---

### 6.2 Master Summary Table

| Concept | Defining Question | Core Mechanism | Key Example |
| :--- | :--- | :--- | :--- |
| **SDE vs. MLE** | *Who writes the rules?* | SDE = Human coders; MLE = Optimization algorithm learns from data. | Handcrafted regex rules vs. trained Spam Classifier. |
| **Tom Mitchell ETP** | *Is the problem well-defined?* | Quantifies Task $T$, Experience $E$, and Performance Measure $P$. | Predict house price ($T$) from sales data ($E$) measured by RMSE ($P$). |
| **Classification** | *Is the target categorical?* | Predicts discrete class memberships; evaluated via Accuracy/F1. | Patient has diabetes vs. healthy. |
| **Regression** | *Is the target continuous?* | Predicts a real-valued number $y \in \mathbb{R}$; evaluated via RMSE/MAE. | Predicting tomorrow's maximum temperature. |
| **Supervised Learning** | *Are ground-truth labels provided?* | Uses paired examples $(x_i, y_i)$ to learn mapping $x \mapsto y$. | Loan default prediction, property valuation. |
| **Unsupervised Learning** | *Is the system discovering structure?* | Learns from $x_i$ alone to identify geometric clusters or compressions. | Customer market basket segmentation, PCA compression. |

**Citations & References:**
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830.
- Harris, C. R. et al. (2020). Array programming with NumPy. Nature, 585, 357-362.

---
