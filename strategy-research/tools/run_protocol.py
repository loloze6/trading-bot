"""
run_protocol.py — walk-forward protocol runner.

CLI (run from repo root or strategy-research/):
  python strategy-research/tools/run_protocol.py <config_path> <protocol_path>
  python strategy-research/tools/run_protocol.py <config_path> <protocol_path> --holdout --i-understand
"""
import sys
import contextlib
import copy
import os
import csv
import json
import math
import argparse
import statistics
import re
import collections
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import NoReturn

_HERE = os.path.dirname(os.path.abspath(__file__))   # strategy-research/tools/
_SR   = os.path.dirname(_HERE)                        # strategy-research/
_REPO = os.path.dirname(_SR)                          # repo root
_TBOT = os.path.join(_REPO, "trading-bot")            # trading-bot/

if _TBOT not in sys.path:
    sys.path.insert(0, _TBOT)

from core.launcher import run_backtest, parse_interval_seconds

if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from workflow_artifact_validation import validate_workflow_artifact  # noqa: E402  (CUL-11 sibling helper)
import cost_helpers as _cost_helpers  # noqa: E402  (E-062 S2a: one shared commission / edge-to-cost definition)
import protocol_resolution as _protocol_resolution  # noqa: E402  (E-061 C1.6: one shared _era_id_for_timestamp)

# CUL-213: the emoji status prints in this module (incl. the load-bearing
# ⚠️⚠️⚠️ [CROSS-CHECK] DISAGREEMENT line) crash on a Windows cp1252 console
# (UnicodeEncodeError) the moment stdout is redirected/piped/captured (e.g. run
# as a captured subprocess). Degrade unencodable glyphs to '?' rather than
# raising — same fix as setup_run.py (CUL-12). getattr because typeshed types
# sys.stdout as TextIO (no reconfigure); contextlib.suppress because a captured
# stream may reject it (OSError) — never crash a context the raw prints survived.
_reconfigure = getattr(sys.stdout, "reconfigure", None)
if _reconfigure is not None:
    with contextlib.suppress(OSError):
        _reconfigure(errors="replace")

_RESULTS_ROOT = os.path.join(_SR, "results")

# A3.4: windows with fewer than this many closed trades get null Sharpe in protocol_result
_SPARSE_TRADE_FLOOR = 5

# E-016 (fee-reduction autopsy field): lookback/lookahead window, in bars, shared
# by all 8 fee-reduction diagnostic metrics below (combine_nearby_trades,
# exit_later, enter_earlier, trade_less_often). Picked as a small fixed bar
# count consistent with this bot's typical holding period rather than an
# arbitrary round number: prereg_whale_footprint_v2.yaml's measured
# avg_holding_bars=5.74 is the closest real reference point available in this
# repo for "how long a trade here typically lasts", so N=6 (rounded up) keeps
# the pre-entry/post-exit lookback on the same scale as an actual trade
# instead of, say, 5 or 20 (the unrelated post_exit_return_5bars/20bars
# window already used elsewhere in this file for a different diagnostic).
# Named constant, not inlined, so it is cheap to retune per strategy family
# later without touching any of the metric formulas themselves.
_FEE_REDUCTION_LOOKAHEAD_BARS = 6

# CUL-275 (route-mode tiebreak): tie-break precedence for
# `post_backtest_route_real` when two or more of the 5 possible
# `determine_route()` values (trading-bot/performance/signal_statistics.py)
# are tied for most-common across (symbol, window) slots. `statistics.mode()`
# silently returns whichever tied value appears FIRST in iteration order in
# that case -- not documented as an error, just quietly order-dependent -- so
# a genuine tie could flip `post_backtest_route_real` (and therefore
# `cost_dominated_real`) depending only on `for symbol in symbols: for window
# in protocol["windows"]` order, with nothing downstream able to tell a real
# majority from an ordering artifact.
#
# Precedence order below is `determine_route()`'s OWN if/elif priority chain,
# verbatim (see that function's docstring), which already encodes a severity
# ordering from "most concerning" to "least concerning":
#   kill_no_ic          -- no detectable directional content at all
#   refine_inverted_ic  -- signal is real but backwards
#   kill_cost_hurdle    -- signal real, right direction, but structurally
#                          can't clear costs
#   refine_cost_hurdle  -- signal real, right direction, marginally short of
#                          the cost hurdle
#   proceed_to_interpretation -- passes both gates
# Reusing this existing order (rather than inventing a new one) means a tied
# route resolves to whichever candidate the codebase already treats as most
# worth flagging first. It also matches the brief's own reasoning: a false
# "not cost-dominated" (silently picking `proceed_to_interpretation` or a
# `refine_*` route over a tied `kill_*`) is worse here than a false
# "cost-dominated", since verdict_interpreter treats `kill_cost_hurdle`/
# `refine_cost_hurdle` as a high-confidence mechanical signal -- but
# `kill_no_ic`/`refine_inverted_ic` are even more fundamental problems than a
# cost hurdle (no signal, or a backwards one, beats "right signal, wrong
# economics" as the thing worth surfacing first), so they outrank the cost
# routes rather than only the two cost routes outranking the pass route.
_ROUTE_TIE_PRECEDENCE = (
    "kill_no_ic",
    "refine_inverted_ic",
    "kill_cost_hurdle",
    "refine_cost_hurdle",
    "proceed_to_interpretation",
)


def _resolve_tied_route(routes: list[str]) -> tuple[str | None, bool]:
    """
    Tie-aware replacement for `statistics.mode(routes)`.

    Returns (winning_route, tied). `tied` is True iff two or more distinct
    values in `routes` share the highest count (a genuine tie for most
    common) -- regardless of which one this function resolves to. When not
    tied, the plain most-common value wins (identical to `statistics.mode`'s
    result in the no-tie case). When tied, the winner is the tied candidate
    that sorts first in `_ROUTE_TIE_PRECEDENCE`; a tied value absent from
    that tuple (should not happen -- `determine_route()` only emits the 5
    named values) sorts last, never crashes.
    """
    if not routes:
        return None, False
    counts = collections.Counter(routes)
    ranked = counts.most_common()
    top_count = ranked[0][1]
    tied_candidates = [route for route, count in ranked if count == top_count]
    tied = len(tied_candidates) > 1
    if not tied:
        return ranked[0][0], False

    def _precedence_key(route):
        try:
            return _ROUTE_TIE_PRECEDENCE.index(route)
        except ValueError:
            return len(_ROUTE_TIE_PRECEDENCE)

    winner = min(tied_candidates, key=_precedence_key)
    return winner, True


def _config_sha(config_source):
    """Canonical config digest, returning (sha256_hex, sha256_hex[:8]).

    Accepts a path (str/Path) OR raw config bytes. The bytes form lets a caller
    hash the exact snapshot it will run from, so the stamp certifies what
    actually ran rather than a separate disk read a mid-run rewrite could desync
    (CUL-165 / GH#79). Either source is json.loads-ed and canonicalized with the
    same sort_keys/compact formula as the engine manifest
    (reporting/run_artifact.py) -- the digest is byte-identical across sources.
    """
    if isinstance(config_source, (bytes, bytearray)):
        cfg = json.loads(config_source)
    else:
        with open(config_source, encoding="utf-8") as f:
            cfg = json.load(f)
    canonical = json.dumps(cfg, sort_keys=True, separators=(",", ":"))
    digest = sha256(canonical.encode()).hexdigest()
    return digest, digest[:8]


def _protocol_run_id(sha8: str) -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + sha8


# ---------------------------------------------------------------------------
# Trade-level diagnostics (Step 03 + A3.1–A3.5)
# ---------------------------------------------------------------------------

def _load_trades(run_dir: Path) -> list:
    """Load trades.json; return [] if missing or empty."""
    p = run_dir / "trades.json"
    if not p.exists():
        return []
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _load_bars(run_dir: Path) -> list:
    """Load bars.csv as list of {timestamp, open, high, low, close} dicts."""
    p = run_dir / "bars.csv"
    if not p.exists():
        return []
    rows = []
    seen = 0
    bad = 0
    bad_samples: list = []
    with open(p, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            seen += 1
            try:
                rows.append({
                    "timestamp": row["timestamp"],
                    "open":  float(row["open"])  if row.get("open")  else None,
                    "high":  float(row["high"])  if row.get("high")  else None,
                    "low":   float(row["low"])   if row.get("low")   else None,
                    "close": float(row["close"]) if row.get("close") else None,
                    # E-016: forecast, when the column is present (it is on every
                    # engine-produced bars.csv -- core/backtester.py always merges
                    # it in before write_bars_csv; absent only on hand-written
                    # fixtures that predate this addition, e.g.
                    # test_run_protocol_exit_reason.py's minimal 5-column rows).
                    # row.get() returns None for a genuinely missing column
                    # (DictReader has no such key at all) the same way it already
                    # does for a present-but-blank cell.
                    "forecast": float(row["forecast"]) if row.get("forecast") not in (None, "") else None,
                })
            except (ValueError, KeyError) as e:
                # #47: this used to be a bare `pass`. A dropped bar silently
                # degrades every field derived from bar POSITION -- the same
                # class the :387 warning was added for -- and left no trace.
                bad += 1
                if len(bad_samples) < 3:
                    bad_samples.append((reader.line_num, repr(e)))

    if bad:
        # Deliberately not fatal, matching this file's documented choice at
        # :387: "partial diagnostics still beat aborting a completed
        # multi-window protocol run". Loud, though -- silence was the defect.
        print(
            f"    WARNING: bars.csv dropped {bad} of {seen} row(s) as "
            f"unparseable in {p} (first {len(bad_samples)}: {bad_samples}) -- "
            f"every bar-position-derived diagnostic (MAE/MFE, entry/exit "
            f"efficiency, post-exit returns, exit_reason) is unreliable for "
            f"trades spanning them",
            file=sys.stderr,
        )

    if seen and not rows:
        # #47's nastier half: when EVERY row fails -- a renamed or missing
        # `timestamp` column makes each one a KeyError -- the list comes back
        # empty, and the :387 integrity warning cannot fire because it is
        # gated on `if bars`. So the total failure was quieter than the
        # partial one. This is a broken artifact, not partial degradation.
        print(
            f"    WARNING: bars.csv at {p} has {seen} data row(s) and ALL of "
            f"them failed to parse -- returning no bars. The per-trade "
            f"integrity warning cannot fire on an empty list, so this line is "
            f"the only signal. Most likely a renamed or missing column; "
            f"expected: timestamp, open, high, low, close",
            file=sys.stderr,
        )
    return rows


def _load_cost_model() -> dict | None:
    """Load config/cost_model.yaml if available (Step 09 creates this file)."""
    p = Path(_SR) / "config" / "cost_model.yaml"
    if not p.exists():
        return None
    try:
        import yaml
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None


# E-062 S2a (code review finding 3): the commission lookup moved, verbatim, to
# tools/cost_helpers.py so tools/portfolio_whole_test.py's buy-and-hold uses the
# SAME definition without importing this module (which imports core.launcher).
# The old names stay as aliases; behaviour is unchanged.
_commission_rate_for_symbol = _cost_helpers.commission_rate_for_symbol
_resolve_commission_rate = _cost_helpers.resolve_commission_rate


def _ts_normalize(ts: str) -> str:
    """Normalize ISO 8601 trade timestamp to bars.csv format ('YYYY-MM-DD HH:MM:SS')."""
    return ts.replace("T", " ").split("+")[0].split("Z")[0]


def _ts_key(ts: str) -> str:
    """Canonical comparison key for a timestamp string ('YYYY-MM-DD HH:MM:SS').

    2026-08-15: `_bar_idx_at` used to compare raw strings, which is only correct
    when bars.csv and trades.json happen to render the same instant identically.
    They do not on daily runs: since the CandleBuilder._align local-timezone fix
    (2529f5b) 1d bars land on midnight UTC and pandas writes them date-only
    ('2019-12-01'), while trades.json still carries the full ISO form
    ('2019-12-01T00:00:00'). Every lookup in such a run missed, returning -1 —
    measured on run_059: 699 of 699 trades, every MAE/MFE 0.0, every entry/exit
    efficiency and post-exit return null, every exit_reason defaulted. Padding a
    date-only stamp to midnight (and dropping fractional seconds) makes the two
    renderings of one instant compare equal.
    """
    t = ts.strip().replace("T", " ").split("+")[0].split("Z")[0].strip()
    t = t.split(".")[0]          # drop fractional seconds if present
    if len(t) == 10:             # date-only → the bar at midnight of that day
        t += " 00:00:00"
    return t


def _bar_idx_at(bars: list, ts_str: str) -> int:
    """Return index of bar with timestamp matching ts_str, or -1."""
    key = _ts_key(ts_str)
    for i, b in enumerate(bars):
        if _ts_key(b["timestamp"]) == key:
            return i
    return -1


def _compute_mae_mfe(side: str, entry_price: float, holding_bars: list) -> tuple:
    """
    MAE: max adverse excursion as positive % of entry_price during holding window.
    MFE: max favorable excursion as positive % of entry_price during holding window.
    """
    mae, mfe = 0.0, 0.0
    for bar in holding_bars:
        h = bar.get("high")
        l = bar.get("low")
        if h is None or l is None:
            continue
        if side == "LONG":
            adverse   = (entry_price - l) / entry_price
            favorable = (h - entry_price) / entry_price
        else:  # SHORT
            adverse   = (h - entry_price) / entry_price
            favorable = (entry_price - l) / entry_price
        mae = max(mae, adverse)
        mfe = max(mfe, favorable)
    return round(mae * 100, 4), round(mfe * 100, 4)


def _compute_entry_efficiency(
    side: str, entry_price: float, exit_price: float, bars: list, entry_idx: int
) -> float | None:
    """
    realized_return_at_actual_entry − hypothetical_return_if_entered_next_bar_open.
    Positive = entering immediately was better than waiting one bar.
    Negative = entry timing degraded the edge.
    """
    if entry_idx < 0 or entry_idx + 1 >= len(bars):
        return None
    next_open = bars[entry_idx + 1].get("open")
    if not next_open:
        return None
    if side == "LONG":
        actual = (exit_price - entry_price) / entry_price * 100
        hypo   = (exit_price - next_open)   / next_open   * 100
    else:
        actual = (entry_price - exit_price) / entry_price * 100
        hypo   = (next_open   - exit_price) / next_open   * 100
    return round(actual - hypo, 4)


def _compute_exit_efficiency(
    side: str, entry_price: float, exit_price: float, holding_bars: list
) -> float | None:
    """
    Fraction of best possible return captured (hindsight optimum benchmark).
    A3.3: this benchmarks against an unattainable optimum; valid for relative
    comparison across variants and trend detection within a family only — do not
    interpret as achievable headroom.
    """
    if not holding_bars:
        return None
    if side == "LONG":
        realized  = (exit_price - entry_price) / entry_price
        best_high = max((b["high"] for b in holding_bars if b.get("high")), default=None)
        if best_high is None:
            return None
        best = (best_high - entry_price) / entry_price
    else:
        realized = (entry_price - exit_price) / entry_price
        best_low = min((b["low"] for b in holding_bars if b.get("low")), default=None)
        if best_low is None:
            return None
        best = (entry_price - best_low) / entry_price
    if best <= 1e-9:
        return 0.0
    return round(realized / best, 4)


def _compute_post_exit_returns(
    side: str, exit_price: float, bars: list, exit_idx: int
) -> tuple:
    """
    A3.1: signed return in the direction of the closed position for 5 and 20 bars after exit.
    Required for the holding_sizing rule (stop_loss_recovery_rate).
    """
    if exit_idx < 0 or exit_price == 0:
        return None, None

    def _signed(n: int) -> float | None:
        target_idx = exit_idx + n
        if target_idx >= len(bars):
            return None
        close = bars[target_idx].get("close")
        if close is None:
            return None
        ret = (close - exit_price) / exit_price * 100
        return round(ret if side == "LONG" else -ret, 4)

    return _signed(5), _signed(20)


# ---------------------------------------------------------------------------
# E-016: fee-reduction autopsy field -- per-trade metric halves for the
# "exit_later" and "enter_earlier" levers. Deliberately separate from
# _compute_post_exit_returns above (same shape, different N and different
# sign convention documented inline) so callers never have to guess which of
# three different N's a given field used.
# ---------------------------------------------------------------------------

def _compute_pre_entry_drift(
    side: str, entry_price: float, bars: list, entry_idx: int,
    n: int = _FEE_REDUCTION_LOOKAHEAD_BARS,
) -> float | None:
    """
    enter_earlier metric (a): (entry_price - price N bars before entry) / price
    N bars before entry, as a %, sign-adjusted so positive = favorable (price
    was already moving toward the trade's eventual direction before entry).
    For LONG the trade profits from price rising, which is exactly what a
    positive raw ratio already means -- no flip needed. For SHORT the trade
    profits from price FALLING, so the raw ratio's sign is flipped, mirroring
    the existing convention in _compute_post_exit_returns above.
    """
    if entry_idx is None or entry_idx < n:
        return None
    price_before = bars[entry_idx - n].get("close")
    if not price_before:
        return None
    raw = (entry_price - price_before) / price_before * 100
    return round(raw if side == "LONG" else -raw, 4)


def _compute_entered_earlier_better(
    side: str, entry_price: float, bars: list, entry_idx: int,
) -> bool | None:
    """
    enter_earlier metric (b): would entering exactly 1 bar earlier have given a
    better entry price (lower for LONG, higher for SHORT) than the trade's
    actual fill? None when the prior bar is unavailable (entry on bar 0).
    """
    if entry_idx is None or entry_idx < 1:
        return None
    prior_close = bars[entry_idx - 1].get("close")
    if prior_close is None:
        return None
    return bool(prior_close < entry_price) if side == "LONG" else bool(prior_close > entry_price)


def _compute_post_exit_drift(
    side: str, exit_price: float, bars: list, exit_idx: int,
    n: int = _FEE_REDUCTION_LOOKAHEAD_BARS,
) -> float | None:
    """
    exit_later metric (a): (price N bars after exit - exit_price) / exit_price,
    as a %, sign-adjusted so positive = favorable (the position would have kept
    gaining had it stayed open N bars longer). Same signed convention as
    _compute_post_exit_returns's 5/20-bar fields, just parameterized on this
    lever's own N instead.
    """
    if exit_idx is None or exit_idx < 0 or not exit_price:
        return None
    target_idx = exit_idx + n
    if target_idx >= len(bars):
        return None
    close = bars[target_idx].get("close")
    if close is None:
        return None
    raw = (close - exit_price) / exit_price * 100
    return round(raw if side == "LONG" else -raw, 4)


def _compute_held_longer_better(
    side: str, exit_price: float, bars: list, exit_idx: int,
) -> bool | None:
    """
    exit_later metric (b): would holding exactly 1 more bar have given a
    better exit price (higher for LONG, lower for SHORT) than the trade's
    actual exit? None when the next bar is unavailable (exit on the last bar).
    """
    if exit_idx is None or exit_idx < 0:
        return None
    next_idx = exit_idx + 1
    if next_idx >= len(bars):
        return None
    next_close = bars[next_idx].get("close")
    if next_close is None:
        return None
    return bool(next_close > exit_price) if side == "LONG" else bool(next_close < exit_price)


def _infer_exit_reason(
    side: str, exit_forecast: float, bars: list, exit_idx: int, window_end: str
) -> str:
    """
    Classify exit as signal_flip | end_of_window | stop_loss | time_stop.
    In this bot, exits are driven by forecast sign-change (signal_flip) or window end.
    Stop-loss and time-stop are not currently implemented; included for schema completeness.
    """
    exit_date = ""
    if exit_idx >= 0 and exit_idx < len(bars):
        exit_date = bars[exit_idx]["timestamp"][:10]
    elif exit_idx >= len(bars):
        # exit_idx beyond bar list → window end
        return "end_of_window"

    window_end_date = window_end[:10] if window_end else ""
    if window_end_date and exit_date >= window_end_date:
        return "end_of_window"
    # Exited on the run's LAST bar → the position was still open when the data
    # ran out and the engine force-closed it.
    #
    # 2026-08-15: compare TIMESTAMPS, not indices. `exit_idx == len(bars) - 1`
    # silently failed whenever bars.csv carried a duplicated final row — which
    # is exactly the shape every open-position backtest produced before
    # c5b1dc6 (_close_all_positions_at_end re-recorded the final bar). The
    # first-match _bar_idx_at then returns len(bars)-2 for a trade that did
    # exit on the last bar, the index test misses, and the trade falls through
    # to the signal_flip default. Measured on run_054: 15 of the 16 windows
    # ending held were misclassified this way (end_of_window_pct 0.85 instead
    # of ~13.7); the single correct one was the only window whose bars.csv had
    # no duplicate row. Timestamp equality is also the honest statement of the
    # intent ("this trade exited on the final bar") and survives a trailing run
    # of duplicates of any length.
    #
    # The window_end check above cannot cover this case: window_end is the
    # protocol's NOMINAL boundary and the engine's last bar routinely falls
    # days short of it (run_054: last bar 2018-09-28 vs window_end 2018-10-01),
    # so `exit_date >= window_end_date` is False for every held-to-end trade.
    if exit_idx >= 0 and bars and bars[exit_idx]["timestamp"] == bars[-1]["timestamp"]:
        return "end_of_window"

    # Signal flip: forecast at exit contradicts the position direction
    if side == "LONG" and (exit_forecast is not None) and exit_forecast <= 0:
        return "signal_flip"
    if side == "SHORT" and (exit_forecast is not None) and exit_forecast >= 0:
        return "signal_flip"
    return "signal_flip"  # default (allocation dropped below rebalance threshold)


def _cost_paid_bps(trade: dict, cost_model: dict | None,
                   commission_bps: float | None = None, product: str = "spot") -> float:
    """
    A3.2: per-trade round-trip cost in bps.
    Uses config/cost_model.yaml when available; falls back to actual commission data.

    E-062 S2a (second-round review finding 6): the one-way fee is resolved by
    the SAME function that sets the engine's commission_rate
    (cost_helpers.resolve_fee_bps with the run's --commission-bps /
    --cost-product), so cost_paid is the fee actually charged. With the default
    flags (None, "spot") and a symbol or 'default' entry in fee_rate_bps this is
    the value the lookup below always returned. Differences: a --commission-bps
    or --cost-product perp run now reports its real fee (it used to report the
    spot table's), and a symbol whose table entry is 0 now reports 0 (the old
    `or` fell through to 'default'). When nothing resolves, the legacy lookup
    below runs unchanged.
    """
    if cost_model or commission_bps is not None:
        fee_bps = _cost_helpers.resolve_fee_bps(
            trade.get("symbol", ""), cost_model, commission_bps, product)
        if fee_bps is not None:
            return round(fee_bps * 2, 2)  # round-trip = 2 legs
    if cost_model:
        symbol = trade.get("symbol", "")
        fees = cost_model.get("fee_rate_bps", {})
        rate = fees.get(symbol) or fees.get("default", 10)
        return round(float(rate) * 2, 2)  # round-trip = 2 legs
    # Fallback: actual commission from trade record (total_commission_percent is round-trip)
    commission_pct = trade.get("total_commission_percent") or 0
    return round(float(commission_pct) * 100, 2)  # % → bps


def _compute_trade_records_for_window(
    run_dir: Path,
    symbol: str,
    window: str,
    window_end: str,
    cost_model: dict | None,
    commission_bps: float | None = None,
    cost_product: str = "spot",
) -> list:
    """
    Compute per-trade diagnostic records for one backtest window.
    Returns empty list if no trades or missing data files.
    commission_bps / cost_product: the run's --commission-bps / --cost-product,
    so each record's cost_paid is the fee the engine charged (_cost_paid_bps).
    """
    trades = _load_trades(run_dir)
    if not trades:
        return []
    bars = _load_bars(run_dir)

    records = []
    for trade in trades:
        side         = trade.get("side", "LONG")
        entry_price  = float(trade.get("entry_price", 0) or 0)
        exit_price   = float(trade.get("exit_price",  0) or 0)
        entry_ts     = _ts_normalize(trade.get("entry_time", ""))
        exit_ts      = _ts_normalize(trade.get("exit_time",  ""))
        exit_forecast = trade.get("exit_forecast")

        entry_idx = _bar_idx_at(bars, entry_ts)
        exit_idx  = _bar_idx_at(bars, exit_ts)

        # 2026-08-15: an unresolved lookup silently degrades EVERY field derived
        # from bar position (MAE/MFE collapse to 0.0, entry/exit efficiency and
        # post-exit returns to null, exit_reason to the signal_flip default) and
        # used to leave no trace at all. It is a data-integrity signal about the
        # artifact pair, not a normal outcome — say so on stderr rather than
        # emitting a confident-looking record. Not fatal: partial diagnostics
        # still beat aborting a completed multi-window protocol run.
        if bars and (entry_idx < 0 or exit_idx < 0):
            print(
                f"    WARNING: bars.csv has no bar matching "
                f"{'entry ' + entry_ts if entry_idx < 0 else ''}"
                f"{' and ' if entry_idx < 0 and exit_idx < 0 else ''}"
                f"{'exit ' + exit_ts if exit_idx < 0 else ''} "
                f"for trade {trade.get('trade_id', '')} ({symbol} {window}) -- "
                f"bar-derived diagnostics for this trade are unreliable",
                file=sys.stderr,
            )

        if entry_idx >= 0 and exit_idx >= 0 and exit_idx >= entry_idx:
            holding_bars = bars[entry_idx : exit_idx + 1]
        elif entry_idx >= 0:
            holding_bars = bars[entry_idx:]
        else:
            holding_bars = []

        holding_bars_count = max(len(holding_bars) - 1, 1) if holding_bars else max(
            round((trade.get("duration_minutes") or 60) / 60), 1
        )

        mae, mfe = _compute_mae_mfe(side, entry_price, holding_bars) if holding_bars else (0.0, 0.0)
        entry_eff = _compute_entry_efficiency(side, entry_price, exit_price, bars, entry_idx)
        exit_eff  = _compute_exit_efficiency(side, entry_price, exit_price, holding_bars)
        post_5, post_20 = _compute_post_exit_returns(side, exit_price, bars, exit_idx)
        exit_reason = _infer_exit_reason(side, exit_forecast, bars, exit_idx, window_end)
        cost_bps = _cost_paid_bps(trade, cost_model, commission_bps, cost_product)

        # E-016 (fee-reduction autopsy): per-trade halves of the enter_earlier/
        # exit_later metrics, plus entry_price/exit_price/entry_idx/exit_idx --
        # the latter two so _compute_window_fee_reduction_diagnostics can pair
        # up consecutive trades (combine_nearby_trades) without re-deriving bar
        # positions from timestamps a second time. entry_idx/exit_idx are only
        # meaningful WITHIN this one window's own bars.csv (indices reset to 0
        # per window) -- never compare them across two different windows.
        pre_entry_drift    = _compute_pre_entry_drift(side, entry_price, bars, entry_idx) if entry_idx >= 0 else None
        entered_earlier_ok = _compute_entered_earlier_better(side, entry_price, bars, entry_idx) if entry_idx >= 0 else None
        post_exit_drift    = _compute_post_exit_drift(side, exit_price, bars, exit_idx) if exit_idx >= 0 else None
        held_longer_ok     = _compute_held_longer_better(side, exit_price, bars, exit_idx) if exit_idx >= 0 else None

        records.append({
            "trade_id":                trade.get("trade_id", ""),
            "symbol":                  symbol,
            "window":                  window,
            "regime_at_entry":         trade.get("entry_regime", "unknown"),
            "direction":               "long" if side == "LONG" else "short",
            "entry_time":              trade.get("entry_time", ""),
            "exit_time":               trade.get("exit_time",  ""),
            "holding_bars":            holding_bars_count,
            # Gross position-level return (% of position value) — used for MAE/MFE comparisons
            # and entry/exit_efficiency (all denominated relative to entry price).
            "realized_return":         round(float(trade.get("profit_loss_percent", 0) or 0), 4),
            # Net portfolio-level return (% of total portfolio value, after commission).
            # This is what investors experience; used for per_trade_expectancy_bps and
            # win classification. Matches the engine's own PerformanceTracker records.
            "profitable_net":          bool(trade.get("profitable_net", False)),
            "net_portfolio_return_pct": round(
                float(trade.get("net_portfolio_profit_loss_percent", 0) or 0), 6
            ),
            "mae":                     mae,
            "mfe":                     mfe,
            "entry_efficiency":        entry_eff,
            "exit_efficiency":         exit_eff,
            "exit_reason":             exit_reason,
            "post_exit_return_5bars":  post_5,   # A3.1
            "post_exit_return_20bars": post_20,  # A3.1
            "cost_paid":               cost_bps, # A3.2
            "entry_price":             entry_price,          # E-016
            "exit_price":              exit_price,           # E-016
            "entry_idx":               entry_idx,            # E-016 (window-local index; see note above)
            "exit_idx":                exit_idx,             # E-016 (window-local index; see note above)
            "pre_entry_drift_pct":     pre_entry_drift,       # E-016 (enter_earlier, metric a)
            "entered_earlier_better":  entered_earlier_ok,    # E-016 (enter_earlier, metric b)
            "post_exit_drift_pct":     post_exit_drift,       # E-016 (exit_later, metric a)
            "held_longer_better":      held_longer_ok,        # E-016 (exit_later, metric b)
        })
    return records


def _resolve_boundary_level(strategy_config: dict | None) -> float:
    """
    E-016 (trade_less_often, metric a -- boundary re-cross rate): the forecast
    level whose repeated re-crossing indicates whipsaw. Prefers this specific
    strategy's own `threshold_filter` op (params.min_abs) when its config
    declares one -- that is already the value this strategy treats as
    meaningful, wherever it sits in the config's component/transform tree
    (see strategies/registry.py::TRANSFORM_OPS_REGISTRY for the op shape).
    Falls back to the forecast's natural zero-crossing (0.0) when no
    threshold_filter is configured -- a strategy with no such gate still has a
    well-defined "flips direction" boundary at 0.

    Generic recursive search (not a fixed-depth path lookup) because
    strategy_config.json's transform lists can be nested under different keys
    per strategy (component-level `transforms` vs `history_transforms`, per
    DOC/STRATEGY_FRAMEWORK.md) -- walking the whole tree for the first
    matching op is simpler and more robust than enumerating every shape.

    CUL-275 (visibility, not behavior): today's real
    trading-bot/strategy_config.json has exactly one `threshold_filter`, so
    this ambiguity never fires in practice -- but this function is written
    to generalize to configs with several per-component `threshold_filter`
    ops, and picking the first one found via an unordered tree walk in that
    case is a silent judgment call. Resolution is unchanged (still the
    first value found, in the same traversal order as before), but when more
    than one distinct threshold_filter.min_abs is found, a WARNING is now
    printed naming the count and values so the ambiguity is visible instead
    of silent.
    """
    found_values = []

    def _walk(node):
        if isinstance(node, dict):
            if node.get("op") == "threshold_filter":
                min_abs = (node.get("params") or {}).get("min_abs")
                if isinstance(min_abs, (int, float)):
                    found_values.append(float(min_abs))
            for value in node.values():
                _walk(value)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    if not strategy_config:
        return 0.0
    _walk(strategy_config)
    if len(found_values) > 1:
        print(
            f"WARNING: _resolve_boundary_level found {len(found_values)} "
            f"threshold_filter.min_abs values in this strategy config "
            f"{found_values} -- using the first ({found_values[0]}) as the "
            "trade_less_often boundary_level. Other components' thresholds "
            "are not reflected in this diagnostic."
        )
    return found_values[0] if found_values else 0.0


def _compute_window_fee_reduction_diagnostics(
    run_dir: Path, symbol: str, window: str, trade_records: list, boundary_level: float,
) -> dict | None:
    """
    E-016 (fee-reduction autopsy field): per-window halves of the
    combine_nearby_trades and trade_less_often metrics. Re-reads this
    window's own bars.csv (forecast + close columns) rather than threading a
    second return value through `_compute_trade_records_for_window` -- that
    function's return shape (a plain list of trade records) is pinned by
    test_run_protocol_exit_reason.py, which destructures it directly; adding
    a second value there would break every existing call site and test for a
    result this function can get more cheaply by re-reading the same
    already-on-disk bars.csv (same re-read pattern this file already uses in
    `_pooled_ic_with_bootstrap_fallback`).

    Returns None when there are fewer than 2 bars (nothing to diff).
    """
    bars = _load_bars(run_dir)
    if len(bars) < 2:
        return None

    # --- trade_less_often (a): boundary re-cross rate -----------------------
    # A "crossing" is a sign change of (forecast - boundary_level) between two
    # consecutive bars. Re-cross rate = fraction of crossings that repeat
    # within _FEE_REDUCTION_LOOKAHEAD_BARS of the PREVIOUS crossing -- high
    # values mean the forecast keeps flapping back across the same level
    # (whipsaw); low values mean crossings are clean, isolated direction
    # changes.
    crossing_idxs: list[int] = []
    prev_sign = None
    for i, bar in enumerate(bars):
        f = bar.get("forecast")
        if f is None:
            continue
        sign = 1 if f >= boundary_level else -1
        if prev_sign is not None and sign != prev_sign:
            crossing_idxs.append(i)
        prev_sign = sign

    boundary_recross_rate = None
    avg_boundary_recross_gap_bars = None
    if len(crossing_idxs) >= 2:
        gaps = [crossing_idxs[i] - crossing_idxs[i - 1] for i in range(1, len(crossing_idxs))]
        recrosses = [g for g in gaps if g <= _FEE_REDUCTION_LOOKAHEAD_BARS]
        boundary_recross_rate = round(len(recrosses) / len(gaps), 4)
        if recrosses:
            avg_boundary_recross_gap_bars = round(statistics.mean(recrosses), 4)

    # --- trade_less_often (b): frequency vs. volatility ratio ---------------
    # trades_per_day (this window) / realized bar-to-bar return volatility
    # (this window) -- distinguishes "the market was genuinely volatile"
    # (ratio tracks volatility) from "there's a real whipsaw inefficiency"
    # (ratio stays high even when volatility is low).
    closes = [b.get("close") for b in bars]
    returns = [
        (closes[i] - closes[i - 1]) / closes[i - 1]
        for i in range(1, len(closes))
        if closes[i - 1] and closes[i] is not None
    ]
    volatility = statistics.stdev(returns) if len(returns) >= 2 else None

    span_days = None
    try:
        t0 = datetime.strptime(_ts_key(bars[0]["timestamp"]), "%Y-%m-%d %H:%M:%S")
        t1 = datetime.strptime(_ts_key(bars[-1]["timestamp"]), "%Y-%m-%d %H:%M:%S")
        span_seconds = (t1 - t0).total_seconds()
        if span_seconds > 0:
            span_days = span_seconds / 86400.0
    except (ValueError, KeyError):
        span_days = None

    trades_per_day = len(trade_records) / span_days if span_days else None
    frequency_vs_volatility_ratio = (
        round(trades_per_day / volatility, 6)
        if trades_per_day is not None and volatility else None
    )

    # --- combine_nearby_trades: same-direction re-entry rate + avg gap ------
    # Consecutive-in-TIME trade pairs within THIS window only -- a different
    # window's bars.csv resets entry_idx/exit_idx to 0, so a gap computed
    # across two windows would compare unrelated bar positions. trade_records
    # is already in chronological order (trades.json is written in execution
    # order, one symbol per window by construction).
    total_pair_count = 0
    reentry_pair_count = 0
    reentry_gaps: list[int] = []
    for i in range(1, len(trade_records)):
        prev_t, cur_t = trade_records[i - 1], trade_records[i]
        if prev_t.get("exit_idx", -1) < 0 or cur_t.get("entry_idx", -1) < 0:
            continue
        total_pair_count += 1
        if cur_t["direction"] == prev_t["direction"]:
            gap = cur_t["entry_idx"] - prev_t["exit_idx"]
            if 0 <= gap <= _FEE_REDUCTION_LOOKAHEAD_BARS:
                reentry_pair_count += 1
                reentry_gaps.append(gap)

    return {
        "symbol":                        symbol,
        "window":                        window,
        "boundary_level":                boundary_level,
        "n_crossings":                   len(crossing_idxs),
        "boundary_recross_rate":         boundary_recross_rate,
        "avg_boundary_recross_gap_bars": avg_boundary_recross_gap_bars,
        "trades_per_day":                round(trades_per_day, 4) if trades_per_day is not None else None,
        "realized_volatility":           round(volatility, 6) if volatility is not None else None,
        "frequency_vs_volatility_ratio": frequency_vs_volatility_ratio,
        "total_pair_count":              total_pair_count,
        "reentry_pair_count":            reentry_pair_count,
        "reentry_gaps":                  reentry_gaps,
    }


def _aggregate_fee_reduction_diagnostics(all_records: list, all_window_diagnostics: list) -> dict:
    """
    E-016 (fee-reduction autopsy field): aggregate the 8 diagnostic metrics
    (2 per lever x 4 levers: combine_nearby_trades, exit_later, enter_earlier,
    trade_less_often) across every trade/window already computed by
    `_compute_trade_records_for_window` and `_compute_window_fee_reduction_diagnostics`
    above -- no new data source, no re-run. Diagnostic-only: none of this
    touches any existing numeric output.

    Returns {} when there is nothing to aggregate (mirrors
    _aggregate_trade_diagnostics's own empty-input contract).
    """
    windows = [w for w in all_window_diagnostics if w]
    if not all_records and not windows:
        return {}

    # combine_nearby_trades
    total_pairs   = sum(w["total_pair_count"]   for w in windows)
    reentry_pairs = sum(w["reentry_pair_count"] for w in windows)
    all_reentry_gaps = [g for w in windows for g in w["reentry_gaps"]]
    same_direction_reentry_rate = round(reentry_pairs / total_pairs, 4) if total_pairs else None
    avg_reentry_gap_bars = round(statistics.mean(all_reentry_gaps), 4) if all_reentry_gaps else None

    # exit_later
    post_exit_drifts  = [r["post_exit_drift_pct"] for r in all_records if r.get("post_exit_drift_pct") is not None]
    held_longer_flags = [r["held_longer_better"]  for r in all_records if r.get("held_longer_better")  is not None]
    avg_post_exit_drift_pct = round(statistics.mean(post_exit_drifts), 4) if post_exit_drifts else None
    pct_better_exit_1bar_later = (
        round(sum(1 for f in held_longer_flags if f) / len(held_longer_flags) * 100, 2)
        if held_longer_flags else None
    )

    # enter_earlier
    pre_entry_drifts      = [r["pre_entry_drift_pct"]    for r in all_records if r.get("pre_entry_drift_pct")    is not None]
    entered_earlier_flags = [r["entered_earlier_better"] for r in all_records if r.get("entered_earlier_better") is not None]
    avg_pre_entry_drift_pct = round(statistics.mean(pre_entry_drifts), 4) if pre_entry_drifts else None
    pct_better_entry_1bar_earlier = (
        round(sum(1 for f in entered_earlier_flags if f) / len(entered_earlier_flags) * 100, 2)
        if entered_earlier_flags else None
    )

    # trade_less_often
    recross_rates   = [w["boundary_recross_rate"]         for w in windows if w["boundary_recross_rate"]         is not None]
    freq_vol_ratios = [w["frequency_vs_volatility_ratio"] for w in windows if w["frequency_vs_volatility_ratio"] is not None]
    boundary_recross_rate         = round(statistics.mean(recross_rates),   4) if recross_rates   else None
    frequency_vs_volatility_ratio = round(statistics.mean(freq_vol_ratios), 6) if freq_vol_ratios else None

    return {
        "lookback_bars": _FEE_REDUCTION_LOOKAHEAD_BARS,
        "combine_nearby_trades": {
            "same_direction_reentry_rate": same_direction_reentry_rate,
            "avg_reentry_gap_bars":        avg_reentry_gap_bars,
        },
        "exit_later": {
            "avg_post_exit_drift_pct":    avg_post_exit_drift_pct,
            "pct_better_exit_1bar_later": pct_better_exit_1bar_later,
        },
        "enter_earlier": {
            "avg_pre_entry_drift_pct":       avg_pre_entry_drift_pct,
            "pct_better_entry_1bar_earlier": pct_better_entry_1bar_earlier,
        },
        "trade_less_often": {
            "boundary_recross_rate":         boundary_recross_rate,
            "frequency_vs_volatility_ratio": frequency_vs_volatility_ratio,
        },
    }


def _compute_cost_basis(all_records: list) -> dict:
    """
    CUL-300 (cost-survival criterion field): honestly report which cost
    components are actually itemized in the per-trade diagnostic records
    this run measured, by inspecting the records themselves rather than
    assuming a fixed answer.

    - "fees": True when cost_paid (A3.2, set by every record built in
      _compute_trade_records_for_window from _cost_paid_bps -- either
      config/cost_model.yaml's fee_rate_bps or the trade's own
      total_commission_percent) is present and non-null. This is the ONLY
      cost source realized_edge_to_cost_ratio's denominator uses.
    - "slippage": the engine (trading-bot/execution/execution_handler.py::
      MockExecutionHandler, S3 2026-09-10) applies flat-bps slippage
      directly to the FILL PRICE at execution time, on by default -- so
      slippage cost is economically baked into entry_price/exit_price/
      realized_return, but it is NOT broken out as its own field anywhere
      in CompletedTrade.to_dict() (trading-bot/performance/metrics.py) or
      in this file's per-trade diagnostic record. Structurally absent from
      every record we can see -> False. This is a determinable fact (the
      field genuinely does not exist here), not a guess -- but it does mean
      realized_edge_to_cost_ratio's cost denominator (fees only) UNDERSTATES true
      round-trip cost whenever slippage_bps > 0.
    - "funding": perpetual funding settlements are not modeled anywhere in
      the engine's trade records at all (no funding field exists in
      CompletedTrade.to_dict() or here) -- always False. See the E-053 note
      next to realized_edge_to_cost_ratio below.
    """
    # CODE-REVIEW FIX (2026-09-20): was any() -- true the moment ONE record had
    # cost_paid, even if most didn't, silently claiming full fee coverage on a
    # partial sample. all() requires EVERY record to carry it before claiming
    # "fees" is reliably measured, matching the numerator/denominator fix
    # below (both now share the exact same filtered record set).
    has_cost_paid = bool(all_records) and all(
        r.get("cost_paid") is not None for r in all_records
    )
    return {
        "fees": has_cost_paid,
        "funding": False,   # not modeled by the engine at all -- see E-053 note near realized_edge_to_cost_ratio
        "slippage": False,  # baked into fill price upstream, not itemized as its own trade-record field (see docstring above)
    }


def _aggregate_trade_diagnostics(
    all_records: list, results: list, all_window_fee_diagnostics: list | None = None,
) -> dict:
    """
    Aggregate per-trade records into the trade_diagnostics_summary block.
    Includes A3.1 stop_loss_recovery_rate, A3.4 per_trade_expectancy_bps and zero_trade_slot_pct.

    Win rate: uses profitable_net (engine's net-of-commission definition) — NOT gross realized_return > 0.
    Expectancy bps: uses net_portfolio_return_pct (portfolio-level net) — NOT position-level gross.
    These two fixes ensure the keltner_163 fixture reproduces 50.7%→57.4% / −26→−58 bps.

    all_window_fee_diagnostics: E-016, optional. Per-window output of
    _compute_window_fee_reduction_diagnostics, one entry per (symbol, window).
    When provided (and all_records is non-empty), the returned dict gains a
    "fee_reduction_metrics" key. Defaults to None so this function's existing
    behaviour is unchanged for any caller that does not pass it.
    """
    if not all_records:
        return {}

    entry_effs = [r["entry_efficiency"]  for r in all_records if r.get("entry_efficiency") is not None]
    exit_effs  = [r["exit_efficiency"]   for r in all_records if r.get("exit_efficiency")  is not None]
    holdings   = [r["holding_bars"]      for r in all_records if r.get("holding_bars")     is not None]

    # MAE/MFE ratio — high ratio with low realized return flags premature exits
    mae_mfe_ratios = [
        r["mae"] / r["mfe"]
        for r in all_records
        if r.get("mae") is not None and r.get("mfe") and r["mfe"] > 0
    ]

    # PnL concentration — uses net portfolio returns (sorted descending: best first)
    portf_returns_bps = [r["net_portfolio_return_pct"] * 100 for r in all_records]
    portf_returns_sorted = sorted(portf_returns_bps, reverse=True)  # best → worst
    n = len(portf_returns_sorted)
    top_n = max(1, n // 10)
    total_pnl = sum(portf_returns_sorted)
    top_pnl   = sum(portf_returns_sorted[:top_n])
    pnl_conc  = (top_pnl / total_pnl * 100) if total_pnl != 0 else None

    # Loss concentration: worst-decile contribution (sorted ascending: worst first)
    worst_n   = max(1, n // 10)
    worst_pnl = sum(portf_returns_sorted[n - worst_n:])  # bottom decile (worst returns)
    loss_conc = (worst_pnl / total_pnl * 100) if total_pnl != 0 else None

    # Exit reason breakdown
    reasons = [r.get("exit_reason", "signal_flip") for r in all_records]
    total_trades = len(reasons)
    # All signal_flip exits are post-hoc inferences (the engine does not record exit reason).
    # Only end_of_window exits are definitively identified by timestamp matching.
    # The backlog item (trading-bot PerformanceTracker) is to record exit_reason as an event
    # at execution time so this inference step becomes unnecessary.
    n_inferred = sum(1 for r in all_records if r.get("exit_reason") == "signal_flip")
    def _pct(reason):
        return round(sum(1 for x in reasons if x == reason) / total_trades * 100, 2) if total_trades else 0.0

    # A3.1: stop_loss recovery rate
    sl_trades = [r for r in all_records if r.get("exit_reason") == "stop_loss"]
    sl_recovery = 0.0
    if sl_trades:
        recovered = sum(1 for r in sl_trades if (r.get("post_exit_return_20bars") or 0) > 0)
        sl_recovery = round(recovered / len(sl_trades), 4)

    # A3.4: per_trade_expectancy_bps — net portfolio return in bps (matches engine's own records)
    n_trades = len(portf_returns_bps)
    mean_bps = statistics.mean(portf_returns_bps) if portf_returns_bps else None
    se_bps   = (statistics.stdev(portf_returns_bps) / math.sqrt(n_trades)
                if n_trades > 1 else None)
    t_stat   = (round(mean_bps / se_bps, 4)
                if mean_bps is not None and se_bps and se_bps > 0 else None)

    # A3.4: win_rate (net-of-commission, matches engine's PerformanceTracker)
    n_wins   = sum(1 for r in all_records if r.get("profitable_net", False))
    win_rate = round(n_wins / n_trades * 100, 2) if n_trades else None

    # A3.4: zero_trade_slot_pct
    total_slots = len(results)
    zero_slots  = sum(1 for r in results if r["core"].get("trade_count", 0) == 0)
    zero_trade_slot_pct = round(zero_slots / total_slots * 100, 2) if total_slots else 0.0

    # Holding period distribution (percentiles)
    hs = sorted(holdings)
    def _pct_val(lst, p):
        if not lst:
            return None
        idx = max(0, int(len(lst) * p / 100) - 1)
        return lst[idx]

    # CUL-300 (cost-survival criterion field): realized_edge_to_cost_ratio + cost_components_measured.
    # Purely additive -- computed from data _aggregate_trade_diagnostics
    # already has, no new data source, no re-run.
    #
    # Numerator is GROSS (pre-commission) edge, from realized_return -- the
    # position-level gross return already computed above (see that field's
    # own comment: "Gross position-level return"). Deliberately NOT
    # per_trade_expectancy_bps.mean: that figure is net_portfolio_return_pct,
    # already net-of-commission (see per_trade_expectancy_bps's own
    # docstring) -- dividing an already-net figure by cost again would
    # double-count the fee deduction and understate how many multiples of
    # cost the raw edge actually represents, which is what a cost-survival
    # ratio (c.f. CLAUDE.fork.md's "still positive at 1.5x/2x modeled
    # costs" bar) needs to measure. cost_paid (denominator, A3.2) is also
    # a position-level round-trip figure, so numerator and denominator
    # share the same basis.
    # CODE-REVIEW FIX (2026-09-20): the numerator used to span every record
    # while the denominator silently dropped any record missing cost_paid --
    # a real N-mismatch (mean-of-all vs mean-of-a-subset) with no signal in
    # the payload that it happened. Both now come from the exact same
    # filtered set, so the ratio is always a like-for-like comparison over
    # the trades that actually have a measured cost.
    # E-062 S2a (code review finding 6): the computation moved, verbatim, to
    # tools/cost_helpers.realized_edge_to_cost_ratio (one definition, shared with
    # tools/portfolio_whole_test.pooled_edge_to_cost_ratio); output unchanged.
    realized_edge_to_cost_ratio = _cost_helpers.realized_edge_to_cost_ratio(all_records)
    cost_components_measured = _compute_cost_basis(all_records)

    return {
        "mae_mfe_ratio_median":    round(statistics.median(mae_mfe_ratios), 4) if mae_mfe_ratios else None,
        "entry_efficiency_median": round(statistics.median(entry_effs),     4) if entry_effs     else None,
        "exit_efficiency_median":  round(statistics.median(exit_effs),       4) if exit_effs      else None,
        "win_rate_net":            win_rate,  # net-of-commission win rate (matches engine)
        "holding_period_distribution": {
            "p10_bars": _pct_val(hs, 10),
            "p50_bars": _pct_val(hs, 50),
            "p90_bars": _pct_val(hs, 90),
        },
        "pnl_concentration": {
            "pct_pnl_from_top_decile_trades":  round(pnl_conc,  2) if pnl_conc  is not None else None,
            "pct_pnl_from_worst_decile_trades": round(loss_conc, 2) if loss_conc is not None else None,
        },
        "exit_reason_breakdown": {
            "signal_flip_pct":   _pct("signal_flip"),
            "stop_loss_pct":     _pct("stop_loss"),
            "time_stop_pct":     _pct("time_stop"),
            "end_of_window_pct": _pct("end_of_window"),
            # Fraction of exits classified by post-hoc inference (signal_flip) vs
            # definitively detected (end_of_window by timestamp matching). The engine
            # does not record exit_reason directly; see backlog note in PerformanceTracker.
            "inferred_classification_pct": round(n_inferred / total_trades * 100, 2) if total_trades else 0.0,
        },
        "stop_loss_recovery_rate": sl_recovery,  # A3.1
        "per_trade_expectancy_bps": {            # A3.4: net portfolio bps (NOT position-level gross)
            "mean":   round(mean_bps, 4) if mean_bps is not None else None,
            "se":     round(se_bps,   4) if se_bps   is not None else None,
            "t_stat": t_stat,
            "n":      n_trades,
        },
        "zero_trade_slot_pct": zero_trade_slot_pct,  # A3.4
        "fee_reduction_metrics": (  # E-016
            _aggregate_fee_reduction_diagnostics(all_records, all_window_fee_diagnostics)
            if all_window_fee_diagnostics is not None else None
        ),
        # CUL-300: cost-survival criterion field, an addressable input for a
        # future (not-yet-built, separate project's) pass/fail rule -- this
        # function only computes and exposes the figure, it makes no
        # promote/kill decision itself.
        #
        # UNDER-COMPLETE for perpetuals held across a funding settlement:
        # funding cash flows are not modeled anywhere in the engine's trade
        # records (see cost_components_measured["funding"] above) until E-053 (sub-daily
        # funding accrual) lands -- so for perp strategies this ratio is
        # missing a real cost/benefit source, not just an approximation.
        "realized_edge_to_cost_ratio": realized_edge_to_cost_ratio,
        "cost_components_measured": cost_components_measured,
    }


# ---------------------------------------------------------------------------
# Hypothesis-specific verdict evaluation (evaluate_against_decision_rules)
# ---------------------------------------------------------------------------

_UNTESTED_KEYWORDS = [
    'delta', 'walk-forward pe', 'holdout pe', ' pe ', ' lag',
    'conditional sharpe', 'regime-conditional', 'v5', 'reverse control',
    'parameter drift', 'generalization', 'buy-hold', 'buy.hold',
]

_KEYWORD_TO_FIELD = [
    (['mr frequency', 'mr freq', 'regime frequency', 'regime_frequency', 'mr regime'], 'regime_frequency'),
    (['win rate', 'win_rate', 'hit rate'],                          'median_win_rate'),
    (['sharpe'],                                                     'median_sharpe'),
    (['drawdown'],                                                   'max_abs_drawdown_pct'),
    (['trade count', 'trade_count', 'trades'],                      'min_trade_count'),
    # 2026-07-09: previously unmapped -- "Walk-forward pooled IC >= ..." criteria were
    # ALWAYS UNTESTED (no matching keyword), regardless of what forecast_return_corr
    # actually contained. Now resolves to median_forecast_return_corr, which
    # _build_extended_summary populates with a block-bootstrap fallback for
    # degenerate (constant-magnitude-when-active) signals -- see that function.
    # DELIBERATELY NARROW: a broader keyword (e.g. bare " ic ") also matched
    # "block-bootstrapped pooled_ic is statistically significant (p<0.05)" --
    # a DIFFERENT criterion about a P-VALUE, not an IC magnitude. That
    # collision made a real number (0.037) satisfy an unrelated "< 0.05"
    # threshold by coincidence and flipped the verdict to a false PROMOTE.
    # Only match the specific "walk-forward pooled ic" phrase this brief's
    # validation_protocol.yaml actually uses for the MAGNITUDE criterion, and
    # explicitly exclude anything mentioning significance/p-value wording.
    (['walk-forward pooled ic', 'walk forward pooled ic'], 'median_forecast_return_corr'),
]
# KNOWN UNIT AMBIGUITY (2026-07-09, deliberately unresolved): this criterion's
# threshold is worded as a percentage ("IC >= 1.5-2.0%"), but
# median_forecast_return_corr is a raw correlation coefficient (e.g. 0.037).
# Compared raw-vs-raw (0.037 >= 1.5) this FAILS; rescaled by x100 (3.72 >= 1.5)
# it would PASS. _apply_op does no unit conversion -- deliberately left as
# raw-vs-raw (the conservative reading: never silently inflate toward a PASS)
# rather than guessing the LLM-authored criterion's intended scale. Does not
# change the overall verdict either way for run_054 (still 'refine'). If this
# ever becomes the deciding criterion for a promote/kill call, resolve the
# ambiguity explicitly before trusting it.

def _is_untested(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in _UNTESTED_KEYWORDS)

# 2026-07-09: significance/p-value wording that must NEVER resolve to
# median_forecast_return_corr -- a criterion phrased as "pooled_ic is
# statistically significant (p<0.05)" is asking about a P-VALUE threshold, not
# an IC magnitude threshold. Conflating the two let a real IC value (0.037)
# coincidentally satisfy an unrelated "< 0.05" p-value threshold and flip a
# verdict to a false PROMOTE -- see _KEYWORD_TO_FIELD's own note.
_SIGNIFICANCE_WORDING = ['p<', 'p <', 'p-value', 'significant']


def _resolve_field(text: str):
    lower = text.lower()
    for keywords, field in _KEYWORD_TO_FIELD:
        if any(kw in lower for kw in keywords):
            if field == 'median_forecast_return_corr' and any(
                w in lower for w in _SIGNIFICANCE_WORDING
            ):
                continue
            return field
    return None

def _parse_op_value(text: str):
    m = re.search(r'([≥>≤<]=?)\s*([0-9]+\.?[0-9]*)\s*%?', text)
    if not m:
        return None, None
    op  = m.group(1).replace('≥', '>=').replace('≤', '<=')
    val = float(m.group(2))
    return op, val

def _apply_op(op: str, actual: float, threshold: float) -> bool:
    return {'>': actual > threshold, '>=': actual >= threshold,
            '<': actual < threshold, '<=': actual <= threshold}.get(op, False)

def _pooled_ic_with_bootstrap_fallback(rows: list, runs_root) -> tuple:
    """
    2026-07-09: returns (median_forecast_return_corr, method) for one symbol's
    rows across all its windows.

    Uses the plain median of each window's forecast_return_corr (from
    trading-bot/reporting/run_artifact.py::build_core) when at least one window
    produced a defined value. Falls back to prescreen_signal's own
    circular-block-bootstrap significance test -- IMPORTED, not reimplemented --
    only when EVERY window's forecast_return_corr is None: the same degenerate,
    constant-magnitude-when-active signal shape prescreen_signal.py already
    detects via _is_degenerate_active_forecast (see that module and
    trading-bot/performance/signal_statistics.py for why the correlation is
    undefined there, not zero). Pools this symbol's bars.csv across ALL its
    windows (chronological order, never crossing into another symbol's data --
    same pooling discipline prescreen_signal.py uses across symbols).

    This extension was authorized after observing a real negative walk-forward
    Sharpe on the SMA(100)-daily hypothesis (P4_ts_trend/run_054): it makes a
    pre-registered criterion (this brief already commits to
    block_bootstrap_all_bars_v1 for exactly this signal shape) computable via
    the pre-committed method, rather than leaving it permanently UNTESTED.
    Expected effect is CONFIRMING the existing negative-Sharpe result, not
    rescuing the hypothesis -- median_sharpe/min_trade_count (already computed,
    never contaminated by this bug) remain the primary evidence either way.

    CUL-259 (#50 family, deliberately deferred out of CUL-15/CUL-20's D1a
    patches): bars.csv carries a "timestamp" column, but records built here
    never captured it, so this caller always passed expected_step_by_symbol=None
    into the block bootstrap -- gap-unaware even after CUL-20 made the bootstrap
    itself gap-aware. This is the degenerate-active-forecast fallback path;
    it fires only when every window's forecast_return_corr is None, but on the
    windows where it does fire, this is the family the committed production
    strategy belongs to. Fixed by threading "timestamp" through and deriving
    expected_step from the first window's own first two consecutive bars
    (backtest bars are generated at a fixed interval by construction, so any
    in-window consecutive pair gives the true step) -- gated on every window
    actually carrying the column, so an older bars.csv without it falls back
    to expected_step=None (today's byte-identical positional behaviour)
    instead of _contiguous_segments' fail-loud missing-timestamp KeyError.
    """
    corrs = [r['core'].get('forecast_return_corr') for r in rows
             if r.get('core', {}).get('forecast_return_corr') is not None]
    if corrs:
        return round(statistics.median(corrs), 4), 'per_window_median_pearson'
    if runs_root is None:
        return None, None

    # Repointed 2026-09-12 (E-039 step 5): sourced from
    # trading-bot/performance/signal_statistics.py, not prescreen_signal.py
    # (being removed) -- _TBOT already on sys.path at module load, above.
    from performance.signal_statistics import stationary_block_bootstrap_ic_significance

    records, expected_step, all_have_timestamp = _assemble_pooled_symbol_records(rows, runs_root)
    if not records:
        return None, None

    symbol = rows[0]['symbol']
    expected_step_by_symbol = (
        {symbol: expected_step}
        if (all_have_timestamp and expected_step is not None) else None
    )
    boot = stationary_block_bootstrap_ic_significance(
        {symbol: records}, expected_step_by_symbol=expected_step_by_symbol,
    )
    return boot.get('pooled_ic'), boot['method']


def _assemble_pooled_symbol_records(rows: list, runs_root) -> tuple:
    """
    Pool ONE symbol's per-bar records across all of its windows, in chronological
    window order. Returns (records, expected_step, all_have_timestamp).

    Extracted from _pooled_ic_with_bootstrap_fallback (CUL-265) so the A8.5.1a
    episode path reuses this assembly rather than rebuilding it -- the two
    consumers must see exactly the same pooled bars, or a disagreement between
    the bootstrap IC and the episode IC would be an artifact of two different
    record builders rather than a real methodological difference.

    Record shape matches prescreen_signal._extract_forecasts' own: forecast,
    next_return_bps, plus "active"/"timestamp"/"symbol" where derivable.
    "active" uses prescreen's own _ACTIVE_THRESHOLD rather than a local literal,
    so "did the signal speak on this bar" means the same thing on both sides of
    the pipeline; episode identification (A8.5.1a) is defined entirely in terms
    of it. "symbol" is constant here (rows are pre-filtered per symbol) but is
    carried so era_of can return prescreen's own (symbol, era_id) tuple shape.

    The "active"/"symbol" keys are additive: _stationary_block_bootstrap_ic_
    significance and _contiguous_segments read only forecast/next_return_bps/
    timestamp, so the pre-existing bootstrap path is unaffected by their presence.
    """
    import pandas as pd
    # Repointed 2026-09-12 (E-039 step 5): sourced from
    # trading-bot/performance/signal_statistics.py, not prescreen_signal.py
    # (being removed) -- _TBOT already on sys.path at module load, above.
    from performance.signal_statistics import ACTIVE_THRESHOLD

    symbol = rows[0]['symbol'] if rows else None
    records = []
    expected_step = None
    all_have_timestamp = True
    for r in sorted(rows, key=lambda x: x['window']):
        bars_path = Path(runs_root) / r['run_id'] / 'bars.csv'
        if not bars_path.exists():
            continue
        bdf = pd.read_csv(bars_path)
        if 'forecast' not in bdf.columns or 'close' not in bdf.columns:
            continue
        has_ts = 'timestamp' in bdf.columns
        all_have_timestamp = all_have_timestamp and has_ts
        closes = bdf['close'].tolist()
        forecasts = bdf['forecast'].tolist()
        timestamps = None
        if has_ts:
            timestamps = pd.to_datetime(bdf['timestamp']).tolist()
            if expected_step is None and len(timestamps) > 1:
                step = timestamps[1] - timestamps[0]
                if step > pd.Timedelta(0):
                    expected_step = step
        for i in range(len(bdf) - 1):
            if closes[i] == 0:
                continue
            rec = {
                'forecast': float(forecasts[i]),
                'next_return_bps': (closes[i + 1] - closes[i]) / closes[i] * 10000.0,
                'active': abs(float(forecasts[i])) > ACTIVE_THRESHOLD,
                'symbol': symbol,
            }
            if has_ts:
                rec['timestamp'] = timestamps[i]
            records.append(rec)
    return records, expected_step, all_have_timestamp


#: CUL-339: the campaign data policy -- the single source of truth for
#: holdout_range. Read at CALL time (never captured at import) so a test can
#: point it at a sandboxed copy with monkeypatch.
_DATA_POLICY_PATH = Path(_SR) / "config" / "campaign_data_policy.yaml"


def _load_campaign_data_policy() -> dict:
    """Thin delegator (E-061 C1.6/C1.7 second-round code-review fix, dedup)
    to the ONE shared implementation, tools/protocol_resolution.py::
    load_campaign_data_policy -- see that function's own docstring. Kept as
    a module-level name here so this module's own callers are unchanged.
    CUL-339: passes _DATA_POLICY_PATH (read at call time) so a test can
    sandbox the policy with monkeypatch."""
    return _protocol_resolution.load_campaign_data_policy(Path(_DATA_POLICY_PATH))


def _era_id_for_timestamp(ts, eras: list) -> str:
    """Thin delegator (E-061 C1.6 code-review fix, dedup) to the ONE shared
    implementation, tools/protocol_resolution.py::era_id_for_timestamp -- see
    that function's own docstring for the open-ended-era history and the
    None-handling logic. Kept as a module-level name here (rather than
    replacing every call site with the qualified name) so this module's own
    A8.5.1a callers are unchanged."""
    return _protocol_resolution.era_id_for_timestamp(ts, eras)


def _a851a_episode_significance(rows: list, runs_root, timeframe: str) -> dict | None:
    """
    A8.5.1a episode-blocked significance for ONE symbol, pooled across its
    windows (CUL-265). Returns compute_a851a_significance's own result dict, or
    None when it is not computable.

    WHY THIS LIVES HERE AND NOT IN build_core. compute_a851a_significance pools
    across eras/windows for one hypothesis -- that is its entire purpose (it was
    built for multi-era backward-extension protocols). trading-bot's
    reporting/run_artifact.py::build_core only ever sees ONE run's own bars_df
    and structurally cannot do that pooling. Cross-window pooling already lives
    here, so this is the correct layer. Unlike CUL-262's Fisher-z, no port is
    needed: run_protocol.py and episode_significance.py are both in
    strategy-research, so the real function is IMPORTED -- there is no second
    implementation to drift.

    WHY IT IS COMPUTED UNCONDITIONALLY (and not behind prescreen's
    significance_methodology flag). In prescreen, A8.5.1a REPLACES the headline
    significance that decides kill-vs-proceed, so switching method changes a
    verdict and must be pre-registered and opted into. Here it is purely
    additive -- median_forecast_return_corr remains the headline and is
    untouched -- so the pre-registration argument does not apply, and gating it
    behind a flag would mean the number is absent from exactly the archived runs
    someone later wants to compare. Gating on "spans multiple eras" was also
    rejected: an era boundary is only ONE of the two things that closes an
    episode (a >gap_bars hole is the other), so a single-era but bursty signal
    still needs the correction, and an eras list that fails to cover a run's
    window would silently read as one era and suppress it.

    COST, MEASURED not assumed (2026-09-04, CUL-265): the expensive bootstrap is
    self-limiting -- compute_a851a_significance returns early and cheaply on the
    dense (>=50% activation) and insufficient-episode (<8) paths, so the 2000
    resamples run only for the sparse bursty signals the method exists for. Timed
    on a synthetic worst case matching a 95-window 1h protocol (20,000 pooled
    bars, 7.9% active, 139 episodes -> the full bootstrap path): 15.2s per
    symbol. Against the 3.5-52 MINUTES E-039 S1 measured for the backtest that
    must already have run before this code is reached, that is noise.
    """
    if runs_root is None or not rows:
        return None

    sys.path.insert(0, _HERE)
    import pandas as pd
    import episode_significance as _es
    from timeframe import bars_per_day, timeframe_seconds

    records, _expected_step, all_have_timestamp = _assemble_pooled_symbol_records(rows, runs_root)
    if not records:
        return None

    policy = _load_campaign_data_policy()
    eras = policy.get('eras', [])
    es_cfg = policy.get('episode_significance', {})

    # Era mapping needs a per-bar timestamp. Without it (an older bars.csv), fall
    # back to era_of=None -- episodes then close on gap alone, which is the
    # method's own documented behaviour when no era list applies, NOT a silent
    # substitution of a different statistic.
    era_of = None
    if eras and all_have_timestamp:
        def era_of(i, _records=records, _eras=eras):
            return (_records[i]['symbol'],
                    _era_id_for_timestamp(_records[i]['timestamp'], _eras))

    # Scalar bar step for gap-aware episode splitting (GH#66), mirroring
    # prescreen's own derivation from the timeframe rather than from the data --
    # the protocol's declared timeframe is the authority on what one bar means.
    episode_expected_step = (
        pd.Timedelta(timeframe_seconds(timeframe), unit='s') if all_have_timestamp else None
    )

    return _es.compute_a851a_significance(
        records,
        era_of=era_of,
        gap_bars=es_cfg.get('gap_bars', _es._DEFAULT_GAP_BARS),
        density_fallback_pct=es_cfg.get('density_fallback_pct', _es._DEFAULT_DENSITY_FALLBACK_PCT),
        min_n_episodes=es_cfg.get('min_n_episodes', _es._MIN_N_EPISODES),
        block_size=bars_per_day(timeframe),
        n_resamples=es_cfg.get('n_resamples', _es._DEFAULT_N_RESAMPLES),
        expected_step=episode_expected_step,
    )


def _build_extended_summary(per_symbol_summary: dict, results: list, runs_root=None,
                            timeframe: str = "1h") -> dict:
    """Augment per_symbol_summary with median_win_rate, regime_frequency, and
    median_forecast_return_corr (with a degenerate-signal bootstrap fallback --
    see _pooled_ic_with_bootstrap_fallback).

    timeframe: protocol-level bar size, used ONLY by the additive A8.5.1a
    episode-blocked significance field (CUL-265) for its block size and bar
    step. Defaults to "1h" to preserve every existing caller's behaviour, the
    same convention main()'s own protocol_timeframe default uses."""
    extended = {s: dict(v) for s, v in per_symbol_summary.items()}
    for symbol in extended:
        rows = [r for r in results if r['symbol'] == symbol]
        win_rates = [r['core']['win_rate'] for r in rows
                     if r.get('core', {}).get('win_rate') is not None]
        extended[symbol]['median_win_rate'] = (
            round(statistics.median(win_rates), 4) if win_rates else None
        )
        freqs = []
        for r in rows:
            pr = r.get('per_regime')
            if pr:
                mr_bars = pr.get('mean_reversion', {}).get('bar_count', 0)
                total   = sum(v.get('bar_count', 0) for v in pr.values())
                if total > 0:
                    freqs.append(mr_bars / total * 100)  # as %, to match "≥ 5%" in text
        extended[symbol]['regime_frequency'] = (
            round(statistics.median(freqs), 4) if freqs else None
        )
        corr, method = _pooled_ic_with_bootstrap_fallback(rows, runs_root)
        extended[symbol]['median_forecast_return_corr'] = corr
        extended[symbol]['median_forecast_return_corr_method'] = method
        # CUL-265 (A8.5.1a, E-039): ADDITIVE. Episode-blocked significance for
        # bursty signals, pooled across this symbol's windows. Never replaces
        # median_forecast_return_corr above -- that stays the headline, byte for
        # byte. None (not a fabricated number) whenever it is not computable:
        # no runs_root, no bars.csv, or no usable records. See
        # _a851a_episode_significance for why it is unconditional rather than
        # behind prescreen's significance_methodology flag.
        a851a = _a851a_episode_significance(rows, runs_root, timeframe)
        extended[symbol]['episode_blocked_significance'] = a851a
        extended[symbol]['episode_blocked_significance_method'] = (
            a851a.get('method') if a851a else None
        )
    return extended

def _split_criteria(text: str) -> list:
    return [p.strip().rstrip('.')
            for p in re.split(r'\bAND\b|\bOR\b', text, flags=re.IGNORECASE)
            if p.strip()]

def _evaluate_criterion(text: str, extended: dict, is_reject: bool) -> dict:
    if _is_untested(text):
        return {'criterion': text, 'result': 'UNTESTED',
                'reason': 'not available in current metrics pipeline'}
    field = _resolve_field(text)
    if field is None:
        return {'criterion': text, 'result': 'UNTESTED',
                'reason': 'no matching metric keyword'}
    op, threshold = _parse_op_value(text)
    if op is None:
        return {'criterion': text, 'result': 'UNTESTED',
                'reason': 'could not parse numeric threshold'}
    # 2026-07-09: sanity check for an impossible threshold -- a correlation
    # coefficient can never exceed 1.0 in absolute value, so a criterion like
    # "IC >= 1.5%" parsed as a raw threshold of 1.5 (not 0.015) is structurally
    # unpassable, almost always a percent/decimal unit mismatch in the
    # LLM-authored validation_protocol.yaml, not a real evidentiary FAIL. See
    # workflow_artifacts/skills/quant-validation/SKILL.md's changelog for the incident this closes
    # (P4_ts_trend/run_054's "Walk-forward pooled IC >= 1.5-2.0%").
    if field == 'median_forecast_return_corr' and abs(threshold) > 1.0:
        return {'criterion': text, 'field': field, 'result': 'SPEC_ERROR',
                'reason': (f'threshold={threshold} exceeds 1.0 -- impossible for a '
                           f'correlation coefficient; likely a percent/decimal unit '
                           f'mismatch in validation_protocol.yaml, not a real criterion')}
    per_symbol = []
    for symbol, vals in extended.items():
        actual = vals.get(field)
        if actual is None:
            per_symbol.append({'symbol': symbol, 'result': 'UNTESTED',
                                'reason': f'{field} not computed'})
            continue
        condition_met = _apply_op(op, actual, threshold)
        result = ('FAIL' if (is_reject and condition_met)
                         or (not is_reject and not condition_met)
                  else 'PASS')
        per_symbol.append({'symbol': symbol, 'actual': round(actual, 4),
                            'required': f'{op} {threshold}', 'result': result})
    overall = ('UNTESTED' if all(r['result'] == 'UNTESTED' for r in per_symbol)
               else 'FAIL'  if any(r['result'] == 'FAIL'    for r in per_symbol)
               else 'PASS')
    return {'criterion': text, 'field': field, 'required': threshold,
            'result': overall, 'per_symbol': per_symbol}

def evaluate_against_decision_rules(
    per_symbol_summary: dict,
    results: list,
    validation_protocol: dict,
    trade_diagnostics_summary: dict | None = None,
    runs_root=None,
    timeframe: str = "1h",
) -> dict:
    """
    Evaluate per_symbol_summary against criteria from a loaded validation_protocol.yaml dict.
    Reads both decision_rules AND required_evidence (D1).
    Derives win_rate and regime_frequency from results list (D2).
    Reject criteria FAILing → kill; approve/evidence FAILing → refine only (D3).
    trade_diagnostics_summary: optional; when provided, enriches diagnostics block with
    per_trade_expectancy_bps and zero_trade_slot_pct (A3.4).
    runs_root: optional; when provided, enables the block-bootstrap IC fallback
    for degenerate (constant-magnitude-when-active) signals in
    _build_extended_summary (2026-07-09).
    timeframe: protocol bar size, passed through to _build_extended_summary for
    the additive A8.5.1a episode-blocked significance field only (CUL-265).
    """
    extended = _build_extended_summary(per_symbol_summary, results, runs_root, timeframe)

    decision_rules    = validation_protocol.get('decision_rules', {})
    required_evidence = validation_protocol.get('required_evidence', []) or []

    def _normalize_evidence_item(item) -> str:
        if isinstance(item, dict):
            k, v = next(iter(item.items()))
            return f"{k}: {v}"
        return str(item)
    required_evidence = [_normalize_evidence_item(i) for i in required_evidence]

    def _dict_to_criterion_text(d: dict) -> str:
        metric    = d.get('metric',    d.get('criterion', ''))
        operator  = d.get('operator',  d.get('op', ''))
        threshold = d.get('threshold', d.get('value', ''))
        window    = d.get('window', '')
        text = f"{metric}: {operator} {threshold}"
        if window:
            text += f" ({window})"
        return text

    if isinstance(decision_rules, list):
        approve_texts = []
        for item in decision_rules:
            if isinstance(item, dict):
                if len(item) == 1:
                    k, v = next(iter(item.items()))
                    approve_texts.append(f"{k}: {v}")
                else:
                    approve_texts.append(_dict_to_criterion_text(item))
            elif isinstance(item, str):
                approve_texts.append(item)
        reject_texts = []
    elif 'approve_if_all_met' in decision_rules:
        approve_texts = list(decision_rules['approve_if_all_met'])
        reject_texts  = list(decision_rules.get('reject_if_any_met', []))
    else:
        approve_texts = _split_criteria(decision_rules.get('approve', ''))
        reject_texts  = _split_criteria(decision_rules.get('reject',  ''))

    criteria_results = []
    approve_rows, reject_rows, evidence_rows = [], [], []

    for text in approve_texts:
        row = _evaluate_criterion(text, extended, is_reject=False)
        criteria_results.append(row); approve_rows.append(row)

    for text in reject_texts:
        row = _evaluate_criterion(text, extended, is_reject=True)
        criteria_results.append(row); reject_rows.append(row)

    for text in required_evidence:
        row = _evaluate_criterion(text, extended, is_reject=False)
        criteria_results.append(row); evidence_rows.append(row)

    # Deduplicate by resolved metric field
    seen = set()
    deduped = []
    for row in criteria_results:
        key = row.get('field') or row['criterion'].lower().strip()
        if key not in seen:
            seen.add(key)
            deduped.append(row)
    criteria_results = deduped
    row_ids = {id(r) for r in criteria_results}
    approve_rows  = [r for r in approve_rows  if id(r) in row_ids]
    reject_rows   = [r for r in reject_rows   if id(r) in row_ids]
    evidence_rows = [r for r in evidence_rows if id(r) in row_ids]

    # 2026-07-09: SPEC_ERROR (an impossible threshold, e.g. a percent/decimal unit
    # mismatch -- see _evaluate_criterion) must be treated like UNTESTED here, not
    # like a real evaluated criterion. Otherwise a criterion that can never
    # mathematically pass OR fail would still count toward approve_evaluated,
    # and if it's the only criterion evaluated, approve_fails==0 (SPEC_ERROR != FAIL)
    # would incorrectly satisfy the promote condition.
    _NOT_REALLY_EVALUATED = ('UNTESTED', 'SPEC_ERROR')
    reject_triggered  = any(r['result'] == 'FAIL' for r in reject_rows)
    approve_fails     = sum(1 for r in approve_rows + evidence_rows if r['result'] == 'FAIL')
    approve_evaluated = sum(1 for r in approve_rows + evidence_rows if r['result'] not in _NOT_REALLY_EVALUATED)

    if reject_triggered:
        verdict = 'kill'
    elif approve_fails == 0 and approve_evaluated > 0:
        verdict = 'promote'
    else:
        verdict = 'refine'

    tested   = [r for r in criteria_results if r['result'] not in _NOT_REALLY_EVALUATED]
    untested = [r for r in criteria_results if r['result'] in _NOT_REALLY_EVALUATED]
    fail_n   = sum(1 for r in tested if r['result'] == 'FAIL')

    diagnostics = _build_diagnostics(results, criteria_results, trade_diagnostics_summary)

    return {
        'verdict':          verdict,
        'criteria_results': criteria_results,
        'verdict_reason':   f"{fail_n} of {len(tested)} evaluable criteria FAIL; "
                            f"{len(untested)} UNTESTED",
        'diagnostics':      diagnostics,
    }


# E-061 C1.3 review fix 3: the one criteria-derived diagnostic, when there is
# no rule set to derive it from (diagnostics-only mode).
WIN_RATE_VS_SHARPE_NO_RULES = "N/A (no rule set)"


def _build_diagnostics(results: list, criteria_results: list | None,
                       trade_diagnostics_summary: dict | None) -> dict:
    """The hypothesis_verdict.diagnostics block (moved verbatim out of
    evaluate_against_decision_rules, E-061 C1.3, so the diagnostics-only mode
    computes it without evaluating any criterion). Everything here derives from
    the per-window `results` and the trade-diagnostics summary, except
    `win_rate_vs_sharpe`, which reads the evaluated criteria: with
    `criteria_results=None` (no rule set) it is WIN_RATE_VS_SHARPE_NO_RULES,
    never the "both PASS or N/A" an empty evaluation would print."""
    # Diagnostics block — evidence for altitude decision by verdict_interpreter
    gross_pnls  = [r["core"].get("gross_pnl")                for r in results if r["core"].get("gross_pnl")                is not None]
    cost_drags  = [r["core"].get("cost_drag_pct")            for r in results if r["core"].get("cost_drag_pct")            is not None]
    corrs       = [r["core"].get("forecast_return_corr")     for r in results if r["core"].get("forecast_return_corr")     is not None]
    durations   = [r["core"].get("avg_trade_duration_bars")  for r in results if r["core"].get("avg_trade_duration_bars")  is not None]

    # E-016 (fee-reduction autopsy field): the REAL, mechanical cost-check
    # route from trading-bot/reporting/run_artifact.py::build_core()'s
    # `post_backtest_route_real` (CUL-264/CUL-272's determine_route(), fed
    # real per-trade fees/edge -- not the LLM's soft mechanism_failure
    # judgment). One value per (symbol, window); take the most common
    # non-null value across all windows as this run's overall route. A
    # cost-dominated kill is `kill_cost_hurdle` (structural) or
    # `refine_cost_hurdle` (marginal) -- see signal_statistics.py::determine_route.
    #
    # CUL-275: `statistics.mode()` does not flag ties -- on equal counts it
    # silently returns whichever value appears first in `_routes_real`, which
    # depends only on `for symbol in symbols: for window in
    # protocol["windows"]` iteration order. `_resolve_tied_route` replaces it
    # with tie-aware logic: `post_backtest_route_real_tied` records whether
    # this run's result was a genuine tie, and the winner is chosen by
    # `_ROUTE_TIE_PRECEDENCE` (documented above) rather than by list order.
    _routes_real = [
        r["core"].get("post_backtest_route_real") for r in results
        if r["core"].get("post_backtest_route_real") is not None
    ]
    post_backtest_route_real, post_backtest_route_real_tied = _resolve_tied_route(_routes_real)
    cost_dominated_real = (
        post_backtest_route_real in ("kill_cost_hurdle", "refine_cost_hurdle")
        if post_backtest_route_real is not None else None
    )

    uninformative: list = []
    for r in results:
        for regime, stats in r.get("regime_validity", {}).items():
            if not stats.get("informative", True) and regime not in uninformative:
                uninformative.append(regime)

    wr_rows     = [row for row in criteria_results or [] if row.get("field") == "median_win_rate"]
    sharpe_rows = [row for row in criteria_results or [] if row.get("field") == "median_sharpe"]
    wr_pass     = bool(wr_rows)     and all(r["result"] == "PASS" for r in wr_rows)
    sharpe_fail = bool(sharpe_rows) and any(r["result"] == "FAIL" for r in sharpe_rows)
    if criteria_results is None:
        wr_vs_sharpe = WIN_RATE_VS_SHARPE_NO_RULES
    elif wr_pass and sharpe_fail:
        wr_vs_sharpe = "win_rate PASS + sharpe FAIL"
    elif not wr_pass and sharpe_fail:
        wr_vs_sharpe = "both FAIL"
    else:
        wr_vs_sharpe = "both PASS or N/A"

    # A3.4: below_floor_pct — fraction of windows with trade_count < _SPARSE_TRADE_FLOOR
    total_windows = len(results)
    sparse_windows = sum(
        1 for r in results if r["core"].get("trade_count", 0) < _SPARSE_TRADE_FLOOR
    )
    below_floor_pct = round(sparse_windows / total_windows * 100, 2) if total_windows else 0.0

    diagnostics = {
        "median_gross_pnl":               round(statistics.median(gross_pnls),  4) if gross_pnls  else None,
        "median_cost_drag_pct":           round(statistics.median(cost_drags),  4) if cost_drags  else None,
        "median_forecast_return_corr":    round(statistics.median(corrs),       4) if corrs       else None,
        "median_avg_trade_duration_bars": round(statistics.median(durations),   2) if durations   else None,
        "uninformative_regimes":          uninformative,
        "win_rate_vs_sharpe":             wr_vs_sharpe,
        "below_floor_pct":                below_floor_pct,  # A3.4
        "post_backtest_route_real":       post_backtest_route_real,  # E-016
        "post_backtest_route_real_tied":  post_backtest_route_real_tied,  # CUL-275
        "cost_dominated_real":            cost_dominated_real,       # E-016
    }

    # A3.4: inject per_trade_expectancy_bps and zero_trade_slot_pct from trade diagnostics
    if trade_diagnostics_summary:
        diagnostics["per_trade_expectancy_bps"] = trade_diagnostics_summary.get("per_trade_expectancy_bps")
        diagnostics["zero_trade_slot_pct"]       = trade_diagnostics_summary.get("zero_trade_slot_pct")
        # E-016: fee-reduction autopsy metrics, feeding verdict_interpreter's
        # fee_reduction_assessment.candidate_system decision when
        # cost_dominated_real is true (see workflow_artifacts/skills/
        # verdict-interpreter/SKILL.md's fee-reduction autopsy rule).
        diagnostics["fee_reduction_metrics"] = trade_diagnostics_summary.get("fee_reduction_metrics")

    return diagnostics


# E-061 C1.3 (G14, C2_S1_FINDINGS.md Decision): --diagnostics-only, passed by
# the orchestrator only under orchestrator.config_direct_authoring (which never
# writes validation_protocol.yaml). Without the flag and without
# --validation-protocol, hypothesis_verdict stays null exactly as before.
DIAGNOSTICS_ONLY_VERDICT_REASON = (
    "--diagnostics-only: no validation protocol, no rule set -- diagnostics only, no verdict")


def diagnostics_only_hypothesis_verdict(results: list,
                                        trade_diagnostics_summary: dict | None = None) -> dict:
    """E-061 C1.3 (G14): hypothesis_verdict under --diagnostics-only. The
    diagnostics block (cost drag, gross PnL, forecast/return correlation,
    below_floor_pct, per-trade expectancy, ...) is the one
    evaluate_against_decision_rules writes (same _build_diagnostics), so its
    readers (build_reports' overall slices, the trial row's expectancy /
    statistic_valid, the profitability reader) keep their inputs. No rule set:
    `verdict` None, `criteria_results` empty, win_rate_vs_sharpe
    WIN_RATE_VS_SHARPE_NO_RULES. Evaluates no criterion, so it does not build
    the extended (per-symbol, bootstrap) summary a second time."""
    return {
        'verdict':          None,
        'criteria_results': [],
        'verdict_reason':   DIAGNOSTICS_ONLY_VERDICT_REASON,
        'diagnostics':      _build_diagnostics(results, None, trade_diagnostics_summary),
    }


# C5.6 (D-043): --legacy-verdict-retired, passed by run_tool_worker only when a
# protocol's promotion block decides nothing (config_direct_authoring AND
# verdict_routing_retired: the grid and the profit bars decide, the legacy
# verdict_interpreter route is retired). The top-level promote/kill/refine
# verdict is then recorded as null with this reason and no promotion block is
# read. Without the flag the verdict is computed from the protocol's block, and
# a protocol whose block is missing, empty or lacks one of the four keys the
# verdict reads (LEGACY_VERDICT_PROMOTION_KEYS) is refused before any backtest
# (it used to raise KeyError after every window had run).
LEGACY_VERDICT_PROMOTION_KEYS = ("median_sharpe_gt", "max_abs_drawdown_pct_lt",
                                 "min_trade_count_gte", "kill_median_sharpe_lt")
LEGACY_VERDICT_RETIRED_REASON = (
    "legacy promote/kill/refine verdict not computed (--legacy-verdict-retired: "
    "config_direct_authoring + verdict_routing_retired -- the grid and the profit bars "
    "decide, C5.6 / D-043)")


def legacy_top_level_verdict(per_symbol: dict, symbols: list, promo: dict) -> tuple:
    """(verdict, verdict_reason): the legacy top-level promote/kill/refine verdict
    from the protocol's `promotion` block. The reason cites that block's own
    thresholds (C5.6 review fix 7: it used to print the abolished generic
    numbers >0 / <30 / >=20 / <-1 whatever the protocol registered)."""
    def _promote(s):
        p = per_symbol[s]
        if p["median_sharpe"] is None:
            return False
        return (p["median_sharpe"]        >  promo["median_sharpe_gt"]
                and p["max_abs_drawdown_pct"] <  promo["max_abs_drawdown_pct_lt"]
                and p["min_trade_count"]       >= promo["min_trade_count_gte"])

    def _kill(s):
        p = per_symbol[s]
        if p["median_sharpe"] is None:
            return False
        return p["median_sharpe"] < promo["kill_median_sharpe_lt"]

    if all(_promote(s) for s in symbols):
        parts = [f"{s}: median_sharpe={per_symbol[s]['median_sharpe']:.3f}"
                 f">{promo['median_sharpe_gt']}"
                 f" max_dd={per_symbol[s]['max_abs_drawdown_pct']:.1f}%"
                 f"<{promo['max_abs_drawdown_pct_lt']}"
                 f" min_trades={per_symbol[s]['min_trade_count']}"
                 f">={promo['min_trade_count_gte']}"
                 for s in symbols]
        return "promote", "; ".join(parts)
    if all(_kill(s) for s in symbols):
        parts = [f"{s}: median_sharpe={per_symbol[s]['median_sharpe']:.3f}"
                 f"<{promo['kill_median_sharpe_lt']}" for s in symbols]
        return "kill", "every symbol below the kill threshold: " + ", ".join(parts)
    parts = []
    for s in symbols:
        p = per_symbol[s]
        fails = []
        if p["median_sharpe"] is None:
            fails.append("median_sharpe=null (all windows sparse)")
        elif p["median_sharpe"] <= promo["median_sharpe_gt"]:
            fails.append(f"median_sharpe={p['median_sharpe']:.3f}<={promo['median_sharpe_gt']}")
        if p["max_abs_drawdown_pct"] >= promo["max_abs_drawdown_pct_lt"]:
            fails.append(f"max_dd={p['max_abs_drawdown_pct']:.1f}%"
                         f">={promo['max_abs_drawdown_pct_lt']}")
        if p["min_trade_count"] < promo["min_trade_count_gte"]:
            fails.append(f"min_trades={p['min_trade_count']}<{promo['min_trade_count_gte']}")
        if fails:
            parts.append(f"{s}: " + ", ".join(fails))
    return "refine", ("; ".join(parts) if parts
                      else "mixed — not all pass promote, not all fail at kill")


# E-061 C1.3: a refusal BEFORE any window ran -- no market data was touched, so
# the orchestrator records no trial row for it (an engineering failure, not a
# spent look). The exit code and the stderr token live in tools/protocol_refusal.py,
# shared with the orchestrator.
from protocol_refusal import EXIT_NO_DATA_TOUCHED, NO_DATA_TOUCHED_TOKEN  # noqa: E402


def _refuse_before_any_backtest(reason: str) -> NoReturn:
    """Exit EXIT_NO_DATA_TOUCHED with NO_DATA_TOUCHED_TOKEN opening stderr's line."""
    sys.stderr.flush()
    print(f"{NO_DATA_TOUCHED_TOKEN}: {reason} -- refusing to run any backtest.",
          file=sys.stderr)
    sys.exit(EXIT_NO_DATA_TOUCHED)


import holdout_policy as _holdout_policy  # noqa: E402  (CUL-339: the ONE strict policy/day parser)


def _load_policy_or_refuse() -> dict:
    """The campaign data policy, or a refusal before any backtest (missing,
    unreadable, unparseable or not a mapping). Deny by default."""
    try:
        return _holdout_policy.load_policy(_DATA_POLICY_PATH)
    except _holdout_policy.HoldoutPolicyError as exc:
        _refuse_before_any_backtest(str(exc))


def _policy_holdout_range(policy: dict) -> tuple[str, str]:
    """CUL-339: (start, end) of the policy's holdout_range, both inclusive
    "YYYY-MM-DD" days. The policy is the ONLY source of the sealed range --
    never a protocol's own `holdout` block, and never the wall clock. A
    malformed range, an open (null/empty) end, or an end before the start
    refuses before any backtest (exit EXIT_NO_DATA_TOUCHED)."""
    try:
        return _holdout_policy.holdout_range_of(policy, f"{_DATA_POLICY_PATH} holdout_range")
    except _holdout_policy.HoldoutPolicyError as exc:
        _refuse_before_any_backtest(str(exc))


def _protocol_holdout_block(protocol: dict) -> dict | None:
    """The protocol's own `holdout` block, validated as a mapping: None when
    absent or null (treated identically), a refusal when it is anything but a
    {start, end} mapping. The ONE reader of that block in this module."""
    block = protocol.get("holdout")
    if block is None:
        return None
    if not isinstance(block, dict):
        _refuse_before_any_backtest(f"the protocol's holdout block {block!r} is not a "
                                    f"{{start, end}} mapping")
    return block


def _resolve_holdout_window(protocol: dict, policy: dict) -> tuple[str, str]:
    """CUL-339: the window `--holdout` backtests. It is the policy's
    holdout_range and nothing else. A protocol with no `holdout` block (absent
    or null) uses it as-is; a protocol whose block disagrees with it on either
    end -- including an `end: null`, which used to mean "today" and scored the
    whole sealed window plus post-holdout data -- is refused before any fetch.
    The block is never used to widen, narrow or shift the range."""
    start, end = _policy_holdout_range(policy)
    block = _protocol_holdout_block(protocol)
    if block is None:
        return start, end
    p_start, p_end = block.get("start"), block.get("end")
    if (_holdout_policy.iso_day(p_start) != start
            or _holdout_policy.iso_day(p_end) != end):
        _refuse_before_any_backtest(
            f"the protocol's holdout block {{start: {p_start!r}, end: {p_end!r}}} disagrees "
            f"with campaign_data_policy.yaml holdout_range [{start}, {end}]. --holdout takes "
            f"its range ONLY from the policy; fix or remove the protocol's block")
    return start, end


def _training_holdout_start(protocol: dict, policy: dict) -> str:
    """CUL-339: the upper bound every walk-forward window (and its warmup
    prefetch) must stay strictly before -- min(protocol holdout start, policy
    holdout start), so a protocol's own block can only make the guard STRICTER
    than the policy, never looser. Only the policy's START is validated here:
    training never reads the sealed range's end, so an open or undecided end
    must not block it (config/README.md). A protocol with no block (or a block
    with no start) gets the policy start; a present but malformed start is
    refused."""
    try:
        policy_start = _holdout_policy.holdout_start_of(
            policy, f"{_DATA_POLICY_PATH} holdout_range")
    except _holdout_policy.HoldoutPolicyError as exc:
        _refuse_before_any_backtest(str(exc))
    block = _protocol_holdout_block(protocol)
    raw = None if block is None else block.get("start")
    if raw is None:
        return policy_start
    p_start = _holdout_policy.iso_day(raw)
    if p_start is None:
        _refuse_before_any_backtest(f"the protocol's holdout start {raw!r} is not a "
                                    f"YYYY-MM-DD day")
    return min(p_start, policy_start)


def _preflight_training_windows(protocol: dict, holdout_start: str) -> None:
    """CUL-339 review fix: EVERY walk-forward window's test.start AND test.end
    must be a strict YYYY-MM-DD day, start <= end, and end strictly before
    `holdout_start` (inclusive-by-day engine semantics) -- all checked before
    any output directory, snapshot or backtest, so one bad window can no
    longer let earlier windows spend data first. An explicit refusal, never an
    `assert` (which `python -O` strips)."""
    try:
        _holdout_policy.check_windows_before(protocol.get("windows"), holdout_start)
    except _holdout_policy.HoldoutPolicyError as exc:
        _refuse_before_any_backtest(str(exc))


def _refuse_if_holdout_consumed(policy: dict, hypothesis_id) -> None:
    """CUL-339 review fix (A6.1 single-use): --holdout needs the hypothesis id
    it spends the seal for, and refuses -- before any fetch -- when that id is
    already in the policy's holdout_consumed_by. Neither the protocol nor the
    strategy config carries a hypothesis id, so it comes from --hypothesis-id
    (the operator copies it from holdout_decision_record / hypothesis_card.yaml).
    Exact match, as the orchestrator's own check. This module never WRITES
    holdout_consumed_by; the orchestrator's record step does."""
    if not isinstance(hypothesis_id, str) or not hypothesis_id.strip():
        _refuse_before_any_backtest(
            "--holdout requires --hypothesis-id <id> (the hypothesis this spend is for) so "
            "a hypothesis already in holdout_consumed_by can be refused")
    if hypothesis_id != hypothesis_id.strip():
        # exact match below: padding would make a consumed id look unspent
        _refuse_before_any_backtest(f"--hypothesis-id {hypothesis_id!r} has surrounding "
                                    f"whitespace")
    try:
        consumed = _holdout_policy.consumed_hypothesis_ids(policy)
    except _holdout_policy.HoldoutPolicyError as exc:
        _refuse_before_any_backtest(f"{_DATA_POLICY_PATH}: {exc}")
    if hypothesis_id in consumed:
        _refuse_before_any_backtest(
            f"hypothesis {hypothesis_id!r} is already in {_DATA_POLICY_PATH} "
            f"holdout_consumed_by -- the holdout is single-use per hypothesis (A6.1)")


# The dry run's synthetic input: two windows of one symbol, every field the
# rule evaluator reads. Only the validation protocol's SHAPE is under test.
_DRY_RUN_PER_SYMBOL = {"DRYRUN": {"median_sharpe": 0.1, "max_abs_drawdown_pct": 5.0,
                                  "min_trade_count": 20, "zero_trade_slot_pct": 0.0}}
_DRY_RUN_RESULTS = [
    {"symbol": "DRYRUN", "window": f"w{i}", "run_id": f"dry_{i}", "per_regime": {},
     "regime_validity": {}, "data_quality": None, "component_errors": None,
     "core": {"trade_count": 20, "sharpe": 0.1, "net_return_pct": 1.0, "win_rate": 0.5,
              "max_drawdown_pct": -5.0, "forecast_return_corr": 0.01,
              "forecast_return_corr_pvalue": 0.5, "gross_pnl": 1.0, "cost_drag_pct": 10.0,
              "avg_trade_duration_bars": 5}}
    for i in (1, 2)]


def _load_validation_protocol(path, timeframe: str = "1h") -> dict:
    """E-061 C1.3: read --validation-protocol and DRY-RUN the rule evaluator on
    it BEFORE any backtest (it used to be opened only after every window had
    run). The refusal is exactly "would evaluate_against_decision_rules crash on
    this document": a missing, unreadable (incl. undecodable), unparseable file,
    or one the evaluator raises on (run_003's `decision_rules: {approve: [...]}`,
    `approve_if_all_met: null`, an empty or non-mapping document) exits
    EXIT_NO_DATA_TOUCHED with NO_DATA_TOUCHED_TOKEN. A document the evaluator
    accepts -- even one with zero rules, like run_018's rules nested under
    `variants` -- proceeds exactly as before."""
    import yaml
    try:
        with open(path, encoding="utf-8") as f:
            doc = yaml.safe_load(f)
    except (OSError, ValueError, yaml.YAMLError) as exc:  # ValueError: UnicodeDecodeError
        _refuse_before_any_backtest(f"--validation-protocol {str(path)!r} cannot be read "
                                    f"({type(exc).__name__}: {exc})")
    try:
        evaluate_against_decision_rules(
            copy.deepcopy(_DRY_RUN_PER_SYMBOL), copy.deepcopy(_DRY_RUN_RESULTS),
            copy.deepcopy(doc), None, runs_root=None, timeframe=timeframe)
    except Exception as exc:
        _refuse_before_any_backtest(f"--validation-protocol {str(path)!r}: the rule evaluator "
                                    f"cannot evaluate it ({type(exc).__name__}: {exc})")
    return doc


def _cross_check_prescreen_vs_backtest(out_dir: Path, results: list, extended: dict | None = None) -> dict | None:
    """
    2026-07-09: institutionalized after the P4_ts_trend incident where prescreen's
    bootstrap IC (pooled_ic=0.0359, p=0.004, significant) and the full backtest's
    own forecast_return_corr silently disagreed -- the old (buggy) build_core
    reported a fabricated corr=0.0/p=1.0 IDENTICALLY across all 24 window-symbol
    results, and verdict_interpreter cited that as "confirmed no edge, high
    confidence" without anyone noticing the contradiction with prescreen's own
    significant result. Two stages computing nominally the same quantity must
    never coexist silently on a material disagreement.

    extended: optional, the per-symbol dict from _build_extended_summary. When
    provided, uses its median_forecast_return_corr (which already applies the
    block-bootstrap fallback for degenerate signals -- see
    _pooled_ic_with_bootstrap_fallback) instead of the raw per-window
    forecast_return_corr. Without this, a signal that's ALREADY been resolved
    via the fallback would still get flagged as "disagreement: undefined",
    contradicting the resolved value sitting right next to it in the same
    protocol_result.yaml -- confirmed live: verdict_interpreter got confused by
    exactly this internal inconsistency on its first re-run.

    Always written to protocol_result.yaml (even when no disagreement is found,
    so this check is auditable going forward), or returns None if no
    prescreen_result.yaml exists for this run to compare against.
    """
    prescreen_path = out_dir / "artifacts" / "prescreen_result.yaml"
    if not prescreen_path.exists():
        return None
    import yaml
    with open(prescreen_path, encoding="utf-8") as f:
        prescreen = yaml.safe_load(f) or {}

    ic_sig = prescreen.get("ic_significance") or {}
    prescreen_significant = bool(ic_sig.get("significant"))
    prescreen_pooled_ic = ic_sig.get("pooled_ic")

    if extended:
        # Resolved values (post block-bootstrap-fallback) -- the honest, final
        # per-symbol IC this run actually used for its criteria evaluation.
        resolved_corrs = [vals.get("median_forecast_return_corr") for vals in extended.values()]
        resolved_methods = {vals.get("median_forecast_return_corr_method") for vals in extended.values()}
        defined_corrs = [c for c in resolved_corrs if c is not None]
        n_total = len(resolved_corrs)
        n_defined = len(defined_corrs)
        fallback_used = "block_bootstrap_all_bars_v1" in resolved_methods
    else:
        corr_values = [r["core"].get("forecast_return_corr") for r in results]
        defined_corrs = [c for c in corr_values if c is not None]
        n_total = len(corr_values)
        n_defined = len(defined_corrs)
        fallback_used = False

    disagreement = False
    detail = None
    if prescreen_significant and prescreen_pooled_ic is not None:
        if n_defined == 0:
            disagreement = True
            detail = (
                f"prescreen reports significant pooled_ic={prescreen_pooled_ic} "
                f"(p={ic_sig.get('p_value')}), but forecast_return_corr is undefined "
                f"(None) in ALL {n_total} window-symbol backtest results, and no "
                f"block-bootstrap fallback resolved it either -- likely a degenerate "
                f"active-bar-forecast shape (see "
                f"trading-bot/performance/signal_statistics.py)."
            )
        else:
            backtest_pooled = sum(defined_corrs) / len(defined_corrs)
            if (prescreen_pooled_ic > 0) != (backtest_pooled > 0):
                disagreement = True
                detail = (
                    f"prescreen pooled_ic={prescreen_pooled_ic} (significant, "
                    f"p={ic_sig.get('p_value')}) disagrees in SIGN with the backtest's "
                    f"own {'bootstrap-resolved' if fallback_used else 'mean'} "
                    f"forecast_return_corr={backtest_pooled:.4f} across "
                    f"{n_defined}/{n_total} {'symbols' if extended else 'windows'}."
                )

    result = {
        "prescreen_significant":       prescreen_significant,
        "prescreen_pooled_ic":         prescreen_pooled_ic,
        "backtest_n_windows_defined":  n_defined,
        "backtest_n_windows_total":    n_total,
        "backtest_bootstrap_fallback_used": fallback_used,
        "disagreement_detected":       disagreement,
        "detail":                      detail,
    }
    if disagreement:
        print(f"\n⚠️⚠️⚠️ [CROSS-CHECK] prescreen/backtest DISAGREEMENT: {detail}")
        print("⚠️⚠️⚠️ Treat any verdict_interpreter narrative citing forecast_return_corr "
              "with suspicion until this is investigated.\n")
    elif fallback_used:
        print(f"\n✅ [CROSS-CHECK] prescreen/backtest agree after block-bootstrap fallback "
              f"(prescreen pooled_ic={prescreen_pooled_ic}, backtest resolved "
              f"{n_defined}/{n_total} symbols to the same sign).\n")
    return result


def main():
    parser = argparse.ArgumentParser(description="Walk-forward protocol runner")
    parser.add_argument("config_path",   help="Path to strategy_config.json")
    parser.add_argument("protocol_path", help="Path to protocol JSON spec")
    parser.add_argument("--holdout",      action="store_true")
    parser.add_argument("--i-understand", action="store_true", dest="i_understand")
    parser.add_argument("--hypothesis-id", default=None, dest="hypothesis_id",
                        help="Required with --holdout (and only with it): the hypothesis "
                             "this holdout spend is for. Refused before any fetch when it "
                             "is already in campaign_data_policy.yaml holdout_consumed_by "
                             "(CUL-339). Never written by this tool.")
    parser.add_argument("--validation-protocol", default=None,
                        help="Path to validation_protocol.yaml for hypothesis-specific verdict")
    parser.add_argument("--diagnostics-only", action="store_true", dest="diagnostics_only",
                        help="E-061 C1.3: no validation protocol (config-direct authoring) -- "
                             "write hypothesis_verdict as the diagnostics block with no rule "
                             "set and no verdict. Without it (and without "
                             "--validation-protocol) hypothesis_verdict stays null. Mutually "
                             "exclusive with --validation-protocol.")
    parser.add_argument("--legacy-verdict-retired", action="store_true",
                        dest="legacy_verdict_retired",
                        help="C5.6 (D-043): record the legacy top-level promote/kill/refine "
                             "verdict as null (LEGACY_VERDICT_RETIRED_REASON) and read no "
                             "`promotion` block. Passed by run_tool_worker only under "
                             "orchestrator.config_direct_authoring + verdict_routing_retired. "
                             "Without it a protocol whose promotion block is missing, empty "
                             "or partial is refused before any backtest.")
    parser.add_argument("--out-dir", default=None,
                        help="Override output directory (default: results/protocols/<run_id>)")
    parser.add_argument("--cost-product", default="spot", choices=["spot", "perp"],
                        dest="cost_product",
                        help="2026-07-20 (Dispatch H): which cost_model.yaml fee block to "
                             "cost this re-run at. Default 'spot' preserves exact prior "
                             "behavior (top-level fee_rate_bps). 'perp' reads the additive "
                             "cost_model['perp']['fee_rate_bps'] block instead -- valid only "
                             "for price-based strategies (funding cash flows are not modeled; "
                             "do not use for funding-carry strategies, see cost_model.yaml's "
                             "PERP CALIBRATION block).")
    parser.add_argument("--commission-bps", type=float, default=None, dest="commission_bps",
                        help="2026-07-20 (Dispatch L): explicit one-way taker commission in bps "
                             "per leg (e.g. 10 for the historical 0.001 default, 5 for the perp "
                             "0.0005 rate), converted the same way as --cost-product (/10000, no "
                             "double-charge). Takes precedence over --cost-product when both are "
                             "given. Absent, behavior is byte-identical to today (falls through "
                             "to --cost-product's existing resolution). Intended for controlled "
                             "fee-isolation experiments that need an exact rate cost_model.yaml "
                             "doesn't happen to supply as either 'spot' or 'perp'.")
    parser.add_argument("--exchange", default=None,
                        help="2026-08-09 (fix/exchange-plumbing-campaign-aux, Ticket 13): CCXT "
                             "exchange id for every run_backtest() call this campaign makes. "
                             "Takes precedence over the protocol file's own top-level 'exchange' "
                             "field when both are given. Option Y (locked): resolution is "
                             "--exchange -> protocol field -> explicit 'binance', and this NEVER "
                             "falls through to run_backtest's own config.json-read arm -- ambient "
                             "config.json must not silently decide a campaign's venue. Absent "
                             "both, campaigns resolve to 'binance', identical to the venue every "
                             "existing campaign already scored via the engine's own default.")
    parser.add_argument("--drop-feeds", default=None,
                        help="2026-08-11 (fix/feed-dependency-safety, Step 2): comma-separated "
                             "FEED_REGISTRY names (e.g. 'funding_rate,fear_greed') to exclude "
                             "from every run_backtest() call this campaign makes. Takes "
                             "precedence over the protocol file's own top-level 'drop_feeds' "
                             "field when both are given. Absent both, no feed is dropped -- "
                             "byte-identical to today (same resolution shape as --exchange "
                             "above, but with no forced fallback: None IS the correct "
                             "'drop nothing' value here, not a placeholder needing one).")
    args = parser.parse_args()

    # Holdout gate: require BOTH flags or NEITHER
    if args.holdout != args.i_understand:
        print("ERROR: --holdout requires --i-understand (and vice versa). Pass both or neither.",
              file=sys.stderr)
        sys.exit(1)

    # E-061 C1.3: read the validation protocol now, before any data is spent.
    # Holdout mode never reads it (unchanged).
    if args.diagnostics_only and args.validation_protocol:
        _refuse_before_any_backtest("--diagnostics-only and --validation-protocol are "
                                    "mutually exclusive")
    validation_protocol = None
    if args.validation_protocol and not args.holdout:
        validation_protocol = _load_validation_protocol(args.validation_protocol)

    if args.commission_bps is not None:
        print(f"[cost-override] --commission-bps={args.commission_bps} -> "
              f"commission_rate={float(args.commission_bps) / 10000.0} "
              f"(takes precedence over --cost-product={args.cost_product!r} for this entire run)")

    with open(args.protocol_path, encoding="utf-8") as f:
        protocol = json.load(f)

    # CUL-339: resolve the holdout boundary from campaign_data_policy.yaml NOW,
    # and pre-flight everything that depends on it, before any output
    # directory, snapshot or data fetch. Every check below refuses
    # (EXIT_NO_DATA_TOUCHED) rather than asserting.
    if args.hypothesis_id is not None and not args.holdout:
        _refuse_before_any_backtest("--hypothesis-id is only meaningful with --holdout")
    policy = _load_policy_or_refuse()
    if args.holdout:
        holdout_window = _resolve_holdout_window(protocol, policy)
        _refuse_if_holdout_consumed(policy, args.hypothesis_id)
    _holdout_start = _training_holdout_start(protocol, policy)
    if not args.holdout:
        _preflight_training_windows(protocol, _holdout_start)

    # C5.6 (D-043): the legacy top-level verdict needs the protocol's promotion
    # block. Without --legacy-verdict-retired a missing, null, empty or partial
    # block used to crash (KeyError/TypeError) AFTER every window -- and every
    # holdout window -- had been spent; it is refused here instead, before any
    # fetch.
    _promo_block = protocol.get("promotion") if isinstance(protocol, dict) else None
    if not args.legacy_verdict_retired and not (
            isinstance(_promo_block, dict)
            and all(k in _promo_block for k in LEGACY_VERDICT_PROMOTION_KEYS)):
        _refuse_before_any_backtest(
            f"{args.protocol_path}: its `promotion` block is missing, empty or lacks one of "
            f"{list(LEGACY_VERDICT_PROMOTION_KEYS)} (got {_promo_block!r}), which the legacy "
            f"top-level promote/kill/refine verdict needs. Under "
            f"orchestrator.config_direct_authoring + verdict_routing_retired pass "
            f"--legacy-verdict-retired (run_tool_worker does; so must a by-hand --holdout "
            f"run); otherwise use a protocol with pre-registered thresholds (C5.6, D-043)")

    # CUL-165 / GH#79: read the config bytes once and hash those bytes, so the
    # protocol-level stamp certifies the exact bytes every run_backtest() below
    # parses. The run_id/out_dir are derived from the hash (before out_dir
    # exists), so we hash the in-memory bytes here; the immutable snapshot is
    # written into out_dir once it is created and its path replaces
    # args.config_path at every run_backtest() call -- a mid-run rewrite of the
    # original file can no longer desync certificate from what actually ran.
    config_bytes = Path(args.config_path).read_bytes()
    config_sha256, config_sha8 = _config_sha(config_bytes)
    # E-016 (fee-reduction autopsy field): resolve the boundary_recross_rate
    # level once from these exact config bytes (same discipline as the sha
    # above -- one parse, no risk of a mid-run rewrite desyncing the level
    # from what actually ran).
    _fee_reduction_boundary_level = _resolve_boundary_level(json.loads(config_bytes))
    symbols = protocol["symbols"]
    # Option Y (locked 2026-08-09, Ticket 13): --exchange -> protocol field ->
    # explicit "binance". Resolved with `is not None` rather than truthiness so
    # an EXPLICITLY empty venue ("exchange": "" or --exchange "") is preserved
    # and rejected downstream by _validated_exchange (sys.exit 1), not silently
    # swallowed to binance (reviewer-48 §2). A genuinely ABSENT source (None)
    # still coalesces to "binance": unlike interval_seconds/commission_rate
    # below, venue must NEVER fall through to run_backtest's own config.json-read
    # arm, where ambient, machine-local state would silently decide which market
    # a campaign scores. Every existing campaign (no field, no flag) resolves to
    # "binance", identical to the venue it already scored via the engine's own
    # pre-existing default -- byte-identical by construction.
    exchange = args.exchange
    if exchange is None:
        exchange = protocol.get("exchange")
    if exchange is None:
        exchange = "binance"
    # fix/feed-dependency-safety Step 2: --drop-feeds -> protocol field -> None
    # ("drop nothing", the pre-existing default). Unlike exchange above, a
    # genuinely absent source stays None rather than coalescing to a forced
    # default -- None IS the correct "no drop" value here, not a placeholder.
    if args.drop_feeds is not None:
        drop_feeds = [name.strip() for name in args.drop_feeds.split(",") if name.strip()]
    else:
        drop_feeds = protocol.get("drop_feeds")
    # Protocol-level timeframe (default "1h" preserves exact prior behavior —
    # run_backtest's own interval_seconds=None default falls back identically
    # to the pre-existing global-config-derived interval).
    protocol_timeframe = protocol.get("timeframe", "1h")
    interval_seconds = parse_interval_seconds(protocol_timeframe) if protocol_timeframe != "1h" else None
    os.makedirs(_RESULTS_ROOT, exist_ok=True)

    run_id = _protocol_run_id(config_sha8)
    if args.out_dir:
        out_dir = Path(args.out_dir)
    else:
        out_dir = Path(_RESULTS_ROOT) / "protocols" / run_id
    # 2026-07-07: resolve to absolute. run_phase1_research.py's ROOT = Path(".") makes
    # --out-dir a RELATIVE string (e.g. "runs/run_054"); left relative, it propagates
    # into run_backtest's runs_root -> new_run_dir's run_dir, which
    # trading-bot/performance/metrics.py's export_trades_to_excel/export_metrics_to_excel
    # then re-anchor to trading-bot/'s OWN package directory (os.path.join(project_folder,
    # filepath) -- a no-op for an absolute path, but silently rewrites a relative one to a
    # different, non-existent directory than what new_run_dir actually created). This was
    # dormant because every prior hypothesis in this campaign was killed at prescreen,
    # before ever reaching protocol_execution with a per-run --out-dir; SMA(100)-daily
    # (P4_ts_trend/run_054) is the first to clear prescreen and expose it.
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # CUL-165 / GH#79: immutable run-private snapshot of the config bytes hashed
    # above. Every run_backtest() below reads THIS instead of args.config_path,
    # so the stamp and the runs derive from the same frozen bytes. Written
    # atomically (temp + os.replace) so a concurrent reader never sees a partial
    # file; the no-desync guarantee holds within a per-run out_dir.
    config_snapshot_path = str(out_dir / "config.snapshot.json")
    _snap_tmp = out_dir / "config.snapshot.json.tmp"
    _snap_tmp.write_bytes(config_bytes)
    os.replace(_snap_tmp, config_snapshot_path)

    cost_model = _load_cost_model()

    # ------------------------------------------------------------------
    # HOLDOUT MODE
    # ------------------------------------------------------------------
    if args.holdout:
        # CUL-339: the policy's holdout_range, resolved (and cross-checked
        # against the protocol's own block) before out_dir was created above.
        # It used to be read from protocol["holdout"], with `end: null` meaning
        # date.today() -- a block of {start: <validation year>, end: null}
        # would have scored validation, the whole seal and post-holdout data.
        start, end = holdout_window

        _runs_root = str(out_dir / "results") if args.out_dir else None
        holdout_results = {}
        for symbol in symbols:
            print(f"[holdout] {symbol}  {start} to {end} ...")
            # 2026-07-07: warmup_prefetch=True unconditionally -- see
            # launcher.run_backtest's docstring. No holdout_start guard here: this
            # loop's OWN start IS the holdout start, so its prefetch legitimately
            # reaches backward into pre-holdout training data for warmup only
            # (never scored) -- that's the intended, correct behavior.
            # 2026-09-02 (E-041): bar_equity=True -- DECLARED OUTPUT CHANGE. Adds
            # a purely additive "bar_equity" block to metrics.json (bar-level
            # maxDD/Sharpe/Sortino from the full portfolio_states series, more
            # honest than core's trade-exit curve). Proven bit-identical/additive
            # by tests/test_bar_equity_bit_identical.py; this call site was the
            # last place still defaulting the flag off (E037-42, E-041's S1).
            rd = run_backtest(config_snapshot_path, symbol, start, end, _RESULTS_ROOT,
                              runs_root=_runs_root, interval_seconds=interval_seconds,
                              warmup_prefetch=True, bar_equity=True,
                              commission_rate=_resolve_commission_rate(
                                  symbol, cost_model, args.commission_bps, args.cost_product),
                              exchange=exchange, drop_feeds=drop_feeds)
            with open(rd / "metrics.json", encoding="utf-8") as f:
                m = json.load(f)
            holdout_results[symbol] = {"run_id": rd.name, "core": m["core"]}

        payload = {
            "protocol_run_id": run_id,
            "config_sha256":   config_sha256,
            "holdout_window":  {"start": start, "end": end},
            "results":         holdout_results,
        }
        validate_workflow_artifact(out_dir / "holdout_result.json", payload)  # CUL-11: opt-in schema check
        (out_dir / "holdout_result.json").write_text(
            json.dumps(payload, indent=2, default=str), encoding="utf-8"
        )
        print(f"Holdout result: {out_dir / 'holdout_result.json'}")

        log_path = Path(_RESULTS_ROOT) / "holdout_log.jsonl"
        line = {
            "utc":             datetime.now(timezone.utc).isoformat(),
            "config_sha256":   config_sha256,
            "protocol_run_id": run_id,
            "symbols_core":    {s: holdout_results[s]["core"] for s in symbols},
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(line, default=str) + "\n")
        print(f"Appended to {log_path}")
        return

    # ------------------------------------------------------------------
    # NORMAL MODE — walk-forward windows
    # ------------------------------------------------------------------
    prior_runs = 0
    n_new = len(symbols) * len(protocol["windows"])
    print(f"Budget used for this config: {prior_runs}/20 scored runs")
    if prior_runs + n_new > 20:
        print(f"WARNING: this run adds {n_new}, bringing total to {prior_runs + n_new}/20 (over budget). Continuing.")

    _runs_root = str(out_dir / "results") if args.out_dir else None
    results = []
    all_trade_records = []  # Step 03: accumulate per-trade diagnostics
    all_window_fee_diagnostics = []  # E-016: accumulate per-window fee-reduction diagnostics

    # 2026-07-07: holdout boundary guard for the warmup_prefetch buffer (see
    # launcher.run_backtest's warmup_prefetch docstring). Read once; every window
    # is checked against it below, both directly (this loop, general protocol
    # sanity: no training window may reach into holdout) and inside run_backtest
    # itself (the prefetch's computed fetch_start must stay before it too).
    # CUL-339: _holdout_start is resolved right after the protocol is loaded --
    # min(protocol holdout start, policy holdout start), never None, so the
    # guard can no longer be looser than the policy or silently absent -- and
    # EVERY window was pre-flighted against it there (_preflight_training_windows:
    # strict days, start <= end, end STRICTLY before it), before out_dir existed.
    # Strictly less than, not <=: `end` reads as an exclusive bound (the next
    # window starts on the same date) but run_backtest passes it to
    # load_data(end_date=end), which yields every bar of the end DAY through
    # 23:00, so end == holdout_start would materialise 24 holdout bars -- see
    # campaign_data_policy.yaml: holdout_contaminated_runs.

    for symbol in symbols:
        for window in protocol["windows"]:
            label     = window["label"]
            start     = window["test"]["start"]
            end       = window["test"]["end"]
            print(f"  {symbol}  window={label}  {start} to {end} ...")
            # 2026-09-02 (E-041): bar_equity=True -- see the holdout call site
            # above for the full declaration; same change, same proof.
            rd = run_backtest(config_snapshot_path, symbol, start, end, _RESULTS_ROOT,
                              runs_root=_runs_root, interval_seconds=interval_seconds,
                              warmup_prefetch=True, bar_equity=True, holdout_start=_holdout_start,
                              commission_rate=_resolve_commission_rate(
                                  symbol, cost_model, args.commission_bps, args.cost_product),
                              exchange=exchange, drop_feeds=drop_feeds)
            with open(rd / "metrics.json", encoding="utf-8") as f:
                m = json.load(f)
            core = m["core"]

            # A3.4: null per-window Sharpe for sparse windows (< _SPARSE_TRADE_FLOOR trades)
            if core.get("trade_count", 0) < _SPARSE_TRADE_FLOOR:
                core = dict(core)  # don't mutate original
                core["sharpe"] = None

            result_entry = {
                "symbol":          symbol,
                "window":          label,
                "run_id":          rd.name,
                "core":            core,
                "per_regime":      m.get("per_regime", {}),
                "regime_validity": m.get("regime_validity", {}),
                # CUL-263 (E-039): metrics.json's "data_quality" block (CUL-261, gap
                # detection) is a top-level sibling of "core", not nested inside it --
                # unlike CUL-262's forecast_return_corr_pvalue_block_adjusted/n_eff,
                # which already ride along inside "core" and therefore already reached
                # this dict. None when gap_detection was off for this window (the
                # default), so this key is always present but usually null --
                # matches "core"/"per_regime" always being present rather than the
                # optional-key idiom metrics.json itself uses, since result_entry is
                # an internal aggregation structure, not the byte-identity-sensitive
                # artifact metrics.json is.
                "data_quality":    m.get("data_quality"),
                # CUL-274: bars whose NaN forecast was held (no strategy trade);
                # absent from metrics.json (None here) when there were none.
                "nan_forecast":    m.get("nan_forecast"),
                # E-039 step 5 follow-up (2026-09-12): same sibling-of-"core" shape
                # as data_quality above -- metrics.json's component_errors block
                # (F5b's error count/samples, now wired through by
                # core/backtester.py) would otherwise be silently dropped here the
                # same way data_quality was before CUL-263.
                "component_errors": m.get("component_errors"),
            }
            results.append(result_entry)

            # Step 03: compute trade diagnostics while run directory is available
            trade_records = _compute_trade_records_for_window(
                rd, symbol, label, end, cost_model,
                commission_bps=args.commission_bps, cost_product=args.cost_product,
            )
            all_trade_records.extend(trade_records)

            # E-016: per-window fee-reduction autopsy diagnostics (same run
            # directory, no re-run) -- see _compute_window_fee_reduction_diagnostics
            # for why this is a separate re-read rather than a second return
            # value off _compute_trade_records_for_window.
            all_window_fee_diagnostics.append(
                _compute_window_fee_reduction_diagnostics(
                    rd, symbol, label, trade_records, _fee_reduction_boundary_level
                )
            )

            print(f"    sharpe={core.get('sharpe') or 0:.3f}  trades={m['core'].get('trade_count', 0)}"
                  f"  dd={m['core'].get('max_drawdown_pct', 0):.1f}%")

    # Step 03: aggregate trade diagnostics and write trade_diagnostics.json
    trade_diagnostics_summary = _aggregate_trade_diagnostics(
        all_trade_records, results, all_window_fee_diagnostics
    )
    if all_trade_records:
        td_payload = {
            # A3.5: keltner_163 fixture — production of this artifact is what the regression
            # fixture tests against. Run against strategy-research/results/protocols/
            # 20260702T091324Z_18fad381/protocol_summary.json to reproduce the known signature:
            # win rate 51%→57% from 2024→2025 cohorts while per-trade expectancy −26→−58 bps.
            "trades":  all_trade_records,
            "summary": trade_diagnostics_summary,
        }
        validate_workflow_artifact(out_dir / "trade_diagnostics.json", td_payload)  # CUL-11: opt-in schema check
        (out_dir / "trade_diagnostics.json").write_text(
            json.dumps(td_payload, indent=2, default=str), encoding="utf-8"
        )
        print(f"Trade diagnostics: {out_dir / 'trade_diagnostics.json'} "
              f"({len(all_trade_records)} trades)")

    # Per-symbol summary (A3.4: median_sharpe excludes null-sharpe sparse windows)
    # C5.6: a missing/empty/partial block was refused before any backtest,
    # unless run_tool_worker said the legacy verdict is retired (none is read).
    promo = None if args.legacy_verdict_retired else protocol["promotion"]
    per_symbol = {}
    for symbol in symbols:
        rows    = [r for r in results if r["symbol"] == symbol]
        sharpes = [r["core"]["sharpe"] for r in rows if r["core"].get("sharpe") is not None]
        dds     = [abs(m["core"]["max_drawdown_pct"])
                   for r in rows
                   for m in [{"core": {**r["core"], "max_drawdown_pct":
                               r["core"].get("max_drawdown_pct", 0) or 0}}]]
        trades  = [r["core"].get("trade_count", 0) for r in rows]

        # A3.4: zero_trade_slot_pct per symbol
        sym_zero_pct = round(
            sum(1 for r in rows if r["core"].get("trade_count", 0) == 0) / len(rows) * 100, 2
        ) if rows else 0.0

        per_symbol[symbol] = {
            "median_sharpe":        round(statistics.median(sharpes), 4) if sharpes else None,
            "max_abs_drawdown_pct": round(max(dds), 4) if dds else 0.0,
            "min_trade_count":      min(trades) if trades else 0,
            "zero_trade_slot_pct":  sym_zero_pct,  # A3.4
        }

    if args.legacy_verdict_retired:
        verdict, verdict_reason = None, LEGACY_VERDICT_RETIRED_REASON
    else:
        verdict, verdict_reason = legacy_top_level_verdict(per_symbol, symbols, promo)

    # 2026-07-09: compute the extended (bootstrap-fallback-resolved) per-symbol
    # summary BEFORE the cross-check, so the check reports whether the
    # fallback already reconciled prescreen/backtest, rather than flagging a
    # "disagreement" that's actually been resolved elsewhere in this same file.
    extended_for_cross_check = _build_extended_summary(
        per_symbol, results, _runs_root, protocol_timeframe)
    cross_check = _cross_check_prescreen_vs_backtest(out_dir, results, extended_for_cross_check)

    hypothesis_verdict = None
    if validation_protocol is not None:
        # Parsed and shape-checked before the windows ran (_load_validation_protocol).
        hypothesis_verdict = evaluate_against_decision_rules(
            per_symbol, results, validation_protocol, trade_diagnostics_summary or None,
            runs_root=_runs_root, timeframe=protocol_timeframe,
        )
    elif args.diagnostics_only:
        # E-061 C1.3 (G14): config-direct authoring -> the diagnostics block,
        # no rule set, no verdict.
        hypothesis_verdict = diagnostics_only_hypothesis_verdict(
            results, trade_diagnostics_summary or None)
    if hypothesis_verdict is not None:
        print(f"Hypothesis verdict : {hypothesis_verdict['verdict']}")
        print(f"Reason             : {hypothesis_verdict['verdict_reason']}")

    summary = {
        "protocol_run_id":        run_id,
        "config_sha256":          config_sha256,
        "protocol_file":          args.protocol_path,
        "results":                results,
        "per_symbol_summary":     per_symbol,
        "verdict":                verdict,
        "verdict_reason":         verdict_reason,
        "hypothesis_verdict":     hypothesis_verdict,
        "trade_diagnostics_summary": trade_diagnostics_summary if all_trade_records else None,
        "prescreen_backtest_cross_check": cross_check,
        # E-039 step 5 (2026-09-12): CUL-265's per-symbol A8.5.1a methodology
        # label was computed (extended_for_cross_check, above) and used
        # transiently for the cross-check, but never actually persisted --
        # exposing it here so the relocated pre-registration conformance
        # check (which replaces the removed signal_prescreen stage's own
        # significance_methodology_used check) has something real to read.
        "episode_blocked_significance_by_symbol": {
            s: v.get("episode_blocked_significance_method")
            for s, v in extended_for_cross_check.items()
        } if extended_for_cross_check else None,
    }
    (out_dir / "protocol_summary.json").write_text(
        json.dumps(summary, indent=2, default=str), encoding="utf-8"
    )
    print(f"\nProtocol summary: {out_dir / 'protocol_summary.json'}")
    print(f"Verdict : {verdict}")
    print(f"Reason  : {verdict_reason}")


if __name__ == "__main__":
    main()
