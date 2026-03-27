import pandas as pd
from sqlalchemy import create_engine, text
import urllib

# CSV path
csv_path = r"C:\\Users\\Sanman\\Downloads\\final_online_retail.csv"

# Read CSV
df = pd.read_csv(csv_path)

# Standardize column names exactly as SQL table expects
df.columns = [
    'invoice',
    'stockcode',
    'description',
    'quantity',
    'invoicedate',
    'price',
    'customer_id',
    'country',
    'revenue',
    'year',
    'month',
    'month_name',
    'weekday',
    'hour'
]

# Convert all values safely
df['invoice'] = df['invoice'].astype(str)
df['stockcode'] = df['stockcode'].astype(str)
df['description'] = df['description'].astype(str)
df['invoicedate'] = df['invoicedate'].astype(str)
df['country'] = df['country'].astype(str)
df['month_name'] = df['month_name'].astype(str)
df['weekday'] = df['weekday'].astype(str)

# SQL Server connection
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=Sanmaankadam\\SQLEXPRESS;"
    "DATABASE=OnlineRetailDB;"
    "Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=True)

# Optional: clear old rows
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE dbo.retail_sales"))

# Insert data
df.to_sql(
    name='retail_sales',
    con=engine,
    schema='dbo',
    if_exists='append',
    index=False,
    method=None,
    chunksize=5000
)

print("Data inserted successfully.")
print("Rows loaded:", len(df))