"""Tests of the shared helpers (common/lib.py): the header readers, the idea fields step 3 reads, atomic writes."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import common_text, header, header_fields, idea_fields, write_atomic  # noqa: E402

STEP7_IDEA = """---
brief: 002_some-brief
source-idea: 002-03_some-idea
line: 7.d not profitable
backtest: 002-03_some-idea_1d
instruments: BTC, ETH
bar: 1d
period: folds A, D
---
Idea: While a coin's close is above its N-day average, the further above, the larger its rise over the next N days.
Consequence: Take longs further above the average.
Why:
- F1: a number measured on the data, t 3.1.
"""


def test_header_and_fields():
    lines, body = header(STEP7_IDEA)
    assert lines[0] == "brief: 002_some-brief" and body.startswith("Idea:")
    assert header_fields(STEP7_IDEA)["period"] == "folds A, D"
    assert header_fields("no header") == {}
    with pytest.raises(SystemExit):
        header("no header")


def test_idea_fields_keep_only_what_step3_reads():
    out = idea_fields(STEP7_IDEA)
    assert "Why" not in out and "t 3.1" not in out and "source-idea" not in out and "backtest" not in out
    assert out.splitlines() == ["---", "brief: 002_some-brief", "instruments: BTC, ETH", "bar: 1d",
                                "period: folds A, D", "---",
                                "Idea: While a coin's close is above its N-day average, the further above, the larger its rise over the next N days.",
                                "Consequence: Take longs further above the average."]
    with pytest.raises(SystemExit):
        idea_fields("---\nbrief: x\n---\nIdea: no consequence line\n")


def test_write_atomic_and_common_text(tmp_path):
    p = tmp_path / "f.md"
    write_atomic(p, "one")
    write_atomic(p, "two")
    assert p.read_text() == "two" and not (tmp_path / "f.md.tmp").exists()
    assert "Every idea" in common_text("idea_definition")


def test_the_line_a_model_call_prints():
    import lib
    d = {"usage": {"input_tokens": 5, "cache_read_input_tokens": 600, "cache_creation_input_tokens": 4000,
                   "output_tokens": 9000, "output_tokens_details": {"thinking_tokens": 7000}},
         "total_cost_usd": 0.41234, "stop_reason": "end_turn"}
    line = lib.call_line(d, 63.04)
    assert line == ("model call: 63.0 s; tokens: input 5, cache read 600, cache write 4000, output 9000 (thinking 7000); "
                    "0.4123 USD; stop: end_turn")
    assert "cost" not in line.split(";")[2]          # run_idea's "cost: X USD" pattern must not count it twice
