import os
import json
import logging
import boto3
from difflib import SequenceMatcher, get_close_matches

# ---------- Config ----------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.getLogger().setLevel(LOG_LEVEL)
log = logging.getLogger(__name__)

AURORA_ARN = os.getenv("AURORA_ARN")
SECRET_ARN = os.getenv("DB_SECRET_ARN")
DB_NAME = os.getenv("DB_NAME", "supplier360")

rds = boto3.client("rds-data")

# ---------- SQL ----------
SQL_FETCH_ALL = """
SELECT supplier_id, supplier_name
FROM supplier_master;
"""

# ---------- Helpers ----------
def _exec(sql, params=None):
    return rds.execute_statement(
        resourceArn=AURORA_ARN,
        secretArn=SECRET_ARN,
        database=DB_NAME,
        sql=sql,
        parameters=params or []
    )

def _from_bedrock_event(event):
    if isinstance(event, dict) and "apiPath" in event:
        params = event.get("parameters", [])
        pmap = {p.get("name"): p.get("value") for p in params}
        return {
            "supplier_name": pmap.get("supplier_name"),
            "_bedrock": True
        }
    return {
        "supplier_name": (event or {}).get("supplier_name"),
        "_bedrock": False
    }

def _respond_bedrock(status, body):
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": "deduplication",
            "apiPath": "/deduplication",
            "httpMethod": "GET",
            "httpStatusCode": status,
            "responseBody": {
                "application/json": {
                    "body": json.dumps(body, default=str)
                }
            }
        }
    }

# ---------- Handler ----------
def lambda_handler(event, context):
    log.info("Event: %s", json.dumps(event, default=str))

    req = _from_bedrock_event(event)
    supplier_input = (req.get("supplier_name") or "").strip()
    is_bedrock = req["_bedrock"]

    if not supplier_input:
        body = {
            "error": "supplier_name is required",
            "example": {"supplier_name": "Ford Motors"}
        }
        return _respond_bedrock(400, body) if is_bedrock else body

    try:
        # 1) Fetch supplier list
        resp = _exec(SQL_FETCH_ALL)
        records = resp.get("records", [])

        supplier_list = []
        id_map = {}

        for r in records:
            sid = r[0]["stringValue"]
            sname = r[1]["stringValue"]
            supplier_list.append(sname)
            id_map[sname] = sid

        if not supplier_list:
            body = {"message": "No suppliers found in the database."}
            return _respond_bedrock(200, body) if is_bedrock else body

        # 2) Fuzzy matching using built-in difflib
        matches = get_close_matches(supplier_input, supplier_list, n=1, cutoff=0.5)

        if matches:
            best_match = matches[0]
            similarity = int(SequenceMatcher(None, supplier_input, best_match).ratio() * 100)
        else:
            best_match = None
            similarity = 0

        is_duplicate = similarity >= 90

        result = {
            "input_supplier": supplier_input,
            "is_duplicate": is_duplicate,
            "matched_supplier": best_match if is_duplicate else None,
            "matched_supplier_id": id_map.get(best_match) if is_duplicate else None,
            "similarity_score": similarity,
            "message": (
                f"Potential duplicate found: '{best_match}' ({similarity}% match)"
                if is_duplicate
                else "No duplicate supplier found."
            ),
            "mode": "aurora"
        }

        return _respond_bedrock(200, result) if is_bedrock else result

    except Exception as e:
        log.exception("Error in Duplicate Detection Lambda")
        body = {"error": "InternalError", "detail": str(e)}
        return _respond_bedrock(500, body) if is_bedrock else body
