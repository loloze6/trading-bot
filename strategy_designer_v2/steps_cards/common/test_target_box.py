"""Tests of the target box (common/target_box.md): the rule, the run's file, the theme note, the brief's check, the
visibility field."""
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


def test_the_rule_counts_exact_names_divides_the_share_and_breaks_ties_by_the_map():
    shares = {p: 0.1 for p in tb.PROFILES} | {"rising agitated": 0.2, "falling calm": 0.3}
    strategies = [{"named": "agitated", "side": "long"}, {"named": "rising", "side": "long"},          # not exact
                  {"named": "falling calm", "side": "long"}, {"named": "falling calm", "side": "both"},
                  {"named": None, "side": "long"}]
    c = tb.choose(strategies=strategies, shares=shares)
    rows = {(r["profile"], r["side"]): r for r in c["table"]}
    assert rows[("rising agitated", "long")]["named_exactly"] == 0 and rows[("rising agitated", "long")]["in_map"] == 2
    assert rows[("falling calm", "long")]["named_exactly"] == 2 and rows[("falling calm", "short")]["named_exactly"] == 1
    assert rows[("falling calm", "short")]["score"] == pytest.approx(0.15)
    # rising agitated: 0.2 on both sides; the tie goes to the side with fewer strategies acting there at all (short: 0)
    assert c["box"] == ("rising agitated", "short")
    assert (c["table"][1]["profile"], c["table"][1]["side"]) == ("rising agitated", "long")
    c = tb.choose(strategies=[], shares=shares)
    assert c["box"][0] == "falling calm"


def write_box(root, run, profile="falling calm", side="long"):
    f = tb.box_file(run, root)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"profile": profile, "side": side}))


def test_the_theme_note_is_empty_without_a_box_and_names_the_box_with_one(tmp_path):
    assert tb.theme_note("a_run", tmp_path) == ""
    write_box(tmp_path, "a_run")
    n = tb.theme_note("a_run", tmp_path)
    assert "falling calm markets, long positions" in n and "`profile: falling calm`" in n and "off the brief's theme" in n


def test_a_boxed_run_s_brief_names_a_profile_and_a_side_holding_the_box():
    box = {"profile": "falling calm", "side": "long"}
    ok = ("---\nprofile: falling calm\nside: long only\n---\nx", "---\nprofile: falling\nside: long and short\n---\nx",
          "---\nprofile: calm\nside: long only\n---\nx")
    for t in ok:
        assert tb.brief_refusal(t, box) is None, t
    assert "no profile" in tb.brief_refusal("---\nside: long only\n---\nx", box)
    assert "does not hold" in tb.brief_refusal("---\nprofile: rising calm\nside: long only\n---\nx", box)
    assert "no side" in tb.brief_refusal("---\nprofile: falling calm\n---\nx", box)
    assert "not long" in tb.brief_refusal("---\nprofile: falling calm\nside: short only\n---\nx", box)


def test_whether_an_idea_acts_in_the_box_is_read_from_its_own_profile_and_side(tmp_path):
    box = {"profile": "rising agitated", "side": "long"}
    idea = lambda prof, side="long": ("---\nbrief: 003_b\n" + (f"profile: {prof}\n" if prof else "")
                                      + (f"side: {side}\n" if side else "") + "---\nIdea: x.\n")
    for prof, inside in (("rising agitated", True), ("rising", True), ("agitated", True), ("rising calm", False),
                         ("choppy", False), (None, False)):
        assert tb.in_box(idea(prof), "a_run", box, tmp_path) is inside, prof
    for side in ("short", "both", None, "long only"):                 # not the box's side, or unknown: outside
        assert not tb.in_box(idea("rising", side), "a_run", box, tmp_path), side


def test_an_idea_s_side_is_its_own_line_else_its_brief_s_only(tmp_path):
    d = tmp_path / "01_brief" / "b_run" / "briefs"
    d.mkdir(parents=True)
    (d / "003_short.md").write_text("---\nside: short only\n---\nA theory.\n")
    (d / "004_both.md").write_text("---\nside: long and short\n---\nA theory.\n")
    (d / "005_none.md").write_text("---\n---\nA theory.\n")
    idea = lambda brief, side=None: f"---\nbrief: {brief}\n" + (f"side: {side}\n" if side else "") + "---\nIdea: x.\n"
    assert tb.idea_side(idea("003_short", "long"), "b_run", tmp_path) == "long"        # its own line first
    assert tb.idea_side(idea("004_both", "both"), "b_run", tmp_path) == "both"
    assert tb.idea_side(idea("003_short"), "b_run", tmp_path) == "short"               # written before the line: the brief's "only"
    assert tb.idea_side(idea("003_short", "short only"), "b_run", tmp_path) == "short"  # a brief's line copied by step 2, before
    assert tb.idea_side(idea("004_both"), "b_run", tmp_path) is None                   # "long and short": unknown
    assert tb.idea_side(idea("005_none"), "b_run", tmp_path) is None                   # no side line: unknown
    assert tb.idea_side(idea("009_missing"), "b_run", tmp_path) is None                # no brief found: unknown


def test_the_earlier_ideas_sides_file_is_read_third_and_unknown_stays_unknown(tmp_path):
    d = tmp_path / "01_brief" / "b_run" / "briefs"
    d.mkdir(parents=True)
    (d / "003_short.md").write_text("---\nside: short only\n---\nA theory.\n")
    (d / "004_both.md").write_text("---\nside: long and short\n---\nA theory.\n")
    (tmp_path / "common").mkdir()
    rec = lambda side: {"side": side}
    (tmp_path / "common" / "earlier_idea_sides.json").write_text(json.dumps({"ideas": {
        "i1": rec("long"), "i2": rec("long"), "i3": rec("unknown"), "i4": rec("long"), "i5": rec("maybe")}}))
    idea = lambda brief, side=None: f"---\nbrief: {brief}\n" + (f"side: {side}\n" if side else "") + "---\nIdea: x.\n"
    s = lambda text, i: tb.idea_side(text, "b_run", tmp_path, i)
    assert s(idea("004_both"), "i1") == "long"                        # 3. the file, when the line and the brief say nothing
    assert s(idea("004_both", "short"), "i1") == "short"              # 1. the idea's own line beats the file
    assert s(idea("003_short"), "i2") == "short"                      # 2. the brief's "only" beats the file
    assert s(idea("004_both"), "i3") is None                          # unknown stays unknown
    assert s(idea("004_both"), "i5") is None                          # a word outside the three: unknown
    assert s(idea("004_both"), "i9") is None and s(idea("004_both"), None) is None   # not in the file / no id
    box = {"profile": "falling calm", "side": "long"}
    text = "---\nbrief: 004_both\nprofile: falling calm\n---\nIdea: x.\n"
    assert tb.in_box(text, "b_run", box, tmp_path, "i4") is True and tb.in_box(text, "b_run", box, tmp_path, "i3") is False


def test_the_run_s_box_is_written_once_and_kept(tmp_path, monkeypatch):
    assert tb.start("a_run", None, tmp_path) is None and not tb.box_file("a_run", tmp_path).exists()
    b = tb.start("a_run", "rising agitated, long", tmp_path)
    assert b["profile"] == "rising agitated" and b["side"] == "long" and b["chosen_by"] == "the operator"
    assert json.loads(tb.box_file("a_run", tmp_path).read_text()) == b
    assert tb.start("a_run", None, tmp_path) == b and tb.start("a_run", "auto", tmp_path) == b      # resumed: kept
    with pytest.raises(SystemExit):
        tb.start("a_run", "falling calm, short", tmp_path)            # another box: refused
    with pytest.raises(SystemExit):
        tb.start("b_run", "rising, long", tmp_path)                   # not one of the twelve
    monkeypatch.setattr(tb, "choose", lambda steps: {"box": ("falling calm", "long"), "table": [], "strategies": 3,
                                                     "shares_from": "v3", "candidates_read": 3})
    b = tb.start("c_run", "auto", tmp_path)
    assert (b["profile"], b["side"]) == ("falling calm", "long") and b["chosen_by"].startswith("the rule")
