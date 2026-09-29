"""
#57: the two lockstep DSR paths must dedup trials by the SAME predicate.

The pipeline (run_phase1_research) and the library (deflate_sharpe) each
deduplicate trials on (forecast_hash, source). They disagreed on what a
falsy-but-PRESENT hash means: the pipeline's `if fh` read "" as "no hash" and
kept duplicates as unique, while the library's `if fh is None` read "" as a real
hash and deduped them. Same ledger in, different N out -- and N is the deflated
Sharpe denominator.

Following the #43 pattern deliberately: this pins AGREEMENT BETWEEN THE TWO
PATHS rather than either one's literal predicate, because the defect class here
is mirrored sites drifting, not any particular wrong constant. Third instance
after correction_method (#40) and sigma_sr (#56).
"""
import math
import statistics
import sys
from pathlib import Path

import pytest

_SR = Path(__file__).parent.parent
sys.path.insert(0, str(_SR / "tools"))

from deflate_sharpe import deduplicate_trials  # noqa: E402


def _pipeline_dedup(valid_trials):
    """The pipeline's predicate, transcribed from
    run_phase1_research.py's dedup block. Kept as a local transcription so the
    test states the contract even where the pipeline body is not importable."""
    seen_keys: set = set()
    deduped, n_removed = [], 0
    for t in valid_trials:
        fh = t.get("forecast_hash")
        if fh is None:
            deduped.append(t)
            continue
        key = (fh, t.get("source"))
        if key in seen_keys:
            n_removed += 1
        else:
            seen_keys.add(key)
            deduped.append(t)
    return deduped, n_removed


def _row(trial_id, fh, source="backtest"):
    return {"trial_id": trial_id, "forecast_hash": fh, "source": source,
            "sharpe": 0.1, "statistic_valid": "sharpe", "n_trades": 100}


@pytest.mark.parametrize("hash_value, expect_deduped", [
    ("", True),        # THE #57 case: falsy but PRESENT -> a real hash, dedups
    (0, True),         # same class, numeric
    ("abc123", True),  # ordinary hash, control
    (None, False),     # genuinely absent -> always unique, never deduped
])
def test_both_paths_agree_on_falsy_but_present_hash(hash_value, expect_deduped):
    ledger = [_row("t1", hash_value), _row("t2", hash_value)]

    lib_kept, lib_removed = deduplicate_trials(ledger)
    pipe_kept, pipe_removed = _pipeline_dedup(ledger)

    assert len(lib_kept) == len(pipe_kept), (
        f"paths disagree on forecast_hash={hash_value!r}: "
        f"library kept {len(lib_kept)}, pipeline kept {len(pipe_kept)}"
    )
    assert lib_removed == pipe_removed, (
        f"paths disagree on removal count for forecast_hash={hash_value!r}: "
        f"library {lib_removed}, pipeline {pipe_removed}"
    )

    expected_kept = 1 if expect_deduped else 2
    assert len(lib_kept) == expected_kept


def test_distinct_hashes_are_never_deduped_by_either_path():
    """Control: the fix must not over-dedup."""
    ledger = [_row("t1", "aaa"), _row("t2", "bbb")]
    lib_kept, _ = deduplicate_trials(ledger)
    pipe_kept, _ = _pipeline_dedup(ledger)
    assert len(lib_kept) == len(pipe_kept) == 2


def test_same_hash_different_source_is_not_deduped_by_either_path():
    """The key is (forecast_hash, source) -- a trial legitimately carries one
    prescreen row plus one backtest row (WRITER_CONTRACT)."""
    ledger = [_row("t1", "aaa", "prescreen"), _row("t1", "aaa", "backtest")]
    lib_kept, _ = deduplicate_trials(ledger)
    pipe_kept, _ = _pipeline_dedup(ledger)
    assert len(lib_kept) == len(pipe_kept) == 2


def test_the_real_pipeline_site_uses_the_unified_predicate():
    """The agreement tests above run a TRANSCRIPTION of the pipeline, because
    run_phase1_research constructs a genai.Client() at import time and so cannot
    be imported without the API-key env var present. A transcription proves the
    contract but guards nothing in the real file -- and a test of the
    ingredients is not a test of the recipe (learned the hard way on #50, where
    three mutations of the real call site survived an isolated test).

    So: assert against the real source that the drifted predicate has not come
    back. Crude, deliberately -- it is the cheapest control that actually reads
    the shipped file.
    """
    src = (_SR / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    block_start = src.index("deduped_trials = []")
    block = src[block_start:block_start + 1600]

    assert 'if fh is None:' in block, (
        "the pipeline dedup site must use the `is None` predicate (#57)"
    )
    assert 'if fh and key in seen_keys' not in block, (
        "the truthiness predicate is back at the pipeline dedup site -- a "
        'falsy-but-present forecast_hash ("" or 0) would again be kept as '
        "unique here while deflate_sharpe dedups it, so the two paths would "
        "report different N for the same ledger (#57)"
    )


# --------------------------------------------------------------------------
# #56 -- sigma_sr must agree between the same two lockstep paths.
#
# Second drift of this class (after correction_method, #40/#43); the dedup
# predicate above is the third. Same test shape deliberately: pin AGREEMENT,
# not a literal denominator, because the recurring defect is mirrored sites
# drifting apart rather than any one wrong formula.
# --------------------------------------------------------------------------

def _library_sigma_sr(sharpes):
    """deflate_sharpe.py's form: POPULATION variance, n denominator."""
    n = len(sharpes)
    mu = sum(sharpes) / n
    return math.sqrt(sum((s - mu) ** 2 for s in sharpes) / n)


def _pipeline_sigma_sr(sharpes):
    """run_phase1_research.py's form, transcribed after the #56 fix."""
    mu = statistics.mean(sharpes)
    var = sum((v - mu) ** 2 for v in sharpes) / len(sharpes)
    return math.sqrt(var)


@pytest.mark.parametrize("sharpes", [
    [0.1, 0.4, -0.2, 0.9, 0.3],
    [1.0, 1.0000001],                      # near-degenerate, n=2
    [-0.5, -0.4, -0.45, -0.6, -0.2, 0.1],
    [0.2] * 3 + [0.9],
])
def test_sigma_sr_agrees_between_paths(sharpes):
    lib = _library_sigma_sr(sharpes)
    pipe = _pipeline_sigma_sr(sharpes)
    assert lib == pytest.approx(pipe, rel=1e-12), (
        f"sigma_sr drift for {sharpes}: library={lib}, pipeline={pipe}"
    )


def test_sample_stdev_would_be_caught():
    """Sentinel: the pre-#56 sample form must NOT agree, or the test above is
    vacuous. sqrt(n/(n-1)) is ~5.4% at n=10."""
    sharpes = [0.1, 0.4, -0.2, 0.9, 0.3]
    assert statistics.stdev(sharpes) != pytest.approx(_library_sigma_sr(sharpes), rel=1e-6)


def test_the_real_pipeline_site_uses_the_population_denominator():
    """Guards the shipped file, not a transcription -- same reasoning as the
    dedup guard above."""
    src = (_SR / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    idx = src.index("mu_sr    = statistics.mean(sharpe_values)")
    block = src[idx:idx + 1200]
    assert "sum((v - mu_sr) ** 2 for v in sharpe_values) / len(sharpe_values)" in block, (
        "the pipeline must use the POPULATION denominator to match "
        "deflate_sharpe (#56)"
    )
    assert "statistics.stdev(sharpe_values)" not in block, (
        "statistics.stdev (SAMPLE, n-1) is back at the pipeline sigma_sr site -- "
        "the two lockstep DSR paths would again return different sigma_sr, "
        "E_max_SR and DSR for identical trial Sharpes (#56)"
    )


# --------------------------------------------------------------------------
# #48 F3 -- the promotion-audit SHAPE must agree between the two paths.
#
# Fourth instance of the mirrored-paths drift, and the first in the shape rather
# than a value: the pipeline's excluded_trial_counts carried dedup_removed and
# invalidated_artifact while the library's carried neither, then only the
# latter -- so audits from the two implementations were not field-comparable
# even though N itself agreed.
# --------------------------------------------------------------------------

_PIPELINE_EXCLUDED_KEYS = {
    "statistic_expectancy", "statistic_neither", "no_sharpe_value",
    "non_finite_sharpe", "dedup_removed", "invalidated_artifact",
}


def test_library_excluded_counts_carry_the_pipeline_key_set():
    """Runs compute_promotion_audit end-to-end so the assertion reads the real
    emitted dict, not a transcription of it."""
    from deflate_sharpe import compute_promotion_audit

    ledger = [
        _row("t1", "h1"), _row("t2", "h2"), _row("t3", "h3"),
        _row("t4", "h4"), _row("t5", "h5"),
    ]
    for i, r in enumerate(ledger):
        r["sharpe"] = 0.1 * (i + 1)

    result = compute_promotion_audit(
        hypothesis_id="h_test",
        candidate_sr=0.5,
        campaign_state={"trial_sharpes": ledger},
        n_trades=100,
    )
    excluded = result.get("excluded_trial_counts")

    assert excluded is not None, "compute_dsr must emit excluded_trial_counts"
    assert set(excluded) == _PIPELINE_EXCLUDED_KEYS, (
        "audit shape drift between the two DSR paths (#48 F3): library emits "
        f"{sorted(set(excluded))}, pipeline emits {sorted(_PIPELINE_EXCLUDED_KEYS)}"
    )


def test_the_real_pipeline_site_still_emits_the_same_key_set():
    """Guards the shipped pipeline file, so the agreement above cannot be
    satisfied by the library alone drifting to match a stale expectation."""
    src = (_SR / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    idx = src.index('excluded = {"statistic_expectancy"')
    block = src[idx:idx + 300]
    for key in _PIPELINE_EXCLUDED_KEYS:
        assert f'"{key}"' in block, (
            f"pipeline excluded-counts dict no longer carries {key!r} (#48 F3)"
        )


# --------------------------------------------------------------------------
# E-062 S2b-3c (D-047 (5)) -- EVERY dedupe copy agrees on mixed rows.
#
# Declared extension (S2b-3c): the dedupe key gained the optional window
# fingerprint `windows_sha256` next to `symbols`. The copies it must stay in
# lockstep across -- run on the REAL code, not a transcription:
#   deflate_sharpe.deduplicate_trials (and through it select_same_basis_sample's
#   N and compute_promotion_audit's total_hypotheses_tested),
#   run_phase1_research._dedupe_trials (and through it _promotion_dsr_context's
#   n_dsr_total, cross-checked by _whole_test_dsr_context), and
#   run_phase1_research._dedup_collapse_target's key (the dedup_collapse reason
#   must name the row the dedupe actually collapsed onto).
# --------------------------------------------------------------------------

def _mixed_rows(seed: int) -> list:
    import random
    rng = random.Random(seed)
    fps = ["a" * 64, "b" * 64, "c" * 64]
    rows = []
    for i in range(60):
        r = {"trial_id": f"t{i}", "source": rng.choice(["backtest", "backtest_failed"]),
             "statistic_valid": "sharpe", "sharpe": round(rng.uniform(-1, 1), 3),
             "forecast_hash": rng.choice(["h1", "h2", None])}
        if rng.random() < 0.6:
            r["symbols"] = [rng.choice(["BTCUSDT", "XRPUSD"])]
        if rng.random() < 0.5:
            r["windows_sha256"] = rng.choice(fps)
        rows.append(r)
    return rows


@pytest.mark.parametrize("seed", range(6))
def test_every_dedupe_copy_agrees_on_rows_with_and_without_the_window_fingerprint(seed):
    sys.path.insert(0, str(_SR / "workflow"))
    import run_phase1_research as rpr
    from deflate_sharpe import compute_promotion_audit, select_same_basis_sample

    rows = _mixed_rows(seed)
    lib_kept, lib_removed = deduplicate_trials(rows)
    pipe_kept, pipe_removed = rpr._dedupe_trials(rows)
    assert lib_kept == pipe_kept and lib_removed == pipe_removed
    n = len(lib_kept)
    assert select_same_basis_sample(rows)["N"] == n
    assert compute_promotion_audit(hypothesis_id="h", candidate_sr=0.1,
                                   campaign_state={"trial_sharpes": rows},
                                   n_trades=100)["total_hypotheses_tested"] == n
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, {"campaign_id": "t", "runs": [], "trial_sharpes": rows})
    assert rpr._promotion_dsr_context()["n_dsr_total"] == n
    assert rpr._whole_test_dsr_context()["n_dsr_total"] == n  # raises if its sample N differs

    # _dedup_collapse_target's key: every collapsed row names the FIRST kept row
    # with its full key (hash, coins, fingerprint, source) -- never another.
    kept_ids = {id(r) for r in lib_kept}
    wctx = {"rows": rows}
    for r in rows:
        if id(r) in kept_ids:
            continue
        first = next(k for k in lib_kept
                     if k.get("forecast_hash") == r.get("forecast_hash")
                     and k.get("source") == r.get("source")
                     and sorted(k.get("symbols") or []) == sorted(r.get("symbols") or [])
                     and ("symbols" in k) == ("symbols" in r)
                     and k.get("windows_sha256") == r.get("windows_sha256"))
        assert rpr._dedup_collapse_target(wctx, r) == (
            f"trial {first['trial_id']!r} (same forecast_hash, coins and source)")


def test_the_fingerprint_changes_n_only_where_it_is_present():
    """Stripping every fingerprint gives the pre-S2b-3c partition; the
    fingerprinted ledger can only count MORE trials (N never shrinks)."""
    for seed in range(6):
        rows = _mixed_rows(seed)
        stripped = [{k: v for k, v in r.items() if k != "windows_sha256"} for r in rows]
        assert len(deduplicate_trials(rows)[0]) >= len(deduplicate_trials(stripped)[0])
