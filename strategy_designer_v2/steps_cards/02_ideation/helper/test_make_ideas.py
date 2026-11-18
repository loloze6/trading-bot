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
