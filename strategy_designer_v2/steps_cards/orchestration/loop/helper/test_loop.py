"""Tests of loop's own logic (no model call, no backtest): stopping, failures, the goal mark, the turns."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import loop  # noqa: E402


def test_stopping():
    assert loop.stop_reason(None, 99.0, [{"idea": "x"}]) is None                      # no budget: no limit
    assert loop.stop_reason(3.0, 3.2, [{"idea": "x"}]).startswith("budget reached")
    assert loop.stop_reason(3.0, 1.0, []) == "no candidate left"


def test_goal_mark():
    assert loop.goal({"step5": "confirmed (+2.20)", "step6": "profitable enough"})
    assert not loop.goal({"step5": "confirmed (+2.20)", "step6": "not profitable enough (failed: Calmar)"})
    assert not loop.goal(None)


def test_turns_spend_and_failures(tmp_path):
    (tmp_path / "run_idea" / "x_run").mkdir(parents=True)
    (tmp_path / "run_idea" / "x_run" / "table.json").write_text(json.dumps([{"idea": "a", "cost": 1.25}, {"idea": "b", "cost": 0.5}]))
    assert loop.spent("x_run", tmp_path) == 1.75
    loop.log_turn("x_run", {"turn": 1, "idea": "a"}, tmp_path)
    loop.log_turn("x_run", {"idea": "c", "outcome": "failed: step 3 wrote no plan"}, tmp_path)
    loop.log_turn("x_run", {"stop": "budget reached", "spent": 1.75}, tmp_path)
    assert len(loop.turns("x_run", tmp_path)) == 3 and loop.failed("x_run", tmp_path) == {"c"}
    assert loop.next_turn("x_run", tmp_path) == 2                  # stop and failure lines are not turns


def test_the_queue_marks_a_goal(tmp_path):
    (tmp_path / "run_idea" / "x_run").mkdir(parents=True)
    (tmp_path / "run_idea" / "x_run" / "table.json").write_text(json.dumps(
        [{"idea": "a", "cost": 1.0, "step5": "confirmed (+2.2)", "step6": "profitable enough"}]))
    loop.write_queue("x_run", [{"idea": "b", "line": "7.e", "generation": 1, "record": 0.75, "score": 0.375, "status": "candidate"},
                               {"idea": "a", "line": "step 2", "generation": 0, "record": 0.25, "score": 0.25, "status": "tested"}], tmp_path)
    q = (tmp_path / "loop" / "x_run" / "queue.md").read_text()
    assert "| 1 | b | 7.e |" in q and "GOAL REACHED" in q and "Spent: 1.00 USD" in q
