"""
E-055 end-to-end proof, same style/scenario as test_risk_layer_bit_identical.py.

OFF (strategy_config.json omits strategies.min_allocation_change): byte-identical
to today's behaviour -- the committed baseline dir hash 5ccbec42 reproduces exactly,
because omitting the key means Launcher._build_risk_and_forecast_managers never
touches the controls_cfg dict it reads from config.json.

ON (strategy_config.json sets strategies.min_allocation_change): distinguishable and
bites in the expected direction -- a LOWER threshold than config.json's 0.2 default
must not decrease trade count (a smaller floor can only let MORE rebalances through),
and a HIGHER threshold must not increase it.

SLOW INTEGRATION TEST. Run explicitly:
  pytest tests/test_min_allocation_change_override_bit_identical.py -v -m slow --timeout=0
"""

import json
import sys
from pathlib import Path

import pandas as pd
import pytest
from _cache_guard import cache_skip_reason

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

START, END, SYMBOL = "2024-04-01", "2024-05-30", "BTCUSDT"
BASELINE_CONFIG_SHA8 = "5ccbec42"  # committed strategy_config.json canonical hash

_NEEDED_CACHES = ("BTCUSDT_1h.csv", "BTCUSDT_funding_8h.csv", "fear_greed_daily.csv")
_CACHE_SKIP = cache_skip_reason(PROJECT_ROOT / "local_data", _NEEDED_CACHES, START, END)
pytestmark = [
    pytest.mark.slow,
    pytest.mark.skipif(_CACHE_SKIP is not None, reason=_CACHE_SKIP or "local_data caches usable"),
]


def _run(tmp_dir, config_path, **kwargs):
    from core.launcher import run_backtest

    run_dir = run_backtest(
        config_path=config_path,
        symbol=SYMBOL,
        start=START,
        end=END,
        results_root=str(tmp_dir),
        trades_log_file=str(Path(tmp_dir) / "interim_trades.json"),
        **kwargs,
    )
    return Path(run_dir)


def _planted_config(tmp_path, min_allocation_change=None):
    base = json.loads((PROJECT_ROOT / "strategy_config.json").read_text())
    if min_allocation_change is not None:
        base["strategies"]["min_allocation_change"] = min_allocation_change
    path = tmp_path / "strategy_config.json"
    path.write_text(json.dumps(base))
    return str(path)


def _trade_count(run_dir):
    """Count bars where a rebalance was actually APPROVED (bars.csv's
    `approved_rebalance` column) -- not just requested. `allocation_change != 0.0`
    is nonzero almost every bar regardless of the min_allocation_change threshold
    (it's the raw target-vs-actual delta before RiskManager ever sees it); the
    thing this override changes is whether RiskManager approves acting on it."""
    bars = pd.read_csv(run_dir / "bars.csv")
    return int(bars["approved_rebalance"].infer_objects(copy=False).fillna(False).astype(bool).sum())


# --- OFF: key absent is byte-identical to today ---


@pytest.fixture(scope="module")
def off_committed(tmp_path_factory):
    return _run(tmp_path_factory.mktemp("off_committed"), str(PROJECT_ROOT / "strategy_config.json"))


@pytest.fixture(scope="module")
def off_planted_absent(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("off_planted")
    return _run(tmp_dir, _planted_config(tmp_dir))


_IDENTITY_FILES = ("metrics.json", "portfolio_states.csv", "bars.csv", "trades.json")


@pytest.mark.parametrize("fname", _IDENTITY_FILES)
def test_absent_key_matches_committed_config(off_committed, off_planted_absent, fname):
    """A strategy_config.json that is byte-for-byte the committed one, just re-written
    through json.dumps (no min_allocation_change key added), must still reproduce the
    exact same run -- confirms the planting mechanism itself introduces no drift before
    testing the real variable."""
    assert (off_committed / fname).read_text() == (off_planted_absent / fname).read_text()


def test_off_reproduces_committed_baseline_hash(off_committed):
    assert off_committed.name.split("_")[-1] == BASELINE_CONFIG_SHA8
    manifest = json.loads((off_committed / "manifest.json").read_text())
    assert manifest["config_sha256"].startswith(BASELINE_CONFIG_SHA8)


# --- ON: threshold override is distinguishable and bites in the right direction ---


@pytest.fixture(scope="module")
def on_lower(tmp_path_factory):
    """Threshold well below config.json's 0.2 default -- must not REDUCE trade count."""
    tmp_dir = tmp_path_factory.mktemp("on_lower")
    return _run(tmp_dir, _planted_config(tmp_dir, min_allocation_change=0.02))


@pytest.fixture(scope="module")
def on_higher(tmp_path_factory):
    """Threshold well above config.json's 0.2 default -- must not INCREASE trade count."""
    tmp_dir = tmp_path_factory.mktemp("on_higher")
    return _run(tmp_dir, _planted_config(tmp_dir, min_allocation_change=1.5))


def test_lower_threshold_does_not_decrease_trade_count(off_committed, on_lower):
    baseline_trades = _trade_count(off_committed)
    lower_trades = _trade_count(on_lower)
    assert lower_trades >= baseline_trades, (baseline_trades, lower_trades)


def test_higher_threshold_does_not_increase_trade_count(off_committed, on_higher):
    baseline_trades = _trade_count(off_committed)
    higher_trades = _trade_count(on_higher)
    assert higher_trades <= baseline_trades, (baseline_trades, higher_trades)


def test_on_runs_have_different_provenance_from_off(off_committed, on_lower, on_higher):
    off_hash = off_committed.name.split("_")[-1]
    assert on_lower.name.split("_")[-1] != off_hash
    assert on_higher.name.split("_")[-1] != off_hash
    assert on_lower.name.split("_")[-1] != on_higher.name.split("_")[-1]
