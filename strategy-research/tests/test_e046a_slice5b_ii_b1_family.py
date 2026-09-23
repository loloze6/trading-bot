"""
E-046a Slice 5b-ii-B1: operator decisions 4 and 5 of
engineering/roadmap/E-046a/S1_FINDINGS_5B_II.md ("Decision (operator,
2026-09-23, second round -- for 5b-ii-B)").

  Task 1 -- hypothesis `family` set once at idea creation, inherited on refine
    (orchestrator.family_at_creation.enabled, off by default):
      * the validator (_hypothesis_family_problem) and its parity with both schemas
      * the flag reader (fail loud on non-bool)
      * flag-off byte-identity: hypothesis_generation's handoff/prompt, the
        post-stage check, _route_refine's child, the refinement-brief child, the
        multi-card split
      * flag-on: FAMILY_FIELD.md reaches the prompt; fresh cards must carry a
        valid family; refine children (all three creation paths) inherit the
        parent's family IN CODE even when the child's LLM wrote another one;
        legacy parents without a family do not break refine
      * _synthesize_verdict reads the family from the card and fails closed
  Task 2 -- primary_failure_mode / reactivation_trigger rebuilt mechanically on
    every decided_by path, their fit to the existing consumers
    (near_miss_scoreboard bucketing, KB reactivation parsing), schema
    enforcement incl. smuggled/unknown values.

Every fixture is hand-built in tmp_path; no LLM, no real run directory.
"""
import copy
import inspect
import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

jsonschema = pytest.importorskip("jsonschema")

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import build_reports  # noqa: E402
import near_miss_scoreboard  # noqa: E402
import anti_adjacency_gate  # noqa: E402
# Reuse the K4 sandbox (fake setup_run / fake setup_run.py subprocess) rather
# than re-deriving it; importing the fixture makes it available here.
from test_k4_routing_registration import (  # noqa: E402,F401
    campaign_root, _write_fresh_scaffold, _write_campaign_state, _save_queue_entries,
    _write_refinement_brief,
)
# The 5b-ii-A fixture builders -- same run shape, so both suites stay in step.
from test_e046a_slice5b_ii_a_synthesis import (  # noqa: E402
    _protocol_result, _detector_report, _proposal, _binding, _assert_valid, VALIDATOR, SCHEMA,
)

HYP_SCHEMA = json.loads((SR_ROOT / "workflow_artifacts" / "schemas" / "hypothesis_card.schema.json")
                        .read_text(encoding="utf-8"))
FAMILY_FIELD_MD = SR_ROOT / "workflow_artifacts" / "skills" / "hypothesis-design" / "FAMILY_FIELD.md"
HYP_SKILL_MD = SR_ROOT / "workflow_artifacts" / "skills" / "hypothesis-design" / "SKILL.md"
FAM = "keltner_breakout"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _set_flag(value):
    """Write orchestrator.family_at_creation.enabled into whatever ROOT the
    active sandbox (autouse or campaign_root) points rpr at. value=None ->
    no config file at all."""
    cfg = rpr.ROOT / "config" / "campaign_config.yaml"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    if value is None:
        if cfg.exists():
            cfg.unlink()
        return
    cfg.write_text(yaml.safe_dump({"orchestrator": {"family_at_creation": {"enabled": value}}}),
                   encoding="utf-8")


def _card(run_dir: Path, **fields):
    art = run_dir / "artifacts"
    art.mkdir(parents=True, exist_ok=True)
    data = {"hypothesis_id": "H-TEST-1", "thesis": "t"}
    data.update(fields)
    path = art / "hypothesis_card.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def _read(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _state(run_dir: Path) -> dict:
    return _read(run_dir / "pipeline_state.yaml")


def _make_run(tmp_path, *, family=FAM, protocol=None, pass_rule=None, proposals=None,
              raw_proposals=None, state=None):
    art = tmp_path / "run" / "artifacts"
    art.mkdir(parents=True)
    card = {"hypothesis_id": "H-TEST-1"}
    if family is not _ABSENT:
        card["family"] = family
    (art / "hypothesis_card.yaml").write_text(yaml.safe_dump(card), encoding="utf-8")
    (art / "protocol_result.yaml").write_text(
        yaml.safe_dump(protocol if protocol is not None else _protocol_result()), encoding="utf-8")
    if pass_rule is not None:
        (art / "pass_rule_evaluation.yaml").write_text(yaml.safe_dump(pass_rule), encoding="utf-8")
    if proposals is not None or raw_proposals is not None:
        (art / "proposals").mkdir()
    for cat, items in (proposals or {}).items():
        (art / "proposals" / f"{cat}.yaml").write_text(yaml.safe_dump(items), encoding="utf-8")
    for name, text in (raw_proposals or {}).items():
        (art / "proposals" / name).write_text(text, encoding="utf-8")
    if state is not None:
        (tmp_path / "run" / "pipeline_state.yaml").write_text(
            state if isinstance(state, str) else yaml.safe_dump(state), encoding="utf-8")
    return tmp_path / "run"


_ABSENT = object()


def _synth(run_dir, report="default"):
    return rpr._synthesize_verdict(run_dir, _detector_report() if report == "default" else report)


# ===========================================================================
# Task 1a -- the validator
# ===========================================================================

@pytest.mark.parametrize("value", ["keltner_breakout", "a", "rsi2", "funding_rate_mean_reversion",
                                   "x" * 48, "fg_2_contrarian"])
def test_valid_family_labels(value):
    assert rpr._hypothesis_family_problem(value) is None


@pytest.mark.parametrize("value", [None, "", " ", " keltner", "keltner ", "Keltner", "keltner-breakout",
                                   "keltner breakout", "keltner__breakout", "_keltner", "keltner_",
                                   "1keltner", "keltner\n", "x" * 49, 123, True, ["keltner"],
                                   {"f": 1}, "kéltner"])
def test_invalid_family_labels_are_rejected_never_normalised(value):
    assert rpr._hypothesis_family_problem(value) is not None


def test_family_rule_is_identical_in_code_and_both_schemas():
    """One rule, three places: the code validator, hypothesis_card.schema.json
    (where the field is authored) and verdict_synthesis.schema.json (where it
    is copied). Drift between them would let a label pass one gate and fail
    another."""
    hyp = HYP_SCHEMA["properties"]["family"]
    syn = SCHEMA["properties"]["hypothesis_family"]
    code_pattern = rpr.HYPOTHESIS_FAMILY_RE.pattern.replace("(?:", "(")
    assert hyp["pattern"] == syn["pattern"] == code_pattern
    assert hyp["maxLength"] == syn["maxLength"] == rpr.HYPOTHESIS_FAMILY_MAX_LEN
    # family is optional on the card (legacy cards stay valid), never required
    assert "family" not in HYP_SCHEMA["required"]
    validator = jsonschema.Draft7Validator({"type": "object", "properties": {"family": hyp}})
    for good in ("keltner_breakout", "a1_b2"):
        assert not list(validator.iter_errors({"family": good}))
    for bad in ("", "Keltner", "keltner__x", "x" * 49):
        assert list(validator.iter_errors({"family": bad})), bad


# ===========================================================================
# Task 1b -- the flag reader
# ===========================================================================

def test_flag_defaults_off_when_config_absent_or_key_missing():
    _set_flag(None)
    assert rpr._family_at_creation_enabled() is False
    (rpr.ROOT / "config" / "campaign_config.yaml").write_text(
        yaml.safe_dump({"orchestrator": {}}), encoding="utf-8")
    assert rpr._family_at_creation_enabled() is False


def test_flag_on_off():
    _set_flag(True)
    assert rpr._family_at_creation_enabled() is True
    _set_flag(False)
    assert rpr._family_at_creation_enabled() is False


@pytest.mark.parametrize("bad", ["true", "false", None, 1, 0])
def test_flag_non_bool_fails_loud(bad):
    (rpr.ROOT / "config" / "campaign_config.yaml").write_text(
        yaml.safe_dump({"orchestrator": {"family_at_creation": {"enabled": bad}}}), encoding="utf-8")
    with pytest.raises(ValueError, match="family_at_creation"):
        rpr._family_at_creation_enabled()


@pytest.mark.real_repo_readonly
def test_shipped_config_is_off_and_registered():
    cfg = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["family_at_creation"]["enabled"] is False
    reg = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml").read_text(encoding="utf-8"))
    entry = [f for f in reg["flags"] if f["name"] == "family_at_creation"]
    assert len(entry) == 1
    assert entry[0]["config_key"] == "orchestrator.family_at_creation.enabled"
    assert entry[0]["reader"] == "run_phase1_research._family_at_creation_enabled"
    assert entry[0]["state"] == "off_incomplete" and entry[0]["blocked_on"]
    assert hasattr(rpr, "_family_at_creation_enabled")


# ===========================================================================
# Task 1c -- prompt injection (flag-off byte identity / flag-on content)
# ===========================================================================

def _prompt_tree(tmp_path):
    """A throwaway strategy-research-shaped tree: CWD-relative SKILL.md (what
    _build_stage_prompt reads) + the ../../ relative FAMILY_FIELD.md."""
    root = tmp_path / "tree"
    skill_dir = root / "workflow_artifacts" / "skills" / "hypothesis-design"
    skill_dir.mkdir(parents=True)
    shutil.copyfile(HYP_SKILL_MD, skill_dir / "SKILL.md")
    shutil.copyfile(FAMILY_FIELD_MD, skill_dir / "FAMILY_FIELD.md")
    run_dir = root / "runs" / "run_900"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "research_brief.yaml").write_text("research_goal: x\n", encoding="utf-8")
    (run_dir / "pipeline_state.yaml").write_text(yaml.safe_dump({"run_id": "run_900"}), encoding="utf-8")
    handoff = {"required_inputs": [{"path": "artifacts/research_brief.yaml", "reason": "brief"}],
               "deliverables": ["hypothesis_card.yaml"],
               "injected_context": {"stage_attempt": "0"}}
    return root, run_dir, handoff


@pytest.mark.parametrize("flag", [None, False])
@pytest.mark.parametrize("stage", ["hypothesis_generation", "innovation_expansion", "validation"])
def test_flag_off_handoff_and_prompt_byte_identical(tmp_path, monkeypatch, flag, stage):
    _set_flag(flag)
    root, run_dir, handoff = _prompt_tree(tmp_path)
    rpr.update_state(path=run_dir, inherited_hypothesis_family=FAM)  # even with a marker present
    before = copy.deepcopy(handoff)
    rpr._apply_family_at_creation_context(stage, handoff, run_dir)
    assert handoff == before
    if stage == "hypothesis_generation":
        monkeypatch.chdir(root)
        assert rpr._build_stage_prompt(stage, handoff, run_dir) == \
            rpr._build_stage_prompt(stage, before, run_dir)
        assert "FAMILY_FIELD" not in rpr._build_stage_prompt(stage, handoff, run_dir)


def test_skill_md_itself_does_not_mention_the_family_field():
    """The flag-off byte-identity rests on SKILL.md being untouched; the rules
    live only in FAMILY_FIELD.md."""
    text = HYP_SKILL_MD.read_text(encoding="utf-8")
    assert "FAMILY_FIELD" not in text and "family_at_creation" not in text


def test_flag_on_injects_family_rules_into_the_prompt(tmp_path, monkeypatch):
    _set_flag(True)
    root, run_dir, handoff = _prompt_tree(tmp_path)
    rpr._apply_family_at_creation_context("hypothesis_generation", handoff, run_dir)
    paths = [r["path"] for r in handoff["required_inputs"]]
    assert paths.count(rpr._FAMILY_FIELD_INSTRUCTIONS_PATH) == 1
    assert rpr._INHERITED_FAMILY_STATE_KEY not in handoff["injected_context"]  # fresh idea
    rpr._apply_family_at_creation_context("hypothesis_generation", handoff, run_dir)  # idempotent
    assert [r["path"] for r in handoff["required_inputs"]].count(rpr._FAMILY_FIELD_INSTRUCTIONS_PATH) == 1
    monkeypatch.chdir(root)
    prompt = rpr._build_stage_prompt("hypothesis_generation", handoff, run_dir)
    assert FAMILY_FIELD_MD.read_text(encoding="utf-8").strip()[:200] in prompt


def test_flag_on_refine_child_gets_inherited_family_in_injected_context(tmp_path):
    _set_flag(True)
    _, run_dir, handoff = _prompt_tree(tmp_path)
    rpr.update_state(path=run_dir, inherited_hypothesis_family=FAM)
    rpr._apply_family_at_creation_context("hypothesis_generation", handoff, run_dir)
    assert handoff["injected_context"][rpr._INHERITED_FAMILY_STATE_KEY] == FAM
    assert handoff["injected_context"]["stage_attempt"] == "0"  # merged, not replaced


def test_flag_on_other_stages_untouched(tmp_path):
    _set_flag(True)
    _, run_dir, handoff = _prompt_tree(tmp_path)
    before = copy.deepcopy(handoff)
    for stage in ("innovation_expansion", "validation", "verdict_interpreter", "campaign_review"):
        rpr._apply_family_at_creation_context(stage, handoff, run_dir)
    assert handoff == before


def test_helpers_are_wired_at_their_call_sites():
    """Static guard: the injector runs in async_invoke_agent and the check runs
    after hypothesis_generation in run_loop."""
    assert "_apply_family_at_creation_context(stage_name, handoff, RUN_DIR)" in \
        inspect.getsource(rpr.async_invoke_agent)
    loop_src = inspect.getsource(rpr.run_loop)
    assert 'if current_stage == "hypothesis_generation":\n                _enforce_hypothesis_family(RUN_DIR)' \
        in loop_src
    assert "inherited_family = _family_to_inherit(path)" in inspect.getsource(rpr._route_refine)
    assert "orch._family_to_inherit(" in inspect.getsource(camp.process_once)


# ===========================================================================
# Task 1d -- creation-time check (_enforce_hypothesis_family)
# ===========================================================================

@pytest.mark.parametrize("flag", [None, False])
@pytest.mark.parametrize("fields", [{}, {"family": ""}, {"family": "Not Valid"}, {"family": FAM}])
def test_flag_off_check_is_a_noop(tmp_path, flag, fields):
    """Legacy behaviour: whatever the card says (or omits) is left exactly as is."""
    _set_flag(flag)
    run = tmp_path / "run"
    path = _card(run, **fields)
    before = path.read_bytes()
    rpr._enforce_hypothesis_family(run)
    assert path.read_bytes() == before


def test_flag_on_fresh_valid_family_is_left_untouched(tmp_path):
    _set_flag(True)
    run = tmp_path / "run"
    path = _card(run, family=FAM)
    before = path.read_bytes()
    rpr._enforce_hypothesis_family(run)
    assert path.read_bytes() == before


@pytest.mark.parametrize("fields", [{}, {"family": ""}, {"family": None}, {"family": "Keltner Breakout"},
                                    {"family": " keltner"}, {"family": ["keltner"]}],
                         ids=["missing", "empty", "null", "spaces_caps", "leading_space", "list"])
def test_flag_on_fresh_bad_family_fails_closed(tmp_path, fields):
    _set_flag(True)
    run = tmp_path / "run"
    path = _card(run, **fields)
    before = path.read_bytes()
    with pytest.raises(ValueError, match="E-046a family"):
        rpr._enforce_hypothesis_family(run)
    assert path.read_bytes() == before  # never silently repaired


def test_flag_on_missing_card_fails_closed(tmp_path):
    _set_flag(True)
    (tmp_path / "run" / "artifacts").mkdir(parents=True)
    with pytest.raises(ValueError):
        rpr._enforce_hypothesis_family(tmp_path / "run")


@pytest.mark.parametrize("fields", [{}, {"family": "keltner_threshold_regime"}, {"family": ""},
                                    {"family": "Bad Label"}],
                         ids=["llm_omitted", "llm_different_valid", "llm_empty", "llm_malformed"])
def test_flag_on_refine_child_family_is_overwritten_in_code(tmp_path, fields):
    _set_flag(True)
    run = tmp_path / "run"
    path = _card(run, thesis="kept", **fields)
    (run / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"run_id": "run", rpr._INHERITED_FAMILY_STATE_KEY: FAM}), encoding="utf-8")
    rpr._enforce_hypothesis_family(run)
    card = _read(path)
    assert card["family"] == FAM
    assert card["thesis"] == "kept" and card["hypothesis_id"] == "H-TEST-1"


def test_flag_on_refine_child_matching_family_not_rewritten(tmp_path):
    _set_flag(True)
    run = tmp_path / "run"
    path = _card(run, family=FAM)
    (run / "pipeline_state.yaml").write_text(
        yaml.safe_dump({rpr._INHERITED_FAMILY_STATE_KEY: FAM}), encoding="utf-8")
    before = path.read_bytes()
    rpr._enforce_hypothesis_family(run)
    assert path.read_bytes() == before


@pytest.mark.parametrize("marker", ["", None, "Bad Label"])
def test_flag_on_corrupt_inheritance_marker_fails_closed(tmp_path, marker):
    _set_flag(True)
    run = tmp_path / "run"
    _card(run, family=FAM)
    (run / "pipeline_state.yaml").write_text(
        yaml.safe_dump({rpr._INHERITED_FAMILY_STATE_KEY: marker}), encoding="utf-8")
    with pytest.raises(ValueError):
        rpr._enforce_hypothesis_family(run)


# ===========================================================================
# Task 1e -- refine children inherit (all three creation paths)
# ===========================================================================

def _refine_parent(campaign_root, run_id="run_100", **card_fields):
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, run_id)
    run_dir = runs_dir / run_id
    (run_dir / "artifacts" / "proposed_brief.yaml").write_text(
        yaml.safe_dump({"strategy_domain": "test", "timeframe": "1h"}), encoding="utf-8")
    if card_fields is not None:
        _card(run_dir, **card_fields)
    _write_campaign_state(campaign_root["campaign_state_path"], runs=[run_id])
    return run_dir


# the LLM verdict re-invents the label -- exactly the legacy failure mode
_LLM_INTERP = {"proposed_change_dimension": "test_dim", "hypothesis_family": "keltner_threshold_regime"}


def test_route_refine_child_inherits_parent_card_family_not_the_llm_label(campaign_root):
    _set_flag(True)
    parent = _refine_parent(campaign_root, family=FAM)
    assert rpr._route_refine(parent, "run_100", dict(_LLM_INTERP), {}) == "completed_refined"
    child = campaign_root["runs_dir"] / "run_101"
    assert _state(child)[rpr._INHERITED_FAMILY_STATE_KEY] == FAM
    # the child's own LLM hypothesis_generation then writes a different label ...
    card_path = _card(child, family="keltner_threshold_regime")
    rpr._enforce_hypothesis_family(child)
    # ... and code puts the inherited one back.
    assert _read(card_path)["family"] == FAM


def test_route_refine_grandchild_keeps_the_original_family(campaign_root):
    _set_flag(True)
    parent = _refine_parent(campaign_root, family=FAM)
    rpr._route_refine(parent, "run_100", dict(_LLM_INTERP), {})
    child = campaign_root["runs_dir"] / "run_101"
    _card(child, family="something_else")
    rpr._enforce_hypothesis_family(child)
    (child / "artifacts" / "proposed_brief.yaml").write_text("strategy_domain: t\n", encoding="utf-8")
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_100", "run_101"])
    rpr._route_refine(child, "run_101", dict(_LLM_INTERP), {})
    assert _state(campaign_root["runs_dir"] / "run_102")[rpr._INHERITED_FAMILY_STATE_KEY] == FAM


@pytest.mark.parametrize("flag", [None, False])
def test_route_refine_flag_off_child_is_byte_identical_to_a_plain_scaffold(campaign_root, tmp_path, flag):
    _set_flag(flag)
    parent = _refine_parent(campaign_root, family=FAM)
    rpr._route_refine(parent, "run_100", dict(_LLM_INTERP), {})
    child_state = (campaign_root["runs_dir"] / "run_101" / "pipeline_state.yaml").read_bytes()
    reference_dir = tmp_path / "reference_runs"
    _write_fresh_scaffold(reference_dir, "run_101")
    assert child_state == (reference_dir / "run_101" / "pipeline_state.yaml").read_bytes()


def test_route_refine_legacy_parent_without_family_still_refines(campaign_root):
    """Legacy card (no family key): refine proceeds, nothing is inherited, and
    the child sets its own family at its own creation."""
    _set_flag(True)
    parent = _refine_parent(campaign_root)  # card with no family
    assert rpr._route_refine(parent, "run_100", dict(_LLM_INTERP), {}) == "completed_refined"
    child = campaign_root["runs_dir"] / "run_101"
    assert rpr._INHERITED_FAMILY_STATE_KEY not in _state(child)
    _card(child, family="volatility_breakout")
    rpr._enforce_hypothesis_family(child)  # valid fresh label accepted
    _card(child)
    with pytest.raises(ValueError):
        rpr._enforce_hypothesis_family(child)  # and a fresh card still needs one


@pytest.mark.parametrize("bad", ["", None, "Bad Label"])
def test_route_refine_corrupt_parent_family_raises_before_any_child_exists(campaign_root, bad):
    _set_flag(True)
    parent = _refine_parent(campaign_root, family=bad)
    with pytest.raises(ValueError, match="corrupted family"):
        rpr._route_refine(parent, "run_100", dict(_LLM_INTERP), {})
    assert not (campaign_root["runs_dir"] / "run_101").exists()


def test_route_refine_parent_without_any_card_inherits_nothing(campaign_root):
    _set_flag(True)
    parent = _refine_parent(campaign_root, family=FAM)
    (parent / "artifacts" / "hypothesis_card.yaml").unlink()
    assert rpr._route_refine(parent, "run_100", dict(_LLM_INTERP), {}) == "completed_refined"
    assert rpr._INHERITED_FAMILY_STATE_KEY not in _state(campaign_root["runs_dir"] / "run_101")


@pytest.mark.parametrize("text", ["- a\n- list\n", ""])
def test_route_refine_non_mapping_parent_card_raises_before_any_child(campaign_root, text):
    _set_flag(True)
    parent = _refine_parent(campaign_root, family=FAM)
    (parent / "artifacts" / "hypothesis_card.yaml").write_text(text, encoding="utf-8")
    with pytest.raises(ValueError, match="not a mapping"):
        rpr._route_refine(parent, "run_100", dict(_LLM_INTERP), {})
    assert not (campaign_root["runs_dir"] / "run_101").exists()


def _refinement_brief_setup(campaign_root, **card_fields):
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_600")
    _card(runs_dir / "run_600", **card_fields)
    (root / "briefs").mkdir()
    _write_refinement_brief(root / "briefs" / "test_refinement.yaml")
    _save_queue_entries(campaign_root["queue_path"], [{
        "id": "TEST_ENTRY", "brief_path": "briefs/irrelevant.yaml",
        "status": "in_progress", "priority": 1, "run_ids": ["run_600"], "outcome": None,
        "refinement_brief_path": "briefs/test_refinement.yaml",
    }])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_600"])


def test_refinement_brief_child_inherits_parent_family(campaign_root):
    _set_flag(True)
    _refinement_brief_setup(campaign_root, family=FAM)
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(camp.orch, "run_loop", lambda run_id: None)
        assert camp.process_once() is True
    assert _state(campaign_root["runs_dir"] / "run_601")[rpr._INHERITED_FAMILY_STATE_KEY] == FAM


@pytest.mark.parametrize("flag", [None, False])
def test_refinement_brief_child_flag_off_writes_no_marker(campaign_root, flag):
    _set_flag(flag)
    _refinement_brief_setup(campaign_root, family=FAM)
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(camp.orch, "run_loop", lambda run_id: None)
        camp.process_once()
    assert rpr._INHERITED_FAMILY_STATE_KEY not in _state(campaign_root["runs_dir"] / "run_601")


def test_refinement_brief_corrupt_parent_family_pauses_and_builds_no_child(campaign_root):
    """CODE-REVIEW REGRESSION: the raise used to escape process_once, leaving
    the entry selectable so every restart crash-looped on it. It now pauses
    the entry (same shape as the conflict pause) and records halt history."""
    _set_flag(True)
    _refinement_brief_setup(campaign_root, family="")
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(camp.orch, "run_loop", lambda run_id: None)
        assert camp.process_once() is False
    assert not (campaign_root["runs_dir"] / "run_601").exists()
    entry = _read(campaign_root["queue_path"])["queue"][0]
    assert entry["status"] == "paused:refinement_brief_parent_family_invalid"
    history = _state(campaign_root["runs_dir"] / "run_600").get("halt_history") or []
    assert history and history[-1]["reason"] == "refinement_brief_parent_family_invalid"
    # and the pause is documented for the operator
    assert "refinement_brief_parent_family_invalid" in (SR_ROOT / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")


def _split_setup(campaign_root, families, marker=None):
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_700")
    run_dir = runs_dir / "run_700"
    for i, fam in enumerate(families):
        card = {"hypothesis_id": f"H-{i}"}
        if fam is not _ABSENT:
            card["family"] = fam
        (run_dir / "artifacts" / f"hypothesis_card_{i}.yaml").write_text(yaml.safe_dump(card), encoding="utf-8")
    if marker is not None:
        rpr.update_state(path=run_dir, **{rpr._INHERITED_FAMILY_STATE_KEY: marker})
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_700"])
    return run_dir


def test_split_siblings_of_a_refine_child_inherit(campaign_root):
    _set_flag(True)
    run_dir = _split_setup(campaign_root, ["other_a", "other_b"], marker=FAM)
    assert rpr._handle_hypothesis_generation_multi_card_split("run_700", run_dir) is True
    sib = campaign_root["runs_dir"] / "run_701"
    assert _read(sib / "artifacts" / "hypothesis_card.yaml")["family"] == FAM
    assert _state(sib)[rpr._INHERITED_FAMILY_STATE_KEY] == FAM
    rpr._enforce_hypothesis_family(run_dir)  # what run_loop does next for the kept card
    assert _read(run_dir / "artifacts" / "hypothesis_card.yaml")["family"] == FAM


@pytest.mark.parametrize("families", [["volatility_breakout", "Bad Label"], [_ABSENT, "volatility_breakout"]],
                         ids=["bad_sibling", "bad_first_card"])
def test_split_fresh_bad_family_fails_before_any_sibling(campaign_root, families):
    _set_flag(True)
    run_dir = _split_setup(campaign_root, families)
    with pytest.raises(ValueError):
        rpr._handle_hypothesis_generation_multi_card_split("run_700", run_dir)
    assert not (campaign_root["runs_dir"] / "run_701").exists()
    assert not (run_dir / "artifacts" / "hypothesis_card.yaml").exists()


def test_split_fresh_valid_families_kept_per_card(campaign_root):
    _set_flag(True)
    run_dir = _split_setup(campaign_root, ["volatility_breakout", "funding_carry"])
    rpr._handle_hypothesis_generation_multi_card_split("run_700", run_dir)
    sib = campaign_root["runs_dir"] / "run_701"
    assert _read(sib / "artifacts" / "hypothesis_card.yaml")["family"] == "funding_carry"
    assert rpr._INHERITED_FAMILY_STATE_KEY not in _state(sib)


@pytest.mark.parametrize("flag", [None, False])
def test_split_flag_off_sibling_card_is_a_verbatim_copy(campaign_root, flag):
    _set_flag(flag)
    run_dir = _split_setup(campaign_root, [_ABSENT, "Bad Label"], marker=FAM)
    src = (run_dir / "artifacts" / "hypothesis_card_1.yaml").read_bytes()
    rpr._handle_hypothesis_generation_multi_card_split("run_700", run_dir)
    sib = campaign_root["runs_dir"] / "run_701"
    assert (sib / "artifacts" / "hypothesis_card.yaml").read_bytes() == src
    assert rpr._INHERITED_FAMILY_STATE_KEY not in _state(sib)


# ===========================================================================
# Task 1f -- _synthesize_verdict reads the family from the card
# ===========================================================================

def test_synthesis_family_comes_from_the_card(tmp_path):
    out = _synth(_make_run(tmp_path, family="funding_carry"))
    assert out["hypothesis_family"] == "funding_carry"
    _assert_valid(out)


def test_synthesis_signature_no_longer_takes_a_family():
    assert list(inspect.signature(rpr._synthesize_verdict).parameters) == ["run_dir", "regime_detector_report"]


@pytest.mark.parametrize("family", [_ABSENT, None, "", "  ", "Keltner Breakout", " keltner", "keltner\n",
                                    "x" * 49, 7],
                         ids=["legacy_missing", "null", "empty", "blank", "caps_space", "leading_space",
                              "trailing_newline", "too_long", "int"])
def test_synthesis_fails_closed_on_missing_or_bad_family(tmp_path, family):
    with pytest.raises(rpr.VerdictSynthesisError, match="family"):
        _synth(_make_run(tmp_path, family=family))


def test_synthesis_family_is_checked_even_on_a_safety_pause(tmp_path):
    run = _make_run(tmp_path, family=_ABSENT, protocol=_protocol_result(component_error_count=1))
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(run)


def test_synthesis_rejects_a_card_family_that_breaks_inheritance(tmp_path):
    run = _make_run(tmp_path, family="keltner_threshold_regime",
                    state={"run_id": "run", rpr._INHERITED_FAMILY_STATE_KEY: FAM})
    with pytest.raises(rpr.VerdictSynthesisError, match="inherited"):
        _synth(run)


def test_synthesis_accepts_a_matching_inheritance_marker_and_plain_state(tmp_path):
    out = _synth(_make_run(tmp_path / "a", state={rpr._INHERITED_FAMILY_STATE_KEY: FAM}))
    assert out["hypothesis_family"] == FAM
    assert _synth(_make_run(tmp_path / "b", state={"run_id": "x"}))["hypothesis_family"] == FAM


@pytest.mark.parametrize("state", ["- not\n- a mapping\n", "[unclosed"])
def test_synthesis_rejects_a_corrupt_pipeline_state(tmp_path, state):
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(_make_run(tmp_path, state=state))


# ===========================================================================
# Task 2 -- primary_failure_mode / reactivation_trigger on every path
# ===========================================================================

def _bucket(text):
    return near_miss_scoreboard.classify_bucket(text)


def test_safety_pause_component_execution_error(tmp_path):
    out = _synth(_make_run(tmp_path, protocol=_protocol_result(component_error_count=2)))
    _assert_valid(out)
    assert out["primary_failure_mode"] == (
        "component_execution_error: protocol_result.yaml results[0] (BTCUSDT/w1): "
        "component_errors.count=2 (+3 more)")
    assert out["reactivation_trigger"] == (
        "component_execution_error: re-run once the component fault is fixed -- every "
        "protocol_result.yaml results[i].component_errors.count must be 0 (4 result(s) currently > 0)")
    assert _bucket(out["primary_failure_mode"]) == ["other"]


def test_safety_pause_single_evidence_line_has_no_more_suffix(tmp_path):
    pr = _protocol_result()
    pr["results"][2]["component_errors"]["count"] = 1
    out = _synth(_make_run(tmp_path, protocol=pr))
    assert out["primary_failure_mode"] == \
        "component_execution_error: protocol_result.yaml results[2] (ETHUSDT/w1): component_errors.count=1"
    assert out["reactivation_trigger"].endswith("(1 result(s) currently > 0)")


def test_safety_pause_regime_misattribution(tmp_path):
    out = _synth(_make_run(tmp_path, protocol=_protocol_result(uninformative=("trending", "ranging"))),
                 report=_detector_report("low"))
    _assert_valid(out)
    assert out["primary_failure_mode"].startswith(
        "regime_misattribution: RULE 4: uninformative regime 'trending' (median n_bars=50")
    assert out["primary_failure_mode"].endswith("(+3 more)")  # ranging + 2 low-confidence lines
    # CODE-REVIEW REGRESSION: the trigger names BOTH conditions that clear the
    # pause (detector confirmed high, or a sample-size reclassification).
    assert out["reactivation_trigger"] == (
        "regime_misattribution: re-run once either (a) regime_detector_report.yaml exists and reports "
        "confidence=high for every tested symbol (BTCUSDT, ETHUSDT), or (b) each uninformative regime "
        "[trending, ranging] has a measured median n_bars below 20 (a sample issue, not a regime finding)")
    assert _bucket(out["primary_failure_mode"]) == ["regime"]


@pytest.mark.parametrize("blocked_by,named", [(["G1", "G5"], "G1, G5"), ([], "none named"), (None, "none named")])
def test_verdict_blocked(tmp_path, blocked_by, named):
    pr = {"result": "VERDICT_BLOCKED", "reason": "funding not modeled"}
    if blocked_by is not None:
        pr["blocked_by"] = blocked_by
    out = _synth(_make_run(tmp_path, pass_rule=pr))
    _assert_valid(out)
    shown = blocked_by if blocked_by is not None else []
    assert out["primary_failure_mode"] == (
        f"verdict_blocked: pass_rule_evaluation.yaml result=VERDICT_BLOCKED, blocked_by={shown}: "
        f"funding not modeled")
    assert out["reactivation_trigger"] == (
        f"verdict_blocked: re-run once pass_rule_evaluation.yaml's blocked precondition(s) [{named}] "
        f"are satisfied (result no longer VERDICT_BLOCKED)")


@pytest.mark.parametrize("blocked_by", ["G1", [1], [""], [None], {"G1": 1}])
def test_verdict_blocked_malformed_blocked_by_fails_closed(tmp_path, blocked_by):
    pr = {"result": "VERDICT_BLOCKED", "blocked_by": blocked_by}
    with pytest.raises(rpr.VerdictSynthesisError, match="blocked_by"):
        _synth(_make_run(tmp_path, pass_rule=pr))


def test_binding_promote_has_no_failure_mode(tmp_path):
    out = _synth(_make_run(tmp_path, pass_rule=_binding("PASS", "promote", None),
                           proposals={"profitability": [_proposal("profitability", scores=(3, 3, 3))]}))
    _assert_valid(out)
    assert out["primary_failure_mode"] is None and out["reactivation_trigger"] is None


@pytest.mark.parametrize("hv,lr", [("kill", "terminate"), ("kill", "pivot"), ("kill", "escalate"),
                                   ("refine", "refine")])
def test_binding_without_evidence_bearing_winner(tmp_path, hv, lr):
    out = _synth(_make_run(tmp_path, pass_rule=_binding("FAIL", hv, lr),
                           proposals={"regime_power": [_proposal("regime_power", scores=(0, 0, 0))]}))
    _assert_valid(out)
    assert out["primary_failure_mode"] == \
        f"pass_rule_branch: pass_rule FAIL branch FAIL-a ({hv}/{lr}), failed criteria [a]"
    assert out["reactivation_trigger"] is None
    assert _bucket(out["primary_failure_mode"]) == ["other"]


def test_binding_with_evidence_bearing_winner_leads_with_its_category(tmp_path):
    out = _synth(_make_run(tmp_path, pass_rule=_binding("FAIL", "kill", "terminate"),
                           proposals={"regime_power": [_proposal("regime_power", scores=(1, 1, 0))]}))
    _assert_valid(out)
    assert out["primary_failure_mode"] == (
        "regime_power: regime_power-run_test-1 (S=2/9, low confidence) slices.overall.diagnostics.x=1; "
        "pass_rule FAIL branch FAIL-a (kill/terminate), failed criteria [a]")
    assert out["reactivation_trigger"] is None  # never softens a registered kill
    assert _bucket(out["primary_failure_mode"]) == ["regime"]


def test_binding_unrecorded_branch_and_no_failed_criteria(tmp_path):
    pr = _binding("FAIL", "kill", "terminate", criteria_results=[{"id": "a", "result": "INCONCLUSIVE"}])
    pr.pop("statement_branch_matched")
    out = _synth(_make_run(tmp_path, pass_rule=pr))
    assert out["primary_failure_mode"] == \
        "pass_rule_branch: pass_rule FAIL branch unrecorded (kill/terminate), failed criteria []"


@pytest.mark.parametrize("scores,conf", [((3, 2, 2), ""), ((2, 1, 2), ", low confidence")])
def test_scored_refine_names_the_winner(tmp_path, scores, conf):
    out = _synth(_make_run(tmp_path, proposals={"forecast_power": [_proposal("forecast_power", scores=scores)]}))
    _assert_valid(out)
    assert out["primary_failure_mode"] == (
        f"forecast_power: forecast_power-run_test-1 (S={sum(scores)}/9{conf}) slices.overall.diagnostics.x=1")
    assert out["reactivation_trigger"] is None


def test_scored_refine_appends_failed_criteria_when_present(tmp_path):
    pr = {"result": "FAIL", "discretion": "stage", "hypothesis_verdict": None, "lineage_routing": None,
          "statement_branch_matched": "FAIL-a", "branches_failed": ["FAIL-a"],
          "criteria_results": [{"id": "a", "result": "FAIL"}, {"id": "b", "result": "PASS"},
                               {"id": "c", "result": "FAIL"}]}
    out = _synth(_make_run(tmp_path, pass_rule=pr,
                           proposals={"profitability": [_proposal("profitability", scores=(3, 3, 3))]}))
    _assert_valid(out)
    assert out["primary_failure_mode"].endswith("; failed criteria [a, c]")


def test_scored_kill_no_proposals(tmp_path):
    out = _synth(_make_run(tmp_path))
    _assert_valid(out)
    assert out["primary_failure_mode"] == "no_evidence_bearing_proposal: no reader proposed anything"
    assert out["reactivation_trigger"] is None


def test_scored_kill_all_zero(tmp_path):
    out = _synth(_make_run(tmp_path, proposals={
        "profitability": [_proposal("profitability", scores=(0, 0, 0))],
        "trade_efficiency": [_proposal("trade_efficiency", scores=(0, 0, 0))]}))
    _assert_valid(out)
    assert out["primary_failure_mode"] == "no_evidence_bearing_proposal: all 2 proposal(s) scored 0/9"


def test_scored_kill_with_failed_criteria(tmp_path):
    pr = {"result": "SPEC_ERROR", "reason": "x", "criteria_results": [{"id": "q", "result": "FAIL"}]}
    out = _synth(_make_run(tmp_path, pass_rule=pr))
    assert out["primary_failure_mode"] == \
        "no_evidence_bearing_proposal: no reader proposed anything; failed criteria [q]"


def test_multiline_evidence_is_collapsed_to_one_line(tmp_path):
    p = _proposal("profitability", scores=(3, 3, 3))
    p["evidence"] = ["slices.overall.core.cost_drag_pct=142.8\n   (dominant\tdriver)", "second"]
    out = _synth(_make_run(tmp_path, proposals={"profitability": [p]}))
    assert out["primary_failure_mode"] == \
        "profitability: profitability-run_test-1 (S=9/9) slices.overall.core.cost_drag_pct=142.8 (dominant driver)"
    assert "\n" not in out["primary_failure_mode"]


@pytest.mark.parametrize("evidence", [["   "], ["\n\t"], ["ok", " "]])
def test_whitespace_only_evidence_line_fails_closed(tmp_path, evidence):
    p = _proposal("profitability", scores=(3, 3, 3))
    p["evidence"] = evidence
    with pytest.raises(rpr.VerdictSynthesisError, match="evidence"):
        _synth(_make_run(tmp_path, proposals={"profitability": [p]}))


def test_unknown_failure_mode_tag_fails_closed(tmp_path, monkeypatch):
    """If the category list and the tag vocabulary ever drift apart, the
    synthesis raises instead of emitting an unbucketable tag."""
    monkeypatch.setattr(rpr, "_SYNTHESIS_FAILURE_MODE_TAGS",
                        rpr._SYNTHESIS_FAILURE_MODE_TAGS - {"profitability"})
    with pytest.raises(rpr.VerdictSynthesisError, match="closed vocabulary"):
        _synth(_make_run(tmp_path, proposals={"profitability": [_proposal("profitability", scores=(3, 3, 3))]}))


# --- consumer fit ------------------------------------------------------------

def test_tag_vocabulary_matches_report_categories_and_schema():
    assert rpr._SYNTHESIS_READER_CATEGORY_TAGS == tuple(build_reports.REPORT_CATEGORIES)
    pattern = SCHEMA["properties"]["primary_failure_mode"]["pattern"]
    schema_tags = set(pattern[len("^("):pattern.index("):")].split("|"))
    assert schema_tags == set(rpr._SYNTHESIS_FAILURE_MODE_TAGS)
    trig = SCHEMA["properties"]["reactivation_trigger"]["pattern"]
    assert set(trig[len("^("):trig.index("):")].split("|")) == \
        {"component_execution_error", "regime_misattribution", "verdict_blocked"}


@pytest.mark.parametrize("tag", sorted(rpr._SYNTHESIS_FAILURE_MODE_TAGS))
def test_scoreboard_bucket_is_decided_by_the_tag_alone(tag):
    """near_miss_scoreboard buckets on the first sentence; '<tag>: ' ends it,
    so even a detail full of other buckets' keywords cannot leak in."""
    text = f"{tag}: cost drag 180% of gross; no predictive edge; insufficient sample. regime gate"
    expected = ["regime"] if tag in ("regime_misattribution", "regime_power") else ["other"]
    assert _bucket(text) == expected


def test_reactivation_triggers_name_no_timeframe_branch(tmp_path):
    """anti_adjacency_gate parses KB reactivation_condition prose for timeframe
    tokens (1h/4h/daily...) to decide which sibling branches stay open; a
    mechanical trigger must never open one by accident."""
    outs = [
        _synth(_make_run(tmp_path / "a", protocol=_protocol_result(component_error_count=1))),
        _synth(_make_run(tmp_path / "b", protocol=_protocol_result(uninformative=("trending",))), report=None),
        _synth(_make_run(tmp_path / "c", pass_rule={"result": "VERDICT_BLOCKED", "blocked_by": ["G1"]})),
    ]
    for out in outs:
        assert out["reactivation_trigger"]
        assert anti_adjacency_gate._extract_named_branches(out["reactivation_trigger"]) == set()


def test_failure_mode_feeds_the_pivot_kb_text_check(tmp_path):
    """_route_pivot concatenates primary_failure_mode into the text
    _check_kb_reactivation_conformance scans; a reader evidence line naming an
    exhausted hypothesis is still caught through the rebuilt field."""
    p = _proposal("forecast_power", scores=(3, 3, 3))
    p["evidence"] = ["slices.overall.diagnostics.corr=0.01 mirrors H-041-A"]
    out = _synth(_make_run(tmp_path, proposals={"forecast_power": [p]}))
    kb = {"findings": [{"id": "f1", "hypothesis_id": "H-041-A", "exhausted": True,
                        "reactivation_condition": None, "outcome": "no_edge"}]}
    assert rpr._check_kb_reactivation_conformance({"research_goal": out["primary_failure_mode"]}, kb)


# --- schema --------------------------------------------------------------------

def _samples(tmp_path):
    return {
        "cee": _synth(_make_run(tmp_path / "1", protocol=_protocol_result(component_error_count=1))),
        "regime": _synth(_make_run(tmp_path / "2", protocol=_protocol_result(uninformative=("trending",))),
                         report=None),
        "blocked": _synth(_make_run(tmp_path / "3", pass_rule={"result": "VERDICT_BLOCKED", "blocked_by": ["G1"]})),
        "promote": _synth(_make_run(tmp_path / "4", pass_rule=_binding("PASS", "promote", None))),
        "binding_kill": _synth(_make_run(tmp_path / "5", pass_rule=_binding("FAIL", "kill", "terminate"))),
        "scored_refine": _synth(_make_run(tmp_path / "6", proposals={
            "profitability": [_proposal("profitability", scores=(3, 3, 3))]})),
        "scored_kill": _synth(_make_run(tmp_path / "7")),
    }


def test_every_path_validates(tmp_path):
    for name, out in _samples(tmp_path).items():
        errors = [e.message for e in VALIDATOR.iter_errors(out)]
        assert not errors, (name, errors)


@pytest.mark.parametrize("sample,field,value", [
    ("scored_refine", "primary_failure_mode", "cost: made up tag"),               # unknown tag
    ("scored_refine", "primary_failure_mode", "profitability:"),                 # tag without detail
    ("scored_refine", "primary_failure_mode", "profitability:  "),               # whitespace detail
    ("scored_refine", "primary_failure_mode", None),                             # non-promote needs one
    ("scored_refine", "primary_failure_mode", "no_evidence_bearing_proposal: x"),  # refine with kill tag
    ("scored_kill", "primary_failure_mode", "profitability: x"),                 # kill with winner tag
    ("binding_kill", "primary_failure_mode", "no_evidence_bearing_proposal: x"), # scored-only tag
    ("binding_kill", "primary_failure_mode", "verdict_blocked: x"),              # pause-only tag
    ("promote", "primary_failure_mode", "pass_rule_branch: x"),                  # promote has none
    ("scored_refine", "reactivation_trigger", "verdict_blocked: x"),             # off-pause trigger
    ("binding_kill", "reactivation_trigger", "component_execution_error: x"),
    ("cee", "reactivation_trigger", None),                                       # pause needs one
    ("cee", "reactivation_trigger", "regime_misattribution: x"),                 # wrong reason tag
    ("cee", "primary_failure_mode", "verdict_blocked: x"),
    ("regime", "primary_failure_mode", "component_execution_error: x"),
    ("blocked", "reactivation_trigger", "regime_misattribution: x"),
    ("blocked", "reactivation_trigger", ""),
])
def test_schema_rejects_inconsistent_failure_fields(tmp_path, sample, field, value):
    out = copy.deepcopy(_samples(tmp_path)[sample])
    _assert_valid(out)
    out[field] = value
    assert list(VALIDATOR.iter_errors(out)), f"{sample}: {field}={value!r} was accepted"


@pytest.mark.parametrize("field", ["primary_failure_mode", "reactivation_trigger"])
def test_schema_requires_both_new_fields(tmp_path, field):
    out = copy.deepcopy(_samples(tmp_path)["scored_refine"])
    del out[field]
    assert list(VALIDATOR.iter_errors(out))


@pytest.mark.parametrize("dropped", ["config_to_failure_map", "power_disposition", "trade_attribution",
                                     "prescreen_result_summary", "prescreen_summary"])
def test_dropped_legacy_fields_are_smuggled_fields(tmp_path, dropped):
    """Operator decision item 5: these have no home in the new artifact."""
    assert dropped not in SCHEMA["properties"]
    out = copy.deepcopy(_samples(tmp_path)["binding_kill"])
    out[dropped] = "x"
    assert list(VALIDATOR.iter_errors(out))


def test_schema_rejects_malformed_family(tmp_path):
    out = copy.deepcopy(_samples(tmp_path)["scored_kill"])
    for bad in ("Keltner", "keltner__x", "x" * 49, ""):
        out["hypothesis_family"] = bad
        assert list(VALIDATOR.iter_errors(out)), bad



# ---------------------------------------------------------------------------
# CODE-REVIEW REGRESSIONS (2026-09-23 review of bbd91643)
# ---------------------------------------------------------------------------

def test_route_refine_parent_without_card_falls_back_to_its_own_marker(campaign_root):
    """A parent that is itself a refine child but failed before its own
    hypothesis_generation has no card -- its marker still carries the
    lineage's family, which must not be dropped."""
    _set_flag(True)
    parent = _refine_parent(campaign_root, family=FAM)
    (parent / "artifacts" / "hypothesis_card.yaml").unlink()
    rpr.update_state(path=parent, **{rpr._INHERITED_FAMILY_STATE_KEY: FAM})
    assert rpr._route_refine(parent, "run_100", dict(_LLM_INTERP), {}) == "completed_refined"
    assert _state(campaign_root["runs_dir"] / "run_101")[rpr._INHERITED_FAMILY_STATE_KEY] == FAM


def test_route_refine_legacy_parent_card_falls_back_to_its_own_marker(campaign_root):
    _set_flag(True)
    parent = _refine_parent(campaign_root)  # card without `family`
    rpr.update_state(path=parent, **{rpr._INHERITED_FAMILY_STATE_KEY: FAM})
    rpr._route_refine(parent, "run_100", dict(_LLM_INTERP), {})
    assert _state(campaign_root["runs_dir"] / "run_101")[rpr._INHERITED_FAMILY_STATE_KEY] == FAM


def test_refine_child_overwrite_works_under_raise_mode_validation(tmp_path, monkeypatch):
    """load_yaml schema-validates on read; under raise mode a wrong family
    used to raise before the documented overwrite could happen."""
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    _set_flag(True)
    run = tmp_path / "run_x"
    card = _card(run, family="Keltner-Breakout")
    # Isolate the READ: this minimal card fails other schema rules, which
    # raise mode would (correctly) enforce on write -- not what is tested here.
    monkeypatch.setattr(rpr, "save_yaml",
                        lambda p, d: Path(p).write_text(yaml.safe_dump(d), encoding="utf-8"))
    (run / "pipeline_state.yaml").write_text(
        yaml.safe_dump({rpr._INHERITED_FAMILY_STATE_KEY: FAM}), encoding="utf-8")
    rpr._enforce_hypothesis_family(run)
    assert _read(card)["family"] == FAM


def test_enforce_rejects_a_multi_document_card_instead_of_silently_dropping_one(tmp_path):
    _set_flag(True)
    run = tmp_path / "run_y"
    path = _card(run, family=FAM)
    second_doc = "\n".join(["---", "hypothesis_id: H-TEST-2", ""])
    path.write_text(path.read_text(encoding="utf-8") + second_doc, encoding="utf-8")
    with pytest.raises(ValueError, match="single YAML document"):
        rpr._enforce_hypothesis_family(run)
