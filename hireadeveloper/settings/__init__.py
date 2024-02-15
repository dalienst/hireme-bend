from decouple import config

from .base import *  # noqa F403, F401

env = config("ENV_NAME", "local")

if env == "Production":
    from .production import *  # noqa F403, F401

elif env == "Staging":
    from .staging import *  # noqa F403, F401

else:
    from .local import *  # noqa F403, F401
