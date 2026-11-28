irm https://raw.githubusercontent.com/aayushgabhane/dse/main/aiml.py -o aiml.py; irm https://raw.githubusercontent.com/aayushgabhane/dse/main/aiml_theory.txt -o aiml_theory.txt; notepad aiml.py; notepad aiml_theory.txt

sleep 5; Add-Type -AssemblyName System.Windows.Forms; Add-Type -MemberDefinition '[DllImport("user32.dll")]public static extern short GetAsyncKeyState(int v);' -Name K -Namespace W; (gcb -Raw).ToCharArray() | % { if ([W.K]::GetAsyncKeyState(0x1B) -ne 0) { break }; if ($_ -ne [char]13) { $k = if ($_ -eq [char]10) {'{ENTER}'} elseif ($_ -match '[+^%~(){}\[\]]') {'{' + $_ + '}'} else {$_}; [Windows.Forms.SendKeys]::SendWait($k); sleep -m 25 } }

# ==============================================================================
# EXPERIMENT 01 - SUPERVISED LEARNING (LINEAR & LOGISTIC REGRESSION)
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression

# --- Part A: Linear Regression ---
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
y = np.array([35, 40, 50, 55, 65, 70, 78, 85])

plt.figure(figsize=(6, 4))
plt.scatter(X, y)
plt.xlabel("Hours of Study")
plt.ylabel("Test Scores")
plt.title("Hours of Study vs Test Scores")
plt.show()

lin_model = LinearRegression()
lin_model.fit(X, y)

print("Linear Regression Coefficient:", lin_model.coef_[0])
print("Linear Regression Intercept:", lin_model.intercept_)

prediction = lin_model.predict([[9]])
print("Predicted marks for 9 hours:", prediction[0])

plt.figure(figsize=(6, 4))
plt.scatter(X, y, label="Actual Data")
plt.plot(X, lin_model.predict(X), color="red", label="Regression Line")
plt.xlabel("Hours Studied")
plt.ylabel("Marks")
plt.title("Linear Regression")
plt.legend()
plt.show()

# --- Part B: Logistic Regression ---
X_cls = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
y_cls = np.array([0, 0, 0, 0, 1, 1, 1, 1])  # 0 = Fail, 1 = Pass

plt.figure(figsize=(6, 4))
plt.scatter(X_cls, y_cls)
plt.xlabel("Hours Studied")
plt.ylabel("Result (0 = Fail, 1 = Pass)")
plt.title("Study Hours vs Result")
plt.show()

log_model = LogisticRegression()
log_model.fit(X_cls, y_cls)

print("\nLogistic Regression Coefficient:", log_model.coef_[0][0])
print("Logistic Regression Intercept:", log_model.intercept_[0])

pred_cls = log_model.predict([[4.5]])
print("Predicted result for 4.5 hours:", pred_cls[0], "->", "Pass" if pred_cls[0] == 1 else "Fail")

prob = log_model.predict_proba([[4.5]])
print("Probability of Fail:", prob[0][0])
print("Probability of Pass:", prob[0][1])

X_test = np.linspace(1, 8, 100).reshape(-1, 1)
probabilities = log_model.predict_proba(X_test)[:, 1]

plt.figure(figsize=(6, 4))
plt.scatter(X_cls, y_cls, label="Actual Data")
plt.plot(X_test, probabilities, color="green", label="Classification Curve")
plt.xlabel("Hours Studied")
plt.ylabel("Probability of Passing")
plt.title("Logistic Regression")
plt.legend()
plt.show()


# ==============================================================================
# EXPERIMENT 02 - UNSUPERVISED LEARNING (K-MEANS CLUSTERING & PCA)
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

iris = load_iris()
X = iris.data

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(X)

labels = kmeans.labels_
print("Cluster Labels:\n", labels)
print("\nCluster Centers:\n", kmeans.cluster_centers_)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

plt.figure(figsize=(8, 5))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap="viridis", s=50)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("K-Means Clustering on Iris Dataset")
plt.colorbar(label="Cluster")
plt.show()

print("\nInertia:", kmeans.inertia_)


# ==============================================================================
# EXPERIMENT 03 - ARTIFICIAL NEURAL NETWORK (ANN) FROM SCRATCH (XOR PROBLEM)
# ==============================================================================
import numpy as np

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

np.random.seed(42)
input_neurons = 2
hidden_neurons = 4
output_neurons = 1

W1 = np.random.randn(input_neurons, hidden_neurons)
b1 = np.zeros((1, hidden_neurons))
W2 = np.random.randn(hidden_neurons, output_neurons)
b2 = np.zeros((1, output_neurons))

learning_rate = 0.5
epochs = 10000

for epoch in range(epochs):
    # Forward propagation
    hidden_input = np.dot(X, W1) + b1
    hidden_output = sigmoid(hidden_input)
    final_input = np.dot(hidden_output, W2) + b2
    predicted_output = sigmoid(final_input)

    # Error & Backpropagation
    error = y - predicted_output
    output_delta = error * sigmoid_derivative(predicted_output)
    hidden_delta = np.dot(output_delta, W2.T) * sigmoid_derivative(hidden_output)

    # Update weights and biases
    W2 += learning_rate * np.dot(hidden_output.T, output_delta)
    b2 += learning_rate * np.sum(output_delta, axis=0, keepdims=True)
    W1 += learning_rate * np.dot(X.T, hidden_delta)
    b1 += learning_rate * np.sum(hidden_delta, axis=0, keepdims=True)

print("Predictions after training:\n", np.round(predicted_output, 3))
print("\nActual outputs:\n", y)
print("\nPredicted classes:\n", (predicted_output >= 0.5).astype(int))


# ==============================================================================
# EXPERIMENT 04 - ACTIVATION FUNCTIONS (SIGMOID, RELU, TANH) WITH PLOTS
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 100)

sigmoid = 1 / (1 + np.exp(-x))
relu = np.maximum(0, x)
tanh = np.tanh(x)

plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.plot(x, sigmoid, label="Sigmoid", color="blue")
plt.title("Sigmoid Activation")
plt.xlabel("Input")
plt.ylabel("Output")
plt.grid(True)
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(x, relu, label="ReLU", color="orange")
plt.title("ReLU Activation")
plt.xlabel("Input")
plt.ylabel("Output")
plt.grid(True)
plt.legend()

plt.subplot(1, 3, 3)
plt.plot(x, tanh, label="Tanh", color="green")
plt.title("Tanh Activation")
plt.xlabel("Input")
plt.ylabel("Output")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

print("ANALYSIS OF ACTIVATION FUNCTIONS")
print("---------------------------------")
print("1. Sigmoid: Output ranges from 0 to 1. Used mainly in binary classification output layers.")
print("2. ReLU: Output is 0 for negative inputs and x for positive inputs. Commonly used in hidden layers.")
print("3. Tanh: Output ranges from -1 to 1. Zero-centered and commonly used in hidden layers.")


# ==============================================================================
# EXPERIMENT 05 - PROBLEM-SOLVING AGENT (VACUUM CLEANER WORLD)
# ==============================================================================
environment = {"A": "Dirty", "B": "Dirty"}
current_location = "A"
goal_state = {"A": "Clean", "B": "Clean"}

def vacuum_agent(location, env):
    print("Initial Environment:", env)
    print("Initial Location:", location)

    while env != goal_state:
        percept = env[location]
        print("\nCurrent Location:", location)
        print("Percept:", percept)

        if percept == "Dirty":
            action = "Suck"
            env[location] = "Clean"
            print("Action:", action)
        else:
            if location == "A":
                action = "Right"
                location = "B"
            else:
                action = "Left"
                location = "A"
            print("Action:", action)

        print("Updated Environment:", env)

    print("\nGoal State Achieved!")
    print("Final Environment:", env)
    print("Both rooms are clean. Problem Solved Successfully.")

vacuum_agent(current_location, environment)


# ==============================================================================
# EXPERIMENT 06 - RATIONAL AGENT SIMULATION (TRAFFIC SIGNAL MANAGEMENT)
# ==============================================================================
traffic_environment = {
    "North": "High",
    "South": "Low",
    "East": "Medium",
    "West": "Low"
}

def traffic_signal_agent(environment):
    print("Traffic Signal Agent Started")
    print("\nTraffic Environment:")
    for direction, density in environment.items():
        print(direction, ":", density)

    print("\nAgent Decisions:")
    for direction, density in environment.items():
        if density == "High":
            green_time = 60
        elif density == "Medium":
            green_time = 40
        else:
            green_time = 20

        print(f"\nDirection: {direction} | Traffic Density: {density} -> Action: Green Signal ({green_time} seconds)")

    print("\nTraffic management completed. Rational Agent Stopped.")

traffic_signal_agent(traffic_environment)


# ==============================================================================
# EXPERIMENT 07 - NON-GRADIENT OPTIMIZATION (GENETIC ALGORITHM: MAX f(x) = x^2)
# ==============================================================================
import random
import matplotlib.pyplot as plt

BITS = 5
POPULATION_SIZE = 10
GENERATIONS = 30
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.05

def create_chromosome():
    return [random.randint(0, 1) for _ in range(BITS)]

def decode(chromosome):
    return int("".join(map(str, chromosome)), 2)

def fitness(chromosome):
    x = decode(chromosome)
    return x ** 2

def select(population):
    c1, c2 = random.choice(population), random.choice(population)
    return c1.copy() if fitness(c1) > fitness(c2) else c2.copy()

def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, BITS - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
    return parent1.copy(), parent2.copy()

def mutate(chromosome):
    for i in range(BITS):
        if random.random() < MUTATION_RATE:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

random.seed(42)
population = [create_chromosome() for _ in range(POPULATION_SIZE)]
best_fitness_history = []

for generation in range(GENERATIONS):
    best_chrom = max(population, key=fitness)
    best_x = decode(best_chrom)
    best_score = fitness(best_chrom)
    best_fitness_history.append(best_score)
    print(f"Generation {generation + 1}: Best x = {best_x}, Fitness = {best_score}")

    new_population = []
    while len(new_population) < POPULATION_SIZE:
        p1, p2 = select(population), select(population)
        c1, c2 = crossover(p1, p2)
        new_population.append(mutate(c1))
        if len(new_population) < POPULATION_SIZE:
            new_population.append(mutate(c2))
    population = new_population

best_chrom = max(population, key=fitness)
print("\n========== FINAL RESULT ==========")
print("Best Chromosome:", "".join(map(str, best_chrom)))
print("Best Value of x:", decode(best_chrom))
print("Maximum Fitness:", fitness(best_chrom))
print("Theoretical Maximum Fitness:", 31 ** 2)

plt.figure(figsize=(8, 5))
plt.plot(range(1, GENERATIONS + 1), best_fitness_history, marker="o")
plt.title("Genetic Algorithm Convergence")
plt.xlabel("Generation")
plt.ylabel("Best Fitness")
plt.grid(True)
plt.show()


# ==============================================================================
# EXPERIMENT 08 - CONSTRAINT-BASED OPTIMIZATION (RESOURCE ALLOCATION - PULP)
# ==============================================================================
# Run in Colab first if needed: !pip install -q "pulp[highs]"
import pulp

problem = pulp.LpProblem("Resource_Allocation", pulp.LpMaximize)

# Decision variables (in thousands)
A = pulp.LpVariable("Project_A", lowBound=0)
B = pulp.LpVariable("Project_B", lowBound=0)
C = pulp.LpVariable("Project_C", lowBound=0)

# Objective function: Maximize total profit
problem += 8 * A + 6 * B + 5 * C

# Constraints
problem += A + B + C <= 100  # Total budget
problem += A <= 50           # Max investment Project A
problem += B <= 40           # Max investment Project B
problem += C <= 60           # Max investment Project C

try:
    solver = pulp.HiGHS(msg=False)
    problem.solve(solver)
except Exception:
    problem.solve(pulp.PULP_CBC_CMD(msg=False))

print("\nRESOURCE ALLOCATION RESULTS")
print("---------------------------")
print("Status:", pulp.LpStatus[problem.status])
print("Investment in Project A:", A.varValue, "thousand")
print("Investment in Project B:", B.varValue, "thousand")
print("Investment in Project C:", C.varValue, "thousand")
print("Total Investment:", A.varValue + B.varValue + C.varValue, "thousand")
print("Maximum Profit:", pulp.value(problem.objective))


# ==============================================================================
# EXPERIMENT 09 - MINI PROJECT: SPAM DETECTION USING ML (TF-IDF + NAIVE BAYES)
# ==============================================================================
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

messages = [
    "Congratulations! You won a free lottery ticket. Claim now!",
    "Hey, are we still meeting at the library at 4 PM?",
    "URGENT! Your bank account is suspended. Click here to verify.",
    "Can you send me the AIML lab manual PDF?",
    "Win cash prizes instantly! Reply YES to enter.",
    "Don't forget to submit the assignment before tonight.",
    "Exclusive deal! Get 90% off luxury watches today only.",
    "Let's grab coffee after the afternoon practical exam.",
    "Free entry in a weekly competition to win an iPhone!",
    "Please review the attached project report and share feedback."
]
labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 1 = Spam, 0 = Ham

vectorizer = TfidfVectorizer(stop_words="english")
X_vec = vectorizer.fit_transform(messages)

X_train, X_test, y_train, y_test = train_test_split(X_vec, labels, test_size=0.3, random_state=42)
clf = MultinomialNB()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print("Spam Detection Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

sample = ["Claim your free cash reward now!", "See you in Lab 545 tomorrow."]
sample_preds = clf.predict(vectorizer.transform(sample))
for msg, p in zip(sample, sample_preds):
    print(f"Message: '{msg}' -> {'SPAM' if p == 1 else 'HAM'}")


# ==============================================================================
# EXPERIMENT 10 - CAPSTONE PROJECT: CREDIT CARD FRAUD DETECTION APPLICATION
# ==============================================================================
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

X, y = make_classification(
    n_samples=500, n_features=5, n_informative=3, n_redundant=1,
    weights=[0.85, 0.15], random_state=42
)
feature_names = ["Transaction_Amount", "Time_Since_Last_Tx", "Distance_From_Home", "Merchant_Risk", "Device_Score"]
df_fraud = pd.DataFrame(X, columns=feature_names)
df_fraud["Fraud"] = y

X_train, X_test, y_train, y_test = train_test_split(
    df_fraud[feature_names], df_fraud["Fraud"], test_size=0.25, random_state=42, stratify=df_fraud["Fraud"]
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

y_pred = rf_model.predict(X_test_scaled)
print("Fraud Detection Accuracy:", round(accuracy_score(y_test, y_pred) * 100, 2), "%")
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

def predict_transaction(tx_features):
    scaled = scaler.transform(pd.DataFrame([tx_features], columns=feature_names))
    pred = rf_model.predict(scaled)[0]
    prob = rf_model.predict_proba(scaled)[0][1]
    return f"Prediction: {'FRAUD ALERT' if pred == 1 else 'LEGITIMATE'} (Fraud Probability: {prob:.2%})"

print(predict_transaction([2.5, -1.2, 3.1, 1.8, -0.9]))
