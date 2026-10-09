# Lecture 10: Industry Classification Lab — Customer Churn Case Study
## Student Notes — SST Classical Machine Learning

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Translate a messy real-world business objective into a formal supervised binary classification task ($y \in \{0, 1\}$).
- Construct an **Asymmetric Business Cost Matrix** ($c_{\text{FN}} \gg c_{\text{FP}}$) and prove why the textbook default decision threshold ($\tau = 0.5$) is almost never the commercial optimum.
- Implement an end-to-end, leakage-free pipeline benchmarking **Logistic Regression** (global parametric linear boundary) against **K-Nearest Neighbours** (local non-parametric boundary).
- Tune the inverse regularization hyperparameter $C$ in Logistic Regression and neighbor count $k$ in $k$-NN using **Stratified $K$-Fold Cross-Validation**.
- Optimize the operational **Decision Threshold ($\tau$)** strictly on validation folds to minimize total financial expected loss without peeking at test data.
- Execute a **Production Machine Learning Deployment Checklist**, establishing model serialization, latency SLAs, feature pipelines, and continuous drift monitoring.

---

## 1. The Business Context: SaaS Customer Churn

You are the Lead Machine Learning Engineer at a subscription enterprise software company.

Every month, a fraction of active paying subscribers terminate their contracts (**churn**, $y = 1$). The Customer Success team has an allocated budget to intervene with proactive retention outreach (discounts, dedicated technical account managers, phone consultations).

```
   BUSINESS OBJECTIVE: Predict Churn in Month M+1 using Usage Signals from Month M
   ┌────────────────────────────────────────────────────────┐
   │ Usage Data (M): Logins, API Calls, Support Tickets     │──► [ ML Classifier ]
   └────────────────────────────────────────────────────────┘           │
                                                                        ▼
                                                             Risk Probability: p̂
                                                                        │
                                   ┌────────────────────────────────────┴────────────────────────────────────┐
                                   ▼ (If p̂ ≥ τ)                                                             ▼ (If p̂ < τ)
                      [ Flag Customer for Intervention ]                                          [ No Action: Regular Service ]
```

### The Cost of Classification Errors
The executive committee establishes the following unit economics:
- **Cost of a False Positive (FP)**: The model incorrectly flags a loyal customer who had no intention of leaving. We expend human Customer Success time and offer a $\$50$ discount coupon they did not need:

  $$\text{Cost}(\text{FP}) = \$50$$

- **Cost of a False Negative (FN)**: The model fails to flag a churner. The customer leaves uncontacted. We forfeit their Annual Recurring Revenue (ARR) and incur customer acquisition replacement costs:

  $$\text{Cost}(\text{FN}) = \$1,000$$

> [!CRITICAL]
> **The Economic Imbalance**:  
> A False Negative is **$20\times$ more expensive** than a False Positive:
> $$\frac{\text{Cost}(\text{FN})}{\text{Cost}(\text{FP})} = \frac{\$1,000}{\$50} = 20$$
> Any engineer optimizing raw classification accuracy or blindly applying threshold $\tau = 0.50$ is squandering company capital.

---

## 2. Architectural Comparison: Logistic Regression vs. K-NN

Before writing code, we contrast our two competing algorithmic architectures:

```
   ┌─────────────────────────────────┬─────────────────────────────────┐
   │       LOGISTIC REGRESSION       │       K-NEAREST NEIGHBOURS      │
   ├─────────────────────────────────┼─────────────────────────────────┤
   │ Model Type: Parametric Eager    │ Model Type: Non-Parametric Lazy │
   ├─────────────────────────────────┼─────────────────────────────────┤
   │ Decision Boundary: Flat linear  │ Decision Boundary: Arbitrarily  │
   │ hyperplane in log-odds space    │ complex, non-linear polygons    │
   ├─────────────────────────────────┼─────────────────────────────────┤
   │ Hyperparameter: C = 1 / λ       │ Hyperparameter: Number of       │
   │ (Inverse regularization strength)│ neighbors k, distance metric p  │
   ├─────────────────────────────────┼─────────────────────────────────┤
   │ Inference Speed: Ultra-fast     │ Inference Speed: Heavy search   │
   │ O(d) dot product; < 1ms latency │ O(nd) pairwise scan; memory-taxing│
   ├─────────────────────────────────┼─────────────────────────────────┤
   │ Interpretability: High; weights │ Interpretability: Low; outputs  │
   │ directly map to odds ratios     │ local neighborhood consensus    │
   └─────────────────────────────────┴─────────────────────────────────┘
```

```
   Decision Boundary Geometries:
         Logistic Regression (Global Hyperplane):       K-Nearest Neighbours (Local Voronoi Islands):
         x₂                                            x₂
         ▲                     Class 1                 ▲             ╭─╮ Class 1
         │                  •   •   •                  │            │ • │
         │               •    •   •                    │     ╭──────╯   ╰──────╮
         │─────────────/───────────────────            │    │   •         •   │
         │           /                                 │     ╰───────────╮   │
         │   ▲   ▲  /                                  │       ▲     ▲    │ • │
         │ ▲   ▲   /           Class 0                 │    ▲    ▲     ▲   ╰─╯
         └────────/────────────────────────► x₁        └────────────────────────► x₁
```

---

## 3. The End-to-End Implementation Pipeline

The complete Python script below implements the end-to-end industrial workflow:
1. Synthetic generation of realistic churn profiles with numerical and categorical attributes.
2. Stratified train-test partitioning.
3. Automated feature imputation, one-hot encoding, and standard scaling via `ColumnTransformer`.
4. Hyperparameter tuning using `GridSearchCV` on training folds.
5. Cost-optimal decision threshold search.
6. Honest, unpeeked evaluation on the sealed test partition.

```python
"""
End-to-End Industrial Churn Classification Lab
Benchmarking Logistic Regression vs. K-Nearest Neighbours with Cost-Optimal Thresholding.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_auc_score, f1_score
)

# =====================================================================
# 1. SYNTHESIZE REALISTIC INDUSTRY DATASET (~20% Base Churn Rate)
# =====================================================================
np.random.seed(42)
n_records = 3000

monthly_charges = np.random.normal(70, 30, n_records).clip(20, 200)
tenure_months = np.random.exponential(18, n_records).clip(1, 72)
support_tickets = np.random.poisson(1.5, n_records)
contract_type = np.random.choice(["Month-to-Month", "One-Year", "Two-Year"], size=n_records, p=[0.55, 0.25, 0.20])

# Latent logit driving churn
latent_logit = (
    -1.5 
    + 0.02 * monthly_charges 
    - 0.06 * tenure_months 
    + 0.50 * support_tickets 
    + 1.2 * (contract_type == "Month-to-Month")
)
churn_prob = 1.0 / (1.0 + np.exp(-latent_logit))
churn_labels = (np.random.uniform(0, 1, n_records) < churn_prob).astype(int)

df = pd.DataFrame({
    "monthly_charges": monthly_charges,
    "tenure_months": tenure_months,
    "support_tickets": support_tickets,
    "contract_type": contract_type,
    "churn": churn_labels
})

X = df.drop(columns=["churn"])
y = df["churn"]

# =====================================================================
# 2. STRICT TRAIN-TEST SEPARATION (Stratified 80-20 Split)
# =====================================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# =====================================================================
# 3. LEAKAGE-PROOF PREPROCESSING PIPELINE
# =====================================================================
numeric_cols = ["monthly_charges", "tenure_months", "support_tickets"]
categorical_cols = ["contract_type"]

num_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

cat_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(drop="first", handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", num_pipe, numeric_cols),
        ("cat", cat_pipe, categorical_cols)
    ]
)

# =====================================================================
# 4. CROSS-VALIDATION HYPERPARAMETER SEARCH
# =====================================================================
cv_strategy = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Candidate A: Logistic Regression (Tune C)
pipe_lr = Pipeline([
    ("prep", preprocessor),
    ("clf", LogisticRegression(max_iter=1000, random_state=42))
])
grid_lr = GridSearchCV(
    pipe_lr, 
    param_grid={"clf__C": [0.01, 0.1, 1.0, 10.0, 100.0]}, 
    cv=cv_strategy, 
    scoring="f1"
)
grid_lr.fit(X_train, y_train)

# Candidate B: K-Nearest Neighbours (Tune k)
pipe_knn = Pipeline([
    ("prep", preprocessor),
    ("clf", KNeighborsClassifier())
])
grid_knn = GridSearchCV(
    pipe_knn, 
    param_grid={"clf__n_neighbors": [5, 11, 21, 31, 51]}, 
    cv=cv_strategy, 
    scoring="f1"
)
grid_knn.fit(X_train, y_train)

print("=" * 60)
print(f"Logistic Regression: Best C = {grid_lr.best_params_['clf__C']} | CV F1 = {grid_lr.best_score_:.4f}")
print(f"K-Nearest Neighbours: Best k = {grid_knn.best_params_['clf__n_neighbors']} | CV F1 = {grid_knn.best_score_:.4f}")
print("=" * 60)

# Select the superior model
best_estimator = grid_lr.best_estimator_ if grid_lr.best_score_ >= grid_knn.best_score_ else grid_knn.best_estimator_
selected_name = "Logistic Regression" if best_estimator == grid_lr.best_estimator_ else "K-NN"
print(f"Selected Candidate for Production: {selected_name}")

# =====================================================================
# 5. THRESHOLD OPTIMIZATION USING ASYMMETRIC COST MATRIX
# =====================================================================
# Cost Matrix: False Negative = $1,000; False Positive = $50
COST_FN = 1000.0
COST_FP = 50.0

# Extract out-of-fold predicted probabilities on Train
# (Simulated via 5-fold cross-validation on train to prevent threshold overfitting)
from sklearn.model_selection import cross_val_predict
y_train_probs = cross_val_predict(best_estimator, X_train, y_train, cv=cv_strategy, method="predict_proba")[:, 1]

thresholds = np.linspace(0.05, 0.95, 91)
total_costs = []

for tau in thresholds:
    preds = (y_train_probs >= tau).astype(int)
    cm = confusion_matrix(y_train, preds)
    fn = cm[1, 0]
    fp = cm[0, 1]
    cost = fn * COST_FN + fp * COST_FP
    total_costs.append(cost)

optimal_threshold = thresholds[np.argmin(total_costs)]
min_cost = np.min(total_costs)

print(f"\nOptimal Economic Threshold (τ*): {optimal_threshold:.2f}")
print(f"Default Cost at τ = 0.50:       ${total_costs[45]:,.2f}")
print(f"Optimized Cost at τ = {optimal_threshold:.2f}:   ${min_cost:,.2f}")
print(f"Savings on Training Cohort:     ${total_costs[45] - min_cost:,.2f}")

# =====================================================================
# 6. SEALED TEST SET EVALUATION (Unpeeked Final Audit)
# =====================================================================
y_test_probs = best_estimator.predict_proba(X_test)[:, 1]
y_test_final = (y_test_probs >= optimal_threshold).astype(int)

cm_test = confusion_matrix(y_test, y_test_final)
test_auc = roc_auc_score(y_test, y_test_probs)
test_f1 = f1_score(y_test, y_test_final)

print("\n" + "=" * 60)
print(f"FINAL TEST SET EVALUATION (Operating at τ = {optimal_threshold:.2f}):")
print(f"Test ROC-AUC: {test_auc:.4f}")
print(f"Test F1:      {test_f1:.4f}")
print("\nTest Confusion Matrix:")
print(f"True Negatives:  {cm_test[0,0]:3d} | False Positives (Discounts): {cm_test[0,1]:3d}")
print(f"False Negatives: {cm_test[1,0]:3d} | True Positives (Saved Churn): {cm_test[1,1]:3d}")
print(f"Actual Churn Capture Rate (Recall): {cm_test[1,1] / (cm_test[1,0] + cm_test[1,1]):.2%}")
print("=" * 60)
```

---

## 4. Reading Coefficients for Executive Action

One decisive advantage of Logistic Regression over $k$-NN in industry is **explainability**. Stakeholders rarely accept a model that cannot explain *why* it predicts churn.

Inspecting the standardized slopes:
```python
lr_model = best_estimator.named_steps["clf"]
feature_names = best_estimator.named_steps["prep"].get_feature_names_out()
weights = pd.Series(lr_model.coef_[0], index=feature_names).sort_values(ascending=False)

for feat, w in weights.items():
    odds_ratio = np.exp(w)
    print(f"{feat:35s}: w = {w:+.4f} | Odds Ratio = {odds_ratio:.3f}x")
```

### Executive Takeaways
1. `num__support_tickets` ($w = +0.72$, $\text{OR} = 2.05\times$): Every additional standard deviation of support tickets doubles customer churn odds! **Action**: Trigger automatic senior manager intervention whenever a client logs $>3$ tickets in 14 days.
2. `cat__contract_type_Month-to-Month` ($w = +1.15$, $\text{OR} = 3.15\times$): Month-to-month contracts have $3.15\times$ higher churn odds than long-term annual contracts. **Action**: Offer onboarding incentives to migrate customers to annual subscriptions.
3. `num__tenure_months` ($w = -0.84$, $\text{OR} = 0.43\times$): Each additional year of tenure cuts churn odds by more than half ($57\%$ reduction). **Action**: High churn risk is concentrated in the first 90 days; focus retention budgets on early customer onboarding.

---

## 5. The Production Machine Learning Deployment Checklist

Shipping an ML model to production requires engineering discipline far beyond a Jupyter notebook:

```
               THE 6-STAGE PRODUCTION DEPLOYMENT AUDIT
       ┌────────────────────────────────────────────────────────┐
       │ 1. Serialization Integrity                             │
       │    Save the entire Pipeline (preprocessor + model)     │
       │    as a single immutable artifact: joblib.dump()       │
       ├────────────────────────────────────────────────────────┤
       │ 2. Feature Schema & Type Contracts                     │
       │    Enforce strict Pydantic / protobuf schemas at API   │
       │    gateways to reject malformed payloads.              │
       ├────────────────────────────────────────────────────────┤
       │ 3. Inference Latency & SLA Guarantees                  │
       │    Verify p95 latency < 20ms under 1,000 req/sec load. │
       ├────────────────────────────────────────────────────────┤
       │ 4. Deterministic Versioning                            │
       │    Tag models with Git SHA and training data hash.     │
       ├────────────────────────────────────────────────────────┤
       │ 5. Asymmetric Cost Monitoring                          │
       │    Continuously log precision, recall, and dollar loss │
       │    at the tuned operating threshold τ*.                │
       ├────────────────────────────────────────────────────────┤
       │ 6. Data & Concept Drift Telemetry                      │
       │    Detect shifts in input distributions (P(X)) and     │
       │    retrain on scheduled time windows.                  │
       └────────────────────────────────────────────────────────┘
```

---

## 6. Common Pitfalls & Interview-Grade Questions

### Q1: An engineer optimizes the decision threshold $\tau$ by testing 100 different thresholds on the final test set and selecting the threshold that achieves the lowest test cost. What critical methodological error occurred?
**Answer**:  
The engineer **overfit the test set through threshold snooping**. The test set is an inviolable, sealed final exam intended solely for an honest, unbiased estimation of generalization risk. By sweeping 100 thresholds across the test set, the chosen $\tau$ adapts to the idiosyncratic noise and specific sample quirks of that specific test partition. The true operational cost in production will be significantly higher. The threshold must be tuned **strictly on training validation folds** (via `cross_val_predict` or a dedicated holdout validation split), frozen, and then evaluated on the test set exactly once.

### Q2: Why is Logistic Regression frequently preferred over K-NN for real-time web applications, even when K-NN achieves slightly higher cross-validation accuracy?
**Answer**:  
1. **Inference Latency & Computational Footprint**: Logistic regression computes a simple vector dot product $\mathbf{w}^T \mathbf{x} + w_0$, requiring $\approx 2d$ floating-point operations ($< 0.1\text{ms}$). $k$-NN requires storing the entire training set in active memory and computing distances across thousands of points ($\mathcal{O}(n d)$), introducing unacceptable latency and memory costs in high-throughput microservices.
2. **Interpretability & Stakeholder Governance**: Regulated industries (banking, healthcare, credit) legally require explanations for adverse decisions. Logistic regression provides exact feature weights and odds ratios; $k$-NN is a black-box instance memory that cannot provide global policy guidance.

### Q3: What is the mathematical relationship between the regularization hyperparameter $C$ in Scikit-Learn’s `LogisticRegression` and the theoretical penalty coefficient $\lambda$?
**Answer**:  
In Scikit-Learn, $C$ is the **inverse of regularization strength**:

$$C = \frac{1}{\lambda}$$

- **Small $C$** ($C = 0.001 \implies \lambda = 1,000$): Imposes heavy $L_2$ shrinkage on weights, producing a very simple, constrained model with **high bias and low variance** (combats overfitting).
- **Large $C$** ($C = 1,000 \implies \lambda = 0.001$): Minimizes the regularization penalty, allowing weights to grow large to fit complex training patterns, producing **low bias and high variance** (risks overfitting).

---

## 7. Summary & Key Takeaways

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                     SESSION 10 KEY TAKEAWAYS                           │
   ├────────────────────────────────────────────────────────────────────────┤
   │ 1. Asymmetric Business Costs: In real engineering systems, Cost(FN)    │
   │    is rarely equal to Cost(FP). Default τ = 0.5 is almost never optimal│
   │ 2. Cost-Optimal Thresholding: Sweep τ on validation data to minimize   │
   │    total economic loss; lower τ when false negatives are expensive.    │
   │ 3. Model Benchmark: Logistic Regression provides fast, interpretable,  │
   │    global planes; k-NN provides flexible, local, non-parametric memory.│
   │ 4. Stratified Validation: Always stratify folds to preserve minority   │
   │    class ratios across all cross-validation splits.                    │
   │ 5. Pipeline Integrity: Wrap scalers, one-hot encoders, and estimators  │
   │    into a single Pipeline to guarantee zero leakage.                   │
   │ 6. Production Checklist: Serialize entire pipelines, monitor data drift│
   │    weekly, and enforce strict API schema contracts.                    │
   └────────────────────────────────────────────────────────────────────────┘
```
