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

