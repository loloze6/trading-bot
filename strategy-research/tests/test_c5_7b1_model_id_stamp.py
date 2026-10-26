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

from _reader_test_helpers import (  # noqa: E402,F401  (D-197: the shared reader-test helpers)
    ALL_ON, BASELINE_ENTRY_KEYS, DATED, ON, REQUESTED, RUN_ID, _assistant, _bytes, _loaded, _one_proposal,
    _reader_text, _result, _run_1a, _seed_run, _set_orchestrator, _stream, _stub_tbot_python,
)
from test_e059_s2a_decide_next import _decide, _one_source, _patch  # noqa: E402

CAT = "profitability"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

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


def test_flag_on_alone_reads_true():
    """D-198: no dependency any more (it required specialist_readers)."""
    _set_orchestrator({"score_provenance": {"enabled": True}})
    assert rpr._score_provenance_enabled() is True


def test_the_launch_preflight_reads_and_refuses_it():
    assert "score_provenance" in camp._flag_readers()
    _set_orchestrator({**ALL_ON, "score_provenance": {"enabled": "true"}})
    refusal = camp._flag_preflight_refusal()
    assert refusal and "orchestrator.score_provenance.enabled='true'" in refusal
    _set_orchestrator(ON)
    values, refusal = camp._flag_preflight()
    assert refusal is None and values["score_provenance"] is True


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
# 3. (D-198: the reader stamp, the reader flag-off identity and decide_next's stamped reader
#     proposals went with the readers; the brief-card stamp below stays)
# ---------------------------------------------------------------------------

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
