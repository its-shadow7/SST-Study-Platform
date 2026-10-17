# 2. Data Preparation, Feature Preprocessing & Leakage Prevention Pipelines
**Term:** Term 5 | **Subject:** CML | **Note ID:** `cml-t5-l02`
**Last Updated:** 2026-10-16T00:00:00Z

## Abstract & Summary
An exhaustive, rigorous masterclass on machine learning data preparation. Covers the mathematical necessity of preprocessing, the insidious 'fake-good scores' phenomenon of data leakage, nominal vs. ordinal encoding mechanics, the Dummy Variable Trap, numerical scaling mathematics and gradient descent geometry, missingness mechanisms (MCAR, MAR, MNAR), and industrial pipeline architecture using Scikit-Learn's ColumnTransformer and Pipeline.

## Learning Objectives
- Diagnose and eliminate all forms of data leakage (preprocessing, target, temporal, and group leakage).
- Enforce strict train/test hygiene by partitioning data before computing any statistical parameters.
- Implement optimal categorical encoding strategies for nominal and ordinal feature spaces.
- Select and apply numerical scaling transformations (StandardScaler, MinMaxScaler, RobustScaler) based on feature geometry and algorithm sensitivity.
- Handle missing data via robust statistical imputation and missing indicator mechanisms.
- Construct modular, leakage-proof machine learning pipelines using Scikit-Learn ColumnTransformer and Pipeline.

## Key Takeaways
- Preprocessing bugs never manifest as syntax errors or runtime exceptions; they manifest as deceptively inflated 'fake-good' cross-validation scores that collapse in production.
- Any statistic learned from data (mean, standard deviation, median, category vocabulary, quantile bins) must be fitted on training data only and merely transformed on test data.
- Nominal features require One-Hot Encoding with handle_unknown='ignore' to prevent runtime crashes; ordinal features require ordered integer mappings preserving monotonic hierarchy.
- Treating nominal categories as arbitrary integers invents false Euclidean distances and invalidates linear and metric-based models.
- Distance-based algorithms (KNN, K-Means, SVM) and gradient-based optimizers require feature scaling; tree-based models are scale-invariant.
- Median imputation is strictly superior to mean imputation for skewed numeric features with heavy outlier tails.
- Scikit-Learn Pipelines lock preprocessing and modeling into a single atomic object, eliminating data leakage by architectural design.

---

## 1. The Data Preparation Imperative & The 'Fake-Good Scores' Trap
### 1.1 The Machine Learning Data Reality

Mathematical learning algorithms do not ingest raw enterprise data tables directly. Algorithms operate on numerical tensors $\mathbf{X} \in \mathbb{R}^{n \times d}$. Raw enterprise datasets, however, are inherently heterogeneous and imperfect:
1. **Unformatted Text & Categorical Attributes**: Strings like `"NEAR OCEAN"`, `"ISLAND"`, `"San Francisco"`, `"Medium"`.
2. **Missing Observations**: Null entries, NaNs, sentinel values (`-999`, `"N/A"`).
3. **Disparate Physical Scales**: A feature like `total_rooms` measured in thousands ($10^3$) juxtaposed with `median_income` measured in tens ($10^1$).
4. **Outliers & Heavy Tails**: Log-normal distributions with extreme values that destabilize gradient optimization.

Data preparation is the architectural bridge that converts raw, messy real-world tables into standardized numerical feature spaces.

```
Raw Real-World Table:
+---------+----------+-------------+---------------+--------------------+
| Income  | Bedrooms | Total Rooms | Ocean Prox    | Median House Value |
+---------+----------+-------------+---------------+--------------------+
| 8.32    | 129.0    | 880.0       | NEAR BAY      | 452600.0           |
| 3.87    | NaN      | 7099.0      | INLAND        | 358500.0           |
| 1.68    | 342.0    | 1467.0      | <1H OCEAN     | 104200.0           |
+---------+----------+-------------+---------------+--------------------+
                                |
                                v  Data Preprocessing Pipeline
+-----------------------------------------------------------------------+
|  1. Impute NaNs (Median / Mode)                                       |
|  2. Encode Categoricals (One-Hot / Ordinal)                           |
|  3. Scale Numerics (StandardScaler / RobustScaler)                    |
+-----------------------------------------------------------------------+
                                |
                                v
Pure Numerical Design Matrix X in R^(n x d) -> Ready for ML Model
```

---

### 1.2 The Hook: The "Fake-Good Scores" Phenomenon

In traditional software development, bugs reveal themselves through compiler errors, syntax crashes, or runtime stack traces. **In Machine Learning, preprocessing bugs do not look like code bugs. They look like suspiciously perfect scores.**

> **The Production Failure Pattern**:
> An engineer prepares a dataset, trains a model, and reports a stellar $98.5\%$ accuracy or a near-zero RMSE on the test set. The model is shipped to production. Within 48 hours, live production accuracy plummets to $61.2\%$. 
> 
> What happened? The model did not discover a brilliant predictive pattern. The engineer accidentally allowed test set information to **leak** into the training preprocessing steps, giving the model an illegal preview of the exam answers during study time.

---

### 1.3 The Fundamental Preprocessing Law

$$\mathbf{Rule}: \quad \text{Every statistical parameter } \theta \in \{\mu, \sigma, \text{median}, \text{min}, \text{max}, \text{vocabulary}\} \text{ must be estimated exclusively from } \mathbf{X}_{\text{train}}.$$

At inference time, the frozen transformation parameters learned from the training fold must be applied directly to the test fold (or live production requests). Under no circumstances should `.fit()` ever be executed on test data.

**Citations & References:**
- Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. (2012). Leakage in data mining: Formulation, detection, and avoidance. ACM Transactions on Knowledge Discovery from Data, 6(4), 1-21.
- Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (3rd ed.). O'Reilly Media, Chapter 2.

---

## 2. Taxonomy of Data Leakage & Train/Test Hygiene
### 2.1 Formal Definition of Data Leakage

**Data Leakage** occurs when information from outside the training dataset is used to create or tune the model. This leads to overly optimistic performance estimates during development and catastrophic generalization failure in production.

```
       +-------------------------------------------------------------+
       |                  The Train / Test Firewall                  |
       +-------------------------------------------------------------+
       |                                                             |
       |     [ TRAINING FOLD (80%) ]       |   [ TEST HOLDOUT (20%) ]|
       |     - Compute Mean (mu)           |   - DO NOT compute mu   |
       |     - Compute Std (sigma)         |   - Borrow mu_train     |
       |     - Compute Median Impute       |   - Borrow median_train |
       |     - Fit Encoders                |   - Borrow enc_train    |
       |                                   |                         |
       |     =====> FIT TRANSFORM =====>   |   =====> TRANSFORM ONLY |
       +-------------------------------------------------------------+
```

---

### 2.2 Complete Taxonomy of Data Leakage

| Leakage Category | Manifestation Mechanism | Concrete Example | Architectural Prevention |
| :--- | :--- | :--- | :--- |
| **Preprocessing Leakage** | Summary statistics calculated across full $X$ before partitioning. | Calling `StandardScaler().fit_transform(X)` on all 20,000 rows prior to `train_test_split`. | Execute `train_test_split` **first**. Fit transformers strictly on $X_{\text{train}}$. |
| **Target Leakage** | Feature contains information only available *after* the target occurs. | Predicting patient hospital readmission using a feature `"Discharge Summary Prepared"`. | Apply the Golden Prediction-Time Test: Drop proxy features created downstream of the label. |
| **Temporal / Lookahead Leakage** | Randomly shuffling time-dependent data, allowing past predictions to peek at future data. | Random split on stock price data where Monday's model is trained on Friday's closing prices. | Enforce chronological walk-forward splitting (`TimeSeriesSplit`). Never randomly shuffle temporal sequences. |
| **Group / Clustered Leakage** | Multiple observations from the same entity appear in both train and test splits. | Training on MRI scans where patient P101 has 3 scans in train and 2 scans in test. | Deploy `GroupKFold` or `GroupShuffleSplit` partitioned by entity ID (Patient, Device, User). |

---

### 2.3 The Golden Prediction-Time Test

Whenever evaluating whether a feature is safe to include in a model pipeline, apply this deterministic operational test:

> **The Prediction-Time Test**:
> *"At the exact microsecond this inference request executes on the production server, will this exact feature value already be recorded and genuinely accessible in the database?"*
> 
> If the answer is "No" (e.g., the feature is generated during or after the event occurs), the feature constitutes **Target Leakage** and must be deleted from the feature matrix.

---

### 2.4 Safe vs. Unsafe Operations Before Train/Test Split

```
SAFE Before Split:
[x] Dropping rows where the target y is NaN (target cleaning)
[x] Removing duplicate records
[x] Domain-driven fixed cuts: pd.cut(df['income'], bins=[-inf, 2.5, 4.5, inf])

UNSAFE Before Split (LEAKAGE):
[!] StandardScaler().fit(X) or fit_transform(X)
[!] SimpleImputer(strategy='median').fit(X)
[!] OneHotEncoder().fit(X) (leaks test-set category vocabulary)
[!] Quantile binning: pd.qcut(df['income'], q=4) (computes empirical quantiles from test data)
[!] Outlier filtering based on full-dataset mean +/- 3*sigma
```

#### Code Implementation: Strict Hygiene Protocol
```python
from sklearn.model_selection import train_test_split

# STEP 1: Clean target labels if missing (Safe before split)
df_clean = df.dropna(subset=["median_house_value"]).copy()

X = df_clean.drop(columns=["median_house_value"])
y = df_clean["median_house_value"]

# STEP 2: Partition IMMEDIATELY before computing any feature statistics
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=None
)
# Note: Use stratify=y for imbalanced classification tasks!
```

**Citations & References:**
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). Springer, Chapter 7.
- Kaufman, S. et al. (2012). Leakage in data mining: Formulation, detection, and avoidance.

---

## 3. Categorical Feature Encoding: Nominal vs. Ordinal Mechanics
### 3.1 Nominal vs. Ordinal Categorical Variables

Categorical variables represent qualitative states and must be mapped to numbers. However, applying the wrong mathematical representation creates catastrophic geometric distortions:

| Categorical Type | Intrinsic Ordering | Examples | Proper Encoding Method | Danger of Mis-encoding |
| :--- | :--- | :--- | :--- | :--- |
| **Nominal** | **None** (Categories are mutually disjoint with zero natural hierarchy). | `ocean_proximity` (`INLAND`, `NEAR OCEAN`, `ISLAND`), City, Blood Type, Color. | **One-Hot Encoding** (`OneHotEncoder`). | Arbitrary integer encoding (0, 1, 2) invents fake distances: assumes `ISLAND` (2) is twice as large as `NEAR OCEAN` (1). |
| **Ordinal** | **Strict Natural Order** (Magnitude hierarchy exists, though spacing may be unequal). | `shirt_size` (`S < M < L < XL`), `income_band` (`low < mid < high`), Education Level. | **Ordinal Encoding** (`OrdinalEncoder`) with explicit category ordering. | One-hot encoding discards valuable monotonic ranking information. |

```
The Geometric Distortion of Arbitrary Label Encoding on Nominal Features:
If we assign: Red = 0, Green = 1, Blue = 2:
   Euclidean Distance(Red, Green) = |0 - 1| = 1
   Euclidean Distance(Red, Blue)  = |0 - 2| = 2
The linear model assumes Blue is mathematically twice as "far" from Red as Green is!
This geometric bias distorts Linear Models, Ridge/Lasso, KNN, and Neural Networks.
```

---

### 3.2 One-Hot Encoding & The Dummy Variable Trap

One-Hot Encoding maps a nominal categorical feature with $K$ unique levels into $K$ binary indicator columns:

$$x_i = \text{"NEAR BAY"} \implies \begin{bmatrix} x_{\text{INLAND}} \\ x_{\text{ISLAND}} \\ x_{\text{NEAR BAY}} \\ x_{\text{NEAR OCEAN}} \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 1 \\ 0 \end{bmatrix}$$

#### The Dummy Variable Trap (Multicollinearity)
In an unregularized Ordinary Least Squares (OLS) linear regression model with an intercept term $\beta_0$, retaining all $K$ binary columns introduces **perfect multicollinearity**:
$$\sum_{k=1}^K x_{\text{dummy}, k} = 1.0 = \mathbf{1}$$
The design matrix $\mathbf{X}$ is not full column rank, rendering $\mathbf{X}^T \mathbf{X}$ non-invertible.
- **The Classical Solution**: Drop one category (`drop='first'`), resulting in $K-1$ degrees of freedom. The dropped category becomes the baseline reference.
- **The Modern ML Rule**: In regularized linear models (Ridge, Lasso, ElasticNet) and tree ensembles (Random Forest, XGBoost), **keep all $K$ columns** (`drop=None`). Regularization penalizes weights and resolves the singularity, while symmetric encoding improves interpretability.

#### Out-of-Vocabulary (OOV) Robustness at Inference
When deploying to production, a test record may contain a previously unseen category (e.g., `ocean_proximity = "ARCTIC"`).
- By default, standard encoders throw a runtime exception (`ValueError: Found unknown categories`).
- **Scikit-Learn Solution**: Initialize `OneHotEncoder(handle_unknown='ignore')`. This silently encodes the unseen category as an **all-zeros row** $\begin{bmatrix} 0 & 0 & 0 & 0 \end{bmatrix}^T$, allowing inference to proceed seamlessly without crashing.

---

### 3.3 Ordinal Encoding Implementation

Ordinal features require explicit declaration of category ordering during instantiation:

```python
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

# 1. Nominal Encoding with OOV Safety
ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
X_train_nom = ohe.fit_transform(X_train[['ocean_proximity']])
X_test_nom = ohe.transform(X_test[['ocean_proximity']])

# 2. Ordinal Encoding with Explicit Monotonic Hierarchy
ord_enc = OrdinalEncoder(categories=[['low', 'mid', 'high']])
X_train_ord = ord_enc.fit_transform(X_train[['income_band']])
X_test_ord = ord_enc.transform(X_test[['income_band']])
```

**Citations & References:**
- Micci-Barreca, D. (2001). A preprocessing scheme for high-cardinality categorization predictors in data mining. ACM SIGKDD Explorations, 3(1), 27-32.
- Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python.

---

## 4. Numerical Feature Scaling: Standard, Min-Max & Robust Transformations
### 4.1 Why Algorithm Sensitivity Depends on Feature Scale

Different machine learning model families exhibit starkly different mathematical responses to feature magnitudes:

```
Distance-Based Distortion (KNN / K-Means / SVM):
   Point A: Income = 50,000 USD, Age = 25
   Point B: Income = 52,000 USD, Age = 45
   Euclidean Distance = sqrt( (52000 - 50000)^2 + (45 - 25)^2 )
                      = sqrt( 4,000,000 + 400 ) = sqrt( 4,000,400 ) approx 2000.1
   The Age difference (20 years) is completely drowned out by Income ($2000)!
```

#### 1. Distance-Based Algorithms (KNN, K-Means, SVM, PCA)
Calculate distances using the Euclidean metric $d(\mathbf{x}_1, \mathbf{x}_2) = \sqrt{\sum_{j=1}^d (x_{1,j} - x_{2,j})^2}$. Features with large raw numerical ranges (`total_rooms` $\in [100, 30000]$) dominate the metric tensor, rendering small-scale features (`median_income` $\in [0.5, 15.0]$) mathematically invisible.

#### 2. Gradient Descent Optimizers (Logistic Regression, Neural Nets)
When feature scales differ drastically, the loss landscape contours form highly elongated, eccentric ellipses. Gradient vectors oscillate perpendicular to the optimal trajectory, demanding painfully small learning rates. Scaling spherizes the loss surface, enabling direct, rapid descent toward the global minimum.

```
Unscaled Features (Elongated Ellipse):            Scaled Features (Spherical Contours):
         w_2 ^                                            w_2 ^
             |      /---------\                               |       /-----\
             |     /     |     \                              |      /   |   \
             |    /  <---|--->  \                             |     | <--+--> |
             |    \      |      /                             |      \   |   /
             |     \-----------/                              |       \-----/
             +--------------------> w_1                       +--------------------> w_1
       Oscillatory zigzagging path                      Direct radial descent path
```

#### 3. Regularized Models (Ridge $L_2$, Lasso $L_1$)
Regularization appends a penalty $\lambda \sum w_j^2$ or $\lambda \sum |w_j|$ to the objective function. Unscaled features with tiny numerical values require massive weights $w_j$ to exert predictive impact; the regularization penalty disproportionately shrinks these weights, biasing the model against unscaled features.

#### 4. Scale-Invariant Models: Decision Trees
Decision Trees, Random Forests, and Gradient Boosting evaluate splits purely on rank-order thresholds ($x_j \le \tau$). Because any monotonic transformation preserves order, **tree models are completely scale-invariant**.

---

### 4.2 Mathematical Comparison of Numerical Scalers

| Scaler Name | Mathematical Formulation | Center & Scale Statistics | Primary Use Case & Sensitivity |
| :--- | :--- | :--- | :--- |
| **StandardScaler (Z-Score)** | $$z = \frac{x - \mu}{\sigma}$$ | Mean $\mu = 0$, Variance $\sigma^2 = 1$ | Default choice for linear models, logistic regression, PCA. Assumes roughly Gaussian-like distributions. **Highly sensitive to extreme outliers**. |
| **MinMaxScaler** | $$x_{\text{norm}} = \frac{x - x_{\text{min}}}{x_{\text{max}} - x_{\text{min}}}$$ | Bounds data to $[0, 1]$ (or $[a, b]$) | Neural networks, image processing, bounded bounded ranges. **Extremely sensitive to outliers** (one huge outlier compresses all other data into $[0, 0.05]$). |
| **RobustScaler** | $$x_{\text{rob}} = \frac{x - Q_2(\mathbf{x})}{Q_3(\mathbf{x}) - Q_1(\mathbf{x})} = \frac{x - \text{median}}{\text{IQR}}$$ | Centered at Median, scaled by Interquartile Range (IQR) | **Heavy-tailed distributions with severe outliers**. Outliers do not influence the median or IQR. |

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# ALWAYS fit on train, transform test
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train[num_cols])
X_test_scaled = scaler.transform(X_test[num_cols])  # Uses mu_train and sigma_train!
```

**Citations & References:**
- Ioffe, S., & Szegedy, C. (2015). Batch normalization: Accelerating deep network training by reducing internal covariate shift. ICML.
- Rousseeuw, P. J., & Croux, C. (1993). Alternatives to the median absolute deviation. Journal of the American Statistical Association, 88(424), 1273-1283.

---

## 5. Missing Value Imputation: Mechanisms, Trade-offs & Hygiene
### 5.1 The Missing Data Taxonomy (Rubin's Framework)

Before imputing missing values, an engineer must diagnose the underlying statistical mechanism driving the missingness:

1. **Missing Completely at Random (MCAR)**: The probability of missingness is entirely independent of observed and unobserved data: $P(M \mid Y_{\text{obs}}, Y_{\text{mis}}) = P(M)$. Example: A blood sample test tube accidentally drops and shatters on the laboratory floor.
2. **Missing at Random (MAR)**: Missingness depends systematically on observed features, but not on the missing value itself: $P(M \mid Y_{\text{obs}}, Y_{\text{mis}}) = P(M \mid Y_{\text{obs}})$. Example: In a survey, men may report income less frequently, but among men, missingness is unrelated to the actual income level.
3. **Missing Not at Random (MNAR)**: Missingness depends directly on the unobserved value itself: $P(M \mid Y_{\text{obs}}, Y_{\text{mis}}) = P(M \mid Y_{\text{mis}})$. Example: Individuals with extremely high income systematically refuse to disclose their salary.

---

### 5.2 Imputation Strategies & Trade-offs

| Strategy | Scikit-Learn Class | When to Use | Trade-offs & Risks |
| :--- | :--- | :--- | :--- |
| **Drop Rows (Complete Case)** | `df.dropna(subset=['col'])` | Negligible missingness ($< 1-2\%$), confirmed MCAR. | **Fatal at Inference**: If a live user sends a request missing that field, the production API cannot drop the user and crashes. |
| **Drop Column** | `df.drop(columns=['col'])` | Column is $> 70-80\%$ null and offers zero unique predictive signal. | Permanently destroys potentially vital signals. |
| **Mean Imputation** | `SimpleImputer(strategy='mean')` | Strictly symmetric, Gaussian numeric distributions without outliers. | Artificially reduces variance, underestimates standard errors, and distorts covariance structures. |
| **Median Imputation** | `SimpleImputer(strategy='median')` | **Default choice for skewed numeric features with outliers**. | Robust to extreme values; preserves distributional median. |
| **Mode Imputation** | `SimpleImputer(strategy='most_frequent')` | Categorical and discrete features. | Can amplify majority class imbalance. |
| **Missing Indicator** | `SimpleImputer(add_indicator=True)` | When missingness itself carries informative predictive signal. | Appends binary column $\mathbb{I}(x_{ij} = \text{NaN})$, allowing models to learn the pattern of absence. |

```
The Distortion of Mean vs. Median Imputation under Skewness:
   Raw Sample with Outlier: [ 20, 22, 21, 24, 23, 22, 500 ] (e.g., California rooms)
   Median = 22.0  <--- Representative typical value
   Mean   = 90.3  <--- Pulled massively by the single 500 outlier!
Filling missing values with 90.3 injects high-bias fictitious data into the training set.
```

#### Code Implementation: Safe Imputation Protocol
```python
from sklearn.impute import SimpleImputer

# Instantiate imputer
imputer = SimpleImputer(strategy="median", add_indicator=True)

# Fit on TRAIN ONLY
X_train_imputed = imputer.fit_transform(X_train[num_cols])

# Transform TEST using train medians
X_test_imputed = imputer.transform(X_test[num_cols])
```

**Citations & References:**
- Little, R. J., & Rubin, D. B. (2019). Statistical Analysis with Missing Data (3rd ed.). John Wiley & Sons.
- Van Buuren, S. (2018). Flexible Imputation of Missing Data. CRC Press.

---

## 6. Industrial Pipeline Architecture with Scikit-Learn
### 6.1 The "Locked Train Stats Box" Architecture

Manual preprocessing requires orchestrating dozens of separate imputers, scalers, and encoders. In production, this ad-hoc workflow inevitably leads to leakage bugs or training-serving skew.

Scikit-Learn solves this via **`ColumnTransformer`** and **`Pipeline`**:
- **`ColumnTransformer`**: Directs column subsets (numeric, nominal, ordinal) to distinct transformation sub-pipelines.
- **`Pipeline`**: Combines the preprocessing transformers with an estimator into a single, cohesive, atomic object.

```
                        The Scikit-Learn Monolithic Pipeline:
+---------------------------------------------------------------------------------------+
|  ColumnTransformer:                                                                   |
|   +-- Numeric Cols ----> [ SimpleImputer(median) ] ----> [ StandardScaler() ] ------+ |
|   |                                                                                 | |
|   +-- Nominal Cols ----> [ SimpleImputer(mode) ] ------> [ OneHotEncoder(ignore) ] -+ |
|   |                                                                                 | |
|   +-- Ordinal Cols ----> [ SimpleImputer(mode) ] ------> [ OrdinalEncoder(...) ] ---+ |
+-------------------------------------------------------------------------------------|-+
                                                                                      | Concatenated
                                                                                      v Matrix
                                                                     [ Ridge Regression ]
```

When you execute `pipeline.fit(X_train, y_train)`:
1. Every statistical parameter (medians, means, standard deviations, categorical vocabularies) is estimated **strictly from `X_train`**.
2. All parameters are stored internally in the pipeline's estimator state (`named_steps`).
3. Calling `pipeline.predict(X_test)` transforms test data using the frozen training statistics and outputs predictions. **Data leakage becomes structurally impossible.**

---

### 6.2 Complete End-to-End Implementation

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 1. Feature Partitioning
num_cols = ["median_income", "housing_median_age", "total_rooms", "total_bedrooms", "population", "households"]
nom_cols = ["ocean_proximity"]
ord_cols = ["income_band"]

# 2. Build Sub-Pipelines
numeric_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

nominal_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

ordinal_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("ordinal", OrdinalEncoder(categories=[["low", "mid", "high"]]))
])

# 3. Assemble Master ColumnTransformer
preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_pipe, num_cols),
    ("nom", nominal_pipe, nom_cols),
    ("ord", ordinal_pipe, ord_cols)
])

# 4. Bind Preprocessor and Estimator into Master Pipeline
full_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", Ridge(alpha=1.0))
])

# 5. Fit Once on Train; Evaluate on Test
full_pipeline.fit(X_train, y_train)
y_pred = full_pipeline.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Test RMSE: {rmse:,.2f}")
print(f"Test MAE:  {mae:,.2f}")
print(f"Test R^2:  {r2:.4f}")
```

---

### 6.3 The Leakage Detective: Real-World Case Studies

| Case Study Scenario | Leakage Verdict | Root Cause & Architectural Fix |
| :--- | :--- | :--- |
| **Case 1**: Calculating median of `total_bedrooms` across the entire CSV before running `train_test_split`. | **LEAK** | *Preprocessing Leakage*: Test median leaks into train fill values. **Fix**: Split first, compute median on `X_train` only. |
| **Case 2**: Splitting first, fitting `OneHotEncoder(handle_unknown='ignore')` on `X_train`, transforming `X_test`. | **NO LEAK** | Clean pipeline design. Vocabulary learned from train; unseen test categories encoded safely as all-zeros. |
| **Case 3**: Adding `is_high_value = (median_house_value > 200000)` into feature matrix $X$ to predict house value. | **LEAK** | *Target Leakage*: Target variable explicitly copied into the feature set. **Fix**: Delete label-derived features. |
| **Case 4**: Evaluating credit risk where 20% highest income applicants are manually selected into test set. | **LEAK** | *Covariate Shift / Evaluation Bias*: Non-random holdout biases metrics. **Fix**: Random stratified or chronological holdout. |

**Citations & References:**
- Buitinck et al. (2013). API design for machine learning software: experiences from the scikit-learn project. ECML PKDD Workshop.
- Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn. O'Reilly Media.

---
