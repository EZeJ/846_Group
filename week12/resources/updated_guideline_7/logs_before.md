User: I have /Users/sofiiatkach/Desktop/LLM/846_Group/week12/resources/user_profile_service.py. Add logging to the update_user_profile function.

Requirements:
- Include relevant runtime context such as input parameters, output results,
  and key intermediate states
- Logs should help debug failures and understand execution flow

GitHub Copilot: Read [](file:///Users/sofiiatkach/Desktop/LLM/846_Group/week12/resources/user_profile_service.py#1-1), lines 1 to 50

Read [](file:///Users/sofiiatkach/Desktop/LLM/846_Group/week12/resources/user_profile_service.py#51-51), lines 51 to 98

Using "Edit File"

Using ""


````

````
I have added logging to the `update_user_profile` function to capture input parameters, intermediate states, and results. Let me know if you need further modifications or additional features.

Made changes.

```python

def update_user_profile(
    user_id: str,
    email: str,
    phone_number: str,
    date_of_birth: str,
    shipping_address: str,
) -> dict:
    logger.info(
        "update_user_profile called: user_id=%s, email=%s, phone_number=%s, "
        "date_of_birth=%s, shipping_address=%s",
        user_id, email, phone_number, date_of_birth, shipping_address,
    )

    profile = get_user_profile(user_id)
    logger.debug("fetched profile: %s", profile)

    if profile is None:
        logger.warning("update failed: user not found, user_id=%s", user_id)
        return {"success": False, "error": "user_not_found"}

    if not validate_email(email):
        logger.warning(
            "update failed: invalid email, user_id=%s, email=%s",
            user_id, email,
        )
        return {"success": False, "error": "invalid_email"}

    if not validate_phone(phone_number):
        logger.warning(
            "update failed: invalid phone, user_id=%s, phone_number=%s",
            user_id, phone_number,
        )
        return {"success": False, "error": "invalid_phone"}

    profile.email = email
    profile.phone_number = phone_number
    profile.date_of_birth = date_of_birth
    profile.shipping_address = shipping_address

    saved = save_user_profile(profile)
    logger.info(
        "profile updated: user_id=%s, email=%s, phone_number=%s, "
        "date_of_birth=%s, shipping_address=%s, saved=%s",
        user_id, email, phone_number, date_of_birth, shipping_address, saved,
    )

    if not saved:
        logger.error("db write failed: user_id=%s", user_id)
        return {"success": False, "error": "db_write_failed"}

    return {"success": True, "error": None}

```