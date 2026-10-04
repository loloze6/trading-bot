"""
O-21 (operator, 2026-10-04): run_070's step 1b parked an idea as component_gap
twice, although PriceEvolutionComponent(period=1) + zscore expresses "the 1h move
in units of its usual size". It misread the component as lagged (the catalogue's
`close[-1]`) and never tried the transform pipeline.

- A component_gap must carry `tried` (decision.yaml), at least one item naming a
  transform op. Missing, or naming none: ONE 1b retry with that message; then
  the answer is accepted and the remaining problem recorded on the component
  request (`tried_warning`), never a stop.
- The catalogue says `close[-1]` is the CURRENT bar, and states PriceEvolution in
  t notation.
"""
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
REPO = SR_ROOT.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
from test_k3_protocol_pinning import _minimal_run  # noqa: E402

GOOD = [{"config": "PriceEvolutionComponent(period=1) + [zscore, negate, clip(-20,20)]",
         "fails_on": "needs ATR, not std"}]
NO_TRANSFORM = [{"config": "KeltnerBreakoutComponent(atr_period=20)", "fails_on": "EMA distance"}]


# ---------------------------------------------------------------------------
# The check
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tried,ok", [
    (None, False), ([], False), ("zscore", False),           # not a list
    (NO_TRANSFORM, False),
    ([{"config": "PriceEvolutionComponent scaled and clipboard"}], False),   # whole words only
    (GOOD, True),
    (["PriceEvolutionComponent(period=1) then percentile"], True),           # plain strings accepted
])
def test_the_tried_check(tried, ok):
    decision = {"status": "component_gap"}
    if tried is not None:
        decision["tried"] = tried
    problem = rpr._component_gap_tried_problem(decision)
    assert (problem is None) is ok
    if not ok:
        assert "tried" in problem


def test_the_transform_list_matches_the_engine_registry():
    sys.path.insert(0, str(REPO / "trading-bot"))
    from strategies.registry import TRANSFORM_OPS_REGISTRY
    assert set(rpr._TRANSFORM_OP_NAMES) | set(rpr._TRANSFORM_OPS_NOT_DETECTED) == \
        set(TRANSFORM_OPS_REGISTRY)
    assert set(rpr._TRANSFORM_OPS_NOT_DETECTED) == {"identity", "ema"}


def test_the_word_ema_in_prose_is_not_a_transform():
    """Found while testing: 'EMA distance' must not pass as a transform tried."""
    assert rpr._component_gap_tried_problem(
        {"tried": [{"config": "KeltnerBreakoutComponent", "fails_on": "EMA distance, not a move"}]})


# ---------------------------------------------------------------------------
# The route: one retry, then accept and record
# ---------------------------------------------------------------------------

def _gap_run(run_id, tried=None):
    run_dir = _minimal_run(rpr.ROOT, run_id)
    decision = {"hypothesis_id": "H-1", "stage": "strategy_config_authoring",
                "status": "component_gap", "rationale": "needs ShockComponent",
                "blocking_issues": ["engine lacks ShockComponent"]}
    if tried is not None:
        decision["tried"] = tried
    rpr.save_yaml(run_dir / "artifacts" / "decision.yaml", decision)
    return run_dir


def _requests():
    path = rpr.ROOT / "campaign_record" / "component_requests.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))["requests"] if path.exists() else []


@pytest.mark.parametrize("tried", [None, NO_TRANSFORM])
def test_an_incomplete_gap_gets_one_retry_then_is_accepted_and_recorded(tried):
    run_dir = _gap_run("run_960", tried)
    route = rpr.determine_post_strategy_config_authoring_route(run_dir, routing_retired=True)
    assert route == "strategy_config_authoring"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state[rpr._COMPONENT_GAP_RETRY_STATE_KEY]["attempts"] == 1
    assert rpr.PARKED_KEY not in state and _requests() == []
    # 1b answers the same incomplete gap again: accepted, parked, warning recorded
    route = rpr.determine_post_strategy_config_authoring_route(run_dir, routing_retired=True)
    assert route == "human_pause"
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml")[rpr.PARKED_KEY]["kind"] == "component"
    [req] = _requests()
    assert req["tried_warning"] and "tried" in req["tried_warning"]
    assert req["tried"] == (tried or [])


def test_a_complete_gap_parks_at_once_with_its_tried_list():
    run_dir = _gap_run("run_961", GOOD)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir, routing_retired=True) == \
        "human_pause"
    [req] = _requests()
    assert req["tried"] == GOOD and req["tried_warning"] is None
    assert rpr._COMPONENT_GAP_RETRY_STATE_KEY not in rpr.load_yaml(run_dir / "pipeline_state.yaml")


def test_without_retired_routing_the_retry_also_comes_first_then_the_pause():
    run_dir = _gap_run("run_962")
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "human_pause"
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml")["status"] == "paused_for_human"


def test_a_spec_ready_answer_is_untouched_by_the_check(monkeypatch):
    run_dir = _gap_run("run_963")
    rpr.save_yaml(run_dir / "artifacts" / "decision.yaml", {"status": "spec_ready"})
    monkeypatch.setattr(rpr, "_route_block_manifest_check", lambda path: "innovation_expansion")
    monkeypatch.setattr(rpr, "_record_claim_match", lambda path: None)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"


# ---------------------------------------------------------------------------
# The retry message reaches 1b
# ---------------------------------------------------------------------------

def test_the_retry_message_reaches_1b_only_when_pending(tmp_path):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "pipeline_state.yaml").write_text(yaml.safe_dump({"status": "active"}),
                                                 encoding="utf-8")
    handoff = {}
    rpr._apply_component_gap_retry_context("strategy_config_authoring", handoff, run_dir)
    assert handoff == {}
    rpr.update_state(path=run_dir, **{rpr._COMPONENT_GAP_RETRY_STATE_KEY: {
        "attempts": 1, "last_error": "component_gap without a `tried` list"}})
    rpr._apply_component_gap_retry_context("innovation_expansion", handoff, run_dir)
    assert handoff == {}
    rpr._apply_component_gap_retry_context("strategy_config_authoring", handoff, run_dir)
    msg = handoff["injected_context"]["component_gap_tried_error"]
    assert msg.startswith("Retry 1/1.") and "without a `tried` list" in msg and "DEVIATION" in msg


# ---------------------------------------------------------------------------
# The instructions
# ---------------------------------------------------------------------------

def test_the_catalogue_says_close_minus_one_is_the_current_bar():
    text = (SR_ROOT / "docs" / "COMPONENT_CATALOG.md").read_text(encoding="utf-8")
    assert "`close[-1]` is the CURRENT bar" in text
    rows = {line.split("|")[1].strip(): line for line in text.splitlines()
            if line.startswith("| `PriceEvolution")}
    assert "(close[t] - close[t-period]) / close[t-period]" in rows["`PriceEvolutionComponent`"]
    assert "close[t-comparison_period]" in rows["`PriceEvolutionOnPeriodComponent`"]
    assert all("close[-(" not in row for row in rows.values())


def test_the_1b_skill_states_the_rule():
    skill = (SR_ROOT / "workflow_artifacts" / "skills" / "strategy-config-authoring" /
             "SKILL.md").read_text(encoding="utf-8")
    rule = skill.split("**`component_gap` only after compositions are ruled out.**")[1].split("## ")[0]
    for needle in ("zscore", "`tried`", "DEVIATION", "PriceEvolutionComponent(period=1)",
                   "sends you back once"):
        assert needle in rule, needle
    assert "- tried: REQUIRED when status is component_gap" in skill
    assert "- hypothesis_id:" in skill
