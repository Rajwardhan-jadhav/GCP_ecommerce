"""Load raw e-commerce CSV objects from GCS into BigQuery Bronze tables."""

from __future__ import annotations

import argparse
import logging
import os
from datetime import date

from dotenv import load_dotenv
from google.api_core.exceptions import NotFound
from google.cloud import bigquery

SCHEMAS: dict[str, list[tuple[str, str]]] = {
    "customers": [
        ("customer_id", "INTEGER"), ("first_name", "STRING"),
        ("last_name", "STRING"), ("email", "STRING"), ("phone", "STRING"),
        ("city", "STRING"), ("state", "STRING"), ("country", "STRING"),
        ("postal_code", "STRING"), ("created_at", "TIMESTAMP"),
    ],
    "categories": [
        ("category_id", "INTEGER"), ("category_name", "STRING"),
        ("description", "STRING"),
    ],
    "products": [
        ("product_id", "INTEGER"), ("category_id", "INTEGER"),
        ("sku", "STRING"), ("product_name", "STRING"),
        ("unit_price", "NUMERIC"), ("stock_quantity", "INTEGER"),
        ("is_active", "BOOLEAN"), ("created_at", "TIMESTAMP"),
    ],
    "orders": [
        ("order_id", "INTEGER"), ("customer_id", "INTEGER"),
        ("order_date", "TIMESTAMP"), ("status", "STRING"),
        ("shipping_address", "STRING"), ("total_amount", "NUMERIC"),
    ],
    "order_items": [
        ("order_item_id", "INTEGER"), ("order_id", "INTEGER"),
        ("product_id", "INTEGER"), ("quantity", "INTEGER"),
        ("unit_price", "NUMERIC"), ("line_total", "NUMERIC"),
    ],
    "payments": [
        ("payment_id", "INTEGER"), ("order_id", "INTEGER"),
        ("payment_date", "TIMESTAMP"), ("payment_method", "STRING"),
        ("amount", "NUMERIC"), ("payment_status", "STRING"),
        ("transaction_reference", "STRING"),
    ],
}


def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Required environment variable {name} is not set")
    return value


def ensure_dataset(
    client: bigquery.Client, dataset_id: str, location: str
) -> bigquery.Dataset:
    full_id = f"{client.project}.{dataset_id}"
    try:
        dataset = client.get_dataset(full_id)
        if dataset.location.lower() != location.lower():
            raise ValueError(
                f"Dataset {full_id} is in {dataset.location}, expected {location}"
            )
        return dataset
    except NotFound:
        dataset = bigquery.Dataset(full_id)
        dataset.location = location
        dataset.description = "Bronze raw tables loaded from the GCS landing zone"
        dataset.labels = {"layer": "bronze", "pipeline": "ecommerce"}
        dataset.default_table_expiration_ms = 30 * 24 * 60 * 60 * 1000
        dataset.max_time_travel_hours = 48
        return client.create_dataset(dataset, timeout=30)


def load_tables(
    client: bigquery.Client,
    dataset_id: str,
    bucket_name: str,
    prefix: str,
    load_date: str,
) -> dict[str, int]:
    row_counts: dict[str, int] = {}
    for table_name, fields in SCHEMAS.items():
        uri = (
            f"gs://{bucket_name}/{prefix.strip('/')}/"
            f"load_date={load_date}/{table_name}.csv"
        )
        table_id = f"{client.project}.{dataset_id}.{table_name}"
        config = bigquery.LoadJobConfig(
            schema=[bigquery.SchemaField(name, field_type) for name, field_type in fields],
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )
        job = client.load_table_from_uri(uri, table_id, job_config=config)
        job.result()
        table = client.get_table(table_id)
        row_counts[table_name] = table.num_rows
        logging.info("Loaded %-12s %d rows from %s", table_name, table.num_rows, uri)
    return row_counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load GCS CSV files into Bronze")
    parser.add_argument("--load-date", default=date.today().isoformat())
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    load_dotenv()
    args = parse_args()
    try:
        project_id = required_env("GCP_PROJECT_ID")
        dataset_id = os.getenv("BQ_BRONZE_DATASET", "rajwardhan_bronze")
        location = os.getenv("BQ_LOCATION", "us-central1")
        client = bigquery.Client(project=project_id, location=location)
        ensure_dataset(client, dataset_id, location)
        load_tables(
            client=client,
            dataset_id=dataset_id,
            bucket_name=required_env("GCS_BUCKET_NAME"),
            prefix=os.getenv("GCS_RAW_PREFIX", "raw/ecommerce"),
            load_date=args.load_date,
        )
    except Exception:
        logging.exception("BigQuery Bronze load failed")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
