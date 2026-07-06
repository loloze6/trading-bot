"""
F5c (P1a shakedown, 2026-07-04) regression test.

active_n_bars==0 (or a pervasive component-error rate) must route to a new
no_signal_artifact outcome, taking priority over every other route — NEVER
kill_no_ic. Fixture: a deliberately-broken component reproduces the "component
errors on every bar" case (F5a's actual ZeroDivisionError is now fixed and can't be
used to trigger this directly anymore); a real, healthy but never-firing config
covers the "zero activation, no errors" case.
"""
import json
import sys
import tempfile
from pathlib import Path

import pytest

TOOLS_PATH = Path(__file__).parent.parent / "tools"
TBOT_PATH = Path(__file__).parent.parent.parent / "trading-bot"
sys.path.insert(0, str(TOOLS_PATH))
sys.path.insert(0, str(TBOT_PATH))

import prescreen_signal as ps

_OHLCV = TBOT_PATH / "local_data" / "BTCUSDT_1h.csv"
_FUNDING = TBOT_PATH / "local_data" / "BTCUSDT_funding_8h.csv"
_PROTOCOL = {
    "symbols": ["BTCUSDT"],
    "timeframe": "1h",
    "windows": [{"label": "test", "test": {"start": "2024-01-01", "end": "2024-01-08"}}],
}


def _write(obj, path):
    path.write_text(json.dumps(obj), encoding="utf-8")
    return path


@pytest.mark.skipif(not _OHLCV.exists(), reason="local_data fixture not present")
def test_component_errors_route_to_no_signal_artifact(tmp_path):
    config = {
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
        "strategies": {"warmup": 3, "regimes": {
            "unknown": {"components": [{
                "id": "broken",
                "class": "tests.test_main_strategy_error_surfacing._AlwaysThrowsComponent",
                "weight": 1.0, "transforms": [{"op": "identity"}], "params": {},
            }]},
            "trending": None, "mean_reversion": None, "chop": None,
        }},
    }
    config_path = _write(config, tmp_path / "config.json")
    protocol_path = _write(_PROTOCOL, tmp_path / "protocol.json")

    result = ps.run_prescreen(str(config_path), str(protocol_path), run_id="test_f5c_errors", out_dir=tmp_path)

    assert result["route"] == "no_signal_artifact"
    assert result["prescreen_kill_reason"] == "component_error"
    assert result["active_n_bars"] == 0
    assert result["component_error_count"] > 0
    assert len(result["component_error_sample"]) > 0
    assert result["component_error_sample"][0]["error_type"] == "ZeroDivisionError"
    assert "engineering" in result["route_rationale"].lower() or "bug" in result["route_rationale"].lower()


@pytest.mark.skipif(not _OHLCV.exists() or not _FUNDING.exists(), reason="local_data fixtures not present")
def test_zero_activation_no_errors_still_routes_to_no_signal_artifact(tmp_path):
    """A healthy component that simply never fires (threshold set impossibly high)
    must ALSO route to no_signal_artifact, not kill_no_ic — it has been tested for
    activation, not for directional content."""
    config = {
        "aux_feeds": ["funding_rate"],
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
        "strategies": {"warmup": 3, "regimes": {
            "unknown": {"components": [{
                "id": "funding_rate_mean_reversion",
                "class": "strategies.strategy_components.FundingRateMeanReversionComponent",
                "weight": 1.0, "transforms": [{"op": "identity"}],
                "params": {"threshold": 999.0, "scaling_factor": 10.0},  # never exceeded
            }]},
            "trending": None, "mean_reversion": None, "chop": None,
        }},
    }
    config_path = _write(config, tmp_path / "config2.json")
    protocol_path = _write(_PROTOCOL, tmp_path / "protocol2.json")

    result = ps.run_prescreen(str(config_path), str(protocol_path), run_id="test_f5c_zero_activation", out_dir=tmp_path)

    assert result["route"] == "no_signal_artifact"
    assert result["prescreen_kill_reason"] == "zero_activation"
    assert result["active_n_bars"] == 0
    assert result["component_error_count"] == 0
    assert "never activated" in result["route_rationale"]


@pytest.mark.skipif(not _OHLCV.exists(), reason="local_data fixture not present")
def test_healthy_active_signal_does_not_get_flagged_as_no_signal_artifact(tmp_path):
    """Sanity/non-regression: a genuinely active, error-free signal must still reach
    a normal route (kill_no_ic/proceed_to_backtest/etc.), not be swept into
    no_signal_artifact by an overly broad condition."""
    config = {
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
        "strategies": {"warmup": 25, "regimes": {
            "unknown": {"components": [{
                "id": "ema_spread", "class": "strategies.strategy_components.EMASpreadComponent",
                "weight": 1.0, "transforms": [{"op": "identity"}],
                "params": {"fast_period": 9, "slow_period": 21, "scaling_factor": 5.0},
            }]},
            "trending": None, "mean_reversion": None, "chop": None,
        }},
    }
    config_path = _write(config, tmp_path / "config3.json")
    protocol_path = _write(_PROTOCOL, tmp_path / "protocol3.json")

    result = ps.run_prescreen(str(config_path), str(protocol_path), run_id="test_f5c_healthy", out_dir=tmp_path)

    assert result["route"] != "no_signal_artifact"
    assert result["component_error_count"] == 0
    assert result["active_n_bars"] > 0


@pytest.mark.skipif(not _OHLCV.exists() or not _FUNDING.exists(), reason="local_data fixtures not present")
def test_run_044_real_config_no_longer_produces_no_signal_artifact_after_f5a(tmp_path):
    """End-to-end confirmation that F5a's fix + F5c's routing together mean run_044's
    ACTUAL config (threshold=0.0) now produces a real IC result, not the previous
    active_n_bars=0 artifact."""
    run_044_config = (
        Path(__file__).parent.parent / "runs" / "run_044" / "artifacts" / "candidate_strategy_config.json"
    )
    if not run_044_config.exists():
        pytest.skip("run_044 config not present on disk")

    protocol_path = _write(_PROTOCOL, tmp_path / "protocol4.json")
    result = ps.run_prescreen(str(run_044_config), str(protocol_path), run_id="test_f5_e2e", out_dir=tmp_path)

    assert result["component_error_count"] == 0, "F5a should have eliminated the divide-by-zero entirely"
    assert result["active_n_bars"] > 0, "the continuous-mode signal should now genuinely fire"
    assert result["route"] != "no_signal_artifact"
