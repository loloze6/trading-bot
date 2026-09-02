"""
CUL-233: deduplicate_trials must honour `reproduces_trial`.

deduplicate_trials keyed only on (forecast_hash, source) and always kept a
hashless row. H006's T038 is a byte-identical re-execution of H005's T036
(reproduces_trial=T036, identical config_sha b9bfab00, result reproduced to
1e-6), but T036 predates the forecast_hash field (hashless) and T038 carries a
fresh hash 43ca26c6 -- so the two did NOT collapse and counted TWICE in the DSR
N. Fix: a row whose reproduces_trial chain resolves (transitively, within the
same source) to an original present in the input collapses onto it, independent
of hash presence.

Rules pinned here:
  (1) the pair counts once when both are present;
  (2) an absent referenced trial => the reproducing row counts on its own
      (never silently drop a trial);
  (3) a CHAIN (A->B->C) collapses transitively onto the terminal original;
      cycles (A<->B) and self-reference fail loud;
  (4) the collapse is WITHIN-source -- it respects the (forecast_hash, source)
      convention that a trial legitimately carries one row per source (see
      test_issue36_dedup_source.py::test_prescreen_and_backtest_rows_both_survive_dedup);
  (5) rows WITHOUT reproduces_trial dedupe byte-identically to before.

The lockstep test executes the REAL pipeline function
(run_phase1_research._dedupe_trials, CUL-233 F3) against the library, not a
transcription.
"""

import sys
from pathlib import Path

import pytest

_SR = Path(__file__).parent.parent
sys.path.insert(0, str(_SR / "tools"))
sys.path.insert(0, str(_SR / "workflow"))

import deflate_sharpe as ds  # noqa: E402


def _row(
    trial_id,
    source="backtest",
    forecast_hash=None,
    reproduces_trial=None,
    sharpe: float | None = 0.1,
):
    r = {
        "trial_id": trial_id,
        "source": source,
        "sharpe": sharpe,
        "statistic_valid": "sharpe",
    }
    if forecast_hash is not None:
        r["forecast_hash"] = forecast_hash
    if reproduces_trial is not None:
        r["reproduces_trial"] = reproduces_trial
    return r


# ---------------------------------------------------------------------------
# Rule 1 -- the pair counts once when both are present.
# ---------------------------------------------------------------------------


def test_reproduces_pair_counts_once():
    """The exact T036/T038 shape: T036 hashless (predates the field), T038 a
    fresh-hashed reproduction. Under the old (forecast_hash, source)-only key
    they counted twice; now T038 collapses onto T036."""
    t036 = _row("T036", forecast_hash=None, sharpe=5.2577)
    t038 = _row("T038", forecast_hash="43ca26c6", reproduces_trial="T036", sharpe=5.2577)

    kept, n_removed = ds.deduplicate_trials([t036, t038])

    assert n_removed == 1
    assert len(kept) == 1
    assert kept[0]["trial_id"] == "T036", "the original is kept, the reproduction collapses"


def test_reproduces_collapse_independent_of_hash_presence():
    """The collapse must fire regardless of whether the reproducing row carries a
    hash -- both a hashed and a hashless reproduction collapse onto their target."""
    orig = _row("A", forecast_hash=None)
    repro_hashed = _row("B", forecast_hash="ffff", reproduces_trial="A")
    repro_hashless = _row("C", forecast_hash=None, reproduces_trial="A")

    kept, n_removed = ds.deduplicate_trials([orig, repro_hashed, repro_hashless])

    assert n_removed == 2
    assert [r["trial_id"] for r in kept] == ["A"]


def test_reproduces_pair_counts_once_reversed_order():
    """Membership is over the whole input, not just already-seen rows: the
    reproduction collapses even when it appears BEFORE its original."""
    t038 = _row("T038", forecast_hash="43ca26c6", reproduces_trial="T036")
    t036 = _row("T036", forecast_hash=None)

    kept, n_removed = ds.deduplicate_trials([t038, t036])

    assert n_removed == 1
    assert [r["trial_id"] for r in kept] == ["T036"]


# ---------------------------------------------------------------------------
# Rule 2 -- absent referenced trial => count on its own (never silently drop).
# ---------------------------------------------------------------------------


def test_reproduces_target_absent_counts_alone():
    """If the referenced trial is not in the input, the reproducing row is a real
    counted attempt and must be kept -- dropping it would understate N."""
    repro = _row("T038", forecast_hash="43ca26c6", reproduces_trial="T036")

    kept, n_removed = ds.deduplicate_trials([repro])

    assert n_removed == 0
    assert len(kept) == 1
    assert kept[0]["trial_id"] == "T038"


def test_reproduces_target_present_only_under_other_source_counts_alone():
    """WITHIN-source (rule 4): the reproducing backtest row collapses only onto a
    same-source target. A T036 present only as a prescreen row does NOT absorb a
    T038 backtest row -- that would drop a real backtest Sharpe onto a different
    facet, the #36 bug class. Both survive."""
    t036_prescreen = _row("T036", source="prescreen", sharpe=None)
    t038_backtest = _row("T038", source="backtest", forecast_hash="43ca26c6", reproduces_trial="T036")

    kept, n_removed = ds.deduplicate_trials([t036_prescreen, t038_backtest])

    assert n_removed == 0
    assert {r["trial_id"] for r in kept} == {"T036", "T038"}


# ---------------------------------------------------------------------------
# Rule 3 -- chain collapses transitively; cycles / self-reference fail loud.
# ---------------------------------------------------------------------------


def test_reproduces_chain_collapses_transitively():
    """A -> B -> C (C terminal): a third-generation reproduction still counts
    once. Both A and B collapse onto C; only C survives (CUL-233 F4)."""
    a = _row("A", reproduces_trial="B")
    b = _row("B", reproduces_trial="C")
    c = _row("C")

    kept, n_removed = ds.deduplicate_trials([a, b, c])

    assert n_removed == 2
    assert [r["trial_id"] for r in kept] == ["C"]


def test_reproduces_chain_to_absent_terminal_keeps_row():
    """A -> B -> X where X is absent: the chain leaves the input, so the
    reproducing rows are kept (never silently dropped). B keeps A alive too."""
    a = _row("A", reproduces_trial="B")
    b = _row("B", reproduces_trial="X")  # X not in input

    kept, n_removed = ds.deduplicate_trials([a, b])

    assert n_removed == 0
    assert {r["trial_id"] for r in kept} == {"A", "B"}


def test_reproduces_self_reference_fails_loud():
    rec = _row("A", reproduces_trial="A")
    with pytest.raises(ValueError, match="self-reference"):
        ds.deduplicate_trials([rec])


def test_reproduces_cycle_fails_loud():
    """A reproduces B, B reproduces A -- must raise, not loop or silently drop."""
    a = _row("A", reproduces_trial="B")
    b = _row("B", reproduces_trial="A")
    with pytest.raises(ValueError, match="cycle"):
        ds.deduplicate_trials([a, b])


def test_reproduces_three_cycle_fails_loud():
    """A -> B -> C -> A: a longer cycle must also be refused, not loop forever."""
    a = _row("A", reproduces_trial="B")
    b = _row("B", reproduces_trial="C")
    c = _row("C", reproduces_trial="A")
    with pytest.raises(ValueError, match="cycle"):
        ds.deduplicate_trials([a, b, c])


# ---------------------------------------------------------------------------
# Rule 5 -- default no-op: rows without reproduces_trial are unchanged.
# ---------------------------------------------------------------------------


def test_no_reproduces_field_is_byte_identical_noop():
    """A ledger with no reproduces_trial anywhere must dedupe exactly as before
    the fix (the FORK_CHANGES default-behaviour guarantee)."""
    records = [{"trial_id": f"run_{i:03d}", "source": "backtest", "sharpe": float(i)} for i in range(14)]
    kept, n_removed = ds.deduplicate_trials(records)

    assert n_removed == 0
    assert kept == records


# ---------------------------------------------------------------------------
# Lockstep -- the REAL pipeline function agrees with the library (CUL-233 F3).
# run_phase1_research imports clean (lazy genai client), so the test executes
# the shipped _dedupe_trials, not a transcription.
# ---------------------------------------------------------------------------

import run_phase1_research as rpr  # noqa: E402


@pytest.mark.parametrize(
    "ledger",
    [
        [_row("T036"), _row("T038", forecast_hash="43ca26c6", reproduces_trial="T036")],
        [_row("T038", forecast_hash="43ca26c6", reproduces_trial="T036"), _row("T036")],
        [_row("A"), _row("B", reproduces_trial="A"), _row("C", reproduces_trial="A")],
        [_row("A", reproduces_trial="B"), _row("B", reproduces_trial="C"), _row("C")],
        [_row("T038", forecast_hash="43ca26c6", reproduces_trial="T036")],  # target absent
        [_row("t1", forecast_hash="h"), _row("t2", forecast_hash="h")],  # #36 hash collide
        [_row("t1", source="prescreen"), _row("t1", source="backtest")],  # cross-source keep
        [{"trial_id": f"r{i}", "source": "backtest", "sharpe": float(i)} for i in range(5)],
    ],
)
def test_both_paths_agree_on_reproduces(ledger):
    lib_kept, lib_removed = ds.deduplicate_trials(ledger)
    pipe_kept, pipe_removed = rpr._dedupe_trials(ledger)

    assert len(lib_kept) == len(pipe_kept)
    assert lib_removed == pipe_removed
    assert [r["trial_id"] for r in lib_kept] == [r["trial_id"] for r in pipe_kept]


@pytest.mark.parametrize(
    "bad_ledger",
    [
        [_row("A", reproduces_trial="A")],  # self-reference
        [_row("A", reproduces_trial="B"), _row("B", reproduces_trial="A")],  # cycle
    ],
)
def test_both_paths_fail_loud_on_bad_reproduces(bad_ledger):
    with pytest.raises(ValueError):
        ds.deduplicate_trials(bad_ledger)
    with pytest.raises(ValueError):
        rpr._dedupe_trials(bad_ledger)


# ---------------------------------------------------------------------------
# F2(a) -- _record_backtest_trial plumbs reproduces_trial additively.
# ---------------------------------------------------------------------------


def _capture_record(monkeypatch, summary):
    """Run rpr._record_backtest_trial against an in-memory campaign_state,
    returning the appended trial row."""
    state = {"trial_sharpes": []}
    monkeypatch.setattr(rpr, "load_campaign_state", lambda: state)
    monkeypatch.setattr(rpr, "_save_campaign_state", lambda s: None)
    monkeypatch.setattr(rpr, "_compute_forecast_hash", lambda p: "hash_x")
    rpr._record_backtest_trial("run_x", summary, Path("cfg.json"))
    return state["trial_sharpes"][-1]


_BASE_SUMMARY = {
    "per_symbol_summary": {"BTCUSDT": {"median_sharpe": 1.2}},
    "results": [{"core": {"trade_count": 100}}],
    "hypothesis_verdict": {"diagnostics": {}},
}


def test_record_backtest_trial_omits_reproduces_when_absent(monkeypatch):
    """Byte-identical default: a summary without reproduces_trial yields a row
    with NO reproduces_trial key (the pre-CUL-233 schema)."""
    row = _capture_record(monkeypatch, dict(_BASE_SUMMARY))
    assert "reproduces_trial" not in row
    assert set(row) == {
        "trial_id",
        "source",
        "sharpe",
        "expectancy_bps",
        "n_trades",
        "statistic_valid",
        "below_floor_pct",
        "forecast_hash",
    }


def test_record_backtest_trial_carries_reproduces_when_present(monkeypatch):
    """When the summary declares reproduces_trial, the ledger row carries it so
    deduplicate_trials can collapse the re-execution in the DSR N."""
    summary = dict(_BASE_SUMMARY, reproduces_trial="T036")
    row = _capture_record(monkeypatch, summary)
    assert row["reproduces_trial"] == "T036"
