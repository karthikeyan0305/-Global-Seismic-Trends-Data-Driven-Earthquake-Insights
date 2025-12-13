# -Global-Seismic-Trends-Data-Driven-Earthquake-Insights
Analyze and interpret global earthquake data to identify seismic patterns, trends, and risk zones. Build a data-driven system using API-based retrieval, preprocessing, and SQL analytics for meaningful earthquake insights.
**🌍 Project Overview**

Global Seismic Trends is a full end-to-end data analytics project that retrieves earthquake data from the USGS API, preprocesses it using Python & Pandas, stores the cleaned dataset in MySQL, performs deep analysis using SQL queries, and visualizes insights through an interactive Streamlit Dashboard.

This project helps governments, researchers, and disaster-management organizations identify global earthquake patterns, high-risk zones, and seismic trends.

**🛠️ Tech Stack

Python (Pandas, Requests, SQLAlchemy)

Regex

MySQL / MySQL Workbench

Streamlit

USGS Earthquake API

Virtual Environment (venv)**


Global-Sesimic/
│
├── data/
│   ├── earthquakes_raw.csv
│   ├── earthquakes_clean.csv
│
├── src/
│   ├── config.py
│   ├── fetch_api.py
│   ├── clean_data.py
│   ├── load_to_mysql.py
│   ├── main.py
│
├── sql/
│   ├── create_table.sql
│   ├── analysis_queries.sql
│
│
├── streamlit_app/
│   ├── dashboard.py
│
│
└── README.md
