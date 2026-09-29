"""
C5.7b-1 -- score provenance, slices S0 + S1 + S3 (D-048;
engineering/review_2026-09-27/C5_7B_PROVENANCE_S1.md). Review finding C12.

Behind orchestrator.score_provenance.enabled (default off, strict bool, hard
dependency on specialist_readers):
  S0  the model(s) that actually answered (AssistantMessage.model, and the keys
      of ResultMessage.model_usage as information) are captured on each reader
      call and each Claude stage call and recorded in the audit-log entry's
      `provenance` block;
  S1  the reader proposals' `model_id` is stamped by code with the observed
      model; the self-report is kept in the audit log; `mismatch` is observed
      vs REQUESTED (D-048), never a raise or a retry;
  S3  the same stamp on the brief-card scores (extra_card_scores.yaml);
      `brief-card-v1` enforcement at decide_next is unchanged.

Proven here with stubs only (no LLM, no API call, no backtest, no trial row, no
holdout, nothing under the real campaign_record/ or runs/): the flag, the
capture from a stub stream, the no-observation path, the stamp, mismatch
recorded with the run continuing, flag-off byte identity of the reader file, the
card file and the audit-log entry, and the stamped value reaching decide_next's
decision record. tests/conftest.py's autouse sandbox redirects rpr.ROOT.
"""
from __future__ import annotations

import asyncio
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
import decide_next as dn  # noqa: E402
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock  # noqa: E402

from test_e046a_slice5b_ii_b_readers_stage import (  # noqa: E402
    ALL_ON, RUN_ID, _seed_run, _set_orchestrator,
)
from test_e059_s2a_decide_next import _decide, _one_source, _patch  # noqa: E402

CAT = "profitability"
REQUESTED = rpr._CLAUDE_WORKER_MODEL
DATED = f"{REQUESTED}-20251001"
ON = {**ALL_ON, "score_provenance": {"enabled": True}}
BASELINE_ENTRY_KEYS = {"timestamp", "engine", "execution_time_seconds", "cost_usd",
                       "num_turns", "tokens"}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _reader_text(proposals: list) -> str:
    return "```yaml\n# proposals/profitability.yaml\n" + yaml.safe_dump(proposals) + "```"


def _one_proposal(model_id="self-reported-model", pid="profitability-run_990-1") -> dict:
    p = _patch(pid)
    p["model_id"] = model_id
    return p


def _stub_llm(text: str, models=None, calls: list | None = None):
    """An async stand-in for _invoke_reader_llm. `models` None models a stub with
    no observation (meta has no `models` key, like the pre-change return)."""
    async def _fake(prompt: str):
        if calls is not None:
            calls.append(prompt)
        meta = {"usage": {"input_tokens": 10, "output_tokens": 5}, "cost_usd": 0.0, "num_turns": 1}
        if models is not None:
            meta["models"] = list(models)
        return text, meta
    return _fake


def _run_reader(monkeypatch, llm, orchestrator=ON):
    """Seed a run, run ONE reader (profitability) through run_reader_worker."""
    _set_orchestrator(orchestrator)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    monkeypatch.setattr(rpr, "_invoke_reader_llm", llm)
    dest = rpr.run_reader_worker(CAT, RUN_ID, run_dir, stage_attempt=0)
    audit = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    return run_dir, dest, audit[f"specialist_readers_{CAT}_attempt_0"]


def _bytes(path: Path) -> bytes:
    """File bytes with the platform's text-mode newline translation undone (the
    workers write with open(..., "w"), unchanged by this slice)."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def _loaded(dest: Path) -> list:
    return yaml.safe_load(dest.read_text(encoding="utf-8"))


def _stream(*messages):
    async def _q(*, prompt, options=None):
        for m in messages:
            yield m
    return _q


def _assistant(text: str, model: str):
    return AssistantMessage(content=[TextBlock(text=text)], model=model)


def _result(model_usage=None):
    return ResultMessage(subtype="success", duration_ms=1, duration_api_ms=1, is_error=False,
                         num_turns=1, session_id="s", total_cost_usd=0.0,
                         usage={"input_tokens": 1, "output_tokens": 1}, model_usage=model_usage)


# ---------------------------------------------------------------------------
# 1. the flag
# ---------------------------------------------------------------------------

def test_flag_off_when_config_or_key_absent():
    _set_orchestrator(None)
    assert rpr._score_provenance_enabled() is False
    _set_orchestrator({})
    assert rpr._score_provenance_enabled() is False
    _set_orchestrator({"score_provenance": {}})
    assert rpr._score_provenance_enabled() is False
    _set_orchestrator({**ALL_ON, "score_provenance": {"enabled": False}})
    assert rpr._score_provenance_enabled() is False


@pytest.mark.parametrize("bad", ["true", "false", None, 0, 1])
def test_flag_non_bool_raises(bad):
    _set_orchestrator({**ALL_ON, "score_provenance": {"enabled": bad}})
    with pytest.raises(ValueError, match=r"orchestrator\.score_provenance\.enabled=.* not a real boolean"):
        rpr._score_provenance_enabled()


def test_flag_on_with_specialist_readers_reads_true():
    _set_orchestrator(ON)
    assert rpr._score_provenance_enabled() is True


def test_flag_on_without_specialist_readers_raises():
    _set_orchestrator({"score_provenance": {"enabled": True}})
    with pytest.raises(ValueError, match="requires orchestrator.specialist_readers.enabled=true"):
        rpr._score_provenance_enabled()
    # specialist_readers on but its own dependency off: its own message surfaces
    _set_orchestrator({"specialist_readers": {"enabled": True},
                       "score_provenance": {"enabled": True}})
    with pytest.raises(ValueError, match="orchestrator.grid_evaluation.enabled=true"):
        rpr._score_provenance_enabled()


def test_the_launch_preflight_reads_and_refuses_it():
    assert "score_provenance" in camp._flag_readers()
    _set_orchestrator({**ALL_ON, "score_provenance": {"enabled": "true"}})
    refusal = camp._flag_preflight_refusal()
    assert refusal and "orchestrator.score_provenance.enabled='true'" in refusal
    _set_orchestrator({"score_provenance": {"enabled": True}})
    refusal = camp._flag_preflight_refusal()
    assert refusal and "score_provenance.enabled=true requires" in refusal
    _set_orchestrator(ON)
    values, refusal = camp._flag_preflight()
    assert refusal is None and values["score_provenance"] is True


def test_run_loop_fails_at_start_when_specialist_readers_is_off(monkeypatch):
    _set_orchestrator({"score_provenance": {"enabled": True}})
    run_dir = _seed_run(pending="protocol_execution")
    invoked = []
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", lambda *a, **k: invoked.append(a[0]))
    rpr.run_loop(RUN_ID)  # sets status=failed, does not escape
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert invoked == []
    assert state["pending_stage"] == "protocol_execution"
    assert state["status"] == "failed" and "score_provenance" in state["last_error"]


# ---------------------------------------------------------------------------
# 2. S0: capture from the SDK stream
# ---------------------------------------------------------------------------

def test_capture_from_a_stream_with_two_models(monkeypatch):
    _set_orchestrator(ON)
    monkeypatch.setattr(rpr, "query", _stream(
        _assistant("part one ", "model-b"), _assistant("part two", "model-a"),
        _result({"model-a": {}, "model-helper": {}})))
    text, meta = asyncio.run(rpr._invoke_reader_llm("prompt"))
    assert text == "part one part two"
    assert meta["models"] == ["model-a", "model-b"]            # sorted, distinct
    assert meta["result_models"] == ["model-a", "model-helper"]  # informational only
    assert meta["num_turns"] == 1 and meta["cost_usd"] == 0.0


def test_no_model_stub_stream_captures_nothing(monkeypatch):
    """CUL-336's stub yields a bare object with no `.model`: no observation."""
    _set_orchestrator(ON)

    async def _q(*, prompt, options=None):
        yield type("R", (), {"total_cost_usd": 0.0, "num_turns": 1, "usage": {}})()
    monkeypatch.setattr(rpr, "query", _q)
    _, meta = asyncio.run(rpr._invoke_reader_llm("prompt"))
    assert meta["models"] == [] and meta["result_models"] == []


def test_flag_off_meta_is_the_unchanged_three_keys(monkeypatch):
    _set_orchestrator({**ALL_ON, "score_provenance": {"enabled": False}})
    monkeypatch.setattr(rpr, "query", _stream(_assistant("x", "model-a"), _result({"model-a": {}})))
    _, meta = asyncio.run(rpr._invoke_reader_llm("prompt"))
    assert set(meta) == {"usage", "cost_usd", "num_turns"}


def test_model_facts_rules():
    f = rpr._observed_model_facts
    assert f([]) == (None, None) and f(None) == (None, None)
    assert f([REQUESTED]) == (REQUESTED, False)
    assert f([DATED]) == (DATED, False)                       # a dated snapshot of the request
    assert f([f"{REQUESTED}0"]) == (f"{REQUESTED}0", True)    # not a `-suffix`
    assert f(["claude-sonnet-4-5"]) == ("claude-sonnet-4-5", True)
    assert f(["b", "a", "a"]) == ("a,b", True)                # several distinct: sorted, joined, mismatch
    assert f([REQUESTED, DATED]) == (f"{REQUESTED},{DATED}", True)


# ---------------------------------------------------------------------------
# 3. S1: the reader stamp
# ---------------------------------------------------------------------------

def test_stamp_overwrites_the_self_report_and_records_both(monkeypatch):
    calls = []
    _, dest, entry = _run_reader(monkeypatch, _stub_llm(_reader_text([_one_proposal()]),
                                                        [DATED], calls))
    (p,) = _loaded(dest)
    assert p["model_id"] == DATED
    # everything else is what the model wrote
    assert p["rubric_version"] == "profitability-reader-v1"
    assert p["scores"] == _one_proposal()["scores"] and p["evidence"] == _one_proposal()["evidence"]
    reader_proposals.load_proposals(dest.parent, [CAT])       # still a valid proposals file
    prov = entry["provenance"]
    assert prov["requested"] == REQUESTED and prov["observed_models"] == [DATED]
    assert prov["observed"] == DATED and prov["stamped"] is True
    assert prov["self_reported"] == {"profitability-run_990-1": "self-reported-model"}
    assert prov["mismatch"] is False              # observed matches the REQUESTED model
    assert prov["self_report_differs"] is True    # informational only
    assert len(calls) == 1


def test_a_mismatch_is_recorded_and_the_run_continues(monkeypatch):
    calls = []
    _, dest, entry = _run_reader(monkeypatch, _stub_llm(_reader_text([_one_proposal()]),
                                                        ["claude-sonnet-4-5"], calls))
    assert dest.exists() and _loaded(dest)[0]["model_id"] == "claude-sonnet-4-5"
    assert entry["provenance"]["mismatch"] is True
    assert entry["provenance"]["requested"] == REQUESTED
    assert len(calls) == 1                         # no retry on a mismatch
    reader_proposals.load_proposals(dest.parent, [CAT])


def test_several_distinct_models_are_sorted_joined_and_a_mismatch(monkeypatch):
    _, dest, entry = _run_reader(monkeypatch, _stub_llm(_reader_text([_one_proposal()]),
                                                        [REQUESTED, "claude-other"]))
    assert _loaded(dest)[0]["model_id"] == f"{REQUESTED},claude-other"
    assert entry["provenance"]["mismatch"] is True
    assert entry["provenance"]["observed_models"] == [REQUESTED, "claude-other"]


def test_every_proposal_in_the_file_is_stamped(monkeypatch):
    two = [_one_proposal(pid="profitability-run_990-1"),
           _one_proposal(model_id="another", pid="profitability-run_990-2")]
    _, dest, entry = _run_reader(monkeypatch, _stub_llm(_reader_text(two), [REQUESTED]))
    assert [p["model_id"] for p in _loaded(dest)] == [REQUESTED, REQUESTED]
    assert entry["provenance"]["self_reported"] == {"profitability-run_990-1": "self-reported-model",
                                                    "profitability-run_990-2": "another"}


def test_no_observation_leaves_the_self_report_and_records_null(monkeypatch):
    text = _reader_text([_one_proposal()])
    _, dest, entry = _run_reader(monkeypatch, _stub_llm(text, models=None))
    body = rpr._READER_OUTPUT_BLOCK_RE.findall(text)[0].strip() + "\n"
    assert dest.read_text(encoding="utf-8") == body            # verbatim: never fabricated
    prov = entry["provenance"]
    assert prov["observed_models"] == [] and prov["observed"] is None
    assert prov["mismatch"] is None and prov["self_report_differs"] is None
    assert prov["stamped"] is False
    assert prov["self_reported"] == {"profitability-run_990-1": "self-reported-model"}


def test_an_already_equal_self_report_leaves_the_body_verbatim(monkeypatch):
    text = _reader_text([_one_proposal(model_id=REQUESTED)])
    _, dest, entry = _run_reader(monkeypatch, _stub_llm(text, [REQUESTED]))
    assert dest.read_text(encoding="utf-8") == rpr._READER_OUTPUT_BLOCK_RE.findall(text)[0].strip() + "\n"
    assert entry["provenance"]["self_report_differs"] is False
    assert entry["provenance"]["mismatch"] is False


def test_an_empty_proposal_list_is_not_rewritten(monkeypatch):
    _, dest, entry = _run_reader(monkeypatch, _stub_llm("```yaml\n# p.yaml\n[]\n```", [DATED]))
    assert dest.read_text(encoding="utf-8") == "# p.yaml\n[]\n"  # verbatim, header comment kept
    assert entry["provenance"]["self_reported"] == {} and entry["provenance"]["observed"] == DATED


def test_end_to_end_through_the_real_invoke_with_a_stub_stream(monkeypatch):
    _set_orchestrator(ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    monkeypatch.setattr(rpr, "query", _stream(
        _assistant(_reader_text([_one_proposal()]), DATED), _result({DATED: {}})))
    dest = rpr.run_reader_worker(CAT, RUN_ID, run_dir, stage_attempt=0)
    assert _loaded(dest)[0]["model_id"] == DATED
    entry = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"][f"specialist_readers_{CAT}_attempt_0"]
    assert entry["provenance"]["observed_models"] == [DATED]
    assert entry["provenance"]["result_models"] == [DATED]


def test_stamp_reader_body_never_raises_and_leaves_the_body_on_failure(tmp_path):
    (tmp_path / "artifacts").mkdir()
    body, prov = rpr._stamp_reader_body("just: a mapping\n", CAT, tmp_path, [DATED])
    assert body == "just: a mapping\n"
    assert prov["stamped"] is False and "not a list" in prov["stamp_error"]
    assert prov["observed"] == DATED and prov["mismatch"] is False


def test_a_stamped_body_that_fails_validation_is_not_used(monkeypatch, tmp_path):
    (tmp_path / "artifacts").mkdir()
    monkeypatch.setattr(rpr, "_validate_reader_output", lambda *a, **k: (None, "boom"))
    body, prov = rpr._stamp_reader_body(yaml.safe_dump([_one_proposal()]), CAT, tmp_path, [DATED])
    assert yaml.safe_load(body)[0]["model_id"] == "self-reported-model"
    assert prov["stamped"] is False and "stamped body failed validation: boom" in prov["stamp_error"]


def test_the_budget_sum_ignores_the_provenance_block(monkeypatch):
    run_dir, _, entry = _run_reader(monkeypatch, _stub_llm(_reader_text([_one_proposal()]), [DATED]))
    assert "provenance" in entry
    audit = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    total, _ = rpr._compute_weighted_budget_usage(audit)
    assert total == entry["tokens"]["weighted"]


# ---------------------------------------------------------------------------
# 4. flag-off byte identity
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("orchestrator", [ALL_ON, {**ALL_ON, "score_provenance": {"enabled": False}}])
def test_flag_off_reader_file_and_audit_entry_are_unchanged(monkeypatch, orchestrator):
    text = _reader_text([_one_proposal()])
    # even a stub that reports models (a flag-on meta) must change nothing flag-off
    _, dest, entry = _run_reader(monkeypatch, _stub_llm(text, ["claude-sonnet-4-5"]), orchestrator)
    assert _bytes(dest) == (rpr._READER_OUTPUT_BLOCK_RE.findall(text)[0].strip() + "\n").encode("utf-8")
    assert _loaded(dest)[0]["model_id"] == "self-reported-model"
    assert set(entry) == BASELINE_ENTRY_KEYS and "provenance" not in entry


# ---------------------------------------------------------------------------
# 5. decide_next carries the stamped value
# ---------------------------------------------------------------------------

def test_decide_next_records_the_stamped_model_id(monkeypatch):
    p = _one_proposal(pid="profitability-run_061-1")
    _, dest, _ = _run_reader(monkeypatch, _stub_llm(_reader_text([p]), [DATED]))
    proposals = reader_proposals.load_proposals(dest.parent, [CAT])[CAT]
    assert proposals[0]["model_id"] == DATED
    rec = _decide(_one_source(proposals))
    cand = next(c for c in rec["candidates"] if c["candidate_id"] == "profitability-run_061-1")
    assert cand["scores"]["model_id"] == DATED
    assert cand["scores"]["rubric_version"] == "profitability-reader-v1"


# ---------------------------------------------------------------------------
# 6. S3: the brief-card scores
# ---------------------------------------------------------------------------

def _card_scores(rubric="brief-card-v1", model_id="self-reported-model"):
    def item(card):
        return {"card": card, "model_id": model_id, "rubric_version": rubric,
                "scores": {"confidence_real": 2, "distance_to_profitable": 1,
                           "mechanism_plausibility": 3}}
    return {"cards": [item("hypothesis_card_2.yaml"), item("hypothesis_card_3.yaml")]}


def _stage_text(scores_yaml: str) -> str:
    return ("Done.\n```yaml\n# hypothesis_card.yaml\nhypothesis_id: H-1\n```\n"
            f"```yaml\n# extra_card_scores.yaml\n{scores_yaml}```\n")


def _run_1a(monkeypatch, tmp_path, text, models, orchestrator=ON):
    _set_orchestrator(orchestrator)
    monkeypatch.chdir(SR_ROOT)  # _build_stage_prompt opens the skill relative to cwd
    run_dir = tmp_path / "runs" / "run_c57"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"status": "active", "audit_log": {}}), encoding="utf-8")
    # `models` empty: an AssistantMessage whose model is "" -- no observation
    first = models[0] if models else ""
    monkeypatch.setattr(rpr, "query", _stream(
        _assistant(text, first), *[_assistant("", m) for m in models[1:]],
        _result({first: {}} if first else None)))
    handoff = {"required_inputs": [], "optional_inputs": [], "injected_context": {"stage_attempt": "0"}}
    asyncio.run(rpr.run_claude_worker("validation", handoff, run_dir))
    audit = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    return run_dir, audit["validation_attempt_0"]


def test_card_scores_are_stamped_and_recorded(monkeypatch, tmp_path):
    scores = yaml.safe_dump(_card_scores())
    run_dir, entry = _run_1a(monkeypatch, tmp_path, _stage_text(scores), [DATED])
    out = yaml.safe_load((run_dir / "artifacts" / "extra_card_scores.yaml").read_text(encoding="utf-8"))
    assert [c["model_id"] for c in out["cards"]] == [DATED, DATED]
    assert [c["card"] for c in out["cards"]] == ["hypothesis_card_2.yaml", "hypothesis_card_3.yaml"]
    # brief-card-v1 enforcement at decide_next is unchanged: the stamped item still validates ...
    for item in out["cards"]:
        assert dn.validate_card_scores(item, "x")["model_id"] == DATED
    # ... and a wrong rubric is still refused
    bad = {**out["cards"][0], "rubric_version": "brief-card-v0"}
    with pytest.raises(dn.DecideNextError, match="brief-card-v1"):
        dn.validate_card_scores(bad, "x")
    # the other deliverable of the same stage is untouched
    assert (run_dir / "artifacts" / "hypothesis_card.yaml").read_text(encoding="utf-8") == "hypothesis_id: H-1"
    prov = entry["provenance"]
    assert prov["requested"] == REQUESTED and prov["observed_models"] == [DATED]
    cards = prov["cards"]
    assert cards["observed"] == DATED and cards["mismatch"] is False and cards["stamped"] is True
    assert cards["self_reported"] == {"hypothesis_card_2.yaml": "self-reported-model",
                                      "hypothesis_card_3.yaml": "self-reported-model"}
    assert cards["self_report_differs"] is True


def test_card_mismatch_is_recorded_and_the_stage_completes(monkeypatch, tmp_path):
    run_dir, entry = _run_1a(monkeypatch, tmp_path, _stage_text(yaml.safe_dump(_card_scores())),
                             ["claude-sonnet-4-5"])
    assert (run_dir / "artifacts" / "extra_card_scores.yaml").exists()
    assert entry["provenance"]["cards"]["mismatch"] is True


def test_an_unparseable_card_file_is_written_verbatim_and_recorded(monkeypatch, tmp_path):
    junk = "cards: [unclosed\n"
    run_dir, entry = _run_1a(monkeypatch, tmp_path, _stage_text(junk), [DATED])
    assert (run_dir / "artifacts" / "extra_card_scores.yaml").read_text(encoding="utf-8") == junk.strip()
    cards = entry["provenance"]["cards"]
    assert cards["stamped"] is False and cards["stamp_error"]


def test_a_stage_with_no_card_file_gets_only_the_base_provenance(monkeypatch, tmp_path):
    text = "```yaml\n# hypothesis_card.yaml\nhypothesis_id: H-1\n```\n"
    _, entry = _run_1a(monkeypatch, tmp_path, text, [DATED])
    assert entry["provenance"] == {"requested": REQUESTED, "observed_models": [DATED],
                                   "result_models": [DATED]}


def test_card_flag_off_file_and_audit_entry_are_unchanged(monkeypatch, tmp_path):
    scores = yaml.safe_dump(_card_scores())
    run_dir, entry = _run_1a(monkeypatch, tmp_path, _stage_text(scores), ["claude-sonnet-4-5"],
                             orchestrator=ALL_ON)
    assert _bytes(run_dir / "artifacts" / "extra_card_scores.yaml") == scores.strip().encode("utf-8")
    assert "provenance" not in entry


def test_card_scores_with_no_observed_model_are_left_as_written(monkeypatch, tmp_path):
    scores = yaml.safe_dump(_card_scores())
    run_dir, entry = _run_1a(monkeypatch, tmp_path, _stage_text(scores), [])
    assert _bytes(run_dir / "artifacts" / "extra_card_scores.yaml") == scores.strip().encode("utf-8")
    cards = entry["provenance"]["cards"]
    assert cards["observed"] is None and cards["mismatch"] is None and cards["stamped"] is False
    assert entry["provenance"]["observed_models"] == []
