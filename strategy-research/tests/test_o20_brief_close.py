"""
O-20 (operator, 2026-10-04): a brief closes on step 1a's word only after two
CONSECUTIVE independent "exhausted" answers (one per queue entry). A single one
is recorded and the brief stays open. Every close names the rule that closed it
(two exhausted answers, or the empty-R2 streak) so the operator can reopen,
and a reopen marker stops the same history from closing it again.
"""
import sys
from pathlib import Path

import pytest

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import decide_next as dn  # noqa: E402
import run_campaign as camp  # noqa: E402

E = "completed_brief_exhausted"


def _owner(status="done", outcome="refuted", **kw):
    e = {"id": "B", "brief_path": "briefs/B.md", "status": status, "priority": 1,
         "brief_status": "open"}
    if outcome:
        e["outcome"] = outcome
    e.update(kw)
    return e


def _req(n, status="done", outcome=None):
    e = {"id": f"B__more_{n}", "brief_path": "briefs/B.md", "status": status,
         "origin": "brief", "priority": 999}
    if outcome:
        e["outcome"] = outcome
    return e


# ---------------------------------------------------------------------------
# consecutive_exhausted
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rows,expected", [
    ([(1, "done", E), (2, "done", E)], ["B__more_1", "B__more_2"]),
    ([(1, "done", E), (2, "done", "refuted"), (3, "done", E)], ["B__more_3"]),          # a card resets
    ([(1, "done", E), (2, "done", "completed_no_new_hypothesis"), (3, "done", E)],
     ["B__more_3"]),                                                                   # a repeat is an answer
    ([(1, "done", E), (2, "done", "quarantined_engineering_failure"), (3, "done", E)],
     ["B__more_1", "B__more_3"]),                                                      # no answer: skipped
    ([(1, "done", E), (2, "blocked_on_e068", None), (3, "done", E)], ["B__more_1", "B__more_3"]),
    ([(1, "done", E), (2, "paused:unhandled_exception", None)], ["B__more_1"]),
    ([(1, "done", E), (2, "ready", None)], ["B__more_1"]),
    ([(2, "done", E), (1, "done", "refuted")], ["B__more_2"]),                          # number order
])
def test_consecutive_exhausted(rows, expected):
    owner = _owner()
    entries = [owner] + [_req(n, s, o) for n, s, o in rows]
    assert dn.consecutive_exhausted(owner, entries) == expected


def test_the_owners_own_answer_counts_first():
    owner = _owner(outcome=E)
    assert dn.consecutive_exhausted(owner, [owner, _req(1, "done", E)]) == ["B", "B__more_1"]


def test_an_unfinished_owner_does_not_count():
    owner = _owner(status="in_progress", outcome=None)
    assert dn.consecutive_exhausted(owner, [owner, _req(1, "done", E)]) == ["B__more_1"]


@pytest.mark.parametrize("marker,expected", [
    (None, ["B", "B__more_1", "B__more_2"]),       # no marker: the whole history counts
    ("B", ["B__more_1", "B__more_2"]),             # the owner's own answer no longer counts
    ("B__more_1", ["B__more_2"]),
    ("B__more_2", [])])
def test_the_reopen_marker_drops_the_history(marker, expected):
    owner = _owner(outcome=E, brief_reopened_after=marker)
    entries = [owner, _req(1, "done", E), _req(2, "done", E)]
    assert dn.consecutive_exhausted(owner, entries) == expected


def test_the_reopen_marker_also_resets_the_empty_streak():
    owner = _owner(brief_reopened_after="B__more_2")
    entries = [owner, _req(1, "done", E), _req(2, "done", E)]
    assert dn.consecutive_empty_r2(owner, entries) == []
    entries.append(_req(3, "done", E))
    assert dn.consecutive_empty_r2(owner, entries) == ["B__more_3"]


@pytest.mark.parametrize("bad", ["C__more_1", "B__more_x", "nonsense"])
def test_a_reopen_marker_naming_nothing_fails_loud(bad):
    owner = _owner(brief_reopened_after=bad)
    with pytest.raises(dn.DecideNextError, match="brief_reopened_after"):
        dn.consecutive_exhausted(owner, [owner, _req(1, "done", E)])


# ---------------------------------------------------------------------------
# run_campaign._brief_updates
# ---------------------------------------------------------------------------

def _updates(entries, finished_id, monkeypatch):
    logs = []
    monkeypatch.setattr(camp, "_log", lambda msg: logs.append(msg))
    entry = next(e for e in entries if e["id"] == finished_id)
    return camp._brief_updates({"queue": entries}, entry), logs


def test_a_single_exhausted_answer_is_recorded_and_the_brief_stays_open(monkeypatch):
    entries = [_owner(), _req(1, "done", E)]
    up, logs = _updates(entries, "B__more_1", monkeypatch)
    assert up == {"B": {"brief_exhausted_answers": ["B__more_1"]}}
    assert any(m.startswith("BRIEF-EXHAUSTED-ONCE B:") and "1 of 2" in m for m in logs)


def test_two_consecutive_answers_close_the_brief_and_name_the_rule(monkeypatch):
    entries = [_owner(), _req(1, "done", E), _req(2, "done", E)]
    up, logs = _updates(entries, "B__more_2", monkeypatch)
    assert up["B"]["brief_status"] == "exhausted"
    assert up["B"]["brief_status_reason"] == "two_exhausted_answers"
    assert up["B"]["brief_status_rule"].startswith("two consecutive step-1a 'exhausted' answers")
    assert "B__more_1, B__more_2" in up["B"]["brief_status_rule"]
    assert up["B"]["brief_exhausted_answers"] == ["B__more_1", "B__more_2"]
    assert any(m.startswith("BRIEF-EXHAUSTED B:") for m in logs)


def test_the_empty_streak_close_names_its_rule(monkeypatch):
    """Q1 (operator): one exhausted answer then a failed run still closes the
    brief through the termination streak -- with a reason naming THAT rule."""
    entries = [_owner(), _req(1, "done", E), _req(2, "done", "quarantined_engineering_failure")]
    up, _ = _updates(entries, "B__more_2", monkeypatch)
    assert up["B"]["brief_status"] == "exhausted"
    assert up["B"]["brief_status_reason"] == "no_new_hypothesis"
    assert up["B"]["brief_status_rule"].startswith("empty-R2 streak: 2 consecutive R2 requests")
    assert "B__more_1, B__more_2" in up["B"]["brief_status_rule"]


def test_a_card_clears_a_stale_single_answer(monkeypatch):
    entries = [_owner(brief_exhausted_answers=["B__more_1"]), _req(1, "done", E),
               _req(2, "done", "refuted")]
    up, _ = _updates(entries, "B__more_2", monkeypatch)
    assert up == {"B": {"brief_exhausted_answers": []}}


def test_a_brief_with_no_answers_gets_no_new_field(monkeypatch):
    entries = [_owner(), _req(1, "done", "refuted")]
    up, _ = _updates(entries, "B__more_1", monkeypatch)
    assert up == {}


def test_a_reopened_brief_is_not_closed_again_by_its_history(monkeypatch):
    entries = [_owner(brief_reopened_after="B__more_2"), _req(1, "done", E), _req(2, "done", E),
               _req(3, "done", E)]
    up, logs = _updates(entries, "B__more_3", monkeypatch)
    assert up == {"B": {"brief_exhausted_answers": ["B__more_3"]}}
    assert any("BRIEF-EXHAUSTED-ONCE" in m for m in logs)


def test_a_reader_candidate_entry_touches_no_brief(monkeypatch):
    entries = [_owner(), {"id": "cand_1", "status": "done", "outcome": E, "origin": "reader"}]
    up, _ = _updates(entries, "cand_1", monkeypatch)
    assert "B" not in up


# ---------------------------------------------------------------------------
# Independence: the next request never sees the earlier "exhausted" reason
# ---------------------------------------------------------------------------

def test_the_next_requests_context_carries_no_earlier_reason(monkeypatch):
    saved = {}
    monkeypatch.setattr(camp.orch, "save_yaml", lambda path, doc: saved.update(doc))
    monkeypatch.setattr(dn, "brief_hypothesis_ids", lambda root, queue, path: ["H1"])
    entries = [_owner(brief_exhausted_answers=["B__more_1"]), _req(1, "done", E),
               _req(2, "ready")]
    camp._write_brief_hypotheses_context({"queue": entries}, entries[2], "run_x")
    assert set(saved) == {"schema_version", "queue_entry", "brief_owner", "brief_path",
                          "request", "already_produced"}
    assert "exhausted" not in str(saved)
