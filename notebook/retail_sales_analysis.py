# =============================================================================
# RETAIL SALES ANALYTICS DASHBOARD
# =============================================================================
# Project  : Retail Sales Analytics & Customer Segmentation
# Dataset  : Online Retail II (UCI Machine Learning Repository)
# Author   : Sanman
# Date     : March 2026
# =============================================================================

# -----------------------------------------------------------------------------
# PROBLEM STATEMENT
# -----------------------------------------------------------------------------
"""
Retail businesses generate vast amounts of transactional data every day.
However, without structured analysis, this data remains an untapped resource.
This project addresses the challenge of transforming raw e-commerce transaction
records into actionable business intelligence.

The dataset used is the "Online Retail II" dataset, which contains sales
transactions from a UK-based online retailer between 2009 and 2011. The data
includes invoice records, product descriptions, quantities sold, prices,
customer IDs, and country information.

Key challenges include:
  - Significant missing customer data (~24% of transactions)
  - Presence of cancellations, returns, and invalid entries
  - No pre-existing customer segmentation or KPI metrics
  - Need to uncover temporal, geographic, and behavioral sales patterns

This analysis aims to clean and transform the raw data, derive meaningful
KPIs, and apply RFM (Recency, Frequency, Monetary) segmentation to classify
customers into actionable groups that can drive targeted marketing and
retention strategies.
"""

# -----------------------------------------------------------------------------
# OBJECTIVES
# -----------------------------------------------------------------------------
"""
1. DATA QUALITY & CLEANING
   - Identify and handle missing values, duplicate records, and outliers.
   - Remove cancelled transactions, zero-price records, and negative quantities.
   - Prepare a clean, analysis-ready dataset.

2. EXPLORATORY DATA ANALYSIS (EDA)
   - Analyze monthly revenue trends to identify seasonal patterns.
   - Discover top-performing products and their revenue contribution.
   - Examine geographic distribution of sales across countries.
   - Study customer purchasing behavior by weekday and hour.

3. CUSTOMER ANALYTICS
   - Identify high-value customers based on total revenue contribution.
   - Analyze the distribution of order values to understand purchasing patterns.

4. RFM CUSTOMER SEGMENTATION
   - Compute RFM (Recency, Frequency, Monetary) scores for each customer.
   - Segment customers into meaningful groups: Champions, Loyal Customers,
     Potential Loyalists, At Risk, and Lost Customers.
   - Analyze revenue contribution by customer segment.

5. ACTIONABLE INSIGHTS
   - Derive business recommendations from each analytical phase.
   - Export clean and segmented datasets for further use in dashboards or models.
"""

# =============================================================================
# SECTION 1 - IMPORTS & SETUP
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)

<<<<<<< HEAD
df = pd.read_csv("data\\raw\\online_retail_II.csv")
=======
# =============================================================================
# SECTION 2 - DATA LOADING
# =============================================================================

df = pd.read_csv(
    "C:\\Users\\Sanman\\Downloads\\Projects\\retail-sales-analytics-dashboard\\data\\raw\\online_retail_II.csv"
)
>>>>>>> aeecaef (Updated.)

df.head()

print("Shape of dataset:", df.shape)
print("\nColumns:")
print(df.columns)

print("\nData types:")
print(df.dtypes)

df.info()

df.describe(include='all')

"""
Observation:
The dataset contains transactional retail data with multiple data quality
issues such as missing customer IDs, negative quantities (returns), and zero
or invalid prices. Additionally, the majority of transactions originate from
the United Kingdom, indicating a geographically concentrated customer base.
Data cleaning is required before performing meaningful analysis.
"""

# =============================================================================
# SECTION 3 - MISSING VALUE ANALYSIS
# =============================================================================

# Missing values count
df.isnull().sum()

"""
Observation:
The dataset contains missing values primarily in the Customer ID column,
indicating incomplete customer information for a significant portion of
transactions. Minor missing values exist in Description, Quantity, Price,
InvoiceDate, and Country, which will be removed during data cleaning to
ensure data quality.
"""

missing_percent = (df.isnull().sum() / len(df)) * 100
missing_percent.sort_values(ascending=False)

"""
Observation:
A significant portion of transactions (~24%) lack customer identifiers,
indicating incomplete customer-level information. These records will be
excluded from customer segmentation analysis but retained for overall
sales analysis.

To ensure data quality, rows with missing values in critical fields such as
Description, Quantity, InvoiceDate, Price, and Country will be removed.
Customer ID will be retained for general sales analysis but excluded when
performing customer-level analytics.
"""

# =============================================================================
# SECTION 4 - DATA CLEANING
# =============================================================================

clean_df = df.copy()

# Drop rows with missing critical values
clean_df = clean_df.dropna(subset=['Description', 'Quantity', 'InvoiceDate', 'Price', 'Country'])

# Remove cancelled invoices (starting with 'C')
clean_df = clean_df[~clean_df['Invoice'].astype(str).str.startswith('C')]

# Remove negative or zero quantity (returns / data errors)
clean_df = clean_df[clean_df['Quantity'] > 0]

# Remove zero or negative price
clean_df = clean_df[clean_df['Price'] > 0]

# Separate dataset with valid Customer IDs for customer-level analysis
customer_df = clean_df[clean_df['Customer ID'].notnull()]

print("Original dataset shape :", df.shape)
print("Cleaned dataset shape  :", clean_df.shape)
print("Customer dataset shape :", customer_df.shape)

# =============================================================================
# SECTION 5 - FEATURE ENGINEERING
# =============================================================================

clean_df['InvoiceDate'] = pd.to_datetime(clean_df['InvoiceDate'])

# Derived revenue column
clean_df['revenue'] = clean_df['Quantity'] * clean_df['Price']

# Temporal features
clean_df['year']       = clean_df['InvoiceDate'].dt.year
clean_df['month']      = clean_df['InvoiceDate'].dt.month
clean_df['month_name'] = clean_df['InvoiceDate'].dt.month_name()
clean_df['weekday']    = clean_df['InvoiceDate'].dt.day_name()
clean_df['hour']       = clean_df['InvoiceDate'].dt.hour

# Key performance indicators (KPIs)
print("-" * 40)
print(f"  Total Revenue  : GBP {clean_df['revenue'].sum():,.2f}")
print(f"  Total Orders   : {clean_df['Invoice'].nunique():,}")
print(f"  Total Customers: {clean_df['Customer ID'].nunique():,}")
print("-" * 40)

# =============================================================================
# SECTION 6 - EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================================

# -- 6.1 Monthly Sales Trend --------------------------------------------------

monthly_sales = clean_df.groupby(['year', 'month'])['revenue'].sum().reset_index()
monthly_sales = monthly_sales.sort_values(['year', 'month'])

plt.figure(figsize=(12, 5))
plt.plot(monthly_sales['revenue'], marker='o', linewidth=2, color='steelblue')
plt.title("Monthly Sales Trend", fontsize=14, fontweight='bold')
plt.xlabel("Time Index (Month)")
plt.ylabel("Revenue (GBP)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

"""
Observation:
Sales show clear fluctuations over time, indicating seasonal demand patterns.
Certain months exhibit peak revenue, suggesting high customer activity during
those periods. Revenue peaks in Q4 likely align with the holiday shopping season.
"""

# -- 6.2 Top 10 Products by Revenue -------------------------------------------

top_products = (
    clean_df.groupby('Description')['revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))
top_products.plot(kind='bar', color='coral', edgecolor='black')
plt.title("Top 10 Products by Revenue", fontsize=14, fontweight='bold')
plt.ylabel("Revenue (GBP)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

"""
Observation:
A small number of products contribute significantly to total revenue,
indicating a strong product concentration effect (Pareto Principle).
These top-performing products are key drivers of business revenue and
should be prioritized in inventory and marketing decisions.
"""

# -- 6.3 Top Countries by Revenue ---------------------------------------------

country_sales = (
    clean_df.groupby('Country')['revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))
country_sales.plot(kind='bar', color='mediumseagreen', edgecolor='black')
plt.title("Top 10 Countries by Revenue", fontsize=14, fontweight='bold')
plt.ylabel("Revenue (GBP)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

"""
Observation:
The United Kingdom dominates sales, contributing the vast majority of total
revenue. Other countries such as Germany, France, and EIRE have significantly
lower contributions, indicating a geographically concentrated market. This
presents an opportunity for targeted international expansion.
"""

# -- 6.4 Sales by Weekday -----------------------------------------------------

weekday_sales = clean_df.groupby('weekday')['revenue'].sum()
weekday_sales = weekday_sales.reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
])

plt.figure(figsize=(10, 5))
weekday_sales.plot(kind='bar', color='mediumpurple', edgecolor='black')
plt.title("Sales by Weekday", fontsize=14, fontweight='bold')
plt.ylabel("Revenue (GBP)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""
Observation:
Sales activity varies significantly across weekdays, with mid-week days
(Tuesday to Thursday) typically showing higher customer engagement. Sunday
records notably lower activity. These patterns can inform scheduling of
promotions and staffing decisions.
"""

# -- 6.5 Sales by Hour --------------------------------------------------------

hourly_sales = clean_df.groupby('hour')['revenue'].sum()

plt.figure(figsize=(10, 5))
hourly_sales.plot(kind='line', marker='o', color='darkorange', linewidth=2)
plt.title("Sales by Hour of Day", fontsize=14, fontweight='bold')
plt.xlabel("Hour (24h)")
plt.ylabel("Revenue (GBP)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

"""
Observation:
Sales peak during mid-morning hours (approximately 10:00 to 12:00), reflecting
a concentrated window of peak customer purchasing behavior. These peak hours
can be leveraged for targeted flash promotions, push notifications, and
operational resource planning.
"""

# -- 6.6 Top 10 Customers by Revenue ------------------------------------------

top_customers = (
    clean_df.groupby('Customer ID')['revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
top_customers.plot(kind='bar', color='dodgerblue', edgecolor='black')
plt.title("Top 10 Customers by Revenue", fontsize=14, fontweight='bold')
plt.ylabel("Revenue (GBP)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""
Observation:
A small group of customers contributes a disproportionately large share of
total revenue, confirming the Pareto Principle in customer value distribution.
Retaining these high-value customers through loyalty programs and personalized
engagement is critical for sustained business growth.
"""

# -- 6.7 Order Value Distribution ---------------------------------------------

order_value = clean_df.groupby('Invoice')['revenue'].sum()

plt.figure(figsize=(10, 5))
sns.histplot(order_value, bins=50, color='teal', kde=True)
plt.title("Order Value Distribution", fontsize=14, fontweight='bold')
plt.xlabel("Order Value (GBP)")
plt.ylabel("Count")
plt.xlim(0, order_value.quantile(0.99))   # clip extreme outliers for clarity
plt.tight_layout()
plt.show()

"""
Observation:
The distribution of order values is heavily right-skewed: most orders are of
low to moderate value, while a small number of very high-value orders
significantly impact total revenue. This skewness suggests the presence of
bulk/wholesale buyers alongside regular retail customers.
"""

# =============================================================================
# SECTION 7 - SAVE CLEANED DATA
# =============================================================================

output_dir = 'data/processed'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

clean_df.to_csv(os.path.join(output_dir, "final_online_retail.csv"), index=False)
print(f"Cleaned dataset saved to: {output_dir}/final_online_retail.csv")

# =============================================================================
# SECTION 8 - RFM CUSTOMER SEGMENTATION
# =============================================================================

# -- 8.1 Compute RFM Metrics --------------------------------------------------

rfm_df = clean_df[clean_df['Customer ID'].notnull()]

snapshot_date = rfm_df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = rfm_df.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
    'Invoice'    : 'nunique',                                  # Frequency
    'revenue'    : 'sum'                                       # Monetary
})

rfm.rename(columns={
    'InvoiceDate': 'recency',
    'Invoice'    : 'frequency',
    'revenue'    : 'monetary'
}, inplace=True)

rfm.head()

"""
Observation:
RFM metrics were calculated for each customer:
  - Recency   : Days since the customer's last purchase (lower = better).
  - Frequency : Total number of unique invoices (higher = more engaged).
  - Monetary  : Total revenue generated by the customer (higher = more valuable).
"""

# -- 8.2 Score Customers on RFM Dimensions ------------------------------------

rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm['rfm_score'] = (
    rfm['r_score'].astype(str)
    + rfm['f_score'].astype(str)
    + rfm['m_score'].astype(str)
)

rfm.head()

# -- 8.3 Segment Customers ----------------------------------------------------

def segment_customer(row):
    if row['rfm_score'] in ['555', '554', '545', '544', '455']:
        return 'Champions'
    elif row['rfm_score'] in ['543', '444', '435', '355', '354']:
        return 'Loyal Customers'
    elif row['rfm_score'] in ['512', '511', '422', '421']:
        return 'Potential Loyalists'
    elif row['rfm_score'] in ['311', '312', '221']:
        return 'At Risk'
    else:
        return 'Lost Customers'

rfm['segment'] = rfm.apply(segment_customer, axis=1)

# -- 8.4 Customer Segment Distribution ----------------------------------------

segment_counts = rfm['segment'].value_counts()

plt.figure(figsize=(9, 5))
segment_counts.plot(kind='bar', color='slateblue', edgecolor='black')
plt.title("Customer Segmentation - Count per Segment", fontsize=14, fontweight='bold')
plt.ylabel("Number of Customers")
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()

"""
Observation:
Customers are segmented based on their purchasing behavior. A significant
portion falls into high-value segments such as Champions and Loyal Customers,
reflecting a solid core of engaged buyers. Others are categorized as At Risk
or Lost Customers, indicating clear opportunities for targeted re-engagement
and retention strategies.
"""

# -- 8.5 Revenue by Customer Segment ------------------------------------------

segment_revenue = rfm.groupby('segment')['monetary'].sum().sort_values(ascending=False)

plt.figure(figsize=(9, 5))
segment_revenue.plot(kind='bar', color='tomato', edgecolor='black')
plt.title("Revenue by Customer Segment", fontsize=14, fontweight='bold')
plt.ylabel("Total Revenue (GBP)")
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()

"""
Observation:
High-value segments such as Champions and Loyal Customers contribute the
overwhelming majority of total revenue. This underscores the critical
importance of customer retention strategies, loyalty programs, and
personalized engagement campaigns to protect revenue.
"""

# -- 8.6 Export RFM Segmentation Results --------------------------------------

rfm.to_csv(os.path.join(output_dir, "rfm_customer_segmentation.csv"))
print(f"RFM segmentation saved to: {output_dir}/rfm_customer_segmentation.csv")

# =============================================================================
# SECTION 9 - FINALIZE & EXPORT CLEANED DATASET
# =============================================================================

clean_df.columns = [
    'invoice', 'stockcode', 'description', 'quantity',
    'invoicedate', 'price', 'customer_id', 'country',
    'revenue', 'year', 'month', 'month_name', 'weekday', 'hour'
]

clean_df.to_csv(os.path.join(output_dir, "final_online_retail.csv"), index=False)
print(f"Final cleaned dataset saved to: {output_dir}/final_online_retail.csv")

# =============================================================================
# SECTION 10 - OVERALL CONCLUSION
# =============================================================================
"""
OVERALL CONCLUSION
==================

This project performed a comprehensive end-to-end retail sales analytics
pipeline on the Online Retail II dataset, covering data quality assessment,
exploratory analysis, and customer segmentation.

DATA QUALITY
------------
The raw dataset had significant quality issues, including approximately 24%
missing customer IDs, cancelled transactions, negative quantities, and zero-
price records. After rigorous cleaning, the dataset was reduced to a reliable,
analysis-ready form while preserving the vast majority of valid transactions.

SALES TRENDS
------------
Monthly revenue analysis revealed clear seasonal demand patterns, with peaks
occurring towards the end of the year (Q4), consistent with the holiday
shopping season. These patterns provide a strong signal for planning inventory,
marketing budgets, and staffing well in advance.

PRODUCT & GEOGRAPHY
-------------------
A small set of products drives the majority of revenue (Pareto Effect),
meaning that inventory and promotional decisions should prioritize these
high-impact SKUs. Geographically, the United Kingdom is the dominant market,
while countries like Germany and France present growth opportunities for
targeted international expansion strategies.

TEMPORAL BEHAVIOR
-----------------
Customers are most active mid-week (Tuesday to Thursday) and during mid-morning
hours (10:00 to 12:00). These insights can be used to time promotions, flash
sales, email campaigns, and operational resource allocation for maximum impact.

CUSTOMER SEGMENTATION (RFM)
----------------------------
RFM segmentation revealed that a core group of Champions and Loyal Customers
generates the majority of business revenue. This confirms the Pareto Principle
at the customer level. Specific recommendations:

  - Champions & Loyal Customers:
    Reward with loyalty programs and early access to new products to sustain
    long-term engagement.

  - Potential Loyalists:
    Nurture with targeted offers, discounts, and personalized communication
    to convert them into loyal customers.

  - At Risk Customers:
    Re-engage via win-back campaigns and feedback surveys to understand
    churn drivers and reduce attrition.

  - Lost Customers:
    Analyze exit patterns and apply win-back strategies or reallocate
    acquisition budget toward higher-potential segments.

STRATEGIC TAKEAWAYS
-------------------
1. Prioritize retention spend on the top customer tier, as they generate
   outsized revenue relative to their count.
2. Invest in seasonal campaigns aligned with Q4 revenue spikes.
3. Schedule promotions for mid-week, mid-morning timeframes to maximize
   customer reach and conversion.
4. Expand strategically into European markets beyond the United Kingdom.
5. Consolidate and promote top-revenue products to maximize inventory
   efficiency and reduce carrying costs.

In summary, this analysis transforms raw transactional data into strategic
business intelligence, enabling data-driven decisions across marketing,
operations, customer retention, and international growth planning.
"""

# =============================================================================
# END OF NOTEBOOK
# =============================================================================
