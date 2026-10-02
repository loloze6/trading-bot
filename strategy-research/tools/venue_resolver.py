"""
venue_resolver -- the brief's (venue, product) -> what the backtest models (O-12).

Until now a brief's `venue`/`product` reached only the tradability check
(E-014/E-015); the protocol named no exchange, so every backtest read Binance
data with the default costs (O-12; CUL-46 was the deferred design). This
module is the ONE place that turns a brief's (venue, product) into the
protocol keys the existing machinery already reads:

  * `exchange` + `market_type`: run_protocol.py passes both to run_backtest,
    so the engine prices fills from trading-bot/config/cost_model.json
    (E-010, the single cost source) for that (exchange, market_type), and
    reads that exchange's price data. The E-054 data gate already resolves
    `exchange` from the protocol (its Q2/Q3: it checks the protocol, never
    the brief).
  * a `venue` block of labels: product, market_type, price_source,
    price_proxy, funding_modelled, label -- carried into every result so it
    says what it modelled.
  * `symbols` in the price source's own naming (Kraken spot: BTCUSD).

Rules:
  * venue absent or "binance": None -- nothing is written, byte-identical to
    every run before this module (operator, 2026-10-02).
  * any other venue must resolve completely, or VenueResolutionError (fail
    loud at protocol creation, i.e. at run start before any LLM call; this
    replaces a separate registration gate, CUL-183):
      - a cost entry (exchange, market_type) in cost_model.json;
      - a price source: the market's own price data, or a declared
        `price_proxy` in config/venue_data_capability.yaml (E-054 Layer 1);
      - the price source must be the venue's SPOT market -- the only market
        the engine's price fetcher reads today (CcxtFetcher defaultType
        "spot", CUL-287).
  * one vocabulary alias, here only: product "perp" (venue_tradability.yaml)
    == market_type "futures" (cost_model.json, venue_data_capability.yaml).

Kraken futures (operator decision O-12, option A): Kraken SPOT prices as a
labelled proxy, Kraken FUTURES fees and slippage, funding not modelled.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml

_HERE = Path(__file__).resolve().parent
_SR = _HERE.parent
_TBOT = _SR.parent / "trading-bot"
LAYER1_PATH = _SR / "config" / "venue_data_capability.yaml"

DEFAULT_VENUE = "binance"
PRODUCT_ALIASES = {"perp": "futures"}  # brief/tradability word -> cost/capability key
ENGINE_PRICE_MARKET = "spot"           # CcxtFetcher's hardcoded defaultType (CUL-287)
_QUOTE_SUFFIXES = ("USDT", "USDC", "BUSD", "USD", "EUR")
_BASE_ALIASES = {"XBT": "BTC"}


class VenueResolutionError(ValueError):
    """The brief's (venue, product) cannot be backtested as declared."""


def base_asset(symbol: str) -> str:
    """BTCUSDT / BTCUSD / XBTUSD -> BTC."""
    base = str(symbol).upper()
    for quote in _QUOTE_SUFFIXES:
        if base.endswith(quote) and len(base) > len(quote):
            base = base[:-len(quote)]
            break
    return _BASE_ALIASES.get(base, base)


def load_layer1(path=LAYER1_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _fee_bps(exchange: str, market_type: str) -> float:
    if str(_TBOT) not in sys.path:
        sys.path.insert(0, str(_TBOT))
    from config.cost_model import resolve_cost_model, UnknownCostModelError  # noqa: E402
    try:
        fee_bps, _slippage_table = resolve_cost_model(exchange, market_type)
    except UnknownCostModelError as exc:
        raise VenueResolutionError(
            f"no cost entry for (exchange={exchange!r}, market_type={market_type!r}) in "
            f"trading-bot/config/cost_model.json (E-010) -- add one before backtesting this "
            f"venue/product") from exc
    return float(fee_bps)


def resolve(venue, product, *, layer1: dict | None = None) -> dict | None:
    """The protocol keys for a brief's (venue, product); None for the default
    venue (nothing written)."""
    if venue is None or str(venue).strip().lower() in ("", DEFAULT_VENUE):
        return None
    venue = str(venue).strip().lower()
    if not product:
        raise VenueResolutionError(f"brief venue {venue!r} has no product")
    product = str(product).strip().lower()
    market_type = PRODUCT_ALIASES.get(product, product)
    _fee_bps(venue, market_type)  # fail loud first: no cost entry, no run (value not copied:
    #                               cost_model.json stays the single source, E-010)
    layer1 = load_layer1() if layer1 is None else layer1
    venue_block = ((layer1.get("venues") or {}).get(venue)) or {}
    market_block = venue_block.get(market_type)
    if not isinstance(market_block, dict):
        raise VenueResolutionError(
            f"(venue={venue!r}, market={market_type!r}) is not in "
            f"config/venue_data_capability.yaml (E-054 Layer 1) -- unconfirmed, not available")
    proxy = market_block.get("price_proxy")
    if isinstance(proxy, dict) and proxy.get("source"):
        price_market, price_proxy = str(proxy["source"]), True
        label = proxy.get("label") or f"{venue} {price_market} prices as a proxy for {market_type}"
    else:
        price_market, price_proxy, label = market_type, False, None
    if price_market != ENGINE_PRICE_MARKET:
        raise VenueResolutionError(
            f"(venue={venue!r}, market={market_type!r}): prices would come from the "
            f"{price_market!r} market, but the engine reads only {ENGINE_PRICE_MARKET!r} prices "
            f"(CUL-287) -- declare a price_proxy in venue_data_capability.yaml or wire that market")
    if not isinstance(venue_block.get(price_market), dict):
        raise VenueResolutionError(
            f"price source {venue}.{price_market} is not in venue_data_capability.yaml")
    return {
        "exchange": venue,
        "market_type": market_type,
        "venue": {"venue": venue, "product": product, "market_type": market_type,
                  "price_source": f"{venue}.{price_market}", "price_proxy": price_proxy,
                  "funding_modelled": False,
                  **({"label": label} if label else {})},
    }


def venue_symbol(symbol: str, resolved: dict, *, layer1: dict | None = None) -> str:
    """A coin in the price source's own naming (Kraken spot: <BASE>USD),
    checked against that market's confirmed symbol list. Unknown -> raise."""
    venue, market = resolved["venue"]["price_source"].split(".", 1)
    layer1 = load_layer1() if layer1 is None else layer1
    block = (((layer1.get("venues") or {}).get(venue)) or {}).get(market) or {}
    confirmed = set(((block.get("symbols") or {}).get("confirmed_universe")) or [])
    candidates = [f"{base_asset(symbol)}{quote}" for quote in ("USD", "USDT")]
    for name in candidates:
        if name in confirmed:
            return name
    raise VenueResolutionError(
        f"coin {symbol!r} has no {venue}.{market} symbol in venue_data_capability.yaml "
        f"(tried {candidates}) -- not backtestable on this venue")


def protocol_keys(brief: dict, symbols: list, *, layer1: dict | None = None) -> dict:
    """Everything protocol creation writes for this brief: {} for the default
    venue, else exchange, market_type, venue labels and the mapped symbols."""
    resolved = resolve(brief.get("venue"), brief.get("product"), layer1=layer1)
    if resolved is None:
        return {}
    layer1 = load_layer1() if layer1 is None else layer1
    return {**resolved, "symbols": [venue_symbol(s, resolved, layer1=layer1) for s in symbols]}
