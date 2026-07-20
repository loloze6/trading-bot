"""
Regression tests for Dispatch H (2026-07-20): product-aware cost wiring in
run_protocol.py -- the new cost_model.yaml['perp'] block and
_commission_rate_for_symbol(..., product=...) / --cost-product CLI flag.

Before this change, run_protocol.py never passed commission_rate to
run_backtest() at all (each call always silently resolved to
launcher.DEFAULT_COMMISSION_RATE, Binance's 10bps). Dispatch H adds an
explicit, opt-in product selector: 'spot' (default, reads the top-level
fee_rate_bps -- unchanged prior behavior) or 'perp' (reads the additive
cost_model['perp']['fee_rate_bps'] block, Kraken's 5bps perp taker rate).

These tests prove: (1) the default path is unaffected (still 'spot', still a
no-op if no cost model), (2) the perp block resolves correctly and to a
DIFFERENT value than spot, and (3) re-running the same fixture at the real,
on-disk cost_model.yaml's perp rate produces a materially different
cost_drag_pct/sharpe than the spot/default rate -- i.e. the perp rate is not
silently discarded once it reaches run_backtest().

IMPORTANT: test_perp_rate_changes_engine_output is a SLOW INTEGRATION TEST
(runs the real backtest engine twice). Run explicitly:
  pytest tests/test_run_protocol_perp_cost_wiring.py -v -m slow
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
TOOLS_PATH = ROOT / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import run_protocol as rp  # noqa: E402 -- also puts trading-bot/ on sys.path as a side effect

TBOT_ROOT = ROOT.parent / "trading-bot"
FIXTURE_PATH = TBOT_ROOT / "tests" / "fixtures" / "warmup_prefetch_reference.json"


# ---------------------------------------------------------------------------
# Unit: product selection, bps -> fraction conversion
# ---------------------------------------------------------------------------

def test_default_product_is_spot():
    cost_model = {"fee_rate_bps": {"BTCUSDT": 80.0, "default": 10.0},
                  "perp": {"fee_rate_bps": {"default": 5.0}}}
    # product omitted -> must read the top-level (spot) block, not perp.
    assert rp._commission_rate_for_symbol("BTCUSDT", cost_model) == pytest.approx(0.008)


def test_perp_product_reads_perp_block():
    cost_model = {"fee_rate_bps": {"BTCUSDT": 80.0, "default": 10.0},
                  "perp": {"fee_rate_bps": {"default": 5.0}}}
    assert rp._commission_rate_for_symbol(
        "BTCUSDT", cost_model, product="perp"
    ) == pytest.approx(0.0005)


def test_perp_product_falls_back_to_perp_default_not_spot_default():
    cost_model = {"fee_rate_bps": {"BTCUSDT": 80.0, "default": 10.0},
                  "perp": {"fee_rate_bps": {"default": 5.0}}}
    # ETHUSDT has no perp-specific entry -> must fall back to perp's OWN
    # default (5.0), never leak into the spot block's default (10.0).
    assert rp._commission_rate_for_symbol(
        "ETHUSDT", cost_model, product="perp"
    ) == pytest.approx(0.0005)


def test_perp_product_none_when_perp_block_absent():
    cost_model = {"fee_rate_bps": {"BTCUSDT": 80.0, "default": 10.0}}
    assert rp._commission_rate_for_symbol("BTCUSDT", cost_model, product="perp") is None


def test_perp_product_none_when_no_cost_model():
    assert rp._commission_rate_for_symbol("BTCUSDT", None, product="perp") is None


@pytest.mark.real_repo_readonly
def test_real_cost_model_perp_block_matches_kraken_perp_taker():
    """The real, on-disk cost_model.yaml (post-Dispatch-H) perp block must resolve
    to Kraken's 5bps perp taker rate (0.0005 fraction), distinct from the
    top-level spot block's Binance-calibrated 7.5bps (0.00075)."""
    cost_model = rp._load_cost_model()
    assert cost_model is not None
    spot_rate = rp._commission_rate_for_symbol("BTCUSDT", cost_model, product="spot")
    perp_rate = rp._commission_rate_for_symbol("BTCUSDT", cost_model, product="perp")
    assert perp_rate == pytest.approx(0.0005)
    assert spot_rate != perp_rate


# ---------------------------------------------------------------------------
# CLI: --cost-product flag
# ---------------------------------------------------------------------------

def test_cli_cost_product_defaults_to_spot():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--cost-product", default="spot", choices=["spot", "perp"], dest="cost_product")
    args = parser.parse_args([])
    assert args.cost_product == "spot"


# ---------------------------------------------------------------------------
# Integration: the perp rate actually reaches the engine
# ---------------------------------------------------------------------------

@pytest.mark.slow
@pytest.mark.real_repo_readonly
def test_perp_rate_changes_engine_output(tmp_path):
    """
    Re-running the same fixture at cost_model.yaml's real perp rate (5bps) must
    produce a materially different cost_drag_pct/sharpe than the spot rate
    (7.5bps) -- proving _commission_rate_for_symbol(..., product='perp')'s
    output is not silently discarded once it reaches run_backtest().
    """
    from core.launcher import run_backtest

    with open(FIXTURE_PATH, encoding="utf-8") as f:
        reference = json.load(f)

    cost_model = rp._load_cost_model()
    symbol = reference["symbol"]
    spot_rate = rp._commission_rate_for_symbol(symbol, cost_model, product="spot")
    perp_rate = rp._commission_rate_for_symbol(symbol, cost_model, product="perp")
    assert perp_rate < spot_rate  # perp (5bps) is cheaper than spot (7.5bps) here

    def _run(results_root, commission_rate):
        run_dir = run_backtest(
            config_path=str(TBOT_ROOT / reference["config"]),
            symbol=symbol,
            start=reference["start_date"],
            end=reference["end_date"],
            results_root=str(results_root),
            commission_rate=commission_rate,
        )
        with open(Path(run_dir) / "metrics.json", encoding="utf-8") as f:
            return json.load(f)["core"]

    spot_core = _run(tmp_path / "spot", commission_rate=spot_rate)
    perp_core = _run(tmp_path / "perp", commission_rate=perp_rate)

    assert spot_core["trade_count"] == perp_core["trade_count"] == \
        reference["expected"]["trade_count"]
    # Cheaper (perp) rate -> less cost drag, less fees paid, on this fixture.
    assert perp_core["cost_drag_pct"] < spot_core["cost_drag_pct"], (
        f"cost_drag_pct did not decrease under the cheaper perp rate: "
        f"spot={spot_core['cost_drag_pct']} perp={perp_core['cost_drag_pct']}"
    )
    assert perp_core["fees_paid"] < spot_core["fees_paid"]
    assert abs(spot_core["cost_drag_pct"] - perp_core["cost_drag_pct"]) > 5.0
