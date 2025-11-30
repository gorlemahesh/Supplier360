# Supplier360 – Amazon Bedrock Agent

This folder contains the configuration used to build the Supplier360 Orchestrator Agent in Amazon Bedrock.  
The agent coordinates three Lambda-backed action groups to generate a complete supplier risk profile using only system-verified data from Aurora PostgreSQL.

The agent never invents or infers information. All responses are generated strictly from the outputs of the Deduplication, Compliance, and Performance action groups.

The agent is designed to orchestrate the following workflow:

1. Data Integrity (Deduplication)
2. Certification (Compliance)
3. Operational Performance (Performance)
4. Final Risk Report Assembly

All components required to reconstruct the Bedrock Agent are located in this directory.

---

## Action Groups Overview

The agent uses three OpenAPI-defined action groups.  
Each action group is a separate Lambda function that fetches data from Aurora.

### 1. Deduplication (Data Integrity Check)
**OpenAPI file:** `action-groups/deduplication.yaml`  
**Lambda:** `Supplier360-Deduplication`  
**Purpose:**  
Performs fuzzy matching on supplier_name to detect duplicates in the `supplier_master` table.

**Key Output Fields:**
- input_supplier  
- is_duplicate  
- matched_supplier  
- matched_supplier_id  
- similarity_score  
- message  

Used as the first step in the agent pipeline to identify the correct canonical supplier identity.

---

### 2. Compliance (Certification Step)
**OpenAPI file:** `action-groups/compliance.yaml`  
**Lambda:** `Supplier360-Compliance`  
**Purpose:**  
Returns the supplier’s compliance score, certificate breakdown (valid, expired, missing, pending), and industry-mapped required certificates.

**Key Output Fields:**
- supplier_id  
- supplier_name  
- industry  
- required_set  
- status_breakdown  
- issues  
- compliance_score  
- summary  

This is the second step in the agent pipeline.

---

### 3. Performance (Operational Step)
**OpenAPI file:** `action-groups/performance.yaml`  
**Lambda:** `Supplier360-Performance`  
**Purpose:**  
Computes delivery, quality, invoice, and weighted performance scores from the `supplier_performance_history` table.

**Key Output Fields:**
- supplier_id  
- supplier_name  
- delivery_score  
- quality_score  
- invoice_score  
- performance_score  
- notes  

This is the third step in the agent pipeline.

---

## System Prompt

**File:** `prompts/system_prompt.md`

The system prompt defines:

- The agent’s orchestration rules  
- Mandatory action group call order  
  1. Deduplication → Data Integrity Score  
  2. Compliance → Certification Score  
  3. Performance → Operational Score  
- The mandatory seven-section final report format  
- Weighted Trust Score formula  
- Markdown table layout requirements  
- Paragraph spacing rules  
- Plain-text only styling constraints  
- Approved helpful link categories  
- Strict prohibition on hallucination or invented data  

The prompt ensures that the agent outputs a structured, repeatable, and audit-ready supplier risk report.

---

## End-to-End Workflow Summary

1. User provides a `supplier_name`.
2. Agent calls **Deduplication**:
   - Finds correct supplier identity.
   - Returns Data Integrity Score.
3. Agent feeds canonical supplier name into **Compliance**:
   - Returns certification compliance score and breakdown.
4. Agent feeds same name into **Performance**:
   - Returns operational performance score.
5. Agent computes the **Trust Score**:
