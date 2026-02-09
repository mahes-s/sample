"""Transform raw sales data into analytics-ready format."""

import logging
from pathlib import Path

import pandas as pd

from config.config import load_settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("transform_sales")


def transform_sales(raw_sales: pd.DataFrame) -> pd.DataFrame:
    """Clean, normalize, and enrich raw sales data."""

    logger.info("Starting transformation on %d records", len(raw_sales))

    cleaned = raw_sales.copy()
    cleaned.columns = [column.strip().lower() for column in cleaned.columns]

    required_columns = {
        "sale_id",
        "sale_timestamp",
        "customer_id",
        "product_id",
        "quantity",
        "unit_price",
        "currency",
        "source_system",
    }

    missing_columns = required_columns - set(cleaned.columns)
    if missing_columns:
        message = f"Missing required columns: {sorted(missing_columns)}"
        logger.error(message)
        raise ValueError(message)

    cleaned["quantity"] = cleaned["quantity"].fillna(0).astype(int)
    cleaned["unit_price"] = cleaned["unit_price"].fillna(0).astype(float)
    cleaned["currency"] = cleaned["currency"].fillna("USD")
    cleaned["sale_timestamp"] = pd.to_datetime(
        cleaned["sale_timestamp"], errors="coerce"
    )

    cleaned = cleaned.dropna(subset=["sale_id", "sale_timestamp"])
    cleaned["total_sale"] = cleaned["quantity"] * cleaned["unit_price"]
    cleaned["sale_date"] = cleaned["sale_timestamp"].dt.date

    analytics = cleaned[
        [
            "sale_id",
            "sale_date",
            "customer_id",
            "product_id",
            "quantity",
            "unit_price",
            "total_sale",
            "currency",
            "source_system",
        ]
    ]

    logger.info("Transformation complete with %d records", len(analytics))
    return analytics


def main() -> None:
    """CLI entrypoint for running transformations."""

    settings = load_settings()
    input_path = Path(settings.raw_sales_path)
    raw_sales = pd.read_csv(input_path)
    analytics = transform_sales(raw_sales)

    output_path = Path("data/analytics_sales.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    analytics.to_csv(output_path, index=False)
    logger.info("Wrote transformed data to %s", output_path)


if __name__ == "__main__":
    main()
