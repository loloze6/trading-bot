"""The coin groups of `coins.md` and the data rules of `data_use.md`, in one place for every helper.

Why this cannot leak: it reads each coin's daily file only for its dates (its first day, its holes); no price enters a
decision here, and a window is left out or kept before the engine reads any of its bars.
"""
import csv, datetime as dt, json, math, random, subprocess, sys, tempfile
from pathlib import Path

STEPS = Path(__file__).resolve().parents[1]
DATA = STEPS.parents[1] / "trading-bot" / "local_data"
WINDOWS = STEPS / "04_backtest" / "windows" / "research_2016.json"
BT = STEPS.parents[1] / "trading-bot" / "backtest"   # the backtest wrapper (read only: its warm-up is asked, never changed)

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
DRAW_SHARE = 0.5           # data_use.md, 1.3: a research coin can be tested on at least this share of the check half's windows


def portfolio_group():
    """Every universe coin not in the final group, in the categories' order."""
    return [c for v in CATEGORIES.values() for c in v if c not in FINAL]


def research_draw(run_name, drawable):
    """The run's 8 research coins among the drawable portfolio coins (data_use.md, 1.3): one per category that has a
    drawable coin (the categories in the table's order, coins sorted by name), then the rest drawn among all the
    remaining drawable coins; random.Random(run_name), so the same run always draws the same coins."""
    rng, pool = random.Random(run_name), set(drawable) & set(portfolio_group())
    picked = [rng.choice(sorted(c for c in v if c in pool)) for v in CATEGORIES.values() if any(c in pool for c in v)]
    rest = sorted(pool - set(picked))
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


def new_data_use(run, python):
    """What a run in the new data use is backtested on: its 8 research coins, drawn among the drawable portfolio coins
    (data_use.md, 1.3), and the research windows (the file's path relative to steps_cards/). The draw's count is kept
    beside them: the warm-up it was counted with and each portfolio coin's testable windows of the check half."""
    seconds = detector_warmup(python)
    windows = json.loads(WINDOWS.read_text(encoding="utf-8"))
    counts = testable_counts(seconds, windows)
    need = draw_need(windows)
    return {"version": DATA_USE_VERSION, "research_coins": research_draw(run, drawable(counts, need)),
            "windows": str(WINDOWS.relative_to(STEPS)),
            "draw": {"warmup_days": seconds // 86400, "check_windows": len(check_half(windows)), "needed": need,
                     "testable": counts}}


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


FIRST_DAYS = "the coin's first 90 days"


def warmup_start(start, warmup_seconds):
    """The first day the wrapper loads for a window starting on `start`: its start minus the warm-up, as the bot
    computes it (trading-bot/core/launcher.py, run_backtest with warmup_prefetch: the start's midnight minus the
    warm-up's seconds, read as a day)."""
    start = dt.date.fromisoformat(start) if isinstance(start, str) else start
    return (dt.datetime.combine(start, dt.time()) - dt.timedelta(seconds=warmup_seconds)).date()


def left_out(coin, start, end, data=DATA, days=None, warmup_seconds=None):
    """data_use.md, section 3: why the coin is left out of the window [start, end], or None when it is used. In order:
    the coin's first 90 days (the window starts before its 91st day); a history shorter than the plan's warm-up (the
    coin's first day is after the first day the wrapper loads for the window; `warmup_seconds`: what the wrapper loads
    for this plan, `plan_warmup`); a hole of more than one day in the window."""
    days = dates(coin, data) if days is None else days
    first = dt.date.fromisoformat(start) if isinstance(start, str) else start
    if first < days[0] + dt.timedelta(days=LISTING_DAYS):
        return FIRST_DAYS
    if warmup_seconds and days[0] > warmup_start(start, warmup_seconds):
        return f"the coin's history is shorter than the plan's warm-up: {warmup_days(warmup_seconds)} days asked"
    hole = longest_hole(days, start, end)
    return f"a hole of {hole} days" if hole > HOLE_DAYS else None


# The warm-up a plan asks (data_use.md, section 3): what the wrapper loads before each window. The bot's own rule
# (trading-bot/core/launcher.py, run_backtest with warmup_prefetch, which run_protocol.py always sets): twice the
# strategy's required bars. The required bars are asked from the bot's own classes, in the venv; the factor 2 is the
# launcher's, written inline there (no function to call), so it is repeated here and proven on real records
# (runs/BUILD_A12.md).
PREFETCH_FACTOR = 2
_ASK = ("import json, sys; sys.path.insert(0, '..'); sys.path.insert(0, '.');"
        "import timeframe;"
        "from strategies.main_strategy import AdvancedStrategy;"
        "from strategies.regime_engine import ConfigDrivenRegimeEngine;"
        "path, bar, what = sys.argv[1:4]; i = timeframe.timeframe_seconds(bar);"
        "n = (AdvancedStrategy(config_path=path, candle_interval_seconds=i).required_bars if what == 'plan' else "
        "ConfigDrivenRegimeEngine(json.load(open(path))['regime_detector']).get_required_periods());"
        "print('WARMUP ' + json.dumps({'required_bars': n, 'bar_seconds': i}))")


def _ask(python, config_path, bar, what):
    r = subprocess.run([str(python), "-c", _ASK, str(Path(config_path).resolve()), bar, what], cwd=BT,
                       capture_output=True, text=True)
    line = next((l for l in reversed(r.stdout.splitlines()) if l.startswith("WARMUP ")), None)
    if r.returncode or line is None:
        sys.exit(f"could not read the warm-up of {Path(config_path).name}: {(r.stderr or r.stdout)[-500:]}")
    a = json.loads(line[len("WARMUP "):])
    return PREFETCH_FACTOR * a["required_bars"] * a["bar_seconds"]


def plan_warmup(python, config_path, bar):
    """The seconds of data the wrapper loads before each window of this plan: twice its strategy's required bars
    (the bot's AdvancedStrategy on the plan's config, asked in the venv)."""
    return _ask(python, config_path, bar, "plan")


def detector_warmup(python, bar="1d"):
    """The seconds the wrapper loads for the market-profile detector alone (common/market_profile.md: the trend over
    60 days, the agitation over 30 days against a year), built by step 3's own code and asked from the bot's regime
    engine: the least any plan naming a full profile asks."""
    sys.path.insert(0, str(STEPS / "03_test_plan" / "helper"))
    import make_test_plan
    config = make_test_plan.add_profile({"strategies": {"regimes": {}}}, "falling calm", bar)
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "detector.json"
        f.write_text(json.dumps(config))
        return _ask(python, f, bar, "detector")


def warmup_days(warmup_seconds):
    """The warm-up in days, rounded up (what a reason line names)."""
    return -(-warmup_seconds // 86400)


# The draw's rule (data_use.md, 1.3): a portfolio coin is drawable when it can be tested on at least half of the check
# half's windows, counted with the market-profile detector's warm-up.
def check_half(windows):
    """The check half's windows (data_use.md, section 2): those starting on or after CHECK_FROM."""
    return [w for w in windows if w["test"]["start"] >= CHECK_FROM]


def testable(coin, warmup_seconds, windows, data=DATA):
    """The numbers K (w1 = the file's first window) of the windows the coin is used in, with this warm-up."""
    days = dates(coin, data)
    return [k for k, w in enumerate(windows, 1)
            if left_out(coin, w["test"]["start"], w["test"]["end"], data, days, warmup_seconds) is None]


def testable_counts(warmup_seconds, windows, coin_list=None, data=DATA):
    """{coin: how many of the check half's windows it can be tested on}, for the portfolio coins."""
    first = len(windows) - len(check_half(windows))
    return {c: sum(k > first for k in testable(c, warmup_seconds, windows, data))
            for c in (coin_list or portfolio_group())}


def draw_need(windows):
    """How many check-half windows a drawable coin needs: at least half of them."""
    return math.ceil(len(check_half(windows)) * DRAW_SHARE)


def drawable(counts, need):
    """The drawable coins, in the portfolio group's order."""
    return [c for c, n in counts.items() if n >= need]
