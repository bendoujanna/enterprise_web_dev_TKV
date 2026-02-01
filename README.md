# enterprise_web_dev_TKV

## team name: Sprint Zero


### Project description (week 1)

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
├── docs/
│   ├── erd_diagram.png       # ERD image
│   └── api_docs.md
├── database/                 # Database implementation
│   └── database_setup.sql
├── json/                     # json schemas
│    └── examples
│       ├── json_schemas.json
│       ├── system_log.json
│       ├── transaction_category.json
│       ├── transaction_clean.json  
│       ├── transaction_complete.json   
│       └── user_example.json
├── api/
│   ├── server.py            # The main API server (handles requests)
│   ├── transactions.json    # The persistent database (JSON format)
│   └── test_api.sh          # Automated test script
├── dsa/
│   ├── modified_sms_v2.xml  # The raw XML data source
│   ├── xml_parser.py        # Script to convert XML -> JSON
│   ├── search_analysis.py   # DSA Performance comparison script
│   └── performance_results.json # Results of the DSA analysis
└── screenshots

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


## Database design and implementation  (week 2)

## I. Entity relationship diagram design

[View the Entity Relationship Diagram](docs/erd_diagram.png)

**Database design justification**

This Entity Relationship Diagram (ERD) represents a relational database architecture designed to efficiently store and manage Mobile Money (MoMo) transactions parsed from XML data. The design prioritizes data integrity, scalability, and strict financial accuracy, implemented using MySQL. The schema follows the Third Normal Form (3NF) to eliminate redundancy and ensure that non-key attributes are fully dependent on the primary key.

Core Architecture and Relationships The central entity is the Transactions table, which is linked to Transaction_Categories via a One-to-Many (1:M) relationship, allowing us to categorize operations (e.g., "P2P", "Bill Payment") without duplicating text.

The most critical design decision was resolving the Many-to-Many (M:N) relationship between Users and Transactions. Since a single MoMo transaction involves multiple actors (a Sender, a Receiver, and often an Agent), a direct link would have been insufficient. We resolved this by creating a junction table named Transaction_Parties. This table records every participant in a transaction with a specific role (SENDER, RECEIVER, AGENT). We assigned a surrogate Primary Key (party_id) of type INT for efficient indexing, while simultaneously enforcing a UNIQUE constraint on the combination of transaction_id, user_id, and role to prevent logical duplicates.

Data Integrity and Types To ensure financial precision, all monetary fields (amount, fee, account_balance) use the DECIMAL(15, 2) data type rather than FLOAT, eliminating the risk of rounding errors during calculations. We also utilized ENUM types for columns like status and user_type to restrict data entry to valid, predefined states. Finally, the System_Logs entity provides an independent audit trail, tracking the parsing process and capturing any errors via a log_level attribute, ensuring the system is transparent and debuggable.

## II. Database setup and implementation

### Overview
MySQL database for MoMo SMS transaction processing with support for multiple user types, transaction categories, and comprehensive audit logging.

### Prerequisites
- MySQL 8.0 or higher installed
- MySQL Workbench (recommended for running scripts)

### Quick Setup

**Using MySQL Workbench:**
1. Open MySQL Workbench
2. Connect to Local instance (password: `michealkong24@x`)
3. File → Open SQL Script → Select `database_setup.sql`
4. Click Execute
5. Refresh schemas to see `momo_sms_db`

**Verify Installation:**
```sql
USE momo_sms_db;
SHOW TABLES;
```

### Database Structure

**Tables:**
- `users` - MoMo account holders (5 sample records)
  - Supports PERSON, MERCHANT, BANK, SYSTEM account types
  - Indexed on phone_number, account_code, user_type
  
- `transaction_categories` - Transaction types (5 sample records)
  - Money Transfer, Airtime, Bill Payment, Merchant Payment, Cash Withdrawal
  - Indexed on category_code
  
- `transactions` - Main transaction records (5 sample records)
  - Stores amount, currency, fee, status, reference codes
  - Indexed on category_id, transaction_date, status, currency
  
- `transaction_parties` - User-Transaction junction table (10 sample records)
  - Resolves M:N relationship between users and transactions
  - Tracks SENDER and RECEIVER roles
  - Indexed on transaction_id, user_id, role
  
- `system_logs` - System audit logs (5 sample records)
  - Tracks all system operations and errors
  - Indexed on log_date, log_level, user_id, transaction_id

### Key Features

  **Foreign Key Constraints** - Referential integrity across all tables
- transactions → transaction_categories
- transaction_parties → transactions, users
- system_logs → users, transactions

  **CHECK Constraints** - Data validation rules
- Phone numbers must start with '+'
- Transaction amounts must be positive
- Fees must be non-negative
- Log levels must be INFO/WARNING/ERROR/CRITICAL

  **15 Performance Indexes** - Optimized for common queries
- All foreign keys indexed
- Frequently searched columns indexed (phone, dates, status)

  **Column Comments** - Self-documenting schema
- Every column has descriptive comments

  **M:N Relationship** - Junction table pattern
- Users and Transactions linked via transaction_parties table
- Supports multiple participants per transaction

### Sample Queries

**View all users:**
```sql
SELECT * FROM users;
```

**Transactions with categories (JOIN):**
```sql
SELECT t.transaction_id, t.amount, tc.name AS category, t.status
FROM transactions t
JOIN transaction_categories tc ON t.category_id = tc.category_id;
```

**User transaction history (M:N relationship):**
```sql
SELECT tp.transaction_id, u.name AS user_name, tp.role, t.amount
FROM transaction_parties tp
JOIN users u ON tp.user_id = u.user_id
JOIN transactions t ON tp.transaction_id = t.transaction_id
ORDER BY tp.transaction_id;
```

### Assignment Files

- `database/database_setup.sql` - Complete database setup script with DDL and sample data
- `json_schemas.json` - JSON representations of database entities for API design
- `screenshots/` - Query results demonstrating CRUD operations and constraints
  - 01_tables.png - Database tables
  - 02_users.png - User records
  - 03_transactions_join.png - JOIN query results
  - 04_many_to_many.png - M:N relationship demonstration
  - 05_update.png - UPDATE operation
  - 06_constraints.png - Database constraints
  - 07_indexes.png - Performance indexes

### III. JSON Data Modeling 

Added JSON schemas for MoMo transaction API responses in `/data/json_models/`:
- Complete transaction examples with nested relationships
- SQL-to-JSON mapping documentation

[View the documentation](json/task3_report.md)

- 6 JSON example files for all database entities

#### Database design documentation

[Database Design documentation.pdf](https://github.com/user-attachments/files/24858284/Database.Design.documentation.pdf)

##### Team sheet

[BSE Team Task Sheet_EWD_Database Design and Implementation_Cohort 3_Team16 - 1 (1).pdf](https://github.com/user-attachments/files/24858298/BSE.Team.Task.Sheet_.EWD_Database.Design.and.Implementation_Cohort.3_Team16.-.1.1.pdf)

## Mobile Money SMS Transaction API

This project is a **RESTful API** designed to manage Mobile Money transaction records. It was built to solve the problem of parsing, storing, and efficiently searching through thousands of SMS transaction logs.

The system performs three main tasks:
1.  **Parses** raw XML SMS data into a structured JSON format.

2.  **Serves** this data via a secure HTTP API (Create, Read, Update, Delete).

3.  **Demonstrates** the performance difference between Linear Search (O(n)) and Dictionary Lookup (O(1)).

# I. Getting started 

**Prerequisites**

        Python 3.x is installed on your system.
        
        Terminal/Command Prompt access.

**Installation & Setup**

1. Parse the Data First, run the parser script to convert the raw XML logs (1,691 records) into a usable JSON database.

       python3 dsa/xml_parser.py

2. Start the API Server: Navigate to the api folder and start the server

        cd api
        python3 server.py

The server will start at: http://localhost:8000

# II. Authentification

The API is secured using Basic Authentication. You must provide these credentials to access any endpoint.

    Username: admin
    
    Password: password123

Requests without credentials will return 401 Unauthorized

# III. API endpoints

**1. List All Transactions**
   
Retrieves the full list of transactions.

- Method: GET

- URL: /transactions

- Response: JSON array of all transactions.

**2. Get Single Transaction**
   
Retrieves details for a specific ID.

- Method: GET

- URL: /transactions/{id}

- Example: /transactions/1

**3. Create Transaction**

Adds a new record to the database.

- Method: POST

- URL: /transactions

- Body (JSON):
  
          {
            "type": "SEND",
            "amount": 5000,
            "sender": "You",
            "receiver": "Samuel Carter 58769",
            "status": "completed"
          }

**4. Update Transaction**

Modifies an existing record.

- Method: PUT

- URL: /transactions/{id}

- Body (JSON):

      {
        "amount": 6000,
        "status": "completed"
      }

**5. Delete Transaction**

Permanently removes a record.

- Method: DELETE

- URL: /transactions/{id}

## IV. DSA Component: Performance Analysis

A key requirement of this project was to prove that Hash Maps (Dictionaries) are faster than Linear Lists for data retrieval.

We compared two search algorithms:

1. Linear Search (O(n)): Loops through the list one by one. Slower as data grows.

2. Dictionary Lookup (O(1)): Uses a hash key to jump directly to the data. Instant access.

**How to run the analysis**

    python3 dsa/search_analysis.py

**Results**

1. LINEAR SEARCH (O(n) - checks each item) 

       Average time: 0.000051707 seconds
       Total time:   0.001034138 seconds
       Fastest:      0.000039141 seconds
       Slowest:      0.000117806 seconds

2. DICTIONARY LOOKUP (O(1) - direct access)
   
       Dict creation: 0.000160624 seconds
       Average time:  0.000000230 seconds
       Total time:    0.000004606 seconds
       Fastest:       0.000000074 seconds
       Slowest:       0.000001958 seconds


#### Team members

Bendou Janna Vitalina Soeur

Kamy Uwambaye

Tumba II Zikoranachukwudi M Kongolo
