"""Tests of the earlier ideas' sides pass (common/target_box.md, "The earlier ideas' sides"). No model is called."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import earlier_idea_sides as eis  # noqa: E402

TEXT = "Idea: In a rising, calm market, a coin keeps rising.\nConsequence: A trader buys."


def test_an_answer_outside_the_four_words_is_refused_and_recorded_unknown():
    assert eis.parse_answer("long\nIdea: In a rising, calm market, a coin keeps rising.", TEXT)[:3] == (
        "long", "Idea: In a rising, calm market, a coin keeps rising.", True)
    assert eis.parse_answer("Short.\n", TEXT)[0] == "short"
    assert eis.parse_answer("unknown\n", TEXT) == ("unknown", "", False, None)
    for bad in ("maybe long\nx", "The idea bets long", "", "```\nlong"):
        side, _, _, note = eis.parse_answer(bad, TEXT)
        assert side == "unknown" and note.startswith("refused"), bad


def test_a_sentence_not_found_in_the_idea_is_flagged_not_dropped():
    assert eis.parse_answer("long\nA trader buys.", TEXT)[2] is True
    assert eis.parse_answer("long\nSomething the idea never said.", TEXT)[:3] == ("long", "Something the idea never said.", False)


def test_the_model_is_given_the_idea_and_consequence_lines_only():
    text = "---\nbrief: b\nprofile: rising calm\n---\nIdea: i.\nConsequence: c.\nWhy:\n- F3: next return +0.5 % (t 3.1).\n"
    assert eis.idea_text(text) == "Idea: i.\nConsequence: c."


def test_the_pass_is_for_untested_exact_profile_ideas_with_no_known_side(tmp_path, monkeypatch):
    files = {}
    for n, h in (("a", "profile: rising calm\n"), ("b", "profile: rising\n"), ("c", "brief: z\n"),
                 ("d", "profile: falling agitated\n"), ("e", "profile: falling calm\nside: long\n")):
        files[n] = ("r1_run", tmp_path / f"{n}.md")
        files[n][1].write_text(f"---\n{h}---\nIdea: x.\nConsequence: y.\n")
    monkeypatch.setattr(eis, "earlier_ideas", lambda steps: files)
    monkeypatch.setattr(eis.target_box, "answered", lambda steps: {"d"})              # d has a step 5 answer
    todo, why = eis.concerned(tmp_path)
    assert {i: (r, p) for i, (r, _, p) in todo.items()} == {"a": ("r1_run", "rising calm")}
    assert dict(why) == {"profile not exact": 2, "tested": 1, "side already known": 1}


def test_the_pass_is_resumable_an_idea_already_in_the_file_is_not_asked_again(tmp_path, monkeypatch):
    path = tmp_path / "sides.json"
    eis.save(path, {"a": {"side": "long", "cost_usd": 0.0}})
    monkeypatch.setattr(eis, "concerned", lambda steps: ({i: ("r_run", Path("x"), "rising calm") for i in "ab"}, {}))
    asked = []
    monkeypatch.setattr(eis, "ask_one", lambda i, r, f, p, m: asked.append(i) or {"side": "short", "cost_usd": 0.01})
    spent, stopped = eis.ask(["a", "b"], "m", path, workers=1)
    assert asked == ["b"] and not stopped
    assert {i: r["side"] for i, r in eis.load(path).items()} == {"a": "long", "b": "short"}


def test_the_pass_stops_when_the_spend_passes_the_cap(tmp_path, monkeypatch):
    path = tmp_path / "sides.json"
    monkeypatch.setattr(eis, "concerned", lambda steps: ({i: ("r_run", Path("x"), "rising calm") for i in "abcd"}, {}))
    monkeypatch.setattr(eis, "ask_one", lambda i, r, f, p, m: {"side": "long", "cost_usd": 1.0})
    spent, stopped = eis.ask(list("abcd"), "m", path, max_usd=2.0, workers=1)
    assert stopped and sorted(eis.load(path)) == ["a", "b"]
