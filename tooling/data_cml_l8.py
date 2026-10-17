"""
Data definition for data_cml_l8:
"""

L8_DATA = {   'approval_status': 'approved',
    'key_takeaways': [   'Linear regression predicts continuous real values that exceed [0, 1] and is sensitive to '
                         'extreme outliers; Logistic Regression applies the Sigmoid function to map unbounded scores '
                         'to valid probabilities.',
                         'The decision boundary is the linear hyperplane where w^T x + w_0 = 0, corresponding to '
                         'probability P(y=1|x) = 0.5. Points deeper into positive space have higher confidence.',
                         'MSE with Sigmoid produces a non-convex loss surface with flat plateaus; Log-Loss (Binary '
                         'Cross-Entropy) guarantees a strictly convex bowl with a unique global minimum.',
                         'Accuracy is fatally deceptive on imbalanced datasets: a dummy model predicting majority '
                         'class on 99% non-fraud data achieves 99% accuracy while catching zero fraud.',
                         'Precision measures exactness (low false alarms); Recall measures completeness (low false '
                         'negatives). The F1-score balances them via the harmonic mean.',
                         'ROC-AUC measures ranking ability across all thresholds but is insensitive to false positives '
                         'when negatives dominate; Precision-Recall (PR-AUC) is the gold standard for rare positive '
                         'classes.',
                         'Remediating class imbalance requires class-weighted loss functions '
                         "(class_weight='balanced'), threshold shifting based on business costs, and leak-free "
                         'resampling inside CV folds.'],
    'last_updated': '2026-10-18T00:00:00Z',
    'learning_objectives': [   'Understand why linear regression fails for binary classification and formulate the '
                               'Sigmoid activation and Log-Odds representation.',
                               'Derive and interpret the Binary Cross-Entropy (Log-Loss) objective function and '
                               'explain why MSE is mathematically unsuitable.',
                               'Compute and diagnose all primary classification metrics (Accuracy, Precision, Recall, '
                               'Specificity, F1-Score) from a confusion matrix.',
                               'Analyze operating threshold trade-offs and evaluate models using ROC-AUC and '
                               'Precision-Recall (PR) curves.',
                               "Diagnose the 'Accuracy Trap' in severely imbalanced datasets and deploy industry "
                               'solutions (class weighting, threshold tuning, and PR-AUC optimization).'],
    'note_id': 'cml-t5-l08',
    'quiz': {   'questions': [   {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'Because sigma(z) = 1 / (1 + e^(-z)), as z becomes a large '
                                                    'negative number, e^(-z) becomes huge, making the denominator '
                                                    'massive and driving sigma(z) toward 0.',
                                     'id': 'q-cml-l08-01',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'The output becomes a negative number.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'The output approaches 0 asymptotically.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The output approaches 1.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The output becomes mathematically undefined.'}],
                                     'question': 'What happens to the output of the standard Sigmoid function sigma(z) '
                                                 'when its input z is a very large negative value (e.g., z = -25)?',
                                     'subtopic': 'Sigmoid Behavior',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'The score z represents the signed distance to the decision '
                                                    'surface. Since sigmoid is monotonically increasing, higher z '
                                                    'values directly translate to higher predicted probabilities '
                                                    'P(y=1|x).',
                                     'id': 'q-cml-l08-02',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'A point with z = -3.5 located far on the negative '
                                                                'side of the decision boundary.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'A point with z = +4.2 located deep on the positive '
                                                                'side of the decision boundary.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'A point resting directly on the line z = 0.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Both points have identical probabilities because '
                                                                'logistic regression is linear.'}],
                                     'question': 'In a 2D logistic regression classifier with linear score z = w1*x1 + '
                                                 'w2*x2 + w0, which observation will be assigned a higher predicted '
                                                 'probability of belonging to class 1?',
                                     'subtopic': 'Decision Boundary Geometry',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'When y = 0, loss = -ln(1 - p_hat) = -ln(1 - 0.01) = -ln(0.99) '
                                                    'approx 0.01. Because the model predicted a 99% probability of the '
                                                    'correct class 0, the error penalty is near zero.',
                                     'id': 'q-cml-l08-03',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Log-loss will be a massive positive penalty '
                                                                'approaching infinity.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Log-loss will be a very low value near zero, because '
                                                                "the model's prediction is confident and accurate."},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Log-loss will be negative.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Log-loss cannot be calculated when p_hat is less than '
                                                                '0.05.'}],
                                     'question': 'Suppose an observation has true ground-truth label y = 0, and the '
                                                 'model predicts a probability p_hat = 0.01 of belonging to class 1. '
                                                 'What is true about the resulting Log-Loss for this observation?',
                                     'subtopic': 'Log-Loss Intuition',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'easy',
                                     'explanation': 'Sigmoid maps the linear logit score into a bounded continuous '
                                                    'interval (0, 1), representing the conditional probability P(Y = 1 '
                                                    '| X) under the Bernoulli likelihood framework.',
                                     'id': 'q-cml-l08-04',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'As the estimated posterior class probability P(Y = 1 '
                                                                '| X).'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'As the regression residual error.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'As the feature importance ranking.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'As the condition number of the design matrix.'}],
                                     'question': 'In Logistic Regression, how is the numerical output of the Sigmoid '
                                                 'function formally interpreted?',
                                     'subtopic': 'Sigmoid Output Meaning',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'easy',
                                     'explanation': 'Precision = TP / (TP + FP). When False Positives carry severe '
                                                    'business costs (deleting important user emails), you must demand '
                                                    'high Precision to ensure that flagged emails are truly spam.',
                                     'id': 'q-cml-l08-05',
                                     'options': [   {'id': 'opt-1', 'is_correct': True, 'text': 'Precision'},
                                                    {'id': 'opt-2', 'is_correct': False, 'text': 'Recall'},
                                                    {'id': 'opt-3', 'is_correct': False, 'text': 'Mean Squared Error'},
                                                    {'id': 'opt-4', 'is_correct': False, 'text': 'R-squared'}],
                                     'question': 'You are designing an email spam classifier. If a legitimate email is '
                                                 'misclassified as spam and deleted (False Positive), the user may '
                                                 'miss a critical job offer. Which metric should you prioritize '
                                                 'maximizing?',
                                     'subtopic': 'Metric Selection: Spam Filter',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'Recall = TP / (TP + FN). When False Negatives are catastrophic '
                                                    '(failing to detect cancer), maximizing Recall ensures that '
                                                    'virtually all true positive patients are caught.',
                                     'id': 'q-cml-l08-06',
                                     'options': [   {'id': 'opt-1', 'is_correct': False, 'text': 'Specificity'},
                                                    {'id': 'opt-2', 'is_correct': True, 'text': 'Recall (Sensitivity)'},
                                                    {'id': 'opt-3', 'is_correct': False, 'text': 'Precision'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Mean Absolute Percentage Error'}],
                                     'question': 'In an emergency medical screening tool for malignant tumors, missing '
                                                 'an actual cancer patient (False Negative) can be fatal. Which metric '
                                                 'is the primary optimization objective?',
                                     'subtopic': 'Metric Selection: Disease Screening',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'The Accuracy Paradox: when positive cases are rare, a model that '
                                                    'never predicts the positive class still scores high accuracy '
                                                    'while catching zero fraud (TP = 0, Recall = 0).',
                                     'id': 'q-cml-l08-07',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Because its accuracy is too low for enterprise '
                                                                'deployment.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Because it fails to detect a single fraudulent '
                                                                'transaction (Recall = 0.0), completely failing the '
                                                                'business objective despite high accuracy.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Because credit card systems cannot compute '
                                                                'percentages with decimals.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Because dummy models consume excessive server RAM.'}],
                                     'question': 'A credit card transaction dataset contains 99.8% legitimate '
                                                 'transactions and 0.2% fraudulent transactions. A trivial dummy model '
                                                 "that classifies every transaction as 'Legitimate' achieves 99.8% "
                                                 'accuracy. Why is this model useless?',
                                     'subtopic': 'The Accuracy Paradox',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'An ROC-AUC of 0.5 corresponds to the diagonal baseline on an ROC '
                                                    "plot, meaning the model's ranking of positive vs. negative "
                                                    'instances is no better than random chance.',
                                     'id': 'q-cml-l08-08',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'The model has perfect discriminatory capability.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': "The model's predictions are no better than random "
                                                                'guessing (like flipping an unbiased coin).'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The model achieved 50% Precision and 50% Recall '
                                                                'simultaneously.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The model is overfitted to the training data.'}],
                                     'question': 'What does a model with an Area Under the ROC Curve (ROC-AUC) score '
                                                 'of exactly 0.50 indicate?',
                                     'subtopic': 'ROC-AUC Meaning',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'When squared loss is composed with the sigmoid function, the '
                                                    'resulting objective function is non-convex. The sigmoid '
                                                    'derivatives vanish at the extremes, causing gradient descent to '
                                                    'stall. Log-loss guarantees a strictly convex bowl with a unique '
                                                    'global optimum.',
                                     'id': 'q-cml-l08-09',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'MSE produces negative loss values when applied to '
                                                                'probabilities.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Combining MSE with the non-linear Sigmoid activation '
                                                                'creates a non-convex loss surface with flat plateaus '
                                                                'and local minima where gradients vanish.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'MSE cannot be differentiated in Python.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Log-loss is only used because it trains faster on '
                                                                'GPUs.'}],
                                     'question': 'Why is Mean Squared Error (MSE) rejected in favor of Binary '
                                                 'Cross-Entropy (Log-Loss) when optimizing Logistic Regression with '
                                                 'gradient descent?',
                                     'subtopic': 'Loss Function Convexity',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'Lowering the decision threshold makes the model classify samples '
                                                    'as positive more readily. This catches more true positives '
                                                    '(increasing Recall) at the expense of admitting more false '
                                                    'positives (lowering Precision).',
                                     'id': 'q-cml-l08-10',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Precision increases; Recall decreases.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Recall increases (fewer false negatives); Precision '
                                                                'typically decreases (more false alarms).'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Both Precision and Recall are guaranteed to reach '
                                                                '1.0.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Neither metric changes because model weights are '
                                                                'unchanged.'}],
                                     'question': 'In a binary classification model, what happens to Precision and '
                                                 'Recall when you lower the decision threshold from tau = 0.50 to tau '
                                                 '= 0.20?',
                                     'subtopic': 'Threshold Shifting Dynamics',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'Logistic regression is linear in the log-odds. A unit increase in '
                                                    'x_j changes log-odds by w_j, which multiplies the odds ratio by '
                                                    'e^(w_j). It does not change raw probability by a constant amount '
                                                    'because the sigmoid curve is non-linear.',
                                     'id': 'q-cml-l08-11',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'For each 1-unit increase in Credit Score, the '
                                                                'probability of default decreases by 40%.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'For each 1-unit increase in Credit Score, the '
                                                                'log-odds of default decrease by 0.40, meaning the '
                                                                'odds of default are multiplied by e^(-0.40) approx '
                                                                '0.67.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Credit score has a negative correlation with '
                                                                'accuracy.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The loan applicant has an absolute 40% chance of '
                                                                'approval.'}],
                                     'question': 'In a logistic regression model for loan default, the estimated '
                                                 "coefficient for 'Credit Score' is w_credit = -0.40. How is this "
                                                 'coefficient interpreted?',
                                     'subtopic': 'Coefficient Interpretation in Logistic Regression',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'When the negative class vastly outnumbers the positive class, a '
                                                    'model generating hundreds of false alarms still has a tiny False '
                                                    'Positive Rate because the denominator (TN + FP) is enormous. The '
                                                    'PR curve ignores TN and highlights the false alarm penalty '
                                                    'directly via Precision.',
                                     'id': 'q-cml-l08-12',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'The ROC curve is computationally slower to plot.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'The ROC x-axis (FPR = FP / (TN + FP)) is diluted by a '
                                                                'massive number of True Negatives, making the curve '
                                                                'look deceptively optimistic; the PR curve focuses '
                                                                'exclusively on the minority positive class.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'PR curves can only be used when sample size n < 100.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The ROC curve assumes all features follow a Gaussian '
                                                                'distribution.'}],
                                     'question': 'Why is the Precision-Recall (PR) curve strictly preferred over the '
                                                 'ROC curve when assessing model performance on severely imbalanced '
                                                 'datasets?',
                                     'subtopic': 'ROC vs PR Curve in Imbalance',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'medium',
                                     'explanation': 'Specificity is TN / (TN + FP), and False Positive Rate is FP / '
                                                    '(TN + FP). Therefore, FPR = (TN + FP - TN) / (TN + FP) = 1 - '
                                                    'Specificity.',
                                     'id': 'q-cml-l08-13',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'FPR = 1 - Specificity'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'FPR = Specificity / Precision'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'FPR = 1 + Specificity'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'FPR is the inverse of Recall.'}],
                                     'question': 'What is the mathematical relationship between Specificity (True '
                                                 'Negative Rate) and the False Positive Rate (FPR) plotted on the ROC '
                                                 'curve?',
                                     'subtopic': 'Specificity vs FPR',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': "The 'balanced' mode automatically adjusts weights inversely "
                                                    'proportional to class frequencies: w_j = n_samples / (n_classes * '
                                                    'np.bincount(y)). This scales up the loss incurred whenever the '
                                                    'model misclassifies a rare class instance.',
                                     'id': 'q-cml-l08-14',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'It physically duplicates minority class samples in '
                                                                'memory.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'It weights the loss contribution of each sample '
                                                                'inversely proportional to its class frequency, '
                                                                'penalizing errors on rare instances much more '
                                                                'heavily.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It deletes 50% of the majority class observations at '
                                                                'random.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It shifts the decision threshold from 0.5 to 0.0.'}],
                                     'question': "How does setting class_weight='balanced' in Scikit-Learn's "
                                                 'LogisticRegression address class imbalance during training?',
                                     'subtopic': 'Class Weighting Mechanism',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'The decision boundary occurs where P(Y=1|X) = 0.5, which is '
                                                    'exactly where the logit score z = w^T x + w0 = 0. In '
                                                    'd-dimensional feature space, this equation defines a flat linear '
                                                    'hyperplane.',
                                     'id': 'q-cml-l08-15',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'A circle or hypersphere.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'A linear hyperplane defined by w^T x + w0 = 0.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'A non-linear parabolic curve.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'A piecewise step function.'}],
                                     'question': 'In standard Logistic Regression without polynomial feature '
                                                 'expansions, what geometric shape does the decision boundary form in '
                                                 'feature space?',
                                     'subtopic': 'Decision Surface Geometry',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'The harmonic mean of two numbers is dominated by the smaller '
                                                    'value: 2*P*R / (P + R). If a model predicts positive for '
                                                    'everything, Recall = 1.0 but Precision might be 0.05. The '
                                                    'arithmetic mean would be ~0.525 (deceptive), whereas F1 will '
                                                    'correctly plummet to ~0.095.',
                                     'id': 'q-cml-l08-16',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'The harmonic mean is easier to calculate on '
                                                                'microprocessors.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'The harmonic mean punishes extreme trade-offs; if '
                                                                'either Precision or Recall collapses close to zero, '
                                                                'F1 plummets toward zero.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The arithmetic mean cannot handle floating point '
                                                                'numbers between 0 and 1.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Scikit-Learn requires all metrics to be calculated '
                                                                'using harmonic equations.'}],
                                     'question': 'Why is the F1-Score defined as the harmonic mean of Precision and '
                                                 'Recall rather than their arithmetic mean?',
                                     'subtopic': 'Harmonic Mean Intuition',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'Using the chain rule: dJ/dw = (dJ/dp_hat) * (dp_hat/dz) * '
                                                    '(dz/dw). Since dJ/dp_hat = -(y/p_hat - (1-y)/(1-p_hat)) and '
                                                    'dp_hat/dz = p_hat(1 - p_hat), the terms cancel out to yield '
                                                    '(p_hat - y). Multiplying by dz/dw = x gives (1/n) * X^T (p_hat - '
                                                    'y).',
                                     'id': 'q-cml-l08-17',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'grad_w J = (1/n) * X^T (p_hat - y)'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'grad_w J = (2/n) * (p_hat - y)^2'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'grad_w J = X^T X w - y'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'grad_w J = -ln(p_hat) * X'}],
                                     'question': 'What is the mathematical gradient of the Binary Cross-Entropy loss '
                                                 'function J(w) with respect to parameter vector w in Logistic '
                                                 'Regression?',
                                     'subtopic': 'Binary Cross-Entropy Gradient',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1', 'opt-2', 'opt-3', 'opt-4'],
                                     'difficulty': 'hard',
                                     'explanation': 'All four statements are foundational invariants. ROC-AUC random '
                                                    'baseline is always 0.50. PR-AUC random baseline is the minority '
                                                    'prevalence P / (P + N). The PR curve is non-monotonic because '
                                                    'moving the threshold can capture a false positive that drops '
                                                    'precision sharply.',
                                     'id': 'q-cml-l08-18',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'The ROC curve is monotonic with respect to threshold '
                                                                'changes (both TPR and FPR decrease or remain constant '
                                                                'as threshold increases).'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'The Precision-Recall curve can exhibit non-monotonic '
                                                                'jagged oscillations as the threshold shifts.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'A baseline random classifier has an expected ROC-AUC '
                                                                'of 0.50 regardless of class balance.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': True,
                                                        'text': 'A baseline random classifier has an expected PR-AUC '
                                                                'equal to the positive class prevalence (e.g., 0.02 '
                                                                'for a 2% positive rate).'}],
                                     'question': 'Which of the following statements represent true mathematical and '
                                                 'diagnostic invariants of ROC and Precision-Recall curves?',
                                     'subtopic': 'ROC vs PR Invariants',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'hard',
                                     'explanation': 'Threshold optimization in enterprise settings calculates Total '
                                                    'Cost = (FN * Cost_FN) + (FP * Cost_FP) across all candidate '
                                                    'thresholds on validation data to identify the cost-optimal '
                                                    'operating threshold.',
                                     'id': 'q-cml-l08-19',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Keep tau fixed at 0.50 because statistical models '
                                                                'cannot account for financial costs.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Compute the Expected Financial Cost matrix over a '
                                                                'sweep of candidate thresholds on validation data, and '
                                                                'select the tau that minimizes total business loss.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Always set tau = 1.0 to reject all loans.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Select the threshold that maximizes overall '
                                                                'accuracy.'}],
                                     'question': 'In loan default prediction, a False Negative (approving a borrower '
                                                 'who defaults) costs the bank 10,000 USD, while a False Positive '
                                                 '(denying a creditworthy borrower) costs 200 USD in lost interest. '
                                                 'How should the decision threshold tau be selected?',
                                     'subtopic': 'Cost-Sensitive Threshold Optimization',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'Softmax normalizes the exponentiated linear scores across all K '
                                                    'classes so that each class receives a probability in (0, 1) and '
                                                    'their sum across all K classes equals 1.0.',
                                     'id': 'q-cml-l08-20',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'By calculating the softmax probability P(Y=k|x) = '
                                                                'exp(w_k^T x) / sum_j exp(w_j^T x), ensuring the sum '
                                                                'of all K class probabilities equals exactly 1.0.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'By running K independent linear regressions and '
                                                                'taking the highest real value.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'By applying K-Means clustering to the predicted '
                                                                'labels.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'By multiplying individual binary sigmoid outputs '
                                                                'together.'}],
                                     'question': 'How does Multinomial Logistic Regression (Softmax Regression) '
                                                 'generalize the binary sigmoid function to K mutually exclusive '
                                                 'classes?',
                                     'subtopic': 'Multi-Class Extensions',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'If SMOTE runs globally before CV, synthetic minority instances in '
                                                    'the training folds will be interpolated from instances that '
                                                    'belong to the validation folds, directly leaking target and '
                                                    'feature distributions.',
                                     'id': 'q-cml-l08-21',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'SMOTE creates synthetic samples by interpolating '
                                                                'between nearest neighbors; if applied before '
                                                                'splitting, synthetic training points will be '
                                                                'generated from validation points, leaking holdout '
                                                                'data.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'SMOTE deletes rows from the test set.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Scikit-Learn prohibits running SMOTE on Python 3.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'SMOTE converts all numerical features into '
                                                                'categorical strings.'}],
                                     'question': 'Why is executing SMOTE (Synthetic Minority Over-sampling Technique) '
                                                 'on the entire dataset prior to K-Fold cross-validation a fatal data '
                                                 'leakage error?',
                                     'subtopic': 'SMOTE Leakage Prevention',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'Calibration refers to empirical alignment between predicted '
                                                    "probabilities and observed frequencies. A well-calibrated model's "
                                                    'confidence scores reflect real-world event frequencies.',
                                     'id': 'q-cml-l08-22',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'Among samples assigned a predicted probability p_hat '
                                                                'approx 0.80, approximately 80% of them actually '
                                                                'belong to the positive class in reality.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'The model achieves an AUC of 1.0.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The model has equal Precision and Recall.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'All feature weights w_j are normalized to sum to 1.'}],
                                     'question': 'What does it mean for a probabilistic classifier to be '
                                                 "'well-calibrated'?",
                                     'subtopic': 'Probability Calibration',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1', 'opt-2', 'opt-3'],
                                     'difficulty': 'hard',
                                     'explanation': 'Options 1, 2, and 3 are correct. Option 4 is false: Logistic '
                                                    'Regression makes no assumptions regarding the distributional form '
                                                    'of input features X (they can be binary, continuous, skewed, or '
                                                    'multimodal).',
                                     'id': 'q-cml-l08-23',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'It belongs to the Generalized Linear Model (GLM) '
                                                                'family with a logit link function and binomial error '
                                                                'distribution.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'It can be regularized using L1 (Lasso) or L2 (Ridge) '
                                                                'penalties by adding them to the Log-Loss objective.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'It can handle non-linear decision boundaries if '
                                                                'non-linear basis expansions (polynomial or '
                                                                'interaction terms) are included in feature matrix X.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It requires the input features X to follow a '
                                                                'multivariate normal distribution.'}],
                                     'question': 'Which of the following statements are mathematically true regarding '
                                                 'Logistic Regression?',
                                     'subtopic': 'Logistic Regression Invariants',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'When classes are perfectly separable, the log-loss can be made '
                                                    'arbitrarily close to 0 by scaling the weight vector ||w|| -> inf '
                                                    '(making the sigmoid step infinitely steep). Adding an L2 penalty '
                                                    '(e.g. C = 1.0 in Scikit-Learn) bounds weight growth.',
                                     'id': 'q-cml-l08-24',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'The optimization algorithm fails to converge because '
                                                                'the weights w grow toward positive and negative '
                                                                'infinity to drive probabilities to exact 0 and 1; L2 '
                                                                'regularization is required to stabilize weights.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'The model achieves an optimal solution in 1 '
                                                                'iteration.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The Hessian matrix becomes non-invertible.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The loss function becomes strictly zero for all '
                                                                'possible weights.'}],
                                     'question': 'What happens if a dataset is perfectly linearly separable (classes '
                                                 'can be divided with 100% accuracy by a hyperplane) and trained with '
                                                 'unregularized Logistic Regression?',
                                     'subtopic': 'Separability Hazard',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'MCC = (TP*TN - FP*FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN)). '
                                                    'Unlike F1 (which completely ignores True Negatives) or Accuracy '
                                                    '(which is bloated by TNs), MCC provides an honest Pearson '
                                                    'correlation between predictions and true labels across all four '
                                                    'quadrants.',
                                     'id': 'q-cml-l08-25',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'It takes into account all four quadrants of the '
                                                                'confusion matrix (TP, TN, FP, FN) in both the '
                                                                'numerator and denominator, producing a score in [-1, '
                                                                '+1] where 0 is random guessing.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'It is calculated only on the training set.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It eliminates the need for computing probabilities.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It is always strictly equal to the ROC-AUC score.'}],
                                     'question': 'Why is the Matthews Correlation Coefficient (MCC) considered '
                                                 'superior to Accuracy and F1-score when assessing binary classifiers '
                                                 'on heavily imbalanced data?',
                                     'subtopic': 'Matthews Correlation Coefficient',
                                     'type': 'single_choice'}]},
    'schema_version': 1,
    'sections': [   {   'body': '### 1.1 The Telco Churn Case Study: The Business Imperative of Binary Classification\n'
                                '\n'
                                'Consider a major telecom provider (such as Bharti Airtel or AT&T).\n'
                                'Every month, the company tracks millions of active mobile subscribers. A fundamental '
                                'business challenge is **Customer Churn**:\n'
                                '- $y = 0$: **Retained Customer** (Continues using the service, paying monthly '
                                'bills).\n'
                                '- $y = 1$: **Churned Customer** (Ported their SIM to a competitor, canceled '
                                'subscription, or ceased recharges).\n'
                                '\n'
                                '```\n'
                                'Customer Churn Timeline:\n'
                                '   Month t-1: Active Subscriber ──► Month t: Evaluates Competitor Offers ──► Month '
                                't+1: Decision\n'
                                '                                            │                                        '
                                '│\n'
                                '                                            ├── Network issues in local area?       '
                                '├── Stays (y = 0)\n'
                                '                                            ├── Better data tariff elsewhere?       '
                                '└── Churns (y = 1)\n'
                                '                                            └── High volume of support calls?\n'
                                '```\n'
                                '\n'
                                '#### Why Early Predictive Identification is Worth Millions\n'
                                'Acquiring a new customer in the telecom sector costs between **5 to 25 times more** '
                                'than retaining an existing customer.\n'
                                'If the company can predict that high-value subscriber $U$ has an $85\\%$ probability '
                                'of churning next month:\n'
                                '1. **Targeted Incentives**: The business can proactively offer a 20 USD bill credit, '
                                '50% recharge discount, or bonus 5G data pack.\n'
                                '2. **Infrastructure Root-Cause Resolution**: If multiple customers churning in an IT '
                                'corridor (e.g., Electronic City) cite call drops, network engineers can deploy '
                                'localized micro-cell towers before thousands more churn.\n'
                                '3. **Optimized Retention Spend**: Offering discounts to customers who were never '
                                'going to leave wastes valuable marketing budget. Predicting accurate probabilities '
                                'ensures retention capital is deployed only where it moves the needle.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.2 Why Linear Regression Fails Catastrophically for Classification\n'
                                '\n'
                                'A natural first instinct of a student might be: *"We already know Ordinary Least '
                                'Squares Linear Regression ($\\hat{y} = \\mathbf{w}^T \\mathbf{x} + w_0$). Can we not '
                                'simply train a line on the binary targets $\\{0, 1\\}$ and predict Class 1 whenever '
                                '$\\hat{y} \\ge 0.5$?"*\n'
                                '\n'
                                'The answer is an emphatic **NO**. Linear regression fails for binary classification '
                                'due to two fatal geometric and statistical flaws:\n'
                                '\n'
                                '```\n'
                                'Why Linear Regression Fails for Binary Targets:\n'
                                '       y (Target)\n'
                                '         ^\n'
                                '       1 |           *  *  *  *  *  *  *  * (Class 1)                 * (Extreme '
                                'Outlier x = 50)\n'
                                '         |                                                           /\n'
                                '         |                                                          /\n'
                                '     0.5 |------------------ Threshold '
                                '----------------------------/-----------------\n'
                                '         |                                                        /\n'
                                '         |                                                       / (Fitted Line '
                                'shifted right!)\n'
                                '       0 |   *  *  *  *  *  * (Class 0)                         /\n'
                                '         +----------------------------------------------------> x\n'
                                '                    Unbounded: y_hat can be -0.4 or +2.8!\n'
                                '```\n'
                                '\n'
                                '#### Flaw 1: Nonsensical, Unbounded Output Ranges\n'
                                'Ordinary Least Squares is designed for continuous unbounded target spaces '
                                '$\\mathcal{Y} = (-\\infty, +\\infty)$.\n'
                                'For extreme values of feature $x$ (e.g., very high monthly usage), linear regression '
                                'outputs values like $\\hat{y} = 2.45$ or $\\hat{y} = -0.38$.\n'
                                'In classification, we require outputs to represent **posterior probabilities** $P(Y = '
                                '1 \\mid \\mathbf{x})$.\n'
                                'A probability of $-0.38$ or $+2.45$ violates the fundamental Kolmogorov axioms of '
                                'probability ($0 \\le P(E) \\le 1$) and cannot be interpreted as risk or confidence.\n'
                                '\n'
                                '#### Flaw 2: The Outlier Sensitivity Disaster (The Tilting Boundary)\n'
                                'In Ordinary Least Squares, the loss function minimizes squared vertical residuals '
                                '$\\sum (y^{(i)} - \\hat{y}^{(i)})^2$.\n'
                                'Suppose we have well-separated clusters for Class 0 ($x \\in [1, 5]$) and Class 1 ($x '
                                '\\in [7, 12]$). The linear threshold $\\hat{y} = 0.5$ falls cleanly at $x = 6.0$.\n'
                                'Now introduce a single extreme outlier: a heavy enterprise customer at $x = 50$ who '
                                'also belongs to Class 1 ($y = 1$).\n'
                                '- Because OLS squares the error $(1 - (w \\cdot 50 + w_0))^2$, this distant point '
                                'exerts an enormous lever-arm torque on the regression line.\n'
                                '- The fitted line pivots and flattens out to reduce the squared residual on this '
                                'distant point.\n'
                                '- As the line pivots, the point where it crosses $\\hat{y} = 0.5$ **shifts '
                                'drastically to the right** (e.g., from $x = 6.0$ to $x = 8.5$).\n'
                                '- Consequently, dozens of genuine Class 1 customers between $x = 7.0$ and $x = 8.5$ '
                                'are now falsely classified as Class 0!\n'
                                '- *Irony*: An observation that was **extremely positive** caused other positive '
                                'observations to be misclassified as negative!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.3 Geometric Foundations: Line of Best Fit vs. Hyperplane of Separation\n'
                                '\n'
                                '| Architectural Dimension | Linear Regression | Logistic Regression |\n'
                                '| :--- | :--- | :--- |\n'
                                '| **Fundamental Nature** | Function Approximation / Curve Fitting | Pattern '
                                'Classification / Space Partitioning |\n'
                                '| **Geometric Objective** | Finds the **line of best fit** that passes through the '
                                'spatial center of data points. | Finds the **decision hyperplane** that separates '
                                'points of Class 0 from Class 1. |\n'
                                '| **Target Variable Space** | Continuous scalar $y \\in \\mathbb{R}$ | Discrete '
                                'categorical class label $y \\in \\{0, 1\\}$ |\n'
                                '| **Hypothesis Output** | Real-valued numerical estimate $\\hat{y} \\in (-\\infty, '
                                '+\\infty)$ | Calibrated probability estimate $\\hat{p} = P(Y=1 \\mid \\mathbf{x}) '
                                '\\in (0, 1)$ |\n'
                                '| **Loss Function** | Convex Mean Squared Error (MSE) | Convex Binary Cross-Entropy '
                                '(Log-Loss / NLL) |\n'
                                '| **Response to Outliers** | Highly vulnerable: line pivots to chase distant points. '
                                '| Exceptionally robust: points far from boundary saturate at $p \\approx 0$ or $1$. |',
                        'citations': [   'Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of '
                                         'Statistical Learning (2nd ed.). Springer, Chapter 4.',
                                         'James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). An Introduction '
                                         'to Statistical Learning. Springer, Chapter 4.'],
                        'heading': '1. Classification Foundations: Why Linear Regression Fails for Binary Outcomes',
                        'section_id': 'cml-l08-sec01'},
                    {   'body': '### 2.1 The Two-Step Prediction Pipeline\n'
                                '\n'
                                'To resolve the unbounded range problem, Logistic Regression constructs a two-stage '
                                'hypothesis:\n'
                                '1. First, compute a standard linear combination of the input features (the **Logit / '
                                'Linear Score** $z$).\n'
                                '2. Second, pass this continuous score $z$ through a non-linear squashing function '
                                'that maps $(-\\infty, +\\infty)$ strictly into the open interval $(0, 1)$.\n'
                                '\n'
                                '```\n'
                                'The Logistic Regression Feedforward Flow:\n'
                                '   Features x = [x1, x2, ..., xd]^T\n'
                                '            │\n'
                                '            ▼\n'
                                '   ┌────────────────────────────────────────────────────────┐\n'
                                '   │ Step 1: Linear Combination (Dot Product + Bias)        │\n'
                                '   │ z = w^T x + w0 = w0 + w1*x1 + w2*x2 + ... + wd*xd      │\n'
                                '   │ Output Range: z in (-inf, +inf)                        │\n'
                                '   └────────────────────────────────────────────────────────┘\n'
                                '            │\n'
                                '            ▼\n'
                                '   ┌────────────────────────────────────────────────────────┐\n'
                                '   │ Step 2: Non-Linear Activation (Standard Sigmoid / GLM) │\n'
                                '   │ p_hat = sigma(z) = 1 / (1 + e^(-z))                    │\n'
                                '   │ Output Range: p_hat in (0, 1)                          │\n'
                                '   └────────────────────────────────────────────────────────┘\n'
                                '            │\n'
                                '            ▼\n'
                                '   Predicted Class Posterior Probability: P(Y = 1 | x)\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.2 The Sigmoid (Logistic) Function & Its Mathematical Elegance\n'
                                '\n'
                                'The squashing function used is the **Standard Sigmoid Function** $\\sigma(z)$:\n'
                                '\n'
                                '$$\\sigma(z) = \\frac{1}{1 + e^{-z}} = \\frac{e^z}{1 + e^z}$$\n'
                                '\n'
                                '```\n'
                                'The S-Shaped Sigmoid Curve:\n'
                                '       sigma(z) ^\n'
                                '            1.0 |                              .-------- (Asymptote at 1.0)\n'
                                "                |                           .-'\n"
                                "            0.5 |------------------------.-' (z = 0, p = 0.5)\n"
                                "                |                     .-'\n"
                                "            0.0 | --------'                                (Asymptote at 0.0)\n"
                                '                +-------------------------+-------------------------> z\n'
                                '                                         0\n'
                                '```\n'
                                '\n'
                                '#### Core Mathematical Properties:\n'
                                '1. **Strictly Bounded**: For all $z \\in \\mathbb{R}$, $0 < \\sigma(z) < 1$. It never '
                                'reaches 0 or 1 at any finite $z$, acting as asymptotic probability bounds.\n'
                                '2. **Symmetry About the Origin**:\n'
                                '   $$\\sigma(-z) = \\frac{1}{1 + e^z} = \\frac{1 + e^z - e^z}{1 + e^z} = 1 - '
                                '\\frac{e^z}{1 + e^z} = 1 - \\sigma(z)$$\n'
                                '3. **Midpoint Anchor at $z = 0$**:\n'
                                '   $$\\sigma(0) = \\frac{1}{1 + e^0} = \\frac{1}{1 + 1} = \\mathbf{0.5}$$\n'
                                '4. **Asymptotic Limits**:\n'
                                '   $$\\lim_{z \\to +\\infty} \\sigma(z) = 1.0, \\qquad \\lim_{z \\to -\\infty} '
                                '\\sigma(z) = 0.0$$\n'
                                '5. **The Magical Derivative Property**:\n'
                                '   The derivative of $\\sigma(z)$ with respect to $z$ can be written entirely in '
                                'terms of its own output:\n'
                                '   $$\\frac{d\\sigma}{dz} = \\frac{d}{dz}(1 + e^{-z})^{-1} = -(1 + e^{-z})^{-2} '
                                '\\cdot (-e^{-z}) = \\frac{1}{1 + e^{-z}} \\cdot \\frac{e^{-z}}{1 + e^{-z}} = '
                                '\\sigma(z) \\cdot (1 - \\sigma(z))$$\n'
                                '   This property allows neural networks and gradient descent optimizers to compute '
                                'derivatives with extreme computational efficiency.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.3 Odds and Log-Odds (The Logit Transformation)\n'
                                '\n'
                                'To understand where the Sigmoid comes from, we view Logistic Regression through the '
                                'lens of **Odds**:\n'
                                '\n'
                                '$$\\text{Odds} = \\frac{P(Y = 1 \\mid \\mathbf{x})}{P(Y = 0 \\mid \\mathbf{x})} = '
                                '\\frac{p}{1 - p} \\in [0, \\infty)$$\n'
                                '\n'
                                '- If the probability of rain is $p = 0.80$, the odds are $\\frac{0.80}{0.20} = 4.0$ '
                                '(spoken as "4 to 1 in favor of rain").\n'
                                '- If the probability is $p = 0.50$, the odds are $\\frac{0.50}{0.50} = 1.0$ ("even '
                                'odds").\n'
                                '- If the probability is $p = 0.10$, the odds are $\\frac{0.10}{0.90} \\approx 0.111$ '
                                '("1 to 9 against rain").\n'
                                '\n'
                                'While probability $p$ is constrained to $[0, 1]$, the Odds ratio ranges from $0$ to '
                                '$+\\infty$.\n'
                                'Taking the natural logarithm of the odds maps it across the entire real number line '
                                '$(-\\infty, +\\infty)$:\n'
                                '\n'
                                '$$\\text{Logit}(p) = \\ln(\\text{Odds}) = \\ln\\left(\\frac{p}{1 - p}\\right) \\in '
                                '(-\\infty, +\\infty)$$\n'
                                '\n'
                                'In Logistic Regression, we model this **Log-Odds (Logit)** as a linear function of '
                                'features:\n'
                                '\n'
                                '$$\\ln\\left(\\frac{p}{1 - p}\\right) = \\mathbf{w}^T \\mathbf{x} + w_0$$\n'
                                '\n'
                                'Solving for probability $p$ by exponentiating both sides:\n'
                                '$$\\frac{p}{1 - p} = e^{\\mathbf{w}^T \\mathbf{x} + w_0} \\implies p = '
                                'e^{\\mathbf{w}^T \\mathbf{x} + w_0}(1 - p) \\implies p(1 + e^{\\mathbf{w}^T '
                                '\\mathbf{x} + w_0}) = e^{\\mathbf{w}^T \\mathbf{x} + w_0}$$\n'
                                '$$p = \\frac{e^{\\mathbf{w}^T \\mathbf{x} + w_0}}{1 + e^{\\mathbf{w}^T \\mathbf{x} + '
                                'w_0}} = \\frac{1}{1 + e^{-(\\mathbf{w}^T \\mathbf{x} + w_0)}} = \\sigma(\\mathbf{w}^T '
                                '\\mathbf{x} + w_0)$$\n'
                                '\n'
                                '> **The Fundamental Definition**:\n'
                                '> **Logistic Regression is a linear model for the log-odds of the positive class.**\n'
                                '> When feature $x_j$ increases by $1$ unit (holding all other features fixed), the '
                                'log-odds increase by $w_j$, and the **odds are multiplied by $e^{w_j}$**.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.4 The Decision Boundary Geometry & Confidence\n'
                                '\n'
                                'When we apply the standard classification threshold $\\tau = 0.50$:\n'
                                '$$\\hat{y} = 1 \\iff \\hat{p} \\ge 0.50 \\iff \\sigma(z) \\ge 0.50 \\iff z \\ge 0$$\n'
                                '$$\\hat{y} = 1 \\iff \\mathbf{w}^T \\mathbf{x} + w_0 \\ge 0$$\n'
                                '\n'
                                'The **Decision Boundary** is the exact set of points where the model is maximally '
                                'uncertain ($\\hat{p} = 0.50$):\n'
                                '\n'
                                '$$\\mathbf{w}^T \\mathbf{x} + w_0 = 0$$\n'
                                '\n'
                                '```\n'
                                'Decision Boundary Geometry in 2D Feature Space:\n'
                                '         x2 ^\n'
                                '            │       + (Positive class, p_hat > 0.5)\n'
                                '            │      +      +\n'
                                '            │         +   * (Perpendicular distance d indicates high confidence!)\n'
                                '            │            /\n'
                                '            │           /  Decision Boundary: w1*x1 + w2*x2 + w0 = 0\n'
                                '            │          /   (On the line: p_hat = 0.50)\n'
                                '            │         /\n'
                                '            │  o     /       o (Negative class, p_hat < 0.5)\n'
                                '            │    o  /    o\n'
                                '            │      /  o\n'
                                '            +─────/─────────────────────────► x1\n'
                                '```\n'
                                '\n'
                                '1. The decision boundary is an **affine hyperplane** of dimension $d-1$ in '
                                '$d$-dimensional space (a line in 2D, a flat plane in 3D).\n'
                                '2. The parameter vector $\\mathbf{w}$ is the **normal vector orthogonal** to the '
                                'decision boundary, pointing in the direction of increasing Class 1 probability.\n'
                                '3. The signed perpendicular distance from any observation $\\mathbf{x}^{(i)}$ to the '
                                'boundary is:\n'
                                '   $$\\text{dist}(\\mathbf{x}^{(i)}) = \\frac{\\mathbf{w}^T \\mathbf{x}^{(i)} + '
                                'w_0}{\\|\\mathbf{w}\\|_2}$$\n'
                                '4. Points located far from the boundary have large $|z|$, producing $\\hat{p} '
                                '\\approx 0.999$ or $\\hat{p} \\approx 0.001$ (**High Confidence**).\n'
                                '5. Points hovering right beside the boundary have $z \\approx 0$, producing $\\hat{p} '
                                '\\approx 0.51$ (**Low Confidence / Hesitant**).',
                        'citations': [   'Cox, D. R. (1958). The regression analysis of binary sequences. Journal of '
                                         'the Royal Statistical Society: Series B, 20(2), 215-232.',
                                         'Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer, '
                                         'Chapter 4.'],
                        'heading': '2. The Sigmoid Activation, Odds & The Logit Function',
                        'section_id': 'cml-l08-sec02'},
                    {   'body': '### 3.1 Why Mean Squared Error (MSE) Breaks with Sigmoid\n'
                                '\n'
                                'If we attempted to train Logistic Regression using MSE:\n'
                                '\n'
                                '$$J_{\\text{MSE}}(\\mathbf{w}) = \\frac{1}{n} \\sum_{i=1}^n \\left(y^{(i)} - '
                                '\\sigma(\\mathbf{w}^T \\mathbf{x}^{(i)})\\right)^2$$\n'
                                '\n'
                                'Because $\\sigma(z)$ is non-linear and saturates at both ends, the resulting loss '
                                'surface $J_{\\text{MSE}}$ is **non-convex**. It possesses severe local plateaus where '
                                "gradients vanish ($\\sigma'(z) \\to 0$), causing gradient descent to get trapped in "
                                'terrible sub-optimal states.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.2 Derivation of Log-Loss via Maximum Likelihood Estimation\n'
                                '\n'
                                'For a single binary observation $(x^{(i)}, y^{(i)})$ where $y^{(i)} \\in \\{0, 1\\}$, '
                                'the probability of observing the label is modeled as a Bernoulli random variable:\n'
                                '\n'
                                '$$P(Y = y^{(i)} \\mid \\mathbf{x}^{(i)}) = (\\hat{p}_i)^{y^{(i)}} (1 - \\hat{p}_i)^{1 '
                                '- y^{(i)}}$$\n'
                                '\n'
                                'Where $\\hat{p}_i = \\sigma(\\mathbf{w}^T \\mathbf{x}^{(i)})$.\n'
                                '\n'
                                'Assuming independent observations, the likelihood of the entire training dataset is '
                                'the product of individual probabilities:\n'
                                '\n'
                                '$$L(\\mathbf{w}) = \\prod_{i=1}^n (\\hat{p}_i)^{y^{(i)}} (1 - \\hat{p}_i)^{1 - '
                                'y^{(i)}}$$\n'
                                '\n'
                                'To maximize this likelihood without multiplying tiny probabilities (which causes '
                                'numerical underflow), we take the natural logarithm to get the log-likelihood:\n'
                                '\n'
                                '$$\\ln L(\\mathbf{w}) = \\sum_{i=1}^n \\left[ y^{(i)} \\ln(\\hat{p}_i) + (1 - '
                                'y^{(i)}) \\ln(1 - \\hat{p}_i) \\right]$$\n'
                                '\n'
                                'To convert this maximization into a standard loss minimization, we negate it and '
                                'divide by $n$. This defines **Binary Cross-Entropy (Log-Loss)**:\n'
                                '\n'
                                '$$J(\\mathbf{w}) = -\\frac{1}{n} \\sum_{i=1}^n \\left[ y^{(i)} \\ln(\\hat{p}_i) + (1 '
                                '- y^{(i)}) \\ln(1 - \\hat{p}_i) \\right]$$\n'
                                '\n'
                                '```\n'
                                'Behavior of Log-Loss Penalty:\n'
                                '   When True Label y = 1:                    When True Label y = 0:\n'
                                '   Loss = -ln(p_hat)                         Loss = -ln(1 - p_hat)\n'
                                '      Loss ^                                    Loss ^\n'
                                '           | \\                                       |          /\n'
                                '           |  \\                                      |         /\n'
                                '           |   \\                                     |        /\n'
                                "           |    '--.                                 |   .--'\n"
                                '         0 +---------> p_hat                       0 +---------> p_hat\n'
                                '           0        1                                0        1\n'
                                '       p_hat -> 1: Loss -> 0                     p_hat -> 0: Loss -> 0\n'
                                '       p_hat -> 0: Loss -> +inf!                 p_hat -> 1: Loss -> +inf!\n'
                                '```\n'
                                '\n'
                                '> **The Penalty Intuition**:\n'
                                '> - If true label is $y = 1$ and model predicts $\\hat{p} = 0.99$, Loss $= '
                                '-\\ln(0.99) \\approx 0.01$ (Virtually zero penalty).\n'
                                '> - If true label is $y = 1$ and model confidently predicts $\\hat{p} = 0.001$, Loss '
                                '$= -\\ln(0.001) \\approx 6.91$ (Severe penalty tending to infinity).\n'
                                '\n'
                                '### 3.3 Concrete Hand-Calculated Log-Loss Walkthrough\n'
                                '\n'
                                'Let us evaluate the Log-Loss across 5 representative patient predictions to see how '
                                'confident mistakes are penalized:\n'
                                '\n'
                                '| Patient ($i$) | True Label ($y_i$) | Predicted Probability ($\\hat{p}_i$) | Loss '
                                'Formula Applied | Loss $\\ell_i$ | Diagnostic Behavior |\n'
                                '| :--- | :--- | :--- | :--- | :--- | :--- |\n'
                                '| **Patient 1** | $y = 1$ | $\\hat{p} = 0.90$ | $-\\ln(0.90)$ | **$0.105$** | '
                                'Confident correct detection (tiny loss). |\n'
                                '| **Patient 2** | $y = 0$ | $\\hat{p} = 0.10$ | $-\\ln(1 - 0.10) = -\\ln(0.90)$ | '
                                '**$0.105$** | Confident correct rejection (tiny loss). |\n'
                                '| **Patient 3** | $y = 1$ | $\\hat{p} = 0.60$ | $-\\ln(0.60)$ | **$0.511$** | '
                                'Hesitant correct detection (moderate loss). |\n'
                                '| **Patient 4** | $y = 0$ | $\\hat{p} = 0.40$ | $-\\ln(1 - 0.40) = -\\ln(0.60)$ | '
                                '**$0.511$** | Hesitant correct rejection (moderate loss). |\n'
                                '| **Patient 5** | $y = 1$ | $\\hat{p} = 0.05$ | $-\\ln(0.05)$ | **$2.996$** | '
                                '**Confident Blunder!** (Severe exponential blowup). |\n'
                                '\n'
                                '#### Dataset Average Log-Loss:\n'
                                '$$J(\\mathbf{w}) = \\frac{1}{5}(0.105 + 0.105 + 0.511 + 0.511 + 2.996) = '
                                '\\frac{4.228}{5} = \\mathbf{0.846}$$\n'
                                '\n'
                                'Notice that Patient 5 accounts for over **70% of the entire dataset loss** ($2.996 / '
                                '4.228 = 70.9\\%$)! Log-Loss relentlessly forces optimization away from confident '
                                'false assurances.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.4 The Gradient Update Rule\n'
                                '\n'
                                'Taking the derivative of the Log-Loss with respect to weight vector $\\mathbf{w}$ '
                                'yields an extraordinarily elegant result:\n'
                                '\n'
                                '$$\\nabla_{\\mathbf{w}} J(\\mathbf{w}) = \\frac{1}{n} \\mathbf{X}^T '
                                '(\\hat{\\mathbf{p}} - \\mathbf{y})$$\n'
                                '\n'
                                '> **The Mathematical Parallel**:\n'
                                '> Notice that the gradient of Logistic Regression has the **exact same functional '
                                'form** as the gradient of Ordinary Least Squares Linear Regression! The only '
                                'difference is that $\\hat{\\mathbf{p}} = \\sigma(\\mathbf{Xw})$ instead of '
                                '$\\hat{\\mathbf{y}} = \\mathbf{Xw}$.',
                        'citations': [   'Good, I. J. (1952). Rational decisions. Journal of the Royal Statistical '
                                         'Society: Series B, 14(1), 107-114.',
                                         'McCullagh, P., & Nelder, J. A. (1989). Generalized Linear Models (2nd ed.). '
                                         'Chapman and Hall/CRC.'],
                        'heading': '3. The Optimization Objective: Binary Cross-Entropy (Log-Loss)',
                        'section_id': 'cml-l08-sec03'},
                    {   'body': '### 4.1 The Confusion Matrix Anatomy\n'
                                '\n'
                                'To convert continuous probabilities $\\hat{p} \\in (0, 1)$ into actionable '
                                'operational decisions, we compare them against a decision threshold $\\tau \\in [0, '
                                '1]$ (default $\\tau = 0.50$):\n'
                                '\n'
                                '$$\\hat{y} = \\begin{cases} 1 & \\text{if } \\hat{p} \\ge \\tau \\\\ 0 & \\text{if } '
                                '\\hat{p} < \\tau \\end{cases}$$\n'
                                '\n'
                                'Every single prediction falls into one of four mutually exclusive quadrants in the '
                                '**Confusion Matrix**:\n'
                                '\n'
                                '```\n'
                                'The 2x2 Confusion Matrix:\n'
                                '                         Predicted Negative (0)         Predicted Positive (1)\n'
                                '                   ┌──────────────────────────────┬──────────────────────────────┐\n'
                                '    Actual         │      TRUE NEGATIVE (TN)      │     FALSE POSITIVE (FP)      │\n'
                                '    Negative (0)   │   Healthy patient cleared.   │   Healthy patient panicked.  │\n'
                                '                   │   Correct Rejection.         │   Type I Error (False Alarm) │\n'
                                '                   ├──────────────────────────────┼──────────────────────────────┤\n'
                                '    Actual         │     FALSE NEGATIVE (FN)      │      TRUE POSITIVE (TP)      │\n'
                                '    Positive (1)   │   Sick patient sent home!    │   Sick patient diagnosed.    │\n'
                                '                   │   Type II Error (Missed Hit) │   Correct Hit.               │\n'
                                '                   └──────────────────────────────┴──────────────────────────────┘\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.2 Comprehensive Metric Formulas & Hand-Calculated 1,000-Patient Example\n'
                                '\n'
                                'Suppose an oncology clinic evaluates a diagnostic AI model on $N = 1,000$ patients:\n'
                                '- Actual Sick Patients ($y = 1$): $100$\n'
                                '- Actual Healthy Patients ($y = 0$): $900$\n'
                                '\n'
                                'The model produces the following Confusion Matrix:\n'
                                '- $\\text{TP} = 80$ (Caught 80 sick patients)\n'
                                '- $\\text{FN} = 20$ (Missed 20 sick patients)\n'
                                '- $\\text{FP} = 50$ (Falsely flagged 50 healthy people)\n'
                                '- $\\text{TN} = 850$ (Correctly cleared 850 healthy people)\n'
                                '\n'
                                '#### 1. Accuracy\n'
                                '$$\\text{Accuracy} = \\frac{TP + TN}{TP + TN + FP + FN} = \\frac{80 + 850}{1000} = '
                                '\\frac{930}{1000} = \\mathbf{93.0\\%}$$\n'
                                '- *Limitation*: If a doctor simply guessed "Healthy" for all 1,000 patients without '
                                'even seeing them, they would achieve $90.0\\%$ accuracy! Accuracy masks poor minority '
                                'detection.\n'
                                '\n'
                                '#### 2. Precision (Positive Predictive Value)\n'
                                '$$\\text{Precision} = \\frac{TP}{TP + FP} = \\frac{80}{80 + 50} = \\frac{80}{130} '
                                '\\approx \\mathbf{61.5\\%}$$\n'
                                '- *Meaning*: When the model fires an alarm and says "Patient is Positive", there is a '
                                '$61.5\\%$ chance they actually have the disease. (The other $38.5\\%$ are false '
                                'alarms).\n'
                                '\n'
                                '#### 3. Recall (Sensitivity / True Positive Rate / Hit Rate)\n'
                                '$$\\text{Recall} = \\frac{TP}{TP + FN} = \\frac{80}{80 + 20} = \\frac{80}{100} = '
                                '\\mathbf{80.0\\%}$$\n'
                                '- *Meaning*: Out of all people who genuinely have the disease in reality, the model '
                                'successfully catches $80\\%$. (It missed $20\\%$ of cancer patients!).\n'
                                '\n'
                                '#### 4. Specificity (True Negative Rate / Selectivity)\n'
                                '$$\\text{Specificity} = \\frac{TN}{TN + FP} = \\frac{850}{850 + 50} = '
                                '\\frac{850}{900} \\approx \\mathbf{94.4\\%}$$\n'
                                '- *Meaning*: Out of all healthy people, $94.4\\%$ were correctly cleared.\n'
                                '- *False Positive Rate (Fall-out)*: $\\text{FPR} = 1 - \\text{Specificity} = '
                                '\\frac{50}{900} \\approx \\mathbf{5.6\\%}$.\n'
                                '\n'
                                '#### 5. F1-Score (The Harmonic Mean)\n'
                                '$$\\text{F}_1 = 2 \\cdot \\frac{\\text{Precision} \\cdot '
                                '\\text{Recall}}{\\text{Precision} + \\text{Recall}} = 2 \\cdot \\frac{0.6154 \\cdot '
                                '0.8000}{0.6154 + 0.8000} = \\frac{0.9846}{1.4154} \\approx \\mathbf{0.696}$$\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.3 Type I vs. Type II Errors: The Real-World Asymmetry\n'
                                '\n'
                                'In pure mathematics, all errors have equal cost. In the real world, the costs of Type '
                                'I and Type II errors are wildly asymmetric:\n'
                                '\n'
                                '| Industry Domain | Positive Event ($y=1$) | Type I Error (False Positive) | Type II '
                                'Error (False Negative) | Critical Priority |\n'
                                '| :--- | :--- | :--- | :--- | :--- |\n'
                                '| **Oncology Diagnosis** | Malignant Tumor Present | Healthy patient undergoes '
                                'follow-up biopsy. Stressful, but non-fatal. | Cancer missed; patient sent home '
                                'without treatment. **Fatal outcome!** | **MAXIMIZE RECALL** (Drive False Negatives to '
                                '0). |\n'
                                '| **Email Spam Filtering** | Unsolicited Phishing Spam | Legitimate job offer or '
                                'urgent bank notice sent to Spam folder. Catastrophic disruption. | Spam email slips '
                                'into inbox. Mild annoyance to user. | **MAXIMIZE PRECISION** (Ensure flagged emails '
                                'are 99.9% true spam). |\n'
                                '| **Credit Card Fraud** | Stolen Card Transaction | Cardholder declined at dinner; '
                                'mild embarrassment, quick SMS confirmation. | 5,000 USD fraudulent charge approved; '
                                'bank suffers financial loss. | **BALANCED F1 / HIGH RECALL** |\n'
                                '| **Telecom Churn Retention** | Customer Will Churn | Loyal customer given an '
                                'unneeded 500 USD retention voucher. Direct revenue loss. | Customer churns to '
                                'competitor; lifetime value lost. | **CALIBRATED PRECISION** (Spend retention bonus '
                                'only when sure). |',
                        'citations': [   'Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition '
                                         'Letters, 27(8), 861-874.',
                                         'Powers, D. M. (2020). Evaluation: from precision, recall and F-measure to '
                                         'ROC, informedness, markedness and correlation. arXiv:2010.16061.'],
                        'heading': '4. The Confusion Matrix & Primary Classification Metrics',
                        'section_id': 'cml-l08-sec04'},
                    {   'body': '### 5.1 The Threshold Lever: Balancing Precision and Recall\n'
                                '\n'
                                'The decision threshold $\\tau$ is an external business knob, **not** a fixed '
                                'mathematical law:\n'
                                '\n'
                                '```\n'
                                'Threshold Dynamic:\n'
                                '   Lower Threshold (tau = 0.2):\n'
                                '     --> Model predicts Positive much more aggressively.\n'
                                '     --> Catches almost all positives: RECALL INCREASES.\n'
                                '     --> Generates more false alarms: PRECISION DECREASES.\n'
                                '\n'
                                '   Raise Threshold (tau = 0.8):\n'
                                '     --> Model predicts Positive only when extremely confident.\n'
                                '     --> Low false alarms: PRECISION INCREASES.\n'
                                '     --> Misses borderline positive cases: RECALL DECREASES.\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.2 The ROC Curve and Area Under the Curve (ROC-AUC)\n'
                                '\n'
                                'The **Receiver Operating Characteristic (ROC)** curve plots the trade-off across all '
                                'possible thresholds $\\tau \\in [0, 1]$:\n'
                                '- **Y-axis**: True Positive Rate ($\\text{TPR} = \\text{Recall}$)\n'
                                '- **X-axis**: False Positive Rate ($\\text{FPR} = 1 - \\text{Specificity}$)\n'
                                '\n'
                                '```\n'
                                'ROC Curve Interpretation:\n'
                                '       TPR (Recall) ^\n'
                                '                1.0 |               .------------ (Perfect Classifier: AUC = 1.0)\n'
                                "                    |            .-'\n"
                                "                    |         .-'\n"
                                "                    |      .-'   AUC = 0.85\n"
                                "                    |   .-'\n"
                                "                    |.-' (Diagonal line: Random Guessing, AUC = 0.5)\n"
                                '                0.0 +-------------------------------------------> FPR\n'
                                '                    0.0                                       1.0\n'
                                '```\n'
                                '\n'
                                '#### Meaning of ROC-AUC:\n'
                                'The Area Under the ROC Curve (ROC-AUC) has a concrete probabilistic interpretation:\n'
                                '> *ROC-AUC is the probability that the classifier will rank a randomly chosen '
                                'positive sample higher than a randomly chosen negative sample.*\n'
                                '- $\\text{AUC} = 0.5$: Worthless coin flip.\n'
                                '- $\\text{AUC} = 0.85$: Strong discrimination ability.\n'
                                '- $\\text{AUC} = 1.0$: Perfect class separation.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.3 Worked Whiteboard Example: Calculating ROC-AUC by Hand\n'
                                '\n'
                                'Suppose your model scores 5 website browsing sessions predicting whether the visitor '
                                'will make a purchase ($y = 1$).\n'
                                'Two sessions bought ($A, B$) and three did not ($C, D, E$):\n'
                                '\n'
                                '| Session | Actually Bought? ($y$) | Model Predicted Score ($\\hat{p}$) |\n'
                                '| :--- | :--- | :--- |\n'
                                '| **A** | **Yes ($y = 1$)** | **0.90** |\n'
                                '| **C** | No ($y = 0$) | 0.70 |\n'
                                '| **B** | **Yes ($y = 1$)** | **0.40** |\n'
                                '| **D** | No ($y = 0$) | 0.30 |\n'
                                '| **E** | No ($y = 0$) | 0.10 |\n'
                                '\n'
                                '#### Step 1: Pairwise Ranking (Concordant Pairs)\n'
                                'There are $N_{\\text{pos}} \\times N_{\\text{neg}} = 2 \\times 3 = \\mathbf{6}$ '
                                'possible buyer–non-buyer pairs.\n'
                                'Let us test every single pair to check if the buyer received a strictly higher score '
                                'than the non-buyer:\n'
                                '1. **$A$ (0.90) vs $C$ (0.70)**: $A$ scores higher $\\implies$ **Win (+1)**\n'
                                '2. **$A$ (0.90) vs $D$ (0.30)**: $A$ scores higher $\\implies$ **Win (+1)**\n'
                                '3. **$A$ (0.90) vs $E$ (0.10)**: $A$ scores higher $\\implies$ **Win (+1)**\n'
                                '4. **$B$ (0.40) vs $C$ (0.70)**: $B$ scores lower ($0.40 < 0.70$) $\\implies$ **Loss '
                                '(0)**\n'
                                '5. **$B$ (0.40) vs $D$ (0.30)**: $B$ scores higher $\\implies$ **Win (+1)**\n'
                                '6. **$B$ (0.40) vs $E$ (0.10)**: $B$ scores higher $\\implies$ **Win (+1)**\n'
                                '\n'
                                'Total buyer wins across all pairs: $3 + 2 = \\mathbf{5}$.\n'
                                '$$\\text{ROC-AUC} = \\frac{\\text{Concordant Pairs}}{\\text{Total Pairs}} = '
                                '\\frac{5}{6} \\approx \\mathbf{0.833}$$\n'
                                '\n'
                                '#### Step 2: Step-by-Step Threshold Sweep\n'
                                'If we sweep decision threshold $\\tau$ across the scores, we generate the empirical '
                                'ROC coordinates:\n'
                                '\n'
                                '| Threshold ($\\tau$) | Predicted Positives | True Positives ($TP$) | False Positives '
                                '($FP$) | $\\text{TPR} = \\frac{TP}{2}$ | $\\text{FPR} = \\frac{FP}{3}$ |\n'
                                '| :--- | :--- | :--- | :--- | :--- | :--- |\n'
                                '| $\\tau > 0.90$ | None | 0 | 0 | **0.0** | **0.0** |\n'
                                '| $\\tau = 0.90$ | {A} | 1 | 0 | **0.5** | **0.0** |\n'
                                '| $\\tau = 0.70$ | {A, C} | 1 | 1 | **0.5** | **0.333** |\n'
                                '| $\\tau = 0.40$ | {A, C, B} | 2 | 1 | **1.0** | **0.333** |\n'
                                '| $\\tau = 0.30$ | {A, C, B, D} | 2 | 2 | **1.0** | **0.667** |\n'
                                '| $\\tau = 0.10$ | All 5 | 2 | 3 | **1.0** | **1.0** |\n'
                                '\n'
                                'Calculating the area under these stepped rectangular blocks gives:\n'
                                '$$\\text{Area} = (0.333 - 0.0) \\times 0.5 + (1.0 - 0.333) \\times 1.0 = 0.1667 + '
                                '0.6667 = \\mathbf{0.833}$$\n'
                                'Both the pairwise ranking count and the geometric integral match with 100% '
                                'mathematical precision!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.4 Why ROC Deceives on Imbalanced Data (And Why PR Curves Rule)\n'
                                '\n'
                                'Consider a fraud detection dataset with 100,000 transactions:\n'
                                '- 99,000 legitimate ($y = 0$)\n'
                                '- 1,000 fraudulent ($y = 1$)\n'
                                '\n'
                                'Suppose a model produces **990 False Positives** ($FP = 990$) while catching 800 '
                                'frauds ($TP = 800$):\n'
                                '- $\\text{False Positive Rate} = \\frac{FP}{TN + FP} = \\frac{990}{98,010 + 990} = '
                                '\\frac{990}{99,000} = 0.01$ (Only 1%! The ROC curve looks stunning!).\n'
                                '- But look at **Precision**: $\\text{Precision} = \\frac{TP}{TP + FP} = '
                                '\\frac{800}{800 + 990} = \\frac{800}{1790} \\approx 44.7\\%$! More than half of all '
                                'flagged transactions are false alarms!\n'
                                '\n'
                                '> **The Golden Production Rule**:\n'
                                '> - Use **ROC-AUC** when classes are roughly balanced.\n'
                                '> - Use the **Precision-Recall Curve (PR-AUC)** whenever positive events are rare (< '
                                '10%). The PR curve ignores True Negatives ($TN$), exposing false alarm dilution '
                                'immediately.',
                        'citations': [   'Saito, T., & Rehmsmeier, M. (2015). The precision-recall plot is more '
                                         'informative than the ROC plot when evaluating binary classifiers on '
                                         'imbalanced datasets. PloS ONE, 10(3), e0118432.'],
                        'heading': '5. Operating Thresholds & Diagnostic Curves: ROC-AUC vs. Precision-Recall',
                        'section_id': 'cml-l08-sec05'},
                    {   'body': '### 6.1 The Accuracy Paradox in Imbalanced Regimes\n'
                                '\n'
                                'If $99\\%$ of credit card transactions are legitimate and $1\\%$ are fraudulent, a '
                                'trivial model that outputs `Legitimate` for every single query achieves:\n'
                                '\n'
                                '$$\\text{Accuracy} = \\frac{99,000 + 0}{100,000} = \\mathbf{99.0\\%}$$\n'
                                '\n'
                                'The model has a 99% accuracy score, yet it stops **zero fraud** and is completely '
                                'worthless.\n'
                                'In real-world ML systems with imbalanced targets, **Accuracy is a toxic metric**.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 6.2 Industry Remediation Strategies\n'
                                '\n'
                                '```\n'
                                'Remediation Strategy Spectrum:\n'
                                '   '
                                '┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐\n'
                                '   │ 1. Cost-Sensitive Learning      │ 2. Data Resampling (SMOTE)      │ 3. Threshold '
                                'Tuning             │\n'
                                '   '
                                '├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤\n'
                                '   │ Multiplies minority loss by     │ Synthesizes artificial minority │ Optimizes '
                                'decision threshold τ  │\n'
                                '   │ class weight factor.            │ samples using k-NN vectors.     │ on '
                                'validation PR curve.         │\n'
                                '   │ Zero data duplication.          │ Balances training distribution. │ Direct '
                                'alignment to business $. │\n'
                                '   '
                                '└─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘\n'
                                '```\n'
                                '\n'
                                "#### Strategy 1: Cost-Sensitive Loss Weighting (`class_weight='balanced'`)\n"
                                'Instead of treating all errors equally, we scale the loss of each sample by its class '
                                'weight:\n'
                                '\n'
                                '$$J_{\\text{weighted}}(\\mathbf{w}) = -\\frac{1}{n} \\sum_{i=1}^n w_{y^{(i)}} \\left[ '
                                'y^{(i)} \\ln(\\hat{p}_i) + (1 - y^{(i)}) \\ln(1 - \\hat{p}_i) \\right]$$\n'
                                '\n'
                                "In Scikit-Learn, `class_weight='balanced'` computes weights inversely proportional to "
                                'class frequencies:\n'
                                '\n'
                                '$$w_c = \\frac{n_{\\text{samples}}}{k \\cdot n_c}$$\n'
                                '\n'
                                'For 1,000 samples with 950 Class 0 and 50 Class 1 ($k=2$):\n'
                                '$$w_0 = \\frac{1000}{2 \\times 950} \\approx 0.526, \\qquad w_1 = \\frac{1000}{2 '
                                '\\times 50} = \\mathbf{10.000}$$\n'
                                'Missing a single Class 1 sample is penalized **19 times more severely** than missing '
                                'a Class 0 sample! The optimizer shifts the decision boundary to protect the minority '
                                'class.\n'
                                '\n'
                                '#### Strategy 2: SMOTE (Synthetic Minority Over-sampling Technique)\n'
                                'Instead of simply duplicating existing minority points (which causes overfitting), '
                                'SMOTE synthesizes new plausible feature vectors along the line segments connecting '
                                '$k$-nearest minority neighbors:\n'
                                '\n'
                                '$$\\mathbf{x}_{\\text{new}} = \\mathbf{x}_i + \\lambda \\cdot (\\mathbf{x}_{zi} - '
                                '\\mathbf{x}_i), \\qquad \\lambda \\sim \\text{Uniform}(0, 1)$$\n'
                                '\n'
                                '```\n'
                                'SMOTE Geometric Synthesis:\n'
                                '         x2 ^\n'
                                '            │            x_zi (Minority Neighbor)\n'
                                '            │           /\n'
                                '            │          * (x_new synthesized on line segment!)\n'
                                '            │         /\n'
                                '            │        x_i (Minority Sample)\n'
                                '            +────────────────────────► x1\n'
                                '```\n'
                                '\n'
                                '*Critical Anti-Leakage Rule*: Never run SMOTE on the whole dataset before '
                                'cross-validation! SMOTE must be performed **strictly inside each training fold**.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 6.3 End-to-End Scikit-Learn Production Pipeline\n'
                                '\n'
                                '```python\n'
                                'import numpy as np\n'
                                'from sklearn.datasets import make_classification\n'
                                'from sklearn.model_selection import train_test_split\n'
                                'from sklearn.linear_model import LogisticRegression\n'
                                'from sklearn.preprocessing import StandardScaler\n'
                                'from sklearn.pipeline import Pipeline\n'
                                'from sklearn.metrics import (\n'
                                '    classification_report,\n'
                                '    confusion_matrix,\n'
                                '    roc_auc_score,\n'
                                '    average_precision_score,\n'
                                '    precision_recall_curve\n'
                                ')\n'
                                '\n'
                                '# 1. Generate imbalanced binary problem: 2,500 samples, 95% Class 0 (Retain), 5% '
                                'Class 1 (Churn)\n'
                                'X, y = make_classification(\n'
                                '    n_samples=2500,\n'
                                '    n_features=12,\n'
                                '    n_informative=6,\n'
                                '    weights=[0.95, 0.05],\n'
                                '    random_state=42\n'
                                ')\n'
                                '\n'
                                '# 2. Stratified Train / Test Split (Guarantees 5% positive class in both partitions)\n'
                                'X_train, X_test, y_train, y_test = train_test_split(\n'
                                '    X, y, test_size=0.25, random_state=42, stratify=y\n'
                                ')\n'
                                '\n'
                                '# 3. Cost-Sensitive Logistic Pipeline (Leak-free scaling + balanced loss weights)\n'
                                'pipeline = Pipeline([\n'
                                '    ("scaler", StandardScaler()),\n'
                                '    ("classifier", LogisticRegression(\n'
                                '        class_weight="balanced",  # Multiplies minority loss by n / (2 * n_pos)\n'
                                '        solver="lbfgs",\n'
                                '        C=1.0,                    # Inverse regularization strength (C = 1 / lambda)\n'
                                '        random_state=42\n'
                                '    ))\n'
                                '])\n'
                                'pipeline.fit(X_train, y_train)\n'
                                '\n'
                                '# 4. Predict Raw Probabilities on Unseen Test Partition\n'
                                'y_probs = pipeline.predict_proba(X_test)[:, 1]\n'
                                '\n'
                                '# 5. Business Threshold Optimization (Default tau = 0.50 vs Custom tau = 0.35)\n'
                                'default_preds = pipeline.predict(X_test)\n'
                                'custom_tau = 0.35\n'
                                'custom_preds = (y_probs >= custom_tau).astype(int)\n'
                                '\n'
                                '# 6. Comprehensive Metric Reporting\n'
                                'roc_auc = roc_auc_score(y_test, y_probs)\n'
                                'pr_auc = average_precision_score(y_test, y_probs)\n'
                                '\n'
                                'print("=== IMBALANCE-AWARE PERFORMANCE REPORT ===")\n'
                                'print(f"ROC-AUC Score:                 {roc_auc:.4f}")\n'
                                'print(f"PR-AUC (Average Precision):    {pr_auc:.4f}")\n'
                                'print("\\nConfusion Matrix at Custom Threshold (tau = 0.35):")\n'
                                'print(confusion_matrix(y_test, custom_preds))\n'
                                'print("\\nDetailed Classification Report (tau = 0.35):")\n'
                                'print(classification_report(y_test, custom_preds, target_names=["Retain", "Churn"]))\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 6.4 Key Diagnostic Summary & Engineering Pitfalls\n'
                                '\n'
                                '| Diagnostic Pitfall | Why It Happens | Severe Consequence | Production Solution |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **Evaluating Imbalanced Data with Accuracy** | Majority class dominates sample '
                                'counts. | Model predicts majority class everywhere and passes evaluation while '
                                'completely failing in production. | Ban accuracy; evaluate strictly with **PR-AUC, '
                                'F1-Score, and Recall**. |\n'
                                '| **Applying SMOTE Before Cross-Validation Split** | Synthetic points created from '
                                'test fold distribution leak into training fold. | Optimistic validation metrics; '
                                'massive performance collapse in production. | Run SMOTE strictly inside training '
                                'folds using `imblearn.pipeline.Pipeline`. |\n'
                                '| **Treating 0.50 as an Inviolable Threshold** | Blindly using `.predict()` without '
                                'tuning $\\tau$. | Fails business objectives when False Negatives cost 50x more than '
                                'False Positives. | Use `.predict_proba()` and select threshold $\\tau$ from '
                                'validation PR curve. |\n'
                                '| **Unstandardized Features Before Logistic Regression** | Features have different '
                                'numerical ranges (e.g. Salary vs Age). | L2 regularization (`C` parameter) penalizes '
                                'small-scale features unfairly; gradient descent oscillates. | Always wrap '
                                '`StandardScaler` and `LogisticRegression` inside a `Pipeline`. |',
                        'citations': [   'Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). '
                                         'SMOTE: synthetic minority over-sampling technique. JAIR, 16, 321-357.',
                                         'He, H., & Garcia, E. A. (2009). Learning from imbalanced data. IEEE TKDE, '
                                         '21(9), 1263-1284.'],
                        'heading': '6. Class Imbalance Remediation & Production Scikit-Learn Pipeline',
                        'section_id': 'cml-l08-sec06'}],
    'subject_code': 'CML',
    'summary': 'An exhaustive, intuitive masterclass on Binary Classification using Logistic Regression. Contrasts '
               'lines of best fit with hyperplanes of best separation, demystifies the Sigmoid function, Logit, and '
               'Odds, formalizes the convex Binary Cross-Entropy loss surface, and delivers a rigorous breakdown of '
               'the Confusion Matrix. Explores threshold tuning dynamics, shows why ROC curves deceive on imbalanced '
               'data while Precision-Recall curves tell the truth, and details production remediation for class '
               'imbalance.',
    'tags': [   'Logistic Regression',
                'Classification',
                'Sigmoid',
                'Log-Loss',
                'Binary Cross-Entropy',
                'Confusion Matrix',
                'Precision and Recall',
                'F1-Score',
                'ROC-AUC',
                'Precision-Recall Curve',
                'Class Imbalance',
                'Cost-Sensitive Learning'],
    'term': 'Term 5',
    'topic_title': '8. Logistic Regression, Classification Metrics & Class Imbalance'}

