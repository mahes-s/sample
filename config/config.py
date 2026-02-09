"""Centralized configuration loading for the ETL pipeline."""

import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Runtime configuration loaded from environment variables."""

    database_url: str
    raw_sales_path: str
    source_system: str
    api_url: str


def load_settings() -> Settings:
    """Load settings from environment variables with sensible defaults."""

    return Settings(
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://etl_user:etl_password@localhost:5432/sales_dw",
        ),
        raw_sales_path=os.getenv("RAW_SALES_PATH", "data/raw_sales.csv"),
        source_system=os.getenv("SOURCE_SYSTEM", "csv"),
        api_url=os.getenv(
            "SALES_API_URL",
            "https://api.sampleapis.com/coffee/hot",
        ),
    )
