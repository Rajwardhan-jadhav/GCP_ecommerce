"""Upload extracted e-commerce CSV files to the GCS raw landing bucket."""

from __future__ import annotations

import argparse
import logging
import os
from datetime import date
from pathlib import Path, PurePosixPath

from dotenv import load_dotenv
from google.cloud import storage
from google.cloud.exceptions import NotFound


def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Required environment variable {name} is not set")
    return value


def upload_csvs(
    source_dir: Path,
    bucket_name: str,
    project_id: str,
    prefix: str,
    load_date: str,
    dry_run: bool = False,
) -> list[str]:
    """Upload every CSV in source_dir and return its gs:// URI."""
    csv_files = sorted(source_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {source_dir}")

    bucket = None
    if not dry_run:
        client = storage.Client(project=project_id)
        bucket = client.bucket(bucket_name)
        try:
            bucket.reload()
        except NotFound as exc:
            raise RuntimeError(f"GCS bucket does not exist: {bucket_name}") from exc

    uploaded_uris: list[str] = []
    for csv_file in csv_files:
        object_name = str(
            PurePosixPath(prefix.strip("/"))
            / f"load_date={load_date}"
            / csv_file.name
        )
        uri = f"gs://{bucket_name}/{object_name}"

        if dry_run:
            logging.info("Would upload %s -> %s", csv_file, uri)
        else:
            assert bucket is not None
            blob = bucket.blob(object_name)
            blob.upload_from_filename(
                str(csv_file), content_type="text/csv", checksum="auto"
            )
            logging.info("Uploaded %s -> %s", csv_file, uri)
        uploaded_uris.append(uri)

    return uploaded_uris


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload extracted CSVs to GCS")
    parser.add_argument("--source-dir", type=Path, default=Path("data/csv"))
    parser.add_argument("--load-date", default=date.today().isoformat())
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    load_dotenv()
    args = parse_args()
    try:
        upload_csvs(
            source_dir=args.source_dir,
            bucket_name=required_env("GCS_BUCKET_NAME"),
            project_id=required_env("GCP_PROJECT_ID"),
            prefix=os.getenv("GCS_RAW_PREFIX", "raw/ecommerce"),
            load_date=args.load_date,
            dry_run=args.dry_run,
        )
    except Exception:
        logging.exception("GCS upload failed")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
