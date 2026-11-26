powershell -c "sleep 5; Add-Type -AssemblyName System.Windows.Forms; Add-Type -MemberDefinition '[DllImport(\"user32.dll\")]public static extern short GetAsyncKeyState(int v);' -Name K -Namespace W; (gcb -Raw).ToCharArray() | % { if ([W.K]::GetAsyncKeyState(0x1B) -ne 0) { break }; if ($_ -ne [char]13) { $k = if ($_ -eq [char]10) {'{ENTER}'} elseif ($_ -match '[+^%~(){}\[\]]') {'{' + $_ + '}'} else {$_}; [Windows.Forms.SendKeys]::SendWait($k); sleep -m 25 } }"


# ==============================================================================
# EXP 01 (Lab 1) - PART A: NORMAL DISTRIBUTION
# ==============================================================================
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(42)
mean, std, n = 50, 10, 1000

# 1. Generate normal data and summarize
df = pd.DataFrame({"Values": rng.normal(mean, std, n)})
print(df.head(10), "\n")
print(df.describe(), "\n")
print(
    f"Mean: {df['Values'].mean():.4f} | "
    f"Var: {df['Values'].var():.4f} | "
    f"Std: {df['Values'].std():.4f}"
)

# 2. Plot sample histogram + theoretical normal PDF
x = np.linspace(mean - 4 * std, mean + 4 * std, 500)
pdf = stats.norm.pdf(x, loc=mean, scale=std)
plt.hist(df["Values"], bins=30, density=True, edgecolor="black", alpha=0.6, label="Sample")
plt.plot(x, pdf, linewidth=2, label="Normal PDF")
plt.xlabel("Value")
plt.ylabel("Probability Density")
plt.title("Normal Distribution")
plt.legend()
plt.tight_layout()
plt.show()


# ==============================================================================
# EXP 01 (Lab 1) - PART B: BINOMIAL DISTRIBUTION
# ==============================================================================
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import binom

rng = np.random.default_rng(42)
n, p, size = 10, 0.5, 1000

# 1. Simulate binomial trials and summarize
df = pd.DataFrame({"Successes": rng.binomial(n, p, size)})
print(df.head(10), "\n")
print(df.describe(), "\n")
print(
    f"Sample Mean: {df['Successes'].mean():.4f} | "
    f"Sample Std: {df['Successes'].std():.4f}"
)

# 2. Exact and cumulative probabilities for k = 6
print(f"P(X = 6): {binom.pmf(6, n, p):.4f}")
print(f"P(X <= 6): {binom.cdf(6, n, p):.4f}")

# 3. Plot theoretical PMF across all possible counts
x = np.arange(0, n + 1)
plt.bar(x, binom.pmf(x, n, p), edgecolor="black")
plt.xlabel("Number of Successes")
plt.ylabel("Probability")
plt.title(f"Binomial PMF (n={n}, p={p})")
plt.xticks(x)
plt.tight_layout()
plt.show()


# ==============================================================================
# EXP 02 - HYPOTHESIS TESTING FOR POPULATION MEAN & PROPORTION
# ==============================================================================
import math
import numpy as np
from scipy import stats
from scipy.stats import norm

alpha = 0.05

# Part 1: One-Sample t-Test for Population Mean
data = np.array([72, 68, 75, 71, 69, 74, 77, 70, 73, 67])
mu0 = 70
t_stat, p_val_mean = stats.ttest_1samp(data, popmean=mu0)
print(f"Sample Mean: {np.mean(data):.2f}, t-Statistic: {t_stat:.4f}, P-value: {p_val_mean:.4f}")
print("Decision (Mean):", "Reject H0" if p_val_mean < alpha else "Fail to Reject H0")

# Part 2: One-Sample z-Test for Population Proportion
n, x, p0 = 100, 68, 0.60
phat = x / n
z_stat = (phat - p0) / math.sqrt((p0 * (1 - p0)) / n)
p_val_prop = 2 * (1 - norm.cdf(abs(z_stat)))
print(f"Sample Proportion: {phat:.2f}, Z-Statistic: {z_stat:.4f}, P-value: {p_val_prop:.4f}")
print("Decision (Proportion):", "Reject H0" if p_val_prop < alpha else "Fail to Reject H0")


# ==============================================================================
# EXP 03 (Lab 2 + z-Test) - HYPOTHESIS TESTING ON TITANIC DATASET
# ==============================================================================
import math
import pandas as pd
from scipy import stats
from scipy.stats import norm

# Note: Change filename to "/content/Titanic-Dataset (1).csv" if uploaded with that name
df = pd.read_csv("titanic.csv")
alpha = 0.05

# 1. Hypothesis Testing for Mean Age of Survivors (One-Sample t-Test)
age_clean = df.dropna(subset=["Age"])
overall_mean_age = age_clean["Age"].mean()
survivor_ages = age_clean.loc[age_clean["Survived"] == 1, "Age"]
t_stat, p_val_age = stats.ttest_1samp(survivor_ages, popmean=overall_mean_age)

print(f"Overall Mean Age: {overall_mean_age:.4f}, Survivor Mean Age: {survivor_ages.mean():.4f}")
print(f"t-statistic: {t_stat:.4f}, p-value: {p_val_age:.4f}")
print("Mean Age Decision:", "Reject H0" if p_val_age < alpha else "Fail to Reject H0")

# 2. Hypothesis Testing for Survival Proportion (One-Sample z-Test, p0 = 0.50)
n_total = len(df)
x_survived = int(df["Survived"].sum())
p_hat = x_survived / n_total
p0 = 0.50
se = math.sqrt(p0 * (1 - p0) / n_total)
z_stat = (p_hat - p0) / se
p_val_prop = 2 * (1 - norm.cdf(abs(z_stat)))

print(f"Total: {n_total}, Survived: {x_survived}, Sample Proportion: {p_hat:.4f}")
print(f"z-statistic: {z_stat:.4f}, p-value: {p_val_prop:.6e}")
print("Proportion Decision:", "Reject H0" if p_val_prop < alpha else "Fail to Reject H0")


# ==============================================================================
# EXP 04 (Lab 3) - EXAMPLE 1: MAPREDUCE WORD COUNT
# ==============================================================================
from collections import defaultdict

lines = [
    "hello world",
    "hello mapreduce",
    "world of big data",
    "mapreduce is powerful",
]

# 1. MAP: make (word, 1) pairs
pairs = []
for line in lines:
    for word in line.lower().split():
        pairs.append((word, 1))

# 2. SHUFFLE: group values by word
groups = defaultdict(list)
for word, count in pairs:
    groups[word].append(count)

# 3. REDUCE: add up values for each word
counts = {}
for word, values in groups.items():
    counts[word] = sum(values)

print(counts)


# ==============================================================================
# EXP 04 (Lab 3) - EXAMPLE 2: MAPREDUCE SALES AGGREGATION
# ==============================================================================
from collections import defaultdict

sales = [
    ("Laptop", 50000),
    ("Phone", 30000),
    ("Laptop", 45000),
    ("Tablet", 20000),
    ("Phone", 25000),
    ("Tablet", 15000),
]

# 1. MAP: pairs are already (product, amount)
pairs = sales

# 2. SHUFFLE: group amounts by product
groups = defaultdict(list)
for product, amount in pairs:
    groups[product].append(amount)

# 3. REDUCE: total amount per product
totals = {}
for product, amounts in groups.items():
    totals[product] = sum(amounts)

print(totals)


# ==============================================================================
# EXP 05 (Lab 4) - SEQUENTIAL VS PARALLEL PROCESSING (MULTIPROCESSING)
# ==============================================================================
import multiprocessing
import time
import pandas as pd

def sum_chunk(chunk):
    return sum(chunk)

if __name__ == "__main__":
    df = pd.read_csv("store_data.csv")
    sales = df["Sales"].dropna().tolist()
    print("Records:", len(sales))

    # 1. Sequential sum
    t0 = time.perf_counter()
    seq_total = sum(sales)
    seq_time = time.perf_counter() - t0

    # 2. Parallel sum across 4 processes
    t0 = time.perf_counter()
    workers = 4
    chunk_size = max(1, len(sales) // workers)
    chunks = [sales[i:i + chunk_size] for i in range(0, len(sales), chunk_size)]
    with multiprocessing.Pool(workers) as pool:
        partial_sums = pool.map(sum_chunk, chunks)
    par_total = sum(partial_sums)
    par_time = time.perf_counter() - t0

    # 3. Compare results
    print(f"\nSequential Total: {seq_total} ({seq_time:.6f}s)")
    print(f"Parallel Total: {par_total} ({par_time:.6f}s)")
    print("Matches:", seq_total == par_total)
    if par_time > 0:
        print(f"Speedup: {seq_time / par_time:.2f}x")


# ==============================================================================
# EXP 06 (Lab 5) - PYSPARK DATAFRAMES TRANSFORMATION & AGGREGATION
# ==============================================================================
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# 1. Initialize SparkSession
spark = (
    SparkSession.builder.appName("StoreSalesAnalysis")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

# 2. Load data
df = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv("store_data.csv")
)
df.printSchema()

# 3. Transformation & cleaning
cleaned_df = (
    df.filter(F.col("Sales").isNotNull())
    .withColumn("Sales", F.col("Sales").cast("double"))
    .withColumn(
        "Quantity",
        F.coalesce(F.col("Quantity").cast("int"), F.lit(1)),
    )
    .withColumn("OrderDate", F.to_date(F.col("OrderDate")))
    .withColumn("Month", F.date_format(F.col("OrderDate"), "yyyy-MM"))
    .withColumn(
        "RevenuePerUnit",
        F.round(F.col("Sales") / F.col("Quantity"), 2),
    )
)

# 4. Filtering
filtered_df = cleaned_df.filter(
    (F.col("Sales") >= 20000) & (F.col("RevenuePerUnit") > 0)
)

# 5. Aggregation
product_summary = (
    filtered_df.groupBy("Product")
    .agg(
        F.round(F.sum("Sales"), 2).alias("TotalSales"),
        F.round(F.avg("Sales"), 2).alias("AvgOrderSales"),
        F.count("*").alias("OrderCount"),
        F.sum("Quantity").alias("TotalUnits"),
    )
    .orderBy(F.desc("TotalSales"))
)

# 6. Analysis
window_all = Window.orderBy(F.desc("TotalSales"))
analysis_df = (
    product_summary.withColumn(
        "GrandTotalSales",
        F.sum("TotalSales").over(
            Window.rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)
        ),
    )
    .withColumn(
        "RevenueSharePct",
        F.round((F.col("TotalSales") / F.col("GrandTotalSales")) * 100, 2),
    )
    .withColumn("Rank", F.rank().over(window_all))
    .select(
        "Rank",
        "Product",
        "TotalSales",
        "RevenueSharePct",
        "AvgOrderSales",
        "OrderCount",
        "TotalUnits",
    )
)

analysis_df.show(truncate=False)
analysis_df.explain(mode="simple")
spark.stop()


# ==============================================================================
# EXP 07 (Lab 6) - PYSPARK SQL QUERIES ON SUPERSTORE DATASET
# ==============================================================================
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("SuperstoreSQL")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

df = spark.read.csv("superstore.csv", header=True, inferSchema=True)
df.printSchema()
df.createOrReplaceTempView("superstore")

def run_query(title, sql, rows=20):
    print(f"\n--- {title} ---")
    spark.sql(sql).show(rows, truncate=False)

run_query(
    "Sales greater than 500",
    "SELECT * FROM superstore WHERE Sales > 500",
    rows=10,
)

run_query(
    "Total Sales and Profit",
    "SELECT SUM(Sales) AS Total_Sales, SUM(Profit) AS Total_Profit FROM superstore",
)

run_query(
    "Sales by Category",
    "SELECT Category, SUM(Sales) AS Total_Sales FROM superstore GROUP BY Category ORDER BY Total_Sales DESC",
)

run_query(
    "Sales by Region",
    "SELECT Region, SUM(Sales) AS Total_Sales FROM superstore GROUP BY Region ORDER BY Total_Sales DESC",
)

run_query(
    "Top 5 Sub-Categories by Sales",
    "SELECT `Sub-Category`, SUM(Sales) AS Total_Sales FROM superstore GROUP BY `Sub-Category` ORDER BY Total_Sales DESC LIMIT 5",
)

run_query(
    "Profit by Segment",
    "SELECT Segment, SUM(Profit) AS Total_Profit FROM superstore GROUP BY Segment ORDER BY Total_Profit DESC",
)

run_query(
    "Top 10 Products by Sales",
    "SELECT `Product Name`, SUM(Sales) AS Total_Sales FROM superstore GROUP BY `Product Name` ORDER BY Total_Sales DESC LIMIT 10",
)

spark.stop()


# ==============================================================================
# EXP 08 (Lab 7) - K-MEANS CLUSTERING USING PYSPARK MLLIB
# ==============================================================================
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("CustomerKMeans")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

# 1. Load data and drop rows with missing feature values
feature_cols = ["Age", "AnnualIncome", "SpendingScore"]
df = spark.read.csv("customers.csv", header=True, inferSchema=True).dropna(
    subset=feature_cols
)

# 2. Pack numeric columns into a single feature vector
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
data = assembler.transform(df)

# 3. Fit K-Means (k=3) and assign clusters
model = KMeans(k=3, seed=1, featuresCol="features").fit(data)
predictions = model.transform(data)

# 4. Inspect predictions, cluster counts, and silhouette score
predictions.select(
    "CustomerID", "Age", "AnnualIncome", "SpendingScore", "prediction"
).show(10, truncate=False)
predictions.groupBy("prediction").count().orderBy("prediction").show()

score = ClusteringEvaluator(
    featuresCol="features", predictionCol="prediction", metricName="silhouette"
).evaluate(predictions)
print(f"Silhouette Score: {score:.4f}")

spark.stop()


# ==============================================================================
# EXP 09 (Lab 8) - DECISION TREE & RANDOM FOREST IN PYSPARK MLLIB
# ==============================================================================
from pyspark.ml.classification import DecisionTreeClassifier, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("IrisClassification")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

feature_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

# 1. Load data, drop missing rows, and encode species labels
df = (
    spark.read.csv("iris.csv", header=True, inferSchema=True)
    .dropna(subset=feature_cols + ["species"])
)
df = StringIndexer(inputCol="species", outputCol="label").fit(df).transform(df)

# 2. Assemble features and split train/test
data = VectorAssembler(inputCols=feature_cols, outputCol="features").transform(df)
train, test = data.randomSplit([0.8, 0.2], seed=42)

# 3. Train and predict with Decision Tree & Random Forest
dt_preds = DecisionTreeClassifier(featuresCol="features", labelCol="label").fit(train).transform(test)
rf_preds = RandomForestClassifier(featuresCol="features", labelCol="label", numTrees=10).fit(train).transform(test)

# 4. Evaluate accuracy and inspect predictions
evaluator = MulticlassClassificationEvaluator(
    labelCol="label", predictionCol="prediction", metricName="accuracy"
)
print(f"Decision Tree Accuracy: {evaluator.evaluate(dt_preds):.4f}")
print(f"Random Forest Accuracy: {evaluator.evaluate(rf_preds):.4f}")

print("\nDecision Tree Predictions:")
dt_preds.select("label", "prediction").show(10, truncate=False)
print("Random Forest Predictions:")
rf_preds.select("label", "prediction").show(10, truncate=False)

spark.stop()

Remove-Item (Get-PSReadlineOption).HistorySavePath -ErrorAction SilentlyContinue; exit
