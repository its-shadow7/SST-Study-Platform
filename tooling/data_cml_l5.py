"""
Data definition for data_cml_l5:
"""

CML_L05_DATA = {   'approval_status': 'approved',
    'key_takeaways': [   '1. While Ordinary Least Squares possesses a closed-form analytical solution, its O(d^3) '
                         'matrix inversion cost and O(m*d) memory footprint make it unviable for massive feature '
                         'spaces (d > 10,000) or streaming datasets (m > 1,000,000).',
                         '2. The gradient vector nabla J(w) points in the direction of maximum directional derivative '
                         '(steepest ascent); moving along the negative gradient vector -nabla J(w) guarantees the '
                         'greatest local decrease in loss.',
                         '3. For Mean Squared Error, the gradient is an error-weighted average of the input feature '
                         'vectors: nabla_w J(w) = (2/m) * X^T (Xw - y). The prediction error (y_hat - y) acts as an '
                         'adaptive gain for each feature.',
                         '4. Learning rate eta governs convergence: if eta < 2 / L (where L is the Lipschitz '
                         'smoothness constant of the gradient), convergence is guaranteed on convex bowls; exceeding '
                         'this threshold causes explosive divergence.',
                         '5. Batch GD computes exact gradients over all m samples (stable, O(m*d) per step, but '
                         'sluggish on massive data); SGD samples k=1 point (O(d) step, highly stochastic, escapes '
                         'shallow local traps, but never settles without decay); Mini-Batch GD samples k in [32, 256] '
                         'points (optimal SIMD hardware utilization and low gradient noise).',
                         '6. Unscaled features produce highly eccentric elliptical loss contours (condition number '
                         'kappa >> 1), causing orthogonal gradient bouncing across narrow valley walls; Z-score '
                         'standardization restores hyperspherical contours for direct, accelerated descent.',
                         '7. Production gradient descent requires robust stopping criteria (gradient L2 norm < '
                         'epsilon, relative loss delta < tol) and dynamic learning rate decay (step decay, exponential '
                         'decay, or cosine annealing).'],
    'last_updated': '2026-10-16T00:00:00Z',
    'order': 5,
    'prerequisites': ['cml-t5-l01', 'cml-t5-l02', 'cml-t5-l03', 'cml-t5-l04'],
    'quiz': {   'description': '25-question examination evaluating analytical vs. iterative optimization, gradient '
                               'vector calculus, learning rate stability limits, Batch/SGD/Mini-Batch trade-offs, loss '
                               'surface conditioning, stopping criteria, and Scikit-Learn implementations.',
                'questions': [   {   'correct_answer': 'opt-b',
                                     'difficulty': 'easy',
                                     'explanation': 'By definition in multivariate calculus, the gradient vector '
                                                    'points in the direction of maximum directional '
                                                    'derivative—steepest ascent. To minimize loss, Gradient Descent '
                                                    'steps in the opposite direction (-nabla J).',
                                     'id': 'q-cml-l05-01',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'The direction of steepest descent where the loss '
                                                                'function decreases most rapidly'},
                                                    {   'id': 'opt-b',
                                                        'text': 'The direction of steepest ascent where the loss '
                                                                'function increases most rapidly'},
                                                    {   'id': 'opt-c',
                                                        'text': 'The tangent line parallel to the contour ellipse of '
                                                                'constant loss'},
                                                    {   'id': 'opt-d',
                                                        'text': 'The vector pointing directly toward the origin (0, '
                                                                '0)'}],
                                     'question': 'In iterative optimization, what does the gradient vector \\nabla '
                                                 'J(\\mathbf{w}) geometrically represent on the loss surface?',
                                     'subtopic': 'Fundamental Concept of Gradient Descent',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-c',
                                     'difficulty': 'easy',
                                     'explanation': 'Because the gradient points uphill in the direction of steepest '
                                                    'ascent, moving in the negative direction (-nabla J) moves '
                                                    'downhill in the direction of steepest descent, minimizing the '
                                                    'loss function.',
                                     'id': 'q-cml-l05-02',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'Because weights in machine learning must always be '
                                                                'strictly negative'},
                                                    {   'id': 'opt-b',
                                                        'text': 'To subtract the learning rate from the sample count'},
                                                    {   'id': 'opt-c',
                                                        'text': 'Because stepping opposite the gradient moves '
                                                                'parameters downhill toward the minimum'},
                                                    {   'id': 'opt-d',
                                                        'text': 'To ensure that the Hessian matrix remains positive '
                                                                'semi-definite'}],
                                     'question': 'Why is there a negative sign in the standard gradient descent '
                                                 'parameter update rule \\mathbf{w}^{(t+1)} := \\mathbf{w}^{(t)} - '
                                                 '\\eta \\nabla J(\\mathbf{w}^{(t)})?',
                                     'subtopic': 'Update Rule Operator',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-a',
                                     'difficulty': 'easy',
                                     'explanation': 'In pure Stochastic Gradient Descent (SGD), the batch size is '
                                                    'exactly 1: a single randomly chosen sample is used to compute the '
                                                    'gradient and update weights at each step.',
                                     'id': 'q-cml-l05-03',
                                     'options': [   {'id': 'opt-a', 'text': 'Exactly 1 sample'},
                                                    {'id': 'opt-b', 'text': 'Exactly 32 samples'},
                                                    {'id': 'opt-c', 'text': 'Half of the dataset (m / 2)'},
                                                    {'id': 'opt-d', 'text': 'The entire dataset (all m samples)'}],
                                     'question': 'What is the batch size (number of data samples evaluated per '
                                                 'parameter update) in pure Stochastic Gradient Descent (SGD)?',
                                     'subtopic': 'Batch Sizes in GD Variants',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-c',
                                     'difficulty': 'easy',
                                     'explanation': 'Batch Gradient Descent evaluates all m observations in the '
                                                    'training set before performing a single parameter update.',
                                     'id': 'q-cml-l05-04',
                                     'options': [   {'id': 'opt-a', 'text': '1 sample'},
                                                    {'id': 'opt-b', 'text': 'A fixed mini-batch of 64 samples'},
                                                    {'id': 'opt-c', 'text': 'The entire training dataset of m samples'},
                                                    {   'id': 'opt-d',
                                                        'text': 'The square root of the number of features (sqrt(d))'}],
                                     'question': 'What is the batch size in Batch Gradient Descent (BGD)?',
                                     'subtopic': 'Batch Sizes in GD Variants',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-b',
                                     'difficulty': 'easy',
                                     'explanation': 'The learning rate acts as a step-size multiplier that scales the '
                                                    'gradient vector, dictating how far the parameters move during '
                                                    'each update.',
                                     'id': 'q-cml-l05-05',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'It determines how many features are dropped during '
                                                                'backward selection'},
                                                    {   'id': 'opt-b',
                                                        'text': 'It scales the step magnitude taken in the direction '
                                                                'of the negative gradient'},
                                                    {   'id': 'opt-c',
                                                        'text': 'It sets the regularization penalty on the L2 norm of '
                                                                'the weights'},
                                                    {   'id': 'opt-d',
                                                        'text': 'It controls the number of hidden layers in a neural '
                                                                'network'}],
                                     'question': 'What is the primary role of the learning rate hyperparameter (\\eta '
                                                 'or \\alpha) in Gradient Descent?',
                                     'subtopic': 'Learning Rate Role',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-c',
                                     'difficulty': 'easy',
                                     'explanation': 'An excessively large learning rate causes the updates to '
                                                    'overshoot the valley floor and jump higher up the opposing walls, '
                                                    'causing explosive divergence to +inf or NaN.',
                                     'id': 'q-cml-l05-06',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'Training halts immediately with a zero gradient'},
                                                    {   'id': 'opt-b',
                                                        'text': 'The model underfits due to excessive parameter '
                                                                'shrinkage'},
                                                    {   'id': 'opt-c',
                                                        'text': 'The weights overshoot the minimum and the loss '
                                                                'function diverges (often outputting NaN or inf)'},
                                                    {   'id': 'opt-d',
                                                        'text': 'The optimization path becomes perfectly straight and '
                                                                'smooth'}],
                                     'question': 'What typically happens during training if the learning rate \\eta is '
                                                 'set excessively large?',
                                     'subtopic': 'Symptom of High Learning Rate',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-b',
                                     'difficulty': 'easy',
                                     'explanation': 'When eta is too small, parameters make microscopic progress each '
                                                    'epoch, requiring millions of steps to reach the optimum and '
                                                    'exhausting training time budgets.',
                                     'id': 'q-cml-l05-07',
                                     'options': [   {'id': 'opt-a', 'text': 'Catastrophic numerical divergence'},
                                                    {   'id': 'opt-b',
                                                        'text': 'Painfully slow convergence requiring an impractical '
                                                                'number of iterations'},
                                                    {'id': 'opt-c', 'text': 'Immediate convergence in a single step'},
                                                    {   'id': 'opt-d',
                                                        'text': 'The model switches automatically to closed-form OLS'}],
                                     'question': 'What is the consequence of selecting a learning rate that is '
                                                 'severely too small (e.g., \\eta = 10^{-9})?',
                                     'subtopic': 'Symptom of Low Learning Rate',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-b',
                                     'difficulty': 'easy',
                                     'explanation': 'Unscaled features create elongated, ravine-like loss contours '
                                                    'where gradients bounce between steep walls instead of heading '
                                                    'down the valley. Scaling restores spherical contours where '
                                                    'gradients point directly to the minimum.',
                                     'id': 'q-cml-l05-08',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'Because Gradient Descent cannot mathematically '
                                                                'compute derivatives on negative numbers'},
                                                    {   'id': 'opt-b',
                                                        'text': 'To transform eccentric elliptical loss contours into '
                                                                'spherical bowls, preventing zig-zagging and speeding '
                                                                'up descent'},
                                                    {   'id': 'opt-c',
                                                        'text': 'To convert the regression problem into a '
                                                                'classification problem'},
                                                    {   'id': 'opt-d',
                                                        'text': 'To eliminate the need for an intercept term w_0'}],
                                     'question': 'Why is feature scaling (e.g., StandardScaler) strongly recommended '
                                                 'before training linear regression with Gradient Descent?',
                                     'subtopic': 'Feature Scaling in GD',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-b',
                                     'difficulty': 'medium',
                                     'explanation': 'By applying the chain rule to 1/m * sum (y_hat - y)^2, we get '
                                                    '(2/m) * sum (y_hat - y) * d(y_hat)/d(w_j). Since d(y_hat)/d(w_j) '
                                                    '= x_{ij}, the scalar derivative is (2/m) * sum (y_hat_i - y_i) * '
                                                    'x_{ij}.',
                                     'id': 'q-cml-l05-09',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': '\\frac{1}{m} \\sum_{i=1}^m (\\hat{y}_i - y_i)'},
                                                    {   'id': 'opt-b',
                                                        'text': '\\frac{2}{m} \\sum_{i=1}^m (\\hat{y}_i - y_i) x_{ij}'},
                                                    {   'id': 'opt-c',
                                                        'text': '\\frac{2}{m} \\sum_{i=1}^m (\\hat{y}_i - y_i)^2 '
                                                                'x_{ij}'},
                                                    {   'id': 'opt-d',
                                                        'text': '\\frac{1}{2m} \\sum_{i=1}^m (\\hat{y}_i - y_i) '
                                                                'x_{ij}^2'}],
                                     'question': 'What is the analytical scalar partial derivative \\frac{\\partial '
                                                 'J}{\\partial w_j} for Mean Squared Error J(\\mathbf{w}) = '
                                                 '\\frac{1}{m} \\sum_{i=1}^m (\\hat{y}_i - y_i)^2?',
                                     'subtopic': 'MSE Gradient Formula',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-b',
                                     'difficulty': 'medium',
                                     'explanation': 'The matrix derivative of J(w) = (1/m) ||Xw - y||^2 with respect '
                                                    'to w is (2/m) X^T (Xw - y), mapping the m-dimensional residual '
                                                    'vector back to the (d+1)-dimensional parameter space.',
                                     'id': 'q-cml-l05-10',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': '\\frac{2}{m} (\\mathbf{X}\\mathbf{w} - \\mathbf{y})'},
                                                    {   'id': 'opt-b',
                                                        'text': '\\frac{2}{m} \\mathbf{X}^T (\\mathbf{X}\\mathbf{w} - '
                                                                '\\mathbf{y})'},
                                                    {   'id': 'opt-c',
                                                        'text': '\\frac{1}{m} (\\mathbf{X}^T \\mathbf{X})^{-1} '
                                                                '\\mathbf{y}'},
                                                    {   'id': 'opt-d',
                                                        'text': '\\frac{2}{m} \\mathbf{X} (\\mathbf{X}^T \\mathbf{w} - '
                                                                '\\mathbf{y})'}],
                                     'question': 'In compact matrix notation, what is the gradient '
                                                 '\\nabla_{\\mathbf{w}} J(\\mathbf{w}) of Mean Squared Error with '
                                                 'design matrix \\mathbf{X} \\in \\mathbb{R}^{m \\times (d+1)}?',
                                     'subtopic': 'Vectorized Gradient Formulation',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-b',
                                     'difficulty': 'medium',
                                     'explanation': 'Because BGD averages over all m points, its gradient is exact and '
                                                    'smooth. SGD uses only 1 point, so its gradient estimator has high '
                                                    'variance, causing a noisy, erratic path.',
                                     'id': 'q-cml-l05-11',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'BGD follows a jagged, erratic zig-zag path, while SGD '
                                                                'moves in a perfectly smooth curve'},
                                                    {   'id': 'opt-b',
                                                        'text': 'BGD moves smoothly and deterministically '
                                                                'perpendicular to contour lines, while SGD exhibits '
                                                                'jagged fluctuations due to single-sample gradient '
                                                                'variance'},
                                                    {   'id': 'opt-c',
                                                        'text': 'Both algorithms follow identical mathematical paths '
                                                                'regardless of sample size'},
                                                    {   'id': 'opt-d',
                                                        'text': 'BGD spirals outward away from the minimum, while SGD '
                                                                'jumps directly to the center in one step'}],
                                     'question': 'Which of the following describes the trajectory of Batch Gradient '
                                                 'Descent vs. Stochastic Gradient Descent on a 2D contour plot?',
                                     'subtopic': 'Trajectory Comparison',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-c',
                                     'difficulty': 'medium',
                                     'explanation': 'Mini-batch strikes the optimal balance: it exploits matrix '
                                                    'vectorization on modern hardware (CPUs/GPUs) while reducing '
                                                    'gradient variance by factor 1/k, converging faster in wall-clock '
                                                    'time than both BGD and pure SGD.',
                                     'id': 'q-cml-l05-12',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'It guarantees that the final model will achieve 100% '
                                                                'test accuracy'},
                                                    {   'id': 'opt-b',
                                                        'text': 'It eliminates the need for any learning rate '
                                                                'hyperparameter'},
                                                    {   'id': 'opt-c',
                                                        'text': 'It leverages SIMD/GPU parallel vectorization for fast '
                                                                'compute while averaging out single-sample gradient '
                                                                'noise'},
                                                    {   'id': 'opt-d',
                                                        'text': 'It produces an exact closed-form matrix inversion at '
                                                                'the end of each epoch'}],
                                     'question': 'Why is Mini-Batch Gradient Descent (e.g., batch size 32 to 128) '
                                                 'considered the practical industry standard over pure SGD and full '
                                                 'Batch GD?',
                                     'subtopic': 'Mini-Batch Advantage',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-b',
                                     'difficulty': 'medium',
                                     'explanation': 'Because each sample has an individual residual (y_hat_i - y_i) != '
                                                    '0 at the global minimum, individual sample gradients do not '
                                                    'vanish. With a constant learning rate, SGD bounces continuously '
                                                    'around w* without settling.',
                                     'id': 'q-cml-l05-13',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'It will converge to the exact machine-precision '
                                                                'minimum w*'},
                                                    {   'id': 'opt-b',
                                                        'text': 'It will fluctuate endlessly in a bounding ball around '
                                                                'the minimum due to non-vanishing gradient variance'},
                                                    {'id': 'opt-c', 'text': 'It will immediately diverge to infinity'},
                                                    {'id': 'opt-d', 'text': 'It will freeze and stop taking steps'}],
                                     'question': 'If pure SGD is run with a constant learning rate \\eta > 0 on a '
                                                 'convex loss surface, what will happen to the parameter vector as '
                                                 'iterations approach infinity?',
                                     'subtopic': 'SGD Non-Convergence at Constant Learning Rate',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-b',
                                     'difficulty': 'medium',
                                     'explanation': 'At a minimum of a differentiable convex function, nabla J(w) = 0. '
                                                    'A gradient L2 norm smaller than 10^-5 confirms the optimizer has '
                                                    'reached the flat basin floor of the loss bowl.',
                                     'id': 'q-cml-l05-14',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'The model has diverged and the weights must be reset'},
                                                    {   'id': 'opt-b',
                                                        'text': 'The parameters are in an extremely flat region near '
                                                                'an optimum where loss changes are virtually zero, '
                                                                'satisfying convergence'},
                                                    {   'id': 'opt-c',
                                                        'text': 'The learning rate has automatically dropped to zero'},
                                                    {   'id': 'opt-d',
                                                        'text': 'The data contains severe multicollinearity'}],
                                     'question': 'An engineer monitors Gradient Descent and observes that ||\\nabla '
                                                 'J(\\mathbf{w}^{(t)})||_2 < 10^{-5}. What does this diagnostic signal '
                                                 'indicate?',
                                     'subtopic': 'Stopping Criteria Mechanics',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-b',
                                     'difficulty': 'medium',
                                     'explanation': 'Early in training, large learning rates traverse flat plateaus '
                                                    'and long distances quickly. Late in training, decaying the '
                                                    'learning rate dampens stochastic oscillations, allowing the model '
                                                    'to settle precisely into the minimum.',
                                     'id': 'q-cml-l05-15',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'To increase the training speed during the final '
                                                                'epochs'},
                                                    {   'id': 'opt-b',
                                                        'text': 'To allow large, rapid initial strides when far from '
                                                                'the optimum, followed by tiny, fine-grained '
                                                                'adjustments that settle into the minimum'},
                                                    {   'id': 'opt-c',
                                                        'text': 'To prevent the design matrix from becoming singular'},
                                                    {'id': 'opt-d', 'text': 'To force all parameter weights to zero'}],
                                     'question': 'What is the primary motivation for implementing a decaying learning '
                                                 'rate schedule (such as step decay or inverse scaling \\eta_t = '
                                                 '\\frac{\\eta_0}{(1 + decay \\cdot t)^p})?',
                                     'subtopic': 'Learning Rate Schedules',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-a',
                                     'difficulty': 'medium',
                                     'explanation': 'Across one full epoch, all m observations are processed exactly '
                                                    'once under all three paradigms. Thus the total FLOPs per epoch is '
                                                    'O(m*d). The difference is in update frequency: BGD does 1 update, '
                                                    'MBGD does m/k updates, and SGD does m updates.',
                                     'id': 'q-cml-l05-16',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'Batch GD: O(m*d); Mini-Batch GD: O(m*d); SGD: O(m*d) '
                                                                '— all three require evaluating every point once per '
                                                                'epoch'},
                                                    {   'id': 'opt-b',
                                                        'text': 'Batch GD: O(d^3); Mini-Batch GD: O(d^2); SGD: O(d)'},
                                                    {   'id': 'opt-c',
                                                        'text': 'Batch GD: O(m*d); Mini-Batch GD: O(k*d); SGD: O(d)'},
                                                    {   'id': 'opt-d',
                                                        'text': 'Batch GD is O(1) because it computes a closed-form '
                                                                'formula'}],
                                     'question': 'For a dataset with m = 1,000,000 observations and d = 50 features, '
                                                 'what is the computational complexity of completing ONE full epoch '
                                                 '(one complete pass over all data) using Batch GD vs. Mini-Batch GD '
                                                 'vs. SGD?',
                                     'subtopic': 'Computational Complexity per Epoch',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-c',
                                     'difficulty': 'medium',
                                     'explanation': "Passing loss='squared_error' with penalty=None specifies the "
                                                    'exact unregularized MSE objective function J(w), solved '
                                                    'iteratively via stochastic gradient descent.',
                                     'id': 'q-cml-l05-17',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'It trains Ridge Regression with L2 regularization'},
                                                    {   'id': 'opt-b',
                                                        'text': 'It trains Lasso Regression with L1 regularization'},
                                                    {   'id': 'opt-c',
                                                        'text': 'It minimizes standard unregularized Ordinary Least '
                                                                'Squares MSE loss via iterative gradient updates'},
                                                    {   'id': 'opt-d',
                                                        'text': 'It raises an exception because regularization is '
                                                                'mandatory in SGDRegressor'}],
                                     'question': "In Scikit-Learn's SGDRegressor, what is the default behavior if the "
                                                 "argument `penalty=None` is passed with `loss='squared_error'`?",
                                     'subtopic': 'Scikit-Learn SGDRegressor',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-b',
                                     'difficulty': 'hard',
                                     'explanation': 'The error contraction matrix is (I - eta * H). For spectral '
                                                    'radius to satisfy max |1 - eta * lambda_i| < 1, we require -1 < 1 '
                                                    '- eta * lambda_max < 1, which solves directly to eta < 2 / '
                                                    'lambda_max.',
                                     'id': 'q-cml-l05-18',
                                     'options': [   {'id': 'opt-a', 'text': '\\eta < \\frac{1}{\\det(\\mathbf{H})}'},
                                                    {   'id': 'opt-b',
                                                        'text': '\\eta < \\frac{2}{\\lambda_{\\max}(\\mathbf{H})}, '
                                                                'where \\lambda_{\\max} is the largest eigenvalue of '
                                                                'the Hessian'},
                                                    {   'id': 'opt-c',
                                                        'text': '\\eta < \\frac{\\text{trace}(\\mathbf{H})}{m}'},
                                                    {   'id': 'opt-d',
                                                        'text': '\\eta < 2 \\cdot \\lambda_{\\min}(\\mathbf{H})'}],
                                     'question': 'For a quadratic loss function with Hessian matrix \\mathbf{H} = '
                                                 '\\nabla^2 J(\\mathbf{w}), what is the exact theoretical upper bound '
                                                 'on the learning rate \\eta to guarantee convergence of Batch '
                                                 'Gradient Descent?',
                                     'subtopic': 'Mathematical Convergence Bound',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-b',
                                     'difficulty': 'hard',
                                     'explanation': 'The condition number kappa = lambda_max / lambda_min = 10,000. '
                                                    'High condition numbers produce highly eccentric elliptical '
                                                    'contours, causing severe orthogonal oscillation and sluggish '
                                                    'convergence.',
                                     'id': 'q-cml-l05-19',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': '\\kappa = 1; gradient descent converges in exactly '
                                                                'one iteration'},
                                                    {   'id': 'opt-b',
                                                        'text': '\\kappa = 10,000; the loss contours form an extreme '
                                                                'ravine where gradients oscillate violently across the '
                                                                'narrow axis while making minuscule progress along the '
                                                                'flat axis'},
                                                    {   'id': 'opt-c',
                                                        'text': '\\kappa = 0.0001; the learning rate can be safely set '
                                                                'to 100'},
                                                    {   'id': 'opt-d',
                                                        'text': '\\kappa = 9,999; the loss function is non-convex and '
                                                                'possesses multiple local minima'}],
                                     'question': 'Suppose the Hessian matrix of an unscaled dataset has eigenvalues '
                                                 '\\lambda_{\\max} = 10,000 and \\lambda_{\\min} = 1. What is the '
                                                 'condition number \\kappa, and what is its effect on gradient '
                                                 'descent?',
                                     'subtopic': 'Condition Number & Ravine Geometry',
                                     'type': 'single_choice'},
                                 {   'correct_answer': 'opt-a',
                                     'difficulty': 'hard',
                                     'explanation': 'For w = [0, 0], predictions are y_hat = 0. Errors: e_1 = 0 - 5 = '
                                                    '-5; e_2 = 0 - 11 = -11. Gradient: (2/m) * sum e_i * x_i. For m=2, '
                                                    'factor (2/2)=1. grad = e_1 * x^(1) + e_2 * x^(2) = -5*[1, 2]^T + '
                                                    '-11*[1, 4]^T = [-5-11, -10-44]^T = [-16, -54]^T. Update: w^(1) = '
                                                    '[0, 0]^T - 0.05 * [-16, -54]^T = [0.8, 2.7]^T.',
                                     'id': 'q-cml-l05-20',
                                     'options': [   {'id': 'opt-a', 'text': '[0.8, 2.7]^T'},
                                                    {'id': 'opt-b', 'text': '[0.4, 1.35]^T'},
                                                    {'id': 'opt-c', 'text': '[-0.8, -2.7]^T'},
                                                    {'id': 'opt-d', 'text': '[1.6, 5.4]^T'}],
                                     'question': 'Given 2 training samples: x^{(1)} = [1, 2]^T with y^{(1)} = 5, and '
                                                 'x^{(2)} = [1, 4]^T with y^{(2)} = 11. Let initial weights be '
                                                 '\\mathbf{w} = [0, 0]^T, loss J(\\mathbf{w}) = \\frac{1}{m}\\sum '
                                                 '(\\hat{y}_i - y_i)^2, and \\eta = 0.05. What is the weight vector '
                                                 '\\mathbf{w}^{(1)} after ONE Batch GD update?',
                                     'subtopic': 'Numerical Calculation of Gradient Step',
                                     'type': 'single_choice'},
                                 {   'correct_answer': ['opt-a', 'opt-b', 'opt-c'],
                                     'difficulty': 'hard',
                                     'explanation': 'Options A, B, and C address numerical divergence. Option D is '
                                                    'incorrect: unlike the Normal Equation matrix inversion, Gradient '
                                                    'Descent functions perfectly when d > m (though it requires '
                                                    'regularization to avoid overfitting).',
                                     'id': 'q-cml-l05-21',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'The learning rate \\eta was slightly above the '
                                                                'stability threshold; reducing \\eta by a factor of '
                                                                '5-10 will prevent overflow'},
                                                    {   'id': 'opt-b',
                                                        'text': 'One or more input features were unscaled, leading to '
                                                                'explosive gradient accumulation along steep curvature '
                                                                'directions'},
                                                    {   'id': 'opt-c',
                                                        'text': 'The target response y contains massive unnormalized '
                                                                'values (e.g., millions); log-transforming or scaling '
                                                                'y will mitigate gradient scaling'},
                                                    {   'id': 'opt-d',
                                                        'text': 'The dataset has more features than samples (d > m), '
                                                                'which mathematically prevents Gradient Descent from '
                                                                'executing'}],
                                     'question': 'A data scientist runs Mini-Batch GD and observes that the training '
                                                 'loss decreases for the first 100 epochs, but at epoch 105 suddenly '
                                                 'spikes to 10^{28} and outputs NaN. Which of the following are valid '
                                                 'root causes and corrective actions?',
                                     'subtopic': 'Diagnostic Debugging of Divergence',
                                     'type': 'multi_choice'},
                                 {   'correct_answer': 'opt-b',
                                     'difficulty': 'hard',
                                     'explanation': 'The Robbins-Monro conditions require sum(eta_t) = infinity '
                                                    '(ensuring the optimizer can travel arbitrary distances to reach '
                                                    'the minimum regardless of initialization) and sum(eta_t^2) < '
                                                    'infinity (ensuring step sizes diminish sufficiently fast to '
                                                    'extinguish stochastic gradient variance).',
                                     'id': 'q-cml-l05-22',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': '\\sum_{t=1}^\\infty \\eta_t < \\infty \\quad '
                                                                '\\text{and} \\quad \\sum_{t=1}^\\infty \\eta_t^2 < '
                                                                '\\infty'},
                                                    {   'id': 'opt-b',
                                                        'text': '\\sum_{t=1}^\\infty \\eta_t = \\infty \\quad '
                                                                '\\text{and} \\quad \\sum_{t=1}^\\infty \\eta_t^2 < '
                                                                '\\infty'},
                                                    {   'id': 'opt-c',
                                                        'text': '\\lim_{t \\to \\infty} \\eta_t = 1 \\quad \\text{and} '
                                                                '\\quad \\eta_t > 0'},
                                                    {   'id': 'opt-d',
                                                        'text': '\\eta_{t+1} = \\frac{1}{2} \\eta_t \\quad \\text{for '
                                                                'all } t'}],
                                     'question': 'What are the formal Robbins-Monro conditions on the learning rate '
                                                 'sequence \\{\\eta_t\\} required to guarantee asymptotic convergence '
                                                 'of Stochastic Gradient Descent to the true minimum?',
                                     'subtopic': 'Robbins-Monro Conditions',
                                     'type': 'single_choice'},
                                 {   'correct_answer': ['opt-a', 'opt-b', 'opt-d'],
                                     'difficulty': 'hard',
                                     'explanation': 'Options A, B, and D are accurate. Option C is false: scaling does '
                                                    'not change the algebraic solution of the Normal Equation (X^T '
                                                    'X)^{-1} X^T y; scaling is only required for iterative gradient '
                                                    'descent stability.',
                                     'id': 'q-cml-l05-23',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'Normal Equations require O(d^3) operations, while '
                                                                'Gradient Descent requires O(m*d) per epoch'},
                                                    {   'id': 'opt-b',
                                                        'text': 'Gradient Descent requires hyperparameter tuning '
                                                                '(learning rate, batch size), whereas the Normal '
                                                                'Equation has zero hyperparameters'},
                                                    {   'id': 'opt-c',
                                                        'text': 'Feature scaling is strictly mandatory for the Normal '
                                                                'Equation to calculate correct weights'},
                                                    {   'id': 'opt-d',
                                                        'text': 'Mini-batch Gradient Descent can train on infinite '
                                                                'streaming data out-of-core, whereas the Normal '
                                                                'Equation requires all data in memory'}],
                                     'question': 'Which of the following statements are mathematically true regarding '
                                                 'the Normal Equation vs. Gradient Descent for linear regression?',
                                     'subtopic': 'Comparing Inversion vs Iterative Solvers',
                                     'type': 'multi_choice'},
                                 {   'correct_answer': 'opt-b',
                                     'difficulty': 'hard',
                                     'explanation': 'By the Central Limit Theorem and basic probability theory for '
                                                    'independent samples, the variance of the sample mean of k '
                                                    'independent random variables with variance sigma^2 is Var(1/k * '
                                                    'sum X_i) = (1/k^2) * k * sigma^2 = sigma^2 / k.',
                                     'id': 'q-cml-l05-24',
                                     'options': [   {'id': 'opt-a', 'text': 'k \\cdot \\sigma^2'},
                                                    {'id': 'opt-b', 'text': '\\frac{\\sigma^2}{k}'},
                                                    {'id': 'opt-c', 'text': '\\frac{\\sigma^2}{\\sqrt{k}}'},
                                                    {'id': 'opt-d', 'text': '\\sigma^2 - k'}],
                                     'question': "If the variance of a single sample's gradient in pure SGD is "
                                                 '\\sigma^2, what is the variance of the mini-batch gradient estimator '
                                                 'when using batch size k?',
                                     'subtopic': 'Variance Reduction in Mini-Batches',
                                     'type': 'single_choice'},
                                 {   'correct_answer': ['opt-a', 'opt-b', 'opt-c'],
                                     'difficulty': 'hard',
                                     'explanation': 'A, B, and C are well-documented pathological failure modes. '
                                                    'Option D is NOT a failure mode for linear regression: because the '
                                                    'MSE loss surface is convex, zero initialization w=0 is perfectly '
                                                    'safe and standard (unlike neural networks with symmetric hidden '
                                                    'units where zero initialization breaks symmetry).',
                                     'id': 'q-cml-l05-25',
                                     'options': [   {   'id': 'opt-a',
                                                        'text': 'Failing to shuffle the dataset between epochs when '
                                                                'training with Mini-Batch GD, locking the updates into '
                                                                'cyclic non-convergent oscillations'},
                                                    {   'id': 'opt-b',
                                                        'text': 'Setting \\eta > \\frac{2}{\\lambda_{\\max}}, causing '
                                                                'exponential divergence of the parameter norms'},
                                                    {   'id': 'opt-c',
                                                        'text': 'Extremely unstandardized features with scale '
                                                                'differences of 10^6, forcing the optimizer into '
                                                                'severe orthogonal oscillations across ravine walls'},
                                                    {   'id': 'opt-d',
                                                        'text': 'Initializing weights to exact zeros (\\mathbf{w} = '
                                                                '\\mathbf{0}) for linear regression'}],
                                     'question': 'Which of the following scenarios will cause a standard Gradient '
                                                 'Descent implementation on Mean Squared Error to fail or produce '
                                                 'pathological behavior?',
                                     'subtopic': 'Gradient Descent Failure Modes',
                                     'type': 'multi_choice'}],
                'time_limit': '30 mins',
                'title': 'Comprehensive Examination: Gradient Descent Optimization & Convergence Dynamics'},
    'read_time': '55 mins',
    'sections': [   {   'body': '### 1.1 The Analytical Dilemma of Modern Machine Learning\n'
                                '\n'
                                'In Lectures 3 and 4, we explored the mathematical elegance of the Ordinary Least '
                                'Squares (OLS) closed-form solution:\n'
                                '$$\\boldsymbol{\\theta}^* = (\\mathbf{X}^T \\mathbf{X})^{-1} \\mathbf{X}^T '
                                '\\mathbf{y}$$\n'
                                '\n'
                                'This formula computes the exact global minimizer of the Mean Squared Error (MSE) '
                                'objective function in a single mathematical stroke. If a closed-form formula exists, '
                                'why does the discipline of Machine Learning dedicate extensive literature to '
                                'iterative optimization algorithms like Gradient Descent?\n'
                                '\n'
                                'The answer lies at the intersection of **computational complexity**, **hardware '
                                'memory hierarchies**, and **architectural generality**:\n'
                                '\n'
                                '```\n'
                                '                         Analytical OLS vs. Iterative Gradient Descent\n'
                                '  +-------------------------------------+-------------------------------------+\n'
                                '  | OLS Closed-Form (Normal Equations)  | Iterative Gradient Descent          |\n'
                                '  +-------------------------------------+-------------------------------------+\n'
                                '  | Time Complexity: O(d^3)             | Time Complexity per Epoch: O(m * d) |\n'
                                '  | Memory Footprint: O(d^2 + m*d)      | Memory Footprint: O(batch_size * d) |\n'
                                '  | Scalability: Collapses when d>10,000| Scalability: Scales to d=10^9, m=10^9|\n'
                                '  | Generality: Linear models only      | Generality: Universally applicable  |\n'
                                '  | Closed Form: Inversion required     | First-order: Evaluates slope only   |\n'
                                '  +-------------------------------------+-------------------------------------+\n'
                                '```\n'
                                '\n'
                                '#### 1. The Dimensionality Bottleneck ($d \\gg 1$)\n'
                                'Computing the Gram matrix $\\mathbf{X}^T \\mathbf{X}$ requires $\\mathcal{O}(m \\cdot '
                                'd^2)$ floating-point operations (FLOPs). Subsequently, inverting that $(d+1) \\times '
                                '(d+1)$ matrix via Gaussian elimination, LU decomposition, or Cholesky factorization '
                                'incurs an asymptotic time complexity of $\\mathcal{O}(d^3)$.\n'
                                '- For $d = 1,000$ features, $d^3 = 10^9$ operations—easily processed by modern CPUs '
                                'in fractions of a second.\n'
                                '- For $d = 100,000$ features (typical in natural language processing, genomics, or '
                                'high-cardinality categorical embeddings), $d^3 = 10^{15}$ operations. Even on a '
                                'dedicated cluster executing $10^{12}$ FLOPs/sec, Cholesky factorization would require '
                                'over 16 minutes of sustained compute.\n'
                                '- For $d = 1,000,000$, $d^3 = 10^{18}$ FLOPs, demanding weeks of cluster compute and '
                                'petabytes of RAM simply to store the intermediate matrix.\n'
                                '\n'
                                '#### 2. The Sample Size Bottleneck ($m \\gg 1$)\n'
                                'The Normal Equation assumes that the entire design matrix $\\mathbf{X} \\in '
                                '\\mathbb{R}^{m \\times (d+1)}$ can be loaded into system RAM. In contemporary web '
                                'applications (e.g., ad click-through rate prediction, fraud detection, recommendation '
                                'engines), the dataset spans hundreds of millions to billions of rows ($m > 10^9$). '
                                'Loading hundreds of gigabytes or terabytes of tabular data simultaneously into RAM is '
                                'prohibitively expensive or physically impossible on single-node hardware.\n'
                                '\n'
                                '#### 3. Loss Non-Invertibility & Non-Linear Hypotheses\n'
                                'While linear regression yields a quadratic loss with a linear derivative that can be '
                                'set to zero and solved algebraically, the vast majority of machine learning models do '
                                '**not** yield closed-form solutions:\n'
                                '- **Logistic Regression**: The log-loss objective '
                                '$\\mathcal{L}(\\boldsymbol{\\theta}) = -\\sum [y_i '
                                '\\ln(\\sigma(\\boldsymbol{\\theta}^T \\mathbf{x}_i)) + '
                                '(1-y_i)\\ln(1-\\sigma(\\boldsymbol{\\theta}^T \\mathbf{x}_i))]$ produces '
                                'transcendental equations with no algebraic closed-form inversion.\n'
                                '- **Support Vector Machines & Neural Networks**: Non-linear activations, max-pooling '
                                'layers, and hinge losses lack analytical inverses.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 1.2 The Iterative Philosophy: Walking Down the Bowl\n'
                                '\n'
                                'Iterative optimization reframes parameter estimation from an algebraic inversion '
                                'problem into a **geometric search trajectory**:\n'
                                '1. Begin with an initial parameter estimate $\\boldsymbol{\\theta}^{(0)} \\in '
                                '\\mathbb{R}^{d+1}$ (often initialized as zeros or small random Gaussian numbers).\n'
                                '2. Compute the local slope (gradient) of the loss surface at the current position.\n'
                                '3. Take a calculated step downhill in the direction of steepest descent.\n'
                                '4. Repeat this evaluation-step cycle until the model parameters settle into the '
                                'lowest point of the loss bowl.',
                        'citations': [   'Nesterov, Y. (2018). Lectures on Convex Optimization. Springer.',
                                         'Boyd, S., & Vandenberghe, L. (2004). Convex Optimization. Cambridge '
                                         'University Press.',
                                         'Bottou, L. (2010). Large-scale machine learning with stochastic gradient '
                                         'descent. COMPSTAT 2010, 177-186.'],
                        'heading': '1. Optimization Foundations: Why Closed-Form Inversion Fails & The Necessity of '
                                   'Iterative Search',
                        'section_id': 'cml-l05-sec01'},
                    {   'body': '### 2.1 The Geometry of the Loss Surface\n'
                                '\n'
                                'Consider a simple linear model with a single feature $x_1$ and a bias term $w_0$:\n'
                                '$$\\hat{y} = w_0 + w_1 x_1$$\n'
                                '\n'
                                'The Mean Squared Error loss function $J(w_0, w_1)$ defines a surface over the 2D '
                                'parameter space $(w_0, w_1)$:\n'
                                '$$J(w_0, w_1) = \\frac{1}{m} \\sum_{i=1}^m \\left( (w_0 + w_1 x_{i1}) - y_i '
                                '\\right)^2$$\n'
                                '\n'
                                'Because $J(w_0, w_1)$ is a quadratic function of the parameters $w_0$ and $w_1$, its '
                                'graph in three dimensions forms an elliptical paraboloid—colloquially called an '
                                '**optimization bowl**:\n'
                                '\n'
                                '```\n'
                                '                       Loss Surface J(w0, w1) - The Convex Bowl\n'
                                '                           \n'
                                '                               \\                 /\n'
                                '                                \\   w_init      /\n'
                                '                                 \\    \\        /\n'
                                '                                  \\    v      /\n'
                                '                                   \\    \\    /\n'
                                '                                    \\    v  /\n'
                                '                                     \\  w* /   <-- Global Minimum (nabla J = 0)\n'
                                '                                      +---+\n'
                                '                             -----------------------\n'
                                '                               Parameter Space (w)\n'
                                '```\n'
                                '\n'
                                'In horizontal cross-sections, this bowl projects onto the $(w_0, w_1)$ plane as a '
                                'family of **concentric contour ellipses**:\n'
                                '- Every point on a given contour ellipse shares the exact same scalar loss value '
                                '$J(w_0, w_1) = C$.\n'
                                '- The center of the ellipses corresponds to the optimal parameter vector '
                                '$\\mathbf{w}^*$ where loss reaches its global minimum.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.2 Formal Definition of the Gradient Vector\n'
                                '\n'
                                'In multivariate calculus, for a differentiable scalar-valued function $J: '
                                '\\mathbb{R}^d \\to \\mathbb{R}$, the **gradient** $\\nabla_{\\mathbf{w}} '
                                'J(\\mathbf{w})$ is the column vector of all first-order partial derivatives:\n'
                                '\n'
                                '$$\\nabla_{\\mathbf{w}} J(\\mathbf{w}) = \\begin{bmatrix} \\frac{\\partial '
                                'J}{\\partial w_0} \\\\ \\frac{\\partial J}{\\partial w_1} \\\\ \\vdots \\\\ '
                                '\\frac{\\partial J}{\\partial w_d} \\end{bmatrix} \\in \\mathbb{R}^{d+1}$$\n'
                                '\n'
                                '#### Fundamental Geometric Properties of the Gradient:\n'
                                '1. **Direction of Maximum Rate of Increase**: The gradient vector $\\nabla '
                                'J(\\mathbf{w})$ points in the direction of steepest ascent. If you stand at '
                                'coordinates $\\mathbf{w}$ and take an infinitesimal step along $\\nabla '
                                'J(\\mathbf{w})$, the function value $J(\\mathbf{w})$ increases faster than in any '
                                'other possible direction.\n'
                                '2. **Orthogonality to Level Curves (Contour Lines)**: The gradient vector $\\nabla '
                                'J(\\mathbf{w})$ is mathematically orthogonal (perpendicular) to the tangent '
                                'hyperplane of the contour line at that point:\n'
                                '   $$\\nabla J(\\mathbf{w}) \\perp \\mathcal{T}_{\\mathbf{w}} \\{ \\mathbf{v} \\in '
                                '\\mathbb{R}^{d+1} \\mid J(\\mathbf{v}) = J(\\mathbf{w}) \\}$$\n'
                                '3. **Magnitude as Steepness**: The Euclidean norm $\\|\\nabla J(\\mathbf{w})\\|_2 = '
                                '\\sqrt{\\sum_{j=0}^d \\left(\\frac{\\partial J}{\\partial w_j}\\right)^2}$ quantifies '
                                'the steepness of the slope at $\\mathbf{w}$. Near the basin minimum, $\\|\\nabla '
                                'J(\\mathbf{w})\\|_2 \\to 0$.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 2.3 Why the Minus Sign? Direction of Steepest Descent\n'
                                '\n'
                                'Our engineering objective in supervised learning is **loss minimization** (finding '
                                '$\\arg\\min_{\\mathbf{w}} J(\\mathbf{w})$). \n'
                                'Because $\\nabla J(\\mathbf{w})$ points uphill (steepest ascent), moving in the '
                                'opposite direction $-\\nabla J(\\mathbf{w})$ points downhill (steepest descent).\n'
                                '\n'
                                'The general iterative update rule is defined as:\n'
                                '$$\\mathbf{w}^{(t+1)} := \\mathbf{w}^{(t)} - \\eta \\nabla_{\\mathbf{w}} '
                                'J(\\mathbf{w}^{(t)})$$\n'
                                '\n'
                                'where:\n'
                                '- $\\mathbf{w}^{(t)}$ is the parameter vector at iteration $t$.\n'
                                '- $\\eta > 0$ (Greek letter *eta*, often denoted $\\alpha$) is the **learning rate** '
                                'or step size.\n'
                                '- $\\nabla_{\\mathbf{w}} J(\\mathbf{w}^{(t)})$ is the gradient evaluated at the '
                                'current coordinates $\\mathbf{w}^{(t)}$.\n'
                                '- $:=$ denotes the in-place variable reassignment operator.\n'
                                '\n'
                                '#### Intuitive 1D Demonstration: Tangent Slope & Directional Correction\n'
                                'Consider a 1D scalar parameter $w$ and loss $J(w)$:\n'
                                '\n'
                                '```\n'
                                '           Case A: w is right of minimum             Case B: w is left of minimum\n'
                                '                     J(w)                                      J(w)\n'
                                '                    |     *                                   | *\n'
                                '                    |    / \\                                  |  \\\n'
                                '                    |   /   \\                                 |   \\\n'
                                '                    |  /  *  *  (w)                           |    * (w)\n'
                                '                    | /  /                                    |     \\  \\\n'
                                '                    |/  / Slope > 0                           |      \\  \\ Slope < '
                                '0\n'
                                '                    +-----------------                        +-----------------\n'
                                '                         w*     w                                  w     w*\n'
                                '```\n'
                                '\n'
                                '- **Case A ($w > w^*$)**: The parameter is to the right of the minimum. The tangent '
                                'line tilts upward, so the derivative $\\frac{\\partial J}{\\partial w} > 0$.\n'
                                '  - Update: $w_{\\text{new}} = w_{\\text{old}} - \\eta (\\text{positive value}) '
                                '\\implies w$ decreases, stepping left toward $w^*$.\n'
                                '- **Case B ($w < w^*$)**: The parameter is to the left of the minimum. The tangent '
                                'line tilts downward, so the derivative $\\frac{\\partial J}{\\partial w} < 0$.\n'
                                '  - Update: $w_{\\text{new}} = w_{\\text{old}} - \\eta (\\text{negative value}) = '
                                'w_{\\text{old}} + \\eta |\\text{negative value}| \\implies w$ increases, stepping '
                                'right toward $w^*$.\n'
                                '\n'
                                'In both scenarios, the negative sign automatically guides the parameter toward the '
                                'minimum! If we mistakenly used a plus sign ($\\mathbf{w} := \\mathbf{w} + \\eta '
                                '\\nabla J$), the algorithm would execute **Gradient Ascent**, running away from the '
                                'optimum toward infinite loss.',
                        'citations': [   'Cauchy, A. (1847). Méthode générale pour la résolution des systèmes '
                                         "d'équations simultanées. Comp. Rend. Sci. Paris, 25, 536-538.",
                                         'Ruder, S. (2016). An overview of gradient descent optimization algorithms. '
                                         'arXiv preprint arXiv:1609.04747.'],
                        'heading': '2. Mathematical Mechanics of Gradient Descent: Loss Geometry & The Negative '
                                   'Gradient Operator',
                        'section_id': 'cml-l05-sec02'},
                    {   'body': '### 3.1 Scalar Derivation via Single-Variable Calculus\n'
                                '\n'
                                'Let our training set comprise $m$ observations with $d$ features. The linear '
                                'prediction for sample $i$ is:\n'
                                '$$\\hat{y}_i = \\mathbf{w}^T \\mathbf{x}_i = \\sum_{k=0}^d w_k x_{ik}$$\n'
                                '\n'
                                'The empirical Mean Squared Error loss is:\n'
                                '$$J(\\mathbf{w}) = \\frac{1}{m} \\sum_{i=1}^m (\\hat{y}_i - y_i)^2$$\n'
                                '\n'
                                '*(Note: In theoretical texts, a prefactor of $\\frac{1}{2m}$ is often used so that '
                                'the exponent $2$ cancels cleanly upon differentiation. The resulting minimum '
                                '$\\mathbf{w}^*$ is mathematically identical).*\n'
                                '\n'
                                'To compute the partial derivative of $J(\\mathbf{w})$ with respect to a single '
                                'arbitrary weight $w_j$:\n'
                                '$$\\frac{\\partial J}{\\partial w_j} = \\frac{\\partial}{\\partial w_j} \\left[ '
                                '\\frac{1}{m} \\sum_{i=1}^m (\\hat{y}_i - y_i)^2 \\right]$$\n'
                                '\n'
                                'Applying the linearity of the derivative operator and the **Chain Rule** '
                                '($\\frac{d}{dw} [u(w)]^2 = 2 u(w) \\frac{du}{dw}$):\n'
                                '$$\\frac{\\partial J}{\\partial w_j} = \\frac{1}{m} \\sum_{i=1}^m 2 (\\hat{y}_i - '
                                'y_i) \\cdot \\frac{\\partial}{\\partial w_j} (\\hat{y}_i - y_i)$$\n'
                                '\n'
                                'Differentiating the internal residual $(\\hat{y}_i - y_i) = \\left(\\sum_{k=0}^d w_k '
                                'x_{ik} - y_i\\right)$ with respect to $w_j$:\n'
                                '- For all terms $k \\neq j$, the partial derivative is $0$.\n'
                                '- For $k = j$, $\\frac{\\partial}{\\partial w_j} (w_j x_{ij}) = x_{ij}$.\n'
                                '- The target $y_i$ is a constant with respect to weights, so $\\frac{\\partial '
                                'y_i}{\\partial w_j} = 0$.\n'
                                '\n'
                                'Therefore:\n'
                                '$$\\frac{\\partial (\\hat{y}_i - y_i)}{\\partial w_j} = x_{ij}$$\n'
                                '\n'
                                'Substituting this back into the summation yields the **Scalar Gradient Formula**:\n'
                                '$$\\frac{\\partial J}{\\partial w_j} = \\frac{2}{m} \\sum_{i=1}^m (\\hat{y}_i - y_i) '
                                'x_{ij}$$\n'
                                '\n'
                                '#### Physical & Pedagogical Intuition of the Derivative:\n'
                                '1. **The Error Term $(\\hat{y}_i - y_i)$**: Represents the directional error of the '
                                'model on sample $i$. If the model overshoots ($\\hat{y}_i > y_i$), the term is '
                                'positive. If the model undershoots ($\\hat{y}_i < y_i$), the term is negative.\n'
                                '2. **The Feature Multiplier $x_{ij}$**: Serves as a sensitivity amplifier. If feature '
                                '$x_{ij} = 0$, that feature contributed nothing to the error for sample $i$, so its '
                                'corresponding weight $w_j$ receives zero update from this observation. If $|x_{ij}|$ '
                                'is large, $w_j$ was heavily responsible for the prediction error, receiving an '
                                'proportionally larger update.\n'
                                '3. **The Average $\\frac{1}{m} \\sum_{i=1}^m$**: Accumulates the gradient signals '
                                'across all $m$ training samples, computing the consensus direction.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 3.2 Vectorized Derivation via Matrix Calculus\n'
                                '\n'
                                'In production data science libraries, scalar summation loops are discarded in favor '
                                'of vectorized matrix operations executed in BLAS/LAPACK.\n'
                                '\n'
                                'Let:\n'
                                '- $\\mathbf{X} \\in \\mathbb{R}^{m \\times (d+1)}$ be the full feature design '
                                'matrix.\n'
                                '- $\\mathbf{y} \\in \\mathbb{R}^{m \\times 1}$ be the target response vector.\n'
                                '- $\\mathbf{w} \\in \\mathbb{R}^{(d+1) \\times 1}$ be the weight vector.\n'
                                '- $\\hat{\\mathbf{y}} = \\mathbf{X} \\mathbf{w} \\in \\mathbb{R}^{m \\times 1}$ be '
                                'the model predictions.\n'
                                '- $\\mathbf{e} = (\\hat{\\mathbf{y}} - \\mathbf{y}) = (\\mathbf{X}\\mathbf{w} - '
                                '\\mathbf{y}) \\in \\mathbb{R}^{m \\times 1}$ be the residual error vector.\n'
                                '\n'
                                'The vector MSE cost function can be expressed as an inner product:\n'
                                '$$J(\\mathbf{w}) = \\frac{1}{m} \\|\\mathbf{X}\\mathbf{w} - \\mathbf{y}\\|_2^2 = '
                                '\\frac{1}{m} (\\mathbf{X}\\mathbf{w} - \\mathbf{y})^T (\\mathbf{X}\\mathbf{w} - '
                                '\\mathbf{y})$$\n'
                                '\n'
                                'Expanding the quadratic matrix product:\n'
                                '$$J(\\mathbf{w}) = \\frac{1}{m} \\left( \\mathbf{w}^T \\mathbf{X}^T \\mathbf{X} '
                                '\\mathbf{w} - \\mathbf{w}^T \\mathbf{X}^T \\mathbf{y} - \\mathbf{y}^T \\mathbf{X} '
                                '\\mathbf{w} + \\mathbf{y}^T \\mathbf{y} \\right)$$\n'
                                '\n'
                                'Noting that $\\mathbf{w}^T \\mathbf{X}^T \\mathbf{y}$ is a scalar, its transpose '
                                '$(\\mathbf{w}^T \\mathbf{X}^T \\mathbf{y})^T = \\mathbf{y}^T \\mathbf{X} \\mathbf{w}$ '
                                'is identical:\n'
                                '$$J(\\mathbf{w}) = \\frac{1}{m} \\left( \\mathbf{w}^T (\\mathbf{X}^T \\mathbf{X}) '
                                '\\mathbf{w} - 2 (\\mathbf{X}^T \\mathbf{y})^T \\mathbf{w} + \\mathbf{y}^T \\mathbf{y} '
                                '\\right)$$\n'
                                '\n'
                                'We apply standard matrix calculus identities:\n'
                                '- $\\nabla_{\\mathbf{w}} (\\mathbf{w}^T \\mathbf{A} \\mathbf{w}) = 2 \\mathbf{A} '
                                '\\mathbf{w}$ (for symmetric matrix $\\mathbf{A} = \\mathbf{X}^T \\mathbf{X}$)\n'
                                '- $\\nabla_{\\mathbf{w}} (\\mathbf{b}^T \\mathbf{w}) = \\mathbf{b}$\n'
                                '\n'
                                'Differentiating with respect to $\\mathbf{w}$:\n'
                                '$$\\nabla_{\\mathbf{w}} J(\\mathbf{w}) = \\frac{1}{m} \\left( 2 \\mathbf{X}^T '
                                '\\mathbf{X} \\mathbf{w} - 2 \\mathbf{X}^T \\mathbf{y} \\right) = \\frac{2}{m} '
                                '\\mathbf{X}^T (\\mathbf{X}\\mathbf{w} - \\mathbf{y})$$\n'
                                '\n'
                                '$$\\nabla_{\\mathbf{w}} J(\\mathbf{w}) = \\frac{2}{m} \\mathbf{X}^T '
                                '(\\hat{\\mathbf{y}} - \\mathbf{y})$$\n'
                                '\n'
                                '#### Matrix Dimension Verification:\n'
                                '$$\\mathbf{X}^T \\in \\mathbb{R}^{(d+1) \\times m}, \\quad (\\hat{\\mathbf{y}} - '
                                '\\mathbf{y}) \\in \\mathbb{R}^{m \\times 1} \\implies \\mathbf{X}^T '
                                '(\\hat{\\mathbf{y}} - \\mathbf{y}) \\in \\mathbb{R}^{(d+1) \\times 1}$$\n'
                                'The dimensions match the parameter vector $\\mathbf{w}$ identically.\n'
                                '\n'
                                '#### The Vectorized Gradient Descent Update Rule:\n'
                                '$$\\mathbf{w}^{(t+1)} := \\mathbf{w}^{(t)} - \\eta \\cdot \\frac{2}{m} \\mathbf{X}^T '
                                '(\\mathbf{X}\\mathbf{w}^{(t)} - \\mathbf{y})$$',
                        'citations': [   'Deisenroth, M. P., Faisal, A. A., & Ong, C. S. (2020). Mathematics for '
                                         'Machine Learning. Cambridge University Press.',
                                         'Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT '
                                         'Press.'],
                        'heading': '3. Analytical Derivation of the Mean Squared Error Gradient (Scalar & Vectorized '
                                   'Matrix Form)',
                        'section_id': 'cml-l05-sec03'},
                    {   'body': '### 4.1 The Role of the Learning Rate Hyperparameter $\\eta$\n'
                                '\n'
                                'The learning rate $\\eta > 0$ controls the step magnitude along the negative gradient '
                                'vector. It is the single most critical hyperparameter in first-order optimization.\n'
                                '\n'
                                '```\n'
                                '                           Learning Rate Regimes Comparison\n'
                                ' \n'
                                '      Loss J(w)                     Loss J(w)                     Loss J(w)\n'
                                '        |    *                        |    *                        | *       *\n'
                                '        |   / \\                       |   / \\                       |  \\     /\n'
                                '        |  /   \\                      |  /   \\                      |   *   *\n'
                                '        | *     *                     | *     *                     |    \\ /\n'
                                '        |*.......*  eta too small     |  \\   /   eta optimal        |     *     eta '
                                'too large\n'
                                '        +------------------           +------------------           '
                                '+------------------\n'
                                '         Slow crawl (10,000 steps)     Direct convergence (30 steps)  Overshoots & '
                                'explodes\n'
                                '```\n'
                                '\n'
                                '| Learning Rate Regime | Parameter Trajectory | Loss Behavior $J(\\mathbf{w})$ | '
                                'Convergence Time |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **Severely Too Small ($\\eta \\ll \\eta_{\\text{opt}}$)** | Tiny, microscopic steps '
                                'along the gradient. | Monotonically decreases at an excruciatingly slow rate. | Fails '
                                'to reach optimum within standard epoch budgets. High compute cost. |\n'
                                '| **Moderately Small ($\\eta \\lesssim \\eta_{\\text{opt}}$)** | Smooth, stable '
                                'trajectory directly toward $\\mathbf{w}^*$. | Smooth exponential decay without '
                                'oscillation. | Steady convergence; robust but could be accelerated. |\n'
                                '| **Optimal ($\\eta \\approx \\eta_{\\text{opt}}$)** | Large, decisive strides toward '
                                'the minimum. | Rapid drop, arriving near $\\mathbf{w}^*$ in minimum wall-clock time. '
                                '| Maximum efficiency. |\n'
                                '| **Moderately Large ($\\eta > \\eta_{\\text{opt}}$)** | Steps overshoot the valley '
                                'center, bouncing between walls. | Oscillates erratically; may eventually settle or '
                                'enter limit cycle. | Slowed by oscillatory ping-ponging. |\n'
                                '| **Critically Too Large ($\\eta > \\frac{2}{L}$)** | Steps overshoot further and '
                                'further outward up the opposite wall. | Loss decreases briefly, then explodes '
                                'exponentially to `+inf` / `NaN`. | **Catastrophic divergence**. |\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 4.2 The Exact Mathematical Stability Limit: Lipschitz Smoothness\n'
                                '\n'
                                'Why does Gradient Descent diverge if $\\eta$ exceeds a specific threshold? \n'
                                '\n'
                                'For a quadratic objective function $J(\\mathbf{w}) = \\frac{1}{2} \\mathbf{w}^T '
                                '\\mathbf{A} \\mathbf{w} - \\mathbf{b}^T \\mathbf{w}$, the gradient is $\\nabla '
                                'J(\\mathbf{w}) = \\mathbf{A} \\mathbf{w} - \\mathbf{b}$. The gradient itself is '
                                '**Lipschitz continuous** with constant $L = \\|\\mathbf{A}\\|_2 = '
                                '\\lambda_{\\max}(\\mathbf{A})$, where $\\lambda_{\\max}$ represents the largest '
                                'eigenvalue of the Hessian matrix $\\mathbf{H} = \\nabla^2 J(\\mathbf{w})$.\n'
                                '\n'
                                'For MSE linear regression, the Hessian is:\n'
                                '$$\\mathbf{H} = \\nabla^2 J(\\mathbf{w}) = \\frac{2}{m} \\mathbf{X}^T \\mathbf{X}$$\n'
                                '\n'
                                'Let $\\lambda_{\\max}$ be the maximum eigenvalue of $\\mathbf{H}$. The fundamental '
                                'convergence theorem of convex optimization dictates:\n'
                                '$$\\mathbf{w}^{(t)} - \\mathbf{w}^* = (\\mathbf{I} - \\eta \\mathbf{H})^t '
                                '(\\mathbf{w}^{(0)} - \\mathbf{w}^*)$$\n'
                                '\n'
                                'For the error $(\\mathbf{w}^{(t)} - \\mathbf{w}^*)$ to contract to $\\mathbf{0}$ as '
                                '$t \\to \\infty$, the spectral radius of the transition matrix $(\\mathbf{I} - \\eta '
                                '\\mathbf{H})$ must be strictly less than $1$:\n'
                                '$$|1 - \\eta \\lambda_i| < 1 \\quad \\forall i \\in \\{1, \\dots, d+1\\}$$\n'
                                '\n'
                                'Solving this inequality for all positive eigenvalues $\\lambda_i > 0$:\n'
                                '$$-1 < 1 - \\eta \\lambda_i < 1 \\implies 0 < \\eta \\lambda_i < 2 \\implies \\eta < '
                                '\\frac{2}{\\lambda_i}$$\n'
                                '\n'
                                'Because this must hold for the most extreme curvature direction:\n'
                                '$$\\eta_{\\text{critical}} = \\frac{2}{\\lambda_{\\max}(\\mathbf{H})} = '
                                '\\frac{m}{\\lambda_{\\max}(\\mathbf{X}^T \\mathbf{X})}$$\n'
                                '\n'
                                'Furthermore, the theoretically **optimal learning rate** that maximizes contraction '
                                'along both the steepest and shallowest directions is the harmonic mean of the '
                                'stability bounds:\n'
                                '$$\\eta^* = \\frac{2}{\\lambda_{\\max} + \\lambda_{\\min}}$$\n'
                                '\n'
                                'If an engineer sets $\\eta \\ge \\frac{2}{\\lambda_{\\max}}$, each step moves further '
                                'from the valley bottom than the previous step ($|1 - \\eta \\lambda_{\\max}| > 1$). '
                                'The error amplifies by a factor of $|1 - \\eta \\lambda_{\\max}|$ every single '
                                'iteration, leading to rapid numerical overflow.',
                        'citations': [   'Polyak, B. T. (1987). Introduction to Optimization. Optimization Software.',
                                         'Bengio, Y. (2012). Practical recommendations for gradient-based training of '
                                         'deep architectures. Neural Networks: Tricks of the Trade, 437-478.'],
                        'heading': '4. Learning Rate Dynamics: Stability Bounds, Divergence, Oscillation & The '
                                   'Lipschitz Constant',
                        'section_id': 'cml-l05-sec04'},
                    {   'body': '### 5.1 The Fundamental Trade-Off: Gradient Precision vs. Computational Throughput\n'
                                '\n'
                                'How many data samples should be evaluated before computing a gradient step? This '
                                'algorithmic choice divides Gradient Descent into three primary paradigms:\n'
                                '\n'
                                '```\n'
                                '                            The Gradient Descent Spectrum\n'
                                '      Batch GD (BGD)              Mini-Batch GD (MBGD)           Stochastic GD (SGD)\n'
                                '  +--------------------+        +---------------------+        '
                                '+--------------------+\n'
                                '  | Batch Size = m     |        | Batch Size = k      |        | Batch Size = 1     '
                                '|\n'
                                '  | (All data points)  |        | (e.g., 32, 64, 128) |        | (Single sample)    '
                                '|\n'
                                '  +--------------------+        +---------------------+        '
                                '+--------------------+\n'
                                '   Exact Gradient                Low Noise Gradient             Extremely Noisy\n'
                                '   O(m * d) compute              O(k * d) compute               O(d) compute\n'
                                '   Deterministic path            Mild trajectory wiggles        Jagged, erratic path\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.2 Deep Dive: Batch Gradient Descent (BGD)\n'
                                '\n'
                                'In Batch Gradient Descent, every single parameter update evaluates the sum of errors '
                                'across the **entire dataset of $m$ observations**:\n'
                                '$$\\mathbf{w}^{(t+1)} := \\mathbf{w}^{(t)} - \\eta \\cdot \\frac{2}{m} \\sum_{i=1}^m '
                                '(\\hat{y}_i - y_i) \\mathbf{x}_i$$\n'
                                '\n'
                                '#### Characteristics:\n'
                                '1. **Deterministic Loss Trajectory**: Because the gradient is computed over all $m$ '
                                'samples, $J(\\mathbf{w})$ is guaranteed to decrease monotonically at every step '
                                '(provided $\\eta \\le \\eta_{\\text{critical}}$).\n'
                                '2. **Smooth, Direct Path**: On a 2D contour plot, the optimization path descends '
                                'gracefully perpendicular to the contour rings directly toward the global minimum '
                                'without random jitter.\n'
                                '3. **Severe Computational Bottleneck**:\n'
                                '   - Each individual update requires $\\mathcal{O}(m \\cdot d)$ operations.\n'
                                '   - For $m = 10,000,000$, one single parameter update requires ten million dot '
                                'products!\n'
                                '   - Cannot process streaming data; the entire dataset must reside statically on disk '
                                'or in memory.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.3 Deep Dive: Stochastic Gradient Descent (SGD)\n'
                                '\n'
                                'In pure Stochastic Gradient Descent (introduced by Robbins & Monro, 1951), the batch '
                                'size is set to **$k = 1$**. At each iteration $t$, a single random sample '
                                '$(\\mathbf{x}_i, y_i)$ is drawn uniformly from the dataset:\n'
                                '$$\\mathbf{w}^{(t+1)} := \\mathbf{w}^{(t)} - \\eta \\cdot 2 (\\hat{y}_i - y_i) '
                                '\\mathbf{x}_i$$\n'
                                '\n'
                                '#### Characteristics:\n'
                                '1. **Blazing Step Speed**: Each parameter update costs $\\mathcal{O}(d)$ '
                                'FLOPs—instantaneous even on low-power CPUs.\n'
                                "2. **High Gradient Variance (Noise)**: A single sample's gradient is an extremely "
                                'noisy, unbiased estimator of the true population gradient:\n'
                                '   $$\\mathbb{E}_{i \\sim \\mathcal{U}(1, m)} \\left[ \\nabla J_i(\\mathbf{w}) '
                                '\\right] = \\nabla J(\\mathbf{w})$$\n'
                                '   Because individual samples may be mislabeled, unrepresentative, or noisy outliers, '
                                'the optimization trajectory resembles a drunken random walk, oscillating violently '
                                'across the loss surface.\n'
                                '3. **Escaping Saddle Points & Local Minima**: In non-convex optimization (such as '
                                'deep neural networks), this violent stochastic noise is a superpower—it kicks the '
                                'weights out of flat saddle points and shallow local traps where Batch GD would '
                                'freeze.\n'
                                '4. **Failure to Settle**: Pure SGD with a constant learning rate $\\eta$ **never '
                                'converges** to the exact minimum $\\mathbf{w}^*$. Instead, it wanders endlessly in a '
                                'limit cycle or bounding cloud around the optimum. To force SGD to settle, the '
                                'learning rate must be systematically decayed over time (satisfying the Robbins-Monro '
                                'conditions $\\sum \\eta_t = \\infty$ and $\\sum \\eta_t^2 < \\infty$).\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.4 Deep Dive: Mini-Batch Gradient Descent (MBGD)\n'
                                '\n'
                                'Mini-Batch Gradient Descent is the industry standard for production machine learning '
                                'and deep learning. Instead of using 1 point or all $m$ points, it samples a balanced '
                                'mini-batch of size $k$ (typically powers of 2: $k \\in \\{32, 64, 128, 256, '
                                '512\\}$):\n'
                                '$$\\mathbf{w}^{(t+1)} := \\mathbf{w}^{(t)} - \\eta \\cdot \\frac{2}{k} \\sum_{i \\in '
                                '\\mathcal{B}_t} (\\hat{y}_i - y_i) \\mathbf{x}_i$$\n'
                                'where $\\mathcal{B}_t \\subset \\{1, \\dots, m\\}$ is a randomly sampled subset of '
                                'cardinality $|\\mathcal{B}_t| = k$.\n'
                                '\n'
                                '#### Characteristics:\n'
                                '1. **Hardware Vectorization (SIMD & Tensor Cores)**: Modern hardware architectures '
                                '(Intel AVX-512 CPUs, NVIDIA GPUs, Google TPUs) process matrix-matrix products over '
                                'small batches in parallel with virtually the same wall-clock latency as a single '
                                'sample.\n'
                                '2. **Variance Reduction**: By the Central Limit Theorem, averaging over $k$ samples '
                                'reduces gradient estimator variance by a factor of $\\frac{1}{k}$:\n'
                                '   $$\\text{Var}\\left( \\frac{1}{k} \\sum_{i \\in \\mathcal{B}} \\nabla '
                                'J_i(\\mathbf{w}) \\right) = \\frac{\\sigma^2}{k}$$\n'
                                '   For $k = 64$, variance drops by $98.4\\%$ compared to pure SGD, suppressing wild '
                                'jitters into mild, productive ripples.\n'
                                '3. **High Convergence Velocity**: Achieves near-optimal balance—fast parameter '
                                'updates per wall-clock second combined with stable, directional trajectory '
                                'progression.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 5.5 Comprehensive Architectural Comparison Table\n'
                                '\n'
                                '| Attribute | Batch Gradient Descent (BGD) | Mini-Batch GD (MBGD) | Stochastic GD '
                                '(SGD) |\n'
                                '| :--- | :--- | :--- | :--- |\n'
                                '| **Batch Size ($k$)** | $k = m$ (full dataset) | $16 \\le k \\le 512$ (standard: '
                                '32/64) | $k = 1$ (single instance) |\n'
                                '| **Step Complexity** | $\\mathcal{O}(m \\cdot d)$ | $\\mathcal{O}(k \\cdot d)$ | '
                                '$\\mathcal{O}(d)$ |\n'
                                '| **Gradient Precision** | Exact analytical sample gradient | Low-variance Monte '
                                'Carlo approximation | High-variance noisy approximation |\n'
                                '| **Trajectory Geometry** | Perfectly smooth, direct descent | Mild wiggles, stable '
                                'directional descent | Highly erratic, jagged zig-zagging |\n'
                                '| **Memory Footprint** | Massive (stores entire dataset) | Compact (fits single batch '
                                'in cache) | Minimal (single row) |\n'
                                '| **Local Minima Escape** | Poor (trapped by local basins) | Good (mild stochastic '
                                'noise helps escape) | Excellent (violent noise escapes traps) |\n'
                                '| **Convergence at Constant $\\eta$** | Converges smoothly to exact $\\mathbf{w}^*$ | '
                                'Bounces closely around $\\mathbf{w}^*$ | Fluctuates widely around $\\mathbf{w}^*$ |\n'
                                '| **Out-of-Core / Streaming Data** | Incompatible | **Fully Supported** | **Fully '
                                'Supported** |\n'
                                '| **Production Recommendation** | Only small datasets ($m < 20,000$) | **Default '
                                'Choice for Modern ML** | Online streaming / edge devices |',
                        'citations': [   'Robbins, H., & Monro, S. (1951). A stochastic approximation method. The '
                                         'Annals of Mathematical Statistics, 22(3), 400-407.',
                                         'Bottou, L., Curtis, F. E., & Nocedal, J. (2018). Optimization methods for '
                                         'large-scale machine learning. SIAM Review, 60(2), 223-311.'],
                        'heading': '5. Gradient Descent Variants: Batch, Stochastic (SGD) & Mini-Batch (MBGD)',
                        'section_id': 'cml-l05-sec05'},
                    {   'body': '### 6.1 The Geometry of Ravines: Unscaled vs. Scaled Features\n'
                                '\n'
                                'In Lecture 2 and Lecture 4, we emphasized the necessity of feature scaling. Here, we '
                                'unveil the exact geometric and optimization rationale: **how unscaled features '
                                'distort the loss landscape into an ill-conditioned ravine**.\n'
                                '\n'
                                'Suppose we predict house price ($y$) using two features:\n'
                                '- Feature 1: Number of bedrooms, $x_1 \\in [1, 5]$ (scale $\\sim 10^0$).\n'
                                '- Feature 2: Square footage, $x_2 \\in [500, 5000]$ (scale $\\sim 10^3$).\n'
                                '\n'
                                'Let us analyze the second partial derivatives (curvatures) of MSE with respect to '
                                'weights $w_1$ and $w_2$:\n'
                                '$$\\frac{\\partial^2 J}{\\partial w_1^2} = \\frac{2}{m} \\sum_{i=1}^m x_{i1}^2 '
                                '\\approx \\mathcal{O}(10^1)$$\n'
                                '$$\\frac{\\partial^2 J}{\\partial w_2^2} = \\frac{2}{m} \\sum_{i=1}^m x_{i2}^2 '
                                '\\approx \\mathcal{O}(10^7)$$\n'
                                '\n'
                                'The curvature along the $w_2$ axis is **one million times steeper** than along the '
                                '$w_1$ axis!\n'
                                '\n'
                                '```\n'
                                '      Unscaled Features: Highly Eccentric Ravine        Scaled Features: Concentric '
                                'Hypersphere\n'
                                '               (Condition Number kappa >> 1)                          (Condition '
                                'Number kappa approx 1)\n'
                                ' \n'
                                '         w2 ^                                                w2 ^\n'
                                '            |       /-------------------\\                       |        /-------\\\n'
                                '            |      /                     \\                      |       /         '
                                '\\\n'
                                '            |     |   *   *   *   *       |                     |      |     *     |  '
                                '<-- Steps point\n'
                                '            |      \\                     /                      |       \\         '
                                '/      directly to w*\n'
                                '            |       \\-------------------/                       |        \\-------/\n'
                                '            +------------------------------> w1                 '
                                '+------------------------------> w1\n'
                                '               Oscillates violently across                         Descends smoothly '
                                'in few\n'
                                '               walls, crawls along bottom                          iterations\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 6.2 The Orthogonal Oscillation Phenomenon\n'
                                '\n'
                                'When the loss contours are elongated ellipses (an anisotropic valley or "ravine"):\n'
                                '1. The gradient vector $\\nabla J(\\mathbf{w})$ is perpendicular to the tangent of '
                                'the contour ellipse.\n'
                                '2. For an eccentric ellipse, perpendicular vectors point **almost entirely toward the '
                                'opposite valley wall**, rather than down the longitudinal floor of the ravine toward '
                                'the global minimum $\\mathbf{w}^*$.\n'
                                '3. When Gradient Descent executes an update:\n'
                                '   - The large gradient component along $w_2$ hurls the parameter across the ravine '
                                'to the opposing wall.\n'
                                '   - At the opposite wall, the gradient reverses direction, hurls the parameter back '
                                'again.\n'
                                '   - Meanwhile, the minuscule gradient component along $w_1$ makes negligible '
                                'progress along the valley floor.\n'
                                '4. **The Dilemma**:\n'
                                '   - If you increase $\\eta$ to speed up progress along $w_1$, the algorithm diverges '
                                'along $w_2$ and explodes.\n'
                                '   - If you decrease $\\eta$ to prevent divergence along $w_2$, the algorithm crawls '
                                'along $w_1$, taking hundreds of thousands of epochs to converge.\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 6.3 Mathematical Restoration via Z-Score Standardization\n'
                                '\n'
                                'When features are standardized using Z-score normalization ($z = \\frac{x - '
                                '\\mu}{\\sigma}$):\n'
                                '$$\\mathbb{E}[z_j] = 0, \\quad \\text{Var}(z_j) = 1 \\quad \\forall j \\in \\{1, '
                                '\\dots, d\\}$$\n'
                                '\n'
                                'The off-diagonal elements of the covariance matrix shrink, and the eigenvalues of the '
                                'Hessian matrix become roughly equal:\n'
                                '$$\\lambda_1 \\approx \\lambda_2 \\approx \\dots \\approx \\lambda_d \\implies '
                                '\\kappa(\\mathbf{H}) = \\frac{\\lambda_{\\max}}{\\lambda_{\\min}} \\approx 1$$\n'
                                '\n'
                                '#### Benefits of Conditioning:\n'
                                '- Contours transform from narrow elliptical canyons into **circular hyperspheres**.\n'
                                '- The negative gradient $-\\nabla J(\\mathbf{w})$ points **directly toward the global '
                                'center $\\mathbf{w}^*$**.\n'
                                '- Orthogonal bouncing vanishes.\n'
                                '- A single, aggressive learning rate $\\eta$ can be utilized, accelerating '
                                'convergence by several orders of magnitude.',
                        'citations': [   'LeCun, Y. A., Bottou, L., Orr, G. B., & Müller, K. R. (2012). Efficient '
                                         'backprop. Neural Networks: Tricks of the Trade, 9-48.',
                                         'Ioffe, S., & Szegedy, C. (2015). Batch normalization: Accelerating deep '
                                         'network training by reducing internal covariate shift. ICML 2015, 448-456.'],
                        'heading': '6. Geometric Pitfalls: Loss Landscape Conditioning, Ravines, Zig-Zagging & Feature '
                                   'Standardization',
                        'section_id': 'cml-l05-sec06'},
                    {   'body': '### 7.1 Engineering Stopping Criteria\n'
                                '\n'
                                'In practical machine learning applications, algorithms do not run for an arbitrary '
                                'fixed number of steps. Instead, automated **stopping criteria** terminate execution '
                                'when convergence is achieved:\n'
                                '\n'
                                '#### 1. Gradient Norm Threshold ($\\|\\nabla J(\\mathbf{w})\\|_2 < \\epsilon$)\n'
                                'At the true global minimum, the gradient is exactly zero: $\\nabla J(\\mathbf{w}^*) = '
                                '\\mathbf{0}$. We monitor the Euclidean $L_2$ norm of the gradient vector:\n'
                                '$$\\|\\nabla J(\\mathbf{w}^{(t)})\\|_2 = \\sqrt{\\sum_{j=0}^d \\left( '
                                '\\frac{\\partial J}{\\partial w_j} \\right)^2} < \\epsilon_{\\text{grad}}$$\n'
                                'where $\\epsilon_{\\text{grad}}$ is a small user-defined tolerance (e.g., $10^{-4}$ '
                                'or $10^{-6}$).\n'
                                '\n'
                                '#### 2. Relative Loss Improvement Criterion ($\\Delta J < \\text{tol}$)\n'
                                'When the loss function flattens out and successive iterations yield negligible '
                                'improvements:\n'
                                '$$\\frac{|J(\\mathbf{w}^{(t)}) - J(\\mathbf{w}^{(t-1)})|}{J(\\mathbf{w}^{(t-1)}) + '
                                '\\epsilon} < \\text{tol}$$\n'
                                'If this relative change remains below $\\text{tol} = 10^{-5}$ for $P$ consecutive '
                                'evaluations (a "patience" window), optimization halts.\n'
                                '\n'
                                '#### 3. Parameter Displacement Criterion ($\\|\\mathbf{w}^{(t)} - '
                                '\\mathbf{w}^{(t-1)}\\|_2 < \\epsilon_{\\text{step}}$)\n'
                                'Monitors whether the parameter vector has stopped moving in coordinate space:\n'
                                '$$\\|\\mathbf{w}^{(t)} - \\mathbf{w}^{(t-1)}\\|_2 < \\epsilon_{\\text{step}}$$\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 7.2 Dynamic Learning Rate Schedules\n'
                                '\n'
                                'A static, unchanging learning rate $\\eta$ is inherently suboptimal:\n'
                                '- **Early Phase**: Parameters are far from the minimum; a large $\\eta$ is desirable '
                                'to traverse long distances rapidly.\n'
                                '- **Late Phase**: Parameters arrive in the neighborhood of $\\mathbf{w}^*$; a large '
                                '$\\eta$ causes overshooting or endless stochastic bouncing. A decaying $\\eta$ is '
                                'required to settle cleanly into the basin minimum.\n'
                                '\n'
                                '```\n'
                                '                           Common Learning Rate Decay Schedules\n'
                                ' \n'
                                '      Learning Rate eta(t)\n'
                                '        |  +---------------+\n'
                                '        |  |               \\\n'
                                '        |  | Step Decay     \\              Exponential Decay\n'
                                '        |  |                 +----------\\  eta(t) = eta_0 * e^(-k*t)\n'
                                '        |  |                             \\\n'
                                '        |  |                              +--------\\\n'
                                '        |  \\~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Cosine Annealing\n'
                                '        +----------------------------------------------------> Epochs\n'
                                '```\n'
                                '\n'
                                '#### 1. Step Decay (Piecewise Constant)\n'
                                'Reduces the learning rate by a multiplicative factor $\\gamma \\in (0, 1)$ (e.g., '
                                '$\\gamma = 0.5$ or $0.1$) every $E$ epochs:\n'
                                '$$\\eta_t = \\eta_0 \\cdot \\gamma^{\\lfloor t / E \\rfloor}$$\n'
                                '\n'
                                '#### 2. Exponential Decay\n'
                                'Continuously decays the learning rate smoothly across every epoch:\n'
                                '$$\\eta_t = \\eta_0 \\cdot e^{-k \\cdot t}$$\n'
                                'where $k > 0$ is the decay rate constant.\n'
                                '\n'
                                '#### 3. Inverse Time Decay (Scikit-Learn Standard)\n'
                                'Popularized by Leon Bottou for stochastic gradient descent on convex objectives:\n'
                                '$$\\eta_t = \\frac{\\eta_0}{(1 + \\text{decay} \\cdot t)^p}$$\n'
                                "Scikit-Learn's `SGDRegressor` implements this with power $p = 0.25$ under the setting "
                                "`learning_rate='invscaling'`.\n"
                                '\n'
                                '#### 4. Cosine Annealing (Loshchilov & Hutter, 2016)\n'
                                'Follows a cosine curve down to a minimum floor $\\eta_{\\min}$:\n'
                                '$$\\eta_t = \\eta_{\\min} + \\frac{1}{2}(\\eta_0 - \\eta_{\\min}) \\left(1 + '
                                '\\cos\\left(\\frac{t}{T_{\\max}} \\pi\\right)\\right)$$\n'
                                'Widely favored in deep learning for its smooth deceleration toward the minimum.',
                        'citations': [   'Loshchilov, I., & Hutter, F. (2016). SGDR: Stochastic gradient descent with '
                                         'warm restarts. arXiv preprint arXiv:1608.03983.',
                                         'Prechelt, L. (1998). Early stopping—but when? Neural Networks: Tricks of the '
                                         'Trade, 55-69.'],
                        'heading': '7. Convergence Diagnostics, Stopping Criteria & Learning Rate Schedules',
                        'section_id': 'cml-l05-sec07'},
                    {   'body': '### 8.1 Pure NumPy Implementation: Vectorized Mini-Batch Gradient Descent\n'
                                '\n'
                                'Below is a production-grade, vectorized implementation of Mini-Batch Gradient Descent '
                                'with feature scaling, early stopping, and loss history tracking:\n'
                                '\n'
                                '```python\n'
                                'import numpy as np\n'
                                '\n'
                                'class MiniBatchLinearRegressionGD:\n'
                                "    '''\n"
                                '    Vectorized Linear Regression solved via Mini-Batch Gradient Descent.\n'
                                '    \n'
                                '    Parameters:\n'
                                '    -----------\n'
                                '    learning_rate : float, default=0.01\n'
                                '        Step size along the negative gradient.\n'
                                '    batch_size : int, default=32\n'
                                '        Number of samples per mini-batch update.\n'
                                '    max_epochs : int, default=1000\n'
                                '        Maximum passes over the entire training dataset.\n'
                                '    tol : float, default=1e-5\n'
                                '        Early stopping tolerance on relative loss change.\n'
                                '    patience : int, default=5\n'
                                '        Number of consecutive epochs with relative loss change < tol before '
                                'stopping.\n'
                                '    random_state : int, default=42\n'
                                '        Seed for reproducible mini-batch shuffling.\n'
                                "    '''\n"
                                '    def __init__(self, learning_rate=0.01, batch_size=32, max_epochs=1000, \n'
                                '                 tol=1e-5, patience=5, random_state=42):\n'
                                '        self.learning_rate = learning_rate\n'
                                '        self.batch_size = batch_size\n'
                                '        self.max_epochs = max_epochs\n'
                                '        self.tol = tol\n'
                                '        self.patience = patience\n'
                                '        self.random_state = random_state\n'
                                '        self.weights = None\n'
                                '        self.intercept = None\n'
                                '        self.loss_history = []\n'
                                '        \n'
                                '    def fit(self, X, y):\n'
                                '        rng = np.random.RandomState(self.random_state)\n'
                                '        m, d = X.shape\n'
                                '        \n'
                                '        # Initialize parameters: w in R^d as small Gaussian, bias as 0\n'
                                '        self.weights = rng.normal(loc=0.0, scale=0.01, size=d)\n'
                                '        self.intercept = 0.0\n'
                                '        \n'
                                '        patience_counter = 0\n'
                                '        best_loss = np.inf\n'
                                '        \n'
                                '        for epoch in range(self.max_epochs):\n'
                                '            # Shuffle dataset at the beginning of each epoch\n'
                                '            indices = rng.permutation(m)\n'
                                '            X_shuffled = X[indices]\n'
                                '            y_shuffled = y[indices]\n'
                                '            \n'
                                '            # Mini-batch iteration\n'
                                '            for start_idx in range(0, m, self.batch_size):\n'
                                '                end_idx = min(start_idx + self.batch_size, m)\n'
                                '                X_b = X_shuffled[start_idx:end_idx]\n'
                                '                y_b = y_shuffled[start_idx:end_idx]\n'
                                '                k = len(y_b)\n'
                                '                \n'
                                '                # Predictions and residual error: e = y_hat - y\n'
                                '                y_hat = np.dot(X_b, self.weights) + self.intercept\n'
                                '                errors = y_hat - y_b\n'
                                '                \n'
                                '                # Vectorized gradients\n'
                                '                grad_w = (2.0 / k) * np.dot(X_b.T, errors)\n'
                                '                grad_b = (2.0 / k) * np.sum(errors)\n'
                                '                \n'
                                '                # In-place parameter updates\n'
                                '                self.weights -= self.learning_rate * grad_w\n'
                                '                self.intercept -= self.learning_rate * grad_b\n'
                                '                \n'
                                '            # Compute full-dataset epoch loss for monitoring\n'
                                '            full_preds = np.dot(X, self.weights) + self.intercept\n'
                                '            epoch_loss = np.mean((full_preds - y) ** 2)\n'
                                '            self.loss_history.append(epoch_loss)\n'
                                '            \n'
                                '            # Early stopping diagnostic check\n'
                                '            rel_change = abs(best_loss - epoch_loss) / (best_loss + 1e-12)\n'
                                '            if rel_change < self.tol:\n'
                                '                patience_counter += 1\n'
                                '                if patience_counter >= self.patience:\n'
                                '                    print(f"Early stopping triggered at epoch {epoch}. Final MSE: '
                                '{epoch_loss:.6f}")\n'
                                '                    break\n'
                                '            else:\n'
                                '                patience_counter = 0\n'
                                '                \n'
                                '            if epoch_loss < best_loss:\n'
                                '                best_loss = epoch_loss\n'
                                '                \n'
                                '        return self\n'
                                '    \n'
                                '    def predict(self, X):\n'
                                '        return np.dot(X, self.weights) + self.intercept\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 8.2 Scikit-Learn Production Pipeline: `SGDRegressor`\n'
                                '\n'
                                'In production pipelines, Scikit-Learn provides `SGDRegressor`, which incorporates '
                                'optimized Cython routines, multiple loss formulations, and automated learning rate '
                                'schedules:\n'
                                '\n'
                                '```python\n'
                                'from sklearn.linear_model import SGDRegressor\n'
                                'from sklearn.preprocessing import StandardScaler\n'
                                'from sklearn.pipeline import Pipeline\n'
                                'from sklearn.metrics import mean_squared_error, r2_score\n'
                                'from sklearn.datasets import fetch_california_housing\n'
                                'from sklearn.model_selection import train_test_split\n'
                                '\n'
                                '# 1. Load enterprise dataset\n'
                                'housing = fetch_california_housing(as_frame=True)\n'
                                'X, y = housing.data, housing.target\n'
                                '\n'
                                'X_train, X_test, y_train, y_test = train_test_split(\n'
                                '    X, y, test_size=0.2, random_state=42\n'
                                ')\n'
                                '\n'
                                '# 2. Build Pipeline: Feature Scaling is MANDATORY for Gradient Descent!\n'
                                'sgd_pipeline = Pipeline([\n'
                                '    ("scaler", StandardScaler()),\n'
                                '    ("sgd", SGDRegressor(\n'
                                '        loss="squared_error",       # Standard MSE loss J(w)\n'
                                '        penalty=None,               # Pure unregularized OLS optimization\n'
                                '        learning_rate="invscaling", # eta_t = eta0 / (t^power_t)\n'
                                '        eta0=0.01,                  # Initial step size\n'
                                '        power_t=0.25,               # Bottou inverse-scaling exponent\n'
                                '        max_iter=2000,              # Epoch ceiling\n'
                                '        tol=1e-4,                   # Convergence stopping threshold\n'
                                '        random_state=42\n'
                                '    ))\n'
                                '])\n'
                                '\n'
                                '# 3. Train and Evaluate\n'
                                'sgd_pipeline.fit(X_train, y_train)\n'
                                'y_pred_test = sgd_pipeline.predict(X_test)\n'
                                '\n'
                                'mse = mean_squared_error(y_test, y_pred_test)\n'
                                'r2 = r2_score(y_test, y_pred_test)\n'
                                '\n'
                                'print(f"SGD Test MSE: {mse:.4f}")\n'
                                'print(f"SGD Test R^2: {r2:.4f}")\n'
                                'print(f"Total iterations to converge: {sgd_pipeline.named_steps[\'sgd\'].n_iter_}")\n'
                                '```\n'
                                '\n'
                                '---\n'
                                '\n'
                                '### 8.3 Production Checklist: Debugging Failing Gradient Descent\n'
                                '\n'
                                "If your model's loss fails to converge or explodes in production, run this diagnostic "
                                'checklist:\n'
                                '\n'
                                '1. **Did you standardize your features?**\n'
                                '   - Check `X.mean()` and `X.std()`. If standard deviations differ by more than a '
                                'factor of $5$, fit a `StandardScaler`.\n'
                                '2. **Is your learning rate $\\eta$ too large?**\n'
                                '   - If loss oscillates or outputs `NaN` / `inf`, immediately divide $\\eta$ by 10. '
                                'Repeat until loss decreases monotonically.\n'
                                '3. **Is your learning rate $\\eta$ too small?**\n'
                                '   - If loss decreases by less than $0.0001\\%$ over 50 epochs and remains far above '
                                'benchmark OLS error, multiply $\\eta$ by 5.\n'
                                '4. **Did you shuffle data between epochs in mini-batch training?**\n'
                                '   - Failing to shuffle mini-batches traps the optimization trajectory in cyclic '
                                'correlations, preventing convergence.\n'
                                '5. **Are target values unscaled?**\n'
                                '   - In datasets where $y \\in [10^6, 10^9]$ (e.g., corporate revenue), gradients '
                                '$(\\hat{y} - y)\\mathbf{x}$ will scale to $10^{15}$, instantly causing numerical '
                                'overflow even with $\\eta = 10^{-6}$. Normalize or log-transform $y$.',
                        'citations': [   'Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. '
                                         'Journal of Machine Learning Research, 12, 2825-2830.',
                                         'Harris, C. R., et al. (2020). Array programming with NumPy. Nature, '
                                         '585(7825), 357-362.'],
                        'heading': '8. Industrial Implementation: Vectorized NumPy Solvers, Scikit-Learn SGDRegressor '
                                   '& Production Best Practices',
                        'section_id': 'cml-l05-sec08'}],
    'slug': 'cml-t5-l05',
    'status': 'published',
    'subject': 'Classical Machine Learning',
    'subject_code': 'CML',
    'summary': 'An exhaustive, mathematically rigorous, and production-oriented masterclass on Gradient Descent '
               'optimization for machine learning. Explores why closed-form matrix inversions fail at enterprise '
               'scale, formalizes the calculus and multivariate geometry of gradient operators on convex MSE surfaces, '
               'proves the exact scalar and vectorized gradient update rules, diagnoses learning rate dynamics '
               '(understepping, critical stability thresholds, and numerical explosion), contrasts Batch, Stochastic, '
               'and Mini-Batch variants across variance-computation trade-offs, analyzes loss surface conditioning and '
               'ravine oscillation, investigates modern learning rate schedules, and implements high-throughput NumPy '
               'and Scikit-Learn optimizers.',
    'term': 'Term 5',
    'title': '5. Gradient Descent Optimization: Batch, Stochastic, Mini-Batch & Convergence Dynamics'}

