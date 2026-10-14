"""Which cached daily Kraken coins cover fold A with warm-up (bounded, read only).

For each trading-bot/local_data/kraken_<COIN>USD_1d.csv it reads ONLY the date column, and prints:
the first date, whether the cache reaches the window end, and how many calendar days are missing
inside [first window day minus warm-up, fold A end]. It never prints the cache's last date or any
row, and never opens the sealed-holdout store.

Usage: python daily_cache_coverage.py <local_data dir> [warmup_days]
"""
from __future__ import annotations

import csv
import sys
from datetime import date, timedelta
from pathlib import Path

FOLDS_FILE = Path(__file__).resolve().parents[2] / "config" / "folds.yaml"


def fold_a_span() -> tuple:
    import yaml
    doc = yaml.safe_load(FOLDS_FILE.read_text(encoding="utf-8"))
    blocks = doc["folds"]["A"]
    return (date.fromisoformat(str(blocks[0]["start"])), date.fromisoformat(str(blocks[-1]["end"])))


def main() -> None:
    data_dir = Path(sys.argv[1])
    warmup = int(sys.argv[2]) if len(sys.argv) > 2 else 250
    start, end = fold_a_span()
    need_from = start - timedelta(days=warmup)
    print(f"fold A {start}..{end}; warm-up {warmup} days -> need data from {need_from}")
    for path in sorted(data_dir.glob("kraken_*USD_1d.csv")):
        days = set()
        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row:
                    days.add(date.fromisoformat(row[0][:10]))
        first = min(days)
        reaches_end = max(days) >= end  # compared, never printed
        window = [need_from + timedelta(days=k) for k in range((end - need_from).days + 1)]
        missing = sum(1 for d in window if d not in days)
        covers = first <= need_from and reaches_end
        coin = path.name.split("_")[1].replace("USD", "")
        print(f"{coin:6s} first {first}  reaches_fold_end {reaches_end}  missing_days_in_window {missing:4d}"
              f"  covers_with_warmup {covers}")


if __name__ == "__main__":
    main()
