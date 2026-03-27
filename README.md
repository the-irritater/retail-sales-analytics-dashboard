# Retail Business Insights Dashboard | Revenue, Customer & Product Analysis

## Overview

This project presents an end-to-end data analytics workflow focused on extracting actionable business insights from retail transaction data. The goal is to analyze revenue performance, customer behavior, product trends, and geographical sales distribution using Python, SQL, and Power BI.

The project demonstrates the complete journey from raw data processing to building an interactive business intelligence dashboard.

---

## Problem Statement

Retail businesses generate large volumes of transactional data, but converting this data into meaningful insights for decision-making is often challenging. This project aims to transform raw retail data into structured insights to support business strategy and operational optimization.

---

## Objectives

* Analyze key business metrics such as revenue, orders, and customers
* Identify top-performing products by revenue and quantity
* Evaluate country-wise sales performance
* Understand purchasing patterns by weekday and hour
* Build an interactive dashboard for business insights

---

## Tools & Technologies Used

* Python (Pandas, NumPy)
* SQL (MySQL / SQL Server)
* Power BI
* Excel (Initial exploration)

---

## Dataset

The dataset used in this project is based on online retail transaction data.

* Raw Dataset: Original transaction-level data
* Processed Dataset: Cleaned and feature-engineered dataset used for analysis

Note: A processed dataset is included in this repository to ensure reproducibility.

---

## Project Workflow

### 1. Data Cleaning & Feature Engineering (Python)

* Handled missing values and inconsistencies
* Converted date columns into proper datetime format
* Created derived features:

  * Revenue (Quantity × Price)
  * Year, Month, Month Name
  * Weekday and Hour
* Identified and handled anomalies such as negative quantities and invalid records

---

### 2. Data Loading & SQL Analysis

* Created database and structured tables
* Developed a Python-based data loading pipeline to overcome SQL import limitations
* Handled:

  * Datatype inconsistencies
  * Datetime conversion issues
  * Large dataset insertion challenges
* Performed analytical queries to derive business insights:

  * Total revenue, orders, customers, products
  * Average order value
  * Top products by revenue and quantity
  * Country-wise sales distribution
  * Weekly and hourly trends
  * Customer segmentation (one-time vs repeat)
* Created summary views for reporting

---

## Data Pipeline Automation

A Python script was developed to automate the process of loading cleaned data into SQL.

* Resolved SQL import wizard limitations
* Managed datetime conversion issues
* Ensured consistent data insertion into database tables
* Improved reliability and reproducibility of the data workflow

Script location: `scripts/load_to_sql.py`

---

### 3. Power BI Dashboard Development

An interactive dashboard was built to visualize business insights.

#### Key Features

**KPI Cards**

* Total Revenue
* Total Quantity
* Total Products
* Total Orders
* Total Customers
* Average Order Value

**Visualizations**

* Monthly Revenue Trend
* Top 10 Products by Revenue
* Sales by Weekday
* Top Countries by Revenue
* Hourly Revenue Distribution

**Interactive Filters**

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

* A small number of products contribute significantly to total revenue
* The United Kingdom accounts for the largest share of revenue
* Customer behavior indicates repeat purchasing patterns
* Sales peak during mid-day hours
* Weekday trends show variations in customer activity

---

## Dashboard Preview

!"C:\Users\Sanman\Downloads\Projects\Retail-Sales-Analytics-Dashboard\screenshot\dashboard-overview.png"->


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
├── scripts/
│   └── load_to_sql.py
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

This project demonstrates an end-to-end analytics pipeline, from raw data preprocessing to business insight generation and dashboard visualization. It reflects the ability to solve real-world data challenges and communicate insights effectively.

---

## Future Enhancements

* Customer segmentation using RFM analysis
* Profit and margin analysis
* Predictive modeling for forecasting
* Multi-page dashboard with deeper analysis

---

## Author

Sanman Kadam
MSc Statistics | Data Analyst | Data Science Enthusiast

GitHub: https://github.com/the-irritater


