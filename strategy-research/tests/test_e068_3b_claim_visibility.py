"""E-068 3b: can the claim's tests SEE the block 1b built, and the ONE claim
revision after 1b.

Covers:
  1. claim_card.block_visibility: ok / blind / not_applicable for forecast and
     regime blocks; run_070's real claim + manifest -> blind;
  2. artifacts/claim_match.yaml carries the claim-level `block_visibility`;
  3. _claim_revision_after_1b: no call when the tests see the block; one call
     when blind; accepted only if code passes it with statement and kind
     unchanged; spliced into the card and its numbered twin, the queued copies
     byte-unchanged; refused answers keep the original; one call across a
     resume (state key `claim_revision`, never the 1a retry key); budget skip;
     a still-blind valid revision kept with a warning; the power bound;
  4. the flag: off -> no file, no call; the skill is a flag-on-only input;
  5. the files are cleared at 1a/1b entry.

INFORMATION ONLY throughout: the route never changes, nothing raises. No real
LLM call (the call function is replaced), no backtest, no market data.
"""
import copy
import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import claim_card as cc  # noqa: E402

from test_k3_protocol_pinning import _minimal_run  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
from test_e056_1b_block_manifest import GOOD, _authored_1b  # noqa: E402
from test_e068_s2_claim_card import CARD, REGIME, UPPER, _claim  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures" / "e068_3b"
ON = {"config_direct_authoring": {"enabled": True}, "claim_tests": {"enabled": True}}
REGIME_MANIFEST = {"block": {"kind": "regime", "config_paths": ["/regime_detector"]},
                   "scaffolding": ["/strategies"], "rationale": "the detector is the idea"}

CLOSE_Q = {"name": "close_level",
           "selector": {"kind": "quantile", "field": "close", "side": "top", "q": 0.1,
                        "lookback": 100},
           "outcome": {"kind": "fwd_return", "horizons": [1, 2]},
           "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "less",
           "floor": {"min_events": 50}}
MOVE_Q = dict(copy.deepcopy(CLOSE_Q), name="big_moves",
              selector={"kind": "quantile", "field": "past_return", "bars": 1, "side": "top",
                        "q": 0.1, "lookback": 100})
FC_Q = dict(copy.deepcopy(CLOSE_Q), name="forecast_top",
            selector={"kind": "quantile", "field": "forecast", "side": "top", "q": 0.1,
                      "lookback": 100})
IC_ALL = {"name": "ic", "selector": {"kind": "all"},
          "outcome": {"kind": "fwd_return", "horizons": [1]}, "statistic": "rank_ic",
          "direction": "greater", "floor": {"min_blocks": 30}}
OTHER_SEL_FC = dict(copy.deepcopy(CLOSE_Q), name="vs_forecast",
                    selector={"kind": "all"},
                    baseline={"kind": "other_selector",
                              "selector": {"kind": "event", "field": "forecast", "op": ">",
                                           "value": 5}})
REGIME_CHANGE = {"name": "flip", "selector": {"kind": "regime_change", "to": "trending"},
                 "outcome": {"kind": "trend_ends", "horizons": [24]},
                 "baseline": {"kind": "placebo"}, "statistic": "hit_rate",
                 "direction": "greater", "floor": {"min_events": 30}}


def _c(*tests, **kw):
    return _claim(tests=[copy.deepcopy(t) for t in tests], **kw)


# ---------------------------------------------------------------------------
# 1. block_visibility
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tests,kind,want", [
    ((UPPER,), "forecast", "ok"),                      # event on forecast
    ((FC_Q,), "forecast", "ok"),                       # quantile on forecast
    ((IC_ALL,), "forecast", "ok"),                     # rank_ic reads the forecast
    ((OTHER_SEL_FC,), "forecast", "ok"),               # the baseline's selector reads it
    ((CLOSE_Q,), "forecast", "blind"),                 # price level only
    ((MOVE_Q,), "forecast", "blind"),                  # a past move only
    ((CLOSE_Q, UPPER), "forecast", "ok"),              # ANY test is enough
    ((CLOSE_Q, MOVE_Q), "forecast", "blind"),
    ((REGIME,), "regime", "ok"),
    ((REGIME_CHANGE,), "regime", "ok"),
    ((UPPER,), "regime", "blind"),                     # forecast is not the regime
    ((CLOSE_Q, REGIME_CHANGE), "regime", "ok"),
    ((REGIME,), "forecast", "blind"),
])
def test_block_visibility(tests, kind, want):
    assert cc.block_visibility(_c(*tests), kind) == want


@pytest.mark.parametrize("claim,kind", [
    (None, "forecast"),
    ("not a mapping", "forecast"),
    (_claim(kind="lead_lag", tests="none", missing_block="x"), "forecast"),
    (_claim(tests=None, criteria_refs=["realized_edge_to_cost_ratio"]), "forecast"),
    (_claim(tests=[]), "forecast"),
    (_claim(), None),                                  # no manifest
    (_claim(), "detector"),                            # a kind with no column
])
def test_block_visibility_not_applicable(claim, kind):
    assert cc.block_visibility(claim, kind) == "not_applicable"


def test_run_070_real_claim_and_manifest_are_blind():
    card = yaml.safe_load((FIXTURES / "run_070_hypothesis_card.yaml").read_text(encoding="utf-8"))
    manifest = yaml.safe_load((FIXTURES / "run_070_block_manifest.yaml").read_text(encoding="utf-8"))
    assert manifest["block"]["kind"] == "forecast"
    assert cc.block_visibility(card["claim"], manifest["block"]["kind"]) == "blind"


# ---------------------------------------------------------------------------
# 2. claim_match.yaml
# ---------------------------------------------------------------------------

@pytest.fixture
def no_revision_call(monkeypatch):
    async def _never(prompt):
        pytest.fail("no LLM call expected")
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _never)


@pytest.mark.parametrize("claim,want", [(_claim(), "ok"), (_c(CLOSE_Q), "blind"),
                                        (_claim(kind="lead_lag", tests="none",
                                                missing_block="x"), "not_applicable")])
def test_claim_match_records_block_visibility(claim, want, no_revision_call):
    _set_orchestrator(ON)
    run_dir = _authored_1b("run_950", GOOD)
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=claim))
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    doc = rpr.load_yaml(run_dir / "artifacts" / "claim_match.yaml")
    assert doc["block_visibility"] == want


@pytest.mark.parametrize("claim,want", [(_claim(), "ok"), (_c(CLOSE_Q), "blind")])
def test_a_decide_next_patch_card_is_matched_on_the_code_written_manifest(
        claim, want, monkeypatch, no_revision_call):
    """CUL-405 + CUL-406 through the real 1b route: 1b edited the manifest's
    rationale (run_072); code writes the brief's manifest back, and the patch
    card's own claim gets a real visibility result instead of `exempt`."""
    if want == "blind":   # a blind claim asks for the one revision: none here
        monkeypatch.setattr(rpr, "_claim_revision_after_1b", lambda *a, **k: None)
    _set_orchestrator(ON)
    run_dir = _authored_1b("run_953", GOOD)
    arts = run_dir / "artifacts"
    source_manifest = rpr.load_yaml(arts / "block_manifest.yaml")
    rpr.save_yaml(arts / "research_brief.yaml", {"candidate": {
        "manifest": copy.deepcopy(source_manifest),
        "source": {"expected_config_sha256": "c" * 64,
                   "expected_manifest_sha256": rpr._canonical_json_sha256(source_manifest)}}})
    edited = dict(copy.deepcopy(source_manifest), rationale="edited by 1b")
    rpr.save_yaml(arts / "block_manifest.yaml", edited)
    rpr.save_yaml(arts / "hypothesis_card.yaml", dict(CARD, claim=claim, pass_through=True))
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert rpr.load_yaml(arts / "block_manifest.yaml") == source_manifest
    doc = rpr.load_yaml(arts / "claim_match.yaml")
    assert doc.get("status") != "exempt" and doc["block_visibility"] == want


def test_claim_match_exempt_is_not_applicable(monkeypatch, no_revision_call):
    _set_orchestrator(ON)
    run_dir = _authored_1b("run_951", GOOD)
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_c(CLOSE_Q)))
    monkeypatch.setattr(rpr, "_claim_check_exempt", lambda *a: "composition run")
    rpr._record_claim_match(run_dir)
    doc = rpr.load_yaml(run_dir / "artifacts" / "claim_match.yaml")
    assert doc == {"status": "exempt", "reason": "composition run",
                   "block_visibility": "not_applicable"}


# ---------------------------------------------------------------------------
# 3. the one claim revision after 1b
# ---------------------------------------------------------------------------

class FakeLLM:
    def __init__(self, *answers):
        self.answers = list(answers)
        self.prompts = []

    async def __call__(self, prompt):
        self.prompts.append(prompt)
        answer = self.answers.pop(0)
        if isinstance(answer, BaseException):
            raise answer
        return answer, {"usage": {"input_tokens": 100, "output_tokens": 50},
                        "cost_usd": 0.002, "num_turns": 1}


def _answer(claim: dict) -> str:
    return "```yaml\n# claim.yaml\n" + yaml.safe_dump({"claim": claim}, sort_keys=False) + "```\n"


def _revised(claim: dict, *tests, **kw) -> dict:
    """The answer's claim: statement and kind omitted (code keeps them)."""
    out = {k: v for k, v in claim.items() if k not in ("statement", "kind", "tests")}
    out["tests"] = [copy.deepcopy(t) for t in tests]
    out.update(kw)
    return out


@pytest.fixture
def blind_run(monkeypatch):
    """A flag-on run past 1b: forecast manifest, a card whose only test reads
    the close's level (blind), a numbered twin, another card, queued copies."""
    monkeypatch.chdir(SR_ROOT)          # _build_stage_prompt reads ./workflow_artifacts
    _set_orchestrator(ON)
    run_id = "run_960"
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    (arts / "block_manifest.yaml").write_text(yaml.safe_dump(GOOD), encoding="utf-8")
    card = dict(CARD, claim=_c(CLOSE_Q))
    rpr.save_yaml(arts / "hypothesis_card.yaml", card)
    rpr.save_yaml(arts / "hypothesis_card_1.yaml", card)                 # the kept card's twin
    other = dict(CARD, hypothesis_id="H-2", claim=_c(CLOSE_Q))
    rpr.save_yaml(arts / "hypothesis_card_2.yaml", other)
    qdir = rpr.ROOT / "campaign_record" / "queued_cards" / run_id
    qdir.mkdir(parents=True)
    rpr.save_yaml(qdir / "hypothesis_card_2.yaml", other)
    rpr.save_yaml(qdir / "hypothesis_card_1.yaml", card)
    rpr.update_state(path=run_dir, claim_check_retry={"attempts": 0, "last_error": None,
                                                      "last_check": None})
    return run_dir


def _queued_bytes(run_dir):
    qdir = rpr.ROOT / "campaign_record" / "queued_cards" / run_dir.name
    return {p.name: p.read_bytes() for p in sorted(qdir.iterdir())}


def _rev(run_dir):
    return rpr.load_yaml(run_dir / "artifacts" / "claim_revision.yaml")


def _state(run_dir):
    return rpr.load_yaml(run_dir / "pipeline_state.yaml")


def test_no_call_when_the_tests_see_the_block(monkeypatch, no_revision_call):
    monkeypatch.chdir(SR_ROOT)
    _set_orchestrator(ON)
    run_dir = _authored_1b("run_961", GOOD)
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", dict(CARD, claim=_claim()))
    rpr._claim_revision_after_1b(run_dir, "run_961")
    doc = _rev(run_dir)
    assert doc["status"] == "not_needed" and doc["visibility_before"] == "ok"
    assert rpr.CLAIM_REVISION_STATE_KEY not in _state(run_dir)
    assert rpr.CLAIM_REVISION_AUDIT_KEY not in _state(run_dir)["audit_log"]


def test_blind_claim_gets_one_revision_spliced_into_card_and_twin(blind_run, monkeypatch):
    run_dir = blind_run
    old = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]
    queued_before = _queued_bytes(run_dir)
    other_before = (run_dir / "artifacts" / "hypothesis_card_2.yaml").read_bytes()
    fake = FakeLLM(_answer(_revised(old, FC_Q)))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", fake)
    rpr._claim_revision_after_1b(run_dir, run_dir.name)

    assert len(fake.prompts) == 1
    prompt = fake.prompts[0]
    assert rpr.CLAIM_BLIND_MESSAGE == ("your tests cannot see the block: base and variants "
                                       "would measure the same")
    assert rpr.CLAIM_BLIND_MESSAGE in " ".join(prompt.split())    # yaml.dump wraps it
    skill = (SR_ROOT / "workflow_artifacts" / "skills" / "claim-revision" / "SKILL.md")
    assert skill.read_text(encoding="utf-8").splitlines()[0] in prompt
    assert "CLAIM_TESTS.md: the claim block and its test slots" in prompt
    assert "the RSI pullback component is the idea" in prompt          # the manifest
    assert "close_level" in prompt                                     # the card

    doc = _rev(run_dir)
    assert doc["status"] == "accepted" and doc["visibility_before"] == "blind"
    assert doc["visibility_after"] == "ok" and "warning" not in doc
    assert doc["claim_before"] == old and doc["message"] == rpr.CLAIM_BLIND_MESSAGE
    new = doc["claim_after"]
    assert new["statement"] == old["statement"] and new["kind"] == old["kind"]
    assert [t["name"] for t in new["tests"]] == ["forecast_top"]
    assert doc["cards_updated"] == ["hypothesis_card.yaml", "hypothesis_card_1.yaml"]
    for name in ("hypothesis_card.yaml", "hypothesis_card_1.yaml"):
        assert rpr.load_yaml(run_dir / "artifacts" / name)["claim"] == new
    # the twin stays a twin: _claim_card_paths still sees one card for it
    assert [p.name for p in rpr._claim_card_paths(run_dir)] == ["hypothesis_card.yaml",
                                                                "hypothesis_card_2.yaml"]
    assert (run_dir / "artifacts" / "hypothesis_card_2.yaml").read_bytes() == other_before
    assert _queued_bytes(run_dir) == queued_before                     # never touched
    # the checks re-ran on the revised card
    status = rpr.load_yaml(run_dir / "artifacts" / "claim_test_status.yaml")
    assert status["usable"] is True and [t["name"] for t in status["tests"]] == ["forecast_top"]
    assert rpr.load_yaml(run_dir / "artifacts" / "claim_match.yaml")["block_visibility"] == "ok"
    state = _state(run_dir)
    assert state[rpr.CLAIM_REVISION_STATE_KEY]["revision_called"] is True
    assert rpr.CLAIM_REVISION_AUDIT_KEY == "claim_revision_attempt_0"
    assert state["audit_log"][rpr.CLAIM_REVISION_AUDIT_KEY]["tokens"]["input"] == 100
    # the 1a retry's state key is not this one, and is left as it was
    assert rpr.CLAIM_REVISION_STATE_KEY != rpr.CLAIM_RETRY_STATE_KEY
    assert state[rpr.CLAIM_RETRY_STATE_KEY] == {"attempts": 0, "last_error": None,
                                                "last_check": None}


@pytest.mark.parametrize("bad,why", [
    ("no block at all", "fenced YAML block"),
    ("```yaml\nclaim: [unclosed\n```", "not YAML"),
    ("```yaml\nclaim:\n  tests: []\n```\n```yaml\nclaim: {}\n```", "fenced YAML block"),
    ("```yaml\nnot_claim: {}\n```", "exactly one key"),
    ("REVISED_WITH_ALPHA", "check_claim"),
    ("CHANGED_STATEMENT", "claim.statement was changed"),
    ("CHANGED_KIND", "claim.kind was changed"),
])
def test_refused_answer_keeps_the_original(blind_run, monkeypatch, bad, why):
    run_dir = blind_run
    card_before = (run_dir / "artifacts" / "hypothesis_card.yaml").read_bytes()
    twin_before = (run_dir / "artifacts" / "hypothesis_card_1.yaml").read_bytes()
    old = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]
    if bad == "REVISED_WITH_ALPHA":
        bad = _answer(_revised(old, dict(FC_Q, alpha=0.1)))
    elif bad == "CHANGED_STATEMENT":
        bad = _answer(dict(_revised(old, FC_Q), statement=old["statement"] + " (and more)"))
    elif bad == "CHANGED_KIND":
        bad = _answer(dict(_revised(old, FC_Q), kind="direction_forecast"))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(bad))
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    doc = _rev(run_dir)
    assert doc["status"] == "refused" and why in doc["reason"]
    assert doc["claim_after"] == old and doc["visibility_after"] == "blind"
    assert (run_dir / "artifacts" / "hypothesis_card.yaml").read_bytes() == card_before
    assert (run_dir / "artifacts" / "hypothesis_card_1.yaml").read_bytes() == twin_before


def test_statement_and_kind_copied_unchanged_are_accepted(blind_run, monkeypatch):
    run_dir = blind_run
    old = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]
    answer = dict(_revised(old, IC_ALL), statement=old["statement"], kind=old["kind"])
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(_answer(answer)))
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    assert _rev(run_dir)["status"] == "accepted"


def test_a_valid_but_still_blind_revision_is_kept_with_a_warning(blind_run, monkeypatch):
    run_dir = blind_run
    old = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(_answer(_revised(old, MOVE_Q))))
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    doc = _rev(run_dir)
    assert doc["status"] == "accepted" and doc["visibility_after"] == "blind"
    assert "still cannot see the block" in doc["warning"]
    assert rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]["tests"][0][
        "name"] == "big_moves"


def test_one_call_across_a_resume(blind_run, monkeypatch):
    """The state key is written BEFORE the call: a crash inside it, a resume, a
    1b re-run (which clears claim_revision.yaml) -- never a second call."""
    run_dir = blind_run
    fake = FakeLLM(RuntimeError("the process died mid-call"))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", fake)
    rpr._claim_revision_after_1b(run_dir, run_dir.name)                # never raises
    assert _rev(run_dir)["status"] == "error" and "mid-call" in _rev(run_dir)["error"]
    rpr._clear_claim_revision_files("strategy_config_authoring", run_dir)
    assert not (run_dir / "artifacts" / "claim_revision.yaml").exists()
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    assert len(fake.prompts) == 1
    doc = _rev(run_dir)
    assert doc["status"] == "skipped" and "one per run" in doc["reason"]
    # the history survives the cleared file: it comes from the state key
    old = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]
    assert doc["claim_before"] == old and doc["card_holds_revised_claim"] is False
    assert doc["previous"]["visibility_before"] == "blind"
    assert doc["previous"]["status"] == "error"


def test_a_pending_1a_claim_retry_does_not_block_the_revision(blind_run, monkeypatch):
    run_dir = blind_run
    rpr.update_state(path=run_dir, claim_check_retry={"attempts": 1, "last_error": "x",
                                                      "last_check": "claim"})
    old = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(_answer(_revised(old, FC_Q))))
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    assert _rev(run_dir)["status"] == "accepted"
    assert _state(run_dir)[rpr.CLAIM_RETRY_STATE_KEY]["attempts"] == 1   # untouched


def test_over_budget_skips_and_records(blind_run, monkeypatch, no_revision_call):
    run_dir = blind_run
    rpr.update_state(path=run_dir, audit_log={"hypothesis_generation_attempt_0": {
        "tokens": {"weighted": 10.0 ** 12}}})
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    doc = _rev(run_dir)
    assert doc["status"] == "skipped_budget" and "budget" in doc["reason"]
    assert rpr.CLAIM_REVISION_STATE_KEY not in _state(run_dir)


def test_an_unreachable_floor_refuses_the_revision(blind_run, monkeypatch):
    run_dir = blind_run
    proto = rpr.ROOT / "protocols" / f"{run_dir.name}_generated.json"
    proto.parent.mkdir(parents=True, exist_ok=True)
    proto.write_text(json.dumps({"windows": [{"test": {"start": "2022-01-01",
                                                        "end": "2022-01-02"}}],
                                 "symbols": ["BTCUSDT"], "timeframe": "1h"}))
    old = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]
    big_floor = dict(FC_Q, floor={"min_events": 1000})                # 48 bars // 2 < 1000
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(_answer(_revised(old, big_floor))))
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    doc = _rev(run_dir)
    assert doc["status"] == "refused" and doc["reason"].startswith("power:")
    assert rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"] == old


def test_exempt_and_regime_blocks(blind_run, monkeypatch):
    run_dir = blind_run
    arts = run_dir / "artifacts"
    # a regime block whose claim reads the regime: no call
    (arts / "block_manifest.yaml").write_text(yaml.safe_dump(REGIME_MANIFEST), encoding="utf-8")
    rpr.save_yaml(arts / "hypothesis_card.yaml", dict(CARD, claim=_c(REGIME_CHANGE)))
    async def _never(prompt):
        pytest.fail("no call")
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _never)
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    assert _rev(run_dir)["status"] == "not_needed"
    assert _rev(run_dir)["visibility_before"] == "ok"
    # exempt (a composition run): not applicable, no call
    monkeypatch.setattr(rpr, "_claim_check_exempt", lambda *a: "composition run")
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    assert _rev(run_dir)["status"] == "not_applicable"


def test_a_bug_inside_is_recorded_never_raised(blind_run, monkeypatch):
    run_dir = blind_run

    def _boom(*a, **k):
        raise KeyError("bug")
    monkeypatch.setattr(cc, "block_visibility", _boom)
    assert rpr._claim_revision_after_1b(run_dir, run_dir.name) is None
    assert _rev(run_dir)["status"] == "error"


def test_the_route_is_never_changed(blind_run, monkeypatch):
    """Through run_loop's own route call: innovation_expansion either way."""
    run_dir = blind_run
    rpr.save_yaml(run_dir / "artifacts" / "decision.yaml",
                  {"stage": "strategy_config_authoring", "status": "spec_ready",
                   "rationale": "x", "blocking_issues": []})
    rpr.save_yaml(run_dir / "artifacts" / "backtest_spec.yaml",
                  {"status": "spec_ready", "config": {}, "config_rationale": ["x"],
                   "component_gap": None})
    monkeypatch.setattr(rpr, "_route_block_manifest_check", lambda p: "innovation_expansion")
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"


# ---------------------------------------------------------------------------
# 4. the flag
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("orch", [None, {"config_direct_authoring": {"enabled": True}},
                                  {"config_direct_authoring": {"enabled": True},
                                   "claim_tests": {"enabled": False}}],
                         ids=["no_config", "cda_only", "explicit_off"])
def test_flag_off_no_file_no_call(orch, monkeypatch, no_revision_call):
    monkeypatch.chdir(SR_ROOT)
    _set_orchestrator(orch)
    run_dir = _authored_1b("run_970", GOOD)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "hypothesis_card.yaml", dict(CARD, claim=_c(CLOSE_Q)))
    (arts / "claim_revision.yaml").write_text("left: by hand\n", encoding="utf-8")
    before = {p.name: p.read_bytes() for p in arts.iterdir()}
    state_before = (run_dir / "pipeline_state.yaml").read_bytes()
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    rpr._claim_revision_after_1b(run_dir, "run_970")
    for stage in ("hypothesis_generation", "strategy_config_authoring"):
        rpr._clear_claim_revision_files(stage, run_dir)
    assert {p.name: p.read_bytes() for p in arts.iterdir()} == before
    assert (run_dir / "pipeline_state.yaml").read_bytes() == state_before


def test_flag_on_the_only_call_is_the_revision_and_only_when_blind(monkeypatch):
    """claim_tests on: no LLM call at all when a test sees the block (no other
    call exists in 3b -- the review was parked after its offline measurement)."""
    monkeypatch.chdir(SR_ROOT)
    _set_orchestrator(ON)
    fake = FakeLLM()
    monkeypatch.setattr(rpr, "_invoke_reader_llm", fake)
    run_dir = _authored_1b("run_971", GOOD)
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml",
                  dict(CARD, claim=_c(CLOSE_Q, UPPER)))
    rpr._claim_revision_after_1b(run_dir, "run_971")
    assert fake.prompts == [] and _rev(run_dir)["status"] == "not_needed"
    assert not (run_dir / "artifacts" / "claim_review.yaml").exists()
    assert not hasattr(rpr, "_claim_test_review_mode")


def test_the_revision_skill_is_a_flag_on_only_input():
    assert rpr.CLAIM_REVISION_SKILL not in rpr._SKILL_MAP.values()
    skills = SR_ROOT / "workflow_artifacts" / "skills"
    assert (skills / rpr.CLAIM_REVISION_SKILL / "SKILL.md").exists()
    for skill in skills.glob("*/SKILL.md"):
        if skill.parent.name != rpr.CLAIM_REVISION_SKILL:
            assert "claim-revision" not in skill.read_text(encoding="utf-8"), skill
    guide = (SR_ROOT / "workflow_artifacts" / "skills" / "hypothesis-design" /
             "CLAIM_TESTS.md").read_text(encoding="utf-8")
    assert "At least one test must read the block's own output" in guide
    assert "Never approximate." in guide


def test_guide_path_is_the_run_relative_one():
    run_dir = rpr.ROOT / "runs" / "run_x"
    assert (run_dir / rpr._claim_guide_rel(run_dir)).resolve() == rpr._CLAIM_GUIDE_SOURCE


# ---------------------------------------------------------------------------
# 5. cleared at 1a/1b entry
# ---------------------------------------------------------------------------

def test_cleared_at_1a_and_1b_entry_only():
    _set_orchestrator(ON)
    run_dir = _minimal_run(rpr.ROOT, "run_980")
    path = run_dir / "artifacts" / "claim_revision.yaml"
    for stage, cleared in (("innovation_expansion", False), ("protocol_execution", False),
                           ("hypothesis_generation", True), ("strategy_config_authoring", True)):
        path.write_text("status: accepted\n", encoding="utf-8")
        rpr._clear_claim_revision_files(stage, run_dir)
        assert path.exists() is not cleared, stage
    rpr.update_state(path=run_dir, claim_revision={"revision_called": True})
    rpr._clear_claim_revision_files("strategy_config_authoring", run_dir)
    assert _state(run_dir)["claim_revision"] == {"revision_called": True}   # kept


def test_async_invoke_agent_clears_at_stage_entry():
    import inspect
    src = inspect.getsource(rpr.async_invoke_agent)
    assert "_clear_claim_revision_files(stage_name, RUN_DIR)" in src


def test_run_loop_calls_the_revision_only_on_the_innovation_expansion_route():
    import inspect
    src = inspect.getsource(rpr.run_loop)
    i = src.index("next_stage = determine_post_strategy_config_authoring_route(")
    tail = src[i:i + 900]
    assert 'if next_stage == "innovation_expansion":' in tail
    assert "_claim_revision_after_1b(RUN_DIR, run_id)" in tail
    assert src.count("_claim_revision_after_1b(") == 1



# ---------------------------------------------------------------------------
# 6. review fixes: crash-resume history, failures, warnings, nits
# ---------------------------------------------------------------------------

class _Crash(BaseException):
    """A process death (not an Exception: nothing in the pipeline catches it)."""


def test_crash_after_the_splice_then_resume_keeps_the_history(blind_run, monkeypatch):
    run_dir = blind_run
    old = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]
    fake = FakeLLM(_answer(_revised(old, FC_Q)))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", fake)
    real = rpr._claim_check_cards

    def _die(*a, **k):
        raise _Crash()
    monkeypatch.setattr(rpr, "_claim_check_cards", _die)
    with pytest.raises(_Crash):
        rpr._claim_revision_after_1b(run_dir, run_dir.name)
    assert rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]["tests"][0][
        "name"] == "forecast_top"                                       # the splice happened
    state = _state(run_dir)[rpr.CLAIM_REVISION_STATE_KEY]
    assert state["claim_before"] == old and len(state["claim_before_sha256"]) == 64
    monkeypatch.setattr(rpr, "_claim_check_cards", real)
    # resume: 1b re-runs (clears the file), then the hook again
    rpr._clear_claim_revision_files("strategy_config_authoring", run_dir)
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    assert len(fake.prompts) == 1
    doc = _rev(run_dir)
    assert doc["status"] == "skipped" and doc["claim_before"] == old
    assert doc["card_holds_revised_claim"] is True
    assert doc["claim_current"]["tests"][0]["name"] == "forecast_top"
    assert doc["previous"]["status"] is None                          # no outcome was recorded


def test_an_exception_after_the_splice_is_merged_not_lost(blind_run, monkeypatch):
    run_dir = blind_run
    old = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(_answer(_revised(old, FC_Q))))

    def _boom(*a, **k):
        raise KeyError("status writer")
    monkeypatch.setattr(rpr, "_finish_claim_status", _boom)
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    doc = _rev(run_dir)
    assert doc["status"] == "accepted" and "after the splice" in doc["error"]
    assert doc["claim_before"] == old and doc["manifest_kind"] == "forecast"
    assert doc["message"] == rpr.CLAIM_BLIND_MESSAGE
    assert _state(run_dir)[rpr.CLAIM_REVISION_STATE_KEY]["status"] == "accepted"


def test_a_half_splice_is_rolled_back(blind_run, monkeypatch):
    run_dir = blind_run
    arts = run_dir / "artifacts"
    before = {n: (arts / n).read_bytes() for n in ("hypothesis_card.yaml",
                                                   "hypothesis_card_1.yaml")}
    old = rpr.load_yaml(arts / "hypothesis_card.yaml")["claim"]
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(_answer(_revised(old, FC_Q))))
    real_save = rpr.save_yaml

    def _save(path, data):
        if Path(path).name == "hypothesis_card_1.yaml":
            raise OSError("disk full")
        return real_save(path, data)
    monkeypatch.setattr(rpr, "save_yaml", _save)
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    monkeypatch.setattr(rpr, "save_yaml", real_save)
    assert {n: (arts / n).read_bytes() for n in before} == before        # all or nothing
    doc = _rev(run_dir)
    assert doc["status"] == "error" and "disk full" in doc["error"]
    assert doc["claim_after"] == old
    assert [p.name for p in rpr._claim_card_paths(run_dir)] == ["hypothesis_card.yaml",
                                                                "hypothesis_card_2.yaml"]


def test_a_failed_restore_is_named_and_never_reported_unchanged(blind_run, monkeypatch):
    """Review round 2: if the restore after a failed splice also fails, the
    record names the cards that may hold the revised claim and does not
    present the old claim as `claim_after`."""
    run_dir = blind_run
    arts = run_dir / "artifacts"
    old = rpr.load_yaml(arts / "hypothesis_card.yaml")["claim"]
    new = _revised(old, FC_Q)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(_answer(new)))
    real_atomic = rpr._atomic_write_bytes

    def _locked(path, data):
        # the cards are locked by another process: the splice write AND the
        # restore both fail (save_yaml writes through the same helper)
        if Path(path).name.startswith("hypothesis_card"):
            raise PermissionError("sharing violation")
        return real_atomic(path, data)
    monkeypatch.setattr(rpr, "_atomic_write_bytes", _locked)
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    monkeypatch.setattr(rpr, "_atomic_write_bytes", real_atomic)
    doc = _rev(run_dir)
    assert doc["status"] == "error" and "sharing violation" in doc["error"]
    assert doc["restore_failed"] == ["hypothesis_card.yaml", "hypothesis_card_1.yaml"]
    assert "claim_after" not in doc and doc["claim_attempted"] is not None
    assert "could not be restored" in doc["warning"]


def test_a_call_that_raises_records_cost_unknown(blind_run, monkeypatch):
    run_dir = blind_run
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(RuntimeError("sdk down")))
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    doc = _rev(run_dir)
    assert doc["status"] == "error" and "sdk down" in doc["error"]
    assert doc["cost"].startswith("unknown")
    assert doc["claim_before"] and doc["message"] == rpr.CLAIM_BLIND_MESSAGE
    entry = _state(run_dir)["audit_log"][rpr.CLAIM_REVISION_AUDIT_KEY]
    assert entry["cost_unknown"] is True and "sdk down" in entry["error"]


@pytest.mark.parametrize("answer_kw", [
    {"tests": "none", "missing_block": "a selector on the z-score of the 1h move"},
    {"tests": None, "criteria_refs": ["realized_edge_to_cost_ratio"]},
], ids=["tests_none", "criteria_only"])
def test_a_revision_that_removes_the_tests_is_warned(blind_run, monkeypatch, answer_kw):
    run_dir = blind_run
    arts = run_dir / "artifacts"
    card = rpr.load_yaml(arts / "hypothesis_card.yaml")
    card["criteria"] = [{"id": "realized_edge_to_cost_ratio"}]
    for name in ("hypothesis_card.yaml", "hypothesis_card_1.yaml"):
        rpr.save_yaml(arts / name, card)
    old = card["claim"]
    answer = {k: v for k, v in old.items() if k not in ("statement", "kind", "tests")}
    answer.update({k: v for k, v in answer_kw.items() if v is not None})
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(_answer(answer)))
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    doc = _rev(run_dir)
    assert doc["status"] == "accepted" and doc["visibility_after"] == "not_applicable"
    assert "removed the measurable tests" in doc["warning"]


def test_power_checked_once_and_only_the_own_card_rechecked(blind_run, monkeypatch):
    run_dir = blind_run
    proto = rpr.ROOT / "protocols" / f"{run_dir.name}_generated.json"
    proto.parent.mkdir(parents=True, exist_ok=True)
    proto.write_text(json.dumps({"windows": [{"test": {"start": "2022-01-01",
                                                        "end": "2022-03-31"}}],
                                 "symbols": ["BTCUSDT", "ETHUSDT"], "timeframe": "1h"}))
    old = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]
    fake = FakeLLM(_answer(_revised(old, FC_Q)))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", fake)
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    assert _rev(run_dir)["status"] == "accepted"
    checks = rpr.load_yaml(run_dir / "artifacts" / "claim_power.yaml")["checks"]
    assert len([c for c in checks if c["attempt"] == "claim_revision"]) == 1
    attempts = rpr.load_yaml(run_dir / "artifacts" / "claim_check.yaml")["attempts"]
    assert list(attempts[-1]["cards"]) == ["hypothesis_card.yaml"]
    # the floor facts reached the prompt: 90 days x 24 bars, 2 coins
    flat = " ".join(fake.prompts[0].split())
    assert "bars_in_test_windows: 2160" in flat and "coins: 2" in flat
    assert _rev(run_dir)["floor_facts"]["bars_in_test_windows"] == 2160


def test_a_card_sharing_the_id_but_not_the_content_is_not_a_twin(blind_run, monkeypatch):
    run_dir = blind_run
    arts = run_dir / "artifacts"
    other = dict(CARD, thesis="another idea, same id", claim=_c(CLOSE_Q))
    rpr.save_yaml(arts / "hypothesis_card_3.yaml", other)
    before = (arts / "hypothesis_card_3.yaml").read_bytes()
    old = rpr.load_yaml(arts / "hypothesis_card.yaml")["claim"]
    monkeypatch.setattr(rpr, "_invoke_reader_llm", FakeLLM(_answer(_revised(old, FC_Q))))
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    assert _rev(run_dir)["cards_updated"] == ["hypothesis_card.yaml", "hypothesis_card_1.yaml"]
    assert (arts / "hypothesis_card_3.yaml").read_bytes() == before


# ---------------------------------------------------------------------------
# D-100: a child built to confirm a claim on its fold keeps that claim frozen
# ---------------------------------------------------------------------------

REF = "runs/run_071/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_071-4"


def _child_brief(run_dir, claim, ref=REF):
    cand = {"claim": copy.deepcopy(claim)}
    if ref is not None:
        cand["source"] = {"proposal_ref": ref}
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", {"candidate": cand})


def test_folds_on_a_claim_built_child_is_frozen_no_call(blind_run, monkeypatch, no_revision_call):
    _set_orchestrator({**ON, "folds": {"enabled": True}})
    run_dir = blind_run
    card_before = (run_dir / "artifacts" / "hypothesis_card.yaml").read_bytes()
    old = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]
    _child_brief(run_dir, old)
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    doc = _rev(run_dir)
    assert doc["status"] == "frozen" and REF in doc["reason"] and "D-100" in doc["reason"]
    assert doc["visibility_before"] == "blind" and doc["claim_after"] == old
    assert (run_dir / "artifacts" / "hypothesis_card.yaml").read_bytes() == card_before
    state = _state(run_dir)
    assert rpr.CLAIM_REVISION_STATE_KEY not in state
    assert rpr.CLAIM_REVISION_AUDIT_KEY not in (state.get("audit_log") or {})


@pytest.mark.parametrize("folds,brief", [
    (False, "child"),            # flag off: exactly as before, even for a claim-built child
    (True, "no_ref"),            # a pre-filled claim with no source proposal
    (True, "no_claim"),          # a brief without a pre-filled claim
    (True, None),                # no research_brief.yaml
])
def test_otherwise_the_blind_claim_is_still_revised(blind_run, monkeypatch, folds, brief):
    _set_orchestrator({**ON, "folds": {"enabled": True}} if folds else ON)
    run_dir = blind_run
    old = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")["claim"]
    if brief == "child":
        _child_brief(run_dir, old)
    elif brief == "no_ref":
        _child_brief(run_dir, old, ref=None)
    elif brief == "no_claim":
        rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml",
                      {"candidate": {"source": {"proposal_ref": REF}}})
    fake = FakeLLM(_answer(_revised(old, FC_Q)))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", fake)
    rpr._claim_revision_after_1b(run_dir, run_dir.name)
    assert len(fake.prompts) == 1 and _rev(run_dir)["status"] == "accepted"


def test_frozen_check_reads_nothing_with_the_flag_off(tmp_path, monkeypatch):
    _set_orchestrator(ON)
    def _boom(*a, **k):
        raise AssertionError("research_brief.yaml must not be read with folds off")
    monkeypatch.setattr(rpr, "load_yaml", _boom)
    assert rpr._claim_frozen_for_fold(tmp_path) is None
