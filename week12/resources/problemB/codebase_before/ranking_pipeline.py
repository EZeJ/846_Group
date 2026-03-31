def normalize_email(email: str) -> str:
from api_client import fetch_profile_score
import logging


def normalize_email(email: str) -> str:
    return email.strip().lower()


def deduplicate_candidates(candidates: list[dict]) -> list[dict]:
    logger = logging.getLogger("ranking_pipeline")
    seen = set()
    unique = []
    dropped = 0
    for c in candidates:
        email = normalize_email(c["email"])
        if email not in seen:
            seen.add(email)
            updated = dict(c)
            updated["email"] = email
            unique.append(updated)
        else:
            dropped += 1
    if dropped > 0:
        logger.warning(f"Dropped {dropped} duplicate candidate(s) during deduplication.")
    return unique


def filter_invalid_candidates(candidates: list[dict]) -> list[dict]:
    logger = logging.getLogger("ranking_pipeline")
    valid = []
    dropped = 0
    for c in candidates:
        suspicious = False
        if not c.get("name"):
            dropped += 1
            logger.warning(f"Dropped candidate with missing name: {c}")
            continue
        if not c.get("email") or "@" not in c["email"]:
            dropped += 1
            logger.warning(f"Dropped candidate with invalid email: {c}")
            continue
        if c.get("years_experience", 0) < 0:
            dropped += 1
            logger.warning(f"Dropped candidate with negative years_experience: {c}")
            continue
        if c.get("years_experience", 0) > 40:
            suspicious = True
        if suspicious:
            logger.warning(f"Suspicious years_experience for candidate: {c}")
        valid.append(c)
    if dropped > 0:
        logger.info(f"Filtered out {dropped} invalid candidate(s).")
    return valid


def score_candidate(candidate: dict) -> float:
    logger = logging.getLogger("ranking_pipeline")
    profile_score = fetch_profile_score(candidate["email"])
    skill_bonus = len(candidate.get("skills", [])) * 1.5
    exp_bonus = min(candidate.get("years_experience", 0), 10) * 2
    total = profile_score + skill_bonus + exp_bonus
    logger.info(
        f"Scored candidate {candidate.get('name')} ({candidate.get('email')}): profile_score={profile_score}, skill_bonus={skill_bonus}, exp_bonus={exp_bonus}, total={total}"
    )
    return total


def rank_candidates(candidates: list[dict], top_k: int = 3) -> list[dict]:
    logger = logging.getLogger("ranking_pipeline")
    logger.info("Starting candidate filtering stage.")
    filtered = filter_invalid_candidates(candidates)
    logger.info("Starting deduplication stage.")
    unique = deduplicate_candidates(filtered)

    logger.info("Scoring candidates.")
    scored = []
    for candidate in unique:
        score = score_candidate(candidate)
        enriched = dict(candidate)
        enriched["score"] = score
        scored.append(enriched)

    scored.sort(key=lambda x: x["score"], reverse=True)
    logger.info(f"Ranking complete. Returning top {top_k} candidates out of {len(scored)}.")
    return scored[:top_k]