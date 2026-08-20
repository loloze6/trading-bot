"""
C7-EXT-R2 (2026-07-23) — closed schema, deny by default.

G6 has failed three times, each time by enumerating the names of FORBIDDEN
fields, and each time the next reader defeated it with a name nobody had thought
of. Every test below re-runs a bypass from
engineering/sessions/session_reports/20260723_c7ext_r_audit.md VERBATIM, plus the two negative
cases that correctly held and must not regress, plus the one D-4 claim that
audit confirmed empirically.

A test here failing means the record store can once again be made to assert
something the campaign never established.
"""
import sys
from pathlib import Path

import pytest

_SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_SR_ROOT / "tools"))
sys.path.insert(0, str(_SR_ROOT / "workflow"))

import record_schema as rs  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402


# --------------------------------------------------------------------------
# The five audit bypasses, verbatim
# --------------------------------------------------------------------------

def test_r2_bypass_1_path_traversal_cannot_borrow_another_runs_result():
    """Re-audit attack 1 — the most consequential bypass found. The ownership
    check substring-matched the UNRESOLVED path, so the literal text contained
    "/runs/run_999_FAKE/" while open() followed ".." to run_059's real FAIL: a
    fabricated hypothesis citing a run that never executed borrowed a genuine
    result from an unrelated one."""
    entry = {
        "id": "FAKE_HYPOTHESIS_NEVER_RAN",
        "outcome": "kill_mechanism_falsified",
        "evidence_runs": ["run_999_FAKE"],
        "pass_rule_evaluation_ref":
            "runs/run_999_FAKE/../run_059/artifacts/pass_rule_evaluation.yaml",
    }
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry, root=_SR_ROOT)
    # Keep this verbatim replay honest across platforms: Windows collapses `..`
    # lexically so `run_999_FAKE/../run_059` resolves to a real file and the
    # containment gate fires; POSIX won't walk `..` through the non-existent
    # run_999_FAKE, so the existence gate fires first with a different message.
    # Both are the ref-resolution refusal we mean to pin; the containment branch
    # is exercised on every platform by the hermetic companion below.
    msg = str(exc.value)
    assert "does not confer provenance" in msg, msg
    assert ("does not exist" in msg
            or "does not lie under any of this entry's own runs" in msg), msg


def test_r2_bypass_1a_containment_branch_fires_on_every_platform(tmp_path):
    """The containment gate — the only thing standing between a fabricated entry
    and a victim run's real PASS — must fire on every OS, not only where the OS
    happens to collapse `..` lexically. The cited run EXISTS here, so `..`
    resolves through it into a DIFFERENT run; existence passes and containment is
    what refuses it. This is the cross-platform half of the verbatim replay above."""
    runs = tmp_path / "runs"
    (runs / "run_B").mkdir(parents=True)
    victim = runs / "run_A" / "artifacts"
    victim.mkdir(parents=True)
    (victim / "pass_rule_evaluation.yaml").write_text("result: PASS\n", encoding="utf-8")

    entry = {
        "id": "FAKE_BORROWS_RUN_A",
        "outcome": "kill_mechanism_falsified",
        "evidence_runs": ["run_B"],  # exists, but is not the victim
        "pass_rule_evaluation_ref":
            "runs/run_B/../run_A/artifacts/pass_rule_evaluation.yaml",
    }
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry, root=tmp_path)
    assert "does not lie under any of this entry's own runs" in str(exc.value)
    assert "resolves to" in str(exc.value), "must be refused on the RESOLVED path"


def test_r2_bypass_2_verdict_nested_one_level_down_is_refused():
    """Re-audit attack 2. strict_fields iterated only the entry's top-level keys."""
    entry = {"id": "FAKE_NESTED",
             "details": {"hypothesis_verdict": "kill", "verdict_c7": "kill"}}
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry, root=_SR_ROOT)
    assert "details" in str(exc.value)


def test_r2_bypass_3_verdict_inside_a_list_is_refused():
    """Re-audit attack 3."""
    entry = {"id": "FAKE_LIST",
             "decisions": [{"verdict_c7": "kill", "note": "buried in a list"}]}
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry, root=_SR_ROOT)
    assert "decisions" in str(exc.value)


@pytest.mark.parametrize("field", ["status", "disposition", "resolution",
                                   "result", "decision", "conclusion"])
def test_r2_bypass_4_plain_english_names_are_refused(field):
    """Re-audit attack 4 — all six were accepted, because none of these names
    contains the substring "verdict"."""
    with pytest.raises(vce.UngatedVerdictError):
        vce.validate_verdict_provenance({"id": "FAKE_" + field, field: "kill"},
                                        root=_SR_ROOT)


@pytest.mark.parametrize("field", ["veredicto_c7", "urteil", "verdikt",
                                   "verdicto", "final_veredicto"])
def test_r2_bypass_5_non_english_names_are_refused(field):
    """Re-audit attack 5. Four of five were accepted; only "verdicto" was caught,
    and only because the English word happens to be a prefix of the Spanish one.
    A gate that works by linguistic coincidence is not a gate."""
    with pytest.raises(vce.UngatedVerdictError):
        vce.validate_verdict_provenance({"id": "FAKE_" + field, field: "kill"},
                                        root=_SR_ROOT)


def test_r2_bypass_6_entry_naming_no_run_cannot_cite_any_evaluation():
    """NOT from the re-audit — found while implementing C7-EXT-R2, and named
    rather than silently fixed. With no evidence_runs/run_ids/run_id the
    ownership check was skipped outright (`if run_ids:`), so an entry naming no
    run at all could cite any evaluation in the tree."""
    entry = {"id": "FAKE_NO_RUNS", "outcome": "kill_mechanism_falsified",
             "pass_rule_evaluation_ref":
                 "runs/run_059/artifacts/pass_rule_evaluation.yaml"}
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry, root=_SR_ROOT)
    assert "names no run" in str(exc.value)


# --------------------------------------------------------------------------
# The negative cases that correctly held — must not regress, and must still be
# refused for their ORIGINAL reason rather than incidentally by the schema
# --------------------------------------------------------------------------

def test_r2_hold_a_real_file_with_no_binding_result_still_refused():
    """Re-audit attack 6 (correct-hold). run_059's prescreen_result.yaml is real
    and correctly run-scoped, but records no PASS/FAIL."""
    entry = {"id": "A", "outcome": "completed_rejected", "evidence_runs": ["run_059"],
             "pass_rule_evaluation_ref": "runs/run_059/artifacts/prescreen_result.yaml"}
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry, root=_SR_ROOT)
    assert "is not a resolved verdict" in str(exc.value)


def test_r2_hold_b_absolute_path_outside_any_run_still_refused(tmp_path):
    """Re-audit attack 7 (correct-hold). The non-traversal absolute-path escape
    was already caught; it still is."""
    fabricated = tmp_path / "fake.yaml"
    fabricated.write_text("result: PASS\n", encoding="utf-8")
    entry = {"id": "B", "outcome": "completed_rejected", "evidence_runs": ["run_059"],
             "pass_rule_evaluation_ref": str(fabricated)}
    with pytest.raises(vce.UngatedVerdictError) as exc:
        vce.validate_verdict_provenance(entry, root=_SR_ROOT)
    assert "does not lie under any of this entry's own runs" in str(exc.value)


# --------------------------------------------------------------------------
# The D-4 claim the re-audit confirmed empirically
# --------------------------------------------------------------------------

def test_r2_save_queue_whole_list_atomicity_no_partial_write(tmp_path, monkeypatch):
    """A bad entry mixed into an otherwise-legitimate write is rejected AND the
    file is not written at all — os.replace is never reached."""
    import run_campaign
    queue_dir = tmp_path / "config"
    queue_dir.mkdir(parents=True)
    queue_path = queue_dir / "campaign_queue.yaml"
    monkeypatch.setattr(run_campaign, "QUEUE_PATH", queue_path)
    monkeypatch.setattr(run_campaign, "ROOT", tmp_path)

    with pytest.raises(vce.UngatedVerdictError):
        run_campaign._save_queue({"queue": [
            {"id": "legit_entry", "status": "ready"},
            {"id": "BAD_HAND_EDIT", "outcome": "kill_mechanism_falsified",
             "run_ids": ["run_999_never_ran"]},
        ]})
    assert not queue_path.exists(), "partial write occurred: os.replace was reached"

    # The same list, with the bad entry made honest, writes cleanly.
    run_campaign._save_queue({"queue": [
        {"id": "legit_entry", "status": "ready"},
        {"id": "NOW_HONEST", "outcome": "kill_mechanism_falsified",
         "run_ids": ["run_999_never_ran"], "verdict_status": "ungated"},
    ]})
    assert queue_path.exists()


# --------------------------------------------------------------------------
# The closed schema's own properties — why this is a different class of fix
# --------------------------------------------------------------------------

def test_r2_closed_schema_rejects_unknown_fields_by_default():
    """Rejection does not depend on recognising the field as dangerous."""
    with pytest.raises(rs.RecordSchemaError) as exc:
        rs.validate_kb_finding({"id": "x", "some_field_nobody_anticipated": "hello"})
    assert "unknown field" in str(exc.value)


def test_r2_closed_schema_refuses_a_nested_mapping_inside_a_data_field():
    """signal_property holds 66 distinct measurement keys, so its KEYS cannot be
    enumerated. Its SHAPE can: flat scalars only, which is what stops an
    arbitrary structure being smuggled inside a permitted field."""
    with pytest.raises(rs.RecordSchemaError) as exc:
        rs.validate_kb_finding({"id": "x",
                                "signal_property": {"nested": {"verdict": "kill"}}})
    assert "nested mapping is not permitted" in str(exc.value)


def test_r2_bare_verdict_token_refused_as_a_value_anywhere():
    """The name-agnostic half: the key is arbitrary and unenumerable, so the
    CLAIM is what gets refused."""
    with pytest.raises(rs.RecordSchemaError):
        rs.validate_kb_finding({"id": "x", "signal_property": {"anything_at_all": "kill"}})
    with pytest.raises(rs.RecordSchemaError):
        rs.validate_kb_finding({"id": "x", "root_cause": "promote"})
    # Prose that DISCUSSES a verdict is untouched — the match is whole-value.
    rs.validate_kb_finding({"id": "x", "outcome_reason":
                            "the pass_rule would kill this on criterion (a)"})


def test_r2_superseded_history_may_still_record_a_withdrawn_verdict():
    """Retaining what was once claimed is the opposite of asserting it, and the
    D-5/D-6 corrections depend on being able to keep that history."""
    rs.validate_kb_finding({
        "id": "x",
        "outcome_history_superseded": [
            {"outcome": "kill_er_gate_mechanism_falsified",
             "recorded_at": "2026-07-11", "superseded_at": "2026-07-22",
             "superseded_reason": "see readjudication"},
        ],
    })
    with pytest.raises(rs.RecordSchemaError) as exc:
        rs.validate_kb_finding({"id": "x", "outcome_history_superseded": [
            {"outcome": "kill_x", "smuggled": "kill"}]})
    assert "smuggled" in str(exc.value)


def test_r2_queue_status_and_relation_keep_their_own_vocabularies():
    """`status: done` and `relation: refine` are legitimate queue values that
    collide with the verdict-token rule. They are handled by giving each field a
    closed vocabulary — tighter than free text, not looser — which is what lets
    the token rule stay absolute everywhere else."""
    rs.validate_queue_entry({"id": "Q", "status": "done", "relation": "refine",
                             "source": "agent"})
    with pytest.raises(rs.RecordSchemaError):
        rs.validate_queue_entry({"id": "Q", "status": "kill"})
    with pytest.raises(rs.RecordSchemaError):
        rs.validate_queue_entry({"id": "Q", "relation": "kill"})


def test_r2_live_records_conform_to_the_closed_schema():
    """The corrected archive itself must satisfy the schema it is now governed by."""
    import yaml
    kb = yaml.safe_load(
        (_SR_ROOT / "campaign_record" / "campaign_knowledge_base.yaml").read_text(encoding="utf-8"))
    for entry in kb["findings"]:
        rs.validate_kb_finding(entry, "KB " + repr(entry.get("id")))
    queue = yaml.safe_load(
        (_SR_ROOT / "config" / "campaign_queue.yaml").read_text(encoding="utf-8"))
    for entry in queue["queue"]:
        rs.validate_queue_entry(entry, "queue " + repr(entry.get("id")))
