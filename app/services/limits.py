from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database.mongo import get_db

db = get_db()

async def reset_daily_limits():
    db.users.update_many({}, {"$set": {"ai_count": 0, "human_count": 0}})

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(reset_daily_limits, "cron", hour=0, minute=0)
    scheduler.start()
