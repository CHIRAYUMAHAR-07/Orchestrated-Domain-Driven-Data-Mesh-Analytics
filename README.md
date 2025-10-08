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

├── notebooks/
│   ├── orchestrated_data_mesh.ipynb        # Main Colab notebook
│   ├── customer360_streaming.ipynb         # Real-time socket + Delta streaming
│   └── profiling_and_eda.ipynb             # YData-Profiling integration
├── dashboards/
│   └── powerbi_dashboard.pbix              # Interactive Power BI dashboard
├── data/
│   ├── customers.parquet
│   ├── products.parquet
│   ├── sales.parquet
│   └── finance.parquet
├── delta/
│   └── curated Delta tables for each domain
├── visuals/
│   └── Plotly charts and saved images
├── README.md                               # This file

