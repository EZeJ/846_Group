import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class UserProfile:
    user_id: str
    email: str
    phone_number: str
    date_of_birth: str      # format: YYYY-MM-DD
    shipping_address: str
    full_name: str


# Simulated database
_USER_DB: dict[str, UserProfile] = {
    "usr_001": UserProfile(
        user_id="usr_001",
        email="alice@example.com",
        phone_number="+1-416-555-0192",
        date_of_birth="1990-03-15",
        shipping_address="123 King St W, Toronto, ON M5H 1J9",
        full_name="Alice Dupont",
    ),
    "usr_002": UserProfile(
        user_id="usr_002",
        email="bob@example.com",
        phone_number="+1-604-555-0174",
        date_of_birth="1985-07-22",
        shipping_address="456 Granville St, Vancouver, BC V6C 1T2",
        full_name="Bob Martin",
    ),
}


def get_user_profile(user_id: str) -> Optional[UserProfile]:
    return _USER_DB.get(user_id)


def save_user_profile(profile: UserProfile) -> bool:
    """Persist updated profile. Returns True on success."""
    _USER_DB[profile.user_id] = profile
    return True


def validate_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[-1]


def validate_phone(phone: str) -> bool:
    digits = phone.replace("+", "").replace("-", "").replace(" ", "")
    return digits.isdigit() and 7 <= len(digits) <= 15


def update_user_profile(
    user_id: str,
    email: str,
    phone_number: str,
    date_of_birth: str,
    shipping_address: str,
) -> dict:
    """
    Update an existing user's profile fields.

    Args:
        user_id:          Internal user identifier.
        email:            New email address.
        phone_number:     New phone number (E.164 or local format).
        date_of_birth:    Date of birth in YYYY-MM-DD format.
        shipping_address: Full mailing address.

    Returns:
        dict with keys: success (bool), error (str or None)
    """
    profile = get_user_profile(user_id)
    if profile is None:
        return {"success": False, "error": "user_not_found"}

    if not validate_email(email):
        return {"success": False, "error": "invalid_email"}

    if not validate_phone(phone_number):
        return {"success": False, "error": "invalid_phone"}

    profile.email = email
    profile.phone_number = phone_number
    profile.date_of_birth = date_of_birth
    profile.shipping_address = shipping_address

    saved = save_user_profile(profile)
    if not saved:
        return {"success": False, "error": "db_write_failed"}

    return {"success": True, "error": None}
