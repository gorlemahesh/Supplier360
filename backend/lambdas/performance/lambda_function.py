import os
import json
import logging
import boto3

# ---------- Config ----------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.getLogger().setLevel(LOG_LEVEL)
log = logging.getLogger(__name__)

AURORA_ARN = os.getenv("AURORA_ARN")
SECRET_ARN = os.getenv("DB_SECRET_ARN")
DB_NAME = os.getenv("DB_NAME", "supplier360")

rds = boto3.client("rds-data")

# ---------- SQL ----------
SQL_SUPPLIER_HISTORY = """
SELECT
    on_time,
    delivery_delay_days,
    quality_compliance_pct,
    invoice_match_pct,
    incidents,
    notes
FROM supplier_performance_history
WHERE supplier_id = :sid;
"""

SQL_SUPPLIER_LOOKUP = """
SELECT supplier_id, supplier_name
FROM supplier_master
WHERE LOWER(supplier_name) = LOWER(:sname)
LIMIT 1;
"""

# ---------- Helpers ----------
def _param(name, value):
    return {"name": name, "value": {"stringValue": str(value) if value else ""}}

def _exec(sql, params):
    return rds.execute_statement(
        resourceArn=AURORA_ARN,
        secretArn=SECRET_ARN,
        database=DB_NAME,
        sql=sql,
        parameters=params
    )

# ---------- Bedrock Helpers ----------
def _from_bedrock_event(event):
    """
    Parse Bedrock Agent event format.
    """
    if isinstance(event, dict) and "apiPath" in event:
        params = event.get("parameters", [])
        pmap = {p["name"]: p["value"] for p in params}
        return {
            "supplier_name": pmap.get("supplier_name"),
            "_bedrock": True
        }
    # Direct invoke
    return {
        "supplier_name": (event or {}).get("supplier_name"),
        "_bedrock": False
    }

def _respond_bedrock(status, body):
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": "performance",
            "apiPath": "/performance",
            "httpMethod": "GET",
            "httpStatusCode": status,
            "responseBody": {
                "application/json": {
                    "body": json.dumps(body, default=str)
                }
            }
        }
    }

# ---------- Scoring ----------
def compute_scores(rows):
    if not rows:
        return {
            "delivery_score": 0,
            "quality_score": 0,
            "invoice_score": 0,
            "performance_score": 0,
            "notes": ["No performance records found"]
        }

    delivery_scores, quality_scores, invoice_scores, notes_list = [], [], [], []

    for r in rows:
        on_time = r[0].get("booleanValue") if r[0] else None
        delay_days = int(r[1].get("longValue", 0)) if r[1] else 0

        quality_pct = float(r[2].get("doubleValue") or r[2].get("stringValue"))
        invoice_pct = float(r[3].get("doubleValue") or r[3].get("stringValue"))

        incidents = int(r[4].get("longValue", 0)) if r[4] else 0
        notes = r[5]["stringValue"] if r[5] else ""
        if notes:
            notes_list.append(notes)

        # Delivery
        if on_time:
            delivery_scores.append(100)
        else:
            penalty = min(delay_days * 5, 100)
            delivery_scores.append(max(0, 100 - penalty))

        quality_scores.append(quality_pct)
        invoice_scores.append(invoice_pct)

    avg_del = sum(delivery_scores) / len(delivery_scores)
    avg_qual = sum(quality_scores) / len(quality_scores)
    avg_inv = sum(invoice_scores) / len(invoice_scores)

    final = avg_del * 0.40 + avg_qual * 0.35 + avg_inv * 0.25

    return {
        "delivery_score": round(avg_del, 2),
        "quality_score": round(avg_qual, 2),
        "invoice_score": round(avg_inv, 2),
        "performance_score": round(final, 2),
        "notes": notes_list
    }

# ---------- Handler ----------
def lambda_handler(event, context):
    log.info("Event: %s", json.dumps(event, default=str))

    req = _from_bedrock_event(event)
    supplier_name = req["supplier_name"]
    is_bedrock = req["_bedrock"]

    if not supplier_name:
        body = {"error": "supplier_name is required"}
        return _respond_bedrock(400, body) if is_bedrock else body

    try:
        # Resolve supplier ID using supplier_name
        lookup = _exec(SQL_SUPPLIER_LOOKUP, [
            _param("sname", supplier_name)
        ])

        if not lookup.get("records"):
            body = {"error": "Supplier not found", "input": supplier_name}
            return _respond_bedrock(404, body) if is_bedrock else body

        row = lookup["records"][0]
        supplier_id = row[0]["stringValue"]
        supplier_name = row[1]["stringValue"]

        # Fetch performance history
        perf = _exec(SQL_SUPPLIER_HISTORY, [_param("sid", supplier_id)])
        rows = perf.get("records", [])

        result = compute_scores(rows)

        body = {
            "supplier_name": supplier_name,
            "supplier_id": supplier_id,
            "delivery_score": result["delivery_score"],
            "quality_score": result["quality_score"],
            "invoice_score": result["invoice_score"],
            "performance_score": result["performance_score"],
            "notes": result["notes"],
            "mode": "performance_scoring"
        }

        return _respond_bedrock(200, body) if is_bedrock else body

    except Exception as e:
        log.exception("Performance Lambda Error")
        body = {"error": str(e)}
        return _respond_bedrock(500, body) if is_bedrock else body
