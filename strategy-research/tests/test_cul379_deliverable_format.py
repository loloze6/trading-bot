"""
CUL-379: a stage answer whose file name sits outside the YAML fence is read,
and a missing deliverable gets one retry with a format reminder.

run_065 (C4 on Kraken, 2026-10-02): step 1a wrote a valid hypothesis_card.yaml
but put `# hypothesis_card.yaml` on the line ABOVE the ```yaml fence. The
parser only reads the name inside the fence, so nothing was saved and the run
halted on "Missing files" -- F4b retries only unparseable YAML. The real raw
answer is the fixture below.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
from test_c5_7b1_model_id_stamp import DATED, _run_1a  # noqa: E402
from test_deliverable_block_parser import UNPREFIXED_SAMPLES  # noqa: E402

RUN_065 = (Path(__file__).parent / "fixtures" / "run_065_step1a_name_outside_fence.txt"
           ).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. The parser
# ---------------------------------------------------------------------------

def test_run_065s_answer_is_read():
    assert rpr._DELIVERABLE_BLOCK_RE.findall(RUN_065) == []  # the bug
    [(name, body)] = rpr._find_deliverable_blocks(RUN_065)
    assert name == "hypothesis_card.yaml"
    assert yaml.safe_load(body)["hypothesis_id"] == "C4_donchian_daily_trend"


@pytest.mark.parametrize("text", UNPREFIXED_SAMPLES)
def test_answers_with_names_inside_the_fence_parse_exactly_as_before(text):
    assert rpr._find_deliverable_blocks(text) == rpr._DELIVERABLE_BLOCK_RE.findall(text)


def test_a_fence_named_inside_is_not_read_twice():
    text = "# hypothesis_card.yaml\n```yaml\n# hypothesis_card.yaml\nhypothesis_id: H\n```\n"
    assert [n for n, _ in rpr._find_deliverable_blocks(text)] == ["hypothesis_card.yaml"]


def test_mixed_forms_keep_answer_order():
    text = ("```yaml\n# a.yaml\nx: 1\n```\n\n# b.yaml\n```yaml\ny: 2\n```\n"
            "```yaml\n# c.yaml\nz: 3\n```\n")
    assert [n for n, _ in rpr._find_deliverable_blocks(text)] == ["a.yaml", "b.yaml", "c.yaml"]


@pytest.mark.parametrize("header", ["# ../../campaign_record/feed_wishlist.yaml",
                                    "# other/x.yaml", "Here is # x.yaml"])
def test_a_name_above_the_fence_follows_the_same_name_rule(header):
    text = f"{header}\n```yaml\nx: 1\n```\n"
    assert rpr._find_deliverable_blocks(text) == []


def test_the_worker_saves_run_065s_card(monkeypatch, tmp_path):
    run_dir, _entry = _run_1a(monkeypatch, tmp_path, RUN_065, [DATED])
    card = rpr.load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml")
    assert card["hypothesis_id"] == "C4_donchian_daily_trend"
    assert not (run_dir / "artifacts" / "debug_validation_raw_output.txt").exists()


# ---------------------------------------------------------------------------
# 2. One retry when a deliverable is missing
# ---------------------------------------------------------------------------

def _retry_harness(monkeypatch, tmp_path, stage, answers):
    """Drive _invoke_agent_with_yaml_retry with a fake agent: `answers` is a
    list of (outcome, files to write) per call. Returns (calls, raised)."""
    run_dir = tmp_path / "run"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "pipeline_state.yaml").write_text(yaml.safe_dump({"status": "active"}),
                                                  encoding="utf-8")
    calls = []

    async def fake_invoke(stage_name, run_id, retry_context=None):
        outcome, files = answers[len(calls)]
        calls.append(retry_context)
        for f in files:
            (run_dir / "artifacts" / f).write_text("x: 1\n", encoding="utf-8")
        return outcome

    monkeypatch.setattr(rpr, "async_invoke_agent", fake_invoke)
    expected = [run_dir / "artifacts" / n for n in ("hypothesis_card.yaml", "other.yaml")]
    raised = None
    try:
        rpr._invoke_agent_with_yaml_retry(stage, "run_x", run_dir, expected, {})
    except FileNotFoundError as e:
        raised = e
    return calls, raised, run_dir


def test_no_readable_block_is_retried_once_with_the_format(monkeypatch, tmp_path):
    calls, raised, run_dir = _retry_harness(
        monkeypatch, tmp_path, "hypothesis_generation",
        [({"no_blocks": True}, []), ({"saved": ["x"]}, ["hypothesis_card.yaml", "other.yaml"])])
    assert raised is None and len(calls) == 2
    assert calls[0] is None
    assert "Missing: hypothesis_card.yaml, other.yaml" in calls[1]
    assert "```yaml\n# <file_name>.yaml" in calls[1]
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml")["format_retry_count"] == 1


def test_a_second_miss_still_fails_to_a_human(monkeypatch, tmp_path):
    calls, raised, _ = _retry_harness(
        monkeypatch, tmp_path, "innovation_expansion",
        [({"no_blocks": True}, []), ({"no_blocks": True}, [])])
    assert isinstance(raised, FileNotFoundError) and len(calls) == 2


def test_a_partial_answer_is_retried_outside_step_1a(monkeypatch, tmp_path):
    """O-11 item 5: step 2 once wrote 1 of its 3 files."""
    calls, raised, _ = _retry_harness(
        monkeypatch, tmp_path, "innovation_expansion",
        [({"saved": ["other.yaml"]}, ["other.yaml"]), ({"saved": ["x"]}, ["hypothesis_card.yaml"])])
    assert raised is None and len(calls) == 2
    assert "Missing: hypothesis_card.yaml" in calls[1] and "other.yaml" not in calls[1].split("Missing:")[1].splitlines()[0]


def test_a_partial_answer_in_step_1a_is_not_retried(monkeypatch, tmp_path):
    """In 1a a missing card with other blocks present is how a multi-card split
    or an exhausted brief reaches its handler -- never re-asked."""
    calls, raised, _ = _retry_harness(
        monkeypatch, tmp_path, "hypothesis_generation",
        [({"saved": ["brief_status.yaml"]}, ["other.yaml"])])
    assert isinstance(raised, FileNotFoundError) and len(calls) == 1


def test_an_engine_that_reports_nothing_is_not_retried(monkeypatch, tmp_path):
    calls, raised, _ = _retry_harness(monkeypatch, tmp_path, "innovation_expansion", [(None, [])])
    assert isinstance(raised, FileNotFoundError) and len(calls) == 1


def _worker_outcome(monkeypatch, tmp_path, text):
    """The real run_claude_worker's return value for one stubbed answer."""
    import asyncio
    import test_c5_7b1_model_id_stamp as stamp
    stamp._set_orchestrator(stamp.ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = tmp_path / "runs" / "run_w"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"status": "active", "audit_log": {}}), encoding="utf-8")
    monkeypatch.setattr(rpr, "query", stamp._stream(stamp._assistant(text, DATED),
                                                    stamp._result({DATED: {}})))
    handoff = {"required_inputs": [], "optional_inputs": [], "injected_context": {"stage_attempt": "0"}}
    return asyncio.run(rpr.run_claude_worker("validation", handoff, run_dir))


def test_the_worker_reports_an_answer_without_any_block(monkeypatch, tmp_path):
    assert _worker_outcome(monkeypatch, tmp_path, "No blocks here.") == {"no_blocks": True}


def test_the_worker_reports_what_it_saved(monkeypatch, tmp_path):
    assert _worker_outcome(monkeypatch, tmp_path, RUN_065) == {"saved": ["hypothesis_card.yaml"]}
