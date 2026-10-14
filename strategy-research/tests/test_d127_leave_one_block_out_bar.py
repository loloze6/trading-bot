"""E-078 item 2 (D-127): the branch-3 leave-one-block-out bar,
`leave_one_block_out_sharpe_min` in config/profitability_bars.yaml (v2): the lowest
whole-test Sharpe with one 4-month block left out must be > the threshold (0: FAIL if any
leave-one-out Sharpe <= 0). A block is the 4-month calendar slice a day falls in (a fold's
window is one slice). One definition, portfolio_whole_test.leave_one_block_out_sharpes,
shared with the E-078 read-only pass. Optional key: absent or null = no row.
"""
from __future__ import annotations

import math
import statistics
import sys
from datetime import date
from pathlib import Path

import pytest

SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR / "tests"))
sys.path.insert(0, str(SR / "workflow"))
sys.path.insert(0, str(SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import portfolio_whole_test as pwt  # noqa: E402
import test_e062_s2b1_profit_bars_v2 as t62  # noqa: E402

# three windows in three different 4-month slices (2020-01, 2020-05, 2020-09)
WINS = (("a", date(2020, 1, 1), date(2020, 2, 1)), ("b", date(2020, 5, 1), date(2020, 6, 1)),
        ("c", date(2020, 9, 1), date(2020, 10, 1)))
WITH = {**t62.V2_BARS, "leave_one_block_out_sharpe_min": 0.0}


def _strat(gains):
    return lambda label, k: gains[label] + 0.002 * (-1) ** k


def _run(tmp_path, bars, gains=None, windows=WINS, name="r"):
    run_dir = tmp_path / name
    pr = t62._build(run_dir, windows=windows,
                    strat=_strat(gains or {"a": 0.003, "b": 0.002, "c": 0.001}))
    return pr, run_dir, t62._rows(pr, run_dir, bars=bars)


def _manual_sharpe(rets):
    return statistics.mean(rets) / statistics.stdev(rets) * math.sqrt(365)


@pytest.mark.parametrize("day, label", [(date(2020, 1, 1), "2020-01"), (date(2020, 4, 30), "2020-01"),
                                        (date(2020, 5, 1), "2020-05"), (date(2020, 8, 31), "2020-05"),
                                        (date(2020, 9, 1), "2020-09"), (date(2020, 12, 31), "2020-09")])
def test_a_block_is_the_4_month_calendar_slice(day, label):
    assert pwt.loo_block_label(day) == label


def test_absent_or_null_key_has_no_row_and_grades_exactly_as_before(tmp_path):
    base = _run(tmp_path, t62.V2_BARS, name="a")[2]
    null = _run(tmp_path, {**t62.V2_BARS, "leave_one_block_out_sharpe_min": None}, name="b")[2]
    assert "leave_one_block_out_sharpe_min" not in base[0]
    assert "leave_one_block_out_sharpe_min" not in null[0]
    strip = lambda rs: [{k: v for k, v in r.items() if k not in ("note", "detail")} for r in rs]  # noqa: E731
    assert strip(base[3]) == strip(null[3]) and base[1] == null[1]


def test_the_value_is_the_lowest_whole_test_sharpe_leaving_one_window_out(tmp_path):
    pr, run_dir, (rows, overall, _r, results) = _run(tmp_path, WITH)
    chain, _coins = rpr._whole_test_chain(run_dir, pr)
    bounds = rpr._v2_protocol_window_bounds(pr, rpr._pd.load_windows(run_dir, pr)[0])
    expected = {}
    for w, (a, b) in bounds.items():   # the window bounds, independently of the slice label
        a, b = (date.fromisoformat(str(x)[:10]) for x in (a, b))
        expected[w] = _manual_sharpe([r for d, r in chain["daily_returns"] if not a <= d <= b])
    row = rows["leave_one_block_out_sharpe_min"]
    assert row["actual"] == pytest.approx(min(expected.values()), rel=1e-9)
    assert sorted(row["detail"]["by_block"].values()) == pytest.approx(sorted(expected.values()))
    assert row["basis"] == "min_whole_test_sharpe_leaving_one_4_month_block_out"
    assert row["comparator"] == ">" and row["result"] == "PASS"
    assert results[-1]["name"] == "leave_one_block_out_sharpe_min"


def test_one_block_carrying_the_run_fails(tmp_path):
    """Window a gains, b and c lose: without a, the Sharpe is <= 0 -> FAIL."""
    _pr, _rd, (rows, overall, reasons, _) = _run(
        tmp_path, WITH, gains={"a": 0.02, "b": -0.004, "c": -0.004})
    row = rows["leave_one_block_out_sharpe_min"]
    assert row["actual"] <= 0 and row["detail"]["worst_block"] == "2020-01"
    assert row["result"] == "FAIL" and overall == "FAIL"


@pytest.mark.parametrize("offset, result", [(0.0, "FAIL"), (-1e-9, "PASS")])
def test_the_comparison_is_strict(tmp_path, offset, result):
    pr, run_dir, (rows, *_rest) = _run(tmp_path, WITH, name="a")
    actual = rows["leave_one_block_out_sharpe_min"]["actual"]
    bars = {**t62.V2_BARS, "leave_one_block_out_sharpe_min": actual + offset}
    got = t62._rows(pr, run_dir, bars=bars)[0]["leave_one_block_out_sharpe_min"]
    assert got["result"] == result


def test_a_single_block_reads_not_evaluable(tmp_path):
    """The default windows W1/W2 both fall in 2020-01: nothing would be left."""
    pr = t62._build(tmp_path / "r")
    row = t62._rows(pr, tmp_path / "r", bars=WITH)[0]["leave_one_block_out_sharpe_min"]
    assert row["result"] == "NOT_EVALUABLE" and "1 block(s)" in row["not_evaluable_reason"]


def test_a_chain_that_cannot_be_built_reads_not_evaluable(tmp_path):
    pr = t62._build(tmp_path / "r", windows=WINS, protocol=False)
    metrics = t62._metrics(pr, tmp_path / "r", bars=WITH)
    row = metrics["leave_one_block_out_sharpe_min"]
    assert row["actual"] is None and row["not_evaluable_reason"]


def test_the_epic_script_reads_the_same_function():
    src = (SR / "engineering" / "roadmap" / "E-078" / "leave_one_out_and_bh.py").read_text(
        encoding="utf-8")
    assert "pwt.leave_one_block_out_sharpes(returns)" in src


@pytest.mark.parametrize("value, ok", [(0.0, True), (-1.0, True), (None, True), (0.5, True),
                                       (True, False), ("0", False), (float("nan"), False),
                                       (99.0, False)])
def test_the_loader_checks_the_key_only_when_present(value, ok):
    t62._write_bars({**t62.V2_BARS, "leave_one_block_out_sharpe_min": value})
    if ok:
        assert rpr._load_profitability_bars(v2=True)["leave_one_block_out_sharpe_min"] == value
    else:
        with pytest.raises(rpr.ProfitabilityBarsSchemaError, match="leave_one_block_out"):
            rpr._load_profitability_bars(v2=True)
