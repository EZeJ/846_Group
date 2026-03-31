User: I have /Users/sofiiatkach/Desktop/LLM/846_Group/week12/resources/updated_guideline_7/user_profile_service.py. Add logging to the update_user_profile function. Requirements:
- Include relevant runtime context to help debug failures and understand
  execution flow.
- Log user_id and outcome (success or error type) at every decision point.

Privacy constraints — the following fields contain PII and must NEVER appear
in any log statement:
- email
- phone_number
- date_of_birth
- shipping_address
- any field from the UserProfile dataclass other than user_id

Do not log the full profile object. Do not echo user-supplied values back
into warning or error messages.

GitHub Copilot: Read [](file:///Users/sofiiatkach/Desktop/LLM/846_Group/week12/resources/updated_guideline_7/user_profile_service.py#1-1), lines 1 to 50

Read [](file:///Users/sofiiatkach/Desktop/LLM/846_Group/week12/resources/updated_guideline_7/user_profile_service.py#51-51), lines 51 to 98

Using "Edit File"

Using ""


````

````
I have added logging to the `update_user_profile` function to log the `user_id` and outcome at every decision point, ensuring that no PII fields are logged. Let me know if you need further modifications or assistance!

Made changes.

```python
def update_user_profile(
    user_id: str,
    email: str,
    phone_number: str,
    date_of_birth: str,
    shipping_address: str,
) -> dict:
    logger.info("update_user_profile started: user_id=%s", user_id)

    profile = get_user_profile(user_id)

    if profile is None:
        logger.warning("update failed: user_not_found, user_id=%s", user_id)
        return {"success": False, "error": "user_not_found"}

    if not validate_email(email):
        logger.warning("update failed: invalid_email, user_id=%s", user_id)
        return {"success": False, "error": "invalid_email"}

    if not validate_phone(phone_number):
        logger.warning("update failed: invalid_phone, user_id=%s", user_id)
        return {"success": False, "error": "invalid_phone"}

    profile.email = email
    profile.phone_number = phone_number
    profile.date_of_birth = date_of_birth
    profile.shipping_address = shipping_address

    saved = save_user_profile(profile)

    if not saved:
        logger.error("db write failed: user_id=%s", user_id)
        return {"success": False, "error": "db_write_failed"}

    logger.info("update_user_profile succeeded: user_id=%s", user_id)
    return {"success": True, "error": None}
```
