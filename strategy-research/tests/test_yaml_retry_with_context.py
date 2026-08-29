"""
F4b (2026-07-05): the generic retry-with-context fallback. When a stage's
deliverable is unrepairable YAML, `_invoke_agent_with_yaml_retry` must re-invoke
the SAME stage exactly once with the parse error + offending lines appended to
the prompt (via `async_invoke_agent`'s `retry_context` param), and only fail to
human if the retry's output ALSO fails. `yaml_retry_count` must be logged to
pipeline_state.yaml on the retry.

The LLM call itself is mocked (no real API call) — this tests the retry
plumbing, not model behavior.
"""

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
WORKFLOW_PATH = ROOT / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402


def _make_run_dir(tmp_path, run_id="test_run"):
    run_dir = tmp_path / run_id
    (run_dir / "artifacts").mkdir(parents=True)
    # update_state() requires pipeline_state.yaml to already exist — true in the
    # real pipeline (setup_run.py always creates it before any stage runs).
    (run_dir / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"run_id": run_id, "yaml_retry_count": 0}), encoding="utf-8"
    )
    return run_dir


def test_retry_succeeds_after_one_bad_attempt(tmp_path, monkeypatch):
    run_dir = _make_run_dir(tmp_path)
    target = run_dir / "artifacts" / "hypothesis_card.yaml"

    calls = {"n": 0, "retry_contexts": []}

    async def fake_async_invoke_agent(stage_name, run_id, retry_context=None):
        calls["n"] += 1
        calls["retry_contexts"].append(retry_context)
        if calls["n"] == 1:
            # Simulate the real run_047 failure: a colon on a wrapped continuation
            # line that _quote_yaml_line alone can't fix (F4b path exercises this
            # too, but here we force straight to "still broken after repair" by
            # using a shape _repair_yaml truly can't handle: an unmatched brace).
            target.write_text(
                "hypothesis_id: H-TEST\nbroken: [unterminated\n", encoding="utf-8"
            )
        else:
            target.write_text("hypothesis_id: H-TEST\nfixed: true\n", encoding="utf-8")

    monkeypatch.setattr(rpr, "async_invoke_agent", fake_async_invoke_agent)

    state = {"yaml_retry_count": 0}
    rpr._invoke_agent_with_yaml_retry(
        "hypothesis_generation", "test_run", run_dir, [target], state
    )

    assert calls["n"] == 2
    assert calls["retry_contexts"][0] is None  # first attempt: no prior error yet
    assert calls["retry_contexts"][1] is not None  # retry: error context was built
    assert (
        "broken" in calls["retry_contexts"][1]
        or "Parse error" in calls["retry_contexts"][1]
    )
    assert yaml.safe_load(target.read_text(encoding="utf-8"))["fixed"] is True


def test_retry_fails_to_human_if_second_attempt_also_broken(tmp_path, monkeypatch):
    run_dir = _make_run_dir(tmp_path)
    target = run_dir / "artifacts" / "hypothesis_card.yaml"

    calls = {"n": 0}

    async def fake_async_invoke_agent(stage_name, run_id, retry_context=None):
        calls["n"] += 1
        target.write_text("still: [broken\n", encoding="utf-8")

    monkeypatch.setattr(rpr, "async_invoke_agent", fake_async_invoke_agent)

    state = {"yaml_retry_count": 0}
    with pytest.raises(rpr.UnrepairableYAMLError):
        rpr._invoke_agent_with_yaml_retry(
            "hypothesis_generation", "test_run", run_dir, [target], state
        )

    assert calls["n"] == 2  # first attempt + exactly one retry, then give up


def test_yaml_retry_count_logged_to_pipeline_state(tmp_path, monkeypatch):
    run_dir = _make_run_dir(tmp_path)
    target = run_dir / "artifacts" / "hypothesis_card.yaml"
    state_path = run_dir / "pipeline_state.yaml"

    calls = {"n": 0}

    async def fake_async_invoke_agent(stage_name, run_id, retry_context=None):
        calls["n"] += 1
        if calls["n"] == 1:
            target.write_text("broken: [unterminated\n", encoding="utf-8")
        else:
            target.write_text("fixed: true\n", encoding="utf-8")

    monkeypatch.setattr(rpr, "async_invoke_agent", fake_async_invoke_agent)

    state = rpr.load_yaml(state_path)
    rpr._invoke_agent_with_yaml_retry(
        "hypothesis_generation", "test_run", run_dir, [target], state
    )

    updated_state = rpr.load_yaml(state_path)
    assert updated_state["yaml_retry_count"] == 1


def test_default_no_retry_context_on_first_attempt_success(tmp_path, monkeypatch):
    """Non-regression: when the first attempt succeeds outright, no retry
    happens and no yaml_retry_count increment occurs."""
    run_dir = _make_run_dir(tmp_path)
    target = run_dir / "artifacts" / "hypothesis_card.yaml"

    calls = {"n": 0}

    async def fake_async_invoke_agent(stage_name, run_id, retry_context=None):
        calls["n"] += 1
        target.write_text("hypothesis_id: H-TEST\ngood: true\n", encoding="utf-8")

    monkeypatch.setattr(rpr, "async_invoke_agent", fake_async_invoke_agent)

    state = {"yaml_retry_count": 0}
    rpr._invoke_agent_with_yaml_retry(
        "hypothesis_generation", "test_run", run_dir, [target], state
    )

    assert calls["n"] == 1
    state_after = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state_after["yaml_retry_count"] == 0  # update_state never called
