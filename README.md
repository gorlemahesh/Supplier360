# Supplier360 – AI-Powered Supplier Risk & Compliance Assistant

Supplier360 is an end-to-end **AI + AWS Bedrock–powered Supplier 360° view** that helps procurement and risk teams:

- Evaluate **supplier compliance** against internal policies  
- Detect **duplicate / overlapping suppliers**  
- Monitor **performance & risk signals** over time  

It uses **Amazon Bedrock Agents** with custom **Lambda-based action groups** and an **Aurora PostgreSQL** database, with a simple **Streamlit UI** for local demos.

---

## 1. Key Features

- 🤖 **Bedrock Agent–driven workflow**  
  Natural language questions like _“Give me the compliance health score for Supplier X”_ or  
  _“Show high-risk suppliers by region”_.

- 📊 **Compliance scoring engine**  
  Lambda functions query Aurora and compute **compliance health scores** based on rules and weights.

- 🧹 **Supplier deduplication**  
  Identify suppliers that may be duplicates (similar names, tax IDs, locations, etc).

- 📈 **Performance insights**  
  Aggregate metrics (on-time delivery, quality issues, etc.) exposed through the Agent.

- 🖥️ **Local Streamlit UI**  
  Simple chat-style UI to talk to the Bedrock Agent and view responses, perfect for demos.

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
 - Ability to run Streamlit:
 ```bash
      streamlit run app.py
 ```

