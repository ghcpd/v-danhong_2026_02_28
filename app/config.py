import os
import secrets

# Application configuration settings
# Secrets should never be hardcoded in source control. Load from environment
# variables in production and fall back to a secure random value if not set.

SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_urlsafe(32)
JWT_SECRET = os.environ.get("JWT_SECRET") or secrets.token_urlsafe(32)

DATABASE_NAME = os.environ.get("DATABASE_NAME") or "securevault.db"

# ADMIN_PASSWORD should be set via an environment variable in production.
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or secrets.token_urlsafe(16)

DEBUG = os.environ.get("DEBUG", "True").lower() in ("1", "true", "yes")

MAX_LOGIN_ATTEMPTS = int(os.environ.get("MAX_LOGIN_ATTEMPTS", "5"))

TOKEN_EXPIRY_SECONDS = int(os.environ.get("TOKEN_EXPIRY_SECONDS", "3600"))
