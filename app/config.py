import os
import secrets

# Application configuration settings
# Secrets should always be loaded from the environment in production.
# When running tests or in development, fall back to a randomly generated
# value so the code never contains a hardcoded constant.

SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

JWT_SECRET = os.environ.get("JWT_SECRET") or secrets.token_hex(32)

DATABASE_NAME = "securevault.db"

# Administrative password must be supplied via environment or else a random
# high-entropy string is used.  Do NOT ship the source with a predictable
# default value.
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or secrets.token_urlsafe(16)

DEBUG = True

MAX_LOGIN_ATTEMPTS = 5

TOKEN_EXPIRY_SECONDS = 3600
