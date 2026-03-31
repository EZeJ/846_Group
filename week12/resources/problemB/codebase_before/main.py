from ranking_pipeline import rank_candidates
from sample_input import CANDIDATES


def run() -> None:
    logger = logging.getLogger("main")
    logger.info("Starting candidate ranking workflow.")
    top = rank_candidates(CANDIDATES, top_k=3)

    logger.info(f"Top {len(top)} candidates selected. Names: {[c['name'] for c in top]}")
    print("Top candidates:")
    for candidate in top:
        print(candidate["name"], candidate["email"], candidate["score"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    run()