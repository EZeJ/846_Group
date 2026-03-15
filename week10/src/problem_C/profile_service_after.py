# profile_service.py

CACHE = {}

def get_user_profile(user_id, db):
    if user_id in CACHE:
        return CACHE[user_id]

    profile = db.load_profile(user_id)
    CACHE[user_id] = profile
    return profile

def update_user_profile(user_id, new_data, db):
    db.save_profile(user_id, new_data)
    return {"status": "ok"}
