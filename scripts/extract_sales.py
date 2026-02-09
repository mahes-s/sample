"""Extract raw sales data from a CSV file or public API."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
import requests

from config.config import load_settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("extract_sales")


def _read_csv(path: str) -> pd.DataFrame:
    """Read sales data from a local CSV file."""

    logger.info("Reading CSV from %s", path)
    return pd.read_csv(path)


def _read_api(url: str) -> pd.DataFrame:
    """Read sales-like data from a public API endpoint."""

    logger.info("Fetching data from API %s", url)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    payload: List[Dict[str, Any]] = response.json()
    logger.info("Received %d records from API", len(payload))

    normalized = []
    for record in payload:
        normalized.append(
            {
                "sale_id": record.get("id") or record.get("title"),
                "sale_timestamp": datetime.utcnow().isoformat(),
                "customer_id": record.get("title", "unknown").replace(" ", "_").lower(),
                "product_id": record.get("title", "product").replace(" ", "_").lower(),
                "quantity": 1,
                "unit_price": 5.00,
                "currency": "USD",
                "source_system": "api",
            }
        )

    return pd.DataFrame(normalized)


def extract_sales() -> pd.DataFrame:
    """Extract sales data based on the configured source."""

    settings = load_settings()
    try:
        if settings.source_system.lower() == "api":
            data_frame = _read_api(settings.api_url)
        else:
            data_frame = _read_csv(settings.raw_sales_path)
    except (OSError, requests.RequestException, json.JSONDecodeError) as exc:
        logger.error("Failed to extract sales data: %s", exc)
        raise

    logger.info("Extracted %d records", len(data_frame))
    return data_frame


def main() -> None:
    """CLI entrypoint for running extraction."""

    data_frame = extract_sales()
    output_path = Path("data/raw_sales_extracted.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data_frame.to_csv(output_path, index=False)
    logger.info("Wrote extracted data to %s", output_path)


if __name__ == "__main__":
    main()
