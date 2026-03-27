/* =========================================================
   ONLINE RETAIL SALES ANALYSIS PROJECT
   Database: OnlineRetailDB
   Table: dbo.retail_sales
   ========================================================= */

------------------------------------------------------------
-- 1. CREATE DATABASE
------------------------------------------------------------
CREATE DATABASE OnlineRetailDB;
GO

USE OnlineRetailDB;
GO

------------------------------------------------------------
-- 2. DROP EXISTING TABLE IF EXISTS
------------------------------------------------------------
DROP TABLE IF EXISTS dbo.retail_sales;
GO

------------------------------------------------------------
-- 3. CREATE MAIN TABLE
------------------------------------------------------------
CREATE TABLE dbo.retail_sales (
    invoice NVARCHAR(50) NULL,
    stockcode NVARCHAR(50) NULL,
    description NVARCHAR(500) NULL,
    quantity INT NULL,
    invoicedate NVARCHAR(50) NULL,
    price FLOAT NULL,
    customer_id FLOAT NULL,
    country NVARCHAR(100) NULL,
    revenue FLOAT NULL,
    year SMALLINT NULL,
    month TINYINT NULL,
    month_name NVARCHAR(50) NULL,
    weekday NVARCHAR(50) NULL,
    hour TINYINT NULL
);
GO

------------------------------------------------------------
-- 4. CHECK CURRENT DATABASE
------------------------------------------------------------
SELECT DB_NAME() AS current_database;
GO

------------------------------------------------------------
-- 5. CHECK TABLES IN DATABASE
------------------------------------------------------------
SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
ORDER BY TABLE_SCHEMA, TABLE_NAME;
GO

------------------------------------------------------------
-- 6. CHECK TOTAL ROWS AFTER IMPORT
------------------------------------------------------------
SELECT COUNT(*) AS total_rows
FROM dbo.retail_sales;
GO

------------------------------------------------------------
-- 7. PREVIEW TOP 10 ROWS
------------------------------------------------------------
SELECT TOP 10 *
FROM dbo.retail_sales;
GO

------------------------------------------------------------
-- 8. ADD CLEAN DATETIME COLUMN
------------------------------------------------------------
ALTER TABLE dbo.retail_sales
ADD invoicedate_clean DATETIME2;
GO

------------------------------------------------------------
-- 9. CONVERT INVOICEDATE TO PROPER DATETIME
------------------------------------------------------------
UPDATE dbo.retail_sales
SET invoicedate_clean = TRY_PARSE(invoicedate AS datetime2 USING 'en-GB');
GO

------------------------------------------------------------
-- 10. CHECK DATE CONVERSION STATUS
------------------------------------------------------------
SELECT 
    COUNT(*) AS total_rows,
    COUNT(invoicedate_clean) AS converted_rows,
    COUNT(*) - COUNT(invoicedate_clean) AS failed_rows
FROM dbo.retail_sales;
GO

------------------------------------------------------------
-- 11. VIEW FAILED DATE CONVERSIONS
------------------------------------------------------------
SELECT TOP 20 
    invoicedate,
    invoicedate_clean
FROM dbo.retail_sales
WHERE invoicedate_clean IS NULL;
GO

------------------------------------------------------------
-- 12. TOTAL REVENUE
------------------------------------------------------------
SELECT ROUND(SUM(revenue), 2) AS total_revenue
FROM dbo.retail_sales;
GO

------------------------------------------------------------
-- 13. TOTAL ORDERS
------------------------------------------------------------
SELECT COUNT(DISTINCT invoice) AS total_orders
FROM dbo.retail_sales;
GO

------------------------------------------------------------
-- 14. TOTAL CUSTOMERS
------------------------------------------------------------
SELECT COUNT(DISTINCT customer_id) AS total_customers
FROM dbo.retail_sales
WHERE customer_id IS NOT NULL;
GO

------------------------------------------------------------
-- 15. TOTAL PRODUCTS
------------------------------------------------------------
SELECT COUNT(DISTINCT stockcode) AS total_products
FROM dbo.retail_sales;
GO

------------------------------------------------------------
-- 16. AVERAGE ORDER VALUE
------------------------------------------------------------
SELECT ROUND(AVG(order_value), 2) AS avg_order_value
FROM (
    SELECT invoice, SUM(revenue) AS order_value
    FROM dbo.retail_sales
    GROUP BY invoice
) t;
GO

------------------------------------------------------------
-- 17. MONTHLY SALES TREND
------------------------------------------------------------
SELECT
    year,
    month,
    month_name,
    ROUND(SUM(revenue), 2) AS monthly_revenue
FROM dbo.retail_sales
GROUP BY year, month, month_name
ORDER BY year, month;
GO

------------------------------------------------------------
-- 18. HOURLY SALES ANALYSIS
------------------------------------------------------------
SELECT
    hour,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice) AS total_orders
FROM dbo.retail_sales
GROUP BY hour
ORDER BY hour;
GO

------------------------------------------------------------
-- 19. WEEKDAY SALES ANALYSIS
------------------------------------------------------------
SELECT
    weekday,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice) AS total_orders
FROM dbo.retail_sales
GROUP BY weekday
ORDER BY total_revenue DESC;
GO

------------------------------------------------------------
-- 20. TOP 10 PRODUCTS BY REVENUE
------------------------------------------------------------
SELECT TOP 10
    description,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM dbo.retail_sales
GROUP BY description
ORDER BY total_revenue DESC;
GO

------------------------------------------------------------
-- 21. TOP 10 PRODUCTS BY QUANTITY SOLD
------------------------------------------------------------
SELECT TOP 10
    description,
    SUM(quantity) AS total_quantity
FROM dbo.retail_sales
GROUP BY description
ORDER BY total_quantity DESC;
GO

------------------------------------------------------------
-- 22. COUNTRY-WISE SALES ANALYSIS
------------------------------------------------------------
SELECT
    country,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers
FROM dbo.retail_sales
GROUP BY country
ORDER BY total_revenue DESC;
GO

------------------------------------------------------------
-- 23. TOP 10 CUSTOMERS BY REVENUE
------------------------------------------------------------
SELECT TOP 10
    customer_id,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice) AS total_orders
FROM dbo.retail_sales
WHERE customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY total_revenue DESC;
GO

------------------------------------------------------------
-- 24. ONE-TIME VS REPEAT CUSTOMERS
------------------------------------------------------------
SELECT
    customer_type,
    COUNT(*) AS customer_count
FROM (
    SELECT
        customer_id,
        CASE
            WHEN COUNT(DISTINCT invoice) = 1 THEN 'One-Time'
            ELSE 'Repeat'
        END AS customer_type
    FROM dbo.retail_sales
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id
) t
GROUP BY customer_type;
GO

------------------------------------------------------------
-- 25. RUNNING MONTHLY REVENUE USING WINDOW FUNCTION
------------------------------------------------------------
WITH monthly_sales AS (
    SELECT
        year,
        month,
        SUM(revenue) AS monthly_revenue
    FROM dbo.retail_sales
    GROUP BY year, month
)
SELECT
    year,
    month,
    monthly_revenue,
    SUM(monthly_revenue) OVER (
        ORDER BY year, month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_revenue
FROM monthly_sales
ORDER BY year, month;
GO

------------------------------------------------------------
-- 26. CREATE MONTHLY SALES SUMMARY VIEW
------------------------------------------------------------
CREATE VIEW vw_monthly_sales_summary AS
SELECT
    year,
    month,
    month_name,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice) AS total_orders
FROM dbo.retail_sales
GROUP BY year, month, month_name;
GO

------------------------------------------------------------
-- 27. VIEW MONTHLY SALES SUMMARY
------------------------------------------------------------
SELECT TOP 10 *
FROM vw_monthly_sales_summary;
GO