"""
Data definition for data_cml_l15:
"""

L15_DATA = {   'approval_status': 'approved',
    'key_takeaways': [   'Dimensionality reduction compresses high-dimensional feature spaces into fewer informative '
                         'axes to enable 2D/3D visualization, accelerate models, and eliminate multicollinearity.',
                         'In PCA, variance equals information: a feature axis with zero variance provides zero '
                         'distinguishing power, whereas directions of widest spread preserve maximum data geometry.',
                         'Because PCA is variance-greedy, features must be standardized (StandardScaler) beforehand; '
                         'otherwise, columns measured in large arbitrary units will artificially dominate PC1.',
                         'Geometrically, PCA rotates the coordinate axes: PC1 aligns with the direction of maximal '
                         'variance, and PC2 is strictly orthogonal (at 90 degrees) to PC1 capturing the next greatest '
                         'spread.',
                         'Eigenvectors of the covariance matrix define the principal component axis directions; '
                         'eigenvalues represent the exact amount of variance along each direction.',
                         'The Explained Variance Ratio is the eigenvalue divided by the sum of all eigenvalues; scree '
                         'plots and cumulative variance curves determine how many components to keep.',
                         'PCA must always be fitted strictly on the training set (e.g. inside a Pipeline) to prevent '
                         'test data leakage into the principal components.'],
    'last_updated': '2026-10-18T00:00:00Z',
    'learning_objectives': [   'Explain why dimensionality reduction is necessary for visualization, computational '
                               'speed, noise filtering, and distance metric stability.',
                               'Articulate the geometric intuition of PCA: rotating coordinate axes to align with '
                               'directions of maximum data spread (variance).',
                               'Demonstrate why standardizing features (mean 0, variance 1) is mandatory before PCA to '
                               'avoid arbitrary physical unit dominance.',
                               'Define eigenvalues and eigenvectors in plain language and calculate explained variance '
                               'ratios step-by-step.',
                               'Select the optimal number of principal components using scree plots, cumulative '
                               'variance thresholds, and cross-validated downstream models.',
                               'Implement PCA pipelines in Scikit-Learn without data leakage for high-dimensional '
                               'visualization and lossy data compression.'],
    'note_id': 'cml-t5-l15',
    'quiz': {   'questions': [   {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': 'PCA rotates coordinate axes to find orthogonal directions that '
                                                    'maximize the variance (spread) of the data, capturing the largest '
                                                    'possible amount of information in the fewest components.',
                                     'id': 'q1',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'To find orthogonal directions (principal components) '
                                                                'along which the variance of the projected data is '
                                                                'maximized'},
                                                    {   'id': 'opt2',
                                                        'text': 'To maximize the separation between labeled class '
                                                                'centroids'},
                                                    {   'id': 'opt3',
                                                        'text': 'To fit a non-linear polynomial curve through all data '
                                                                'points'},
                                                    {   'id': 'opt4',
                                                        'text': 'To convert continuous features into categorical '
                                                                'one-hot vectors'}],
                                     'question': 'What is the primary geometric objective of Principal Component '
                                                 'Analysis (PCA)?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': 'If one feature is measured in thousands (e.g. income in rupees) '
                                                    'and another in single digits (e.g. household size), the unscaled '
                                                    'variance of income will be millions of times larger, forcing PC1 '
                                                    'to point directly along income purely due to arbitrary unit '
                                                    'choice.',
                                     'id': 'q2',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Because PCA is variance-greedy; unscaled features '
                                                                'with large numerical magnitudes will artificially '
                                                                'dominate the first principal component regardless of '
                                                                'their true importance'},
                                                    {   'id': 'opt2',
                                                        'text': 'Because PCA algorithms cannot calculate square roots '
                                                                'on unscaled numbers'},
                                                    {   'id': 'opt3',
                                                        'text': 'Because unscaled features cause the target vector y '
                                                                'to become undefined'},
                                                    {   'id': 'opt4',
                                                        'text': 'Because Scikit-Learn will raise a syntax error if '
                                                                'inputs are not normalized'}],
                                     'question': 'Why is feature standardization (e.g. StandardScaler) strictly '
                                                 'recommended before running PCA on tabular data with mixed physical '
                                                 'units?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': 'By definition, all principal components are constructed to be '
                                                    'mutually orthogonal (at 90 degrees to each other), which '
                                                    'guarantees that the correlation between any pair of principal '
                                                    'components is exactly zero.',
                                     'id': 'q3',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Exactly 90 degrees (orthogonal / perpendicular)'},
                                                    {'id': 'opt2', 'text': '45 degrees'},
                                                    {   'id': 'opt3',
                                                        'text': '180 degrees (parallel in opposite directions)'},
                                                    {'id': 'opt4', 'text': '0 degrees (completely identical)'}],
                                     'question': 'What is the geometric angle between the First Principal Component '
                                                 '(PC1) and the Second Principal Component (PC2)?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': 'For any principal component direction (eigenvector), its '
                                                    'corresponding eigenvalue lambda represents the numerical variance '
                                                    'of the data projected onto that axis.',
                                     'id': 'q4',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'The amount of variance captured along each '
                                                                'corresponding eigenvector (principal component '
                                                                'direction)'},
                                                    {   'id': 'opt2',
                                                        'text': 'The number of training samples assigned to each '
                                                                'cluster'},
                                                    {   'id': 'opt3',
                                                        'text': 'The classification accuracy on the holdout validation '
                                                                'set'},
                                                    {   'id': 'opt4',
                                                        'text': 'The learning rate required for gradient descent'}],
                                     'question': 'In the context of the covariance matrix of standardized data, what '
                                                 'do the eigenvalues represent?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': 'The explained variance ratio for component k is lambda_k / '
                                                    'sum(lambda_j), representing the fraction of total dataset '
                                                    'variance explained by that specific component.',
                                     'id': 'q5',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'By dividing eigenvalue lambda_k by the sum of all '
                                                                'eigenvalues'},
                                                    {   'id': 'opt2',
                                                        'text': 'By multiplying eigenvalue lambda_k by the number of '
                                                                'samples N'},
                                                    {   'id': 'opt3',
                                                        'text': 'By taking the square root of the mean squared error'},
                                                    {'id': 'opt4', 'text': 'By subtracting lambda_k from 1.0'}],
                                     'question': "How is the 'Explained Variance Ratio' of the k-th principal "
                                                 'component calculated?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': 'A scree plot displays the variance explained by each principal '
                                                    "component in decreasing order. The 'elbow' or knee point "
                                                    'indicates where adding more components yields diminishing '
                                                    'returns.',
                                     'id': 'q6',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'A bar or line chart showing the explained variance '
                                                                'ratio for each principal component, used to visually '
                                                                "locate the 'elbow'"},
                                                    {   'id': 'opt2',
                                                        'text': 'A 3D scatter plot of raw unstandardized features'},
                                                    {   'id': 'opt3',
                                                        'text': 'A plot of training loss versus gradient descent '
                                                                'iterations'},
                                                    {   'id': 'opt4',
                                                        'text': 'A confusion matrix displaying true positives and '
                                                                'false positives'}],
                                     'question': "What is a 'Scree Plot' in PCA analysis?",
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1', 'opt2', 'opt3'],
                                     'difficulty': 'easy',
                                     'explanation': 'PCA is widely used for 2D/3D visualization, lossy compression, '
                                                    'and decorrelating features to prevent multicollinearity. It is an '
                                                    'unsupervised technique and cannot generate supervised ground '
                                                    'truth labels.',
                                     'id': 'q7',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Projecting high-dimensional data (e.g., 64-pixel '
                                                                'images) down to 2D for visual exploration'},
                                                    {   'id': 'opt2',
                                                        'text': 'Lossy data compression to reduce memory footprint and '
                                                                'storage size'},
                                                    {   'id': 'opt3',
                                                        'text': 'Eliminating multicollinearity before training linear '
                                                                'regression or logistic regression models'},
                                                    {   'id': 'opt4',
                                                        'text': 'Generating labeled synthetic targets for unsupervised '
                                                                'datasets'}],
                                     'question': 'Which of the following are common practical applications of '
                                                 'Principal Component Analysis? (Select all that apply)',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': "When 0 < n_components < 1, Scikit-Learn's PCA automatically "
                                                    'selects the minimum number of components such that the cumulative '
                                                    'explained variance meets or exceeds the specified threshold.',
                                     'id': 'q8',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Pass a float between 0 and 1, such as '
                                                                'PCA(n_components=0.95)'},
                                                    {'id': 'opt2', 'text': "Set PCA(n_components='auto_95')"},
                                                    {   'id': 'opt3',
                                                        'text': 'Run a while loop manually fitting 1 to p components'},
                                                    {'id': 'opt4', 'text': 'Set PCA(max_features=0.95)'}],
                                     'question': "In Scikit-Learn's PCA, how can you automatically select the minimum "
                                                 'number of components needed to retain at least 95% of total '
                                                 'variance?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'For a 2x2 correlation matrix [[1, r], [r, 1]], the eigenvalues '
                                                    'are 1 + r and 1 - r. For r = 0.6: lambda_1 = 1 + 0.6 = 1.6, and '
                                                    'lambda_2 = 1 - 0.6 = 0.4.',
                                     'id': 'q9',
                                     'options': [   {'id': 'opt1', 'text': 'lambda_1 = 1.6, lambda_2 = 0.4'},
                                                    {'id': 'opt2', 'text': 'lambda_1 = 1.0, lambda_2 = 1.0'},
                                                    {'id': 'opt3', 'text': 'lambda_1 = 0.6, lambda_2 = 0.4'},
                                                    {'id': 'opt4', 'text': 'lambda_1 = 2.0, lambda_2 = 0.0'}],
                                     'question': 'Suppose two standardized features have a correlation coefficient of '
                                                 'r = 0.6. What are the two eigenvalues lambda_1 and lambda_2 of their '
                                                 '2x2 covariance matrix?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'Total variance is lambda_1 + lambda_2 = 1.6 + 0.4 = 2.0. '
                                                    'Explained variance ratio of PC1 is 1.6 / 2.0 = 0.80 = 80%.',
                                     'id': 'q10',
                                     'options': [   {'id': 'opt1', 'text': '80%'},
                                                    {'id': 'opt2', 'text': '60%'},
                                                    {'id': 'opt3', 'text': '16%'},
                                                    {'id': 'opt4', 'text': '100%'}],
                                     'question': 'In the previous question (lambda_1 = 1.6, lambda_2 = 0.4), what '
                                                 'percentage of total variance is captured by the first principal '
                                                 'component?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'PCA learns the data center and covariance structure from '
                                                    'whichever data it is fitted on. Fitting on the full dataset '
                                                    'allows test set variance and spatial distribution to leak into '
                                                    'the transformation matrix, resulting in overly optimistic test '
                                                    'scores.',
                                     'id': 'q11',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'The principal component directions and means are '
                                                                'computed using information from the test samples, '
                                                                'artificially biasing downstream test evaluation'},
                                                    {'id': 'opt2', 'text': 'PCA deletes test set labels permanently'},
                                                    {   'id': 'opt3',
                                                        'text': 'Scikit-Learn throws an immediate runtime error if PCA '
                                                                'is called before splitting'},
                                                    {   'id': 'opt4',
                                                        'text': 'The test set variance will always collapse to exactly '
                                                                'zero'}],
                                     'question': 'Why does fitting PCA on the entire dataset before performing '
                                                 'train/test splitting constitute dangerous data leakage?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1', 'opt2'],
                                     'difficulty': 'medium',
                                     'explanation': 'transform projects data to k coordinates. inverse_transform '
                                                    'reconstructs approximate original features; because dropped '
                                                    'components carried variance, the reconstruction is lossy '
                                                    '(approximate, not 100% exact unless k = p).',
                                     'id': 'q12',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'transform(X) projects centered p-dimensional data '
                                                                'onto the top k principal components to produce '
                                                                'low-dimensional coordinates'},
                                                    {   'id': 'opt2',
                                                        'text': 'inverse_transform(Z) reconstructs an approximation of '
                                                                'the original p features by multiplying latent '
                                                                'coordinates by components_ and adding back the mean'},
                                                    {   'id': 'opt3',
                                                        'text': 'inverse_transform(Z) always reconstructs the original '
                                                                'dataset with 100% exact mathematical precision '
                                                                'regardless of k'},
                                                    {   'id': 'opt4',
                                                        'text': 'transform(X) drops any rows that contain negative '
                                                                'values'}],
                                     'question': "Which of the following operations are performed by Scikit-Learn's "
                                                 'PCA.transform() and PCA.inverse_transform()? (Select all that apply)',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'Dropping the remaining 45 components means discarding their '
                                                    'variance (8% of the total spread). This is the tradeoff of lossy '
                                                    'compression.',
                                     'id': 'q13',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'It was discarded as information loss along the 45 '
                                                                'unselected orthogonal directions'},
                                                    {   'id': 'opt2',
                                                        'text': 'It was converted into classification target accuracy'},
                                                    {   'id': 'opt3',
                                                        'text': 'It was automatically distributed evenly among the 5 '
                                                                'kept components'},
                                                    {'id': 'opt4', 'text': 'It caused the model bias to drop to zero'}],
                                     'question': 'If you reduce a dataset from p = 50 features down to k = 5 principal '
                                                 'components that collectively explain 92% of total variance, what '
                                                 'happened to the remaining 8% of variance?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'PCA is completely unsupervised: it maximizes data variance in X '
                                                    'regardless of class labels y. (Supervised dimensionality '
                                                    'reduction that maximizes class separation is Linear Discriminant '
                                                    'Analysis, LDA).',
                                     'id': 'q14',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'No, PCA is strictly an unsupervised algorithm that '
                                                                'maximizes feature variance without looking at labels '
                                                                'y'},
                                                    {   'id': 'opt2',
                                                        'text': 'Yes, PCA optimizes the Fisher discriminant ratio '
                                                                'between classes'},
                                                    {   'id': 'opt3',
                                                        'text': 'Yes, PCA ensures that classes with fewer instances '
                                                                'receive larger eigenvalues'},
                                                    {'id': 'opt4', 'text': 'Only if the target is binary (0 or 1)'}],
                                     'question': 'Does Principal Component Analysis take class labels y into account '
                                                 'when finding the principal directions?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'The rank of a centered data matrix of size N x p is at most min(N '
                                                    '- 1, p). For N = 100 and p = 200, the maximum number of non-zero '
                                                    'eigenvalues is min(99, 200) = 99.',
                                     'id': 'q15',
                                     'options': [   {'id': 'opt1', 'text': '99 (min(N - 1, p))'},
                                                    {'id': 'opt2', 'text': '200'},
                                                    {'id': 'opt3', 'text': '100'},
                                                    {'id': 'opt4', 'text': '10'}],
                                     'question': 'What is the maximum possible number of non-zero principal components '
                                                 'that can be extracted from a dataset with N = 100 samples and p = '
                                                 '200 features?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'If Sigma * v = lambda * v, then multiplying by -1 gives Sigma * '
                                                    '(-v) = lambda * (-v). Both v and -v define the same line in '
                                                    'space, so either orientation is equally valid.',
                                     'id': 'q16',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Because both v and -v define the exact same geometric '
                                                                'axis of projection; the sign choice is mathematically '
                                                                'arbitrary'},
                                                    {   'id': 'opt2',
                                                        'text': 'Because Scikit-Learn uses complex numbers while NumPy '
                                                                'uses real numbers'},
                                                    {   'id': 'opt3',
                                                        'text': 'Because NumPy fails to normalize eigenvectors to unit '
                                                                'length'},
                                                    {   'id': 'opt4',
                                                        'text': 'Because sign flipping indicates severe numerical '
                                                                'instability'}],
                                     'question': "Why might a sign flip occur in an eigenvector between NumPy's "
                                                 "np.linalg.eig and Scikit-Learn's PCA.components_?",
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1', 'opt4'],
                                     'difficulty': 'medium',
                                     'explanation': 'StandardScaler must precede PCA so features start with equal unit '
                                                    'variance. The classifier must be the terminal step. Option 1 is '
                                                    'the canonical PCA pipeline, and Option 4 is the valid standard '
                                                    'baseline without PCA.',
                                     'id': 'q17',
                                     'options': [   {   'id': 'opt1',
                                                        'text': "Pipeline([('scaler', StandardScaler()), ('pca', "
                                                                "PCA(n_components=5)), ('clf', "
                                                                'LogisticRegression())])'},
                                                    {   'id': 'opt2',
                                                        'text': "Pipeline([('pca', PCA(n_components=5)), ('scaler', "
                                                                "StandardScaler()), ('clf', LogisticRegression())])"},
                                                    {   'id': 'opt3',
                                                        'text': "Pipeline([('clf', LogisticRegression()), ('pca', "
                                                                'PCA(n_components=5))])'},
                                                    {   'id': 'opt4',
                                                        'text': "Pipeline([('scaler', StandardScaler()), ('clf', "
                                                                'LogisticRegression())]) (if PCA is omitted)'}],
                                     'question': 'When constructing an end-to-end Machine Learning pipeline using '
                                                 "Scikit-Learn's Pipeline class, which order of steps is correct? "
                                                 '(Select all that apply)',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'If all columns represent the same physical quantity on the same '
                                                    'scale (such as pixel brightness across an image), differences in '
                                                    'variance represent true visual contrast rather than arbitrary '
                                                    'unit mismatches.',
                                     'id': 'q18',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'When all features naturally share identical physical '
                                                                'units, scales, and measurement domains (e.g., image '
                                                                'pixel intensities from 0 to 255)'},
                                                    {   'id': 'opt2',
                                                        'text': 'When features have severe multicollinearity'},
                                                    {'id': 'opt3', 'text': 'When the dataset has fewer than 100 rows'},
                                                    {   'id': 'opt4',
                                                        'text': 'When using a Random Forest classifier downstream'}],
                                     'question': 'Under what condition is feature scaling UNNECESSARY prior to running '
                                                 'PCA?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'hard',
                                     'explanation': 'PCA maximizes total variance in X without knowing y. It is '
                                                    'possible that the variation distinguishing class 0 from class 1 '
                                                    'lies along a low-variance direction (e.g. PC3 or PC4) rather than '
                                                    'PC1.',
                                     'id': 'q19',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Because the directions of greatest overall data '
                                                                'variance might not align with the directions that '
                                                                'separate the target classes'},
                                                    {   'id': 'opt2',
                                                        'text': 'Because PCA deletes the intercept term beta_0'},
                                                    {'id': 'opt3', 'text': 'Because eigenvalues cannot exceed 1.0'},
                                                    {   'id': 'opt4',
                                                        'text': 'Because variance is mathematically inversely '
                                                                'proportional to information'}],
                                     'question': 'Why is high explained variance NOT a guarantee of high '
                                                 'classification accuracy for a downstream model?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'hard',
                                     'explanation': 'PCA only rotates straight axes and projects orthogonally. '
                                                    'Non-linear manifolds (like a spiral or Swiss roll) get smashed '
                                                    'and overlapping in linear PCA; non-linear methods like Kernel PCA '
                                                    'or t-SNE/UMAP are required.',
                                     'id': 'q20',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Standard PCA is strictly a linear projection '
                                                                'technique and cannot unroll curved non-linear '
                                                                'manifolds'},
                                                    {   'id': 'opt2',
                                                        'text': 'Standard PCA requires all features to be perfectly '
                                                                'independent'},
                                                    {   'id': 'opt3',
                                                        'text': 'Standard PCA cannot compute eigenvalues if the number '
                                                                'of features p > 2'},
                                                    {   'id': 'opt4',
                                                        'text': 'Standard PCA converts continuous curves into step '
                                                                'functions'}],
                                     'question': 'What is a major limitation of standard Principal Component Analysis '
                                                 "when applied to non-linear data structures (such as a 'Swiss Roll' "
                                                 'or concentric circles)?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'hard',
                                     'explanation': 'pca.components_ has shape (n_components, n_features). Each row is '
                                                    'an eigenvector (principal axis in feature space) describing the '
                                                    'linear combination of original features.',
                                     'id': 'q21',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Shape (n_components, n_features), where each row is '
                                                                'an eigenvector representing the weights/loadings of '
                                                                'original features for that component'},
                                                    {   'id': 'opt2',
                                                        'text': 'Shape (n_samples, n_components), containing the '
                                                                'projected coordinates of each data point'},
                                                    {   'id': 'opt3',
                                                        'text': 'Shape (n_components,), containing the eigenvalues'},
                                                    {   'id': 'opt4',
                                                        'text': 'Shape (n_features, n_features), representing the '
                                                                'inverted correlation matrix'}],
                                     'question': "In Scikit-Learn, how is the attribute 'pca.components_' shaped and "
                                                 'structured?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1', 'opt2', 'opt3'],
                                     'difficulty': 'hard',
                                     'explanation': 'Dropping 90 components can discard vital predictive variance, '
                                                    'variance does not guarantee class separation, and forgetting to '
                                                    'scale causes arbitrary feature dominance. Logistic regression is '
                                                    'fully compatible with PCA components.',
                                     'id': 'q22',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Keeping only 10 components discarded too much '
                                                                'predictive signal that resided in the remaining 90 '
                                                                'components'},
                                                    {   'id': 'opt2',
                                                        'text': 'The 10 components with highest variance were '
                                                                'dominated by background noise rather than '
                                                                'class-separating features'},
                                                    {   'id': 'opt3',
                                                        'text': 'The team forgot to include StandardScaler before PCA, '
                                                                'causing 1 or 2 high-magnitude features to monopolize '
                                                                'the components'},
                                                    {   'id': 'opt4',
                                                        'text': 'Logistic regression is mathematically incompatible '
                                                                'with principal components'}],
                                     'question': 'A data science team trains a LogisticRegression model on 100 raw '
                                                 'features and gets 85% test accuracy. They then insert '
                                                 'PCA(n_components=10) and test accuracy drops to 72%. Which of the '
                                                 'following are plausible explanations? (Select all that apply)',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'hard',
                                     'explanation': 'If features are uncorrelated, the covariance matrix of '
                                                    'standardized data is the Identity matrix I_10. The eigenvalues of '
                                                    'the identity matrix are all 1.0. Dimensionality reduction offers '
                                                    'zero compression benefit here because there is zero redundancy to '
                                                    'exploit.',
                                     'id': 'q23',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'All 10 eigenvalues will be exactly equal to 1.0; each '
                                                                'component will explain exactly 10% of the variance'},
                                                    {   'id': 'opt2',
                                                        'text': 'PC1 will explain 100% of the variance and the '
                                                                'remaining 9 will be 0'},
                                                    {'id': 'opt3', 'text': 'All eigenvalues will be exactly 0'},
                                                    {   'id': 'opt4',
                                                        'text': 'The eigenvalues will decrease exponentially'}],
                                     'question': 'Suppose a dataset has p = 10 features, and all 10 features are '
                                                 'completely uncorrelated with each other (pairwise correlations are '
                                                 'all 0). If you standardize the data and run PCA, what will the '
                                                 'eigenvalues be?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'hard',
                                     'explanation': 'Reconstruction requires calculating Z * V_k^T + mean. Thus, you '
                                                    'must store the low-dimensional codes Z, the k principal component '
                                                    'vectors V_k, and the empirical mean vector.',
                                     'id': 'q24',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'The projected coordinates Z (N x k), the principal '
                                                                'components matrix (k x p), and the mean vector (p,)'},
                                                    {'id': 'opt2', 'text': 'Only the projected coordinates Z (N x k)'},
                                                    {   'id': 'opt3',
                                                        'text': 'The original dataset X plus the eigenvalues'},
                                                    {'id': 'opt4', 'text': 'The full N x N distance matrix'}],
                                     'question': 'When compressing an image dataset with PCA, what data must be stored '
                                                 'to allow subsequent reconstruction with inverse_transform?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'hard',
                                     'explanation': 'In fact, Scikit-Learn implements PCA via SVD on centered data '
                                                    'because it is numerically more stable than explicitly forming the '
                                                    'covariance matrix X^T * X. The right singular vectors V are the '
                                                    'principal component directions, and lambda_i = s_i^2 / (N - 1).',
                                     'id': 'q25',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'The right singular vectors V from SVD(X) = U * S * '
                                                                'V^T are identical to the eigenvectors of the '
                                                                'covariance matrix X^T * X, and singular values s_i '
                                                                'are related by lambda_i = s_i^2 / (N - 1)'},
                                                    {   'id': 'opt2',
                                                        'text': 'SVD is only used for square matrices while PCA is '
                                                                'used for rectangular matrices'},
                                                    {   'id': 'opt3',
                                                        'text': 'SVD computes eigenvalues without using vectors'},
                                                    {   'id': 'opt4',
                                                        'text': 'SVD and PCA are completely unrelated mathematical '
                                                                'concepts'}],
                                     'question': 'How does PCA relate to Singular Value Decomposition (SVD) of a '
                                                 'centered data matrix X of size N x p?',
                                     'type': 'single_choice'}],
                'quiz_id': 'quiz-cml-t5-l15',
                'title': 'Topic Quiz: Principal Component Analysis (PCA)'},
    'schema_version': 1,
    'sections': [   {   'body': '### 1.1 The Hook: 13 Numbers or 2?\n'
                                '\n'
                                'Consider the classic **Wine benchmark dataset**:\n'
                                '- Chemical analysis of 178 bottles of wine across 3 grape cultivars (classes).\n'
                                '- Each bottle is described by **13 continuous measurements**: `alcohol`, '
                                '`malic_acid`, `ash`, `alcalinity`, `magnesium`, `phenols`, `flavanoids`, '
                                '`nonflavanoids`, `proanthocyanins`, `color_intensity`, `hue`, `od280`, and '
                                '`proline`.\n'
                                '- Human cognition cannot visualize 13-dimensional hyperspace. We can only look at 2D '
                                'or 3D scatter plots.\n'
                                '- Could we somehow compress these 13 chemical features into **just 2 summary axes**, '
                                'while preserving enough geometric information to clearly separate the three grape '
                                'varieties?\n'
                                '\n'
                                '**Principal Component Analysis (PCA)**, invented by Karl Pearson in 1901 and '
                                'independently developed by Harold Hotelling in 1933, is the premier unsupervised '
                                'technique for **Dimensionality Reduction**:\n'
                                'It projects high-dimensional data onto a smaller number of orthogonal axes that '
                                'maximize data spread (variance).\n'
                                '\n'
                                '```\n'
                                'Dimensionality Reduction Workflow:\n'
                                '   Raw Feature Space (d = 13 dimensions) ──► [ PCA Rotation & Projection ] ──► '
                                'Compressed Space (k = 2 Principal Components)\n'
                                '   - High storage footprint                  - Finds orthogonal axes of         - '
                                'Visualizable on a 2D scatter plot!\n'
                                '   - High multicollinearity                    maximum spread (variance)        - '
                                'Zero correlation between PC1 and PC2!\n'
                                '   - Prone to Curse of Dimensionality                                           - '
                                'Preserves ~55% of total variance!\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.2 The Four Core Motivations for Dimensionality Reduction\n'
                                '\n'
                                '1. **High-Dimensional Data Visualization**:\n'
                                '   Compressing complex feature spaces ($d = 50, 100, 1000$) down to $k = 2$ or $3$ '
                                'components enables human visual inspection of cluster clusters, class separations, '
                                'and anomaly outliers.\n'
                                '2. **Computational Speedup & Storage Compression**:\n'
                                '   Training complex non-linear models on 1,000 features is orders of magnitude slower '
                                'than training on 25 principal components that capture $95\\%$ of the information.\n'
                                '3. **Elimination of Multicollinearity**:\n'
                                '   By mathematical construction, all principal components are **strictly orthogonal '
                                '(mutually perpendicular)**. Their pairwise correlation is identically zero '
                                '($\\text{Corr}(\\text{PC}_i, \\text{PC}_j) = 0$). Feeding uncorrelated components '
                                'into linear models eliminates matrix inversion instabilities!\n'
                                '4. **Noise Filtering**:\n'
                                '   Real-world signals tend to dominate the principal directions of largest variance, '
                                'while random, high-frequency measurement noise lives in the trailing components with '
                                'tiny eigenvalues. Truncating trailing components acts as a natural low-pass filter!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.3 Variance as the Currency of Information\n'
                                '\n'
                                'Why does PCA prioritize variance?\n'
                                '- Consider a feature where every single observation has the exact same value: $x_{i} '
                                '= 5.0$ for all $i$. Its variance is $\\sigma^2 = 0$.\n'
                                '  This feature provides **zero distinguishing power**. It tells you nothing about how '
                                'samples differ.\n'
                                '- Now consider a feature where values are widely dispersed across positive and '
                                'negative values. Its high variance reflects diversity, structure, and distinguishing '
                                'patterns.\n'
                                '- In PCA, **Variance = Information**. The direction along which data points are most '
                                'spread out preserves the maximum amount of original geometric distance!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.4 The Catastrophic "Forgot-to-Scale" Trap: The Proline Pathology\n'
                                '\n'
                                'Because PCA actively seeks directions of maximum numerical variance, it is '
                                '**exceptionally vulnerable to arbitrary physical units of measurement**:\n'
                                '\n'
                                'Let us examine the raw variances of features in the unstandardized Wine dataset:\n'
                                '- `proline` is measured in milligrams per liter ($278$ to $1{,}680\\text{ mg/L}$), '
                                'giving an immense sample variance of:\n'
                                '  $$\\text{Var}(\\text{proline}) \\approx \\mathbf{99,166.7}$$\n'
                                '- `flavanoids` is measured in grams per liter ($0.34$ to $5.08 \\text{ g/L}$), giving '
                                'a tiny sample variance of:\n'
                                '  $$\\text{Var}(\\text{flavanoids}) \\approx \\mathbf{0.99}$$\n'
                                '- `nonflavanoids` has a variance of:\n'
                                '  $$\\text{Var}(\\text{nonflavanoids}) \\approx \\mathbf{0.015}$$\n'
                                '\n'
                                '#### The Disastrous Illusion of Unscaled PCA:\n'
                                'When PCA is fitted directly on the raw, unscaled Wine dataset:\n'
                                '- **PC1 claims to explain 99.80% of total variance**!\n'
                                '- A naive engineer might celebrate: *"PC1 captures 99.8% of the entire dataset!"*\n'
                                '- But inspect the eigenvector weights (loadings) of PC1:\n'
                                '  $$\\mathbf{v}_1 = [0.001, -0.002, 0.000, -0.005, 0.018, 0.001, 0.002, -0.000, '
                                '0.002, 0.005, 0.000, 0.001, \\mathbf{0.9998}]$$\n'
                                '- PC1 has an loading of **$0.9998$ on Proline** and near-zero on all other 12 '
                                'features!\n'
                                '- The algorithm did not discover a profound chemical pattern; it was simply blinded '
                                'by the fact that Proline was recorded in big numbers.\n'
                                '\n'
                                '```\n'
                                'Unscaled vs. Standardized PCA on Wine Dataset:\n'
                                '┌─────────────────────┬────────────────────────────────────┬────────────────────────────────────┐\n'
                                '│ Metric              │ Raw Unscaled PCA                   │ Standardized PCA '
                                '(StandardScaler)  │\n'
                                '├─────────────────────┼────────────────────────────────────┼────────────────────────────────────┤\n'
                                '│ PC1 Variance Share  │ **99.80%** (Fake discovery!)       │ **36.20%** (Real '
                                'multivariate signal│\n'
                                '│ PC2 Variance Share  │ **0.18%**                          │ '
                                '**19.20%**                         │\n'
                                '│ Cumulative (PC1+PC2)│ **99.98%**                         │ '
                                '**55.40%**                         │\n'
                                '│ PC1 Loading Focus   │ 100% Proline; 0% other 12 features │ Balanced chemical '
                                'contribution     │\n'
                                '│ Cultivar Separation │ Poor (overlaps classes)            │ **Distinct, clear '
                                '3-class clusters│\n'
                                '└─────────────────────┴────────────────────────────────────┴────────────────────────────────────┘\n'
                                '```\n'
                                '\n'
                                '> **The Non-Negotiable Rule of PCA**:\n'
                                '> **Always standardize features (`StandardScaler`: $\\mu = 0, \\sigma = 1$) before '
                                'running PCA**, unless all features are already measured in the exact same physical '
                                'units (such as raw image pixel intensities $\\in [0, 255]$).',
                        'citations': [   'Pearson, K. (1901). On lines and planes of closest fit to systems of points '
                                         'in space. Philosophical Magazine, 2(11), 559-572.',
                                         'Hotelling, H. (1933). Analysis of a complex of statistical variables into '
                                         'principal components. Journal of Educational Psychology, 24(6), 417-441.'],
                        'heading': '1. Why Reduce Dimensions? Variance as Information',
                        'section_id': 'cml-l15-sec01'},
                    {   'body': '### 2.1 The Mathematical Derivation of PCA via Variance Maximization\n'
                                '\n'
                                'Let $\\mathbf{X} \\in \\mathbb{R}^{n \\times d}$ be a dataset of $n$ observations '
                                'across $d$ features.\n'
                                'Assume without loss of generality that the data has been **mean-centered** so that '
                                'the empirical column means are zero:\n'
                                '$$\\frac{1}{n}\\sum_{i=1}^n \\mathbf{x}_i = \\mathbf{0}$$\n'
                                '\n'
                                'The empirical **Covariance Matrix** $\\mathbf{\\Sigma} \\in \\mathbb{R}^{d \\times '
                                'd}$ is given by:\n'
                                '$$\\mathbf{\\Sigma} = \\frac{1}{n - 1} \\mathbf{X}^T \\mathbf{X}$$\n'
                                '\n'
                                'We wish to project each $d$-dimensional observation $\\mathbf{x}_i$ onto a '
                                '1-dimensional line defined by a unit direction vector $\\mathbf{w} \\in '
                                '\\mathbb{R}^d$, where:\n'
                                '$$\\|\\mathbf{w}\\|_2^2 = \\mathbf{w}^T \\mathbf{w} = 1$$\n'
                                '\n'
                                'The scalar projection (coordinate) of observation $\\mathbf{x}_i$ along direction '
                                '$\\mathbf{w}$ is:\n'
                                '$$z_i = \\mathbf{w}^T \\mathbf{x}_i$$\n'
                                '\n'
                                '#### Calculating the Variance of the Projections:\n'
                                'Because the data is mean-centered, the mean of the projected coordinates is also '
                                'zero:\n'
                                '$$\\bar{z} = \\frac{1}{n}\\sum_{i=1}^n \\mathbf{w}^T \\mathbf{x}_i = \\mathbf{w}^T '
                                '\\left(\\frac{1}{n}\\sum_{i=1}^n \\mathbf{x}_i\\right) = 0$$\n'
                                '\n'
                                'The empirical sample variance of the projected coordinates is:\n'
                                '$$\\text{Var}(z) = \\frac{1}{n - 1} \\sum_{i=1}^n (z_i - 0)^2 = \\frac{1}{n - 1} '
                                '\\sum_{i=1}^n (\\mathbf{w}^T \\mathbf{x}_i)^2 = \\frac{1}{n - 1} \\sum_{i=1}^n '
                                '\\mathbf{w}^T \\mathbf{x}_i \\mathbf{x}_i^T \\mathbf{w}$$\n'
                                '$$\\text{Var}(z) = \\mathbf{w}^T \\left( \\frac{1}{n - 1} \\mathbf{X}^T \\mathbf{X} '
                                '\\right) \\mathbf{w} = \\mathbf{w}^T \\mathbf{\\Sigma} \\mathbf{w}$$\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.2 Constrained Optimization via Lagrange Multipliers\n'
                                '\n'
                                'To find the direction $\\mathbf{w}$ that maximizes projected variance subject to the '
                                'unit-norm constraint $\\mathbf{w}^T \\mathbf{w} = 1$, we formulate the '
                                '**Lagrangian**:\n'
                                '\n'
                                '$$\\mathcal{L}(\\mathbf{w}, \\lambda) = \\mathbf{w}^T \\mathbf{\\Sigma} \\mathbf{w} - '
                                '\\lambda (\\mathbf{w}^T \\mathbf{w} - 1)$$\n'
                                '\n'
                                'Taking the gradient with respect to $\\mathbf{w}$:\n'
                                '$$\\nabla_{\\mathbf{w}} \\mathcal{L} = 2\\mathbf{\\Sigma} \\mathbf{w} - 2\\lambda '
                                '\\mathbf{w} = \\mathbf{0}$$\n'
                                '$$\\mathbf{\\Sigma} \\mathbf{w} = \\lambda \\mathbf{w}$$\n'
                                '\n'
                                '> **The Mathematical Revelation**:\n'
                                '> The condition $\\mathbf{\\Sigma} \\mathbf{w} = \\lambda \\mathbf{w}$ is the '
                                'fundamental **Eigenvalue Equation** of linear algebra!\n'
                                '> - The optimal projection directions $\\mathbf{w}$ are the **Eigenvectors** of the '
                                'covariance matrix $\\mathbf{\\Sigma}$.\n'
                                '> - The scalar $\\lambda$ is the corresponding **Eigenvalue**.\n'
                                '\n'
                                '#### What Does the Eigenvalue $\\lambda$ Represent?\n'
                                'Multiply both sides of the eigenvalue equation on the left by $\\mathbf{w}^T$:\n'
                                '$$\\mathbf{w}^T \\mathbf{\\Sigma} \\mathbf{w} = \\mathbf{w}^T (\\lambda \\mathbf{w}) '
                                '= \\lambda (\\mathbf{w}^T \\mathbf{w}) = \\lambda (1) = \\lambda$$\n'
                                '\n'
                                'Since $\\text{Var}(z) = \\mathbf{w}^T \\mathbf{\\Sigma} \\mathbf{w}$, we obtain:\n'
                                '$$\\text{Var}(z) = \\lambda$$\n'
                                '\n'
                                '> **Profound Geometric Insight**:\n'
                                '> - Each eigenvalue $\\lambda_j$ is **literally the exact variance** of the data '
                                'along principal component axis $\\mathbf{v}_j$!\n'
                                '> - To maximize variance, we simply pick the eigenvector $\\mathbf{v}_1$ '
                                'corresponding to the **largest eigenvalue** $\\lambda_1$. This is **PC1**!\n'
                                '> - The second principal component **PC2** is the eigenvector $\\mathbf{v}_2$ '
                                'corresponding to the second largest eigenvalue $\\lambda_2$, and is mathematically '
                                'guaranteed to be orthogonal to PC1 ($\\mathbf{v}_1^T \\mathbf{v}_2 = 0$).\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.3 Concrete Hand-Calculated Walkthrough: 2D Correlated System ($r = 0.8$)\n'
                                '\n'
                                'Let us solve the exact 2D system taught on the whiteboard:\n'
                                'Suppose standardized variables $x_1$ and $x_2$ have unit variance ($\\text{Var}(x_1) '
                                '= 1, \\text{Var}(x_2) = 1$) and correlation $r = 0.80$.\n'
                                'The covariance matrix is:\n'
                                '\n'
                                '$$\\mathbf{\\Sigma} = \\begin{pmatrix} 1.0 & 0.8 \\\\ 0.8 & 1.0 \\end{pmatrix}$$\n'
                                '\n'
                                '#### Step 1: Solve the Characteristic Equation $\\det(\\mathbf{\\Sigma} - \\lambda '
                                '\\mathbf{I}) = 0$\n'
                                '$$\\det \\begin{pmatrix} 1 - \\lambda & 0.8 \\\\ 0.8 & 1 - \\lambda \\end{pmatrix} = '
                                '(1 - \\lambda)(1 - \\lambda) - (0.8)(0.8) = 0$$\n'
                                '$$(1 - \\lambda)^2 - 0.64 = 0$$\n'
                                '$$(1 - \\lambda)^2 = 0.64 \\implies 1 - \\lambda = \\pm 0.80$$\n'
                                '\n'
                                'Solving for the two roots:\n'
                                '$$\\lambda_1 = 1 + 0.80 = \\mathbf{1.80}$$\n'
                                '$$\\lambda_2 = 1 - 0.80 = \\mathbf{0.20}$$\n'
                                '\n'
                                '#### Total Variance Check:\n'
                                '$$\\text{Total Variance} = \\text{Tr}(\\mathbf{\\Sigma}) = 1.0 + 1.0 = 2.00$$\n'
                                '$$\\lambda_1 + \\lambda_2 = 1.80 + 0.20 = \\mathbf{2.00} \\quad (\\text{Preserved '
                                'perfectly!})$$\n'
                                '\n'
                                '#### Explained Variance Ratios:\n'
                                '- **PC1**: $\\frac{\\lambda_1}{\\lambda_1 + \\lambda_2} = \\frac{1.80}{2.00} = '
                                '\\mathbf{90.0\\%}$\n'
                                '- **PC2**: $\\frac{\\lambda_2}{\\lambda_1 + \\lambda_2} = \\frac{0.20}{2.00} = '
                                '\\mathbf{10.0\\%}$\n'
                                '*(A single principal component PC1 captures 90% of all information in this 2D '
                                'system!)*\n'
                                '\n'
                                '---\n'
                                '\n'
                                '#### Step 2: Calculate Eigenvector for $\\lambda_1 = 1.80$ (PC1 Direction)\n'
                                'Substitute $\\lambda_1 = 1.80$ into $(\\mathbf{\\Sigma} - \\lambda_1 '
                                '\\mathbf{I})\\mathbf{v}_1 = \\mathbf{0}$:\n'
                                '$$\\begin{pmatrix} 1.0 - 1.8 & 0.8 \\\\ 0.8 & 1.0 - 1.8 \\end{pmatrix} '
                                '\\begin{pmatrix} v_{11} \\\\ v_{12} \\end{pmatrix} = \\begin{pmatrix} -0.8 & 0.8 \\\\ '
                                '0.8 & -0.8 \\end{pmatrix} \\begin{pmatrix} v_{11} \\\\ v_{12} \\end{pmatrix} = '
                                '\\begin{pmatrix} 0 \\\\ 0 \\end{pmatrix}$$\n'
                                '\n'
                                '$$-0.8 v_{11} + 0.8 v_{12} = 0 \\implies v_{11} = v_{12}$$\n'
                                '\n'
                                'Normalize to unit length ($v_{11}^2 + v_{12}^2 = 1 \\implies 2v_{11}^2 = 1 \\implies '
                                'v_{11} = \\frac{1}{\\sqrt{2}}$):\n'
                                '$$\\mathbf{v}_1 = \\begin{pmatrix} 1/\\sqrt{2} \\\\ 1/\\sqrt{2} \\end{pmatrix} '
                                '\\approx \\begin{pmatrix} \\mathbf{0.7071} \\\\ \\mathbf{0.7071} \\end{pmatrix}$$\n'
                                '*(This points precisely along the $45^\\circ$ diagonal line $x_2 = x_1$, the '
                                'direction of maximal spread!)*\n'
                                '\n'
                                '---\n'
                                '\n'
                                '#### Step 3: Calculate Eigenvector for $\\lambda_2 = 0.20$ (PC2 Direction)\n'
                                'Substitute $\\lambda_2 = 0.20$ into $(\\mathbf{\\Sigma} - \\lambda_2 '
                                '\\mathbf{I})\\mathbf{v}_2 = \\mathbf{0}$:\n'
                                '$$\\begin{pmatrix} 1.0 - 0.2 & 0.8 \\\\ 0.8 & 1.0 - 0.2 \\end{pmatrix} '
                                '\\begin{pmatrix} v_{21} \\\\ v_{22} \\end{pmatrix} = \\begin{pmatrix} 0.8 & 0.8 \\\\ '
                                '0.8 & 0.8 \\end{pmatrix} \\begin{pmatrix} v_{21} \\\\ v_{22} \\end{pmatrix} = '
                                '\\begin{pmatrix} 0 \\\\ 0 \\end{pmatrix}$$\n'
                                '\n'
                                '$$0.8 v_{21} + 0.8 v_{22} = 0 \\implies v_{21} = -v_{22}$$\n'
                                '\n'
                                'Normalized unit vector:\n'
                                '$$\\mathbf{v}_2 = \\begin{pmatrix} -1/\\sqrt{2} \\\\ 1/\\sqrt{2} \\end{pmatrix} '
                                '\\approx \\begin{pmatrix} \\mathbf{-0.7071} \\\\ \\mathbf{0.7071} \\end{pmatrix}$$\n'
                                '*(This points along the $135^\\circ$ line, strictly orthogonal to PC1: '
                                '$\\mathbf{v}_1^T \\mathbf{v}_2 = (0.7071)(-0.7071) + (0.7071)(0.7071) = 0$!)*\n'
                                '\n'
                                '```\n'
                                'Geometric Visualization of Principal Axes:\n'
                                '       x2 ^\n'
                                '          │           PC1 Direction (λ1 = 1.80, 90% Variance, 45°)\n'
                                '          │             /\n'
                                "          │           .'\n"
                                "          │         .'  *\n"
                                "          │       .' * *\n"
                                "          │     .' * * *\n"
                                "    ──────┼───.'──────────────► x1\n"
                                "          │ .' * *\n"
                                "          │' *\n"
                                '       PC2 Direction (λ2 = 0.20, 10% Variance, 135° Orthogonal)\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.4 The Duality Theorem: Variance Maximization is Equivalent to Reconstruction '
                                'Error Minimization\n'
                                '\n'
                                'There are two completely distinct ways to derive PCA, and remarkably, both lead to '
                                'the exact same mathematical solution:\n'
                                '\n'
                                '#### Formulation 1: Maximum Variance Perspective (Hotelling 1933)\n'
                                'Find an orthogonal coordinate system that maximizes the variance of projected '
                                'coordinates:\n'
                                '$$\\max_{\\mathbf{W}} \\text{Tr}(\\mathbf{W}^T \\mathbf{\\Sigma} \\mathbf{W}) \\quad '
                                '\\text{s.t. } \\mathbf{W}^T \\mathbf{W} = \\mathbf{I}_k$$\n'
                                '\n'
                                '#### Formulation 2: Minimum Reconstruction Error Perspective (Pearson 1901)\n'
                                'Approximate each $d$-dimensional observation $\\mathbf{x}_i$ using a $k$-dimensional '
                                'linear subspace ($k < d$):\n'
                                '$$\\hat{\\mathbf{x}}_i = \\sum_{j=1}^k z_{ij} \\mathbf{v}_j = \\mathbf{V}_k '
                                '\\mathbf{z}_i$$\n'
                                'Find the orthogonal basis $\\mathbf{V}_k$ that minimizes the **Mean Squared '
                                'Reconstruction Error**:\n'
                                '$$\\text{MSRE} = \\frac{1}{n} \\sum_{i=1}^n \\|\\mathbf{x}_i - '
                                '\\hat{\\mathbf{x}}_i\\|_2^2$$\n'
                                '\n'
                                '#### The Fundamental Spectral Duality Proof:\n'
                                'By the Pythagorean theorem in Euclidean space, the squared length of vector '
                                '$\\mathbf{x}_i$ decomposes into preserved and discarded components:\n'
                                '$$\\|\\mathbf{x}_i\\|^2 = \\|\\hat{\\mathbf{x}}_i\\|^2 + \\|\\mathbf{x}_i - '
                                '\\hat{\\mathbf{x}}_i\\|^2$$\n'
                                'Averaging over all $n$ observations:\n'
                                '$$\\frac{1}{n}\\sum_{i=1}^n \\|\\mathbf{x}_i\\|^2 = \\frac{1}{n}\\sum_{i=1}^n '
                                '\\|\\hat{\\mathbf{x}}_i\\|^2 + \\frac{1}{n}\\sum_{i=1}^n \\|\\mathbf{x}_i - '
                                '\\hat{\\mathbf{x}}_i\\|^2$$\n'
                                '$$\\text{Total Variance} = \\text{Preserved Projected Variance} + '
                                '\\text{Reconstruction Error}$$\n'
                                '\n'
                                'Because Total Variance $\\sum_{j=1}^d \\lambda_j$ is a fixed constant determined '
                                'solely by the dataset:\n'
                                '$$\\text{Reconstruction Error} = \\text{Total Variance} - \\text{Preserved Variance} '
                                '= \\sum_{j=1}^d \\lambda_j - \\sum_{j=1}^k \\lambda_j = \\mathbf{\\sum_{j=k+1}^d '
                                '\\lambda_j}$$\n'
                                '\n'
                                '> **The Landmark Equivalence**:\n'
                                '> **Maximizing preserved variance is mathematically identical to minimizing '
                                'reconstruction error!**\n'
                                '> The reconstruction error of a $k$-component PCA projection is **identically equal '
                                'to the sum of the discarded eigenvalues**:\n'
                                '> $$\\text{MSRE} = \\lambda_{k+1} + \\lambda_{k+2} + \\dots + \\lambda_d$$',
                        'citations': [   'Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of '
                                         'Statistical Learning (2nd ed.). Springer, Chapter 14.5.'],
                        'heading': '2. Step 0: Standardize First! (The Units Disaster)',
                        'section_id': 'cml-l15-sec02'},
                    {   'body': '### 3.1 Choosing the Number of Components $k$: The Scree Plot & Cumulative Variance\n'
                                '\n'
                                'When reducing dimensionality from $d = 50$ down to $k$, how do we select the optimal '
                                '$k$?\n'
                                '\n'
                                '```\n'
                                'Scree Plot & Cumulative Explained Variance Curve:\n'
                                '    Individual Variance Ratio (%)            Cumulative Variance (%)\n'
                                '      40% ^ [PC1: 36%]                        100% ^                           .- - - '
                                '(95% Threshold)\n'
                                "          │                                        │                     . - '\n"
                                "      20% │     [PC2: 19%]                     80% │               . - '\n"
                                "          │          [PC3: 11%]                    │         . - '\n"
                                "      10% │               [PC4: 7%]            60% │   . - ' (PC1+PC2: 55%)\n"
                                "          │    . . . . . . . .                 40% │ .'\n"
                                '        0 ┴───┴────┴────┴────┴────► Component    0 ┴─────────────────────────► '
                                'Components\n'
                                '             PC1  PC2  PC3  PC4                   k=1   k=2   k=3   k=4   k=13\n'
                                '```\n'
                                '\n'
                                '#### The Three Core Decision Heuristics:\n'
                                '1. **Cumulative Variance Threshold (The 90% or 95% Rule)**:\n'
                                '   Retain the smallest number of components $k$ such that their cumulative explained '
                                'variance ratio reaches a pre-determined engineering threshold:\n'
                                '   $$\\sum_{j=1}^{k} \\frac{\\lambda_j}{\\sum_{i=1}^d \\lambda_i} \\ge 0.90 \\quad '
                                '(\\text{or } 0.95)$$\n'
                                '   In Scikit-Learn, this can be automated directly by passing a float to '
                                '`n_components`: `PCA(n_components=0.95)`.\n'
                                "2. **Cattell's Scree Test (Elbow Heuristic)**:\n"
                                '   Plot the individual eigenvalues $\\lambda_j$ against component rank $j$. Look for '
                                'the "elbow" where the steep drop (the cliff) flattens out into loose scree (the '
                                'rubble slope at the base of the mountain). Retain all components before the elbow.\n'
                                '3. **The Kaiser-Guttman Criterion**:\n'
                                '   On standardized data (where each original feature had variance $1.0$), only retain '
                                'principal components whose eigenvalue exceeds the average variance of a single '
                                'feature:\n'
                                '   $$\\lambda_j \\ge 1.0$$\n'
                                '   *(Any component with $\\lambda < 1.0$ contains less information than a single raw '
                                'feature!)*\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.2 Computational Engine: Singular Value Decomposition (SVD)\n'
                                '\n'
                                'In modern libraries (including Scikit-Learn), PCA is **almost never computed by '
                                'explicitly forming the $d \\times d$ covariance matrix $\\mathbf{\\Sigma} = '
                                '\\frac{1}{n-1}\\mathbf{X}^T \\mathbf{X}$**:\n'
                                '- Forming $\\mathbf{X}^T \\mathbf{X}$ costs $O(n d^2)$ operations and squares '
                                'numerical rounding errors.\n'
                                '- If $d = 10{,}000$ features, storing $\\mathbf{\\Sigma}$ in RAM requires $10{,}000 '
                                '\\times 10{,}000 \\times 8 \\text{ bytes} \\approx 800 \\text{ MB}$.\n'
                                '\n'
                                'Instead, Scikit-Learn uses **Singular Value Decomposition (SVD)** directly on the '
                                'mean-centered data matrix $\\mathbf{X}$:\n'
                                '\n'
                                '$$\\mathbf{X} = \\mathbf{U} \\mathbf{S} \\mathbf{V}^T$$\n'
                                '\n'
                                'Where:\n'
                                '- $\\mathbf{U} \\in \\mathbb{R}^{n \\times n}$ is an orthogonal matrix of left '
                                'singular vectors.\n'
                                '- $\\mathbf{S} \\in \\mathbb{R}^{n \\times d}$ is a diagonal matrix of singular '
                                'values $s_1 \\ge s_2 \\ge \\dots \\ge s_d \\ge 0$.\n'
                                '- $\\mathbf{V} \\in \\mathbb{R}^{d \\times d}$ is an orthogonal matrix of right '
                                'singular vectors.\n'
                                '\n'
                                '#### The Beautiful Mathematical Equivalence:\n'
                                '$$\\mathbf{X}^T \\mathbf{X} = (\\mathbf{U} \\mathbf{S} \\mathbf{V}^T)^T (\\mathbf{U} '
                                '\\mathbf{S} \\mathbf{V}^T) = \\mathbf{V} \\mathbf{S}^T (\\mathbf{U}^T \\mathbf{U}) '
                                '\\mathbf{S} \\mathbf{V}^T = \\mathbf{V} \\mathbf{S}^2 \\mathbf{V}^T$$\n'
                                '- The right singular vectors $\\mathbf{V}$ are **identically the eigenvectors of the '
                                'covariance matrix**!\n'
                                '- The singular values $s_j$ relate directly to the eigenvalues:\n'
                                '  $$\\lambda_j = \\frac{s_j^2}{n - 1}$$\n'
                                '- Computing SVD is numerically stable, avoids matrix inversion, and runs in '
                                '$O(\\min(n d^2, n^2 d))$ time.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.3 Dimensionality Reduction Taxonomy: PCA vs. LDA vs. t-SNE vs. UMAP\n'
                                '\n'
                                'Choosing the right dimensionality reduction technique depends on whether you have '
                                'labels and whether your data manifold is linear or curved:\n'
                                '\n'
                                '```\n'
                                'Dimensionality Reduction Comparison:\n'
                                '┌─────────────────────┬──────────────────┬──────────────────┬──────────────────┬────────────────────────────────────┐\n'
                                '│ Algorithm           │ Learning Paradigm│ Manifold Geometry│ Primary Objective│ '
                                'Optimal Use Case                   │\n'
                                '├─────────────────────┼──────────────────┼──────────────────┼──────────────────┼────────────────────────────────────┤\n'
                                '│ **PCA**             │ **Unsupervised** │ **Linear**       │ Maximize spread /│ '
                                'Compression, noise removal, model  │\n'
                                '│                     │ (No labels)      │ (Flat planes)    │ minimize error   │ '
                                'speedup, multicollinearity fix.    │\n'
                                '├─────────────────────┼──────────────────┼──────────────────┼──────────────────┼────────────────────────────────────┤\n'
                                '│ **LDA (Linear       │ **Supervised**   │ **Linear**       │ Maximize between-│ '
                                'Supervised classification when     │\n'
                                '│ Discriminant Anal.) │ (Uses labels $y$)│ (Flat planes)    │ to-within spread │ '
                                'classes overlap along high variance│\n'
                                '├─────────────────────┼──────────────────┼──────────────────┼──────────────────┼────────────────────────────────────┤\n'
                                '│ **t-SNE**           │ **Unsupervised** │ **Non-Linear**   │ Preserves local  │ Pure '
                                '2D/3D visualization of dense, │\n'
                                '│                     │                  │ (Manifold curve) │ neighborhoods    │ '
                                'complex clusters (e.g. single cell)│\n'
                                '├─────────────────────┼──────────────────┼──────────────────┼──────────────────┼────────────────────────────────────┤\n'
                                '│ **UMAP**            │ Unsupervised or  │ **Non-Linear**   │ Preserves local +│ Fast '
                                'non-linear visualization and  │\n'
                                '│                     │ Semi-Supervised  │ (Riemannian geom)│ global structure │ '
                                'general-purpose manifold embedding.│\n'
                                '└─────────────────────┴──────────────────┴──────────────────┴──────────────────┴────────────────────────────────────┘\n'
                                '```\n'
                                '\n'
                                '#### Why PCA Differs from LDA (The Unsupervised Blind Spot):\n'
                                '- PCA finds axes of maximal overall data spread **without knowing class labels**.\n'
                                '- If two distinct classes are distributed along a narrow corridor, PCA will choose '
                                'the long direction of the corridor (PC1), merging the two classes together!\n'
                                '- **Linear Discriminant Analysis (LDA)** uses class labels to find directions that '
                                "maximize between-class variance while minimizing within-class variance (Fisher's "
                                'criterion), separating the classes cleanly!',
                        'citations': [   'Strang, G. (2016). Introduction to Linear Algebra (5th ed.). '
                                         'Wellesley-Cambridge Press, Chapter 6 & 7.'],
                        'heading': '3. Geometric Intuition & Eigenvalues in Plain Language',
                        'section_id': 'cml-l15-sec03'},
                    {   'body': '### 4.1 The Data Leakage Hazard: Fitting PCA on Test Data\n'
                                '\n'
                                'A widespread and catastrophic mistake made by junior practitioners is running PCA on '
                                'the entire dataset before splitting into training and testing sets:\n'
                                '\n'
                                '```python\n'
                                '# CATASTROPHIC DATA LEAKAGE TRAP - DO NOT DO THIS!\n'
                                'X_scaled = StandardScaler().fit_transform(X)\n'
                                'X_pca = PCA(n_components=5).fit_transform(X_scaled)  # LEAKAGE OCCURS HERE!\n'
                                'X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.25)\n'
                                '```\n'
                                '\n'
                                '#### Why is this Data Leakage?\n'
                                '- PCA learns the principal directions $\\mathbf{V}$ by examining the **covariance '
                                'structure of all rows**.\n'
                                '- If test samples are included when computing means $\\boldsymbol{\\mu}$, standard '
                                'deviations $\\boldsymbol{\\sigma}$, and eigenvectors $\\mathbf{V}$, **information '
                                'about the test set distribution leaks directly into the training features**!\n'
                                "- The model's validation scores will be artificially optimistic and will degrade when "
                                'deployed to real production traffic.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.2 The Leak-Free Scikit-Learn Pipeline\n'
                                '\n'
                                'To guarantee zero data leakage, PCA must be treated as an estimator that is fitted '
                                '**strictly and exclusively on the training split**:\n'
                                '\n'
                                '```python\n'
                                'from sklearn.pipeline import Pipeline\n'
                                'from sklearn.preprocessing import StandardScaler\n'
                                'from sklearn.decomposition import PCA\n'
                                'from sklearn.linear_model import LogisticRegression\n'
                                'from sklearn.model_selection import train_test_split\n'
                                '\n'
                                '# 1. Split FIRST\n'
                                'X_train, X_test, y_train, y_test = train_test_split(\n'
                                '    X, y, test_size=0.25, random_state=42, stratify=y\n'
                                ')\n'
                                '\n'
                                '# 2. Encapsulate in a Leak-Free Pipeline\n'
                                'pca_pipeline = Pipeline([\n'
                                '    ("scaler", StandardScaler()),\n'
                                '    ("pca", PCA(n_components=0.95)),  # Retain 95% of training variance\n'
                                '    ("classifier", LogisticRegression(random_state=42))\n'
                                '])\n'
                                '\n'
                                '# 3. Fit strictly on training data\n'
                                'pca_pipeline.fit(X_train, y_train)\n'
                                '\n'
                                '# 4. Evaluate on untouched test set\n'
                                'test_score = pca_pipeline.score(X_test, y_test)\n'
                                'print(f"Holdout Test Accuracy (Leak-Free): {test_score * 100:.2f}%")\n'
                                '```\n'
                                '\n'
                                'When `pca_pipeline.fit(X_train, y_train)` executes:\n'
                                '- `StandardScaler` computes $\\boldsymbol{\\mu}_{\\text{train}}$ and '
                                '$\\boldsymbol{\\sigma}_{\\text{train}}$ from `X_train` only.\n'
                                '- `PCA` computes eigenvectors $\\mathbf{V}_{\\text{train}}$ from `X_train` only.\n'
                                '- When `predict(X_test)` is called, test points are transformed using the frozen '
                                'training parameters:\n'
                                '  $$\\mathbf{z}_{\\text{test}} = \\left( \\frac{\\mathbf{x}_{\\text{test}} - '
                                '\\boldsymbol{\\mu}_{\\text{train}}}{\\boldsymbol{\\sigma}_{\\text{train}}} \\right) '
                                '\\mathbf{V}_{\\text{train}}$$',
                        'citations': [   'Cattell, R. B. (1966). The scree test for the number of factors. '
                                         'Multivariate Behavioral Research, 1(2), 245-276.',
                                         'Pedregosa, F. et al. (2011). Scikit-learn: Machine learning in Python. JMLR, '
                                         '12, 2825-2830.'],
                        'heading': '4. Selecting k: Scree Plots & Leakage-Free Pipelines',
                        'section_id': 'cml-l15-sec04'},
                    {   'body': '### 5.1 Hands-On Python Implementation: 64-Pixel Handwritten Digit Compression\n'
                                '\n'
                                'The following production script applies PCA to compress, reconstruct, and visualize '
                                'the 64-dimensional Scikit-Learn `digits` dataset (8x8 pixel images of numbers 0 '
                                'through 9):\n'
                                '\n'
                                '```python\n'
                                'import numpy as np\n'
                                'import pandas as pd\n'
                                'import matplotlib.pyplot as plt\n'
                                'from sklearn.datasets import load_digits\n'
                                'from sklearn.decomposition import PCA\n'
                                'from sklearn.model_selection import train_test_split\n'
                                'from sklearn.linear_model import LogisticRegression\n'
                                'from sklearn.metrics import accuracy_score\n'
                                '\n'
                                '# 1. Load 8x8 Grayscale Digits Dataset (1,797 images, 64 features)\n'
                                'digits = load_digits()\n'
                                'X, y = digits.data, digits.target\n'
                                'print(f"Original Dataset Shape: {X.shape} (1,797 images with 64 pixel features '
                                'each)")\n'
                                '\n'
                                '# 2. Strict Train / Test Split\n'
                                'X_train, X_test, y_train, y_test = train_test_split(\n'
                                '    X, y, test_size=0.25, random_state=42, stratify=y\n'
                                ')\n'
                                '\n'
                                '# 3. Fit Full PCA to Analyze Explained Variance Spectrum\n'
                                'pca_full = PCA(random_state=42)\n'
                                'pca_full.fit(X_train)\n'
                                'cum_var = np.cumsum(pca_full.explained_variance_ratio_)\n'
                                '\n'
                                'k_50 = np.argmax(cum_var >= 0.50) + 1\n'
                                'k_90 = np.argmax(cum_var >= 0.90) + 1\n'
                                'k_95 = np.argmax(cum_var >= 0.95) + 1\n'
                                '\n'
                                'print("\\n=== VARIANCE COMPONENT RETENTION ===")\n'
                                'print(f"Components for 50% variance: {k_50:2d} / 64 components")\n'
                                'print(f"Components for 90% variance: {k_90:2d} / 64 components")\n'
                                'print(f"Components for 95% variance: {k_95:2d} / 64 components")\n'
                                '\n'
                                '# 4. Compare Compression & Classification Fidelity Across k\n'
                                'k_candidates = [2, 5, 10, 21, 29, 64]\n'
                                'comparison_records = []\n'
                                '\n'
                                'for k in k_candidates:\n'
                                '    pca = PCA(n_components=k, random_state=42)\n'
                                '    X_train_pca = pca.fit_transform(X_train)\n'
                                '    X_test_pca = pca.transform(X_test)\n'
                                '\n'
                                '    # Reconstruct images from k components: X_hat = Z * V_k^T + mu\n'
                                '    X_reconstructed = pca.inverse_transform(X_test_pca)\n'
                                '    \n'
                                '    # Compute Mean Squared Reconstruction Error (MSRE)\n'
                                '    msre = np.mean((X_test - X_reconstructed) ** 2)\n'
                                '\n'
                                '    # Evaluate Downstream Classifier\n'
                                '    clf = LogisticRegression(max_iter=1000, random_state=42)\n'
                                '    clf.fit(X_train_pca, y_train)\n'
                                '    test_acc = accuracy_score(y_test, clf.predict(X_test_pca))\n'
                                '    \n'
                                '    var_preserved = np.sum(pca.explained_variance_ratio_) * 100\n'
                                '\n'
                                '    comparison_records.append({\n'
                                '        "Components (k)": k,\n'
                                '        "Variance Preserved": f"{var_preserved:.1f}%",\n'
                                '        "Compression Ratio": f"{64 / k:.1f}x",\n'
                                '        "Reconstruction Error (MSRE)": f"{msre:.3f}",\n'
                                '        "Holdout Test Accuracy": f"{test_acc * 100:.2f}%"\n'
                                '    })\n'
                                '\n'
                                'results_df = pd.DataFrame(comparison_records)\n'
                                'print("\\n=== PCA COMPRESSION & ACCURACY TRADEOFF TABLE ===")\n'
                                'print(results_df.to_string(index=False))\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.2 Compression Trade-Off Table\n'
                                '\n'
                                '| Number of Components ($k$) | Variance Preserved | Storage Compression | '
                                'Reconstruction MSE | Test Accuracy (LogReg) | Visual Fidelity & Utility |\n'
                                '| :---: | :---: | :---: | :---: | :---: | :--- |\n'
                                '| **$k = 2$** | $28.5\\%$ | **$32.0\\times$** | $8.420$ | $61.78\\%$ | Blurry blobs; '
                                'suitable only for 2D exploratory scatter plots. |\n'
                                '| **$k = 5$** | $50.3\\%$ | **$12.8\\times$** | $5.850$ | $85.33\\%$ | Coarse digit '
                                'outlines recognizable; rapid classification. |\n'
                                '| **$k = 10$** | $74.2\\%$ | **$6.4\\times$** | $3.030$ | $92.89\\%$ | Sharp, '
                                'readable digits; captures primary strokes. |\n'
                                '| **$k = 21$** | $\\mathbf{90.1\\%}$ | **$3.0\\times$** | $1.160$ | '
                                '$\\mathbf{95.78\\%}$ | **Optimal Compression Sweet Spot**: Indistinguishable from raw '
                                'images. |\n'
                                '| **$k = 29$** | $\\mathbf{95.0\\%}$ | **$2.2\\times$** | $0.580$ | '
                                '$\\mathbf{96.22\\%}$ | Matches full model accuracy while cutting dimensions in half. '
                                '|\n'
                                '| **$k = 64$ (Raw)** | $100.0\\%$ | $1.0\\times$ | $0.000$ | $96.22\\%$ | '
                                'Uncompressed baseline. |\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.3 Diagnostic Failure Modes & Engineering Pitfalls\n'
                                '\n'
                                '| Engineering Failure Mode | Underlying Root Cause | Catastrophic Symptom | '
                                'Recommended Production Solution |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **The Non-Linear Manifold Trap** | PCA only searches for straight, orthogonal flat '
                                'hyperplanes. | Fails completely on non-linear manifolds (e.g. Swiss roll, concentric '
                                'circles). | Use **Kernel PCA** (RBF kernel), **t-SNE** (for visualization), or '
                                '**UMAP**. |\n'
                                '| **Outlier Distortion of Covariance** | Covariance calculation sums squared '
                                'differences $(x_i - \\mu)^2$. | A single extreme outlier violently drags PC1 toward '
                                'itself, tilting the principal axis. | Apply **Robust PCA** (using median absolute '
                                'deviations) or trim outliers prior to PCA. |\n'
                                '| **Unsupervised Blind Spot** | PCA maximizes variance without knowing target labels '
                                '$y$. | The direction of maximum variance might be completely orthogonal to the class '
                                'boundary! | Use **Linear Discriminant Analysis (LDA)** or supervised feature '
                                'selection (Mutual Information). |\n'
                                '| **Loss of Feature Interpretability** | Principal components are linear combinations '
                                'of all original features. | Stakeholders cannot understand what $\\text{PC1} = '
                                '0.42(\\text{Income}) - 0.38(\\text{Age}) + \\dots$ means in business terms. | Use '
                                '**Sparse PCA** (adds L1 penalty to loadings) or feature importance from Random '
                                'Forests. |\n'
                                '| **Information Leakage via Global PCA** | Fitting PCA on combined train and test '
                                'splits before modeling. | Validation accuracy is overly optimistic; model performance '
                                'collapses in production. | Encapsulate PCA strictly inside a Scikit-Learn `Pipeline`. '
                                '|\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.4 Production Code: PCA Biplot & Feature Loading Analysis\n'
                                '\n'
                                'To understand what each principal component represents in real-world domain terms, '
                                'engineers construct a **PCA Biplot**:\n'
                                '\n'
                                '```python\n'
                                '# Inspect feature loadings on Wine dataset\n'
                                'from sklearn.datasets import load_wine\n'
                                'wine = load_wine()\n'
                                'X_w, y_w = wine.data, wine.target\n'
                                '\n'
                                'scaler = StandardScaler()\n'
                                'X_w_scaled = scaler.fit_transform(X_w)\n'
                                '\n'
                                'pca_w = PCA(n_components=2, random_state=42)\n'
                                'X_w_pca = pca_w.fit_transform(X_w_scaled)\n'
                                '\n'
                                '# Loadings matrix: eigenvectors scaled by square root of eigenvalues\n'
                                'loadings = pd.DataFrame(\n'
                                '    pca_w.components_.T,\n'
                                '    columns=["PC1_Loading", "PC2_Loading"],\n'
                                '    index=wine.feature_names\n'
                                ')\n'
                                '\n'
                                '# Sort by absolute contribution to PC1\n'
                                'loadings["PC1_Magnitude"] = loadings["PC1_Loading"].abs()\n'
                                'sorted_loadings = loadings.sort_values(by="PC1_Magnitude", ascending=False)\n'
                                '\n'
                                'print("=== WINE DATASET: TOP FEATURE LOADINGS ON PC1 ===")\n'
                                'print(sorted_loadings[["PC1_Loading", "PC2_Loading"]].head(6).round(3))\n'
                                '```\n'
                                '\n'
                                'This reveals that features like `flavanoids` ($+0.423$) and `phenols` ($+0.395$) '
                                'strongly load onto PC1, while `color_intensity` ($-0.530$) dominates PC2, providing '
                                'an interpretable chemical basis for cultivar separation!',
                        'citations': [   'Turk, M. A., & Pentland, A. P. (1991). Face recognition using eigenfaces. '
                                         'CVPR, 586-591.'],
                        'heading': '5. Applications: Lossy Compression & 2D Image Visualization',
                        'section_id': 'cml-l15-sec05'}],
    'subject_code': 'CML',
    'summary': 'An intuitive yet mathematically rigorous guide to Principal Component Analysis (PCA) and '
               'Dimensionality Reduction. Establishes variance as the geometric currency of information, uses the '
               'torch-and-shadow analogy to explain projection, demystifies eigenvalues and eigenvectors as stretch '
               'factors and invariant directions of the covariance matrix, demonstrates the catastrophic '
               "'forgot-to-scale' trap, guides component selection via scree plots, and constructs production "
               'Scikit-Learn pipelines for visualization, compression, and classification.',
    'tags': [   'Dimensionality Reduction',
                'PCA',
                'Principal Component Analysis',
                'Eigenvalues',
                'Eigenvectors',
                'Covariance Matrix',
                'Variance Maximization',
                'Scree Plot',
                'Data Compression',
                'Data Visualization',
                'StandardScaler',
                'Pipeline'],
    'term': 'Term 5',
    'topic_title': '15. Dimensionality Reduction: Principal Component Analysis (PCA) & Variance Maximization'}

