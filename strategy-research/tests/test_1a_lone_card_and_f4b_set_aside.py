"""
run_067 (2026-10-04), two step-1a stops on a real run:

1. Step 1a wrote ONE card named hypothesis_card_2.yaml (BRIEF_HYPOTHESES.md's
   name for the first of several cards). The split handler needs two or more,
   so the run stopped on a missing hypothesis_card.yaml. Fix: one numbered card
   is one card (`_adopt_lone_numbered_card`, step 1a only).
2. F4b: the YAML-repair retry wrote a different file name, and the check re-read
   the first attempt's broken file, so the retry could never succeed. Fix: the
   broken file is moved to .previous_attempts/<stage>_yaml_retry<n>/ before the
   retry (`_set_aside_unrepairable`).

The LLM call is mocked; these test the plumbing, not the model.
"""
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "workflow"))

import run_phase1_research as rpr  # noqa: E402

BROKEN = "hypothesis_id: H-TEST\nbroken: [unterminated\n"
GOOD = "hypothesis_id: H-TEST\nfixed: true\n"


def _make_run_dir(tmp_path, run_id="test_run"):
    run_dir = tmp_path / run_id
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"run_id": run_id, "yaml_retry_count": 0}), encoding="utf-8")
    return run_dir


def _fake_agent(calls, writes):
    """writes: one dict {file name: text} per call, in order."""
    async def fake(stage_name, run_id, retry_context=None):
        n = calls["n"]
        calls["n"] += 1
        calls["retry_contexts"].append(retry_context)
        for name, text in writes[n].items():
            (calls["arts"] / name).write_text(text, encoding="utf-8")
    return fake


def _run(monkeypatch, run_dir, stage, writes, expected="hypothesis_card.yaml"):
    arts = run_dir / "artifacts"
    calls = {"n": 0, "retry_contexts": [], "arts": arts}
    monkeypatch.setattr(rpr, "async_invoke_agent", _fake_agent(calls, writes))
    rpr._invoke_agent_with_yaml_retry(stage, "test_run", run_dir, [arts / expected],
                                      {"yaml_retry_count": 0})
    return calls


def test_run_067_reproduction_retry_writes_numbered_card(tmp_path, monkeypatch):
    """The exact run_067 sequence: a broken hypothesis_card.yaml, then a retry
    that writes only hypothesis_card_2.yaml. Before the fix: UnrepairableYAMLError
    on the stale file. After: the retry's card is the run's card."""
    run_dir = _make_run_dir(tmp_path)
    arts = run_dir / "artifacts"
    calls = _run(monkeypatch, run_dir, "hypothesis_generation",
                 [{"hypothesis_card.yaml": BROKEN}, {"hypothesis_card_2.yaml": GOOD}])
    assert calls["n"] == 2
    assert yaml.safe_load((arts / "hypothesis_card.yaml").read_text(encoding="utf-8"))["fixed"] is True
    assert not (arts / "hypothesis_card_2.yaml").exists()
    kept = run_dir / ".previous_attempts" / "hypothesis_generation_yaml_retry1" / "hypothesis_card.yaml"
    assert kept.read_text(encoding="utf-8") == BROKEN


def test_lone_numbered_card_on_first_attempt_is_the_card(tmp_path, monkeypatch):
    run_dir = _make_run_dir(tmp_path)
    arts = run_dir / "artifacts"
    calls = _run(monkeypatch, run_dir, "hypothesis_generation", [{"hypothesis_card_2.yaml": GOOD}])
    assert calls["n"] == 1
    assert (arts / "hypothesis_card.yaml").read_text(encoding="utf-8") == GOOD
    assert list(arts.glob("hypothesis_card_*.yaml")) == []


def test_two_numbered_cards_are_left_to_the_split(tmp_path, monkeypatch):
    run_dir = _make_run_dir(tmp_path)
    arts = run_dir / "artifacts"
    with pytest.raises(FileNotFoundError):
        _run(monkeypatch, run_dir, "hypothesis_generation",
             [{"hypothesis_card_2.yaml": GOOD, "hypothesis_card_3.yaml": GOOD}])
    assert not (arts / "hypothesis_card.yaml").exists()
    assert sorted(p.name for p in arts.glob("hypothesis_card_*.yaml")) == [
        "hypothesis_card_2.yaml", "hypothesis_card_3.yaml"]


def test_card_plus_numbered_card_is_untouched(tmp_path, monkeypatch):
    """Ambiguous output stays ambiguous: the review-fix-8 check downstream refuses it."""
    run_dir = _make_run_dir(tmp_path)
    arts = run_dir / "artifacts"
    _run(monkeypatch, run_dir, "hypothesis_generation",
         [{"hypothesis_card.yaml": GOOD, "hypothesis_card_2.yaml": BROKEN}])
    assert (arts / "hypothesis_card.yaml").read_text(encoding="utf-8") == GOOD
    assert (arts / "hypothesis_card_2.yaml").read_text(encoding="utf-8") == BROKEN


def test_adoption_is_step_1a_only(tmp_path, monkeypatch):
    run_dir = _make_run_dir(tmp_path)
    arts = run_dir / "artifacts"
    with pytest.raises(FileNotFoundError):
        _run(monkeypatch, run_dir, "innovation_expansion", [{"hypothesis_card_2.yaml": GOOD}])
    assert (arts / "hypothesis_card_2.yaml").exists()
    assert not (arts / "hypothesis_card.yaml").exists()


def test_f4b_sets_the_broken_file_aside_on_any_stage(tmp_path, monkeypatch):
    run_dir = _make_run_dir(tmp_path)
    arts = run_dir / "artifacts"
    calls = _run(monkeypatch, run_dir, "innovation_expansion",
                 [{"innovation_notes.yaml": BROKEN}, {"innovation_notes.yaml": GOOD}],
                 expected="innovation_notes.yaml")
    assert calls["n"] == 2
    assert (arts / "innovation_notes.yaml").read_text(encoding="utf-8") == GOOD
    kept = run_dir / ".previous_attempts" / "innovation_expansion_yaml_retry1" / "innovation_notes.yaml"
    assert kept.read_text(encoding="utf-8") == BROKEN


def test_f4b_retry_without_the_file_still_fails_loud(tmp_path, monkeypatch):
    """The retry writes nothing: the set-aside must not hide the failure."""
    run_dir = _make_run_dir(tmp_path)
    with pytest.raises(FileNotFoundError):
        _run(monkeypatch, run_dir, "innovation_expansion",
             [{"innovation_notes.yaml": BROKEN}, {}], expected="innovation_notes.yaml")


def test_failed_set_aside_never_stops_the_retry(tmp_path, monkeypatch):
    run_dir = _make_run_dir(tmp_path)
    arts = run_dir / "artifacts"

    def boom(*a, **k):
        raise OSError("locked")

    monkeypatch.setattr(rpr.shutil, "move", boom)
    calls = _run(monkeypatch, run_dir, "innovation_expansion",
                 [{"innovation_notes.yaml": BROKEN}, {"innovation_notes.yaml": GOOD}],
                 expected="innovation_notes.yaml")
    assert calls["n"] == 2
    assert (arts / "innovation_notes.yaml").read_text(encoding="utf-8") == GOOD


def test_a_stale_numbered_card_is_never_adopted(tmp_path, monkeypatch):
    """review round 1: a lone hypothesis_card_2.yaml left by an earlier attempt
    (claim_tests off: nothing is set aside on a resume) and a new answer that
    writes no card -> still the loud missing-card stop, never a silent adoption."""
    run_dir = _make_run_dir(tmp_path)
    arts = run_dir / "artifacts"
    (arts / "hypothesis_card_2.yaml").write_text(GOOD, encoding="utf-8")
    with pytest.raises(FileNotFoundError):
        _run(monkeypatch, run_dir, "hypothesis_generation", [{}, {}])
    assert (arts / "hypothesis_card_2.yaml").exists()
    assert not (arts / "hypothesis_card.yaml").exists()


def test_a_stale_numbered_card_rewritten_by_this_call_is_adopted(tmp_path, monkeypatch):
    run_dir = _make_run_dir(tmp_path)
    arts = run_dir / "artifacts"
    (arts / "hypothesis_card_2.yaml").write_text(BROKEN, encoding="utf-8")
    _run(monkeypatch, run_dir, "hypothesis_generation", [{"hypothesis_card_2.yaml": GOOD}])
    assert (arts / "hypothesis_card.yaml").read_text(encoding="utf-8") == GOOD


def test_a_lone_broken_numbered_card_gets_the_f4b_retry(tmp_path, monkeypatch):
    run_dir = _make_run_dir(tmp_path)
    arts = run_dir / "artifacts"
    calls = _run(monkeypatch, run_dir, "hypothesis_generation",
                 [{"hypothesis_card_2.yaml": BROKEN}, {"hypothesis_card_2.yaml": GOOD}])
    assert calls["n"] == 2 and calls["retry_contexts"][1] is not None
    assert (arts / "hypothesis_card.yaml").read_text(encoding="utf-8") == GOOD
    kept = run_dir / ".previous_attempts" / "hypothesis_generation_yaml_retry1" / "hypothesis_card.yaml"
    assert kept.read_text(encoding="utf-8") == BROKEN


def test_a_second_f4b_retry_keeps_the_first_set_aside_copy(tmp_path, monkeypatch):
    """review round 1 nit: shutil.move overwrites; each retry has its own folder."""
    run_dir = _make_run_dir(tmp_path)
    arts = run_dir / "artifacts"
    calls = {"n": 0, "retry_contexts": [], "arts": arts}
    writes = [{"innovation_notes.yaml": BROKEN}, {"innovation_notes.yaml": GOOD},
              {"innovation_notes.yaml": "second: [broken\n"}, {"innovation_notes.yaml": GOOD}]
    monkeypatch.setattr(rpr, "async_invoke_agent", _fake_agent(calls, writes))
    for count in (0, 1):
        rpr._invoke_agent_with_yaml_retry("innovation_expansion", "test_run", run_dir,
                                          [arts / "innovation_notes.yaml"], {"yaml_retry_count": count})
    prev = run_dir / ".previous_attempts"
    assert (prev / "innovation_expansion_yaml_retry1" / "innovation_notes.yaml").read_text(
        encoding="utf-8") == BROKEN
    assert (prev / "innovation_expansion_yaml_retry2" / "innovation_notes.yaml").read_text(
        encoding="utf-8") == "second: [broken\n"
