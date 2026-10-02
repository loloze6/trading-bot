"""
E-046a Slice 5b-ii-B -- the specialist_readers stage and the interim route from
the grid (orchestrator.specialist_readers.enabled, off by default).

Covers:
  1. The flag helper: off/absent, non-bool, and its two hard dependencies
     (grid_evaluation, category_reports) -- enforced at run_loop start.
  2. Flag-off byte-identity: stage registry, _build_stage_prompt, the
     protocol_execution -> verdict_interpreter route, no new handoff file,
     the campaign log line.
  3. The reader loop: 5 readers -> 5 distinct skill dirs -> 5 distinct output
     paths, each prompt carrying only its own report plus the grid; the
     retune firewall before regime_power; resume skips valid files.
  4. Fail-loud reader output: malformed proposals, zero/several fenced blocks,
     a malformed file already on disk.
  5. The route: validated -> promote, refuted -> kill/terminate,
     inconclusive -> human_pause (inconclusive_grid); component errors pause
     first; missing/malformed idea_status fails loud.
  6. Reader scores cannot change the route; the route never reads proposals.
  7. verdict_interpreter is never invoked under the flag.

No LLM: the one model call (_invoke_reader_llm) is replaced in every test that
reaches it. Sandboxing: tests/conftest.py's autouse _sandbox_by_default
redirects rpr.ROOT / camp.ROOT to a per-test tmp dir.
"""
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import reader_proposals  # noqa: E402
from build_reports import REPORT_CATEGORIES  # noqa: E402

from test_k3_protocol_pinning import _minimal_run  # noqa: E402
from test_e033_slice4b_gate_conformance_promotion import _minimal_run_at, _noop_invoke  # noqa: E402

RUN_ID = "run_990"
ALL_ON = {"grid_evaluation": {"enabled": True}, "category_reports": {"enabled": True},
          "specialist_readers": {"enabled": True}}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _set_orchestrator(orchestrator: dict | None) -> None:
    config_dir = rpr.ROOT / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    path = config_dir / "campaign_config.yaml"
    if orchestrator is None:
        if path.exists():
            path.unlink()
        return
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump({"orchestrator": orchestrator}, f)


def _protocol_result(errors_count=None, variant_dir: Path | None = None) -> dict:
    entry = {"symbol": "BTCUSDT", "window": "w1", "core": {"sharpe": 0.1}}
    if errors_count is not None:
        entry["component_errors"] = {"count": errors_count, "samples": []}
    return {"verdict": "kill", "results": [entry]}


def _seed_run(run_id=RUN_ID, idea_status="refuted", errors_count=None, pending="specialist_readers",
              with_reports=True) -> Path:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["pending_stage"] = pending
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "protocol_result.yaml", _protocol_result(errors_count))
    rpr.save_yaml(arts / "grid_evaluation.yaml", {"result": "X", "marker": "GRID_MARKER"})
    # E-061 C2 S2e: the stage writes this before the first reader; tests that call
    # _run_specialist_readers directly need the stand-in the handoff now requires.
    rpr.save_yaml(arts / "registry_summary.yaml", {"marker": "REGISTRY_SUMMARY_MARKER"})
    rpr.save_yaml(arts / "hypothesis_card.yaml", {"hypothesis_id": "H-TEST-1"})
    _write_menu_pre_registration(run_dir)
    if idea_status is not None:
        rpr.save_yaml(arts / "idea_status.yaml",
                      rpr._build_idea_status_artifact({"idea_status": idea_status, "reason": "r"}, run_id))
    if with_reports:
        for c in REPORT_CATEGORIES:
            rpr.save_yaml(arts / "reports" / f"{c}.yaml", {"category": c, "marker": f"REPORT_{c.upper()}"})
    return run_dir


MENU_PASS_RULE = {"criteria": [{"id": "c1", "source": "core.sharpe", "reducer": "median"}]}


def _write_menu_pre_registration(run_dir: Path) -> None:
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml", {"pass_rule": MENU_PASS_RULE})


def _proposal(cat: str, run_id: str = RUN_ID, n: int = 1, score: int = 2) -> dict:
    return {
        "proposal_id": f"{cat}-{run_id}-{n}", "kind": "patch",
        "patch": [{"component_id": "c1", "field": "params.x", "before": 1, "after": 2}],
        "evidence": [f"slices.overall.x=1 ({cat})"],
        "scores": {"confidence_real": score, "distance_to_profitable": score,
                   "mechanism_plausibility": score},
        "model_id": "m", "rubric_version": f"{cat}-reader-v1",
    }


def _fake_llm(outputs: dict | None = None, calls: list | None = None):
    """An async stand-in for _invoke_reader_llm. `outputs` maps category ->
    raw model text; default is an honest empty list for every reader."""
    async def _fake(prompt: str):
        cat = next(c for c in REPORT_CATEGORIES if f"reader_category: {c}\n" in prompt)
        if calls is not None:
            calls.append((cat, prompt))
        text = (outputs or {}).get(cat, f"```yaml\n# {cat}.yaml\n[]\n```")
        return text, {"usage": {"input_tokens": 10, "output_tokens": 5}, "cost_usd": 0.0,
                      "num_turns": 1}
    return _fake


# ---------------------------------------------------------------------------
# 1. Flag helper and its dependencies
# ---------------------------------------------------------------------------

def test_flag_false_when_config_absent_or_key_absent():
    _set_orchestrator(None)
    assert rpr._specialist_readers_enabled() is False
    _set_orchestrator({})
    assert rpr._specialist_readers_enabled() is False


def test_flag_true_with_both_dependencies():
    _set_orchestrator(ALL_ON)
    assert rpr._specialist_readers_enabled() is True


@pytest.mark.parametrize("missing", ["grid_evaluation", "category_reports"])
def test_flag_on_without_a_dependency_raises(missing):
    orch = {k: dict(v) for k, v in ALL_ON.items()}
    orch[missing]["enabled"] = False
    _set_orchestrator(orch)
    with pytest.raises(ValueError, match=f"orchestrator.{missing}.enabled=true"):
        rpr._specialist_readers_enabled()


@pytest.mark.parametrize("bad", ["false", None, 1])
def test_flag_non_bool_raises(bad):
    _set_orchestrator({"specialist_readers": {"enabled": bad}})
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._specialist_readers_enabled()


def test_run_loop_fails_at_start_when_dependency_off(monkeypatch):
    _set_orchestrator({"specialist_readers": {"enabled": True}, "category_reports": {"enabled": True}})
    run_dir = _seed_run(pending="protocol_execution")
    invoked = []
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", lambda *a, **k: invoked.append(a[0]))
    rpr.run_loop(RUN_ID)  # code-review fix 9: sets status=failed, does not escape
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert invoked == []
    assert state["pending_stage"] == "protocol_execution"
    assert state["status"] == "failed" and "grid_evaluation" in state["last_error"]


# ---------------------------------------------------------------------------
# 2. Registry and flag-off identity
# ---------------------------------------------------------------------------

def test_verdict_interpreter_entry_kept_and_new_stage_registered_without_skill():
    assert rpr.STAGE_CONFIGS["verdict_interpreter"] == {
        "handoff": "protocol_to_verdict_interpreter.yaml",
        "default_next": "dynamic_routing", "skill": "verdict-interpreter"}
    assert rpr.STAGE_CONFIGS["protocol_execution"]["default_next"] == "verdict_interpreter"
    assert rpr.STAGE_CONFIGS["specialist_readers"] == {
        "handoff": "protocol_to_specialist_readers.yaml", "default_next": "dynamic_routing"}
    assert "specialist_readers" not in rpr._SKILL_MAP


def test_build_stage_prompt_unchanged_for_existing_stages(monkeypatch, tmp_path):
    monkeypatch.chdir(SR_ROOT)
    handoff = {"required_inputs": [], "optional_inputs": []}
    for stage, skill in rpr._SKILL_MAP.items():
        assert rpr._build_stage_prompt(stage, handoff, tmp_path) == \
            rpr._build_stage_prompt(stage, handoff, tmp_path, skill_file_name=skill)


@pytest.mark.parametrize("orchestrator", [None, {}, {"grid_evaluation": {"enabled": True},
                                                      "category_reports": {"enabled": True}}])
def test_flag_off_protocol_execution_routes_to_verdict_interpreter(monkeypatch, orchestrator):
    _set_orchestrator(orchestrator)
    run_dir = _minimal_run_at(rpr.ROOT, RUN_ID, "protocol_execution")
    rpr.save_yaml(run_dir / "handoffs" / "backtest_spec_to_protocol_execution.yaml",
                  {"required_inputs": [], "deliverables": []})
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", _protocol_result())
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)
    # Stop the loop at the next stage without running it: its handoff is absent,
    # so run_loop raises on loading it, after persisting the route.
    monkeypatch.setitem(rpr.STAGE_CONFIGS, "verdict_interpreter",
                        {**rpr.STAGE_CONFIGS["verdict_interpreter"], "handoff": "missing.yaml"})
    with pytest.raises(FileNotFoundError):
        rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["pending_stage"] == "verdict_interpreter"
    assert state["completed_stages"][-1] == "protocol_execution"
    assert not (run_dir / "handoffs" / "protocol_to_specialist_readers.yaml").exists()


def test_flag_on_protocol_execution_routes_to_specialist_readers(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _minimal_run_at(rpr.ROOT, RUN_ID, "protocol_execution")
    _write_menu_pre_registration(run_dir)
    rpr.save_yaml(run_dir / "handoffs" / "backtest_spec_to_protocol_execution.yaml",
                  {"required_inputs": [], "deliverables": []})
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", _protocol_result())
    seen = []

    async def _record(stage_name, run_id, retry_context=None):
        seen.append(stage_name)
    monkeypatch.setattr(rpr, "async_invoke_agent", _record)
    # The specialist_readers stage then fails loud on the missing idea_status.yaml.
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert seen == ["protocol_execution"]
    assert state["completed_stages"][-1] == "protocol_execution"
    assert state["pending_stage"] == "specialist_readers"
    assert state["status"] == "failed" and "idea_status.yaml" in state["last_error"]
    assert (run_dir / "handoffs" / "protocol_to_specialist_readers.yaml").exists()


def test_flag_off_campaign_log_line_ignores_idea_status():
    _set_orchestrator({"grid_evaluation": {"enabled": True}, "category_reports": {"enabled": True}})
    run_dir = _seed_run(idea_status="validated")
    assert "idea_status" not in camp._extract_run_numbers(run_dir)
    _set_orchestrator(ALL_ON)
    assert camp._extract_run_numbers(run_dir)["idea_status"] == "validated"


# ---------------------------------------------------------------------------
# 3. The reader loop
# ---------------------------------------------------------------------------

def test_loop_dispatches_five_readers_to_five_skills_and_five_paths(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    calls, skills = [], []
    real_build = rpr._build_stage_prompt

    def _spy_build(stage_name, handoff, path, retry_context=None, skill_file_name=None):
        skills.append(skill_file_name)
        return real_build(stage_name, handoff, path, retry_context, skill_file_name=skill_file_name)
    monkeypatch.setattr(rpr, "_build_stage_prompt", _spy_build)
    monkeypatch.setattr(rpr, "_invoke_reader_llm",
                        _fake_llm({c: f"```yaml\n# proposals/{c}.yaml\n- {yaml.safe_dump(_proposal(c), default_flow_style=True).strip()}\n```"
                                   for c in REPORT_CATEGORIES}, calls))

    result = rpr._run_specialist_readers(RUN_ID, run_dir, stage_attempt=0)

    assert [c for c, _ in calls] == list(REPORT_CATEGORIES)
    assert skills == [f"readers/{c}-reader" for c in REPORT_CATEGORIES]
    assert len(set(skills)) == 5
    for c, prompt in calls:
        # the real SKILL.md of this category's reader, and only this category's report
        assert f"name: {c}-reader" in prompt
        assert f"REPORT_{c.upper()}" in prompt and "GRID_MARKER" in prompt
        # E-061 C2 S2e: the registry summary is the one extra input, for every reader
        assert "REGISTRY_SUMMARY_MARKER" in prompt
        others = [o for o in REPORT_CATEGORIES if o != c]
        assert not any(f"REPORT_{o.upper()}" in prompt for o in others)
        assert "pre_registration" not in prompt.split("YOUR PROVIDED CONTEXT FILES:")[1]
    outputs = sorted((run_dir / "artifacts" / "proposals").glob("*.yaml"))
    assert [p.name for p in outputs] == sorted(f"{c}.yaml" for c in REPORT_CATEGORIES)
    assert {c: len(v) for c, v in result.items()} == {c: 1 for c in REPORT_CATEGORIES}
    audit = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    assert {f"specialist_readers_{c}_attempt_0" for c in REPORT_CATEGORIES} <= set(audit)


def test_retune_firewall_runs_at_stage_entry_before_any_reader(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    rpr.save_yaml(run_dir / "artifacts" / "regime_audit_decision.yaml",
                  {"recommended_action": "retune until sharpe improves"})
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(calls=calls))
    # code-review fix 5: checked at stage entry, before ANY reader call ...
    with pytest.raises(RuntimeError, match="RETUNE FIREWALL"):
        rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert calls == []
    # ... and again on a resume where some proposals already exist
    (run_dir / "artifacts" / "proposals").mkdir(parents=True)
    (run_dir / "artifacts" / "proposals" / "profitability.yaml").write_text("[]", encoding="utf-8")
    with pytest.raises(RuntimeError, match="RETUNE FIREWALL"):
        rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert calls == []


def test_resume_revalidates_existing_files_without_rerunning(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    (run_dir / "artifacts" / "proposals").mkdir(parents=True)
    (run_dir / "artifacts" / "proposals" / "profitability.yaml").write_text("[]\n", encoding="utf-8")
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(calls=calls))
    rpr._run_specialist_readers(RUN_ID, run_dir)
    assert "profitability" not in [c for c, _ in calls]
    assert len(calls) == 4


# ---------------------------------------------------------------------------
# 4. Fail-loud reader output
# ---------------------------------------------------------------------------

def _dropped(run_dir, category="profitability"):
    audit = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    return audit[f"specialist_readers_{category}_attempt_0_retry1"]["dropped_proposals"]


def test_malformed_proposal_is_dropped_loudly_after_one_retry(monkeypatch):
    """CUL-380: still refused and recorded, never kept -- but the run goes on
    (before: the run halted)."""
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    bad = _proposal("profitability")
    bad["scores"]["confidence_real"] = 5
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(
        {"profitability": "```yaml\n" + yaml.safe_dump([bad]) + "```"}, calls))
    result = rpr._run_specialist_readers(RUN_ID, run_dir)
    # one bounded retry, with the validation error in the second prompt
    assert [c for c, _ in calls if c == "profitability"] == ["profitability", "profitability"]
    assert "FAILED VALIDATION" in calls[1][1] and "confidence_real" in calls[1][1]
    # code-review fix 3 still holds: the bad proposal never reaches the final path
    assert result["profitability"] == []
    assert rpr.load_yaml(run_dir / "artifacts" / "proposals" / "profitability.yaml") == []
    assert (run_dir / "artifacts" / "debug_specialist_readers_profitability_raw_output.txt").exists()
    [drop] = _dropped(run_dir)
    assert drop["index"] == 0 and "confidence_real" in drop["error"]


def test_a_retry_can_succeed(monkeypatch):
    """code-review fix 3: a first invalid then valid answer succeeds, with no
    drop recorded. (CUL-380: a reader that fails twice no longer stops the run,
    so there is no failed attempt left to resume from.)"""
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    bad = _proposal("profitability")
    bad["scores"]["confidence_real"] = 5
    answers = iter(["```yaml\n" + yaml.safe_dump([bad]) + "```", "```yaml\n[]\n```"])
    calls = []
    good = _fake_llm(calls=calls)

    async def _flaky(prompt):
        if "reader_category: profitability\n" in prompt:
            return next(answers), {"usage": {}, "cost_usd": 0.0, "num_turns": 1}
        return await good(prompt)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _flaky)
    result = rpr._run_specialist_readers(RUN_ID, run_dir)
    assert result["profitability"] == []
    assert len(calls) == 4
    audit = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    assert "dropped_proposals" not in audit["specialist_readers_profitability_attempt_0_retry1"]


def test_a_reader_that_routes_is_refused_and_recorded(monkeypatch):
    """A reader emitting routing vocabulary as a field is rejected, not ignored:
    the proposal never reaches the proposals file and the refusal is recorded
    (CUL-380: dropped, the run goes on)."""
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    bad = _proposal("profitability")
    bad["hypothesis_verdict"] = "promote"
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(
        {"profitability": "```yaml\n" + yaml.safe_dump([bad]) + "```"}))
    result = rpr._run_specialist_readers(RUN_ID, run_dir)
    assert result["profitability"] == []
    assert "hypothesis_verdict" not in (run_dir / "artifacts" / "proposals" / "profitability.yaml"
                                        ).read_text(encoding="utf-8")
    [drop] = _dropped(run_dir)
    assert "undeclared field" in drop["error"]


def test_a_valid_proposal_next_to_an_invalid_one_is_kept(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    good, bad = _proposal("profitability"), _proposal("profitability")
    bad["scores"]["confidence_real"] = 5
    bad["proposal_id"] = good["proposal_id"][:-1] + "9"
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(
        {"profitability": "```yaml\n" + yaml.safe_dump([good, bad]) + "```"}))
    result = rpr._run_specialist_readers(RUN_ID, run_dir)
    assert [p["proposal_id"] for p in result["profitability"]] == [good["proposal_id"]]
    [drop] = _dropped(run_dir)
    assert drop["index"] == 1 and drop["proposal_id"] == bad["proposal_id"]


@pytest.mark.parametrize("text", ["no fenced block at all", "```yaml\n[]\n```\n```yaml\n[]\n```"])
def test_zero_or_several_blocks_give_no_proposals_and_a_record(monkeypatch, text):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm({"profitability": text}, calls))
    result = rpr._run_specialist_readers(RUN_ID, run_dir)
    assert len([c for c, _ in calls if c == "profitability"]) == 2
    assert result["profitability"] == []
    assert (run_dir / "artifacts" / "debug_specialist_readers_profitability_raw_output.txt").exists()
    [drop] = _dropped(run_dir)
    assert drop["index"] is None and "exactly one is required" in drop["error"]


def test_malformed_file_already_on_disk_fails_loud_not_regenerated(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    (run_dir / "artifacts" / "proposals").mkdir(parents=True)
    (run_dir / "artifacts" / "proposals" / "profitability.yaml").write_text("{a: 1}\n", encoding="utf-8")
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(calls=calls))
    with pytest.raises(reader_proposals.ProposalError):
        rpr._run_specialist_readers(RUN_ID, run_dir)
    assert calls == []


# ---------------------------------------------------------------------------
# 5. The route from the grid
# ---------------------------------------------------------------------------

def test_validated_routes_to_promote(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="validated")
    assert rpr.determine_post_specialist_readers_route(run_dir, RUN_ID) == "holdout_evaluation"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["flags"]["walk_forward_passed"] is True
    audit = rpr.load_yaml(run_dir / "artifacts" / "promotion_audit.yaml")
    assert audit["hypothesis_id"] == "H-TEST-1"  # from hypothesis_card.yaml, not run_id
    assert not (run_dir / "artifacts" / "verdict_interpretation.yaml").exists()


def test_promote_without_hypothesis_id_fails_loud():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="validated")
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", {"title": "no id"})
    with pytest.raises(ValueError, match="hypothesis_id"):
        rpr.determine_post_specialist_readers_route(run_dir, RUN_ID)


def test_refuted_routes_to_kill_terminate(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="refuted")
    dispatched = []
    real = rpr._dispatch_verdict_route

    def _spy(path, run_id, interp, campaign, hv, lr):
        dispatched.append((interp, hv, lr))
        return real(path, run_id, interp, campaign, hv, lr)
    monkeypatch.setattr(rpr, "_dispatch_verdict_route", _spy)
    breaker = []
    monkeypatch.setattr(rpr, "_apply_circuit_breaker", lambda *a: breaker.append(a))
    assert rpr.determine_post_specialist_readers_route(run_dir, RUN_ID) == "completed_rejected"
    assert dispatched == [({}, "kill", "terminate")]
    assert breaker == []
    # code-review fix 8: no continuation_* bookkeeping under the flag
    assert "continuation_child" not in rpr.load_yaml(run_dir / "pipeline_state.yaml")


def test_inconclusive_pauses_with_inconclusive_grid():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="inconclusive")
    assert rpr.determine_post_specialist_readers_route(run_dir, RUN_ID) == "human_pause"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "paused_for_human"
    assert state["flags"] == {"inconclusive_grid": True}
    assert camp._classify_human_pause(run_dir, state) == "inconclusive_grid"
    assert dict(camp._PAUSE_FLAG_TO_REASON)["inconclusive_grid"] == "inconclusive_grid"


@pytest.mark.parametrize("idea_status", ["validated", "refuted", "inconclusive", None])
def test_component_errors_pause_first(idea_status):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status=idea_status, errors_count=3)
    assert rpr.determine_post_specialist_readers_route(run_dir, RUN_ID) == "human_pause"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["flags"] == {"component_execution_error_flagged": True}
    assert not (run_dir / "artifacts" / "promotion_audit.yaml").exists()
    assert camp._classify_human_pause(run_dir, state) == "component_execution_error"


def test_component_errors_in_a_variant_count_too():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="validated")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "v2" / "protocol_result.yaml", _protocol_result(1))
    errors = rpr._protocol_component_errors(run_dir)
    assert len(errors) == 1 and "variants/v2/protocol_result.yaml" in errors[0]


def test_component_errors_zero_or_null_do_not_pause():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(errors_count=0)
    assert rpr._protocol_component_errors(run_dir) == []


@pytest.mark.parametrize("block", [{"count": "3"}, {"samples": []}, "x", {"count": True}])
def test_malformed_component_errors_fail_loud(block):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run()
    pr = _protocol_result()
    pr["results"][0]["component_errors"] = block
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", pr)
    with pytest.raises(ValueError, match="malformed"):
        rpr.determine_post_specialist_readers_route(run_dir, RUN_ID)


def test_missing_idea_status_fails_loud():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status=None)
    with pytest.raises(FileNotFoundError, match="Refusing to guess"):
        rpr.determine_post_specialist_readers_route(run_dir, RUN_ID)
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml").get("flags") == {}


@pytest.mark.parametrize("mutate,match", [
    (lambda d: d.update(idea_status="maybe"), "not one of"),
    (lambda d: d.update(result="PASS"), "disagrees"),
    (lambda d: d.update(lineage_routing="pivot"), "disagrees"),
    (lambda d: d.update(run_id="run_001"), "stale"),
])
def test_malformed_idea_status_fails_loud(mutate, match):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="refuted")
    doc = rpr.load_yaml(run_dir / "artifacts" / "idea_status.yaml")
    mutate(doc)
    rpr.save_yaml(run_dir / "artifacts" / "idea_status.yaml", doc)
    with pytest.raises(ValueError, match=match):
        rpr.determine_post_specialist_readers_route(run_dir, RUN_ID)


def test_unparseable_idea_status_fails_loud():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status=None)
    (run_dir / "artifacts" / "idea_status.yaml").write_text("idea_status: [unclosed\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unparseable"):
        rpr.determine_post_specialist_readers_route(run_dir, RUN_ID)


def test_stage_body_skips_readers_on_component_errors_and_checks_idea_status_first(monkeypatch):
    _set_orchestrator(ALL_ON)
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(calls=calls))
    run_dir = _seed_run(idea_status=None, errors_count=2)
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert calls == []
    run_dir = _seed_run(run_id="run_991", idea_status=None)
    with pytest.raises(FileNotFoundError, match="idea_status"):
        rpr._run_specialist_readers_stage("run_991", run_dir)
    assert calls == []


# ---------------------------------------------------------------------------
# 6. Reader scores cannot change the route
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("idea_status,expected", [
    ("validated", "holdout_evaluation"), ("refuted", "completed_rejected"), ("inconclusive", "human_pause")])
def test_reader_scores_cannot_change_the_route(monkeypatch, idea_status, expected):
    _set_orchestrator(ALL_ON)
    routes = []
    for i, (n_props, score) in enumerate([(0, 0), (3, 0), (3, 3)]):
        run_id = f"run_99{i}"
        run_dir = _seed_run(run_id=run_id, idea_status=idea_status)
        pdir = run_dir / "artifacts" / "proposals"
        pdir.mkdir(parents=True)
        for c in REPORT_CATEGORIES:
            rpr.save_yaml(pdir / f"{c}.yaml", [_proposal(c, run_id, n, score) for n in range(1, n_props + 1)])
        reader_proposals.load_proposals(pdir, REPORT_CATEGORIES)  # the fixtures are valid proposals
        routes.append(rpr.determine_post_specialist_readers_route(run_dir, run_id))
    assert routes == [expected] * 3


def test_route_never_reads_proposals(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="refuted")

    def _boom(*a, **k):
        raise AssertionError("the route must not read proposals")
    monkeypatch.setattr(reader_proposals, "load_proposals", _boom)
    monkeypatch.setattr(rpr, "_reader_proposals_module", _boom)
    real_load = rpr.load_yaml

    def _guarded_load(path):
        assert "proposals" not in Path(path).parts, path
        assert Path(path).name != "verdict_interpretation.yaml", path
        return real_load(path)
    monkeypatch.setattr(rpr, "load_yaml", _guarded_load)
    assert rpr.determine_post_specialist_readers_route(run_dir, RUN_ID) == "completed_rejected"


# ---------------------------------------------------------------------------
# 7. verdict_interpreter is never invoked under the flag
# ---------------------------------------------------------------------------

def test_full_loop_under_flag_never_invokes_verdict_interpreter(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _minimal_run_at(rpr.ROOT, RUN_ID, "protocol_execution")
    _seed_run(pending="protocol_execution", idea_status="refuted")
    rpr._ensure_protocol_ref_pinned(run_dir, RUN_ID, {"protocol_ref": f"protocols/{RUN_ID}_pinned.json"})
    rpr.save_yaml(run_dir / "handoffs" / "backtest_spec_to_protocol_execution.yaml",
                  {"required_inputs": [], "deliverables": []})
    stages = []

    async def _record(stage_name, run_id, retry_context=None):
        stages.append(stage_name)
    monkeypatch.setattr(rpr, "async_invoke_agent", _record)
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(calls=calls))

    rpr.run_loop(RUN_ID)

    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert stages == ["protocol_execution"]
    assert len(calls) == 5
    assert state["completed_stages"][-2:] == ["protocol_execution", "specialist_readers"]
    assert state["pending_stage"] == "completed_rejected"
    assert "verdict_interpreter" not in state["completed_stages"]
    assert not (run_dir / "artifacts" / "verdict_interpretation.yaml").exists()


def test_pending_verdict_interpreter_under_flag_stops_without_invoking(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(pending="verdict_interpreter")
    rpr.save_yaml(run_dir / "handoffs" / "protocol_to_verdict_interpreter.yaml",
                  {"required_inputs": [], "deliverables": []})
    invoked = []
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", lambda *a, **k: invoked.append(a[0]))
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert invoked == []
    assert state["status"] == "failed" and "unreached" in state["last_error"]
