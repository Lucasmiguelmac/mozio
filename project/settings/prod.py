import os

from project.settings.base import *

cors_allowed_origins: str = os.environ.get("CORS_ALLOWED_ORIGINS") or ""

STATIC_ROOT = os.environ.get("STATIC_ROOT")
CORS_ALLOWED_ORIGINS = [i for i in cors_allowed_origins.split(",")]
