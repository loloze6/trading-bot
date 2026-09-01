"""
E-025 S4 -- tests for the one-command two-writer demo (tools/dual_writer_demo.py).

Every proof the driver makes is asserted here, and each is mutation-proven at the
value level: the three named mutations -- an id collision that passes, the killed
row dropped, forecast_hash treated as optional -- each turns a green assertion red.

Synthetic fixtures only; the no-DSR-until-merged proof drives a hermetic local git
repo (no network). No market data, no live ledger.
"""
import copy
import sys
from pathlib import Path

import pytest

TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_PATH))

import deflate_sharpe as ds  # noqa: E402
import dual_writer_demo as demo  # noqa: E402


@pytest.fixture
def states():
    return demo.load_state("master_ledger.yaml"), demo.load_state("fork_ledger.yaml")


@pytest.fixture
def merged(states):
    master, fork = states
    return ds.union_merge_trial_ledgers(master["trial_sharpes"], fork["trial_sharpes"])


# ---------------------------------------------------------------------------
# End-to-end: the whole driver
# ---------------------------------------------------------------------------

def test_run_demo_all_proofs_pass():
    results = demo.run_demo()
    assert len(results) == 7
    failed = [r["name"] for r in results if not r["passed"]]
    assert not failed, f"proofs failed: {failed}"


def test_main_exits_zero_and_prints_verdict(capsys):
    rc = demo.main()
    out = capsys.readouterr().out
    assert rc == 0
    assert "VERDICT: ALL PROOFS PASS (7/7)" in out


# ---------------------------------------------------------------------------
# Fixtures synthetic -- mutation: a non-synthetic fixture must fail
# ---------------------------------------------------------------------------

def test_fixtures_are_synthetic(states):
    master, fork = states
    assert demo.proof_fixtures_are_synthetic(master, fork)["passed"]


def test_synthetic_proof_bites_on_a_live_range_id(states):
    master, fork = states
    fork = copy.deepcopy(fork)
    fork["trial_sharpes"][0]["trial_id"] = "run_d_042"  # a live-range id
    assert not demo.proof_fixtures_are_synthetic(master, fork)["passed"]


def test_synthetic_proof_bites_when_flag_missing(states):
    master, fork = states
    master = copy.deepcopy(master)
    master["synthetic"] = False
    assert not demo.proof_fixtures_are_synthetic(master, fork)["passed"]


# ---------------------------------------------------------------------------
# forecast_hash contract -- mutation: a null fh on a non-failed row must fail
# ---------------------------------------------------------------------------

def test_forecast_hash_contract_holds(states):
    _, fork = states
    assert demo.proof_forecast_hash_contract(fork)["passed"]


def test_forecast_hash_proof_bites_when_prescreen_hash_optional(states):
    """Named mutation 'forecast_hash optional': null a prescreen row's forecast_hash
    (illegal -- only backtest_failed may be null) and the proof must go red."""
    _, fork = states
    fork = copy.deepcopy(fork)
    for r in fork["trial_sharpes"]:
        if (r["trial_id"], r["source"]) == ("run_d_901", "prescreen"):
            r["forecast_hash"] = None
    assert not demo.proof_forecast_hash_contract(fork)["passed"]


# ---------------------------------------------------------------------------
# Union merges both
# ---------------------------------------------------------------------------

def test_union_merges_both(states):
    master, fork = states
    result = demo.proof_union_merges_both(master, fork)
    assert result["passed"]
    assert len(result["merged"]) == 9


# ---------------------------------------------------------------------------
# Append-only + idempotent
# ---------------------------------------------------------------------------

def test_append_only_and_idempotent(states, merged):
    master, fork = states
    assert demo.proof_append_only_and_idempotent(master, fork, merged)["passed"]


# ---------------------------------------------------------------------------
# Duplicate refusal -- mutation: an id collision that passes must fail a test
# ---------------------------------------------------------------------------

def test_duplicate_refusal_fires_on_manufactured_collision(states):
    master, fork = states
    assert demo.proof_duplicate_refusal(master, fork)["passed"]


def test_collision_refusal_is_specific_to_the_collision(states):
    """Named mutation 'id collision passing': the guard must refuse ONLY a true
    (trial_id, source) collision with differing content, not the shared-ancestor
    row. The clean union does NOT raise; the poisoned one DOES -- so a guard that
    let a collision through (mutation) would be caught here."""
    master, fork = states
    # clean: identical shared run_900/backtest on both sides -> no refusal
    ds.union_merge_trial_ledgers(master["trial_sharpes"], fork["trial_sharpes"])
    # poisoned: fork's shared row differs -> must refuse
    poisoned = copy.deepcopy(fork["trial_sharpes"])
    for r in poisoned:
        if (r["trial_id"], r["source"]) == ("run_900", "backtest"):
            r["sharpe"] = 0.999
    with pytest.raises(ValueError):
        ds.union_merge_trial_ledgers(master["trial_sharpes"], poisoned)


# ---------------------------------------------------------------------------
# Killed row counts toward N -- mutation: dropping it must change N
# ---------------------------------------------------------------------------

def test_killed_row_counts_toward_N(merged):
    assert demo.proof_killed_row_counts_toward_N(merged)["passed"]


def test_dropping_the_killed_row_lowers_N_by_one(merged):
    """Named mutation 'killed row dropped': removing the killed prescreen row from
    the ledger drops the deduplicated N by exactly one -- proof it was counted."""
    killed_key = ("run_d_901", "prescreen")
    n_with = len(ds.deduplicate_trials(merged)[0])
    without = [r for r in merged if (r["trial_id"], r["source"]) != killed_key]
    n_without = len(ds.deduplicate_trials(without)[0])
    assert n_with == n_without + 1


def test_killed_row_absent_from_sharpe_sample(merged):
    sharpe_values, _ = ds.load_sharpe_trials({"trial_sharpes": merged})
    assert sorted(sharpe_values) == [-0.6375, 0.18, 0.30]  # no null/killed value


# ---------------------------------------------------------------------------
# No DSR until merged (hermetic git)
# ---------------------------------------------------------------------------

def test_no_dsr_until_merged(states, merged):
    master, fork = states
    result = demo.proof_no_dsr_until_merged(master, fork, merged)
    assert result["passed"], result["detail"]


def test_pre_merge_N_is_strictly_smaller_than_merged_N(states, merged):
    _, fork = states
    n_premerge = len(ds.deduplicate_trials(fork["trial_sharpes"])[0])
    n_merged = len(ds.deduplicate_trials(merged)[0])
    assert n_premerge < n_merged  # computing DSR pre-merge understates the correction
