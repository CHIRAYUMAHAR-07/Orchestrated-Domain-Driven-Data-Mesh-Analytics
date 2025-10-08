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
    return tot, dedup, dup_rate


Profiling with YData-Profiling : 

from ydata_profiling import ProfileReport\
df = spark.read.format("delta").load("/tmp/delta_data_mesh/customers").limit(10000).toPandas()\
profile = ProfileReport(df, title="Customers Profile", explorative=True)\
profile.to_file("/tmp/customers_profile_report.html")


# Analytics & Visualizations
Customer Lifetime Value (LTV)

ltv = spark_sales.groupBy("customer_id").agg(\
    F.sum("total_price").alias("ltv"),\
    F.count("*").alias("purchase_count")\
)

Product Price Distribution:
fig = px.histogram(products, x='price', nbins=50, title='Product Price Distribution')

# Real-Time Streaming Simulation
Socket Server

def start_socket_server(...): \ 
    # Emits synthetic events with customer_id, product_id, quantity, unit_price\

Spark Structured Streaming

socket_df = spark.readStream.format("socket").option("host", "127.0.0.1").option("port", 9998).load()\
json_df = socket_df.select(F.from_json(F.col("value"), schema).alias("data")).select("data.*")\


# Power BI Dashboard
The dashboard complements the notebook with rich visuals:

Comparative Analysis: UnitPrice vs. Country Count
Borough Classification: Service zone influence on Bronx
Fraud Detection: Sum of balances by transaction type
Zone Distribution: Across NYC boroughs
Customer Segmentation: Spend by segment and geography

# Key Learnings: 
Modular orchestration enables scalable simulation and analytics
Delta Lake provides reliability and ACID compliance for domain tables
Real-time streaming can be simulated and visualized with ease
Profiling tools accelerate EDA and data quality assurance
Power BI enhances storytelling and stakeholder communication

# Future Enhancements
Integrate ML models for fraud prediction and customer churn
Deploy FastAPI endpoints for real-time querying
Add CI/CD pipeline for automated data refresh
Expand dashboard with drill-downs and filters

# Tech Stack
Languages: Python, SQL
Libraries: PySpark, Delta Lake, Plotly, Seaborn, Faker, FastAPI, YData-Profiling
Tools: Google Colab, Power BI
Storage: Delta Lake (local simulation)

# Full Project Explanation

This project is a comprehensive demonstration of how to build a scalable, modular, and business-relevant data analytics platform using PySpark, Delta Lake, and Power BI. It is designed around the principles of domain-driven design and data mesh architecture, simulating realistic business domains and orchestrating them into a unified analytics ecosystem.

The project begins by setting up the environment in Google Colab, where system dependencies like Java and Python packages are installed. This includes configuring PySpark version 3.5.0 and Delta Lake version 3.1.0, ensuring compatibility and reliability for lakehouse operations. The environment is further enriched with libraries such as Faker for synthetic data generation, Plotly and Seaborn for visualization, and YData-Profiling for automated exploratory data analysis.

Once the environment is ready, the architecture is initialized using a custom Spark session builder. This function encapsulates all necessary Delta Lake configurations, allowing seamless creation and querying of Delta tables. This setup ensures that the data mesh is not only reproducible but also scalable across different domains and use cases.

The core of the project lies in simulating four distinct business domains: customers, products, sales, and finance. Each domain is crafted with realistic attributes. The customer domain includes 5,000 synthetic profiles with details such as name, email, country code, segment classification (consumer, small business, enterprise), signup date, and activity status. The product domain features 800 items spread across categories like software, hardware, subscription, service, and accessory, each with a launch date and price generated from a normal distribution. The sales domain simulates 120,000 transactions, linking customers and products with timestamped events, quantities, unit prices, and calculated total prices. The finance domain includes 50,000 entries categorized as either revenue or expense, each with a timestamp and descriptive note.

All these datasets are written to Delta Lake in overwrite mode, creating a curated and reliable foundation for analytics. Temporary views are registered for each domain, enabling SQL-like querying and transformation within Spark.

To ensure data integrity, a data quality report is generated for each domain. This involves checking for duplicate records based on primary keys. The results confirm that all domains have zero duplication, validating the robustness of the simulation and ingestion pipeline.

The project then moves into analytical territory, starting with customer lifetime value (LTV) analysis. Sales data is aggregated to compute total spend and purchase count per customer. This enriched view is joined with the customer domain, creating a comprehensive Customer360 table. The LTV distribution is visualized using Plotly histograms, and the top 20 customers by spend are identified and displayed.

In parallel, product price distribution is analyzed to understand pricing trends across categories. This helps in identifying outliers and validating the synthetic generation logic.

To simulate real-time analytics, a socket server is implemented in Python. This server emits synthetic events such as sales and signups at high frequency, mimicking a live data stream. Each event includes a timestamp, customer ID, product ID, quantity, and unit price. Spark Structured Streaming is configured to ingest these events, parse them into structured format, and write them to a Delta table in append mode. A checkpoint directory is maintained to ensure fault tolerance and recovery.

Once the stream is active, the ingested data is read back into Spark and converted to Pandas for visualization. Transactions per second (TPS) are computed by flooring timestamps to the nearest second and counting events. This metric is plotted over time, providing a clear view of system throughput and event density.

For deeper profiling, YData-Profiling is used to generate an HTML report of the customer domain. This report includes distributions, correlations, missing value analysis, and other statistical summaries, offering a quick yet thorough overview of the dataset.

The final layer of the project is the Power BI dashboard, which transforms the curated data into interactive visual stories. The dashboard includes comparative analysis of unit prices and country counts, borough classification influenced by service zones, fraud detection metrics segmented by transaction type, and zone distribution across NYC boroughs. It also visualizes customer segmentation by spend and geography, providing actionable insights for business stakeholders.

This project exemplifies how to build an enterprise-grade analytics platform that is modular, scalable, and impactful. It blends technical rigor with creative storytelling, demonstrating the power of orchestrated data mesh architecture in delivering business intelligence.

From environment setup to real-time streaming, from synthetic simulation to dashboard storytelling — every component is designed to be reusable, reproducible, and recruiter-ready. This project is not just a technical showcase but a strategic blueprint for modern data analytics.
