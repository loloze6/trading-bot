"""
E-018 (2026-09-13): mechanical-routing-first regression tests.

Design (agreed with the user in full, see the E-018 Linear epic): a BINDING
pass_rule_evaluation.yaml -- one carrying a concrete PASS/FAIL result, not a
`discretion: stage` branch -- now drives determine_post_verdict_route's
(hypothesis_verdict, lineage_routing) resolution DIRECTLY, instead of relying
on verdict_interpreter's own restated copy of that same pair (the old B4
"copy-through" discipline, which had no code-side enforcement of the copy
being correct -- routing read the LLM's restatement, and a mismatch could
only ever be caught POST-HOC by _check_pass_rule_evaluation_conformance).
This is what makes it safe to also give verdict_interpreter direct read
access to the near-miss scoreboard (documented separately in the epic): for
any run with a binding pass rule, the stage no longer holds the pen on the
actual promote/kill/refine decision, only on the qualitative writeup
(root_cause, findings_carryover, proposed_brief) -- so a scoreboard-informed
LLM cannot itself soften a mechanical bar.

Per the user's explicit instruction, there is NO guard conditioning the
scoreboard's visibility on whether a pass_rule happens to be registered for
this run (see verdict-interpreter/SKILL.md) -- but that is a prompt-level
concern; these tests only cover the routing-mechanics half, in
run_phase1_research.py.

Two things this file proves:
  1. A binding pass_rule_evaluation.yaml routes correctly even when
     verdict_interpretation.yaml disagrees -- and the disagreement is now
     INFORMATIONAL (recorded as a flag), not a human_pause.
  2. Absent or non-binding pass_rule_evaluation.yaml preserves the exact
     pre-E-018 behavior (regression safety) -- the artifact's own
     hypothesis_verdict/lineage_routing still drive routing, unchanged.
"""
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402

from test_k4_routing_registration import campaign_root, _write_fresh_scaffold  # noqa: E402,F401


def _write_verdict_interpretation(run_dir: Path, **fields):
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    with open(run_dir / "artifacts" / "verdict_interpretation.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(fields, f, sort_keys=False)


def _write_pass_rule_evaluation(run_dir: Path, **fields):
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    with open(run_dir / "artifacts" / "pass_rule_evaluation.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(fields, f, sort_keys=False)


def test_binding_fail_routes_kill_terminate_over_disagreeing_promote(campaign_root):
    """The LLM's own verdict_interpretation.yaml claims 'promote'; the binding
    mechanical evaluation says FAIL -> kill/terminate. Routing must follow the
    mechanical pair (completed_rejected, via _route_kill), not the LLM's
    claim -- and must NOT human_pause on the disagreement."""
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_800")
    run_dir = runs_dir / "run_800"

    _write_verdict_interpretation(
        run_dir,
        status="promote",
        hypothesis_verdict="promote",
        lineage_routing=None,
        hypothesis_family="test_family",
        root_cause={},
    )
    _write_pass_rule_evaluation(
        run_dir,
        result="FAIL",
        statement_branch_matched="FAIL-a",
        hypothesis_verdict="kill",
        lineage_routing="terminate",
    )

    next_stage = rpr.determine_post_verdict_route(run_dir, "run_800")

    assert next_stage == "completed_rejected", (
        "must route on the BINDING mechanical (kill, terminate) pair, not the "
        "stage's own disagreeing 'promote' restatement"
    )

    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state.get("status") != "paused_for_human", (
        "a stage/mechanical disagreement must be INFORMATIONAL only, per E-018 "
        "-- it must never block routing now that routing already used the "
        "mechanical verdict directly"
    )
    assert state.get("flags", {}).get("pass_rule_evaluation_disagreement") is True, (
        "the disagreement must still be recorded as a flag (LLM-comprehension "
        "signal), even though it no longer blocks"
    )


def test_binding_pass_routes_promote_over_disagreeing_kill(campaign_root):
    """Symmetric case: the LLM claims kill/terminate but the binding mechanical
    evaluation is PASS -> promote. Routing must follow promote (holdout_evaluation)."""
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_801")
    run_dir = runs_dir / "run_801"

    _write_verdict_interpretation(
        run_dir,
        status="kill",
        hypothesis_verdict="kill",
        lineage_routing="terminate",
        hypothesis_family="test_family",
        root_cause={},
    )
    _write_pass_rule_evaluation(
        run_dir,
        result="PASS",
        statement_branch_matched="PASS",
        hypothesis_verdict="promote",
        lineage_routing=None,
    )

    next_stage = rpr.determine_post_verdict_route(run_dir, "run_801")

    assert next_stage == "holdout_evaluation"
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state.get("flags", {}).get("walk_forward_passed") is True
    assert state.get("status") != "paused_for_human"


def test_absent_pass_rule_evaluation_preserves_prior_behavior(campaign_root):
    """No pass_rule_evaluation.yaml at all (pre-K2 / no registered pass rule):
    the artifact's own hypothesis_verdict/lineage_routing still drive routing,
    completely unchanged from pre-E-018 behavior."""
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_802")
    run_dir = runs_dir / "run_802"

    _write_verdict_interpretation(
        run_dir,
        status="kill",
        hypothesis_verdict="kill",
        lineage_routing="terminate",
        hypothesis_family="test_family",
        root_cause={},
    )
    assert not (run_dir / "artifacts" / "pass_rule_evaluation.yaml").exists()

    next_stage = rpr.determine_post_verdict_route(run_dir, "run_802")

    assert next_stage == "completed_rejected"
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert "pass_rule_evaluation_disagreement" not in state.get("flags", {})


def test_non_binding_discretion_stage_pass_rule_evaluation_ignored(campaign_root):
    """A pass_rule_evaluation.yaml carrying `discretion: stage` (the pass rule
    explicitly deferred the call to the stage) must NOT be treated as binding
    -- the artifact's own fields still drive routing, exactly as before."""
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_803")
    run_dir = runs_dir / "run_803"

    _write_verdict_interpretation(
        run_dir,
        status="kill",
        hypothesis_verdict="kill",
        lineage_routing="terminate",
        hypothesis_family="test_family",
        root_cause={},
    )
    _write_pass_rule_evaluation(
        run_dir,
        result="PASS",
        discretion="stage",
        statement_branch_matched="PASS-discretionary",
        hypothesis_verdict="promote",
        lineage_routing=None,
    )

    next_stage = rpr.determine_post_verdict_route(run_dir, "run_803")

    assert next_stage == "completed_rejected", (
        "discretion:stage must NOT be treated as binding -- the stage's own "
        "kill/terminate call must stand"
    )
