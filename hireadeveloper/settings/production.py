from hireadeveloper.settings.base import ALLOWED_HOSTS
from decouple import config


ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")]
)

DEBUG = True
