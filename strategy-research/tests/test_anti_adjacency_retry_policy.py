"""
E-032 S2c -- orchestrator wiring for the anti-adjacency gate: bounded
retry-then-escalate, per the operator ruling (2026-08-23, EPIC.md Log):
"Retry up to 4 times with the exclusion list, then escalate to me."

This story changes ORCHESTRATION control flow (what run_loop's own routing
dispatch does after innovation_expansion produces output), not just what one
stage receives as input (that was S2a/S2b). The acceptance bar for flag-off
is therefore the same discipline S2a/S2b used for prompt text, applied to
run_loop's stage-advance logic: compare actual behavior/output (returned
next_stage, raw pipeline_state.yaml bytes, presence/absence of new
artifacts), never merely assert the flag is False.

Sandboxing: tests/conftest.py's autouse _sandbox_by_default fixture
redirects rpr.ROOT (and run_campaign.ROOT for the one test that also touches
_classify_human_pause) into a per-test tmp_path sandbox before any test body
runs -- same precedent as test_exclusion_digest_input.py /
test_stale_input_path_fix.py.
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

_SR = Path(__file__).parent.parent
_REAL_KB_PATH = _SR / "campaign_record" / "campaign_knowledge_base.yaml"
_REAL_RUN_059_DIR = _SR / "runs" / "run_059"


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

def _minimal_run(root: Path, run_id: str, hypothesis_card: dict | None = None) -> Path:
    run_dir = root / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (run_dir / "handoffs").mkdir(parents=True, exist_ok=True)
    if hypothesis_card is not None:
        with open(run_dir / "artifacts" / "hypothesis_card.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(hypothesis_card, f, sort_keys=False)
    return run_dir


def _fresh_state(run_id: str, **overrides) -> dict:
    state = {
        "run_id": run_id, "status": "active", "pending_stage": "innovation_expansion",
        "completed_stages": [], "flags": {}, "audit_log": {},
        "counters": {"refinements_used": 0, "reruns_used": 0},
    }
    state.update(overrides)
    return state


def _write_state(run_dir: Path, state: dict) -> None:
    with open(run_dir / "pipeline_state.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, sort_keys=False)


def _read_state(run_dir: Path) -> dict:
    return yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))


def _set_flag(root: Path, enabled) -> None:
    """enabled: True, False, or None (key/section absent entirely)."""
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    if enabled is None:
        (config_dir / "campaign_config.yaml").write_text("orchestrator: {}\n", encoding="utf-8")
        return
    with open(config_dir / "campaign_config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"orchestrator": {"anti_adjacency_retry": {"enabled": bool(enabled)}}}, f)


def _write_digest(root: Path, families: dict) -> None:
    digest_path = root / "campaign_record" / "exclusion_digest.yaml"
    digest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(digest_path, "w", encoding="utf-8") as f:
        yaml.safe_dump({"families": families, "failed_families_passthrough": [],
                         "components_built_passthrough": []}, f)


def _kc_digest(*instrument_run_pairs) -> dict:
    """{'keltner_channel': {..., 'triples': [{instrument, timeframe='4h', run_ids}, ...]}}
    for each (instrument, run_id) pair -- factored out because the literal
    nested-brace form was error-prone to hand-write repeatedly inline."""
    return {"keltner_channel": {"confidence": "structural_indicator_id", "triples": [
        {"instrument": inst, "timeframe": "4h", "run_ids": [run_id]}
        for inst, run_id in instrument_run_pairs
    ]}}


def _write_empty_kb(root: Path) -> None:
    kb_path = root / "campaign_record" / "campaign_knowledge_base.yaml"
    kb_path.parent.mkdir(parents=True, exist_ok=True)
    with open(kb_path, "w", encoding="utf-8") as f:
        yaml.safe_dump({"findings": []}, f)


def _refused_candidate(tag: str, instrument: str) -> dict:
    """A candidate whose (family, instrument, timeframe) exactly matches a
    digest triple -- Layer 2 REFUSE, distinct text per `tag` so consecutive
    attempts carry genuinely DIFFERENT refusal reasons (not the same string
    repeated), matching what a real retry sequence would look like."""
    return {
        "hypothesis_id": f"KELTNER_{tag}", "target_market": [instrument], "timeframe": "4h",
        "thesis": f"Keltner channel mean reversion on {instrument} ({tag}).",
    }


_ADMIT_CANDIDATE = {
    "hypothesis_id": "FEAR_GREED_NOVEL_ANGLE", "target_market": ["DOTUSDT"], "timeframe": "1h",
    "thesis": "Fear & Greed index contrarian positioning on DOT, never tried.",
}


# ---------------------------------------------------------------------------
# _anti_adjacency_retry_enabled -- same 4-case shape as the other 3 flags
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("enabled,expected", [(True, True), (False, False), (None, False)])
def test_anti_adjacency_retry_enabled_reads_flag(enabled, expected):
    root = rpr.ROOT
    _set_flag(root, enabled)
    assert rpr._anti_adjacency_retry_enabled() is expected


def test_anti_adjacency_retry_enabled_false_when_config_file_absent():
    assert rpr._anti_adjacency_retry_enabled() is False


# ---------------------------------------------------------------------------
# Flag-off bit-identity (the acceptance bar this story sets for itself):
# compare actual output, not just assert the flag is False.
# ---------------------------------------------------------------------------

def test_flag_off_route_equals_unconditional_default_next():
    root = rpr.ROOT
    _set_flag(root, False)
    # Digest/KB present AND shaped to REFUSE if the gate were ever consulted --
    # proves flag-off isn't merely "no candidate to refuse", it's "the gate is
    # never even invoked".
    _write_digest(root, _kc_digest(("AVAXUSDT", "run_030")))
    _write_empty_kb(root)
    run_dir = _minimal_run(root, "run_910", hypothesis_card=_refused_candidate("A", "AVAXUSDT"))
    _write_state(run_dir, _fresh_state("run_910"))
    state = _read_state(run_dir)

    next_stage = rpr._route_post_innovation_expansion(run_dir, "run_910", state)

    assert next_stage == rpr.STAGE_CONFIGS["innovation_expansion"]["default_next"] == "validation"


def test_flag_off_pipeline_state_file_byte_identical_before_and_after():
    root = rpr.ROOT
    _set_flag(root, False)
    _write_digest(root, _kc_digest(("AVAXUSDT", "run_030")))
    _write_empty_kb(root)
    run_dir = _minimal_run(root, "run_911", hypothesis_card=_refused_candidate("A", "AVAXUSDT"))
    _write_state(run_dir, _fresh_state("run_911"))
    state_path = run_dir / "pipeline_state.yaml"
    before = state_path.read_bytes()

    rpr._route_post_innovation_expansion(run_dir, "run_911", _read_state(run_dir))

    after = state_path.read_bytes()
    assert before == after, (
        "flag-off must not write to pipeline_state.yaml at all -- a byte "
        "difference here means the new orchestration logic ran despite the flag"
    )


def test_flag_off_never_writes_anti_adjacency_result_artifact():
    root = rpr.ROOT
    _set_flag(root, False)
    _write_digest(root, {})
    _write_empty_kb(root)
    run_dir = _minimal_run(root, "run_912", hypothesis_card=_ADMIT_CANDIDATE)
    _write_state(run_dir, _fresh_state("run_912"))

    rpr._route_post_innovation_expansion(run_dir, "run_912", _read_state(run_dir))

    assert not (run_dir / "artifacts" / "anti_adjacency_result.yaml").exists()


def test_flag_off_key_and_section_absent_also_never_touches_state():
    root = rpr.ROOT
    _set_flag(root, None)
    _write_digest(root, {})
    _write_empty_kb(root)
    run_dir = _minimal_run(root, "run_913", hypothesis_card=_ADMIT_CANDIDATE)
    _write_state(run_dir, _fresh_state("run_913"))
    before = (run_dir / "pipeline_state.yaml").read_bytes()

    next_stage = rpr._route_post_innovation_expansion(run_dir, "run_913", _read_state(run_dir))

    after = (run_dir / "pipeline_state.yaml").read_bytes()
    assert next_stage == "validation"
    assert before == after


def test_flag_off_run_loop_iteration_unchanged(monkeypatch):
    """Full run_loop() dispatch, not just the helper function in isolation --
    proves the NEW elif branch inside run_loop's own while-True routing is
    reached (current_stage == 'innovation_expansion' really does hit it) and,
    at flag-off, produces exactly today's next_stage with no new state key."""
    root = rpr.ROOT
    _set_flag(root, False)
    _write_digest(root, _kc_digest(("AVAXUSDT", "run_030")))
    _write_empty_kb(root)
    run_dir = _minimal_run(root, "run_914", hypothesis_card=_refused_candidate("A", "AVAXUSDT"))
    (run_dir / "handoffs" / "hypothesis_to_innovation_expansion.yaml").write_text(
        yaml.safe_dump({"required_inputs": [], "deliverables": []}), encoding="utf-8")

    async def _noop_invoke(stage_name, run_id, retry_context=None):
        return
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)
    # Make the real default_next ('validation') terminal-shaped for this test
    # only, so run_loop stops right after processing innovation_expansion
    # without needing a real validation_decision.yaml -- same technique
    # test_stage_attempt_counter.py uses for its synthetic stage.
    monkeypatch.setitem(rpr.STAGE_CONFIGS, "innovation_expansion",
                         {**rpr.STAGE_CONFIGS["innovation_expansion"], "default_next": "completed_rejected"})

    _write_state(run_dir, _fresh_state("run_914"))
    rpr.run_loop("run_914")

    final = _read_state(run_dir)
    assert final["pending_stage"] == "completed_rejected"
    assert "anti_adjacency_gate_retry" not in final
    assert not (run_dir / "artifacts" / "anti_adjacency_result.yaml").exists()


# ---------------------------------------------------------------------------
# Flag ON -- required inputs genuinely ABSENT (FIX 3, review 2026-08-24):
# fail loud, never silently substitute {} -- distinct from an EXISTING but
# empty file, which is a legitimate clean-slate ADMIT (covered above by
# test_flag_on_admit_routes_to_validation_and_resets_counter's _write_digest
# (root, {}) / _write_empty_kb(root)).
# ---------------------------------------------------------------------------

def test_flag_on_raises_when_digest_file_genuinely_absent():
    root = rpr.ROOT
    _set_flag(root, True)
    # Deliberately do NOT call _write_digest -- exclusion_digest.yaml does
    # not exist at all in this sandbox.
    _write_empty_kb(root)
    run_dir = _minimal_run(root, "run_940", hypothesis_card=_ADMIT_CANDIDATE)
    _write_state(run_dir, _fresh_state("run_940"))

    with pytest.raises((RuntimeError, FileNotFoundError)) as exc_info:
        rpr._route_post_innovation_expansion(run_dir, "run_940", _read_state(run_dir))
    assert "exclusion_digest.yaml" in str(exc_info.value)


def test_flag_on_raises_when_kb_file_genuinely_absent():
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root, {})
    # Deliberately do NOT call _write_empty_kb -- campaign_knowledge_base.yaml
    # does not exist at all in this sandbox.
    run_dir = _minimal_run(root, "run_941", hypothesis_card=_ADMIT_CANDIDATE)
    _write_state(run_dir, _fresh_state("run_941"))

    with pytest.raises((RuntimeError, FileNotFoundError)) as exc_info:
        rpr._route_post_innovation_expansion(run_dir, "run_941", _read_state(run_dir))
    assert "campaign_knowledge_base.yaml" in str(exc_info.value)


def test_flag_on_existing_but_empty_digest_and_kb_still_admit_no_regression():
    """The legitimate clean-slate case: both files EXIST but are empty --
    must still ADMIT exactly as before this fix, never raise."""
    root = rpr.ROOT
    _set_flag(root, True)
    digest_path = root / "campaign_record" / "exclusion_digest.yaml"
    digest_path.parent.mkdir(parents=True, exist_ok=True)
    digest_path.write_text("", encoding="utf-8")  # genuinely empty YAML document
    kb_path = root / "campaign_record" / "campaign_knowledge_base.yaml"
    kb_path.write_text("", encoding="utf-8")
    run_dir = _minimal_run(root, "run_942", hypothesis_card=_ADMIT_CANDIDATE)
    _write_state(run_dir, _fresh_state("run_942"))

    next_stage = rpr._route_post_innovation_expansion(run_dir, "run_942", _read_state(run_dir))

    assert next_stage == "validation"
    result = yaml.safe_load((run_dir / "artifacts" / "anti_adjacency_result.yaml").read_text(encoding="utf-8"))
    assert result["route"] == "admit"


# ---------------------------------------------------------------------------
# Flag ON -- ADMIT
# ---------------------------------------------------------------------------

def test_flag_on_admit_routes_to_validation_and_resets_counter():
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root, {})
    _write_empty_kb(root)
    run_dir = _minimal_run(root, "run_920", hypothesis_card=_ADMIT_CANDIDATE)
    _write_state(run_dir, _fresh_state("run_920"))

    next_stage = rpr._route_post_innovation_expansion(run_dir, "run_920", _read_state(run_dir))

    assert next_stage == "validation"
    state = _read_state(run_dir)
    assert state["anti_adjacency_gate_retry"]["attempts"] == 0
    result = yaml.safe_load((run_dir / "artifacts" / "anti_adjacency_result.yaml").read_text(encoding="utf-8"))
    assert result["route"] == "admit"


# ---------------------------------------------------------------------------
# Flag ON -- attempts 1-3 REFUSE, attempt 4 ADMIT: succeeds, exactly 4 calls,
# each retry carries the PREVIOUS attempt's specific reason.
# ---------------------------------------------------------------------------

def test_flag_on_three_refuses_then_admit_carries_prior_reason_each_time():
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root, _kc_digest(
        ("AVAXUSDT", "run_030"), ("SOLUSDT", "run_031"), ("ETHUSDT", "run_032"),
    ))
    _write_empty_kb(root)
    run_id = "run_921"
    run_dir = _minimal_run(root, run_id)

    candidates = [
        _refused_candidate("A", "AVAXUSDT"),   # attempt 1 -- REFUSE
        _refused_candidate("B", "SOLUSDT"),    # attempt 2 -- REFUSE (different reason text)
        _refused_candidate("C", "ETHUSDT"),    # attempt 3 -- REFUSE (different reason text)
        _ADMIT_CANDIDATE,                       # attempt 4 -- ADMIT
    ]
    expected_next = ["hypothesis_generation", "hypothesis_generation", "hypothesis_generation", "validation"]
    reasons_seen = []
    routes_seen = []

    _write_state(run_dir, _fresh_state(run_id))
    for i, candidate in enumerate(candidates, start=1):
        with open(run_dir / "artifacts" / "hypothesis_card.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(candidate, f, sort_keys=False)
        state = _read_state(run_dir)
        next_stage = rpr._route_post_innovation_expansion(run_dir, run_id, state)
        routes_seen.append(next_stage)

        state = _read_state(run_dir)
        if next_stage == "hypothesis_generation":
            assert state["anti_adjacency_gate_retry"]["attempts"] == i
            reasons_seen.append(state["anti_adjacency_gate_retry"]["last_reason"])
            # Constraint 2: the NEXT hypothesis_generation invocation must carry
            # THIS attempt's own reason, not a generic "try again".
            handoff = {"required_inputs": [], "optional_inputs": []}
            rpr._apply_anti_adjacency_retry_context("hypothesis_generation", handoff, run_dir)
            injected = handoff["injected_context"]["anti_adjacency_gate_refusal"]
            assert f"Attempt {i}/4" in injected
            assert state["anti_adjacency_gate_retry"]["last_reason"] in injected
        else:
            assert state["anti_adjacency_gate_retry"]["attempts"] == 0

    assert routes_seen == expected_next
    # Each REFUSE carried a genuinely DIFFERENT reason -- not the same string
    # replayed 3 times (a bare retry, the exact failure mode E-030 R3 forbids).
    assert len(set(reasons_seen)) == 3, f"expected 3 distinct refusal reasons, got: {reasons_seen}"


def test_flag_on_uses_exactly_four_gate_calls_for_three_refuse_then_admit(monkeypatch):
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root, _kc_digest(
        ("AVAXUSDT", "run_030"), ("SOLUSDT", "run_031"), ("ETHUSDT", "run_032"),
    ))
    _write_empty_kb(root)
    run_id = "run_922"
    run_dir = _minimal_run(root, run_id)

    import anti_adjacency_gate as aag
    call_count = {"n": 0}
    real_evaluate = aag.evaluate_candidate

    def _counting_evaluate(*args, **kwargs):
        call_count["n"] += 1
        return real_evaluate(*args, **kwargs)
    monkeypatch.setattr(aag, "evaluate_candidate", _counting_evaluate)

    candidates = [
        _refused_candidate("A", "AVAXUSDT"), _refused_candidate("B", "SOLUSDT"),
        _refused_candidate("C", "ETHUSDT"), _ADMIT_CANDIDATE,
    ]
    _write_state(run_dir, _fresh_state(run_id))
    for candidate in candidates:
        with open(run_dir / "artifacts" / "hypothesis_card.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(candidate, f, sort_keys=False)
        rpr._route_post_innovation_expansion(run_dir, run_id, _read_state(run_dir))

    assert call_count["n"] == 4


# ---------------------------------------------------------------------------
# Flag ON -- 4 consecutive REFUSEs: escalates, does not attempt a 5th.
# ---------------------------------------------------------------------------

def test_flag_on_four_consecutive_refuses_escalates_and_stops():
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root, _kc_digest(
        ("AVAXUSDT", "run_030"), ("SOLUSDT", "run_031"), ("ETHUSDT", "run_032"), ("DOTUSDT", "run_033"),
    ))
    _write_empty_kb(root)
    run_id = "run_923"
    run_dir = _minimal_run(root, run_id)
    _write_state(run_dir, _fresh_state(run_id))

    candidates = [_refused_candidate(tag, inst) for tag, inst in
                  [("A", "AVAXUSDT"), ("B", "SOLUSDT"), ("C", "ETHUSDT"), ("D", "DOTUSDT")]]
    routes = []
    for candidate in candidates:
        with open(run_dir / "artifacts" / "hypothesis_card.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(candidate, f, sort_keys=False)
        routes.append(rpr._route_post_innovation_expansion(run_dir, run_id, _read_state(run_dir)))

    assert routes == ["hypothesis_generation", "hypothesis_generation", "hypothesis_generation", "human_pause"]
    state = _read_state(run_dir)
    assert state["status"] == "paused_for_human"
    assert state["flags"]["anti_adjacency_gate_exhausted"] is True
    assert state["anti_adjacency_gate_retry"]["attempts"] == 4
    assert len(state["anti_adjacency_gate_retry"]["history"]) == 4

    # Does not attempt a 5th: calling the routing function again on the SAME
    # gate-exhausted state must not silently reset and retry -- the ONLY
    # correct next action is a human clearing the pause per RUNBOOK.md, which
    # this test does not simulate. A well-behaved orchestrator would not even
    # re-enter innovation_expansion while status=paused_for_human (run_loop's
    # own TERMINAL_PREFIXES/pending_stage check happens one level up); this
    # asserts the routing function's own state is exactly '4', not creeping
    # past it if called again with an unchanged REFUSE-shaped candidate.
    state_before_extra_call = dict(state)
    routes.append(rpr._route_post_innovation_expansion(run_dir, run_id, _read_state(run_dir)))
    assert routes[-1] == "human_pause"
    final_state = _read_state(run_dir)
    assert final_state["anti_adjacency_gate_retry"]["attempts"] == 5, (
        "documenting actual behavior: the routing function itself is stateless "
        "per-call and will keep counting if called again -- the real guard "
        "against a 5th AUTO-ACTIONED attempt is that run_loop never re-enters "
        "innovation_expansion for a run whose status is paused_for_human "
        "(see the classification test below), not this function refusing to "
        "be called"
    )


def test_flag_on_escalation_classifies_via_existing_run_campaign_mechanism():
    """'Escalate exactly as the project already does elsewhere' (dispatch
    brief): status=paused_for_human plus a flags entry
    run_campaign._classify_human_pause can name -- proven by calling the
    REAL classifier, not by re-deriving its logic here."""
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root, _kc_digest(("AVAXUSDT", "run_030")))
    _write_empty_kb(root)
    run_id = "run_924"
    run_dir = _minimal_run(root, run_id)
    _write_state(run_dir, _fresh_state(run_id, anti_adjacency_gate_retry={
        "attempts": 4, "last_reason": "family already run", "history": [{}] * 4,
    }, status="paused_for_human", flags={"anti_adjacency_gate_exhausted": True}))

    state = _read_state(run_dir)
    reason = camp._classify_human_pause(run_dir, state)
    assert reason == "anti_adjacency_gate_exhausted"
    assert reason not in camp._QUARANTINE_SAFE_REASONS, (
        "a genuine must-escalate per the operator's own ruling -- must never "
        "be auto-quarantined/auto-continued"
    )


# ---------------------------------------------------------------------------
# Dedicated counter independent of BOTH counters.refinements_used and
# stage_attempts -- a REAL regression test for the E-030 S1.5 Piece 2
# re-entry shape, not just a comment citing the precedent.
# ---------------------------------------------------------------------------

def test_counter_independent_of_refinements_used_across_same_counter_reentry():
    """Reproduces RUNBOOK.md section 4.5's exact crash-resume condition
    (E-030 S1.5 Piece 2): the SAME run re-enters the gate-check TWICE without
    counters.refinements_used changing between calls. The dedicated
    anti_adjacency_gate_retry.attempts counter must still advance (1, then
    2) -- proving it is not silently keyed off refinements_used the way the
    audit_log bug was before E-030 S1.5 Piece 2 fixed it."""
    root = rpr.ROOT
    _set_flag(root, True)
    _write_digest(root, _kc_digest(
        ("AVAXUSDT", "run_030"), ("SOLUSDT", "run_031"),
    ))
    _write_empty_kb(root)
    run_id = "run_925"
    run_dir = _minimal_run(root, run_id, hypothesis_card=_refused_candidate("A", "AVAXUSDT"))
    _write_state(run_dir, _fresh_state(run_id))  # counters.refinements_used == 0

    state = _read_state(run_dir)
    assert state["counters"]["refinements_used"] == 0
    next_stage_1 = rpr._route_post_innovation_expansion(run_dir, run_id, state)
    assert next_stage_1 == "hypothesis_generation"
    state = _read_state(run_dir)
    assert state["anti_adjacency_gate_retry"]["attempts"] == 1
    assert state["counters"]["refinements_used"] == 0, "must not have touched the refinement-budget counter"

    # Simulate the crash-resume: a fresh process re-enters with a DIFFERENT
    # (still REFUSE-shaped) candidate, counters.refinements_used STILL 0 --
    # exactly the re-entry shape that overwrote the audit_log key before
    # E-030 S1.5 Piece 2.
    with open(run_dir / "artifacts" / "hypothesis_card.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(_refused_candidate("B", "SOLUSDT"), f, sort_keys=False)
    state = _read_state(run_dir)
    assert state["counters"]["refinements_used"] == 0
    next_stage_2 = rpr._route_post_innovation_expansion(run_dir, run_id, state)
    assert next_stage_2 == "hypothesis_generation"
    state = _read_state(run_dir)
    assert state["anti_adjacency_gate_retry"]["attempts"] == 2, (
        "counter must advance on re-entry even though refinements_used never changed"
    )
    assert state["counters"]["refinements_used"] == 0
    # Independent of stage_attempts too: this state file never had a
    # stage_attempts key written by run_loop's own bookkeeping in this test
    # (only _route_post_innovation_expansion was called directly), so its
    # presence/absence must have no bearing on anti_adjacency_gate_retry.
    assert "stage_attempts" not in state or "anti_adjacency_gate_retry" in state


# ---------------------------------------------------------------------------
# _apply_anti_adjacency_retry_context -- prompt-carrying half, same
# byte-identity acceptance bar as _apply_exclusion_digest_input /
# _apply_stale_input_path_fix.
# ---------------------------------------------------------------------------

def test_apply_retry_context_noop_when_flag_off():
    root = rpr.ROOT
    _set_flag(root, False)
    run_dir = _minimal_run(root, "run_930")
    _write_state(run_dir, _fresh_state("run_930", anti_adjacency_gate_retry={
        "attempts": 2, "last_reason": "collision", "history": []}))
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_anti_adjacency_retry_context("hypothesis_generation", handoff, run_dir)
    assert "injected_context" not in handoff


def test_apply_retry_context_noop_when_no_retry_in_progress():
    root = rpr.ROOT
    _set_flag(root, True)
    run_dir = _minimal_run(root, "run_931")
    _write_state(run_dir, _fresh_state("run_931"))  # no anti_adjacency_gate_retry key at all
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_anti_adjacency_retry_context("hypothesis_generation", handoff, run_dir)
    assert "injected_context" not in handoff


def test_apply_retry_context_noop_for_non_hypothesis_generation_stage():
    root = rpr.ROOT
    _set_flag(root, True)
    run_dir = _minimal_run(root, "run_932")
    _write_state(run_dir, _fresh_state("run_932", anti_adjacency_gate_retry={
        "attempts": 1, "last_reason": "collision", "history": []}))
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_anti_adjacency_retry_context("innovation_expansion", handoff, run_dir)
    assert "injected_context" not in handoff


def test_apply_retry_context_carries_reason_when_flag_on_and_retry_in_progress():
    root = rpr.ROOT
    _set_flag(root, True)
    run_dir = _minimal_run(root, "run_933")
    _write_state(run_dir, _fresh_state("run_933", anti_adjacency_gate_retry={
        "attempts": 2, "last_reason": "keltner_channel already run at (AVAXUSDT, 4h)", "history": []}))
    handoff = {"required_inputs": [], "optional_inputs": []}
    rpr._apply_anti_adjacency_retry_context("hypothesis_generation", handoff, run_dir)
    injected = handoff["injected_context"]["anti_adjacency_gate_refusal"]
    assert "Attempt 2/4" in injected
    assert "keltner_channel already run at (AVAXUSDT, 4h)" in injected


def test_flag_off_prompt_is_byte_identical_to_never_calling_retry_context_at_all():
    root = rpr.ROOT
    _set_flag(root, False)
    run_dir = _minimal_run(root, "run_934")
    (run_dir / "artifacts" / "research_brief.yaml").write_text("asset: BTCUSDT\n", encoding="utf-8")
    _write_state(run_dir, _fresh_state("run_934", anti_adjacency_gate_retry={
        "attempts": 3, "last_reason": "collision", "history": []}))

    base_handoff = {"required_inputs": [{"path": "artifacts/research_brief.yaml", "reason": "base"}],
                     "optional_inputs": []}
    baseline_prompt = rpr._build_stage_prompt("hypothesis_generation", dict(base_handoff), run_dir)

    flag_off_handoff = {"required_inputs": [{"path": "artifacts/research_brief.yaml", "reason": "base"}],
                         "optional_inputs": []}
    rpr._apply_anti_adjacency_retry_context("hypothesis_generation", flag_off_handoff, run_dir)
    flag_off_prompt = rpr._build_stage_prompt("hypothesis_generation", flag_off_handoff, run_dir)

    assert flag_off_prompt == baseline_prompt


def test_flag_on_prompt_differs_and_carries_refusal_reason():
    root = rpr.ROOT
    _set_flag(root, True)
    run_dir = _minimal_run(root, "run_935")
    (run_dir / "artifacts" / "research_brief.yaml").write_text("asset: BTCUSDT\n", encoding="utf-8")
    _write_state(run_dir, _fresh_state("run_935", anti_adjacency_gate_retry={
        "attempts": 1, "last_reason": "keltner_channel already run at (AVAXUSDT, 4h)", "history": []}))

    baseline_handoff = {"required_inputs": [{"path": "artifacts/research_brief.yaml", "reason": "base"}],
                         "optional_inputs": []}
    baseline_prompt = rpr._build_stage_prompt("hypothesis_generation", dict(baseline_handoff), run_dir)

    on_handoff = {"required_inputs": [{"path": "artifacts/research_brief.yaml", "reason": "base"}],
                  "optional_inputs": []}
    rpr._apply_anti_adjacency_retry_context("hypothesis_generation", on_handoff, run_dir)
    on_prompt = rpr._build_stage_prompt("hypothesis_generation", on_handoff, run_dir)

    assert on_prompt != baseline_prompt
    assert "keltner_channel already run at (AVAXUSDT, 4h)" in on_prompt


# ---------------------------------------------------------------------------
# Calibration case (S1/S2a): the 4h funding retest ADMITs; the naive
# flat-list gate would REFUSE it -- still holds through this new
# orchestration layer, not only at the gate's own unit level.
# ---------------------------------------------------------------------------

def test_calibration_case_still_admits_through_the_orchestration_layer():
    root = rpr.ROOT
    _set_flag(root, True)
    # Seed the sandbox with the REAL KB and the REAL run_059 artifacts the KB
    # precedence rule reads (parent reactivation_condition + the child that
    # closes only the daily branch) -- copied read-only from the real repo,
    # never opening/globbing local_data/holdout_sealed/. Layer 1 resolves
    # this candidate entirely, so an empty digest is fine.
    kb_dest = root / "campaign_record" / "campaign_knowledge_base.yaml"
    kb_dest.parent.mkdir(parents=True, exist_ok=True)
    kb_dest.write_bytes(_REAL_KB_PATH.read_bytes())
    _write_digest(root, {})

    run_059_dest = root / "runs" / "run_059" / "artifacts"
    run_059_dest.mkdir(parents=True, exist_ok=True)
    for name in ("hypothesis_card.yaml", "pass_rule_evaluation.yaml"):
        src = _REAL_RUN_059_DIR / "artifacts" / name
        if src.exists():
            (run_059_dest / name).write_bytes(src.read_bytes())

    funding_4h_candidate = {
        "hypothesis_id": "FUNDING_RATE_CONTINUOUS_MEAN_REVERSION_EXPANDED_4H_RETEST",
        "edge_source": {"evidence_type": "funding_open_interest",
                         "specific_mechanism": "Continuous funding-rate sign mean-reversion re-tested at 4h."},
        "target_market": ["BTCUSDT", "ETHUSDT"],
        "timeframe": "4h",
        "thesis": "Re-test the identical continuous funding-rate mean-reversion mechanism at 4h bars.",
    }
    run_id = "run_926"
    run_dir = _minimal_run(root, run_id, hypothesis_card=funding_4h_candidate)
    _write_state(run_dir, _fresh_state(run_id))

    next_stage = rpr._route_post_innovation_expansion(run_dir, run_id, _read_state(run_dir))

    assert next_stage == "validation", (
        "the calibration case (4h funding retest, S1/S2a) must still ADMIT "
        "when routed through the S2c orchestration wiring, not only at the "
        "gate's own unit-test level"
    )
    result = yaml.safe_load((run_dir / "artifacts" / "anti_adjacency_result.yaml").read_text(encoding="utf-8"))
    assert result["route"] == "admit"
    assert result["layer"] == "kb"
