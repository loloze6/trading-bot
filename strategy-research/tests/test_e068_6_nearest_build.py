"""
E-068 (operator, 2026-10-05; D-075): step 1b builds the nearest version of an
idea instead of parking it, behind orchestrator.nearest_build.enabled (off;
requires config_direct_authoring and claim_tests).

Operator decisions: a new flag (Q1); structured `deviations` in decision.yaml
(Q2); deviation request rows stay out of --unpark, the cap and decide-next's
request count (Q3). Additions: (1) `core_lost` names the claim clause that
cannot be approximated and why, recorded in the run and on the request row;
(2) deviations shown FIRST in the finding and the readers' digest, with the
line "this run tested an approximation of the idea: ", and a deviations count
on the findings-summary row; (3) CLAIM_TESTS.md prefers a forecast quantile
over an absolute threshold.

Sections: 1 the flag; 2 flag off is byte-identical; 3 the pure module;
4 1b's inputs; 5 the route (spec_ready, component_gap, run_071's real answer);
6 the finding, the summary rows and the digest; 7 decide-next's count;
8 instructions text. No LLM call, no backtest, no market data.
"""
import copy
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import nearest_build as nb  # noqa: E402
import claim_findings as cf  # noqa: E402
import reader_findings as rf  # noqa: E402
import decide_next as dn  # noqa: E402

from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
from test_e056_1b_block_manifest import GOOD, _authored_1b  # noqa: E402
from test_k3_protocol_pinning import _minimal_run  # noqa: E402

FIX = SR_ROOT / "tests" / "fixtures" / "e068_nearest_build"
FIX4 = SR_ROOT / "tests" / "fixtures" / "e068_4" / "run_070"
CDA = {"config_direct_authoring": {"enabled": True}}
NB_ON = {**CDA, "claim_tests": {"enabled": True}, "nearest_build": {"enabled": True}}
TRIED_OK = [{"config": "PriceEvolutionComponent(period=1) + [zscore, scale]",
             "fails_on": "needs the bar's own range"}]
DEVS = [
    {"clause": "body fraction > 0.7", "built_instead": "PriceEvolutionComponent(period=1) + zscore",
     "missing": "the current bar's open, high and low", "effect": "selects about half the bars"},
    {"clause": "4-bar hold", "built_instead": "none (forecast / 10 sizing)", "missing": None,
     "effect": "positions change every bar"},
]
CORE = {"clause": "close in the top 10% of the bar's own range",
        "why": "no component reads the current bar's high and low"}


def _requests():
    path = rpr.ROOT / "campaign_record" / "component_requests.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))["requests"] if path.exists() else []


def _spec_ready_run(run_id, deviations=None, rationale=None):
    run_dir = _authored_1b(run_id, GOOD)
    arts = run_dir / "artifacts"
    if deviations is not None:
        d = rpr.load_yaml(arts / "decision.yaml")
        d["deviations"] = deviations
        rpr.save_yaml(arts / "decision.yaml", d)
    if rationale is not None:
        s = rpr.load_yaml(arts / "backtest_spec.yaml")
        s["config_rationale"] = rationale
        rpr.save_yaml(arts / "backtest_spec.yaml", s)
    return run_dir


def _gap_run(run_id, tried=TRIED_OK, core_lost=None):
    run_dir = _minimal_run(rpr.ROOT, run_id)
    decision = {"hypothesis_id": "H-1", "stage": "strategy_config_authoring",
                "status": "component_gap", "rationale": "needs BodyFractionComponent",
                "blocking_issues": ["no OHLC component"], "tried": tried}
    if core_lost is not None:
        decision["core_lost"] = core_lost
    rpr.save_yaml(run_dir / "artifacts" / "decision.yaml", decision)
    return run_dir


def _record(run_dir):
    return rpr.load_yaml(run_dir / "artifacts" / nb.DEVIATIONS_FILE)


# ---------------------------------------------------------------------------
# 1. The flag
# ---------------------------------------------------------------------------

def test_flag_off_by_default_and_in_the_shipped_config():
    _set_orchestrator(CDA)
    assert rpr._nearest_build_enabled() is False
    shipped = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(
        encoding="utf-8"))
    assert shipped["orchestrator"]["nearest_build"]["enabled"] is False
    _set_orchestrator(NB_ON)
    assert rpr._nearest_build_enabled() is True


def test_flag_on_without_config_direct_authoring_raises():
    _set_orchestrator({"nearest_build": {"enabled": True}})
    with pytest.raises(ValueError, match="config_direct_authoring.enabled=true"):
        rpr._nearest_build_enabled()


def test_flag_on_without_claim_tests_raises():
    """Review round 1: the deviations go into the claim's finding, which exists
    only under claim_tests."""
    _set_orchestrator({**CDA, "nearest_build": {"enabled": True}})
    with pytest.raises(ValueError, match="claim_tests.enabled=true"):
        rpr._nearest_build_enabled()


@pytest.mark.parametrize("bad", ["true", 1, None])
def test_flag_non_bool_raises(bad):
    _set_orchestrator({**CDA, "nearest_build": {"enabled": bad}})
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._nearest_build_enabled()


def test_flag_is_registered_everywhere():
    reg = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml").read_text(
        encoding="utf-8"))
    [entry] = [f for f in reg["flags"] if f["name"] == "nearest_build"]
    assert entry["config_key"] == "orchestrator.nearest_build.enabled"
    assert entry["reader"] == "run_phase1_research._nearest_build_enabled"
    src = Path(camp.__file__).read_text(encoding="utf-8")
    assert '"nearest_build": orch._nearest_build_enabled' in src


# ---------------------------------------------------------------------------
# 2. Flag off: byte-identical
# ---------------------------------------------------------------------------

def test_flag_off_1b_handoff_is_untouched(tmp_path):
    _set_orchestrator(CDA)
    handoff = {"required_inputs": [{"path": "a"}], "injected_context": {"x": "1"}}
    before = copy.deepcopy(handoff)
    rpr._apply_nearest_build_context("strategy_config_authoring", handoff, tmp_path)
    assert handoff == before


def test_flag_off_spec_ready_with_deviations_writes_nothing():
    _set_orchestrator(CDA)
    run_dir = _spec_ready_run("run_980", deviations=DEVS)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert not (run_dir / "artifacts" / nb.DEVIATIONS_FILE).exists()
    assert _requests() == []


def test_flag_off_component_gap_without_core_lost_parks_at_once():
    """Exactly today's O-21 behaviour: a complete `tried` list parks at once."""
    _set_orchestrator(CDA)
    run_dir = _gap_run("run_981")
    assert rpr.determine_post_strategy_config_authoring_route(
        run_dir, routing_retired=True) == "human_pause"
    [req] = _requests()
    assert "core_lost" not in req and req["tried_warning"] is None
    assert not (run_dir / "artifacts" / nb.DEVIATIONS_FILE).exists()


def test_flag_off_finding_and_digest_unchanged(tmp_path):
    run070 = tmp_path / "run_070"
    shutil.copytree(FIX4, run070)
    entry = yaml.safe_load((run070 / "memory_entry.yaml").read_text(encoding="utf-8"))
    finding = cf.build_finding(run070, "run_070", entry)
    assert "approximation" not in finding and list(finding)[0] == "finding_id"
    assert "deviations" not in cf._summary_row("run_070", finding)
    assert "approximation" not in rf.claim_result_digest(run070)


# ---------------------------------------------------------------------------
# 3. The pure module
# ---------------------------------------------------------------------------

def test_structured_deviations_and_rationale_lines():
    items = nb.structured_deviations({"deviations": DEVS + ["a bare clause", {}]})
    assert [i["clause"] for i in items] == ["body fraction > 0.7", "4-bar hold", "a bare clause"]
    lines = nb.rationale_deviation_lines({"config_rationale": [
        {"hypothesis_claim": "open", "config_choice": "DEVIATION: previous close used"},
        {"hypothesis_claim": "move", "config_choice": "/strategies/... PriceEvolution"},
        "not a mapping"]})
    assert lines == [{"clause": "open", "text": "previous close used"}]


@pytest.mark.parametrize("core,ok", [(None, False), ({"clause": "x"}, False),
                                     ({"clause": " ", "why": "y"}, False), (CORE, True)])
def test_core_lost_check(core, ok):
    decision = {"status": "component_gap"} | ({"core_lost": core} if core is not None else {})
    problem = nb.core_lost_problem(decision)
    assert (problem is None) is ok
    if not ok:
        assert "core_lost" in problem and "clause" in problem


def test_the_approximation_line_is_the_operators_wording():
    assert nb.APPROX_LINE == "this run tested an approximation of the idea: "


def test_approximation_block_from_items_and_from_lines():
    rec = nb.build_record("run_1", {"status": "spec_ready", "deviations": DEVS}, {})
    block = nb.approximation_block(rec)
    assert rec["status"] == nb.STATUS_APPROXIMATION and block["n_deviations"] == 2
    assert block["line"] == (nb.APPROX_LINE + "body fraction > 0.7 -> PriceEvolutionComponent"
                             "(period=1) + zscore; 4-bar hold -> none (forecast / 10 sizing)")
    rec = nb.build_record("run_1", {"status": "spec_ready"}, {"config_rationale": [
        {"hypothesis_claim": "open", "config_choice": "DEVIATION: previous close"}]})
    assert nb.approximation_block(rec)["line"] == nb.APPROX_LINE + "open -> previous close"
    exact = nb.build_record("run_1", {"status": "spec_ready"}, {})
    assert exact["status"] == nb.STATUS_EXACT and nb.approximation_block(exact) is None
    parked = nb.build_record("run_1", {"status": "component_gap", "core_lost": CORE,
                                       "tried": TRIED_OK}, {})
    assert parked["status"] == nb.STATUS_PARKED and parked["core_lost"] == CORE
    assert nb.approximation_block(parked) is None


def test_request_rows_only_for_missing_pieces():
    rec = nb.build_record("run_1", {"status": "spec_ready", "deviations": DEVS}, {})
    [row] = nb.request_rows("run_1", rec)
    assert row["kind"] == "deviation" and row["run_continued"] is True
    assert row["reason"] == "deviation: the current bar's open, high and low"
    assert nb.request_rows("run_1", nb.build_record("run_1", {"status": "component_gap"}, {})) == []


# ---------------------------------------------------------------------------
# 4. 1b's inputs
# ---------------------------------------------------------------------------

def test_flag_on_1b_gets_the_note_once_and_other_stages_nothing(tmp_path):
    _set_orchestrator(NB_ON)
    handoff = {"required_inputs": []}
    rpr._apply_nearest_build_context("strategy_config_authoring", handoff, tmp_path)
    rpr._apply_nearest_build_context("strategy_config_authoring", handoff, tmp_path)
    assert [r["path"] for r in handoff["required_inputs"]] == [rpr.NEAREST_BUILD_NOTE]
    other = {"required_inputs": []}
    rpr._apply_nearest_build_context("innovation_expansion", other, tmp_path)
    assert other == {"required_inputs": []}
    note = SR_ROOT / "workflow_artifacts" / "skills" / "strategy-config-authoring" / "NEAREST_BUILD.md"
    # run-relative, like CLAIM_NOTE.md: runs/<run>/../../workflow_artifacts/...
    assert (SR_ROOT / "runs" / "run_x" / rpr.NEAREST_BUILD_NOTE).resolve() == note.resolve()
    assert note.is_file()


def test_the_1b_skill_is_untouched():
    skill = (SR_ROOT / "workflow_artifacts" / "skills" / "strategy-config-authoring" /
             "SKILL.md").read_text(encoding="utf-8")
    assert "nearest_build" not in skill and "core_lost" not in skill


def test_a_stale_record_is_cleared_when_1b_starts():
    run_dir = _minimal_run(rpr.ROOT, "run_982")
    path = run_dir / "artifacts" / nb.DEVIATIONS_FILE
    path.write_text("status: approximation\n", encoding="utf-8")
    rpr._clear_stale_deviations("innovation_expansion", run_dir)
    assert path.exists()
    rpr._clear_stale_deviations("strategy_config_authoring", run_dir)
    assert not path.exists()


# ---------------------------------------------------------------------------
# 5. The route
# ---------------------------------------------------------------------------

def test_spec_ready_with_deviations_continues_and_records(capsys):
    _set_orchestrator(NB_ON)
    run_dir = _spec_ready_run("run_983", deviations=DEVS)
    assert rpr.determine_post_strategy_config_authoring_route(
        run_dir, routing_retired=True) == "innovation_expansion"
    rec = _record(run_dir)
    assert rec["status"] == "approximation" and len(rec["deviations"]) == 2
    assert rpr.PARKED_KEY not in (rpr.load_yaml(run_dir / "pipeline_state.yaml") or {})
    [req] = _requests()
    assert req["kind"] == "deviation" and req["run_continued"] is True and req["run_id"] == "run_983"
    assert nb.APPROX_LINE in capsys.readouterr().out
    # a resumed route does not duplicate the request row
    rpr.determine_post_strategy_config_authoring_route(run_dir, routing_retired=True)
    assert len(_requests()) == 1


def test_spec_ready_exact_records_no_request():
    _set_orchestrator(NB_ON)
    run_dir = _spec_ready_run("run_984")
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert _record(run_dir)["status"] == "exact" and _requests() == []


def test_a_manifest_retry_records_nothing_yet():
    _set_orchestrator(NB_ON)
    run_dir = _spec_ready_run("run_985", deviations=DEVS)
    (run_dir / "artifacts" / "block_manifest.yaml").unlink()
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    assert not (run_dir / "artifacts" / nb.DEVIATIONS_FILE).exists() and _requests() == []


def test_component_gap_without_core_lost_gets_one_retry_then_parks():
    _set_orchestrator(NB_ON)
    run_dir = _gap_run("run_986")
    assert rpr.determine_post_strategy_config_authoring_route(
        run_dir, routing_retired=True) == "strategy_config_authoring"
    retry = rpr.load_yaml(run_dir / "pipeline_state.yaml")[rpr._COMPONENT_GAP_RETRY_STATE_KEY]
    assert retry["attempts"] == 1 and "core_lost" in retry["last_error"]
    handoff = {}
    rpr._apply_component_gap_retry_context("strategy_config_authoring", handoff, run_dir)
    assert "core_lost" in handoff["injected_context"]["component_gap_tried_error"]
    # the same answer again: accepted, parked, the gap recorded
    assert rpr.determine_post_strategy_config_authoring_route(
        run_dir, routing_retired=True) == "human_pause"
    [req] = _requests()
    assert req["core_lost"] is None and "core_lost" in req["tried_warning"]
    assert _record(run_dir)["status"] == "parked"


def test_component_gap_with_core_lost_parks_at_once_and_records_it(capsys):
    _set_orchestrator(NB_ON)
    run_dir = _gap_run("run_987", core_lost=CORE)
    assert rpr.determine_post_strategy_config_authoring_route(
        run_dir, routing_retired=True) == "human_pause"
    [req] = _requests()
    assert req["core_lost"] == CORE and req["tried_warning"] is None
    rec = _record(run_dir)
    assert rec["status"] == "parked" and rec["core_lost"] == CORE and rec["tried"] == TRIED_OK
    assert "the core is lost" in capsys.readouterr().out


def test_one_retry_message_carries_both_missing_fields():
    """Review round 1: no `tried` AND no `core_lost` -> the single retry names both."""
    _set_orchestrator(NB_ON)
    run_dir = _gap_run("run_991", tried=None)
    assert rpr.determine_post_strategy_config_authoring_route(
        run_dir, routing_retired=True) == "strategy_config_authoring"
    err = rpr.load_yaml(run_dir / "pipeline_state.yaml")[rpr._COMPONENT_GAP_RETRY_STATE_KEY][
        "last_error"]
    assert "without a `tried` list" in err and "core_lost" in err
    handoff = {}
    rpr._apply_component_gap_retry_context("strategy_config_authoring", handoff, run_dir)
    msg = handoff["injected_context"]["component_gap_tried_error"]
    assert msg.endswith("answer component_gap again with a complete `tried` list and "
                        "`core_lost` in decision.yaml.")


def test_flag_off_retry_message_is_unchanged():
    _set_orchestrator(CDA)
    run_dir = _gap_run("run_992", tried=None)
    rpr.determine_post_strategy_config_authoring_route(run_dir, routing_retired=True)
    handoff = {}
    rpr._apply_component_gap_retry_context("strategy_config_authoring", handoff, run_dir)
    msg = handoff["injected_context"]["component_gap_tried_error"]
    assert "core_lost" not in msg and msg.endswith(
        "Either build the closest composition (spec_ready, with a DEVIATION entry in "
        "config_rationale) or answer component_gap again with a complete `tried` list in "
        "decision.yaml.")


def test_model_written_deviations_are_bounded():
    many = [{"clause": f"clause {i} " + "x" * 400, "built_instead": "b", "missing": f"m{i}",
             "effect": None} for i in range(nb.MAX_ITEMS + 2)]
    rec = nb.build_record("run_1", {"status": "spec_ready", "deviations": many}, {})
    assert len(rec["deviations"]) == nb.MAX_ITEMS and rec["deviations_not_listed"] == 2
    assert all(len(d["clause"]) <= nb.MAX_CHARS for d in rec["deviations"])
    block = nb.approximation_block(rec)
    assert block["n_deviations"] == nb.MAX_ITEMS + 2
    assert block["line"].endswith("; and 2 more (not listed)")
    assert len(nb.request_rows("run_1", rec)) == nb.MAX_ITEMS
    lines = nb.rationale_deviation_lines({"config_rationale": [
        {"hypothesis_claim": str(i), "config_choice": "DEVIATION: x"} for i in range(30)]})
    assert len(lines) == nb.MAX_ITEMS


def test_two_deviations_with_the_same_missing_piece_keep_two_rows():
    _set_orchestrator(NB_ON)
    same = [{"clause": "body", "built_instead": "a", "missing": "OHLC", "effect": None},
            {"clause": "close location", "built_instead": "none", "missing": "OHLC",
             "effect": None}]
    run_dir = _spec_ready_run("run_993", deviations=same)
    rpr.determine_post_strategy_config_authoring_route(run_dir)
    assert [r["clause"] for r in _requests()] == ["body", "close location"]


def test_run_071s_real_answer_is_sent_back_for_the_nearest_build():
    """run_071's 1b parked at once (complete `tried`, O-21 satisfied). Under the
    flag the same answer has no core_lost, so 1b is asked once for the nearest build."""
    decision = yaml.safe_load((FIX / "run_071_decision.yaml").read_text(encoding="utf-8"))
    assert decision["status"] == "component_gap" and rpr._component_gap_tried_problem(decision) is None
    run_dir = _minimal_run(rpr.ROOT, "run_988")
    rpr.save_yaml(run_dir / "artifacts" / "decision.yaml", decision)
    _set_orchestrator(CDA)
    assert rpr._route_component_gap_tried(run_dir, decision) == (None, None)  # today: parks
    _set_orchestrator(NB_ON)
    route, warning = rpr._route_component_gap_tried(run_dir, decision)
    assert route == "strategy_config_authoring" and warning is None


def test_the_record_never_raises(monkeypatch, capsys):
    _set_orchestrator(NB_ON)
    run_dir = _spec_ready_run("run_989", deviations=DEVS)

    def _boom(*a, **k):
        raise RuntimeError("disk full")
    monkeypatch.setattr(nb, "build_record", _boom)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert "nearest-build record could not be written" in capsys.readouterr().out


def test_claim_match_carries_the_approximation_line():
    _set_orchestrator({**NB_ON, "claim_tests": {"enabled": True}})
    run_dir = _spec_ready_run("run_990", deviations=DEVS)
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", {"hypothesis_id": "H-1"})
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    doc = rpr.load_yaml(run_dir / "artifacts" / "claim_match.yaml")
    assert doc["approximation"].startswith(nb.APPROX_LINE)


# ---------------------------------------------------------------------------
# 6. The finding, the summary rows and the digest
# ---------------------------------------------------------------------------

@pytest.fixture
def run070_approx(tmp_path) -> Path:
    dst = tmp_path / "run_070"
    shutil.copytree(FIX4, dst)
    rec = nb.build_record("run_070", {"status": "spec_ready", "deviations": DEVS}, {})
    (dst / "artifacts" / nb.DEVIATIONS_FILE).write_text(yaml.safe_dump(rec), encoding="utf-8")
    return dst


def test_the_finding_says_approximation_first(run070_approx):
    entry = yaml.safe_load((run070_approx / "memory_entry.yaml").read_text(encoding="utf-8"))
    finding = cf.build_finding(run070_approx, "run_070", entry)
    assert list(finding)[0] == "approximation"
    assert finding["approximation"]["line"].startswith(nb.APPROX_LINE)
    assert finding["approximation"]["n_deviations"] == 2
    # everything else is the same finding as without the record
    (run070_approx / "artifacts" / nb.DEVIATIONS_FILE).unlink()
    plain = cf.build_finding(run070_approx, "run_070", entry)
    assert {k: v for k, v in finding.items() if k != "approximation"} == plain


def test_the_summary_rows_carry_a_deviations_count(run070_approx):
    entry = yaml.safe_load((run070_approx / "memory_entry.yaml").read_text(encoding="utf-8"))
    finding = cf.build_finding(run070_approx, "run_070", entry)
    row = cf._summary_row("run_070", finding)
    assert list(row)[0] == "deviations" and row["deviations"] == 2
    memory = {"runs": {"run_070": {"recorded_at": "t1", cf.FINDING_KEY: finding}}}
    [r] = rf.reader_findings_summary(memory, "run_071")["findings"]
    assert list(r)[0] == "deviations" and r["deviations"] == 2


def test_the_digest_says_approximation_before_the_claim(run070_approx):
    d = rf.claim_result_digest(run070_approx)
    keys = list(d)
    assert "approximation" in d and keys.index("approximation") < keys.index("statement")
    assert d["approximation"]["line"].startswith(nb.APPROX_LINE)
    assert "status" not in d   # no error


# ---------------------------------------------------------------------------
# 7. Decide-next's request count
# ---------------------------------------------------------------------------

def test_deviation_rows_are_not_counted():
    rows = [{"run_id": "r1", "reason": "park"}, {"run_id": "r2", "kind": "deviation"},
            {"run_id": "r3", "kind": "deviation"}, "odd"]
    assert dn.requests_count({"requests": rows}) == 2
    assert dn.requests_count({}) == 0 and dn.requests_count(None) == 0


# ---------------------------------------------------------------------------
# 8. Instructions text
# ---------------------------------------------------------------------------

def test_claim_tests_md_prefers_a_forecast_quantile():
    text = (SR_ROOT / "workflow_artifacts" / "skills" / "hypothesis-design" /
            "CLAIM_TESTS.md").read_text(encoding="utf-8")
    assert "step 1b, not you, chooses the forecast's scale" in text
    assert 'selector:  {kind: event, field: forecast, op: ">=", value: 12}' not in text


def test_the_note_states_the_rules():
    text = (SR_ROOT / "workflow_artifacts" / "skills" / "strategy-config-authoring" /
            "NEAREST_BUILD.md").read_text(encoding="utf-8")
    for needle in ("deviations:", "built_instead", "missing", "core_lost:", "clause:",
                   "spec_ready", "previous close"):
        assert needle in text
