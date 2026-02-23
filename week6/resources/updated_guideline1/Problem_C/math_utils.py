def normalize(scores):
    total = sum(scores)
    return [s / total for s in scores]