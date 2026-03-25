# Add these at the top of your settings.py
import os
from decouple import config
from urllib.parse import urlparse, parse_qsl

# Replace the DATABASES section of your settings.py with this
tmpPostgres = config("DATABASE_URL")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": tmpPostgres.path.replace("/", ""),
        "USER": tmpPostgres.username,
        "PASSWORD": tmpPostgres.password,
        "HOST": tmpPostgres.hostname,
        "PORT": 5432,
        "OPTIONS": dict(parse_qsl(tmpPostgres.query)),
    }
}
