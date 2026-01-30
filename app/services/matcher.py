import time
from app.database.mongo import get_db

db = get_db()

def add_to_queue(user):
    db.waiting.update_one(
        {"user_id": user["user_id"]},
        {"$set": {
            "user_id": user["user_id"],
            "gender": user["gender"],
            "preference": user.get("preference", "random"),
            "joined_at": time.time()
        }},
        upsert=True
    )

def remove_from_queue(user_id):
    db.waiting.delete_one({"user_id": user_id})

def find_match(user):
    queue = list(db.waiting.find({"user_id": {"$ne": user["user_id"]}}))

    for partner in queue:
        # preference filter
        if user.get("preference") != "random":
            if partner["gender"] != user["preference"]:
                continue

        # partner preference
        partner_user = db.users.find_one({"user_id": partner["user_id"]})
        if partner_user.get("preference") != "random":
            if user["gender"] != partner_user["preference"]:
                continue

        return partner

    return None
