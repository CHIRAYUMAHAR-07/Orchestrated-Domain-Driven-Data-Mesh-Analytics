# Orchestrated-Domain-Driven-Data-Mesh-Analytics

# Project Overview
This project demonstrates a full-stack data analytics pipeline that combines domain-driven design, data mesh architecture, and real-time streaming analytics using PySpark, Delta Lake, and Power BI. It simulates realistic business domains, orchestrates scalable data workflows, and delivers insights through both code and dashboards.

The goal is to showcase how modern data platforms can be built with modularity, reproducibility, and business relevance — from raw simulation to curated insights.

# Architecture Summary
The project is structured around four core domains:

Customers: Profiles with country, segment, signup date, and activity status
Products: Items across categories with price and launch date
Sales: Timestamped transactions with quantity, unit price, and total price
Finance: Revenue and expense entries with notes and timestamps
Each domain is simulated using Python and Faker, stored in Delta Lake tables, and analyzed using PySpark, Plotly, and Power BI.

# Environment Setup
The notebook installs and configures:

openjdk-11-jdk-headless for Spark
pyspark==3.5.0, delta-spark==3.1.0 for Delta Lake integration
faker, plotly, seaborn, matplotlib, fastapi, uvicorn, scikit-learn, pandas-profiling, ydata-profiling for analytics and simulation

Delta Lake is configured via:

builder = SparkSession.builder \
    .appName("DeltaLake-Colab") \
    .master("local[*]") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
spark = configure_spark_with_delta_pip(builder).getOrCreate()


# Data Simulation
Customers
5,000 synthetic profiles

Attributes: customer_id, name, email, country, segment, signup_date, is_active
Segments: consumer, small_business, enterprise

Products
800 products across 5 categories: software, hardware, subscription, service, accessory

Price distribution: Normal(120, 60) + 5

Sales
120,000 transactions
Attributes: transaction_id, customer_id, product_id, quantity, unit_price, total_price, ts

Finance
50,000 entries

Attributes: entry_id, date, amount, type, note
All datasets are saved as .parquet and written to Delta Lake.

# Data Quality & Profiling
Deduplication Report

Using PySpark:

def dq_report(df, key_cols):\
    tot = df.count()\
    dedup = df.dropDuplicates(key_cols).count()\
    dup_rate = (tot - dedup) / max(1, tot)\
    return tot, dedup, dup_rate\


Profiling with YData-Profiling : 

from ydata_profiling import ProfileReport\
df = spark.read.format("delta").load("/tmp/delta_data_mesh/customers").limit(10000).toPandas()\
profile = ProfileReport(df, title="Customers Profile", explorative=True)\
profile.to_file("/tmp/customers_profile_report.html")\
