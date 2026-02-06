import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Application Configuration
APP_TITLE = "Todo Full-Stack Web Application API"
APP_DESCRIPTION = "REST API for todo management application with JWT authentication"
APP_VERSION = "1.0.0"

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Better Auth Configuration
BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "")

# API Prefix
API_PREFIX = "/api"

# Backup Configuration
BACKUP_DIR_PATH = os.getenv("BACKUP_DIR_PATH", "./backups")