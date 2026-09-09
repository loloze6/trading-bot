"""
Cost model resolver -- fee_bps/slippage_bps lookup keyed by (exchange, market_type).

Part of E-010 (Slippage and lot-size/min-notional model). `trading-bot/config/
cost_model.json` is the single settings source both existing, previously-
independent commission mechanisms must resolve `fee_bps` from:

  1. performance/metrics.py's DEFAULT_COMMISSION_RATE / EnhancedPerformanceTracker
     -- drives reported P&L/Sharpe (what any promotion decision reads).
  2. execution/portfolio_info.py's CommonPortfolioDef(commission_rate=0.001)
     -- drives the actual simulated balance mutation (real position sizing).

execution/execution_handler.py's MockExecutionHandler resolves `slippage_bps`
from the same lookup, per SYMBOL, at fill time (see its own docstring for the
price-adjustment seam).

`exchange` reuses the existing _validated_exchange()/ccxt-id concept
(core/launcher.py) -- this module does not validate the exchange id itself,
only look it up once it is already validated. `market_type` is new plumbing
(e.g. "margin", "futures"); nothing else in the codebase validates it either.

A missing (exchange, market_type) combination in cost_model.json IS the
venue-tradability check for cost-model purposes -- it raises loud rather than
silently defaulting, by design (E-010 design decision: no second, separate
"is this a valid venue" layer). See Linear project E-010 for the full design
log and CUL-46 for the venue-identity cross-reference.

S3 (2026-09-10, "slippage becomes on-by-default, real per-symbol calibration"):
`slippage_bps` in cost_model.json is no longer a flat number -- it is a
per-symbol map with a mandatory "default" fallback key, e.g.
{"default": 1.5, "BTCUSDT": 1, "ETHUSDT": 1.5}. A symbol with no explicit
entry resolves to "default" -- conservative (the highest known figure for
that venue), never a silent guess presented as calibrated. `fee_bps` is
UNAFFECTED by this change: real fee schedules don't vary per-symbol, only per
maker/taker tier, so it stays a flat float regardless of `symbol`.
"""
from __future__ import annotations

import json
import os
from typing import Tuple, Union

_DEFAULT_COST_MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "cost_model.json"
)


class UnknownCostModelError(KeyError):
    """Raised when cost_model.json has no entry for a (exchange, market_type) pair.

    Subclasses KeyError (the lookup that fails is a nested dict lookup) but
    carries a message naming exactly which combination is unconfigured and
    what IS configured, instead of a bare KeyError's single missing key.

    NOTE: a SYMBOL missing from an otherwise-configured (exchange, market_type)
    slippage table does NOT raise this -- that is the documented, logged
    fallback-to-"default" path (see resolve_cost_model's `used_fallback`
    return value), not an unconfigured venue. Only a genuinely unconfigured
    (exchange, market_type) pair raises.
    """


def _load_cost_model(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_cost_model(
    exchange: str,
    market_type: str,
    symbol: str | None = None,
    path: str = _DEFAULT_COST_MODEL_PATH,
) -> Union[Tuple[float, dict], Tuple[float, float, bool]]:
    """
    Look up (fee_bps, slippage_bps) for (exchange, market_type) in cost_model.json.

    fee_bps is always a flat float, unaffected by `symbol` -- real fee
    schedules don't vary per-symbol, only per maker/taker tier.

    slippage_bps DOES vary per symbol (S3, 2026-09-10). Two calling
    conventions, selected by whether `symbol` is given:

      symbol=None (default): returns (fee_bps, slippage_table) where
        slippage_table is the RAW per-symbol dict straight from
        cost_model.json (always has at least a "default" key). For callers
        that need the whole table rather than one trade's fill -- e.g. run
        manifest provenance (core/backtester.py's cost_model_provenance fold).

      symbol="BTCUSDT" (etc.): returns (fee_bps, slippage_bps, used_fallback)
        where slippage_bps is the float resolved for THIS symbol (falling
        back to the table's "default" entry when the symbol has no explicit
        key), and used_fallback is True exactly when that fallback fired. A
        caller that executes a real trade using a used_fallback=True value
        MUST log it (see execution_handler.py's MockExecutionHandler.
        _resolve_slippage_bps) -- a fallback estimate must never silently
        read as a calibrated number for that symbol.

    Raises:
        UnknownCostModelError: no cost_model.json entry exists for this
        (exchange, market_type) combination. No silent fallback and no
        default fee/slippage table -- a caller must never catch this and
        substitute a guess; an unconfigured venue/market_type must not run.
        A symbol missing from an otherwise-configured venue's slippage table
        is a DIFFERENT case (the used_fallback path above), not this raise.
    """
    model = _load_cost_model(path)
    exchange_block = model.get(exchange)
    if exchange_block is None or market_type not in exchange_block:
        configured = {ex: sorted(mts.keys()) for ex, mts in model.items()}
        raise UnknownCostModelError(
            f"No cost model configured for (exchange={exchange!r}, "
            f"market_type={market_type!r}). Configured combinations: {configured}. "
            f"Add an entry to {path} before backtesting this venue/market_type."
        )
    entry = exchange_block[market_type]
    fee_bps = float(entry["fee_bps"])
    slippage_table = entry["slippage_bps"]
    if symbol is None:
        return fee_bps, slippage_table
    if symbol in slippage_table:
        return fee_bps, float(slippage_table[symbol]), False
    return fee_bps, float(slippage_table["default"]), True
