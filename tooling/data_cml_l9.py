"""
Data definition for data_cml_l9:
"""

L9_DATA = {   'approval_status': 'approved',
    'key_takeaways': [   'k-NN is a non-parametric, lazy learner: it learns no explicit mathematical formula (no '
                         'weights w); training stores the dataset, and all computation occurs at query time.',
                         'Classification predicts via local majority vote; Regression predicts via the arithmetic mean '
                         '(or median) of the k nearest neighbors.',
                         'Distance metrics (Euclidean L2, Manhattan L1) depend entirely on feature units; failing to '
                         'standardize features allows wide-scale features to completely dominate distance '
                         'calculations.',
                         'Small k (k = 1) yields complex, fragmented decision boundaries with zero training error '
                         '(High Variance / Overfitting); Large k (k = n) yields flat, rigid predictions equal to the '
                         'global majority (High Bias / Underfitting).',
                         'In binary classification, choose an odd integer for k to naturally prevent 50-50 voting '
                         'deadlocks.',
                         'The Curse of Dimensionality causes hyperspace volume to concentrate in outer shells; as '
                         'dimension d grows, all pairwise distances converge to the same value, rendering distance '
                         'discrimination useless.',
                         'KD-Trees and BallTrees accelerate neighbor queries in low-to-moderate dimensions (d < 20), '
                         'but degrade to O(n) brute-force linear scans in high dimensions.'],
    'last_updated': '2026-10-18T00:00:00Z',
    'learning_objectives': [   'Understand instance-based (lazy) learning and contrast k-NN with parametric models '
                               '(Linear and Logistic Regression).',
                               'Calculate and contrast distance metrics (Euclidean, Manhattan, Minkowski) and explain '
                               'why feature scaling is strictly mandatory.',
                               'Analyze how hyperparameter k governs the Bias-Variance tradeoff from k=1 (high '
                               'variance) to k=n (high bias).',
                               'Explain the geometric reality of the Curse of Dimensionality and the distance '
                               'concentration phenomenon.',
                               'Implement production k-NN classification and regression pipelines using Scikit-Learn, '
                               'KD-Trees, and BallTrees.'],
    'note_id': 'cml-t5-l09',
    'quiz': {   'questions': [   {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'k-NN is a lazy, instance-based learner. It does not learn an '
                                                    'explicit parameter equation during training; it merely indexes '
                                                    'and stores the training points in memory. Computation occurs at '
                                                    'prediction time.',
                                     'id': 'q-cml-l09-01',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'The algorithm executes gradient descent to find '
                                                                'optimal weight coefficients w.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'The algorithm simply stores the training dataset in '
                                                                'memory (lazy learning).'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The algorithm computes the inverse of the feature '
                                                                'covariance matrix.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The algorithm builds a neural network architecture.'}],
                                     'question': "What primary computational operation occurs during the 'fit' "
                                                 '(training) stage of a classic K-Nearest Neighbours algorithm?',
                                     'subtopic': 'Lazy Learning Nature',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'k-NN computes the distance from the query to every training '
                                                    'sample, selects the k nearest samples, and predicts the class '
                                                    'that appears most frequently among them (majority voting).',
                                     'id': 'q-cml-l09-02',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'By calculating the dot product between the query '
                                                                'vector and a weight vector.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'By taking a majority vote among the class labels of '
                                                                'the k closest training points in feature space.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'By finding the centroid of all training points '
                                                                'combined.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'By fitting a straight line between the query point '
                                                                'and the origin.'}],
                                     'question': 'How does a k-NN classifier determine the predicted class label for '
                                                 'an unseen query instance x*?',
                                     'subtopic': 'Classification Prediction Mechanism',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'easy',
                                     'explanation': 'In k-NN regression, instead of a majority vote, the model '
                                                    'averages the continuous target values y of the k nearest '
                                                    'neighbors: y_hat = (1/k) * sum(y_i).',
                                     'id': 'q-cml-l09-03',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'It computes the arithmetic mean (or median) of the '
                                                                'continuous target values of the k nearest neighbors.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'It rounds all continuous numbers to the nearest '
                                                                'integer and takes a majority vote.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It fits an Ordinary Least Squares line through the k '
                                                                'points.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'KNN is mathematically incapable of performing '
                                                                'regression.'}],
                                     'question': 'How is K-Nearest Neighbours adapted to solve Regression problems '
                                                 'where the target y is a continuous numeric value?',
                                     'subtopic': 'KNN Regression',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'Euclidean distance is the square root of the sum of squared '
                                                    'coordinate differences: sqrt( sum (x_j - z_j)^2 ). Option 1 is '
                                                    'Manhattan, and Option 3 is Chebyshev.',
                                     'id': 'q-cml-l09-04',
                                     'options': [   {'id': 'opt-1', 'is_correct': False, 'text': 'sum |x_j - z_j|'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'sqrt( sum (x_j - z_j)^2 )'},
                                                    {'id': 'opt-3', 'is_correct': False, 'text': 'max |x_j - z_j|'},
                                                    {'id': 'opt-4', 'is_correct': False, 'text': '1 - (x . z)'}],
                                     'question': 'Which mathematical distance formula corresponds to the straight-line '
                                                 'Euclidean distance (L2 norm) between vectors x and z in d '
                                                 'dimensions?',
                                     'subtopic': 'Distance Metric Formulation',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'Distance calculations sum squared coordinate differences. A '
                                                    'feature with values in the tens of thousands will produce squared '
                                                    'differences in the hundreds of millions, completely drowning out '
                                                    'features measured on scales of 1 to 10.',
                                     'id': 'q-cml-l09-05',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Because k-NN algorithms crash if features have '
                                                                'different units.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Because features with large numerical magnitudes '
                                                                '(e.g. Income in thousands) will completely dominate '
                                                                'distance calculations, blinding the model to features '
                                                                'on smaller scales (e.g. Age).'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Because scaling converts non-linear relationships '
                                                                'into linear ones.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Scaling is only required for tree-based models, not '
                                                                'for k-NN.'}],
                                     'question': 'Why is feature scaling (e.g., StandardScaler) strictly required '
                                                 'before applying K-Nearest Neighbours?',
                                     'subtopic': 'Feature Scaling Necessity',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'easy',
                                     'explanation': "When k = 1, each training point's nearest neighbor is itself "
                                                    '(distance = 0), yielding 0% training error. The decision boundary '
                                                    'wiggles around every single noise point, resulting in high '
                                                    'variance and severe overfitting.',
                                     'id': 'q-cml-l09-06',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'Extreme Overfitting: it achieves 0% training error, '
                                                                'produces jagged decision boundaries, and has high '
                                                                'variance.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Extreme Underfitting: it predicts a flat linear '
                                                                'boundary and has high bias.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It is mathematically identical to Logistic '
                                                                'Regression.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It achieves optimal generalization on all unseen test '
                                                                'sets.'}],
                                     'question': 'What is the primary characteristic of a K-Nearest Neighbours model '
                                                 'trained with k = 1?',
                                     'subtopic': 'Bias-Variance: k=1',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'When k = n, the neighborhood is the entire training set. The '
                                                    'majority vote will always be the overall most frequent class in '
                                                    'the dataset, completely ignoring local query geometry (maximum '
                                                    'bias).',
                                     'id': 'q-cml-l09-07',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'The model achieves 100% test accuracy.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Extreme Underfitting: the model considers every '
                                                                'sample in the dataset for every query, predicting the '
                                                                'global majority class everywhere (high bias).'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The model splits into n separate clusters.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The algorithm executes in O(1) time.'}],
                                     'question': 'In a dataset with n total training observations, what happens if you '
                                                 'set hyperparameter k = n in k-NN classification?',
                                     'subtopic': 'Bias-Variance: k=n',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'With two classes (binary), an odd number of votes can never '
                                                    'result in an equal tie (e.g. 5 votes can split 3-2 or 4-1, but '
                                                    'never 2.5-2.5).',
                                     'id': 'q-cml-l09-08',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Odd numbers run faster on 64-bit operating systems.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'It mathematically prevents 50-50 tie votes between '
                                                                'the two classes.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Even numbers violate the triangle inequality.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Scikit-Learn throws an error if an even k is '
                                                                'provided.'}],
                                     'question': 'Why is it standard industry practice to choose an ODD integer for k '
                                                 '(e.g., k = 3, 5, 7) in binary classification problems?',
                                     'subtopic': 'Odd k in Binary Classification',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'Squaring terms in Euclidean distance causes large outlier '
                                                    'deviations to dominate the entire distance calculation. Manhattan '
                                                    'distance penalizes deviations linearly, reducing the leverage of '
                                                    'isolated extreme values.',
                                     'id': 'q-cml-l09-09',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Manhattan distance ignores negative numbers.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Euclidean distance squares coordinate differences '
                                                                '(delta x)^2, exponentially magnifying large '
                                                                'deviations, whereas Manhattan distance increases '
                                                                'linearly |delta x|.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Manhattan distance automatically discards the top 5% '
                                                                'of features.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Manhattan distance is only defined for integer '
                                                                'values.'}],
                                     'question': 'Why is Manhattan distance (L1) generally more robust than Euclidean '
                                                 'distance (L2) when a feature contains extreme outlier values?',
                                     'subtopic': 'Manhattan vs Euclidean Outlier Robustness',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'medium',
                                     'explanation': 'Minkowski distance with p = 1 corresponds to Manhattan (L1) '
                                                    'distance; p = 2 corresponds to standard Euclidean (L2) distance.',
                                     'id': 'q-cml-l09-10',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': "Set metric='minkowski' and parameter p = 1."},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': "Set metric='minkowski' and parameter p = 2."},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': "Set algorithm='manhattan'."},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Set n_neighbors = -1.'}],
                                     'question': "In Scikit-Learn's KNeighborsClassifier, how do you configure the "
                                                 'model to use Manhattan distance instead of default Euclidean '
                                                 'distance?',
                                     'subtopic': 'Minkowski Metric Parameter',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'Brute-force k-NN must compute the d-dimensional distance to all n '
                                                    'stored training points, requiring O(n * d) operations per query.',
                                     'id': 'q-cml-l09-11',
                                     'options': [   {'id': 'opt-1', 'is_correct': False, 'text': 'O(1)'},
                                                    {'id': 'opt-2', 'is_correct': True, 'text': 'O(n * d)'},
                                                    {'id': 'opt-3', 'is_correct': False, 'text': 'O(d^3)'},
                                                    {'id': 'opt-4', 'is_correct': False, 'text': 'O(log n)'}],
                                     'question': 'What is the time complexity to classify a single query point using '
                                                 'brute-force k-NN on a dataset with n training samples and d '
                                                 'features?',
                                     'subtopic': 'Inference Time Complexity',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'medium',
                                     'explanation': "With weights='distance', each neighbor's vote is weighted by 1 / "
                                                    'distance. A neighbor very close to the query exerts much more '
                                                    'voting pull than a neighbor on the outer fringe of the '
                                                    'neighborhood.',
                                     'id': 'q-cml-l09-12',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'It gives each neighbor a vote inversely proportional '
                                                                'to its distance, meaning closer neighbors have '
                                                                'greater influence on the predicted label.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'It discards the farthest neighbor and votes among k - '
                                                                '1 points.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It weights neighbors by their target value y rather '
                                                                'than distance.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It forces k to equal the Euclidean distance.'}],
                                     'question': "How does setting weights='distance' in KNeighborsClassifier modify "
                                                 'the standard majority voting rule?',
                                     'subtopic': 'Distance-Weighted Voting',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'Hypercube volume scales as s^d. In high dimensions, points become '
                                                    'sparse, isolated islands. Finding a neighbor requires searching '
                                                    'across nearly the entire range of features, losing local '
                                                    'relevance.',
                                     'id': 'q-cml-l09-13',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'High-dimensional datasets contain more missing NaN '
                                                                'values.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'As dimensionality d grows, the volume of feature '
                                                                'space expands exponentially, causing fixed-size '
                                                                'sample points to become extremely sparse and isolated '
                                                                'from each other.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Computer memory empties automatically during nearest '
                                                                'neighbor calculation.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The distance between all points collapses to zero.'}],
                                     'question': 'In the context of the Curse of Dimensionality, what is meant by the '
                                                 "'empty space phenomenon'?",
                                     'subtopic': 'Empty Space Phenomenon',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'medium',
                                     'explanation': 'Beyer et al. (1999) proved that under broad conditions, lim_{d -> '
                                                    'inf} (d_max - d_min) / d_min = 0. All points become approximately '
                                                    'equidistant from the query, destroying metric contrast.',
                                     'id': 'q-cml-l09-14',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'As dimensionality d grows, the relative difference '
                                                                'between the distance to the nearest neighbor (d_min) '
                                                                'and the farthest neighbor (d_max) approaches zero.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'All points concentrate at the exact origin (0, 0, '
                                                                '..., 0).'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Distance calculations become negative.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Nearest neighbors always belong to the majority '
                                                                'class.'}],
                                     'question': "What is the 'distance concentration phenomenon' in high-dimensional "
                                                 'feature spaces?',
                                     'subtopic': 'Distance Concentration',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'A larger k averages votes across a broader local neighborhood, '
                                                    'dampening the influence of individual noisy points and smoothing '
                                                    'the decision boundary.',
                                     'id': 'q-cml-l09-15',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'The boundary becomes much more jagged, isolated, and '
                                                                'complex.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'The boundary becomes smoother, more continuous, and '
                                                                'less sensitive to individual outlier points.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The boundary turns into a 3D sphere.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The boundary rotates by 90 degrees.'}],
                                     'question': 'How does increasing hyperparameter k from k = 3 to k = 25 affect the '
                                                 'visual geometry of the decision boundary in feature space?',
                                     'subtopic': 'Decision Boundary Smoothness',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'Parametric models (logistic regression, linear regression) '
                                                    'compute a single dot product w^T x in microseconds. k-NN requires '
                                                    'searching massive datasets at query time, creating unacceptable '
                                                    'latency bottlenecks unless approximate nearest neighbor indexing '
                                                    '(ANN) is used.',
                                     'id': 'q-cml-l09-16',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'k-NN is legally prohibited in advertising systems.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'At inference time, k-NN must calculate distances to '
                                                                'millions of stored records in memory, which is too '
                                                                'slow and memory-intensive for low-latency '
                                                                'production.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'k-NN cannot output probabilities.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'k-NN cannot be run in parallel.'}],
                                     'question': 'Why is standard k-NN rarely deployed for real-time recommendation or '
                                                 'ad-bidding systems serving millions of users with sub-millisecond '
                                                 'latency requirements?',
                                     'subtopic': 'Production Latency Limitations',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'KD-trees hierarchically partition space along coordinate axes, '
                                                    'allowing tree pruning in O(log n) time for low dimensions. '
                                                    'However, when d > 20, almost all branches overlap with the query '
                                                    'radius, forcing the tree to inspect every node (degrading to '
                                                    'O(n)).',
                                     'id': 'q-cml-l09-17',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'They partition space hierarchically to prune distant '
                                                                'branches in O(log n) time, but degrade back to O(n) '
                                                                'linear scans in high dimensions (d > 20) due to the '
                                                                'curse of dimensionality.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'They compress dataset rows by deleting 50% of '
                                                                'features.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'They convert k-NN into an Ordinary Least Squares '
                                                                'regression.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'They only work for datasets where all features are '
                                                                'integers.'}],
                                     'question': 'How do spatial tree structures like KD-Tree accelerate nearest '
                                                 'neighbor search over brute-force linear scans, and when do they '
                                                 'fail?',
                                     'subtopic': 'Spatial Indexing Structures',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1', 'opt-2', 'opt-4'],
                                     'difficulty': 'hard',
                                     'explanation': 'Options 1, 2, and 4 are fundamental theorems. Option 3 is false: '
                                                    'adding a new training point requires zero training; you simply '
                                                    'append it to the stored dataset.',
                                     'id': 'q-cml-l09-18',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'k-NN is non-parametric: it makes no strong '
                                                                'assumptions about the functional form of the data '
                                                                'distribution.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'With k = 1 and n -> infinity, the asymptotic error '
                                                                'rate of 1-NN is bounded by at most twice the optimal '
                                                                'Bayes error rate.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'k-NN requires retraining all weights w when a new '
                                                                'training observation is added to the database.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': True,
                                                        'text': 'Adding completely irrelevant noise features degrades '
                                                                'k-NN performance because noise corrupts distance '
                                                                'metrics.'}],
                                     'question': 'Which of the following statements represent true mathematical and '
                                                 'architectural invariants of K-Nearest Neighbours?',
                                     'subtopic': 'KNN Invariants',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'The Cover and Hart theorem is a landmark result in statistical '
                                                    'learning theory: with infinite data, half of all information in '
                                                    'an infinite sample is contained in the nearest neighbor alone, '
                                                    'bounding error at P_Bayes <= P_1NN <= 2 * P_Bayes.',
                                     'id': 'q-cml-l09-19',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'It proves that as sample size n approaches infinity, '
                                                                'the probability of error of the simple 1-NN '
                                                                'classifier is bounded by at most 2 * P_Bayes (twice '
                                                                'the irreducible Bayes error).'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'It proves that 1-NN always achieves zero error on '
                                                                'test data.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It proves that k-NN is identical to decision trees.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It proves that Euclidean distance is superior to all '
                                                                'other metrics.'}],
                                     'question': 'What is the significance of the Cover and Hart (1967) theorem '
                                                 'regarding 1-Nearest Neighbor classification?',
                                     'subtopic': 'Cover and Hart Theorem',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'hard',
                                     'explanation': 'Label encoding nominal categories invents false Euclidean '
                                                    'distances (e.g. Red is distance 1 from Blue, but distance 2 from '
                                                    'Green). One-hot encoding creates orthogonal dimensions with '
                                                    'equidistant separation, or dedicated metrics like Gower distance '
                                                    'are used.',
                                     'id': 'q-cml-l09-20',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Use arbitrary label encoding (Red=1, Blue=2, Green=3) '
                                                                'and compute Euclidean distance directly.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Use One-Hot Encoding (or Hamming / Gower distance '
                                                                'metrics) to avoid inventing artificial Euclidean '
                                                                'distances between nominal categories.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Drop all categorical columns because distance cannot '
                                                                'be computed on non-continuous variables.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Replace all category names with their ASCII character '
                                                                'codes.'}],
                                     'question': "How can categorical string variables (e.g., Color in {'Red', 'Blue', "
                                                 "'Green'}) be properly handled in a distance-based k-NN model?",
                                     'subtopic': 'Categorical Features in KNN',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'hard',
                                     'explanation': 'In Scikit-Learn, ties are typically broken by closest neighbor '
                                                    'distance or by internal class index ordering. Using '
                                                    "distance-weighted voting (weights='distance') prevents exact "
                                                    'voting ties almost entirely.',
                                     'id': 'q-cml-l09-21',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'It crashes with an UnresolvedTieException.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'It breaks ties by picking the class whose nearest '
                                                                'neighbor is closest among the tied contenders, or '
                                                                'selects based on first encounter in the dataset.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It deletes the query point.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It randomly picks an integer between 1 and 6.'}],
                                     'question': 'In a multi-class problem (e.g., classes A, B, C) with k = 6, suppose '
                                                 'the 6 nearest neighbors produce a tie: 2 votes for A, 2 votes for B, '
                                                 '2 votes for C. How does Scikit-Learn resolve this deadlock?',
                                     'subtopic': 'Tie-Breaking Strategies',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'Linear models assume a flat hyperplane decision surface. When '
                                                    'data manifests as complex non-linear geometries (interlocking '
                                                    "rings, spirals, multimodal clusters), k-NN's locally adaptive "
                                                    'neighborhood consensus easily captures the true boundary.',
                                     'id': 'q-cml-l09-22',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'When the classes form highly non-linear, disjoint, or '
                                                                'concentric patterns (e.g., two interlocking spiral '
                                                                'arms or concentric circles).'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'When the dataset has 10,000,000 features and 100 '
                                                                'rows.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'When the relationship between features and target is '
                                                                'perfectly linear.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'When all features have zero variance.'}],
                                     'question': 'Under what data geometry is a non-parametric model like k-NN '
                                                 'dramatically superior to linear models (like Linear or Logistic '
                                                 'Regression)?',
                                     'subtopic': 'Non-Parametric Advantage',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1', 'opt-2', 'opt-3', 'opt-4'],
                                     'difficulty': 'hard',
                                     'explanation': 'All four properties define a formal metric space. Distance '
                                                    'functions violating these (such as asymmetric KL-divergence) are '
                                                    'divergences, not formal distance metrics.',
                                     'id': 'q-cml-l09-23',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'Symmetry: d(x, z) = d(z, x)'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Non-negativity: d(x, z) >= 0'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'Triangle Inequality: d(x, z) <= d(x, u) + d(u, z)'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': True,
                                                        'text': 'Identity: d(x, z) = 0 if and only if x = z'}],
                                     'question': 'Which of the following mathematical properties are required for a '
                                                 'function d(x, z) to be considered a valid metric in metric space?',
                                     'subtopic': 'Metric Space Axioms',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'hard',
                                     'explanation': 'Standard k-NN weights all dimensions equally in Euclidean space. '
                                                    'Twenty noise dimensions contribute 20 random squared differences '
                                                    'to the distance sum, completely corrupting true neighborhood '
                                                    'proximity.',
                                     'id': 'q-cml-l09-24',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'k-NN automatically ignores the 20 noise features by '
                                                                'setting their weights to zero.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'k-NN performance degrades severely because the 20 '
                                                                'noise dimensions dominate the distance calculations, '
                                                                'washing out the true signal of x1 and x2.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'k-NN accuracy improves because more features always '
                                                                'provide more information.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'It converts k-NN into a decision tree.'}],
                                     'question': 'Suppose you have a 3-dimensional dataset where features x1 and x2 '
                                                 'contain strong predictive signal, but 20 pure random Gaussian noise '
                                                 'features (x3 ... x22) are added. How does this affect k-NN '
                                                 'performance?',
                                     'subtopic': 'Impact of Irrelevant Features',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'hard',
                                     'explanation': 'PCA projects high-dimensional coordinates into a compact '
                                                    'low-dimensional space (e.g. 100 features down to 10 principal '
                                                    'components). This eliminates redundant correlated noise and '
                                                    'restores meaningful distance gradients between nearest and '
                                                    'farthest neighbors.',
                                     'id': 'q-cml-l09-25',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'It projects high-dimensional data onto a '
                                                                'low-dimensional subspace that captures maximum '
                                                                'variance, discarding noise dimensions and restoring '
                                                                'distance metric contrast.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'It increases the number of features to infinity.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'It converts k-NN from a lazy learner into an eager '
                                                                'learner.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'PCA eliminates the need to choose hyperparameter k.'}],
                                     'question': 'How does applying Principal Component Analysis (PCA) prior to k-NN '
                                                 'help mitigate the curse of dimensionality?',
                                     'subtopic': 'Curse Remediation with PCA',
                                     'type': 'single_choice'}]},
    'schema_version': 1,
    'sections': [   {   'body': '### 1.1 The Lazy Learning Paradigm: Zero Training, Heavy Inference\n'
                                '\n'
                                'Most machine learning algorithms we study (Linear Regression, Logistic Regression, '
                                'Decision Trees, Support Vector Machines) belong to the family of **Eager Learners**:\n'
                                '- During the training phase, they analyze the training dataset, solve an optimization '
                                'problem, extract abstract parameters (weights $\\mathbf{w}$, split rules), and then '
                                '**discard the raw training data**.\n'
                                '- At inference time, predicting a new observation requires only evaluating a compact '
                                'mathematical formula: $\\hat{y} = \\sigma(\\mathbf{w}^T \\mathbf{x} + w_0)$ or '
                                'traversing a pre-built tree.\n'
                                '- Inference is instantaneous ($O(d)$ or $O(\\text{depth})$), and the model footprint '
                                'in RAM is tiny (just the weights).\n'
                                '\n'
                                'In stark contrast, **$k$-Nearest Neighbors ($k$-NN)** is a classic **Lazy Learner '
                                '(Instance-Based Learner / Memory-Based Learner)**:\n'
                                '- **Training Phase ($O(1)$ Time)**: The algorithm does virtually zero computation '
                                'during training. It simply memorizes and stores the training feature vectors '
                                '$\\mathbf{X} \\in \\mathbb{R}^{n \\times d}$ and targets $\\mathbf{y} \\in '
                                '\\mathbb{R}^n$ directly in memory (or organizes them into spatial index trees).\n'
                                '- **Inference Phase ($O(n \\cdot d)$ Time)**: When a query point $\\mathbf{x}_q$ '
                                'arrives, the algorithm computes distances between $\\mathbf{x}_q$ and **every single '
                                'stored training point**, finds the $k$ closest observations, and aggregates their '
                                'labels.\n'
                                '- **Memory Footprint**: The model **is** the entire training dataset. For a dataset '
                                'with $n = 1,000,000$ rows and $d = 300$ dense embedding features (float64), storing '
                                'the model in RAM requires $10^6 \\times 300 \\times 8 \\text{ bytes} \\approx 2.4 '
                                '\\text{ GB}$ of physical memory just to serve predictions!\n'
                                '\n'
                                '```\n'
                                'Eager Learning vs. Lazy Learning Workflow:\n'
                                '   Eager Learning (e.g., Logistic Regression / Neural Net):\n'
                                '      [ Training Data ] ──► [ Intensive Optimization (GD / Adam) ] ──► [ Model '
                                'Weights w ]\n'
                                '                                                                                │\n'
                                '      Query Point x_q ──────────────────────────────────────────────────────────┴─► '
                                'Instant Pred: O(d)\n'
                                '\n'
                                '   Lazy Learning (k-NN):\n'
                                '      [ Training Data ] ──► [ Zero Optimization! Store in RAM ] ──► Stored Database '
                                'in Memory (O(n*d) RAM)\n'
                                '                                                                                │\n'
                                '      Query Point x_q ──► [ Compute Distances to ALL n Points ] ────────────────┴─► '
                                'Query Time: O(n*d)\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.2 Algorithmic Formulation: Classification & Regression Rules\n'
                                '\n'
                                '#### 1. Classification (Majority Voting)\n'
                                'Given a query point $\\mathbf{x}_q$, identify the set $\\mathcal{N}_k(\\mathbf{x}_q)$ '
                                'containing the indices of the $k$ closest training points under chosen metric '
                                '$D(\\cdot, \\cdot)$.\n'
                                'The predicted class $\\hat{y}$ is determined by the mode (plurality / majority '
                                'vote):\n'
                                '\n'
                                '$$\\hat{y}(\\mathbf{x}_q) = \\operatorname{mode}\\left(\\{y^{(i)} \\mid i \\in '
                                '\\mathcal{N}_k(\\mathbf{x}_q)\\}\\right)$$\n'
                                '\n'
                                'The estimated posterior class probability for class $c$ is the local empirical '
                                'proportion:\n'
                                '$$\\hat{P}(Y = c \\mid \\mathbf{x}_q) = \\frac{1}{k} \\sum_{i \\in '
                                '\\mathcal{N}_k(\\mathbf{x}_q)} \\mathbb{I}(y^{(i)} = c)$$\n'
                                '\n'
                                '#### 2. Regression (Neighborhood Averaging)\n'
                                'In regression, targets $y \\in \\mathbb{R}$ are continuous quantities (e.g., house '
                                'prices, hospital length of stay):\n'
                                '\n'
                                '$$\\hat{y}(\\mathbf{x}_q) = \\frac{1}{k} \\sum_{i \\in \\mathcal{N}_k(\\mathbf{x}_q)} '
                                'y^{(i)}$$\n'
                                '\n'
                                '*Robust Variant*: Instead of the arithmetic mean, we can compute the **median** of '
                                'the $k$ neighbors to insulate the prediction from local extreme outliers or recording '
                                'anomalies.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.3 Concrete Hand-Calculated Regression Walkthrough: Uniform vs. Distance '
                                'Weighting\n'
                                '\n'
                                'Suppose an automated valuation model predicts house price for a query home $Q$. Its '
                                '$k = 5$ nearest neighbors in feature space have the following actual selling prices '
                                'and distances:\n'
                                '- Neighbor 1: Price $y_1 = 320{,}000\\text{ USD}$, Distance $d_1 = 1.0$ km\n'
                                '- Neighbor 2: Price $y_2 = 340{,}000\\text{ USD}$, Distance $d_2 = 1.5$ km\n'
                                '- Neighbor 3: Price $y_3 = 350{,}000\\text{ USD}$, Distance $d_3 = 2.0$ km\n'
                                '- Neighbor 4: Price $y_4 = 390{,}000\\text{ USD}$, Distance $d_4 = 3.0$ km\n'
                                '- Neighbor 5: Price $y_5 = 450{,}000\\text{ USD}$, Distance $d_5 = 5.0$ km\n'
                                '\n'
                                '#### Method A: Uniform Average ($k = 5$)\n'
                                'Every neighbor gets equal weight $w_i = \\frac{1}{5} = 0.20$:\n'
                                '$$\\hat{y}_{\\text{uniform}} = \\frac{320 + 340 + 350 + 390 + 450}{5} = '
                                '\\frac{1{,}850}{5} = \\mathbf{370{,}000\\text{ USD}}$$\n'
                                '\n'
                                '#### Method B: Inverse Distance Weighting ($w_i = 1 / d_i$)\n'
                                'Points that are geographically and architecturally closer should exert stronger '
                                'influence on the predicted valuation:\n'
                                '- $w_1 = 1 / 1.0 = 1.0000$\n'
                                '- $w_2 = 1 / 1.5 \\approx 0.6667$\n'
                                '- $w_3 = 1 / 2.0 = 0.5000$\n'
                                '- $w_4 = 1 / 3.0 \\approx 0.3333$\n'
                                '- $w_5 = 1 / 5.0 = 0.2000$\n'
                                '- Sum of weights $\\sum_{i=1}^5 w_i = 1.0000 + 0.6667 + 0.5000 + 0.3333 + 0.2000 = '
                                '\\mathbf{2.7000}$\n'
                                '\n'
                                'Normalized weights $\\tilde{w}_i = w_i / \\sum w_j$:\n'
                                '- $\\tilde{w}_1 = 1.0000 / 2.7000 \\approx 0.3704$ ($37.0\\%$ of total vote)\n'
                                '- $\\tilde{w}_2 = 0.6667 / 2.7000 \\approx 0.2469$ ($24.7\\%$ of total vote)\n'
                                '- $\\tilde{w}_3 = 0.5000 / 2.7000 \\approx 0.1852$ ($18.5\\%$ of total vote)\n'
                                '- $\\tilde{w}_4 = 0.3333 / 2.7000 \\approx 0.1235$ ($12.3\\%$ of total vote)\n'
                                '- $\\tilde{w}_5 = 0.2000 / 2.7000 \\approx 0.0741$ ($7.4\\%$ of total vote)\n'
                                '\n'
                                '$$\\hat{y}_{\\text{weighted}} = 0.3704(320,000) + 0.2469(340,000) + 0.1852(350,000) + '
                                '0.1235(390,000) + 0.0741(450,000)$$\n'
                                '$$\\hat{y}_{\\text{weighted}} = 118,528 + 83,946 + 64,820 + 48,165 + 33,345 = '
                                '\\mathbf{348{,}804\\text{ USD}}$$\n'
                                '\n'
                                '#### Method C: Gaussian Radial Basis Function (RBF) Kernel Weighting\n'
                                'Instead of inverse distance, standard kernel regression uses a smooth Gaussian '
                                'decay:\n'
                                '$$w_i = \\exp\\left(-\\frac{d_i^2}{2\\sigma^2}\\right)$$\n'
                                'Where bandwidth parameter $\\sigma$ dictates the radius of neighborhood influence:\n'
                                'Suppose $\\sigma = 2.0$ km ($\\implies 2\\sigma^2 = 8.0$):\n'
                                '- $w_1 = \\exp(-1.0^2 / 8.0) = \\exp(-0.125) \\approx \\mathbf{0.8825}$\n'
                                '- $w_2 = \\exp(-1.5^2 / 8.0) = \\exp(-0.28125) \\approx \\mathbf{0.7548}$\n'
                                '- $w_3 = \\exp(-2.0^2 / 8.0) = \\exp(-0.500) \\approx \\mathbf{0.6065}$\n'
                                '- $w_4 = \\exp(-3.0^2 / 8.0) = \\exp(-1.125) \\approx \\mathbf{0.3247}$\n'
                                '- $w_5 = \\exp(-5.0^2 / 8.0) = \\exp(-3.125) \\approx \\mathbf{0.0439}$\n'
                                '- Total sum: $\\sum w_i = 0.8825 + 0.7548 + 0.6065 + 0.3247 + 0.0439 = '
                                '\\mathbf{2.6124}$\n'
                                '\n'
                                'Notice how the distant neighbor at $5.0$ km receives only a tiny $0.0439$ weight '
                                'under the Gaussian kernel ($1.7\\%$ of influence), naturally filtering out distant '
                                'noise!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.4 Voronoi Tessellation & The Cover-Hart Asymptotic Theoretical Bound\n'
                                '\n'
                                'When $k = 1$, the feature space is partitioned into convex polyhedral cells called a '
                                '**Voronoi Diagram (Voronoi Tessellation)**:\n'
                                'For each training point $\\mathbf{x}^{(i)}$, its Voronoi cell $V(\\mathbf{x}^{(i)})$ '
                                'contains all query locations in $\\mathbb{R}^d$ closer to $\\mathbf{x}^{(i)}$ than to '
                                'any other training sample:\n'
                                '$$V(\\mathbf{x}^{(i)}) = \\left\\{ \\mathbf{x} \\in \\mathbb{R}^d \\mid '
                                '\\|\\mathbf{x} - \\mathbf{x}^{(i)}\\| \\le \\|\\mathbf{x} - \\mathbf{x}^{(j)}\\| \\; '
                                '\\forall j \\ne i \\right\\}$$\n'
                                '\n'
                                '```\n'
                                'Voronoi Tessellation (k = 1 Partitioning of Feature Space):\n'
                                '        x2 ^\n'
                                '           │      \\      /             * = Class 1 (Positive)\n'
                                '           │       \\ *  /              o = Class 0 (Negative)\n'
                                '           │   *    \\  /      *\n'
                                '           │  ───────┼───────────────\n'
                                '           │   o    / \\        o\n'
                                '           │       /   \\   o\n'
                                '           │      /  o  \\\n'
                                '           +─────/───────\\──────────► x1\n'
                                '```\n'
                                '\n'
                                '#### The Celebrated Cover & Hart (1967) Theorem:\n'
                                'One of the most foundational mathematical proofs in statistical pattern recognition '
                                'demonstrates that the humble 1-NN rule has extraordinary asymptotic guarantees:\n'
                                'Let $R^*$ denote the **Bayes Optimal Error Rate** (the absolute theoretical lower '
                                'bound on classification error achievable by an omniscient observer with perfect '
                                'knowledge of the true posterior probability distributions $P(Y \\mid X)$).\n'
                                'As sample size $n \\to \\infty$, the asymptotic error rate of the 1-NN classifier '
                                '$R_{\\text{1-NN}}$ satisfies:\n'
                                '\n'
                                '$$R^* \\le R_{\\text{1-NN}} \\le 2R^*(1 - R^*) \\le 2R^*$$\n'
                                '\n'
                                '> **Theoretical Milestone**:\n'
                                '> No matter how arbitrarily complex or non-linear the underlying probability '
                                'distributions are, given enough training data, **the error rate of the nearest '
                                'neighbor classifier is bounded above by at most twice the optimal Bayes error**!\n'
                                '> Formally, if the optimal Bayes error is $5\\%$, the 1-NN classifier will never '
                                'exceed $2(0.05)(0.95) = 9.5\\%$ error as $n \\to \\infty$. Half of all classification '
                                'information resides in the single nearest neighbor.',
                        'citations': [   'Cover, T., & Hart, P. (1967). Nearest neighbor pattern classification. IEEE '
                                         'Transactions on Information Theory, 13(1), 21-27.',
                                         'Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer, '
                                         'Chapter 2.'],
                        'heading': '1. Instance-Based Learning: The Lazy Paradigm of k-NN',
                        'section_id': 'cml-l09-sec01'},
                    {   'body': '### 2.1 The Minkowski Distance Family\n'
                                '\n'
                                'Distance is the fundamental yardstick of $k$-NN. The general mathematical formulation '
                                'for vector distance between $\\mathbf{x}, \\mathbf{z} \\in \\mathbb{R}^d$ is the '
                                '**Minkowski Distance** of order $p$:\n'
                                '\n'
                                '$$D_p(\\mathbf{x}, \\mathbf{z}) = \\|\\mathbf{x} - \\mathbf{z}\\|_p = \\left( '
                                '\\sum_{j=1}^d |x_j - z_j|^p \\right)^{1/p}$$\n'
                                '\n'
                                '```\n'
                                'Unit Circles (Points at Distance = 1.0 from Origin) Across Minkowski Orders:\n'
                                '     Manhattan (p = 1)          Euclidean (p = 2)          Chebyshev (p -> inf)\n'
                                '           x2 ^                       x2 ^                       x2 ^\n'
                                '            1 |    /\\                  1 |   .---.                1 | ┌───────┐\n'
                                '              |   /  \\                   |  /     \\                 | │       │\n'
                                '      -1 -----+----+----+ 1      -1 -----+--+-----+--+ 1    -1 -----+─┼───────┼─ 1\n'
                                '              |   \\  /                   |  \\     /                 | │       │\n'
                                "           -1 |    \\/                 -1 |   '---'               -1 | └───────┘\n"
                                '              +---------> x1             +---------> x1             +---------> x1\n'
                                '             Diamond                     Circle                     Square\n'
                                '```\n'
                                '\n'
                                '#### 1. Manhattan Distance ($p = 1$, City Block / Taxicab Distance)\n'
                                '$$D_1(\\mathbf{x}, \\mathbf{z}) = \\sum_{j=1}^d |x_j - z_j|$$\n'
                                '- Measures movement strictly along orthogonal coordinate axes (like a taxi navigating '
                                'the grid layout of Manhattan).\n'
                                '- **Outlier Robustness**: Because coordinate differences are not squared, a massive '
                                'anomaly along one single feature does not disproportionately dominate the overall '
                                'metric.\n'
                                '- Recommended when working in higher dimensions or when data has heavy-tailed noise.\n'
                                '\n'
                                '#### 2. Euclidean Distance ($p = 2$, Ruler / L2 Distance)\n'
                                '$$D_2(\\mathbf{x}, \\mathbf{z}) = \\sqrt{\\sum_{j=1}^d (x_j - z_j)^2}$$\n'
                                '- The standard straight-line distance in Euclidean geometry.\n'
                                '- **Isotropic**: Rotationally invariant; distances do not depend on the orientation '
                                'of the coordinate axes.\n'
                                '- Highly sensitive to extreme single-feature deviations because coordinate errors are '
                                'squared before summing.\n'
                                '\n'
                                '#### 3. Chebyshev Distance ($p \\to \\infty$, Chessboard / L-Infinity Distance)\n'
                                '$$D_\\infty(\\mathbf{x}, \\mathbf{z}) = \\lim_{p \\to \\infty} \\left( \\sum_{j=1}^d '
                                '|x_j - z_j|^p \\right)^{1/p} = \\max_{j \\in \\{1, \\dots, d\\}} |x_j - z_j|$$\n'
                                '- Measures the number of moves a King needs to travel between two squares on an $8 '
                                '\\times 8$ chessboard (since the King can move diagonally, horizontally, or '
                                'vertically in 1 step).\n'
                                '- Reflects the single worst-case dimensional difference between two feature vectors.\n'
                                '\n'
                                '#### 4. Cosine Similarity & Cosine Distance\n'
                                'When vector magnitude is irrelevant and only the **angular orientation** carries '
                                'meaning (e.g., text document classification where document length varies, or facial '
                                'recognition embeddings):\n'
                                '\n'
                                '$$\\text{Cosine Similarity} = \\cos(\\theta) = \\frac{\\mathbf{x} \\cdot '
                                '\\mathbf{z}}{\\|\\mathbf{x}\\|_2 \\|\\mathbf{z}\\|_2} = \\frac{\\sum x_j '
                                'z_j}{\\sqrt{\\sum x_j^2}\\sqrt{\\sum z_j^2}} \\in [-1, 1]$$\n'
                                '$$\\text{Cosine Distance} = 1 - \\cos(\\theta) \\in [0, 2]$$\n'
                                '\n'
                                '#### 5. Mahalanobis Distance (Covariance-Aware Distance)\n'
                                'Standard Euclidean distance implicitly assumes that all features are uncorrelated and '
                                'have equal variance ($\\mathbf{\\Sigma} = \\mathbf{I}$). When features are strongly '
                                'correlated (e.g., Height and Weight), Euclidean distance distorts true statistical '
                                'similarity.\n'
                                'The **Mahalanobis Distance** scales differences by the inverse covariance matrix '
                                '$\\mathbf{\\Sigma}^{-1}$:\n'
                                '\n'
                                '$$D_M(\\mathbf{x}, \\mathbf{z}) = \\sqrt{(\\mathbf{x} - \\mathbf{z})^T '
                                '\\mathbf{\\Sigma}^{-1} (\\mathbf{x} - \\mathbf{z})}$$\n'
                                '\n'
                                '- Warps space so that level curves of equal distance are ellipsoids aligned with the '
                                'principal axes of data spread.\n'
                                '- Statistically equivalent to standardizing features and decorrelating them via PCA '
                                'whitening before calculating Euclidean distance!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.2 Concrete Hand-Calculated Walkthrough: 2D Neighbor Ranking Reversal\n'
                                '\n'
                                'Suppose a query point arrives at $\\mathbf{x}_q = (3.0, 4.0)$, and we have three '
                                'candidate training samples in the database:\n'
                                '- Point $A = (1.0, 2.0)$ with Class 1\n'
                                '- Point $B = (4.0, 7.0)$ with Class 0\n'
                                '- Point $C = (6.0, 4.0)$ with Class 1\n'
                                '\n'
                                'Let us compute the exact distances under Manhattan ($L_1$), Euclidean ($L_2$), and '
                                'Chebyshev ($L_\\infty$) metrics:\n'
                                '\n'
                                '| Candidate Point | Coordinate $(x_1, x_2)$ | Coordinate Differences $(\\Delta x_1, '
                                '\\Delta x_2)$ | Manhattan Distance ($L_1$) | Euclidean Distance ($L_2$) | Chebyshev '
                                'Distance ($L_\\infty$) | Class Label |\n'
                                '| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n'
                                '| **Point A** | $(1.0, 2.0)$ | $|3 - 1| = 2.0, \\; |4 - 2| = 2.0$ | $2.0 + 2.0 = '
                                '\\mathbf{4.00}$ | $\\sqrt{2^2 + 2^2} = \\sqrt{8} \\approx \\mathbf{2.828}$ | Class 1 '
                                '|\n'
                                '| **Point B** | $(4.0, 7.0)$ | $|3 - 4| = 1.0, \\; |4 - 7| = 3.0$ | $1.0 + 3.0 = '
                                '\\mathbf{4.00}$ | $\\sqrt{1^2 + 3^2} = \\sqrt{10} \\approx \\mathbf{3.162}$ | Class 0 '
                                '|\n'
                                '| **Point C** | $(6.0, 4.0)$ | $|3 - 6| = 3.0, \\; |4 - 4| = 0.0$ | $3.0 + 0.0 = '
                                '\\mathbf{3.00}$ | $\\sqrt{3^2 + 0^2} = \\sqrt{9} = \\mathbf{3.000}$ | Class 1 |\n'
                                '\n'
                                '#### Neighbor Ranking Comparison:\n'
                                '- Under **Manhattan ($L_1$)**:\n'
                                '  1. Rank 1: **Point C** ($D_1 = 3.00$) $\\implies$ Prediction for $k=1$ is **Class '
                                '1**.\n'
                                '  2. Rank 2: **Point A & Point B Tied!** ($D_1 = 4.00$)\n'
                                '- Under **Euclidean ($L_2$)**:\n'
                                '  1. Rank 1: **Point A** ($D_2 = 2.828$) $\\implies$ Prediction for $k=1$ is **Class '
                                '1**.\n'
                                '  2. Rank 2: **Point C** ($D_2 = 3.000$)\n'
                                '  3. Rank 3: **Point B** ($D_2 = 3.162$)\n'
                                '- Under **Chebyshev ($L_\\infty$)**:\n'
                                '  1. Rank 1: **Point A** ($\\max(2, 2) = \\mathbf{2.00}$)\n'
                                '  2. Rank 2: **Point B & Point C Tied!** ($\\max(1, 3) = \\mathbf{3.00}$ vs $\\max(3, '
                                '0) = \\mathbf{3.00}$)\n'
                                '\n'
                                '> **Crucial Pedagogical Takeaway**:\n'
                                '> The choice of distance metric **alters the neighbor ranking**!\n'
                                '> Under Euclidean distance, Point $A$ is closest ($2.828 < 3.000$); under Manhattan '
                                'distance, Point $C$ is closest ($3.00 < 4.00$). Metric selection is a critical '
                                'hyperparameter that dictates which geometric patterns the algorithm prioritizes.',
                        'citations': [   'Deza, M. M., & Deza, E. (2009). Encyclopedia of Distances. Springer.',
                                         'Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of '
                                         'Statistical Learning (2nd ed.). Springer.'],
                        'heading': '2. Distance Metrics: Euclidean, Manhattan & The Minkowski Family',
                        'section_id': 'cml-l09-sec02'},
                    {   'body': '### 3.1 The Feature Magnitude Catastrophe\n'
                                '\n'
                                'Imagine building a loan default classifier with two features:\n'
                                '- $x_1$ = `Annual Salary` in dollars (ranges from 20,000 USD to 200,000 USD).\n'
                                '- $x_2$ = `Age` in years (ranges from $18$ to $75$).\n'
                                '\n'
                                'Suppose we have two applicants compared to query applicant $Q = (60{,}000, 30)$: \n'
                                '- Applicant $A_1 = (61{,}000, 30)$: Salary differs by 1,000 USD, Age is identical.\n'
                                '- Applicant $A_2 = (60{,}000, 70)$: Salary is identical, Age differs by 40 years (an '
                                'entire generation!).\n'
                                '\n'
                                'Let us compute Euclidean distance to query applicant $Q$:\n'
                                '$$D(Q, A_1) = \\sqrt{(60000 - 61000)^2 + (30 - 30)^2} = \\sqrt{(-1{,}000)^2 + 0^2} = '
                                '\\sqrt{1{,}000{,}000} = \\mathbf{1{,}000.0}$$\n'
                                '$$D(Q, A_2) = \\sqrt{(60000 - 60000)^2 + (30 - 70)^2} = \\sqrt{0^2 + (-40)^2} = '
                                '\\sqrt{1{,}600} = \\mathbf{40.0}$$\n'
                                '\n'
                                '#### The Disastrous Illusion:\n'
                                'The algorithm declares that $A_2$ (a 70-year-old pensioner) is **25 times closer** to '
                                'a 30-year-old millennial than $A_1$ (another 30-year-old who makes 1,000 USD more)!\n'
                                'Because Salary is measured in tens of thousands while Age is measured in tens, '
                                'squared salary differences completely overpower age differences by factors of '
                                'millions.\n'
                                'The algorithm is **completely blind to Age**! Distance metrics calculate isotropic '
                                'geometry; they cannot know that 1,000 USD is a negligible salary increment while 40 '
                                'years is a massive biological span.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.2 Standardization vs. MinMax Normalization\n'
                                '\n'
                                'To ensure every feature contributes equitably to geometric distance, features must be '
                                'transformed to a shared numerical scale:\n'
                                '\n'
                                '```\n'
                                'Feature Scaling Comparison:\n'
                                '┌─────────────────────┬────────────────────────────────────┬────────────────────────────────────┐\n'
                                '│ Attribute           │ StandardScaler (Z-Score)           │ '
                                'MinMaxScaler                       │\n'
                                '├─────────────────────┼────────────────────────────────────┼────────────────────────────────────┤\n'
                                '│ Mathematical Formula│ z = (x - μ) / σ                    │ x_norm = (x - '
                                'x_min)/(x_max - x_min│\n'
                                '│ Output Range        │ Unbounded, centered at 0 (σ = 1)   │ Strictly bounded in [0, '
                                '1]         │\n'
                                '│ Outlier Handling    │ Robust: preserves relative spread  │ Fragile: an extreme '
                                'outlier squashes│\n'
                                '│                     │ without compressing normal points  │ all normal data into a '
                                'tiny cluster│\n'
                                '│ Recommended Regime  │ Default for k-NN, SVM, Ridge/Lasso │ Bounded coordinates, '
                                'image pixels  │\n'
                                '└─────────────────────┴────────────────────────────────────┴────────────────────────────────────┘\n'
                                '```\n'
                                '\n'
                                '#### Re-evaluating the Loan Applicants After Z-Score Standardization:\n'
                                'Suppose in the population:\n'
                                '- Salary has mean $\\mu_{\\text{sal}} = 60{,}000\\text{ USD}$ and std '
                                '$\\sigma_{\\text{sal}} = 20{,}000\\text{ USD}$.\n'
                                '- Age has mean $\\mu_{\\text{age}} = 35$ and std $\\sigma_{\\text{age}} = 10$.\n'
                                '\n'
                                'Let us transform query $Q$ and candidate applicants $A_1, A_2$:\n'
                                '- Query $Q = (60k, 30) \\implies z_Q = \\left(\\frac{60k - 60k}{20k}, \\frac{30 - '
                                '35}{10}\\right) = (0.00, -0.50)$\n'
                                '- Applicant $A_1 = (61k, 30) \\implies z_{A_1} = \\left(\\frac{61k - 60k}{20k}, '
                                '\\frac{30 - 35}{10}\\right) = (+0.05, -0.50)$\n'
                                '- Applicant $A_2 = (60k, 70) \\implies z_{A_2} = \\left(\\frac{60k - 60k}{20k}, '
                                '\\frac{70 - 35}{10}\\right) = (0.00, +3.50)$\n'
                                '\n'
                                'Now compute standardized Euclidean distances:\n'
                                '$$D(z_Q, z_{A_1}) = \\sqrt{(0.00 - 0.05)^2 + (-0.50 - (-0.50))^2} = \\sqrt{0.0025 + '
                                '0} = \\mathbf{0.050}$$\n'
                                '$$D(z_Q, z_{A_2}) = \\sqrt{(0.00 - 0.00)^2 + (-0.50 - 3.50)^2} = \\sqrt{0 + (-4.0)^2} '
                                '= \\mathbf{4.000}$$\n'
                                '\n'
                                'Now, applicant $A_1$ is **80 times closer** to query $Q$ than $A_2$ ($0.050 \\ll '
                                '4.000$), perfectly aligning model geometry with true financial and demographic '
                                'reality!\n'
                                '\n'
                                '---\n'
                                '\n'
                                "### 3.3 Handling Categorical Features & Gower's Distance\n"
                                '\n'
                                'What happens when data contains a mix of numerical features and categorical features '
                                '(e.g., `City: [Delhi, Mumbai, Bengaluru]` or `Education: [High School, Bachelors, '
                                'Masters]`)?\n'
                                '- **The One-Hot Encoding Trap**:\n'
                                '  If a nominal feature with 10 categories is one-hot encoded into 10 binary columns '
                                '($0$ or $1$), two samples differing in that category have squared Euclidean distance '
                                '$(\\Delta x)^2 = 1^2 + 1^2 = 2.0$ (distance $\\sqrt{2} \\approx 1.414$).\n'
                                '  If numerical features are standardized to variance $1.0$, a single categorical '
                                'discrepancy can overpower several numerical features!\n'
                                "- **Gower's General Distance**:\n"
                                "  For mixed datasets, Gower's metric defines pairwise distance between observations "
                                '$\\mathbf{x}_i, \\mathbf{x}_j$ as:\n'
                                '  $$S_{ij} = \\frac{\\sum_{k=1}^p w_k s_{ijk}}{\\sum_{k=1}^p w_k}$$\n'
                                '  Where for numerical feature $k$, $s_{ijk} = 1 - \\frac{|x_{ik} - x_{jk}|}{R_k}$ '
                                '($R_k$ is the feature range), and for categorical feature $k$, $s_{ijk} = 1$ if '
                                "$x_{ik} == x_{jk}$ else $0$. Gower's distance is then $D_G = 1 - S_{ij} \\in [0, 1]$.",
                        'citations': [   'Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn, Keras, and '
                                         "TensorFlow (3rd ed.). O'Reilly Media, Chapter 2."],
                        'heading': '3. The Scaling Imperative: Why Unscaled Features Blind k-NN',
                        'section_id': 'cml-l09-sec03'},
                    {   'body': '### 4.1 The Bias-Variance Trade-Off Across $k$\n'
                                '\n'
                                'The number of neighbors $k$ is the master hyperparameter controlling model '
                                'complexity:\n'
                                '\n'
                                '```\n'
                                'The Spectrum of k:\n'
                                '  k = 1                                k = Optimal Sweet Spot                      k '
                                '= n\n'
                                '  '
                                '├──────────────────────────────────────────────┼────────────────────────────────────┤\n'
                                '  High Variance (Overfitting)          Balanced Generalization            High Bias '
                                '(Underfitting)\n'
                                '  Complex, jagged boundaries           Smooth boundary separating signal  Flat '
                                'boundary everywhere\n'
                                '  Train Error = 0.0!                   Optimal test set performance       Predicts '
                                'majority class\n'
                                '```\n'
                                '\n'
                                '| Hyperparameter Setting | Effective Degrees of Freedom | Model Complexity | Behavior '
                                'on Outliers & Noise |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **$k = 1$ (Minimum $k$)** | Maximum ($n$ parameters) | **Extreme Overfitting** '
                                '(High Variance). Training error is identically $0.0\\%$. | A single mislabeled '
                                'training point creates an isolated "island" in feature space that misclassifies '
                                'nearby test points. |\n'
                                '| **$k$ Small ($3 - 7$)** | High | Flexible, localized decision boundaries. | '
                                'Captures subtle non-linear boundaries while averaging out isolated noise spikes. |\n'
                                '| **$k$ Moderate ($11 - 25$)** | Balanced | **Optimal Trade-off**. Low generalization '
                                'error. | Broad statistical consensus; filters out measurement noise. |\n'
                                '| **$k = n$ (Maximum $k$)** | Minimum ($1$ parameter) | **Extreme Underfitting** '
                                '(High Bias). | Evaluates all $n$ samples in the dataset for every query, predicting '
                                'the global majority class everywhere. |\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.2 Non-Linear Decision Boundaries: Comparing Logistic Regression vs. $k$-NN\n'
                                '\n'
                                'In class, we visualized a synthetic dataset with 400 observations across two features '
                                '($F_1, F_2$) where classes overlap in non-linear curved geometries:\n'
                                '\n'
                                '```\n'
                                'Boundary Geometry Comparison:\n'
                                '   Logistic Regression (Parametric Linear):       k-NN (Non-Parametric Local):\n'
                                '        F2 ^                                           F2 ^\n'
                                '           │         /  Straight Line                     │        .---.  Flexible '
                                'Local Contour\n'
                                '           │  +  +  /   (Cannot bend!)                    │  +  + /     \\\n'
                                '           │   +   /  +                                   │   +  |   +   |\n'
                                '           │  ────/─────────                              │  ────+───────+──\n'
                                '           │  o  /   o                                    │  o  o \\     / o\n'
                                "           │    /  o                                      │        '---'\n"
                                '           +───/────────────────► F1                      +─────────────────► F1\n'
                                '```\n'
                                '\n'
                                '1. **Why Logistic Regression Struggles**:\n'
                                '   Logistic regression can only construct straight lines ($w_1 F_1 + w_2 F_2 + w_0 = '
                                '0$) or flat hyperplanes. If the true class boundary is circular, crescent-shaped, or '
                                'interleaved, a straight line will inevitably misclassify large clusters of points.\n'
                                '2. **Why $k$-NN Excels on Non-Linear Geometries**:\n'
                                '   Because $k$-NN makes zero assumptions about the functional form of the boundary, '
                                'it organically flexes and bends around complex geometric clusters, forming circular, '
                                'winding, or multi-modal boundary enclosures.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.3 Tie-Breaking Rules & Distance-Weighted Voting\n'
                                '\n'
                                '#### 1. Why $k$ Should Be Odd for Binary Classification\n'
                                'If $k = 4$ in binary classification, a query point might find 2 neighbors of Class 0 '
                                'and 2 neighbors of Class 1 ($2 - 2$ tie).\n'
                                'To prevent arbitrary tie-breaking, **always select odd values of $k$** ($k \\in \\{3, '
                                '5, 7, 9, \\dots\\}$) when solving binary classification problems.\n'
                                'For multi-class problems ($C > 2$), ties can still occur even with odd $k$ (e.g., '
                                '$k=5$ with 2 votes for Class A, 2 votes for Class B, 1 vote for Class C). Common '
                                'tie-breaking strategies include:\n'
                                '1. Fall back to 1-NN (pick the class of the single closest neighbor).\n'
                                '2. Weight votes by inverse distance.\n'
                                '3. Randomly break ties (non-deterministic).\n'
                                '\n'
                                "#### 2. Distance-Weighted Voting (`weights='distance'`)\n"
                                "In standard uniform voting (`weights='uniform'`), a neighbor located $0.001$ units "
                                'away has the exact same voting weight as a neighbor located $9.999$ units away.\n'
                                "Under **Distance-Weighted Voting**, each neighbor's vote is weighted inversely by its "
                                'distance:\n'
                                '\n'
                                '$$w_i = \\frac{1}{D(\\mathbf{x}_q, \\mathbf{x}^{(i)}) + \\epsilon}$$\n'
                                '\n'
                                'Where $\\epsilon$ is a tiny positive constant (e.g., $10^{-5}$) to prevent division '
                                'by zero if a query point coincides with a training point.\n'
                                '- Nearby neighbors exert a massive gravitational pull on the prediction.\n'
                                '- Distant background points on the periphery of the neighborhood have negligible '
                                'impact.',
                        'citations': [   'Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of '
                                         'Statistical Learning (2nd ed.). Springer, Chapter 2.',
                                         'James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). An Introduction '
                                         'to Statistical Learning. Springer, Chapter 2.'],
                        'heading': '4. Choosing k: Navigating the Bias-Variance Spectrum',
                        'section_id': 'cml-l09-sec04'},
                    {   'body': '### 5.1 The Geometry of High Dimensions: Space Becomes Exponentially Empty\n'
                                '\n'
                                'Human intuition is calibrated in 2D and 3D space, where volume is compact. In '
                                'high-dimensional machine learning ($d = 50, 100, 1000$), geometry behaves in bizarre, '
                                'counter-intuitive ways:\n'
                                '\n'
                                '> **The Unit Hypercube Paradox**:\n'
                                '> Suppose observations are uniformly distributed in a $d$-dimensional unit hypercube '
                                '$[0, 1]^d$.\n'
                                '> To capture a fraction $r$ of the data points in a localized neighborhood, we must '
                                'construct a hypercube of edge length $s$:\n'
                                '> $$\\text{Volume} = s^d = r \\implies s = r^{1/d}$$\n'
                                '\n'
                                'Let us calculate the required neighborhood edge length $s$ to capture just **10% of '
                                'the data ($r = 0.10$)**:\n'
                                '- In $d = 1$ dimension: $s = (0.10)^{1/1} = \\mathbf{0.10}$ (Requires only 10% of the '
                                'axis length).\n'
                                '- In $d = 2$ dimensions: $s = (0.10)^{1/2} \\approx \\mathbf{0.32}$ (Requires 32% of '
                                'each axis).\n'
                                '- In $d = 10$ dimensions: $s = (0.10)^{1/10} \\approx \\mathbf{0.794}$ (Must span '
                                "nearly 80% of each feature's entire range!).\n"
                                '- In $d = 100$ dimensions: $s = (0.10)^{1/100} \\approx \\mathbf{0.977}$ (Must span '
                                "98% of each feature's range!).\n"
                                '\n'
                                'To find even 10% of your nearest neighbors in 100-dimensional space, your "local '
                                'neighborhood" must stretch across **almost the entire breadth of the universe**!\n'
                                'Neighbors are no longer "local" in high dimensions.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.2 The Inscribed Hypersphere Volume Vanishing Theorem\n'
                                '\n'
                                'Consider a $d$-dimensional hypercube $[-1, 1]^d$ with side length $2$, whose total '
                                'volume is:\n'
                                '$$V_{\\text{cube}}(d) = 2^d$$\n'
                                'Inside this hypercube, inscribe a $d$-dimensional hypersphere of radius $R = 1$. The '
                                'volume of a $d$-dimensional sphere is given by:\n'
                                '$$V_{\\text{sphere}}(d) = \\frac{\\pi^{d/2}}{\\Gamma\\left(\\frac{d}{2} + '
                                '1\\right)}$$\n'
                                '\n'
                                'Let us compute the ratio of the volume of the inscribed sphere to the surrounding '
                                'cube as dimension $d$ grows:\n'
                                '$$\\text{Ratio}(d) = \\frac{V_{\\text{sphere}}(d)}{V_{\\text{cube}}(d)} = '
                                '\\frac{\\pi^{d/2}}{2^d \\cdot \\Gamma\\left(\\frac{d}{2} + 1\\right)}$$\n'
                                '\n'
                                '| Dimension $d$ | Hypercube Volume $2^d$ | Inscribed Hypersphere Volume | Sphere / '
                                'Cube Volume Ratio | Physical Meaning |\n'
                                '| :--- | :--- | :--- | :--- | :--- |\n'
                                '| **$d = 1$** | $2^1 = 2$ | $2.000$ | $1.0000$ ($100.0\\%$) | The sphere (line '
                                'segment) fills the entire box. |\n'
                                '| **$d = 2$** | $2^2 = 4$ | $\\pi \\approx 3.1416$ | $\\frac{\\pi}{4} \\approx '
                                '0.7854$ ($78.5\\%$) | A circle occupies most of the square. |\n'
                                '| **$d = 3$** | $2^3 = 8$ | $\\frac{4}{3}\\pi \\approx 4.1888$ | $\\frac{\\pi}{6} '
                                '\\approx 0.5236$ ($52.4\\%$) | A ball fills over half the cube. |\n'
                                '| **$d = 5$** | $2^5 = 32$ | $\\frac{8\\pi^2}{15} \\approx 5.2638$ | $0.1645$ '
                                '($16.5\\%$) | Most volume is now outside the sphere. |\n'
                                '| **$d = 10$** | $2^{10} = 1,024$ | $\\frac{\\pi^5}{120} \\approx 2.5502$ | $0.00249$ '
                                '($\\mathbf{0.25\\%}$) | Over $99.7\\%$ of volume is in the corners! |\n'
                                '| **$d = 20$** | $2^{20} \\approx 1.05 \\times 10^6$ | $\\approx 0.0258$ | $2.46 '
                                '\\times 10^{-8}$ ($\\mathbf{0.000002\\%}$) | The sphere volume is virtually zero. |\n'
                                '\n'
                                '$$\\lim_{d \\to \\infty} \\frac{V_{\\text{sphere}}(d)}{V_{\\text{cube}}(d)} = 0$$\n'
                                '\n'
                                '> **Geometrical Consequence**:\n'
                                '> In high dimensions, the interior volume of the hypersphere completely vanishes!\n'
                                '> **Almost 100% of the volume in high-dimensional space is concentrated in the spiky '
                                '"corners" of the hypercube.**\n'
                                '> Points do not cluster in the interior; they all lie along the outer shell!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.3 Metric Collapse: The Distance Concentration Phenomenon\n'
                                '\n'
                                'In 1999, Beyer et al. proved a mathematically devastating property of '
                                'high-dimensional metrics:\n'
                                'Under broad distributional assumptions, as dimensionality $d \\to \\infty$, the '
                                'distance to the **farthest point** and the distance to the **nearest point** converge '
                                'to the same value:\n'
                                '\n'
                                '$$\\lim_{d \\to \\infty} \\frac{D_{\\max} - D_{\\min}}{D_{\\min}} = 0$$\n'
                                '\n'
                                '```\n'
                                'Distance Concentration Ratio as Dimensionality Increases:\n'
                                '   (D_max - D_min) / D_min\n'
                                '      ^\n'
                                '      │  \\\n'
                                '      │   \\\n'
                                "      │    '.\n"
                                "      │      '--.\n"
                                "      │          '───────────────────► 0.0 (All points become equidistant!)\n"
                                '      +────────────────────────────────► Dimension d\n'
                                '      d = 2         d = 20        d = 100\n'
                                '```\n'
                                '\n'
                                '#### The Engineering Disaster:\n'
                                'If the nearest neighbor is at distance $10.00$ and the farthest neighbor is at '
                                'distance $10.01$, all data points are virtually equidistant from the query point.\n'
                                'The concept of a "nearest neighbor" completely collapses, and $k$-NN degrades into '
                                '**random neighbor selection**.\n'
                                '\n'
                                '#### Practical Remedies for the Curse of Dimensionality:\n'
                                '1. **Dimensionality Reduction**: Apply **PCA** or UMAP to compress $100$ features '
                                'down to the $10-15$ principal axes carrying $95\\%$ of variance.\n'
                                '2. **Feature Selection**: Use **Lasso (L1)** or Mutual Information to delete '
                                'uninformative noise features before computing distances.\n'
                                '3. **Domain Metrics**: Use Manhattan ($L_1$) distance, which degrades much more '
                                'gracefully in high dimensions than Euclidean ($L_2$) distance.',
                        'citations': [   'Bellman, R. (1957). Dynamic Programming. Princeton University Press.',
                                         'Beyer, K., Goldstein, J., Ramakrishnan, R., & Shaft, U. (1999). When is '
                                         "'nearest neighbor' meaningful? ICDT 1999, 217-235."],
                        'heading': '5. The Curse of Dimensionality & Metric Collapse',
                        'section_id': 'cml-l09-sec05'},
                    {   'body': '### 6.1 Computational Complexity: Brute Force vs. KD-Trees vs. Ball-Trees\n'
                                '\n'
                                'Evaluating distances against all $n$ training points for every query requires $O(n '
                                '\\cdot d)$ operations. For real-time applications (e.g., search engines, fraud '
                                'scoring with $n = 10^7$), brute-force search is far too slow.\n'
                                '\n'
                                '```\n'
                                'Spatial Indexing Strategies:\n'
                                '┌─────────────────┬──────────────────┬──────────────────┬──────────────────┬────────────────────────────────────┐\n'
                                '│ Algorithm       │ Training Build   │ Query Time       │ Space Complexity │ Optimal '
                                'Operational Regime         │\n'
                                '├─────────────────┼──────────────────┼──────────────────┼──────────────────┼────────────────────────────────────┤\n'
                                '│ **Brute Force** │ $O(1)$           │ $O(n \\cdot d)$   │ $O(n \\cdot d)$   │ Small '
                                'datasets ($n < 1,000$) or    │\n'
                                '│                 │ (Instant)        │ (Slowest)        │                  │ very '
                                'high dimensions ($d > 50$).   │\n'
                                '│ **KD-Tree**     │ $O(d \\cdot n\\log n│ $O(\\log n)$      │ $O(n \\cdot d)$   │ Low '
                                'dimensions ($d < 20$) with     │\n'
                                '│                 │                  │ (Fastest)        │                  │ '
                                'Euclidean/Manhattan metrics.       │\n'
                                '│ **Ball-Tree**   │ $O(d \\cdot n\\log n│ $O(\\log n)$      │ $O(n \\cdot d)$   │ '
                                'Moderate dimensions ($d \\le 40$)   │\n'
                                '│                 │                  │                  │                  │ and '
                                'arbitrary distance metrics.    │\n'
                                '└─────────────────┴──────────────────┴──────────────────┴──────────────────┴────────────────────────────────────┘\n'
                                '```\n'
                                '\n'
                                '#### Detailed KD-Tree Construction & Search Walkthrough:\n'
                                'A $k$-d tree (short for $k$-dimensional tree) recursively bisects feature space using '
                                'axis-aligned orthogonal hyperplanes:\n'
                                '1. **Cycle Dimensions**: At depth 0, split along axis $x_1$ at the median value. All '
                                'points with $x_1 < \\text{median}$ go to the left child; points with $x_1 \\ge '
                                '\\text{median}$ go to the right child.\n'
                                '2. At depth 1, split each subset along axis $x_2$ at their respective medians.\n'
                                '3. At depth $m$, split along axis $x_{(m \\bmod d) + 1}$.\n'
                                '4. **Query & Branch Pruning**:\n'
                                '   - Descend the tree to find the leaf containing query point $\\mathbf{x}_q$ '
                                '(candidate best neighbor at distance $r$).\n'
                                '   - Backtrack up the tree. For each parent node, check if a sphere of radius $r$ '
                                'centered at $\\mathbf{x}_q$ crosses the splitting hyperplane:\n'
                                '     $$|\\mathbf{x}_{q, \\text{split\\_axis}} - \\text{split\\_val}| < r$$\n'
                                '   - If the sphere crosses the hyperplane, the other subtree **must** be searched; if '
                                'it does not cross, the entire opposite branch is **pruned**, saving millions of '
                                'calculations!\n'
                                '   - In high dimensions ($d > 20$), the hypersphere almost always intersects every '
                                'dividing hyperplane, forcing the algorithm to visit virtually every node ($O(n)$ '
                                'collapse).\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 6.2 Production Scikit-Learn Pipeline: Hyperparameter Grid Search\n'
                                '\n'
                                '```python\n'
                                'import numpy as np\n'
                                'from sklearn.datasets import load_breast_cancer\n'
                                'from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold\n'
                                'from sklearn.neighbors import KNeighborsClassifier\n'
                                'from sklearn.preprocessing import StandardScaler\n'
                                'from sklearn.pipeline import Pipeline\n'
                                'from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score\n'
                                '\n'
                                '# 1. Load benchmark medical diagnostic dataset (30 continuous features)\n'
                                'data = load_breast_cancer()\n'
                                'X, y = data.data, data.target\n'
                                '\n'
                                '# 2. Strict Stratified Train / Test Partition (Prevent leakage)\n'
                                'X_train, X_test, y_train, y_test = train_test_split(\n'
                                '    X, y, test_size=0.25, random_state=42, stratify=y\n'
                                ')\n'
                                '\n'
                                '# 3. Encapsulate in Leak-Free Pipeline\n'
                                '# StandardScaler fits ONLY on training folds during CV to prevent data leakage!\n'
                                'knn_pipeline = Pipeline([\n'
                                '    ("scaler", StandardScaler()),\n'
                                '    ("knn", KNeighborsClassifier(algorithm="auto"))\n'
                                '])\n'
                                '\n'
                                '# 4. Hyperparameter Search Grid\n'
                                'param_grid = {\n'
                                '    "knn__n_neighbors": [1, 3, 5, 7, 9, 11, 15, 21, 29],\n'
                                '    "knn__weights": ["uniform", "distance"],\n'
                                '    "knn__metric": ["euclidean", "manhattan"]\n'
                                '}\n'
                                '\n'
                                '# 5. Execute Stratified 5-Fold Cross-Validation\n'
                                'cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n'
                                'grid_search = GridSearchCV(\n'
                                '    knn_pipeline,\n'
                                '    param_grid,\n'
                                '    cv=cv,\n'
                                '    scoring="roc_auc",\n'
                                '    n_jobs=-1\n'
                                ')\n'
                                'grid_search.fit(X_train, y_train)\n'
                                '\n'
                                '# 6. Evaluate Best Tuned Model on Untouched Test Set\n'
                                'best_model = grid_search.best_estimator_\n'
                                'y_probs = best_model.predict_proba(X_test)[:, 1]\n'
                                'y_preds = best_model.predict(X_test)\n'
                                '\n'
                                'test_auc = roc_auc_score(y_test, y_probs)\n'
                                '\n'
                                'print("=== BEST HYPERPARAMETER CONFIGURATION ===")\n'
                                'print(f"Optimal Parameters: {grid_search.best_params_}")\n'
                                'print(f"Best CV ROC-AUC:    {grid_search.best_score_:.4f}")\n'
                                'print(f"Holdout Test AUC:   {test_auc:.4f}")\n'
                                '\n'
                                'print("\\nConfusion Matrix:")\n'
                                'print(confusion_matrix(y_test, y_preds))\n'
                                'print("\\nClassification Report:")\n'
                                'print(classification_report(y_test, y_preds, target_names=data.target_names))\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 6.3 Diagnostic Failure Modes & Engineering Pitfalls\n'
                                '\n'
                                '| Engineering Pitfall | Root Mechanism | Catastrophic Consequence | Production '
                                'Solution |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **Omitting Feature Scaling** | Features with large numerical spans dominate '
                                'Euclidean sum of squares. | Small-scale features (e.g., Age) are completely ignored; '
                                'distance geometry corrupted. | Enforce `StandardScaler` inside a Scikit-Learn '
                                '`Pipeline`. |\n'
                                '| **Choosing Even $k$ in Binary Problems** | Equal neighbor voting counts split '
                                '50/50. | Arbitrary tie-breaking introduces non-deterministic random predictions. | '
                                'Always select odd $k$ values ($k \\in \\{3, 5, 7, \\dots\\}$). |\n'
                                '| **Deploying Brute-Force in Latency-Critical APIs** | $O(n \\cdot d)$ linear scan '
                                'over millions of stored records per query. | Inference latency exceeds SLA limits '
                                "(500ms+ per API call). | Use spatial indexing (`algorithm='ball_tree'`) or "
                                'approximate nearest neighbors (FAISS/HNSW). |\n'
                                '| **Running $k$-NN on $d > 100$ Features** | Distance concentration phenomenon: '
                                '$D_{\\max} \\approx D_{\\min}$. | All points become equidistant; algorithm degrades '
                                'to random coin flips. | Precede $k$-NN with PCA or Lasso feature selection to reduce '
                                'dimensions below 20. |\n'
                                '| **Scaling Categorical One-Hot Columns Inappropriately** | One-hot binary columns '
                                'span $0$ to $1$, creating artificial Euclidean leaps. | Distance metric is distorted '
                                "by arbitrary category card. | Use Gower's distance or target encoding, or standardize "
                                'continuous features appropriately. |\n'
                                '| **Data Leakage in Normalization** | Normalizing the entire dataset before '
                                'train-test split. | Test distribution information leaks into train scaling params '
                                '($\\mu, \\sigma$), giving optimistic validation metrics. | Fit scalers exclusively on '
                                'training splits inside `Pipeline`. |',
                        'citations': [   'Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. JMLR, '
                                         '12, 2825-2830.'],
                        'heading': '6. Hands-On Python Implementations & Algorithmic Indexing',
                        'section_id': 'cml-l09-sec06'}],
    'subject_code': 'CML',
    'summary': 'A comprehensive, intuitive masterclass on K-Nearest Neighbours (k-NN) and metric-space learning. '
               "Explores the non-parametric, instance-based paradigm where 'training' consists of memorizing data and "
               'inference computes local neighborhood majorities. Deconstructs Euclidean, Manhattan, and Minkowski '
               'distances, demonstrates why unscaled features blind the algorithm, maps the Bias-Variance tradeoff as '
               'k shifts from 1 to n, and proves why high-dimensional feature spaces suffer from distance '
               'concentration.',
    'tags': [   'K-Nearest Neighbours',
                'KNN',
                'Instance-Based Learning',
                'Lazy Learning',
                'Distance Metrics',
                'Euclidean Distance',
                'Manhattan Distance',
                'Minkowski Distance',
                'Bias-Variance Tradeoff',
                'Curse of Dimensionality',
                'Feature Scaling'],
    'term': 'Term 5',
    'topic_title': '9. K-Nearest Neighbours (k-NN), Distance Metrics & The Curse of Dimensionality'}

