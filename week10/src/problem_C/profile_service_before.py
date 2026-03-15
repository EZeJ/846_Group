# profile_service.py

def get_user_profile(user_id, db):
    return db.load_profile(user_id)

def update_user_profile(user_id, new_data, db):
    db.save_profile(user_id, new_data)
    return {"status": "ok"}
