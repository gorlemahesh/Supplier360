"""
Common Amazon Bedrock Agent helpers for Supplier360.

These utilities can be used by Lambdas that are invoked as Bedrock
Agent action group handlers.
"""

import json
from typing import Any, Dict, List, Tuple


def from_bedrock_event(
    event: Dict[str, Any],
    expected_params: List[str],
) -> Tuple[Dict[str, Any], bool]:
    """
    Normalize event input for Lambdas that may be called either:
    - directly (plain JSON), or
    - via Bedrock Agent action groups.

    Returns:
      (normalized_payload, is_bedrock_event)
    """
    if isinstance(event, dict) and "apiPath" in event:
        params = event.get("parameters", [])
        pmap = {p.get("name"): p.get("value") for p in params}
        payload = {key: pmap.get(key) for key in expected_params}
        payload["_raw"] = event
        return payload, True

    payload = {key: (event or {}).get(key) for key in expected_params}
    payload["_raw"] = event
    return payload, False


def bedrock_response(
    action_group: str,
    api_path: str,
    status_code: int,
    body: Dict[str, Any],
    http_method: str = "GET",
) -> Dict[str, Any]:
    """
    Build a standard Bedrock Agent response wrapper.
    """
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": action_group,
            "apiPath": api_path,
            "httpMethod": http_method,
            "httpStatusCode": status_code,
            "responseBody": {
                "application/json": {
                    "body": json.dumps(body, default=str)
                }
            },
        },
    }
