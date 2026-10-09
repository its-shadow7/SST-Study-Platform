# Lecture 2: Data Preparation for Machine Learning
## Student Notes — SST Classical Machine Learning

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Define **Data Leakage** in all its forms (**Preprocessing Leakage**, **Target Leakage**, and **Temporal Leakage**) and identify subtle leakage vectors in production code.
- Enforce strict **Train-Test Hygiene**: prove mathematically why transformations must be fit *exclusively* on the training partition and merely applied to validation/test partitions.
- Differentiate between **Nominal** and **Ordinal** categorical variables, avoiding the **Nominal Distance Trap** and the **Dummy Variable Trap** ($k$ vs. $k-1$ collinearity).
- Mathematically formulate and implement the three primary continuous feature scalers: **StandardScaler**, **MinMaxScaler**, and **RobustScaler**, explaining their behavior under heavy outlier distributions.
- Analyze the three classical statistical mechanisms of missing data (**MCAR**, **MAR**, and **MNAR**) and select appropriate imputation strategies (Median, Mode, MissingIndicator).
- Architect clean, leakage-proof, modular production workflows using Scikit-Learn's `ColumnTransformer` and `Pipeline`.

---

## 1. The Hook: "Fake-Good" Scores and the Silent Bug

In traditional software development, bugs manifest loudly: `NullPointerException`, `IndexOutOfBoundsError`, or segmentation faults.

In Machine Learning, **data preparation mistakes do not crash your program**. Instead, they manifest as **"fake-good" scores**:
- An engineer trains a fraud detection model and observes a suspicious $99.8\%$ ROC-AUC on their test set.
- Management celebrates and deploys the model to production.
- Within 48 hours, the live production ROC-AUC plummets to $58.2\%$, costing the company millions.

What happened? The model was not brilliant; it was simply cheating. During preprocessing, information from the test set or from the future was inadvertently leaked into the training feature space.

```
   Traditional Bug:            Machine Learning Data Leakage Bug:
   ┌────────────────┐          ┌────────────────┐
   │ Code Crashes   │          │ Program Runs   │
   │ Stack Trace    │          │ Test AUC = 99% │───► Catastrophic Failure
   │ (Immediate Fix)│          │ (Silent Fake   │     in Production
   └────────────────┘          │  Good Score)   │
                               └────────────────┘
```

---

## 2. The Taxonomy of Data Leakage

Data leakage occurs whenever training data is contaminated with information that will not be legitimately available at inference time.

```
                                      DATA LEAKAGE
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         ▼                                 ▼                                 ▼
   Preprocessing Leakage            Target Leakage                    Temporal Leakage
  (Fitting scalers, imputers,      (Feature includes proxy of       (Using future timestamps to
   or encoders on full dataset)     the target label itself)         predict historical events)
```

### 1. Preprocessing Leakage (The "Fit-on-All" Trap)
This is the most widespread beginner mistake.
```python
# ❌ CATASTROPHIC LEAKAGE: Scaler computes mean/std over X_test!
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X) # Peeks at test set!
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)
```
When `scaler.fit(X)` executes across the whole dataframe, the sample mean $\mu_{\text{total}}$ and standard deviation $\sigma_{\text{total}}$ incorporate observations from `X_test`. Consequently, `X_train` receives indirect statistical knowledge of the test set's distribution.

### 2. Target Leakage (The "Future Proxy" Trap)
Target leakage occurs when an independent feature $x_j$ contains information directly caused by or chronologically succeeding the target variable $y$.
- **Example 1**: Predicting hospital patient mortality ($y \in \{0, 1\}$). A feature in the table is `ICU_Palliative_Care_Medication_Administered`. Doctors only administer this medication when a patient is already in terminal distress. The feature is a proxy for the label.
- **Example 2**: Predicting customer loan default. A column `Total_Late_Fee_Refund_Requests` collected 6 months *after* loan origination is included in the training table for credit underwriting. At the moment of loan origination, this feature does not exist.

### 3. Temporal Leakage (The "Time Traveler" Trap)
In time-series, financial, or user-behavior datasets, random train-test splitting leaks future patterns into the past.
- If you randomly split stock market records between 2018 and 2024 into $80\%$ train and $20\%$ test, the model trains on Wednesday's price to predict Tuesday's price.
- **Remedy**: Always perform a chronological **Time-Based Split** (e.g., Train on 2018–2022, Validate on 2023, Test on 2024).

---

## 3. Strict Train-Test Hygiene: The Locked Train Stats Box

To guarantee mathematically sound evaluation, conceptualize a **Locked Box** labeled **TRAIN STATS**:

```
                  ┌─────────────────────────────────────────┐
                  │          LOCKED BOX: TRAIN STATS        │
                  │   μ_train, σ_train, Median_train,       │
                  │   Vocabulary_train, OneHotCategories    │
                  └─────────────────────────────────────────┘
                                       │
                      Fit on Train Only │ Borrowed by Test
                                       ▼
     ┌──────────────────────┐                     ┌──────────────────────┐
     │    X_train (80%)     │                     │     X_test (20%)     │
     │                      │                     │                      │
     │ Fit Imputer & Scaler │                     │ Only Transform!      │
     │ Transform X_train    │                     │ Never call .fit()!   │
     └──────────────────────┘                     └──────────────────────┘
```

### Golden Rule of ML Hygiene
> **Every single parameter or statistic learned from data** ($\mu, \sigma$, median, most-frequent category, vocabulary tokens, PCA eigenvectors) **must be calculated solely from $X_{\text{train}}$. Validation and test sets only borrow those fitted transformations.**

```python
# ✅ CORRECT HYGIENE:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train) # Computes mu_train, sigma_train
X_test_scaled  = scaler.transform(X_test)      # Uses mu_train, sigma_train!
```

---

## 4. Handling Categorical Variables: Nominal vs. Ordinal

Machine learning algorithms are vector machines; they cannot compute inner products $\mathbf{w}^T \mathbf{x}$ on string literals such as `"California"` or `"Executive"`. We must project strings into numeric representations.

```
                                  CATEGORICAL FEATURES
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    ▼                                             ▼
           Nominal Features                              Ordinal Features
       (No intrinsic ordering)                       (Clear, intrinsic hierarchy)
       Examples: City, Color, BloodType              Examples: T-Shirt Size, Education
                    │                                             │
                    ▼                                             ▼
            One-Hot Encoding                              Ordinal Encoding
       (Dummy Indicator Vectors)                     (Ordered Monotonic Integers)
```

### 1. Nominal Features: One-Hot Encoding
Nominal features possess no natural mathematical hierarchy.
- Cities: `["Mumbai", "Bengaluru", "Delhi"]`
- Colors: `["Red", "Green", "Blue"]`

#### The Nominal Distance Trap
If you naively map `{"Mumbai": 1, "Bengaluru": 2, "Delhi": 3}`, a linear regression or distance-based algorithm asserts:

$$\text{Delhi} (3) - \text{Mumbai} (1) = 2 \times (\text{Bengaluru} (2) - \text{Mumbai} (1))$$

It imposes a false metric space where Delhi is twice as far from Mumbai as Bengaluru is!
- **Remedy**: Use **One-Hot Encoding**, expanding $C$ categories into $C$ orthogonal binary dimensions:
  - $\text{Mumbai} \to [1, 0, 0]$
  - $\text{Bengaluru} \to [0, 1, 0]$
  - $\text{Delhi} \to [0, 0, 1]$

#### The Dummy Variable Trap (Strict Multicollinearity)
If an intercept $\theta_0$ is present in linear regression, including all $C$ one-hot columns creates perfect linear dependence:

$$\sum_{k=1}^C x_k = 1 = x_0$$

The matrix $X^T X$ becomes singular and non-invertible.
- **Remedy**: In unregularized linear models, drop one category: `drop="first"` ($C-1$ columns). In regularized linear models (Ridge/Lasso) or tree models, keep all $C$ columns with `drop=None`.

#### Handling Unseen Test Categories
What happens when $X_{\text{test}}$ encounters a city never observed in $X_{\text{train}}$ (e.g., `"Hyderabad"`)?
- Standard encoders crash with a `ValueError`.
- In Scikit-Learn, always set `OneHotEncoder(handle_unknown="ignore")`. Unseen categories are encoded as an all-zeros vector $[0, 0, \dots, 0]$ without breaking the inference pipeline.

### 2. Ordinal Features: Ordinal Encoding
Ordinal features possess an unambiguous, ranked order:
- Education: `["High School", "Bachelor's", "Master's", "Ph.D."]`
- Size: `["XS", "S", "M", "L", "XL"]`

Here, preserving the order is statistically informative.
```python
from sklearn.preprocessing import OrdinalEncoder

size_order = [["XS", "S", "M", "L", "XL"]]
ordinal_enc = OrdinalEncoder(categories=size_order)
```

---

## 5. Numerical Feature Scaling

When features have radically different physical units, unscaled data causes catastrophic optimization and geometric distortions:

```
   Unscaled Feature Space (Contour Ellipse):   Scaled Feature Space (Spherical Contours):
              x₂ (Salary in ₹: 0 - 2,000,000)                x₂
              ▲                                              ▲
              │   ╭───────────────────────╮                  │       ╭─────╮
              │  │           •             │                 │      │   •   │
              │   ╰───────────────────────╯                  │       ╰─────╯
              └───────────────────────────► x₁               └──────────────► x₁
                   (Age in Years: 18 - 70)
        Gradient Descent oscillates wildly;           Gradient Descent marches directly
        Euclidean distance dominated by x₂!           to the global optimum!
```

### Mathematical Comparison of Scaling Methods

| Scaler | Mathematical Formula | Target Properties | Outlier Sensitivity |
| :--- | :--- | :--- | :--- |
| **StandardScaler** | $$z = \frac{x - \mu}{\sigma}$$ | $\mu = 0, \; \sigma = 1$ (Zero-mean, unit variance) | **High** (Outliers distort both $\mu$ and $\sigma$) |
| **MinMaxScaler** | $$x_{\text{scaled}} = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$$ | Bounded strictly to $[0, 1]$ (or $[a, b]$) | **Extreme** (A single outlier squashes all normal data into a narrow band) |
| **RobustScaler** | $$x_{\text{scaled}} = \frac{x - Q_2}{\text{IQR}} = \frac{x - \text{median}}{Q_3 - Q_1}$$ | Centered on median, scaled by interquartile range | **Immune** (Median and IQR ignore extreme tail outliers) |

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# StandardScaler: Default choice for Gaussian-like features & linear/logistic regression
scaler_standard = StandardScaler()

# MinMaxScaler: Essential when features must strictly fit bounded intervals (e.g. image pixels [0, 1])
scaler_minmax = MinMaxScaler(feature_range=(0, 1))

# RobustScaler: Essential for financial / heavy-tailed data with extreme anomalies
scaler_robust = RobustScaler()
```

---

## 6. Missing Data: Mechanisms & Imputation Strategies

Before applying an imputation formula, an engineer must diagnose the underlying statistical missingness mechanism (Donald Rubin’s framework):

```
                               MISSINGNESS MECHANISMS
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
   Missing Completely               Missing at                      Missing Not
    at Random (MCAR)               Random (MAR)                   at Random (MNAR)
 (Probability of missingness      (Missingness depends on       (Missingness depends on the
  is purely random; independent    other observed features;      unobserved value itself; e.g.
  of any feature or target)        e.g., young men omit mood)    high-earners refuse salary Qs)
```

### Imputation Techniques

```python
from sklearn.impute import SimpleImputer, MissingIndicator

# 1. Median Imputation (For skewed continuous features with outliers)
med_imputer = SimpleImputer(strategy="median")

# 2. Mean Imputation (Only for symmetric, normally distributed features)
mean_imputer = SimpleImputer(strategy="mean")

# 3. Mode (Most Frequent) Imputation (For categorical features)
mode_imputer = SimpleImputer(strategy="most_frequent")

# 4. Constant Imputation (For explicit placeholder semantics)
const_imputer = SimpleImputer(strategy="constant", fill_value="Unknown")
```

> [!IMPORTANT]
> **Why Median over Mean for Skewed Features?**  
> Consider house prices in a neighborhood: nine houses are valued at $\$300\text{k}$, and one celebrity mansion is valued at $\$20\text{M}$.  
> - $\text{Mean} = \$2.27\text{M}$  
> - $\text{Median} = \$300\text{k}$  
> Imputing the mean creates nine distorted, fictitious multimillion-dollar entries. Imputing the median preserves typical neighborhood characteristics.

#### The MissingIndicator Pattern
Sometimes the fact that a value was missing carries profound predictive signal (e.g., patients who did not take a secondary blood test were deemed healthier by their physician). Adding a binary flag preserves this signal:

$$\tilde{x}_j = \text{impute}(x_j), \quad m_j = \mathbb{I}(x_j \text{ is missing})$$

---

## 7. Gluing It Together: Leakage-Proof Production Pipelines

To make accidental leakage impossible, combine Scikit-Learn’s `ColumnTransformer` with `Pipeline`. The resulting composite object can be serialized (`joblib.dump`) and served in production as an atomic unit.

```python
"""
Production-Grade Leakage-Proof Machine Learning Pipeline
Encapsulates missing value imputation, categorical encoding, scaling, and regressor fitting.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score

# 1. Create realistic synthetic dataset with mixed types & missing values
np.random.seed(42)
n = 1000

data = pd.DataFrame({
    "income": np.random.lognormal(mean=10.5, sigma=0.8, size=n),
    "age": np.random.randint(18, 75, size=n).astype(float),
    "education": np.random.choice(["High School", "Bachelor", "Master", "PhD"], size=n),
    "city": np.random.choice(["New York", "London", "Tokyo", "Berlin"], size=n),
    "credit_score": np.random.normal(650, 50, size=n)
})

# Inject missing values into numeric and categorical columns
data.loc[np.random.choice(n, 30), "age"] = np.nan
data.loc[np.random.choice(n, 20), "city"] = np.nan

# Define synthetic target
y = (data["income"] * 0.05 + data["credit_score"] * 2.5 + np.random.normal(0, 50, n))
X = data

# 2. Strict Train/Test Separation FIRST
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# 3. Partition Feature Sets
numeric_cols = ["income", "age", "credit_score"]
categorical_cols = ["education", "city"]

# 4. Define Sub-Pipelines for Specific Data Types
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", drop="first"))
])

# 5. Assemble Global ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols)
    ],
    remainder="drop"
)

# 6. Glue Preprocessor to Estimator
full_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", Ridge(alpha=1.0))
])

# 7. Fit: Computes all imputers, scalers, and encoders SOLELY on X_train
full_model.fit(X_train, y_train)

# 8. Predict & Evaluate: Uses learned train statistics seamlessly on X_test
y_pred_test = full_model.predict(X_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
test_r2 = r2_score(y_test, y_pred_test)

print(f"Pipeline Test RMSE: {test_rmse:.2f}")
print(f"Pipeline Test R²:   {test_r2:.4f}")
```

---

## 8. Common Pitfalls & Interview-Grade Questions

### Q1: An engineer writes `X_scaled = StandardScaler().fit_transform(X)` followed by 5-fold cross-validation. What critical error occurred, and how will it bias the cross-validation score?
**Answer**:  
This is **cross-validation preprocessing leakage**. By fitting the scaler on the entire dataset $X$ prior to folding, the validation fold in each of the 5 splits has its sample mean and variance leaked into the scaling transformation. Consequently, validation folds are not true independent tests. The reported cross-validation score will be artificially optimistic. In production on genuinely novel data, the model will underperform expectations. The fix is embedding `StandardScaler` inside a Scikit-Learn `Pipeline`, allowing the CV iterator to fit the scaler strictly on the 4 training folds per iteration.

### Q2: Under what conditions is `OneHotEncoder(drop='first')` mandatory, and when should it be avoided?
**Answer**:  
`drop='first'` is mandatory in **unregularized linear models** (standard Ordinary Least Squares, unregularized Logistic Regression) when an intercept term $\theta_0$ is present. Without dropping the first category, the one-hot columns sum identically to $1$ (the intercept column), creating perfect multicollinearity (a singular matrix $X^T X$) that prevents matrix inversion. Conversely, `drop='first'` should be avoided in **regularized models** (Ridge, Lasso) and **tree-based algorithms**. Ridge regression shrinks coefficients toward zero; dropping a baseline category forces the shrinkage penalty to treat the omitted reference category asymmetrically.

### Q3: Why is `SimpleImputer(strategy='mean')` dangerous when applied to features with heavy-tailed distributions like income or transaction volume?
**Answer**:  
The arithmetic mean is not a robust statistic; its breakdown point is $0\%$, meaning a single extreme outlier can pull the mean arbitrarily far from the center of mass. In skewed distributions (e.g., Pareto or log-normal distributions typical in wealth or web traffic), the mean is significantly higher than what $80\%$ of the population exhibits. Imputing missing values with the mean injects uncharacteristically high values into typical profiles, distorting the empirical distribution and damaging downstream model predictions. `strategy='median'` must be used instead.

---

## 9. Summary & Key Takeaways

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                     SESSION 2 KEY TAKEAWAYS                            │
   ├────────────────────────────────────────────────────────────────────────┤
   │ 1. Fake-Good Scores: Preprocessing bugs look like winning models on    │
   │    paper. Always suspect unrealistically high evaluation metrics.      │
   │ 2. Split First, Always: Lock the TRAIN STATS box. Learn μ, σ, medians, │
   │    and category sets only from X_train; only transform X_test.         │
   │ 3. Nominal vs. Ordinal: Never inject artificial integer distances into │
   │    nominal features. Use OneHotEncoder(handle_unknown='ignore').       │
   │ 4. Scaler Selection: Use StandardScaler for Gaussian features,         │
   │    MinMaxScaler for bounded intervals, and RobustScaler for outliers.  │
   │ 5. Median over Mean: In skewed data, median imputation prevents the    │
   │    mean-pull distortion caused by extreme tail values.                 │
   │ 6. Pipeline Architecture: ColumnTransformer + Pipeline makes data     │
   │    leakage architecturally impossible during training and inference.   │
   └────────────────────────────────────────────────────────────────────────┘
```
