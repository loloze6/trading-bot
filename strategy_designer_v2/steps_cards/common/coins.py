"""The coin groups of `coins.md` and the data rules of `data_use.md`, in one place for every helper.

Why this cannot leak: it reads each coin's daily file only to know its first day; no price enters a decision here.
"""
import csv, datetime as dt, random
from pathlib import Path

STEPS = Path(__file__).resolve().parents[1]
DATA = STEPS.parents[1] / "trading-bot" / "local_data"
WINDOWS = STEPS / "04_backtest" / "windows" / "research_2016.json"

# coins.md, the draw of 2026-11-26 (seed 20261126): categories in the table's order
CATEGORIES = {
    "payments": ["BTC", "LTC", "XRP", "XLM", "BCH"],
    "platforms": ["ETH", "ADA", "ATOM", "ALGO", "TRX", "DOT", "SOL", "AVAX", "NEAR", "SUI"],
    "privacy": ["ZEC", "XMR", "DASH"],
    "finance": ["CRV", "UNI", "AAVE", "INJ", "LDO", "ONDO"],
    "infrastructure": ["LINK", "FIL", "GRT"],
    "ai": ["FET", "TAO"],
    "meme": ["DOGE", "SHIB", "PEPE"],
}
FINAL = ["XLM", "SOL", "DASH", "UNI", "LINK", "FET", "SHIB"]
LISTING_DAYS = 90          # data_use.md: a coin's first 90 days are never used
RESEARCH_SIZE = 8          # data_use.md: coins per research run


def portfolio_group():
    """Every universe coin not in the final group, in the categories' order."""
    return [c for v in CATEGORIES.values() for c in v if c not in FINAL]


def research_draw(run_name):
    """The run's 8 research coins: one per category from the portfolio group (coins sorted by name), then the rest
    drawn among the remaining coins; random.Random(run_name), so the same run always draws the same coins."""
    rng, port = random.Random(run_name), set(portfolio_group())
    picked = [rng.choice(sorted(c for c in v if c in port)) for v in CATEGORIES.values()]
    rest = sorted(port - set(picked))
    picked += rng.sample(rest, RESEARCH_SIZE - len(picked))
    return picked


def first_day(coin, data=DATA):
    with open(Path(data) / f"kraken_{coin}USD_1d.csv") as f:
        next(f)
        return dt.date.fromisoformat(next(csv.reader(f))[0][:10])


def first_usable_day(coin, data=DATA):
    """The coin's 91st day (data_use.md, rule on listings)."""
    return first_day(coin, data) + dt.timedelta(days=LISTING_DAYS)


def usable(coin, start, end=None, data=DATA):
    """Whether a period starting on `start` (a date or 'YYYY-MM-DD') is after the coin's first 90 days."""
    start = dt.date.fromisoformat(start) if isinstance(start, str) else start
    return start >= first_usable_day(coin, data)
