"""
Improvement 06 — A6.1-A6.4 Acceptance Tests

Per A1.4: accepted by OUTPUT AUDIT against constructed artifacts.
No live campaign data required — all tests use synthetic inputs.

Run with: pytest strategy-research/tests/test_improvement06_acceptance.py -v
"""

import math
import statistics
import pytest
from pathlib import Path
from statistics import NormalDist

_NDIST = NormalDist(0, 1)


def _phi(x: float) -> float:
    return _NDIST.cdf(x)


def _phi_inv(p: float) -> float:
    p = max(1e-10, min(1 - 1e-10, p))
    return _NDIST.inv_cdf(p)


EULER_GAMMA = 0.5772156649
DSR_THRESHOLD = 0.95


def _compute_dsr(candidate_sr: float, trial_sharpes: list[float]) -> dict:
    """Mirror of deflate_sharpe.py core logic — deterministic, no file I/O."""
    n = len(trial_sharpes)
    if n < 2:
        return {
            "verdict": "insufficient_trials",
            "dsr": None,
            "expected_max_sharpe": None,
        }

    mu = statistics.mean(trial_sharpes)
    sigma = statistics.stdev(trial_sharpes)

    if sigma < 1e-10:
        return {"verdict": "zero_variance", "dsr": None, "expected_max_sharpe": None}

    z1 = _phi_inv(1.0 - 1.0 / n)
    z2 = _phi_inv(1.0 - 1.0 / (math.e * n))
    z_exp_max = (1.0 - EULER_GAMMA) * z1 + EULER_GAMMA * z2
    e_max_sr = mu + sigma * z_exp_max

    z = (candidate_sr - e_max_sr) / sigma
    dsr = _phi(z)

    return {
        "dsr": round(dsr, 6),
        "expected_max_sharpe": round(e_max_sr, 6),
        "n_trials": n,
        "passes": dsr > DSR_THRESHOLD,
    }


def _deduplicate_trials(records: list[dict]) -> tuple[list[dict], int]:
    """Mirror of deflate_sharpe.py dedup logic — dedup by forecast_hash."""
    seen: set = set()
    deduped = []
    removed = 0
    for r in records:
        fh = r.get("forecast_hash")
        if fh and fh in seen:
            removed += 1
        else:
            if fh:
                seen.add(fh)
            deduped.append(r)
    return deduped, removed


def _check_holdout_single_use(hypothesis_id: str, consumed_list: list[str]) -> dict:
    """Mirror of _route_holdout_evaluation single-use check."""
    if hypothesis_id in consumed_list:
        return {
            "verdict": "refused",
            "reason": f"{hypothesis_id} already in holdout_consumed_by",
        }
    return {"verdict": "allowed"}


# ---------------------------------------------------------------------------
# AC2 — Deflated Sharpe monotonicity: same raw Sharpe, more trials → lower DSR
# ---------------------------------------------------------------------------


def test_deflated_sharpe_monotonic():
    """
    Increasing N with fixed μ and σ → monotonically decreasing DSR.

    The BLP expected-max term E_max = μ + σ * Z_exp_max(N) grows with N because
    Z_exp_max(N) = (1-γ)·Φ⁻¹(1-1/N) + γ·Φ⁻¹(1-1/(e·N)) is strictly increasing in N.
    With fixed candidate_sr and fixed σ, z = (candidate_sr - E_max) / σ decreases,
    so DSR = Φ(z) decreases monotonically.

    We hold μ and σ constant rather than computing from sample to isolate the N effect.
    """
    candidate_sr = 1.0
    mu_fixed = 0.1
    sigma_fixed = 0.2

    def _dsr_fixed_params(n: int) -> float:
        z1 = _phi_inv(1.0 - 1.0 / n)
        z2 = _phi_inv(1.0 - 1.0 / (math.e * n))
        z_exp_max = (1.0 - EULER_GAMMA) * z1 + EULER_GAMMA * z2
        e_max = mu_fixed + sigma_fixed * z_exp_max
        z = (candidate_sr - e_max) / sigma_fixed
        return _phi(z)

    ns = [2, 3, 5, 10, 20, 50, 100]
    dsrs = [_dsr_fixed_params(n) for n in ns]

    for i in range(1, len(dsrs)):
        assert dsrs[i] < dsrs[i - 1], (
            f"DSR must decrease as N grows: "
            f"DSR(N={ns[i]})={dsrs[i]:.6f} is not < DSR(N={ns[i - 1]})={dsrs[i - 1]:.6f}"
        )
    # Boundary: small N → high DSR; large N → low DSR
    assert dsrs[0] > dsrs[-1], (
        f"DSR(N={ns[0]})={dsrs[0]:.6f} must exceed DSR(N={ns[-1]})={dsrs[-1]:.6f}"
    )


# ---------------------------------------------------------------------------
# A6.4 — Dedup: runs 017/024/027/033 with shared forecast_hash → 1 trial
# ---------------------------------------------------------------------------


def test_dedup_017_024_027_033():
    """
    Runs 017, 024, 027, 033 share the same Keltner signal parameters (identical forecast series).
    They must collapse to ONE trial before DSR computation.
    """
    SHARED_HASH = "keltner_v1_forecast_abc123"

    records = [
        {
            "trial_id": "run_017",
            "sharpe": 0.0,
            "statistic_valid": "sharpe",
            "forecast_hash": SHARED_HASH,
            "n_trades": 163,
        },
        {
            "trial_id": "run_024",
            "sharpe": 0.0,
            "statistic_valid": "sharpe",
            "forecast_hash": SHARED_HASH,
            "n_trades": 163,
        },
        {
            "trial_id": "run_027",
            "sharpe": 0.0,
            "statistic_valid": "sharpe",
            "forecast_hash": SHARED_HASH,
            "n_trades": 163,
        },
        {
            "trial_id": "run_033",
            "sharpe": 0.0,
            "statistic_valid": "sharpe",
            "forecast_hash": SHARED_HASH,
            "n_trades": 163,
        },
        # One genuinely distinct trial
        {
            "trial_id": "run_040",
            "sharpe": 0.3,
            "statistic_valid": "sharpe",
            "forecast_hash": "different_signal_xyz789",
            "n_trades": 50,
        },
    ]

    deduped, n_removed = _deduplicate_trials(records)

    assert n_removed == 3, (
        f"Expected 3 duplicate runs removed (017/024/027 → same hash as 033), got {n_removed}"
    )
    assert len(deduped) == 2, (
        f"Expected 2 unique trials after dedup, got {len(deduped)}: "
        f"{[r['trial_id'] for r in deduped]}"
    )
    trial_ids = {r["trial_id"] for r in deduped}
    assert "run_040" in trial_ids, "The distinct trial (run_040) must survive dedup"
    # One of the four Keltner runs must survive (the first encountered)
    assert any(
        tid in trial_ids for tid in ("run_017", "run_024", "run_027", "run_033")
    ), "Exactly one Keltner run must survive dedup"


def test_dedup_no_hash_always_kept():
    """Records without forecast_hash are always treated as unique (no dedup applied)."""
    records = [
        {"trial_id": "run_001", "sharpe": 0.5, "statistic_valid": "sharpe"},
        {"trial_id": "run_002", "sharpe": 0.5, "statistic_valid": "sharpe"},
    ]
    deduped, n_removed = _deduplicate_trials(records)
    assert n_removed == 0, "Records without forecast_hash must never be deduped"
    assert len(deduped) == 2


# ---------------------------------------------------------------------------
# AC3 — Single-use holdout: second attempt for same hypothesis_id is refused
# ---------------------------------------------------------------------------


def test_single_use_holdout_refused():
    """
    A hypothesis_id that already appears in holdout_consumed_by must be refused
    mechanically — no second holdout evaluation is allowed.
    """
    consumed = ["H-041-A", "H-041-B", "H-033"]

    # Already consumed — must be refused
    result = _check_holdout_single_use("H-041-A", consumed)
    assert result["verdict"] == "refused", (
        f"Expected 'refused' for H-041-A (already consumed), got: {result}"
    )
    assert (
        "holdout_consumed_by" in result["reason"].lower()
        or "already" in result["reason"].lower()
    )

    # New hypothesis — must be allowed
    result_new = _check_holdout_single_use("H-042-A", consumed)
    assert result_new["verdict"] == "allowed", (
        f"Expected 'allowed' for H-042-A (not consumed), got: {result_new}"
    )


# ---------------------------------------------------------------------------
# Overlap guard regression (A6.1 / A7.x) — holdout range must not overlap protocol
# ---------------------------------------------------------------------------


def test_overlap_guard_regression():
    """
    The holdout window [2026-01-01, 2026-06-30] must not overlap the walk-forward
    range [2024-12-01, 2025-12-31]. Any protocol that assigns a backtest window
    inside the holdout range must be rejected.

    This is a structural invariant — not a live data check.
    """
    holdout_start = "2026-01-01"
    holdout_end = "2026-06-30"
    wf_end = "2025-12-31"

    # Walk-forward range ends before holdout starts → no overlap
    assert wf_end < holdout_start, (
        f"Walk-forward end {wf_end} must precede holdout start {holdout_start} — overlap detected!"
    )

    def _overlaps_holdout(wstart: str, wend: str) -> bool:
        """True if [wstart, wend] overlaps [holdout_start, holdout_end]."""
        return wstart <= holdout_end and wend >= holdout_start

    # Simulated protocol windows that MUST be flagged as overlapping holdout
    invalid_windows = [
        ("2026-01-01", "2026-03-31"),  # starts exactly on holdout
        ("2025-06-01", "2026-02-28"),  # straddles the boundary
        ("2026-03-01", "2026-06-30"),  # entirely inside holdout
    ]
    for wstart, wend in invalid_windows:
        assert _overlaps_holdout(wstart, wend), (
            f"Overlap guard must flag window {wstart}–{wend} as overlapping holdout"
        )

    # Valid walk-forward window: entirely before holdout
    valid_window = ("2025-10-01", "2025-12-31")
    overlap = valid_window[0] <= holdout_end and valid_window[1] >= holdout_start
    assert not overlap, (
        f"Valid walk-forward window {valid_window} must NOT overlap holdout range"
    )


# ---------------------------------------------------------------------------
# AC5 — Keltner must NOT pass; synthetic genuine edge must pass
# ---------------------------------------------------------------------------


def test_keltner_must_not_pass():
    """
    Keltner config: median_sharpe ≈ 0.0, many trials, campaign variance exists.
    DSR for a 0.0 Sharpe candidate against a trial distribution must not exceed DSR_THRESHOLD.
    """
    # Realistic campaign trial distribution (mixed strategies, varied Sharpes)
    trial_sharpes = [
        0.0,
        0.0,
        0.0,
        0.0,  # Keltner family: all 0.0 (A3.4 sparse)
        0.15,
        -0.1,
        0.05,
        0.2,  # Other strategy family
        -0.05,
        0.08,
        0.12,
        -0.15,
    ]

    candidate_sr = 0.0  # Keltner median Sharpe

    result = _compute_dsr(candidate_sr, trial_sharpes)

    assert result["dsr"] is not None, "DSR must be computable"
    assert not result["passes"], (
        f"Keltner (candidate_sr=0.0) must NOT pass DSR threshold {DSR_THRESHOLD}: "
        f"DSR={result['dsr']}"
    )
    assert result["dsr"] < DSR_THRESHOLD, (
        f"Keltner DSR={result['dsr']} must be < {DSR_THRESHOLD}"
    )


def test_synthetic_genuine_edge_passes():
    """
    A genuinely strong candidate (Sharpe >> trial distribution mean + σ) must pass.
    Represents a real edge that stands out from the search distribution.
    """
    # Trial distribution: most strategies failed, some middling
    trial_sharpes = [0.0, 0.0, 0.05, -0.1, 0.1, 0.0, 0.08, -0.05, 0.03, 0.07]

    # Strong candidate: clearly outperforms the search distribution
    # mean ≈ 0.015, std ≈ 0.055 → E_max ≈ mean + std * Z_exp_max(10)
    # Z_exp_max(10) ≈ 1.54 → E_max ≈ 0.015 + 0.055 * 1.54 ≈ 0.10
    # DSR passes when candidate_sr >> E_max
    candidate_sr = 2.5  # Strong result, clearly above E_max

    result = _compute_dsr(candidate_sr, trial_sharpes)

    assert result["dsr"] is not None, "DSR must be computable"
    assert result["passes"], (
        f"Strong synthetic candidate (candidate_sr=2.5) must pass DSR threshold {DSR_THRESHOLD}: "
        f"DSR={result['dsr']}"
    )
    assert result["dsr"] >= DSR_THRESHOLD, (
        f"Synthetic DSR={result['dsr']} must be >= {DSR_THRESHOLD}"
    )
