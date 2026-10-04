"""
E-068 validation follow-up (operator, 2026-10-04): four robustness fixes found on
real runs (VALIDATION_RUN.md, O-20).

1. Parser: a `# name.yaml` line followed by blank lines before its fence is
   read (run_069: one blank line lost a two-card answer).
2. CUL-396: a retry inside _invoke_agent_with_yaml_retry has its own audit_log
   key; the first call's cost is no longer overwritten.
3. Retries are format repairs: the model's own first answer goes back verbatim
   with "keep the content", and step 1a's format note no longer names
   hypothesis_card.yaml as missing (a multi-card answer has none).
4. CUL-398: an R2 request on hold (blocked_on_*) counts as outstanding and holds
   its whole brief: R2 neither flips it ready nor mints a new request.
"""
import asyncio
import json
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import decide_next as dn  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
import test_c5_7b1_model_id_stamp as stamp  # noqa: E402

RUN_069 = (Path(__file__).parent / "fixtures" / "run_069_step1a_blank_line_before_fence.txt"
           ).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. The parser
# ---------------------------------------------------------------------------

def test_run_069s_two_card_answer_is_read():
    names = [n for n, _ in rpr._find_deliverable_blocks(RUN_069)]
    assert names == ["hypothesis_card_2.yaml", "hypothesis_card_3.yaml", "extra_card_scores.yaml"]
    bodies = dict(rpr._find_deliverable_blocks(RUN_069))
    assert yaml.safe_load(bodies["hypothesis_card_2.yaml"])["hypothesis_id"] == \
        "TIME_SERIES_MOMENTUM_UNSCALED"
    assert yaml.safe_load(bodies["hypothesis_card_3.yaml"])["hypothesis_id"] == \
        "TREND_FOLLOWING_MOMENTUM_WITH_VOLATILITY_REGIME_GATING"


@pytest.mark.parametrize("gap", ["\n", "\n\n", "  \n\t\n", "\r\n\r\n"])
def test_blank_lines_between_name_and_fence_are_read(gap):
    text = f"# a.yaml\n{gap}```yaml\nx: 1\n```\n"
    assert rpr._find_deliverable_blocks(text) == [("a.yaml", "x: 1\n")]


@pytest.mark.parametrize("between", ["\n\n\n\n\n", "\nsome prose\n", "\n# note\n"])  # 4 blank lines: too far
def test_anything_else_between_name_and_fence_is_not_read(between):
    text = f"# a.yaml{between}```yaml\nx: 1\n```\n"
    assert "a.yaml" not in [n for n, _ in rpr._find_deliverable_blocks(text)]


# ---------------------------------------------------------------------------
# 3. Retries carry the first answer; step 1a's note follows the multi-card rule
# ---------------------------------------------------------------------------

def _retry_harness(monkeypatch, tmp_path, stage, answers, expected_names):
    """answers: per call, (outcome dict, {file: text}). Returns (contexts, raised)."""
    run_dir = tmp_path / "run"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "pipeline_state.yaml").write_text(yaml.safe_dump({"status": "active"}),
                                                  encoding="utf-8")
    contexts = []

    async def fake_invoke(stage_name, run_id, retry_context=None):
        outcome, files = answers[len(contexts)]
        contexts.append(retry_context)
        for name, text in files.items():
            (run_dir / "artifacts" / name).write_text(text, encoding="utf-8")
        return outcome

    monkeypatch.setattr(rpr, "async_invoke_agent", fake_invoke)
    expected = [run_dir / "artifacts" / n for n in expected_names]
    raised = None
    try:
        rpr._invoke_agent_with_yaml_retry(stage, "run_x", run_dir, expected, {})
    except (FileNotFoundError, rpr.UnrepairableYAMLError) as e:
        raised = e
    return contexts, raised


def test_a_format_retry_in_step_1a_gets_its_first_answer_and_no_false_missing_file(
        monkeypatch, tmp_path):
    contexts, raised = _retry_harness(
        monkeypatch, tmp_path, "hypothesis_generation",
        [({"no_blocks": True, "answer": RUN_069}, {}),
         ({"saved": ["hypothesis_card.yaml"]}, {"hypothesis_card.yaml": "hypothesis_id: H\n"})],
        ["hypothesis_card.yaml"])
    assert raised is None and contexts[0] is None
    ctx = contexts[1]
    assert "Missing:" not in ctx                                   # run_069's contradiction
    assert "hypothesis_card_2.yaml" in ctx and "brief_status.yaml" in ctx
    assert "<<<PREVIOUS ANSWER\n" + RUN_069 + "\nPREVIOUS ANSWER>>>" in ctx
    assert "Keep its content exactly" in ctx


def test_a_format_retry_elsewhere_still_names_the_missing_files(monkeypatch, tmp_path):
    contexts, raised = _retry_harness(
        monkeypatch, tmp_path, "innovation_expansion",
        [({"no_blocks": True, "answer": "no blocks here"}, {}),
         ({"saved": ["a.yaml"]}, {"a.yaml": "x: 1\n"})],
        ["a.yaml"])
    assert raised is None
    assert "Missing: a.yaml" in contexts[1]
    assert "<<<PREVIOUS ANSWER\nno blocks here\nPREVIOUS ANSWER>>>" in contexts[1]


def test_a_yaml_retry_gets_its_first_answer(monkeypatch, tmp_path):
    first = "```yaml\n# a.yaml\nbroken: [unterminated\n```\n"
    contexts, raised = _retry_harness(
        monkeypatch, tmp_path, "innovation_expansion",
        [({"saved": ["a.yaml"], "answer": first}, {"a.yaml": "broken: [unterminated\n"}),
         ({"saved": ["a.yaml"]}, {"a.yaml": "x: 1\n"})],
        ["a.yaml"])
    assert raised is None
    assert "Parse error" in contexts[1]
    assert "<<<PREVIOUS ANSWER\n" + first + "\nPREVIOUS ANSWER>>>" in contexts[1]


def test_an_engine_without_an_answer_gets_the_plain_note(monkeypatch, tmp_path):
    contexts, _ = _retry_harness(
        monkeypatch, tmp_path, "innovation_expansion",
        [({"no_blocks": True}, {}), ({"saved": ["a.yaml"]}, {"a.yaml": "x: 1\n"})],
        ["a.yaml"])
    assert "PREVIOUS ANSWER" not in contexts[1]


def test_a_huge_first_answer_is_capped():
    ctx = rpr._with_previous_answer("note", "x" * (rpr._PREVIOUS_ANSWER_MAX_CHARS + 50))
    assert "[... previous answer truncated ...]" in ctx
    assert len(ctx) < rpr._PREVIOUS_ANSWER_MAX_CHARS + 1000


def test_the_retry_prompt_asks_for_a_repair_not_a_new_answer(tmp_path, monkeypatch):
    monkeypatch.chdir(SR_ROOT)
    run_dir = tmp_path / "runs" / "run_p"
    (run_dir / "artifacts").mkdir(parents=True)
    handoff = {"required_inputs": [], "optional_inputs": []}
    plain = rpr._build_stage_prompt("innovation_expansion", handoff, run_dir)
    retry = rpr._build_stage_prompt("innovation_expansion", handoff, run_dir, retry_context="CTX")
    assert retry.startswith(plain)                       # the first call's prompt is unchanged
    assert "format repair, not a new answer" in retry and "from scratch" not in retry
    assert "CTX" in retry and "CTX" not in plain


# ---------------------------------------------------------------------------
# 2. CUL-396: one audit key per call
# ---------------------------------------------------------------------------

def _worker(monkeypatch, tmp_path, text, retry_context=None, run_dir=None):
    stamp._set_orchestrator(stamp.ON)
    monkeypatch.chdir(SR_ROOT)
    if run_dir is None:
        run_dir = tmp_path / "runs" / "run_w"
        (run_dir / "artifacts").mkdir(parents=True)
        (run_dir / "pipeline_state.yaml").write_text(
            yaml.safe_dump({"status": "active", "audit_log": {}}), encoding="utf-8")
    monkeypatch.setattr(rpr, "query", stamp._stream(stamp._assistant(text, stamp.DATED),
                                                    stamp._result({stamp.DATED: {}})))
    handoff = {"required_inputs": [], "optional_inputs": [],
               "injected_context": {"stage_attempt": "0"}}
    out = asyncio.run(rpr.run_claude_worker("validation", handoff, run_dir,
                                            retry_context=retry_context))
    return out, run_dir


def test_a_retry_has_its_own_audit_key_and_the_first_call_is_kept(monkeypatch, tmp_path):
    out1, run_dir = _worker(monkeypatch, tmp_path, "No blocks here.")
    _worker(monkeypatch, tmp_path, "Still none.", retry_context="CTX", run_dir=run_dir)
    log = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    assert set(log) == {"validation_attempt_0", "validation_attempt_0_retry"}
    assert out1 == {"no_blocks": True, "answer": "No blocks here."}


def test_a_first_call_keeps_its_old_key(monkeypatch, tmp_path):
    out, run_dir = _worker(monkeypatch, tmp_path, "```yaml\n# a.yaml\nx: 1\n```\n")
    assert set(rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]) == \
        {"validation_attempt_0"}
    assert out["saved"] == ["a.yaml"] and out["answer"].startswith("```yaml")


# ---------------------------------------------------------------------------
# 4. CUL-398: a hold holds the brief
# ---------------------------------------------------------------------------

def _owner(oid="B", priority=1):
    return {"id": oid, "brief_path": f"briefs/{oid}.md", "status": "done",
            "brief_status": "open", "priority": priority}


def _req(oid, n, status, outcome=None):
    e = {"id": f"{oid}__more_{n}", "brief_path": f"briefs/{oid}.md", "status": status,
         "origin": "brief", "priority": 999}
    if outcome:
        e["outcome"] = outcome
    return e


@pytest.mark.parametrize("status", ["blocked_on_e068", "blocked_on_component:Foo"])
def test_a_held_request_is_outstanding(status):
    assert dn.r2_request_yielded({"status": status}) is None


def test_r2_never_flips_or_mints_past_a_hold():
    entries = [_owner("B"), _req("B", 1, "blocked_on_e068")]
    out = dn._r2(entries, select=True)
    assert out["fired"] is False and out["held_briefs"] == ["B"]
    assert out["eligible_briefs"] == [] and out["enqueued"] == [] and out["ready"] == []


def test_a_hold_on_one_brief_does_not_stop_another():
    entries = [_owner("B"), _req("B", 1, "blocked_on_e068"), _owner("C", priority=2)]
    out = dn._r2(entries, select=True)
    assert out["held_briefs"] == ["B"] and out["eligible_briefs"] == ["C"]
    assert out["ready"] == ["C__more_1"]


def test_a_released_hold_lets_r2_ask_again():
    entries = [_owner("B"), _req("B", 1, "done", outcome="refuted")]
    out = dn._r2(entries, select=True)
    assert out["held_briefs"] == [] and out["ready"] == ["B__more_2"]


def test_a_hold_neither_counts_nor_breaks_the_empty_streak():
    owner = _owner("B")
    entries = [owner, _req("B", 1, "done", outcome="completed_brief_exhausted"),
               _req("B", 2, "blocked_on_e068"),
               _req("B", 3, "done", outcome="completed_brief_exhausted")]
    assert dn.consecutive_empty_r2(owner, entries) == ["B__more_1", "B__more_3"]


def test_the_decision_record_schema_accepts_held_briefs():
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas" /
                         "decision_record.schema.json").read_text(encoding="utf-8"))
    r2 = dn._r2([_owner("B"), _req("B", 1, "blocked_on_e068")], select=True)
    jsonschema.validate({k: v for k, v in r2.items() if not k.startswith("_")},
                        schema["properties"]["rules"]["properties"]["r2"])
