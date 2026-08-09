"""
run_protocol.py — walk-forward protocol runner.

CLI (run from repo root or strategy-research/):
  python strategy-research/tools/run_protocol.py <config_path> <protocol_path>
  python strategy-research/tools/run_protocol.py <config_path> <protocol_path> --holdout --i-understand
"""
import sys
import os
import csv
import json
import math
import argparse
import statistics
import re
from datetime import datetime, timezone, date
from hashlib import sha256
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))   # strategy-research/tools/
_SR   = os.path.dirname(_HERE)                        # strategy-research/
_REPO = os.path.dirname(_SR)                          # repo root
_TBOT = os.path.join(_REPO, "trading-bot")            # trading-bot/

if _TBOT not in sys.path:
    sys.path.insert(0, _TBOT)

from core.launcher import run_backtest, parse_interval_seconds

_RESULTS_ROOT = os.path.join(_SR, "results")

# A3.4: windows with fewer than this many closed trades get null Sharpe in protocol_result
_SPARSE_TRADE_FLOOR = 5


def _config_sha(config_path: str):
    with open(config_path, encoding="utf-8") as f:
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
    with open(p, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rows.append({
                    "timestamp": row["timestamp"],
                    "open":  float(row["open"])  if row.get("open")  else None,
                    "high":  float(row["high"])  if row.get("high")  else None,
                    "low":   float(row["low"])   if row.get("low")   else None,
                    "close": float(row["close"]) if row.get("close") else None,
                })
            except (ValueError, KeyError):
                pass
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


def _commission_rate_for_symbol(symbol: str, cost_model: dict | None, product: str = "spot") -> float | None:
    """
    2026-07-20 (Dispatch H): convert cost_model.yaml's fee_rate_bps[symbol] (a
    ONE-WAY taker fee in bps, per that file's own header) into launcher.run_backtest's
    commission_rate (a per-side fraction, e.g. 0.0005 for 5bps). Straight bps->fraction
    conversion (/10000), NOT a round-trip conversion: portfolio_info.py's
    update_local_balance applies commission_rate exactly twice per round trip for BOTH
    LONG (once at 'LONG' open, once at 'REDUCE_LONG'/'CLOSE') and SHORT (once at
    'SHORT' open, once at 'REDUCE_SHORT'/'CLOSE') -- confirmed symmetric by direct code
    read and cross-checked against real trades.json records (entry_commission +
    exit_commission = total_commission on both LONG and SHORT trades in run_018). So a
    single per-event fraction of fee_bps/10000 reproduces a round-trip cost of
    fee_bps*2, matching cost_model.yaml's own round_trip_cost_bps = 2*taker_fee+...
    convention -- no *2 or /2 here, that would double- or half-charge.

    product: 'spot' (default, reads the top-level fee_rate_bps -- unchanged existing
        behavior) or 'perp' (reads the additive cost_model['perp']['fee_rate_bps']
        block instead). NOT a general default switch: callers must opt into 'perp'
        explicitly per invocation (see main()'s --cost-product flag) so unrelated
        spot/default runs are never silently re-costed at perp rates.

    Returns None (defer to the engine's own DEFAULT_COMMISSION_RATE) if no cost model
    is loaded, the requested product block is absent, or the symbol has neither a
    specific nor a 'default' fee_rate_bps entry.
    """
    if not cost_model:
        return None
    if product == "perp":
        fees = cost_model.get("perp", {}).get("fee_rate_bps", {})
    else:
        fees = cost_model.get("fee_rate_bps", {})
    rate_bps = fees.get(symbol)
    if rate_bps is None:
        rate_bps = fees.get("default")
    if rate_bps is None:
        return None
    return float(rate_bps) / 10000.0


def _resolve_commission_rate(
    symbol: str, cost_model: dict | None, commission_bps: float | None, product: str
) -> float | None:
    """
    2026-07-20 (Dispatch L): --commission-bps, when set, takes precedence over
    --cost-product for every symbol -- an explicit, flat one-way-per-leg rate for
    controlled fee-isolation experiments, independent of cost_model.yaml (useful
    when neither the 'spot' nor 'perp' block happens to supply the exact rate an
    experiment needs, e.g. the historical DEFAULT_COMMISSION_RATE of 10bps, which
    is neither cost_model.yaml's spot 7.5bps nor its perp 5bps). Same conversion
    as _commission_rate_for_symbol (fee_bps / 10000, one-way-per-side, no
    double-charge -- see that function's docstring for the full rationale; the
    engine applies commission_rate exactly twice per round trip for both LONG and
    SHORT, so no extra *2/  /2 factor here either).

    commission_bps absent (None): falls through unchanged to
    _commission_rate_for_symbol(..., product=product) -- byte-identical to
    pre-existing (pre-Dispatch-L) behavior.
    """
    if commission_bps is not None:
        return float(commission_bps) / 10000.0
    return _commission_rate_for_symbol(symbol, cost_model, product=product)


def _ts_normalize(ts: str) -> str:
    """Normalize ISO 8601 trade timestamp to bars.csv format ('YYYY-MM-DD HH:MM:SS')."""
    return ts.replace("T", " ").split("+")[0].split("Z")[0]


def _bar_idx_at(bars: list, ts_str: str) -> int:
    """Return index of bar with timestamp matching ts_str, or -1."""
    for i, b in enumerate(bars):
        if b["timestamp"] == ts_str:
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
    if exit_idx == len(bars) - 1:
        return "end_of_window"

    # Signal flip: forecast at exit contradicts the position direction
    if side == "LONG" and (exit_forecast is not None) and exit_forecast <= 0:
        return "signal_flip"
    if side == "SHORT" and (exit_forecast is not None) and exit_forecast >= 0:
        return "signal_flip"
    return "signal_flip"  # default (allocation dropped below rebalance threshold)


def _cost_paid_bps(trade: dict, cost_model: dict | None) -> float:
    """
    A3.2: per-trade round-trip cost in bps.
    Uses config/cost_model.yaml when available; falls back to actual commission data.
    """
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
) -> list:
    """
    Compute per-trade diagnostic records for one backtest window.
    Returns empty list if no trades or missing data files.
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
        cost_bps = _cost_paid_bps(trade, cost_model)

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
        })
    return records


def _aggregate_trade_diagnostics(all_records: list, results: list) -> dict:
    """
    Aggregate per-trade records into the trade_diagnostics_summary block.
    Includes A3.1 stop_loss_recovery_rate, A3.4 per_trade_expectancy_bps and zero_trade_slot_pct.

    Win rate: uses profitable_net (engine's net-of-commission definition) — NOT gross realized_return > 0.
    Expectancy bps: uses net_portfolio_return_pct (portfolio-level net) — NOT position-level gross.
    These two fixes ensure the keltner_163 fixture reproduces 50.7%→57.4% / −26→−58 bps.
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
    """
    corrs = [r['core'].get('forecast_return_corr') for r in rows
             if r.get('core', {}).get('forecast_return_corr') is not None]
    if corrs:
        return round(statistics.median(corrs), 4), 'per_window_median_pearson'
    if runs_root is None:
        return None, None

    import pandas as pd
    sys.path.insert(0, _HERE)
    import prescreen_signal as _ps

    records = []
    for r in sorted(rows, key=lambda x: x['window']):
        bars_path = Path(runs_root) / r['run_id'] / 'bars.csv'
        if not bars_path.exists():
            continue
        bdf = pd.read_csv(bars_path)
        if 'forecast' not in bdf.columns or 'close' not in bdf.columns:
            continue
        closes = bdf['close'].tolist()
        forecasts = bdf['forecast'].tolist()
        for i in range(len(bdf) - 1):
            if closes[i] == 0:
                continue
            records.append({
                'forecast': float(forecasts[i]),
                'next_return_bps': (closes[i + 1] - closes[i]) / closes[i] * 10000.0,
            })
    if not records:
        return None, None

    symbol = rows[0]['symbol']
    boot = _ps._stationary_block_bootstrap_ic_significance({symbol: records})
    return boot.get('pooled_ic'), boot['method']


def _build_extended_summary(per_symbol_summary: dict, results: list, runs_root=None) -> dict:
    """Augment per_symbol_summary with median_win_rate, regime_frequency, and
    median_forecast_return_corr (with a degenerate-signal bootstrap fallback --
    see _pooled_ic_with_bootstrap_fallback)."""
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
    """
    extended = _build_extended_summary(per_symbol_summary, results, runs_root)

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

    # Diagnostics block — evidence for altitude decision by verdict_interpreter
    gross_pnls  = [r["core"].get("gross_pnl")                for r in results if r["core"].get("gross_pnl")                is not None]
    cost_drags  = [r["core"].get("cost_drag_pct")            for r in results if r["core"].get("cost_drag_pct")            is not None]
    corrs       = [r["core"].get("forecast_return_corr")     for r in results if r["core"].get("forecast_return_corr")     is not None]
    durations   = [r["core"].get("avg_trade_duration_bars")  for r in results if r["core"].get("avg_trade_duration_bars")  is not None]

    uninformative: list = []
    for r in results:
        for regime, stats in r.get("regime_validity", {}).items():
            if not stats.get("informative", True) and regime not in uninformative:
                uninformative.append(regime)

    wr_rows     = [row for row in criteria_results if row.get("field") == "median_win_rate"]
    sharpe_rows = [row for row in criteria_results if row.get("field") == "median_sharpe"]
    wr_pass     = bool(wr_rows)     and all(r["result"] == "PASS" for r in wr_rows)
    sharpe_fail = bool(sharpe_rows) and any(r["result"] == "FAIL" for r in sharpe_rows)
    if wr_pass and sharpe_fail:
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
    }

    # A3.4: inject per_trade_expectancy_bps and zero_trade_slot_pct from trade diagnostics
    if trade_diagnostics_summary:
        diagnostics["per_trade_expectancy_bps"] = trade_diagnostics_summary.get("per_trade_expectancy_bps")
        diagnostics["zero_trade_slot_pct"]       = trade_diagnostics_summary.get("zero_trade_slot_pct")

    return {
        'verdict':          verdict,
        'criteria_results': criteria_results,
        'verdict_reason':   f"{fail_n} of {len(tested)} evaluable criteria FAIL; "
                            f"{len(untested)} UNTESTED",
        'diagnostics':      diagnostics,
    }


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
    parser.add_argument("--validation-protocol", default=None,
                        help="Path to validation_protocol.yaml for hypothesis-specific verdict")
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
    args = parser.parse_args()

    # Holdout gate: require BOTH flags or NEITHER
    if args.holdout != args.i_understand:
        print("ERROR: --holdout requires --i-understand (and vice versa). Pass both or neither.",
              file=sys.stderr)
        sys.exit(1)

    if args.commission_bps is not None:
        print(f"[cost-override] --commission-bps={args.commission_bps} -> "
              f"commission_rate={float(args.commission_bps) / 10000.0} "
              f"(takes precedence over --cost-product={args.cost_product!r} for this entire run)")

    with open(args.protocol_path, encoding="utf-8") as f:
        protocol = json.load(f)

    config_sha256, config_sha8 = _config_sha(args.config_path)
    symbols = protocol["symbols"]
    # Option Y (locked 2026-08-09, Ticket 13): --exchange -> protocol field ->
    # explicit "binance". NEVER None -- unlike interval_seconds/commission_rate
    # below, venue is the knob where falling through to run_backtest's own
    # config.json-read arm would let ambient, machine-local state silently
    # decide which market a campaign scores. Every existing campaign (no field,
    # no flag) resolves to "binance", identical to the venue it already scored
    # via the engine's own pre-existing default -- byte-identical by construction.
    exchange = args.exchange or protocol.get("exchange") or "binance"
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

    cost_model = _load_cost_model()

    # ------------------------------------------------------------------
    # HOLDOUT MODE
    # ------------------------------------------------------------------
    if args.holdout:
        h = protocol["holdout"]
        start = h["start"]
        end   = h["end"] if h["end"] is not None else date.today().isoformat()

        _runs_root = str(out_dir / "results") if args.out_dir else None
        holdout_results = {}
        for symbol in symbols:
            print(f"[holdout] {symbol}  {start} to {end} ...")
            # 2026-07-07: warmup_prefetch=True unconditionally -- see
            # launcher.run_backtest's docstring. No holdout_start guard here: this
            # loop's OWN start IS the holdout start, so its prefetch legitimately
            # reaches backward into pre-holdout training data for warmup only
            # (never scored) -- that's the intended, correct behavior.
            rd = run_backtest(args.config_path, symbol, start, end, _RESULTS_ROOT,
                              runs_root=_runs_root, interval_seconds=interval_seconds,
                              warmup_prefetch=True,
                              commission_rate=_resolve_commission_rate(
                                  symbol, cost_model, args.commission_bps, args.cost_product),
                              exchange=exchange)
            with open(rd / "metrics.json", encoding="utf-8") as f:
                m = json.load(f)
            holdout_results[symbol] = {"run_id": rd.name, "core": m["core"]}

        payload = {
            "protocol_run_id": run_id,
            "config_sha256":   config_sha256,
            "holdout_window":  {"start": start, "end": end},
            "results":         holdout_results,
        }
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

    # 2026-07-07: holdout boundary guard for the warmup_prefetch buffer (see
    # launcher.run_backtest's warmup_prefetch docstring). Read once; every window
    # is checked against it below, both directly (this loop, general protocol
    # sanity: no training window may reach into holdout) and inside run_backtest
    # itself (the prefetch's computed fetch_start must stay before it too).
    _holdout_start = protocol.get("holdout", {}).get("start")

    for symbol in symbols:
        for window in protocol["windows"]:
            label     = window["label"]
            start     = window["test"]["start"]
            end       = window["test"]["end"]
            if _holdout_start is not None:
                # STRICTLY less than, not <=. `end` reads as an exclusive bound
                # (the next window starts on the same date) but it is not one:
                # run_backtest passes it to load_data(end_date=end), which
                # yields every bar of the end DAY through 23:00. So end ==
                # holdout_start materialises 24 holdout bars. The <= form let
                # exactly that through -- see campaign_data_policy.yaml:
                # holdout_contaminated_runs, whose declared range ends at
                # day 1 of the seal, 23:00.
                assert end < _holdout_start, (
                    f"Window {label} ({symbol}) ends {end}, at or past holdout_start="
                    f"{_holdout_start} -- a training window must never reach into the "
                    f"holdout range. NB `end` is INCLUSIVE-BY-DAY at the engine, so an "
                    f"end equal to holdout_start still materialises that whole day's "
                    f"bars. Fix the protocol's windows before proceeding."
                )
            print(f"  {symbol}  window={label}  {start} to {end} ...")
            rd = run_backtest(args.config_path, symbol, start, end, _RESULTS_ROOT,
                              runs_root=_runs_root, interval_seconds=interval_seconds,
                              warmup_prefetch=True, holdout_start=_holdout_start,
                              commission_rate=_resolve_commission_rate(
                                  symbol, cost_model, args.commission_bps, args.cost_product),
                              exchange=exchange)
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
            }
            results.append(result_entry)

            # Step 03: compute trade diagnostics while run directory is available
            trade_records = _compute_trade_records_for_window(
                rd, symbol, label, end, cost_model
            )
            all_trade_records.extend(trade_records)

            print(f"    sharpe={core.get('sharpe') or 0:.3f}  trades={m['core'].get('trade_count', 0)}"
                  f"  dd={m['core'].get('max_drawdown_pct', 0):.1f}%")

    # Step 03: aggregate trade diagnostics and write trade_diagnostics.json
    trade_diagnostics_summary = _aggregate_trade_diagnostics(all_trade_records, results)
    if all_trade_records:
        td_payload = {
            # A3.5: keltner_163 fixture — production of this artifact is what the regression
            # fixture tests against. Run against strategy-research/results/protocols/
            # 20260702T091324Z_18fad381/protocol_summary.json to reproduce the known signature:
            # win rate 51%→57% from 2024→2025 cohorts while per-trade expectancy −26→−58 bps.
            "trades":  all_trade_records,
            "summary": trade_diagnostics_summary,
        }
        (out_dir / "trade_diagnostics.json").write_text(
            json.dumps(td_payload, indent=2, default=str), encoding="utf-8"
        )
        print(f"Trade diagnostics: {out_dir / 'trade_diagnostics.json'} "
              f"({len(all_trade_records)} trades)")

    # Per-symbol summary (A3.4: median_sharpe excludes null-sharpe sparse windows)
    promo = protocol["promotion"]
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
        verdict = "promote"
        parts = [f"{s}: median_sharpe={per_symbol[s]['median_sharpe']:.3f}>0"
                 f" max_dd={per_symbol[s]['max_abs_drawdown_pct']:.1f}%<30"
                 f" min_trades={per_symbol[s]['min_trade_count']}>=20"
                 for s in symbols]
        verdict_reason = "; ".join(parts)
    elif all(_kill(s) for s in symbols):
        verdict = "kill"
        parts = [f"{s}: median_sharpe={per_symbol[s]['median_sharpe']:.3f}<-1" for s in symbols]
        verdict_reason = "both symbols below kill threshold: " + ", ".join(parts)
    else:
        verdict = "refine"
        parts = []
        for s in symbols:
            p = per_symbol[s]
            fails = []
            if p["median_sharpe"] is None:
                fails.append("median_sharpe=null (all windows sparse)")
            elif p["median_sharpe"] <= promo["median_sharpe_gt"]:
                fails.append(f"median_sharpe={p['median_sharpe']:.3f}<=0")
            if p["max_abs_drawdown_pct"] >= promo["max_abs_drawdown_pct_lt"]:
                fails.append(f"max_dd={p['max_abs_drawdown_pct']:.1f}%>=30")
            if p["min_trade_count"] < promo["min_trade_count_gte"]:
                fails.append(f"min_trades={p['min_trade_count']}<20")
            if fails:
                parts.append(f"{s}: " + ", ".join(fails))
        verdict_reason = "; ".join(parts) if parts else "mixed — not all pass promote, not all fail at kill"

    # 2026-07-09: compute the extended (bootstrap-fallback-resolved) per-symbol
    # summary BEFORE the cross-check, so the check reports whether the
    # fallback already reconciled prescreen/backtest, rather than flagging a
    # "disagreement" that's actually been resolved elsewhere in this same file.
    extended_for_cross_check = _build_extended_summary(per_symbol, results, _runs_root)
    cross_check = _cross_check_prescreen_vs_backtest(out_dir, results, extended_for_cross_check)

    hypothesis_verdict = None
    if args.validation_protocol:
        import yaml
        with open(args.validation_protocol, encoding="utf-8") as f:
            vp = yaml.safe_load(f)
        hypothesis_verdict = evaluate_against_decision_rules(
            per_symbol, results, vp, trade_diagnostics_summary or None,
            runs_root=_runs_root,
        )
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
    }
    (out_dir / "protocol_summary.json").write_text(
        json.dumps(summary, indent=2, default=str), encoding="utf-8"
    )
    print(f"\nProtocol summary: {out_dir / 'protocol_summary.json'}")
    print(f"Verdict : {verdict}")
    print(f"Reason  : {verdict_reason}")


if __name__ == "__main__":
    main()
