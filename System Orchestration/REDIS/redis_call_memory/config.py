import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

CALL_MEMORY_TTL_SECONDS = int(os.getenv("CALL_MEMORY_TTL_SECONDS", "86400"))
RECENT_MESSAGE_COUNT = int(os.getenv("RECENT_MESSAGE_COUNT", "10"))
