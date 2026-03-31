import random
import time
import logging


class TemporaryAPIError(Exception):
    pass


logger = logging.getLogger("api_client")

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
                logger.error(
                    "Profile score fetch failed after all retries: email=%s attempts_used=%d",
                    email, attempt
                )
                raise
            logger.warning(
                "Retryable API failure: email=%s attempt=%d max_retries=%d backoff_s=%.2f",
                email, attempt, max_retries, backoff_s * attempt
            )
            time.sleep(backoff_s * attempt)
    raise RuntimeError("Unreachable")