import random
    if "retry" in email:

import random
import time
import logging


class TemporaryAPIError(Exception):
    pass



    # Simulate API behavior for testing
def fetch_profile_score(email: str, max_retries: int = 3, backoff_s: float = 0.1) -> float:
    logger = logging.getLogger("api_client")
    url = f"https://mock.api/score?email={email}"
    attempt = 0
    last_exc = None

    while attempt < max_retries:
        attempt += 1
        try:
            score = _mock_remote_score(email)
            logger.info(
                f"Fetched score for url={url} attempt={attempt} backoff_s={backoff_s * attempt:.2f} status_code=200 outcome=success"
            )
            return score
        except TemporaryAPIError as exc:
            last_exc = exc
            if attempt == max_retries:
                logger.error(
                    f"Failed to fetch score for url={url} after {attempt} attempts. backoff_s={backoff_s * attempt:.2f} status_code=503 outcome=error: retries exhausted"
                )
                raise
            logger.warning(
                f"Temporary error for url={url} on attempt={attempt} backoff_s={backoff_s * attempt:.2f} status_code=503 outcome=retrying"
            )
            time.sleep(backoff_s * attempt)

    logger.error(
        f"Unreachable code reached for url={url} after {attempt} attempts. outcome=error"
    )
    raise RuntimeError("Unreachable")