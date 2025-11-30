# Supplier360 – Performance Lambda

This Lambda computes delivery, quality, invoice, and final weighted performance scores for a supplier using Aurora data.

## Inputs
- supplier_name (string, required)

Supports:
- Direct invocation
- Bedrock Agent invocation via the /performance action group

## Process
- Resolve supplier_id from supplier_name
- Fetch performance history from supplier_performance_history
- Compute:
  - Delivery Score
  - Quality Score
  - Invoice Score
- Compute final weighted performance_score
- Return scores and aggregated notes
