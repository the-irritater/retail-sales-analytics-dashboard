# Retail Business Insights Dashboard | Revenue, Customer & Product Analysis

## Overview

This project focuses on analyzing retail transaction data to generate meaningful business insights. The objective is to understand revenue patterns, customer behavior, product performance, and geographical sales distribution using an end-to-end data analytics approach.

The project involves data cleaning, feature engineering, SQL-based analysis, and interactive dashboard development using Power BI.

---

## Problem Statement

Retail businesses generate large volumes of transactional data, but extracting actionable insights from this data can be challenging. This project aims to transform raw retail data into structured insights to support data-driven decision-making.

---

## Objectives

* Analyze total revenue, orders, and customer base
* Identify top-performing products by revenue and quantity
* Evaluate country-wise sales performance
* Understand sales patterns by weekday and hour
* Build an interactive dashboard for business insights

---

## Tools & Technologies Used

* Python (Pandas, NumPy)
* SQL (MySQL / SQL Server)
* Power BI
* Excel (for initial data exploration)

---

## Project Workflow

### 1. Data Cleaning & Preprocessing (Python)

* Handled missing values and inconsistencies
* Converted date columns into proper datetime format
* Created new features such as:

  * Revenue (Quantity × Price)
  * Year, Month, Month Name
  * Weekday and Hour
* Identified and handled anomalies such as negative quantities and invalid records

---

### 2. SQL Data Analysis

* Created database and structured tables
* Performed analytical queries to derive key metrics:

  * Total revenue, orders, customers, and products
  * Average order value
  * Top products by revenue and quantity
  * Country-wise sales distribution
  * Weekly and hourly sales trends
  * Customer segmentation (one-time vs repeat customers)
* Built summary views for reporting

---

### 3. Power BI Dashboard Development

Developed an interactive dashboard to visualize business insights.

#### Key Dashboard Features:

* KPI Cards:

  * Total Revenue
  * Total Quantity
  * Total Products
  * Total Orders
  * Total Customers
  * Average Order Value

* Visualizations:

  * Monthly Revenue Trend
  * Top 10 Products by Revenue
  * Sales by Weekday
  * Top Countries by Revenue
  * Hourly Revenue Distribution

* Interactive Filters:

  * Country
  * Year
  * Month

---

## Key Performance Indicators (KPIs)

* Total Revenue: 3.22M
* Total Orders: 6,394
* Total Customers: 2,315
* Total Products: 3,601
* Total Quantity: 1.92M
* Average Order Value: 503.25

---

## Key Insights

* A significant portion of revenue is generated from a small number of top-performing products
* The United Kingdom contributes the majority of total revenue
* Customer behavior indicates repeat purchasing patterns
* Sales peak during mid-day hours, indicating high transaction activity during this period
* Weekday trends highlight variations in customer purchasing behavior across the week

---

## Dashboard Preview

!<img width="1314" height="738" alt="dashboard_overview" src="https://github.com/user-attachments/assets/a10c3cfa-6956-4de7-bc01-c87a1ac6c51b" />


---

## Project Structure

```
Retail-Sales-Analytics-Dashboard/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── retail_sales_analysis.ipynb
│
├── sql/
│   └── retail_sales_analysis.sql
│
├── powerbi/
│   └── Retail_Business_Insights_Dashboard.pbix
│
├── screenshots/
│   └── dashboard_overview.png
│
└── README.md
```

---

## Conclusion

This project demonstrates an end-to-end data analytics workflow, starting from raw data processing to delivering actionable business insights through an interactive dashboard. It highlights the ability to work with real-world data, perform structured analysis, and communicate insights effectively.

---

## Future Enhancements

* Customer segmentation using RFM analysis
* Profit and margin analysis
* Predictive modeling for sales forecasting
* Multi-page dashboard with deeper drill-down analysis

---

## Author

Sanman Kadam
MSc Statistics | Data Analyst | Data Science Enthusiast

GitHub: https://github.com/the-irritater
