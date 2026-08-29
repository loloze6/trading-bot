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
