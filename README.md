# Supplier360 – AI + AWS Bedrock Supplier Trust Scoring System

Supplier360 is an end-to-end **AI + AWS Bedrock–powered Supplier 360° view** that helps procurement and risk teams:

- Evaluate **supplier compliance** against internal policies  
- Detect **duplicate / overlapping suppliers**  
- Monitor **performance & risk signals** over time  

The core intention of this project is to generate a unified Supplier Trust Score by combining data integrity, certification health, and operational performance. The system uses Amazon Bedrock Agents with Lambda-based action groups and an Aurora PostgreSQL backend, supported by a lightweight Streamlit UI for local demos.

---

## 1. Key Features

- 🤖 **Bedrock Agent–orchestrated workflow**  
  Interact using natural language prompts such as “Generate a supplier risk profile” or  
  “What is the compliance score for Supplier X?”. The Agent coordinates all Lambda action groups  
  to produce a unified analysis.

- 📊 **Compliance scoring engine**  
  Lambda functions query Aurora PostgreSQL to evaluate certification validity, identify missing or  
  expired documents, and generate a structured Certification Score.

- 🧹 **Supplier deduplication & data integrity check**  
  Fuzzy matching helps detect duplicate or overlapping supplier records, ensuring accurate supplier  
  identity before any scoring is performed.

- 📈 **Operational performance insights**  
  Aggregates delivery accuracy, quality compliance, invoice accuracy, and incident history to  
  compute the Operational Score.

- 🧮 **Unified Supplier Trust Score**  
  Data integrity, certification health, and operational performance are combined using a weighted  
  scoring model to produce a final Supplier Trust Score.

- 🖥️ **Lightweight Streamlit demo UI**  
  A simple chat-style interface for interacting with the Bedrock Agent and exploring supplier  
  insights locally.

---

## 2. High-Level Architecture

**Core flow (for a typical query):**

1. User opens the **Streamlit UI** and asks a question  
   → e.g., “What is the compliance health report for Supplier A?”

2. Streamlit calls **Amazon Bedrock Agent Runtime** → `InvokeAgent`.

3. The **Bedrock Agent** decides which **Action Group** to call:
   - `compliance` (compliance health, risk score)
   - `deduplication` (duplicate supplier detection)
   - `performance` (supplier performance metrics)

4. The selected **Lambda function** (one per action group) runs:
   - Uses shared helpers from `backend/common`  
   - Connects to **Aurora PostgreSQL (RDS)**  
   - Runs SQL queries  
   - Computes scores / aggregates  
   - Returns structured JSON back to the Agent

5. The **Agent** formats a natural language response and returns it to the **Streamlit UI**.

> Note: For the demo, the **UI is hosted locally**, while AWS resources (Bedrock, Lambda, Aurora) run in the cloud.

---

## 3. Repository Structure

```text
.
├── LICENSE
├── README.md                # (This file)
├── agent
│   ├── action-groups
│   │   ├── compliance.yaml  # Bedrock action group definition – compliance
│   │   ├── deduplication.yaml
│   │   └── performance.yaml
│   └── prompts
│       └── system_prompt.md # System prompt and instructions for the Agent
├── backend
│   ├── common
│   │   ├── __init__.py
│   │   ├── bedrock_utils.py # (If used) Shared utilities for Bedrock / parsing
│   │   └── rds_client.py    # Helper to connect to Aurora / Postgres
│   └── lambdas
│       ├── compliance
│       │   └── lambda_function.py
│       ├── deduplication
│       │   └── lambda_function.py
│       └── performance
│           └── lambda_function.py
├── db
│   ├── data
│   │   └── data.sql         # Sample / synthetic supplier data
│   └── schema
│       └── schema.sql       # Aurora / Postgres DDL (tables, indexes, etc.)
├── docs
│   └── architecture-overview.md  # High-level design & diagrams
└── frontend
    └── streamlit_app
        ├── README.md
        ├── app.py           # Streamlit UI (chat with Bedrock Agent)
        └── requirements.txt # Python dependencies for the UI
```
---
## 4. Tech Stack

### 🧠 AI & Agent Framework
- **Amazon Bedrock Agents**
- **Bedrock Agent Runtime (InvokeAgent)**
- **YAML Action Groups** mapped to Lambda functions
- **System Prompt** defining agent rules and reasoning

### 🖥️ Backend (Serverless)
- **AWS Lambda (Python 3.x)** for compliance, deduplication, and performance logic
- **Amazon Aurora PostgreSQL (RDS)** for supplier master data and scoring data
- **VPC + Private Subnets** for secure database connectivity
- **IAM Roles & Policies** enabling:
  - Lambda → RDS connectivity  
  - Bedrock Agent → Lambda invocation  
  - CloudWatch logging  

### 🗄️ Database Layer
- **Aurora PostgreSQL**
- Includes:
  - `db/schema/schema.sql` — table definitions and indexes  
  - `db/data/data.sql` — synthetic sample dataset for demo  

### 📦 Python Shared Utilities (Backend)
Located under `backend/common/`:
- `rds_client.py` — PostgreSQL database connector  
- `bedrock_utils.py` — common utilities for formatting or Bedrock operations  

### 🖼️ Frontend (Local Demo)
- **Streamlit** UI (`frontend/streamlit_app/app.py`)
- Integrates with Bedrock Agent Runtime via `boto3`
- Chat-based interface for interacting with the Supplier360 agent

### 📦 Frontend Dependencies
---
- streamlit
- boto3
- botocore
- python-dotenv
---

## 5. Prerequisites

Before running or deploying Supplier360, ensure the following setup and tools are available.

### 🔐 AWS Requirements
- Active **AWS Account**
- **Amazon Bedrock** access enabled (Agents + Runtime)
- **AWS Lambda** service available
- **Amazon Aurora PostgreSQL** cluster created
- IAM permissions allowing:
  - Bedrock Agent → invoke Lambda  
  - Lambda → connect to Aurora RDS  
  - Lambda → write logs to CloudWatch  

### 🗄️ Database Requirements
- Aurora PostgreSQL instance with:
  - Host / Endpoint  
  - Port (default: 5432)  
  - Username & Password  
  - Database name (recommended: `supplier360`)  

- Apply database schema and Load synthetic dataset:
  ```bash
  psql -h <RDS_ENDPOINT> -U <USER> -d <DB_NAME> -f db/schema/schema.sql
  psql -h <RDS_ENDPOINT> -U <USER> -d <DB_NAME> -f db/data/data.sql
  ```
  
### 🐍 Local Machine Requirements:
 -  Python 3.9 or higher
 - Package manager:
 - pip or
 - conda or
 - virtualenv
   
## 6. 🚀 Quickstart – Run Supplier360 Locally  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/gorlemahesh/Supplier360.git  
cd Supplier360  
```
### 2️⃣ Create and activate a virtual environment  

Using Python venv: 
```bash
python3 -m venv venv  
source venv/bin/activate      # macOS / Linux  
venv\Scripts\activate         # Windows PowerShell 
```
Or using Conda:  
```bash
conda create -n supplier360 python=3.10 -y  
conda activate supplier360  
```
### 3️⃣ Install frontend dependencies (Streamlit UI)  
```bash
cd frontend/streamlit_app  
pip install -r requirements.txt
```
### 4️⃣ Configure environment variables  
```
cp .env.example .env  
```
Fill in: AWS_REGION, BEDROCK_AGENT_ID, BEDROCK_AGENT_ALIAS_ID, DB_HOST, DB_USER, DB_PASSWORD, etc.  
These will be automatically loaded by the Streamlit app and backend utilities.  
### 5️⃣ Run the Streamlit App  
```
streamlit run app.py  
```
Your local demo will be available at: http://localhost:8501  
🎉 Supplier360 is now ready!


