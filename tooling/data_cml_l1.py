"""
Data definition for data_cml_l1:
"""

L1_DATA = {   'approval_status': 'approved',
    'key_takeaways': [   'Classical programming maps Inputs + Handcrafted Rules -> Outputs, whereas Machine Learning '
                         'maps Inputs + Examples -> Learned Mapping.',
                         'If a problem can be solved reliably with 10–20 deterministic if/else rules, stick to '
                         'classical software engineering; use ML when the pattern is too complex, perceptual, or noisy '
                         'to hand-code.',
                         "Every well-defined ML project must explicitly anchor Tom Mitchell's triplet: Task T (what to "
                         'do), Experience E (training data), and Performance P (how success is scored).',
                         'Classification predicts discrete categories (even if outputting probabilities); Regression '
                         'predicts continuous numbers. The boundary is governed strictly by the target space Y, not '
                         'the input features X.',
                         'Supervised learning learns a mapping X -> Y using ground-truth targets; Unsupervised '
                         'learning discovers emergent geometry/clusters in X without targets.',
                         'Histograms bin continuous values to show distribution shape and modality (unimodal vs. '
                         'bimodal); scatter plots inspect bivariate relationships; bar charts compare discrete '
                         'categories.'],
    'last_updated': '2026-10-18T00:00:00Z',
    'learning_objectives': [   'Understand why and when to transition from rule-based classical software engineering '
                               'to machine learning.',
                               "Formulate any machine learning problem using Tom Mitchell's "
                               'Task-Experience-Performance (T-E-P) framework.',
                               'Select the right exploratory data visualization tool (Histogram, Scatter, Bar, Line) '
                               'based on data types and analytical questions.',
                               'Differentiate classification and regression tasks based on the mathematical nature of '
                               'the target variable.',
                               'Distinguish supervised learning from unsupervised structure discovery (clustering) and '
                               'know when to apply each.'],
    'note_id': 'cml-t5-l01',
    'quiz': {   'questions': [   {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'A Histogram is specifically designed to partition continuous '
                                                    'numeric variables (like student marks) into contiguous bins to '
                                                    'visualize frequency density, modality (unimodal vs. bimodal), and '
                                                    'skewness. A bar plot treats each unique value as a separate '
                                                    'category, a scatter plot requires two variables, and a line plot '
                                                    'implies sequential/ordered time series.',
                                     'id': 'q-cml-l01-01',
                                     'options': [   {'id': 'opt-1', 'is_correct': False, 'text': 'Bar Plot'},
                                                    {'id': 'opt-2', 'is_correct': True, 'text': 'Histogram'},
                                                    {'id': 'opt-3', 'is_correct': False, 'text': 'Scatter Plot'},
                                                    {'id': 'opt-4', 'is_correct': False, 'text': 'Line Plot'}],
                                     'question': "You want to display the distribution of students' scores in a class "
                                                 'to see whether the marks are clustered around 70 or split into two '
                                                 'groups. Which plot is best suited for this task?',
                                     'subtopic': 'Exploratory Data Visualization',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-3'],
                                     'difficulty': 'easy',
                                     'explanation': "Arthur Samuel's classic definition states that Machine Learning "
                                                    'gives computers the ability to learn without being explicitly '
                                                    'programmed. Option 1 is false because ML also includes '
                                                    'unsupervised and reinforcement learning. Option 2 restricts ML '
                                                    'only to robotics, and Option 4 describes classical software '
                                                    'engineering.',
                                     'id': 'q-cml-l01-02',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Machine learning learns exclusively from labelled '
                                                                'data.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Machine learning is the field of giving physical '
                                                                'robots the ability to act intelligently.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'Machine learning enables computers to learn and '
                                                                'improve from data without being explicitly '
                                                                'programmed.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Machine learning is the science of writing '
                                                                'deterministic rule-based algorithms.'}],
                                     'question': 'Which of the following provides the best foundational explanation of '
                                                 'Machine Learning?',
                                     'subtopic': 'Machine Learning Definition',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'Regression models predict continuous numeric outputs (such as '
                                                    'prices, temperatures, or revenues), where the target variable '
                                                    'belongs to the set of real numbers y in R. Option 1 describes '
                                                    'classification, Option 3 describes clustering, and Option 4 '
                                                    'describes dimensionality reduction.',
                                     'id': 'q-cml-l01-03',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'To classify data into distinct discrete categories.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'To predict a continuous outcome or real-valued '
                                                                'numerical quantity.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'To perform clustering on an unlabelled dataset.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'To visualize high-dimensional data in 2D space.'}],
                                     'question': 'What is the main purpose of regression analysis in machine learning?',
                                     'subtopic': 'Regression vs Classification',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-4'],
                                     'difficulty': 'easy',
                                     'explanation': 'All three statements are true: (1) classification maps inputs to '
                                                    'discrete category outputs, (2) models frequently output '
                                                    'continuous probabilities P(Y=k|X) to quantify prediction '
                                                    'confidence before thresholding, and (3) classification algorithms '
                                                    'can ingest continuous, discrete, or mixed input features.',
                                     'id': 'q-cml-l01-04',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Classification can be defined as a predictive model '
                                                                'mapping inputs to discrete outputs.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Class label probabilities enable classification '
                                                                'algorithms to quantify confidence before making '
                                                                'discrete decisions.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'A classification algorithm can accept both discrete '
                                                                'and real-valued continuous input features.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': True,
                                                        'text': 'All of the options are true.'}],
                                     'question': 'Which of the following statements is/are true regarding '
                                                 'classification in machine learning?',
                                     'subtopic': 'Classification Properties',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-3'],
                                     'difficulty': 'easy',
                                     'explanation': 'The target to be predicted is property price, which is a '
                                                    'continuous numeric quantity (in currency units). Because '
                                                    'historical sales data with known prices is available, this is a '
                                                    'supervised regression problem.',
                                     'id': 'q-cml-l01-05',
                                     'options': [   {'id': 'opt-1', 'is_correct': False, 'text': 'Classification'},
                                                    {'id': 'opt-2', 'is_correct': False, 'text': 'Clustering'},
                                                    {'id': 'opt-3', 'is_correct': True, 'text': 'Regression'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Dimensionality Reduction'}],
                                     'question': 'A real estate property dealer has a dataset consisting of features '
                                                 'like square footage, bedrooms, locality, and past sale prices. A '
                                                 'customer asks the dealer to estimate the market price of a property '
                                                 'with 3 bedrooms in that neighborhood. Which machine learning '
                                                 'technique should be used?',
                                     'subtopic': 'Problem Formulation Scenario',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'Because there are no pre-existing ground-truth topic labels '
                                                    'attached to the comments during training, the algorithm must '
                                                    'discover natural clusters and semantic groupings in the text on '
                                                    'its own. This is an unsupervised learning task.',
                                     'id': 'q-cml-l01-06',
                                     'options': [   {'id': 'opt-1', 'is_correct': False, 'text': 'Supervised learning'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Unsupervised learning'}],
                                     'question': 'You have a dataset of 50,000 raw customer feedback comments. No '
                                                 'tags, labels, or predefined categories have been assigned. You want '
                                                 "to group them into emerging topics such as 'Delivery Speed', "
                                                 "'Product Quality', and 'Billing'. Is this a supervised or "
                                                 'unsupervised learning problem?',
                                     'subtopic': 'Supervised vs Unsupervised',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'easy',
                                     'explanation': 'Historical stock market records provide both the input indicators '
                                                    'X and the true historical closing prices Y. Because the model is '
                                                    'trained with explicit target answers, it is a supervised learning '
                                                    'task (specifically, time-series regression).',
                                     'id': 'q-cml-l01-07',
                                     'options': [   {'id': 'opt-1', 'is_correct': True, 'text': 'Supervised learning'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Unsupervised learning'}],
                                     'question': "You are building a system to forecast tomorrow's closing stock price "
                                                 'based on historical market prices, trading volume, and interest '
                                                 'rates. Is this a supervised or unsupervised learning problem?',
                                     'subtopic': 'Supervised vs Unsupervised',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'easy',
                                     'explanation': 'Because the company already has pre-defined, labeled categories '
                                                    "('Direct Interview', 'Hold', 'Reject'), the correct approach is "
                                                    'supervised classification. An unsupervised clustering algorithm '
                                                    'would group resumes by formatting, length, or random keywords, '
                                                    "which would not align with the company's established decision "
                                                    'criteria.',
                                     'id': 'q-cml-l01-08',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'An unsupervised machine learning system that clusters '
                                                                'together similar candidate resumes.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'A supervised machine learning system trained on '
                                                                'historical applicant data with existing decision '
                                                                'labels.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'You should not recommend any machine learning system '
                                                                'because resumes cannot be analyzed mathematically.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'A reinforcement learning system where candidates play '
                                                                'a video game.'}],
                                     'question': 'Your human resources department asks you to create a system that '
                                                 'will automatically triage new job applicants into three existing, '
                                                 "well-defined corporate bands: 'Direct Interview', 'Hold for Review', "
                                                 "and 'Reject'. What type of system should you recommend?",
                                     'subtopic': 'Clustering vs Classification',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'A scatter plot is the primary diagnostic tool for inspecting '
                                                    'bivariate relationships between two continuous variables (square '
                                                    'footage and electricity consumption). It reveals whether the '
                                                    'relationship is linear, non-linear, heteroscedastic, or '
                                                    'clustered.',
                                     'id': 'q-cml-l01-09',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'A line plot connecting observations sorted '
                                                                'alphabetically by city name.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'A scatter plot mapping square footage on the x-axis '
                                                                'and electricity consumption on the y-axis.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'A single pie chart displaying total electricity '
                                                                'consumption across all apartments.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'A histogram binning the square footage alone.'}],
                                     'question': 'An analyst wants to investigate whether an increase in apartment '
                                                 'square footage is associated with higher monthly electricity '
                                                 'consumption. Which visualization tool is most effective?',
                                     'subtopic': 'Exploratory Data Visualization',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'Summary statistics like mean and median collapse distribution '
                                                    'geometry into single scalars. A bimodal distribution with two '
                                                    'separate sub-cohorts (e.g. entry-level staff and executives) can '
                                                    'easily yield a mean of 70,000 USD, completely masking the '
                                                    'bifurcation unless a histogram or KDE is plotted.',
                                     'id': 'q-cml-l01-10',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Mean and median are only valid for categorical string '
                                                                'variables.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'A bimodal distribution with two distinct salary peaks '
                                                                '(e.g. at 35,000 USD and 105,000 USD) can produce a '
                                                                'mean and median of ~70,000 while having virtually no '
                                                                'employees earning 70,000 USD.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The median is mathematically sensitive to extreme '
                                                                'outliers, distorting the center.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'A bell curve requires the mean to be strictly greater '
                                                                'than twice the median.'}],
                                     'question': 'A dataset of employee salaries has a mean of 70,000 USD and a median '
                                                 'of 68,000 USD. Why is calculating only the mean and median '
                                                 'insufficient to conclude that salaries follow a standard bell-shaped '
                                                 'bell curve?',
                                     'subtopic': 'Statistical Diagnostics',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'Under concept drift, rule-based systems accumulate technical debt '
                                                    'as developers write increasingly tangled, fragile manual rules. '
                                                    'An ML architecture addresses drift systematically by refreshing '
                                                    'the training experience E with recent data and updating the '
                                                    'learned parameters.',
                                     'id': 'q-cml-l01-11',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Classical SDE systems adapt automatically without '
                                                                'developer intervention, whereas ML models require '
                                                                'complete code rewrites.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Classical SDE requires engineers to manually write '
                                                                'and patch new conditional rules; an MLE pipeline '
                                                                'adapts by retraining model weights on recent labeled '
                                                                'transaction data.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'SDE systems retrain their database schemas, whereas '
                                                                'MLE systems rely exclusively on hardware upgrades.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Neither system can adapt to concept drift; both must '
                                                                'be permanently discarded.'}],
                                     'question': 'In a production fraud detection system, fraudulent transaction '
                                                 'patterns evolve as fraudsters discover new circumvention techniques. '
                                                 'How do SDE and MLE approaches fundamentally differ when adapting to '
                                                 'this distribution shift (concept drift)?',
                                     'subtopic': 'SDE vs MLE Lifecycle',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'Task T is the operational duty performed (deciding to brake), '
                                                    'Experience E is the empirical data consumed (driving logs and '
                                                    'sensor telemetry), and Performance P is the metric evaluating '
                                                    'operational success (collision avoidance rate and false alarm '
                                                    'rate).',
                                     'id': 'q-cml-l01-12',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'T: Sensor data logs; E: Braking decision; P: Camera '
                                                                'resolution.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'T: Deciding whether to trigger the emergency brake; '
                                                                'E: Historical telemetry and driving logs; P: '
                                                                'Collision avoidance rate and false alarm rate.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'T: Python compiler; E: Accuracy metric; P: Speed of '
                                                                'the car in km/h.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'T: Minimizing Mean Squared Error; E: Testing dataset; '
                                                                'P: Operating system version.'}],
                                     'question': 'An automotive engineering team develops an autonomous emergency '
                                                 "braking system. How is this system formalized within Tom Mitchell's "
                                                 'ETP framework?',
                                     'subtopic': 'Tom Mitchell ETP',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-3'],
                                     'difficulty': 'medium',
                                     'explanation': 'Historical watch logs, ratings, and user interactions constitute '
                                                    'the empirical data (Experience E) from which the algorithm learns '
                                                    'user preference patterns. Option 1 is Task T, and Option 2 is '
                                                    'Performance P.',
                                     'id': 'q-cml-l01-13',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': "The list of 5 movies displayed on the user's home "
                                                                'screen.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'The Mean Reciprocal Rank (MRR) of clicked '
                                                                'recommendations.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'Historical user watch histories, ratings, and '
                                                                'click-through interactions.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The neural network architecture running on GPU '
                                                                'servers.'}],
                                     'question': "Consider a video streaming platform's recommendation engine. Which "
                                                 "component represents the Experience (E) in Mitchell's framework?",
                                     'subtopic': 'Tom Mitchell ETP',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'Probabilities p in [0, 1] serve as intermediate statistical '
                                                    'confidence scores. The ultimate operational goal is to assign the '
                                                    'patient to a discrete clinical state (Diabetic / Non-Diabetic) by '
                                                    'applying a decision threshold tau. The target variable Y is '
                                                    'fundamentally discrete.',
                                     'id': 'q-cml-l01-14',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'It is actually regression, and categorizing it as '
                                                                'classification is an industry misconception.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'The operational objective is to assign a discrete '
                                                                'diagnosis (Diabetic vs. Non-Diabetic) via a decision '
                                                                'threshold; probabilities are intermediate confidence '
                                                                'scores.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Because all medical algorithms are legally prohibited '
                                                                'from using regression.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Because any model that outputs numbers between 0 and '
                                                                '1 is classified as unsupervised clustering.'}],
                                     'question': 'A medical diagnostic model outputs a continuous value p = 0.82 '
                                                 'representing the estimated probability that a patient has Diabetes. '
                                                 'Why is this model categorized as Classification rather than '
                                                 'Regression?',
                                     'subtopic': 'Classification Probabilities',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'medium',
                                     'explanation': 'The classification vs. regression divide is determined strictly '
                                                    'by the target space Y (the output). The input feature matrix X '
                                                    'can contain any combination of continuous, discrete integer, and '
                                                    'encoded categorical variables.',
                                     'id': 'q-cml-l01-15',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'No, regression models can strictly accept only '
                                                                'continuous floating-point features.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Yes, regression algorithms can ingest continuous, '
                                                                'discrete, and encoded categorical inputs; the '
                                                                'regression designation is governed strictly by the '
                                                                'continuous nature of the target Y.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Only if the categorical variable has exactly two '
                                                                'unique categories.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'No, including categorical inputs automatically '
                                                                'converts any model into a classification model.'}],
                                     'question': 'Can a regression model take categorical or discrete variables (such '
                                                 "as 'Neighborhood Name' or 'Number of Bedrooms') as input features?",
                                     'subtopic': 'Feature Spaces in Regression',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1'],
                                     'difficulty': 'medium',
                                     'explanation': 'Unsupervised clustering algorithms discover emergent geometric '
                                                    'density groupings based on distance metrics (e.g. Euclidean '
                                                    'distance). They have no semantic knowledge of real-world business '
                                                    'meanings. A human domain expert must inspect the characteristics '
                                                    'of each cluster to assign meaningful business labels.',
                                     'id': 'q-cml-l01-16',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'K-Means operates purely on geometric distance in '
                                                                'feature space and has no semantic awareness of '
                                                                'business risk definitions.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'K-Means is only capable of generating numerical '
                                                                'outputs, not alphabetical text.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Because clustering algorithms require at least 100 '
                                                                'clusters to produce semantic names.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'K-Means requires labeled target data to partition '
                                                                'feature space.'}],
                                     'question': 'A bank runs K-Means clustering (k = 3) on customer transaction '
                                                 'records. Why can K-Means NOT automatically label the clusters as '
                                                 "'High Risk', 'Medium Risk', and 'Low Risk'?",
                                     'subtopic': 'Clustering Limitations',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-3'],
                                     'difficulty': 'hard',
                                     'explanation': 'The tax code consists of deterministic, static, fully known '
                                                    'mathematical rules where legal compliance demands 100% exactness '
                                                    'and zero statistical error. An ML model would introduce '
                                                    'statistical approximation and potential prediction errors into a '
                                                    'strictly rule-based financial process.',
                                     'id': 'q-cml-l01-17',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Train a Deep Neural Network on 100,000 synthetic '
                                                                'paychecks.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'Train an XGBoost regression model with hyperparameter '
                                                                'tuning.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'Write a deterministic classical software engineering '
                                                                'module (if/else statements) based directly on the tax '
                                                                'statutes.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Deploy K-Means clustering to discover tax tiers from '
                                                                'employee bank statements.'}],
                                     'question': 'A fintech company needs to build a payroll tax calculation module '
                                                 "based on the government's official tax code (containing 5 income "
                                                 'brackets and 3 deduction rules). Which architectural approach should '
                                                 'the engineering team adopt?',
                                     'subtopic': 'Engineering Decision Framework',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1', 'opt-2', 'opt-4'],
                                     'difficulty': 'hard',
                                     'explanation': 'Options 1, 2, and 4 are valid task-metric pairings. Option 3 is '
                                                    'incorrect: sepsis diagnosis is a discrete classification task and '
                                                    'should be evaluated using classification metrics (e.g. '
                                                    'Sensitivity, Specificity, F1), not regression metrics like MSE.',
                                     'id': 'q-cml-l01-18',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'Credit Card Fraud Detection (Binary Classification) '
                                                                'evaluated using F1-score and Precision-Recall AUC.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Residential House Price Prediction (Regression) '
                                                                'evaluated using Root Mean Squared Error (RMSE).'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Hospital Sepsis Diagnosis (Classification) evaluated '
                                                                'using Mean Squared Error (MSE).'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': True,
                                                        'text': 'Customer Churn Prediction (Binary Classification) '
                                                                'evaluated using Area Under the ROC Curve (ROC-AUC).'}],
                                     'question': 'Which of the following correctly pair a Machine Learning Task with '
                                                 'an appropriate, mathematically valid Performance Measure (P)?',
                                     'subtopic': 'Metric Alignment',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-1', 'opt-2', 'opt-4'],
                                     'difficulty': 'hard',
                                     'explanation': 'Options 1, 2, and 4 are foundational invariants. Option 3 is '
                                                    'false: clustering algorithms cannot be evaluated using Accuracy '
                                                    'because there are no ground-truth target labels to compare '
                                                    'against.',
                                     'id': 'q-cml-l01-19',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'Supervised learning requires ground-truth target '
                                                                'pairs (x_i, y_i) during training to compute loss '
                                                                'gradients or parameter updates.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Unsupervised learning algorithms operate exclusively '
                                                                'on feature matrix X without access to target vector y '
                                                                'during model fitting.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Unsupervised clustering algorithms can be objectively '
                                                                'evaluated using test-set Accuracy.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': True,
                                                        'text': 'Supervised learning models can be evaluated by '
                                                                'directly comparing predicted targets y_hat against '
                                                                'ground-truth labels y on unseen data.'}],
                                     'question': 'Which of the following statements represent fundamental invariants '
                                                 'of Supervised vs. Unsupervised learning?',
                                     'subtopic': 'Paradigms Invariants',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'hard',
                                     'explanation': 'In machine learning, model weights are optimized on historical '
                                                    'experience E. If real-world phenomena shift (e.g. consumer '
                                                    'trends, inflation, seasonal patterns), the historical E no longer '
                                                    'represents current reality, leading to degradation in operational '
                                                    'performance P.',
                                     'id': 'q-cml-l01-20',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'The computer program has forgotten its Task T.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'The production environment data distribution has '
                                                                'shifted, making historical Experience E misaligned '
                                                                'with real-time operational data (concept drift).'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'The performance metric P automatically decays after '
                                                                '90 days of server uptime.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'The model has converted from supervised learning into '
                                                                'unsupervised learning.'}],
                                     'question': 'A production machine learning model exhibits degrading Performance '
                                                 "(P) over time despite no changes being made to the model's source "
                                                 "code. In the context of Tom Mitchell's framework, what is the "
                                                 'primary cause?',
                                     'subtopic': 'Tom Mitchell ETP',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'hard',
                                     'explanation': 'When an instance can simultaneously possess multiple active '
                                                    'labels, it is a Multi-label classification problem. Multi-class '
                                                    'classification assumes mutually exclusive classes where '
                                                    'probabilities sum to 1 via Softmax. In multi-label '
                                                    'classification, each label is treated as an independent binary '
                                                    'classification problem using independent Sigmoid functions.',
                                     'id': 'q-cml-l01-21',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Multi-class classification with a Softmax output '
                                                                'layer that forces the sum of class probabilities to '
                                                                '1.0.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Multi-label classification where each pathology is '
                                                                'modeled as an independent binary target using Sigmoid '
                                                                'activations.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Unsupervised K-Means clustering with k = 3.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Continuous Multivariate Ordinary Least Squares '
                                                                'Regression.'}],
                                     'question': "An imaging system analyzes medical chest X-rays. A single patient's "
                                                 "scan can simultaneously show 'Atelectasis', 'Effusion', and "
                                                 "'Infiltration'. How is this machine learning task mathematically "
                                                 'structured?',
                                     'subtopic': 'Multi-Class vs Multi-Label',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'hard',
                                     'explanation': 'Semi-supervised learning combines a small amount of labeled data '
                                                    'with a large amount of unlabelled data during training. The '
                                                    'unlabelled data helps the model understand the underlying '
                                                    'geometry and distribution of the input space X, boosting '
                                                    'generalization.',
                                     'id': 'q-cml-l01-22',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Reinforcement Learning with human feedback.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Semi-Supervised Learning.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Pure Unsupervised Clustering with k = 1000.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Classical deterministic rule-based programming.'}],
                                     'question': 'An AI team has 1,000,000 customer support chat logs, but only 1,000 '
                                                 'of them have been manually tagged by human agents with resolution '
                                                 'categories. Which paradigm best describes utilizing the 999,000 '
                                                 'unlabelled logs to improve the classifier trained on the 1,000 '
                                                 'labeled logs?',
                                     'subtopic': 'Learning Paradigms',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-3'],
                                     'difficulty': 'hard',
                                     'explanation': 'Unlike supervised learning (which receives instructive '
                                                    'ground-truth answers y for each input x), Reinforcement Learning '
                                                    'receives delayed evaluative scalar feedback (rewards/penalties) '
                                                    "through active trial-and-error. Crucially, the agent's actions "
                                                    "dynamically influence the environment's future states.",
                                     'id': 'q-cml-l01-23',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'RL does not use any mathematical optimization or loss '
                                                                'criteria.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': False,
                                                        'text': 'RL receives instantaneous ground-truth correct '
                                                                'actions from a supervisory oracle for every '
                                                                'observation.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'RL learns from delayed evaluative scalar rewards '
                                                                'through active trial-and-error environment '
                                                                'interaction, where current decisions alter future '
                                                                'states.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'RL operates strictly on static tabular CSV files '
                                                                'without sequential time steps.'}],
                                     'question': 'How does Reinforcement Learning (RL) fundamentally differ from '
                                                 'Supervised Learning in terms of its feedback mechanism?',
                                     'subtopic': 'Reinforcement Learning',
                                     'type': 'single_choice'},
                                 {   'correctOptionIds': ['opt-1', 'opt-2', 'opt-3'],
                                     'difficulty': 'hard',
                                     'explanation': 'Options 1, 2, and 3 are standard, optimal visual diagnostics. '
                                                    'Option 4 is poor practice: a line plot connects sequential points '
                                                    'with lines, falsely implying an ordered or continuous '
                                                    'relationship between categorical blood types.',
                                     'id': 'q-cml-l01-24',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': True,
                                                        'text': 'Using a Histogram to evaluate whether feature values '
                                                                'are normally distributed, skewed, or zero-inflated.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Using a Bar Plot to compare transaction volumes '
                                                                'across 5 different payment methods (Credit, Debit, '
                                                                'UPI, NetBanking, Cash).'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': True,
                                                        'text': 'Using a Scatter Plot to inspect potential non-linear '
                                                                'relationships and heteroscedasticity between house '
                                                                'age and sale price.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Using a Line Plot to display unordered categorical '
                                                                'blood types (A, B, AB, O).'}],
                                     'question': 'Which of the following chart selections represent optimal, standard '
                                                 'exploratory data analysis practices?',
                                     'subtopic': 'Exploratory Data Visualization',
                                     'type': 'multiple_choice'},
                                 {   'correctOptionIds': ['opt-2'],
                                     'difficulty': 'hard',
                                     'explanation': 'Perceptual data (images, audio, natural language) exhibits '
                                                    'immense high-dimensional variation. A 100x100 pixel image '
                                                    "contains 30,000 color values. Describing the concept of a 'cat' "
                                                    'using deterministic if/else rules over 30,000 dimensions '
                                                    'collapses under combinatorial explosion, making statistical '
                                                    'pattern recognition from empirical data essential.',
                                     'id': 'q-cml-l01-25',
                                     'options': [   {   'id': 'opt-1',
                                                        'is_correct': False,
                                                        'text': 'Computers before the year 2010 were unable to process '
                                                                'color pixels.'},
                                                    {   'id': 'opt-2',
                                                        'is_correct': True,
                                                        'text': 'Combinatorial explosion: variations in lighting, '
                                                                'pose, deformation, occlusion, and background make it '
                                                                'impossible for human engineers to explicitly write '
                                                                'deterministic rules for pixel arrays.'},
                                                    {   'id': 'opt-3',
                                                        'is_correct': False,
                                                        'text': 'Cat images violate the laws of Euclidean geometry.'},
                                                    {   'id': 'opt-4',
                                                        'is_correct': False,
                                                        'text': 'Classical programming can only process numbers, '
                                                                'whereas digital images are not composed of numbers.'}],
                                     'question': 'Why did classical rule-based computer vision systems (e.g. '
                                                 'hand-crafting edge filters and geometric rules to recognize cats) '
                                                 'fail, necessitating machine learning?',
                                     'subtopic': 'Pattern Recognition Foundation',
                                     'type': 'single_choice'}]},
    'schema_version': 1,
    'sections': [   {   'body': '### 1.1 Why We Need a Solid Base Layer\n'
                                '\n'
                                'Before an algorithm can learn from data, we must first be able to **see**, '
                                '**manipulate**, and **model** that data. In modern data science and classical machine '
                                'learning, we rely on a shared ecosystem of tools:\n'
                                '\n'
                                '| Area | Industry Tools | Core Purpose in Machine Learning |\n'
                                '| :--- | :--- | :--- |\n'
                                '| **Numerics & Arrays** | **NumPy** | High-performance vector/matrix math, '
                                'broadcasting, and linear algebra operations. |\n'
                                '| **Data Tables** | **Pandas** | Tabular data wrangling, cleaning, missing value '
                                'handling, joins, and aggregations. |\n'
                                '| **Visual Diagnostics** | **Matplotlib & Seaborn** | Inspecting empirical '
                                'distributions, relationships, correlations, and anomalies. |\n'
                                '| **Probability & Statistics** | Statistical primitives | Quantifying uncertainty, '
                                'expected value, variance, and confidence intervals. |\n'
                                '| **Linear Algebra** | Vectors & Matrices | Geometric coordinate space for features, '
                                'decision boundaries, and loss surfaces. |\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.2 The Data Visualization Cheat Sheet: Choosing the Right Chart\n'
                                '\n'
                                'One of the most frequent beginner mistakes is picking the wrong chart for the '
                                'question being asked. Visualizations are diagnostic tools. Choosing the wrong plot '
                                'can completely obscure data patterns or lead to false conclusions.\n'
                                '\n'
                                '```\n'
                                'Visual Diagnostic Flowchart:\n'
                                '   What do you want to explore?\n'
                                '     │\n'
                                '     ├── Continuous Variable Distribution / Shape ───────► HISTOGRAM (or KDE)\n'
                                '     ├── Discrete Category Frequencies / Totals ──────────► BAR PLOT\n'
                                '     ├── Association Between Two Continuous Variables ───► SCATTER PLOT\n'
                                '     └── Progression Over Time / Ordered Index ──────────► LINE PLOT\n'
                                '```\n'
                                '\n'
                                '#### Detailed Diagnostic Matrix\n'
                                '\n'
                                '| Analytical Objective | Recommended Chart | Why It Works | What Happens If You Use '
                                'the Wrong Chart |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **Shape & Modality of a Single Continuous Variable** | **Histogram** (or KDE) | '
                                'Partitions values into contiguous numeric bins and displays frequency counts. '
                                'Instantly reveals skewness, outliers, and whether data is unimodal (one peak) or '
                                'bimodal (two separate clusters). | A **scatter plot** cannot aggregate density along '
                                'a single axis; a **bar plot** treats every distinct floating-point number as an '
                                'isolated category, creating an unreadable mess. |\n'
                                '| **Comparing Discrete Categories** | **Bar Plot** | Displays discrete category names '
                                'on one axis and aggregate values (counts, sums, averages) on the other. | A '
                                '**histogram** fails because categories have no natural continuous bin boundaries. |\n'
                                '| **Relationship Between Two Continuous Variables** | **Scatter Plot** | Maps each '
                                'observation $(x_i, y_i)$ as a point in a 2D Cartesian plane. Reveals linear, '
                                'non-linear, or clustering associations. | A **line plot** artificially connects '
                                'points with lines, falsely implying sequential order or time continuity. |\n'
                                '| **Trend Over an Ordered Axis (Time, Steps)** | **Line Plot** | Connects sequential '
                                'observations chronologically to display trajectories, trends, seasonality, and '
                                'cycles. | A **scatter plot** shows points but makes it hard for the human eye to '
                                'track chronological direction. |\n'
                                '\n'
                                '> **The Exam Scores Scenario (Class Intuition)**:\n'
                                '> Imagine you are given the exam scores of 200 students. You need to answer: *"Are '
                                'most students clustered around 70 marks, or is the class split into two distinct '
                                'groups—struggling students at 45 and top performers at 90 (bimodal)?"*\n'
                                '> \n'
                                '> - A **Histogram** answers this immediately: by grouping continuous marks into bins '
                                '(e.g., 40-50, 50-60, 60-70), two separate peaks will visually jump out.\n'
                                '> - A simple **mean** or **median** would completely hide this reality by averaging '
                                'out to ~68, giving the false illusion of a single average class!\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.3 Intuition of Vectors, Matrices, and Uncertainty\n'
                                '\n'
                                'In classical machine learning:\n'
                                '1. **Each row** of your table is an observation: a vector $\\mathbf{x} = [x_1, x_2, '
                                '\\dots, x_d]^T$ representing a point in $d$-dimensional feature space.\n'
                                '2. **Each column** is a feature: a geometric dimension (e.g., square footage, age, '
                                'income).\n'
                                '3. **Dot products** measure geometric alignment and similarity: $\\mathbf{w}^T '
                                '\\mathbf{x} = \\sum_{j=1}^d w_j x_j$. When a linear model computes a score, it is '
                                'projecting the feature vector onto a weight vector.\n'
                                '4. **Probability** is the mathematical language of uncertainty: since empirical data '
                                'contains noise, our predictions represent conditional expectations $\\mathbb{E}[Y '
                                '\\mid X]$ or posterior probabilities $P(Y=k \\mid X)$ rather than absolute '
                                'certainties.',
                        'citations': [   'Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley.',
                                         'Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer, '
                                         'Chapter 1.',
                                         'Strang, G. (2016). Introduction to Linear Algebra (5th ed.). '
                                         'Wellesley-Cambridge Press.'],
                        'heading': '1. The DSML Base Layer: Exploratory Data Visualization & Mathematical Foundations',
                        'section_id': 'cml-l01-sec01'},
                    {   'body': '### 2.1 Where Does the Logic Come From?\n'
                                '\n'
                                'The defining difference between classical software engineering and machine learning '
                                'is **who writes the rules**:\n'
                                '\n'
                                '```\n'
                                'Classical Software Engineering (SDE):\n'
                                '   [ Data / Inputs ] ─────────┐\n'
                                '                              ├───► [ Handcrafted Rules / if-else Logic ] ───► [ '
                                'Outputs / Decisions ]\n'
                                '   [ Human-Written Rules ] ───┘\n'
                                '\n'
                                'Machine Learning Engineering (MLE):\n'
                                '   [ Data / Inputs ] ─────────┐\n'
                                '                              ├───► [ Learning Algorithm / Optimizer ] ──────► [ '
                                'Learned Rules / Model ]\n'
                                '   [ Answers / Ground Truth ] ┘                                                       '
                                '│\n'
                                '                                                                                      '
                                '▼\n'
                                '   [ New Unseen Data ] ────────────────────────────────────────────────────────► [ '
                                'Predictions ]\n'
                                '```\n'
                                '\n'
                                '#### Classical Software Engineering (Deductive Approach)\n'
                                '- **How it works**: A human engineer studies the requirements, figures out the '
                                'logical steps, and writes explicit deterministic rules using `if`, `else`, `for`, and '
                                '`switch` statements.\n'
                                '- **When it shines**: When business logic is clear, deterministic, and static (e.g., '
                                'calculating tax slabs, authenticating passwords, processing database transactions).\n'
                                '- **Where it breaks**: When the problem involves perceptual complexity (recognizing '
                                'faces, speech, handwritten text) or high-dimensional fuzzy patterns.\n'
                                '\n'
                                '#### Machine Learning (Inductive Approach)\n'
                                '- **How it works**: Instead of hand-coding every condition, the engineer provides a '
                                'generic model family (e.g., linear regression, decision tree) and an optimization '
                                'criterion (loss function). The computer analyzes hundreds or thousands of labeled '
                                'historical examples and autonomously tunes its parameters to find the best mapping '
                                'rules.\n'
                                '- **When it shines**: When humans can easily recognize the pattern or provide '
                                'examples, but cannot cleanly express the underlying mathematical rules in code.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.2 The Spam Filter Intuition: Why Rules Collapse\n'
                                '\n'
                                'Consider building an email spam filter:\n'
                                '\n'
                                '```\n'
                                'Attempting Classical SDE:\n'
                                '   if "Viagra" in email_body: return SPAM\n'
                                '   if "Free Cash" in email_body: return SPAM\n'
                                '   if "Click Here Immediately" in email_body: return SPAM\n'
                                '```\n'
                                '\n'
                                'What happens next?\n'
                                '1. Spammers immediately adapt: they send `V!agra`, `V-i-a-g-r-a`, `Free_Ca$h`, or '
                                'embed text inside an image.\n'
                                '2. The engineer adds 50 more rules. Then 500 more rules.\n'
                                '3. Soon, valid emails get accidentally blocked (false positives), the rule base '
                                'becomes an unmaintainable tangled mess of exceptions, and the system collapses under '
                                '**combinatorial explosion**.\n'
                                '\n'
                                '**The Machine Learning Solution**:\n'
                                'Feed 50,000 labeled emails (spam vs. legitimate) into a statistical learning '
                                'algorithm. The algorithm automatically learns the predictive weights of thousands of '
                                'word combinations simultaneously. When spammers mutate their tactics, the engineer '
                                'does not rewrite code; they simply **retrain the pipeline on fresh labeled data**.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.3 Comprehensive Comparison Matrix\n'
                                '\n'
                                '| Architectural Dimension | Classical Software Engineering (SDE) | Machine Learning '
                                'Engineering (MLE) |\n'
                                '| :--- | :--- | :--- |\n'
                                '| **Origin of Logic** | Human engineer explicitly writes every logical branch. | '
                                'Optimization algorithm learns weights from historical data. |\n'
                                '| **Data Requirement** | Minimal; small unit test suites verify functionality. | '
                                'High; performance scales with sample size and feature quality. |\n'
                                '| **Adaptation to Change (Concept Drift)** | Requires code changes, developer '
                                'refactoring, and code redeployment. | Retrain the existing pipeline on newly '
                                'collected empirical data. |\n'
                                '| **Verification & Testing** | Deterministic unit tests, assertions, and edge-case '
                                'coverage. | Statistical validation: train/test split, cross-validation, '
                                'precision/recall. |\n'
                                '| **Primary Failure Modes** | Syntax errors, logic bugs, unhandled null pointers. | '
                                'Overfitting, underfitting, data leakage, distribution drift. |\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.4 Practical Rule of Thumb: When Should You Use ML?\n'
                                '\n'
                                'Never use machine learning when a simple, deterministic rule suffices!\n'
                                '\n'
                                '$$\\text{Engineering Choice} = \\begin{cases} \\text{Classical SDE Code} & \\text{if '
                                'rules are } \\le 20 \\text{ branches and business domain is static} \\\\ '
                                '\\text{Lookup Table / Heuristic} & \\text{if 100\\% exactness is mandatory and zero '
                                'statistical error is allowed} \\\\ \\text{Machine Learning} & \\text{if inputs are '
                                'complex, patterns fuzzy, and labeled data is available} \\end{cases}$$\n'
                                '\n'
                                '> **Core Takeaway**: If you can write a clean, short `if/else` block that solves the '
                                'problem reliably, write classical code. Reach for Machine Learning when the mapping '
                                'function is too complex to write by hand.',
                        'citations': [   'Mitchell, T. M. (1997). Machine Learning. McGraw-Hill Education, Chapter 1.',
                                         'Domingos, P. (2012). A few useful things to know about machine learning. '
                                         'Communications of the ACM, 55(10), 78-87.'],
                        'heading': '2. The Paradigm Shift: Classical Software Engineering (SDE) vs. Machine Learning '
                                   '(MLE)',
                        'section_id': 'cml-l01-sec02'},
                    {   'body': '### 3.1 Turning Vague Ambition into an Engineering Specification\n'
                                '\n'
                                'Saying *"I want to build an AI for my company"* is a vague aspiration, not an '
                                'engineering problem. In 1997, computer scientist **Tom Mitchell** provided the '
                                'foundational mathematical definition that anchors all machine learning:\n'
                                '\n'
                                "> **Tom Mitchell's Definition of Learning**:\n"
                                '> *"A computer program is said to learn from **Experience $E$** with respect to some '
                                'class of **Tasks $T$** and **Performance Measure $P$**, if its performance at tasks '
                                'in $T$, as measured by $P$, improves with experience $E$."*\n'
                                '\n'
                                'Whenever you design an ML project, you must explicitly define these three letters '
                                'before writing a single line of code:\n'
                                '\n'
                                '```\n'
                                "Tom Mitchell's ETP Triplet:\n"
                                '   ┌──────────────────────────────────────────────────────────────┐\n'
                                '   │  T (Task)        ──► What specific operational action?       │\n'
                                '   │  E (Experience)  ──► What historical data / observations?    │\n'
                                '   │  P (Performance) ──► How do we quantitatively score success? │\n'
                                '   └──────────────────────────────────────────────────────────────┘\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.2 Breaking Down the Triplet: T, E, and P\n'
                                '\n'
                                '1. **Task ($T$)**: The operational assignment the machine is executing. This is '
                                '**not** the learning process itself; it is the production task the model performs on '
                                'new data (e.g., classify an email, predict house price, detect credit card fraud).\n'
                                '2. **Experience ($E$)**: The empirical data or interaction history the system '
                                'consumes to learn. Without experience, there is no learning (e.g., historical emails '
                                'with user flags, past real estate transaction logs, sensor telemetry).\n'
                                '3. **Performance Measure ($P$)**: The quantitative metric used to judge whether the '
                                'system is doing well or poorly. It must align with the real-world business objective '
                                '(e.g., accuracy, precision, Root Mean Squared Error).\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.3 Concrete Industry Examples of ETP\n'
                                '\n'
                                '#### Example 1: Email Spam Classifier\n'
                                '- **Task ($T$)**: Classify an incoming email as either `Spam` or `Not Spam`.\n'
                                '- **Experience ($E$)**: A dataset of 100,000 historical emails along with '
                                'human-assigned labels.\n'
                                '- **Performance Measure ($P$)**: Classification F1-score or precision/recall on a '
                                'separate held-out test mailbox.\n'
                                '\n'
                                '#### Example 2: Real Estate Price Appraisal\n'
                                '- **Task ($T$)**: Predict the market selling price (in rupees/dollars) of a house '
                                'given its features.\n'
                                '- **Experience ($E$)**: Historical sales records containing square footage, number of '
                                'bedrooms, locality, and final sale prices.\n'
                                '- **Performance Measure ($P$)**: Root Mean Squared Error (RMSE) or Mean Absolute '
                                'Error (MAE) on unseen house sales.\n'
                                '\n'
                                '#### Example 3: Autonomous Vehicle Emergency Braking\n'
                                '- **Task ($T$)**: Decide whether to trigger the emergency brake system within 50 '
                                'milliseconds.\n'
                                '- **Experience ($E$)**: Telemetry data from LiDAR, radar, front-facing cameras, and '
                                'recorded driver interventions.\n'
                                '- **Performance Measure ($P$)**: Collision avoidance rate and false alarm rate on '
                                'road-simulation test courses.\n'
                                '\n'
                                '#### Example 4: Movie Recommendation Engine\n'
                                '- **Task ($T$)**: Recommend a list of top 5 movies a user is most likely to watch '
                                'next.\n'
                                '- **Experience ($E$)**: Historical user viewing histories, ratings, and click-through '
                                'logs.\n'
                                '- **Performance Measure ($P$)**: Mean Reciprocal Rank (MRR) or Click-Through Rate '
                                '(CTR) on held-out user sessions.\n'
                                '\n'
                                '> **Discussion Question**:\n'
                                '> If a system is trained on 10,000 examples and achieves 80% accuracy, but when '
                                'trained on 100,000 examples its accuracy remains stuck at 80%, is it improving with '
                                'experience $E$?\n'
                                '> Mathematically, if $P$ fails to increase as $E$ expands, the model has saturated '
                                'its hypothesis capacity (underfitting) or reached the irreducible noise limit of the '
                                'data.',
                        'citations': [   'Mitchell, T. M. (1997). Machine Learning. McGraw-Hill Education, Section '
                                         '1.2.',
                                         'Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach '
                                         '(4th ed.). Pearson.'],
                        'heading': "3. Tom Mitchell's Framework: Formulating Well-Defined Learning Problems (ETP)",
                        'section_id': 'cml-l01-sec03'},
                    {   'body': '### 4.1 The Golden Rule: The Target Space Governs the Task\n'
                                '\n'
                                'Once your problem is well-defined, the very first architectural question is: **What '
                                'kind of target are we predicting?**\n'
                                '\n'
                                'The distinction between Classification and Regression is governed **strictly by the '
                                'mathematical nature of the target variable $Y$ (the output)**. It has **nothing** to '
                                'do with whether the input features $X$ are continuous, discrete, or categorical!\n'
                                '\n'
                                '```\n'
                                'Target Output Type:\n'
                                '   ┌──────────────────────────────────────────────────────────────┐\n'
                                '   │  Target Y is Discrete (Categories / Classes)  ──► CLASSIFICATION │\n'
                                '   │  Target Y is Continuous (Real Numbers in ℝ)  ──► REGRESSION     │\n'
                                '   └──────────────────────────────────────────────────────────────┘\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.2 Classification: Predicting Discrete Categories\n'
                                '\n'
                                'In classification, the goal is to assign each input sample $\\mathbf{x}$ to one of '
                                'several mutually exclusive or non-mutually exclusive categories:\n'
                                '\n'
                                '$$y \\in \\{C_1, C_2, \\dots, C_K\\}$$\n'
                                '\n'
                                '- **Binary Classification**: Exactly two classes (e.g., `Spam` vs. `Ham`, `Fraud` vs. '
                                '`Legitimate`, `Churn` vs. `Retain`).\n'
                                '- **Multi-Class Classification**: More than two mutually exclusive classes; each '
                                'sample belongs to exactly one class (e.g., recognizing handwritten digits `0` through '
                                '`9`, classifying blood types `A`, `B`, `AB`, `O`).\n'
                                '- **Multi-Label Classification**: Each sample can simultaneously belong to multiple '
                                'classes (e.g., tagging a news article with both `Finance` and `Technology`, or a '
                                'chest X-ray exhibiting both `Pneumonia` and `Cardiomegaly`).\n'
                                '\n'
                                '#### The "Class Probabilities" Trap: Does Probability Make It Regression?\n'
                                'Beginners often ask: *"My Logistic Regression model outputs $0.85$ (85% probability '
                                "of churn). Since $0.85$ is a continuous decimal number, isn't it doing "
                                'regression?"*\n'
                                '\n'
                                '> **No!**\n'
                                '> Calculating posterior probabilities $P(Y=1 \\mid X)$ is merely **internal '
                                'mathematical machinery** for quantifying confidence. The operational objective of the '
                                'system is still to make a **discrete categorical decision**:\n'
                                '> \n'
                                '> $$\\hat{y} = \\begin{cases} 1 & \\text{if } P(Y=1 \\mid X) \\ge \\tau \\\\ 0 & '
                                '\\text{if } P(Y=1 \\mid X) < \\tau \\end{cases}$$\n'
                                '> \n'
                                '> You cannot evaluate this system using Mean Squared Error or $R^2$; you evaluate it '
                                'using Accuracy, Precision, Recall, and ROC-AUC.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.3 Regression: Predicting Continuous Numeric Values\n'
                                '\n'
                                'In regression, the target variable is a real continuous quantity:\n'
                                '\n'
                                '$$y \\in \\mathbb{R}$$\n'
                                '\n'
                                "- Examples: Predicting next month's electricity consumption in kilowatt-hours, house "
                                'price in rupees, delivery time in minutes, or engine temperature in Celsius.\n'
                                '- The target has natural ordering and meaningful arithmetic differences: the '
                                'difference between 50°C and 60°C represents the exact same physical magnitude as '
                                'between 90°C and 100°C.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.4 Comprehensive Comparison Table\n'
                                '\n'
                                '| Attribute | Classification | Regression |\n'
                                '| :--- | :--- | :--- |\n'
                                '| **Target Variable ($Y$)** | **Discrete** categories / labels (nominal or ordinal). '
                                '| **Continuous** real-valued scalar ($y \\in \\mathbb{R}$). |\n'
                                '| **Typical Model Output** | Predicted class label, or class probability '
                                'distribution. | A single continuous numerical estimate $\\hat{y}$. |\n'
                                '| **Standard Evaluation Metrics** | Accuracy, Precision, Recall, F1-Score, ROC-AUC, '
                                'Log-Loss. | Mean Absolute Error (MAE), Mean Squared Error (MSE), RMSE, $R^2$. |\n'
                                '| **Input Feature Types** | Continuous, discrete, or mixed (text, numeric, '
                                'categorical). | Continuous, discrete, or mixed (numerical, categorical). |\n'
                                '| **Example Business Questions** | *"Will this subscriber cancel their plan this '
                                'month?"* | *"How many total rupees will this customer spend this year?"* |\n'
                                '\n'
                                '> **Input vs. Output Clarification**:\n'
                                '> - Can a regression model have categorical inputs? **Yes!** For example, predicting '
                                'house price ($y$, continuous) using `neighborhood` (discrete/categorical) and '
                                '`bedrooms` (discrete integer).\n'
                                '> - Can a classification model have continuous inputs? **Yes!** For example, '
                                'predicting heart disease diagnosis ($y$, discrete) using `blood_pressure` and '
                                '`cholesterol` (continuous).',
                        'citations': [   'Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of '
                                         'Statistical Learning. Springer, Chapter 2.',
                                         'James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). An Introduction '
                                         'to Statistical Learning. Springer.'],
                        'heading': '4. Task Taxonomy: The Fundamental Divide Between Classification and Regression',
                        'section_id': 'cml-l01-sec04'},
                    {   'body': '### 5.1 The Core Distinction: Is There a Teacher?\n'
                                '\n'
                                'Machine learning paradigms are classified primarily by **what kind of supervision or '
                                'feedback signal** the algorithm receives during training:\n'
                                '\n'
                                '```\n'
                                'Learning Paradigms:\n'
                                '   ├── SUPERVISED LEARNING   ──► Training data includes inputs X AND ground-truth '
                                'targets Y (Learn X -> Y)\n'
                                '   ├── UNSUPERVISED LEARNING ──► Training data has ONLY inputs X (Discover emergent '
                                'structure in X)\n'
                                '   ├── SEMI-SUPERVISED       ──► Massive unlabelled X with a small fraction of '
                                'labeled (X, Y)\n'
                                '   └── REINFORCEMENT         ──► Active agent receives delayed scalar rewards via '
                                'trial-and-error\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.2 Supervised Learning: Learning with a Teacher\n'
                                '\n'
                                'In Supervised Learning, every single observation in the training dataset is paired '
                                'with an explicit ground-truth answer:\n'
                                '\n'
                                '$$\\mathcal{D}_{\\text{train}} = \\{(\\mathbf{x}_1, y_1), (\\mathbf{x}_2, y_2), '
                                '\\dots, (\\mathbf{x}_n, y_n)\\}$$\n'
                                '\n'
                                "The algorithm's job is to adjust its internal parameters so that its prediction "
                                '$\\hat{y} = f(\\mathbf{x})$ matches the true target $y$ as closely as possible.\n'
                                '- **Both Classification and Regression belong to Supervised Learning.**\n'
                                "- Evaluation is straightforward: compare the model's predictions $\\hat{y}$ against "
                                'known true labels $y$ on holdout test data.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.3 Unsupervised Learning: Discovering Hidden Structure\n'
                                '\n'
                                'In Unsupervised Learning, there are **no target labels $y$**. The dataset consists '
                                'solely of feature vectors:\n'
                                '\n'
                                '$$\\mathcal{D}_{\\text{train}} = \\{\\mathbf{x}_1, \\mathbf{x}_2, \\dots, '
                                '\\mathbf{x}_n\\}$$\n'
                                '\n'
                                'The algorithm receives no guidance on what the "correct" answer is. Instead, it '
                                'inspects the geometric and statistical relationships among points in feature space to '
                                'discover hidden structure:\n'
                                '1. **Clustering (e.g., K-Means, Hierarchical)**: Grouping similar data points '
                                'together based on distance or density.\n'
                                '2. **Dimensionality Reduction (e.g., PCA, t-SNE)**: Compressing high-dimensional '
                                'features into fewer dimensions while preserving variance or neighborhood structure.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.4 The Crucial Distinction: Clustering vs. Classification\n'
                                '\n'
                                'This is one of the most widely tested conceptual boundaries in machine learning '
                                'interviews:\n'
                                '\n'
                                '```\n'
                                'Clustering vs. Classification:\n'
                                '   [ Labeled Dataset (Pre-defined Classes) ] ──► CLASSIFICATION  ──► Predicts known '
                                'labels (e.g., Cat / Dog)\n'
                                '   [ Unlabeled Dataset (No Prior Names) ]     ──► CLUSTERING      ──► Discovers '
                                'emergent groups from geometry\n'
                                '```\n'
                                '\n'
                                '| Dimension | Supervised Classification | Unsupervised Clustering |\n'
                                '| :--- | :--- | :--- |\n'
                                '| **Ground-Truth Labels** | **Required during training.** | **Completely absent.** |\n'
                                '| **Output Meaning** | Predicts pre-existing, human-defined category names. | Groups '
                                'data by geometric proximity; human must interpret what each cluster represents. |\n'
                                '| **Evaluation** | Objective comparison against test labels (Accuracy, F1). | '
                                'Internal geometric heuristics (Silhouette score) or qualitative domain inspection. |\n'
                                '| **Analogy** | Sorting mail into labeled mailboxes: `Billing`, `HR`, `Legal`. | '
                                'Arranging pebbles on a table into piles by color and size without knowing their '
                                'names. |\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.5 Four Real-World Benchmark Case Studies (From Class)\n'
                                '\n'
                                "Let's walk through four classic scenarios discussed in class to see how to instantly "
                                'determine the correct paradigm:\n'
                                '\n'
                                "#### Case 1: The Property Dealer's Pricing Tool\n"
                                '- *Scenario*: A real estate broker has historical records containing property size, '
                                'number of bedrooms, locality, and recorded past sale prices. A new client asks what '
                                'price a 3-bedroom apartment should sell for.\n'
                                '- *Analysis*:\n'
                                '  - Are ground-truth targets available? **Yes** (past transaction prices).\n'
                                '  - Is the target discrete or continuous? **Continuous** (sale price in currency).\n'
                                '  - *Correct Paradigm*: **Supervised Regression**.\n'
                                '\n'
                                '#### Case 2: Untagged Customer Feedback Reviews\n'
                                '- *Scenario*: A product manager receives 20,000 free-form customer feedback comments. '
                                'No tags, categories, or labels have been created yet. The manager wants to discover '
                                'the primary underlying themes (e.g., product defects, delivery delays, customer '
                                'support).\n'
                                '- *Analysis*:\n'
                                '  - Are labels available? **No**. The system must inspect the vocabulary geometry and '
                                'group similar reviews together autonomously.\n'
                                '  - *Correct Paradigm*: **Unsupervised Learning (Clustering / Topic Modeling)**.\n'
                                '\n'
                                '#### Case 3: Stock Price Forecasting\n'
                                '- *Scenario*: An investment firm uses past stock price records, trading volume, and '
                                'macroeconomic indicators to predict the exact closing price of a stock tomorrow.\n'
                                '- *Analysis*:\n'
                                "  - Are historical target values available? **Yes** (yesterday's and historical "
                                'closing prices).\n'
                                '  - Is the target discrete or continuous? **Continuous** (numeric stock price).\n'
                                '  - *Correct Paradigm*: **Supervised Regression**.\n'
                                '\n'
                                '#### Case 4: Human Resources Candidate Triage\n'
                                '- *Scenario*: An enterprise HR department has three pre-existing, well-defined '
                                'candidate bands: `Direct Hire`, `Technical Interview`, and `Reject`. They have '
                                'thousands of past resumes with their final HR decisions.\n'
                                '- *Analysis*:\n'
                                '  - The categories already exist and are clearly named (`Direct Hire`, `Interview`, '
                                '`Reject`).\n'
                                '  - Labeled historical examples exist.\n'
                                '  - An unsupervised clustering algorithm would invent mathematical clusters based on '
                                "resume length or font, which would **not** align with HR's business buckets!\n"
                                '  - *Correct Paradigm*: **Supervised Classification**.',
                        'citations': [   'Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of '
                                         'Statistical Learning. Springer, Chapter 14.',
                                         'Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer, '
                                         'Section 1.1.'],
                        'heading': '5. Learning Paradigms: Supervised vs. Unsupervised Learning',
                        'section_id': 'cml-l01-sec05'},
                    {   'body': '### 6.1 Executable Code Demonstrations\n'
                                '\n'
                                'Below are three clean, self-contained Python examples demonstrating:\n'
                                '1. Classification with discrete labels.\n'
                                '2. Regression with a continuous line fit.\n'
                                '3. Unsupervised clustering with K-Means.\n'
                                '\n'
                                '```python\n'
                                'import numpy as np\n'
                                'import matplotlib.pyplot as plt\n'
                                'from sklearn.cluster import KMeans\n'
                                '\n'
                                '# Set random seed for reproducibility\n'
                                'rng = np.random.default_rng(42)\n'
                                '\n'
                                '# =====================================================================\n'
                                '# 1. CLASSIFICATION TOY DEMO (Discrete Labels)\n'
                                '# =====================================================================\n'
                                'n_samples = 60\n'
                                '# Class 0: centered at (-1, -1)\n'
                                'X_class0 = rng.normal(loc=[-1.0, -1.0], scale=0.4, size=(n_samples, 2))\n'
                                '# Class 1: centered at (1, 1)\n'
                                'X_class1 = rng.normal(loc=[1.0, 1.0], scale=0.4, size=(n_samples, 2))\n'
                                '\n'
                                'X_clf = np.vstack([X_class0, X_class1])\n'
                                'y_clf = np.array([0] * n_samples + [1] * n_samples)  # Discrete labels: 0 or 1\n'
                                '\n'
                                '# =====================================================================\n'
                                '# 2. REGRESSION TOY DEMO (Continuous Numeric Target)\n'
                                '# =====================================================================\n'
                                'x_reg = np.linspace(-3, 3, 70)\n'
                                '# Underlying true relation: y = 2.0 * x + 0.5 + Gaussian noise\n'
                                'noise = rng.normal(loc=0.0, scale=0.6, size=x_reg.shape)\n'
                                'y_reg = 2.0 * x_reg + 0.5 + noise\n'
                                '\n'
                                '# Closed-form Ordinary Least Squares slope and intercept\n'
                                'w1 = np.cov(x_reg, y_reg, bias=True)[0, 1] / np.var(x_reg)\n'
                                'w0 = y_reg.mean() - w1 * x_reg.mean()\n'
                                'y_pred_line = w0 + w1 * x_reg\n'
                                '\n'
                                '# =====================================================================\n'
                                '# 3. UNSUPERVISED CLUSTERING TOY DEMO (K-Means without Labels)\n'
                                '# =====================================================================\n'
                                '# Generate 3 unlabelled spatial clusters\n'
                                'blob1 = rng.normal(loc=[-2.0, 0.0], scale=0.5, size=(50, 2))\n'
                                'blob2 = rng.normal(loc=[1.5, 2.0], scale=0.5, size=(50, 2))\n'
                                'blob3 = rng.normal(loc=[1.5, -2.0], scale=0.5, size=(50, 2))\n'
                                'X_unlabeled = np.vstack([blob1, blob2, blob3])\n'
                                '\n'
                                '# Fit KMeans (Notice: fit() takes ONLY X, no target y!)\n'
                                'kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)\n'
                                'cluster_assignments = kmeans.fit_predict(X_unlabeled)\n'
                                'centroids = kmeans.cluster_centers_\n'
                                '\n'
                                '# =====================================================================\n'
                                '# VISUALIZATION\n'
                                '# =====================================================================\n'
                                'fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))\n'
                                '\n'
                                '# Plot 1: Classification\n'
                                'axes[0].scatter(X_clf[y_clf == 0, 0], X_clf[y_clf == 0, 1], color="royalblue", '
                                'alpha=0.8, label="Class 0")\n'
                                'axes[0].scatter(X_clf[y_clf == 1, 0], X_clf[y_clf == 1, 1], color="crimson", '
                                'alpha=0.8, label="Class 1")\n'
                                'axes[0].set_title("1. Classification (Discrete Targets)")\n'
                                'axes[0].set_xlabel("Feature x1")\n'
                                'axes[0].set_ylabel("Feature x2")\n'
                                'axes[0].legend()\n'
                                'axes[0].grid(True, linestyle="--", alpha=0.5)\n'
                                '\n'
                                '# Plot 2: Regression\n'
                                'axes[1].scatter(x_reg, y_reg, color="darkorange", alpha=0.7, label="Observed (x, '
                                'y)")\n'
                                'axes[1].plot(x_reg, y_pred_line, color="black", linewidth=2, label="Fitted Line '
                                '(y_hat)")\n'
                                'axes[1].set_title("2. Regression (Continuous Target)")\n'
                                'axes[1].set_xlabel("Input Feature x")\n'
                                'axes[1].set_ylabel("Continuous Target y")\n'
                                'axes[1].legend()\n'
                                'axes[1].grid(True, linestyle="--", alpha=0.5)\n'
                                '\n'
                                '# Plot 3: Unsupervised Clustering\n'
                                'scatter = axes[2].scatter(X_unlabeled[:, 0], X_unlabeled[:, 1], '
                                'c=cluster_assignments, cmap="viridis", alpha=0.75)\n'
                                'axes[2].scatter(centroids[:, 0], centroids[:, 1], marker="X", s=150, color="red", '
                                'label="Centroids")\n'
                                'axes[2].set_title("3. Unsupervised (K-Means Clustering)")\n'
                                'axes[2].set_xlabel("Feature x1")\n'
                                'axes[2].set_ylabel("Feature x2")\n'
                                'axes[2].legend()\n'
                                'axes[2].grid(True, linestyle="--", alpha=0.5)\n'
                                '\n'
                                'plt.tight_layout()\n'
                                'plt.show()\n'
                                '\n'
                                'print("Summary Check:")\n'
                                'print(f"Classification Classes: {np.unique(y_clf)}")\n'
                                'print(f"Regression Fitted Formula: y_hat = {w1:.2f} * x + {w0:.2f}")\n'
                                'print(f"Discovered Cluster Sizes: {np.bincount(cluster_assignments)}")\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 6.2 Master Summary Table\n'
                                '\n'
                                '| Concept | Defining Question | Core Mechanism | Key Example |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **SDE vs. MLE** | *Who writes the rules?* | SDE = Human coders; MLE = Optimization '
                                'algorithm learns from data. | Handcrafted regex rules vs. trained Spam Classifier. |\n'
                                '| **Tom Mitchell ETP** | *Is the problem well-defined?* | Quantifies Task $T$, '
                                'Experience $E$, and Performance Measure $P$. | Predict house price ($T$) from sales '
                                'data ($E$) measured by RMSE ($P$). |\n'
                                '| **Classification** | *Is the target categorical?* | Predicts discrete class '
                                'memberships; evaluated via Accuracy/F1. | Patient has diabetes vs. healthy. |\n'
                                '| **Regression** | *Is the target continuous?* | Predicts a real-valued number $y '
                                "\\in \\mathbb{R}$; evaluated via RMSE/MAE. | Predicting tomorrow's maximum "
                                'temperature. |\n'
                                '| **Supervised Learning** | *Are ground-truth labels provided?* | Uses paired '
                                'examples $(x_i, y_i)$ to learn mapping $x \\mapsto y$. | Loan default prediction, '
                                'property valuation. |\n'
                                '| **Unsupervised Learning** | *Is the system discovering structure?* | Learns from '
                                '$x_i$ alone to identify geometric clusters or compressions. | Customer market basket '
                                'segmentation, PCA compression. |',
                        'citations': [   'Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. '
                                         'Journal of Machine Learning Research, 12, 2825-2830.',
                                         'Harris, C. R. et al. (2020). Array programming with NumPy. Nature, 585, '
                                         '357-362.'],
                        'heading': '6. Hands-On Python Implementations & Visual Demonstrations',
                        'section_id': 'cml-l01-sec06'}],
    'subject_code': 'CML',
    'summary': 'An intuitive yet rigorous first-principles introduction to Classical Machine Learning. Covers the core '
               'DSML foundation (NumPy, Pandas, visualization taxonomy), the fundamental paradigm shift from '
               "rule-based software engineering (SDE) to statistical learning (MLE), Tom Mitchell's formal ETP "
               'framework for well-defined problems, the mathematical boundary separating classification from '
               'regression, and the operational contrast between supervised prediction and unsupervised structure '
               'discovery.',
    'tags': [   'Classical Machine Learning',
                'Foundations',
                'Tom Mitchell ETP',
                'Classification',
                'Regression',
                'Supervised Learning',
                'Unsupervised Learning',
                'EDA',
                'Data Visualization'],
    'term': 'Term 5',
    'topic_title': '1. Introduction to Classical Machine Learning, Paradigms & Problem Formulation'}

