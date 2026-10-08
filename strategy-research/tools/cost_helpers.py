"""
Cost helpers shared by tools/run_protocol.py and tools/portfolio_whole_test.py
(E-062 S2a code review, findings 3 and 6; second round 6 and 7) -- ONE
definition of:

  * the commission the engine is charged per symbol, in bps (fee_bps_for_symbol,
    resolve_fee_bps) and as run_backtest's per-side fraction
    (commission_rate_for_symbol, resolve_commission_rate); and
  * the realized gross edge / cost ratio of a set of trade records
    (realized_edge_to_cost_ratio_unrounded; realized_edge_to_cost_ratio is the
    same value rounded to 4 decimals, as run_protocol's descriptive summary
    has always shown it).

Moved verbatim out of run_protocol.py (its _commission_rate_for_symbol,
_resolve_commission_rate and the inline ratio block of
_aggregate_trade_diagnostics), so a caller can use them WITHOUT importing
run_protocol, which imports trading-bot's core.launcher at module level. The
bps functions are the same lookup stopped before the /10000 conversion, so the
fraction functions return exactly what they returned before. run_protocol keeps
its old names as aliases/calls; its output is unchanged (pinned in
tests/test_e062_s2a_portfolio_whole_test.py). Standard library only.
"""
from __future__ import annotations

import statistics


def fee_bps_for_symbol(symbol: str, cost_model: dict | None, product: str = "spot") -> float | None:
    """One-way commission in bps for `symbol` from cost_model.yaml: the
    top-level fee_rate_bps (product 'spot') or cost_model['perp']['fee_rate_bps']
    (product 'perp'), the symbol's entry else 'default'. None when no cost
    model, no product block, or neither entry exists (the engine then uses its
    own default rate). See commission_rate_for_symbol for the full rationale."""
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
    return float(rate_bps)


def commission_rate_for_symbol(symbol: str, cost_model: dict | None, product: str = "spot") -> float | None:
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
        explicitly per invocation (see tools/run_protocol.py main()'s --cost-product
        flag) so unrelated spot/default runs are never silently re-costed at perp
        rates.

    Returns None (defer to the engine's own DEFAULT_COMMISSION_RATE) if no cost model
    is loaded, the requested product block is absent, or the symbol has neither a
    specific nor a 'default' fee_rate_bps entry.
    """
    rate_bps = fee_bps_for_symbol(symbol, cost_model, product=product)
    if rate_bps is None:
        return None
    return rate_bps / 10000.0


def resolve_fee_bps(
    symbol: str, cost_model: dict | None, commission_bps: float | None, product: str
) -> float | None:
    """One-way commission in bps the engine is charged for `symbol` under a
    run's flags: --commission-bps when set (it wins for every symbol), else
    fee_bps_for_symbol(symbol, cost_model, product). resolve_commission_rate is
    this value / 10000."""
    if commission_bps is not None:
        return float(commission_bps)
    return fee_bps_for_symbol(symbol, cost_model, product=product)


def resolve_commission_rate(
    symbol: str, cost_model: dict | None, commission_bps: float | None, product: str
) -> float | None:
    """
    2026-07-20 (Dispatch L): --commission-bps, when set, takes precedence over
    --cost-product for every symbol -- an explicit, flat one-way-per-leg rate for
    controlled fee-isolation experiments, independent of cost_model.yaml (useful
    when neither the 'spot' nor 'perp' block happens to supply the exact rate an
    experiment needs, e.g. the historical DEFAULT_COMMISSION_RATE of 10bps, which
    is neither cost_model.yaml's spot 7.5bps nor its perp 5bps). Same conversion
    as commission_rate_for_symbol (fee_bps / 10000, one-way-per-side, no
    double-charge -- see that function's docstring for the full rationale; the
    engine applies commission_rate exactly twice per round trip for both LONG and
    SHORT, so no extra *2/  /2 factor here either).

    commission_bps absent (None): falls through unchanged to
    commission_rate_for_symbol(..., product=product) -- byte-identical to
    pre-existing (pre-Dispatch-L) behavior.
    """
    if commission_bps is not None:
        return float(commission_bps) / 10000.0
    return commission_rate_for_symbol(symbol, cost_model, product=product)


def realized_edge_to_cost_ratio_unrounded(records: list) -> float | None:
    """CUL-300 realized gross edge / cost ratio of trade records, UNROUNDED
    (moved verbatim from run_protocol._aggregate_trade_diagnostics; comments
    kept). A pass/fail bar must compare this value, never the rounded one.

    Numerator is GROSS (pre-commission) edge, from realized_return -- the
    position-level gross return (% of position value). Deliberately NOT
    per_trade_expectancy_bps.mean: that figure is net_portfolio_return_pct,
    already net-of-commission -- dividing an already-net figure by cost again would
    double-count the fee deduction and understate how many multiples of cost the
    raw edge actually represents, which is what a cost-survival ratio needs to
    measure. cost_paid (denominator, A3.2) is also a position-level round-trip
    figure, so numerator and denominator share the same basis.
    CODE-REVIEW FIX (2026-09-20): numerator and denominator come from the exact
    same filtered set (records whose cost_paid is not None), so the ratio is
    always a like-for-like comparison over the trades that actually have a
    measured cost. Zero cost -> None, not inf/nan.
    """
    _records_with_cost = [r for r in records if r.get("cost_paid") is not None]
    gross_edge_bps_values = [r["realized_return"] * 100 for r in _records_with_cost]
    cost_bps_values = [r["cost_paid"] for r in _records_with_cost]
    mean_gross_edge_bps = statistics.mean(gross_edge_bps_values) if gross_edge_bps_values else None
    mean_cost_bps = statistics.mean(cost_bps_values) if cost_bps_values else None
    return (
        mean_gross_edge_bps / mean_cost_bps
        if mean_gross_edge_bps is not None and mean_cost_bps not in (None, 0)
        else None
    )


def realized_edge_to_cost_ratio(records: list) -> float | None:
    """realized_edge_to_cost_ratio_unrounded rounded to 4 decimals -- the
    descriptive figure run_protocol's trade_diagnostics_summary has always
    carried (round(mean_gross / mean_cost, 4))."""
    raw = realized_edge_to_cost_ratio_unrounded(records)
    return round(raw, 4) if raw is not None else None


def edge_to_all_costs_ratio_unrounded(records: list) -> float | None:
    """CUL-414 (orchestrator.cost_bar_all_costs, D-082): the D-038 "survives 2x
    costs" ratio with both sides on the same basis -- mean gross edge per trade
    BEFORE fees and slippage (gross_return_before_costs, % -> bps: the trade's
    return at the bar closes the fills were priced from) / mean cost per trade,
    fees + slippage, both legs (cost_paid_all, bps). realized_edge_to_cost_ratio
    divides a slippage-net return (fill prices) by fees only (A7).

    Records written by run_protocol --cost-bar-all-costs carry both fields; a
    record without them (None: its bars could not be matched, or an artifact
    written without the flag) is left out of numerator AND denominator, the same
    like-for-like rule as realized_edge_to_cost_ratio_unrounded. Zero mean cost
    or no record -> None. UNROUNDED: a pass/fail bar compares this value."""
    kept = [r for r in records
            if r.get("cost_paid_all") is not None and r.get("gross_return_before_costs") is not None]
    if not kept:
        return None
    mean_gross_bps = statistics.mean([r["gross_return_before_costs"] * 100 for r in kept])
    mean_cost_bps = statistics.mean([r["cost_paid_all"] for r in kept])
    return mean_gross_bps / mean_cost_bps if mean_cost_bps != 0 else None


def edge_to_all_costs_ratio(records: list) -> float | None:
    """edge_to_all_costs_ratio_unrounded rounded to 4 decimals, as
    realized_edge_to_cost_ratio is (run_protocol's descriptive summary field
    realized_edge_to_cost_ratio_all_costs, read by the menu criterion under
    the flag)."""
    raw = edge_to_all_costs_ratio_unrounded(records)
    return round(raw, 4) if raw is not None else None
