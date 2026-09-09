"""
Cost model resolver -- fee_bps/slippage_bps lookup keyed by (exchange, market_type).

Part of E-010 (Slippage and lot-size/min-notional model -- fee-rationalization
+ slippage pass, design finalized 2026-09-09). `trading-bot/config/cost_model.json`
is the single settings source both existing, previously-independent commission
mechanisms must resolve `fee_bps` from:

  1. performance/metrics.py's DEFAULT_COMMISSION_RATE / EnhancedPerformanceTracker
     -- drives reported P&L/Sharpe (what any promotion decision reads).
  2. execution/portfolio_info.py's CommonPortfolioDef(commission_rate=0.001)
     -- drives the actual simulated balance mutation (real position sizing).

execution/execution_handler.py's MockExecutionHandler resolves `slippage_bps`
from the same lookup (see its own docstring for the price-adjustment seam).

`exchange` reuses the existing _validated_exchange()/ccxt-id concept
(core/launcher.py) -- this module does not validate the exchange id itself,
only look it up once it is already validated. `market_type` is new plumbing
(e.g. "margin", "futures"); nothing else in the codebase validates it either.

A missing (exchange, market_type) combination in cost_model.json IS the
venue-tradability check for cost-model purposes -- it raises loud rather than
silently defaulting, by design (E-010 design decision: no second, separate
"is this a valid venue" layer). See Linear project E-010 for the full design
log and CUL-46 for the venue-identity cross-reference.
"""
from __future__ import annotations

import json
import os
from typing import Tuple

_DEFAULT_COST_MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "cost_model.json"
)


class UnknownCostModelError(KeyError):
    """Raised when cost_model.json has no entry for a (exchange, market_type) pair.

    Subclasses KeyError (the lookup that fails is a nested dict lookup) but
    carries a message naming exactly which combination is unconfigured and
    what IS configured, instead of a bare KeyError's single missing key.
    """


def _load_cost_model(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_cost_model(
    exchange: str,
    market_type: str,
    path: str = _DEFAULT_COST_MODEL_PATH,
) -> Tuple[float, float]:
    """
    Look up (fee_bps, slippage_bps) for (exchange, market_type) in cost_model.json.

    Returns:
        (fee_bps, slippage_bps) as floats.

    Raises:
        UnknownCostModelError: no entry exists for this combination. No silent
        fallback and no default fee -- a caller must never catch this and
        substitute a guess; an unconfigured venue/market_type must not run.
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
    return float(entry["fee_bps"]), float(entry["slippage_bps"])
