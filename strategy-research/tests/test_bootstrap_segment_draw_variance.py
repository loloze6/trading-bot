"""
CUL-15 red-team regression: the gap-aware block bootstrap must actually
RESAMPLE across segments, not visit every segment deterministically.

The defect (found 2026-09-04 by the red-team audit of the merged #50 family):
`_stationary_block_bootstrap_ic_significance` looped over every contiguous
segment and drew `ceil(seg_len/block_size)` blocks from each. For a segment no
longer than the block length that yields `blk == seg_len`, i.e. a block that is
the whole segment merely ROTATED -- and Spearman rank correlation is
order-invariant, so the rotation is a no-op. Every such segment therefore
contributed an IDENTICAL value to every bootstrap replicate. With all segments
short, the entire bootstrap distribution collapsed to a single point mass, so
`frac_ge_0` (or `frac_le_0`) was 0.0 and the percentile p-value degenerated to
exactly 0.0 -- scoring PURE NOISE as significant, on every such dataset.

That is the precise direction the whole #50 family exists to prevent:
`_gap_aware_block_count`'s own docstring says a gap-blind count "errs toward
making junk look significant." The bootstrap's gap-aware path was doing the
same thing, harder.

Measured before the fix, on 30 gap-separated 6-bar segments of independent
gaussians: p_value=0.0, significant=True (the gap-blind None path on the same
data: p=0.168, not significant). False-positive rate on pure noise was 100%.
"""
import random
import sys
from pathlib import Path

import pandas as pd

TOOLS_PATH = Path(__file__).parent.parent / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import prescreen_signal as ps

_STEP = pd.Timedelta(1, unit="h")
_BASE = pd.Timestamp("2020-01-01 00:00:00")


def _noise_segments(seg_len, n_seg, seed=1):
    """Independent gaussian forecast/return pairs in `n_seg` contiguous runs of
    `seg_len` bars, each run separated from the next by a real 10h hole. There
    is no relationship between forecast and return by construction, so no
    honest significance test may flag this as significant more than
    occasionally."""
    rng = random.Random(seed)
    recs, h = [], 0
    for _s in range(n_seg):
        for _k in range(seg_len):
            h += 1
            recs.append({
                "timestamp": _BASE + pd.Timedelta(h, unit="h"),
                "forecast": rng.gauss(0, 1),
                "next_return_bps": rng.gauss(0, 1),
                "active": True,
            })
        h += 10
    return recs


def test_short_segments_do_not_collapse_the_bootstrap_distribution():
    """The core regression. Every segment is shorter than block_size, so the
    pre-fix code emitted one whole-segment (rotated) block per segment and every
    replicate was identical. p_value must not be the degenerate 0.0, and pure
    noise must not come back significant."""
    recs = _noise_segments(seg_len=6, n_seg=30)
    got = ps._stationary_block_bootstrap_ic_significance(
        {"X": recs}, expected_step_by_symbol={"X": _STEP}
    )
    assert got["p_value"] > 0.0, (
        "bootstrap p_value is exactly 0.0 on pure noise -- the resample "
        "distribution has collapsed to a point mass (every replicate identical), "
        "which is the whole-segment-rotation defect, not a real result"
    )
    assert not got["significant"], (
        f"pure noise flagged significant (p={got['p_value']}) -- the gap-aware "
        "bootstrap is making junk look significant, the exact failure #50 exists "
        "to prevent"
    )


def test_bootstrap_replicates_actually_vary_when_segments_are_short():
    """Directly pins the mechanism rather than only its p-value symptom: the
    resampled IC must take more than one distinct value across replicates."""
    recs = _noise_segments(seg_len=6, n_seg=30, seed=5)
    seen = []
    real_spearman = ps._spearman

    def _spy(f, r):
        ic = real_spearman(f, r)
        seen.append(ic)
        return ic

    ps._spearman = _spy
    try:
        ps._stationary_block_bootstrap_ic_significance(
            {"X": recs}, expected_step_by_symbol={"X": _STEP}, n_resamples=25
        )
    finally:
        ps._spearman = real_spearman

    replicate_ics = [v for v in seen[1:] if v is not None]  # seen[0] = observed IC
    assert len(set(replicate_ics)) > 1, (
        f"all {len(replicate_ics)} bootstrap replicates produced the identical "
        "IC -- segments are being included deterministically, so there is no "
        "resampling variance at all"
    )


def test_noise_false_positive_rate_is_near_nominal_not_total():
    """Calibration guard. At alpha=0.10 a handful of the 30 pure-noise datasets
    may flag by chance (the gap-blind None path measures ~22% on this shape, so
    the bar is deliberately loose); what must never return is the pre-fix
    behaviour where EVERY dataset flagged."""
    flagged = 0
    for sd in range(30):
        recs = _noise_segments(seg_len=6, n_seg=30, seed=2000 + sd)
        got = ps._stationary_block_bootstrap_ic_significance(
            {"X": recs}, expected_step_by_symbol={"X": _STEP}, n_resamples=200
        )
        flagged += bool(got["significant"])
    assert flagged <= 15, (
        f"{flagged}/30 pure-noise datasets flagged significant -- far above the "
        "~22% the accepted gap-blind path measures on this shape; the gap-aware "
        "path is anti-conservative"
    )


def test_single_segment_still_takes_the_deterministic_path():
    """The multi-segment draw must not disturb the single-segment case, which is
    what keeps a gap-free series identical with and without expected_step
    (pinned by test_bootstrap_gapfree_unchanged)."""
    fc = [1.0, 2.0, 1.0, 3.0, 2.0, 1.0, 4.0, 2.0]
    rt = [10.0, -5.0, 3.0, 8.0, -2.0, 6.0, -4.0, 1.0]
    recs = [
        {"forecast": f, "next_return_bps": r, "timestamp": _BASE + pd.Timedelta(i, unit="h")}
        for i, (f, r) in enumerate(zip(fc, rt))
    ]
    with_step = ps._stationary_block_bootstrap_ic_significance(
        {"S": recs}, block_size=3, n_resamples=4, seed=0, expected_step_by_symbol={"S": _STEP}
    )
    without = ps._stationary_block_bootstrap_ic_significance(
        {"S": recs}, block_size=3, n_resamples=4, seed=0
    )
    assert with_step == without
