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
