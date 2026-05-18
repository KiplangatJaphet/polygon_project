# polygon_project

A fully automated stock data ETL (Extract, Transform, Load) pipeline that fetches daily stock prices for major tech companies, stores them in MongoDB Atlas, and is orchestrated using Apache Airflow.

---

## Project Structure

```
polygon_project/
├── dags/
│   └── polygon_dag.py      # Airflow DAG — orchestrates the pipeline hourly
├── extract.py              # Fetches stock data from the API
├── load.py                 # Loads data into MongoDB Atlas
├── stock_data.csv          # Raw stock data (local copy)
└── test.ipynb              # Jupyter notebook for exploration
```

---

## Stocks Tracked

| Symbol | Company   |
|--------|-----------|
| AAPL   | Apple     |
| GOOGL  | Google    |
| MSFT   | Microsoft |
| AMZN   | Amazon    |
| TSLA   | Tesla     |

---

## Architecture

```
Stock API → extract.py → load.py → MongoDB Atlas
                ↑
        Airflow (polygon_dag.py)
        Scheduled: @hourly
```

---

## Prerequisites

- Python 3.12+
- Apache Airflow
- A MongoDB Atlas account and cluster
- A stock data API key

---

## Installation

**Step 1 — Clone the project:**
```bash
git clone <your-repo-url>
cd polygon_project
```

**Step 2 — Create and activate a virtual environment:**
```bash
python3 -m venv env
source env/bin/activate
```

**Step 3 — Install dependencies:**
```bash
pip install requests pandas pymongo certifi apache-airflow asyncpg
```

---

## Configuration

**`extract.py`** — update your API credentials:
```python
api_key = "your_api_key_here"
date = "2026-01-09"  # Change to desired date
```

**`load.py`** — update your MongoDB credentials:
```python
password = "your_mongodb_password"
mongo_url = "mongodb+srv://your_user:{encoded_password}@cluster0.xxxxx.mongodb.net/?appName=Cluster0"
```



---

## Usage

### Manual Run

**Step 1 — Extract (fetch and preview stock data):**
```bash
python3 extract.py
```

Expected output:
```
  symbol        date     open    high       low   close      volume
0   AAPL  2026-01-09  259.075  260.21  256.2200  259.37  39996967.0
1  GOOGL  2026-01-09  327.090  330.83  325.8000  328.57  26214166.0
2   MSFT  2026-01-09  474.060  479.82  472.2001  479.28  18491036.0
3   AMZN  2026-01-09  244.568  247.86  242.2400  247.38  34559961.0
4   TSLA  2026-01-09  435.945  449.05  430.3900  445.01  67331456.0
```

**Step 2 — Load (insert data into MongoDB):**
```bash
python3 load.py
```

Expected output:
```
Loaded 5 records into MongoDB
```

---

### Automated Run with Airflow

**Step 1 — Activate your virtual environment:**
```bash
source /root/env/bin/activate
```

**Step 2 — Copy the DAG to Airflow's dags folder:**
```bash
cp /root/polygon_project/dags/polygon_dag.py /root/airflow/dags/
```

**Step 3 — Start Airflow:**
```bash
airflow standalone
```

**Step 4 — Open the Airflow UI:**
```
http://localhost:8080
```

**Step 5 — Get your login credentials:**
```bash
cat /root/airflow/simple_auth_manager_passwords.json.generated
```

**Step 6 — In the Airflow UI:**
- Find `polygon_stock` in the DAGs list
- Toggle it **ON**
- Click ▶️ to trigger it manually
- Click on the DAG to monitor task status

The pipeline will then run **automatically every hour**.

Pipeline output
<img width="1366" height="654" alt="image" src="https://github.com/user-attachments/assets/8ef82450-5a47-4055-8551-6272a17b924e" />


---

## MongoDB Setup

1. Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Under **Network Access**, add `0.0.0.0/0` to allow connections
3. Under **Database Access**, create a user with read/write permissions
4. Copy your connection string into `load.py`

**Database:** `stock_data_db`  
**Collection:** `stock_prices`

### View Loaded Data

**Option 1 — MongoDB Atlas UI:**
- Go to Atlas → Browse Collections → `stock_data_db` → `stock_prices`

**Option 2 — Terminal:**
```bash
python3 -c "
import pymongo, certifi
from urllib.parse import quote_plus
password = quote_plus('your_password')
client = pymongo.MongoClient(f'mongodb+srv://your_user:{password}@cluster0.xxxxx.mongodb.net/?appName=Cluster0', tlsCAFile=certifi.where())
collection = client['stock_data_db']['stock_prices']
for doc in collection.find():
    print(doc)
"
```

---

## Airflow DAG Details

| Property        | Value                        |
|-----------------|------------------------------|
| DAG ID          | `polygon_stock`              |
| Schedule        | `@hourly`                    |
| Catchup         | `False`                      |
| Task            | `run_stock_prices_pipeline`  |
| Start Date      | `2026-01-01`                 |

---

## Dependencies

| Package            | Purpose                            |
|--------------------|------------------------------------|
| `requests`         | HTTP calls to stock API            |
| `pandas`           | Data manipulation                  |
| `pymongo`          | MongoDB connection                 |
| `certifi`          | SSL certificate fix for WSL/Ubuntu |
| `apache-airflow`   | Pipeline orchestration             |
| `asyncpg`          | Async database driver for Airflow  |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'pymongo'` | `pip install pymongo` |
| `ModuleNotFoundError: No module named 'asyncpg'` | `pip install asyncpg` |
| SSL handshake error connecting to MongoDB | `pip install pymongo[srv] certifi` and use `tlsCAFile=certifi.where()` |
| DAG not visible in Airflow UI | Copy DAG to `/root/airflow/dags/` and wait 30 seconds |
| `DAG.__init__() got unexpected keyword argument 'schedule_interval'` | Replace `schedule_interval` with `schedule` |
| MongoDB connection refused | Add `0.0.0.0/0` to MongoDB Atlas Network Access |

---

## License

MIT
