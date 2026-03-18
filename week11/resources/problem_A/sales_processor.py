from collections import defaultdict
from dataclasses import dataclass
from typing import List


@dataclass
class SaleRecord:
    id: str
    category: str
    amount: float
    region: str


def compute_revenue_by_category(records: List[SaleRecord]) -> dict[str, float]:
    revenue = defaultdict(float)
    seen_ids = set()

    for r in records:
        if r.id in seen_ids:
            continue
        seen_ids.add(r.id)
        revenue[r.category] += r.amount

    return dict(revenue)


if __name__ == "__main__":
    # Simulating an ETL retry: first batch + partial duplicate from a retry
    records = [
        SaleRecord("T001", "Electronics", 75000.0, "NA"),
        SaleRecord("T002", "Clothing",     1200.0, "EU"),
        SaleRecord("T003", "Electronics", 62000.0, "APAC"),
        SaleRecord("T004", "Food",          300.0, "NA"),
        SaleRecord("T005", "Clothing",    55000.0, "EU"),
        # --- retry starts here, T001-T003 re-delivered ---
        SaleRecord("T001", "Electronics", 75000.0, "NA"),
        SaleRecord("T002", "Clothing",     1200.0, "EU"),
        SaleRecord("T003", "Electronics", 62000.0, "APAC"),
    ]

    result = compute_revenue_by_category(records)
    print("Revenue by category:")
    for category, total in result.items():
        print(f"  {category}: ${total:,.2f}")