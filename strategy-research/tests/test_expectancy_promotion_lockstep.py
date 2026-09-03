"""
CUL-193: the sparse/expectancy promotion path must actually produce a real
pass/fail once expectancy_bps and expectancy_se are available, and the two
lockstep implementations (workflow/run_phase1_research.py::_write_promotion_audit
and tools/deflate_sharpe.py::compute_promotion_audit) must agree on the verdict
for identical inputs -- same discipline as test_dedup_predicate_lockstep.py
(#57), correction_method (#40/#43), and sigma_sr (#56): pin AGREEMENT between
the two paths, not either one's literal formula, because the recurring defect
class here is mirrored sites drifting apart.

Root cause this closes: `per_trade_expectancy_bps` in protocol_result.yaml's
hypothesis_verdict.diagnostics is a {mean, se, t_stat, n} dict on the real
trade-diagnostics path (run_protocol.py's A3.4 summary) -- the SE was already
being computed and stored upstream. _write_promotion_audit was reading the
whole dict as if it were the bare mean, so expectancy_se was never extracted
and t_stat/passes stayed permanently null. deflate_sharpe.py already read the
dict correctly; only the pipeline's own implementation had the bug.

run_phase1_research.py cannot be imported directly in this test environment
(constructs a genai.Client() at import time, needs an API key env var), so
this follows the established pattern in test_dedup_predicate_lockstep.py:
a local transcription of the fixed logic, tested for agreement against the
real library function, PLUS a guard that reads the real shipped source and
asserts the fix (and the absence of the old placeholder) is actually there.
"""
import sys
from pathlib import Path

import pytest

_SR = Path(__file__).parent.parent
sys.path.insert(0, str(_SR / "tools"))

from deflate_sharpe import compute_promotion_audit  # noqa: E402


def _pipeline_sparse_verdict(expectancy_bps, expectancy_se):
    """Transcription of _write_promotion_audit's post-fix sparse branch
    (workflow/run_phase1_research.py). States the contract even where the
    pipeline body is not importable."""
    t_stat = None
    if expectancy_bps is not None and expectancy_se is not None and expectancy_se > 0:
        t_stat = expectancy_bps / expectancy_se
    passes = None if t_stat is None else (t_stat > 2.0)
    return t_stat, passes


def _library_sparse_verdict(expectancy_bps, expectancy_se, n_trades=10):
    """Runs the real compute_promotion_audit end-to-end (not a transcription)
    so the library side of the agreement check is the actual shipped code."""
    result = compute_promotion_audit(
        hypothesis_id="h_test",
        candidate_sr=None,  # None triggers the sparse path
        campaign_state={"trial_sharpes": []},
        n_trades=n_trades,
        expectancy_bps=expectancy_bps,
        expectancy_se=expectancy_se,
    )
    ep = result["expectancy_promotion"]
    return ep["t_stat"], ep["passes"]


@pytest.mark.parametrize("expectancy_bps, expectancy_se, expect_t_stat, expect_passes", [
    (10.0, 4.0,  2.5,   True),   # comfortably above threshold -> promotes
    (10.0, 6.0,  1.6667, False), # comfortably below threshold -> fails
    (10.0, 5.0,  2.0,   False),  # exactly at the boundary -> t > 2.0 is strict, does NOT pass
    (10.04, 5.0, 2.008, True),   # just over the boundary -> passes
    (-5.0, 2.0, -2.5,   False),  # negative expectancy -> never passes regardless of magnitude
])
def test_both_paths_agree_on_the_sparse_verdict(expectancy_bps, expectancy_se, expect_t_stat, expect_passes):
    pipe_t, pipe_passes = _pipeline_sparse_verdict(expectancy_bps, expectancy_se)
    lib_t, lib_passes = _library_sparse_verdict(expectancy_bps, expectancy_se)

    assert pipe_t == pytest.approx(expect_t_stat, rel=1e-3)
    assert lib_t == pytest.approx(expect_t_stat, rel=1e-3)
    assert pipe_passes is expect_passes
    assert lib_passes is expect_passes, (
        f"deflate_sharpe.py's own sparse branch disagrees with the expected verdict "
        f"for expectancy_bps={expectancy_bps}, expectancy_se={expectancy_se}"
    )


@pytest.mark.parametrize("expectancy_bps, expectancy_se", [
    (None, 5.0),     # mean unavailable
    (10.0, None),    # SE unavailable -- the exact CUL-193 failure mode before the fix
    (10.0, 0.0),     # SE present but zero -- division-by-zero guard
    (10.0, -1.0),    # SE present but negative -- degenerate, must not compute a t_stat
])
def test_both_paths_return_indeterminate_not_false_when_unmeasurable(expectancy_bps, expectancy_se):
    """CUL-163: an unmeasurable t-stat must stay None (indeterminate), never
    collapse to False -- a candidate that was never evaluated must not be
    treated as a terminal reject."""
    pipe_t, pipe_passes = _pipeline_sparse_verdict(expectancy_bps, expectancy_se)
    lib_t, lib_passes = _library_sparse_verdict(expectancy_bps, expectancy_se)

    assert pipe_t is None and pipe_passes is None
    assert lib_t is None and lib_passes is None


def test_the_real_pipeline_site_extracts_the_dict_shape_not_the_bare_mean():
    """Guards the shipped file, not the transcription above -- same reasoning
    as test_dedup_predicate_lockstep.py's real-source guards. Reading
    per_trade_expectancy_bps as a bare scalar (the CUL-193 bug) is the
    regression this must catch."""
    src = (_SR / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    idx = src.index('_exp_block = hv_diag.get("per_trade_expectancy_bps")')
    block = src[idx:idx + 500]

    assert 'expectancy_se  = _exp_block.get("se")' in block, (
        "the pipeline no longer extracts expectancy_se from the "
        "{mean, se, t_stat, n} dict -- CUL-193's fix has regressed"
    )
    assert 'expectancy_bps = _exp_block.get("mean")' in block, (
        "the pipeline no longer extracts the mean from the dict shape"
    )


def test_the_real_pipeline_site_no_longer_has_the_permanent_placeholder():
    """The exact CUL-193 bug: exp_se hardcoded to None with a comment saying
    it isn't stored yet, guaranteeing passes_deflated stays null forever on
    every sparse candidate. Must not come back."""
    src = (_SR / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    idx = src.index("if is_sparse:")
    block = src[idx:idx + 1800]

    assert 'exp_se   = None  # SE not yet stored in protocol_result; placeholder' not in block, (
        "the permanent SE-unavailable placeholder is back -- CUL-193's sparse "
        "promotion path would be indeterminate on every candidate again"
    )
    assert 't_stat = expectancy_bps / expectancy_se' in block, (
        "the pipeline no longer computes a real t_stat from expectancy_bps/expectancy_se"
    )
    assert 'passes_deflated = None if t_stat is None else (t_stat > 2.0)' in block, (
        "the pipeline no longer computes a real passes_deflated value, or the "
        "threshold/indeterminate convention has drifted from deflate_sharpe.py"
    )
