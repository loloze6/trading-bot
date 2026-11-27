"""Tests of step 2's code (no model call): reading the answer, the bar size an idea may state."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))
import make_ideas as M  # noqa: E402

ANSWER = """idea: price falls in the 2 hours before 08:00 UTC
consequence: crowded longs sell before paying
short-name: pre settlement drop
index-line: a drop before settlement
side: short
bar: 1h
---
idea: a weekend move reverses on Monday
consequence: thin weekend liquidity
short-name: weekend reversal
index-line: weekend reversal
side: both
---
idea: a move within the day
consequence: c
short-name: x y
index-line: z
side: long
bar: 15m because finer
already-indexed: none
"""


def test_an_idea_may_state_bar_1h_only():
    ideas, already = M.parse(ANSWER)
    assert [i[4] for i in ideas] == ["1h", None, None]        # no line: none; anything but 1h: dropped
    assert already == "none"


def test_an_idea_may_name_one_market_profile():
    # topic 49: one of the six profiles, written in any order or case; "none" or no line: none; anything else refused
    answer = ("idea: a sharp fall rebounds\nconsequence: c\nshort-name: a b c\nindex-line: x\nside: long\nprofile: Falling, agitated\n---\n"
              "idea: a weekend move reverses\nconsequence: c\nshort-name: d e f\nindex-line: y\nside: long\nprofile: none\n---\n"
              "idea: a third\nconsequence: c\nshort-name: g h i\nindex-line: z\nside: short\nprofile: choppy\nalready-indexed: none\n")
    ideas, _ = M.parse(answer)
    assert [i[5] for i in ideas] == ["falling agitated", None, "choppy"]
    import pytest
    with pytest.raises(ValueError):
        M.parse("idea: a\nconsequence: c\nshort-name: a b c\nindex-line: x\nside: long\nprofile: bull market\nalready-indexed: none\n")
    with pytest.raises(ValueError):
        M.parse("idea: a\nconsequence: c\nshort-name: a b c\nindex-line: x\nside: long\nprofile: rising or falling\nalready-indexed: none\n")


def test_every_idea_states_its_side():
    """A12 (common/idea_definition.md): long, short or both, on its own line; missing or unknown: refused."""
    import pytest
    ideas, _ = M.parse(ANSWER)
    assert [i[6] for i in ideas] == ["short", "both", "long"]
    block = "idea: a\nconsequence: c\nshort-name: a b c\nindex-line: x\n{}already-indexed: none\n"
    assert M.parse(block.format("side: Long\n"))[0][0][6] == "long"
    for bad in ("", "side: long only\n", "side: up\n", "side: long or short\n"):
        with pytest.raises(ValueError, match="side"):
            M.parse(block.format(bad))


def test_an_idea_file_has_its_own_side_line_not_its_brief_s(tmp_path, monkeypatch):
    brief = tmp_path / "007_some-theory.md"
    brief.write_text("---\nbar: 1d\nside: long only\n---\nA theory.\n")
    monkeypatch.setattr(M, "call", lambda model, system, request: (
        "idea: a\nconsequence: c\nshort-name: a b c\nindex-line: x\nside: long\nprofile: calm\nalready-indexed: none\n", 0.0))
    monkeypatch.setattr(sys, "argv", ["make_ideas.py", str(brief), "--ideas-dir", str(tmp_path / "ideas")])
    M.main()
    text = (tmp_path / "ideas" / "007-01_a-b-c.md").read_text()
    assert text == "---\nbrief: 007_some-theory\nbar: 1d\nprofile: calm\nside: long\n---\nIdea: a\nConsequence: c\n"
    assert (tmp_path / "ideas" / "INDEX.md").read_text() == "007-01_a-b-c: x [bar: 1d, profile: calm, side: long]\n"

