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


def test_an_idea_stopped_mid_run_is_unfinished(tmp_path):
    (tmp_path / "run_idea" / "x_run").mkdir(parents=True)
    (tmp_path / "run_idea" / "x_run" / "table.json").write_text(json.dumps([{"idea": "a", "cost": 1.0}]))
    loop.log_turn("x_run", {"turn": 1, "idea": "a"}, tmp_path)
    loop.log_turn("x_run", {"turn": 2, "idea": "b"}, tmp_path)          # stopped before its row was written
    loop.log_turn("x_run", {"turn": 3, "idea": "c"}, tmp_path)
    loop.log_turn("x_run", {"idea": "c", "outcome": "failed: step 3 wrote no plan"}, tmp_path)
    assert loop.unfinished("x_run", tmp_path) == ["b"]



def test_the_components_step_is_called_every_10_turns_and_before_stopping(tmp_path, monkeypatch):
    root = tmp_path / "orchestration"
    for i in range(1, 12):
        loop.log_turn("x_run", {"turn": i, "idea": f"i{i}"}, root)
    assert loop.turns_since_components("x_run", root) == 11
    loop.log_turn("x_run", {"components": "3 wishes answered", "outcome": "ok"}, root)
    loop.log_turn("x_run", {"turn": 12, "idea": "i12"}, root)
    assert loop.turns_since_components("x_run", root) == 1
    # its cost counts in the run's spend
    (root / "run_idea" / "x_run").mkdir(parents=True)
    (root / "run_idea" / "x_run" / "table.json").write_text(json.dumps([{"idea": "a", "cost": 1.0}]))
    (tmp_path / "components").mkdir()
    (tmp_path / "components" / "journal.jsonl").write_text(
        json.dumps({"run": "x_run", "usd": 0.5}) + "\n" + json.dumps({"run": "y_run", "usd": 9.0}) + "\n")
    assert loop.spent("x_run", root) == 1.5
    # when it is due
    args = type("A", (), {"run": "x_run"})()
    monkeypatch.setattr(loop, "ORCH", root)
    monkeypatch.setattr(loop.wishes, "open_wishes", lambda runs, root=None: [("x_run", "p", "w", "t")])
    assert not loop.components_due(args, None)                       # 1 turn since its last call
    assert loop.components_due(args, "no candidate left")            # but the loop would stop
    loop.log_turn("x_run", {"components": "failed", "outcome": "failed (exit 1)"}, root)
    assert not loop.components_due(args, "no candidate left")        # never twice without a turn between
    monkeypatch.setattr(loop.wishes, "open_wishes", lambda runs, root=None: [])
    for i in range(13, 25):
        loop.log_turn("x_run", {"turn": i, "idea": f"i{i}"}, root)
    assert not loop.components_due(args, None)                       # no open wish: nothing to call


def test_a_turn_line_carries_a_full_utc_timestamp(tmp_path):
    import re
    loop.log_turn("x_run", {"turn": 1, "idea": "a"}, tmp_path)
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", loop.turns("x_run", tmp_path)[0]["at"])


def test_a_failed_components_call_is_not_a_failed_idea(tmp_path):
    """Night 1h (2026-11-19): a components call that ended in failure is a line with no idea; failed() read it as one."""
    loop.log_turn("x_run", {"turn": 1, "idea": "a"}, tmp_path)
    loop.log_turn("x_run", {"components": "x_run | p | W | cannot build", "outcome": "failed (exit -15)"}, tmp_path)
    loop.log_turn("x_run", {"idea": "c", "outcome": "failed: step 3 wrote no plan"}, tmp_path)
    assert loop.failed("x_run", tmp_path) == {"c"}


def test_an_idea_turned_again_after_its_row_is_unfinished_until_its_row_is_written_again(tmp_path):
    """017-02 (intraday_1h_run, 2026-11-19): refused at step 3 (a row), unblocked by the components step, turned again,
    cut before its backtest: unfinished, though it has a row. A row without its end time (written before) counts as
    finished, as before."""
    d = tmp_path / "run_idea" / "x_run"
    d.mkdir(parents=True)
    log = tmp_path / "loop" / "x_run"
    log.mkdir(parents=True)
    turns = [{"at": "2026-11-19T00:10:00Z", "turn": 1, "idea": "a"}, {"at": "2026-11-19T00:20:00Z", "turn": 2, "idea": "b"},
             {"at": "2026-11-19T08:50:00Z", "turn": 3, "idea": "a"}]
    (log / "loop.jsonl").write_text("".join(json.dumps(x) + "\n" for x in turns))
    rows = [{"idea": "a", "finished_at": "2026-11-19T00:13:00Z"}, {"idea": "b"}]
    (d / "table.json").write_text(json.dumps(rows))
    assert loop.unfinished("x_run", tmp_path) == ["a"]
    rows[0]["finished_at"] = "2026-11-19T09:30:00Z"                   # run_idea finished it: its row written again
    (d / "table.json").write_text(json.dumps(rows))
    assert loop.unfinished("x_run", tmp_path) == []



def test_a_retry_line_makes_a_failed_idea_a_candidate_again(tmp_path):
    loop.log_turn("x_run", {"idea": "c", "outcome": "failed: model call failed"}, tmp_path)
    assert loop.failed("x_run", tmp_path) == {"c"}
    loop.log_turn("x_run", {"idea": "c", "outcome": "retry: its failure was the model service's, not the idea's"}, tmp_path)
    assert loop.failed("x_run", tmp_path) == set()


def test_a_refused_call_stops_the_loop_and_marks_nothing_failed(tmp_path):
    (tmp_path / "run_idea" / "x_run").mkdir(parents=True)
    (tmp_path / "run_idea" / "x_run" / "table.json").write_text("[]")
    assert not loop.refused("x_run", "a", 1, ["a bug"], tmp_path)
    assert loop.refused("x_run", "a", loop.SERVICE_REFUSED, ["model call refused by the service: limit"], tmp_path)
    t = loop.turns("x_run", tmp_path)
    assert t[-1]["stop"].startswith(loop.REFUSED) and loop.failed("x_run", tmp_path) == set()


def test_a_resumed_idea_does_not_run_past_the_budget(tmp_path, monkeypatch):
    # night 3: ideas re-admitted by retry lines counted as unfinished and ran before the budget check (58 of 35 USD)
    monkeypatch.setattr(loop, "ORCH", tmp_path)
    run = "x_run"
    (tmp_path / "run_idea" / run).mkdir(parents=True)
    (tmp_path / "run_idea" / run / "table.json").write_text(json.dumps([{"idea": "done", "cost": 40.0}]))
    monkeypatch.setattr(loop, "table_rows", lambda r, root=tmp_path: json.loads((tmp_path / "run_idea" / run / "table.json").read_text()))
    monkeypatch.setattr(loop, "spent", lambda r, root=tmp_path: 40.0)
    monkeypatch.setattr(loop, "unfinished", lambda r, root=tmp_path: ["a"])
    monkeypatch.setattr(loop.select_next, "written_in", lambda r: [tmp_path / "a.md"])
    called = []
    monkeypatch.setattr(loop, "call_run_idea", lambda *a, **k: called.append(a) or (0, [""]))
    monkeypatch.setattr(loop, "log_turn", lambda r, e, root=tmp_path: None)
    monkeypatch.setattr(sys, "argv", ["loop.py", "--run", run, "--python", "py", "--budget", "35"])
    loop.main()
    assert called == []                                              # stopped on the budget before the resumed idea


def test_each_discovery_becomes_a_brief_once(tmp_path, monkeypatch):
    """Topic 50: a discovery a line wrote (07?_*/<run>/<backtest>/discoveries/) goes through step 1 and step 2 once;
    logged in loop.jsonl; a refused model call stops the loop and leaves the discovery for the resume."""
    from types import SimpleNamespace
    steps, orch = tmp_path / "steps", tmp_path / "steps" / "orchestration"
    for n in ("031-01_x.g1_weekday-carry", "031-02_y.e1_other"):
        f = steps / "07g_patterns" / "x_run" / "031-01_x_1d" / "discoveries" / f"{n}.md"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("The pattern: ...")
    calls = []
    monkeypatch.setattr(loop.run_brief, "write_brief", lambda run, source, model=None: (calls.append(source.stem) or Path(f"040_{source.stem}.md"), None))
    monkeypatch.setattr(loop.run_brief, "write_ideas", lambda run, brief, model=None: ([Path("040-01_a.md")], None))
    args = SimpleNamespace(run="x_run", budget=None, model=None)
    assert loop.brief_discoveries(args, steps, orch) and loop.brief_discoveries(args, steps, orch)
    assert calls == ["031-01_x.g1_weekday-carry", "031-02_y.e1_other"]                 # once each
    lines = [t for t in loop.turns("x_run", orch) if "discovery" in t]
    assert [t["ideas"] for t in lines] == [1, 1] and all(t["outcome"] == "ok" for t in lines)

    (steps / "07g_patterns" / "x_run" / "031-01_x_1d" / "discoveries" / "031-03_z.g2_new.md").write_text("x")
    def refuse(run, source, model=None):
        raise SystemExit(loop.SERVICE_REFUSED)
    monkeypatch.setattr(loop.run_brief, "write_brief", refuse)
    assert loop.brief_discoveries(args, steps, orch) is False
    assert "031-03" not in " ".join(loop.briefed("x_run", orch)) and "stop" in loop.turns("x_run", orch)[-1]


def test_a_boxed_run_s_turns_say_whether_the_idea_acts_in_the_box(tmp_path):
    """The operator, 2026-11-27 (common/target_box.md): visibility, not control. Nothing in a run without a box."""
    f = tmp_path / "003-01_a.md"
    f.write_text("---\nbrief: 003_b\nprofile: falling\n---\nIdea: a.\n")
    assert loop.box_field("a_run", f, tmp_path) == {}
    box = tmp_path / "orchestration" / "loop" / "a_run" / "target_box.json"
    box.parent.mkdir(parents=True)
    box.write_text(json.dumps({"profile": "falling calm", "side": "long"}))
    assert loop.box_field("a_run", f, tmp_path) == {"in_box": True}
    box.write_text(json.dumps({"profile": "rising calm", "side": "long"}))
    assert loop.box_field("a_run", f, tmp_path) == {"in_box": False}
