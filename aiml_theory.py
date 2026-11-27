================================================================================
FOUNDATIONS OF ARTIFICIAL INTELLIGENCE & MACHINE LEARNING (CSE3001P)
THEORY, PROCEDURE, PSEUDOCODE & CONCLUSION (EXPERIMENTS 01 - 10)
================================================================================

--------------------------------------------------------------------------------
EXPERIMENT 01: SUPERVISED LEARNING (LINEAR & LOGISTIC REGRESSION)
--------------------------------------------------------------------------------

Aim:
To implement supervised learning using Linear Regression and Logistic Regression in Python with the Scikit-learn library.

Theory:
Supervised learning trains models on labeled input-output pairs (X, y) to map unseen inputs to accurate predictions:
1. Linear Regression: Models a continuous target variable y as a linear function of input feature x using y = m*x + c, where m is the slope (coefficient) and c is the y-intercept. Parameters are learned via Ordinary Least Squares (OLS) by minimizing the Residual Sum of Squares between actual and predicted values.
2. Logistic Regression: Models binary classification problems (e.g., 0 = Fail, 1 = Pass) by passing the linear combination z = m*x + c through the Sigmoid activation function:
   sigma(z) = 1 / (1 + e^(-z))
   This maps real-valued outputs into probabilities between 0 and 1, using a default classification threshold of 0.5.

Procedure:
1. Import NumPy, Matplotlib, and LinearRegression / LogisticRegression from sklearn.linear_model.
2. Create the regression dataset mapping study hours X to continuous test scores y, and plot a scatter chart.
3. Initialize LinearRegression(), train it with fit(X, y), print coef_ and intercept_, predict marks for 9 study hours, and plot the fitted regression line.
4. Create the binary classification dataset mapping study hours X_cls to outcomes y_cls (0 = Fail, 1 = Pass).
5. Initialize LogisticRegression(), train with fit(X_cls, y_cls), and predict both the class label (predict) and class probabilities (predict_proba) for 4.5 study hours.
6. Generate 100 evenly spaced points using np.linspace() and plot the S-shaped sigmoid probability curve alongside actual data points.

Pseudocode:
BEGIN
    IMPORT numpy, matplotlib.pyplot, LinearRegression, LogisticRegression

    // Part A: Linear Regression
    INITIALIZE X <- [[1], [2], ..., [8]], y <- [35, 40, ..., 85]
    PLOT SCATTER(X, y)
    CREATE lin_model <- LinearRegression()
    TRAIN lin_model.FIT(X, y)
    PRINT lin_model.coef_, lin_model.intercept_
    COMPUTE pred_marks <- lin_model.PREDICT([[9]])
    PLOT regression line (X, lin_model.PREDICT(X))

    // Part B: Logistic Regression
    INITIALIZE X_cls <- [[1], [2], ..., [8]], y_cls <- [0, 0, 0, 0, 1, 1, 1, 1]
    CREATE log_model <- LogisticRegression()
    TRAIN log_model.FIT(X_cls, y_cls)
    COMPUTE pred_class <- log_model.PREDICT([[4.5]])
    COMPUTE probs <- log_model.PREDICT_PROBA([[4.5]])
    GENERATE X_test <- LINSPACE(1, 8, 100)
    PLOT classification probability curve (X_test, log_model.PREDICT_PROBA(X_test)[:, 1])
END

Conclusion:
Successfully implemented Linear Regression and Logistic Regression using Scikit-learn, demonstrating how supervised regression predicts continuous numeric values while classification estimates discrete class probabilities using a sigmoid curve.


--------------------------------------------------------------------------------
EXPERIMENT 02: UNSUPERVISED LEARNING (K-MEANS CLUSTERING & PCA)
--------------------------------------------------------------------------------

Aim:
To apply unsupervised learning using K-Means Clustering and Principal Component Analysis (PCA) on the Iris dataset using Python and Scikit-learn.

Theory:
Unsupervised learning discovers hidden patterns and groupings in unlabeled data:
1. K-Means Clustering: Partitions n observations into k distinct clusters by minimizing Within-Cluster Sum of Squares (WCSS / Inertia), defined as the sum of squared Euclidean distances from each point to its assigned cluster centroid. The algorithm iteratively assigns points to the nearest centroid and recomputes centroids as cluster means until convergence.
2. Principal Component Analysis (PCA): A linear dimensionality reduction technique that projects high-dimensional correlated features onto orthogonal axes (principal components) ordered by maximum variance, enabling 2D visualization of multi-feature clusters.

Procedure:
1. Import NumPy, Matplotlib, load_iris from sklearn.datasets, KMeans from sklearn.cluster, and PCA from sklearn.decomposition.
2. Load the 4-feature Iris dataset (150 samples across 3 species) without target labels.
3. Initialize KMeans(n_clusters=3, random_state=42, n_init=10) and fit it to feature matrix X.
4. Extract cluster assignments via kmeans.labels_, centroid coordinates via kmeans.cluster_centers_, and compactness score via kmeans.inertia_.
5. Initialize PCA(n_components=2) and project the 4D Iris features into 2D space using fit_transform(X).
6. Plot a 2D scatter plot of Principal Component 1 vs Principal Component 2 colored by cluster labels.

Pseudocode:
BEGIN
    IMPORT numpy, matplotlib.pyplot, load_iris, KMeans, PCA
    LOAD iris <- load_iris()
    SET X <- iris.data

    // K-Means Clustering
    CREATE kmeans <- KMeans(n_clusters=3, random_state=42, n_init=10)
    TRAIN kmeans.FIT(X)
    GET labels <- kmeans.labels_
    GET centers <- kmeans.cluster_centers_
    PRINT labels, centers, kmeans.inertia_

    // Dimensionality Reduction & Visualization
    CREATE pca <- PCA(n_components=2)
    COMPUTE X_pca <- pca.FIT_TRANSFORM(X)
    PLOT SCATTER(X_pca[:, 0], X_pca[:, 1], color=labels)
END

Conclusion:
Successfully applied K-Means Clustering to group unlabeled Iris samples into three compact clusters and used PCA to project four-dimensional features into a clear two-dimensional cluster visualization.


--------------------------------------------------------------------------------
EXPERIMENT 03: ARTIFICIAL NEURAL NETWORK (ANN) FROM SCRATCH
--------------------------------------------------------------------------------

Aim:
To design and implement a multi-layer Artificial Neural Network (ANN) from scratch using NumPy to solve the non-linear XOR problem.

Theory:
The XOR (Exclusive OR) logic gate outputs 1 when inputs differ and 0 when inputs match. Because XOR is not linearly separable, a single-layer perceptron cannot solve it; at least one hidden layer with a non-linear activation function is required.
Training proceeds in two passes over multiple epochs:
1. Forward Propagation: Computes weighted sums z = X*W + b and applies the Sigmoid activation sigma(z) = 1 / (1 + e^(-z)) across hidden and output layers.
2. Backpropagation & Gradient Descent: Computes output error (y - y_hat), propagates gradients backward using the sigmoid derivative sigma'(x) = x*(1 - x) via the chain rule, and updates weights and biases by W = W + lr * grad.

Procedure:
1. Import NumPy and define the 4x2 XOR input matrix X and 4x1 target vector y.
2. Define sigmoid(x) and its derivative sigmoid_derivative(x) = x * (1 - x).
3. Initialize network dimensions (2 input neurons, 4 hidden neurons, 1 output neuron) with random weights (W1, W2) and zero biases (b1, b2), setting learning_rate = 0.5 and epochs = 10000.
4. Inside the training loop, perform forward propagation to compute hidden_output and predicted_output.
5. Compute output_delta and hidden_delta using element-wise multiplication with sigmoid derivatives, and update W2, b2, W1, and b1.
6. After 10,000 epochs, display rounded predicted probabilities and thresholded binary class predictions (>= 0.5).

Pseudocode:
BEGIN
    IMPORT numpy
    DEFINE X <- [[0,0], [0,1], [1,0], [1,1]], y <- [[0], [1], [1], [0]]
    DEFINE sigmoid(x) <- 1 / (1 + EXP(-x))
    DEFINE sigmoid_derivative(x) <- x * (1 - x)

    INITIALIZE W1 (2x4), b1 (1x4), W2 (4x1), b2 (1x1)
    SET learning_rate <- 0.5, epochs <- 10000

    FOR epoch <- 1 TO epochs DO
        // Forward Pass
        hidden_output <- sigmoid(DOT(X, W1) + b1)
        predicted_output <- sigmoid(DOT(hidden_output, W2) + b2)

        // Backward Pass
        error <- y - predicted_output
        output_delta <- error * sigmoid_derivative(predicted_output)
        hidden_delta <- DOT(output_delta, TRANSPOSE(W2)) * sigmoid_derivative(hidden_output)

        // Parameter Updates
        W2 <- W2 + learning_rate * DOT(TRANSPOSE(hidden_output), output_delta)
        b2 <- b2 + learning_rate * SUM(output_delta, axis=0)
        W1 <- W1 + learning_rate * DOT(TRANSPOSE(X), hidden_delta)
        b1 <- b1 + learning_rate * SUM(hidden_delta, axis=0)
    END FOR

    PRINT ROUND(predicted_output, 3)
    PRINT (predicted_output >= 0.5) AS INTEGER
END

Conclusion:
Successfully built and trained a multi-layer Artificial Neural Network from scratch in NumPy, demonstrating how forward propagation, non-linear sigmoid activation, and backpropagation solve the non-linearly separable XOR problem.


--------------------------------------------------------------------------------
EXPERIMENT 04: ACTIVATION FUNCTIONS (SIGMOID, RELU, TANH) WITH PLOTS
--------------------------------------------------------------------------------

Aim:
To implement, visualize, and analyze Sigmoid, ReLU, and Tanh activation functions using Python, NumPy, and Matplotlib.

Theory:
Activation functions introduce non-linearity into neural networks so multi-layer architectures can approximate complex non-linear mappings:
1. Sigmoid: f(x) = 1 / (1 + e^(-x)). Maps inputs to (0, 1) with an S-shaped curve. Used in binary classification output layers; prone to vanishing gradients for extreme inputs.
2. ReLU (Rectified Linear Unit): f(x) = max(0, x). Outputs 0 for x < 0 and x for x >= 0 (range [0, inf)). Computationally fast and mitigates vanishing gradients in hidden layers, though susceptible to the "dying ReLU" issue for negative inputs.
3. Tanh (Hyperbolic Tangent): f(x) = tanh(x). Maps inputs to (-1, 1) and is zero-centered, often yielding faster hidden-layer convergence than Sigmoid.

Procedure:
1. Import NumPy and Matplotlib (pyplot).
2. Generate 100 evenly spaced input values x between -10 and 10 using np.linspace(-10, 10, 100).
3. Compute outputs for Sigmoid (1 / (1 + np.exp(-x))), ReLU (np.maximum(0, x)), and Tanh (np.tanh(x)).
4. Create a 1x3 subplot grid using plt.subplot(1, 3, i) and plot each activation curve with titles, axis labels, legends, and gridlines.
5. Display the plots using plt.show() and print a comparative summary of output ranges and use cases.

Pseudocode:
BEGIN
    IMPORT numpy, matplotlib.pyplot
    GENERATE x <- LINSPACE(-10, 10, 100)

    COMPUTE sigmoid <- 1 / (1 + EXP(-x))
    COMPUTE relu <- MAXIMUM(0, x)
    COMPUTE tanh <- TANH(x)

    CREATE FIGURE(figsize=(12, 4))
    SUBPLOT(1, 3, 1): PLOT(x, sigmoid) WITH title="Sigmoid Activation"
    SUBPLOT(1, 3, 2): PLOT(x, relu) WITH title="ReLU Activation"
    SUBPLOT(1, 3, 3): PLOT(x, tanh) WITH title="Tanh Activation"
    DISPLAY FIGURE

    PRINT comparative analysis of ranges and neural network layer applications
END

Conclusion:
Successfully plotted and compared Sigmoid, ReLU, and Tanh activation functions, illustrating their distinct output ranges, zero-centering behavior, and roles in hidden and output layers of neural networks.


--------------------------------------------------------------------------------
EXPERIMENT 05: PROBLEM-SOLVING AGENT (VACUUM CLEANER WORLD)
--------------------------------------------------------------------------------

Aim:
To design and implement a goal-driven problem-solving simple reflex agent for the two-room Vacuum Cleaner World in Python.

Theory:
An intelligent agent perceives its environment through sensors and acts upon it through actuators to achieve a goal state. In the classic Vacuum Cleaner World, the environment consists of two locations (Room A and Room B), each either 'Dirty' or 'Clean'.
A simple reflex agent selects actions solely based on the current percept using condition-action rules:
- If current room == 'Dirty' -> Action: 'Suck' (update room to 'Clean').
- Else if current room == 'Clean' -> Action: 'Right' (if in A) or 'Left' (if in B).
- Terminate once the environment matches the goal state {'A': 'Clean', 'B': 'Clean'}.

Procedure:
1. Represent the environment state as a Python dictionary {'A': 'Dirty', 'B': 'Dirty'}, initial location as 'A', and goal_state as {'A': 'Clean', 'B': 'Clean'}.
2. Define the vacuum_agent(location, env) function containing a while loop that runs until env == goal_state.
3. At each iteration, perceive env[location]. If 'Dirty', execute 'Suck' and set env[location] = 'Clean'.
4. If 'Clean', move to the adjacent room ('Right' to 'B' if at 'A', or 'Left' to 'A' if at 'B').
5. Print the current location, percept, chosen action, and updated environment at each step until the goal state is reached.

Pseudocode:
BEGIN
    INITIALIZE environment <- {'A': 'Dirty', 'B': 'Dirty'}
    INITIALIZE current_location <- 'A'
    DEFINE goal_state <- {'A': 'Clean', 'B': 'Clean'}

    FUNCTION vacuum_agent(location, env)
        WHILE env != goal_state DO
            percept <- env[location]
            IF percept == 'Dirty' THEN
                action <- 'Suck'
                env[location] <- 'Clean'
            ELSE
                IF location == 'A' THEN
                    action <- 'Right'
                    location <- 'B'
                ELSE
                    action <- 'Left'
                    location <- 'A'
                END IF
            END IF
            PRINT location, percept, action, env
        END WHILE
        PRINT "Goal State Achieved!"
    END FUNCTION

    CALL vacuum_agent(current_location, environment)
END

Conclusion:
Successfully designed and simulated a problem-solving agent for the Vacuum Cleaner World, demonstrating perception-action cycles and rule-based state transitions toward a defined goal state.


--------------------------------------------------------------------------------
EXPERIMENT 06: RATIONAL AGENT SIMULATION (TRAFFIC SIGNAL MANAGEMENT)
--------------------------------------------------------------------------------

Aim:
To simulate a rational intelligent agent in a four-way traffic intersection environment using Python.

Theory:
A rational agent selects actions that maximize an expected performance measure given its current percept sequence and built-in domain knowledge. In automated traffic signal control, the performance measure is minimizing vehicle congestion and waiting time across North, South, East, and West approaches.
By mapping perceived vehicle density levels to proportional green-light durations (High -> 60s, Medium -> 40s, Low -> 20s), the agent allocates intersection capacity rationally according to real-time demand.

Procedure:
1. Define traffic_environment as a dictionary mapping four directions ('North', 'South', 'East', 'West') to traffic density levels ('High', 'Low', 'Medium', 'Low').
2. Define the traffic_signal_agent(environment) function to inspect each road's perceived traffic density.
3. Apply conditional decision rules (if-elif-else) to assign green_time = 60 seconds for 'High', 40 seconds for 'Medium', and 20 seconds for 'Low'.
4. Print the initial environment, per-direction density percepts, chosen signal action, and allocated green duration.

Pseudocode:
BEGIN
    DEFINE traffic_environment <- {'North': 'High', 'South': 'Low', 'East': 'Medium', 'West': 'Low'}

    FUNCTION traffic_signal_agent(environment)
        PRINT "Traffic Signal Agent Started"
        FOR EACH direction, density IN environment DO
            IF density == 'High' THEN
                green_time <- 60
            ELSE IF density == 'Medium' THEN
                green_time <- 40
            ELSE
                green_time <- 20
            END IF
            PRINT direction, density, "Action: Green Signal", green_time
        END FOR
        PRINT "Traffic management completed."
    END FUNCTION

    CALL traffic_signal_agent(traffic_environment)
END

Conclusion:
Successfully simulated a rational traffic signal management agent that perceives road congestion levels and allocates optimal green-signal durations to maximize intersection throughput.


--------------------------------------------------------------------------------
EXPERIMENT 07: NON-GRADIENT OPTIMIZATION (GENETIC ALGORITHM)
--------------------------------------------------------------------------------

Aim:
To solve a mathematical maximization problem f(x) = x^2 for integer x in [0, 31] using a Genetic Algorithm (GA) in Python.

Theory:
A Genetic Algorithm is a population-based metaheuristic optimization technique inspired by natural selection and genetics. Unlike gradient descent, GAs do not require differentiable objective functions.
Key evolutionary operators include:
1. Encoding & Fitness: Candidate solutions are encoded as 5-bit binary chromosomes (representing integers 0 to 31) and evaluated via fitness function f(x) = x^2.
2. Selection: Tournament selection compares random candidates and retains the fitter parent.
3. Crossover: One-point crossover exchanges chromosome segments between two parents at a random split point with probability CROSSOVER_RATE (0.8).
4. Mutation: Bit-flip mutation inverts individual bits with low probability MUTATION_RATE (0.05) to maintain genetic diversity and avoid local optima.

Procedure:
1. Import random and matplotlib.pyplot, and configure GA hyperparameters (BITS=5, POPULATION_SIZE=10, GENERATIONS=30, CROSSOVER_RATE=0.8, MUTATION_RATE=0.05).
2. Implement helper functions: create_chromosome(), decode() (binary list to base-10 integer), fitness() (x^2), select() (binary tournament), crossover() (one-point), and mutate() (bit-flip).
3. Initialize a population of 10 random 5-bit chromosomes and iterate over 30 generations.
4. In each generation, record the best chromosome's x value and fitness, then build the next generation via selection, crossover, and mutation.
5. Print the best final chromosome (11111 -> x = 31, fitness = 961) and plot the convergence curve across generations.

Pseudocode:
BEGIN
    IMPORT random, matplotlib.pyplot
    SET BITS <- 5, POP_SIZE <- 10, GENERATIONS <- 30, CROSSOVER_RATE <- 0.8, MUTATION_RATE <- 0.05

    FUNCTION decode(chrom): RETURN INT(JOIN(chrom), base=2)
    FUNCTION fitness(chrom): RETURN decode(chrom)^2

    INITIALIZE population <- [random 5-bit chromosomes of size POP_SIZE]
    FOR gen <- 1 TO GENERATIONS DO
        best <- ARGMAX(population, key=fitness)
        APPEND fitness(best) TO history
        new_pop <- []
        WHILE LEN(new_pop) < POP_SIZE DO
            p1, p2 <- TOURNAMENT_SELECT(population)
            c1, c2 <- ONE_POINT_CROSSOVER(p1, p2, CROSSOVER_RATE)
            APPEND MUTATE(c1, MUTATION_RATE) AND MUTATE(c2, MUTATION_RATE) TO new_pop
        END WHILE
        population <- new_pop
    END FOR

    PRINT best chromosome, best x, maximum fitness
    PLOT LINE(1..GENERATIONS, history)
END

Conclusion:
Successfully implemented a Genetic Algorithm to maximize f(x) = x^2, converging to the global optimum x = 31 (chromosome 11111, fitness = 961) through selection, crossover, and mutation.


--------------------------------------------------------------------------------
EXPERIMENT 08: CONSTRAINT-BASED OPTIMIZATION (RESOURCE ALLOCATION)
--------------------------------------------------------------------------------

Aim:
To formulate and solve a linear constraint-based resource allocation problem using Python, PuLP, and the HiGHS solver.

Theory:
Constraint-based optimization (Linear Programming) seeks to maximize or minimize a linear objective function subject to linear equality and inequality constraints over non-negative decision variables.
In this capital allocation model, investments A, B, and C (in thousands) are allocated across three projects to:
- Maximize Profit: Z = 8A + 6B + 5C
- Subject to Total Budget: A + B + C <= 100
- Individual Caps: 0 <= A <= 50, 0 <= B <= 40, 0 <= C <= 60
The HiGHS / CBC simplex solver finds the exact global optimal allocation at a feasible region vertex (A = 50, B = 40, C = 10 -> Max Profit = 690).

Procedure:
1. Import the pulp library and initialize a maximization problem via pulp.LpProblem("Resource_Allocation", pulp.LpMaximize).
2. Define continuous non-negative decision variables A, B, and C using pulp.LpVariable(..., lowBound=0).
3. Add the linear objective function 8*A + 6*B + 5*C to the problem.
4. Add the total budget constraint (A + B + C <= 100) and individual project upper bounds (A <= 50, B <= 40, C <= 60).
5. Solve the model using the HiGHS solver (with CBC fallback) and print the solver status, optimal project investments, total budget used, and maximum profit.

Pseudocode:
BEGIN
    IMPORT pulp
    CREATE problem <- LpProblem("Resource_Allocation", LpMaximize)

    DEFINE A <- LpVariable("Project_A", lowBound=0)
    DEFINE B <- LpVariable("Project_B", lowBound=0)
    DEFINE C <- LpVariable("Project_C", lowBound=0)

    SET OBJECTIVE: problem += 8*A + 6*B + 5*C
    ADD CONSTRAINTS:
        A + B + C <= 100
        A <= 50
        B <= 40
        C <= 60

    SOLVE problem USING HiGHS_SOLVER
    PRINT Status, A.varValue, B.varValue, C.varValue, Total_Investment, Objective_Value
END

Conclusion:
Successfully modeled and solved a constrained resource allocation problem using PuLP and HiGHS, achieving an optimal profit of 690 by allocating 50, 40, and 10 thousand units to Projects A, B, and C respectively.


--------------------------------------------------------------------------------
EXPERIMENT 09: MINI PROJECT - SPAM DETECTION USING MACHINE LEARNING
--------------------------------------------------------------------------------

Aim:
To build and evaluate an NLP-based SMS/Email Spam Detection classifier using TF-IDF feature extraction and Multinomial Naive Bayes in Python.

Theory:
Text classification converts unstructured natural language messages into numerical feature vectors:
1. TF-IDF (Term Frequency-Inverse Document Frequency): Weights words by their frequency within a document penalized by their prevalence across the corpus, highlighting discriminative spam keywords ("lottery", "urgent", "free").
2. Multinomial Naive Bayes: A probabilistic generative classifier applying Bayes' Theorem with conditional feature independence assumptions, well-suited for discrete word-frequency and TF-IDF representations.

Procedure:
1. Import TfidfVectorizer, MultinomialNB, train_test_split, accuracy_score, and classification_report from Scikit-learn.
2. Prepare the labeled corpus of text messages (1 = Spam, 0 = Ham) and transform text into TF-IDF feature vectors removing English stop words.
3. Split the dataset into training (70%) and testing (30%) subsets using train_test_split().
4. Train a MultinomialNB classifier on the training set and evaluate accuracy and precision/recall on the test set.
5. Run live inference on unseen sample messages to classify them as SPAM or HAM.

Pseudocode:
BEGIN
    IMPORT TfidfVectorizer, MultinomialNB, train_test_split, accuracy_score, classification_report
    DEFINE messages, labels (1=Spam, 0=Ham)

    CREATE vectorizer <- TfidfVectorizer(stop_words="english")
    COMPUTE X_vec <- vectorizer.FIT_TRANSFORM(messages)
    SPLIT X_train, X_test, y_train, y_test <- train_test_split(X_vec, labels, test_size=0.3)

    CREATE clf <- MultinomialNB()
    TRAIN clf.FIT(X_train, y_train)
    COMPUTE y_pred <- clf.PREDICT(X_test)
    PRINT accuracy_score(y_test, y_pred), classification_report(y_test, y_pred)

    TRANSFORM new_samples AND PREDICT Spam/Ham labels
END

Conclusion:
Successfully developed an end-to-end Spam Detection pipeline combining TF-IDF text vectorization and Multinomial Naive Bayes to classify unseen messages accurately.


--------------------------------------------------------------------------------
EXPERIMENT 10: CAPSTONE PROJECT - CREDIT CARD FRAUD DETECTION APPLICATION
--------------------------------------------------------------------------------

Aim:
To build and deploy an end-to-end Credit Card Fraud Detection application using feature scaling, Random Forest classification, and real-time transaction scoring in Python.

Theory:
Financial fraud detection is an imbalanced binary classification task where fraudulent transactions represent a minority class:
1. Feature Standardization: StandardScaler normalizes transaction attributes (amount, time delta, distance, merchant risk, device score) to zero mean and unit variance.
2. Random Forest Classifier: An ensemble bagging algorithm that trains multiple decision trees on bootstrapped data subsets and aggregates their votes, reducing variance and capturing complex non-linear fraud interactions.
3. Evaluation & Deployment: Model performance is assessed via Confusion Matrix, Precision, Recall, and F1-score, wrapped in a reusable inference function returning both binary alert status and fraud probability.

Procedure:
1. Generate a synthetic imbalanced transaction dataset (500 records, 5 features, 15% fraud ratio) using make_classification() and structure it into a Pandas DataFrame.
2. Perform a stratified 75/25 train-test split so both sets preserve the exact fraud class ratio.
3. Fit StandardScaler on training features and transform both training and test sets.
4. Train a RandomForestClassifier(n_estimators=100, random_state=42) and evaluate predictions using accuracy_score, confusion_matrix, and classification_report.
5. Implement a predict_transaction(tx_features) inference function that scales incoming transaction inputs and outputs a LEGITIMATE or FRAUD ALERT decision with probability.

Pseudocode:
BEGIN
    IMPORT make_classification, train_test_split, StandardScaler, RandomForestClassifier, metrics
    GENERATE X, y <- make_classification(n_samples=500, n_features=5, weights=[0.85, 0.15])
    SPLIT X_train, X_test, y_train, y_test <- train_test_split(X, y, test_size=0.25, stratify=y)

    CREATE scaler <- StandardScaler()
    SET X_train_scaled <- scaler.FIT_TRANSFORM(X_train)
    SET X_test_scaled <- scaler.TRANSFORM(X_test)

    CREATE rf_model <- RandomForestClassifier(n_estimators=100, random_state=42)
    TRAIN rf_model.FIT(X_train_scaled, y_train)
    COMPUTE y_pred <- rf_model.PREDICT(X_test_scaled)
    PRINT accuracy, confusion_matrix, classification_report

    FUNCTION predict_transaction(tx_features)
        scaled_tx <- scaler.TRANSFORM([tx_features])
        pred <- rf_model.PREDICT(scaled_tx)[0]
        prob <- rf_model.PREDICT_PROBA(scaled_tx)[0][1]
        RETURN alert status AND prob
    END FUNCTION

    CALL predict_transaction(sample_transaction)
END

Conclusion:
Successfully built and tested a Credit Card Fraud Detection application using Scikit-learn's Random Forest classifier, complete with stratified validation, confusion matrix diagnostics, and a real-time transaction risk-scoring function.
