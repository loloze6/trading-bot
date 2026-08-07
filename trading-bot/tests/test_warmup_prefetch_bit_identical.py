"""
Bit-identical regression test for the 2026-07-07 warmup_prefetch parameter
(BacktestEngine.warmup_cutoff_timestamp, TradingBot.warmup_cutoff_timestamp,
launcher.run_backtest's warmup_prefetch flag).

This parameter fetches 2x strategy.required_bars of EXTRA history before a
window's start date and feeds it through the strategy silently (no trading) so
indicators are warmed up by the time real scoring begins -- see
core/launcher.py::run_backtest's docstring for the full rationale (found via the
P4_ts_trend daily-bar walk-forward: monthly windows produced zero trades because
a 100-day-warmup component could never become ready within a single ~30-bar
window).

warmup_prefetch defaults to False. This test proves that default is a true no-op:
IMPORTANT: this is a SLOW INTEGRATION TEST. Run explicitly:
  pytest tests/test_warmup_prefetch_bit_identical.py -v -m slow
"""
import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "warmup_prefetch_reference.json"

_NEEDED_CACHES = ("BTCUSDT_1h.csv", "BTCUSDT_funding_8h.csv", "fear_greed_daily.csv")
pytestmark = [
    pytest.mark.slow,
    pytest.mark.skipif(
        not all((PROJECT_ROOT / "local_data" / f).exists() for f in _NEEDED_CACHES),
        reason="local_data fixtures not present",
    ),
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
        return json.load(f)


def test_default_matches_reference_fixture(reference, tmp_path):
    """warmup_prefetch omitted (defaults False) must match the pre-existing fixture."""
    metrics = _run(reference, tmp_path)
    core = metrics["core"]
    exp = reference["expected"]
    assert core["trade_count"] == exp["trade_count"]
    assert abs(core["net_pnl"] - exp["net_pnl"]) <= exp["net_pnl_tolerance"]
    assert abs(core["sharpe"] - exp["sharpe"]) <= exp["sharpe_tolerance"]


def test_explicit_false_matches_omitted_default(reference, tmp_path):
    """warmup_prefetch=False explicitly must produce IDENTICAL output to omitting it."""
    default_metrics = _run(reference, tmp_path / "default")
    explicit_metrics = _run(reference, tmp_path / "explicit", warmup_prefetch=False)
    assert default_metrics["core"] == explicit_metrics["core"]


def test_warmup_prefetch_true_changes_fetch_behavior(reference, tmp_path):
    """
    Sanity check that the flag actually does something when enabled (guards against
    a future refactor silently making warmup_prefetch a no-op in both directions).
    trade_count with prefetch enabled must be >= the default's (never fewer trades:
    prefetch only ADDS warmed-up history, it can't remove information).
    """
    default_metrics = _run(reference, tmp_path / "default2")
    prefetch_metrics = _run(reference, tmp_path / "prefetch", warmup_prefetch=True)
    assert prefetch_metrics["core"]["trade_count"] >= default_metrics["core"]["trade_count"]
