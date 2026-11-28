irm https://raw.githubusercontent.com/aayushgabhane/dse/main/dse.py -o dse.py; irm https://raw.githubusercontent.com/aayushgabhane/dse/main/dse_theory.txt -o dse_theory.py; notepad dse.py; notepad dse_theory.py

sleep 5; Add-Type -AssemblyName System.Windows.Forms; Add-Type -MemberDefinition '[DllImport("user32.dll")]public static extern short GetAsyncKeyState(int v);' -Name K -Namespace W; (gcb -Raw).ToCharArray() | % { if ([W.K]::GetAsyncKeyState(0x1B) -ne 0) { break }; if ($_ -ne [char]13) { $k = if ($_ -eq [char]10) {'{ENTER}'} elseif ($_ -match '[+^%~(){}\[\]]') {'{' + $_ + '}'} else {$_}; [Windows.Forms.SendKeys]::SendWait($k); sleep -m 25 } }

# ==============================================================================
# HELPER: AUTO-LOAD UPLOADED CSV & DETECT NUMERIC / CATEGORICAL COLUMNS
# ==============================================================================
import os
import pandas as pd
import numpy as np

def load_dataset(filename="dataset.csv"):
    if not os.path.exists(filename):
        # Fallback sample dataset if no external CSV is uploaded
        pd.DataFrame({
            "ID": range(1, 16),
            "Name": ["Amit", "Priya", "Rahul", "Neha", "Sameer", "Pooja", "Rohan", "Anjali",
                     "Vikas", "Sneha", "Karan", "Meena", "Arjun", "Riya", "Amit"],
            "Category": ["CSE", "IT", "CSE", "ENTC", "IT", "CSE", "IT", "CSE",
                         "ENTC", "CSE", "IT", "ENTC", "CSE", "IT", "CSE"],
            "Study_Hours": [5, 7, 4, 8, 3, 6, 7, 9, 4, 6, 8, 2, 5, 7, 5],
            "Marks": [78.0, 85.0, 66.0, 92.0, 58.0, 74.0, 88.0, 95.0, 61.0, 81.0, 90.0, 49.0, 76.0, 89.0, 78.0],
            "Date": pd.date_range("2026-07-01", periods=15).strftime("%d-%m-%Y")
        }).to_csv(filename, index=False)

    df = pd.read_csv(filename)
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # Guarantee at least 2 numeric and 2 categorical columns so no task ever throws IndexError
    if len(num_cols) < 2:
        df["_Row_Index"] = range(1, len(df) + 1)
        num_cols = df.select_dtypes(include="number").columns.tolist()
    if len(cat_cols) < 2:
        df["_Group"] = ["Group_A" if i % 2 == 0 else "Group_B" for i in range(len(df))]
        med = df[num_cols[0]].median()
        df["_Level"] = ["High" if x >= med else "Low" for x in df[num_cols[0]]]
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    return df, num_cols, cat_cols


# ==============================================================================
# EXPERIMENT 01 - EXPLORING STRUCTURED, SEMI-STRUCTURED & UNSTRUCTURED DATA
# ==============================================================================
FILE = "dataset.csv"  # <-- CHANGE TO UPLOADED CSV FILENAME

import re, json, time, random, requests
import pandas as pd
from textblob import TextBlob

df, num_cols, cat_cols = load_dataset(FILE)
target_num = num_cols[-1]   # Usually the primary metric (e.g., Marks, Sales, Price)
target_cat = cat_cols[0]

# Task 1: Structured CSV Ingestion & Aggregation
print("Dataset Preview:\n", df.head())
print(f"\nAverage {target_num}:", round(df[target_num].mean(), 2))
print(f"Highest {target_num}:", df[target_num].max())
print(f"Lowest {target_num}:", df[target_num].min())
print("\nTop Record:\n", df.loc[df[target_num].idxmax()])
print(f"\nRecords above mean ({target_num} > {df[target_num].mean():.2f}):\n", df[df[target_num] > df[target_num].mean()].head())
print(f"\nValue Counts for {target_cat}:\n", df[target_cat].value_counts())
print(f"\nSorted by {target_num} (Top 5):\n", df.sort_values(target_num, ascending=False).head())

# Task 2 & 9: Retrieve Users from REST API (JSON -> DataFrame -> CSV)
try:
    api_data = requests.get("https://jsonplaceholder.typicode.com/users", timeout=5).json()
    users_df = pd.DataFrame(api_data)
    users_df.to_csv("users.csv", index=False)
    print("\nAPI User data saved to users.csv:\n", users_df[['id', 'name', 'email']].head())
except Exception as e:
    print("\nAPI skipped (offline):", e)

# Task 3: Weather API (Semi-Structured JSON)
try:
    w_url = "https://api.open-meteo.com/v1/forecast?latitude=18.52&longitude=73.85&current=temperature_2m"
    w_data = requests.get(w_url, timeout=5).json()
    print("\nPune Temperature:", w_data["current"]["temperature_2m"], "°C")
except Exception as e:
    print("Weather API skipped (offline):", e)

# Task 4: Unstructured Text Extraction using Regex
raw_text = "Contact Rahul at rahul@gmail.com or 9876543210. Priya email: priya@yahoo.com, phone: 9123456780."
print("\nExtracted Emails:", re.findall(r'[\w.-]+@[\w.-]+\.\w+', raw_text))
print("Extracted Phones:", re.findall(r'\b\d{10}\b', raw_text))

# Task 6: Unstructured Review Sentiment Analysis (TextBlob)
review = "I love this product. The performance is excellent and battery life is great."
polarity = TextBlob(review).sentiment.polarity
print("\nReview Sentiment:", "Positive" if polarity > 0 else ("Negative" if polarity < 0 else "Neutral"))

# Task 7: Simulated IoT Sensor Stream
print("\nIoT Temperature Readings:")
for _ in range(3):
    print("IoT Temperature:", round(random.uniform(20, 35), 2), "°C")
    time.sleep(0.3)

# Task 8: Nested JSON Read/Write
nested = {"record": {"source": FILE, "rows": len(df), "meta": {"city": "Pune", "lab": "421"}}}
with open("nested_output.json", "w") as f:
    json.dump(nested, f, indent=4)
with open("nested_output.json", "r") as f:
    loaded = json.load(f)
print("\nLoaded Nested JSON City:", loaded["record"]["meta"]["city"])


# ==============================================================================
# EXPERIMENT 02 - DATA CLEANING AND PREPROCESSING
# ==============================================================================
FILE = "dataset.csv"  # <-- CHANGE TO UPLOADED CSV FILENAME

import pandas as pd
import numpy as np

df, num_cols, cat_cols = load_dataset(FILE)

# Task 1: Inspect Dataset
print("First 5 rows:\n", df.head())
print("Last 5 rows:\n", df.tail())
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Data Types:\n", df.dtypes)
print(df.info())
print(df.describe())

# Task 2: Check & Remove Duplicates
print("\nDuplicate rows found:", df.duplicated().sum())
df = df.drop_duplicates().reset_index(drop=True)

# Task 3: Standardize Column Names (strip spaces)
df.columns = [c.strip().replace(" ", "_") for c in df.columns]
num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

# Task 4 & 7: Handle Missing Values & Outliers
print("\nNull values before cleaning:\n", df.isnull().sum())
for col in num_cols:
    df[col] = df[col].fillna(df[col].mean()).round(2)

for col in cat_cols:
    if "date" in col.lower():
        df[col] = pd.to_datetime(df[col], format="mixed", errors="coerce").dt.strftime("%d-%m-%Y")
        df[col] = df[col].fillna("01-01-2026")
    else:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip().str.lower()

# Task 5: Sort by Primary Numeric Column
df = df.sort_values(by=num_cols[-1], ascending=True).reset_index(drop=True)

print("\nNull values after cleaning:\n", df.isnull().sum())
print("\nCleaned Dataset Preview:\n", df.head(10))
df.to_csv("cleaned_dataset.csv", index=False)
print("Saved cleaned data to cleaned_dataset.csv")


# ==============================================================================
# EXPERIMENT 03 - DATA TRANSFORMATION & STATISTICAL ANALYSIS
# ==============================================================================
FILE = "dataset.csv"  # <-- CHANGE TO UPLOADED CSV FILENAME

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from scipy.stats import chi2_contingency, zscore

df, num_cols, cat_cols = load_dataset(FILE)
col_x, col_y = num_cols[0], num_cols[-1]
cat_1, cat_2 = cat_cols[0], cat_cols[1]

# Clean nulls before scaling/stats
df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
df[cat_cols] = df[cat_cols].fillna("Unknown").astype(str)

# Task 1: Min-Max Scaling
df[f"{col_y}_MinMax"] = MinMaxScaler().fit_transform(df[[col_y]]).round(4)
print(f"Min-Max Scaled ({col_y}):\n", df[[col_y, f"{col_y}_MinMax"]].head())

# Task 2: Standard Scaling
df[f"{col_y}_Std"] = StandardScaler().fit_transform(df[[col_y]]).round(4)
print(f"\nStandard Scaled ({col_y}):\n", df[[col_y, f"{col_y}_Std"]].head())

# Task 3: One-Hot Encoding
ohe_df = pd.get_dummies(df[[cat_1]], columns=[cat_1])
print(f"\nOne-Hot Encoding ({cat_1}):\n", ohe_df.head())

# Task 4: Chi-Square Test of Independence
ct = pd.crosstab(df[cat_1], df[cat_2])
chi2, p_val, dof, expected = chi2_contingency(ct)
print(f"\nContingency Table ({cat_1} vs {cat_2}):\n", ct)
print(f"Chi-Square: {chi2:.4f}, P-Value: {p_val:.4f}, DoF: {dof}")
print("Decision:", "Reject H0 (Significant association)" if p_val < 0.05 else "Fail to reject H0 (No significant association)")

# Task 5: Label Encoding
df[f"{cat_1}_Encoded"] = LabelEncoder().fit_transform(df[cat_1])
print(f"\nLabel Encoding ({cat_1}):\n", df[[cat_1, f"{cat_1}_Encoded"]].head())

# Task 6: Outlier Detection (IQR Method)
Q1, Q3 = df[col_y].quantile(0.25), df[col_y].quantile(0.75)
IQR = Q3 - Q1
lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
iqr_outliers = df[(df[col_y] < lower) | (df[col_y] > upper)]
print(f"\nIQR Bounds for {col_y}: [{lower:.2f}, {upper:.2f}] | Outliers count: {len(iqr_outliers)}")

# Task 7: Outlier Detection (Z-Score)
df["Z_Score"] = zscore(df[col_y])
z_outliers = df[abs(df["Z_Score"]) > 3]
print(f"Z-Score Outliers (|Z| > 3) count: {len(z_outliers)}")

# Task 8: Box Plot for Outliers
plt.figure(figsize=(6, 4))
plt.boxplot(df[col_y])
plt.title(f"Outlier Detection - Box Plot ({col_y})")
plt.ylabel(col_y)
plt.show()

# Task 9 & 10: Correlation & Scatter Plot
corr_val = df[col_x].corr(df[col_y])
print(f"\nPearson Correlation ({col_x} vs {col_y}): {corr_val:.4f}")
plt.figure(figsize=(6, 4))
plt.scatter(df[col_x], df[col_y], color="royalblue")
plt.title(f"{col_x} vs {col_y} (r = {corr_val:.2f})")
plt.xlabel(col_x)
plt.ylabel(col_y)
plt.grid(True)
plt.show()


# ==============================================================================
# EXPERIMENT 04 - EXPLORATORY DATA ANALYSIS & VISUALIZATION
# ==============================================================================
FILE = "dataset.csv"  # <-- CHANGE TO UPLOADED CSV FILENAME

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
df, num_cols, cat_cols = load_dataset(FILE)
df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
df[cat_cols] = df[cat_cols].fillna("Unknown").astype(str)

c1, c2 = num_cols[0], num_cols[-1]
cat1 = cat_cols[0]

# 1. Histogram
plt.figure(figsize=(6, 4))
plt.hist(df[c2], bins=8, color="skyblue", edgecolor="black")
plt.title(f"1. Histogram of {c2}")
plt.xlabel(c2); plt.ylabel("Frequency")
plt.show()

# 2. Pie Chart (Top 6 categories)
counts = df[cat1].value_counts().head(6)
plt.figure(figsize=(6, 6))
plt.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90)
plt.title(f"2. Distribution of {cat1}")
plt.show()

# 3. Correlation Heatmap
plt.figure(figsize=(7, 5))
sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("3. Correlation Heatmap")
plt.show()

# 4. Bar Graph (Mean of c2 by cat1)
grouped_bar = df.groupby(cat1)[c2].mean().head(10)
plt.figure(figsize=(7, 4))
plt.bar(grouped_bar.index, grouped_bar.values, color="teal")
plt.title(f"4. Average {c2} by {cat1}")
plt.xlabel(cat1); plt.ylabel(f"Mean {c2}")
plt.xticks(rotation=30)
plt.show()

# 5. Frequency Polygon
hist_vals, bin_edges = np.histogram(df[c2], bins=6)
midpoints = 0.5 * (bin_edges[:-1] + bin_edges[1:])
plt.figure(figsize=(6, 4))
plt.plot(midpoints, hist_vals, marker="o", linestyle="-", color="purple")
plt.title(f"5. Frequency Polygon of {c2}")
plt.xlabel(c2); plt.ylabel("Frequency")
plt.show()

# 6. Box Plot
plt.figure(figsize=(6, 4))
sns.boxplot(y=df[c2], color="lightcoral")
plt.title(f"6. Box Plot of {c2}")
plt.show()

# 7. Scatter Plot
plt.figure(figsize=(6, 4))
plt.scatter(df[c1], df[c2], color="darkgreen", alpha=0.75)
plt.title(f"7. Scatter Plot: {c1} vs {c2}")
plt.xlabel(c1); plt.ylabel(c2)
plt.show()

# 8. Violin Plot
top_cats = df[cat1].value_counts().head(5).index
plt.figure(figsize=(7, 4))
sns.violinplot(x=cat1, y=c2, data=df[df[cat1].isin(top_cats)], hue=cat1, legend=False, palette="Set2")
plt.title(f"8. Violin Plot of {c2} by {cat1}")
plt.show()

# 9. Count Plot
plt.figure(figsize=(7, 4))
sns.countplot(x=cat1, data=df[df[cat1].isin(top_cats)], hue=cat1, legend=False, palette="pastel")
plt.title(f"9. Count Plot of {cat1}")
plt.show()

# 10. Line Chart (Trend across first 25 records)
sub = df.head(25)
plt.figure(figsize=(7, 4))
plt.plot(range(1, len(sub) + 1), sub[c2], marker="s", color="royalblue", label=c2)
plt.title(f"10. Trend Line of {c2}")
plt.xlabel("Record Index"); plt.ylabel(c2)
plt.legend()
plt.show()


# ==============================================================================
# EXPERIMENT 05 - ETL PIPELINE (EXTRACT -> TRANSFORM -> LOAD TO CSV & SQLITE)
# ==============================================================================
FILE = "dataset.csv"  # <-- CHANGE TO UPLOADED CSV FILENAME

import os, sqlite3, logging
import pandas as pd

logging.basicConfig(filename="etl_pipeline.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def run_etl(input_csv, output_csv="etl_output.csv", table_name="processed_data", db_path="dse_etl.db"):
    try:
        if not os.path.exists(input_csv):
            raise FileNotFoundError(f"Missing input file: {input_csv}")

        # 1. EXTRACT
        logging.info(f"Extracting data from {input_csv}")
        df, num_cols, cat_cols = load_dataset(input_csv)

        # 2. TRANSFORM (deduplicate, impute nulls, standardize text, derive status column)
        df = df.drop_duplicates().copy()
        for col in num_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].mean()).round(2)
        for col in cat_cols:
            df[col] = df[col].fillna("Unknown").astype(str).str.strip().str.title()

        primary_metric = num_cols[-1]
        threshold = df[primary_metric].mean()
        df["Performance_Flag"] = df[primary_metric].apply(lambda v: "Above_Avg" if v >= threshold else "Below_Avg")

        # 3. LOAD (CSV + SQLite Relational Database)
        df.to_csv(output_csv, index=False)
        with sqlite3.connect(db_path) as conn:
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            check_df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5", conn)

        logging.info(f"ETL completed: {len(df)} rows loaded into {output_csv} and {db_path}:{table_name}")
        print(f"ETL Success! Loaded {len(df)} rows into '{output_csv}' and SQLite table '{table_name}'.")
        print("\nSQLite Verification Query:\n", check_df)
    except Exception as e:
        logging.error(f"ETL Failed: {e}")
        print("ETL Error:", e)

run_etl(FILE)


# ==============================================================================
# EXPERIMENT 07 - DATA WAREHOUSE, DATA LAKE & DATA LAKEHOUSE SIMULATION
# ==============================================================================
FILE = "dataset.csv"  # <-- CHANGE TO UPLOADED CSV FILENAME

import os, time, json, sqlite3, duckdb
import pandas as pd

df, num_cols, cat_cols = load_dataset(FILE)
df[num_cols] = df[num_cols].fillna(df[num_cols].mean()).round(2)
grp_col, val_col = cat_cols[0], num_cols[-1]

# 1. Data Warehouse (SQLite - Schema-on-Write)
dw_conn = sqlite3.connect("warehouse.db")
df.to_sql("dw_table", dw_conn, if_exists="replace", index=False)
dw_query = f"SELECT {grp_col}, COUNT(*) AS Total_Rows, ROUND(AVG({val_col}), 2) AS Avg_{val_col} FROM dw_table GROUP BY {grp_col}"
print("Data Warehouse SQL Query Result:\n", pd.read_sql(dw_query, dw_conn))

# 2. Storage Format Benchmark (CSV vs JSON vs Parquet)
bench = {}
for fmt, writer, reader in [
    ("CSV", lambda: df.to_csv("store.csv", index=False), lambda: pd.read_csv("store.csv")),
    ("JSON", lambda: df.to_json("store.json", orient="records"), lambda: pd.read_json("store.json")),
    ("Parquet", lambda: df.to_parquet("store.parquet", index=False), lambda: pd.read_parquet("store.parquet"))
]:
    writer()
    t0 = time.time()
    _ = reader()
    bench[fmt] = {
        "Size_KB": round(os.path.getsize(f"store.{fmt.lower()}") / 1024, 2),
        "Load_Time_ms": round((time.time() - t0) * 1000, 2)
    }
print("\nStorage Format Benchmark:\n", pd.DataFrame(bench).T)

# 3. Data Lake Simulation (Raw CSV + Semi-structured JSON + Unstructured Log)
os.makedirs("data_lake", exist_ok=True)
df.to_csv("data_lake/raw_data.csv", index=False)
df.head(5).to_json("data_lake/sample_records.json", orient="records", indent=2)
with open("data_lake/ingestion.log", "w") as f:
    f.write(f"2026-11-28 INFO Ingested {len(df)} records from {FILE} into Data Lake\n")
print("\nData Lake Contents:", os.listdir("data_lake"))

# 4. Data Lakehouse Simulation (Open Parquet Format + DuckDB SQL Engine)
lh_res = duckdb.sql(f"""
    SELECT {grp_col}, COUNT(*) AS Records, ROUND(SUM({val_col}), 2) AS Total_{val_col}
    FROM 'store.parquet'
    GROUP BY {grp_col}
    ORDER BY Total_{val_col} DESC
""").df()
print("\nData Lakehouse Query Result (DuckDB on Parquet):\n", lh_res)

# 5. Data Quality Check & Incremental Append Pipeline
print("\nData Quality Check -> Duplicates:", df.duplicated().sum(), "| Missing values:", int(df.isnull().sum().sum()))
df.head(2).to_sql("dw_table", dw_conn, if_exists="append", index=False)
print("Total DW Rows After Append:", pd.read_sql("SELECT COUNT(*) AS cnt FROM dw_table", dw_conn)["cnt"][0])
dw_conn.close()
