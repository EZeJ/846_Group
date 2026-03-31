from api_client import fetch_profile_score


import logging
from api_client import fetch_profile_score

logger = logging.getLogger("ranking_pipeline")

def normalize_email(email: str) -> str:
    return email.strip().lower()


    seen = set()
    unique = []

    for c in candidates:
        email = normalize_email(c["email"])
        if email not in seen:
            seen.add(email)
            updated = dict(c)
            updated["email"] = email
            unique.append(updated)

    return unique
def deduplicate_candidates(candidates: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    before_count = len(candidates)
    for c in candidates:
        email = normalize_email(c["email"])
        if email not in seen:
            seen.add(email)
            updated = dict(c)
            updated["email"] = email
            unique.append(updated)
    after_count = len(unique)
    duplicate_count = before_count - after_count
    logger.info(
        "Deduplication summary: before_count=%d after_count=%d duplicate_count=%d",
        before_count, after_count, duplicate_count
    )
    if duplicate_count > 0:
        logger.warning(
            "Duplicate candidates removed: before_count=%d after_count=%d duplicate_count=%d",
            before_count, after_count, duplicate_count
        )
    return unique


    valid = []

    for c in candidates:
        if not c.get("name"):
            continue
        if not c.get("email") or "@" not in c["email"]:
            continue
        if c.get("years_experience", 0) < 0:
            continue
        valid.append(c)

    return valid
def filter_invalid_candidates(candidates: list[dict]) -> list[dict]:
    valid = []
    before_count = len(candidates)
    dropped_count = 0
    for c in candidates:
        if not c.get("name"):
            dropped_count += 1
            continue
        if not c.get("email") or "@" not in c["email"]:
            dropped_count += 1
            continue
        if c.get("years_experience", 0) < 0:
            dropped_count += 1
            continue
        valid.append(c)
    after_count = len(valid)
    logger.info(
        "Filtering summary: before_count=%d after_count=%d dropped_count=%d",
        before_count, after_count, dropped_count
    )
    if dropped_count > 0:
        logger.warning(
            "Invalid candidates dropped: before_count=%d after_count=%d dropped_count=%d",
            before_count, after_count, dropped_count
        )
    return valid


def score_candidate(candidate: dict) -> float:
    profile_score = fetch_profile_score(candidate["email"])

    skill_bonus = len(candidate.get("skills", [])) * 1.5
    exp_bonus = min(candidate.get("years_experience", 0), 10) * 2

    return profile_score + skill_bonus + exp_bonus


    filtered = filter_invalid_candidates(candidates)
    unique = deduplicate_candidates(filtered)

    scored = []
    for candidate in unique:
        score = score_candidate(candidate)
        enriched = dict(candidate)
        enriched["score"] = score
        scored.append(enriched)

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
def rank_candidates(candidates: list[dict], top_k: int = 3) -> list[dict]:
    logger.info("Pipeline start: total_candidates=%d", len(candidates))
    filtered = filter_invalid_candidates(candidates)
    unique = deduplicate_candidates(filtered)

    scored = []
    for candidate in unique:
        score = score_candidate(candidate)
        enriched = dict(candidate)
        enriched["score"] = score
        scored.append(enriched)

    scored.sort(key=lambda x: x["score"], reverse=True)
    result = scored[:top_k]
    logger.info(
        "Final ranking outcome: requested_top_k=%d returned_count=%d",
        top_k, len(result)
    )
    return result