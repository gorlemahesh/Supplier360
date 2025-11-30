# Supplier360 – Database Layer

This folder contains the complete database schema and sample dataset used by the Supplier360 system.  
The database is designed for AWS Aurora PostgreSQL and supports three Lambda microservices:

- Deduplication  
- Compliance Scoring  
- Performance Scoring  


---

## 1. Schema File

### `schema/schema.sql`

This file contains all CREATE TABLE statements for the Supplier360 platform, including:

- supplier_master  
- required_certificates_master  
- compliance_certificates  
- supplier_performance_history  

These tables form the core backend used by:

- Deduplication Lambda  
- Compliance Scoring Lambda  
- Performance Scoring Lambda  

The schema is ordered so it can be executed top-to-bottom with no dependency issues.

---

## 2. Data File

### `data/data.sql`

This file contains the full synthetic dataset used by the Supplier360 system for:

- supplier deduplication  
- compliance scoring  
- performance scoring  

It includes:

- Suppliers across multiple industries  
- Industry-level certificate requirements  
- Detailed compliance certificate records  
- Historical performance data  

The dataset includes realistic scenarios such as:

- expired certificates  
- pending certifications  
- missing requirements  
- delivery delays  
- quality deviations  

---

## Notes

- Run `schema.sql` before inserting any data.  
- All values and IDs are synthetic and created for demonstration purposes.

---

## Status

This database folder is complete and fully compatible with:

- AWS Lambda microservices  
- Bedrock Agent action groups  
- Supplier360 Streamlit UI  

