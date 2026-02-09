"""Load transformed sales data into the analytics database."""

import logging
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from config.config import load_settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("load_sales")


def load_sales(analytics_sales: pd.DataFrame, database_url: str) -> None:
    """Insert analytics sales data into PostgreSQL tables."""

    engine = create_engine(database_url)
    try:
        with engine.begin() as connection:
            logger.info("Loading %d records into analytics_sales", len(analytics_sales))
            analytics_sales.to_sql(
                "analytics_sales",
                con=connection,
                if_exists="append",
                index=False,
                method="multi",
            )
            logger.info("Data load complete")
    except SQLAlchemyError as exc:
        logger.error("Failed to load data: %s", exc)
        raise


def main() -> None:
    """CLI entrypoint for loading data."""

    settings = load_settings()
    input_path = Path("data/analytics_sales.csv")
    if not input_path.exists():
        raise FileNotFoundError(
            "Transformed data not found. Run transform_sales.py first."
        )

    analytics_sales = pd.read_csv(input_path)
    load_sales(analytics_sales, settings.database_url)


if __name__ == "__main__":
    main()
