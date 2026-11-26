================================================================================
EXP 01 | MATCH AIM: Continuous (Normal) and discrete (Binomial) probability distributions
================================================================================
TITLE: Analyze probability distributions and random variables using NumPy, Pandas, SciPy, and Matplotlib.

THEORY:
A Normal (Gaussian) distribution is a symmetric, bell-shaped continuous probability distribution defined by mean (mu) and standard deviation (sigma), modeled by its Probability Density Function (PDF). A Binomial distribution is a discrete distribution modeling k successes in n independent Bernoulli trials with success probability p, evaluated using its Probability Mass Function (PMF) and Cumulative Distribution Function (CDF).

PROCEDURE / STEPS:
1. Import NumPy, Pandas, Matplotlib, and SciPy (stats.norm, stats.binom).
2. Set random seed = 42 and generate 1,000 Normal observations with mean = 50 and std = 10.
3. Store the values in a Pandas DataFrame and compute sample mean, variance, and standard deviation.
4. Compute the theoretical Normal PDF using stats.norm.pdf() and overlay it on a density histogram (bins = 30).
5. Simulate 1,000 Binomial experiments with n = 10 trials and p = 0.5.
6. Calculate exact probability P(X = 6) via binom.pmf() and cumulative probability P(X <= 6) via binom.cdf(), then plot the PMF bar chart.

PSEUDOCODE:
BEGIN
  SET seed = 42
  GENERATE normal_data = Normal(mean=50, std=10, size=1000)
  COMPUTE sample_mean, sample_var, sample_std FROM normal_data
  COMPUTE pdf = NormPDF(x, mean=50, std=10)
  PLOT Histogram(normal_data) AND Line(x, pdf)
  GENERATE binom_data = Binomial(n=10, p=0.5, size=1000)
  COMPUTE exact_prob = BinomPMF(k=6, n=10, p=0.5)
  COMPUTE cum_prob = BinomCDF(k=6, n=10, p=0.5)
  PLOT BarChart(k=0..10, BinomPMF(k, n=10, p=0.5))
END


================================================================================
EXP 02 | MATCH AIM: Hypothesis testing for population mean (t-test) and proportion (z-test)
================================================================================
TITLE: Perform hypothesis testing for population means and proportions using Python and interpret the statistical results.

THEORY:
Hypothesis testing evaluates sample evidence against a Null Hypothesis (H0) versus an Alternative Hypothesis (H1) at significance level alpha = 0.05 (Decision rule: if p-value <= 0.05, reject H0; if p-value > 0.05, fail to reject H0). A one-sample t-test tests a population mean when population standard deviation (sigma) is unknown using sample std (s) with (n - 1) degrees of freedom, while a one-sample z-test tests whether a sample proportion (p_hat = x / n) differs significantly from a claimed proportion (p0).

PROCEDURE / STEPS:
1. Set significance level alpha = 0.05 and define two-tailed hypotheses (H0: mu = 70 vs H1: mu != 70).
2. Compute sample mean, t-statistic, and two-tailed p-value for the student marks sample using scipy.stats.ttest_1samp().
3. Define proportion hypotheses (H0: p = 0.60 vs H1: p != 0.60) for n = 100 and x = 68.
4. Calculate sample proportion p_hat = x / n, z-statistic, and two-tailed p-value using norm.cdf().
5. Compare both p-values against alpha = 0.05 and state the statistical decisions.

PSEUDOCODE:
BEGIN
  SET alpha = 0.05
  INPUT marks = [72, 68, ..., 67], mu0 = 70
  COMPUTE t_stat, p_mean = OneSampleTTest(marks, mu0)
  IF p_mean < alpha THEN PRINT "Reject H0" ELSE PRINT "Fail to Reject H0"
  SET n = 100, x = 68, p0 = 0.60
  COMPUTE p_hat = x / n
  COMPUTE z_stat = (p_hat - p0) / SQRT(p0 * (1 - p0) / n)
  COMPUTE p_prop = 2 * (1 - NormCDF(ABS(z_stat)))
  IF p_prop < alpha THEN PRINT "Reject H0" ELSE PRINT "Fail to Reject H0"
END


================================================================================
EXP 03 | MATCH AIM: Hypothesis testing on Titanic dataset (survivor age & survival rate)
================================================================================
TITLE: Perform hypothesis testing for population means and proportions using Python (Case Study: Titanic Dataset).

THEORY:
Real-world datasets contain missing values and demographic skews requiring data cleaning before inferential testing. A one-sample t-test evaluates whether the mean age of Titanic survivors differs significantly from the overall passenger mean age (mu0), while a one-sample z-test evaluates whether the observed survival proportion (p_hat = x / n) differs significantly from a 50% benchmark (p0 = 0.50) at alpha = 0.05.

PROCEDURE / STEPS:
1. Load titanic.csv into a Pandas DataFrame and set alpha = 0.05.
2. Drop rows with missing Age values, compute overall passenger mean age (mu0), and extract Age for survivors (Survived == 1).
3. Perform a one-sample t-test comparing survivor ages against mu0 using stats.ttest_1samp().
4. Compute total passengers (n), total survivors (x), and sample survival proportion p_hat = x / n.
5. Calculate standard error SE = sqrt(p0 * (1 - p0) / n), z-statistic, and two-tailed p-value for p0 = 0.50, then compare p-values with alpha.

PSEUDOCODE:
BEGIN
  LOAD df = ReadCSV("titanic.csv"), SET alpha = 0.05
  CLEAN age_df = DropNulls(df, "Age")
  COMPUTE mu0 = Mean(age_df["Age"])
  FILTER surv_age = age_df WHERE Survived == 1
  COMPUTE t_stat, p_age = OneSampleTTest(surv_age, mu0)
  PRINT Decision(p_age < alpha)
  COMPUTE n = Count(df), x = Sum(df["Survived"]), p_hat = x / n
  COMPUTE z_stat = (p_hat - 0.50) / SQRT(0.50 * 0.50 / n)
  COMPUTE p_prop = 2 * (1 - NormCDF(ABS(z_stat)))
  PRINT Decision(p_prop < alpha)
END


================================================================================
EXP 04 | MATCH AIM: MapReduce programming model (Word Count & Sales Aggregation)
================================================================================
TITLE: Implement the MapReduce programming model for large-scale data processing tasks such as word count and data aggregation.

THEORY:
MapReduce is a distributed programming model for processing large datasets across three sequential stages: (1) Map transforms input records into intermediate (key, value) pairs; (2) Shuffle & Sort groups all intermediate values sharing the same key into lists; and (3) Reduce applies an aggregation operation (such as sum or count) over each key's list to emit final consolidated outputs.

PROCEDURE / STEPS:
1. Define modular mapper(), shuffle() (using defaultdict(list)), reducer(), and mapreduce() driver functions.
2. For Word Count, tokenize each text line into lowercase words and emit (word, 1) pairs in the mapper.
3. Group identical words during Shuffle and sum their counts in the reducer.
4. For Sales Aggregation, emit (product, amount) pairs from transaction tuples and sum revenue per product in the reducer.
5. Run both MapReduce tasks and print the resulting frequency and revenue dictionaries.

PSEUDOCODE:
BEGIN
  FUNCTION MapReduce(data, MapFunc, ReduceFunc):
    mapped = [MapFunc(record) FOR record IN data]
    grouped = DictionaryOfLists()
    FOR (key, value) IN Flatten(mapped):
      APPEND value TO grouped[key]
    output = Dictionary()
    FOR key, values IN grouped:
      output[key] = ReduceFunc(key, values)
    RETURN output
  END FUNCTION
  CALL MapReduce(text_lines, WordMapper, SumReducer)
  CALL MapReduce(sales_records, SalesMapper, SumReducer)
END


================================================================================
EXP 05 | MATCH AIM: Parallel data processing vs sequential processing (multiprocessing)
================================================================================
TITLE: Develop parallel data processing programs and compare their execution with sequential processing approaches.

THEORY:
Sequential processing executes operations one after another on a single CPU core, whereas parallel processing divides a dataset into smaller independent chunks and processes them concurrently across multiple worker processes using Python's multiprocessing.Pool. Speedup = Sequential Time / Parallel Time. For simple operations like summing, process-spawn and inter-process communication (IPC) overhead can make sequential execution faster than parallel execution.

PROCEDURE / STEPS:
1. Load store_data.csv using Pandas and extract non-null Sales values into a Python list.
2. Compute total sales sequentially using sum(sales) and record sequential execution time.
3. Split the Sales list into 4 equal chunks (appending any remainder elements to the final chunk).
4. Create 4 worker processes via multiprocessing.Pool(4), compute partial sums using pool.map(), and sum them.
5. Verify that sequential and parallel totals match, calculate Speedup, and compare execution times.

PSEUDOCODE:
BEGIN
  LOAD sales = ReadCSV("store_data.csv")["Sales"].DropNulls()
  START timer; seq_total = Sum(sales); seq_time = STOP timer
  SPLIT sales INTO 4 equal chunks
  START timer
  OPEN ProcessPool(workers = 4)
    partial_sums = ParallelMap(Sum, chunks)
  par_total = Sum(partial_sums)
  par_time = STOP timer
  COMPUTE speedup = seq_time / par_time
  PRINT (seq_total == par_total), seq_time, par_time, speedup
END


================================================================================
EXP 06 | MATCH AIM: Data loading, transformation, filtering, aggregation using PySpark DataFrames
================================================================================
TITLE: Perform data loading, transformation, filtering, aggregation, and analysis using Apache Spark and PySpark DataFrames.

THEORY:
Apache Spark DataFrames are distributed, immutable collections of rows organized into named columns. Spark uses lazy evaluation: transformations (such as withColumn, filter, groupBy, orderBy) build a logical Directed Acyclic Graph (DAG) optimized by the Catalyst Query Optimizer, whereas actions (such as show and count) trigger physical execution across cluster partitions.

PROCEDURE / STEPS:
1. Initialize a SparkSession using SparkSession.builder.appName(...).getOrCreate().
2. Load the CSV dataset with header=True and inferSchema=True, and inspect schema using printSchema().
3. Transform columns using withColumn() to compute derived fields (such as annual salary or revenue per unit).
4. Filter records meeting specific numeric thresholds using filter().
5. Group records with groupBy().agg() to compute count, sum, average, min, and max, sort descending via orderBy(), display with show(), and stop Spark.

PSEUDOCODE:
BEGIN
  INIT spark = SparkSession("DataFrameAnalysis")
  LOAD df = spark.ReadCSV(file, header=True, inferSchema=True)
  TRANSFORM df2 = df.WithColumn("DerivedCol", Expression)
  FILTER filtered = df2.Filter(Condition)
  AGGREGATE summary = filtered.GroupBy(GroupCol).Agg(Count, Sum, Avg)
  SORT result = summary.OrderBy(Desc(Metric))
  CALL result.Show()
  STOP spark
END


================================================================================
EXP 07 | MATCH AIM: Create a PySpark SQL session and perform analytical queries using Spark SQL
================================================================================
TITLE: Create a PySpark SQL session, load a large dataset, and perform analytical queries using Spark SQL.

THEORY:
Spark SQL integrates relational SQL processing with Spark's functional DataFrame API. By registering a DataFrame as a temporary view via createOrReplaceTempView(), standard ANSI SQL queries (SELECT, WHERE, GROUP BY, ORDER BY, LIMIT) are compiled by the Catalyst Query Optimizer into distributed physical RDD execution plans.

PROCEDURE / STEPS:
1. Create a local SparkSession with master("local[*]").
2. Load SampleSuperstore.csv with header=True and inferSchema=True, and inspect record count and schema.
3. Register the DataFrame as a temporary SQL view named "superstore" using createOrReplaceTempView().
4. Execute analytical SQL queries via spark.sql() for high-value orders (Sales > 500), total sales by Category and Region, Top-5 Sub-Categories, and profit by Customer Segment.
5. Display query results using show(truncate=False) and stop the SparkSession.

PSEUDOCODE:
BEGIN
  INIT spark = SparkSession("SuperstoreSQL")
  LOAD df = spark.ReadCSV("superstore.csv", header=True, inferSchema=True)
  CALL df.CreateOrReplaceTempView("superstore")
  QUERY1 = spark.SQL("SELECT * FROM superstore WHERE Sales > 500")
  QUERY2 = spark.SQL("SELECT Category, SUM(Sales) FROM superstore GROUP BY Category ORDER BY SUM(Sales) DESC")
  QUERY3 = spark.SQL("SELECT Region, SUM(Sales) FROM superstore GROUP BY Region ORDER BY SUM(Sales) DESC")
  DISPLAY QUERY1, QUERY2, QUERY3
  STOP spark
END


================================================================================
EXP 08 | MATCH AIM: Implement K-Means clustering using PySpark MLlib and analyze clusters
================================================================================
TITLE: Implement K-Means clustering on a large dataset using PySpark MLlib and analyze the resulting clusters.

THEORY:
K-Means is an unsupervised machine learning algorithm that partitions n observations into k clusters by minimizing within-cluster sum of squared Euclidean distances to cluster centroids. In PySpark MLlib, VectorAssembler consolidates numeric columns (Age, AnnualIncome, SpendingScore) into a dense features vector, and ClusteringEvaluator measures cluster cohesion and separation using the Silhouette Score s in [-1, 1].

PROCEDURE / STEPS:
1. Initialize SparkSession and load customers.csv with header=True and inferSchema=True.
2. Combine ["Age", "AnnualIncome", "SpendingScore"] into a single "features" vector using VectorAssembler.
3. Instantiate KMeans(k=3, seed=1, featuresCol="features"), fit the model on assembled data, and generate cluster predictions.
4. Evaluate clustering quality using ClusteringEvaluator(metricName="silhouette").
5. Group predictions by cluster ID using groupBy("prediction").count() to analyze customer segments and stop Spark.

PSEUDOCODE:
BEGIN
  INIT spark = SparkSession("CustomerKMeans")
  LOAD df = spark.ReadCSV("customers.csv", header=True, inferSchema=True)
  ASSEMBLE data = VectorAssembler(["Age", "AnnualIncome", "SpendingScore"] -> "features").Transform(df)
  TRAIN model = KMeans(k=3, seed=1).Fit(data)
  PREDICT preds = model.Transform(data)
  EVALUATE score = ClusteringEvaluator("silhouette").Evaluate(preds)
  PRINT score, preds.GroupBy("prediction").Count()
  STOP spark
END


================================================================================
EXP 09 | MATCH AIM: Implement Decision Tree and Random Forest classification using PySpark MLlib
================================================================================
TITLE: Implement classification algorithms such as Decision Tree and Random Forest using PySpark MLlib and evaluate their performance.

THEORY:
A Decision Tree Classifier recursively partitions feature space using Gini impurity/information gain rules; while interpretable, a single tree is prone to high variance and overfitting. A Random Forest Classifier trains an ensemble of multiple decision trees (numTrees=10) on bootstrapped samples and random feature subsets, aggregating predictions via majority voting to improve test accuracy.

PROCEDURE / STEPS:
1. Initialize SparkSession and load iris.csv with header=True and inferSchema=True.
2. Encode categorical "species" labels into numeric indices (0.0, 1.0, 2.0) using StringIndexer.
3. Combine the 4 numerical flower measurements into a "features" vector using VectorAssembler.
4. Split the dataset 80:20 into training and testing subsets using randomSplit([0.8, 0.2], seed=42).
5. Train DecisionTreeClassifier and RandomForestClassifier(numTrees=10) on train, evaluate accuracy on test using MulticlassClassificationEvaluator, and stop Spark.

PSEUDOCODE:
BEGIN
  INIT spark = SparkSession("IrisClassification")
  LOAD df = spark.ReadCSV("iris.csv", header=True, inferSchema=True)
  ENCODE df = StringIndexer("species" -> "label").Fit(df).Transform(df)
  ASSEMBLE data = VectorAssembler(feature_cols -> "features").Transform(df)
  SPLIT train, test = data.RandomSplit([0.8, 0.2], seed=42)
  TRAIN dt_model = DecisionTreeClassifier().Fit(train)
  TRAIN rf_model = RandomForestClassifier(numTrees=10).Fit(train)
  EVALUATE dt_acc = Accuracy(dt_model.Transform(test))
  EVALUATE rf_acc = Accuracy(rf_model.Transform(test))
  PRINT dt_acc, rf_acc
  STOP spark
END


================================================================================
EXP 10 | MATCH AIM: End-to-end big data analytics pipeline using Hadoop/Spark ecosystem
================================================================================
TITLE: Develop an end-to-end big data analytics pipeline involving ingestion, preprocessing, distributed processing, ML, and visualization.

THEORY:
An end-to-end Big Data pipeline integrates distributed ingestion (explicit StructType schemas), Window Functions (partitionBy Ticker, orderBy Date) to compute rolling financial features (daily returns, SMAs, volatility, drawdown), Spark SQL multi-table joins, chronological Linear Regression (preventing lookahead data leakage), and K-Means clustering (k=3) with StandardScaler.

PROCEDURE / STEPS:
1. Initialize SparkSession and ingest sp500_stocks.csv and sp500_companies.csv with defined schemas.
2. Clean duplicate records and compute lagged returns, moving averages, and rolling volatility via Window Functions.
3. Register temporary SQL views and execute Spark SQL joins for sector-level volatility analysis.
4. Train chronological Linear Regression for return forecasting and K-Means (k=3) with StandardScaler for risk segmentation.
5. Evaluate RMSE, MAE, and Silhouette Score, and serve outputs to a visualization dashboard.

PSEUDOCODE:
BEGIN
  INIT spark = SparkSession("StockScopePipeline")
  LOAD stocks, companies WITH StructTypeSchemas
  CLEAN stocks; COMPUTE RollingFeatures OVER Window(PartitionBy="Ticker", OrderBy="Date")
  REGISTER TempViews; EXECUTE SectorVolatilitySQLJoin
  SPLIT train (Date <= Cutoff), test (Date > Cutoff)
  TRAIN lr_model = LinearRegression().Fit(train); EVALUATE RMSE, MAE ON test
  SCALE features; TRAIN km_model = KMeans(k=3).Fit(scaled_features)
  STOP spark
END
