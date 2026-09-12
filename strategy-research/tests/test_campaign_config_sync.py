"""
Fix 3: Config drift guard.

Asserts every value in campaign_config.yaml matches its named code constant.
Divergence = hard failure. Run with the regression suite.

NOTE: This test enforces *declared parity* between config and code.
The runtime-loading refactor (code reads from config at startup) is deferred.
Until that lands, this test is the only enforcement mechanism — if it diverges,
the canonical value is the config file; update the code constant to match.
"""

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
CONFIG_PATH = ROOT / "config" / "campaign_config.yaml"
TOOLS_PATH = ROOT / "tools"
WORKFLOW_PATH = ROOT / "workflow"
TRADING_BOT_ROOT = ROOT.parent / "trading-bot"

sys.path.insert(0, str(TOOLS_PATH))
sys.path.insert(0, str(WORKFLOW_PATH))
sys.path.insert(0, str(TRADING_BOT_ROOT))


@pytest.fixture(scope="module")
def campaign_config():
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# performance.signal_statistics constants (E-039 step 5, 2026-09-12: relocated
# here from prescreen_signal.py, which is deleted; the values are unchanged --
# verbatim ports, per CUL-264/265 -- so campaign_config.yaml's `prescreen.*`
# keys still name the right constants, just at their new home).
# ---------------------------------------------------------------------------

def test_block_size_1h(campaign_config):
    expected = campaign_config["prescreen"]["block_size_1h"]
    from timeframe import bars_per_day
    assert bars_per_day("1h") == expected, (
        f"derived bars_per_day('1h')={bars_per_day('1h')} "
        f"!= config prescreen.block_size_1h={expected}"
    )


def test_block_size_1d(campaign_config):
    """2026-07-07: daily-bar engine support (P4_ts_trend/SMA(100)-daily)."""
    expected = campaign_config["prescreen"]["block_size_1d"]
    from timeframe import bars_per_day
    assert bars_per_day("1d") == expected, (
        f"derived bars_per_day('1d')={bars_per_day('1d')} "
        f"!= config prescreen.block_size_1d={expected}"
    )


def test_significance_threshold(campaign_config):
    from performance import signal_statistics
    expected = campaign_config["prescreen"]["significance_threshold"]
    assert signal_statistics._SIG_THRESHOLD == expected, (
        f"signal_statistics._SIG_THRESHOLD={signal_statistics._SIG_THRESHOLD} "
        f"!= config prescreen.significance_threshold={expected}"
    )


def test_sigma_bar_bps_degenerate_fallback(campaign_config):
    """
    This constant is a degenerate placeholder (fires only when < 5 return
    observations are available in sigma_bar_bps_from_returns()) -- never a
    volatility estimate. See campaign_config.yaml's comment and
    engineering/improvements/done/design_and_docs/11_viable_space_map.md Part 1 for the misreading this caused.
    """
    from performance import signal_statistics
    expected = campaign_config["prescreen"]["sigma_bar_bps_degenerate_fallback"]
    assert signal_statistics._DEFAULT_SIGMA_BAR_BPS == expected, (
        f"signal_statistics._DEFAULT_SIGMA_BAR_BPS={signal_statistics._DEFAULT_SIGMA_BAR_BPS} "
        f"!= config prescreen.sigma_bar_bps_degenerate_fallback={expected}"
    )


# ---------------------------------------------------------------------------
# validate_regime_detector.py constants
# ---------------------------------------------------------------------------

def test_activation_band_min(campaign_config):
    import validate_regime_detector
    expected = campaign_config["regime_detector"]["activation_band_min"]
    assert validate_regime_detector.ACTIVATION_BAND_MIN == expected, (
        f"validate_regime_detector.ACTIVATION_BAND_MIN={validate_regime_detector.ACTIVATION_BAND_MIN} "
        f"!= config regime_detector.activation_band_min={expected}"
    )


def test_activation_band_max(campaign_config):
    import validate_regime_detector
    expected = campaign_config["regime_detector"]["activation_band_max"]
    assert validate_regime_detector.ACTIVATION_BAND_MAX == expected, (
        f"validate_regime_detector.ACTIVATION_BAND_MAX={validate_regime_detector.ACTIVATION_BAND_MAX} "
        f"!= config regime_detector.activation_band_max={expected}"
    )


def test_default_date_range(campaign_config):
    import validate_regime_detector
    cfg = campaign_config["regime_detector"]
    assert validate_regime_detector._DEFAULT_START == cfg["default_start"], (
        f"validate_regime_detector._DEFAULT_START={validate_regime_detector._DEFAULT_START!r} "
        f"!= config regime_detector.default_start={cfg['default_start']!r}"
    )
    assert validate_regime_detector._DEFAULT_END == cfg["default_end"], (
        f"validate_regime_detector._DEFAULT_END={validate_regime_detector._DEFAULT_END!r} "
        f"!= config regime_detector.default_end={cfg['default_end']!r}"
    )


# ---------------------------------------------------------------------------
# run_phase1_research.py constants (below_floor_pct threshold)
# ---------------------------------------------------------------------------

def test_below_floor_pct_matches_config(campaign_config):
    """
    run_phase1_research.py uses 50.0 as below_floor_pct threshold.
    campaign_config.orchestrator.below_floor_pct_threshold must match.
    """
    expected = campaign_config["orchestrator"]["below_floor_pct_threshold"]
    # This constant is hardcoded in _record_backtest_trial() — we verify via source inspection.
    src = (WORKFLOW_PATH / "run_phase1_research.py").read_text(encoding="utf-8")
    assert f"below_floor > {expected}" in src, (
        f"run_phase1_research.py does not contain 'below_floor > {expected}' — "
        f"config orchestrator.below_floor_pct_threshold={expected} may be out of sync"
    )


# ---------------------------------------------------------------------------
# power_check.py / A8.6 formula self-check -- REMOVED 2026-09-11 (E-039: A8.6
# dropped entirely, "always backtest"). power_check.py and run_phase1_research
# .py's A8.6 mirror are both deleted; the two tests that lived here
# (BLOCK_SIZE-matches-prescreen parity, H-041-C n_eff=13 reproduction) tested
# functions that no longer exist. prescreen_signal.py's own block-size
# derivation (unrelated to A8.6) is still guarded in test_timeframe_block_size.py.
# ---------------------------------------------------------------------------

def test_episode_significance_constants(campaign_config):
    import episode_significance
    cfg = campaign_config["episode_significance"]
    assert episode_significance._DEFAULT_GAP_BARS == cfg["gap_bars"]
    assert episode_significance._DEFAULT_DENSITY_FALLBACK_PCT == cfg["density_fallback_pct"]
    assert episode_significance._MIN_N_EPISODES == cfg["min_n_episodes"]
    assert episode_significance._DEFAULT_N_RESAMPLES == cfg["n_resamples"]


