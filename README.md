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

4. Tech Stack

Cloud & Backend

Amazon Bedrock (Agents + model invocation)

AWS Lambda (Python)

Amazon Aurora PostgreSQL (RDS)

IAM (permissions for Bedrock & Lambda to talk to RDS)

Frontend

Streamlit (local demo UI)

Python Packages (frontend)

streamlit

boto3

botocore

python-dotenv

requests


5. Prerequisites

AWS Account with:

Bedrock access (agent + runtime)

Lambda

RDS (Aurora PostgreSQL)

Python 3.9+ (local)

pip / conda for package management

6. Setup & Installation
6.1. Clone the repository
git clone https://github.com/<your-org>/Supplier360.git
cd Supplier360

6.2. Database (Aurora PostgreSQL)

Create an Aurora PostgreSQL cluster in AWS.

Note the:

Host / endpoint

Port

Database name

Username / password

Apply the schema:

psql -h <RDS_ENDPOINT> -p <PORT> -U <USER> -d <DB_NAME> -f db/schema/schema.sql


Load the sample data:

psql -h <RDS_ENDPOINT> -p <PORT> -U <USER> -d <DB_NAME> -f db/data/data.sql


The sample data is synthetic, designed to look like realistic supplier data for an academic/demo project.

6.3. Backend – Lambda Functions

For each Lambda under backend/lambdas:

compliance/lambda_function.py

deduplication/lambda_function.py

performance/lambda_function.py

You can deploy them using the AWS Console or your preferred IaC (CloudFormation / CDK / Terraform).

Typical configuration:

Runtime: Python 3.x

Environment variables (example – adjust to your code):

DB_HOST – Aurora endpoint

DB_PORT – Aurora port

DB_NAME – Database name

DB_USER – DB user

DB_PASSWORD – DB password

Permissions:

Lambda must be able to:

Connect to RDS (VPC + Security Group)

Be invoked by Bedrock Agent Action Groups

6.4. Bedrock Agent & Action Groups

In the Bedrock console, create a new Agent (e.g., Supplier360Agent).

Configure:

System prompt → from agent/prompts/system_prompt.md

Add Action Groups:

compliance → attach agent/action-groups/compliance.yaml

deduplication → attach agent/action-groups/deduplication.yaml

performance → attach agent/action-groups/performance.yaml

For each action group, map the Lambda you deployed.

Create an Agent Alias (e.g., demo) and note:

Agent ID

Agent Alias ID

You will use these values in the Streamlit app.

6.5. Frontend – Streamlit UI (local)
cd frontend/streamlit_app
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt


Create a .env file in frontend/streamlit_app:

AWS_REGION=us-east-1
BEDROCK_AGENT_ID=<your-agent-id>
BEDROCK_AGENT_ALIAS_ID=<your-agent-alias-id>


(If your app needs AWS credentials locally, configure them via aws configure or environment variables.)

Run the app:

streamlit run app.py


