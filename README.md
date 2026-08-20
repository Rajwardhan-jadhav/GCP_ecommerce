# GCP_ecommerce

Legacy e-commerce data migration pipeline using Python, MySQL, GCS, BigQuery,
Dataflow, and Terraform.

## Stage 1: MySQL to DataFrames to CSV

The sample source dataset contains six related e-commerce tables:

```text
customers ──< orders ──< order_items >── products >── categories
                   └──< payments
```

The SQL files are safe to run more than once. The extractor loads each table into
a pandas DataFrame and writes it to `data/csv/<table>.csv`.

### 1. Create and populate MySQL

Run these commands from a terminal with MySQL 8 installed and running:

```bash
mysql -u root -p < database/01_schema.sql
mysql -u root -p < database/02_seed_data.sql
```

### 2. Configure Python

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set the correct MySQL user and password. The real `.env` is
ignored by Git so credentials are not committed.

### 3. Extract tables to CSV

```bash
python extraction/mysql_to_csv.py
```

Expected files:

```text
data/csv/
├── categories.csv
├── customers.csv
├── order_items.csv
├── orders.csv
├── payments.csv
└── products.csv
```

Use a different destination when needed:

```bash
python extraction/mysql_to_csv.py --output-dir path/to/output
```

## Stage 2: CSV to GCS Raw Landing

The uploader stores each extraction under a date-partitioned path:

```text
gs://<bucket>/raw/ecommerce/load_date=YYYY-MM-DD/<table>.csv
```

Set `GCP_PROJECT_ID`, `GCS_BUCKET_NAME`, and `GCS_RAW_PREFIX` in `.env`.
Authenticate locally with Application Default Credentials, then upload:

```powershell
gcloud auth application-default login
python gcs/upload_to_gcs.py --dry-run
python gcs/upload_to_gcs.py
```

## Stage 3: GCS Raw Landing to BigQuery Bronze

The Bronze loader uses explicit schemas and overwrites each raw table from the
selected landing-date partition. The dataset applies a 30-day default table
expiration and a 48-hour time-travel window.

```powershell
python bigquery/load_bronze.py --load-date 2026-08-20
```

## Repository layout

```text
GCP_ecommerce/
├── data/csv/                    # Generated CSV files
├── database/
│   ├── 01_schema.sql            # Database and table definitions
│   └── 02_seed_data.sql         # Sample e-commerce records
├── extraction/
│   └── mysql_to_csv.py          # MySQL -> DataFrame -> CSV
├── gcs/                          # Next stage: raw landing uploads
├── bigquery/                     # Bronze, Silver, and Gold assets
├── dataflow/                     # Dataflow transformations
├── terraform/                    # GCP infrastructure as code
├── .env.example
└── requirements.txt
```
