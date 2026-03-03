import os

# Application configuration settings

# Load secrets from environment variables - never hardcode secrets
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set")

JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable must be set")

DATABASE_NAME = "securevault.db"

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
if not ADMIN_PASSWORD:
    raise ValueError("ADMIN_PASSWORD environment variable must be set")

DEBUG = True

MAX_LOGIN_ATTEMPTS = 5

TOKEN_EXPIRY_SECONDS = 3600
