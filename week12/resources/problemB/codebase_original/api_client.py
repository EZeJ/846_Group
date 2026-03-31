import random
import time


class TemporaryAPIError(Exception):
    pass


def _mock_remote_score(email: str) -> float:
    if "retry" in email:
        raise TemporaryAPIError("Temporary upstream failure")
    if "slow" in email:
        time.sleep(0.2)
    return round(random.uniform(10.0, 50.0), 2)


def fetch_profile_score(email: str, max_retries: int = 3, backoff_s: float = 0.1) -> float:
    attempt = 0

    while attempt < max_retries:
        attempt += 1
        try:
            return _mock_remote_score(email)
        except TemporaryAPIError:
            if attempt == max_retries:
                raise
            time.sleep(backoff_s * attempt)

    raise RuntimeError("Unreachable")