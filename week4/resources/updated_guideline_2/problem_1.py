def is_valid_username(username: str) -> bool:
    """
    Return True if `username` is valid.

    Rules:
    - Not None; trimmed before validation
    - Length 3–20 characters
    - Starts with a letter
    - Contains only alphanumeric characters or `_`
    - Does not end with `_`
    """
    if username is None:
        return False

    username = username.strip()

    if len(username) < 3 or len(username) > 20:
        return False

    if not username[0].isalpha():
        return False

    for ch in username:
        if not (ch.isalnum() or ch == "_"):
            return False

    return True
