# CML 2 — Quizzes

### Quiz-1 — Encoding choice
You have a feature `shirt_size` with values S, M, L, XL that should respect order for a linear model. Best default?

**Answer:** Ordinal / ordered encoding (not unordered one-hot as the only story — one-hot is ok but loses order).  
**Trap:** Label-encoding *colors* the same way invents fake order.

### Quiz-2 — Scaling leakage
Which is correct?

A) `StandardScaler().fit(X)` then `train_test_split`  
B) `train_test_split` then `scaler.fit(X_train)` and `transform` both  
C) `scaler.fit(X_test)` to be fair to the test set  

**Answer: B**

### Quiz-3 — Imputation
Median imputation for a skewed numeric feature with outliers — why median over mean?

**Answer:** Median is robust to outliers; mean gets pulled and can distort the fill.

### Exit ticket (2 min — write on paper / chat)
1. One sentence: what is preprocessing leakage?  
2. Name two transforms that must be fit on train only.  
3. Nominal vs ordinal — one example each.

**Good enough answers:**  
1. Test info used while preparing train (inflated scores).  
2. Scaler, imputer, encoder (also feature selection, SMOTE, etc.).  
3. Nominal: city/color · Ordinal: size/rating.
