
# YouTube Channel Analytics ETL Project

This project is an end-to-end ETL pipeline that extracts, transforms, and loads YouTube channel data using the YouTube Data API, and visualizes the results in Power BI. It is built with Apache Airflow, Python, Docker, Snowflake, and Power BI.

## 🔧 Technologies Used

- **Python** for scripting
- **YouTube Data API v3** for extracting data
- **Apache Airflow** for orchestration (via Docker)
- **Snowflake** as a cloud data warehouse
- **Power BI** for interactive dashboards
- **Docker** for containerized pipeline execution

## 📁 Folder Structure

```
.
├── scripts/
│   ├── youtube_api_extract.py       # Extracts data from YouTube API
│   ├── etl_pipeline.py              # Main ETL pipeline logic (load to Snowflake)
├── dags/
│   └── youtube_etl_dag.py           # Airflow DAG definition
├── docker/
│   └── Dockerfile                   # Dockerfile for Airflow setup
├── docker-compose.yml              # To spin up Airflow environment
├── requirements.txt                # Python dependencies
├── YouTube_Dashboard.pbix          # Power BI dashboard file
└── README.md                       # Project documentation (this file)
```

## ⚙️ ETL Pipeline Description

1. **Extract**  
   - Pulls metadata about recent videos from a specified YouTube channel using the YouTube Data API.

2. **Transform**  
   - Parses relevant fields like title, publish date, views, likes, comments (if available).
   - Prepares the data for loading.

3. **Load**  
   - Uploads the transformed data to a Snowflake table using `snowflake-connector-python`.

4. **Visualize**  
   - Power BI connects to Snowflake (via ODBC) to build an interactive dashboard.

## 🐳 Running Locally (via Docker)

```bash
# Spin up Airflow environment
docker-compose up --build
```

## 🚀 Airflow DAG

The DAG `youtube_etl_dag.py` runs the full pipeline with tasks for extract, transform, and load.

## 📊 Power BI Dashboard

Once data is in Snowflake, open `YouTube_Dashboard.pbix` to view:

- Number of videos per month
- Most viewed videos
- Engagement trends over time
- Slicer for publish month

## ✅ Requirements

- Snowflake trial account
- YouTube API key & Channel ID
- Docker Desktop installed
- Power BI Desktop

## 🙌 Author

Sachal Tyagi  
[sachaltyagi999@gmail.com](mailto:sachaltyagi999@gmail.com)  
[LinkedIn](https://www.linkedin.com/in/sachal-tyagi-84817726a/)
