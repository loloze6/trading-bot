"""
Regression test for the 2026-07-20 commission_rate parameter on
core/launcher.py::run_backtest (Dispatch C, commission-rate parameterization).

Reuses the existing warmup_prefetch_reference.json fixture (BTCUSDT,
2024-01-01 to 2024-01-11, tests/fixtures/warmup_prefetch_check_config.json) as the
golden default-commission-rate run: its captured expected net_pnl/sharpe already
document what the DEFAULT_COMMISSION_RATE (0.001) path produces, so omitting the
new parameter must reproduce those numbers exactly.

commission_rate defaults to None (resolves to DEFAULT_COMMISSION_RATE, imported
from performance.metrics -- see that module for why it lives there). This test
proves:
  (a) omitting it is a byte-identical no-op vs. the pre-existing golden fixture
  (b) a non-default rate propagates through position sizing itself -- not just a
      linear rescale of the fee total -- by changing a mid-run trade's
      matched_quantity (per strategy-research/docs/session_reports/
      20260720_run059_replay_feasibility.md's finding that trade sizing reads the
      fee-eroded total_portfolio_value carried over from the prior trade).

IMPORTANT: this is a SLOW INTEGRATION TEST. Run explicitly:
  pytest tests/test_commission_rate_param.py -v -m slow
"""
import json
import sys
from pathlib import Path

import pytest
from _cache_guard import cache_skip_reason

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "warmup_prefetch_reference.json"

_NEEDED_CACHES = ("BTCUSDT_1h.csv", "BTCUSDT_funding_8h.csv", "fear_greed_daily.csv")
_ref = json.loads(FIXTURE_PATH.read_text())
_CACHE_SKIP = cache_skip_reason(
    PROJECT_ROOT / "local_data", _NEEDED_CACHES, _ref["start_date"], _ref["end_date"]
)
pytestmark = [
    pytest.mark.slow,
    pytest.mark.skipif(_CACHE_SKIP is not None, reason=_CACHE_SKIP or "local_data caches usable"),
]


@pytest.fixture(scope="module")
def reference():
    with open(FIXTURE_PATH) as f:
        return json.load(f)


def _run(reference, tmp_path, **kwargs):
    from core.launcher import run_backtest

    run_dir = run_backtest(
        config_path=str(PROJECT_ROOT / reference["config"]),
        symbol=reference["symbol"],
        start=reference["start_date"],
        end=reference["end_date"],
        results_root=str(tmp_path),
        # Keep the tracker's interim trades.json inside tmp_path; without this it
        # would fall back to the shared trading-bot/results/trades.json (D4).
        trades_log_file=str(tmp_path / "interim_trades.json"),
        **kwargs,
    )
    with open(Path(run_dir) / "metrics.json") as f:
        metrics = json.load(f)
    trades_path = Path(run_dir) / "trades.json"
    trades = json.load(open(trades_path)) if trades_path.exists() else []
    return metrics, trades


def test_omitted_matches_reference_fixture(reference, tmp_path):
    """commission_rate omitted must match the pre-existing golden fixture."""
    metrics, _ = _run(reference, tmp_path)
    core = metrics["core"]
    exp = reference["expected"]
    assert core["trade_count"] == exp["trade_count"]
    assert abs(core["net_pnl"] - exp["net_pnl"]) <= exp["net_pnl_tolerance"]
    assert abs(core["sharpe"] - exp["sharpe"]) <= exp["sharpe_tolerance"]


def test_explicit_default_matches_omitted(reference, tmp_path):
    """commission_rate=DEFAULT_COMMISSION_RATE explicitly must be IDENTICAL to omitting it."""
    from performance.metrics import DEFAULT_COMMISSION_RATE

    omitted_metrics, omitted_trades = _run(reference, tmp_path / "omitted")
    explicit_metrics, explicit_trades = _run(
        reference, tmp_path / "explicit", commission_rate=DEFAULT_COMMISSION_RATE
    )
    assert omitted_metrics["core"] == explicit_metrics["core"]
    assert omitted_trades == explicit_trades


def test_nondefault_rate_changes_trade_path(reference, tmp_path):
    """
    A non-default commission_rate (Kraken's 80 bps taker rate) must move
    fees_paid/cost_drag_pct/sharpe/net_pnl in the expected direction (higher rate ->
    higher fees_paid and cost_drag_pct, lower sharpe and net_pnl here) AND must
    change the SECOND trade's matched_quantity specifically -- proving the cost
    change propagates through position sizing (fee-eroded portfolio value feeding
    the next trade's size), not merely rescaling a summed fee total after the fact.
    The first trade's matched_quantity is expected to stay IDENTICAL across rates:
    its size is computed off the fixed initial balance, before any commission has
    been deducted from anything yet.
    """
    default_metrics, default_trades = _run(reference, tmp_path / "default")
    kraken_metrics, kraken_trades = _run(
        reference, tmp_path / "kraken", commission_rate=0.008
    )

    default_core = default_metrics["core"]
    kraken_core = kraken_metrics["core"]

    assert kraken_core["fees_paid"] > default_core["fees_paid"]
    assert kraken_core["cost_drag_pct"] > default_core["cost_drag_pct"]
    assert kraken_core["sharpe"] < default_core["sharpe"]
    assert kraken_core["net_pnl"] < default_core["net_pnl"]

    assert len(default_trades) >= 2 and len(kraken_trades) >= 2
    assert default_trades[0]["matched_quantity"] == kraken_trades[0]["matched_quantity"]
    assert default_trades[1]["matched_quantity"] != kraken_trades[1]["matched_quantity"]
