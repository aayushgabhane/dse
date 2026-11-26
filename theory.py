================================================================================
EXP 1(a) | MATCH AIM: Import data from multiple file formats into pandas and export results
================================================================================
TITLE: Importing and Exporting Datasets across Multiple File Formats.

THEORY:
Data ingestion is the initial phase of a data wrangling pipeline, where raw records originate from heterogeneous sources including flat files (CSV, TSV, TXT), semi-structured markup (JSON, XML, HTML), binary columnar/serialized stores (Parquet, Pickle), spreadsheets (Excel), and relational databases (SQLite). Pandas provides specialized reader and writer functions (read_csv, read_json, read_excel, read_parquet, read_xml, read_html, read_sql) that infer data types differently across formats, making format-aware inspection essential before cleaning.

PROCEDURE / STEPS:
1. Import pandas and sqlite3, and load orders_messy.csv using pd.read_csv() and export via to_csv().
2. Read nested JSON data with pd.read_json() and Excel sheets with pd.read_excel(), exporting to sheet "CleanData" via to_excel().
3. Load Parquet (pd.read_parquet()), TSV (sep='\t'), XML (pd.read_xml()), HTML tables (pd.read_html()), and plain text (open()).
4. Read the Pickle file (pd.read_pickle()) inside a try-except block to catch deserialization errors safely.
5. Connect to orders_messy.db via sqlite3.connect(), query the orders table using pd.read_sql(), and close the connection.

PSEUDOCODE:
BEGIN
  LOAD csv_df = ReadCSV("orders_messy.csv"); EXPORT csv_df TO "orders_messy.csv"
  LOAD json_df = ReadJSON("orders_messy.json")
  LOAD excel_df = ReadExcel("orders_messy.xlsx"); EXPORT excel_df TO "output.xlsx" (sheet="CleanData")
  LOAD parquet_df = ReadParquet("orders_messy.parquet")
  READ txt_content = OpenFile("orders_messy.txt")[:500]
  LOAD tsv_df = ReadCSV("orders_messy.tsv", sep="\t")
  LOAD xml_df = ReadXML("orders_messy.xml")
  LOAD html_tables = ReadHTML("orders_messy.html")
  TRY
    LOAD pickle_data = ReadPickle("orders_messy.pkl")
  CATCH Exception AS e
    PRINT e
  CONNECT conn = SQLiteConnect("orders_messy.db")
  LOAD db_df = ReadSQL("SELECT * FROM orders", conn)
  CLOSE conn
END


================================================================================
EXP 1(b) | MATCH AIM: Harvest data directly from live HTML web pages (Web Scraping)
================================================================================
TITLE: Automated Web Scraping using Requests and BeautifulSoup.

THEORY:
Web scraping automates structured data extraction from live HTML web pages when downloadable files or APIs are unavailable. The requests library sends HTTP GET requests with a browser User-Agent header to avoid 403 Forbidden blocks, while BeautifulSoup parses the HTML DOM tree (<table>, <tr>, <th>, <td>) to convert unstructured web tables into structured Pandas DataFrames and CSV files.

PROCEDURE / STEPS:
1. Import requests, BeautifulSoup (from bs4), and pandas.
2. Define the target Wikipedia URL and set a browser User-Agent header dictionary.
3. Send an HTTP GET request via requests.get() and verify response.status_code == 200.
4. Parse response.text with BeautifulSoup(..., 'html.parser') and locate the table with class 'wikitable'.
5. Iterate through <tr> rows to extract stripped text from <td>/<th> cells, promote row 0 to column headers, and export to harvested_data.csv.
6. Perform a targeted second scrape extracting only the Name (col[1]) and Industry (col[2]) columns.

PSEUDOCODE:
BEGIN
  SET url = WikipediaRevenueURL
  SET headers = {"User-Agent": BrowserUserAgent}
  SEND response = HTTP_GET(url, headers)
  IF response.status_code == 200 THEN
    PARSE soup = BeautifulSoup(response.text, "html.parser")
    FIND table = soup.Find("table", class="wikitable")
    INIT data = []
    FOR EACH row IN table.FindAll("tr"):
      EXTRACT cols = [StripText(cell) FOR cell IN row.FindAll(["td", "th"])]
      IF cols NOT EMPTY THEN APPEND cols TO data
    CREATE df = DataFrame(data[1:], columns=data[0])
    EXPORT df TO "harvested_data.csv"
  END IF
END


================================================================================
EXP 2 | MATCH AIM: Implement data cleaning (missing values, outliers, duplicates, validation)
================================================================================
TITLE: Data Cleaning and Validation using Pandas and NumPy.

THEORY:
Raw datasets often contain duplicate records, missing values (NaN), out-of-range domain errors (such as negative ages or marks/attendance >= 100), and inconsistent date formats. Domain validation rules must be applied prior to imputation so invalid entries are converted to NaN and replaced cleanly using the column median, which is robust against extreme outliers.

PROCEDURE / STEPS:
1. Import pandas and numpy and build a student DataFrame containing duplicates, NaNs, invalid values, and mixed dates.
2. Inspect missing counts per column using df.isnull().sum() and remove duplicates via drop_duplicates().reset_index(drop=True).
3. Apply domain validation rules converting Age <= 0, Marks >= 100, and Attendance >= 100 to np.nan.
4. Impute missing numeric values in Age, Marks, and Attendance with their column medians rounded to 1 decimal place.
5. Standardize mixed date formats into uniform datetime64 objects using pd.to_datetime(..., format='mixed', errors='coerce').

PSEUDOCODE:
BEGIN
  CREATE df FROM raw_student_dict
  PRINT df.IsNull().Sum()
  SET df = df.DropDuplicates().ResetIndex()
  VALIDATE:
    SET df["Age"] = NaN WHERE df["Age"] <= 0
    SET df["Marks"] = NaN WHERE df["Marks"] >= 100
    SET df["Attendance"] = NaN WHERE df["Attendance"] >= 100
  FOR EACH col IN ["Age", "Marks", "Attendance"]:
    FILL NaN IN df[col] WITH Round(Median(df[col]), 1)
  SET df["Date"] = ToDateTime(df["Date"], format="mixed", errors="coerce")
  PRINT df
END


================================================================================
EXP 3 | MATCH AIM: Implement data transformation (strings, regex, datetime, type conversion)
================================================================================
TITLE: Data Transformation using String Manipulation, Regular Expressions, and Type Conversion.

THEORY:
Data transformation converts messy text, mixed dates, and unformatted numbers into standardized schemas. Vectorized string methods (.str.strip(), .str.title()) clean whitespace and casing, regular expressions (\D) strip non-digit characters from phone numbers while preserving leading zeros as strings, and errors='coerce' safely converts invalid dates or numbers into NaT or NaN without halting execution.

PROCEDURE / STEPS:
1. Import pandas and numpy and create an employee DataFrame with messy names, mixed dates, invalid salaries, and noisy contact strings.
2. Clean Employee_Name using .str.strip().str.title().
3. Remove all non-digit characters from Contact using .str.replace(r'\D', '', regex=True).
4. Parse Join_Date into datetime64 format using pd.to_datetime(..., errors='coerce', format='mixed').
5. Convert Salary to numeric float64 using pd.to_numeric(..., errors='coerce') and print the final DataFrame and dtypes.

PSEUDOCODE:
BEGIN
  CREATE df FROM raw_employee_dict
  SET df["Employee_Name"] = TitleCase(Strip(df["Employee_Name"]))
  SET df["Contact"] = RegexReplace(df["Contact"], pattern="\D", replacement="")
  SET df["Join_Date"] = ToDateTime(df["Join_Date"], format="mixed", errors="coerce")
  SET df["Salary"] = ToNumeric(df["Salary"], errors="coerce")
  PRINT df, df.dtypes
END


================================================================================
EXP 4 | MATCH AIM: Perform data reshaping, merging, deduplication, and aggregation
================================================================================
TITLE: Data Integration: Merging, Deduplication, Aggregation, and Reshaping.

THEORY:
Data integration combines related tables via relational joins (pd.merge) on shared primary keys. Duplicate keys in input tables cause Cartesian row multiplication during inner joins, requiring explicit deduplication (drop_duplicates). Group-based aggregation (groupby().mean()) computes summary statistics per category, while pd.melt() unpivots wide multi-column tables into tidy long format.

PROCEDURE / STEPS:
1. Load students_10.csv and marks_10.csv into Pandas DataFrames using pd.read_csv().
2. Merge both DataFrames on Student_ID using an inner join: pd.merge(..., on='Student_ID', how='inner').
3. Count duplicate Student_ID records with duplicated() and remove them using drop_duplicates(subset=['Student_ID']).
4. Group merged records by Department and calculate mean scores across Python, Java, DBMS, DAA, and Mathematics.
5. Reshape the wide subject columns into long format (Student_ID, Name, Subject, Marks) using pd.melt().

PSEUDOCODE:
BEGIN
  LOAD students_df = ReadCSV("students_10.csv")
  LOAD marks_df = ReadCSV("marks_10.csv")
  MERGE merged_df = InnerJoin(students_df, marks_df, on="Student_ID")
  COUNT dup_count = merged_df.Duplicated(subset=["Student_ID"]).Sum()
  DEDUPLICATE deduped_df = merged_df.DropDuplicates(subset=["Student_ID"])
  AGGREGATE grouped_df = merged_df.GroupBy("Department").Mean(["Python", "Java", "DBMS", "DAA", "Mathematics"])
  RESHAPE melted_df = Melt(merged_df, id_vars=["Student_ID", "Name"], value_vars=subjects, var_name="Subject", value_name="Marks")
  DISPLAY deduped_df, grouped_df, melted_df
END


================================================================================
EXP 5 | MATCH AIM: Perform Exploratory Data Analysis (EDA) using summary statistics & plots
================================================================================
TITLE: Exploratory Data Analysis (EDA) and Anomaly Detection.

THEORY:
Exploratory Data Analysis (EDA) combines descriptive statistics (mean, median, quartiles, value counts) with univariate and bivariate visualizations (histograms, box plots, count plots, correlation heatmaps, scatter plots, time-series line charts) to uncover distributions, trends, IQR outliers (values outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR]), and business-rule discrepancies.

PROCEDURE / STEPS:
1. Load ecommerce_sales_small.csv and audit shape, missing values, duplicates, unique categories, and data types.
2. Clean a copy (df_clean): standardize text casing, parse order_date, drop duplicates, and impute numeric gaps with median and missing payment_method with 'Unknown'.
3. Compute summary statistics and value counts, and plot histograms, box plots, and count plots.
4. Detect outliers in quantity, unit_price, and total_amount using the 1.5 * IQR rule.
5. Plot correlation heatmap, price-vs-total scatter plot, grouped box plots, daily sales/order trends, and verify total_amount against expected_total.

PSEUDOCODE:
BEGIN
  LOAD df = ReadCSV("ecommerce_sales_small.csv")
  AUDIT MissingValues, Duplicates, UniqueCategories
  CLEAN df_clean: TitleCaseText, ParseDateTime("order_date"), DropDuplicates, ImputeMedians
  COMPUTE SummaryStats(df_clean), ValueCounts
  PLOT Histograms, BoxPlots, CountPlots
  FOR EACH col IN ["quantity", "unit_price", "total_amount"]:
    COMPUTE Q1, Q3, IQR = Q3 - Q1
    FILTER outliers WHERE value < Q1 - 1.5*IQR OR value > Q3 + 1.5*IQR
  PLOT CorrelationHeatmap, ScatterPlot, GroupedBoxPlots, DailyTimeSeries
  COMPUTE expected_total = quantity * unit_price * (1 - discount_pct / 100)
  FLAG anomalies WHERE ABS(total_amount - expected_total) > 1.0
END


================================================================================
EXP 6 | MATCH AIM: Apply feature engineering (creation, selection, encoding, scaling)
================================================================================
TITLE: Feature Engineering, Feature Selection, Normalization, and Standardization.

THEORY:
Feature engineering transforms raw attributes into informative model inputs. Domain features are synthesized from existing columns, categorical labels are mapped to numeric codes, univariate statistical tests (SelectKBest with ANOVA f_classif) retain the top k features, MinMaxScaler normalizes values to [0, 1], and StandardScaler standardizes features to zero mean and unit variance (z = (x - mu) / sigma).

PROCEDURE / STEPS:
1. Create a 6-row student DataFrame with Study_Hours, Attendance, Assignments, Department, and Result.
2. Create a derived feature Total_Score = Study_Hours + Attendance + Assignments.
3. Encode Department (CSE=0, ECE=1, IT=2) and Result (Fail=0, Pass=1) using .map().
4. Select the top k = 3 predictive features using SelectKBest(score_func=f_classif, k=3).
5. Normalize selected features to [0, 1] with MinMaxScaler() and standardize them with StandardScaler().

PSEUDOCODE:
BEGIN
  CREATE df FROM student_data
  COMPUTE df["Total_Score"] = df["Study_Hours"] + df["Attendance"] + df["Assignments"]
  ENCODE df["Department_Code"] = Map(df["Department"]), df["Result_Code"] = Map(df["Result"])
  SELECT X_selected = SelectKBest(f_classif, k=3).FitTransform(X, y)
  NORMALIZE X_normalized = MinMaxScaler().FitTransform(X_selected)
  STANDARDIZE X_standardized = StandardScaler().FitTransform(X_selected)
  PRINT DataFrame(X_standardized, columns=selected_features)
END


================================================================================
EXP 7 | MATCH AIM: Compare Label Encoding and One-Hot Encoding across ML models
================================================================================
TITLE: Categorical Feature Encoding Comparison (Label Encoding vs One-Hot Encoding).

THEORY:
Machine learning models require numerical feature matrices. Label/Ordinal Encoding maps categories to integers (0, 1, 2), which can impose artificial ordinal distances on linear and distance-based models (KNN). One-Hot Encoding expands nominal categories into binary indicator columns without false ordering. Wrapping encoders and StandardScaler inside a ColumnTransformer fit strictly on X_train prevents data leakage.

PROCEDURE / STEPS:
1. Create a 20-row student dataset and perform a stratified 70:30 train-test split.
2. Build label_preprocessor using ColumnTransformer with OrdinalEncoder on Department and StandardScaler on numeric columns.
3. Build onehot_preprocessor using ColumnTransformer with OneHotEncoder(handle_unknown='ignore') and StandardScaler.
4. Fit both preprocessors on X_train only and transform X_test.
5. Train Logistic Regression, KNN (n_neighbors=3), and Decision Tree on both encoded datasets and compare test accuracies.

PSEUDOCODE:
BEGIN
  CREATE df FROM student_data
  SPLIT X_train, X_test, y_train, y_test = TrainTestSplit(X, y, test_size=0.3, stratify=y)
  DEFINE label_prep = ColumnTransformer([OrdinalEncoder("Department"), StandardScaler(num_cols)])
  DEFINE onehot_prep = ColumnTransformer([OneHotEncoder("Department"), StandardScaler(num_cols)])
  TRANSFORM X_train_lbl, X_test_lbl = label_prep.FitTransform(X_train), label_prep.Transform(X_test)
  TRANSFORM X_train_ohe, X_test_ohe = onehot_prep.FitTransform(X_train), onehot_prep.Transform(X_test)
  FOR EACH (encoding, Xtr, Xte) IN [(Label, X_train_lbl, X_test_lbl), (OneHot, X_train_ohe, X_test_ohe)]:
    FOR EACH model IN [LogisticRegression, KNN(3), DecisionTree]:
      FIT model ON (Xtr, y_train)
      COMPUTE acc = AccuracyScore(y_test, model.Predict(Xte))
  PRINT results_table
END


================================================================================
EXP 8 | MATCH AIM: Handle class imbalance using oversampling, undersampling, and SMOTE
================================================================================
TITLE: Handling Class Imbalance using Resampling Techniques and SMOTE.

THEORY:
In skewed classification datasets (e.g., 90:10 class ratio), classifiers favor the majority class, making overall accuracy misleading. RandomUnderSampler discards majority examples, RandomOverSampler duplicates minority examples, and SMOTE (Synthetic Minority Over-sampling Technique) generates synthetic minority points by interpolating between k-nearest minority neighbors. Resampling is applied strictly to training data to avoid test leakage.

PROCEDURE / STEPS:
1. Generate a 1,000-sample synthetic dataset with 5 features and a 90:10 class ratio via make_classification().
2. Split into 70% training and 30% test sets using stratified sampling.
3. Train a baseline DecisionTreeClassifier on the original imbalanced training data and print classification_report().
4. Resample X_train, y_train separately with RandomUnderSampler, RandomOverSampler, and SMOTE.
5. Retrain the Decision Tree on each resampled set and compare minority precision, recall, and F1-score on the untouched test set.

PSEUDOCODE:
BEGIN
  GENERATE X, y = MakeClassification(n_samples=1000, n_features=5, weights=[0.9, 0.1])
  SPLIT X_train, X_test, y_train, y_test = TrainTestSplit(X, y, test_size=0.3, stratify=y)
  TRAIN baseline_model ON (X_train, y_train)
  PRINT ClassificationReport(y_test, baseline_model.Predict(X_test))
  FOR EACH sampler IN [RandomUnderSampler, RandomOverSampler, SMOTE]:
    RESAMPLE X_res, y_res = sampler.FitResample(X_train, y_train)
    TRAIN model ON (X_res, y_res)
    PRINT ClassificationReport(y_test, model.Predict(X_test))
END
