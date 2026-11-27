"""Tests of the target box (common/target_box.md): the rule, the run's file, which ideas act in the box."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import target_box as tb  # noqa: E402


def test_a_box_is_one_of_twelve():
    assert tb.parse_box("rising agitated, long") == ("rising agitated", "long")
    assert tb.parse_box("Agitated rising market, SHORT") == ("rising agitated", "short")
    for bad in ("rising, long", "rising agitated", "rising agitated, long and short", "calm agitated, long", ""):
        assert tb.parse_box(bad) is None, bad
    assert len(tb.BOXES) == 12


def test_the_rule_counts_exact_names_only_and_divides_the_share():
    shares = {p: 0.1 for p in tb.PROFILES} | {"rising agitated": 0.2, "falling calm": 0.3}
    strategies = [{"named": "agitated", "side": "long"}, {"named": "rising", "side": "both"},        # not exact
                  {"named": "falling calm", "side": "long"}, {"named": "falling calm", "side": "both"},
                  {"named": None, "side": "long"}]
    c = tb.choose(strategies=strategies, shares=shares)
    rows = {(r["profile"], r["side"]): r for r in c["table"]}
    assert rows[("rising agitated", "long")]["named_exactly"] == 0
    assert rows[("falling calm", "long")]["named_exactly"] == 2 and rows[("falling calm", "short")]["named_exactly"] == 1
    assert rows[("falling calm", "short")]["score"] == pytest.approx(0.15)
    # falling calm short 0.3 / 2 = 0.15 < rising agitated 0.2 / 1; the tie of its two sides goes to long (the boxes' order)
    assert c["box"] == ("rising agitated", "long") and c["table"][1]["side"] == "short"
    c = tb.choose(strategies=strategies, shares=shares | {"choppy agitated": 0.2})       # equal score: the larger share
    assert c["box"] == ("rising agitated", "long")
    c = tb.choose(strategies=[], shares=shares)
    assert c["box"] == ("falling calm", "long")


def idea(text_profile=None, brief="003_b"):
    return f"---\nbrief: {brief}\n" + (f"profile: {text_profile}\n" if text_profile else "") + "---\nIdea: x.\n"


def brief(root, run, side=None, bid="003_b"):
    d = root / "01_brief" / run / "briefs"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{bid}.md").write_text("---\n" + (f"side: {side}\n" if side else "") + "---\nA theory.\n")


def test_which_ideas_act_in_the_box(tmp_path):
    box = {"profile": "rising agitated", "side": "long"}
    brief(tmp_path, "a_run")                                         # no side line: both sides
    for prof, inside in (("rising agitated", True), ("rising", True), ("agitated", True), ("Agitated, rising", True),
                         ("rising calm", False), ("falling agitated", False), ("choppy", False), (None, False),
                         ("none", False)):
        assert tb.in_box(idea(prof), "a_run", box, tmp_path) is inside, prof
    brief(tmp_path, "b_run", "short only")
    assert not tb.in_box(idea("rising"), "b_run", box, tmp_path)
    assert tb.in_box(idea("rising"), "b_run", {**box, "side": "short"}, tmp_path)
    brief(tmp_path, "c_run", "long only")
    assert tb.in_box(idea("agitated"), "c_run", box, tmp_path)
    assert tb.in_box(idea("rising"), "d_run", box, tmp_path)         # a brief not found: both sides, as step 3
    assert tb.in_box(idea("choppy calm"), "b_run", {"profile": "choppy", "side": "both"}, tmp_path)   # an older header


def test_the_run_s_box_is_written_once_and_kept(tmp_path, monkeypatch):
    assert tb.start("a_run", None, tmp_path) is None and not tb.box_file("a_run", tmp_path).exists()
    b = tb.start("a_run", "rising agitated, long", tmp_path)
    assert b["profile"] == "rising agitated" and b["side"] == "long" and b["chosen_by"] == "the operator"
    assert json.loads(tb.box_file("a_run", tmp_path).read_text()) == b
    assert tb.start("a_run", None, tmp_path) == b and tb.start("a_run", "auto", tmp_path) == b      # resumed: kept
    assert tb.start("a_run", "Rising agitated, long", tmp_path) == b
    with pytest.raises(SystemExit):
        tb.start("a_run", "falling calm, short", tmp_path)            # another box: refused
    with pytest.raises(SystemExit):
        tb.start("b_run", "rising, long", tmp_path)                   # not one of the twelve
    monkeypatch.setattr(tb, "choose", lambda steps: {"box": ("falling calm", "long"), "table": [], "strategies": 3, "read": 3})
    b = tb.start("c_run", "auto", tmp_path)
    assert (b["profile"], b["side"]) == ("falling calm", "long") and b["chosen_by"].startswith("the rule")
