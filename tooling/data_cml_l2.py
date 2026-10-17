"""
Data definition for data_cml_l2:
"""

L2_DATA = {   'approval_status': 'approved',
    'key_takeaways': [   'Preprocessing bugs never manifest as syntax errors or runtime exceptions; they manifest as '
                         "deceptively inflated 'fake-good' cross-validation scores that collapse in production.",
                         'Any statistic learned from data (mean, standard deviation, median, category vocabulary, '
                         'quantile bins) must be fitted on training data only and merely transformed on test data.',
                         "Nominal features require One-Hot Encoding with handle_unknown='ignore' to prevent runtime "
                         'crashes; ordinal features require ordered integer mappings preserving monotonic hierarchy.',
                         'Treating nominal categories as arbitrary integers invents false Euclidean distances and '
                         'invalidates linear and metric-based models.',
                         'Distance-based algorithms (KNN, K-Means, SVM) and gradient-based optimizers require feature '
                         'scaling; tree-based models are scale-invariant.',
                         'Median imputation is strictly superior to mean imputation for skewed numeric features with '
                         'heavy outlier tails.',
                         'Scikit-Learn Pipelines lock preprocessing and modeling into a single atomic object, '
                         'eliminating data leakage by architectural design.'],
    'last_updated': '2026-10-16T00:00:00Z',
    'learning_objectives': [   'Diagnose and eliminate all forms of data leakage (preprocessing, target, temporal, and '
                               'group leakage).',
                               'Enforce strict train/test hygiene by partitioning data before computing any '
                               'statistical parameters.',
                               'Implement optimal categorical encoding strategies for nominal and ordinal feature '
                               'spaces.',
                               'Select and apply numerical scaling transformations (StandardScaler, MinMaxScaler, '
                               'RobustScaler) based on feature geometry and algorithm sensitivity.',
                               'Handle missing data via robust statistical imputation and missing indicator '
                               'mechanisms.',
                               'Construct modular, leakage-proof machine learning pipelines using Scikit-Learn '
                               'ColumnTransformer and Pipeline.'],
    'note_id': 'cml-t5-l02',
    'quiz': {   'description': '25-question examination evaluating data leakage mechanisms, categorical encoding '
                               'mathematics, numerical scaling transformations, missing data imputation strategies, '
                               'and Scikit-Learn pipeline architecture.',
                'questions': [   {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'Train/test hygiene requires splitting the data first. The scaler '
                                                    'or imputer must be fitted exclusively on X_train. The learned '
                                                    'parameters (mean, std, median) are then used to transform both '
                                                    'X_train and X_test.',
                                     'id': 'q-cml-l02-01',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'StandardScaler().fit(X) on all data -> '
                                                                'train_test_split() -> model.fit(X_train)'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'train_test_split() -> scaler.fit(X_train) -> '
                                                                'transform both X_train and X_test -> '
                                                                'model.fit(X_train)'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'train_test_split() -> scaler.fit(X_test) -> transform '
                                                                'both X_train and X_test -> model.fit(X_train)'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'SimpleImputer().fit(X) on all data -> '
                                                                'StandardScaler().fit(X) on all data -> '
                                                                'train_test_split()'}],
                                     'question': 'Which of the following execution sequences correctly enforces '
                                                 'train/test hygiene to prevent preprocessing data leakage?',
                                     'subtopic': 'Train/Test Hygiene',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'Shirt size has an inherent hierarchical order (S < M < L < XL). '
                                                    'OrdinalEncoder with declared categories preserves this monotonic '
                                                    'progression as ordered numerical integers (0, 1, 2, 3), allowing '
                                                    'linear models to learn size-dependent trends.',
                                     'id': 'q-cml-l02-02',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': "One-Hot Encoding with drop='first'"},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': "Ordinal Encoding declaring categories=[['S', 'M', "
                                                                "'L', 'XL']]"},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Assigning random unordered integers to each size'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Dropping the feature entirely to avoid non-numeric '
                                                                'inputs'}],
                                     'question': "You have a feature 'shirt_size' with values 'S', 'M', 'L', 'XL' that "
                                                 'possesses a natural monotonic order relevant for a linear model. '
                                                 'What is the most appropriate encoding strategy?',
                                     'subtopic': 'Categorical Encoding Selection',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'The mean is sensitive to extreme values; a few massive outlier '
                                                    'district room counts pull the mean far above typical values. The '
                                                    'median represents the 50th percentile and remains unaffected by '
                                                    'extreme outlier magnitudes.',
                                     'id': 'q-cml-l02-03',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'The median is always mathematically larger than the '
                                                                'mean.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'The median is robust to extreme outliers, whereas the '
                                                                'mean is pulled heavily into the tail and distorts '
                                                                'imputed values.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Mean imputation cannot be computed on floating-point '
                                                                'numbers.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Scikit-Learn SimpleImputer does not support mean '
                                                                'imputation.'}],
                                     'question': 'When imputing missing values in a heavily right-skewed numerical '
                                                 'feature containing severe extreme outliers (e.g., California '
                                                 "'total_rooms'), why is median imputation preferred over mean "
                                                 'imputation?',
                                     'subtopic': 'Missing Value Imputation',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-3'],
                                     'difficulty': 'easy',
                                     'explanation': 'Removing unlabelled records (where y is NaN) cleans the target '
                                                    'space and does not compute or leak any statistical summary '
                                                    'parameters from test features into the training set. Options 1, '
                                                    '2, and 4 compute dataset-wide statistics and leak test data.',
                                     'id': 'q-cml-l02-04',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Computing the mean of a feature and filling NaN '
                                                                'values.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Fitting a StandardScaler to center features at zero.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'Dropping dataset rows where the target label y is '
                                                                'missing or NaN.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Applying pd.qcut() to discretize continuous features '
                                                                'into empirical quartiles.'}],
                                     'question': 'Which of the following data operations is mathematically SAFE to '
                                                 'execute on a full dataset prior to train/test splitting?',
                                     'subtopic': 'Safe Operations Before Split',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'StandardScaler computes z = (x - mu) / sigma. The resulting '
                                                    'standardized distribution has a mean of 0.0 and a standard '
                                                    'deviation (and variance) of 1.0. Bounding data between 0 and 1 is '
                                                    'the function of MinMaxScaler.',
                                     'id': 'q-cml-l02-05',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Mean = 1.0, Standard Deviation = 0.0'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Mean = 0.0, Standard Deviation = 1.0'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Mean = 0.5, Standard Deviation = 0.5'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Minimum = 0.0, Maximum = 1.0'}],
                                     'question': 'What are the theoretical mean and standard deviation of a feature '
                                                 "immediately after transformation via Scikit-Learn's StandardScaler?",
                                     'subtopic': 'Numerical Scaling Mathematics',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'Assigning arbitrary ordered integers (1, 2, 3) to nominal '
                                                    'categories imposes an artificial quantitative distance (|3 - 1| = '
                                                    '2 vs |2 - 1| = 1), forcing linear and distance-based models to '
                                                    'treat Blue as quantitatively larger than Green and Red.',
                                     'id': 'q-cml-l02-06',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'It assumes all three colors have zero variance.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'It assumes Blue is mathematically twice as high as '
                                                                'Green and three times as high as Red, inventing a '
                                                                'non-existent metric hierarchy.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It causes the design matrix to become non-invertible '
                                                                'due to singularity.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It forces the model to ignore color completely.'}],
                                     'question': "An analyst encodes the nominal feature 'favorite_color' ('Red', "
                                                 "'Green', 'Blue') as Red = 1, Green = 2, Blue = 3. What invalid "
                                                 'geometric assumption does this introduce into a linear regression '
                                                 'model?',
                                     'subtopic': 'Categorical Encoding Mis-specification',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'A Scikit-Learn Pipeline encapsulates all preprocessing steps and '
                                                    'the model into a single object. Calling pipeline.fit(X_train, '
                                                    'y_train) fits transformers strictly on X_train, and '
                                                    'pipeline.predict(X_test) applies stored train statistics, '
                                                    'eliminating leakage.',
                                     'id': 'q-cml-l02-07',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Pipelines automatically convert regression models '
                                                                'into deep neural networks.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Pipelines ensure that transformers are fitted '
                                                                'strictly on training folds during fit() and only '
                                                                'transform() during predict(), preventing leakage by '
                                                                'construction.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Pipelines eliminate the need to collect training '
                                                                'data.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Pipelines guarantee 100% test accuracy on any '
                                                                'dataset.'}],
                                     'question': 'What is the primary architectural advantage of binding transformers '
                                                 'and estimators together inside a Scikit-Learn Pipeline?',
                                     'subtopic': 'Pipeline Purpose',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'Decision Trees make split decisions based on rank order '
                                                    'thresholds (x_j <= threshold). Monotonic scaling does not alter '
                                                    'the relative order of values, making tree algorithms completely '
                                                    'invariant to scaling.',
                                     'id': 'q-cml-l02-08',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'K-Nearest Neighbors (KNN)'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Decision Trees and Random Forests'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Support Vector Machines with RBF Kernel'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Ridge and Lasso Regularized Regression'}],
                                     'question': 'Which of the following machine learning model families is '
                                                 'mathematically INVARIANT to monotonic numerical feature scaling?',
                                     'subtopic': 'Scale Invariant Models',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2', 'opt-4'],
                                     'difficulty': 'medium',
                                     'explanation': "Setting handle_unknown='ignore' ensures that any category not "
                                                    'observed in training data results in all-zeros across the one-hot '
                                                    'columns for that feature. It does not crash (option 1) and never '
                                                    'refits on test data (option 3).',
                                     'id': 'q-cml-l02-09',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'The encoder throws a ValueError and halts program '
                                                                'execution.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'The unseen category is encoded as an all-zeros row '
                                                                'across all one-hot columns for that feature.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The encoder refits its internal category vocabulary '
                                                                'on the test sample.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': True,
                                                        'text': 'The pipeline processes the sample without crashing, '
                                                                'avoiding runtime downtime.'}],
                                     'question': 'When deploying a OneHotEncoder to production, what occurs when an '
                                                 "unseen categorical level (e.g., ocean_proximity = 'ISLAND') appears "
                                                 "in test data if handle_unknown='ignore' was configured? (Select all "
                                                 'that apply)',
                                     'subtopic': 'OneHotEncoder Unknown Levels',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'The sum of all K indicator columns is identically equal to 1 for '
                                                    'every row, which is collinear with the model intercept beta_0 * '
                                                    '1. This linear dependence makes the matrix (X^T X) singular and '
                                                    'non-invertible. Dropping one level restores full rank.',
                                     'id': 'q-cml-l02-10',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'To prevent memory overflow in Python.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Because the sum of all K dummy columns equals the '
                                                                'intercept column (vector of 1s), causing perfect '
                                                                'multicollinearity and making (X^T X) non-invertible.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Because Scikit-Learn cannot fit models with more than '
                                                                '3 features.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Because one category is always corrupted in real '
                                                                'datasets.'}],
                                     'question': 'Why does an unregularized Ordinary Least Squares (OLS) linear '
                                                 'regression model with an intercept term require dropping one '
                                                 "category (drop='first') when one-hot encoding a nominal variable "
                                                 'with K levels?',
                                     'subtopic': 'The Dummy Variable Trap',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-3'],
                                     'difficulty': 'medium',
                                     'explanation': 'RobustScaler centers data using the median and scales using the '
                                                    'Interquartile Range (IQR = Q3 - Q1). Outliers outside the '
                                                    '25th-75th percentiles do not affect the median or IQR, preventing '
                                                    'normal values from being compressed into a near-zero range.',
                                     'id': 'q-cml-l02-11',
                                     'options': [   {'id': 'opt-1', 'is_correct': False, 'text': 'StandardScaler'},
                                                    {'id': 'opt-2', 'is_correct': False, 'text': 'MinMaxScaler'},
                                                    {'id': 'opt-3', 'is_correct': True, 'text': 'RobustScaler'},
                                                    {'id': 'opt-4', 'is_correct': False, 'text': 'Binarizer'}],
                                     'question': 'A dataset contains a financial transaction feature where 95% of '
                                                 'transactions are between 10 USD and 100 USD, but a few fraud '
                                                 'transactions are 500,000 USD. Which scaler scales the typical '
                                                 'transaction range effectively without being crushed by the outliers?',
                                     'subtopic': 'RobustScaler vs StandardScaler',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2', 'opt-3', 'opt-4'],
                                     'difficulty': 'medium',
                                     'explanation': 'Option 2 is Lookahead/Temporal Leakage. Option 3 is Target '
                                                    'Leakage (a refund only occurs after fraud is verified). Option 4 '
                                                    'is Preprocessing Leakage. Option 1 is proper, leak-free '
                                                    'preprocessing.',
                                     'id': 'q-cml-l02-12',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Imputing missing values using the mean of the '
                                                                'training fold only.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Randomly shuffling time-series stock data and using '
                                                                'future closing prices to predict past trends.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'Including an account status feature '
                                                                "'Dispute_Refund_Issued' to predict whether a credit "
                                                                'card transaction was fraudulent.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': True,
                                                        'text': 'Computing Min-Max scaling parameters across the '
                                                                'entire dataset prior to splitting into train and test '
                                                                'folds.'}],
                                     'question': 'Which of the following scenarios represent DATA LEAKAGE? (Select all '
                                                 'that apply)',
                                     'subtopic': 'Forms of Data Leakage',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'MinMaxScaler applies the formula x_scaled = (x - min) / (max - '
                                                    'min). With min=10 and max=50: (60 - 10) / (50 - 10) = 50 / 40 = '
                                                    '1.25. Unless explicitly configured with clip=True, values outside '
                                                    'the training range exceed the [0, 1] interval.',
                                     'id': 'q-cml-l02-13',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'It is clipped to 1.0.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'It is transformed linearly to 1.25.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It throws an out-of-range exception.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It is assigned a value of 0.0.'}],
                                     'question': 'A MinMaxScaler is fitted on training feature values ranging from '
                                                 '[10, 50]. During test inference, a novel sample with value x = 60 is '
                                                 'transformed. What is the resulting transformed value?',
                                     'subtopic': 'MinMaxScaler Out-of-Bounds Behavior',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'ColumnTransformer applies distinct transformer pipelines to '
                                                    'designated subsets of columns (e.g., scaling numerics, one-hot '
                                                    'encoding nominals) and concatenates their outputs horizontally '
                                                    'into a unified numeric array.',
                                     'id': 'q-cml-l02-14',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'To convert tabular data into a relational SQL '
                                                                'database.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'To apply different transformation pipelines to '
                                                                'specified subsets of columns (numeric, nominal, '
                                                                'ordinal) and concatenate the results into a single '
                                                                'feature matrix.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'To drop all columns that have non-zero correlation '
                                                                'with the target.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'To automate hyperparameter tuning via random '
                                                                'search.'}],
                                     'question': "What is the primary role of Scikit-Learn's ColumnTransformer in a "
                                                 'production ML pipeline?',
                                     'subtopic': 'ColumnTransformer Syntax & Role',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'medium',
                                     'explanation': 'Missingness is often Missing at Random (MAR) or Missing Not at '
                                                    'Random (MNAR), where the fact that data was not recorded carries '
                                                    'strong predictive information. Setting add_indicator=True appends '
                                                    'a binary 1/0 indicator column capturing this signal.',
                                     'id': 'q-cml-l02-15',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'It adds a binary column indicating whether a value '
                                                                'was originally missing, preserving the predictive '
                                                                'signal of missingness.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'It deletes columns that have more than 50% missing '
                                                                'values.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It raises a warning flag in the terminal when NaNs '
                                                                'are detected.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It forces the imputer to use deep learning for '
                                                                'fill-ins.'}],
                                     'question': "What is the purpose of setting add_indicator=True in Scikit-Learn's "
                                                 'SimpleImputer?',
                                     'subtopic': 'Missing Indicator Purpose',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1', 'opt-2', 'opt-4'],
                                     'difficulty': 'medium',
                                     'explanation': 'Unscaled features create an ill-conditioned, elongated loss '
                                                    'landscape where gradients oscillate perpendicular to the descent '
                                                    'valley, requiring tiny learning rates and slow convergence. '
                                                    'Option 3 is false: derivatives exist, but optimization dynamics '
                                                    'are degraded.',
                                     'id': 'q-cml-l02-16',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'The loss surface contours become highly eccentric '
                                                                'ellipses, causing gradient updates to oscillate '
                                                                'wildly rather than taking direct paths to the '
                                                                'minimum.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'The learning rate must be set extremely small to '
                                                                'prevent divergence on large-scale features, '
                                                                'drastically slowing convergence on small-scale '
                                                                'features.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Gradient descent cannot mathematically compute '
                                                                'partial derivatives on unscaled numbers.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': True,
                                                        'text': 'Features with larger scales dominate weight updates '
                                                                'regardless of their true underlying predictive '
                                                                'importance.'}],
                                     'question': 'Why does training a gradient-based model (such as Logistic '
                                                 'Regression or a Neural Network) on UNSCALED features with disparate '
                                                 'magnitudes hinder performance? (Select all that apply)',
                                     'subtopic': 'Gradient Descent Loss Geometry',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-3'],
                                     'difficulty': 'medium',
                                     'explanation': 'When missingness depends directly on the unobserved variable '
                                                    "itself (the patient's severe unmeasured health status caused the "
                                                    'absence), it is Missing Not at Random (MNAR). Simple mean/median '
                                                    'imputation on MNAR introduces severe systematic bias.',
                                     'id': 'q-cml-l02-17',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Missing Completely at Random (MCAR)'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Missing at Random (MAR)'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'Missing Not at Random (MNAR)'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Deterministic Zero Fill'}],
                                     'question': 'In a clinical trial, patients who experience severe, debilitating '
                                                 'drug side effects systematically drop out and fail to attend their '
                                                 'final health evaluation visit. What Rubin missingness mechanism '
                                                 'describes this data?',
                                     'subtopic': 'Missing Data Mechanisms',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'hard',
                                     'explanation': "Naive target encoding uses y_i to compute the mean for sample i's "
                                                    'category. For rare categories, the encoded feature becomes an '
                                                    'almost exact proxy for the target y, causing massive target '
                                                    'leakage and severe overfitting. Out-of-fold target encoding with '
                                                    'smoothing is required.',
                                     'id': 'q-cml-l02-18',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'The encoder divides by zero and crashes.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'The categorical column leaks the target value y_i '
                                                                'directly into feature x_i, causing extreme '
                                                                'overfitting where training error drops to zero but '
                                                                'test error explodes.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The design matrix becomes completely sparse.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Target encoding turns regression problems into '
                                                                'classification.'}],
                                     'question': 'An engineer implements Target Encoding (replacing each categorical '
                                                 'level with the mean of target y for that category) across the entire '
                                                 'training dataset without out-of-fold partitioning. What catastrophic '
                                                 'issue occurs?',
                                     'subtopic': 'Target Encoding Leakage Dynamics',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'hard',
                                     'explanation': 'If x_2 = x_1 / 1000, its weight w_2 must equal 1000 * w_1 to have '
                                                    'the same effect on y. The L2 penalty lambda * w_2^2 is (1000)^2 = '
                                                    '1,000,000 times larger, causing the optimizer to shrink w_2 '
                                                    'disproportionately. Scaling features to equal variance is '
                                                    'mandatory for regularized models.',
                                     'id': 'q-cml-l02-19',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'It sets the weight of x_1 to exactly zero.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'To produce equal physical impact, x_2 requires a '
                                                                'weight 1,000 times larger than x_1; the lambda '
                                                                '||w||^2 penalty penalizes this large weight 1,000,000 '
                                                                'times more heavily, crushing x_2 regardless of '
                                                                'importance.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Regularization is mathematically invariant to feature '
                                                                'scale.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'L2 regularization only penalizes negative weights.'}],
                                     'question': 'In Ridge Regression with objective J(w) = ||y - X w||^2 + lambda '
                                                 '||w||_2^2, suppose feature x_1 is measured in meters (values ~1,000) '
                                                 'and feature x_2 is measured in kilometers (values ~1). How does L2 '
                                                 'regularization unfairly penalize x_2?',
                                     'subtopic': 'Regularization with Unscaled Features',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'This is Group Leakage. When multiple records belong to the same '
                                                    'entity (patient, user, device), random splitting places different '
                                                    'records of the same patient into both train and test. The model '
                                                    'memorizes unique patient features (bone shape, device artifacts). '
                                                    'GroupShuffleSplit by patient ID is required.',
                                     'id': 'q-cml-l02-20',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'Group Leakage: Scans from the same patient appeared '
                                                                'in both train and test sets, allowing the model to '
                                                                'memorize patient-specific idiosyncrasies rather than '
                                                                'generalizable disease pathology.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Underfitting: The model had too few parameters to '
                                                                'learn chest pathology.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The test set was evaluated using accuracy instead of '
                                                                'mean squared error.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The hospital used 32-bit floating point images '
                                                                'instead of 64-bit.'}],
                                     'question': 'A medical imaging model is trained on 10,000 chest X-ray images '
                                                 'collected from 1,000 distinct patients (10 images per patient). A '
                                                 'standard random train_test_split() is applied. The test accuracy is '
                                                 "96%, but when deployed on a new hospital's patients, accuracy drops "
                                                 'to 68%. What caused this disparity?',
                                     'subtopic': 'Group Leakage in Clustered Data',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1', 'opt-2', 'opt-3'],
                                     'difficulty': 'hard',
                                     'explanation': 'pd.qcut on the full dataset computes percentiles from all rows, '
                                                    'incorporating test data distribution into the bin edges (Option 1 '
                                                    'is leakage). Fixed domain bins (Option 2) or computing quantiles '
                                                    'on X_train only and applying them via pd.cut (Option 3) are '
                                                    'leak-free.',
                                     'id': 'q-cml-l02-21',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': "pd.qcut(df['income'], q=4) before splitting leaks "
                                                                'test set quantiles into the cut thresholds.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': "pd.cut(df['income'], bins=[-np.inf, 2.5, 4.5, 8.0, "
                                                                'np.inf]) with pre-determined domain thresholds before '
                                                                'splitting does not cause statistical leakage.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'pd.qcut() on X_train, then using the resulting train '
                                                                'quantile bin intervals to pd.cut() both X_train and '
                                                                'X_test is leak-free.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Any form of discretization is mathematically illegal '
                                                                'in classical machine learning.'}],
                                     'question': 'An engineer uses pandas to discretize a continuous income feature '
                                                 "into four income bands ('low', 'mid', 'high', 'very_high') before "
                                                 'splitting the dataset. Which of the following approaches causes '
                                                 'LEAKAGE and why? (Select all that apply)',
                                     'subtopic': 'Categorical Quantile Binning Leakage',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'hard',
                                     'explanation': 'RobustScaler formula is x_scaled = (x - Q2) / (Q3 - Q1). Here Q2 '
                                                    '= 50, and IQR = Q3 - Q1 = 70 - 30 = 40. For x = 90: (90 - 50) / '
                                                    '40 = 40 / 40 = 1.00.',
                                     'id': 'q-cml-l02-22',
                                     'options': [   {'id': 'opt-1', 'is_correct': False, 'text': '0.50'},
                                                    {'id': 'opt-2', 'is_correct': True, 'text': '1.00'},
                                                    {'id': 'opt-3', 'is_correct': False, 'text': '2.00'},
                                                    {'id': 'opt-4', 'is_correct': False, 'text': '0.80'}],
                                     'question': 'Suppose feature x has median Q2 = 50, first quartile Q1 = 30, and '
                                                 'third quartile Q3 = 70. When applying RobustScaler, what is the '
                                                 'transformed value of an observation with x = 90?',
                                     'subtopic': 'RobustScaler Mathematics',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'hard',
                                     'explanation': 'In sequential temporal processes, observations are serially '
                                                    'correlated. Random splitting allows the model to train on t+1 '
                                                    'while testing on t, peeking into future market state. '
                                                    'Chronological walk-forward validation (TimeSeriesSplit) is '
                                                    'mandatory.',
                                     'id': 'q-cml-l02-23',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'K-fold cross-validation requires categorical '
                                                                'features.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Random shuffling shuffles future information into '
                                                                'training folds, allowing the model to condition on '
                                                                'future volatility and momentum to predict past prices '
                                                                '(Lookahead Leakage).'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Scikit-learn cannot split datasets with more than '
                                                                '1,000 rows.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Time-series data has zero variance.'}],
                                     'question': 'When building an algorithmic trading model to predict 1-minute stock '
                                                 'returns from order-book features, why is standard k-fold '
                                                 'cross-validation or random train_test_split() fatally flawed?',
                                     'subtopic': 'Time-Series Walk-Forward Hygiene',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1', 'opt-3', 'opt-4'],
                                     'difficulty': 'hard',
                                     'explanation': 'Option 1 is correct (regularization handles collinearity). Option '
                                                    '2 is a dangerous anti-pattern (100k categories causes massive '
                                                    'dimensional curse and memory exhaustion). Option 3 and 4 '
                                                    'represent best practices for managing categorical cardinality.',
                                     'id': 'q-cml-l02-24',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'When using regularized models (Ridge/Lasso) or '
                                                                'gradient boosted trees, retaining all K dummy columns '
                                                                'without dropping the first is preferred because '
                                                                'regularization resolves singularity and preserves '
                                                                'symmetric feature attribution.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'One-Hot Encoding a categorical feature with 100,000 '
                                                                'distinct unique categories (e.g., User ID) is optimal '
                                                                'because it creates 100,000 orthogonal binary '
                                                                'features.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'For ultra-high cardinality features, One-Hot Encoding '
                                                                'causes catastrophic memory explosion and dimensional '
                                                                'sparsity, requiring Target Encoding or Frequency '
                                                                'Encoding instead.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': True,
                                                        'text': 'Sparse matrices (sparse_output=True) in Scikit-Learn '
                                                                'store only non-zero coordinates, preventing memory '
                                                                'exhaustion when one-hot encoding moderately high '
                                                                'cardinality features.'}],
                                     'question': 'Which of the following statements correctly evaluate One-Hot '
                                                 'Encoding trade-offs in modern production pipelines? (Select all that '
                                                 'apply)',
                                     'subtopic': 'OneHotEncoder vs Regularized Ridge',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'If you scale/impute the dataset before passing it to '
                                                    "GridSearchCV, each validation fold's test set was already seen by "
                                                    'the imputer/scaler during the initial fit. Placing the '
                                                    'preprocessor inside the Pipeline ensures that for each of the 5 '
                                                    'CV folds, the transformers are re-fitted strictly on the 4 '
                                                    'training splits.',
                                     'id': 'q-cml-l02-25',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'If data is transformed before GridSearchCV, the '
                                                                'preprocessing statistics leak information across all '
                                                                '5 validation holdout folds during cross-validation.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'GridSearchCV crashes if given a numpy array.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'PolynomialFeatures cannot run outside a pipeline.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Ridge regression only accepts Pipeline objects as '
                                                                'inputs.'}],
                                     'question': 'An engineer wants to perform 5-fold cross-validation to select the '
                                                 'optimal polynomial degree and Ridge alpha parameter. Why must the '
                                                 'preprocessing transformers (imputer, scaler, encoder) be embedded '
                                                 'INSIDE the GridSearchCV pipeline rather than transformed beforehand?',
                                     'subtopic': 'Hyperparameter Tuning with Pipelines',
                                     'type': 'single_choice'}],
                'time_limit': '30 mins',
                'title': 'Comprehensive Examination: Data Preparation, Feature Preprocessing & Leakage Prevention'},
    'schema_version': 1,
    'sections': [   {   'body': '### 1.1 The Machine Learning Data Reality\n'
                                '\n'
                                'Mathematical learning algorithms do not ingest raw enterprise data tables directly. '
                                'Algorithms operate on numerical tensors $\\mathbf{X} \\in \\mathbb{R}^{n \\times d}$. '
                                'Raw enterprise datasets, however, are inherently heterogeneous and imperfect:\n'
                                '1. **Unformatted Text & Categorical Attributes**: Strings like `"NEAR OCEAN"`, '
                                '`"ISLAND"`, `"San Francisco"`, `"Medium"`.\n'
                                '2. **Missing Observations**: Null entries, NaNs, sentinel values (`-999`, `"N/A"`).\n'
                                '3. **Disparate Physical Scales**: A feature like `total_rooms` measured in thousands '
                                '($10^3$) juxtaposed with `median_income` measured in tens ($10^1$).\n'
                                '4. **Outliers & Heavy Tails**: Log-normal distributions with extreme values that '
                                'destabilize gradient optimization.\n'
                                '\n'
                                'Data preparation is the architectural bridge that converts raw, messy real-world '
                                'tables into standardized numerical feature spaces.\n'
                                '\n'
                                '```\n'
                                'Raw Real-World Table:\n'
                                '+---------+----------+-------------+---------------+--------------------+\n'
                                '| Income  | Bedrooms | Total Rooms | Ocean Prox    | Median House Value |\n'
                                '+---------+----------+-------------+---------------+--------------------+\n'
                                '| 8.32    | 129.0    | 880.0       | NEAR BAY      | 452600.0           |\n'
                                '| 3.87    | NaN      | 7099.0      | INLAND        | 358500.0           |\n'
                                '| 1.68    | 342.0    | 1467.0      | <1H OCEAN     | 104200.0           |\n'
                                '+---------+----------+-------------+---------------+--------------------+\n'
                                '                                |\n'
                                '                                v  Data Preprocessing Pipeline\n'
                                '+-----------------------------------------------------------------------+\n'
                                '|  1. Impute NaNs (Median / Mode)                                       |\n'
                                '|  2. Encode Categoricals (One-Hot / Ordinal)                           |\n'
                                '|  3. Scale Numerics (StandardScaler / RobustScaler)                    |\n'
                                '+-----------------------------------------------------------------------+\n'
                                '                                |\n'
                                '                                v\n'
                                'Pure Numerical Design Matrix X in R^(n x d) -> Ready for ML Model\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.2 The Hook: The "Fake-Good Scores" Phenomenon\n'
                                '\n'
                                'In traditional software development, bugs reveal themselves through compiler errors, '
                                'syntax crashes, or runtime stack traces. **In Machine Learning, preprocessing bugs do '
                                'not look like code bugs. They look like suspiciously perfect scores.**\n'
                                '\n'
                                '> **The Production Failure Pattern**:\n'
                                '> An engineer prepares a dataset, trains a model, and reports a stellar $98.5\\%$ '
                                'accuracy or a near-zero RMSE on the test set. The model is shipped to production. '
                                'Within 48 hours, live production accuracy plummets to $61.2\\%$. \n'
                                '> \n'
                                '> What happened? The model did not discover a brilliant predictive pattern. The '
                                'engineer accidentally allowed test set information to **leak** into the training '
                                'preprocessing steps, giving the model an illegal preview of the exam answers during '
                                'study time.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.3 The Fundamental Preprocessing Law\n'
                                '\n'
                                '$$\\mathbf{Rule}: \\quad \\text{Every statistical parameter } \\theta \\in \\{\\mu, '
                                '\\sigma, \\text{median}, \\text{min}, \\text{max}, \\text{vocabulary}\\} \\text{ must '
                                'be estimated exclusively from } \\mathbf{X}_{\\text{train}}.$$\n'
                                '\n'
                                'At inference time, the frozen transformation parameters learned from the training '
                                'fold must be applied directly to the test fold (or live production requests). Under '
                                'no circumstances should `.fit()` ever be executed on test data.',
                        'citations': [   'Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. (2012). Leakage in '
                                         'data mining: Formulation, detection, and avoidance. ACM Transactions on '
                                         'Knowledge Discovery from Data, 6(4), 1-21.',
                                         'Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn, Keras, and '
                                         "TensorFlow (3rd ed.). O'Reilly Media, Chapter 2."],
                        'heading': "1. The Data Preparation Imperative & The 'Fake-Good Scores' Trap",
                        'section_id': 'cml-l02-sec01'},
                    {   'body': '### 2.1 Formal Definition of Data Leakage\n'
                                '\n'
                                '**Data Leakage** occurs when information from outside the training dataset is used to '
                                'create or tune the model. This leads to overly optimistic performance estimates '
                                'during development and catastrophic generalization failure in production.\n'
                                '\n'
                                '```\n'
                                '       +-------------------------------------------------------------+\n'
                                '       |                  The Train / Test Firewall                  |\n'
                                '       +-------------------------------------------------------------+\n'
                                '       |                                                             |\n'
                                '       |     [ TRAINING FOLD (80%) ]       |   [ TEST HOLDOUT (20%) ]|\n'
                                '       |     - Compute Mean (mu)           |   - DO NOT compute mu   |\n'
                                '       |     - Compute Std (sigma)         |   - Borrow mu_train     |\n'
                                '       |     - Compute Median Impute       |   - Borrow median_train |\n'
                                '       |     - Fit Encoders                |   - Borrow enc_train    |\n'
                                '       |                                   |                         |\n'
                                '       |     =====> FIT TRANSFORM =====>   |   =====> TRANSFORM ONLY |\n'
                                '       +-------------------------------------------------------------+\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.2 Complete Taxonomy of Data Leakage\n'
                                '\n'
                                '| Leakage Category | Manifestation Mechanism | Concrete Example | Architectural '
                                'Prevention |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **Preprocessing Leakage** | Summary statistics calculated across full $X$ before '
                                'partitioning. | Calling `StandardScaler().fit_transform(X)` on all 20,000 rows prior '
                                'to `train_test_split`. | Execute `train_test_split` **first**. Fit transformers '
                                'strictly on $X_{\\text{train}}$. |\n'
                                '| **Target Leakage** | Feature contains information only available *after* the target '
                                'occurs. | Predicting patient hospital readmission using a feature `"Discharge Summary '
                                'Prepared"`. | Apply the Golden Prediction-Time Test: Drop proxy features created '
                                'downstream of the label. |\n'
                                '| **Temporal / Lookahead Leakage** | Randomly shuffling time-dependent data, allowing '
                                'past predictions to peek at future data. | Random split on stock price data where '
                                "Monday's model is trained on Friday's closing prices. | Enforce chronological "
                                'walk-forward splitting (`TimeSeriesSplit`). Never randomly shuffle temporal '
                                'sequences. |\n'
                                '| **Group / Clustered Leakage** | Multiple observations from the same entity appear '
                                'in both train and test splits. | Training on MRI scans where patient P101 has 3 scans '
                                'in train and 2 scans in test. | Deploy `GroupKFold` or `GroupShuffleSplit` '
                                'partitioned by entity ID (Patient, Device, User). |\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.3 The Golden Prediction-Time Test\n'
                                '\n'
                                'Whenever evaluating whether a feature is safe to include in a model pipeline, apply '
                                'this deterministic operational test:\n'
                                '\n'
                                '> **The Prediction-Time Test**:\n'
                                '> *"At the exact microsecond this inference request executes on the production '
                                'server, will this exact feature value already be recorded and genuinely accessible in '
                                'the database?"*\n'
                                '> \n'
                                '> If the answer is "No" (e.g., the feature is generated during or after the event '
                                'occurs), the feature constitutes **Target Leakage** and must be deleted from the '
                                'feature matrix.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.4 Safe vs. Unsafe Operations Before Train/Test Split\n'
                                '\n'
                                '```\n'
                                'SAFE Before Split:\n'
                                '[x] Dropping rows where the target y is NaN (target cleaning)\n'
                                '[x] Removing duplicate records\n'
                                "[x] Domain-driven fixed cuts: pd.cut(df['income'], bins=[-inf, 2.5, 4.5, inf])\n"
                                '\n'
                                'UNSAFE Before Split (LEAKAGE):\n'
                                '[!] StandardScaler().fit(X) or fit_transform(X)\n'
                                "[!] SimpleImputer(strategy='median').fit(X)\n"
                                '[!] OneHotEncoder().fit(X) (leaks test-set category vocabulary)\n'
                                "[!] Quantile binning: pd.qcut(df['income'], q=4) (computes empirical quantiles from "
                                'test data)\n'
                                '[!] Outlier filtering based on full-dataset mean +/- 3*sigma\n'
                                '```\n'
                                '\n'
                                '#### Code Implementation: Strict Hygiene Protocol\n'
                                '```python\n'
                                'from sklearn.model_selection import train_test_split\n'
                                '\n'
                                '# STEP 1: Clean target labels if missing (Safe before split)\n'
                                'df_clean = df.dropna(subset=["median_house_value"]).copy()\n'
                                '\n'
                                'X = df_clean.drop(columns=["median_house_value"])\n'
                                'y = df_clean["median_house_value"]\n'
                                '\n'
                                '# STEP 2: Partition IMMEDIATELY before computing any feature statistics\n'
                                'X_train, X_test, y_train, y_test = train_test_split(\n'
                                '    X, y, test_size=0.20, random_state=42, stratify=None\n'
                                ')\n'
                                '# Note: Use stratify=y for imbalanced classification tasks!\n'
                                '```',
                        'citations': [   'Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of '
                                         'Statistical Learning (2nd ed.). Springer, Chapter 7.',
                                         'Kaufman, S. et al. (2012). Leakage in data mining: Formulation, detection, '
                                         'and avoidance.'],
                        'heading': '2. Taxonomy of Data Leakage & Train/Test Hygiene',
                        'section_id': 'cml-l02-sec02'},
                    {   'body': '### 3.1 Nominal vs. Ordinal Categorical Variables\n'
                                '\n'
                                'Categorical variables represent qualitative states and must be mapped to numbers. '
                                'However, applying the wrong mathematical representation creates catastrophic '
                                'geometric distortions:\n'
                                '\n'
                                '| Categorical Type | Intrinsic Ordering | Examples | Proper Encoding Method | Danger '
                                'of Mis-encoding |\n'
                                '| :--- | :--- | :--- | :--- | :--- |\n'
                                '| **Nominal** | **None** (Categories are mutually disjoint with zero natural '
                                'hierarchy). | `ocean_proximity` (`INLAND`, `NEAR OCEAN`, `ISLAND`), City, Blood Type, '
                                'Color. | **One-Hot Encoding** (`OneHotEncoder`). | Arbitrary integer encoding (0, 1, '
                                '2) invents fake distances: assumes `ISLAND` (2) is twice as large as `NEAR OCEAN` '
                                '(1). |\n'
                                '| **Ordinal** | **Strict Natural Order** (Magnitude hierarchy exists, though spacing '
                                'may be unequal). | `shirt_size` (`S < M < L < XL`), `income_band` (`low < mid < '
                                'high`), Education Level. | **Ordinal Encoding** (`OrdinalEncoder`) with explicit '
                                'category ordering. | One-hot encoding discards valuable monotonic ranking '
                                'information. |\n'
                                '\n'
                                '```\n'
                                'The Geometric Distortion of Arbitrary Label Encoding on Nominal Features:\n'
                                'If we assign: Red = 0, Green = 1, Blue = 2:\n'
                                '   Euclidean Distance(Red, Green) = |0 - 1| = 1\n'
                                '   Euclidean Distance(Red, Blue)  = |0 - 2| = 2\n'
                                'The linear model assumes Blue is mathematically twice as "far" from Red as Green is!\n'
                                'This geometric bias distorts Linear Models, Ridge/Lasso, KNN, and Neural Networks.\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.2 One-Hot Encoding & The Dummy Variable Trap\n'
                                '\n'
                                'One-Hot Encoding maps a nominal categorical feature with $K$ unique levels into $K$ '
                                'binary indicator columns:\n'
                                '\n'
                                '$$x_i = \\text{"NEAR BAY"} \\implies \\begin{bmatrix} x_{\\text{INLAND}} \\\\ '
                                'x_{\\text{ISLAND}} \\\\ x_{\\text{NEAR BAY}} \\\\ x_{\\text{NEAR OCEAN}} '
                                '\\end{bmatrix} = \\begin{bmatrix} 0 \\\\ 0 \\\\ 1 \\\\ 0 \\end{bmatrix}$$\n'
                                '\n'
                                '#### The Dummy Variable Trap (Multicollinearity)\n'
                                'In an unregularized Ordinary Least Squares (OLS) linear regression model with an '
                                'intercept term $\\beta_0$, retaining all $K$ binary columns introduces **perfect '
                                'multicollinearity**:\n'
                                '$$\\sum_{k=1}^K x_{\\text{dummy}, k} = 1.0 = \\mathbf{1}$$\n'
                                'The design matrix $\\mathbf{X}$ is not full column rank, rendering $\\mathbf{X}^T '
                                '\\mathbf{X}$ non-invertible.\n'
                                "- **The Classical Solution**: Drop one category (`drop='first'`), resulting in $K-1$ "
                                'degrees of freedom. The dropped category becomes the baseline reference.\n'
                                '- **The Modern ML Rule**: In regularized linear models (Ridge, Lasso, ElasticNet) and '
                                'tree ensembles (Random Forest, XGBoost), **keep all $K$ columns** (`drop=None`). '
                                'Regularization penalizes weights and resolves the singularity, while symmetric '
                                'encoding improves interpretability.\n'
                                '\n'
                                '#### Out-of-Vocabulary (OOV) Robustness at Inference\n'
                                'When deploying to production, a test record may contain a previously unseen category '
                                '(e.g., `ocean_proximity = "ARCTIC"`).\n'
                                '- By default, standard encoders throw a runtime exception (`ValueError: Found unknown '
                                'categories`).\n'
                                "- **Scikit-Learn Solution**: Initialize `OneHotEncoder(handle_unknown='ignore')`. "
                                'This silently encodes the unseen category as an **all-zeros row** $\\begin{bmatrix} 0 '
                                '& 0 & 0 & 0 \\end{bmatrix}^T$, allowing inference to proceed seamlessly without '
                                'crashing.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.3 Ordinal Encoding Implementation\n'
                                '\n'
                                'Ordinal features require explicit declaration of category ordering during '
                                'instantiation:\n'
                                '\n'
                                '```python\n'
                                'from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder\n'
                                '\n'
                                '# 1. Nominal Encoding with OOV Safety\n'
                                "ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)\n"
                                "X_train_nom = ohe.fit_transform(X_train[['ocean_proximity']])\n"
                                "X_test_nom = ohe.transform(X_test[['ocean_proximity']])\n"
                                '\n'
                                '# 2. Ordinal Encoding with Explicit Monotonic Hierarchy\n'
                                "ord_enc = OrdinalEncoder(categories=[['low', 'mid', 'high']])\n"
                                "X_train_ord = ord_enc.fit_transform(X_train[['income_band']])\n"
                                "X_test_ord = ord_enc.transform(X_test[['income_band']])\n"
                                '```',
                        'citations': [   'Micci-Barreca, D. (2001). A preprocessing scheme for high-cardinality '
                                         'categorization predictors in data mining. ACM SIGKDD Explorations, 3(1), '
                                         '27-32.',
                                         'Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python.'],
                        'heading': '3. Categorical Feature Encoding: Nominal vs. Ordinal Mechanics',
                        'section_id': 'cml-l02-sec03'},
                    {   'body': '### 4.1 Why Algorithm Sensitivity Depends on Feature Scale\n'
                                '\n'
                                'Different machine learning model families exhibit starkly different mathematical '
                                'responses to feature magnitudes:\n'
                                '\n'
                                '```\n'
                                'Distance-Based Distortion (KNN / K-Means / SVM):\n'
                                '   Point A: Income = 50,000 USD, Age = 25\n'
                                '   Point B: Income = 52,000 USD, Age = 45\n'
                                '   Euclidean Distance = sqrt( (52000 - 50000)^2 + (45 - 25)^2 )\n'
                                '                      = sqrt( 4,000,000 + 400 ) = sqrt( 4,000,400 ) approx 2000.1\n'
                                '   The Age difference (20 years) is completely drowned out by Income ($2000)!\n'
                                '```\n'
                                '\n'
                                '#### 1. Distance-Based Algorithms (KNN, K-Means, SVM, PCA)\n'
                                'Calculate distances using the Euclidean metric $d(\\mathbf{x}_1, \\mathbf{x}_2) = '
                                '\\sqrt{\\sum_{j=1}^d (x_{1,j} - x_{2,j})^2}$. Features with large raw numerical '
                                'ranges (`total_rooms` $\\in [100, 30000]$) dominate the metric tensor, rendering '
                                'small-scale features (`median_income` $\\in [0.5, 15.0]$) mathematically invisible.\n'
                                '\n'
                                '#### 2. Gradient Descent Optimizers (Logistic Regression, Neural Nets)\n'
                                'When feature scales differ drastically, the loss landscape contours form highly '
                                'elongated, eccentric ellipses. Gradient vectors oscillate perpendicular to the '
                                'optimal trajectory, demanding painfully small learning rates. Scaling spherizes the '
                                'loss surface, enabling direct, rapid descent toward the global minimum.\n'
                                '\n'
                                '```\n'
                                'Unscaled Features (Elongated Ellipse):            Scaled Features (Spherical '
                                'Contours):\n'
                                '         w_2 ^                                            w_2 ^\n'
                                '             |      /---------\\                               |       /-----\\\n'
                                '             |     /     |     \\                              |      /   |   \\\n'
                                '             |    /  <---|--->  \\                             |     | <--+--> |\n'
                                '             |    \\      |      /                             |      \\   |   /\n'
                                '             |     \\-----------/                              |       \\-----/\n'
                                '             +--------------------> w_1                       +--------------------> '
                                'w_1\n'
                                '       Oscillatory zigzagging path                      Direct radial descent path\n'
                                '```\n'
                                '\n'
                                '#### 3. Regularized Models (Ridge $L_2$, Lasso $L_1$)\n'
                                'Regularization appends a penalty $\\lambda \\sum w_j^2$ or $\\lambda \\sum |w_j|$ to '
                                'the objective function. Unscaled features with tiny numerical values require massive '
                                'weights $w_j$ to exert predictive impact; the regularization penalty '
                                'disproportionately shrinks these weights, biasing the model against unscaled '
                                'features.\n'
                                '\n'
                                '#### 4. Scale-Invariant Models: Decision Trees\n'
                                'Decision Trees, Random Forests, and Gradient Boosting evaluate splits purely on '
                                'rank-order thresholds ($x_j \\le \\tau$). Because any monotonic transformation '
                                'preserves order, **tree models are completely scale-invariant**.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.2 Mathematical Comparison of Numerical Scalers\n'
                                '\n'
                                '| Scaler Name | Mathematical Formulation | Center & Scale Statistics | Primary Use '
                                'Case & Sensitivity |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **StandardScaler (Z-Score)** | $$z = \\frac{x - \\mu}{\\sigma}$$ | Mean $\\mu = 0$, '
                                'Variance $\\sigma^2 = 1$ | Default choice for linear models, logistic regression, '
                                'PCA. Assumes roughly Gaussian-like distributions. **Highly sensitive to extreme '
                                'outliers**. |\n'
                                '| **MinMaxScaler** | $$x_{\\text{norm}} = \\frac{x - x_{\\text{min}}}{x_{\\text{max}} '
                                '- x_{\\text{min}}}$$ | Bounds data to $[0, 1]$ (or $[a, b]$) | Neural networks, image '
                                'processing, bounded bounded ranges. **Extremely sensitive to outliers** (one huge '
                                'outlier compresses all other data into $[0, 0.05]$). |\n'
                                '| **RobustScaler** | $$x_{\\text{rob}} = \\frac{x - '
                                'Q_2(\\mathbf{x})}{Q_3(\\mathbf{x}) - Q_1(\\mathbf{x})} = \\frac{x - '
                                '\\text{median}}{\\text{IQR}}$$ | Centered at Median, scaled by Interquartile Range '
                                '(IQR) | **Heavy-tailed distributions with severe outliers**. Outliers do not '
                                'influence the median or IQR. |\n'
                                '\n'
                                '```python\n'
                                'from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler\n'
                                '\n'
                                '# ALWAYS fit on train, transform test\n'
                                'scaler = StandardScaler()\n'
                                'X_train_scaled = scaler.fit_transform(X_train[num_cols])\n'
                                'X_test_scaled = scaler.transform(X_test[num_cols])  # Uses mu_train and sigma_train!\n'
                                '```',
                        'citations': [   'Ioffe, S., & Szegedy, C. (2015). Batch normalization: Accelerating deep '
                                         'network training by reducing internal covariate shift. ICML.',
                                         'Rousseeuw, P. J., & Croux, C. (1993). Alternatives to the median absolute '
                                         'deviation. Journal of the American Statistical Association, 88(424), '
                                         '1273-1283.'],
                        'heading': '4. Numerical Feature Scaling: Standard, Min-Max & Robust Transformations',
                        'section_id': 'cml-l02-sec04'},
                    {   'body': "### 5.1 The Missing Data Taxonomy (Rubin's Framework)\n"
                                '\n'
                                'Before imputing missing values, an engineer must diagnose the underlying statistical '
                                'mechanism driving the missingness:\n'
                                '\n'
                                '1. **Missing Completely at Random (MCAR)**: The probability of missingness is '
                                'entirely independent of observed and unobserved data: $P(M \\mid Y_{\\text{obs}}, '
                                'Y_{\\text{mis}}) = P(M)$. Example: A blood sample test tube accidentally drops and '
                                'shatters on the laboratory floor.\n'
                                '2. **Missing at Random (MAR)**: Missingness depends systematically on observed '
                                'features, but not on the missing value itself: $P(M \\mid Y_{\\text{obs}}, '
                                'Y_{\\text{mis}}) = P(M \\mid Y_{\\text{obs}})$. Example: In a survey, men may report '
                                'income less frequently, but among men, missingness is unrelated to the actual income '
                                'level.\n'
                                '3. **Missing Not at Random (MNAR)**: Missingness depends directly on the unobserved '
                                'value itself: $P(M \\mid Y_{\\text{obs}}, Y_{\\text{mis}}) = P(M \\mid '
                                'Y_{\\text{mis}})$. Example: Individuals with extremely high income systematically '
                                'refuse to disclose their salary.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.2 Imputation Strategies & Trade-offs\n'
                                '\n'
                                '| Strategy | Scikit-Learn Class | When to Use | Trade-offs & Risks |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                "| **Drop Rows (Complete Case)** | `df.dropna(subset=['col'])` | Negligible "
                                'missingness ($< 1-2\\%$), confirmed MCAR. | **Fatal at Inference**: If a live user '
                                'sends a request missing that field, the production API cannot drop the user and '
                                'crashes. |\n'
                                "| **Drop Column** | `df.drop(columns=['col'])` | Column is $> 70-80\\%$ null and "
                                'offers zero unique predictive signal. | Permanently destroys potentially vital '
                                'signals. |\n'
                                "| **Mean Imputation** | `SimpleImputer(strategy='mean')` | Strictly symmetric, "
                                'Gaussian numeric distributions without outliers. | Artificially reduces variance, '
                                'underestimates standard errors, and distorts covariance structures. |\n'
                                "| **Median Imputation** | `SimpleImputer(strategy='median')` | **Default choice for "
                                'skewed numeric features with outliers**. | Robust to extreme values; preserves '
                                'distributional median. |\n'
                                "| **Mode Imputation** | `SimpleImputer(strategy='most_frequent')` | Categorical and "
                                'discrete features. | Can amplify majority class imbalance. |\n'
                                '| **Missing Indicator** | `SimpleImputer(add_indicator=True)` | When missingness '
                                'itself carries informative predictive signal. | Appends binary column '
                                '$\\mathbb{I}(x_{ij} = \\text{NaN})$, allowing models to learn the pattern of absence. '
                                '|\n'
                                '\n'
                                '```\n'
                                'The Distortion of Mean vs. Median Imputation under Skewness:\n'
                                '   Raw Sample with Outlier: [ 20, 22, 21, 24, 23, 22, 500 ] (e.g., California rooms)\n'
                                '   Median = 22.0  <--- Representative typical value\n'
                                '   Mean   = 90.3  <--- Pulled massively by the single 500 outlier!\n'
                                'Filling missing values with 90.3 injects high-bias fictitious data into the training '
                                'set.\n'
                                '```\n'
                                '\n'
                                '#### Code Implementation: Safe Imputation Protocol\n'
                                '```python\n'
                                'from sklearn.impute import SimpleImputer\n'
                                '\n'
                                '# Instantiate imputer\n'
                                'imputer = SimpleImputer(strategy="median", add_indicator=True)\n'
                                '\n'
                                '# Fit on TRAIN ONLY\n'
                                'X_train_imputed = imputer.fit_transform(X_train[num_cols])\n'
                                '\n'
                                '# Transform TEST using train medians\n'
                                'X_test_imputed = imputer.transform(X_test[num_cols])\n'
                                '```',
                        'citations': [   'Little, R. J., & Rubin, D. B. (2019). Statistical Analysis with Missing Data '
                                         '(3rd ed.). John Wiley & Sons.',
                                         'Van Buuren, S. (2018). Flexible Imputation of Missing Data. CRC Press.'],
                        'heading': '5. Missing Value Imputation: Mechanisms, Trade-offs & Hygiene',
                        'section_id': 'cml-l02-sec05'},
                    {   'body': '### 6.1 The "Locked Train Stats Box" Architecture\n'
                                '\n'
                                'Manual preprocessing requires orchestrating dozens of separate imputers, scalers, and '
                                'encoders. In production, this ad-hoc workflow inevitably leads to leakage bugs or '
                                'training-serving skew.\n'
                                '\n'
                                'Scikit-Learn solves this via **`ColumnTransformer`** and **`Pipeline`**:\n'
                                '- **`ColumnTransformer`**: Directs column subsets (numeric, nominal, ordinal) to '
                                'distinct transformation sub-pipelines.\n'
                                '- **`Pipeline`**: Combines the preprocessing transformers with an estimator into a '
                                'single, cohesive, atomic object.\n'
                                '\n'
                                '```\n'
                                '                        The Scikit-Learn Monolithic Pipeline:\n'
                                '+---------------------------------------------------------------------------------------+\n'
                                '|  '
                                'ColumnTransformer:                                                                   '
                                '|\n'
                                '|   +-- Numeric Cols ----> [ SimpleImputer(median) ] ----> [ StandardScaler() ] '
                                '------+ |\n'
                                '|   |                                                                                 '
                                '| |\n'
                                '|   +-- Nominal Cols ----> [ SimpleImputer(mode) ] ------> [ OneHotEncoder(ignore) ] '
                                '-+ |\n'
                                '|   |                                                                                 '
                                '| |\n'
                                '|   +-- Ordinal Cols ----> [ SimpleImputer(mode) ] ------> [ OrdinalEncoder(...) ] '
                                '---+ |\n'
                                '+-------------------------------------------------------------------------------------|-+\n'
                                '                                                                                      '
                                '| Concatenated\n'
                                '                                                                                      '
                                'v Matrix\n'
                                '                                                                     [ Ridge '
                                'Regression ]\n'
                                '```\n'
                                '\n'
                                'When you execute `pipeline.fit(X_train, y_train)`:\n'
                                '1. Every statistical parameter (medians, means, standard deviations, categorical '
                                'vocabularies) is estimated **strictly from `X_train`**.\n'
                                "2. All parameters are stored internally in the pipeline's estimator state "
                                '(`named_steps`).\n'
                                '3. Calling `pipeline.predict(X_test)` transforms test data using the frozen training '
                                'statistics and outputs predictions. **Data leakage becomes structurally '
                                'impossible.**\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 6.2 Complete End-to-End Implementation\n'
                                '\n'
                                '```python\n'
                                'import numpy as np\n'
                                'import pandas as pd\n'
                                'from sklearn.model_selection import train_test_split\n'
                                'from sklearn.compose import ColumnTransformer\n'
                                'from sklearn.pipeline import Pipeline\n'
                                'from sklearn.impute import SimpleImputer\n'
                                'from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder\n'
                                'from sklearn.linear_model import Ridge\n'
                                'from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score\n'
                                '\n'
                                '# 1. Feature Partitioning\n'
                                'num_cols = ["median_income", "housing_median_age", "total_rooms", "total_bedrooms", '
                                '"population", "households"]\n'
                                'nom_cols = ["ocean_proximity"]\n'
                                'ord_cols = ["income_band"]\n'
                                '\n'
                                '# 2. Build Sub-Pipelines\n'
                                'numeric_pipe = Pipeline([\n'
                                '    ("imputer", SimpleImputer(strategy="median")),\n'
                                '    ("scaler", StandardScaler())\n'
                                '])\n'
                                '\n'
                                'nominal_pipe = Pipeline([\n'
                                '    ("imputer", SimpleImputer(strategy="most_frequent")),\n'
                                '    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))\n'
                                '])\n'
                                '\n'
                                'ordinal_pipe = Pipeline([\n'
                                '    ("imputer", SimpleImputer(strategy="most_frequent")),\n'
                                '    ("ordinal", OrdinalEncoder(categories=[["low", "mid", "high"]]))\n'
                                '])\n'
                                '\n'
                                '# 3. Assemble Master ColumnTransformer\n'
                                'preprocessor = ColumnTransformer(transformers=[\n'
                                '    ("num", numeric_pipe, num_cols),\n'
                                '    ("nom", nominal_pipe, nom_cols),\n'
                                '    ("ord", ordinal_pipe, ord_cols)\n'
                                '])\n'
                                '\n'
                                '# 4. Bind Preprocessor and Estimator into Master Pipeline\n'
                                'full_pipeline = Pipeline([\n'
                                '    ("preprocessor", preprocessor),\n'
                                '    ("regressor", Ridge(alpha=1.0))\n'
                                '])\n'
                                '\n'
                                '# 5. Fit Once on Train; Evaluate on Test\n'
                                'full_pipeline.fit(X_train, y_train)\n'
                                'y_pred = full_pipeline.predict(X_test)\n'
                                '\n'
                                'rmse = np.sqrt(mean_squared_error(y_test, y_pred))\n'
                                'mae = mean_absolute_error(y_test, y_pred)\n'
                                'r2 = r2_score(y_test, y_pred)\n'
                                '\n'
                                'print(f"Test RMSE: {rmse:,.2f}")\n'
                                'print(f"Test MAE:  {mae:,.2f}")\n'
                                'print(f"Test R^2:  {r2:.4f}")\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 6.3 The Leakage Detective: Real-World Case Studies\n'
                                '\n'
                                '| Case Study Scenario | Leakage Verdict | Root Cause & Architectural Fix |\n'
                                '| :--- | :--- | :--- |\n'
                                '| **Case 1**: Calculating median of `total_bedrooms` across the entire CSV before '
                                'running `train_test_split`. | **LEAK** | *Preprocessing Leakage*: Test median leaks '
                                'into train fill values. **Fix**: Split first, compute median on `X_train` only. |\n'
                                "| **Case 2**: Splitting first, fitting `OneHotEncoder(handle_unknown='ignore')` on "
                                '`X_train`, transforming `X_test`. | **NO LEAK** | Clean pipeline design. Vocabulary '
                                'learned from train; unseen test categories encoded safely as all-zeros. |\n'
                                '| **Case 3**: Adding `is_high_value = (median_house_value > 200000)` into feature '
                                'matrix $X$ to predict house value. | **LEAK** | *Target Leakage*: Target variable '
                                'explicitly copied into the feature set. **Fix**: Delete label-derived features. |\n'
                                '| **Case 4**: Evaluating credit risk where 20% highest income applicants are manually '
                                'selected into test set. | **LEAK** | *Covariate Shift / Evaluation Bias*: Non-random '
                                'holdout biases metrics. **Fix**: Random stratified or chronological holdout. |',
                        'citations': [   'Buitinck et al. (2013). API design for machine learning software: '
                                         'experiences from the scikit-learn project. ECML PKDD Workshop.',
                                         "Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn. O'Reilly "
                                         'Media.'],
                        'heading': '6. Industrial Pipeline Architecture with Scikit-Learn',
                        'section_id': 'cml-l02-sec06'}],
    'subject_code': 'CML',
    'summary': 'An exhaustive, rigorous masterclass on machine learning data preparation. Covers the mathematical '
               "necessity of preprocessing, the insidious 'fake-good scores' phenomenon of data leakage, nominal vs. "
               'ordinal encoding mechanics, the Dummy Variable Trap, numerical scaling mathematics and gradient '
               'descent geometry, missingness mechanisms (MCAR, MAR, MNAR), and industrial pipeline architecture using '
               "Scikit-Learn's ColumnTransformer and Pipeline.",
    'tags': [   'Data Preprocessing',
                'Data Leakage',
                'Feature Scaling',
                'Categorical Encoding',
                'Imputation',
                'Scikit-Learn',
                'Pipelines',
                'ColumnTransformer'],
    'term': 'Term 5',
    'topic_title': '2. Data Preparation, Feature Preprocessing & Leakage Prevention Pipelines'}

