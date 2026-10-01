"""
K2 kernel (A8 + A9 + B11 + C7, C9 rider) regression tests, 2026-07-13.
See engineering/improvements/done/design_and_docs/K2_verdict_machinery_design_20260713.md sections 4-8.

Reuses K4's sandboxing fixtures/helpers directly (campaign_root,
_write_fresh_scaffold, _save_queue_entries, _write_campaign_state) rather
than reimplementing them -- same hermeticity story: workflow/setup_run.py
and the _route_pivot/_scaffold_next_run subprocess call both have ROOTs
that don't compose with tmp_path monkeypatching, so campaign_root's fakes
are reused as-is (see test_k4_routing_registration.py's own module
docstring for the full rationale).

run_057's real protocol_result.yaml is read ONLY (never mutated in place,
never copied into a real-repo-adjacent path) -- its content is loaded into
memory and reused as the evaluator's INPUT; the pre_registration.yaml side
is a freshly-CONSTRUCTED fixture dict (K2's new top-level pass_rule schema,
consistent with _materialize_refinement_run's already-established
top-level-pass_rule convention from K4 -- run_057's OWN real
pre_registration.yaml predates that convention and nests pass_rule under
machine_constraints instead; noted, not treated as a contradiction).
"""
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(WORKFLOW_PATH))
sys.path.insert(0, str(TOOLS_PATH))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

from test_k4_routing_registration import (  # noqa: E402
    campaign_root, _write_fresh_scaffold, _save_queue_entries, _write_campaign_state,
)

REAL_RUN_057_PROTOCOL_RESULT = (
    Path(__file__).parent.parent / "runs" / "run_057" / "artifacts" / "protocol_result.yaml"
)

_PASS_RULE_STATEMENT = (
    "PASS (-> refine/promote routing per verdict-interpreter) iff: (a) gated "
    "bar-level median Sharpe >= 0.5791 (BTCUSDT) AND >= 0.0318 (ETHUSDT), computed "
    "over the same 15-window sets; and (b) per-episode expectancy of taken entries "
    "> 0. FAIL on (a) or (b) -> the gate did not rescue the edge."
)


def _run_057_structured_pre_registration() -> dict:
    """K2-conformant pre_registration.yaml content encoding run_057's REAL,
    pre-registered pass rule (quoted verbatim in the design note section 3)
    in the new top-level pass_rule.criteria/outcomes schema."""
    return {
        "run_id": "run_057",
        "hypothesis_id": "P4_SMA_TREND_LONGONLY_DAILY_ER20GATE",
        "pass_rule": {
            "statement": _PASS_RULE_STATEMENT,
            "window_set_ref": "protocols/ts_trend_daily_v1.json",
            "criteria": [
                {
                    "id": "a", "metric": "median_sharpe", "metric_basis": "bar_level",
                    "comparator": ">=",
                    "per_symbol_threshold": {"BTCUSDT": 0.5791, "ETHUSDT": 0.0318},
                    "null_handling": "fails_threshold",
                },
                {
                    "id": "b", "metric": "per_trade_expectancy_bps", "metric_basis": "episode_level",
                    "comparator": ">", "threshold": 0, "statistic": "mean",
                },
            ],
            "outcomes": [
                {"branch": "PASS", "hypothesis_verdict": "promote", "lineage_routing": None},
                {"branch": "FAIL-a", "hypothesis_verdict": "kill", "lineage_routing": "terminate"},
                {"branch": "FAIL-b", "hypothesis_verdict": "kill", "lineage_routing": "terminate"},
            ],
        },
    }


# ---------------------------------------------------------------------------
# C7 -- known-answer fixture over run_057's REAL protocol_result.yaml
# ---------------------------------------------------------------------------

def test_c7_run_057_known_answer_fail_a_kill_terminate():
    assert REAL_RUN_057_PROTOCOL_RESULT.exists(), "run_057's real protocol_result.yaml is missing"
    protocol_result = yaml.safe_load(REAL_RUN_057_PROTOCOL_RESULT.read_text(encoding="utf-8"))
    pre_registration = _run_057_structured_pre_registration()

    # C7-EXT (2026-07-22): the PASS-RULE RESOLUTION semantics this known-answer
    # fixture exists to pin are unchanged, and now live in _resolve_pass_rule.
    # evaluate_pass_rule_criteria() is the gated public entry -- it runs the
    # four verdict preconditions in front of this kernel, and run_057's archived
    # protocol_result.yaml (which predates them) does not satisfy them. That
    # blocking behaviour is asserted separately in
    # test_c7ext_run_057_is_blocked_at_the_public_entry_point below, so the new
    # gate is pinned rather than papered over by this repointing.
    result = vce._resolve_pass_rule(protocol_result, pre_registration)

    assert result["result"] == "FAIL"
    crit_a = next(c for c in result["criteria_results"] if c["id"] == "a")
    assert crit_a["result"] == "FAIL"
    assert "value" in crit_a["per_symbol"]["BTCUSDT"], "BTCUSDT must be PRESENT, not absent/UNTESTED"
    assert crit_a["per_symbol"]["BTCUSDT"]["value"] is None, "BTCUSDT median_sharpe is null (A3.4), not absent"
    assert crit_a["per_symbol"]["BTCUSDT"]["result"] == "FAIL"
    assert crit_a["per_symbol"]["ETHUSDT"]["value"] == -0.686
    assert crit_a["per_symbol"]["ETHUSDT"]["result"] == "FAIL"

    crit_b = next(c for c in result["criteria_results"] if c["id"] == "b")
    assert crit_b["result"] == "PASS"
    assert crit_b["value"] == pytest.approx(433.7313)

    assert result["branches_failed"] == ["FAIL-a"]
    assert result["statement_branch_matched"] == "FAIL-a"
    assert result["hypothesis_verdict"] == "kill"
    assert result["lineage_routing"] == "terminate"


def test_c7_window_set_ref_mismatch_refuses_evaluation():
    """A3 (K2 Phase B amendment): name-level window_set_ref check."""
    protocol_result = yaml.safe_load(REAL_RUN_057_PROTOCOL_RESULT.read_text(encoding="utf-8"))
    pre_registration = _run_057_structured_pre_registration()
    pre_registration["pass_rule"]["window_set_ref"] = "protocols/some_other_protocol_v2.json"

    result = vce._resolve_pass_rule(protocol_result, pre_registration)  # C7-EXT: see above
    assert result["result"] == "SPEC_ERROR"
    assert "some_other_protocol_v2.json" in result["reason"]
    assert "ts_trend_daily_v1.json" in result["reason"]


def test_c7ext_run_057_is_blocked_at_the_public_entry_point():
    """C7-EXT companion to the known-answer fixture above. run_057's archived
    artifacts predate the verdict preconditions and do not satisfy them, so the
    gated public entry point must refuse to issue ANY verdict — including the
    kill/terminate the kernel itself still resolves. Pinned explicitly so the
    repointing of the two tests above cannot quietly hide the new gate."""
    protocol_result = yaml.safe_load(REAL_RUN_057_PROTOCOL_RESULT.read_text(encoding="utf-8"))
    result = vce.evaluate_pass_rule_criteria(
        protocol_result, _run_057_structured_pre_registration())

    assert result["result"] == "VERDICT_BLOCKED"
    assert result.get("hypothesis_verdict") is None
    assert "deployable_today" in result["blocked_by"]


# ---------------------------------------------------------------------------
# R3 -- legacy_not_evaluable hardening (never raises)
#
# C7-EXT: R3's contract is about the RESOLUTION kernel never raising on a
# legacy-shaped pass_rule, so these exercise _resolve_pass_rule directly. The
# public entry point's precondition gate sits in front of it and is covered by
# tests/test_c7ext_verdict_gates.py (G5).
# ---------------------------------------------------------------------------

def test_r3_string_shaped_pass_rule_never_raises():
    protocol_result = {"per_symbol_summary": {}}
    pre_registration = {"pass_rule": _PASS_RULE_STATEMENT}  # run_057's OWN real shape
    result = vce._resolve_pass_rule(protocol_result, pre_registration)
    assert result["result"] == "legacy_not_evaluable"
    assert "reason" in result


def test_r3_absent_pass_rule_never_raises():
    result = vce._resolve_pass_rule({}, {})
    assert result["result"] == "legacy_not_evaluable"


def test_r3_non_string_non_dict_pass_rule_never_raises():
    result = vce._resolve_pass_rule({}, {"pass_rule": 12345})
    assert result["result"] == "legacy_not_evaluable"


# ---------------------------------------------------------------------------
# B11 -- materialization-time total-mapping lint
# ---------------------------------------------------------------------------

def test_b11_lint_rejects_unmapped_fail_branch_naming_it():
    """A registered branch (FAIL-b) missing its verdict+routing pair, with
    no discretion opt-in, must be rejected BY NAME."""
    pre_registration = _run_057_structured_pre_registration()
    pre_registration["pass_rule"]["outcomes"][2]["hypothesis_verdict"] = None
    pre_registration["pass_rule"]["outcomes"][2]["lineage_routing"] = None
    violations, _ = rpr._lint_pass_rule_total_mapping(pre_registration)
    assert violations, "an outcomes branch missing both fields (no discretion opt-in) must be rejected"
    assert any("FAIL-b" in v for v in violations), "the violation must name the specific branch"


def test_b11_lint_accepts_total_mapping():
    pre_registration = _run_057_structured_pre_registration()
    violations, warnings = rpr._lint_pass_rule_total_mapping(pre_registration)
    assert violations == [], violations


def test_b11_lint_rejects_promote_with_non_null_routing():
    pre_registration = _run_057_structured_pre_registration()
    pre_registration["pass_rule"]["outcomes"][0]["lineage_routing"] = "refine"  # PASS branch
    violations, _ = rpr._lint_pass_rule_total_mapping(pre_registration)
    assert violations
    assert any("promote" in v.lower() and "lineage_routing" in v for v in violations)


def test_b11_lint_warns_on_differing_fail_pairs():
    """A1 (operator amendment): multiple FAIL branches with DIFFERING pairs -> WARNING."""
    pre_registration = _run_057_structured_pre_registration()
    pre_registration["pass_rule"]["outcomes"][2]["lineage_routing"] = "pivot"  # FAIL-b now differs from FAIL-a
    violations, warnings = rpr._lint_pass_rule_total_mapping(pre_registration)
    assert violations == [], "differing pairs is a WARNING, never a rejection"
    assert any("DIFFERING" in w for w in warnings)


def test_b11_lint_skips_legacy_string_pass_rule():
    pre_registration = {"pass_rule": _PASS_RULE_STATEMENT}
    violations, warnings = rpr._lint_pass_rule_total_mapping(pre_registration)
    assert violations == [] and warnings == []


def test_b11_lint_wired_into_refinement_brief_materialization(campaign_root):
    """The lint actually blocks materialization end-to-end via
    _materialize_refinement_run, not just as a standalone function."""
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_900")
    briefs_dir = root / "briefs"
    briefs_dir.mkdir()
    brief_path = briefs_dir / "bad_refinement.yaml"
    bad_brief = {
        "brief_id": "BAD_REFINEMENT",
        "lineage": {"parent_queue_entry": "X", "parent_run": "run_900",
                    "relation": "refine", "parent_verdict": "refine"},
        "hypothesis": {"primary": "test"},
        "gate_definition": {"indicator": "test"},
        "evaluation": {
            "pass_rule": {
                "statement": "PASS iff x.",
                "criteria": [{"id": "a", "metric": "median_sharpe", "metric_basis": "bar_level",
                              "comparator": ">=", "per_symbol_threshold": {"BTCUSDT": 0.1},
                              "null_handling": "fails_threshold"}],
                "outcomes": [{"branch": "PASS", "hypothesis_verdict": "promote", "lineage_routing": "refine"}],
                # PASS branch has an invalid non-null routing -- must be rejected.
            },
        },
    }
    brief_path.write_text(yaml.safe_dump(bad_brief, sort_keys=False), encoding="utf-8")

    with pytest.raises(ValueError, match="B11 total-mapping lint"):
        camp._materialize_refinement_run("run_901", bad_brief, brief_path)
    assert not (runs_dir / "run_901" / "artifacts" / "pre_registration.yaml").exists()
    assert not (runs_dir / "run_901" / "artifacts" / "user_brief_verbatim.yaml").exists()


# ---------------------------------------------------------------------------
# A9 -- _route_kill (per-hypothesis) vs _route_campaign_terminate (campaign-wide)
# ---------------------------------------------------------------------------

def test_a9_route_kill_leaves_campaign_status_untouched_and_second_entry_schedulable(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_100")
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_100"], status="active")
    _save_queue_entries(campaign_root["queue_path"], [
        {"id": "ENTRY_A", "brief_path": "briefs/a.yaml", "status": "in_progress",
         "priority": 1, "run_ids": ["run_100"], "outcome": None},
        {"id": "ENTRY_B", "brief_path": "briefs/b.yaml", "status": "ready",
         "priority": 2, "run_ids": [], "outcome": None},
    ])

    interp = {"primary_failure_mode": "no edge", "hypothesis_family": "test_family"}
    next_stage = rpr._route_kill(runs_dir / "run_100", "run_100", interp, {})

    assert next_stage == "completed_rejected"
    campaign_state = yaml.safe_load(campaign_root["campaign_state_path"].read_text(encoding="utf-8"))
    assert campaign_state.get("status") == "active", "campaign_state.status must be untouched by a per-hypothesis kill"
    assert not (root / "campaign_decision.yaml").exists(), "no campaign-wide decision file from a per-hypothesis kill"

    queue = camp._load_queue()
    entry = camp._select_entry(queue["queue"])
    # ENTRY_A is still "in_progress" in the fixture queue (this test drives
    # _route_kill directly, not the full process_once() flow, so the queue
    # entry's own status update is out of scope here) -- what matters is
    # ENTRY_B remains independently schedulable regardless.
    assert any(e["id"] == "ENTRY_B" and e["status"] == "ready" for e in queue["queue"])


def test_a9_route_campaign_terminate_writes_campaign_wide_decision(campaign_root):
    root = campaign_root["root"]
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_200"], status="active")
    review = {"recommendation": "terminate", "recommendation_rationale": "search space exhausted"}

    next_stage = rpr._route_campaign_terminate(
        campaign_root["runs_dir"] / "run_200", "run_200", review,
        rpr.load_campaign_state(),
    )

    assert next_stage == "completed_rejected"
    assert (root / "campaign_decision.yaml").exists(), "campaign-wide decision IS expected here (explicit terminate)"
    campaign_state = yaml.safe_load(campaign_root["campaign_state_path"].read_text(encoding="utf-8"))
    assert campaign_state["status"] == "space_empty"


# ---------------------------------------------------------------------------
# A8 -- verdict/routing split: separately auditable, correct scaffold count
# ---------------------------------------------------------------------------

def test_a8_kill_plus_terminate_produces_no_scaffold(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_300")
    vi_path = runs_dir / "run_300" / "artifacts" / "verdict_interpretation.yaml"
    vi_path.write_text(yaml.safe_dump({
        "hypothesis_id": "TEST", "hypothesis_verdict": "kill", "lineage_routing": "terminate",
        "primary_failure_mode": "no edge",
    }), encoding="utf-8")
    interp = yaml.safe_load(vi_path.read_text(encoding="utf-8"))

    next_stage = rpr._dispatch_verdict_route(
        runs_dir / "run_300", "run_300", interp, {}, "kill", "terminate"
    )

    assert next_stage == "completed_rejected"
    on_disk_after = {p.name for p in runs_dir.iterdir() if p.is_dir()}
    assert on_disk_after == {"run_300"}, "kill+terminate must scaffold nothing"

    reread = yaml.safe_load(vi_path.read_text(encoding="utf-8"))
    assert reread["hypothesis_verdict"] == "kill"
    assert reread["lineage_routing"] == "terminate"
    assert reread["hypothesis_verdict"] != reread["lineage_routing"], (
        "the two fields must remain independently meaningful, not collapsed into one"
    )


def test_a8_kill_plus_pivot_produces_exactly_one_scaffold(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_400")
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_400"])
    vi_path = runs_dir / "run_400" / "artifacts" / "verdict_interpretation.yaml"
    vi_path.write_text(yaml.safe_dump({
        "hypothesis_id": "TEST", "hypothesis_verdict": "kill", "lineage_routing": "pivot",
        "hypothesis_family": "test_family_exhausted",
        "primary_failure_mode": "mechanism falsified, pivot to a different family",
    }), encoding="utf-8")
    interp = yaml.safe_load(vi_path.read_text(encoding="utf-8"))

    next_stage = rpr._dispatch_verdict_route(
        runs_dir / "run_400", "run_400", interp, {}, "kill", "pivot"
    )

    assert next_stage == "completed_refined"
    on_disk_after = {p.name for p in runs_dir.iterdir() if p.is_dir()}
    assert on_disk_after == {"run_400", "run_401"}, "kill+pivot must scaffold EXACTLY one child"

    reread = yaml.safe_load(vi_path.read_text(encoding="utf-8"))
    assert reread["hypothesis_verdict"] == "kill"
    assert reread["lineage_routing"] == "pivot"

    parent_state = yaml.safe_load((runs_dir / "run_400" / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert parent_state["continuation_child"] == "run_401"


# ---------------------------------------------------------------------------
# C9 -- KB exhaustion gate on refine/pivot's own proposal paths
# ---------------------------------------------------------------------------

_PLURAL_KELTNER_SHAPED_FINDING = {
    "id": "kb_finding_007",  # deliberately NOT a substring of its own hypothesis_ids
    "mechanism": "Keltner mean-reversion in TRENDING regime (ER>=0.50)",
    "hypothesis_ids": ["keltner_mean_reversion", "keltner_trend_mean_reversion"],
    "outcome": "no_edge_observed",
    "exhausted": True,
    # D-055: only a ban blocks (evidence_count >= 3 or an approved veto); these C9
    # tests check matching and the pause, so the fixture is a ban.
    "evidence_count": 3,
    "reactivation_condition": None,
}


def test_c9_matches_via_plural_hypothesis_ids_list_member():
    kb = {"findings": [_PLURAL_KELTNER_SHAPED_FINDING]}
    violations = rpr._check_kb_reactivation_conformance(
        {"research_goal": "Let's pivot to keltner_mean_reversion next."}, kb
    )
    assert violations, "must match a plural hypothesis_ids list member"
    assert any("keltner_mean_reversion" in v for v in violations)


def test_c9_id_string_alone_does_not_falsely_match():
    """Proves the match is on hypothesis_ids' actual members, not a looser
    substring coincidence against the finding's own id."""
    kb = {"findings": [_PLURAL_KELTNER_SHAPED_FINDING]}
    violations = rpr._check_kb_reactivation_conformance(
        {"research_goal": "Let's look at kb_finding_007's methodology."}, kb
    )
    assert violations == [], "the finding's own id string must not match by itself"


def test_c9_pivot_route_pauses_before_scaffold_no_child_directory(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_500")
    kb_path = root / "campaign_knowledge_base.yaml"
    kb_path.write_text(yaml.safe_dump({"findings": [_PLURAL_KELTNER_SHAPED_FINDING]}), encoding="utf-8")

    interp = {
        "hypothesis_family": "keltner_mean_reversion",
        "primary_failure_mode": "pivot to keltner_mean_reversion breakout next",
        "config_to_failure_map": "",
        "root_cause": {"supporting_evidence": ""},
    }
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(rpr, "_KB_PATH", kb_path)
        next_stage = rpr._route_pivot(runs_dir / "run_500", "run_500", interp, {})

    assert next_stage == "human_pause"
    on_disk_after = {p.name for p in runs_dir.iterdir() if p.is_dir()}
    assert on_disk_after == {"run_500"}, "no child directory must be scaffolded when the gate fires"

    state = yaml.safe_load((runs_dir / "run_500" / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state.get("flags", {}).get("kb_reactivation_violation") is True
    assert state.get("kb_reactivation_violations")


def test_c9_refine_route_pauses_before_scaffold_no_child_directory(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_600")
    kb_path = campaign_root["root"] / "campaign_knowledge_base.yaml"
    kb_path.write_text(yaml.safe_dump({"findings": [_PLURAL_KELTNER_SHAPED_FINDING]}), encoding="utf-8")

    proposed_path = runs_dir / "run_600" / "artifacts" / "proposed_brief.yaml"
    proposed_path.write_text(yaml.safe_dump({
        "strategy_domain": "test", "timeframe": "1h",
        "research_goal": "Refine toward keltner_trend_mean_reversion parameters.",
    }), encoding="utf-8")
    interp = {"proposed_change_dimension": "threshold", "hypothesis_family": "keltner_family"}

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(rpr, "_KB_PATH", kb_path)
        next_stage = rpr._route_refine(runs_dir / "run_600", "run_600", interp, {})

    assert next_stage == "human_pause"
    on_disk_after = {p.name for p in runs_dir.iterdir() if p.is_dir()}
    assert on_disk_after == {"run_600"}, "no child directory must be scaffolded when the gate fires"
    state = yaml.safe_load((runs_dir / "run_600" / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state.get("flags", {}).get("kb_reactivation_violation") is True


# ---------------------------------------------------------------------------
# K2 rider (2026-07-13) -- pair validation (closes K2 Phase B deviation 3)
# and the holdout-path guard test (regression for deviation 2's fix)
# ---------------------------------------------------------------------------

def test_pair_validation_rejects_incoherent_pair_naming_both_values():
    with pytest.raises(ValueError) as exc_info:
        rpr._dispatch_verdict_route(Path("."), "run_x", {}, {}, "refine", "terminate")
    msg = str(exc_info.value)
    assert "refine" in msg, "the error must name the hypothesis_verdict value"
    assert "terminate" in msg, "the error must name the lineage_routing value"


@pytest.mark.parametrize("hypothesis_verdict,lineage_routing", [
    ("promote", "pivot"),
    ("refine", "pivot"),
    ("refine", "escalate"),
    ("promote", "refine"),
    ("kill", None),
    ("bogus", "refine"),
])
def test_pair_validation_rejects_every_other_incoherent_combination(hypothesis_verdict, lineage_routing):
    with pytest.raises(ValueError) as exc_info:
        rpr._dispatch_verdict_route(Path("."), "run_x", {}, {}, hypothesis_verdict, lineage_routing)
    msg = str(exc_info.value)
    assert str(hypothesis_verdict) in msg and str(lineage_routing) in msg


def test_pair_validation_accepts_kill_terminate(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_800")
    interp = {"primary_failure_mode": "no edge", "hypothesis_family": "f"}
    next_stage = rpr._dispatch_verdict_route(runs_dir / "run_800", "run_800", interp, {}, "kill", "terminate")
    assert next_stage == "completed_rejected"


def test_pair_validation_accepts_kill_pivot(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_801")
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_801"])
    interp = {"hypothesis_family": "f", "primary_failure_mode": "dead, pivot"}
    next_stage = rpr._dispatch_verdict_route(runs_dir / "run_801", "run_801", interp, {}, "kill", "pivot")
    assert next_stage == "completed_refined"
    assert (runs_dir / "run_802").exists()


def test_pair_validation_accepts_kill_escalate(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_803")
    (root / "protocols").mkdir(exist_ok=True)
    (root / "protocols" / "baseline_v1.json").write_text(
        '{"symbols": ["BTCUSDT"], "timeframe": "1h", "windows": []}', encoding="utf-8"
    )
    (root / "config").mkdir(exist_ok=True)
    (root / "config" / "coin_universe.yaml").write_text(yaml.safe_dump({
        "escalation_order": {"sequence": [{"category": "majors", "priority": 1}]},
        "categories": {"majors": {"coins": [{"symbol": "ETHUSDT", "data_cached": True}],
                                   "strategy_affinity": []}},
    }), encoding="utf-8")
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_803"])
    next_stage = rpr._dispatch_verdict_route(runs_dir / "run_803", "run_803", {}, {}, "kill", "escalate")
    assert next_stage == "completed_escalated"
    assert (runs_dir / "run_804").exists()


def test_pair_validation_accepts_refine_refine(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_805")
    (runs_dir / "run_805" / "artifacts" / "proposed_brief.yaml").write_text(
        yaml.safe_dump({"strategy_domain": "test", "timeframe": "1h", "research_goal": "refine test"}),
        encoding="utf-8",
    )
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_805"])
    interp = {"proposed_change_dimension": "threshold", "hypothesis_family": "f"}
    next_stage = rpr._dispatch_verdict_route(runs_dir / "run_805", "run_805", interp, {}, "refine", "refine")
    assert next_stage == "completed_refined"
    assert (runs_dir / "run_806").exists()


def test_pair_validation_accepts_promote_null(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_807")
    (runs_dir / "run_807" / "artifacts" / "verdict_interpretation.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "TEST", "hypothesis_verdict": "promote", "lineage_routing": None}),
        encoding="utf-8",
    )
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_807"], trial_sharpes=[])
    next_stage = rpr._dispatch_verdict_route(runs_dir / "run_807", "run_807", {}, {}, "promote", None)
    assert next_stage == "holdout_evaluation"
    assert (runs_dir / "run_807" / "artifacts" / "promotion_audit.yaml").exists()


def test_holdout_path_guard_campaign_review_continue_promote_reaches_holdout_gate(campaign_root):
    """Regression for K2 Phase B deviation 2: the campaign-review
    continue-branch's promote path must reach the SAME holdout-gated flow
    as the primary dispatch (_write_promotion_audit + holdout_evaluation),
    never the old bare 'completed_promoted' bypass that skipped it."""
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_700")
    run_dir = runs_dir / "run_700"
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(yaml.safe_dump({
        "hypothesis_id": "TEST_PROMOTE", "hypothesis_verdict": "promote", "lineage_routing": None,
        "status": "promote",
    }), encoding="utf-8")
    (run_dir / "artifacts" / "campaign_review.yaml").write_text(yaml.safe_dump({
        "recommendation": "continue",
    }), encoding="utf-8")
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_700"], trial_sharpes=[])

    next_stage = rpr.determine_post_campaign_review_route(run_dir, "run_700")

    assert next_stage == "holdout_evaluation", (
        "must reach the holdout-gated flow, not 'completed_promoted' (the closed bypass)"
    )
    assert (run_dir / "artifacts" / "promotion_audit.yaml").exists(), (
        "promotion_audit.yaml must be written before holdout_evaluation, same as the primary dispatch"
    )
