"""
Cost-structure revision: cost_model.yaml schema + sanity drift-guard.

Asserts config/cost_model.yaml has the required per-symbol keys, plausible fee/spread/
slippage bounds, and the verdict_execution_style hard rule. This does not check code
constants against the config (see test_campaign_config_sync.py for that pattern) —
prescreen_signal.py and run_protocol.py read cost_model.yaml at call time and have no
hardcoded mirrors to drift against. What CAN silently break is the yaml file itself:
a bad edit that drops a symbol, inverts a sign, or removes verdict_execution_style
would not raise until a run hits the missing key. This test catches that class of
regression directly, at collection time, without needing a live run.
"""

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
COST_MODEL_PATH = ROOT / "config" / "cost_model.yaml"

# P2 universe (confirmed 2026-07-04, cost-structure revision)
P2_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT"]

# Plausible bounds (bps, one-way unless noted). Binance spot fees range from
# VIP3+BNB (~3 bps) up to Regular-no-BNB (10 bps); anything outside this is either
# a stale/mistyped assumption or a tier this campaign has not verified.
FEE_BPS_MIN, FEE_BPS_MAX = 3.0, 10.0
SPREAD_BPS_MIN, SPREAD_BPS_MAX = 0.0, 10.0
SLIPPAGE_BPS_MIN, SLIPPAGE_BPS_MAX = 0.0, 5.0
ROUND_TRIP_BPS_MIN, ROUND_TRIP_BPS_MAX = 10.0, 40.0
SAFETY_FACTOR_MIN, SAFETY_FACTOR_MAX = 1.0, 5.0


@pytest.fixture(scope="module")
def cost_model():
    return yaml.safe_load(COST_MODEL_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# verdict_execution_style hard rule
# ---------------------------------------------------------------------------

def test_verdict_execution_style_present_and_taker(cost_model):
    assert "verdict_execution_style" in cost_model, (
        "cost_model.yaml is missing verdict_execution_style — gates and promotion "
        "evidence have no declared hard rule for which cost path to use"
    )
    assert cost_model["verdict_execution_style"] == "taker", (
        f"verdict_execution_style={cost_model['verdict_execution_style']!r}, expected "
        "'taker' — gates/promotion evidence must never key off the maker sensitivity path"
    )


# ---------------------------------------------------------------------------
# Required top-level keys (taker path — consumed directly by
# prescreen_signal.py._load_cost_model / run_protocol.py._cost_paid_bps)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("key", [
    "fee_rate_bps", "spread_estimate_bps", "slippage_estimate_bps",
    "round_trip_cost_bps", "safety_factor",
])
def test_required_top_level_key_present(cost_model, key):
    assert key in cost_model, f"cost_model.yaml missing required top-level key: {key}"


@pytest.mark.parametrize("block_key", [
    "fee_rate_bps", "spread_estimate_bps", "slippage_estimate_bps", "round_trip_cost_bps",
])
@pytest.mark.parametrize("symbol", P2_SYMBOLS)
def test_p2_symbol_present_in_taker_blocks(cost_model, block_key, symbol):
    block = cost_model[block_key]
    assert symbol in block, f"{block_key} missing P2 symbol {symbol}"
    assert "default" in block, f"{block_key} missing 'default' fallback key"


def test_safety_factor_plausible(cost_model):
    sf = cost_model["safety_factor"]
    assert SAFETY_FACTOR_MIN <= sf <= SAFETY_FACTOR_MAX, (
        f"safety_factor={sf} outside plausible bounds [{SAFETY_FACTOR_MIN}, {SAFETY_FACTOR_MAX}]"
    )


@pytest.mark.parametrize("symbol", P2_SYMBOLS)
def test_taker_fee_bounds(cost_model, symbol):
    fee = cost_model["fee_rate_bps"][symbol]
    assert FEE_BPS_MIN <= fee <= FEE_BPS_MAX, (
        f"fee_rate_bps[{symbol}]={fee} outside plausible Binance spot range "
        f"[{FEE_BPS_MIN}, {FEE_BPS_MAX}] bps"
    )


@pytest.mark.parametrize("symbol", P2_SYMBOLS)
def test_taker_spread_bounds(cost_model, symbol):
    spread = cost_model["spread_estimate_bps"][symbol]
    assert SPREAD_BPS_MIN <= spread <= SPREAD_BPS_MAX, (
        f"spread_estimate_bps[{symbol}]={spread} outside plausible range "
        f"[{SPREAD_BPS_MIN}, {SPREAD_BPS_MAX}] bps"
    )


@pytest.mark.parametrize("symbol", P2_SYMBOLS)
def test_taker_slippage_bounds(cost_model, symbol):
    slip = cost_model["slippage_estimate_bps"][symbol]
    assert SLIPPAGE_BPS_MIN <= slip <= SLIPPAGE_BPS_MAX, (
        f"slippage_estimate_bps[{symbol}]={slip} outside plausible range "
        f"[{SLIPPAGE_BPS_MIN}, {SLIPPAGE_BPS_MAX}] bps"
    )


@pytest.mark.parametrize("symbol", P2_SYMBOLS)
def test_round_trip_cost_bounds_and_arithmetic(cost_model, symbol):
    rtc = cost_model["round_trip_cost_bps"][symbol]
    assert ROUND_TRIP_BPS_MIN <= rtc <= ROUND_TRIP_BPS_MAX, (
        f"round_trip_cost_bps[{symbol}]={rtc} outside plausible range "
        f"[{ROUND_TRIP_BPS_MIN}, {ROUND_TRIP_BPS_MAX}] bps"
    )
    fee = cost_model["fee_rate_bps"][symbol]
    spread = cost_model["spread_estimate_bps"][symbol]
    slip = cost_model["slippage_estimate_bps"][symbol]
    expected = round(2 * fee + spread + slip, 2)
    assert abs(rtc - expected) < 0.01, (
        f"round_trip_cost_bps[{symbol}]={rtc} != 2*fee+spread+slippage={expected} "
        "(fee/spread/slippage edited without recomputing round_trip_cost_bps)"
    )


# ---------------------------------------------------------------------------
# execution_style block (additive maker/taker variants)
# ---------------------------------------------------------------------------

def test_execution_style_present(cost_model):
    assert "execution_style" in cost_model, "cost_model.yaml missing execution_style block"
    assert set(cost_model["execution_style"].keys()) >= {"taker", "maker"}, (
        "execution_style must define both 'taker' and 'maker'"
    )


@pytest.mark.parametrize("symbol", P2_SYMBOLS)
def test_execution_style_taker_mirrors_top_level(cost_model, symbol):
    """execution_style.taker must stay in sync with the top-level (code-consumed) keys."""
    es_taker = cost_model["execution_style"]["taker"]
    assert es_taker["fee_bps"][symbol] == cost_model["fee_rate_bps"][symbol]
    assert es_taker["spread_cost_bps"][symbol] == cost_model["spread_estimate_bps"][symbol]
    assert es_taker["slippage_bps"][symbol] == cost_model["slippage_estimate_bps"][symbol]
    assert es_taker["round_trip_cost_bps"][symbol] == cost_model["round_trip_cost_bps"][symbol]


@pytest.mark.parametrize("symbol", P2_SYMBOLS)
def test_execution_style_maker_fee_never_worse_than_taker(cost_model, symbol):
    """At no verified tier should the modeled maker fee exceed the taker fee."""
    maker_fee = cost_model["execution_style"]["maker"]["fee_bps"][symbol]
    taker_fee = cost_model["execution_style"]["taker"]["fee_bps"][symbol]
    assert maker_fee <= taker_fee, (
        f"maker fee_bps[{symbol}]={maker_fee} > taker fee_bps[{symbol}]={taker_fee} — "
        "implausible at any Binance spot tier"
    )


@pytest.mark.parametrize("symbol", P2_SYMBOLS)
def test_execution_style_maker_fill_rate_is_probability(cost_model, symbol):
    rate = cost_model["execution_style"]["maker"]["assumed_fill_rate"][symbol]
    assert 0.0 < rate <= 1.0, (
        f"assumed_fill_rate[{symbol}]={rate} must be a probability in (0, 1]"
    )


@pytest.mark.parametrize("symbol", P2_SYMBOLS)
def test_execution_style_maker_blended_between_if_filled_and_taker(cost_model, symbol):
    """
    round_trip_cost_bps_blended must lie between the best case (always filled at maker)
    and the worst case (never filled, falls back to taker) — a blend outside that
    range indicates a fill-rate or arithmetic error.
    """
    maker = cost_model["execution_style"]["maker"]
    if_filled = maker["round_trip_cost_bps_if_filled"][symbol]
    taker_rtc = cost_model["execution_style"]["taker"]["round_trip_cost_bps"][symbol]
    blended = maker["round_trip_cost_bps_blended"][symbol]
    lo, hi = min(if_filled, taker_rtc), max(if_filled, taker_rtc)
    assert lo - 0.01 <= blended <= hi + 0.01, (
        f"round_trip_cost_bps_blended[{symbol}]={blended} outside "
        f"[if_filled={if_filled}, taker={taker_rtc}]"
    )

    fill_rate = maker["assumed_fill_rate"][symbol]
    expected = round(fill_rate * if_filled + (1 - fill_rate) * taker_rtc, 2)
    assert abs(blended - expected) < 0.02, (
        f"round_trip_cost_bps_blended[{symbol}]={blended} != "
        f"fill_rate*if_filled + (1-fill_rate)*taker={expected}"
    )
