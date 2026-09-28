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
missing, so here a missing junction day is NOT_EVALUABLE instead. Only a real
protocol gap (the later window's nominal start is after the last chained day,
known only from `window_starts`) is linked flat as G1 says. Without
`window_starts`, any window starting after the last chained day is ambiguous
(gap or missing junction day) and is NOT_EVALUABLE.

What v2 adds:
  * chain_windows: one whole-test daily and bar-level curve out of the
    per-window curves (G1, G2);
  * whole_test_max_drawdown: drawdown on the chained BAR-level curve (D-034);
  * whole_test_sharpe: Sharpe of the chained daily returns (G3, D-036);
  * whole_test_trade_counts: per-coin trade count over the whole test, raw and
    without end_of_window forced closes (G5, D-035);
  * chained_buy_and_hold: strategy vs equal-weight buy-and-hold on the chained
    level (final level - 1, multi-day steps included), one round trip per coin
    (G6, D-037);
  * pooled_edge_to_cost_ratio: the shared realized_edge_to_cost_ratio
    (tools/cost_helpers.py) over the trades that are NOT end_of_window forced
    closes, with the min-trades floor on the same set (G7, D-038);
  * readers/lookups: window_close_bars, charged_fee_bps, slippage_bps_for_symbol.

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

def chain_windows(windows: Mapping, coins, window_starts: Mapping | None = None) -> dict:
    """One whole-test equal-weight portfolio curve from per-window backtests.

    windows: {window label: {coin: {naive UTC timestamp: equity}}} -- the shape
        portfolio_daily.load_windows returns (postRebalance_total_value,
        warm-up bars already dropped by its NOT_READY filter). Label order does
        not matter: windows are chained by anchor day.
    coins: the coins every window must hold.
    window_starts: optional {window label: nominal start date} (the protocol's
        window `test.start`). Needed to tell a real protocol gap from a
        missing junction day; without it, a window starting after the last
        chained day is NOT_EVALUABLE.

    Per window (unchanged v1 definition, portfolio_daily.window_common_curve):
    the common UTC days (every coin has a daily close), >= 2 of them, covering
    >= PORTFOLIO_MIN_COMMON_DAY_COVERAGE of the union; each coin normalised at
    its close on the window's first common day (the ANCHOR); portfolio = mean.

    Chaining. Windows are sorted by anchor; two windows with the same anchor
    -> NOT_EVALUABLE. The first window starts the chain at level 1.0 on its
    anchor (with window_starts: its anchor must be its nominal start day, else
    NOT_EVALUABLE -- missing data at the start). With `last_day` = the last day
    already in the chain, the next window w must hold its JOIN day J:
      * J = last_day when w is meant to overlap the chain (window_starts[w] <=
        last_day, or, without window_starts, its anchor <= last_day): the
        one-day overlap every protocol has today ("junction", anchor ==
        last_day) or a longer overlap ("overlap": the EARLIEST window keeps its
        days);
      * J = window_starts[w] when that nominal start is after last_day: a real
        protocol GAP ("gap"). The chain is linked FLAT from last_day to J and
        the calendar days strictly between them are reported in n_gap_days.
      * J missing from w's common days -> NOT_EVALUABLE (a missing junction day,
        or missing data at a gap window's start; deviation from G1's "treat as
        gap", see the module docstring). Without window_starts, anchor >
        last_day -> NOT_EVALUABLE (ambiguous).
    Window w is scaled by level(J) / v_w(J) and owns its common days after J.
    A daily return is counted for a day d only when d and the previous day in
    the chain are consecutive calendar days of the SAME window (v_w(d) /
    v_w(d-1) - 1: bit-identical to portfolio_daily.consecutive_daily_returns);
    a multi-day step inside a window is still in the LEVEL, just not a daily
    return (n_multi_day_steps).

    Bars: each window contributes, between its close on J and its close on its
    last common day, (a) its COMMON BARS (timestamps at which every coin has a
    bar) and (b) the daily-close level of every day it owns -- plus, for the
    first window and a gap window, the level at J itself. (b) puts the anchor
    level (1.0 for the first window) and each day's close in the curve even when
    a coin lacks the bar at another coin's close time (code review finding 5:
    otherwise a fall from the anchor to the first common bar is not a
    drawdown). When every coin has its close bar, (b) coincides with a common
    bar, so for a single such window this is exactly v1's drawdown bar set.

    Whole-test coverage (G2): (number of daily returns + 1) must be >=
    WHOLE_TEST_MIN_COVERAGE x calendar days from the first anchor to the last
    chained day (inclusive), else NOT_EVALUABLE; no daily return at all ->
    NOT_EVALUABLE. It counts RETURN days, so one missing day inside a window
    costs two counted days (stricter than the per-window floor).

    Returns {coins, segments, daily_levels [(date, level)], daily_returns
    [(date, return)], bar_levels [(timestamp, level)], first_day, last_day,
    n_calendar_days, n_gap_days, n_gap_links, n_multi_day_steps, coverage}.
    `segments` is one dict per window in chain order: window, anchor, join_day,
    end_day, kind (first | junction | overlap | gap), scale, common (its common
    days), return_days, n_gap_days_before."""
    coins = _check_coins(coins)
    if not isinstance(windows, Mapping) or not windows:
        if isinstance(windows, Mapping):
            raise PortfolioNotEvaluable("no windows to chain")
        raise ValueError(f"windows must be a mapping, got {type(windows).__name__}")
    _check_windows(windows, coins)
    if window_starts is not None:
        if not isinstance(window_starts, Mapping) or set(window_starts) != set(windows):
            raise ValueError("window_starts must map exactly the windows' labels to dates")
        for w, d in window_starts.items():
            if not isinstance(d, date) or isinstance(d, datetime):
                raise ValueError(f"window_starts[{w!r}] = {d!r} is not a date")

    plans = []
    for win, by_coin in windows.items():
        wc = _pd.window_common_curve(win, by_coin, coins)
        plans.append((wc["common"][0], win, by_coin, wc))
    anchors: dict = {}
    for anchor, win, _b, _w in plans:
        if anchor in anchors:
            raise PortfolioNotEvaluable(f"windows {anchors[anchor]!r} and {win!r} share the "
                                        f"anchor day {anchor}; the chain order is undefined")
        anchors[anchor] = win
        if window_starts is not None and anchor < window_starts[win]:
            raise ValueError(f"window {win!r} has data on {anchor}, before its nominal start "
                             f"{window_starts[win]}")
    plans.sort(key=lambda p: p[0])

    segments: list = []
    daily_levels: list = []
    daily_returns: list = []
    bar_levels: list = []
    level = last_day = None
    n_gap_days = n_gap_links = n_multi = 0

    for anchor, win, by_coin, wc in plans:
        common, daily_w, anchor_val = wc["common"], wc["daily"], wc["anchor"]
        v = dict(zip(common, wc["curve"]))
        gap_before = 0
        if last_day is None:
            if window_starts is not None and anchor != window_starts[win]:
                raise PortfolioNotEvaluable(
                    f"first window {win!r} has no common day on its start "
                    f"{window_starts[win]} (first common day {anchor}): missing data")
            kind, join = "first", anchor
        else:
            start = window_starts[win] if window_starts is not None else None
            if (start if start is not None else anchor) <= last_day:
                kind, join = ("junction" if anchor == last_day else "overlap"), last_day
            elif start is None:
                raise PortfolioNotEvaluable(
                    f"window {win!r} starts on {anchor}, after the last chained day "
                    f"{last_day}: without window_starts a protocol gap cannot be told "
                    f"from a missing junction day")
            else:
                kind, join = "gap", start
            if join not in v:
                what = ("its junction day" if kind != "gap" else "its nominal start day")
                raise PortfolioNotEvaluable(
                    f"window {win!r} has no common day on {what} {join} (its common days "
                    f"start {anchor}): missing data would drop real P&L from the chain")
            if kind == "gap":
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

        segments.append({"window": win, "anchor": anchor, "join_day": join,
                         "end_day": common[-1], "kind": kind, "scale": scale,
                         "common": list(common), "return_days": return_days,
                         "n_gap_days_before": gap_before})

    if not daily_returns:
        raise PortfolioNotEvaluable("no two chained days are consecutive calendar days of "
                                    "one window, so there is no daily return")
    first_day = daily_levels[0][0]
    n_calendar = (last_day - first_day).days + 1
    coverage = (len(daily_returns) + 1) / n_calendar
    if coverage < WHOLE_TEST_MIN_COVERAGE:
        raise PortfolioNotEvaluable(
            f"whole test: {len(daily_returns)} daily return(s) + 1 cover {coverage:.1%} of the "
            f"{n_calendar} calendar day(s) from {first_day} to {last_day} ({n_gap_days} gap "
            f"day(s) over {n_gap_links} gap link(s)), below "
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
    function run_protocol uses to build run_backtest's commission_rate
    (tools/cost_helpers.resolve_commission_rate: --commission-bps if set, else
    cost_model.yaml's fee_rate_bps for `product`). Raises when that function
    returns None (the engine then fell back to its own default rate, which this
    module will not guess). The caller must pass the run's own commission_bps /
    product (see the S2b scope note in the module docstring); NOT the window
    manifest's fee_bps (cost_model.json's table value)."""
    if cost_model is not None and not isinstance(cost_model, Mapping):
        raise ValueError("cost_model must be a mapping or None")
    if commission_bps is not None:
        _nonneg(commission_bps, "commission_bps")
    rate = _ch.resolve_commission_rate(symbol, cost_model, commission_bps, product)
    if rate is None:
        raise ValueError(f"no commission rate for {symbol!r} (product {product!r}): the "
                         f"engine would have used its default rate")
    return _nonneg(rate * 10_000.0, f"commission for {symbol}")


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

    chain: chain_windows(equity windows, coins, ...).
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
    """The variant's POOLED realized gross edge / cost ratio, with the floor,
    over its trade records EXCLUDING end_of_window forced closes (code review
    finding 6: a forced close at every window end is not a trade the strategy
    chose; an always-long book would otherwise reach the floor by construction).

    The ratio is tools/cost_helpers.realized_edge_to_cost_ratio -- the SAME
    function run_protocol._aggregate_trade_diagnostics uses for its
    realized_edge_to_cost_ratio (mean gross bps over mean cost_paid bps) -- on
    that reduced set; no second formula. min_trades is the bar file's
    cost_edge_min_trades (D-039: 100).

    NOT_EVALUABLE when fewer than min_trades records remain, when any remaining
    record lacks a measured cost (cost_paid None), or when the ratio is None
    (zero mean cost). Raises ValueError on a malformed record. Returns {ratio,
    n_trades, n_excluded_end_of_window}."""
    if not _is_int(min_trades) or min_trades < 1:
        raise ValueError(f"min_trades must be a positive int, got {min_trades!r}")
    if isinstance(trade_records, (str, bytes)) or isinstance(trade_records, Mapping) \
            or not hasattr(trade_records, "__iter__"):
        raise ValueError(f"trade_records must be a list of records, got "
                         f"{type(trade_records).__name__}")
    kept, n_forced = [], 0
    for rec in trade_records:
        sym, win, reason = _check_trade_record(rec)
        if reason == END_OF_WINDOW:
            n_forced += 1
            continue
        rr = rec.get("realized_return")
        if not _is_real(rr) or not math.isfinite(float(rr)):
            raise ValueError(f"trade record ({sym}, {win}) has realized_return {rr!r}")
        cost = rec.get("cost_paid")
        if cost is not None:
            _nonneg(cost, f"trade record ({sym}, {win}) cost_paid")
        kept.append(rec)
    missing_cost = sum(1 for r in kept if r.get("cost_paid") is None)
    if missing_cost:
        raise PortfolioNotEvaluable(f"edge/cost ratio: {missing_cost} of {len(kept)} trade(s) "
                                    f"(end_of_window closes excluded) lack a measured cost")
    if len(kept) < min_trades:
        raise PortfolioNotEvaluable(f"edge/cost ratio: {len(kept)} trade(s) with a measured cost "
                                    f"after excluding {n_forced} end_of_window forced close(s), "
                                    f"fewer than min_trades={min_trades}")
    ratio = _ch.realized_edge_to_cost_ratio(kept)
    if ratio is None:
        raise PortfolioNotEvaluable("edge/cost ratio: zero mean measured cost")
    return {"ratio": float(ratio), "n_trades": len(kept), "n_excluded_end_of_window": n_forced}
