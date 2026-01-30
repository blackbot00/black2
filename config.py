import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split(",")))

GROUP1_LOG_ID = int(os.getenv("GROUP1_LOG_ID"))
GROUP2_LOG_ID = int(os.getenv("GROUP2_LOG_ID"))

CASHFREE_APP_ID = os.getenv("CASHFREE_APP_ID")
CASHFREE_SECRET_KEY = os.getenv("CASHFREE_SECRET_KEY")
CASHFREE_ENV = os.getenv("CASHFREE_ENV")
CASHFREE_WEBHOOK_SECRET = os.getenv("CASHFREE_WEBHOOK_SECRET")

AI_ENABLED = os.getenv("AI_ENABLED") == "true"
