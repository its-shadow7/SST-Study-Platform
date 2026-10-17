"""
Data definition for data_cml_l11:
"""

L11_DATA = {   'approval_status': 'approved',
    'key_takeaways': [   'Pre-pruning stops growth early using greedy thresholds; Post-pruning (Cost-Complexity '
                         'Pruning) grows a deep tree first and removes subtrees that do not justify their complexity.',
                         'Cost-Complexity Pruning balances training error R(T) against tree size |T| via the cost '
                         'objective R_alpha(T) = R(T) + alpha * |T|.',
                         'As ccp_alpha increases, more subtrees are pruned away, reducing variance and simplifying the '
                         'tree graph.',
                         "Scikit-Learn's CART implementation requires categorical features to be numerically encoded "
                         '(One-Hot or Ordinal) before building split thresholds.',
                         'Feature Importance (MDI) measures the total weighted impurity reduction brought by a feature '
                         'across all splits where it was chosen.',
                         'MDI feature importance is systematically biased toward high-cardinality features (like '
                         'numerical floats or unique IDs); Permutation Importance provides an unbiased validation '
                         'alternative.'],
    'last_updated': '2026-10-18T00:00:00Z',
    'learning_objectives': [   'Contrast pre-pruning stopping rules with post-pruning via Minimal Cost-Complexity '
                               'Pruning (ccp_alpha).',
                               'Extract the effective alpha pruning path using cost_complexity_pruning_path and select '
                               'optimal tree complexity.',
                               'Compare numerical threshold splits against categorical feature encodings in CART '
                               'trees.',
                               'Compute and interpret Mean Decrease in Impurity (MDI) feature importances and diagnose '
                               'high-cardinality bias.',
                               'Build an end-to-end pruned decision tree pipeline on tabular data and rank feature '
                               'drivers.'],
    'note_id': 'cml-t5-l11',
    'quiz': {   'questions': [   {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'Pruning cuts back unnecessary leaf nodes and branches, '
                                                    "simplifying the tree's decision surface to prevent overfitting "
                                                    'and improve generalization on unseen test data.',
                                     'id': 'q-cml-l11-01',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'To increase the training set error to 100%.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'To reduce tree size and structural complexity, '
                                                                'removing branches that fit training noise to improve '
                                                                'out-of-sample generalization.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'To convert the tree into a deep neural network.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'To eliminate the need for training labels.'}],
                                     'question': "What is the primary objective of 'pruning' a Decision Tree?",
                                     'subtopic': 'Pruning Definition',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-3'],
                                     'difficulty': 'easy',
                                     'explanation': 'Pre-pruning halts growth early during recursion (max_depth, '
                                                    'min_samples_leaf). Post-pruning (ccp_alpha) grows a deep tree '
                                                    'first and then prunes back subtrees based on cost-complexity.',
                                     'id': 'q-cml-l11-02',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Setting max_depth = 4.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Setting min_samples_leaf = 15.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'Minimal Cost-Complexity Pruning via ccp_alpha '
                                                                '(growing the full tree first, then removing weak '
                                                                'subtrees).'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Setting min_samples_split = 20.'}],
                                     'question': 'Which of the following represents a Post-Pruning technique rather '
                                                 'than a Pre-Pruning technique?',
                                     'subtopic': 'Pre-Pruning vs Post-Pruning',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'The cost-complexity equation is R_alpha(T) = R(T) + alpha * |T|. '
                                                    'When alpha = 0, there is zero penalty on tree size |T|, leaving '
                                                    'the tree completely unpruned.',
                                     'id': 'q-cml-l11-03',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'The tree collapses to only the root node.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'No pruning occurs; the tree remains fully grown with '
                                                                'maximum depth and unconstrained leaves.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'All features receive exactly zero importance.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The model is converted into Logistic Regression.'}],
                                     'question': 'In Cost-Complexity Pruning, what happens if you set ccp_alpha = 0.0 '
                                                 'in DecisionTreeClassifier?',
                                     'subtopic': 'ccp_alpha Zero Limit',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': "Scikit-Learn tree models expose 'feature_importances_', an array "
                                                    'of floats summing to 1.0 representing the normalized total '
                                                    'reduction in impurity brought by each feature.',
                                     'id': 'q-cml-l11-04',
                                     'options': [   {'id': 'opt-1', 'is_correct': False, 'text': 'coef_'},
                                                    {'id': 'opt-2', 'is_correct': True, 'text': 'feature_importances_'},
                                                    {'id': 'opt-3', 'is_correct': False, 'text': 'tree_weights_'},
                                                    {'id': 'opt-4', 'is_correct': False, 'text': 'alpha_path_'}],
                                     'question': 'In Scikit-Learn, which attribute of a fitted DecisionTreeClassifier '
                                                 'stores the relative importance of each feature?',
                                     'subtopic': 'Feature Importance Attribute',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'easy',
                                     'explanation': 'Feature importances are normalized by the sum of all impurity '
                                                    'decreases across the tree so that they form a valid relative '
                                                    'distribution summing to 1.0.',
                                     'id': 'q-cml-l11-05',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'It equals exactly 1.0 (or 100%).'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'It equals the sample size n.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It equals the maximum depth of the tree.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It can be any arbitrary number.'}],
                                     'question': "What is the sum of all values in a Decision Tree's "
                                                 'feature_importances_ array?',
                                     'subtopic': 'Feature Importance Normalization',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'easy',
                                     'explanation': 'Because feature importance is computed from the cumulative '
                                                    'impurity decreases at splits, a feature that was never split upon '
                                                    'contributes zero impurity reduction and receives an importance of '
                                                    '0.0.',
                                     'id': 'q-cml-l11-06',
                                     'options': [   {'id': 'opt-1', 'is_correct': True, 'text': 'Exactly 0.0'},
                                                    {'id': 'opt-2', 'is_correct': False, 'text': 'Negative 1.0'},
                                                    {'id': 'opt-3', 'is_correct': False, 'text': '0.50'},
                                                    {'id': 'opt-4', 'is_correct': False, 'text': 'Undefined (NaN)'}],
                                     'question': 'If a feature was never selected for any split throughout an entire '
                                                 'Decision Tree, what will its feature_importances_ value be?',
                                     'subtopic': 'Unused Features Importance',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'easy',
                                     'explanation': 'A higher ccp_alpha penalizes each additional leaf node more '
                                                    'heavily in the cost function R_alpha(T) = R(T) + alpha * |T|, '
                                                    'forcing the pruning algorithm to collapse sub-branches into '
                                                    'leaves.',
                                     'id': 'q-cml-l11-07',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'The number of leaves decreases monotonically as '
                                                                'branches are pruned away.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'The number of leaves increases exponentially.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The tree depth doubles.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Alpha has no effect on leaf count.'}],
                                     'question': 'What happens to the number of leaf nodes in a Decision Tree as '
                                                 'ccp_alpha is increased from 0 to a very large positive number?',
                                     'subtopic': 'Increasing Alpha Effect',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'easy',
                                     'explanation': 'Unlike theoretical tree implementations (which can split on '
                                                    'subsets of strings), Scikit-Learn expects continuous numerical '
                                                    'arrays X, requiring One-Hot or Ordinal encoding beforehand.',
                                     'id': 'q-cml-l11-08',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': "Scikit-Learn's underlying CART algorithm "
                                                                'implementation requires numerical floating-point '
                                                                'arrays as input.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Categorical strings violate the laws of probability.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Encoding removes missing values.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Decision trees can only run on ASCII text files.'}],
                                     'question': "Why must categorical string columns (like 'loan_purpose' in "
                                                 "{'education', 'car', 'medical'}) be encoded into numbers before "
                                                 "training with Scikit-Learn's DecisionTreeClassifier?",
                                     'subtopic': 'Encoding Categoricals in CART',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'Because greedy recursive splitting only looks 1 step ahead, early '
                                                    'stopping rules can abort a branch prematurely before it reaches '
                                                    'highly informative feature interaction splits (like in XOR).',
                                     'id': 'q-cml-l11-09',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Trees cannot predict more than 10 days into the '
                                                                'future.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'A pre-pruning stopping rule might halt a split that '
                                                                'has low immediate gain, missing the fact that a '
                                                                'subsequent child split would have yielded massive '
                                                                'classification accuracy.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The computer screen resolution limits tree plotting.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Horizontal decision boundaries are less accurate than '
                                                                'vertical ones.'}],
                                     'question': "What is the 'Horizon Problem' in greedy decision tree construction?",
                                     'subtopic': 'Horizon Problem Explanation',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': '|T| measures tree complexity as the total count of terminal leaf '
                                                    'nodes. Each additional leaf adds a penalty alpha to the cost.',
                                     'id': 'q-cml-l11-10',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'The total number of training samples.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'The number of terminal leaf nodes in the tree.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The square root of the tree depth.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The condition number of the design matrix.'}],
                                     'question': 'In the cost-complexity equation R_alpha(T) = R(T) + alpha * |T|, '
                                                 'what does the term |T| represent?',
                                     'subtopic': 'Cost-Complexity Pruning Formula',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'medium',
                                     'explanation': 'With many unique values, a feature can easily partition small '
                                                    'groups of samples cleanly on the training set, achieving high '
                                                    'apparent impurity reduction even if the feature is completely '
                                                    'random noise.',
                                     'id': 'q-cml-l11-11',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'Features with many unique values provide many '
                                                                'candidate split points, giving the greedy algorithm '
                                                                'more opportunities to find an accidental split that '
                                                                'reduces training impurity by chance.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'High-cardinality features consume more disk space.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Scikit-Learn divides importance by the number of '
                                                                'unique categories.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'MDI is only defined for binary features.'}],
                                     'question': 'Why does Mean Decrease in Impurity (MDI) feature importance give '
                                                 'falsely inflated importance scores to high-cardinality features '
                                                 '(like continuous float IDs or dates)?',
                                     'subtopic': 'High-Cardinality MDI Bias',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'medium',
                                     'explanation': 'Permutation importance is evaluated on validation data. If a '
                                                    'high-cardinality feature was just memorizing training noise, '
                                                    'shuffling it will cause zero drop in validation performance, '
                                                    'correctly scoring its importance near 0.',
                                     'id': 'q-cml-l11-12',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'It evaluates importance on unseen validation/test '
                                                                "data by shuffling a feature's values and measuring "
                                                                'the actual drop in model prediction score.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'It multiplies all feature importances by their '
                                                                'standard deviation.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It forces all features to have equal importance.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It converts decision trees into neural networks.'}],
                                     'question': 'How does Permutation Feature Importance overcome the '
                                                 'high-cardinality bias of default tree MDI importance?',
                                     'subtopic': 'Permutation Importance Advantage',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'medium',
                                     'explanation': "When split into 100 binary columns, a CART tree can only test 'is "
                                                    "title == Nurse?'. Grouping categories requires many sequential "
                                                    'splits down a single path, inflating depth and diluting the '
                                                    "category's overall signal.",
                                     'id': 'q-cml-l11-13',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'One-hot encoding creates 100 sparse binary features; '
                                                                'the tree can only test one title at a time, resulting '
                                                                'in deep, unbalanced trees and fragmented feature '
                                                                'importances.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Decision trees crash when input features contain 0s '
                                                                'and 1s.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'One-hot encoding converts the tree into a linear '
                                                                'regression model.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It eliminates the need for computing Gini impurity.'}],
                                     'question': 'What is a potential disadvantage of One-Hot Encoding a '
                                                 'high-cardinality categorical feature (e.g., 100 job titles) before '
                                                 'feeding it to a Decision Tree?',
                                     'subtopic': 'One-Hot vs Ordinal in Trees',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'The pruning path returns the exact sequence of alpha thresholds '
                                                    'where the weakest link in the tree is pruned, allowing efficient '
                                                    'grid search over the finite set of unique subtrees.',
                                     'id': 'q-cml-l11-14',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'A dictionary containing the final test set accuracy.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'An array of effective ccp_alphas (the critical '
                                                                'threshold values where subtrees collapse) and their '
                                                                'corresponding total leaf impurities.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'A list of dropped feature names.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The tree depth plotted on a log scale.'}],
                                     'question': 'What does the function clf.cost_complexity_pruning_path(X_train, '
                                                 'y_train) return?',
                                     'subtopic': 'Pruning Path Extraction',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'medium',
                                     'explanation': 'The formula weights Delta I(t) by n_t / N. A split at the root '
                                                    'partitions all N samples (weight = 1.0), whereas a split at depth '
                                                    '8 might only affect 10 samples (weight = 10 / N).',
                                     'id': 'q-cml-l11-15',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'Impurity reduction at each split is weighted by the '
                                                                'fraction of total training samples reaching that node '
                                                                '(n_t / N); root splits affect 100% of samples.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Root splits are always computed using entropy while '
                                                                'leaf splits use Gini.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Root splits are assigned an arbitrary 5x multiplier '
                                                                'by Scikit-Learn.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Leaves cannot compute impurity.'}],
                                     'question': 'Why do splits located near the root of a Decision Tree generally '
                                                 "contribute more to a feature's MDI importance than splits located "
                                                 'near the bottom leaves?',
                                     'subtopic': 'Top Node Influence',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'Selecting alpha on training data would always pick alpha = 0 '
                                                    '(unpruned). Optimal alpha must be selected by evaluating '
                                                    'generalization performance on validation data or '
                                                    'cross-validation.',
                                     'id': 'q-cml-l11-16',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Choose the alpha that achieves the highest accuracy '
                                                                'on the training set.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Choose the alpha that achieves the highest accuracy '
                                                                'on a validation set (or via cross-validation).'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Choose the largest possible alpha to minimize code '
                                                                'size.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Choose alpha = 0.50 by default.'}],
                                     'question': 'When tuning ccp_alpha across candidate values, how should the '
                                                 'optimal alpha be selected?',
                                     'subtopic': 'Pruning Selection Criterion',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'Breiman defines the weakest link as the node t that minimizes '
                                                    'g(t), which measures the rate of increase in error per leaf '
                                                    'eliminated if branch T_t is collapsed into node t.',
                                     'id': 'q-cml-l11-17',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'It is the sub-tree that minimizes the effective cost '
                                                                'per leaf: g(t) = (R(t) - R(T_t)) / (|T_t| - 1), '
                                                                'representing the smallest impurity increase per leaf '
                                                                'removed.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'It is the sub-tree located on the far left side of '
                                                                'the graph.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It is the branch with the fewest total characters in '
                                                                'its feature names.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It is chosen randomly.'}],
                                     'question': "In Breiman's Cost-Complexity Pruning algorithm, how is the 'weakest "
                                                 "link' sub-tree defined at each pruning step?",
                                     'subtopic': 'Weakest Link Pruning',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1', 'opt-2', 'opt-4'],
                                     'difficulty': 'hard',
                                     'explanation': 'Options 1, 2, and 4 are correct. Option 3 is false: permutation '
                                                    'importance uses the already-fitted model; it simply shuffles a '
                                                    'column in the validation set and runs forward prediction.',
                                     'id': 'q-cml-l11-18',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'Pruning a tree decreases training accuracy but '
                                                                'frequently increases test accuracy.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Features that are correlated with a top predictor may '
                                                                'receive near-zero MDI importance if the top predictor '
                                                                'is chosen first and masks their gain.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Permutation importance requires retraining the '
                                                                'decision tree from scratch for every feature.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': True,
                                                        'text': 'The sequence of pruned sub-trees generated by '
                                                                'increasing ccp_alpha is strictly nested: T_0 superset '
                                                                'T_1 superset T_2.'}],
                                     'question': 'Which of the following statements represent true properties of '
                                                 'Cost-Complexity Pruning and Feature Importance?',
                                     'subtopic': 'Pruning and Importance Invariants',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'Once a tree splits on x1, the impurity reduction is captured. In '
                                                    'descendant nodes, x2 provides no new independent information '
                                                    'gain, resulting in a misleadingly low importance score for x2 '
                                                    'despite its true predictive power.',
                                     'id': 'q-cml-l11-19',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'It splits on whichever feature provides slightly '
                                                                'higher gain at the top node, giving it high '
                                                                'importance, while the redundant feature receives '
                                                                'near-zero importance because its gain is masked.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'It divides the importance score exactly 50-50 between '
                                                                'x1 and x2.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It deletes both features.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It forces both importances to 1.0.'}],
                                     'question': 'Suppose features x1 and x2 are 99% correlated and equally '
                                                 'predictive. How does an individual Decision Tree typically assign '
                                                 'MDI feature importance to them?',
                                     'subtopic': 'Correlation Masking in MDI',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'When alpha -> inf, the penalty term alpha * |T| dominates. To '
                                                    'minimize cost, the tree collapses to the minimum possible number '
                                                    'of leaves (|T| = 1), which is the single root node.',
                                     'id': 'q-cml-l11-20',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'A trivial single-node tree (just the root node) that '
                                                                'predicts the global majority class of the training '
                                                                'set for all queries.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'A tree with infinite depth.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'An empty graph with 0 nodes.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'A complete binary tree with 2^d leaves.'}],
                                     'question': 'What is the structure of a Decision Tree as ccp_alpha approaches '
                                                 'positive infinity (alpha -> infinity)?',
                                     'subtopic': 'Infinite Alpha Limit',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'MDI is computed on training splits and is prone to overfitting. A '
                                                    'large drop between training MDI and validation permutation '
                                                    'importance is a definitive indicator of an overfitted feature.',
                                     'id': 'q-cml-l11-21',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'The feature was overfitted to training data: it '
                                                                'provided many splits that reduced training impurity '
                                                                'but has virtually zero real predictive power on '
                                                                'unseen data.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'The validation set was corrupted.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Permutation importance cannot be used on time '
                                                                'features.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The model has high bias.'}],
                                     'question': "A model has a feature 'Transaction_Hour' with MDI importance = 0.35, "
                                                 'but Permutation Importance = 0.01 on validation data. What does this '
                                                 'discrepancy indicate?',
                                     'subtopic': 'MDI vs Permutation Discrepancy',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'Linear models explain outcomes via linear additive effects '
                                                    '(ceteris paribus). Trees explain outcomes via hierarchical '
                                                    "logical conjunctions: 'IF credit > 700 AND income > 50k THEN "
                                                    "Approve'.",
                                     'id': 'q-cml-l11-22',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'Linear models provide global additive feature weights '
                                                                '(w_j is the marginal slope holding others fixed); '
                                                                'Decision Trees provide local conditional rule paths '
                                                                '(if A and B then C).'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Decision trees can only be interpreted using neural '
                                                                'network activation maps.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Linear models are impossible to interpret.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'There is no difference.'}],
                                     'question': 'How does the interpretability of a shallow Decision Tree differ from '
                                                 'the interpretability of a Linear Regression model?',
                                     'subtopic': 'Tree vs Linear Model Interpretability',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1', 'opt-2', 'opt-4'],
                                     'difficulty': 'hard',
                                     'explanation': 'Options 1, 2, and 4 are major advantages. Option 3 is false: '
                                                    'post-pruning requires growing a full unconstrained tree first and '
                                                    'evaluating candidate alphas, which is computationally more '
                                                    'demanding than early stopping.',
                                     'id': 'q-cml-l11-23',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'Post-pruning allows the tree to explore complex '
                                                                'non-linear feature interactions before deciding which '
                                                                'branches to retain.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Post-pruning can produce non-symmetric trees where '
                                                                'informative branches are deep while uninformative '
                                                                'branches are pruned shallow.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Post-pruning is computationally faster than '
                                                                'pre-pruning during training.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': True,
                                                        'text': 'Setting a rigid max_depth chops all branches at the '
                                                                'same depth regardless of their individual predictive '
                                                                'value.'}],
                                     'question': 'Which of the following are advantages of Cost-Complexity '
                                                 'Post-Pruning over simple max_depth Pre-Pruning?',
                                     'subtopic': 'Pre-Pruning vs Post-Pruning Tradeoffs',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': "Breiman's 1-SE rule applies Occam's Razor: among models with "
                                                    'statistically indistinguishable cross-validation performance '
                                                    '(within 1 SE), choose the most parsimonious (simplest/most '
                                                    'pruned) model.',
                                     'id': 'q-cml-l11-24',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'Select the simplest (most heavily pruned / largest '
                                                                'alpha) tree whose cross-validation score is within 1 '
                                                                'standard error of the best score.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Select the tree that achieves exactly 1 error on the '
                                                                'training set.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Add 1 standard deviation to all feature values.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Discard any model whose training takes more than 1 '
                                                                'second.'}],
                                     'question': 'When using K-Fold cross-validation to pick the best ccp_alpha, what '
                                                 'is the 1-SE (One Standard Error) rule often applied in practice?',
                                     'subtopic': 'Subtree Selection Cross-Validation',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'Target encoding avoids expanding the feature space into hundreds '
                                                    'of sparse binary columns. However, because it incorporates the '
                                                    'target y directly into feature values, computing it naively '
                                                    'causes severe target leakage unless out-of-fold cross-fitting and '
                                                    'empirical Bayes smoothing are used.',
                                     'id': 'q-cml-l11-25',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'It collapses high-cardinality categories into a '
                                                                'single informative 1D numeric column, but requires '
                                                                'out-of-fold calculation with smoothing to prevent '
                                                                'catastrophic target leakage.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'It converts Decision Trees into K-Means clustering.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Target encoding can only be used on the test set.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It guarantees that the tree will achieve 100% '
                                                                'accuracy.'}],
                                     'question': 'Why is Target Encoding (replacing categories with the mean of target '
                                                 'y) popular for high-cardinality features in tree models, and what '
                                                 'precaution is mandatory?',
                                     'subtopic': 'Target Encoding for Trees',
                                     'type': 'single_choice'}]},
    'schema_version': 1,
    'sections': [   {   'body': '### 1.1 The Greedy Nature of Tree Induction\n'
                                '\n'
                                'Standard decision tree algorithms (CART, ID3, C4.5) build trees using a **greedy, '
                                'top-down recursive heuristic**:\n'
                                '- At each step, the algorithm chooses the single split $(x_j, \\theta)$ that yields '
                                'the maximum immediate drop in impurity:\n'
                                '  $$\\Delta I(t) = I(t) - \\left[ \\frac{n_L}{n_t} I(t_L) + \\frac{n_R}{n_t} I(t_R) '
                                '\\right]$$\n'
                                '- It makes the locally optimal choice at the current internal node without looking '
                                'ahead to see how that split influences subsequent downstream choices.\n'
                                '- While computationally tractable ($O(d \\cdot n \\log n)$ per split), this myopic '
                                'approach has a fundamental blind spot known as **The Horizon Problem**.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.2 The Horizon Problem & The XOR / Parity Failure\n'
                                '\n'
                                'What happens when no single feature by itself separates the classes, but an '
                                'interaction of two or more features separates them perfectly?\n'
                                'This is the classic **Exclusive-OR (XOR) / Parity Problem**:\n'
                                '\n'
                                'Suppose we have two binary features $x_1 \\in \\{0, 1\\}$ and $x_2 \\in \\{0, 1\\}$, '
                                'and our target label is $y = x_1 \\oplus x_2$:\n'
                                '\n'
                                '| Observation ID | Feature $x_1$ | Feature $x_2$ | Target Label $y$ ($x_1 \\oplus '
                                'x_2$) |\n'
                                '| :---: | :---: | :---: | :---: |\n'
                                '| **Row 1** | $0$ | $0$ | **0** |\n'
                                '| **Row 2** | $0$ | $1$ | **1** |\n'
                                '| **Row 3** | $1$ | $0$ | **1** |\n'
                                '| **Row 4** | $1$ | $1$ | **0** |\n'
                                '\n'
                                '```\n'
                                'The XOR Feature Space Geometry:\n'
                                '    x2 ^\n'
                                '     1 │   (y = 1)        (y = 0)\n'
                                '       │      o              *\n'
                                '       │\n'
                                '     0 │      *              o\n'
                                '       │   (y = 0)        (y = 1)\n'
                                '       └──────┴──────────────┴──────► x1\n'
                                '              0              1\n'
                                '```\n'
                                '\n'
                                '#### Step-by-Step Mathematical Walkthrough of Greedy Failure:\n'
                                '1. **Parent Root Node ($n = 4$)**:\n'
                                '   - Class counts: $2$ zeros, $2$ ones ($p_0 = 0.50, p_1 = 0.50$).\n'
                                '   - Impurity:\n'
                                '     $$H(\\text{Parent}) = - 0.50 \\log_2(0.50) - 0.50 \\log_2(0.50) = \\mathbf{1.000 '
                                '\\text{ bit}}$$\n'
                                '     $$I_G(\\text{Parent}) = 1 - (0.50^2 + 0.50^2) = \\mathbf{0.500}$$\n'
                                '\n'
                                '2. **Evaluating Candidate Split on $x_1$ ($x_1 == 0 \\text{ vs. } x_1 == 1$)**:\n'
                                '   - **Left Child ($x_1 = 0$, Rows 1 & 2)**:\n'
                                '     Targets are $[0, 1] \\implies 1$ zero, $1$ one ($p_0 = 0.50, p_1 = 0.50$).\n'
                                '     $$H(S_L) = \\mathbf{1.000 \\text{ bit}}, \\quad I_G(S_L) = \\mathbf{0.500}$$\n'
                                '   - **Right Child ($x_1 = 1$, Rows 3 & 4)**:\n'
                                '     Targets are $[1, 0] \\implies 1$ zero, $1$ one ($p_0 = 0.50, p_1 = 0.50$).\n'
                                '     $$H(S_R) = \\mathbf{1.000 \\text{ bit}}, \\quad I_G(S_R) = \\mathbf{0.500}$$\n'
                                '   - **Information Gain on $x_1$**:\n'
                                '     $$IG(x_1) = 1.000 - \\left[ \\frac{2}{4}(1.000) + \\frac{2}{4}(1.000) \\right] = '
                                '1.000 - 1.000 = \\mathbf{0.000 \\text{ bits!}}$$\n'
                                '\n'
                                '3. **Evaluating Candidate Split on $x_2$ ($x_2 == 0 \\text{ vs. } x_2 == 1$)**:\n'
                                '   - Identical symmetric result:\n'
                                '     $$IG(x_2) = \\mathbf{0.000 \\text{ bits!}}$$\n'
                                '\n'
                                '#### The Catastrophe of Pre-Pruning:\n'
                                'If we enforce common pre-pruning stopping conditions:\n'
                                '- `min_impurity_decrease = 0.01` $\\implies$ The algorithm sees $IG = 0.000 \\le '
                                '0.01$ and **aborts immediately**!\n'
                                '- `max_depth = 1` $\\implies$ The decision stump achieves $50\\%$ accuracy, '
                                'completely useless.\n'
                                '\n'
                                'However, if the tree is allowed to take this "zero-gain" split on $x_1$ and continue '
                                'to **Depth 2**:\n'
                                '- On the Left child ($x_1 = 0$), splitting on $x_2$ yields:\n'
                                '  - Left-Left ($x_2 = 0$): Row 1 $\\implies$ Target $0$ ($100\\%$ pure, $H = 0.0$).\n'
                                '  - Left-Right ($x_2 = 1$): Row 2 $\\implies$ Target $1$ ($100\\%$ pure, $H = 0.0$).\n'
                                '- On the Right child ($x_1 = 1$), splitting on $x_2$ yields:\n'
                                '  - Right-Left ($x_2 = 0$): Row 3 $\\implies$ Target $1$ ($100\\%$ pure, $H = 0.0$).\n'
                                '  - Right-Right ($x_2 = 1$): Row 4 $\\implies$ Target $0$ ($100\\%$ pure, $H = '
                                '0.0$).\n'
                                '- At Depth 2, the tree achieves **100% purity and 100% accuracy**!\n'
                                '\n'
                                '> **The Pre-Pruning Horizon Blind Spot**:\n'
                                '> Pre-pruning stops growth as soon as local gain falls below a threshold.\n'
                                '> It cannot see beyond the immediate "horizon" to realize that a split with zero '
                                'immediate gain can unlock massive purity gains downstream!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.3 Architectural Comparison: Decision Trees vs. Logistic Regression\n'
                                '\n'
                                '| Architectural Dimension | Decision Trees (Non-Parametric) | Logistic Regression '
                                '(Parametric Linear) |\n'
                                '| :--- | :--- | :--- |\n'
                                '| **Functional Assumption** | Non-parametric: No functional form assumed; partitions '
                                'space into step-wise hyper-rectangles. | Parametric: Assumes log-odds is a strictly '
                                'linear combination: $\\ln\\frac{p}{1-p} = \\mathbf{w}^T \\mathbf{x} + b$. |\n'
                                '| **Decision Boundary** | Axis-aligned piecewise constant orthogonal staircases. | '
                                'Smooth, continuous flat linear hyperplane. |\n'
                                '| **Interaction Modeling** | Automatically captures hierarchical multi-feature '
                                'interactions (depth $k$ models $k$-way interaction). | Cannot capture interactions '
                                'unless manually engineered by multiplying features ($x_1 \\times x_2$). |\n'
                                '| **Feature Scaling** | **Completely scale-invariant**: No standardization or '
                                'normalization needed. | Highly sensitive: Gradient descent and regularization require '
                                'standardized features ($z = \\frac{x-\\mu}{\\sigma}$). |\n'
                                '| **Outlier Robustness** | Extreme outliers in features do not distort splits (only '
                                'order matters). | Extreme outliers pull weights heavily, tilting the decision '
                                'boundary. |\n'
                                '| **Inference Latency** | $O(\\text{depth})$ path traversal; ultra-fast binary '
                                'comparisons. | $O(d)$ dot product evaluation; instantaneous vector multiplication. |\n'
                                '| **Risk of Overfitting** | High variance: Deep unpruned trees easily memorize noise. '
                                '| Low variance: Underfitting risk if true boundary is non-linear. |\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.4 Grow-Then-Prune: The Philosophical Shift\n'
                                '\n'
                                'To overcome the horizon blind spot, Breiman et al. introduced the **Post-Pruning '
                                '(Grow-Then-Prune)** paradigm:\n'
                                '1. **Phase 1 (Grow Fully)**: Build an unconstrained tree $T_{\\max}$ until every leaf '
                                'is pure ($I_G = 0$) or contains fewer than 2 samples. By growing past zero-gain '
                                'nodes, the tree captures multi-variable feature interactions (like XOR).\n'
                                '2. **Phase 2 (Prune Back)**: Systematically collapse unnecessary leaves and subtrees '
                                'that merely model sample noise, retaining only those branches that provide robust '
                                'statistical validation.',
                        'citations': [   'Breiman, L. et al. (1984). Classification and Regression Trees. CRC Press, '
                                         'Chapter 3.',
                                         'Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of '
                                         'Statistical Learning (2nd ed.). Springer, Chapter 9.'],
                        'heading': '1. Pre-Pruning Limitations & The Horizon Problem',
                        'section_id': 'cml-l11-sec01'},
                    {   'body': '### 2.1 The Mathematical Formulation of Cost-Complexity Pruning\n'
                                '\n'
                                'In CART, post-pruning is formalized through **Minimal Cost-Complexity Pruning '
                                '(CCP)**.\n'
                                'Instead of evaluating nodes individually, CCP evaluates the quality of an entire tree '
                                '$T$ using a penalized objective function:\n'
                                '\n'
                                '$$R_\\alpha(T) = R(T) + \\alpha |T|$$\n'
                                '\n'
                                'Where:\n'
                                '- $T \\subseteq T_{\\max}$ is any pruned subtree of the fully grown tree '
                                '$T_{\\max}$.\n'
                                '- $R(T)$ is the **total misclassification cost (or impurity)** of the tree across all '
                                'its terminal leaf nodes:\n'
                                '  $$R(T) = \\sum_{\\tau \\in \\tilde{T}} R(\\tau) = \\sum_{\\tau \\in \\tilde{T}} '
                                'P(\\tau) I(\\tau)$$\n'
                                '  Where $\\tilde{T}$ is the set of terminal leaves in $T$, $P(\\tau) = '
                                '\\frac{n_\\tau}{n}$ is the proportion of training points that reach leaf $\\tau$, and '
                                '$I(\\tau)$ is the impurity of leaf $\\tau$.\n'
                                '- $|T| = |\\tilde{T}|$ is the **number of terminal leaf nodes** in tree $T$ (a direct '
                                'measure of tree complexity).\n'
                                '- $\\alpha \\ge 0$ is the **cost-complexity hyperparameter** (`ccp_alpha` in '
                                'Scikit-Learn), which acts as a penalty per additional leaf.\n'
                                '\n'
                                '```\n'
                                'The Spectrum of ccp_alpha:\n'
                                '  α = 0                                       Optimal α*                             '
                                'α -> ∞\n'
                                '  '
                                '├───────────────────────────────────────────────┼────────────────────────────────────┤\n'
                                '  No penalty for leaves               Balanced Generalization               Extreme '
                                'penalty\n'
                                '  T_max is preferred                  Subtrees with weak gain pruned        Tree '
                                'collapses to\n'
                                '  Overfitting (0% train error)        Optimal test accuracy / ROC-AUC       Single '
                                'Root Node (|T| = 1)\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.2 Derivation of the Effective Alpha $\\alpha_{\\text{eff}}(t)$ of an Internal '
                                'Node\n'
                                '\n'
                                'For any internal node $t$ in tree $T$:\n'
                                '- Let $T_t$ denote the **subtree rooted at node $t$** (the branch expanding below '
                                '$t$).\n'
                                '- If we **keep** the subtree $T_t$, its cost-complexity contribution is:\n'
                                '  $$R_\\alpha(T_t) = R(T_t) + \\alpha |T_t|$$\n'
                                '  *(Where $|T_t|$ is the number of terminal leaves in subtree $T_t$, and $R(T_t) = '
                                '\\sum_{\\tau \\in \\tilde{T}_t} R(\\tau)$).*\n'
                                '- If we **collapse / prune** the subtree $T_t$ into a single terminal leaf at node '
                                '$t$, its cost-complexity becomes:\n'
                                '  $$R_\\alpha(t) = R(t) + \\alpha \\cdot 1$$\n'
                                '  *(Where $R(t)$ is the misclassification error if node $t$ acts as a leaf).*\n'
                                '\n'
                                '#### At What Value of $\\alpha$ Does Pruning Node $t$ Become Preferable?\n'
                                'Because the unpruned subtree $T_t$ was grown to fit the data, its training error is '
                                'always lower than or equal to the collapsed single node: $R(T_t) \\le R(t)$.\n'
                                'However, the collapsed node has only $1$ leaf, whereas the subtree has $|T_t| > 1$ '
                                'leaves.\n'
                                'Setting their cost-complexities equal:\n'
                                '$$R_\\alpha(t) = R_\\alpha(T_t)$$\n'
                                '$$R(t) + \\alpha \\cdot 1 = R(T_t) + \\alpha |T_t|$$\n'
                                '$$R(t) - R(T_t) = \\alpha (|T_t| - 1)$$\n'
                                '\n'
                                'Solving for $\\alpha$ yields the celebrated **Effective Alpha** '
                                '$\\alpha_{\\text{eff}}(t)$:\n'
                                '\n'
                                '$$\\alpha_{\\text{eff}}(t) = \\frac{R(t) - R(T_t)}{|T_t| - 1}$$\n'
                                '\n'
                                '> **Physical Meaning of Effective Alpha**:\n'
                                '> $\\alpha_{\\text{eff}}(t)$ measures the **error rate reduction per leaf** gained by '
                                'keeping subtree $T_t$ instead of collapsing it into a single leaf.\n'
                                '> - When $\\alpha < \\alpha_{\\text{eff}}(t)$, the error reduction exceeds the '
                                'penalty $\\implies$ **Keep the subtree**.\n'
                                '> - When $\\alpha \\ge \\alpha_{\\text{eff}}(t)$, the complexity penalty outweighs '
                                'the error reduction $\\implies$ **Prune the subtree into a leaf**!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.3 Concrete Multi-Node Hand-Calculated Pruning Walkthrough\n'
                                '\n'
                                'Suppose an overfitted loan decision tree has $4$ candidate internal subtrees ($N_A, '
                                'N_B, N_C, N_D$) across different depths:\n'
                                '\n'
                                '| Internal Node ($t$) | Node Error If Leaf ($R(t)$) | Subtree Error ($R(T_t)$) | '
                                'Number of Leaves in Subtree ($|T_t|$) | Effective Alpha Calculation: '
                                '$\\alpha_{\\text{eff}}(t) = \\frac{R(t) - R(T_t)}{|T_t| - 1}$ | Pruning Priority |\n'
                                '| :---: | :---: | :---: | :---: | :---: | :---: |\n'
                                '| **Node $N_A$** | $0.040$ | $0.034$ | $3$ leaves | $\\frac{0.040 - 0.034}{3 - 1} = '
                                '\\frac{0.006}{2} = \\mathbf{0.0030}$ | **1st (Weakest Link)** |\n'
                                '| **Node $N_B$** | $0.075$ | $0.055$ | $5$ leaves | $\\frac{0.075 - 0.055}{5 - 1} = '
                                '\\frac{0.020}{4} = \\mathbf{0.0050}$ | **2nd to Prune** |\n'
                                '| **Node $N_C$** | $0.120$ | $0.080$ | $3$ leaves | $\\frac{0.120 - 0.080}{3 - 1} = '
                                '\\frac{0.040}{2} = \\mathbf{0.0200}$ | **3rd to Prune** |\n'
                                '| **Node $N_D$** | $0.250$ | $0.100$ | $4$ leaves | $\\frac{0.250 - 0.100}{4 - 1} = '
                                '\\frac{0.150}{3} = \\mathbf{0.0500}$ | **4th (Strongest Split)** |\n'
                                '\n'
                                '#### How the Algorithm Executes Pruning:\n'
                                '1. At $\\alpha = 0$, all subtrees are preserved ($T_0 = T_{\\max}$).\n'
                                '2. As $\\alpha$ increases to $0.0030$, Node $N_A$ is the weakest link '
                                '($\\alpha_{\\text{eff}} = 0.0030$). Its 3 leaves are collapsed into a single leaf, '
                                'creating subtree $T_1$.\n'
                                '3. As $\\alpha$ increases to $0.0050$, Node $N_B$ collapses into a leaf, creating '
                                'subtree $T_2$.\n'
                                '4. At $\\alpha = 0.0200$, Node $N_C$ collapses, creating subtree $T_3$.\n'
                                '5. At $\\alpha \\ge 0.0500$, Node $N_D$ collapses, reducing the tree to the single '
                                'root node $T_{\\text{root}}$.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.4 The Nested Sequence of Optimal Subtrees\n'
                                '\n'
                                'A remarkable property established by Breiman is that as $\\alpha$ increases from $0$ '
                                'to $\\infty$, CART does not produce arbitrary trees.\n'
                                'It generates a strictly **nested hierarchy of optimal subtrees**:\n'
                                '\n'
                                '$$T_{\\max} = T_0 \\supset T_1 \\supset T_2 \\supset \\dots \\supset T_k = '
                                'T_{\\text{root}}$$\n'
                                '\n'
                                'Each subtree $T_{i+1}$ is obtained by pruning the weakest link (smallest '
                                '$\\alpha_{\\text{eff}}$) from subtree $T_i$.\n'
                                'Scikit-Learn computes this entire pruning path in a single pass via:\n'
                                '`path = clf.cost_complexity_pruning_path(X_train, y_train)`\n'
                                'Which returns the sequence of critical `ccp_alphas` and their corresponding total '
                                'impurities.',
                        'citations': [   'Breiman, L. et al. (1984). Classification and Regression Trees. CRC Press.',
                                         'Ripley, B. D. (1996). Pattern Recognition and Neural Networks. Cambridge '
                                         'University Press.'],
                        'heading': '2. Cost-Complexity Pruning: The Mechanics of ccp_alpha',
                        'section_id': 'cml-l11-sec02'},
                    {   'body': '### 3.1 Numerical vs. Categorical Features in Tree Splitting\n'
                                '\n'
                                'Machine learning datasets in production almost always contain a mixture of continuous '
                                'numerical features and discrete categorical features:\n'
                                '\n'
                                '| Feature Type | Definition | Mathematical Representation | Example in Credit '
                                'Underwriting |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **Continuous / Numerical** | Quantities with natural metric ordering and infinite '
                                'possible gradations. | $x_j \\in \\mathbb{R}$ | `Annual Income ($)`, `Credit Score`, '
                                '`Debt-to-Income Ratio (%)` |\n'
                                '| **Nominal Categorical** | Unordered discrete levels or classes. | $x_j \\in \\{c_1, '
                                'c_2, \\dots, c_K\\}$ | `Loan Purpose: {Education, Home, Personal, Auto}` |\n'
                                '| **Ordinal Categorical** | Discrete levels with a natural intrinsic rank order. | '
                                '$x_j \\in \\{\\text{Low} < \\text{Medium} < \\text{High}\\}$ | `Risk Rating: '
                                '{Subprime, Near-Prime, Prime, Super-Prime}` |\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.2 Splitting Mechanics: Thresholds vs. Binary Subsets\n'
                                '\n'
                                '#### 1. Splitting on Numerical Features\n'
                                'For a numerical feature, a candidate split always takes the form of a scalar '
                                'threshold test:\n'
                                '$$\\text{Is } x_j \\le \\theta?$$\n'
                                'There are at most $n - 1$ unique candidate thresholds, evaluated in $O(n \\log n)$ '
                                'time.\n'
                                '\n'
                                '#### 2. Splitting on Categorical Features Conceptually\n'
                                'For a categorical feature with $K$ unique categories, a binary tree must partition '
                                'the categories into two non-empty subsets:\n'
                                '$$\\text{Is } x_j \\in \\mathcal{S}_{\\text{left}}? \\quad \\text{where } '
                                '\\mathcal{S}_{\\text{left}} \\subset \\{c_1, \\dots, c_K\\}$$\n'
                                '\n'
                                '```\n'
                                'Categorical Binary Partitioning:\n'
                                '                [ Is Loan_Purpose in {Home, Auto}? ]\n'
                                '                                /        \\\n'
                                '                        Yes   /            \\  No\n'
                                '                            v                v\n'
                                '                 [ Home, Auto Cohort ]   [ Education, Personal Cohort ]\n'
                                '```\n'
                                '\n'
                                '#### The Combinatorial Explosion Problem:\n'
                                'How many non-empty subsets can be formed from $K$ categories?\n'
                                'The number of distinct binary partitions is:\n'
                                '$$N_{\\text{partitions}} = 2^{K-1} - 1$$\n'
                                '\n'
                                '- For $K = 4$ categories (`loan_purpose`): $2^{4-1} - 1 = 2^3 - 1 = \\mathbf{7}$ '
                                'candidate splits. Easy to evaluate!\n'
                                '- For $K = 10$ categories: $2^9 - 1 = \\mathbf{511}$ candidate splits.\n'
                                '- For $K = 20$ categories: $2^{19} - 1 = \\mathbf{524,287}$ candidate splits!\n'
                                '- For $K = 50$ (e.g., US States): $2^{49} - 1 \\approx \\mathbf{5.6 \\times 10^{14}}$ '
                                'candidate splits. Evaluating every partition is computationally impossible.\n'
                                '\n'
                                "#### Breiman's Ordering Theorem for Binary Classification:\n"
                                'Breiman proved an astonishing theorem for binary classification:\n'
                                'If you sort the $K$ categories in ascending order of their **positive class '
                                'proportion**:\n'
                                '$$P(Y = 1 \\mid x_j = c_{(1)}) \\le P(Y = 1 \\mid x_j = c_{(2)}) \\le \\dots \\le P(Y '
                                '= 1 \\mid x_j = c_{(K)})$$\n'
                                'Then the optimal binary partition that maximizes Gini Gain or Information Gain is '
                                '**guaranteed** to be one of the $K - 1$ consecutive cuts along this sorted line!\n'
                                'This collapses the computational search from exponential $O(2^K)$ down to linear $O(K '
                                '\\log K)$!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.3 Target Encoding with Empirical Bayesian Smoothing\n'
                                '\n'
                                'When dealing with high-cardinality categories ($K > 20$, such as `Zip_Code` or '
                                '`Product_Category`), One-Hot encoding blows up dimensionality and fractures trees '
                                'into sparse leaves.\n'
                                'A powerful alternative is **Target Encoding (Mean Target Encoding)**:\n'
                                'Each category $c$ is replaced by the expected target value:\n'
                                '$$\\hat{x}_c = \\mathbb{E}[Y \\mid X = c]$$\n'
                                '\n'
                                '#### The Overfitting Hazard on Rare Categories:\n'
                                'If a category appears only once in the dataset (e.g., `Zip_Code = 90210` with $y = '
                                '1$), naive target encoding assigns it $\\hat{x} = 1.0$. The tree creates a perfect '
                                'leaf on this single sample, causing massive overfitting!\n'
                                'To resolve this, we apply **Empirical Bayesian Smoothing (m-estimate)**:\n'
                                '\n'
                                '$$S_k = \\lambda(n_k) \\bar{y}_k + (1 - \\lambda(n_k)) \\bar{y}_{\\text{global}}$$\n'
                                '$$\\lambda(n_k) = \\frac{n_k}{n_k + m}$$\n'
                                '\n'
                                'Where:\n'
                                '- $n_k$ is the count of observations in category $k$.\n'
                                '- $\\bar{y}_k$ is the local sample target mean for category $k$.\n'
                                '- $\\bar{y}_{\\text{global}}$ is the overall dataset target mean (e.g., $0.20$ '
                                'default rate).\n'
                                '- $m \\ge 1$ is the smoothing weight (e.g., $m = 10$).\n'
                                '\n'
                                '#### Concrete Hand Calculation:\n'
                                'Suppose global default rate $\\bar{y}_{\\text{global}} = 0.20$ ($20\\%$). We have two '
                                'categories:\n'
                                '1. Category A (`Personal Loan`): $n_A = 500$ loans, $150$ defaults $\\implies '
                                '\\bar{y}_A = 150/500 = 0.30$.\n'
                                '   $$\\lambda(500) = \\frac{500}{500 + 10} = \\frac{500}{510} \\approx 0.9804$$\n'
                                '   $$S_A = 0.9804(0.30) + (1 - 0.9804)(0.20) = 0.2941 + 0.0039 = \\mathbf{0.2980} '
                                '\\text{ (Virtually unchanged)}$$\n'
                                '2. Category B (`Rare Yacht Loan`): $n_B = 2$ loans, $2$ defaults $\\implies '
                                '\\bar{y}_B = 2/2 = 1.00$.\n'
                                '   $$\\lambda(2) = \\frac{2}{2 + 10} = \\frac{2}{12} \\approx 0.1667$$\n'
                                '   $$S_B = 0.1667(1.00) + (1 - 0.1667)(0.20) = 0.1667 + 0.1667 = \\mathbf{0.3334}$$\n'
                                '\n'
                                'Notice how the smoothed estimate for the rare category is pulled from a dangerous '
                                '$1.00$ down to $0.3334$, protecting the tree from memorizing a 2-sample fluke!',
                        'citations': [   'Quinlan, J. R. (1993). C4.5: Programs for Machine Learning. Morgan Kaufmann '
                                         'Publishers.'],
                        'heading': '3. Categorical vs. Numerical Features in Decision Trees',
                        'section_id': 'cml-l11-sec03'},
                    {   'body': '### 4.1 Mean Decrease in Impurity (MDI / Gini Importance)\n'
                                '\n'
                                'When a decision tree is trained in Scikit-Learn, it automatically computes and '
                                'exposes the `feature_importances_` attribute.\n'
                                'This metric is formally known as **Mean Decrease in Impurity (MDI)** or **Gini '
                                'Importance**:\n'
                                '\n'
                                '#### Mathematical Definition:\n'
                                'Let $\\mathcal{T}_j$ denote the set of all internal nodes $t$ across the tree where '
                                'feature $j$ was selected as the splitting variable ($v(t) = j$).\n'
                                'The raw importance of feature $j$ is the sum of the impurity decreases achieved at '
                                'those specific nodes, weighted by the fraction of training samples that traverse node '
                                '$t$:\n'
                                '\n'
                                '$$\\text{MDI}(j) = \\sum_{t \\in \\mathcal{T}_j} \\frac{n_t}{n} \\Delta I(t)$$\n'
                                '\n'
                                'Where:\n'
                                '- $n_t$ is the number of training observations reaching node $t$.\n'
                                '- $n$ is the total number of training observations in the entire dataset.\n'
                                '- $\\Delta I(t) = I(t) - \\frac{n_L}{n_t} I(t_L) - \\frac{n_R}{n_t} I(t_R)$ is the '
                                'impurity reduction at node $t$.\n'
                                '\n'
                                'To make importances easily interpretable, Scikit-Learn normalizes the values so they '
                                'sum to $1.0$:\n'
                                '\n'
                                '$$\\text{Importance}(j) = \\frac{\\text{MDI}(j)}{\\sum_{k=1}^d \\text{MDI}(k)}, '
                                '\\quad \\text{where } \\sum_{j=1}^d \\text{Importance}(j) = 1.0$$\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.2 Three Critical Pitfalls of MDI Feature Importance\n'
                                '\n'
                                'While MDI is fast to compute (accumulated for free during tree training), it suffers '
                                'from severe statistical flaws that frequently deceive data scientists:\n'
                                '\n'
                                '#### Pitfall 1: Severe Bias Toward High-Cardinality & Continuous Features\n'
                                '- A continuous feature with 1,000 unique values offers 999 possible split midpoints.\n'
                                '- A binary categorical feature ($0$ or $1$) offers exactly $1$ possible split '
                                'midpoint.\n'
                                '- **Purely by chance**, an uninformative continuous feature (or a random noise '
                                'column) has hundreds of opportunities to find a spurious split that marginally '
                                'reduces training impurity.\n'
                                '- As a result, **MDI heavily inflates the importance of continuous and '
                                'high-cardinality features**, even when they contain zero real predictive signal!\n'
                                '\n'
                                '#### Pitfall 2: Collinear Feature Cannibalization (Shadowing)\n'
                                '- Suppose two features $x_1$ and $x_2$ are nearly identical (e.g., `Annual Income` in '
                                'dollars and `Monthly Income` in dollars).\n'
                                '- At the root node, the tree evaluates both. Suppose $x_1$ achieves an infinitesimal '
                                'edge ($IG = 0.2501$ vs $0.2500$). The tree splits on $x_1$.\n'
                                '- Once the node is partitioned on $x_1$, the residual variance is largely resolved. '
                                'When $x_2$ is evaluated in downstream child nodes, its remaining gain is near zero.\n'
                                '- In the final MDI summary, $x_1$ appears critically important ($0.85$), while $x_2$ '
                                'appears virtually useless ($0.02$), hiding the fact that $x_2$ is just as predictive '
                                'as $x_1$!\n'
                                '\n'
                                '#### Pitfall 3: In-Sample Training Metric (No Generalization Guarantee)\n'
                                '- MDI is calculated strictly on the **training data**.\n'
                                '- If a deep unpruned tree overfits and memorizes random training noise, MDI will '
                                'assign massive importance to the exact features that memorized that noise.\n'
                                '- It tells you what features the tree used to memorize the training set, **not** what '
                                'features reliably predict new, unseen observations!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.3 The Gold Standard Solution: Permutation Feature Importance\n'
                                '\n'
                                'In 2001, Leo Breiman designed **Permutation Feature Importance** to resolve the fatal '
                                'shortcomings of MDI:\n'
                                '\n'
                                '```\n'
                                'Permutation Feature Importance Workflow:\n'
                                '  1. Train the tree model on X_train, y_train.\n'
                                '  2. Compute baseline performance metric on an UNTOUCHED validation set (X_val, '
                                'y_val):\n'
                                '         Baseline Score = ROC-AUC(y_val, Model.predict_proba(X_val))\n'
                                '  3. For each feature j in {1, 2, ..., d}:\n'
                                '         Randomly shuffle ONLY column j in X_val (breaking its relationship with '
                                'y_val).\n'
                                '         Compute new performance score on corrupted data:\n'
                                '             Score_perm(j) = ROC-AUC(y_val, Model.predict_proba(X_val_shuffled_j))\n'
                                '         Calculate Importance as the Performance Drop:\n'
                                '             Importance_perm(j) = Baseline Score - Score_perm(j)\n'
                                '```\n'
                                '\n'
                                '#### Comparing Tree Interpretability Frameworks:\n'
                                '| Attribute | MDI (Gini Importance) | Permutation Importance | SHAP (SHapley Additive '
                                'exPlanations) |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **Data Split Evaluated** | Training set only | Holdout Test / Validation set | Test '
                                '/ Validation set |\n'
                                '| **Computational Speed** | Instant ($O(1)$ post-training) | Moderate ($O(p \\times '
                                'n_{\\text{test}})$) | Fast for trees ($O(T \\cdot L \\cdot D^2)$ via TreeSHAP) |\n'
                                '| **High-Cardinality Bias** | **Severe Positive Bias** | **Unbiased** (Noise scores '
                                '$\\le 0$) | **Unbiased** |\n'
                                '| **Directional Impact** | Magnitude only ($[0, 1]$) | Performance drop only | '
                                'Directional ($+$ or $-$ impact on class probability) |\n'
                                '| **Collinearity Handling** | Arbitrarily picks one feature | Understates correlated '
                                'features | Fairly distributes credit using Shapley values |',
                        'citations': [   'Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5-32.',
                                         'Strobl, C., Boulesteix, A. L., Zeileis, A., & Hothorn, T. (2007). Bias in '
                                         'random forest variable importance measures: Illustrations, sources and a '
                                         'solution. BMC Bioinformatics, 8(1), 25.'],
                        'heading': '4. Feature Importance: Mean Decrease in Impurity (MDI) & Pitfalls',
                        'section_id': 'cml-l11-sec04'},
                    {   'body': '### 5.1 Hands-On Python Implementation: Pruning Path & Feature Importance\n'
                                '\n'
                                'The following production script implements the full CART post-pruning pipeline on a '
                                'bank loan default dataset, tunes `ccp_alpha` using cross-validation, and contrasts '
                                'MDI vs. Permutation Feature Importance:\n'
                                '\n'
                                '```python\n'
                                'import numpy as np\n'
                                'import pandas as pd\n'
                                'import matplotlib.pyplot as plt\n'
                                'from sklearn.datasets import make_classification\n'
                                'from sklearn.model_selection import train_test_split, cross_val_score, '
                                'StratifiedKFold\n'
                                'from sklearn.tree import DecisionTreeClassifier, export_text\n'
                                'from sklearn.inspection import permutation_importance\n'
                                'from sklearn.metrics import accuracy_score, roc_auc_score, classification_report\n'
                                '\n'
                                '# 1. Synthesize Bank Loan Dataset with Categorical & Continuous Features + Random '
                                'Noise\n'
                                'np.random.seed(42)\n'
                                'n_samples = 1200\n'
                                '\n'
                                '# Continuous financial features\n'
                                'credit_score = np.random.normal(650, 80, n_samples).clip(300, 850)\n'
                                'annual_income = np.random.lognormal(10.8, 0.5, n_samples)\n'
                                'loan_amount = annual_income * np.random.uniform(0.1, 0.6, n_samples)\n'
                                'years_employed = np.random.exponential(5, n_samples).clip(0, 30)\n'
                                '\n'
                                '# Categorical feature: loan_purpose\n'
                                'purposes = ["education", "home", "personal", "auto"]\n'
                                'loan_purpose = np.random.choice(purposes, size=n_samples, p=[0.20, 0.35, 0.25, '
                                '0.20])\n'
                                '\n'
                                '# Pure Random Noise column with high cardinality (Tests MDI bias!)\n'
                                'random_noise_high_card = np.random.uniform(0, 1000, n_samples)\n'
                                '\n'
                                '# Generate Ground Truth Target (Default = 1)\n'
                                'logit = (\n'
                                '    - 0.012 * (credit_score - 600)\n'
                                '    + 0.00003 * (loan_amount - 20000)\n'
                                '    - 0.15 * (years_employed - 4)\n'
                                '    + np.where(loan_purpose == "personal", 0.6, 0.0)\n'
                                '    + np.where(loan_purpose == "education", 0.3, 0.0)\n'
                                '    - 1.2\n'
                                ')\n'
                                'prob_default = 1 / (1 + np.exp(-logit))\n'
                                'default = (np.random.uniform(0, 1, n_samples) < prob_default).astype(int)\n'
                                '\n'
                                'df = pd.DataFrame({\n'
                                '    "credit_score": credit_score,\n'
                                '    "annual_income": annual_income,\n'
                                '    "loan_amount": loan_amount,\n'
                                '    "years_employed": years_employed,\n'
                                '    "loan_purpose": loan_purpose,\n'
                                '    "random_noise_col": random_noise_high_card,\n'
                                '    "default": default\n'
                                '})\n'
                                '\n'
                                '# 2. Preprocessing: One-Hot Encode Categorical Column\n'
                                'df_encoded = pd.get_dummies(df, columns=["loan_purpose"], drop_first=False)\n'
                                'X = df_encoded.drop(columns=["default"])\n'
                                'y = df_encoded["default"]\n'
                                '\n'
                                '# 3. Train / Validation / Test Partition\n'
                                'X_train, X_test, y_train, y_test = train_test_split(\n'
                                '    X, y, test_size=0.25, random_state=42, stratify=y\n'
                                ')\n'
                                '\n'
                                '# 4. Extract Cost-Complexity Pruning Path\n'
                                'unpruned_tree = DecisionTreeClassifier(random_state=42)\n'
                                'path = unpruned_tree.cost_complexity_pruning_path(X_train, y_train)\n'
                                'ccp_alphas, impurities = path.ccp_alphas, path.impurities\n'
                                '\n'
                                '# 5. Tune Optimal ccp_alpha via 5-Fold Stratified Cross-Validation\n'
                                'cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n'
                                'alpha_candidates = ccp_alphas[::5]  # Subsample candidates along the path\n'
                                'alpha_scores = []\n'
                                '\n'
                                'for alpha in alpha_candidates:\n'
                                '    clf = DecisionTreeClassifier(random_state=42, ccp_alpha=alpha)\n'
                                '    scores = cross_val_score(clf, X_train, y_train, cv=cv, scoring="roc_auc")\n'
                                '    alpha_scores.append(scores.mean())\n'
                                '\n'
                                'best_alpha = alpha_candidates[np.argmax(alpha_scores)]\n'
                                'print(f"Optimal Tuned ccp_alpha: {best_alpha:.5f}")\n'
                                '\n'
                                '# 6. Fit Final Pruned Tree\n'
                                'best_tree = DecisionTreeClassifier(random_state=42, ccp_alpha=best_alpha)\n'
                                'best_tree.fit(X_train, y_train)\n'
                                '\n'
                                '# 7. Evaluate on Holdout Test Set\n'
                                'test_auc = roc_auc_score(y_test, best_tree.predict_proba(X_test)[:, 1])\n'
                                'print(f"Holdout Test ROC-AUC (Optimal CCP Tree): {test_auc:.4f}")\n'
                                'print(f"Tree Depth: {best_tree.get_depth()} | Leaves: {best_tree.get_n_leaves()}")\n'
                                '\n'
                                '# 8. Compare MDI vs. Permutation Importance\n'
                                'mdi_importances = pd.Series(best_tree.feature_importances_, index=X.columns)\n'
                                '\n'
                                'perm_result = permutation_importance(\n'
                                '    best_tree, X_test, y_test, n_repeats=10, random_state=42, scoring="roc_auc"\n'
                                ')\n'
                                'perm_importances = pd.Series(perm_result.importances_mean, index=X.columns)\n'
                                '\n'
                                'comparison_df = pd.DataFrame({\n'
                                '    "MDI (Gini Importance)": mdi_importances,\n'
                                '    "Permutation Importance (Test)": perm_importances\n'
                                '}).sort_values(by="Permutation Importance (Test)", ascending=False)\n'
                                '\n'
                                'print("\\n=== FEATURE IMPORTANCE COMPARISON ===")\n'
                                'print(comparison_df.round(4))\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.2 Alpha Sweep Results & Pruning Trade-Off Table\n'
                                '\n'
                                'When cost-complexity pruning is evaluated across increasing values of `ccp_alpha`, '
                                'the tree shrinks monotonically:\n'
                                '\n'
                                '| Complexity Penalty ($\\alpha$) | Tree Depth | Terminal Leaves | Train ROC-AUC | '
                                'Test ROC-AUC | Diagnostic State |\n'
                                '| :---: | :---: | :---: | :---: | :---: | :--- |\n'
                                '| **$\\alpha = 0.00000$** | $14$ | $118$ | $1.0000$ | $0.7180$ | **Overfitted Tree**: '
                                'Fits training noise; wide generalization gap. |\n'
                                '| **$\\alpha = 0.00210$** | $8$ | $42$ | $0.9420$ | $0.7810$ | Mild pruning; weak '
                                'subtrees collapsed. |\n'
                                '| **$\\alpha = 0.00485$** | $5$ | $14$ | $0.8830$ | $\\mathbf{0.8350}$ | **Optimal '
                                'CCP Sweet Spot**: Peak test ROC-AUC. Balanced bias-variance. |\n'
                                '| **$\\alpha = 0.01250$** | $3$ | $6$ | $0.8210$ | $0.8120$ | Coarse tree; robust, '
                                'human-interpretable rules. |\n'
                                '| **$\\alpha = 0.03500$** | $1$ | $2$ | $0.7250$ | $0.7200$ | Underfitting (Decision '
                                'Stump). |\n'
                                '| **$\\alpha \\ge 0.08000$** | $0$ | $1$ | $0.5000$ | $0.5000$ | Complete Collapse: '
                                'Single root node predicting global majority class. |\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.3 Diagnostic Failure Modes & Engineering Pitfalls\n'
                                '\n'
                                '| Engineering Failure Mode | Underlying Root Cause | Catastrophic Symptom | '
                                'Recommended Production Solution |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **Relying Exclusively on Pre-Pruning** | Greedy early stopping halts on zero-gain '
                                'splits. | Tree fails completely on multi-variable interactions (e.g., XOR, synergy '
                                'between income and debt). | Use Post-Pruning (`ccp_alpha`) or ensemble methods '
                                '(Random Forests) that grow deep trees before regularizing. |\n'
                                '| **Trusting MDI on High-Cardinality Features** | Continuous/high-cardinality '
                                'features offer hundreds of candidate thresholds, winning spurious gains. | Random '
                                'noise columns or unique IDs rank at the top of `feature_importances_`. | Always '
                                'evaluate **Permutation Feature Importance** on an independent validation/test set. |\n'
                                '| **One-Hot Encoding High-Cardinality Columns** | Categorical features with $50+$ '
                                'categories create dozens of sparse columns. | Splits isolate tiny groups ($1$ vs '
                                '$999$), fracturing tree depth and destroying predictive power. | Use Target Encoding '
                                'with cross-validation smoothing, or switch to LightGBM/CatBoost native categorical '
                                'handling. |\n'
                                '| **Arbitrary Alpha Selection Without CV** | Choosing `ccp_alpha = 0.05` arbitrarily '
                                'without checking the pruning path. | Tree over-prunes into a useless single root '
                                'node, causing massive underfitting. | Always extract `cost_complexity_pruning_path` '
                                'and select $\\alpha$ via `GridSearchCV` on cross-validation ROC-AUC. |\n'
                                '| **Permutation Importance on Collinear Features** | Correlated features share '
                                'identical information. | Shuffling feature A has no effect because feature B provides '
                                'the exact same information, masking both features. | Group correlated features '
                                'together and permute them as a single cluster (**Clustered Permutation Importance**). '
                                '|\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.4 Production Automated Pruning Curve Visualization\n'
                                '\n'
                                'In production machine learning workflows, plotting the pruning path against tree '
                                'complexity and cross-validation accuracy allows engineers to audit the optimal '
                                'stopping point:\n'
                                '\n'
                                '```python\n'
                                '# Extract full alpha path\n'
                                'clf = DecisionTreeClassifier(random_state=42)\n'
                                'path = clf.cost_complexity_pruning_path(X_train, y_train)\n'
                                'ccp_alphas, impurities = path.ccp_alphas, path.impurities\n'
                                '\n'
                                '# Track tree metrics across alpha\n'
                                'clfs = []\n'
                                'for alpha in ccp_alphas[::3]:  # Subsample path for efficiency\n'
                                '    t = DecisionTreeClassifier(random_state=42, ccp_alpha=alpha)\n'
                                '    t.fit(X_train, y_train)\n'
                                '    clfs.append(t)\n'
                                '\n'
                                'node_counts = [t.tree_.node_count for t in clfs]\n'
                                'depths = [t.tree_.max_depth for t in clfs]\n'
                                'train_scores = [t.score(X_train, y_train) for t in clfs]\n'
                                'test_scores = [t.score(X_test, y_test) for t in clfs]\n'
                                '\n'
                                'print(f"Total alpha candidate thresholds evaluated: {len(ccp_alphas)}")\n'
                                'print(f"Max Nodes in Unpruned Tree: {node_counts[0]} | Max Depth: {depths[0]}")\n'
                                'print(f"Nodes in Pruned Tree (Optimal Alpha): {best_tree.tree_.node_count} | Depth: '
                                '{best_tree.tree_.max_depth}")\n'
                                '```',
                        'citations': [   'Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. JMLR, '
                                         '12, 2825-2830.'],
                        'heading': '5. Hands-On Python Implementation: Pruning Path & Feature Importance',
                        'section_id': 'cml-l11-sec05'}],
    'subject_code': 'CML',
    'summary': 'An in-depth, practical continuation of Decision Tree architectures. Explores why pre-pruning can '
               'suffer from the horizon problem and formalizes Cost-Complexity Pruning (ccp_alpha) where a deep tree '
               'is grown and systematically trimmed back. Dissects categorical split mechanics in Scikit-Learn, '
               'demystifies Mean Decrease in Impurity (MDI) feature importance, exposes high-cardinality bias traps, '
               'and implements production pruning on loan default datasets.',
    'tags': [   'Decision Trees',
                'Cost-Complexity Pruning',
                'Post-Pruning',
                'ccp_alpha',
                'Feature Importance',
                'Mean Decrease in Impurity',
                'Categorical Splits',
                'Model Interpretability'],
    'term': 'Term 5',
    'topic_title': '11. Decision Trees II: Pruning, Categorical Features & Feature Importance'}

