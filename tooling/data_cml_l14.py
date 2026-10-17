"""
Data definition for data_cml_l14:
"""

L14_DATA = {   'approval_status': 'approved',
    'key_takeaways': [   'Unsupervised learning uncovers latent structure in feature space X without target labels y; '
                         'cluster IDs are arbitrary and require domain profiling.',
                         'Because clustering algorithms depend heavily on Euclidean distance, feature scaling '
                         '(StandardScaler) is strictly mandatory.',
                         "Lloyd's K-Means alternates between two simple steps: Assign each point to its nearest "
                         'centroid, then Update each centroid to the mean of its points.',
                         'Inertia (Within-Cluster Sum of Squares, WCSS) monotonically decreases during K-Means '
                         'iterations, guaranteeing convergence to a local minimum.',
                         'k-means++ initialization selects spread-out starting seeds with probability proportional to '
                         'squared distance D(x)^2, avoiding bad local minima.',
                         'Inertia always decreases as k increases; therefore, k must be selected using the Elbow knee '
                         'heuristic paired with the Silhouette score.',
                         'Hierarchical Agglomerative Clustering builds a bottom-up merge tree without requiring k '
                         'upfront; cutting the dendrogram at the largest vertical gap yields stable clusters.',
                         'Ward linkage minimizes total within-cluster variance (producing spherical clusters), while '
                         'Single linkage connects closest pairs (capable of finding non-convex moons but prone to '
                         'chaining).'],
    'last_updated': '2026-10-18T00:00:00Z',
    'learning_objectives': [   'Contrast supervised learning against unsupervised learning and define cluster '
                               'homogeneity via Euclidean distance.',
                               "Execute Lloyd's K-Means algorithm step-by-step: nearest-centroid assignment and "
                               'centroid mean update.',
                               'Analyze the K-Means objective function (Inertia/WCSS), explain local minima '
                               'convergence, and evaluate k-means++ seeding.',
                               'Determine the optimal number of clusters k using the Elbow heuristic and Silhouette '
                               'analysis (cohesion a vs separation b).',
                               'Construct Hierarchical Agglomerative Clustering trees, evaluate linkage criteria '
                               '(Single, Complete, Average, Ward), and cut dendrograms.',
                               'Implement end-to-end customer segmentation in Scikit-Learn, profile cluster personas, '
                               'and diagnose geometric failure modes.'],
    'note_id': 'cml-t5-l14',
    'quiz': {   'questions': [   {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': 'Unsupervised learning discovers latent patterns, groupings, or '
                                                    'geometric structure in feature space X without receiving target '
                                                    'labels y.',
                                     'id': 'q1',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'It operates strictly on input features X without any '
                                                                'ground truth target labels y'},
                                                    {   'id': 'opt2',
                                                        'text': 'It requires twice as many training labels as '
                                                                'supervised learning'},
                                                    {   'id': 'opt3',
                                                        'text': 'It is used exclusively for training deep language '
                                                                'models'},
                                                    {   'id': 'opt4',
                                                        'text': 'It requires calculating gradients on the target '
                                                                'vector'}],
                                     'question': 'What is the defining characteristic of unsupervised learning '
                                                 'compared to supervised learning?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': "Lloyd's K-Means alternates between the ASSIGN step (mapping "
                                                    'points to closest centroid) and the UPDATE step (moving centroids '
                                                    'to the mean of their assigned points).',
                                     'id': 'q2',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Assign each point to its nearest centroid -> Update '
                                                                'each centroid to the arithmetic mean of its assigned '
                                                                'points'},
                                                    {   'id': 'opt2',
                                                        'text': 'Merge the two nearest clusters -> Delete empty '
                                                                'clusters'},
                                                    {   'id': 'opt3',
                                                        'text': 'Move centroids to random positions -> Compute PCA '
                                                                'eigenvalues'},
                                                    {   'id': 'opt4',
                                                        'text': 'Compute silhouette score -> Discard points with '
                                                                'negative silhouette'}],
                                     'question': "In each iteration of Lloyd's K-Means algorithm, which two sequential "
                                                 'steps occur in order?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': 'Euclidean distance is sensitive to scale. A feature with values '
                                                    'in tens of thousands (like annual income) will completely '
                                                    'overwhelm a feature with values between 1 and 10 (like household '
                                                    'size) unless standardized.',
                                     'id': 'q3',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Because K-Means uses Euclidean distance, features '
                                                                'with larger numeric scales would completely dominate '
                                                                'distance calculations'},
                                                    {   'id': 'opt2',
                                                        'text': 'Because K-Means cannot compute distances on positive '
                                                                'numbers'},
                                                    {   'id': 'opt3',
                                                        'text': 'Because unscaled data causes matrix inversion errors'},
                                                    {   'id': 'opt4',
                                                        'text': 'Because Scikit-Learn will reject unscaled arrays with '
                                                                'a compiler error'}],
                                     'question': 'Why is feature scaling (e.g., StandardScaler) strictly necessary '
                                                 'before running K-Means clustering?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': 'Inertia is defined as sum_{i=1}^N ||x_i - mu_{c_i}||^2: the total '
                                                    'within-cluster sum of squared Euclidean distances from each point '
                                                    'to its assigned centroid.',
                                     'id': 'q4',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'The sum of squared Euclidean distances of samples to '
                                                                'their closest assigned cluster centroid'},
                                                    {   'id': 'opt2',
                                                        'text': 'The distance between the two farthest cluster '
                                                                'centroids'},
                                                    {   'id': 'opt3',
                                                        'text': 'The execution time of the convergence loop in '
                                                                'milliseconds'},
                                                    {   'id': 'opt4',
                                                        'text': 'The classification accuracy on holdout test rows'}],
                                     'question': "What does the 'Inertia' (Within-Cluster Sum of Squares, WCSS) metric "
                                                 'measure in K-Means?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': 'Adding more centroids always reduces within-cluster distances. At '
                                                    'k = N, inertia is exactly zero, which is trivial and '
                                                    'uninformative.',
                                     'id': 'q5',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Inertia monotonically decreases as k increases, '
                                                                'trivially reaching 0 when k = N (every point is its '
                                                                'own cluster)'},
                                                    {   'id': 'opt2',
                                                        'text': 'Inertia becomes undefined when k is greater than 2'},
                                                    {   'id': 'opt3',
                                                        'text': 'Inertia measures between-cluster distance rather than '
                                                                'within-cluster distance'},
                                                    {   'id': 'opt4',
                                                        'text': 'Inertia is only calculated for Hierarchical '
                                                                'clustering'}],
                                     'question': 'Why CANNOT the optimal number of clusters k be selected simply by '
                                                 'choosing the k that minimizes Inertia?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': 'k-means++ seeds initial centroids with probability proportional '
                                                    'to squared distance from existing seeds, ensuring they are '
                                                    'well-dispersed and drastically reducing convergence to poor local '
                                                    'minima.',
                                     'id': 'q6',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'It selects spread-out initial centroids, preventing '
                                                                'the algorithm from getting trapped in poor local '
                                                                'minima'},
                                                    {   'id': 'opt2',
                                                        'text': 'It automatically determines the optimal value of k'},
                                                    {   'id': 'opt3',
                                                        'text': 'It converts non-spherical clusters into perfect '
                                                                'spheres'},
                                                    {   'id': 'opt4',
                                                        'text': 'It eliminates the need for computing Euclidean '
                                                                'distances'}],
                                     'question': "What is the primary problem solved by the 'k-means++' initialization "
                                                 'algorithm?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': 'Silhouette score s = (b - a) / max(a, b). When s ≈ +1, '
                                                    'intra-cluster distance a is tiny compared to nearest-cluster '
                                                    'distance b, indicating excellent clustering.',
                                     'id': 'q7',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'The point is well inside its assigned cluster and '
                                                                'comfortably far from neighboring clusters'},
                                                    {   'id': 'opt2',
                                                        'text': 'The point lies right on the boundary between two '
                                                                'competing clusters'},
                                                    {   'id': 'opt3',
                                                        'text': 'The point was assigned to the completely wrong '
                                                                'cluster'},
                                                    {   'id': 'opt4',
                                                        'text': 'The point is a statistical outlier that must be '
                                                                'dropped'}],
                                     'question': 'What does a Silhouette Coefficient close to +1.0 indicate for a data '
                                                 'point?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'easy',
                                     'explanation': 'Agglomerative clustering is a bottom-up approach: it starts with '
                                                    'N clusters (one per data point) and successively merges the '
                                                    'closest pairs.',
                                     'id': 'q8',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Each observation starts as its own individual '
                                                                'singleton cluster (N initial clusters)'},
                                                    {   'id': 'opt2',
                                                        'text': 'All points start in one giant cluster that is '
                                                                'recursively split in half'},
                                                    {   'id': 'opt3',
                                                        'text': 'Points are randomly assigned to 3 predetermined '
                                                                'clusters'},
                                                    {   'id': 'opt4',
                                                        'text': 'Centroids are initialized at the origin (0, 0)'}],
                                     'question': 'In Hierarchical Agglomerative Clustering, how does the algorithm '
                                                 'initially treat each data point?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'Distances to mu_1=1 vs mu_2=2: For point 1, dist is 0 to mu_1, 1 '
                                                    'to mu_2 -> Cluster 1. For point 2, dist is 1 to mu_1, 0 to mu_2 '
                                                    '-> Cluster 2. For points 9, 10, 11, distance to mu_2=2 is '
                                                    'strictly smaller than to mu_1=1 -> Cluster 2. So Cluster 1 has '
                                                    '{1} (mean = 1.0) and Cluster 2 has {2, 9, 10, 11} (mean = '
                                                    '(2+9+10+11)/4 = 32/4 = 8.0).',
                                     'id': 'q9',
                                     'options': [   {'id': 'opt1', 'text': 'mu_1 = 1.0, mu_2 = 8.0'},
                                                    {'id': 'opt2', 'text': 'mu_1 = 1.5, mu_2 = 10.0'},
                                                    {'id': 'opt3', 'text': 'mu_1 = 1.0, mu_2 = 10.0'},
                                                    {'id': 'opt4', 'text': 'mu_1 = 5.0, mu_2 = 5.0'}],
                                     'question': 'Suppose in 1D space we have points [1, 2, 9, 10, 11] and choose k = '
                                                 '2 with initial centroids mu_1 = 1 and mu_2 = 2. After the first '
                                                 'assign and update step, what are the new centroids?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 's(i) = (b - a) / max(a, b) = (1.5 - 2.0) / max(2.0, 1.5) = -0.5 / '
                                                    '2.0 = -0.25. The negative score indicates the point is closer on '
                                                    'average to a neighboring cluster than to its own.',
                                     'id': 'q10',
                                     'options': [   {'id': 'opt1', 'text': '-0.25'},
                                                    {'id': 'opt2', 'text': '+0.25'},
                                                    {'id': 'opt3', 'text': '+0.50'},
                                                    {'id': 'opt4', 'text': '-0.50'}],
                                     'question': 'For a specific observation i, its mean distance to other points in '
                                                 'its own cluster is a(i) = 2.0, and its mean distance to points in '
                                                 'the nearest other cluster is b(i) = 1.5. What is its Silhouette '
                                                 'Coefficient s(i)?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'Single linkage defines cluster distance as the minimum pairwise '
                                                    'distance between points in the two clusters: min{d(a, b) : a in '
                                                    'A, b in B}.',
                                     'id': 'q11',
                                     'options': [   {'id': 'opt1', 'text': 'Single Linkage'},
                                                    {'id': 'opt2', 'text': 'Complete Linkage'},
                                                    {'id': 'opt3', 'text': 'Average Linkage'},
                                                    {'id': 'opt4', 'text': "Ward's Linkage"}],
                                     'question': 'Which linkage criterion in Hierarchical Agglomerative Clustering '
                                                 'measures the shortest distance between ANY single point in cluster A '
                                                 'and ANY single point in cluster B?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'Because single linkage looks only at the single closest pair of '
                                                    "points, a thin chain of noisy intermediate points will 'bridge' "
                                                    'two large, distinct clusters into a single elongated cluster.',
                                     'id': 'q12',
                                     'options': [   {   'id': 'opt1',
                                                        'text': "The 'chaining effect', where a few noisy bridge "
                                                                'points between two distinct clusters cause them to '
                                                                'merge prematurely'},
                                                    {   'id': 'opt2',
                                                        'text': 'It can only produce clusters of identical spherical '
                                                                'diameters'},
                                                    {   'id': 'opt3',
                                                        'text': 'It is mathematically incapable of identifying '
                                                                'non-convex curved shapes'},
                                                    {   'id': 'opt4',
                                                        'text': 'It requires the user to specify k before building the '
                                                                'hierarchy'}],
                                     'question': 'What is the primary operational weakness of Single Linkage '
                                                 'clustering?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': "Ward's linkage seeks to minimize the growth of total "
                                                    'within-cluster variance upon merging, making it conceptually and '
                                                    'mathematically analogous to K-Means within a hierarchy.',
                                     'id': 'q13',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'The increase in total within-cluster sum of squares '
                                                                '(variance/inertia)'},
                                                    {   'id': 'opt2',
                                                        'text': 'The maximum distance between any two points in the '
                                                                'merged cluster'},
                                                    {'id': 'opt3', 'text': 'The number of outliers in the dataset'},
                                                    {'id': 'opt4', 'text': 'The correlation between feature columns'}],
                                     'question': "What objective does Ward's Linkage minimize when deciding which two "
                                                 'clusters to merge in Agglomerative Clustering?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1', 'opt2', 'opt3'],
                                     'difficulty': 'medium',
                                     'explanation': 'K-Means assumes convex (spherical) clusters with similar variance '
                                                    'and requires scaled features. It works well on spherical Gaussian '
                                                    'blobs, but fails on rings/moons, unequal variances, or unscaled '
                                                    'data.',
                                     'id': 'q14',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Concentric rings or interleaved half-moon shapes'},
                                                    {   'id': 'opt2',
                                                        'text': 'Clusters with vastly different densities or '
                                                                'variances'},
                                                    {   'id': 'opt3',
                                                        'text': 'Data where features have wildly different unscaled '
                                                                'physical units'},
                                                    {   'id': 'opt4',
                                                        'text': 'Well-separated spherical Gaussian blobs with equal '
                                                                'variances and standard scales'}],
                                     'question': 'Which of the following data distributions cause standard K-Means to '
                                                 'produce counter-intuitive or incorrect partitions? (Select all that '
                                                 'apply)',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'A horizontal cut across a dendrogram partitions the tree into '
                                                    'distinct sub-branches. Each vertical line intersected by the cut '
                                                    'represents one resulting cluster.',
                                     'id': 'q15',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Draw a horizontal cut line across the dendrogram; the '
                                                                'number of intersected vertical branches equals the '
                                                                'number of clusters'},
                                                    {   'id': 'opt2',
                                                        'text': 'Count the number of leaf nodes at the bottom'},
                                                    {   'id': 'opt3',
                                                        'text': 'Take the logarithm of the root merge height'},
                                                    {   'id': 'opt4',
                                                        'text': 'Count the number of data points along the horizontal '
                                                                'axis'}],
                                     'question': 'How do you determine the number of clusters from a hierarchical '
                                                 'clustering dendrogram?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'There are only k^N possible partitions of N points into k '
                                                    'clusters. Since every assign and update step strictly lowers (or '
                                                    'maintains) the bounded inertia function, the algorithm cannot '
                                                    'cycle and must converge.',
                                     'id': 'q16',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Because both the assign and update steps strictly '
                                                                'decrease or preserve inertia across a finite number '
                                                                'of possible cluster assignments'},
                                                    {   'id': 'opt2',
                                                        'text': 'Because it uses stochastic gradient descent with an '
                                                                'adaptive learning rate'},
                                                    {   'id': 'opt3',
                                                        'text': 'Because it inverts a positive-definite covariance '
                                                                'matrix'},
                                                    {   'id': 'opt4',
                                                        'text': 'Because Scikit-Learn caps all loops at 5 iterations'}],
                                     'question': "Why does Lloyd's K-Means algorithm always converge in a finite "
                                                 'number of steps?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1', 'opt2', 'opt3'],
                                     'difficulty': 'medium',
                                     'explanation': 'K-Means is linear in N and can predict new points. Agglomerative '
                                                    'clustering takes O(N^2) memory and has no native predict(). '
                                                    'However, Agglomerative clustering is fully deterministic given a '
                                                    'distance matrix and linkage.',
                                     'id': 'q17',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'K-Means requires specifying k upfront, whereas '
                                                                'Agglomerative Clustering builds the entire hierarchy '
                                                                'and allows cutting later'},
                                                    {   'id': 'opt2',
                                                        'text': 'K-Means scales easily to large datasets (O(N) per '
                                                                'iteration), whereas Agglomerative Clustering requires '
                                                                'O(N^2) memory for pairwise distances'},
                                                    {   'id': 'opt3',
                                                        'text': 'K-Means can assign new unseen test points via nearest '
                                                                'centroid, whereas Agglomerative Clustering does not '
                                                                'have a native out-of-sample predict method'},
                                                    {   'id': 'opt4',
                                                        'text': 'Agglomerative Clustering is non-deterministic and '
                                                                'yields different results on every run'}],
                                     'question': 'Which of the following statements comparing K-Means and '
                                                 'Agglomerative Clustering are TRUE? (Select all that apply)',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'medium',
                                     'explanation': 'In Scikit-Learn, if a cluster loses all members, the centroid is '
                                                    're-initialized to the point with the largest squared distance '
                                                    'from its assigned centroid, ensuring k clusters are maintained.',
                                     'id': 'q18',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Standard implementations like Scikit-Learn re-seed '
                                                                'the empty centroid to the observation farthest from '
                                                                'any current centroid'},
                                                    {   'id': 'opt2',
                                                        'text': 'The computer throws a division by zero exception and '
                                                                'crashes'},
                                                    {   'id': 'opt3',
                                                        'text': 'k is permanently reduced by 1 for all future models'},
                                                    {   'id': 'opt4',
                                                        'text': 'All data points are assigned to cluster 0'}],
                                     'question': 'What happens if you run K-Means on a dataset and one of the clusters '
                                                 'becomes completely empty during an assign step?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'hard',
                                     'explanation': 'While clustering must be performed on scaled data for geometric '
                                                    'validity, interpreting cluster personas requires taking the '
                                                    'unscaled original feature means (e.g., average income in dollars, '
                                                    'average age in years) so business stakeholders understand the '
                                                    'segments.',
                                     'id': 'q19',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Group the dataset by cluster label and calculate the '
                                                                'mean values of the ORIGINAL, unscaled features (plus '
                                                                'segment size)'},
                                                    {   'id': 'opt2',
                                                        'text': 'Report the standardized z-score values directly to '
                                                                'business stakeholders'},
                                                    {   'id': 'opt3',
                                                        'text': 'Multiply cluster labels by the PCA eigenvalue'},
                                                    {   'id': 'opt4',
                                                        'text': 'Delete all clusters that have fewer than 50% of the '
                                                                'total customers'}],
                                     'question': 'Suppose you are performing customer segmentation. After running '
                                                 'K-Means with k = 4 on scaled spending and income features, how '
                                                 'should you compute the business profile of each cluster?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'hard',
                                     'explanation': 'Single linkage follows minimum point-to-point distances along the '
                                                    'circumference of each ring, easily separating the two rings. '
                                                    "Ward's linkage attempts to minimize spherical within-cluster "
                                                    'variance, so it cuts across the rings into chunky spatial blobs.',
                                     'id': 'q20',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Single Linkage correctly isolates the two rings (ARI '
                                                                "= 1.0); Ward's Linkage splits the rings into "
                                                                'half-moons/wedges because it penalizes variance'},
                                                    {   'id': 'opt2',
                                                        'text': "Ward's Linkage isolates the rings perfectly; Single "
                                                                'Linkage fails due to variance explosion'},
                                                    {   'id': 'opt3',
                                                        'text': 'Both methods fail because clustering cannot be '
                                                                'performed in 2 dimensions'},
                                                    {   'id': 'opt4',
                                                        'text': 'Single Linkage places all points into a single '
                                                                'cluster at height zero'}],
                                     'question': 'Consider two concentric circles of data points in 2D space: an inner '
                                                 'ring of radius 1 and an outer ring of radius 5. If you fit '
                                                 "Agglomerative Clustering with Single Linkage vs Ward's Linkage, what "
                                                 'occurs?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'hard',
                                     'explanation': 'Computing pairwise Euclidean distances between all pairs among N '
                                                    'observations requires N*(N-1)/2 distance evaluations, each taking '
                                                    'O(p) operations, leading to O(p * N^2) time and O(N^2) space.',
                                     'id': 'q21',
                                     'options': [   {'id': 'opt1', 'text': 'O(p * N^2)'},
                                                    {'id': 'opt2', 'text': 'O(N * log N)'},
                                                    {'id': 'opt3', 'text': 'O(k * N)'},
                                                    {'id': 'opt4', 'text': 'O(p^3)'}],
                                     'question': 'What is the time complexity of the naive distance matrix computation '
                                                 'in Hierarchical Agglomerative Clustering for N observations with p '
                                                 'features?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1', 'opt2', 'opt3'],
                                     'difficulty': 'hard',
                                     'explanation': 'Subsample bootstrapping (stability checking), cross-algorithm '
                                                    'consensus, and silhouette profile inspection are established '
                                                    'rigorous cluster validation practices. Setting k = p is an '
                                                    'arbitrary, invalid rule.',
                                     'id': 'q22',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Subsample 80% of the dataset multiple times and '
                                                                'measure cluster agreement (e.g., Adjusted Rand Index) '
                                                                'across runs'},
                                                    {   'id': 'opt2',
                                                        'text': 'Compare partitions between two completely different '
                                                                'algorithms (e.g., K-Means vs Ward Hierarchical)'},
                                                    {   'id': 'opt3',
                                                        'text': 'Inspect silhouette plots to confirm that most '
                                                                'clusters have positive silhouette scores and balanced '
                                                                'widths'},
                                                    {   'id': 'opt4',
                                                        'text': 'Always set k equal to the number of columns in the '
                                                                'dataset'}],
                                     'question': 'Which of the following techniques can help validate cluster '
                                                 'stability and prevent over-interpreting random noise? (Select all '
                                                 'that apply)',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'hard',
                                     'explanation': 'n_init runs the whole clustering pipeline n_init times from '
                                                    'different random initializations and outputs the model from the '
                                                    'best run (minimum within-cluster sum of squares).',
                                     'id': 'q23',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Run the complete K-Means algorithm 10 times '
                                                                'independently with different centroid seeds and '
                                                                'retain the run with the lowest final Inertia'},
                                                    {   'id': 'opt2',
                                                        'text': 'Run exactly 10 iterations of the assign-update loop '
                                                                'and stop'},
                                                    {   'id': 'opt3',
                                                        'text': 'Split the dataset into 10 cross-validation folds'},
                                                    {'id': 'opt4', 'text': 'Use 10 features to compute distances'}],
                                     'question': "In Scikit-Learn's KMeans, what does the parameter n_init=10 "
                                                 'specifically instruct the estimator to do?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'hard',
                                     'explanation': 'Silhouette score requires calculating b(i), the distance to the '
                                                    "closest cluster other than the sample's own cluster. With k = 1, "
                                                    'there is no second cluster, so b(i) cannot be computed.',
                                     'id': 'q24',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Because the nearest-cluster distance b(i) requires at '
                                                                'least one neighboring cluster to exist'},
                                                    {'id': 'opt2', 'text': 'Because Inertia is infinite when k = 1'},
                                                    {   'id': 'opt3',
                                                        'text': 'Because Euclidean distance cannot be calculated with '
                                                                'only 1 cluster'},
                                                    {   'id': 'opt4',
                                                        'text': 'Because Scikit-Learn forces k >= 2 for all '
                                                                'estimators'}],
                                     'question': 'Why is the Silhouette Score undefined for k = 1?',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt1'],
                                     'difficulty': 'hard',
                                     'explanation': 'In K-Means, assignment is strictly deterministic given the '
                                                    'centroids: a point is assigned to cluster j if and only if ||x_i '
                                                    '- mu_j||^2 < ||x_i - mu_m||^2 for all other clusters m.',
                                     'id': 'q25',
                                     'options': [   {   'id': 'opt1',
                                                        'text': 'Because the standardized Euclidean distance from '
                                                                'customer #408 to the centroid of Cluster 2 was '
                                                                'strictly smaller than to the centroid of Cluster 1'},
                                                    {   'id': 'opt2',
                                                        'text': 'Because Cluster 2 had a higher decision tree '
                                                                'information gain'},
                                                    {   'id': 'opt3',
                                                        'text': 'Because customer #408 had the highest spending score '
                                                                'in the dataset'},
                                                    {   'id': 'opt4',
                                                        'text': 'Because K-Means randomly sorts customer IDs during '
                                                                'the assign step'}],
                                     'question': "Suppose a business stakeholder asks: 'Why did customer #408 get "
                                                 "assigned to Cluster 2 instead of Cluster 1?'. How can you explain "
                                                 'this decision rigorously based on K-Means mathematics?',
                                     'type': 'single_choice'}],
                'quiz_id': 'quiz-cml-t5-l14',
                'title': 'Topic Quiz: K-Means & Hierarchical Clustering'},
    'schema_version': 1,
    'sections': [   {   'body': '### 1.1 The Hook: Finding Hidden Structure Without Ground Truth Labels\n'
                                '\n'
                                'Imagine examining a retail database containing transaction histories for 10,000 '
                                'customers:\n'
                                '- There is no target variable $y$. No column indicates *"Good Customer"* or *"Bad '
                                'Customer"*.\n'
                                '- The machine learning model is given only the feature matrix $\\mathbf{X} \\in '
                                '\\mathbb{R}^{n \\times d}$ (e.g., Annual Income, Spending Score, Age, Visit '
                                'Frequency).\n'
                                '- Yet, when plotted in feature space, the observations are not uniformly scattered. '
                                'They naturally coalesce into dense geometric islands separated by sparse valleys.\n'
                                '\n'
                                '**Clustering** is the foundational task of **Unsupervised Learning**:\n'
                                'Its objective is to discover natural, coherent groupings (clusters) within data such '
                                'that:\n'
                                '1. **High Intra-Cluster Cohesion**: Observations within the same cluster are as '
                                'geometrically similar (close) to each other as possible.\n'
                                '2. **High Inter-Cluster Separation**: Observations in different clusters are as '
                                'geometrically distinct (distant) from each other as possible.\n'
                                '\n'
                                '```\n'
                                'Supervised vs. Unsupervised Learning Paradigms:\n'
                                '   Supervised Learning (Classification):\n'
                                '      Feature Matrix X + Ground Truth Labels y ──► [ Learn Mapping f(X) -> y ] ──► '
                                'Evaluate on y_test\n'
                                '\n'
                                '   Unsupervised Learning (Clustering):\n'
                                '      Feature Matrix X (No Labels!) ──────────► [ Discover Latent Structure ] ──► '
                                'Geometric Cohesion & Separation\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.2 Comparison: Supervised vs. Unsupervised Learning\n'
                                '\n'
                                '| Dimension | Supervised Learning (Regression / Classification) | Unsupervised '
                                'Learning (Clustering / PCA) |\n'
                                '| :--- | :--- | :--- |\n'
                                '| **Data Requirements** | Feature matrix $\\mathbf{X}$ and target vector '
                                '$\\mathbf{y}$. | Feature matrix $\\mathbf{X}$ **only**. No target $y$ exists. |\n'
                                '| **Objective** | Learn a predictive mapping $f: \\mathbf{x} \\mapsto y$ that '
                                'generalizes to unseen $\\mathbf{x}_{\\text{test}}$. | Partition feature space '
                                '$\\mathbb{R}^d$ into $K$ meaningful clusters or low-dimensional manifolds. |\n'
                                '| **Evaluation** | Concrete external ground truth: Accuracy, ROC-AUC, Mean Squared '
                                'Error. | Internal geometric metrics: Inertia, Silhouette Score, Davies-Bouldin Index. '
                                '|\n'
                                '| **Cluster Label Meaning** | Class names have fixed semantic meaning (e.g., $1 = '
                                '\\text{Default}$). | Cluster IDs (`0, 1, 2`) are completely arbitrary and require '
                                'human domain profiling. |\n'
                                '| **Primary Failure Risk** | Overfitting to training labels; data leakage. | Finding '
                                'meaningless patterns in pure noise (clustering algorithms will happily partition '
                                'random uniform noise into $K$ clusters!). |\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.3 The Non-Negotiable Imperative of Feature Scaling\n'
                                '\n'
                                'Because virtually all clustering algorithms rely directly on **Euclidean Distance**:\n'
                                '$$D(\\mathbf{x}_i, \\mathbf{x}_j) = \\sqrt{\\sum_{k=1}^d (x_{ik} - x_{jk})^2}$$\n'
                                '\n'
                                'Features with large numerical ranges (e.g., `Annual Income` ranging from 20,000 USD '
                                'to 200,000 USD) produce squared differences of $(10,000)^2 = 100,000,000$, while '
                                'features with small numerical ranges (e.g., `Age` ranging from $18$ to $70$) produce '
                                'squared differences of $(20)^2 = 400$.\n'
                                '- The algorithm will compute distances based almost exclusively on Income, '
                                '**completely blinding itself to Age**.\n'
                                '- **Rule of Thumb**: Always standardize features with `StandardScaler` ($z = \\frac{x '
                                '- \\mu}{\\sigma}$) before clustering, unless features share identical physical units.',
                        'citations': [   'Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of '
                                         'Statistical Learning (2nd ed.). Springer, Chapter 14.',
                                         'Jain, A. K. (2010). Data clustering: 50 years beyond K-means. Pattern '
                                         'Recognition Letters, 31(8), 651-666.'],
                        'heading': '1. The Unsupervised Paradigm: Finding Structure Without Labels',
                        'section_id': 'cml-l14-sec01'},
                    {   'body': '### 2.1 The K-Means Objective Function: Within-Cluster Sum of Squares (Inertia)\n'
                                '\n'
                                'Let $\\mathcal{D} = \\{\\mathbf{x}_1, \\dots, \\mathbf{x}_n\\} \\subset '
                                '\\mathbb{R}^d$ be our dataset.\n'
                                'We wish to partition the $n$ points into $K$ mutually disjoint subsets $C_1, C_2, '
                                '\\dots, C_K$ such that each cluster has a prototype center (centroid) '
                                '$\\boldsymbol{\\mu}_k \\in \\mathbb{R}^d$.\n'
                                '\n'
                                'The **K-Means Objective Function**, formally known as the **Within-Cluster Sum of '
                                'Squares (WCSS)** or **Inertia** $J(C, \\boldsymbol{\\mu})$, is defined as:\n'
                                '\n'
                                '$$J(C, \\boldsymbol{\\mu}) = \\sum_{k=1}^{K} \\sum_{i \\in C_k} \\|\\mathbf{x}_i - '
                                '\\boldsymbol{\\mu}_k\\|_2^2$$\n'
                                '\n'
                                'Finding the global minimum of $J(C, \\boldsymbol{\\mu})$ is an **NP-hard '
                                'combinatorial problem**, as there are approximately $K^n / K!$ possible ways to '
                                'assign $n$ points into $K$ clusters.\n'
                                "Instead, we solve it using **Lloyd's Algorithm (1957)**, an alternating greedy "
                                'optimization heuristic.\n'
                                '\n'
                                '---\n'
                                '\n'
                                "### 2.2 Lloyd's Algorithm: The Two-Step Dance\n"
                                '\n'
                                "Lloyd's algorithm alternates between two complementary optimization steps until "
                                'convergence:\n'
                                '\n'
                                '```\n'
                                "Lloyd's K-Means Algorithm:\n"
                                '  Initialize K centroids: μ_1, μ_2, ..., μ_K\n'
                                '  Repeat until centroids stop moving (convergence):\n'
                                '     1. Assignment Step (Fix centroids μ, optimize cluster assignments C):\n'
                                '           Assign each observation x_i to its nearest centroid:\n'
                                '           C_k = { x_i : || x_i - μ_k ||^2 <= || x_i - μ_j ||^2   for all j in {1, '
                                '..., K} }\n'
                                '     2. Update Step (Fix cluster assignments C, optimize centroids μ):\n'
                                '           Recompute each centroid as the center of mass (mean) of its assigned '
                                'points:\n'
                                '           μ_k = (1 / |C_k|) * sum_{x_i in C_k} x_i\n'
                                '```\n'
                                '\n'
                                '#### Mathematical Proof of Monotonic Inertia Convergence:\n'
                                '1. **In the Assignment Step**: Holding centroids $\\boldsymbol{\\mu}$ constant, '
                                'assigning each point $\\mathbf{x}_i$ to its nearest centroid strictly minimizes '
                                '$\\sum_k \\sum_{i \\in C_k} \\|\\mathbf{x}_i - \\boldsymbol{\\mu}_k\\|^2$. Therefore, '
                                '$J(C^{(t+1)}, \\boldsymbol{\\mu}^{(t)}) \\le J(C^{(t)}, \\boldsymbol{\\mu}^{(t)})$.\n'
                                '2. **In the Update Step**: Holding assignments $C$ constant, the point that minimizes '
                                'the sum of squared distances to a set of points is the arithmetic mean '
                                '$\\boldsymbol{\\mu}_k = \\frac{1}{|C_k|}\\sum_{i \\in C_k}\\mathbf{x}_i$. (Setting '
                                '$\\frac{\\partial J}{\\partial \\boldsymbol{\\mu}_k} = 0 \\implies -2\\sum_{i \\in '
                                'C_k}(\\mathbf{x}_i - \\boldsymbol{\\mu}_k) = 0 \\implies \\boldsymbol{\\mu}_k = '
                                '\\bar{\\mathbf{x}}_{C_k}$). Therefore, $J(C^{(t+1)}, \\boldsymbol{\\mu}^{(t+1)}) \\le '
                                'J(C^{(t+1)}, \\boldsymbol{\\mu}^{(t)})$.\n'
                                '3. Because $J$ monotonically decreases at every step and there are a finite number of '
                                "partitions ($K^n$), **Lloyd's algorithm is mathematically guaranteed to converge in a "
                                'finite number of iterations** to a local minimum!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.3 Comprehensive Hand-Calculated Walkthrough: Whiteboard 1 (6 Points in 2D)\n'
                                '\n'
                                "Let us trace Lloyd's algorithm by hand on the exact 6-point dataset from class "
                                'whiteboard 1, using a deliberately poor initialization:\n'
                                '\n'
                                '#### The Dataset ($n = 6$ points in $\\mathbb{R}^2$):\n'
                                '- $A = (1.0, 1.0)$\n'
                                '- $B = (1.0, 2.0)$\n'
                                '- $C = (2.0, 1.0)$\n'
                                '- $D = (5.0, 4.0)$\n'
                                '- $E = (5.0, 5.0)$\n'
                                '- $F = (6.0, 5.0)$\n'
                                '\n'
                                'We want $K = 2$ clusters.\n'
                                '**Deliberately Poor Initialization**:\n'
                                '- Centroid 1: $\\boldsymbol{\\mu}_1 = A = (1.0, 1.0)$\n'
                                '- Centroid 2: $\\boldsymbol{\\mu}_2 = B = (1.0, 2.0)$\n'
                                '\n'
                                '---\n'
                                '\n'
                                '#### Iteration 1 — Step 1: Distance Calculation & Cluster Assignment\n'
                                'Compute squared Euclidean distance from each point to $\\boldsymbol{\\mu}_1(1, 1)$ '
                                'and $\\boldsymbol{\\mu}_2(1, 2)$:\n'
                                '\n'
                                '| Point | $(x_1, x_2)$ | $\\|\\mathbf{x} - \\boldsymbol{\\mu}_1\\|^2 = (x_1-1)^2 + '
                                '(x_2-1)^2$ | $\\|\\mathbf{x} - \\boldsymbol{\\mu}_2\\|^2 = (x_1-1)^2 + (x_2-2)^2$ | '
                                'Assigned Cluster |\n'
                                '| :---: | :---: | :---: | :---: | :---: |\n'
                                '| **A** | $(1.0, 1.0)$ | $(0)^2 + (0)^2 = \\mathbf{0.0}$ | $(0)^2 + (-1)^2 = 1.0$ | '
                                '**Cluster 1** |\n'
                                '| **B** | $(1.0, 2.0)$ | $(0)^2 + (1)^2 = 1.0$ | $(0)^2 + (0)^2 = \\mathbf{0.0}$ | '
                                '**Cluster 2** |\n'
                                '| **C** | $(2.0, 1.0)$ | $(1)^2 + (0)^2 = \\mathbf{1.0}$ | $(1)^2 + (-1)^2 = 2.0$ | '
                                '**Cluster 1** |\n'
                                '| **D** | $(5.0, 4.0)$ | $(4)^2 + (3)^2 = 25.0$ | $(4)^2 + (2)^2 = \\mathbf{20.0}$ | '
                                '**Cluster 2** |\n'
                                '| **E** | $(5.0, 5.0)$ | $(4)^2 + (4)^2 = 32.0$ | $(4)^2 + (3)^2 = \\mathbf{25.0}$ | '
                                '**Cluster 2** |\n'
                                '| **F** | $(6.0, 5.0)$ | $(5)^2 + (4)^2 = 41.0$ | $(5)^2 + (3)^2 = \\mathbf{34.0}$ | '
                                '**Cluster 2** |\n'
                                '\n'
                                '- **Cluster 1**: $\\{A, C\\}$\n'
                                '- **Cluster 2**: $\\{B, D, E, F\\}$\n'
                                '- **Iteration 1 Initial Inertia**: $J = (0 + 1) + (0 + 20 + 25 + 34) = 1 + 79 = '
                                '\\mathbf{80.0}$\n'
                                '\n'
                                '---\n'
                                '\n'
                                '#### Iteration 1 — Step 2: Update Centroids\n'
                                'Recompute centroids as the mean of assigned points:\n'
                                '- $\\boldsymbol{\\mu}_1^{(1)} = \\text{mean}(A, C) = \\left( \\frac{1+2}{2}, '
                                '\\frac{1+1}{2} \\right) = \\mathbf{(1.5, 1.0)}$\n'
                                '- $\\boldsymbol{\\mu}_2^{(1)} = \\text{mean}(B, D, E, F) = \\left( '
                                '\\frac{1+5+5+6}{4}, \\frac{2+4+5+5}{4} \\right) = \\left( \\frac{17}{4}, '
                                '\\frac{16}{4} \\right) = \\mathbf{(4.25, 4.0)}$\n'
                                '\n'
                                '---\n'
                                '\n'
                                '#### Iteration 2 — Step 1: Re-assign Points to Updated Centroids\n'
                                'Compute distances to $\\boldsymbol{\\mu}_1(1.5, 1.0)$ and $\\boldsymbol{\\mu}_2(4.25, '
                                '4.0)$:\n'
                                '\n'
                                '| Point | $(x_1, x_2)$ | $\\|\\mathbf{x} - \\boldsymbol{\\mu}_1\\|^2 = (x_1-1.5)^2 + '
                                '(x_2-1.0)^2$ | $\\|\\mathbf{x} - \\boldsymbol{\\mu}_2\\|^2 = (x_1-4.25)^2 + '
                                '(x_2-4.0)^2$ | New Assigned Cluster |\n'
                                '| :---: | :---: | :---: | :---: | :---: |\n'
                                '| **A** | $(1.0, 1.0)$ | $(-0.5)^2 + 0^2 = \\mathbf{0.25}$ | $(-3.25)^2 + (-3)^2 = '
                                '19.56$ | **Cluster 1** |\n'
                                '| **B** | $(1.0, 2.0)$ | $(-0.5)^2 + (1)^2 = \\mathbf{1.25}$ | $(-3.25)^2 + (-2)^2 = '
                                '14.56$ | **Cluster 1 (FLIPPED!)** |\n'
                                '| **C** | $(2.0, 1.0)$ | $(0.5)^2 + 0^2 = \\mathbf{0.25}$ | $(-2.25)^2 + (-3)^2 = '
                                '14.06$ | **Cluster 1** |\n'
                                '| **D** | $(5.0, 4.0)$ | $(3.5)^2 + (3)^2 = 21.25$ | $(0.75)^2 + 0^2 = '
                                '\\mathbf{0.56}$ | **Cluster 2** |\n'
                                '| **E** | $(5.0, 5.0)$ | $(3.5)^2 + (4)^2 = 28.25$ | $(0.75)^2 + (1)^2 = '
                                '\\mathbf{1.56}$ | **Cluster 2** |\n'
                                '| **F** | $(6.0, 5.0)$ | $(4.5)^2 + (4)^2 = 36.25$ | $(1.75)^2 + (1)^2 = '
                                '\\mathbf{4.06}$ | **Cluster 2** |\n'
                                '\n'
                                'Notice that **Point B flipped from Cluster 2 to Cluster 1**!\n'
                                '- **New Cluster 1**: $\\{A, B, C\\}$\n'
                                '- **New Cluster 2**: $\\{D, E, F\\}$\n'
                                '\n'
                                '---\n'
                                '\n'
                                '#### Iteration 2 — Step 2: Recompute Centroids\n'
                                '- $\\boldsymbol{\\mu}_1^{(2)} = \\text{mean}(A, B, C) = \\left( \\frac{1+1+2}{3}, '
                                '\\frac{1+2+1}{3} \\right) = \\left( \\frac{4}{3}, \\frac{4}{3} \\right) \\approx '
                                '\\mathbf{(1.333, 1.333)}$\n'
                                '- $\\boldsymbol{\\mu}_2^{(2)} = \\text{mean}(D, E, F) = \\left( \\frac{5+5+6}{3}, '
                                '\\frac{4+5+5}{3} \\right) = \\left( \\frac{16}{3}, \\frac{14}{3} \\right) \\approx '
                                '\\mathbf{(5.333, 4.667)}$\n'
                                '\n'
                                '---\n'
                                '\n'
                                '#### Iteration 3: Convergence Check\n'
                                'If we compute distances to these new centroids, no point changes assignment.\n'
                                'The algorithm terminates!\n'
                                'Final Converged Inertia:\n'
                                '$$J = \\|\\mathbf{x}_A - \\boldsymbol{\\mu}_1\\|^2 + \\dots + \\|\\mathbf{x}_F - '
                                '\\boldsymbol{\\mu}_2\\|^2 = \\mathbf{4.000}$$\n'
                                'Inertia plunged from $80.0 \\to 4.000$, achieving the globally optimal clustering!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.4 Voronoi Cell Geometry: The Linear Boundary Theorem\n'
                                '\n'
                                'A fundamental geometric property of K-Means is that it partitions space into convex '
                                'polyhedral cells called a **Voronoi Diagram**:\n'
                                '\n'
                                '> **Theorem of Voronoi Boundaries**:\n'
                                '> For any two centroids $\\boldsymbol{\\mu}_j$ and $\\boldsymbol{\\mu}_k$, the '
                                'decision boundary between them is the set of points equidistant from both:\n'
                                '> $$\\|\\mathbf{x} - \\boldsymbol{\\mu}_j\\|^2 = \\|\\mathbf{x} - '
                                '\\boldsymbol{\\mu}_k\\|^2$$\n'
                                '> Expanding the Euclidean norms:\n'
                                '> $$\\mathbf{x}^T \\mathbf{x} - 2\\boldsymbol{\\mu}_j^T \\mathbf{x} + '
                                '\\|\\boldsymbol{\\mu}_j\\|^2 = \\mathbf{x}^T \\mathbf{x} - 2\\boldsymbol{\\mu}_k^T '
                                '\\mathbf{x} + \\|\\boldsymbol{\\mu}_k\\|^2$$\n'
                                '> Cancelling $\\mathbf{x}^T \\mathbf{x}$ and rearranging yields a **strictly linear '
                                'hyperplane equation**:\n'
                                '> $$2(\\boldsymbol{\\mu}_k - \\boldsymbol{\\mu}_j)^T \\mathbf{x} + '
                                '(\\|\\boldsymbol{\\mu}_j\\|^2 - \\|\\boldsymbol{\\mu}_k\\|^2) = 0$$\n'
                                '> $$(\\boldsymbol{\\mu}_k - \\boldsymbol{\\mu}_j)^T \\left( \\mathbf{x} - '
                                '\\frac{\\boldsymbol{\\mu}_j + \\boldsymbol{\\mu}_k}{2} \\right) = 0$$\n'
                                '\n'
                                '```\n'
                                'Voronoi Linear Boundary Geometry:\n'
                                '       x2 ^\n'
                                '          │      \\                     /\n'
                                '          │       \\   Cluster 1       /   Cluster 2\n'
                                '          │        \\     * μ1        /       * μ2\n'
                                '          │         \\               /\n'
                                '          │  ────────┼─────────────┼──────────────\n'
                                '          │           \\           /\n'
                                '          │   Cluster 3\\         /   Cluster 4\n'
                                '          │      * μ3   \\       /       * μ4\n'
                                '          │              \\     /\n'
                                '          └───────────────┴───┴──────────────────► x1\n'
                                '```\n'
                                '\n'
                                '#### Why K-Means Cannot Learn Non-Convex Geometries:\n'
                                'Because every cell boundary is formed by the intersection of flat linear hyperplanes, '
                                '**every K-Means cluster is mathematically guaranteed to be a convex polyhedron**!\n'
                                'If your real-world data contains non-convex manifolds (such as concentric circles or '
                                'interlocking crescents), K-Means will inevitably slice them into arbitrary '
                                'straight-edged pieces!',
                        'citations': [   'Lloyd, S. (1982). Least squares quantization in PCM. IEEE Transactions on '
                                         'Information Theory, 28(2), 129-137.'],
                        'heading': "2. K-Means Algorithm: Lloyd's Assign-Update Cycle",
                        'section_id': 'cml-l14-sec02'},
                    {   'body': '### 3.1 The Initialization Trap & The K-Means++ Breakthrough\n'
                                '\n'
                                "Because Lloyd's algorithm is a greedy gradient descent method on non-convex surfaces, "
                                '**random initialization frequently gets trapped in terrible local minima**:\n'
                                '- If two initial centroids land in the same dense cluster, that cluster gets '
                                'artificially split in half.\n'
                                '- Meanwhile, two distant distinct clusters are forced to share a single centroid!\n'
                                '- In Scikit-Learn, the brute-force workaround was `n_init=10` (running 10 times with '
                                'different random seeds and keeping the lowest inertia run).\n'
                                '\n'
                                'In 2007, David Arthur and Sergei Vassilvitskii revolutionized clustering with '
                                '**k-means++**:\n'
                                '\n'
                                '```\n'
                                'The k-means++ Initialization Algorithm:\n'
                                '  1. Choose the first centroid μ_1 uniformly at random from the dataset D.\n'
                                '  2. For each remaining point x_i in D:\n'
                                '        Compute D(x_i) = shortest distance from x_i to the closest already chosen '
                                'centroid.\n'
                                '  3. Select the next centroid μ_k from D with probability proportional to SQUARED '
                                'distance:\n'
                                '        P(x_i) = [ D(x_i) ]^2 / sum_{j} [ D(x_j) ]^2\n'
                                '  4. Repeat steps 2-3 until K centroids are chosen.\n'
                                "  5. Proceed with standard Lloyd's iterations.\n"
                                '```\n'
                                '\n'
                                '> **The Arthur-Vassilvitskii Theorem (2007)**:\n'
                                '> The k-means++ initialization algorithm is mathematically guaranteed to be '
                                '**$O(\\log K)$-competitive in expectation** with the optimal clustering:\n'
                                '> $$\\mathbb{E}[J_{\\text{k-means++}}] \\le 8(\\ln K + 2) J_{\\text{optimal}}$$\n'
                                '> By forcing new centroids to be picked far away from existing ones ($D(x)^2$ '
                                'sampling), k-means++ avoids seeding multiple centroids into the same cluster!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.2 Determining the Optimal Number of Clusters $K$\n'
                                '\n'
                                'Because clustering is unsupervised, how do we know whether the data contains $K = 2, '
                                '3, 5,$ or $10$ clusters?\n'
                                '\n'
                                '#### 1. The Fatal Flaw of "Lowest Inertia":\n'
                                'Inertia $J$ **strictly decreases** as $K$ increases:\n'
                                '- When $K = n$, every point is its own centroid ($\\boldsymbol{\\mu}_i = '
                                '\\mathbf{x}_i$), and Inertia is identically **$0.0$**!\n'
                                '- Therefore, **you can never pick $K$ by minimizing inertia**.\n'
                                '\n'
                                '#### 2. The Elbow Method (Knee Point Heuristic):\n'
                                'We plot Inertia $J$ as a function of $K \\in \\{1, 2, \\dots, 10\\}$:\n'
                                '- Initially, as $K$ increases, inertia drops steeply because real clusters are being '
                                'separated.\n'
                                '- Beyond the true number of clusters $K^*$, adding more centroids merely splits '
                                'existing tight clusters, producing only marginal inertia reductions.\n'
                                '- The optimal $K^*$ sits at the **"Elbow"** (the point of maximum curvature / knee).\n'
                                '\n'
                                '```\n'
                                'The Elbow Curve:\n'
                                '    Inertia J\n'
                                '      ^\n'
                                '      │  \\\n'
                                '      │   \\\n'
                                '      │    \\  <-- Rapid drop (Real structure uncovered)\n'
                                '      │     \\\n'
                                "      │      '.  <-- THE ELBOW (Optimal K = 3)\n"
                                "      │        ' - - - - - - - - - - - - - -► Marginal drop (Splitting real "
                                'clusters)\n'
                                '      +──────────────┴────────────────────────► Number of Clusters K\n'
                                '      K = 1        K = 3                    K = 10\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.3 Silhouette Analysis: Quantifying Cohesion vs. Separation\n'
                                '\n'
                                'To mathematically validate cluster quality without subjective visual inspection, '
                                'Rousseeuw (1987) introduced the **Silhouette Coefficient**:\n'
                                '\n'
                                'For each individual observation $i$:\n'
                                '1. **Intra-Cluster Cohesion ($a(i)$)**:\n'
                                '   The mean distance between observation $i$ and all other points belonging to the '
                                '**same cluster**:\n'
                                '   $$a(i) = \\frac{1}{|C_I| - 1} \\sum_{j \\in C_I, j \\ne i} \\|\\mathbf{x}_i - '
                                '\\mathbf{x}_j\\|$$\n'
                                '2. **Nearest-Cluster Separation ($b(i)$)**:\n'
                                '   The mean distance between observation $i$ and all points in the **closest '
                                'neighboring cluster**:\n'
                                '   $$b(i) = \\min_{J \\ne I} \\left[ \\frac{1}{|C_J|} \\sum_{j \\in C_J} '
                                '\\|\\mathbf{x}_i - \\mathbf{x}_j\\| \\right]$$\n'
                                '3. **Silhouette Score ($s(i)$)**:\n'
                                '   $$s(i) = \\frac{b(i) - a(i)}{\\max(a(i), b(i))} \\in [-1, +1]$$\n'
                                '\n'
                                '#### Interpreting the Silhouette Value:\n'
                                '- **$s(i) \\approx +1$ (Strong Clustering)**: $a(i) \\ll b(i)$. The point is tightly '
                                'nestled inside its own cluster and far away from any other cluster.\n'
                                '- **$s(i) \\approx 0$ (Boundary Ambiguity)**: $a(i) \\approx b(i)$. The point sits '
                                'directly on the decision border between two clusters.\n'
                                '- **$s(i) < 0$ (Misassigned Point)**: $a(i) > b(i)$. The point is closer to the '
                                'neighboring cluster than to its own! It should be moved.\n'
                                '\n'
                                '#### Hand-Check from Whiteboard 1:\n'
                                'For Point $A(1, 1)$ in Cluster 1 $\\{A, B, C\\}$:\n'
                                '- Distance to $B(1, 2)$: $1.000$\n'
                                '- Distance to $C(2, 1)$: $1.000$\n'
                                '- Cohesion $a(A) = \\frac{1.0 + 1.0}{2} = \\mathbf{1.000}$\n'
                                '- Nearest Cluster is Cluster 2 $\\{D(5,4), E(5,5), F(6,5)\\}$:\n'
                                '  - Distance to $D$: $\\sqrt{4^2 + 3^2} = 5.000$\n'
                                '  - Distance to $E$: $\\sqrt{4^2 + 4^2} = \\sqrt{32} \\approx 5.657$\n'
                                '  - Distance to $F$: $\\sqrt{5^2 + 4^2} = \\sqrt{41} \\approx 6.403$\n'
                                '  - Separation $b(A) = \\frac{5.000 + 5.657 + 6.403}{3} = \\frac{17.060}{3} \\approx '
                                '\\mathbf{5.687}$\n'
                                '- Silhouette Coefficient:\n'
                                '  $$s(A) = \\frac{5.687 - 1.000}{\\max(1.000, 5.687)} = \\frac{4.687}{5.687} \\approx '
                                '\\mathbf{0.824}$$\n'
                                '  *(Matches the whiteboard lecture value $s(A) \\approx 0.82$ exactly!)*\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.4 Additional Validation Metrics: Davies-Bouldin & Calinski-Harabasz\n'
                                '\n'
                                'In automated machine learning pipelines where human engineers cannot visually inspect '
                                'elbow plots, two additional metrics provide programmatic cluster evaluation:\n'
                                '\n'
                                '#### 1. Davies-Bouldin Index (DBI):\n'
                                'Measures the average similarity between each cluster and its most similar peer:\n'
                                '$$R_{ij} = \\frac{s_i + s_j}{d(\\boldsymbol{\\mu}_i, \\boldsymbol{\\mu}_j)}$$\n'
                                'Where $s_i$ is the average distance of points in cluster $i$ to centroid '
                                '$\\boldsymbol{\\mu}_i$, and $d(\\boldsymbol{\\mu}_i, \\boldsymbol{\\mu}_j)$ is the '
                                'distance between centroids.\n'
                                '$$\\text{DBI} = \\frac{1}{K} \\sum_{i=1}^{K} \\max_{j \\ne i} R_{ij}$$\n'
                                '- **Lower DBI is better**: Indicates clusters that are internally tight ($s_i$ small) '
                                'and widely separated ($d(\\boldsymbol{\\mu}_i, \\boldsymbol{\\mu}_j)$ large).\n'
                                '\n'
                                '#### 2. Calinski-Harabasz Index (Variance Ratio Criterion):\n'
                                'The ratio of between-cluster dispersion to within-cluster dispersion:\n'
                                '$$\\text{CH} = \\frac{\\text{Tr}(\\mathbf{B}_K) / (K - 1)}{\\text{Tr}(\\mathbf{W}_K) '
                                '/ (n - K)}$$\n'
                                'Where $\\mathbf{B}_K$ is the between-cluster scatter matrix and $\\mathbf{W}_K$ is '
                                'the within-cluster scatter matrix.\n'
                                '- **Higher CH is better**: Reflects dense, well-separated clusters with fast $O(1)$ '
                                'computation time.',
                        'citations': [   'Arthur, D., & Vassilvitskii, S. (2007). k-means++: The advantages of careful '
                                         'seeding. SODA, 1027-1035.'],
                        'heading': '3. Inertia (WCSS) & The k-means++ Seeding Advantage',
                        'section_id': 'cml-l14-sec03'},
                    {   'body': '### 4.1 Hierarchical Agglomerative Clustering: The Bottom-Up Tree\n'
                                '\n'
                                'Unlike K-Means, which requires choosing $K$ upfront and flattens data into Voronoi '
                                'cells, **Hierarchical Agglomerative Clustering (HAC)** builds a rich, nested '
                                'hierarchy of clusters:\n'
                                '\n'
                                '```\n'
                                'The Agglomerative Algorithm:\n'
                                '  1. Start with n clusters (each data point is its own cluster of size 1).\n'
                                '  2. Compute pairwise distance matrix D between all clusters.\n'
                                '  3. Repeat until only 1 master cluster remains:\n'
                                '        a. Identify the two closest clusters (A, B) according to Linkage Criterion.\n'
                                '        b. Merge them into a single cluster (A U B).\n'
                                '        c. Record the merge height (distance) in the linkage matrix Z.\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.2 The Four Linkage Criteria\n'
                                '\n'
                                'How do we measure the distance between two clusters of points $A$ and $B$?\n'
                                '\n'
                                '```\n'
                                'Linkage Criteria Visualized:\n'
                                '   Single Linkage (Min)        Complete Linkage (Max)       Average Linkage (Mean)\n'
                                '      (Nearest pair)               (Farthest pair)             (All pairs mean)\n'
                                '     A           B                A           B               A           B\n'
                                '    (o)───────(o)                (o)                         (o)═══╤═══(o)\n'
                                '     │         │                  │           │                │   │   │\n'
                                '     │         │                  │           │                │   │   │\n'
                                '    (o)       (o)                 └──(o)─────(o)──┘           (o)═══╧═══(o)\n'
                                '```\n'
                                '\n'
                                '| Linkage Metric | Mathematical Definition | Geometric Behavior | Critical Failure '
                                'Mode |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **Single Linkage** | $d(A, B) = \\min_{u \\in A, v \\in B} \\|\\mathbf{u} - '
                                '\\mathbf{v}\\|$ | Connects closest points; can trace non-linear, curved manifolds '
                                '(moons, spirals). | **Chaining**: A single line of noise points bridges two distinct '
                                'clusters into one giant chain. |\n'
                                '| **Complete Linkage** | $d(A, B) = \\max_{u \\in A, v \\in B} \\|\\mathbf{u} - '
                                '\\mathbf{v}\\|$ | Considers the farthest points; enforces compact, equal-diameter '
                                'spherical clusters. | **Outlier Sensitivity**: A single extreme outlier violently '
                                'inflates merge height. |\n'
                                '| **Average Linkage (UPGMA)**| $d(A, B) = \\frac{1}{|A||B|}\\sum_{u \\in A}\\sum_{v '
                                '\\in B} \\|\\mathbf{u} - \\mathbf{v}\\|$ | Robust compromise between Single and '
                                'Complete; balances cluster variances. | Computationally slower ($O(n^2 \\log n)$). |\n'
                                "| **Ward's Linkage** | $\\Delta \\text{ESS} = "
                                '\\frac{|A||B|}{|A|+|B|}\\|\\boldsymbol{\\mu}_A - \\boldsymbol{\\mu}_B\\|^2$ | '
                                'Minimizes increase in total within-cluster variance; produces clean, balanced '
                                'clusters. | Assumes spherical, Gaussian-distributed clusters (like K-Means). |\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.3 Hand-Calculated Walkthrough: Whiteboard 2 (1D Points: 1, 2, 5, 7.5, 12)\n'
                                '\n'
                                'Let us trace agglomerative merges by hand on the 1D dataset from class whiteboard 2:\n'
                                'Five points on the real number line: $\\{1.0, 2.0, 5.0, 7.5, 12.0\\}$.\n'
                                '\n'
                                '#### Initial Pairwise Distances:\n'
                                '- $|1 - 2| = \\mathbf{1.0}$\n'
                                '- $|2 - 5| = 3.0$\n'
                                '- $|5 - 7.5| = 2.5$\n'
                                '- $|7.5 - 12| = 4.5$\n'
                                '\n'
                                '#### Step 1: Smallest Distance is between 1 and 2 ($d = 1.0$)\n'
                                '- Merge $\\{1\\}$ and $\\{2\\}$ into cluster $C_{12} = \\{1, 2\\}$.\n'
                                '- Merge Height = **$1.0$**.\n'
                                '- Remaining clusters: $\\{1, 2\\}, \\{5\\}, \\{7.5\\}, \\{12\\}$.\n'
                                '\n'
                                '#### Step 2: Compare Distances to $\\{5\\}$\n'
                                '- Single Linkage: $d(\\{1, 2\\}, \\{5\\}) = \\min(|1-5|, |2-5|) = |2-5| = 3.0$.\n'
                                '- Distance between $\\{5\\}$ and $\\{7.5\\}$ is $|5 - 7.5| = \\mathbf{2.5}$.\n'
                                '- Smallest distance is $2.5 \\implies$ Merge $\\{5\\}$ and $\\{7.5\\}$ into cluster '
                                '$C_{5,7.5} = \\{5, 7.5\\}$.\n'
                                '- Merge Height = **$2.5$**.\n'
                                '- Remaining clusters: $\\{1, 2\\}, \\{5, 7.5\\}, \\{12\\}$.\n'
                                '\n'
                                '#### Step 3: Compare Remaining Clusters\n'
                                '- Single Linkage between $C_{12}$ and $C_{5,7.5}$: $\\min(|2-5|) = \\mathbf{3.0}$.\n'
                                '- Distance between $C_{5,7.5}$ and $\\{12\\}$: $|7.5 - 12| = 4.5$.\n'
                                '- Smallest distance is $3.0 \\implies$ Merge $\\{1, 2\\}$ and $\\{5, 7.5\\}$.\n'
                                '- Merge Height = **$3.0$**.\n'
                                '- Remaining clusters: $\\{1, 2, 5, 7.5\\}$ and $\\{12\\}$.\n'
                                '\n'
                                '#### Step 4: Final Merge with Outlier $\\{12\\}$\n'
                                '- Merge Height = $|7.5 - 12| = \\mathbf{4.5}$.\n'
                                '\n'
                                '```\n'
                                'Dendrogram Structure for 1D Whiteboard Points:\n'
                                '    Height ^\n'
                                '       5.0 │                                   ┌────────── 12.0\n'
                                '           │               ┌───────────────────┴──────────┐\n'
                                '       4.0 │               │                              │\n'
                                '       3.0 │       ┌───────┴───────┐                      │\n'
                                '           │       │               │                      │  <-- CUT AT HEIGHT 4.0:\n'
                                '       2.0 │       │          ┌────┴────┐                 │      Yields 2 Clusters:\n'
                                '           │   ┌───┴───┐      │         │                 │      {1, 2, 5, 7.5} and '
                                '{12}\n'
                                '       1.0 │   │       │      │         │                 │\n'
                                '       0.0 ┴───┴───────┴──────┴─────────┴─────────────────┴► Points\n'
                                '              1.0     2.0    5.0       7.5               12.0\n'
                                '```\n'
                                '\n'
                                '> **Cutting the Dendrogram**:\n'
                                '> If we draw a horizontal cut line across the dendrogram at **Height = 4.0**:\n'
                                '> It crosses exactly **2 vertical branches**, yielding:\n'
                                '> - Cluster A: $\\{1.0, 2.0, 5.0, 7.5\\}$\n'
                                '> - Cluster B: $\\{12.0\\}$ (the isolated outlier!).\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.4 The Lance-Williams Recurrence Formula\n'
                                '\n'
                                'In 1967, Lance and Williams unified all hierarchical clustering algorithms into a '
                                'single generalized recurrence formula:\n'
                                'When two clusters $A$ and $B$ merge into $A \\cup B$, the distance from the new '
                                'merged cluster to any remaining cluster $C$ is computed in $O(1)$ time without '
                                'examining raw points:\n'
                                '\n'
                                '$$d(A \\cup B, C) = \\alpha_A d(A, C) + \\alpha_B d(B, C) + \\beta d(A, B) + \\gamma '
                                '|d(A, C) - d(B, C)|$$\n'
                                '\n'
                                '```\n'
                                'Lance-Williams Parameter Values:\n'
                                '┌─────────────────────┬──────────────────┬──────────────────┬──────────────────┬────────────────────────────────────┐\n'
                                '│ Linkage Method      │ α_A              │ α_B              │ β                │ '
                                'γ                                  │\n'
                                '├─────────────────────┼──────────────────┼──────────────────┼──────────────────┼────────────────────────────────────┤\n'
                                '│ **Single Linkage**  │ 1/2              │ 1/2              │ 0                │ '
                                '-1/2                               │\n'
                                '│ **Complete Linkage**│ 1/2              │ 1/2              │ 0                │ '
                                '+1/2                               │\n'
                                '│ **Average Linkage** │ |A| / (|A| + |B|)│ |B| / (|A| + |B|)│ 0                │ '
                                '0                                  │\n'
                                "│ **Ward's Linkage**  │ (|A|+|C|)/(|A|+|B|+|C|) │ (|B|+|C|)/(|A|+|B|+|C|) │ "
                                '-|C|/(|A|+|B|+|C|) │ 0                  │\n'
                                '└─────────────────────┴──────────────────┴──────────────────┴──────────────────┴────────────────────────────────────┘\n'
                                '```\n'
                                '\n'
                                'This brilliant formula allows SciPy and Scikit-Learn to build dendrograms in $O(n^2)$ '
                                'time instead of recomputing distances from scratch!',
                        'citations': [   'Rousseeuw, P. J. (1987). Silhouettes: a graphical aid to the interpretation '
                                         'and validation of cluster analysis. CAM, 20, 53-65.'],
                        'heading': '4. Selecting k: The Elbow Method, Silhouette Analysis & Failure Modes',
                        'section_id': 'cml-l14-sec04'},
                    {   'body': '### 5.1 Hands-On Python Implementation: End-to-End Customer Segmentation\n'
                                '\n'
                                'The following production script implements, tunes, and diagnoses customer '
                                'segmentation using both K-Means and Hierarchical Agglomerative Clustering on a mall '
                                'customer dataset:\n'
                                '\n'
                                '```python\n'
                                'import numpy as np\n'
                                'import pandas as pd\n'
                                'import matplotlib.pyplot as plt\n'
                                'from sklearn.preprocessing import StandardScaler\n'
                                'from sklearn.cluster import KMeans, AgglomerativeClustering\n'
                                'from sklearn.metrics import silhouette_score, silhouette_samples\n'
                                '\n'
                                '# 1. Synthesize Mall Customer Dataset (400 shoppers, 4 continuous features)\n'
                                'np.random.seed(42)\n'
                                'n_shoppers = 400\n'
                                '\n'
                                'age = np.random.normal(38, 12, n_shoppers).clip(18, 70)\n'
                                'annual_income_lakh = np.concatenate([\n'
                                '    np.random.normal(3.5, 0.8, 100),   # Low Income\n'
                                '    np.random.normal(7.5, 1.2, 200),   # Moderate Income\n'
                                '    np.random.normal(14.0, 2.0, 100)   # High Income\n'
                                ']).clip(1.5, 25.0)\n'
                                '\n'
                                'spending_score = np.concatenate([\n'
                                '    np.random.normal(25, 8, 120),      # Conservative Spenders\n'
                                '    np.random.normal(55, 10, 160),     # Moderate Spenders\n'
                                '    np.random.normal(85, 6, 120)       # VIP High Spenders\n'
                                ']).clip(1, 100)\n'
                                '\n'
                                'visits_per_month = np.random.poisson(4, n_shoppers).clip(1, 15)\n'
                                '\n'
                                'df = pd.DataFrame({\n'
                                '    "age": age,\n'
                                '    "annual_income_lakh": annual_income_lakh,\n'
                                '    "spending_score": spending_score,\n'
                                '    "visits_per_month": visits_per_month\n'
                                '})\n'
                                '\n'
                                '# 2. Strict Standardization (Mandatory for Euclidean Distance!)\n'
                                'scaler = StandardScaler()\n'
                                'X_scaled = scaler.fit_transform(df)\n'
                                '\n'
                                '# 3. Determine Optimal K via Elbow Method and Silhouette Analysis\n'
                                'k_range = range(2, 11)\n'
                                'inertias = []\n'
                                'sil_scores = []\n'
                                '\n'
                                'for k in k_range:\n'
                                '    km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)\n'
                                '    km.fit(X_scaled)\n'
                                '    inertias.append(km.inertia_)\n'
                                '    sil_scores.append(silhouette_score(X_scaled, km.labels_))\n'
                                '\n'
                                'best_k = k_range[np.argmax(sil_scores)]\n'
                                'print(f"Optimal K selected by Peak Silhouette Score: K = {best_k} (Score: '
                                '{max(sil_scores):.4f})")\n'
                                '\n'
                                '# 4. Fit Final K-Means Model\n'
                                'final_km = KMeans(n_clusters=best_k, init="k-means++", n_init=10, random_state=42)\n'
                                'df["Cluster_KM"] = final_km.fit_predict(X_scaled)\n'
                                '\n'
                                '# 5. Profile Customer Segments for Business Stakeholders\n'
                                'segment_profiles = df.groupby("Cluster_KM").mean().round(2)\n'
                                'segment_profiles["Shopper_Count"] = df["Cluster_KM"].value_counts()\n'
                                'print("\\n=== CUSTOMER SEGMENT PERSONAS ===")\n'
                                'print(segment_profiles)\n'
                                '\n'
                                '# 6. Fit Agglomerative Clustering with Ward Linkage for Validation\n'
                                'hac_ward = AgglomerativeClustering(n_clusters=best_k, linkage="ward")\n'
                                'df["Cluster_HAC"] = hac_ward.fit_predict(X_scaled)\n'
                                'print(f"\\nHAC (Ward) Silhouette Score: {silhouette_score(X_scaled, '
                                'df[\'Cluster_HAC\']):.4f}")\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.2 Diagnostic Failure Modes & Geometric Blind Spots\n'
                                '\n'
                                '| Geometric Blind Spot | Underlying Mechanism | Catastrophic Symptom | Recommended '
                                'Alternative Algorithm |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **Non-Convex Manifolds (Moons, Spirals, Rings)** | K-Means partitions space using '
                                'flat linear Voronoi hyperplanes. | Cuts concentric rings or interlocking moons in '
                                'half, assigning points across boundaries. | **DBSCAN** (density-based), '
                                '**Single-Linkage HAC**, or **Spectral Clustering**. |\n'
                                '| **Unequal Cluster Variances (Density Mismatch)** | K-Means objective $J$ minimizes '
                                'sum of squared Euclidean errors isotropically. | Splits large diffuse clusters into '
                                'artificial pieces; merges small dense clusters together. | **Gaussian Mixture Models '
                                '(GMM)** with unconstrained covariance matrices. |\n'
                                '| **Anisotropic (Elongated / Correlated) Clusters** | Euclidean distance implicitly '
                                'assumes spherical, uncorrelated clusters ($\\mathbf{\\Sigma} = \\mathbf{I}$). | '
                                'Misclassifies points along the principal axis of spread. | **GMM with Full '
                                'Covariance** or Mahalanobis distance whitening. |\n'
                                '| **Unscaled Physical Dimensions** | Large numerical features overwhelm smaller ones '
                                'in Euclidean squared sum. | Algorithm completely ignores vital demographic features '
                                '(e.g. Age). | Enforce `StandardScaler` inside an automated preprocessing pipeline. |\n'
                                '| **Extreme Outliers** | Squared distance $\\|\\mathbf{x} - \\boldsymbol{\\mu}\\|^2$ '
                                'penalizes distant anomalies severely. | A single extreme outlier drags a centroid far '
                                'away from real clusters, creating a useless 1-point cluster. | **K-Medoids (PAM)** or '
                                '**DBSCAN** (which flags outliers as noise label `-1`). |\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.3 Production Code: Plotting Per-Sample Silhouette Diagrams\n'
                                '\n'
                                'A single scalar average silhouette score can hide localized cluster collapse.\n'
                                'A **Silhouette Diagram** visualizes the distribution of silhouette values within each '
                                'cluster:\n'
                                '\n'
                                '```python\n'
                                '# Compute per-sample silhouette scores\n'
                                'sample_sil_values = silhouette_samples(X_scaled, df["Cluster_KM"])\n'
                                '\n'
                                'for cluster_id in range(best_k):\n'
                                '    cluster_scores = sample_sil_values[df["Cluster_KM"] == cluster_id]\n'
                                '    cluster_scores.sort()\n'
                                '    \n'
                                '    avg_score = cluster_scores.mean()\n'
                                '    negative_ratio = (cluster_scores < 0).mean()\n'
                                '    \n'
                                '    print(f"Cluster {cluster_id}: Count = {len(cluster_scores):3d} | "\n'
                                '          f"Avg Silhouette = {avg_score:.3f} | "\n'
                                '          f"Misclustered Points (< 0) = {negative_ratio * 100:.1f}%")\n'
                                '```\n'
                                '\n'
                                'If any cluster displays a wide band of negative silhouette scores ($s(i) < 0$), it '
                                'indicates that points in that cluster are closer to a neighboring cluster, signaling '
                                'that $K$ should be adjusted or that cluster shapes are non-spherical!',
                        'citations': [   'Ward, J. H. (1963). Hierarchical grouping to optimize an objective function. '
                                         'JASA, 58(301), 236-244.',
                                         'Müllner, D. (2011). Modern hierarchical, agglomerative clustering '
                                         'algorithms. arXiv:1109.2378.'],
                        'heading': '5. Hierarchical Agglomerative Clustering & Dendrograms',
                        'section_id': 'cml-l14-sec05'}],
    'subject_code': 'CML',
    'summary': 'An exhaustive, first-principles journey through Unsupervised Learning and Clustering. Explores why '
               "learning without labels requires internal geometrical validation, walks through Lloyd's K-Means "
               'algorithm and the mathematical proof of inertia convergence, solves the local minima trap with '
               'k-means++ initialization, and rigorously deconstructs the Elbow method and Silhouette coefficients. '
               'Unpacks Hierarchical Agglomerative Clustering, compares linkage metrics, decodes dendrograms, and '
               'demonstrates production customer segmentation in Scikit-Learn.',
    'tags': [   'Unsupervised Learning',
                'Clustering',
                'K-Means',
                'Inertia',
                'WCSS',
                'k-means++',
                'Elbow Method',
                'Silhouette Score',
                'Hierarchical Clustering',
                'Agglomerative Clustering',
                'Dendrogram',
                'Linkage Criteria',
                'Customer Segmentation'],
    'term': 'Term 5',
    'topic_title': '14. Unsupervised Learning: K-Means Clustering & Hierarchical Clustering'}

