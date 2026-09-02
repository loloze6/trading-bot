"""
P1b wiring test: candidate_strategy_config.json's "significance_methodology":
"episode_blocked_a851a" flag must switch run_prescreen()'s routing significance
from the default block_24_fisher_z method to the new A8.5.1a episode bootstrap —
and, critically, the DEFAULT (flag absent) behavior must be byte-for-byte
unchanged, so every prior recorded prescreen result stays reproducible.
"""
import json
import sys
from pathlib import Path

from _cache_guard import requires_cache

TOOLS_PATH = Path(__file__).parent.parent / "tools"
TBOT_PATH = Path(__file__).parent.parent.parent / "trading-bot"
sys.path.insert(0, str(TOOLS_PATH))
sys.path.insert(0, str(TBOT_PATH))

import prescreen_signal as ps

_OHLCV = TBOT_PATH / "local_data" / "BTCUSDT_1h.csv"
_FUNDING = TBOT_PATH / "local_data" / "BTCUSDT_funding_8h.csv"

# Real backfilled funding data, single era (era_2019_2023_full_feed) — small window
# just to exercise the wiring quickly, not to reproduce the full P1b statistics
# (those are covered by test_a851a_episode_bootstrap.py's dedicated fixtures).
_PROTOCOL = {
    "symbols": ["BTCUSDT"],
    "timeframe": "1h",
    "windows": [{"label": "test", "test": {"start": "2019-09-10", "end": "2020-01-01"}}],
}

_BASE_CONFIG = {
    "aux_feeds": ["funding_rate"],
    "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
    "strategies": {"warmup": 3, "regimes": {
        "unknown": {"components": [{
            "id": "funding_mr",
            "class": "strategies.strategy_components.FundingRateMeanReversionComponent",
            "weight": 1.0, "transforms": [], "params": {"threshold": 0.0002, "scaling_factor": 10.0},
        }]},
        "trending": None, "mean_reversion": None, "chop": None,
    }},
}


def _write(obj, path):
    path.write_text(json.dumps(obj), encoding="utf-8")
    return path


@requires_cache(_OHLCV, _FUNDING)
def test_default_behavior_unchanged_without_flag(tmp_path):
    config_path = _write(_BASE_CONFIG, tmp_path / "config.json")
    protocol_path = _write(_PROTOCOL, tmp_path / "protocol.json")

    result = ps.run_prescreen(str(config_path), str(protocol_path), run_id="test_default", out_dir=tmp_path)

    assert result["significance_methodology_used"] == "block_24_fisher_z"
    assert result["ic_by_era"] is None
    # ic_significance and ic_significance_block24 must be identical when the flag is absent
    assert result["ic_significance"] == result["ic_significance_block24"]


@requires_cache(_OHLCV, _FUNDING)
def test_a851a_flag_switches_methodology_and_reports_per_era(tmp_path):
    config = dict(_BASE_CONFIG)
    config["significance_methodology"] = "episode_blocked_a851a"
    config_path = _write(config, tmp_path / "config_a851a.json")
    protocol_path = _write(_PROTOCOL, tmp_path / "protocol_a851a.json")

    result = ps.run_prescreen(str(config_path), str(protocol_path), run_id="test_a851a", out_dir=tmp_path)

    assert result["significance_methodology_used"] in (
        "episode_block_bootstrap", "episode_bootstrap_insufficient_n", "block_24_dense_fallback",
    )
    # The old method must STILL be computed and reported for comparison, even
    # though it did not decide `route` this time.
    assert result["ic_significance_block24"] is not None
    assert result["ic_significance_block24"]["block_size"] == 24
    # Per-era breakdown must be populated whenever eras are configured (they are,
    # via campaign_data_policy.yaml).
    assert result["ic_by_era"] is not None
    assert isinstance(result["ic_by_era"], dict)
    assert len(result["ic_by_era"]) >= 1
    for era_stats in result["ic_by_era"].values():
        assert "active_n_bars" in era_stats
        assert "n_episodes" in era_stats


@requires_cache(_OHLCV, _FUNDING)
def test_insufficient_episodes_routes_kill_no_ic_with_a851a_kill_reason(tmp_path):
    """A tiny window with too few episodes must NOT silently claim significance —
    route stays kill_no_ic (existing enum, no new route added), but the kill_reason
    and rationale must clearly identify the A8.5.1a floor as the cause, distinct
    from a genuine no-informational-content result."""
    tiny_protocol = {
        "symbols": ["BTCUSDT"],
        "timeframe": "1h",
        # Verified via direct run: active_n_bars=8, n_episodes=1 (below the 8-episode
        # floor but active_n>0, so this must NOT hit the F5c zero-activation path).
        "windows": [{"label": "test", "test": {"start": "2019-09-10", "end": "2019-10-15"}}],
    }
    config = dict(_BASE_CONFIG)
    config["significance_methodology"] = "episode_blocked_a851a"
    config_path = _write(config, tmp_path / "config_tiny.json")
    protocol_path = _write(tiny_protocol, tmp_path / "protocol_tiny.json")

    result = ps.run_prescreen(str(config_path), str(protocol_path), run_id="test_a851a_tiny", out_dir=tmp_path)

    assert result["active_n_bars"] > 0, "must have real activation, not the F5c zero-activation case"
    assert result["significance_methodology_used"] == "episode_bootstrap_insufficient_n"
    assert result["ic_significance"]["n_episodes"] < 8
    assert result["route"] == "kill_no_ic"
    assert result["prescreen_kill_reason"] == "insufficient_episodes_a851a"
    assert "min_n_episodes floor" in result["route_rationale"]
