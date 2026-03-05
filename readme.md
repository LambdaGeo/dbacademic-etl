# DBAcademic ETL 🚀

This repository hosts the **ETL (Extract, Transform, Load)** pipeline for the **DBAcademic** project, developed by [LambdaGEO](https://github.com/LambdaGeo). Its primary goal is to automate the extraction of academic data from public sources, transforming it into a standardized format and loading it into our connected database.

## 📋 About the Project

**DBAcademic** aims to link and provide access to open data from higher education institutions. This ETL module is responsible for:
- **Extraction**: Fetching data from APIs, CSV files, and transparency portals.
- **Transformation**: Data cleaning, normalization, and enrichment (Semantic Web/Linked Data alignment).
- **Loading**: Inserting processed data into the database (PostgreSQL/PostGIS) or publishing it as RDF.

## 🛠️ Tech Stack

- **Python**: Core language for pipeline logic.
- **Docker & Docker Compose**: For environment orchestration and reproducibility.
- **Pandas/Polars**: For high-performance data manipulation.
- **Apache Airflow** (if applicable): For workflow scheduling and monitoring.

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose installed on your machine.

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone [https://github.com/LambdaGeo/dbacademic-etl.git](https://github.com/LambdaGeo/dbacademic-etl.git)
   cd dbacademic-etl
