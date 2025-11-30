"""
Common backend utilities for Supplier360.

Currently exposes:
- RDS Data API helpers (exec_sql, make_param)
- Bedrock Agent helpers (from_bedrock_event, bedrock_response)
"""

from .rds_client import exec_sql, make_param
from .bedrock_utils import from_bedrock_event, bedrock_response

__all__ = [
    "exec_sql",
    "make_param",
    "from_bedrock_event",
    "bedrock_response",
]
