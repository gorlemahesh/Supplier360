"""
Common Aurora RDS Data API helper for Supplier360.

This module centralizes the RDS Data API client and simple helper functions
so Lambdas can reuse the same pattern.
"""

import os
import boto3
from typing import Any, Dict, List, Optional

AURORA_ARN = os.getenv("AURORA_ARN")
SECRET_ARN = os.getenv("DB_SECRET_ARN")
DB_NAME = os.getenv("DB_NAME", "supplier360")

rds = boto3.client("rds-data")


def make_param(name: str, value: Any) -> Dict[str, Any]:
    """
    Create a simple string parameter for the Data API.
    Extend this if you need other types (long, bool, double, etc.).
    """
    return {
        "name": name,
        "value": {
            "stringValue": "" if value is None else str(value)
        },
    }


def exec_sql(
    sql: str,
    params: Optional[List[Dict[str, Any]]] = None,
    database: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute a SQL statement against Aurora using the Data API.
    """
    return rds.execute_statement(
        resourceArn=AURORA_ARN,
        secretArn=SECRET_ARN,
        database=database or DB_NAME,
        sql=sql,
        parameters=params or [],
    )
