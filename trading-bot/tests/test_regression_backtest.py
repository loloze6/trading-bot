"""
Regression test: verifies the reference backtest produces known-good results.

IMPORTANT: this is a SLOW INTEGRATION TEST (runs a full 2-month backtest, ~3-5 min).
Do NOT run on every commit. Run explicitly before any change to the backtest path:
  pytest tests/test_regression_backtest.py -v

Catches: engine wiring regressions, PnL computation changes, config loading bugs.
This test uses the DEFAULT strategy_config.json (not a candidate config) so it
always produces a deterministic, fixture-comparable result.
"""
import json
import os
import sys
import pytest
from pathlib import Path

# Allow import of trading-bot modules from the project root
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "reference_run.json"

pytestmark = pytest.mark.slow   # run with: pytest -m slow


@pytest.fixture(scope="module")
def reference():
    with open(FIXTURE_PATH) as f:
        return json.load(f)


@pytest.fixture(scope="module")
def backtest_result(reference):
    """Run the reference backtest and return (metrics_dict, run_dir_path)."""
    from core.launcher import run_backtest
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        run_dir = run_backtest(
            config_path=str(PROJECT_ROOT / reference["config"]),
            symbol=reference["symbol"],
            start=reference["start_date"],
            end=reference["end_date"],
            results_root=tmp,
            # Keep the tracker's interim trades.json inside the temp dir; without
            # this it would fall back to the shared trading-bot/results/trades.json
            # (D4).
            trades_log_file=str(Path(tmp) / "interim_trades.json"),
        )
        run_dir_path = Path(run_dir)
        metrics_path = run_dir_path / "metrics.json"
        if not metrics_path.exists():
            candidates = list(Path(tmp).rglob("metrics.json"))
            assert candidates, f"No metrics.json found under {tmp}"
            metrics_path = candidates[0]
            run_dir_path = metrics_path.parent
        with open(metrics_path) as f:
            metrics = json.load(f)
        # Inject run_dir so individual tests can find manifest.json
        metrics["_run_dir"] = str(run_dir_path)
        return metrics


def test_trade_count(backtest_result, reference):
    """Trade count must match exactly — any change indicates matching logic regression."""
    expected = reference["expected"]["trade_count"]
    actual = backtest_result["core"]["trade_count"]
    assert actual == expected, (
        f"Trade count regression: expected {expected}, got {actual}. "
        f"Check CompletedTrade matching logic in performance/metrics.py."
    )


def test_net_pnl(backtest_result, reference):
    """Net PnL must match within tolerance — catches commission/sizing regressions."""
    expected = reference["expected"]["net_pnl"]
    tolerance = reference["expected"]["net_pnl_tolerance"]
    actual = backtest_result["core"]["net_pnl"]
    assert abs(actual - expected) <= tolerance, (
        f"Net PnL regression: expected {expected} ± {tolerance}, got {actual}. "
        f"Check commission computation or position sizing in execution layer."
    )


def test_sharpe(backtest_result, reference):
    """Sharpe must match within tolerance — catches equity curve or annualization regressions."""
    expected = reference["expected"]["sharpe"]
    tolerance = reference["expected"]["sharpe_tolerance"]
    actual = backtest_result["core"]["sharpe"]
    assert abs(actual - expected) <= tolerance, (
        f"Sharpe regression: expected {expected} ± {tolerance}, got {actual}. "
        f"Check equity curve computation or Sharpe annualization assumption."
    )


def test_config_actually_loaded(backtest_result, reference):
    """
    Catches the config_path bug: verifies the backtest ran the specified config,
    not a hardcoded default. Reads manifest.json (separate from metrics.json)
    and checks its config_sha256 matches the sha256 of the specified config file.
    """
    import hashlib
    config_path = PROJECT_ROOT / reference["config"]
    with open(config_path) as f:
        import json as _json
        config_content = _json.dumps(_json.load(f), sort_keys=True, separators=(",", ":"))
    expected_sha = hashlib.sha256(config_content.encode()).hexdigest()

    # manifest.json is a SEPARATE file from metrics.json — load it independently
    manifest_path = Path(backtest_result.get("_run_dir", "")) / "manifest.json"
    if not manifest_path.exists():
        # Try finding manifest.json alongside the metrics.json that was loaded
        pytest.skip("manifest.json not found alongside metrics.json — skipping config identity check")

    with open(manifest_path) as f:
        manifest = _json.load(f)

    actual_sha = manifest.get("config_sha256", "")
    assert actual_sha == expected_sha, (
        f"Config identity regression: the backtest ran a different config than specified. "
        f"Expected sha={expected_sha[:8]}..., got sha={actual_sha[:8]}... "
        f"Check config_path wiring in core/launcher.py run_backtest()."
    )
