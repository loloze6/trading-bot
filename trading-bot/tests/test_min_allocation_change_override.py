"""
E-055: strategies.min_allocation_change lets a strategy's own strategy_config.json
override RiskManager's min_allocation_change.threshold control (risk/risk_manager.py)
for that strategy's runs, instead of the one fixed 0.20 in config.json.

Fast unit tests -- no data fetch, no full backtest. See
test_min_allocation_change_override_bit_identical.py for the slow end-to-end
before/after reference-value proof.
"""
import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.launcher import Launcher
from strategies.main_strategy import AdvancedStrategy
from tools.validate_config import validate


def test_advanced_strategy_override_absent_by_default():
    strategy = AdvancedStrategy()  # committed strategy_config.json
    assert strategy.min_allocation_change_override is None


def test_advanced_strategy_reads_override(tmp_path):
    base = json.loads((PROJECT_ROOT / "strategy_config.json").read_text())
    base["strategies"]["min_allocation_change"] = 0.05
    planted = tmp_path / "strategy_config.json"
    planted.write_text(json.dumps(base))

    strategy = AdvancedStrategy(config_path=str(planted))
    assert strategy.min_allocation_change_override == 0.05


def test_build_risk_and_forecast_managers_unchanged_when_override_none():
    launcher = Launcher()
    default_controls = launcher.config.get('risk_management', 'controls', {})

    risk_manager, _, _ = launcher._build_risk_and_forecast_managers(
        min_allocation_change_override=None
    )
    assert risk_manager.controls == default_controls
    assert risk_manager.controls["min_allocation_change"]["threshold"] == 0.2


def test_build_risk_and_forecast_managers_overrides_threshold_only():
    launcher = Launcher()
    risk_manager, _, _ = launcher._build_risk_and_forecast_managers(
        min_allocation_change_override=0.05
    )
    assert risk_manager.controls["min_allocation_change"]["threshold"] == 0.05
    # max_allocation_change (and anything else configured) must pass through untouched.
    default_controls = launcher.config.get('risk_management', 'controls', {})
    assert risk_manager.controls["max_allocation_change"] == default_controls["max_allocation_change"]


@pytest.mark.parametrize("bad_value", [-0.1, "0.2", True, None])
def test_validate_config_rejects_bad_min_allocation_change(bad_value):
    base = json.loads((PROJECT_ROOT / "strategy_config.json").read_text())
    base["strategies"]["min_allocation_change"] = bad_value
    errors = validate(base)
    assert any("V11" in e for e in errors), errors


def test_validate_config_accepts_good_min_allocation_change():
    base = json.loads((PROJECT_ROOT / "strategy_config.json").read_text())
    base["strategies"]["min_allocation_change"] = 0.35
    errors = validate(base)
    assert not any("V11" in e for e in errors), errors


def test_validate_config_accepts_absent_min_allocation_change():
    base = json.loads((PROJECT_ROOT / "strategy_config.json").read_text())
    assert "min_allocation_change" not in base["strategies"]
    errors = validate(base)
    assert not any("V11" in e for e in errors), errors
