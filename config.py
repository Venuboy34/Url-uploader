import os
from os import environ

# Bot Configuration
API_ID = int(environ.get("API_ID", ""))
API_HASH = environ.get("API_HASH", "")
BOT_TOKEN = environ.get("BOT_TOKEN", "")

# Database
DATABASE_URI = environ.get("DATABASE_URI", "")
DATABASE_NAME = environ.get("DATABASE_NAME", "UrlUploaderBot")

# Channels & Groups
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", ""))
SUPPORT_CHAT = environ.get("SUPPORT_CHAT", "")
FORCE_SUB_CHANNEL = environ.get("FORCE_SUB_CHANNEL", "")
FORCE_SUB_CHANNEL2 = environ.get("FORCE_SUB_CHANNEL2", "")

# Admin & Owner
ADMINS = [int(admin) if admin.strip().isdigit() else admin.strip() for admin in environ.get('ADMINS', '').split()]
OWNER_ID = int(environ.get("OWNER_ID", ""))

# Premium Logs
PREMIUM_LOGS = int(environ.get("PREMIUM_LOGS", LOG_CHANNEL))

# Bot Settings
WORKERS = int(environ.get("WORKERS", "500"))
MAX_CONCURRENT = int(environ.get("MAX_CONCURRENT", "500"))

# File Size Limits (in GB)
FREE_USER_LIMIT = int(environ.get("FREE_USER_LIMIT", "2"))  # 2GB
PREMIUM_USER_LIMIT = int(environ.get("PREMIUM_USER_LIMIT", "4"))  # 4GB

# Download/Upload Speed (MB/s)
MAX_SPEED = int(environ.get("MAX_SPEED", "50"))  # 50 MB/s

# Welcome Images
WELCOME_IMAGE = "https://i.ibb.co/pr2H8cwT/img-8312532076.jpg"
RANDOM_IMAGE_API = "https://api.aniwallpaper.workers.dev/random?type=girl"

# Welcome Sticker
WELCOME_STICKER = "CAACAgIAAxkBAAEQZtFpgEdROhGouBVFD3e0K-YjmVHwsgACtCMAAphLKUjeub7NKlvk2TgE"

# Subscription Image
SUBSCRIPTION = environ.get("SUBSCRIPTION", "https://graph.org/file/86da2027469565b5873d6.jpg")

# Developer
DEVELOPER = "@Venuboyy"

# Star Premium Plans (amount: duration)
STAR_PREMIUM_PLANS = {
    50: "7 days",
    100: "1 month",
    200: "2 months",
    500: "6 months",
    1000: "1 year"
}

# Progress Bar
PROGRESS_BAR = "░░░░░░░░░░░░░░░░░░░░"
