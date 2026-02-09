# Sales ETL Pipeline

This project provides a modular, production-ready Sales ETL pipeline that extracts data from a CSV file or public API, transforms it for analytics, and loads it into PostgreSQL. The pipeline can be orchestrated with Apache Airflow.

## Project Structure

```
.
├── config/
│   └── config.py
├── data/
│   └── raw_sales.csv
├── orchestration/
│   └── sales_etl_dag.py
├── scripts/
│   ├── extract_sales.py
│   ├── transform_sales.py
│   └── load_sales.py
├── sql/
│   └── schema.sql
├── requirements.txt
└── README.md
```

## Features

- **Extract** sales data from CSV or API sources.
- **Transform** data by cleaning, handling missing values, and computing total sales.
- **Load** analytics-ready data into PostgreSQL.
- **Orchestrate** daily runs with an Airflow DAG.
- **Logging & error handling** built into each script.

## Setup

### 1) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Create database tables

```bash
psql "postgresql://etl_user:etl_password@localhost:5432/sales_dw" -f sql/schema.sql
```

### 3) Configure environment variables

Set the following environment variables (sample values shown):

```bash
export DATABASE_URL="postgresql+psycopg2://etl_user:etl_password@localhost:5432/sales_dw"
export RAW_SALES_PATH="data/raw_sales.csv"
export SOURCE_SYSTEM="csv"  # or "api"
export SALES_API_URL="https://api.sampleapis.com/coffee/hot"
```

### 4) Run the pipeline locally

```bash
python scripts/extract_sales.py
python scripts/transform_sales.py
python scripts/load_sales.py
```

## Orchestration (Airflow)

1. Copy `orchestration/sales_etl_dag.py` into your Airflow DAGs folder.
2. Ensure Airflow uses the same Python environment with dependencies installed.
3. Configure the environment variables in your Airflow connections or environment.
4. The DAG runs **daily** with `@daily` schedule.

## How the ETL Works

### Extract
- Reads CSV data or calls the API depending on `SOURCE_SYSTEM`.
- Logs record counts and errors during extraction.

### Transform
- Standardizes column names.
- Handles missing values for quantity, price, and currency.
- Converts timestamps to dates and calculates total sale values.

### Load
- Inserts transformed data into the `analytics_sales` table using SQLAlchemy.

## Database Schema

The schema includes:
- `raw_sales`: raw data from ingestion.
- `analytics_sales`: cleansed and enriched data for analytics.

See [`sql/schema.sql`](sql/schema.sql) for full definitions.

## Production Considerations

- Replace the sample API with your production data source.
- Add schema validations and duplicate detection before loading.
- Configure Airflow retries, alerting, and SLA monitoring.
- Use a secrets manager for `DATABASE_URL`.

## Example Database Connection

```python
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://etl_user:etl_password@localhost:5432/sales_dw")
with engine.begin() as connection:
    connection.execute("SELECT 1")
```
