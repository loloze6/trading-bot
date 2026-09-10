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


class InvalidCostModelError(ValueError):
    """Raised when a configured (exchange, market_type) entry in cost_model.json
    has an out-of-range fee_bps or slippage_bps value.

    Sibling to UnknownCostModelError in spirit -- fail loud, name the exact
    bad value and exactly where it came from, never silently clamp/default/
    warn-and-continue -- but a different failure shape: the (exchange,
    market_type) pair IS configured, its *value* is not sane. Two concrete
    silent-corruption paths this guards against (see cost_model.py's module
    docstring and execution/execution_handler.py's fill-price formulas):

      1. A negative slippage_bps (or fee_bps) would silently flip a cost into
         a subsidy -- slippage would HELP every trade instead of hurting it,
         producing a flattering but fake backtest.
      2. A slippage_bps at or above 10000 (100%) drives the sell-side fill
         formula close * (1 - slippage_bps / 10000) non-positive.

    Not a KeyError subclass -- the key IS present, so a bare KeyError would
    be misleading here.
    """


# Sanity ceiling for slippage_bps -- NOT a real-world/theoretical limit, a
# fat-finger tripwire. The real, committed cost_model.json (as of S3,
# 2026-09-10) tops out at 7.5 bps (kraken/futures "default" and its
# AVAXUSD/SOLUSD entries); every other configured value is <= 7.5 bps too.
# 500 bps (5%) is ~66x that real ship-time max: generous enough that no
# plausible calibrated value -- even a stressed, thin-book, flash-crash fill
# on an illiquid altcoin -- should ever legitimately reach it, while still
# catching an obvious units/typo error (e.g. "750" fat-fingered for "7.5",
# or a stray extra digit) with wide margin, long before the sell-side fill
# formula above can go non-positive at slippage_bps >= 10000. If a future,
# genuinely-calibrated value needs to exceed this, raise the constant
# deliberately (with the same reasoning updated), not silently.
MAX_SLIPPAGE_BPS = 500.0


def _validate_cost_model(model: dict, path: str) -> None:
    """Range/sign-check every fee_bps and slippage_bps value in a freshly
    parsed cost_model.json. Raises InvalidCostModelError on the first bad
    value found; never clamps, coerces, or defaults.

    Called from _load_cost_model, i.e. once per JSON parse -- resolve_cost_model
    has no caching today (execution_handler.py::MockExecutionHandler.
    _resolve_slippage_bps calls it fresh per trade, at fill time, per S3), so
    this validation rides the exact same per-call file read/parse rather than
    adding a new overhead pattern; it is a fixed, tiny (exchange x market_type)
    iteration, not a per-bar cost. Hoisting resolve_cost_model itself to a
    cached/one-time load is a separate, out-of-scope change.
    """
    for exchange, market_types in model.items():
        if not isinstance(market_types, dict):
            continue
        for market_type, entry in market_types.items():
            if not isinstance(entry, dict):
                continue
            where = f"{path} [{exchange!r}][{market_type!r}]"

            if "fee_bps" in entry:
                fee_bps = float(entry["fee_bps"])
                if fee_bps < 0:
                    raise InvalidCostModelError(
                        f"{where}.fee_bps = {entry['fee_bps']!r} is negative -- "
                        f"fee_bps must be >= 0 (a negative fee would pay the "
                        f"trader commission instead of charging it)."
                    )

            slippage_table = entry.get("slippage_bps")
            if isinstance(slippage_table, dict):
                for key, raw_value in slippage_table.items():
                    value = float(raw_value)
                    slip_where = f"{where}.slippage_bps[{key!r}]"
                    if value < 0:
                        raise InvalidCostModelError(
                            f"{slip_where} = {raw_value!r} is negative -- "
                            f"slippage_bps must be >= 0 (a negative value "
                            f"would silently make slippage HELP every trade "
                            f"instead of hurting it -- see "
                            f"execution_handler.py's fill-price formulas)."
                        )
                    if value > MAX_SLIPPAGE_BPS:
                        raise InvalidCostModelError(
                            f"{slip_where} = {raw_value!r} exceeds the "
                            f"MAX_SLIPPAGE_BPS sanity ceiling of "
                            f"{MAX_SLIPPAGE_BPS!r} (see config/cost_model.py's "
                            f"MAX_SLIPPAGE_BPS comment) -- today's real "
                            f"committed max is 7.5 bps; this is almost "
                            f"certainly a units/fat-finger error, not a real "
                            f"calibrated value."
                        )


def _load_cost_model(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        model = json.load(f)
    _validate_cost_model(model, path)
    return model


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
