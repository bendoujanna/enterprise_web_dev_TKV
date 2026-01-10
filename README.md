# enterprise_web_dev_TKV

## team name:


### Project description

This project is an enterprise-level full-stack application designed to process, analyze, and visualize Mobile Money (MoMo) transaction data. The system automates the transition of unstructured financial data from raw XML SMS exports into a structured, relational format for meaningful business intelligence.

### Project structure 

```
├── README.md                 # Project overview, setup, and links
├── .env              # Template for environment variables
├── requirements.txt          # Python dependencies (lxml, dateutil, etc.)
├── index.html                # Main Dashboard entry point
├── web/
│   ├── styles.css            # Dashboard styling
│   ├── chart_handler.js      # Logic for fetching and rendering charts
│   └── assets/               # Images, icons, and diagrams
├── data/
│   ├── raw/                  # Raw MoMo XML input (Git-ignored)
│   ├── processed/            # Cleaned JSON outputs for the frontend
│   ├── db.sqlite3            # SQLite Database file
│   └── logs/
│       ├── etl.log           # Logs for the ETL process
│       └── dead_letter/      # Storage for unparsed/invalid XML snippets
├── etl/
│   ├── __init__.py
│   ├── config.py             # File paths and configuration thresholds
│   ├── parse_xml.py          # XML parsing logic
│   ├── clean_normalize.py    # Data cleaning (dates, amounts, phones)
│   ├── categorize.py         # Transaction type classification logic
│   ├── load_db.py            # Database schema and upload logic
│   └── run.py                # Main CLI to execute the full pipeline
├── api/                      # Optional: API layer for data access
│   ├── __init__.py
│   ├── app.py                # FastAPI/Flask entry point
│   └── schemas.py            # Data models
├── scripts/
│   ├── run_etl.sh            # Script to run the ETL pipeline
│   ├── export_json.sh        # Script to rebuild processed JSON
│   └── serve_frontend.sh     # Script to launch local web server
└── tests/
    ├── test_parse_xml.py     # Unit tests for parsing
    ├── test_clean_normalize.py
    └── test_categorize.py
```

#### Team members

Bendou Janna Vitalina Soeur

Kamy Uwambaye

Tumba II Zikoranachukwudi M Kongolo
