from ranking_pipeline import rank_candidates
from sample_input import CANDIDATES


def run() -> None:
    top = rank_candidates(CANDIDATES, top_k=3)

    print("Top candidates:")
    for candidate in top:
        print(candidate["name"], candidate["email"], candidate["score"])


if __name__ == "__main__":
    run()