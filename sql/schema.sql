-- Schema for raw and analytics sales data (PostgreSQL)

CREATE TABLE IF NOT EXISTS raw_sales (
    sale_id TEXT PRIMARY KEY,
    sale_timestamp TIMESTAMP NOT NULL,
    customer_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    currency TEXT NOT NULL,
    source_system TEXT NOT NULL,
    ingestion_timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analytics_sales (
    sale_id TEXT PRIMARY KEY,
    sale_date DATE NOT NULL,
    customer_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    total_sale NUMERIC(14, 2) NOT NULL,
    currency TEXT NOT NULL,
    source_system TEXT NOT NULL,
    transformed_timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_raw_sales_date
    ON raw_sales (sale_timestamp);

CREATE INDEX IF NOT EXISTS idx_analytics_sales_date
    ON analytics_sales (sale_date);
