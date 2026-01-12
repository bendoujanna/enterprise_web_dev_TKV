# enterprise_web_dev_TKV

## team name: TKV_eng


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

## High-Level System Architecture

**Link:** [System architecture](https://docs.google.com/document/d/11Mo64WVRFxF-ntBpAhk93I35mZiF2ezVPgK3KJmt91s/edit?usp=sharing)

To handle the complexity of MoMo transaction data, we have designed a modular pipeline that moves data from raw SMS exports to a polished user dashboard. Here is how the pieces fit together:

**1. Data Ingestion**

The process starts with our raw data source, a MoMo XML file. This contains the original transaction logs that need to be parsed and structured.

**2. The ETL Pipeline (The Engine)**

This is where the heavy lifting happens. We have broken the processing logic into three distinct steps to keep the code maintainable:

    Parsing: parse_xml.py reads the XML structure and extracts the raw message strings.
    
    Cleaning: clean_normalize.py handles the "messy" parts of the data, like standardizing phone numbers, fixing date formats, and ensuring currency amounts are treated as numbers.
    
    Categorizing: categorize.py uses pattern-matching to identify exactly what happened in each transaction—whether it was a peer-to-peer transfer, a withdrawal, or an airtime purchase.

**3. Data Storage & Loading**

Once the data is refined, load_db.py distributes it to three essential locations:

    SQLite Database: Our relational storage for long-term data integrity (db.sqlite3).
    
    JSON Feed: A processed dashboard.json file designed for quick loading by the frontend.
    
    System Logs: An etl.log file to help us track the pipeline's health and troubleshoot any errors.

**4. The Visualization Layer**

The user interacts with a web dashboard (index.html). Using chart_handler.js, the dashboard fetches the processed JSON data and turns it into interactive charts and a searchable transaction table.

**5. Scalability (Bonus API)**

We have also included a REST endpoint in our architecture. This provides a professional gateway to query the database, making the system ready for future expansions or mobile app integration.

## Scrum Board

Our team is using **Trello** for Agile task management and sprint planning.

**Board URL:** [MoMo Dashboard Scrum Board](https://trello.com/invite/b/69624a1558e6a5d62412b76c/ATTIa8c83bd9bb092c937a5cac581aae0704AC5A5E80/momo-dashboard-scrum-board)

**Board Structure:**
- **To Do**: Backlog of upcoming tasks (3 initial tasks added)
- **In Progress**: Currently active work items
- **Done**: Completed tasks

**Initial Tasks:**
1. Set up team GitHub repository
2. Create system architecture diagram
3. Research XML parsing libraries

#### Team members

Bendou Janna Vitalina Soeur

Kamy Uwambaye

Tumba II Zikoranachukwudi M Kongolo
