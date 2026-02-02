import os
from os import environ

# This file is for backward compatibility with the provided scripts
# Import everything from config
from config import *

# Additional backward compatibility
SUPPORT_CHAT = environ.get("SUPPORT_CHAT", "")
