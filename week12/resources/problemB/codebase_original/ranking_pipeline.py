from api_client import fetch_profile_score


def normalize_email(email: str) -> str:
    return email.strip().lower()


def deduplicate_candidates(candidates: list[dict]) -> list[dict]:
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


def filter_invalid_candidates(candidates: list[dict]) -> list[dict]:
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


def score_candidate(candidate: dict) -> float:
    profile_score = fetch_profile_score(candidate["email"])

    skill_bonus = len(candidate.get("skills", [])) * 1.5
    exp_bonus = min(candidate.get("years_experience", 0), 10) * 2

    return profile_score + skill_bonus + exp_bonus


def rank_candidates(candidates: list[dict], top_k: int = 3) -> list[dict]:
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