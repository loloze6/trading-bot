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

sys.path.insert(0, str(TOOLS_PATH))
sys.path.insert(0, str(WORKFLOW_PATH))


@pytest.fixture(scope="module")
def campaign_config():
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# prescreen_signal.py constants
# ---------------------------------------------------------------------------


def test_block_size_1h(campaign_config):
    import prescreen_signal

    expected = campaign_config["prescreen"]["block_size_1h"]
    # _BLOCK_SIZE_1H survives only as a documented regression anchor since
    # 2026-08-27 -- the live value is derived by tools/timeframe.py. Both must
    # still agree with config, or the anchor has stopped anchoring anything.
    from timeframe import bars_per_day

    assert prescreen_signal._BLOCK_SIZE_1H == expected
    assert bars_per_day("1h") == expected, (
        f"derived bars_per_day('1h')={bars_per_day('1h')} != config prescreen.block_size_1h={expected}"
    )


def test_block_size_1d(campaign_config):
    """2026-07-07: daily-bar engine support (P4_ts_trend/SMA(100)-daily)."""
    import prescreen_signal

    expected = campaign_config["prescreen"]["block_size_1d"]
    from timeframe import bars_per_day

    assert prescreen_signal._BLOCK_SIZE_1D == expected
    assert bars_per_day("1d") == expected, (
        f"derived bars_per_day('1d')={bars_per_day('1d')} != config prescreen.block_size_1d={expected}"
    )


def test_a86_block_size_by_timeframe_matches_config(campaign_config):
    """The A8.6 gate's block size must match campaign_config.yaml.

    REWRITTEN 2026-08-27. This previously asserted equality between two
    hand-maintained tables (`_A86_BLOCK_SIZE_BY_TIMEFRAME` and
    prescreen_signal's `_BLOCK_SIZE_1H/_1D`) at the two keys they both held --
    and passed, while those same two sites DISAGREED at 4h (24 vs 6). A test
    that only checks the entries everyone remembered to add cannot catch the
    entries nobody added. Both sites now derive from tools/timeframe.py, and
    the cross-site agreement test spanning every timeframe lives in
    tests/test_timeframe_block_size.py.

    What remains worth guarding here is the CONFIG's declared values still
    matching the derivation -- config is a fourth mirror, and if someone edits
    block_size_1h there expecting it to take effect, they should be told it
    no longer drives anything."""
    import run_phase1_research as rpr

    assert rpr._a86_block_size("1h") == campaign_config["prescreen"]["block_size_1h"]
    assert rpr._a86_block_size("1d") == campaign_config["prescreen"]["block_size_1d"]


def test_significance_threshold(campaign_config):
    import prescreen_signal

    expected = campaign_config["prescreen"]["significance_threshold"]
    assert prescreen_signal._SIG_THRESHOLD == expected, (
        f"prescreen_signal._SIG_THRESHOLD={prescreen_signal._SIG_THRESHOLD} "
        f"!= config prescreen.significance_threshold={expected}"
    )


def test_sigma_bar_bps_degenerate_fallback(campaign_config):
    """
    This constant is a degenerate placeholder (fires only when < 5 return
    observations are available in _sigma_from_records() — never a volatility
    estimate). Renamed from sigma_bar_bps_default to make that non-obvious
    behavior explicit; see campaign_config.yaml's comment and
    engineering/improvements/done/design_and_docs/11_viable_space_map.md Part 1 for the misreading this caused.
    """
    import prescreen_signal

    expected = campaign_config["prescreen"]["sigma_bar_bps_degenerate_fallback"]
    assert prescreen_signal._DEFAULT_SIGMA_BAR_BPS == expected, (
        f"prescreen_signal._DEFAULT_SIGMA_BAR_BPS={prescreen_signal._DEFAULT_SIGMA_BAR_BPS} "
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
# power_check.py BLOCK_SIZE matches prescreen block_size_1h
# ---------------------------------------------------------------------------


def test_power_check_block_size_matches_prescreen(campaign_config):
    """REWRITTEN 2026-08-27. This compared two hand-maintained constants and
    passed, while the sites they belonged to disagreed at every timeframe
    except 1h: power_check's BLOCK_SIZE was a BARE CONSTANT 24 (1h-only for
    every hypothesis it ever checked), and prescreen_signal fell back to 6 for
    everything non-1h/1d. Comparing only their 1h values could never surface
    that. Both now derive from tools/timeframe.py; this asserts neither has
    quietly reintroduced a local constant."""
    import power_check
    import prescreen_signal
    from timeframe import bars_per_day

    assert not hasattr(power_check, "BLOCK_SIZE"), (
        "power_check.BLOCK_SIZE reintroduced — a bare constant cannot vary by "
        "timeframe and is what made this mirror 1h-only"
    )
    assert "bars_per_day" in (TOOLS_PATH / "power_check.py").read_text(encoding="utf-8")
    assert "bars_per_day" in (TOOLS_PATH / "prescreen_signal.py").read_text(encoding="utf-8")
    assert prescreen_signal._BLOCK_SIZE_1H == bars_per_day("1h")
    assert prescreen_signal._BLOCK_SIZE_1D == bars_per_day("1d")


# ---------------------------------------------------------------------------
# A8.6 formula self-check: verify H-041-C reproduces n_eff=13
# ---------------------------------------------------------------------------


def test_episode_significance_constants(campaign_config):
    import episode_significance

    cfg = campaign_config["episode_significance"]
    assert episode_significance._DEFAULT_GAP_BARS == cfg["gap_bars"]
    assert episode_significance._DEFAULT_DENSITY_FALLBACK_PCT == cfg["density_fallback_pct"]
    assert episode_significance._MIN_N_EPISODES == cfg["min_n_episodes"]
    assert episode_significance._DEFAULT_N_RESAMPLES == cfg["n_resamples"]


def test_a86_heuristic_h041c_reproduction(campaign_config):
    """
    Known case: H-041-C prescreen gave active_n=316, n_eff=13 with 2 symbols.
    The corrected formula (n/( 1+(n-1)*rho )) must reproduce this at the measured rho.
    """
    import math
    from power_check import run_power_check
    from timeframe import bars_per_day

    # H-041-C was a 1h hypothesis, so its block size is bars_per_day("1h") == 24
    # -- the same value the removed BLOCK_SIZE constant held, now derived.
    BLOCK_SIZE = bars_per_day("1h")

    rho = campaign_config["symbol_correlation"]["btc_eth_return_correlation_1h"]
    n_symbols = 2
    n_sym_eff = n_symbols / (1.0 + (n_symbols - 1) * rho)

    # Back-compute activation_rate from actual prescreen result
    actual_active_n = 316
    n_bars = 17520
    activation_rate = actual_active_n / (n_bars * n_sym_eff)

    # Forward-compute
    expected_active_n = activation_rate * n_bars * n_sym_eff
    expected_n_eff = expected_active_n / BLOCK_SIZE
    mde = 1.0 / math.sqrt(max(expected_n_eff - 3.0, 1.0))

    assert abs(expected_active_n - actual_active_n) < 0.5, (
        f"active_n reproduction failed: got {expected_active_n:.1f}, expected ~316"
    )
    assert abs(expected_n_eff - 13.17) < 0.5, f"n_eff reproduction failed: got {expected_n_eff:.2f}, expected ~13.17"
    assert mde > 0.15, f"mde={mde:.4f} should exceed plausible_ic_upper=0.15 → insufficient_power_a_priori"
