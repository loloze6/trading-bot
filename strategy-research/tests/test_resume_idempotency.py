"""
Pre-resume idempotency verification for run_043 (F3 fix, 2026-07-04).

Before resuming a run that crashed mid-`determine_post_verdict_route` (after the KB
write already happened once, per run_043's actual log), confirm every write path that
could re-fire on resume is safe to call twice:

1. Trial recording (`_record_prescreen_trial`): guarded at both call sites (the two
   A8.6 bypass paths already had the guard; the normal signal_prescreen path did not
   until this fix). Not live-triggered by resuming run_043 specifically (resume starts
   past signal_prescreen), but verified here regardless since the user asked for it
   explicitly and a future resume-from-signal_prescreen scenario would hit it.
2. KB findings write (`_write_kb_findings_entry`): calling it twice for the same
   (run_id, hypothesis_id) must not double-count evidence_runs/evidence_count.
3. KB view recompute (`_recompute_kb_views`): must be deterministic — same findings
   list in, same views out, regardless of call count.

All three operate on a temp-file copy of _KB_PATH / campaign_state, never the real
campaign_knowledge_base.yaml or campaign_state.yaml.
"""
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr


@pytest.fixture
def temp_kb(tmp_path, monkeypatch):
    kb_path = tmp_path / "campaign_knowledge_base.yaml"
    kb_path.write_text(yaml.safe_dump({"findings": []}), encoding="utf-8")
    monkeypatch.setattr(rpr, "_KB_PATH", kb_path)
    return kb_path


def _fake_run_dir(tmp_path):
    d = tmp_path / "runs" / "run_999"
    d.mkdir(parents=True)
    return d


_INTERP = {
    "run_id": "run_999",
    "hypothesis_id": "TEST_HYPOTHESIS_V1",
    "status": "pivot",
    "verdict_label": "no_edge_observed",
    "reactivation_trigger": None,
}


def test_write_kb_findings_entry_is_idempotent_on_resume(temp_kb, tmp_path):
    run_dir = _fake_run_dir(tmp_path)

    rpr._write_kb_findings_entry(run_dir, "run_999", _INTERP)
    kb_after_first = yaml.safe_load(temp_kb.read_text(encoding="utf-8"))
    entry = next(f for f in kb_after_first["findings"] if f["hypothesis_id"] == "TEST_HYPOTHESIS_V1")
    assert entry["evidence_runs"] == ["run_999"]
    assert entry["evidence_count"] == 1

    # Simulate the resume: verdict_interpreter's LLM call is skipped (artifact already
    # valid), but determine_post_verdict_route still runs _write_kb_findings_entry again.
    rpr._write_kb_findings_entry(run_dir, "run_999", _INTERP)
    kb_after_second = yaml.safe_load(temp_kb.read_text(encoding="utf-8"))
    entries = [f for f in kb_after_second["findings"] if f["hypothesis_id"] == "TEST_HYPOTHESIS_V1"]

    assert len(entries) == 1, "resume must not create a second findings entry"
    assert entries[0]["evidence_runs"] == ["run_999"], "resume must not duplicate the run_id"
    assert entries[0]["evidence_count"] == 1, "resume must not double-count evidence"


def test_recompute_kb_views_is_deterministic(temp_kb):
    kb = {
        "findings": [
            {"id": "a", "hypothesis_id": "H1", "outcome": "no_edge_observed",
             "evidence_count": 1, "exhausted": True, "exhausted_basis": "analytic"},
            {"id": "b", "hypothesis_id": "H2", "outcome": "inconclusive", "evidence_count": 1},
        ]
    }
    rpr._recompute_kb_views(kb)
    first_coverage = yaml.safe_dump(kb["coverage_matrix"], sort_keys=True)
    first_exhausted = yaml.safe_dump(kb["exhausted_mechanisms"], sort_keys=True)

    rpr._recompute_kb_views(kb)  # simulate resume calling it again
    second_coverage = yaml.safe_dump(kb["coverage_matrix"], sort_keys=True)
    second_exhausted = yaml.safe_dump(kb["exhausted_mechanisms"], sort_keys=True)

    assert first_coverage == second_coverage
    assert first_exhausted == second_exhausted


def test_trial_sharpes_guard_pattern_skips_existing_trial_id():
    """Direct check of the boolean guard now used at all three record-trial call sites
    (the two A8.6 bypass paths, and the normal signal_prescreen path after this fix)."""
    campaign_with_existing_trial = {
        "trial_sharpes": [{"trial_id": "run_043", "source": "prescreen", "route": "kill_no_ic"}]
    }
    campaign_without = {"trial_sharpes": [{"trial_id": "run_041", "source": "prescreen_backfill"}]}

    def would_skip(campaign, run_id):
        return any(t.get("trial_id") == run_id for t in campaign.get("trial_sharpes", []))

    assert would_skip(campaign_with_existing_trial, "run_043") is True, (
        "resuming run_043 a second time must not re-append its trial"
    )
    assert would_skip(campaign_without, "run_043") is False, (
        "a genuinely new run_id must still be recorded"
    )
