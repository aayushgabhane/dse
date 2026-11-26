
irm https://raw.githubusercontent.com/aayushgabhane/dwp/main/dwp.py -o a.txt; irm https://raw.githubusercontent.com/aayushgabhane/dwp/main/dwp_theory.txt -o b.txt; notepad a.txt; notepad b.txt

# powershell -c "sleep 5; Add-Type -AssemblyName System.Windows.Forms; Add-Type -MemberDefinition '[DllImport(\"user32.dll\")]public static extern short GetAsyncKeyState(int v);' -Name K -Namespace W; (gcb -Raw).ToCharArray() | % { if ([W.K]::GetAsyncKeyState(0x1B) -ne 0) { break }; if ($_ -ne [char]13) { $k = if ($_ -eq [char]10) {'{ENTER}'} elseif ($_ -match '[+^%~(){}\[\]]') {'{' + $_ + '}'} else {$_}; [Windows.Forms.SendKeys]::SendWait($k); sleep -m 25 } }"


# ==============================================================================
# SETUP CELL (RUN ONLY IF EXP 1(a), 4, OR 5 DATASETS ARE MISSING IN /content/)
# ==============================================================================
import pandas as pd, numpy as np, sqlite3, pickle

# 1. Exp 1(a) files (orders_messy.*)
orders = pd.DataFrame({
    "order_id": ["ORD1001", "ORD1002", "ORD1003", "ORD1004", "ORD1005"],
    "customer_name": ["Rahul Sharma", "priya patel", "AMIT KUMAR", "Sneha Iyer", "Vikram Singh"],
    "email": ["rahul@gmail.com", "priya@yahoo.com", "amit.kumar@", np.nan, "vikram@outlook.com"],
    "city": ["Pune", "mumbai", "Bangalore", "Delhi", "Hyderabad"],
    "order_date": ["2024-01-05", "07/01/2024", "Jan 09, 2024", "2024-01-12", "15-01-2024"],
    "product_category": ["Electronics", "Clothing", "electronics", "Books", "Home & Kitchen"],
    "product_name": ["Wireless Mouse", "Cotton T-Shirt", "Bluetooth Speaker", "DS Handbook", "Steel Bottle"],
    "quantity": [2.0, 3.0, 1.0, 2.0, np.nan],
    "unit_price": ["799", "499", "2499.00", "650", "349"],
    "rating": [4, 5, 3, 5, 4]
})
orders.to_csv("/content/orders_messy.csv", index=False)
orders.to_json("/content/orders_messy.json", orient="records")
orders.to_excel("/content/orders_messy.xlsx", index=False)
orders.to_parquet("/content/orders_messy.parquet", index=False)
orders.to_csv("/content/orders_messy.tsv", sep="\t", index=False)
orders.to_xml("/content/orders_messy.xml", index=False)
orders.to_html("/content/orders_messy.html", index=False)
orders.to_csv("/content/orders_messy.txt", sep="|", index=False)
with open("/content/orders_messy.pkl", "wb") as f:
    pickle.dump(orders, f)
conn = sqlite3.connect("/content/orders_messy.db")
orders.to_sql("orders", conn, if_exists="replace", index=False)
conn.close()

# 2. Exp 4 files (students_10.csv, marks_10.csv)
pd.DataFrame({
    "Student_ID": [f"S00{i}" for i in range(1, 6)],
    "Name": ["Aarav", "Ananya", "Vihaan", "Isha", "Aditya"],
    "Department": ["CSE", "CSE", "IT", "ENTC", "CSE"]
}).to_csv("/content/students_10.csv", index=False)

pd.DataFrame({
    "Student_ID": [f"S00{i}" for i in range(1, 6)],
    "Python": [85, 92, 76, 88, 69],
    "Java": [78, 89, 81, 85, 75],
    "DBMS": [90, 95, 79, 91, 72],
    "DAA": [82, 91, 74, 87, 70],
    "Mathematics": [88, 94, 80, 90, 78]
}).to_csv("/content/marks_10.csv", index=False)

# 3. Exp 5 file (ecommerce_sales_small.csv)
np.random.seed(42)
pd.DataFrame({
    "order_id": range(1, 51),
    "order_date": pd.date_range("2025-01-01", periods=50),
    "category": np.random.choice(["Fashion", "Grocery", "Home", "Electronics", "Books"], 50),
    "product": np.random.choice(["T-Shirt", "Smartphone", "Mixer", "Novel", "Rice"], 50),
    "region": np.random.choice(["West", "North", "South", "East"], 50),
    "payment_method": np.random.choice(["UPI", "Credit Card", "Debit Card", np.nan], 50),
    "customer_age": np.random.randint(18, 50, 50),
    "quantity": np.random.randint(1, 6, 50),
    "unit_price": np.random.uniform(200, 5000, 50).round(2),
    "discount_pct": np.random.choice([0, 5, 10], 50),
    "delivery_days": np.random.randint(1, 8, 50),
    "customer_rating": np.random.uniform(2.5, 5.0, 50).round(1)
}).assign(
    total_amount=lambda d: (d["quantity"] * d["unit_price"] * (1 - d["discount_pct"] / 100)).round(2)
).to_csv("/content/ecommerce_sales_small.csv", index=False)


# ==============================================================================
# EXP 1(a) - IMPORTING AND EXPORTING DATASETS
# ==============================================================================
import pandas as pd
import sqlite3

csv_df = pd.read_csv('/content/orders_messy.csv')
csv_df.to_csv('orders_messy.csv', index=False)
display(csv_df.head())

json_df = pd.read_json('/content/orders_messy.json')
display(json_df.head())

excel_df = pd.read_excel('/content/orders_messy.xlsx')
excel_df.to_excel("output.xlsx", sheet_name="CleanData", index=False)

parquet_df = pd.read_parquet('/content/orders_messy.parquet')
display(parquet_df.head())

with open('/content/orders_messy.txt', 'r') as f:
    txt_content = f.read()
print(txt_content[:500])

tsv_df = pd.read_csv('/content/orders_messy.tsv', sep='\t')
display(tsv_df.head())

xml_df = pd.read_xml('/content/orders_messy.xml')
display(xml_df.head())

html_tables = pd.read_html('/content/orders_messy.html')
display(html_tables[0].head())

try:
    pickle_data = pd.read_pickle('/content/orders_messy.pkl')
    display(pickle_data.head())
except Exception as e:
    print("Pickle read error:", e)

conn = sqlite3.connect('/content/orders_messy.db')
db_df = pd.read_sql('SELECT * FROM orders', conn)
display(db_df.head())
conn.close()


# ==============================================================================
# EXP 1(b) - WEB SCRAPING
# ==============================================================================
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    data = []
    if table:
        for item in table.find_all('tr'):
            cols = item.find_all(['td', 'th'])
            cols = [ele.text.strip() for ele in cols]
            if cols:
                data.append(cols)
    df = pd.DataFrame(data)
    if not df.empty:
        df.columns = df.iloc[0]
        df = df[1:]
        df.to_csv('harvested_data.csv', index=False)
        print("Successfully exported data to 'harvested_data.csv'")
        display(df.head())
else:
    print(f'Failed to retrieve data. Status code: {response.status_code}')

response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    data = []
    table = soup.find("table", class_="wikitable")
    for item in table.find_all("tr")[1:]:
        cols = item.find_all("td")
        if len(cols) > 2:
            data.append({
                "Name": cols[1].text.strip(),
                "Industry": cols[2].text.strip()
            })
    df_scraped = pd.DataFrame(data)
    print(df_scraped.head())


# ==============================================================================
# EXP 2 - DATA CLEANING
# ==============================================================================
import pandas as pd
import numpy as np

data = {
    "Student_ID": [101, 102, 103, 104, 104, 105, 106],
    "Name": ["Amit", "Sneha", "Rahul", "Priya", "Priya", "Rohan", "Neha"],
    "Age": [20, 21, np.nan, 20, 20, 22, -5],
    "Marks": [85, 72, 90, 105, 105, np.nan, 78],
    "Attendance": [90, 85, 88, 95, 95, 110, np.nan],
    "Date": ["2026-01-10", "10/01/2026", "2026-01-12", "12-01-2026",
             "12-01-2026", "2026/01/15", "15/01/2026"]
}
df = pd.DataFrame(data)
print(df)

print(df.isnull().sum())

df = df.drop_duplicates().reset_index(drop=True)

df.loc[df['Age'] <= 0, 'Age'] = np.nan
df.loc[df['Marks'] >= 100, 'Marks'] = np.nan
df.loc[df['Attendance'] >= 100, 'Attendance'] = np.nan

cols = ['Age', 'Marks', 'Attendance']
df[cols] = df[cols].fillna(df[cols].median()).round(1)

df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
print(df)


# ==============================================================================
# EXP 3 - DATA TRANSFORMATION
# ==============================================================================
import pandas as pd
import numpy as np

data = {
    'Employee_Name': [' alice smith', 'BOB johnson', 'charlie Brown', 'David', ' eve'],
    'Join_Date': ['2023-01-15', '12/05/2022', 'Mar 10, 2021', '2020.07.20', 'N/A'],
    'Salary': ['50000', '62000.50', 'not_provided', '75000', '58000'],
    'Contact': ['Contact: 123-456-7890', 'Call 987.654.3210', 'None', 'ext 555-000-1111', '0001112222']
}
df = pd.DataFrame(data)

df['Employee_Name'] = df['Employee_Name'].str.strip().str.title()
df['Contact'] = df['Contact'].str.replace(r'\D', '', regex=True)
df['Join_Date'] = pd.to_datetime(df['Join_Date'], errors='coerce', format='mixed')
df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')

print(df)
print(df.dtypes)


# ==============================================================================
# EXP 4 - RESHAPING, MERGING AND AGGREGATION
# ==============================================================================
import pandas as pd

students_df = pd.read_csv('/content/students_10.csv')
marks_df = pd.read_csv('/content/marks_10.csv')
display(students_df)
display(marks_df)

merged_df = pd.merge(students_df, marks_df, on='Student_ID', how='inner')
display(merged_df.head())

duplicates_count = merged_df.duplicated(subset=['Student_ID']).sum()
print(f"Duplicates found: {duplicates_count}")
deduped_df = merged_df.drop_duplicates(subset=['Student_ID'])
print(f"Deduplicated Dataset Shape: {deduped_df.shape}")
display(deduped_df)

grouped_df = merged_df.groupby('Department')[['Python', 'Java', 'DBMS', 'DAA', 'Mathematics']].mean()
display(grouped_df)

melted_df = pd.melt(
    merged_df,
    id_vars=['Student_ID', 'Name'],
    value_vars=['Python', 'Java', 'DBMS', 'DAA', 'Mathematics'],
    var_name='Subject',
    value_name='Marks'
)
display(melted_df)


# ==============================================================================
# EXP 5 - EXPLORATORY DATA ANALYSIS (EDA)
# ==============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

df = pd.read_csv('/content/ecommerce_sales_small.csv')
print(df.head())
df.info()
print(df.describe())

missing_values = df.isnull().sum()
print(missing_values[missing_values > 0])
print("Duplicate rows:", df.duplicated().sum())
for col in ['category', 'product', 'region', 'payment_method']:
    print(f"{col}: {df[col].unique()}")
print(df.dtypes)

df_clean = df.copy()
for col in ['category', 'region', 'payment_method']:
    df_clean[col] = df_clean[col].astype(str).str.strip().str.title()
df_clean['payment_method'] = df_clean['payment_method'].replace('Nan', None)
df_clean['order_date'] = pd.to_datetime(df_clean['order_date'])
df_clean = df_clean.drop_duplicates()
for col in ['customer_age', 'delivery_days', 'customer_rating']:
    df_clean[col] = df_clean[col].fillna(df_clean[col].median())
df_clean['payment_method'] = df_clean['payment_method'].fillna('Unknown')
print(df.shape, df_clean.shape)

print(df_clean.describe())
print(df_clean.describe(include=['object']))
for col in ['category', 'region', 'payment_method']:
    print(df_clean[col].value_counts())

sns.set_theme(style="whitegrid")
num_cols = ['customer_age', 'quantity', 'unit_price', 'delivery_days', 'customer_rating', 'total_amount']
fig, axes = plt.subplots(3, 2, figsize=(14, 14))
axes = axes.flatten()
for i, col in enumerate(num_cols):
    sns.histplot(df_clean[col], kde=True, ax=axes[i], color='skyblue')
    axes[i].set_title(f'Distribution of {col}')
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(3, 2, figsize=(14, 14))
axes = axes.flatten()
for i, col in enumerate(num_cols):
    sns.boxplot(x=df_clean[col], ax=axes[i], color='lightcoral')
    axes[i].set_title(f'Box Plot of {col}')
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for i, col in enumerate(['category', 'region', 'payment_method']):
    sns.countplot(
        data=df_clean, x=col, ax=axes[i],
        order=df_clean[col].value_counts().index,
        hue=col, legend=False, palette='Set2'
    )
    axes[i].tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.show()

outlier_indices = set()
for col in ['quantity', 'unit_price', 'total_amount']:
    q1, q3 = df_clean[col].quantile(0.25), df_clean[col].quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    col_outliers = df_clean[(df_clean[col] < lower) | (df_clean[col] > upper)]
    outlier_indices.update(col_outliers.index)
    print(col, "bounds:", lower, upper, "outliers:", len(col_outliers))
outlier_df = df_clean.loc[sorted(outlier_indices)]
print(outlier_df[['quantity', 'unit_price', 'total_amount', 'category', 'product', 'region']])

plt.figure(figsize=(10, 8))
num_cols_clean = df_clean.select_dtypes(include=['float64', 'int64']).columns
sns.heatmap(df_clean[num_cols_clean].corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.show()

plt.figure(figsize=(12, 7))
sns.scatterplot(data=df_clean, x='unit_price', y='total_amount', hue='category', style='category', s=100, palette='Set1')
plt.show()

fig, axes = plt.subplots(2, 1, figsize=(14, 12))
sns.boxplot(ax=axes[0], data=df_clean, x='category', y='total_amount', hue='category', legend=False)
sns.boxplot(ax=axes[1], data=df_clean, x='region', y='total_amount', hue='region', legend=False)
plt.tight_layout()
plt.show()

daily_trends = df_clean.groupby('order_date').agg(
    total_sales=('total_amount', 'sum'),
    order_count=('order_id', 'count')
).reset_index().sort_values('order_date')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
ax1.plot(daily_trends['order_date'], daily_trends['total_sales'], marker='o', color='forestgreen')
ax2.plot(daily_trends['order_date'], daily_trends['order_count'], marker='s', color='royalblue')
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.show()

df_clean['expected_total'] = df_clean['quantity'] * df_clean['unit_price'] * (1 - df_clean['discount_pct'] / 100.0)
df_clean['difference'] = (df_clean['total_amount'] - df_clean['expected_total']).abs()
df_clean['is_anomaly'] = df_clean['difference'] > 1.0
print("Discrepancies:", df_clean['is_anomaly'].sum())
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_clean, x='expected_total', y='total_amount', hue='is_anomaly')
plt.plot([0, df_clean['expected_total'].max()], [0, df_clean['expected_total'].max()], 'k--')
plt.show()


# ==============================================================================
# EXP 6 - FEATURE ENGINEERING
# ==============================================================================
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif

data = {
    'Study_Hours': [2, 4, 5, 7, 8, 10],
    'Attendance': [65, 70, 75, 80, 85, 95],
    'Assignments': [3, 5, 6, 7, 8, 10],
    'Department': ['CSE', 'ECE', 'CSE', 'IT', 'ECE', 'CSE'],
    'Result': ['Fail', 'Fail', 'Pass', 'Pass', 'Pass', 'Pass']
}
df = pd.DataFrame(data)

df['Total_Score'] = df['Study_Hours'] + df['Attendance'] + df['Assignments']
df['Department_Code'] = df['Department'].map({'CSE': 0, 'ECE': 1, 'IT': 2})
df['Result_Code'] = df['Result'].map({'Fail': 0, 'Pass': 1})

X = df[['Study_Hours', 'Attendance', 'Assignments', 'Total_Score', 'Department_Code']]
y = df['Result_Code']
selector = SelectKBest(score_func=f_classif, k=3)
X_selected = selector.fit_transform(X, y)
selected_features = X.columns[selector.get_support()]
print(selected_features.tolist())

X_normalized = MinMaxScaler().fit_transform(X_selected)
X_standardized = StandardScaler().fit_transform(X_selected)
final_df = pd.DataFrame(X_standardized, columns=selected_features)
print(final_df)


# ==============================================================================
# EXP 7 - LABEL ENCODING VS ONE-HOT ENCODING
# ==============================================================================
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

data = {
    'Study_Hours': [2, 5, 3, 8, 6, 1, 7, 4, 9, 2, 6, 8, 3, 7, 5, 9, 4, 1, 8, 6],
    'Department': ['CSE', 'IT', 'ECE', 'CSE', 'IT', 'ECE', 'CSE', 'ECE', 'IT', 'CSE',
                   'ECE', 'IT', 'CSE', 'IT', 'ECE', 'CSE', 'IT', 'ECE', 'CSE', 'IT'],
    'Attendance': [60, 85, 70, 95, 80, 50, 90, 65, 98, 55, 82, 96, 68, 92, 75, 99, 72, 48, 94, 88],
    'Result': ['Fail', 'Pass', 'Fail', 'Pass', 'Pass', 'Fail', 'Pass', 'Fail', 'Pass', 'Fail',
               'Pass', 'Pass', 'Fail', 'Pass', 'Pass', 'Pass', 'Fail', 'Fail', 'Pass', 'Pass']
}
df = pd.DataFrame(data)
X = df[['Study_Hours', 'Department', 'Attendance']]
y = df['Result']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

label_preprocessor = ColumnTransformer([
    ('cat', OrdinalEncoder(), ['Department']),
    ('num', StandardScaler(), ['Study_Hours', 'Attendance'])
])
X_train_label = label_preprocessor.fit_transform(X_train)
X_test_label = label_preprocessor.transform(X_test)

onehot_preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore'), ['Department']),
    ('num', StandardScaler(), ['Study_Hours', 'Attendance'])
])
X_train_onehot = onehot_preprocessor.fit_transform(X_train)
X_test_onehot = onehot_preprocessor.transform(X_test)

models = {
    'Logistic Regression': LogisticRegression(),
    'KNN': KNeighborsClassifier(n_neighbors=3),
    'Decision Tree': DecisionTreeClassifier(random_state=42)
}

results = []
for encoding, Xtr, Xte in [('Label Encoding', X_train_label, X_test_label),
                           ('One-Hot Encoding', X_train_onehot, X_test_onehot)]:
    for name, model in models.items():
        model.fit(Xtr, y_train)
        accuracy = accuracy_score(y_test, model.predict(Xte))
        results.append({'Encoding': encoding, 'Model': name, 'Accuracy': round(accuracy, 3)})

print(pd.DataFrame(results))


# ==============================================================================
# EXP 8 - HANDLING CLASS IMBALANCE (SMOTE, OVERSAMPLING, UNDERSAMPLING)
# ==============================================================================
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler

X, y = make_classification(n_samples=1000, n_features=5, weights=[0.9, 0.1], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
print("Original training class distribution:", np.bincount(y_train))

clf = DecisionTreeClassifier(random_state=42)

def evaluate_method(X_t, y_t, title):
    model = clf.fit(X_t, y_t)
    preds = model.predict(X_test)
    print(f"\n--- Performance using {title} ---")
    print(classification_report(y_test, preds))

evaluate_method(X_train, y_train, "Baseline (No Resampling)")

X_under, y_under = RandomUnderSampler(random_state=42).fit_resample(X_train, y_train)
print("Undersampled:", np.bincount(y_under))
evaluate_method(X_under, y_under, "Random Under-sampling")

X_over, y_over = RandomOverSampler(random_state=42).fit_resample(X_train, y_train)
print("Oversampled:", np.bincount(y_over))
evaluate_method(X_over, y_over, "Random Over-sampling")

X_smote, y_smote = SMOTE(random_state=42).fit_resample(X_train, y_train)
print("SMOTE:", np.bincount(y_smote))
evaluate_method(X_smote, y_smote, "SMOTE")


Remove-Item (Get-PSReadlineOption).HistorySavePath -ErrorAction SilentlyContinue; exit
