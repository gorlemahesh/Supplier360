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
SQL_SUPPLIER = """
SELECT supplier_id, supplier_name, industry
FROM supplier_master
WHERE (supplier_id = :sid) OR (LOWER(supplier_name) = LOWER(:sname))
LIMIT 1;
"""

SQL_REQUIRED = """
SELECT required_certificate_type
FROM required_certificates_master
WHERE industry = :industry
ORDER BY required_certificate_type;
"""

SQL_LATEST_CERTS = """
WITH ranked AS (
  SELECT
    certificate_type,
    certificate_number,
    issuing_body,
    issue_date,
    expiry_date,
    valid_status,
    ROW_NUMBER() OVER (
      PARTITION BY certificate_type
      ORDER BY COALESCE(expiry_date, DATE '9999-12-31') DESC,
               issue_date DESC
    ) rn
  FROM compliance_certificates
  WHERE supplier_id = :sid
)
SELECT certificate_type,
       certificate_number,
       issuing_body,
       issue_date,
       expiry_date,
       valid_status
FROM ranked
WHERE rn = 1;
"""

# ---------- Helpers ----------
def _param(name, value):
    return {
        "name": name,
        "value": {
            "stringValue": value if value is not None else ""
        }
    }

def _exec(sql, params):
    return rds.execute_statement(
        resourceArn=AURORA_ARN,
        secretArn=SECRET_ARN,
        database=DB_NAME,
        sql=sql,
        parameters=params
    )

def _score(required, latest):
    """
    Simple scoring:
      - Each required cert has equal weight.
      - Valid   => full weight
      - Pending => half weight
      - Missing / Expired / other => 0
    """
    breakdown = {"Valid": [], "Expired": [], "Missing": [], "Pending": []}
    issues = []
    n = max(1, len(required))
    per = 100 / n
    total = 0.0

    for req in required:
        info = latest.get(req)
        if not info:
            breakdown["Missing"].append(req)
            issues.append({"type": "Missing", "detail": f"{req} is missing"})
            continue

        status = (info.get("valid_status") or "").strip()
        if status == "Valid":
            breakdown["Valid"].append(req)
            total += per
        elif status == "Pending":
            breakdown["Pending"].append(req)
            total += 0.5 * per
            issues.append({"type": "Pending", "detail": f"{req} is pending"})
        else:
            breakdown["Expired"].append(req)
            detail = f"{req} {status.lower() or 'non-compliant'}"
            if info.get("expiry_date"):
                detail += f" (expiry {info['expiry_date']})"
            issues.append({"type": status or "NonCompliant", "detail": detail})

    score = round(total)
    if not breakdown["Expired"] and not breakdown["Missing"] and not breakdown["Pending"]:
        summary = f"Fully compliant: {n}/{n} required certificates valid"
    else:
        summary = (
            f"Mixed: {len(breakdown['Valid'])} valid, "
            f"{len(breakdown['Expired'])} expired, "
            f"{len(breakdown['Missing'])} missing, "
            f"{len(breakdown['Pending'])} pending"
        )

    return breakdown, issues, int(score), summary

# ---------- Bedrock helpers ----------
def _from_bedrock_event(event):
    """
    If invoked by Bedrock Agent action group, event will have:
    {
      "apiPath": "/compliance",
      "parameters": [
        {"name": "supplier_id", "value": "..."},
        {"name": "supplier_name", "value": "..."}
      ],
      ...
    }
    """
    if isinstance(event, dict) and "apiPath" in event:
        params = event.get("parameters", [])
        pmap = {p.get("name"): p.get("value") for p in params}
        return {
            "supplier_id": pmap.get("supplier_id"),
            "supplier_name": pmap.get("supplier_name"),
            "_bedrock": True
        }
    # direct invocation
    return {
        "supplier_id": (event or {}).get("supplier_id"),
        "supplier_name": (event or {}).get("supplier_name"),
        "_bedrock": False
    }

def _respond_bedrock(status, body):
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": "compliance",   # must match your Action Group name
            "apiPath": "/compliance",
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
    supplier_id = req["supplier_id"]
    supplier_name = req["supplier_name"]
    is_bedrock = req["_bedrock"]

    if not supplier_id and not supplier_name:
        body = {
            "error": "Provide supplier_id or supplier_name",
            "example": {
                "by_id": {"supplier_id": "7F9K3A2B"},
                "by_name": {"supplier_name": "Ford Motor Company"}
            }
        }
        return _respond_bedrock(400, body) if is_bedrock else body

    try:
        # 1) Supplier lookup
        sresp = _exec(SQL_SUPPLIER, [
            _param("sid", supplier_id or ""),
            _param("sname", supplier_name or "")
        ])

        if not sresp.get("records"):
            body = {
                "error": "Supplier not found",
                "input": {
                    "supplier_id": supplier_id,
                    "supplier_name": supplier_name
                }
            }
            return _respond_bedrock(404, body) if is_bedrock else body

        row = sresp["records"][0]
        sid      = row[0]["stringValue"]
        sname    = row[1]["stringValue"]
        industry = row[2]["stringValue"]

        # 2) Required certs for this industry
        rresp = _exec(SQL_REQUIRED, [_param("industry", industry)])
        required = [rec[0]["stringValue"] for rec in rresp.get("records", [])]

        # 3) Latest cert per type
        cresp = _exec(SQL_LATEST_CERTS, [_param("sid", sid)])
        latest = {}
        for r in cresp.get("records", []):
            ctype = r[0]["stringValue"]
            latest[ctype] = {
                "certificate_number": r[1]["stringValue"],
                "issuing_body":       r[2]["stringValue"],
                "issue_date":         r[3]["stringValue"],
                "expiry_date":        r[4].get("stringValue") if r[4] else None,
                "valid_status":       r[5]["stringValue"]
            }

        breakdown, issues, score, summary = _score(required, latest)

        body = {
            "supplier_id": sid,
            "supplier_name": sname,
            "industry": industry,
            "required_set": required,
            "status_breakdown": breakdown,
            "issues": issues,
            "compliance_score": score,
            "summary": summary,
            "mode": "aurora"
        }

        return _respond_bedrock(200, body) if is_bedrock else body

    except Exception as e:
        log.exception("Error in Lambda2")
        body = {"error": "InternalError", "detail": str(e)}
        return _respond_bedrock(500, body) if is_bedrock else body
