"""Tests of run_brief's own logic (no model call, no backtest): the brief's ideas, the budget, the checks."""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_brief as rb  # noqa: E402

HELPER = Path(__file__).resolve().parent / "run_brief.py"


def test_a_brief_s_ideas_are_those_with_its_number(tmp_path):
    for n in ("012-01_a", "012-02_b", "002-01_c", "012-01_a.b1_d"):
        (tmp_path / f"{n}.md").write_text("x")
    assert [p.stem for p in rb.ideas_of(Path("012_some-theory.md"), tmp_path)] == ["012-01_a", "012-02_b"]   # not a line's idea


def test_the_budget_is_the_run_s_total(tmp_path):
    assert rb.spent(tmp_path) == 0.0
    (tmp_path / "journal.jsonl").write_text(json.dumps({"usd": 0.25}) + "\n" + json.dumps({"usd": 0.5}) + "\n")
    assert rb.spent(tmp_path) == 0.75


def run(*args):
    return subprocess.run([sys.executable, str(HELPER), *args], capture_output=True, text=True)


def test_refused_before_any_call(tmp_path):
    brief = tmp_path / "012_x.md"
    brief.write_text("---\n---\nA theory.\n")
    assert "ends in _run" in run(str(brief), "--run", "x", "--python", "p").stderr
    assert "exactly one" in run("--run", "x_run", "--python", "p").stderr
    assert "exactly one" in run(str(brief), "--theme", "t", "--run", "x_run", "--python", "p").stderr
    assert "no brief file" in run(str(tmp_path / "nope.md"), "--run", "x_run", "--python", "p").stderr
    assert "positive" in run(str(brief), "--run", "x_run", "--python", "p", "--budget", "0").stderr


def test_step_1_answers_read_by_write_brief():
    # topic 50: a source whose only theory is already a brief gets no new brief; the existing one is named
    out = "already indexed: 033_swing-scaled-fall-next-day-rebound\ncost: 0.06 USD, attempts: 1\n"
    assert rb.ALREADY_INDEXED.search(out).group(1) == "033_swing-scaled-fall-next-day-rebound"
    assert not rb.BRIEF_LINE.search(out) and not rb.NOT_RESEARCHABLE.search(out)
