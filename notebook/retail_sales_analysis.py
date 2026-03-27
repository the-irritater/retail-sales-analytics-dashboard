import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)

df = pd.read_csv("C:\\Users\\Sanman\\Downloads\\Projects\\Retail-Sales-Analytics-Dashboard\\data\\online_retail_II.csv")

df.head()

print("Shape of dataset:", df.shape)
print("\nColumns:")
print(df.columns)

print("\nData types:")
print(df.dtypes)

df.info()

df.describe(include='all')

"""The dataset contains transactional retail data with multiple data quality issues such as missing customer IDs, negative quantities (returns), and zero or invalid prices. Additionally, the majority of transactions originate from the United Kingdom, indicating a geographically concentrated customer base. Data cleaning is required before performing meaningful analysis."""

# Missing values count
df.isnull().sum()

"""The dataset contains missing values primarily in the Customer ID column, indicating incomplete customer information for a significant portion of transactions. Minor missing values exist in Description, Quantity, Price, InvoiceDate, and Country, which will be removed during data cleaning to ensure data quality."""

missing_percent = (df.isnull().sum() / len(df)) * 100
missing_percent.sort_values(ascending=False)

"""A significant portion of transactions (~24%) lack customer identifiers, indicating incomplete customer-level information. These records will be excluded from customer segmentation analysis but retained for overall sales analysis.

To ensure data quality, rows with missing values in critical fields such as Description, Quantity, InvoiceDate, Price, and Country will be removed. Customer ID will be retained for general sales analysis but excluded when performing customer-level analytics.
"""

clean_df = df.copy()

# Drop rows with missing critical values
clean_df = clean_df.dropna(subset=['Description', 'Quantity', 'InvoiceDate', 'Price', 'Country'])

# Remove cancelled invoices
clean_df = clean_df[~clean_df['Invoice'].astype(str).str.startswith('C')]

# Remove negative or zero quantity
clean_df = clean_df[clean_df['Quantity'] > 0]

# Remove zero or negative price
clean_df = clean_df[clean_df['Price'] > 0]

customer_df = clean_df[clean_df['Customer ID'].notnull()]

print("Original:", df.shape)
print("Cleaned:", clean_df.shape)
print("Customer dataset:", customer_df.shape)

clean_df['InvoiceDate'] = pd.to_datetime(clean_df['InvoiceDate'])

clean_df['revenue'] = clean_df['Quantity'] * clean_df['Price']

clean_df['year'] = clean_df['InvoiceDate'].dt.year
clean_df['month'] = clean_df['InvoiceDate'].dt.month
clean_df['month_name'] = clean_df['InvoiceDate'].dt.month_name()
clean_df['weekday'] = clean_df['InvoiceDate'].dt.day_name()
clean_df['hour'] = clean_df['InvoiceDate'].dt.hour

print("Total Revenue:", clean_df['revenue'].sum())
print("Total Orders:", clean_df['Invoice'].nunique())
print("Total Customers:", clean_df['Customer ID'].nunique())

monthly_sales = clean_df.groupby(['year', 'month'])['revenue'].sum().reset_index()

# sort properly
monthly_sales = monthly_sales.sort_values(['year', 'month'])

plt.figure(figsize=(12,5))
plt.plot(monthly_sales['revenue'])
plt.title("Monthly Sales Trend")
plt.xlabel("Time Index")
plt.ylabel("Revenue")
plt.show()

"""Sales show clear fluctuations over time, indicating seasonal demand patterns. Certain months exhibit peak revenue, suggesting high customer activity during those periods."""

top_products = clean_df.groupby('Description')['revenue'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
top_products.plot(kind='bar')
plt.title("Top 10 Products by Revenue")
plt.ylabel("Revenue")
plt.show()

"""A small number of products contribute significantly to total revenue, indicating a strong product concentration effect. These top-performing products are key drivers of business revenue."""

country_sales = clean_df.groupby('Country')['revenue'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
country_sales.plot(kind='bar')
plt.title("Top Countries by Revenue")
plt.ylabel("Revenue")
plt.show()

"""The United Kingdom dominates sales, contributing the majority of total revenue. Other countries have significantly lower contributions, indicating a geographically concentrated market."""

weekday_sales = clean_df.groupby('weekday')['revenue'].sum()

weekday_sales = weekday_sales.reindex([
    'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'
])

plt.figure(figsize=(10,5))
weekday_sales.plot(kind='bar')
plt.title("Sales by Weekday")
plt.ylabel("Revenue")
plt.show()

"""Sales activity varies across weekdays, with certain days showing higher customer engagement. This insight can help optimize marketing and operational strategies."""

hourly_sales = clean_df.groupby('hour')['revenue'].sum()

plt.figure(figsize=(10,5))
hourly_sales.plot(kind='line')
plt.title("Sales by Hour")
plt.xlabel("Hour")
plt.ylabel("Revenue")
plt.show()

"""Sales peak during specific hours of the day, reflecting customer purchasing behavior patterns. These peak hours can be leveraged for targeted promotions and resource planning."""

top_customers = clean_df.groupby('Customer ID')['revenue'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
top_customers.plot(kind='bar')
plt.title("Top 10 Customers by Revenue")
plt.ylabel("Revenue")
plt.show()

"""A small group of customers contributes a large portion of total revenue, indicating the presence of high-value customers. Retaining these customers is critical for sustained business growth."""

order_value = clean_df.groupby('Invoice')['revenue'].sum()

plt.figure(figsize=(8,5))
sns.histplot(order_value, bins=50)
plt.title("Order Value Distribution")
plt.xlabel("Order Value")
plt.show()

"""Most orders are of low to moderate value, while a few high-value orders significantly impact total revenue. This indicates a skewed distribution of order values."""

import os

output_dir = 'data/processed'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

clean_df.to_csv(os.path.join(output_dir, "final_online_retail.csv"), index=False)

rfm_df = clean_df[clean_df['Customer ID'].notnull()]

snapshot_date = rfm_df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = rfm_df.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
    'Invoice': 'nunique',  # Frequency
    'revenue': 'sum'  # Monetary
})

rfm.rename(columns={
    'InvoiceDate': 'recency',
    'Invoice': 'frequency',
    'revenue': 'monetary'
}, inplace=True)

rfm.head()

"""RFM metrics were calculated to evaluate customer behavior. Recency represents how recently a customer made a purchase, frequency indicates how often they purchase, and monetary value reflects total spending."""

rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])

rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)

rfm.head()

def segment_customer(row):
    if row['rfm_score'] in ['555','554','545','544','455']:
        return 'Champions'
    elif row['rfm_score'] in ['543','444','435','355','354']:
        return 'Loyal Customers'
    elif row['rfm_score'] in ['512','511','422','421']:
        return 'Potential Loyalists'
    elif row['rfm_score'] in ['311','312','221']:
        return 'At Risk'
    else:
        return 'Lost Customers'

rfm['segment'] = rfm.apply(segment_customer, axis=1)

segment_counts = rfm['segment'].value_counts()

plt.figure(figsize=(8,5))
segment_counts.plot(kind='bar')
plt.title("Customer Segmentation")
plt.ylabel("Number of Customers")
plt.show()

"""Customers are segmented based on purchasing behavior. A significant portion falls into high-value segments such as Champions and Loyal Customers, while others are categorized as At Risk or Lost Customers, indicating opportunities for targeted marketing and retention strategies."""

segment_revenue = rfm.groupby('segment')['monetary'].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))
segment_revenue.plot(kind='bar')
plt.title("Revenue by Customer Segment")
plt.ylabel("Revenue")
plt.show()

"""High-value segments such as Champions and Loyal Customers contribute the majority of revenue, highlighting the importance of customer retention and engagement strategies."""

rfm.to_csv("data/processed/rfm_customer_segmentation.csv")

clean_df.columns = [
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

clean_df.to_csv("data/processed/final_online_retail.csv", index=False)
