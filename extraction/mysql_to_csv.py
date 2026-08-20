"""Extract every configured MySQL table into a pandas DataFrame and CSV file."""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
from sqlalchemy.engine import Engine

TABLES = (
    "customers",
    "categories",
    "products",
    "orders",
    "order_items",
    "payments",
)


def build_engine() -> Engine:
    """Create a SQLAlchemy engine from environment variables."""
    load_dotenv()
    url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=os.getenv("MYSQL_DATABASE", "ecommerce"),
    )
    return create_engine(url, pool_pre_ping=True)


def extract_tables(engine: Engine, output_dir: Path) -> dict[str, pd.DataFrame]:
    """Load MySQL tables into DataFrames and save one CSV per table."""
    output_dir.mkdir(parents=True, exist_ok=True)
    dataframes: dict[str, pd.DataFrame] = {}

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        for table in TABLES:
            # Table names come only from the hard-coded allowlist above.
            frame = pd.read_sql_query(text(f"SELECT * FROM `{table}`"), connection)
            frame.to_csv(output_dir / f"{table}.csv", index=False, encoding="utf-8")
            dataframes[table] = frame
            logging.info("Exported %-12s %d rows", table, len(frame))

    return dataframes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export MySQL e-commerce tables to CSV")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/csv"),
        help="CSV destination directory (default: data/csv)",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    engine = build_engine()
    try:
        extract_tables(engine, args.output_dir)
    except Exception:
        logging.exception("MySQL extraction failed")
        raise SystemExit(1)
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
