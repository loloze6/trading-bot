"""
Tests for tools/whale_footprint_evaluation.py (dispatch W8 step 6).

Every case here is a SYNTHETIC, planted-answer fixture. Nothing in this file
reads trading-bot/local_data/recorded_reserved/ — the harness is built and
tested here but deliberately never run against the real capture.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_PATH))

from whale_footprint_evaluation import evaluate, load_prereg  # noqa: E402

FEATURES = ["f_signal", "f_noise_a", "f_noise_b"]


def _prereg(required_n=50, coverage_floor=0.05, alpha_corrected=0.0125, fires_once=True):
    return {
        "features": {"names": list(FEATURES)},
        "test_statistic": {"multiple_comparison_correction": {"alpha_corrected": alpha_corrected}},
        "minimum_n_gate": {"required_attested_bars_per_pair": required_n},
        "required_coverage_floor": {"floor": coverage_floor},
        "single_use": {"fires_exactly_once": fires_once},
    }


def _panel(n_pairs, n_bars, *, attested_fraction=1.0, seed=0,
           signal_strength=0.9, flip_pairs=0):
    """
    Builds `n_pairs` synthetic panels of `n_bars` rows each.

    f_signal correlates with target at `signal_strength` (Spearman, roughly)
    for every pair EXCEPT the first `flip_pairs` pairs, whose f_signal is
    NEGATIVELY correlated with target instead — used to plant an UNSTABLE
    (sign-inconsistent) result while keeping the pooled correlation
    significant. f_noise_a / f_noise_b are independent of target everywhere
    (NULL features in every fixture that doesn't override them).
    """
    rng = np.random.RandomState(seed)
    panels = {}
    for i in range(n_pairs):
        target = rng.normal(size=n_bars)
        sign = -1.0 if i < flip_pairs else 1.0
        f_signal = sign * signal_strength * target + rng.normal(scale=0.4, size=n_bars)
        f_noise_a = rng.normal(size=n_bars)
        f_noise_b = rng.normal(size=n_bars)
        attested = rng.uniform(size=n_bars) < attested_fraction
        panels[f"PAIR{i}"] = pd.DataFrame({
            "f_signal": f_signal, "f_noise_a": f_noise_a, "f_noise_b": f_noise_b,
            "target": target, "attested": attested,
        })
    return panels


# ---------------------------------------------------------------------------


def test_pass_when_a_feature_clears_significance_with_consistent_sign():
    prereg = _prereg(required_n=50, coverage_floor=0.05)
    panels = _panel(n_pairs=10, n_bars=200, attested_fraction=1.0, flip_pairs=0, seed=1)
    result = evaluate(prereg, panels)
    assert result.status == "VERDICT"
    assert result.verdict == "PASS"
    f_signal = next(f for f in result.detail["per_feature"] if f["feature"] == "f_signal")
    assert f_signal["verdict"] == "PASS"
    assert f_signal["sign_consistency"]["holds"] is True


def test_null_when_no_feature_clears_significance():
    prereg = _prereg(required_n=50, coverage_floor=0.05)
    # signal_strength=0 -> f_signal degenerates to noise too
    panels = _panel(n_pairs=10, n_bars=200, attested_fraction=1.0,
                     signal_strength=0.0, seed=2)
    result = evaluate(prereg, panels)
    assert result.status == "VERDICT"
    assert result.verdict == "NULL"
    assert all(f["verdict"] == "NULL" for f in result.detail["per_feature"])


def test_unstable_when_a_feature_clears_but_sign_flips_across_pairs():
    prereg = _prereg(required_n=50, coverage_floor=0.05)
    # 10 pairs, 3 flipped (30% disagreement) -> pooled correlation stays
    # significant (majority direction, large N) but per-pair agreement (70%)
    # falls below the 80% sign_consistency floor.
    panels = _panel(n_pairs=10, n_bars=300, attested_fraction=1.0,
                     flip_pairs=3, signal_strength=0.9, seed=3)
    result = evaluate(prereg, panels)
    assert result.status == "VERDICT"
    f_signal = next(f for f in result.detail["per_feature"] if f["feature"] == "f_signal")
    assert f_signal["verdict"] == "UNSTABLE", (
        f"expected f_signal UNSTABLE (sign flips on 3/10 pairs), got {f_signal!r}"
    )
    assert f_signal["sign_consistency"]["agree_fraction"] == pytest.approx(0.7)
    assert result.verdict == "UNSTABLE"


def test_blocked_by_minimum_n_gate():
    prereg = _prereg(required_n=10_000, coverage_floor=0.05)  # unreachable on purpose
    panels = _panel(n_pairs=5, n_bars=50, attested_fraction=1.0, seed=4)
    result = evaluate(prereg, panels)
    assert result.status == "BLOCKED_MIN_N"
    assert result.verdict is None
    assert result.detail["attested_bars_per_pair_avg"] < result.detail["required"]


def test_blocked_by_coverage_floor():
    prereg = _prereg(required_n=10, coverage_floor=0.50)
    panels = _panel(n_pairs=5, n_bars=200, attested_fraction=0.05, seed=5)
    result = evaluate(prereg, panels)
    assert result.status == "BLOCKED_COVERAGE_FLOOR"
    assert result.detail["attested_fraction"] < result.detail["floor"]


def test_blocked_by_single_use_after_first_execution(tmp_path):
    prereg_path = tmp_path / "prereg.yaml"
    prereg = _prereg(required_n=50, coverage_floor=0.05)
    import yaml
    prereg_path.write_text(yaml.safe_dump(prereg), encoding="utf-8")

    panels = _panel(n_pairs=10, n_bars=200, attested_fraction=1.0, seed=6)
    loaded = load_prereg(prereg_path)

    first = evaluate(loaded, panels, prereg_path=prereg_path, run_id="run_a")
    assert first.status == "VERDICT"

    second = evaluate(loaded, panels, prereg_path=prereg_path, run_id="run_b")
    assert second.status == "BLOCKED_SINGLE_USE"
    assert second.detail["consumed_by"]["run_id"] == "run_a"


def test_blocked_run_does_not_consume_single_use(tmp_path):
    """A gate BLOCK (min-N here) must not stamp consumption -- only a run that
    reaches an actual verdict spends the single use."""
    prereg_path = tmp_path / "prereg.yaml"
    prereg = _prereg(required_n=10_000, coverage_floor=0.05)  # forces BLOCKED_MIN_N
    import yaml
    prereg_path.write_text(yaml.safe_dump(prereg), encoding="utf-8")
    loaded = load_prereg(prereg_path)

    panels = _panel(n_pairs=5, n_bars=50, attested_fraction=1.0, seed=7)
    blocked = evaluate(loaded, panels, prereg_path=prereg_path, run_id="run_a")
    assert blocked.status == "BLOCKED_MIN_N"

    # Now satisfy the gate and confirm the single use is STILL available.
    loaded["minimum_n_gate"]["required_attested_bars_per_pair"] = 10
    ok = evaluate(loaded, panels, prereg_path=prereg_path, run_id="run_b")
    assert ok.status == "VERDICT"


def test_the_real_pre_registration_loads_and_wires_into_the_harness():
    """Schema smoke test against the actual committed file -- not a real
    evaluation (the synthetic panel below is far too small to clear its
    minimum_n_gate, which is the point: it proves the wiring without ever
    approaching real capture data)."""
    real_path = (Path(__file__).parent.parent / "protocols" /
                 "prereg_whale_footprint_v1.yaml")
    prereg = load_prereg(real_path)
    assert prereg["features"]["names"] == [
        "whale_lt_imbalance", "whale_cvd_delta", "whale_size_shift",
    ]
    tiny_panels = {
        f"PAIR{i}": pd.DataFrame({
            "whale_lt_imbalance": np.zeros(5), "whale_cvd_delta": np.zeros(5),
            "whale_size_shift": np.zeros(5), "target": np.zeros(5),
            "attested": [True] * 5,
        })
        for i in range(3)
    }
    result = evaluate(prereg, tiny_panels)
    assert result.status == "BLOCKED_MIN_N", (
        "sanity check: a 5-bar synthetic panel must never clear the real "
        "pre-registration's minimum-N gate"
    )
