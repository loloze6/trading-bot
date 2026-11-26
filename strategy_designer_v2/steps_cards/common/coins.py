"""The coin groups of `coins.md` and the data rules of `data_use.md`, in one place for every helper.

Why this cannot leak: it reads each coin's daily file only for its dates (its first day, its holes); no price enters a
decision here, and a window is left out or kept before the engine reads any of its bars.
"""
import csv, datetime as dt, json, random
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


# The data use of a run (data_use.md, build plan part 3). A run in the new data use holds this file, written once when
# the run starts (run_brief --data-use 2); other helpers read it. Without it, the run is in the old data use (the
# brief's coins, folds A to D).
DATA_USE_VERSION = 2
CHECK_FROM = "2022-01-01"  # data_use.md, section 2: the explore half ends before it, the check half starts on it
HOLE_DAYS = 1              # data_use.md, section 3: a hole of one day is ignored; a longer one leaves the window out


def data_use_file(run):
    return STEPS / "orchestration" / "loop" / run / "data_use.json"


def new_data_use(run):
    """What a run in the new data use is backtested on: its 8 research coins and the research windows (the file's
    path relative to steps_cards/)."""
    return {"version": DATA_USE_VERSION, "research_coins": research_draw(run),
            "windows": str(WINDOWS.relative_to(STEPS))}


def data_use(run):
    """The run's data use (data_use.json), or None for a run in the old data use."""
    p = data_use_file(run)
    return json.loads(p.read_text()) if p.exists() else None


def dates(coin, data=DATA):
    """The days of the coin's daily file (dates only, no price)."""
    with open(Path(data) / f"kraken_{coin}USD_1d.csv") as f:
        next(f)
        return [dt.date.fromisoformat(r[0][:10]) for r in csv.reader(f) if r and r[0][:1].isdigit()]


def longest_hole(days, start, end):
    """The longest run of days in [start, end] missing from `days` (a sorted list of dates), the window's edges
    included: a coin that stopped trading before the window's end has a hole up to it."""
    start = dt.date.fromisoformat(start) if isinstance(start, str) else start
    end = dt.date.fromisoformat(end) if isinstance(end, str) else end
    inside = [d for d in days if start <= d <= end]
    edges = [start - dt.timedelta(days=1)] + inside + [end + dt.timedelta(days=1)]
    return max((b - a).days - 1 for a, b in zip(edges, edges[1:]))


def left_out(coin, start, end, data=DATA, days=None):
    """data_use.md, section 3: why the coin is left out of the window [start, end], or None when it is used. The coin's
    first 90 days (the window starts before its 91st day), then a hole of more than one day in the window."""
    if not usable(coin, start, data=data):
        return "the coin's first 90 days"
    hole = longest_hole(dates(coin, data) if days is None else days, start, end)
    return f"a hole of {hole} days" if hole > HOLE_DAYS else None
