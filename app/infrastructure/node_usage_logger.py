import requests
from app.core.logging import logger
from app.core.config import settings

# Wait, let's verify where usage-log is. 
# For now, I'll update it to be consistent if it's ever used.
NODE_USAGE_URL = f"{settings.NODE_API_URL}/api/documents/internal/usage-log"

# def log_usage_to_node(org_id: str, usage_type: str, count: int, meta: dict = None):
#     payload = {
#         "orgId": org_id,
#         "type": usage_type,
#         "count": count,
#         "meta": meta or {}
#     }

#     try:
#         res = requests.post(NODE_USAGE_URL, json=payload, timeout=3)
#         if res.status_code != 200:
#             logger.error(f"⚠ Node usage logging failed: {res.text}")
#     except Exception as e:
#         logger.error(f"⚠ Could not send usage log to Node: {e}")
