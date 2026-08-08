"""
Regression test: verifies the reference backtest produces known-good results.

IMPORTANT: this is a SLOW INTEGRATION TEST (runs a full 2-month backtest). Measured on
this machine: ~7s for this file, ~17s for the whole `-m slow` suite -- cheap enough to
run before any change to the backtest path, though runtime will vary by machine:
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
from _cache_guard import cache_skip_reason

# Allow import of trading-bot modules from the project root
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "reference_run.json"

_NEEDED_CACHES = ("BTCUSDT_1h.csv", "BTCUSDT_funding_8h.csv", "fear_greed_daily.csv")
_ref = json.loads(FIXTURE_PATH.read_text())
_CACHE_SKIP = cache_skip_reason(
    PROJECT_ROOT / "local_data", _NEEDED_CACHES, _ref["start_date"], _ref["end_date"]
)
pytestmark = [
    pytest.mark.slow,  # run with: pytest -m slow
    pytest.mark.skipif(_CACHE_SKIP is not None, reason=_CACHE_SKIP or "local_data caches usable"),
]


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
        yield metrics


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
    Manifest integrity check: the config_sha256 recorded in manifest.json must equal
    the canonical hash of the config file at the path this fixture launched with.
    Catches canonicalization drift or in-memory mutation of the config dict between
    load and write_manifest() (reporting/run_artifact.py:58-73) — i.e. the manifest
    lying about what config produced this run.

    Does NOT catch config_path wiring falling back to the hardcoded default
    (core/backtester.py:261-265): this fixture always launches with the DEFAULT
    strategy_config.json, which IS that fallback's file, so a broken config_path
    that silently falls back reads as a pass here. Needs a run against a non-default
    candidate config, tracked separately, to catch that class of bug.
    """
    import hashlib
    config_path = PROJECT_ROOT / reference["config"]
    with open(config_path) as f:
        import json as _json
        config_content = _json.dumps(_json.load(f), sort_keys=True, separators=(",", ":"))
    # sort_keys/separators here must stay in lockstep with write_manifest's own
    # canonicalization (reporting/run_artifact.py:68) — they agree by construction
    # today; nothing enforces the coupling if either changes independently.
    expected_sha = hashlib.sha256(config_content.encode()).hexdigest()

    # manifest.json is a SEPARATE file from metrics.json — load it independently
    manifest_path = Path(backtest_result.get("_run_dir", "")) / "manifest.json"
    if not manifest_path.exists():
        pytest.fail(
            f"manifest.json missing at {manifest_path}. write_manifest() is called "
            "unconditionally by BacktestEngine._end_of_backtest (core/backtester.py:279), "
            "so an absent manifest is an artifact-writer regression, not a skippable "
            "condition — this exact skip is what hid this test as dead code from "
            "0ca4666d until the fixture-lifetime fix."
        )

    with open(manifest_path) as f:
        manifest = _json.load(f)

    actual_sha = manifest.get("config_sha256", "")
    assert actual_sha == expected_sha, (
        f"Manifest config identity mismatch: manifest.json's config_sha256 does not "
        f"match the config file at the recorded path. "
        f"Expected sha={expected_sha[:8]}..., got sha={actual_sha[:8]}... "
        f"Causes: canonicalization drift vs write_manifest (reporting/run_artifact.py:68), "
        f"the config dict mutated between load and write_manifest, or the config file "
        f"changed on disk after the run. NOTE this cannot be a config_path fallback — "
        f"that reads as a pass here (see docstring)."
    )
