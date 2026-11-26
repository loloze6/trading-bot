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
bar: 1h
---
idea: a weekend move reverses on Monday
consequence: thin weekend liquidity
short-name: weekend reversal
index-line: weekend reversal
---
idea: a move within the day
consequence: c
short-name: x y
index-line: z
bar: 15m because finer
already-indexed: none
"""


def test_an_idea_may_state_bar_1h_only():
    ideas, already = M.parse(ANSWER)
    assert [i[4] for i in ideas] == ["1h", None, None]        # no line: none; anything but 1h: dropped
    assert already == "none"


def test_an_idea_may_name_one_market_profile():
    # topic 49: one of the six profiles, written in any order or case; "none" or no line: none; anything else refused
    answer = ("idea: a sharp fall rebounds\nconsequence: c\nshort-name: a b c\nindex-line: x\nprofile: Falling, agitated\n---\n"
              "idea: a weekend move reverses\nconsequence: c\nshort-name: d e f\nindex-line: y\nprofile: none\n---\n"
              "idea: a third\nconsequence: c\nshort-name: g h i\nindex-line: z\nprofile: choppy\nalready-indexed: none\n")
    ideas, _ = M.parse(answer)
    assert [i[5] for i in ideas] == ["falling agitated", None, "choppy"]
    import pytest
    with pytest.raises(ValueError):
        M.parse("idea: a\nconsequence: c\nshort-name: a b c\nindex-line: x\nprofile: bull market\nalready-indexed: none\n")
    with pytest.raises(ValueError):
        M.parse("idea: a\nconsequence: c\nshort-name: a b c\nindex-line: x\nprofile: rising or falling\nalready-indexed: none\n")
