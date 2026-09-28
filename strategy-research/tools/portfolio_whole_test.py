"""
Whole-test ("profit bars v2") portfolio functions -- E-062 S2a.

PURE FUNCTIONS ONLY. Nothing in the orchestrator calls this module yet (the
wiring, the flag `orchestrator.profit_bars_v2.enabled` and the bar values are
S2b). Definitions: engineering/roadmap/E-062/S1_FINDINGS.md, decisions G1-G9 and
G11 (accepted in that file's "Decision" section), D-034..D-039
(engineering/DECISION_LOG.md).

GOVERNING RULE (S2a code review): when data is missing or ambiguous, a result
is NOT_EVALUABLE or the conservative number -- never the flattering one.

WHY A SIBLING MODULE and not more code in tools/portfolio_daily.py:
portfolio_daily.py is the v1 definition that the flag-off profit bars
(run_phase1_research._portfolio_profit_metrics) and the composition
(tools/composition.load_block_daily_returns) read today. Keeping it
byte-for-byte unchanged makes "flag-off behaviour is untouched" true by
construction (its sha256 is pinned in the tests). This module IMPORTS the v1
primitives (window_common_curve: common days, per-window 0.9 coverage floor,
anchor normalisation; PortfolioNotEvaluable) so the two versions share one
definition of a window's portfolio and differ only in what v2 adds: the
chaining across windows. The one duplicated piece is window_close_bars, a copy
of window_equity_bars' parsing for the `close` column (tested to parse the same
rows identically).

DEVIATION FROM THE ACCEPTED G1 TEXT (code review finding 4): G1 says "a
junction day that the later window lacks is treated as a gap" (linked flat).
Linking flat drops real P&L the strategy made or lost while the data is
missing, so here a missing junction day is NOT_EVALUABLE instead, and so is a
window whose data stops before its nominal end or starts after its nominal
start (second-round findings 1 and 3). The NOT_EVALUABLE reason lists every
missing (window, coin, day) cell and their count (finding 4). Only a real
protocol gap -- a window whose nominal start is after the previous windows'
nominal end, known from the protocol's window bounds -- is linked flat, as G1
says. chain_windows therefore REQUIRES the protocol's nominal (start, end) per
window (window_bounds_from_protocol / load_protocol_window_bounds), never a
window manifest's start (the warm-up prefetch start).

What v2 adds:
  * chain_windows: one whole-test daily and bar-level curve out of the
    per-window curves, over the protocol's nominal span (G1, G2);
  * whole_test_max_drawdown: drawdown on the chained BAR-level curve (D-034);
  * whole_test_sharpe: Sharpe of the chained daily returns (G3, D-036);
  * whole_test_trade_counts: per-coin trade count over the whole test, raw and
    without end_of_window forced closes (G5, D-035);
  * chained_buy_and_hold: strategy vs equal-weight buy-and-hold on the chained
    level (final level - 1, multi-day steps included), one round trip per coin
    (G6, D-037);
  * pooled_edge_to_cost_ratio: the shared, UNROUNDED realized edge / cost
    ratio (tools/cost_helpers.py), the lower of all trades and non-forced
    trades, with the min-trades floor on the non-forced trades (G7, D-038);
  * readers/lookups: window_close_bars, window_bounds_from_protocol,
    load_protocol_window_bounds, charged_fee_bps, slippage_bps_for_symbol.

S2b SCOPE NOTE (fee): buy-and-hold must be charged the commission the strategy
was actually charged. run_protocol passes run_backtest a commission_rate from
cost_helpers.resolve_commission_rate(symbol, cost_model, --commission-bps,
--cost-product), but the run does not record which --commission-bps /
--cost-product it used (the manifest's cost_model.fee_bps is cost_model.json's
table value, not that rate). S2b must record them on the protocol result so
charged_fee_bps can be called with the run's own values.

NOT_EVALUABLE is signalled by raising portfolio_daily.PortfolioNotEvaluable
(message = the reason), like the v1 module. Malformed input (NaN, non-positive
value, bool, unsorted timestamps, duplicate days, unknown exit_reason,
unhashable symbol, inconsistent close series, ...) raises a plain ValueError --
never NOT_EVALUABLE, never AttributeError/TypeError, never a silent default.
Numbers may be Python or numpy scalars (numbers.Real / numbers.Integral); bools
are refused.

No lookahead: every value comes from inside the backtest windows the caller
passes (per-window equity/close bars, per-window trade records). Nothing is
fetched, nothing past a window's last bar is read, and nothing here reads
anything under local_data/holdout_sealed/.
"""
from __future__ import annotations

import csv
import math
import numbers
import statistics
from collections.abc import Mapping
from datetime import date, datetime, timezone
from pathlib import Path

import cost_helpers as _ch  # tools/ sibling: shared commission + edge/cost definitions
import portfolio_daily as _pd  # tools/ sibling: the v1 per-window definition

PortfolioNotEvaluable = _pd.PortfolioNotEvaluable

# G2: the chained span must satisfy the SAME coverage constant as each window
# (counted return days + 1 >= this x calendar days from the first anchor to the
# last chained day).
WHOLE_TEST_MIN_COVERAGE = _pd.PORTFOLIO_MIN_COMMON_DAY_COVERAGE

# G3: fewer daily returns than this -> the Sharpe is NOT_EVALUABLE.
SHARPE_MIN_DAILY_RETURNS = 30
# G3: mean / sample stdev x sqrt(365), rf 0 -- same convention as core.sharpe
# (trading-bot/performance/metrics.py) and bar_equity.
SHARPE_DAYS_PER_YEAR = 365

# The exit_reason vocabulary of trade_diagnostics.json's trade records:
# workflow_artifacts/schemas/trade_diagnostics.schema.json:48 (enum), produced
# by tools/run_protocol.py::_infer_exit_reason (stop_loss/time_stop are schema
# completeness only -- the engine never produces them today).
EXIT_REASONS = frozenset({"signal_flip", "stop_loss", "time_stop", "end_of_window"})
END_OF_WINDOW = "end_of_window"


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

def _is_real(x) -> bool:
    return isinstance(x, numbers.Real) and not isinstance(x, bool)


def _is_int(x) -> bool:
    return isinstance(x, numbers.Integral) and not isinstance(x, bool)


def _finite_positive(value, what: str) -> float:
    if not _is_real(value):
        raise ValueError(f"{what}: {value!r} is not a number")
    v = float(value)
    if not math.isfinite(v) or v <= 0:
        raise ValueError(f"{what}: {value!r} is not a finite positive number")
    return v


def _nonneg(value, what: str) -> float:
    if not _is_real(value) or not math.isfinite(float(value)) or float(value) < 0:
        raise ValueError(f"{what}: {value!r} is not a finite non-negative number")
    return float(value)


def _hashable(value, what: str) -> None:
    try:
        hash(value)
    except TypeError:
        raise ValueError(f"{what}: {value!r} is not hashable") from None


def _check_bars(win, coin, bars) -> None:
    """One (coin, window) bar series {naive datetime: positive finite value},
    timestamps strictly increasing in iteration order (a dict cannot hold a
    duplicate timestamp; an out-of-order one is an input bug, not something to
    sort away silently)."""
    if not isinstance(bars, Mapping):
        raise ValueError(f"window {win!r} coin {coin!r}: bars must be a mapping "
                         f"{{timestamp: value}}, got {type(bars).__name__}")
    prev = None
    for ts, v in bars.items():
        if not isinstance(ts, datetime):
            raise ValueError(f"window {win!r} coin {coin!r}: timestamp {ts!r} is not a datetime")
        if ts.tzinfo is not None:
            raise ValueError(f"window {win!r} coin {coin!r}: timestamp {ts!r} is not naive UTC")
        if prev is not None and ts <= prev:
            raise ValueError(f"window {win!r} coin {coin!r}: timestamps are not strictly "
                             f"increasing ({prev} then {ts})")
        _finite_positive(v, f"window {win!r} coin {coin!r} at {ts}")
        prev = ts


def _check_coins(coins) -> list:
    coins = list(coins)
    for c in coins:
        _hashable(c, "coin")
    if not coins or len(set(coins)) != len(coins):
        raise ValueError(f"coins must be a non-empty list without duplicates, got {coins!r}")
    return coins


def _check_windows(windows, coins, *, coin_mismatch=PortfolioNotEvaluable) -> None:
    """Shape and values of {label: {coin: bars}}. A window whose coin set
    differs raises `coin_mismatch` (NOT_EVALUABLE for the equity series, as v1's
    load_windows; ValueError for inputs that must match an existing chain)."""
    if not isinstance(windows, Mapping):
        raise ValueError(f"windows must be a mapping {{label: {{coin: bars}}}}, got "
                         f"{type(windows).__name__}")
    for win, by_coin in windows.items():
        if not isinstance(by_coin, Mapping):
            raise ValueError(f"window {win!r}: expected {{coin: bars}}, got "
                             f"{type(by_coin).__name__}")
        if set(by_coin) != set(coins):
            raise coin_mismatch(f"window {win!r} has coins {sorted(by_coin, key=str)}, "
                                f"expected {sorted(coins, key=str)}")
        for c in coins:
            _check_bars(win, c, by_coin[c])


def _check_daily_returns(daily_returns) -> list:
    """[(date, return)] with strictly increasing dates (a duplicate day raises)
    and finite returns > -1."""
    out, prev = [], None
    for item in daily_returns:
        try:
            d, r = item
        except (TypeError, ValueError):
            raise ValueError(f"daily return {item!r} is not a (date, return) pair") from None
        if not isinstance(d, date) or isinstance(d, datetime):
            raise ValueError(f"daily return day {d!r} is not a date")
        if prev is not None and d <= prev:
            raise ValueError(f"daily returns: days are not strictly increasing "
                             f"({prev} then {d}; a duplicate day is refused)")
        if not _is_real(r) or not math.isfinite(float(r)) or float(r) <= -1.0:
            raise ValueError(f"daily return on {d}: {r!r} is not a finite return > -1")
        out.append((d, float(r)))
        prev = d
    return out


def _check_trade_record(rec) -> tuple:
    """(symbol, window, exit_reason) of one trade_diagnostics.json record."""
    if not isinstance(rec, Mapping):
        raise ValueError(f"trade record {rec!r} is not a mapping")
    sym, win, reason = rec.get("symbol"), rec.get("window"), rec.get("exit_reason")
    _hashable(sym, "trade record symbol")
    _hashable(win, "trade record window")
    if sym in (None, "") or win in (None, ""):
        raise ValueError(f"trade record lacks symbol/window: {dict(rec)!r}")
    _hashable(reason, "trade record exit_reason")
    if reason not in EXIT_REASONS:
        raise ValueError(f"trade record ({sym}, {win}) has exit_reason {reason!r}, not one "
                         f"of {sorted(EXIT_REASONS)}")
    return sym, win, reason


# ---------------------------------------------------------------------------
# Reader
# ---------------------------------------------------------------------------

def window_close_bars(path: Path) -> dict:
    """{timestamp (naive UTC): close} for one (coin, window) backtest, from its
    portfolio_states.csv `close` column (record_state copies the bar's OHLCV into
    every row, trading-bot/execution/portfolio_info.py). A copy of
    portfolio_daily.window_equity_bars' parsing (that file stays byte-identical):
    the SAME NOT_READY filter and timestamp handling, so both series have the
    same bars (tested). Fails loud on a missing column, a non-numeric /
    non-finite / non-positive close, or a timestamp repeated with a DIFFERENT
    close (a repeated row with the same close -- the engine's re-recorded final
    bar -- collapses, as window_equity_bars keeps one value per timestamp)."""
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        missing = {"timestamp", "regime", "close"} - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"buy-and-hold: {path} lacks column(s) {sorted(missing)}")
        seen: dict = {}
        for row in reader:
            if str(row["regime"]).strip().upper() == "NOT_READY":
                continue
            ts = datetime.fromisoformat(str(row["timestamp"]).strip())
            if ts.tzinfo is not None:
                ts = ts.astimezone(timezone.utc).replace(tzinfo=None)
            try:
                close = float(row["close"])
            except (TypeError, ValueError):
                raise ValueError(f"buy-and-hold: {path} has a non-numeric close at "
                                 f"{row['timestamp']!r}") from None
            if not math.isfinite(close) or close <= 0:
                raise ValueError(f"buy-and-hold: {path} has close {close!r} at "
                                 f"{row['timestamp']!r}")
            if ts in seen and seen[ts] != close:
                raise ValueError(f"buy-and-hold: {path} has two different closes "
                                 f"({seen[ts]!r}, {close!r}) at {row['timestamp']!r}")
            seen[ts] = close
    return {ts: seen[ts] for ts in sorted(seen)}


# ---------------------------------------------------------------------------
# G1/G2: window chaining
# ---------------------------------------------------------------------------

# How many days a window's first recorded day may fall after its nominal start
# before the bounds are refused as the wrong kind (see chain_windows). The
# smallest warm-up prefetch the engine uses is 2 x required_bars with
# required_bars >= 24 (AdvancedStrategy), i.e. 48 hourly bars = 2 days.
DEFAULT_WARMUP_DAYS = 2

# At most this many (window, coin, day) cells are spelled out in a
# NOT_EVALUABLE reason (the total count is always given).
_MAX_CELLS_SHOWN = 20


def _parse_protocol_date(value, what: str) -> date:
    if isinstance(value, datetime) or not isinstance(value, (str, date)):
        raise ValueError(f"{what}: {value!r} is not a YYYY-MM-DD date")
    if isinstance(value, date):
        return value
    try:
        if len(value) != 10:
            raise ValueError
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{what}: {value!r} is not a YYYY-MM-DD date") from None


def window_bounds_from_protocol(protocol: Mapping) -> dict:
    """{window label: (nominal start, nominal end)} from a protocol's
    `windows` list -- each entry {"label": ..., "test": {"start": "YYYY-MM-DD",
    "end": "YYYY-MM-DD"}}, the format of every protocols/*.json and of
    run_phase1_research._generate_monthly_windows; run_protocol.py reads the
    same `window["test"]["start"/"end"]`. `end` is INCLUSIVE by day at the
    engine (trading-bot/data/fetchers/base_fetcher.py _inclusive_end). These
    are the bounds chain_windows expects. NEVER pass a window manifest's start
    instead: the manifest records the warm-up PREFETCH start, before the
    protocol's test.start. Raises ValueError on a malformed protocol."""
    wins = protocol.get("windows") if isinstance(protocol, Mapping) else None
    if not isinstance(wins, list) or not wins:
        raise ValueError("protocol has no `windows` list")
    out: dict = {}
    for w in wins:
        if not isinstance(w, Mapping) or not isinstance(w.get("test"), Mapping):
            raise ValueError(f"protocol window {w!r} lacks label/test")
        label = w.get("label")
        _hashable(label, "protocol window label")
        if label in (None, "") or label in out:
            raise ValueError(f"protocol window label {label!r} is missing or repeated")
        start = _parse_protocol_date(w["test"].get("start"), f"window {label!r} test.start")
        end = _parse_protocol_date(w["test"].get("end"), f"window {label!r} test.end")
        if end < start:
            raise ValueError(f"window {label!r}: test.end {end} is before test.start {start}")
        out[label] = (start, end)
    return out


def load_protocol_window_bounds(path: Path) -> dict:
    """window_bounds_from_protocol of a protocol JSON file (explicit file reader)."""
    import json
    with open(path, encoding="utf-8") as f:
        return window_bounds_from_protocol(json.load(f))


def _check_bounds(window_bounds, windows) -> dict:
    if not isinstance(window_bounds, Mapping) or set(window_bounds) != set(windows):
        raise ValueError("window_bounds must map exactly the windows' labels to (start, end) "
                         "dates (window_bounds_from_protocol)")
    out, starts = {}, {}
    for w, b in window_bounds.items():
        try:
            s, e = b
        except (TypeError, ValueError):
            raise ValueError(f"window_bounds[{w!r}] = {b!r} is not a (start, end) pair") from None
        for d in (s, e):
            if not isinstance(d, date) or isinstance(d, datetime):
                raise ValueError(f"window_bounds[{w!r}] = {b!r}: {d!r} is not a date")
        if e < s:
            raise ValueError(f"window_bounds[{w!r}]: end {e} is before start {s}")
        if s in starts:
            raise ValueError(f"windows {starts[s]!r} and {w!r} have the same nominal start {s}")
        starts[s] = w
        out[w] = (s, e)
    return out


def _missing_cells(win, daily_w, coins, days) -> list:
    """(window, coin, day) for every coin lacking a daily close on each day."""
    return [(win, c, d) for d in days for c in coins if d not in daily_w[c]]


def _not_evaluable_cells(reason: str, cells: list):
    shown = ", ".join(f"({w!r}, {c!r}, {d})" for w, c, d in cells[:_MAX_CELLS_SHOWN])
    more = f", ... {len(cells) - _MAX_CELLS_SHOWN} more" if len(cells) > _MAX_CELLS_SHOWN else ""
    return PortfolioNotEvaluable(f"{reason}; {len(cells)} missing (window, coin, day) "
                                 f"cell(s): {shown}{more}")


def _days(first: date, last: date) -> list:
    return [date.fromordinal(o) for o in range(first.toordinal(), last.toordinal() + 1)]


def chain_windows(windows: Mapping, coins, window_bounds: Mapping, *,
                  warmup_days: int = DEFAULT_WARMUP_DAYS) -> dict:
    """One whole-test equal-weight portfolio curve from per-window backtests.

    windows: {window label: {coin: {naive UTC timestamp: equity}}} -- the shape
        portfolio_daily.load_windows returns (postRebalance_total_value,
        warm-up bars already dropped by its NOT_READY filter).
    coins: the coins every window must hold.
    window_bounds: REQUIRED {window label: (nominal start, nominal end)} -- the
        protocol's test.start / test.end (window_bounds_from_protocol), end
        inclusive by day. NEVER a window manifest's start: that is the warm-up
        PREFETCH start, earlier than test.start.
    warmup_days: a window whose first recorded day is more than this many days
        after its nominal start raises ValueError -- the bounds look like the
        manifest's prefetch start, not the protocol's test.start (the warm-up is
        never recorded). A smaller head shortfall is missing data
        (NOT_EVALUABLE, below). Pass the run's prefetch span in days when it is
        longer than DEFAULT_WARMUP_DAYS.

    Bounds checks (ValueError, an input bug): a recorded bar before a window's
    nominal start or after its nominal end; the head shortfall above; two
    windows with the same nominal start; a window whose nominal end is before
    a day already chained (it lies inside earlier windows).

    Per window (unchanged v1 definition, portfolio_daily.window_common_curve):
    the common UTC days (every coin has a daily close), >= 2 of them, covering
    >= PORTFOLIO_MIN_COMMON_DAY_COVERAGE of the union; each coin normalised at
    its close on the window's first common day (the ANCHOR); portfolio = mean.

    Completeness (governing rule: missing data is NOT_EVALUABLE, never a
    silently shorter or flatter test). Windows are chained in nominal-start
    order and every window must hold, as common days:
      * its nominal END (else its tail is missing: a coin's loss on the
        missing tail days would vanish -- second-round review finding 1);
      * the first window: its nominal START (else the head is missing);
      * a later window w, with `last_day` = the last chained day (= the latest
        nominal end so far, since every tail is complete):
          - nominal start <= last_day (the one-day overlap every protocol has
            today, "junction", or a longer one, "overlap": the EARLIEST window
            keeps its days): w must hold last_day, its JOIN day;
          - nominal start > last_day: a real protocol GAP ("gap"). w must hold
            its nominal start, where it joins; the chain is linked FLAT across
            the gap (G1) and the calendar days strictly between are
            n_gap_days.
    A missing day raises NOT_EVALUABLE naming every missing (window, coin, day)
    cell and their count. DEVIATION FROM G1: G1 says a missing junction day
    is "treated as a gap"; here it is NOT_EVALUABLE (code review finding 4) --
    linking flat would drop real P&L.

    Window w is scaled by level(join) / v_w(join) and owns its common days
    after the join day. A daily return is counted for a day d only when d and
    the previous day in the chain are consecutive calendar days of the SAME
    window (v_w(d) / v_w(d-1) - 1: bit-identical to
    portfolio_daily.consecutive_daily_returns); a multi-day step inside a
    window is still in the LEVEL, just not a daily return (n_multi_day_steps).

    Bars: each window contributes, between its close on the join day and its
    close on its nominal end, (a) its COMMON BARS (timestamps at which every
    coin has a bar) and (b) the daily-close level of every day it owns -- plus,
    for the first window and a gap window, the level at the join day itself.
    (b) puts the anchor level (1.0 for the first window) and each day's close
    in the curve even when a coin lacks the bar at another coin's close time
    (code review finding 5). When every coin has its close bar, (b) coincides
    with a common bar, so for a single such window this is exactly v1's
    drawdown bar set.

    Whole-test coverage (G2), against the NOMINAL span (first window's nominal
    start to the last nominal end, inclusive -- with the completeness checks
    above the chain spans exactly that): (number of daily returns + 1) must be
    >= WHOLE_TEST_MIN_COVERAGE x its calendar days, else NOT_EVALUABLE. It
    counts RETURN days, so one missing day inside a window costs two counted
    days (stricter than the per-window floor).

    Returns {coins, segments, daily_levels [(date, level)], daily_returns
    [(date, return)], bar_levels [(timestamp, level)], first_day, last_day,
    n_calendar_days, n_gap_days, n_gap_links, n_multi_day_steps, coverage}.
    `segments` is one dict per window in chain order: window, nominal_start,
    nominal_end, anchor, join_day, end_day, kind (first | junction | overlap |
    gap), scale, common (its common days), return_days, n_gap_days_before."""
    coins = _check_coins(coins)
    if not isinstance(windows, Mapping):
        raise ValueError(f"windows must be a mapping, got {type(windows).__name__}")
    if not windows:
        raise PortfolioNotEvaluable("no windows to chain")
    _check_windows(windows, coins)
    bounds = _check_bounds(window_bounds, windows)
    if not _is_int(warmup_days) or warmup_days < 0:
        raise ValueError(f"warmup_days must be a non-negative int, got {warmup_days!r}")

    for win, by_coin in windows.items():
        s, e = bounds[win]
        stamps = [t for c in coins for t in by_coin[c]]
        if not stamps:
            continue  # no bar at all: window_common_curve reports it (NOT_EVALUABLE)
        first_rec, last_rec = min(stamps).date(), max(stamps).date()
        if first_rec < s:
            raise ValueError(f"window {win!r} has a recorded bar on {first_rec}, before its "
                             f"nominal start {s} (wrong bounds?)")
        if last_rec > e:
            raise ValueError(f"window {win!r} has a recorded bar on {last_rec}, after its "
                             f"nominal end {e} (wrong bounds?)")
        if (first_rec - s).days > warmup_days:
            raise ValueError(
                f"window {win!r}: first recorded day {first_rec} is {(first_rec - s).days} "
                f"days after the given start {s} (> warmup_days={warmup_days}): the bounds "
                f"look like a window manifest's start (the warm-up prefetch start), not the "
                f"protocol's test.start -- pass window_bounds_from_protocol(...)")

    plans = []
    for win, by_coin in windows.items():
        wc = _pd.window_common_curve(win, by_coin, coins)
        plans.append((bounds[win][0], win, by_coin, wc))
    plans.sort(key=lambda p: p[0])

    segments: list = []
    daily_levels: list = []
    daily_returns: list = []
    bar_levels: list = []
    level = last_day = None
    n_gap_days = n_gap_links = n_multi = 0

    for nominal_start, win, by_coin, wc in plans:
        nominal_end = bounds[win][1]
        common, daily_w, anchor_val = wc["common"], wc["daily"], wc["anchor"]
        anchor = common[0]
        v = dict(zip(common, wc["curve"]))
        if common[-1] != nominal_end:
            raise _not_evaluable_cells(
                f"window {win!r}: last common day {common[-1]} is before its nominal end "
                f"{nominal_end} -- missing tail data would drop real P&L",
                _missing_cells(win, daily_w, coins,
                               _days(date.fromordinal(common[-1].toordinal() + 1), nominal_end)))
        gap_before = 0
        if last_day is None:
            if anchor != nominal_start:
                raise _not_evaluable_cells(
                    f"first window {win!r}: first common day {anchor} is after its nominal "
                    f"start {nominal_start} -- missing head data",
                    _missing_cells(win, daily_w, coins,
                                   _days(nominal_start, date.fromordinal(anchor.toordinal() - 1))))
            kind, join = "first", anchor
        elif nominal_start <= last_day:
            if nominal_end < last_day:
                raise ValueError(f"window {win!r} (nominal {nominal_start}..{nominal_end}) lies "
                                 f"inside earlier windows (chain already reaches {last_day})")
            kind, join = ("junction" if anchor == last_day else "overlap"), last_day
            if join not in v:
                raise _not_evaluable_cells(
                    f"window {win!r} has no common day on its junction day {join} -- missing "
                    f"data would drop real P&L from the chain",
                    _missing_cells(win, daily_w, coins, [join]))
        else:
            kind, join = "gap", nominal_start
            if join not in v:
                raise _not_evaluable_cells(
                    f"window {win!r} (after a protocol gap) has no common day on its nominal "
                    f"start day {join} -- missing head data",
                    _missing_cells(win, daily_w, coins,
                                   _days(nominal_start, date.fromordinal(anchor.toordinal() - 1))))
            gap_before = (join - last_day).days - 1
            n_gap_days += gap_before
            n_gap_links += 1

        scale = (1.0 if level is None else level) / v[join]
        close_ts = {d: max(daily_w[c][d][0] for c in coins) for d in common}
        join_ts, end_ts = close_ts[join], close_ts[common[-1]]
        points: dict = {}
        if kind in ("first", "gap"):
            daily_levels.append((join, scale * v[join]))
            points[join_ts] = scale * v[join]
        return_days = []
        prev = join
        for d in common:
            if d <= join:
                continue
            if (d - prev).days == 1:
                daily_returns.append((d, v[d] / v[prev] - 1.0))
                return_days.append(d)
            else:
                n_multi += 1
            daily_levels.append((d, scale * v[d]))
            prev = d
        level, last_day = daily_levels[-1][1], daily_levels[-1][0]

        inter = set.intersection(*(set(by_coin[c]) for c in coins))
        for t in inter:
            if join_ts < t <= end_ts:
                points[t] = scale * sum(by_coin[c][t] / anchor_val[c] for c in coins) / len(coins)
        for d in common:
            if d > join:
                points[close_ts[d]] = scale * v[d]
        for t in sorted(points):
            if bar_levels and t <= bar_levels[-1][0]:
                raise ValueError(f"chained bars are not strictly increasing at window "
                                 f"{win!r} ({bar_levels[-1][0]} then {t})")
            bar_levels.append((t, points[t]))

        segments.append({"window": win, "nominal_start": nominal_start,
                         "nominal_end": nominal_end, "anchor": anchor, "join_day": join,
                         "end_day": common[-1], "kind": kind, "scale": scale,
                         "common": list(common), "return_days": return_days,
                         "n_gap_days_before": gap_before})

    if not daily_returns:
        raise PortfolioNotEvaluable("no two chained days are consecutive calendar days of "
                                    "one window, so there is no daily return")
    first_day = plans[0][0]
    last_nominal = max(e for _s, e in bounds.values())
    if daily_levels[0][0] != first_day or last_day != last_nominal:
        raise ValueError(f"chain spans {daily_levels[0][0]}..{last_day}, not the nominal "
                         f"{first_day}..{last_nominal}")  # unreachable after the checks above
    n_calendar = (last_nominal - first_day).days + 1
    coverage = (len(daily_returns) + 1) / n_calendar
    if coverage < WHOLE_TEST_MIN_COVERAGE:
        raise PortfolioNotEvaluable(
            f"whole test: {len(daily_returns)} daily return(s) + 1 cover {coverage:.1%} of the "
            f"{n_calendar} calendar day(s) of the nominal span {first_day} to {last_nominal} "
            f"({n_gap_days} gap day(s) over {n_gap_links} gap link(s)), below "
            f"WHOLE_TEST_MIN_COVERAGE={WHOLE_TEST_MIN_COVERAGE}")
    return {"coins": list(coins), "segments": segments, "daily_levels": daily_levels,
            "daily_returns": daily_returns, "bar_levels": bar_levels,
            "first_day": first_day, "last_day": last_day, "n_calendar_days": n_calendar,
            "n_gap_days": n_gap_days, "n_gap_links": n_gap_links,
            "n_multi_day_steps": n_multi, "coverage": coverage}


# ---------------------------------------------------------------------------
# D-034: whole-test drawdown
# ---------------------------------------------------------------------------

def whole_test_max_drawdown(chain: dict) -> dict:
    """Largest peak-to-trough fall of the chained BAR-level curve over the whole
    test: 100 x max_t(1 - V_t / max_{s<=t} V_s), a positive percent (the
    running-peak formula of trading-bot/performance/bar_equity.max_drawdown_pct,
    sign flipped; tested equal on a shared fixture).

    Basis: BARS, not daily closes -- the same basis as today's per-window
    drawdown (run_phase1_research._portfolio_profit_metrics, D-020) and the
    engine's bar_equity drawdown, so intraday drops count; D-034 changes only
    the span (whole test instead of worst window), not the basis. The curve
    starts at the first window's anchor close (level 1.0).

    Returns {max_drawdown_pct, peak_ts, trough_ts, n_bars}."""
    bars = chain.get("bar_levels") if isinstance(chain, Mapping) else None
    if not bars:
        raise ValueError("whole-test drawdown: the chain has no bar_levels")
    peak = peak_ts = None
    dd, dd_peak_ts, dd_trough_ts = 0.0, bars[0][0], bars[0][0]
    prev_ts = None
    for ts, v in bars:
        if prev_ts is not None and ts <= prev_ts:
            raise ValueError(f"whole-test drawdown: bar timestamps not strictly increasing "
                             f"({prev_ts} then {ts})")
        v = _finite_positive(v, f"whole-test drawdown: bar level at {ts}")
        if peak is None or v > peak:
            peak, peak_ts = v, ts
        cur = 1.0 - v / peak
        if cur > dd:
            dd, dd_peak_ts, dd_trough_ts = cur, peak_ts, ts
        prev_ts = ts
    return {"max_drawdown_pct": dd * 100.0, "peak_ts": dd_peak_ts, "trough_ts": dd_trough_ts,
            "n_bars": len(bars)}


# ---------------------------------------------------------------------------
# G3 / D-036: whole-test Sharpe
# ---------------------------------------------------------------------------

def whole_test_sharpe(daily_returns) -> float:
    """mean / sample stdev (ddof 1) x sqrt(365), risk-free 0, of the chained
    daily returns [(date, return)] (chain_windows(...)["daily_returns"]).
    NOT_EVALUABLE below SHARPE_MIN_DAILY_RETURNS returns or at zero stdev."""
    rets = [r for _d, r in _check_daily_returns(daily_returns)]
    if len(rets) < SHARPE_MIN_DAILY_RETURNS:
        raise PortfolioNotEvaluable(f"whole-test Sharpe: {len(rets)} daily return(s), fewer "
                                    f"than SHARPE_MIN_DAILY_RETURNS={SHARPE_MIN_DAILY_RETURNS}")
    sd = statistics.stdev(rets)
    if sd == 0.0:
        raise PortfolioNotEvaluable(f"whole-test Sharpe: the {len(rets)} daily returns have "
                                    f"zero standard deviation")
    return statistics.mean(rets) / sd * math.sqrt(SHARPE_DAYS_PER_YEAR)


# ---------------------------------------------------------------------------
# G5 / D-035: whole-test trade count per coin
# ---------------------------------------------------------------------------

def whole_test_trade_counts(trade_records, results) -> dict:
    """Per-coin trade count over the whole test.

    trade_records: trade_diagnostics.json's `trades` list (written by
        tools/run_protocol.py, one record per closed trade with symbol / window
        / exit_reason, run_protocol.py::_compute_trade_records_for_window); pass
        [] when the file does not exist (run_protocol writes it only when there
        is at least one trade).
    results: protocol_result.results (REQUIRED) -- every (symbol, window) entry
        with core.trade_count. Every coin in results appears in the output (a
        coin with no trade reads 0); per (coin, window) the number of records
        must equal core.trade_count, else NOT_EVALUABLE (a broken artifact
        pair, e.g. the file missing while trades > 0); a record for a (coin,
        window) absent from results raises.

    Returns {coin: {"raw": all records, "end_of_window": records whose
    exit_reason is "end_of_window" (the engine's forced close at the window's
    last bar, run_protocol.py::_infer_exit_reason), "excluding_end_of_window":
    raw - end_of_window}}. The D-035 bar reads "excluding_end_of_window" (G5:
    a strategy that is always long gets one forced close per window and must
    not count it as a trade); both are returned so both can be recorded.
    A position held across a junction is one forced close (excluded) plus the
    continuation trade in the next window (counted): counted once."""
    if isinstance(trade_records, (str, bytes)) or isinstance(trade_records, Mapping) \
            or not hasattr(trade_records, "__iter__"):
        raise ValueError(f"trade_records must be a list of records, got "
                         f"{type(trade_records).__name__}")
    if isinstance(results, (str, bytes)) or isinstance(results, Mapping) \
            or not hasattr(results, "__iter__"):
        raise ValueError(f"results must be a list of protocol_result entries, got "
                         f"{type(results).__name__}")
    expected: dict = {}
    counts: dict = {}
    for r in results:
        if not isinstance(r, Mapping):
            raise ValueError(f"protocol_result.results entry {r!r} is not a mapping")
        sym, win = r.get("symbol"), r.get("window")
        _hashable(sym, "protocol_result.results symbol")
        _hashable(win, "protocol_result.results window")
        if sym in (None, "") or win in (None, ""):
            raise ValueError(f"protocol_result.results entry {r!r} lacks symbol/window")
        core = r.get("core")
        n = core.get("trade_count") if isinstance(core, Mapping) else None
        if not _is_int(n) or n < 0:
            raise ValueError(f"protocol_result.results entry ({sym}, {win}) has "
                             f"core.trade_count {n!r}")
        if (sym, win) in expected:
            raise ValueError(f"protocol_result.results lists ({sym}, {win}) twice")
        expected[(sym, win)] = int(n)
        counts.setdefault(sym, {"raw": 0, "end_of_window": 0})
    if not expected:
        raise ValueError("protocol_result.results is empty")
    per_slot: dict = {}
    for rec in trade_records:
        sym, win, reason = _check_trade_record(rec)
        if (sym, win) not in expected:
            raise ValueError(f"trade record for ({sym}, {win}), which is not in the results")
        per_slot[(sym, win)] = per_slot.get((sym, win), 0) + 1
        counts[sym]["raw"] += 1
        if reason == END_OF_WINDOW:
            counts[sym]["end_of_window"] += 1
    mismatch = [(k, per_slot.get(k, 0), n) for k, n in expected.items()
                if per_slot.get(k, 0) != n]
    if mismatch:
        raise PortfolioNotEvaluable(
            "trade records do not match core.trade_count for (coin, window) "
            + ", ".join(f"{k}: {got} record(s) vs {n}" for k, got, n in mismatch))
    return {sym: {"raw": c["raw"], "end_of_window": c["end_of_window"],
                  "excluding_end_of_window": c["raw"] - c["end_of_window"]}
            for sym, c in sorted(counts.items(), key=lambda kv: str(kv[0]))}


# ---------------------------------------------------------------------------
# G6 / D-037: chained buy-and-hold
# ---------------------------------------------------------------------------

def charged_fee_bps(symbol: str, cost_model: Mapping | None, commission_bps=None,
                    product: str = "spot") -> float:
    """One-way commission in bps the engine charged `symbol`, by the SAME
    lookup run_protocol uses to build run_backtest's commission_rate and each
    trade's cost_paid (tools/cost_helpers.resolve_fee_bps, of which
    resolve_commission_rate is the /10000 form: --commission-bps if set, else
    cost_model.yaml's fee_rate_bps for `product`). Raises when that function
    returns None (the engine then fell back to its own default rate, which this
    module will not guess). The caller must pass the run's own commission_bps /
    product (see the S2b scope note in the module docstring); NOT the window
    manifest's fee_bps (cost_model.json's table value)."""
    if cost_model is not None and not isinstance(cost_model, Mapping):
        raise ValueError("cost_model must be a mapping or None")
    if commission_bps is not None:
        _nonneg(commission_bps, "commission_bps")
    fee = _ch.resolve_fee_bps(symbol, cost_model, commission_bps, product)
    if fee is None:
        raise ValueError(f"no commission rate for {symbol!r} (product {product!r}): the "
                         f"engine would have used its default rate")
    return _nonneg(fee, f"commission for {symbol}")


def slippage_bps_for_symbol(slippage, symbol: str) -> float:
    """One-way slippage in bps the engine applied to `symbol`'s fills, from the
    slippage in effect for the run (a window manifest's
    config.cost_model.slippage_bps, written by trading-bot/core/launcher.py's
    cost-model provenance fold: the override if any, else cost_model.json's
    per-symbol table). Same resolution as
    trading-bot/execution/execution_handler.py::MockExecutionHandler._resolve_slippage_bps:
    a flat number applies to every symbol; a table gives symbol, else "default"."""
    _hashable(symbol, "symbol")
    if isinstance(slippage, Mapping):
        value = slippage.get(symbol)
        if value is None:
            value = slippage.get("default")
        if value is None:
            raise ValueError(f"slippage table has neither {symbol!r} nor 'default'")
        return _nonneg(value, f"slippage_bps[{symbol}]")
    return _nonneg(slippage, f"slippage_bps ({symbol})")


def chained_buy_and_hold(chain: dict, close_windows: Mapping, fee_bps: Mapping,
                         slippage_bps: Mapping) -> dict:
    """Strategy vs equal-weight buy-and-hold on the SAME chained schedule (G6).

    chain: chain_windows(equity windows, coins, window_bounds).
    close_windows: {window label: {coin: {timestamp: close}}} of the SAME
        backtests (window_close_bars), i.e. the prices the strategy saw. The
        window labels and coin sets must be the chain's, and each window's
        common days must equal the equity series' common days (else ValueError:
        the two series do not come from the same rows).
    fee_bps / slippage_bps: {coin: one-way bps} -- the commission the strategy
        was actually charged (charged_fee_bps) and the engine's slippage
        (slippage_bps_for_symbol).

    Both returns are total compounded returns on the CHAINED LEVEL (S1 Q3):
        strategy_total = final chained level - 1 (its costs are in the equity);
        buy_and_hold_gross = prod over windows of c_w(end) / c_w(join) - 1,
    where c_w is the equal-weight close curve normalised at the window anchor
    (equal weight reset at every window start, like the strategy book -- no
    rebalancing cost is charged to buy-and-hold for it, which favours
    buy-and-hold). Multi-day steps inside a window are INCLUDED in both (code
    review finding 1: excluding them hid a strategy's loss across a missing
    day); across a real protocol gap both are flat. One round trip per coin for
    the whole test, c_s = (fee_bps[s] + slippage_bps[s]) / 1e4 per side:
        buy_and_hold_total = (1 + buy_and_hold_gross) x mean_s[(1 - c_s)^2] - 1;
    excess = strategy - buy-and-hold (the D-037 bar passes iff excess > 0;
    that comparison is S2b's). The (1 - c)^2 form is S1 Q3's accepted formula;
    it treats slippage as a proportional cost per side like the fee (the
    engine prices a fill at close x (1 +/- slippage)), which differs from the
    exact fill arithmetic only at second order in c."""
    if not isinstance(chain, Mapping) or "segments" not in chain or "daily_levels" not in chain:
        raise ValueError("chained buy-and-hold: `chain` is not a chain_windows result")
    coins = _check_coins(chain["coins"])
    if not isinstance(close_windows, Mapping):
        raise ValueError("chained buy-and-hold: close_windows must be a mapping")
    labels = [s["window"] for s in chain["segments"]]
    if set(close_windows) != set(labels):
        raise ValueError(f"chained buy-and-hold: close windows {sorted(close_windows, key=str)} "
                         f"differ from the chained windows {sorted(labels, key=str)}")
    _check_windows(close_windows, coins, coin_mismatch=ValueError)
    if not isinstance(fee_bps, Mapping) or not isinstance(slippage_bps, Mapping):
        raise ValueError("chained buy-and-hold: fee_bps and slippage_bps must be mappings")
    costs = {}
    for c in coins:
        if c not in fee_bps or c not in slippage_bps:
            raise ValueError(f"chained buy-and-hold: no fee/slippage for coin {c!r}")
        costs[c] = (_nonneg(fee_bps[c], f"fee_bps[{c}]")
                    + _nonneg(slippage_bps[c], f"slippage_bps[{c}]")) / 10_000.0
        if costs[c] >= 1.0:
            raise ValueError(f"chained buy-and-hold: cost per side for {c!r} is >= 100%")

    bh_growth = 1.0
    for seg in chain["segments"]:
        try:
            wc = _pd.window_common_curve(seg["window"], close_windows[seg["window"]], coins)
        except PortfolioNotEvaluable as exc:
            raise ValueError(f"chained buy-and-hold: window {seg['window']!r} close series "
                             f"is inconsistent with its equity series ({exc})") from None
        if wc["common"] != seg["common"]:
            raise ValueError(f"chained buy-and-hold: window {seg['window']!r} close series "
                             f"has different common days than its equity series")
        cv = dict(zip(wc["common"], wc["curve"]))
        bh_growth *= cv[seg["end_day"]] / cv[seg["join_day"]]
    first_level, final_level = chain["daily_levels"][0][1], chain["daily_levels"][-1][1]
    strat_growth = _finite_positive(final_level, "final chained level") \
        / _finite_positive(first_level, "first chained level")
    cost_multiplier = sum((1.0 - costs[c]) ** 2 for c in coins) / len(coins)
    bh_total = bh_growth * cost_multiplier - 1.0
    strat_total = strat_growth - 1.0
    return {"strategy_total_return": strat_total,
            "buy_and_hold_gross_return": bh_growth - 1.0,
            "buy_and_hold_total_return": bh_total,
            "excess_return": strat_total - bh_total,
            "cost_multiplier": cost_multiplier,
            "cost_per_side_bps": {c: costs[c] * 10_000.0 for c in coins},
            "first_day": chain["first_day"], "last_day": chain["last_day"],
            "n_calendar_days": chain["n_calendar_days"],
            "n_daily_returns": len(chain["daily_returns"])}


# ---------------------------------------------------------------------------
# G7 / D-038: pooled realized edge / cost ratio with its trade floor
# ---------------------------------------------------------------------------

def pooled_edge_to_cost_ratio(trade_records, min_trades: int) -> dict:
    """The variant's POOLED realized gross edge / cost ratio for the D-038 bar,
    conservative both ways (second-round review finding 2):

      ratio = min(ratio over ALL trade records,
                  ratio over the records that are NOT end_of_window forced closes)

    so forced closes can neither lift the figure (a big forced-close gain,
    code review finding 6) nor hide a loss (a big forced-close loss). The
    trade FLOOR counts only the non-forced records (an always-long book gets
    one forced close per window and must not reach the floor by construction).

    Both ratios are tools/cost_helpers.realized_edge_to_cost_ratio_unrounded --
    the SAME computation run_protocol._aggregate_trade_diagnostics shows,
    rounded to 4 decimals, as realized_edge_to_cost_ratio -- UNROUNDED here
    (finding 7: a value just below the threshold must not round up to it).
    min_trades is the bar file's cost_edge_min_trades (D-039: 100).

    NOT_EVALUABLE when any record (forced closes included) lacks a measured
    cost (cost_paid None), when fewer than min_trades non-forced records
    remain, or when either ratio is None (zero mean cost). Raises ValueError
    on a malformed record. Returns {ratio, ratio_all_trades,
    ratio_excluding_end_of_window, n_trades, n_excluded_end_of_window}."""
    if not _is_int(min_trades) or min_trades < 1:
        raise ValueError(f"min_trades must be a positive int, got {min_trades!r}")
    if isinstance(trade_records, (str, bytes)) or isinstance(trade_records, Mapping) \
            or not hasattr(trade_records, "__iter__"):
        raise ValueError(f"trade_records must be a list of records, got "
                         f"{type(trade_records).__name__}")
    records, kept, n_forced = [], [], 0
    for rec in trade_records:
        sym, win, reason = _check_trade_record(rec)
        rr = rec.get("realized_return")
        if not _is_real(rr) or not math.isfinite(float(rr)):
            raise ValueError(f"trade record ({sym}, {win}) has realized_return {rr!r}")
        cost = rec.get("cost_paid")
        if cost is not None:
            _nonneg(cost, f"trade record ({sym}, {win}) cost_paid")
        records.append(rec)
        if reason == END_OF_WINDOW:
            n_forced += 1
        else:
            kept.append(rec)
    missing_cost = sum(1 for r in records if r.get("cost_paid") is None)
    if missing_cost:
        raise PortfolioNotEvaluable(f"edge/cost ratio: {missing_cost} of {len(records)} trade "
                                    f"record(s) lack a measured cost")
    if len(kept) < min_trades:
        raise PortfolioNotEvaluable(f"edge/cost ratio: {len(kept)} trade(s) after excluding "
                                    f"{n_forced} end_of_window forced close(s), fewer than "
                                    f"min_trades={min_trades}")
    r_all = _ch.realized_edge_to_cost_ratio_unrounded(records)
    r_kept = _ch.realized_edge_to_cost_ratio_unrounded(kept)
    if r_all is None or r_kept is None:
        raise PortfolioNotEvaluable("edge/cost ratio: zero mean measured cost")
    return {"ratio": min(float(r_all), float(r_kept)), "ratio_all_trades": float(r_all),
            "ratio_excluding_end_of_window": float(r_kept), "n_trades": len(kept),
            "n_excluded_end_of_window": n_forced}
