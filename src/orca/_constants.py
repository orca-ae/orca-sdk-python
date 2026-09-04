import httpx2

RAW_RESPONSE_HEADER = "X-Orca-Raw-Response"
OVERRIDE_CAST_TO_HEADER = "____orca_override_cast_to"

CLOUD_EXTENSION_GROUP = "cloud.sn.io"
POLICY_EXTENSION_GROUP = "policy.runorca.ai"
PRICING_EXTENSION_GROUP = "pricing.runorca.ai"

# default timeout is 10 minutes
DEFAULT_TIMEOUT = httpx2.Timeout(timeout=10 * 60, connect=5.0)
DEFAULT_MAX_RETRIES = 2
DEFAULT_CONNECTION_LIMITS = httpx2.Limits(max_connections=1000, max_keepalive_connections=100)

INITIAL_RETRY_DELAY = 0.5
MAX_RETRY_DELAY = 8.0
