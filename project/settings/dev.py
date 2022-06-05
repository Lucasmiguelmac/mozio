from typing import List

from project.settings.base import *

INSTALLED_APPS: List[str] = INSTALLED_APPS + ["django_extensions"]
CORS_ALLOW_ALL_ORIGINS = True
