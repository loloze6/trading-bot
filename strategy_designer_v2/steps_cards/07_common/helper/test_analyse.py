"""Tests of step 7's code checks: entry conditions, dates, findings and ideas, the same-idea-on block, shared files."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyse as a  # noqa: E402

F = {"F1": "a finding", "F2": "another"}


def test_entry_conditions_of_the_lines():
    assert a.entry_met({"step5_in": ["inconclusive"]}, "inconclusive", "not profitable enough")
    assert not a.entry_met({"step5_in": ["inconclusive"]}, "confirmed", "profitable enough")
    e = {"step6_in": ["profitable enough"], "step5_not_in": ["confirmed"]}
    assert a.entry_met(e, "inconclusive", "profitable enough") and not a.entry_met(e, "confirmed", "profitable enough")
    assert a.entry_met({}, "rejected", "not profitable enough")


def test_no_period_by_month_and_year():
    a.no_dates("in w12 and in 2022 the book fell")
    for bad in ("in March 2022", "2022-03", "Q1 2022"):
        with pytest.raises(ValueError):
            a.no_dates(bad)


def test_an_idea_rests_on_existing_findings():
    ideas, none = a.parse_ideas("idea: X rises.\nconsequence: buy.\nname: x rises\nfrom: F1\n", F)
    assert ideas[0]["refs"] == ["F1"] and none is None
    with pytest.raises(ValueError, match="do not exist"):
        a.parse_ideas("idea: X rises.\nconsequence: buy.\nfrom: F9\n", F)
    ideas, none = a.parse_ideas("no-ideas: the effect is not there\n", F)
    assert ideas == [] and none == "the effect is not there"


def test_same_idea_on_checks_the_data():
    ok = "same-idea-on: instruments: BTC, ETH, ADA; bar: 1d; period: folds A, B, C, D\nname: more coins\nfrom: F1\n"
    ideas, _ = a.parse_ideas(ok, F)
    assert ideas[0]["same-idea-on"].startswith("instruments: BTC")
    for bad in ("instruments: BTC, BNB; period: folds A, D", "instruments: BTC (others missing); period: folds A",
                "instruments: BTC, ETH; period: all four folds"):
        with pytest.raises(ValueError, match="not available"):
            a.parse_ideas(f"same-idea-on: {bad}\nfrom: F1\n", F)
    with pytest.raises(ValueError):
        a.parse_ideas("same-idea-on: instruments: BTC; period: folds A\n", F)


def test_shared_files_are_pasted_where_a_prompt_names_them():
    out = a.with_common("before\n{{DATA_AVAILABLE}}\nafter")
    assert "{{" not in out and "BTC, ETH, LTC" in out
    for line in sorted(Path(a.STEPS).glob("07?_*/helper/line_prompt.md")):
        assert "{{" not in a.with_common(line.read_text()), line


def test_line_7d_runs_only_on_a_confirmed_idea_whose_book_does_not_pay():
    """Operator, 2026-11-22 (topic 45): 7.d repairs a real idea; a book whose idea is not confirmed goes to the verdict's line."""
    import yaml
    from pathlib import Path
    entry = yaml.safe_load((Path(a.__file__).resolve().parents[2] / "07d_not_profitable/helper/line.yaml").read_text())["entry"]
    assert a.entry_met(entry, "confirmed", "not profitable enough")
    for s5 in ("inconclusive", "rejected", "not observable", "mismatch"):
        assert not a.entry_met(entry, s5, "not profitable enough")
    assert not a.entry_met(entry, "confirmed", "profitable enough")
