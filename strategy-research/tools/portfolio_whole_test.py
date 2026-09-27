"""
Whole-test ("profit bars v2") portfolio functions -- E-062 S2a.

PURE FUNCTIONS ONLY. Nothing in the orchestrator calls this module yet (the
wiring, the flag `orchestrator.profit_bars_v2.enabled` and the bar values are
S2b). Definitions: engineering/roadmap/E-062/S1_FINDINGS.md, decisions G1-G9 and
G11 (accepted in that file's "Decision" section), D-034..D-039 (engineering/DECISION_LOG.md).

WHY A SIBLING MODULE and not more code in tools/portfolio_daily.py:
portfolio_daily.py is the v1 definition that the flag-off profit bars
(run_phase1_research._portfolio_profit_metrics) and the composition
(tools/composition.load_block_daily_returns) read today. Keeping it
byte-for-byte unchanged makes "flag-off behaviour is untouched" true by
construction, not by review. This module IMPORTS the v1 primitives
(window_common_curve: common days, per-window 0.9 coverage floor, anchor
normalisation; daily_closes; PortfolioNotEvaluable) so the two versions share
one definition of a window's portfolio and can only differ in what v2 adds:
the chaining across windows.

What v2 adds:
  * chain_windows: one whole-test daily and bar-level curve out of the
    per-window curves (G1, G2);
  * whole_test_max_drawdown: drawdown on the chained BAR-level curve (D-034);
  * whole_test_sharpe: Sharpe of the chained daily returns (G3, D-036);
  * whole_test_trade_counts: per-coin trade count over the whole test, raw and
    without end_of_window forced closes (G5, D-035);
  * chained_buy_and_hold: equal-weight buy-and-hold over the SAME counted days,
    one round trip per coin (G6, D-037);
  * pooled_edge_to_cost_ratio: the existing realized_edge_to_cost_ratio with
    the 100-trade floor (G7, D-038);
  * readers/lookups: window_close_bars, spot_fee_rate_bps, slippage_bps_for_symbol.

NOT_EVALUABLE is signalled by raising portfolio_daily.PortfolioNotEvaluable
(message = the reason), like the v1 module. Malformed input (NaN, non-positive
value, unsorted timestamps, duplicate days, unknown exit_reason, ...) raises a
plain ValueError -- never NOT_EVALUABLE, never a silent default.

No lookahead: every value comes from inside the backtest windows the caller
passes (per-window equity/close bars, per-window trade records, the protocol
result's trade summary). Nothing is fetched, nothing past a window's last bar
is read, and nothing here reads anything under local_data/holdout_sealed/.
"""
from __future__ import annotations

import csv
import math
import statistics
from collections.abc import Mapping
from datetime import date, datetime, timezone
from pathlib import Path

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

def _finite_positive(value, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{what}: {value!r} is not a number")
    v = float(value)
    if not math.isfinite(v) or v <= 0:
        raise ValueError(f"{what}: {value!r} is not a finite positive number")
    return v


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


def _check_windows(windows, coins) -> list:
    if not isinstance(windows, Mapping):
        raise ValueError(f"windows must be a mapping {{label: {{coin: bars}}}}, got "
                         f"{type(windows).__name__}")
    coins = list(coins)
    if not coins or len(set(coins)) != len(coins):
        raise ValueError(f"coins must be a non-empty list without duplicates, got {coins!r}")
    if not windows:
        raise PortfolioNotEvaluable("no windows to chain")
    for win, by_coin in windows.items():
        if not isinstance(by_coin, Mapping):
            raise ValueError(f"window {win!r}: expected {{coin: bars}}, got "
                             f"{type(by_coin).__name__}")
        if set(by_coin) != set(coins):
            raise PortfolioNotEvaluable(f"window {win!r} has coins {sorted(by_coin, key=str)}, "
                                        f"expected {sorted(coins, key=str)}")
        for c in coins:
            _check_bars(win, c, by_coin[c])
    return coins


def _check_daily_returns(daily_returns) -> list:
    """[(date, return)] with strictly increasing dates (a duplicate day raises)
    and finite returns > -1."""
    out, prev = [], None
    for item in daily_returns:
        try:
            d, r = item
        except (TypeError, ValueError):
            raise ValueError(f"daily return {item!r} is not a (date, return) pair")
        if not isinstance(d, date) or isinstance(d, datetime):
            raise ValueError(f"daily return day {d!r} is not a date")
        if prev is not None and d <= prev:
            raise ValueError(f"daily returns: days are not strictly increasing "
                             f"({prev} then {d}; a duplicate day is refused)")
        if isinstance(r, bool) or not isinstance(r, (int, float)) or not math.isfinite(r) \
                or r <= -1.0:
            raise ValueError(f"daily return on {d}: {r!r} is not a finite return > -1")
        out.append((d, float(r)))
        prev = d
    return out


# ---------------------------------------------------------------------------
# Reader
# ---------------------------------------------------------------------------

def window_close_bars(path: Path) -> dict:
    """{timestamp (naive UTC): close} for one (coin, window) backtest, from its
    portfolio_states.csv `close` column (record_state copies the bar's OHLCV into
    every row, trading-bot/execution/portfolio_info.py). Warm-up bars (regime
    NOT_READY) are dropped with the SAME filter as
    portfolio_daily.window_equity_bars, so the two series share their bars.
    Fails loud on a missing column, a non-numeric / non-finite / non-positive
    close, or a timestamp repeated with a DIFFERENT close (a repeated row with
    the same close -- the engine's re-recorded final bar -- collapses, exactly
    as window_equity_bars keeps one value per timestamp)."""
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
                                 f"{row['timestamp']!r}")
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

def chain_windows(windows: Mapping, coins) -> dict:
    """One whole-test equal-weight portfolio curve from per-window backtests.

    windows: {window label: {coin: {naive UTC timestamp: equity}}} -- the shape
        portfolio_daily.load_windows returns (postRebalance_total_value,
        warm-up bars already dropped). Order of the labels does not matter:
        windows are chained by their anchor day.
    coins: the coins every window must hold.

    Per window (unchanged v1 definition, portfolio_daily.window_common_curve):
    the common UTC days (every coin has a daily close), >= 2 of them, covering
    >= PORTFOLIO_MIN_COMMON_DAY_COVERAGE of the union; each coin normalised at
    its close on the window's first common day (the ANCHOR); portfolio = mean.

    Chaining (G1). Windows are sorted by anchor; two windows with the same
    anchor -> NOT_EVALUABLE. The first window starts the chain at level 1.0 on
    its anchor. With `last_day` = the last day already in the chain, the next
    window w JOINS at:
      * its anchor, when anchor == last_day (the one-day overlap every protocol
        has today: `end` is inclusive by day and equals the next `start`);
      * last_day, when anchor < last_day (an overlap longer than one day: the
        EARLIEST window keeps its days) and last_day is one of w's common days;
      * otherwise it is a GAP: w joins at its first common day after last_day
        (its anchor for a real gap, or the day after a junction day that w
        lacks -- G1 "a missing junction day is treated as a gap"). The chain is
        linked FLAT across it (level unchanged), and no return is counted
        between last_day and the join day. The calendar days strictly between
        them are reported in n_gap_days. A window with no common day after
        last_day contributes nothing (kind "contained").
    Window w is scaled by level(join) / v_w(join) and owns its common days
    after the join day. A daily return is counted for a day d only when d and
    the previous day in the chain are consecutive calendar days of the SAME
    window (v_w(d) / v_w(d-1) - 1: bit-identical to
    portfolio_daily.consecutive_daily_returns); a multi-day step inside a
    window is not a daily return (n_multi_day_steps).

    Bars: each window contributes its COMMON BARS (timestamps at which every
    coin has a bar) from its close on the join day onwards (the first window,
    and a window after a gap, include that bar; a junction window starts
    strictly after it, since the earlier window owns it) up to its close on its
    last common day, scaled like the daily curve. For a single window this is
    exactly v1's per-window drawdown bar set.

    Whole-test coverage (G2): (number of daily returns + 1) must be >=
    WHOLE_TEST_MIN_COVERAGE x calendar days from the first anchor to the last
    chained day (inclusive), else NOT_EVALUABLE; no daily return at all ->
    NOT_EVALUABLE.

    Returns {coins, segments, daily_levels [(date, level)], daily_returns
    [(date, return)], bar_levels [(timestamp, level)], first_day, last_day,
    n_calendar_days, n_gap_days, n_gap_links, n_multi_day_steps, coverage}.
    `segments` is one dict per window in chain order: window, anchor, join_day,
    end_day, kind (first | junction | overlap | gap | contained), scale,
    common (its common days), return_days, n_gap_days_before."""
    coins = _check_windows(windows, coins)
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
            kind, join = "first", anchor
        elif anchor == last_day:
            kind, join = "junction", anchor
        elif anchor < last_day and last_day in v:
            kind, join = "overlap", last_day
        else:
            later = [d for d in common if d > last_day]
            if not later:
                segments.append({"window": win, "anchor": anchor, "join_day": None,
                                 "end_day": None, "kind": "contained", "scale": None,
                                 "common": list(common), "return_days": [],
                                 "n_gap_days_before": 0})
                continue
            kind, join = "gap", later[0]
            gap_before = (join - last_day).days - 1
            n_gap_days += gap_before
            n_gap_links += 1

        scale = (1.0 if level is None else level) / v[join]
        if kind in ("first", "gap"):
            daily_levels.append((join, scale * v[join]))
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

        join_ts = max(daily_w[c][join][0] for c in coins)
        end_ts = max(daily_w[c][common[-1]][0] for c in coins)
        inter = set.intersection(*(set(by_coin[c]) for c in coins))
        if kind in ("first", "gap"):
            wbars = sorted(t for t in inter if join_ts <= t <= end_ts)
        else:
            wbars = sorted(t for t in inter if join_ts < t <= end_ts)
        if kind in ("first", "gap") and not wbars:
            raise PortfolioNotEvaluable(f"window {win!r} has no bar, from its close on "
                                        f"{join} onwards, at which every coin has a value")
        for t in wbars:
            val = scale * sum(by_coin[c][t] / anchor_val[c] for c in coins) / len(coins)
            if bar_levels and t <= bar_levels[-1][0]:
                raise ValueError(f"chained bars are not strictly increasing at window "
                                 f"{win!r} ({bar_levels[-1][0]} then {t})")
            bar_levels.append((t, val))

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
    test: 100 x max_t(1 - V_t / max_{s<=t} V_s), a positive percent.

    Basis: BARS, not daily closes -- the same basis as today's per-window
    drawdown (run_phase1_research._portfolio_profit_metrics, D-020) and the
    engine's bar_equity drawdown, so intraday drops count; D-034 changes only
    the span (whole test instead of worst window), not the basis. The first
    window's bars start at its anchor close (level 1.0 for one coin).

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
        _finite_positive(v, f"whole-test drawdown: bar level at {ts}")
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

def whole_test_trade_counts(trade_records, results=None) -> dict:
    """Per-coin trade count over the whole test from trade_diagnostics.json's
    `trades` records (written by tools/run_protocol.py, one record per closed
    trade with symbol / window / exit_reason, run_protocol.py:604-716).

    Returns {coin: {"raw": all records, "end_of_window": records whose
    exit_reason is "end_of_window" (the engine's forced close at the window's
    last bar, run_protocol.py::_infer_exit_reason), "excluding_end_of_window":
    raw - end_of_window}}. The D-035 bar reads "excluding_end_of_window" (G5:
    a strategy that is always long gets one forced close per window and must
    not count it as a trade); both are returned so both can be recorded.

    results (optional): protocol_result.results -- every (symbol, window) entry
    with core.trade_count. When given, every coin in results appears in the
    output (0 when it has no record), and per (coin, window) the number of
    records must equal core.trade_count, else NOT_EVALUABLE (a broken artifact
    pair); a record for a (coin, window) absent from results raises. When
    omitted, only the coins present in the records appear.

    Raises ValueError on a malformed record (not a mapping, symbol/window
    missing, exit_reason missing or outside EXIT_REASONS)."""
    if trade_records is None:
        trade_records = []
    per_slot: dict = {}
    counts: dict = {}
    for rec in trade_records:
        if not isinstance(rec, Mapping):
            raise ValueError(f"trade record {rec!r} is not a mapping")
        sym, win, reason = rec.get("symbol"), rec.get("window"), rec.get("exit_reason")
        if sym in (None, "") or win in (None, ""):
            raise ValueError(f"trade record lacks symbol/window: {dict(rec)!r}")
        if reason not in EXIT_REASONS:
            raise ValueError(f"trade record ({sym}, {win}) has exit_reason {reason!r}, not one "
                             f"of {sorted(EXIT_REASONS)}")
        per_slot[(sym, win)] = per_slot.get((sym, win), 0) + 1
        c = counts.setdefault(sym, {"raw": 0, "end_of_window": 0})
        c["raw"] += 1
        if reason == END_OF_WINDOW:
            c["end_of_window"] += 1
    if results is not None:
        expected: dict = {}
        for r in results:
            if not isinstance(r, Mapping) or r.get("symbol") in (None, "") \
                    or r.get("window") in (None, ""):
                raise ValueError(f"protocol_result.results entry {r!r} lacks symbol/window")
            core = r.get("core")
            n = core.get("trade_count") if isinstance(core, Mapping) else None
            if isinstance(n, bool) or not isinstance(n, int) or n < 0:
                raise ValueError(f"protocol_result.results entry ({r['symbol']}, "
                                 f"{r['window']}) has core.trade_count {n!r}")
            key = (r["symbol"], r["window"])
            if key in expected:
                raise ValueError(f"protocol_result.results lists ({key[0]}, {key[1]}) twice")
            expected[key] = n
            counts.setdefault(r["symbol"], {"raw": 0, "end_of_window": 0})
        extra = sorted(set(per_slot) - set(expected), key=str)
        if extra:
            raise ValueError(f"trade records for (coin, window) not in the results: {extra}")
        mismatch = sorted((k, per_slot.get(k, 0), n) for k, n in expected.items()
                          if per_slot.get(k, 0) != n)
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

def spot_fee_rate_bps(cost_model: Mapping, symbol: str) -> float:
    """One-way commission in bps the engine charged `symbol`: cost_model.yaml's
    top-level fee_rate_bps[symbol], else its "default" -- the same lookup as
    tools/run_protocol.py::_commission_rate_for_symbol (product "spot", the
    only one the pipeline uses) which feeds run_backtest's commission_rate.
    NOT the window manifest's fee_bps (cost_model.json's table value, which is
    not what the engine charged when run_protocol passes commission_rate).
    Raises instead of falling back to the engine default."""
    fees = cost_model.get("fee_rate_bps") if isinstance(cost_model, Mapping) else None
    if not isinstance(fees, Mapping):
        raise ValueError("cost model has no fee_rate_bps table")
    rate = fees.get(symbol)
    if rate is None:
        rate = fees.get("default")
    if rate is None:
        raise ValueError(f"cost model fee_rate_bps has neither {symbol!r} nor 'default'")
    return _nonneg(rate, f"fee_rate_bps[{symbol}]")


def slippage_bps_for_symbol(slippage, symbol: str) -> float:
    """One-way slippage in bps the engine applied to `symbol`'s fills, from the
    slippage in effect for the run (a window manifest's
    config.cost_model.slippage_bps, written by trading-bot/core/launcher.py's
    cost-model provenance fold: the override if any, else cost_model.json's
    per-symbol table). Same resolution as
    trading-bot/execution/execution_handler.py::MockExecutionHandler._resolve_slippage_bps:
    a flat number applies to every symbol; a table gives symbol, else "default"."""
    if isinstance(slippage, Mapping):
        value = slippage.get(symbol)
        if value is None:
            value = slippage.get("default")
        if value is None:
            raise ValueError(f"slippage table has neither {symbol!r} nor 'default'")
        return _nonneg(value, f"slippage_bps[{symbol}]")
    return _nonneg(slippage, f"slippage_bps ({symbol})")


def _nonneg(value, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) \
            or not math.isfinite(value) or value < 0:
        raise ValueError(f"{what}: {value!r} is not a finite non-negative number")
    return float(value)


def chained_buy_and_hold(chain: dict, close_windows: Mapping, fee_bps: Mapping,
                         slippage_bps: Mapping) -> dict:
    """Strategy vs equal-weight buy-and-hold over the SAME counted days (G6).

    chain: chain_windows(equity windows, coins).
    close_windows: {window label: {coin: {timestamp: close}}} of the SAME
        backtests (window_close_bars), i.e. the prices the strategy saw. The
        window labels must be the chain's, and each window's common days must
        equal the equity series' common days (else ValueError: the two series
        do not come from the same rows).
    fee_bps / slippage_bps: {coin: one-way bps} (spot_fee_rate_bps,
        slippage_bps_for_symbol).

    Buy-and-hold uses the chain's own schedule: per window the same common
    days, anchor and counted return days, with each coin's close normalised at
    the window anchor (equal weight reset at every window start, like the
    strategy book -- no rebalancing cost is charged to buy-and-hold for it,
    which favours buy-and-hold). One round trip per coin for the whole test,
    c_s = (fee_bps[s] + slippage_bps[s]) / 1e4 per side:
        buy_and_hold_total = prod_d(1 + r_bh,d) x mean_s[(1 - c_s)^2] - 1
        strategy_total     = prod_d(1 + r_d) - 1   (costs already in the equity)
    over the chain's counted daily returns d; excess = strategy - buy-and-hold
    (the D-037 bar passes iff excess > 0; that comparison is S2b's).
    The (1 - c)^2 form is S1 Q3's accepted formula; it treats slippage as a
    proportional cost per side like the fee (the engine prices a fill at
    close x (1 +/- slippage)), which differs from the exact fill arithmetic
    only at second order in c."""
    if not isinstance(chain, Mapping) or "segments" not in chain:
        raise ValueError("chained buy-and-hold: `chain` is not a chain_windows result")
    coins = list(chain["coins"])
    if not isinstance(close_windows, Mapping):
        raise ValueError("chained buy-and-hold: close_windows must be a mapping")
    labels = {s["window"] for s in chain["segments"]}
    if set(close_windows) != labels:
        raise ValueError(f"chained buy-and-hold: close windows {sorted(close_windows, key=str)} "
                         f"differ from the chained windows {sorted(labels, key=str)}")
    _check_windows(close_windows, coins)
    costs = {}
    for c in coins:
        if c not in fee_bps or c not in slippage_bps:
            raise ValueError(f"chained buy-and-hold: no fee/slippage for coin {c!r}")
        costs[c] = (_nonneg(fee_bps[c], f"fee_bps[{c}]")
                    + _nonneg(slippage_bps[c], f"slippage_bps[{c}]")) / 10_000.0
        if costs[c] >= 1.0:
            raise ValueError(f"chained buy-and-hold: cost per side for {c!r} is >= 100%")

    bh_growth = 1.0
    n_days = 0
    for seg in chain["segments"]:
        if not seg["return_days"]:
            continue
        wc = _pd.window_common_curve(seg["window"], close_windows[seg["window"]], coins)
        if wc["common"] != seg["common"]:
            raise ValueError(f"chained buy-and-hold: window {seg['window']!r} close series "
                             f"has different common days than its equity series")
        cv = dict(zip(wc["common"], wc["curve"]))
        for d in seg["return_days"]:
            prev = date.fromordinal(d.toordinal() - 1)
            bh_growth *= cv[d] / cv[prev]
            n_days += 1
    strat_growth = 1.0
    for _d, r in _check_daily_returns(chain["daily_returns"]):
        strat_growth *= 1.0 + r
    if n_days != len(chain["daily_returns"]):
        raise ValueError(f"chained buy-and-hold: {n_days} buy-and-hold day(s) vs "
                         f"{len(chain['daily_returns'])} strategy daily return(s)")
    cost_multiplier = sum((1.0 - costs[c]) ** 2 for c in coins) / len(coins)
    bh_total = bh_growth * cost_multiplier - 1.0
    strat_total = strat_growth - 1.0
    return {"strategy_total_return": strat_total,
            "buy_and_hold_gross_return": bh_growth - 1.0,
            "buy_and_hold_total_return": bh_total,
            "excess_return": strat_total - bh_total,
            "cost_multiplier": cost_multiplier,
            "cost_per_side_bps": {c: costs[c] * 10_000.0 for c in coins},
            "n_days": n_days}


# ---------------------------------------------------------------------------
# G7 / D-038: pooled realized edge / cost ratio with its trade floor
# ---------------------------------------------------------------------------

def pooled_edge_to_cost_ratio(trade_diagnostics_summary, min_trades: int) -> dict:
    """The variant's POOLED realized gross edge / cost ratio, with the floor.

    Reuses the existing figure -- trade_diagnostics_summary
    ["realized_edge_to_cost_ratio"], computed once by
    tools/run_protocol.py::_aggregate_trade_diagnostics (mean gross bps over
    mean cost_paid bps, pooled over every trade record of the variant that has
    a measured cost) -- and does NOT recompute it. min_trades is the bar
    file's cost_edge_min_trades (D-039: 100).

    NOT_EVALUABLE when the summary is missing/empty, the ratio is None (no
    trade, or zero cost), cost_components_measured.fees is not True (some
    trade lacks a measured cost), or per_trade_expectancy_bps.n (the number of
    records -- equal to the ratio's record count once fees is True) is below
    min_trades. Returns {ratio, n_trades}."""
    if isinstance(min_trades, bool) or not isinstance(min_trades, int) or min_trades < 1:
        raise ValueError(f"min_trades must be a positive int, got {min_trades!r}")
    if not trade_diagnostics_summary:
        raise PortfolioNotEvaluable("edge/cost ratio: no trade_diagnostics_summary (no trade "
                                    "records)")
    if not isinstance(trade_diagnostics_summary, Mapping):
        raise ValueError("trade_diagnostics_summary is not a mapping")
    fees = (trade_diagnostics_summary.get("cost_components_measured") or {}).get("fees")
    if fees is not True:
        raise PortfolioNotEvaluable(f"edge/cost ratio: cost_components_measured.fees is "
                                    f"{fees!r} -- not every trade has a measured cost")
    n = (trade_diagnostics_summary.get("per_trade_expectancy_bps") or {}).get("n")
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"trade_diagnostics_summary per_trade_expectancy_bps.n is {n!r}")
    if n < min_trades:
        raise PortfolioNotEvaluable(f"edge/cost ratio: {n} pooled trade(s) with a measured "
                                    f"cost, fewer than min_trades={min_trades}")
    ratio = trade_diagnostics_summary.get("realized_edge_to_cost_ratio")
    if ratio is None:
        raise PortfolioNotEvaluable("edge/cost ratio: realized_edge_to_cost_ratio is None "
                                    "(zero measured cost)")
    if isinstance(ratio, bool) or not isinstance(ratio, (int, float)) or not math.isfinite(ratio):
        raise ValueError(f"realized_edge_to_cost_ratio is {ratio!r}")
    return {"ratio": float(ratio), "n_trades": n}
