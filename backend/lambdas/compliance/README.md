# Supplier360 – Compliance Lambda

This Lambda calculates a supplier's certification compliance score using required certificates and latest certificate records from Aurora.

## Inputs
- supplier_id (string) or
- supplier_name (string)
(At least one required)

Supports:
- Direct invocation
- Bedrock Agent invocation via the /compliance action group

## Process
- Resolve supplier and industry
- Fetch required certificates for industry
- Fetch latest certificate per type
- Compute:
  - Breakdown: Valid, Expired, Missing, Pending
  - Issues list
  - Compliance score
  - Summary text
