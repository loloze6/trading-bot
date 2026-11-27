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


def test_an_idea_may_name_one_market_profile():
    # topic 49: one of the six profiles, or none; any other text is refused
    ideas, _ = a.parse_ideas("idea: X rebounds.\nconsequence: buy.\nname: x\nfrom: F1\nprofile: falling, agitated\n", F)
    assert a.profile_name(ideas[0]["profile"]) == "falling agitated"
    ideas, _ = a.parse_ideas("idea: X rebounds.\nconsequence: buy.\nname: x\nfrom: F1\nprofile: none\n", F)
    assert a.profile_name(ideas[0]["profile"]) is None
    with pytest.raises(ValueError, match="a market profile"):
        a.parse_ideas("idea: X rebounds.\nconsequence: buy.\nname: x\nfrom: F1\nprofile: a bear market\n", F)


def test_an_idea_off_the_theme_is_a_discovery_written_for_step_1():
    # topic 50: lines 7.e and 7.g mark an idea `theme: discovery`; it is written as a source for a new brief
    ideas, _ = a.parse_ideas("idea: A week's gain carries into Saturday.\nconsequence: buy Friday.\nname: x\nfrom: F1\n"
                             "theme: discovery\n\nidea: X rebounds.\nconsequence: buy.\nname: y\nfrom: F1\ntheme: on\n", F)
    assert [a.is_discovery(g) for g in ideas] == [True, False]
    src = a.discovery_source(ideas[0], {"bar": "1d", "instruments": "BTC, ETH"}, {"id": "7.g", "name": "patterns"},
                             "031-01_x_1d", {"idea": "031-01_x", "brief": "031_y"}, "\n- F1: " + F["F1"])
    assert "The pattern: A week's gain carries into Saturday." in src and "1d bars of BTC, ETH" in src and "F1:" in src


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
        assert "{{" not in a.with_common(line.read_text().replace("{{PROFILE_MAP}}", a.profile_map())), line


def test_line_7d_runs_only_on_a_confirmed_idea_whose_book_does_not_pay():
    """Operator, 2026-11-22 (topic 45): 7.d repairs a real idea; a book whose idea is not confirmed goes to the verdict's line."""
    import yaml
    from pathlib import Path
    entry = yaml.safe_load((Path(a.__file__).resolve().parents[2] / "07d_not_profitable/helper/line.yaml").read_text())["entry"]
    assert a.entry_met(entry, "confirmed", "not profitable enough", 1)
    for s5 in ("inconclusive", "no effect", "not observable", "mismatch"):
        assert not a.entry_met(entry, s5, "not profitable enough", 1)
    assert not a.entry_met(entry, "confirmed", "profitable enough", 0)


def test_line_7d_repairs_only_a_close_book():
    """B12, operator 2026-11-27: a repair only when the book fails at most 2 of step 6's measures."""
    import yaml
    entry = yaml.safe_load((Path(a.__file__).resolve().parents[2] / "07d_not_profitable/helper/line.yaml").read_text())["entry"]
    assert a.entry_met(entry, "confirmed", "not profitable enough", 2)
    assert not a.entry_met(entry, "confirmed", "not profitable enough", 3)
    assert not a.entry_met(entry, "confirmed", "not profitable enough", None)     # no check: not close
    assert a.entry_met({"step5_in": ["inconclusive"]}, "inconclusive", "none", None)   # no cap: the count is not read


def test_failed_of_counts_the_measures_step_6_failed(tmp_path):
    import json
    (tmp_path / "x").mkdir()
    (tmp_path / "x" / "result.json").write_text(json.dumps({"status": "not profitable enough", "measures": [
        {"measure": "a", "passed": True}, {"measure": "b", "passed": False}, {"measure": "c", "passed": False}]}))
    assert a.failed_of(tmp_path, "x") == 2 and a.failed_of(tmp_path, "y") is None


def test_line_7c_reads_no_effect_and_an_old_rejected():
    """B11, operator 2026-11-27 (common/verdicts.md): 7.c runs on "no effect"; an old "rejected" is read as it."""
    import yaml
    sys.path.insert(0, str(Path(a.__file__).resolve().parents[2] / "common"))
    from lib import step5_answer
    entry = yaml.safe_load((Path(a.__file__).resolve().parents[2] / "07c_rejected/helper/line.yaml").read_text())["entry"]
    assert a.entry_met(entry, step5_answer("no effect"), "none") and a.entry_met(entry, step5_answer("rejected"), "none")
    assert not a.entry_met(entry, step5_answer("inconclusive"), "none")


def test_the_analyst_reads_how_sure_the_size_is(tmp_path):
    import json
    f = tmp_path / "size.json"; rec = tmp_path / "rec"; rec.mkdir()
    base = {"horizon_bars": 2, "cases": 10, "unusual_move": 0.004, "normal_drift": 0.001, "total_move": 0.005, "usual_move": 0.05, "strength": 0.08}
    f.write_text(json.dumps(base)); assert "how sure" not in a.size_and_cost(f, rec)
    f.write_text(json.dumps(dict(base, unusual_move_t=-1.5, case_days=9)))
    assert "+0.40 % (how sure: t -1.50, the cases of one day taken together, 9 days)" in a.size_and_cost(f, rec)


def test_explorations_see_the_exploration_folds_only(tmp_path):
    import gzip
    plan = "---\ndata-period: folds A, B, C, D\n---\n"
    rec = tmp_path / "rec"
    (rec / "BTCUSD" / "fold_A").mkdir(parents=True)
    for w in ("w1", "w7", "w18", "w19"):
        (rec / "BTCUSD" / w).mkdir()
        with gzip.open(rec / "BTCUSD" / w / "bars.csv.gz", "wt") as f:
            f.write("timestamp,close,postRebalance_total_value\n2020-01-01,1,100\n2020-01-02,2,101\n")
    only = a.exploration_windows(plan, rec)
    assert only == [f"w{i}" for i in range(7, 19)]
    code = "def explore(data):\n    import pandas as pd\n    return {'windows': pd.Series(sorted(data['bars']['BTCUSD']))}\n"
    out = a.run_explore(sys.executable, rec, code, only)
    assert "w7" in out and "w18" in out and "w1 " not in out.replace("w18", "") and "w19" not in out
    assert "w1" in a.run_explore(sys.executable, rec, code)          # without the restriction every window is seen
    summary = a.data_summary(rec, only)
    assert "w7" in summary and "w18" in summary and "w19" not in summary and "(w1," not in summary


def test_lines_e_and_g_read_the_profile_map():
    """Next steps 1q (2026-11-25): the two lines that write discoveries are given the profile map."""
    for line in ("07e_profitable_unproven", "07g_patterns"):
        t = (Path(a.STEPS) / line / "helper" / "line_prompt.md").read_text()
        assert "{{PROFILE_MAP}}" in t and "[THE PROFILE MAP]" in t
    assert "{{PROFILE_MAP}}" not in a.with_common((Path(a.STEPS) / "07g_patterns" / "helper" / "line_prompt.md").read_text().replace("{{PROFILE_MAP}}", a.profile_map()))
