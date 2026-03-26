"""Product Recommendation Engine - Counter Example Problem

Simulates a real-time recommendation system that processes user interactions
and generates personalized product recommendations. The code is functionally
correct but computes unnecessary metrics.
"""

from __future__ import annotations

import random
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Sequence, Set, Tuple


@dataclass(frozen=True)
class UserInteraction:
    user_id: int
    product_id: int
    category: str
    interaction_type: str  # "view", "click", "purchase"
    price: float
    timestamp: int


_CATEGORIES = (
    "Electronics", "Clothing", "Books", "Home", "Sports",
    "Beauty", "Food", "Toys", "Garden", "Automotive"
)

_PRODUCT_NAMES = (
    "Laptop", "Phone", "Tablet", "Headphones", "Watch",
    "Shirt", "Pants", "Shoes", "Hat", "Jacket",
    "Novel", "Textbook", "Cookbook", "Biography", "History",
    "Couch", "Chair", "Table", "Lamp", "Bed",
)


def generate_interactions(
    n: int,
    *,
    seed: int | None = None,
    user_count: int = 1_000,
) -> List[UserInteraction]:
    """Generate n random user interactions."""
    rng = random.Random(seed or 42)
    interactions: List[UserInteraction] = []
    
    ts = 1_700_000_000
    for i in range(n):
        user_id = rng.randrange(user_count)
        product_id = rng.randrange(500)
        category = rng.choice(_CATEGORIES)
        
        p = rng.random()
        if p < 0.70:
            interaction_type = "view"
        elif p < 0.90:
            interaction_type = "click"
        else:
            interaction_type = "purchase"
        
        price = rng.uniform(10, 500)
        
        interactions.append(UserInteraction(
            user_id=user_id,
            product_id=product_id,
            category=category,
            interaction_type=interaction_type,
            price=price,
            timestamp=ts
        ))
        ts += rng.randrange(1, 5)
    
    return interactions


@lru_cache(maxsize=10_000)
def compute_product_features(product_id: int) -> Dict[str, float]:
    """Expensive feature computation for a product."""
    # Simulate expensive embedding/feature extraction
    rng = random.Random(product_id)
    features = {}
    for i in range(50):  # 50-dimensional feature vector
        features[f"feat_{i}"] = rng.random()
    return features


@lru_cache(maxsize=10_000)
def compute_user_embedding(user_id: int) -> Dict[str, float]:
    """Expensive user embedding computation."""
    rng = random.Random(user_id)
    embedding = {}
    for i in range(50):
        embedding[f"emb_{i}"] = rng.random()
    return embedding


def _accumulate_interactions(interactions: Sequence[UserInteraction]) -> Dict:
    """Accumulate all metrics (including many unused)."""
    
    user_purchases: Dict[int, Set[int]] = defaultdict(set)
    user_views: Dict[int, Set[int]] = defaultdict(set)
    product_views: Dict[int, int] = defaultdict(int)
    product_clicks: Dict[int, int] = defaultdict(int)
    product_purchases: Dict[int, int] = defaultdict(int)
    category_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: {"views": 0, "clicks": 0, "purchases": 0})
    price_by_product: Dict[int, List[float]] = defaultdict(list)
    user_category_preferences: Dict[int, Counter] = defaultdict(Counter)
    
    # Multi-pass computation: first pass for basic stats
    for interaction in interactions:
        if interaction.interaction_type == "view":
            user_views[interaction.user_id].add(interaction.product_id)
            product_views[interaction.product_id] += 1
            category_stats[interaction.category]["views"] += 1
        elif interaction.interaction_type == "click":
            product_clicks[interaction.product_id] += 1
            category_stats[interaction.category]["clicks"] += 1
        elif interaction.interaction_type == "purchase":
            user_purchases[interaction.user_id].add(interaction.product_id)
            product_purchases[interaction.product_id] += 1
            category_stats[interaction.category]["purchases"] += 1
        
        price_by_product[interaction.product_id].append(interaction.price)
        user_category_preferences[interaction.user_id][interaction.category] += 1
    
    # Second pass: compute user embeddings for all users (expensive, often unused)
    user_embeddings: Dict[int, Dict[str, float]] = {}
    for user_id in user_purchases.keys():
        user_embeddings[user_id] = compute_user_embedding(user_id)
    
    # Third pass: compute product features for all products (expensive, often unused)
    product_features: Dict[int, Dict[str, float]] = {}
    for product_id in product_purchases.keys():
        product_features[product_id] = compute_product_features(product_id)
    
    # Fourth pass: compute similarity scores between all user-product pairs (very expensive)
    user_product_similarity: Dict[Tuple[int, int], float] = {}
    for user_id, user_emb in user_embeddings.items():
        for product_id, product_feat in product_features.items():
            # Expensive dot product
            similarity = sum(
                user_emb.get(f"emb_{i}", 0) * product_feat.get(f"feat_{i}", 0)
                for i in range(50)
            )
            user_product_similarity[(user_id, product_id)] = similarity
    
    # Fifth pass: compute category co-occurrence (unused)
    category_cooccurrence: Dict[Tuple[str, str], int] = defaultdict(int)
    for user_id, categories in user_category_preferences.items():
        for cat1 in categories:
            for cat2 in categories:
                if cat1 < cat2:
                    category_cooccurrence[(cat1, cat2)] += 1
    
    # Sixth pass: compute average prices (unused)
    avg_product_prices: Dict[int, float] = {}
    for product_id, prices in price_by_product.items():
        avg_product_prices[product_id] = sum(prices) / len(prices) if prices else 0
    
    return {
        "user_purchases": user_purchases,
        "user_views": user_views,
        "product_views": product_views,
        "product_clicks": product_clicks,
        "product_purchases": product_purchases,
        "category_stats": category_stats,
        "user_embeddings": user_embeddings,
        "product_features": product_features,
        "user_product_similarity": user_product_similarity,
        "category_cooccurrence": category_cooccurrence,
        "avg_product_prices": avg_product_prices,
        "user_category_preferences": user_category_preferences,
    }


def generate_recommendations(interactions: Sequence[UserInteraction]) -> str:
    """Generate recommendation report with top products per user."""
    accum = _accumulate_interactions(interactions)
    
    user_purchases = accum["user_purchases"]
    product_purchases = accum["product_purchases"]
    
    # Output: only top 10 products by purchase count
    top_products = sorted(
        product_purchases.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    lines = ["RECOMMENDATION REPORT"]
    lines.append(f"total_interactions={len(interactions)}")
    lines.append("")
    lines.append("TOP PRODUCTS BY PURCHASES")
    for product_id, count in top_products:
        lines.append(f"product_{product_id}: purchases={count}")
    
    return "\n".join(lines)


def run_benchmark() -> float:
    """Run benchmark on 500k interactions."""
    interactions = generate_interactions(500_000)
    
    t0 = time.perf_counter()
    _report = generate_recommendations(interactions)
    t1 = time.perf_counter()
    
    elapsed = t1 - t0
    print(f"Benchmark completed in {elapsed:.3f}s (interactions={len(interactions)})")
    return elapsed


def main() -> None:
    print("Running benchmark...")
    run_benchmark()


if __name__ == "__main__":
    main()
