"""D-172 (PR-12, run_098 analyst re-run): an invented claim key is refused by name, with the
allowed keys, and the analyst skill's claim example lists those keys.

The refusal text is claim_card.check_claim's; this pins it as the analyst hears it (through
analyst_session.check_answer and the retry section), with the keys read from the one source,
claim_card.CLAIM_KEYS. The retry itself is not changed here: run_phase1_research's analyst loop
already runs `for attempt in range(2)` and appends asm.retry_section(...) after any refusal.
"""
from __future__ import annotations

import sys
from pathlib import Path

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import analyst_session as asm  # noqa: E402
import claim_card as cc  # noqa: E402

import test_e075_pr4_queries as q4  # noqa: E402
from test_e075_pr5_analyst import RUN_ID, _claim_answer, _entries_for_claim  # noqa: E402

INVENTED = {"rationale_end": "x", "pass_if_note": "y", "fail_if_note": "z"}


def _errors(text):
    return asm.check_answer(
        text, lens="forecast", run_id=RUN_ID, entries=_entries_for_claim(),
        claim_check=lambda claim: cc.check_claim(claim, folds=True, trade_tests=True),
        holdout_start=q4.HOLDOUT, fold="A", model_id="m")[2]


def test_the_refusal_names_each_invented_key_and_every_allowed_key():
    errors = _errors(_claim_answer(claim=INVENTED))
    (msg,) = [e for e in errors if "unknown keys" in e]
    for bad in INVENTED:
        assert repr(bad) in msg, msg
    allowed = msg.split("allowed:", 1)[1]
    for key in cc.CLAIM_KEYS:                       # the one source, not a second copy
        assert repr(key) in allowed, (key, msg)
    for bad in INVENTED:
        assert repr(bad) not in allowed, msg


def test_an_answer_with_only_allowed_keys_has_no_key_refusal():
    assert not [e for e in _errors(_claim_answer()) if "unknown keys" in e]


def test_the_retry_section_carries_the_key_refusal_to_the_second_session():
    errors = _errors(_claim_answer(claim={"rationale_end": "x"}))
    section = asm.retry_section(_claim_answer(claim={"rationale_end": "x"}), errors,
                                _entries_for_claim())
    assert "'rationale_end'" in section and "allowed:" in section
    for key in cc.CLAIM_KEYS:
        assert repr(key) in section, key


def test_the_analyst_skill_claim_example_lists_exactly_the_allowed_keys():
    skill = (SR_ROOT / "workflow_artifacts/skills/analyst/SKILL.md").read_text(encoding="utf-8")
    (line,) = [ln for ln in skill.splitlines() if "allowed keys of claim" in ln]
    listed = {k.strip() for k in line.split(":", 1)[1].split(",")}
    assert listed == set(cc.CLAIM_KEYS), (listed, sorted(cc.CLAIM_KEYS))
    # the line sits inside the claim example, between `claim:` and its first key
    assert "outcome: claim\nclaim:\n  # allowed keys of claim" in skill.replace("\r\n", "\n")
