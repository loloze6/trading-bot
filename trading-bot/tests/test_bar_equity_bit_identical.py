"""
Bit-identical regression test for the 2026-07-31 bar_equity parameter
(BacktestEngine.bar_equity, launcher.run_backtest's bar_equity flag).

This parameter adds an off-by-default "bar_equity" block to metrics.json,
computed from the full per-bar portfolio_states series instead of core's
trade-exit equity curve -- see core/launcher.py::run_backtest's docstring for
the full rationale and performance/bar_equity.py for the math.

bar_equity defaults to False. This test proves that default is a true no-op:
not just numerically equal output, but the "bar_equity" key never inserted
into metrics.json at all (reporting/run_artifact.py::write_metrics_json).

IMPORTANT: this is a SLOW INTEGRATION TEST. Run explicitly:
  pytest tests/test_bar_equity_bit_identical.py -v -m slow
"""

import json
import sys
from pathlib import Path

import pytest
from _cache_guard import cache_skip_reason

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "bar_equity_reference.json"

_NEEDED_CACHES = ("BTCUSDT_1h.csv", "BTCUSDT_funding_8h.csv", "fear_greed_daily.csv")
_ref = json.loads(FIXTURE_PATH.read_text())
_CACHE_SKIP = cache_skip_reason(PROJECT_ROOT / "local_data", _NEEDED_CACHES, _ref["start_date"], _ref["end_date"])
pytestmark = [
    pytest.mark.slow,
    pytest.mark.skipif(_CACHE_SKIP is not None, reason=_CACHE_SKIP or "local_data caches usable"),
]


@pytest.fixture(scope="module")
def reference():
    with open(FIXTURE_PATH) as f:
        return json.load(f)


def _run_metrics_path(reference, tmp_path, **kwargs) -> Path:
    from core.launcher import run_backtest

    run_dir = run_backtest(
        config_path=str(PROJECT_ROOT / reference["config"]),
        symbol=reference["symbol"],
        start=reference["start_date"],
        end=reference["end_date"],
        results_root=str(tmp_path),
        trades_log_file=str(tmp_path / "interim_trades.json"),
        **kwargs,
    )
    return Path(run_dir) / "metrics.json"


def _run(reference, tmp_path, **kwargs):
    with open(_run_metrics_path(reference, tmp_path, **kwargs)) as f:
        return json.load(f)


def test_default_omits_bar_equity_key(reference, tmp_path):
    """bar_equity omitted (defaults False) -- metrics.json must have NO
    "bar_equity" key at all, not an empty/null one."""
    metrics = _run(reference, tmp_path)
    assert "bar_equity" not in metrics


def test_explicit_false_matches_omitted_default(reference, tmp_path):
    """bar_equity=False explicitly must produce a BYTE-IDENTICAL metrics.json
    FILE to omitting it -- compares raw file text (read_text()), not parsed-
    dict equality. Dict equality can't see key order, whitespace, or float
    repr differences; this test's own docstring claims byte-identity, so it
    must check bytes."""
    default_path = _run_metrics_path(reference, tmp_path / "default")
    explicit_path = _run_metrics_path(reference, tmp_path / "explicit", bar_equity=False)
    assert default_path.read_text() == explicit_path.read_text()


def test_bar_equity_flag_does_not_change_core_or_other_sections(reference, tmp_path):
    """Sanity check that enabling the flag is purely additive: every
    pre-existing metrics.json section is untouched when bar_equity=True."""
    off_metrics = _run(reference, tmp_path / "off")
    on_metrics = _run(reference, tmp_path / "on", bar_equity=True)
    for key in ("core", "per_regime", "forecast_bins", "dynamic", "regime_validity"):
        assert on_metrics[key] == off_metrics[key], f"bar_equity=True changed metrics.json[{key!r}]"
    assert "bar_equity" not in off_metrics
    assert "bar_equity" in on_metrics


def test_bar_equity_matches_reference(reference, tmp_path):
    """bar_equity=True must reproduce the pre-registered, independently
    cross-checked numbers in tests/fixtures/bar_equity_reference.json."""
    metrics = _run(reference, tmp_path, bar_equity=True)
    block = metrics["bar_equity"]
    expected = reference["expected_bar_equity"]
    tolerance = expected["tolerance"]

    for key in ("max_drawdown_pct", "sharpe", "sortino", "exposure_pct", "turnover"):
        assert abs(block[key] - expected[key]) <= tolerance, (
            f"bar_equity[{key!r}] regression: expected {expected[key]} ± {tolerance}, got {block[key]}."
        )
    assert block["n_bars_total"] == expected["n_bars_total"]
    assert block["n_bars_warmup_excluded"] == expected["n_bars_warmup_excluded"]
    assert block["n_daily_returns"] == expected["n_daily_returns"]
    assert block["n_downside_days"] == expected["n_downside_days"]
