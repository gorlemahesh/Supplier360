# Supplier360 – Deduplication Lambda

This Lambda performs fuzzy matching on supplier names to detect duplicates in supplier_master.

## Inputs
- supplier_name (string, required)

Supports:
- Direct invocation
- Bedrock Agent invocation via the /deduplication action group

## Process
- Load all suppliers from supplier_master
- Use difflib to calculate similarity
- Determine closest match
- Mark as duplicate if similarity >= 90%
