================================================================================
INTRODUCTION TO DATA SCIENCE & ENGINEERING (DSC3001P) - THEORY & PSEUDOCODE
================================================================================

--------------------------------------------------------------------------------
EXPERIMENT 01: EXPLORING STRUCTURED, SEMI-STRUCTURED & UNSTRUCTURED DATA
--------------------------------------------------------------------------------

Aim:
To explore structured, semi-structured, and unstructured data, and perform data ingestion, extraction, integration, and basic analysis from CSV files, REST APIs, JSON, and plain text using Python.

Theory:
Data in data engineering is categorized into three structural types based on schema rigidity:
1. Structured Data: Follows a fixed tabular schema of rows and columns with well-defined data types (e.g., CSV files, relational SQL databases). Processed efficiently using Pandas DataFrames.
2. Semi-Structured Data: Does not conform to a rigid table schema but uses tags, keys, or hierarchical markers to separate elements (e.g., JSON, XML, REST API payloads).
3. Unstructured Data: Lacks any predefined data model or internal structure (e.g., customer reviews, emails, server logs, sensor streams).
Data ingestion collects data from these heterogeneous sources into an analytical workspace. Python libraries such as Pandas (tabular ingestion), Requests (HTTP REST API calls), json (hierarchical parsing), re (Regular Expressions for pattern matching), and TextBlob (NLP sentiment polarity scoring between -1 and +1) enable unified ingestion and preprocessing.

Procedure:
1. Import required Python libraries: pandas, requests, re, json, random, time, and TextBlob.
2. Load the structured CSV dataset into a Pandas DataFrame and compute summary aggregations (mean, maximum, minimum, value counts, filtering, and sorting).
3. Send an HTTP GET request to a public REST API endpoint, parse the semi-structured JSON response into a Pandas DataFrame, and export it to CSV.
4. Query a live weather REST API using latitude and longitude parameters and extract nested JSON keys to display current temperature.
5. Read unstructured text and apply Regular Expressions (re.findall) to extract email addresses and 10-digit phone numbers.
6. Analyze unstructured customer review text using TextBlob to compute sentiment polarity and classify it as Positive, Negative, or Neutral.
7. Simulate real-time IoT temperature sensor readings and demonstrate reading/writing nested JSON files using json.dump() and json.load().

Pseudocode:
BEGIN
    IMPORT pandas, requests, re, json, TextBlob

    // 1. Structured CSV Analysis
    LOAD df <- READ_CSV("dataset.csv")
    COMPUTE mean_val <- MEAN(df[target_col])
    COMPUTE max_val <- MAX(df[target_col]), min_val <- MIN(df[target_col])
    FILTER high_records <- df WHERE df[target_col] > mean_val
    PRINT summary statistics, value counts, and sorted records

    // 2. Semi-Structured REST API & Nested JSON Ingestion
    SEND response <- HTTP_GET("https://jsonplaceholder.typicode.com/users")
    PARSE json_data <- response.JSON()
    CONVERT users_df <- DATAFRAME(json_data)
    SAVE users_df TO "users.csv"

    SEND weather_res <- HTTP_GET(weather_api_url)
    PRINT weather_res["current"]["temperature_2m"]

    WRITE nested_dict TO "nested_output.json" USING json.dump()
    READ loaded_dict FROM "nested_output.json" USING json.load()

    // 3. Unstructured Text Extraction & Sentiment Analysis
    EXTRACT emails <- REGEX_FINDALL(email_pattern, raw_text)
    EXTRACT phones <- REGEX_FINDALL(phone_pattern, raw_text)
    COMPUTE polarity <- TextBlob(review_text).sentiment.polarity
    IF polarity > 0 THEN
        PRINT "Positive"
    ELSE IF polarity < 0 THEN
        PRINT "Negative"
    ELSE
        PRINT "Neutral"
    END IF
END

Conclusion:
Successfully explored and ingested structured (CSV), semi-structured (JSON/REST APIs), and unstructured (free text/reviews) datasets using Python, demonstrating tabular aggregation, regex pattern extraction, JSON parsing, and sentiment classification.


--------------------------------------------------------------------------------
EXPERIMENT 02: DATA CLEANING AND PREPROCESSING
--------------------------------------------------------------------------------

Aim:
To perform data cleaning and preprocessing on a dataset using Python and Pandas by handling duplicate records, missing values, invalid entries, inconsistent date formats, and text standardization.

Theory:
Raw real-world datasets frequently suffer from missing values (NaN/null), duplicate rows, out-of-range anomalies, inconsistent column names, and mixed date or string formats. Garbage-in leads to inaccurate analytics and biased models.
Data cleaning improves data quality and consistency through:
- Deduplication: Identifying and dropping identical records using duplicated() and drop_duplicates().
- Range Validation & Imputation: Filtering impossible values (such as negative marks or marks > 100) and replacing missing numerical values with central tendency measures (mean or median) via fillna().
- Format Standardization: Parsing mixed date strings into a uniform datetime format using pd.to_datetime(..., errors='coerce') and normalizing text case/whitespace using vectorized string methods (.str.strip().str.lower()).

Procedure:
1. Import Pandas and NumPy, and load the raw CSV dataset into a DataFrame.
2. Inspect dataset dimensions, column names, data types, summary statistics, and null counts using head(), tail(), shape, info(), describe(), and isnull().sum().
3. Identify duplicate records using duplicated().sum() and remove them with drop_duplicates().
4. Standardize column names by stripping leading/trailing spaces and replacing internal spaces with underscores.
5. Filter out out-of-range invalid numeric entries and impute remaining missing numerical values using column mean.
6. Convert date columns into a uniform DD-MM-YYYY format using pd.to_datetime() with error coercion, and standardize categorical text to lowercase without extra spaces.
7. Sort the cleaned dataset by the primary numeric attribute and export it to a new CSV file.

Pseudocode:
BEGIN
    IMPORT pandas, numpy
    LOAD df <- READ_CSV("dataset.csv")

    // 1. Inspect Dataset
    PRINT df.shape, df.dtypes, df.info(), df.describe()
    PRINT NULL_COUNT(df)

    // 2. Deduplicate & Standardize Headers
    REMOVE duplicates FROM df USING drop_duplicates()
    CLEAN column_names by stripping spaces

    // 3. Handle Missing Values, Invalid Ranges & Formatting
    FOR EACH col IN numeric_columns DO
        FILTER invalid out-of-range entries
        REPLACE missing values in df[col] WITH MEAN(df[col])
    END FOR

    FOR EACH col IN categorical_columns DO
        IF col is a date column THEN
            CONVERT df[col] TO datetime("DD-MM-YYYY", errors="coerce")
            FILL missing dates WITH default_date
        ELSE
            FILL missing values WITH "Unknown"
            CONVERT df[col] TO LOWERCASE(STRIP(df[col]))
        END IF
    END FOR

    // 4. Sort and Export
    SORT df BY primary_numeric_col ASCENDING
    SAVE df TO "cleaned_dataset.csv"
END

Conclusion:
Successfully performed end-to-end data cleaning and preprocessing using Pandas, resolving duplicates, missing entries, invalid ranges, and inconsistent date/string formats to produce a reliable dataset ready for analysis.


--------------------------------------------------------------------------------
EXPERIMENT 03: DATA TRANSFORMATION & STATISTICAL ANALYSIS
--------------------------------------------------------------------------------

Aim:
To perform data transformation and statistical analysis using Python by applying feature scaling, categorical encoding, hypothesis testing (Chi-Square), outlier detection (IQR and Z-Score), and correlation analysis.

Theory:
Data transformation converts raw attributes into standardized numerical representations required by machine learning and statistical models:
- Feature Scaling: Min-Max Scaling rescales features to a fixed [0, 1] range using (X - X_min) / (X_max - X_min), whereas Standard Scaling (Z-score standardization) centers data at mean = 0 and standard deviation = 1 using (X - mean) / std.
- Categorical Encoding: One-Hot Encoding creates binary indicator columns for nominal categories without imposing order, while Label Encoding maps each unique category to an integer (0 to K-1).
- Statistical Testing & Correlation: The Chi-Square test of independence evaluates whether two categorical variables are significantly associated (rejecting H0 when p-value < 0.05). Pearson correlation (r in [-1, 1]) quantifies linear dependence between two continuous variables.
- Outlier Detection: The Interquartile Range (IQR = Q3 - Q1) flags values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR; the Z-Score method flags extreme points where |Z| > 3.

Procedure:
1. Import Pandas, NumPy, Matplotlib, Scikit-learn (MinMaxScaler, StandardScaler, LabelEncoder), and SciPy (chi2_contingency, zscore).
2. Load the dataset and impute any missing values prior to numerical transformations.
3. Apply MinMaxScaler and StandardScaler to normalize and standardize the primary numerical column.
4. Transform categorical columns into binary dummy variables using pd.get_dummies() (One-Hot Encoding) and integer labels using LabelEncoder().
5. Construct a contingency table using pd.crosstab() between two categorical features and execute chi2_contingency() to test statistical independence at alpha = 0.05.
6. Detect numerical outliers using both the IQR boundary method and Z-Score threshold (|Z| > 3), and visualize distribution spread using a Box Plot.
7. Compute the Pearson correlation coefficient between two numerical features and plot a Scatter Plot to inspect their linear relationship.

Pseudocode:
BEGIN
    IMPORT pandas, numpy, matplotlib, MinMaxScaler, StandardScaler, LabelEncoder, chi2_contingency, zscore
    LOAD df <- READ_CSV("dataset.csv")

    // 1. Feature Scaling
    df["MinMax_Col"] <- MinMaxScaler().FIT_TRANSFORM(df[[num_col]])
    df["Std_Col"] <- StandardScaler().FIT_TRANSFORM(df[[num_col]])

    // 2. Categorical Encoding
    ohe_df <- GET_DUMMIES(df[[cat_col1]])
    df["Encoded_Col"] <- LabelEncoder().FIT_TRANSFORM(df[cat_col1])

    // 3. Chi-Square Hypothesis Test
    contingency_table <- CROSSTAB(df[cat_col1], df[cat_col2])
    chi2, p_val, dof, expected <- CHI2_CONTINGENCY(contingency_table)
    IF p_val < 0.05 THEN
        PRINT "Reject H0: Significant association exists"
    ELSE
        PRINT "Fail to reject H0: No significant association"
    END IF

    // 4. Outlier Detection (IQR & Z-Score)
    COMPUTE Q1 <- QUANTILE(df[num_col], 0.25), Q3 <- QUANTILE(df[num_col], 0.75)
    COMPUTE IQR <- Q3 - Q1
    SET lower <- Q1 - 1.5 * IQR, upper <- Q3 + 1.5 * IQR
    FILTER iqr_outliers <- df WHERE df[num_col] < lower OR df[num_col] > upper

    COMPUTE df["Z_Score"] <- ZSCORE(df[num_col])
    FILTER z_outliers <- df WHERE ABS(df["Z_Score"]) > 3
    PLOT BOXPLOT(df[num_col])

    // 5. Correlation Analysis
    COMPUTE r <- CORRELATION(df[num_col1], df[num_col2])
    PLOT SCATTER(df[num_col1], df[num_col2])
END

Conclusion:
Successfully implemented feature scaling, categorical encoding, Chi-Square hypothesis testing, IQR/Z-Score outlier detection, and Pearson correlation analysis using Python, preparing numerical and categorical features for downstream modeling.


--------------------------------------------------------------------------------
EXPERIMENT 04: EXPLORATORY DATA ANALYSIS (EDA) & DATA VISUALIZATION
--------------------------------------------------------------------------------

Aim:
To perform Exploratory Data Analysis (EDA) and data visualization using Python, Matplotlib, and Seaborn by generating Histograms, Pie Charts, Heatmaps, Bar Graphs, Frequency Polygons, Box Plots, Scatter Plots, Violin Plots, Count Plots, and Line Charts.

Theory:
Exploratory Data Analysis (EDA) uses visual and quantitative summaries to uncover underlying data distributions, trends, category proportions, correlations, and anomalies before modeling. Matplotlib provides low-level control over figures and axes, while Seaborn offers high-level statistical graphics built on Pandas DataFrames.
Different chart types address specific analytical questions:
- Distribution Plots: Histograms, Frequency Polygons, Box Plots, and Violin Plots reveal skewness, spread, quartiles, and kernel density.
- Categorical Comparisons: Bar Graphs, Count Plots, and Pie Charts compare frequencies and group averages across discrete categories.
- Multivariate & Trend Plots: Scatter Plots and Correlation Heatmaps show pairwise relationships between continuous variables, while Line Charts track sequential trends.

Procedure:
1. Import Pandas, NumPy, Matplotlib (pyplot), and Seaborn, and apply a clean visual theme (sns.set_theme).
2. Load the dataset and handle any missing values in numeric and categorical columns.
3. Plot a Histogram and a Frequency Polygon to examine the frequency distribution and class midpoints of the primary numeric variable.
4. Plot a Box Plot and a Violin Plot to inspect median, interquartile spread, density, and outliers across categories.
5. Plot a Bar Graph (group means), Count Plot (category frequencies), and Pie Chart (percentage share) for categorical analysis.
6. Compute the pairwise correlation matrix across numeric columns and display it as an annotated Seaborn Heatmap.
7. Plot a Scatter Plot between two numerical features and a Line Chart across sequential records to analyze relationships and trends.

Pseudocode:
BEGIN
    IMPORT pandas, numpy, matplotlib.pyplot, seaborn
    LOAD df <- READ_CSV("dataset.csv")
    CLEAN missing values in numeric and categorical columns

    // 1. Distribution Visualizations
    PLOT HISTOGRAM(df[num_col2], bins=8)
    COMPUTE hist_vals, bin_edges <- HISTOGRAM_DATA(df[num_col2])
    COMPUTE midpoints <- 0.5 * (bin_edges[:-1] + bin_edges[1:])
    PLOT LINE(midpoints, hist_vals) AS Frequency_Polygon
    PLOT BOXPLOT(df[num_col2])
    PLOT VIOLINPLOT(x=df[cat_col1], y=df[num_col2])

    // 2. Categorical Visualizations
    COMPUTE counts <- VALUE_COUNTS(df[cat_col1])
    PLOT PIE_CHART(counts)
    COMPUTE group_means <- GROUPBY(df, cat_col1).MEAN(num_col2)
    PLOT BAR_CHART(group_means)
    PLOT COUNTPLOT(df[cat_col1])

    // 3. Relationship & Trend Visualizations
    COMPUTE corr_matrix <- CORR(df[numeric_columns])
    PLOT HEATMAP(corr_matrix, annot=True)
    PLOT SCATTER(df[num_col1], df[num_col2])
    PLOT LINE_CHART(index, df[num_col2])
END

Conclusion:
Successfully conducted Exploratory Data Analysis using Matplotlib and Seaborn, creating ten distinct statistical visualizations to interpret data distributions, category proportions, feature correlations, and sequential trends.


--------------------------------------------------------------------------------
EXPERIMENT 05: DESIGN AND IMPLEMENTATION OF ETL PIPELINES
--------------------------------------------------------------------------------

Aim:
To design and implement a reusable, fault-tolerant ETL (Extract, Transform, Load) pipeline using Python, Pandas, SQLite3, and Logging to extract raw data, clean and enrich it, and load it into CSV and SQLite database targets.

Theory:
ETL (Extract, Transform, Load) is the foundational data engineering workflow for moving raw operational data into structured analytical storage:
1. Extract: Ingesting raw data from heterogeneous sources such as flat CSV files, JSON documents, or REST APIs while validating source availability.
2. Transform: Enforcing schema and business rules—removing duplicate records, coercing numeric types, imputing missing values, standardizing text casing, and deriving calculated attributes (such as performance flags or totals).
3. Load: Persisting the curated dataset into target destinations such as cleaned CSV files or relational database tables (SQLite via sqlite3 and DataFrame.to_sql()).
Integrating exception handling (try-except) and structured execution logging (logging module) ensures observability, auditability, and fault tolerance in automated data pipelines.

Procedure:
1. Import os, sqlite3, logging, and pandas, and configure file-based logging (etl_pipeline.log) with timestamps and severity levels.
2. Define a reusable run_etl(input_csv, output_csv, table_name, db_path) function wrapped in a try-except error-handling block.
3. In the Extract stage, verify that the input file exists on disk and load it into a Pandas DataFrame.
4. In the Transform stage, remove duplicate records, coerce numeric columns, impute missing numeric values with the mean, standardize categorical strings, and derive a new Performance_Flag column comparing each record against the dataset average.
5. In the Load stage, write the transformed DataFrame to an output CSV file and load it into a SQLite relational table using to_sql().
6. Execute a SQL SELECT verification query on the SQLite table and log pipeline completion status.

Pseudocode:
BEGIN
    IMPORT os, sqlite3, logging, pandas
    CONFIGURE logging TO "etl_pipeline.log"

    FUNCTION run_etl(input_csv, output_csv, table_name, db_path)
        TRY
            IF NOT EXISTS(input_csv) THEN
                RAISE FileNotFoundError
            END IF

            // 1. EXTRACT
            LOG_INFO("Extracting data from " + input_csv)
            LOAD df <- READ_CSV(input_csv)

            // 2. TRANSFORM
            REMOVE duplicates FROM df
            FOR EACH col IN numeric_columns DO
                COERCE df[col] TO numeric
                FILL missing values WITH MEAN(df[col])
            END FOR
            FOR EACH col IN categorical_columns DO
                FILL missing values WITH "Unknown"
                FORMAT df[col] AS TitleCase(STRIP(df[col]))
            END FOR
            COMPUTE avg_val <- MEAN(df[primary_metric])
            CREATE df["Performance_Flag"] <- IF df[primary_metric] >= avg_val THEN "Above_Avg" ELSE "Below_Avg"

            // 3. LOAD
            SAVE df TO output_csv
            CONNECT conn <- SQLITE_CONNECT(db_path)
            WRITE df TO SQL_TABLE(table_name, conn, if_exists="replace")
            VERIFY via SQL_QUERY("SELECT * FROM " + table_name + " LIMIT 5")
            LOG_INFO("ETL pipeline completed successfully")
        CATCH Exception AS e
            LOG_ERROR("ETL failed: " + e)
            PRINT error message
        END TRY
    END FUNCTION

    CALL run_etl("dataset.csv", "etl_output.csv", "processed_data", "dse_etl.db")
END

Conclusion:
Successfully designed and executed a modular, logged ETL pipeline in Python that extracted raw CSV data, applied schema cleaning and derived feature transformations, and loaded verified records into both CSV and SQLite database storage.


--------------------------------------------------------------------------------
EXPERIMENT 06: INTERACTIVE DASHBOARD & DAX ANALYSIS IN POWER BI
--------------------------------------------------------------------------------

Aim:
To import a dataset into Microsoft Power BI Desktop, create calculated measures using Data Analysis Expressions (DAX), and build an interactive dashboard with Bar Charts, Pie Charts, Maps, Filters, and Slicers.

Theory:
Microsoft Power BI is a Business Intelligence (BI) and data visualization platform used to model data, compute dynamic metrics, and build interactive reports.
DAX (Data Analysis Expressions) is Power BI's formula language for creating calculated columns and measures:
- Aggregation Functions: SUM(), AVERAGE(), COUNT(), COUNTROWS(), DISTINCTCOUNT(), MIN(), MAX().
- Logical Functions: IF(), AND(), OR(), and SWITCH(TRUE(), ...) for conditional classification.
- Filter Context Functions: CALCULATE() modifies the active filter context (e.g., filtering by a specific category or overriding filters using ALL() / REMOVEFILTERS()).
Interactive visuals such as Bar Charts, Pie Charts, Geographic Maps, KPI Cards, and Slicers allow end-users to dynamically slice and drill down into business metrics.

Procedure:
1. Launch Microsoft Power BI Desktop and click Home -> Get Data -> Text/CSV (or Excel) to import the dataset.
2. Open Power Query Editor (Transform Data) to verify column data types, remove null/duplicate rows, and click Close & Apply.
3. Switch to Report View and create calculated measures using DAX (Total Sales = SUM(...), Average Sales = AVERAGE(...), Transaction Count = COUNTROWS(...), and conditional CALCULATE/IF measures).
4. Add a Clustered Bar/Column Chart to compare metrics across categories/regions and a Pie/Donut Chart to show percentage contribution.
5. Add a Map visual by dragging geographic fields (City/Region/Country) to Location and numeric metrics to Bubble Size.
6. Insert KPI Cards to display headline totals and add Slicers (for Category, Region, or Date) to enable interactive cross-filtering across all dashboard visuals.

Pseudocode:
BEGIN
    OPEN Microsoft Power BI Desktop
    IMPORT dataset FROM CSV/Excel INTO Power BI Model
    CLEAN data types and nulls IN Power Query Editor -> APPLY changes

    // Define DAX Calculated Measures
    DEFINE Total_Metric <- SUM(Table[Numeric_Col])
    DEFINE Avg_Metric <- AVERAGE(Table[Numeric_Col])
    DEFINE Record_Count <- COUNTROWS(Table)
    DEFINE Status_Flag <- IF(Table[Numeric_Col] >= Threshold, "High", "Low")
    DEFINE Filtered_Metric <- CALCULATE([Total_Metric], Table[Category] = "Target_Category")
    DEFINE Unfiltered_Total <- CALCULATE([Total_Metric], ALL(Table[Category]))

    // Build Interactive Dashboard Visuals
    CREATE Bar_Chart(Axis = Category, Value = Total_Metric)
    CREATE Pie_Chart(Legend = Category, Value = Total_Metric)
    CREATE Map_Visual(Location = City/Region, Size = Total_Metric)
    CREATE KPI_Cards(Total_Metric, Avg_Metric, Record_Count)
    ADD Slicers(Category, Region, Date) TO filter all visuals interactively
END

Conclusion:
Successfully imported the dataset into Microsoft Power BI, implemented aggregation, logical, and filter-context DAX measures, and constructed an interactive dashboard with Bar Charts, Pie Charts, Maps, KPI Cards, and Slicers for visual decision-making.


--------------------------------------------------------------------------------
EXPERIMENT 07: SIMULATION & COMPARISON OF DATA WAREHOUSE, DATA LAKE & LAKEHOUSE
--------------------------------------------------------------------------------

Aim:
To simulate and compare Data Warehouse, Data Lake, and Data Lakehouse architectures using Python, SQLite3, Parquet, and DuckDB by storing datasets across multiple formats and evaluating schema strategy, file size, and query performance.

Theory:
Modern data platforms rely on three primary storage architectures:
1. Data Warehouse (Schema-on-Write): Stores structured, cleaned, and transformed data in relational tables optimized for SQL analytics and BI (simulated using SQLite3). Enforces strict schema integrity before loading.
2. Data Lake (Schema-on-Read): Stores vast volumes of raw structured (CSV), semi-structured (JSON), and unstructured (log/text) files in native formats at low cost without upfront schema enforcement.
3. Data Lakehouse (Hybrid Architecture): Combines the low-cost open file storage of a Data Lake (such as columnar Apache Parquet files) with the ACID transactions, metadata management, and high-speed SQL query performance of a Data Warehouse (simulated using DuckDB directly over Parquet files).

Procedure:
1. Import os, time, json, sqlite3, duckdb, and pandas.
2. Simulate a Data Warehouse by loading cleaned tabular records into a SQLite database (warehouse.db) and executing SQL GROUP BY aggregation queries.
3. Benchmark storage efficiency and read latency by saving the dataset in CSV, JSON, and columnar Parquet formats and measuring file sizes (KB) and load times (ms).
4. Simulate a Data Lake directory (data_lake/) storing multi-format raw files: raw CSV data, semi-structured JSON records, and unstructured ingestion log text files.
5. Simulate a Data Lakehouse by querying the open Parquet file directly with SQL using the DuckDB analytical engine without importing into a traditional database.
6. Perform automated data quality checks (duplicate and null counts) and demonstrate incremental append updates to the warehouse table.

Pseudocode:
BEGIN
    IMPORT os, time, json, sqlite3, duckdb, pandas
    LOAD df <- READ_CSV("dataset.csv")

    // 1. Data Warehouse Simulation (SQLite - Schema-on-Write)
    CONNECT dw_conn <- SQLITE_CONNECT("warehouse.db")
    WRITE df TO SQL_TABLE("dw_table", dw_conn, if_exists="replace")
    EXECUTE SQL_QUERY("SELECT group_col, COUNT(*), AVG(val_col) FROM dw_table GROUP BY group_col")

    // 2. Storage Format Benchmark (CSV vs JSON vs Parquet)
    FOR EACH fmt IN ["CSV", "JSON", "Parquet"] DO
        WRITE df TO file_in_format(fmt)
        START_TIMER()
        READ file_in_format(fmt)
        RECORD load_time_ms AND file_size_kb
    END FOR
    PRINT storage benchmark comparison table

    // 3. Data Lake Simulation (Schema-on-Read Multi-Format Repository)
    CREATE DIRECTORY "data_lake"
    SAVE raw CSV, sample JSON, AND unstructured text log INTO "data_lake/"

    // 4. Data Lakehouse Simulation (Open Parquet + DuckDB SQL Engine)
    EXECUTE lh_result <- DUCKDB_SQL("SELECT group_col, COUNT(*), SUM(val_col) FROM 'store.parquet' GROUP BY group_col")
    PRINT lh_result

    // 5. Data Quality Audit & Incremental Pipeline
    CHECK duplicate_count AND null_count ON df
    APPEND new_records TO SQL_TABLE("dw_table", dw_conn, if_exists="append")
END

Conclusion:
Successfully simulated and compared Data Warehouse (SQLite), Data Lake (multi-format raw storage), and Data Lakehouse (Parquet + DuckDB) architectures, demonstrating that Parquet with DuckDB delivers compact columnar storage alongside fast direct SQL analytics.
