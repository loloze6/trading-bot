"""D-188 (direction 2026-10-24, PR-3): the Calmar bar. `calmar_min` 0.75 (strict >) = the chained
whole-test total return annualised over the COUNTED days, (1 + R)^(365 / counted_days) - 1,
over the D-129 drawdown of the same chain; a negative total return FAILs. `max_drawdown_pct_max`
stays in the file (20) but its row is ADVISORY (D-119's `advisory: true` flag): computed and
printed, never decides the verdict. `deflated_sharpe_threshold` unchanged. Applies to backtests
graded after; nothing regraded (a bars file without `calmar_min` grades exactly as before)."""
from __future__ import annotations

import math
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "tests"))
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import campaign_memory as cm  # noqa: E402,F401
import portfolio_whole_test as pw  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
import test_e062_s2b1_profit_bars_v2 as t62  # noqa: E402

D0 = date(2020, 1, 1)
CALMAR_BARS = {**t62.V2_BARS, "calmar_min": 0.75}
ROWS = ["sharpe_min", "max_drawdown_pct_max", "calmar_min", "trade_count_min",
        "avg_daily_return_min", "buy_and_hold_sharpe_excess_min", "cost_edge_ratio_min"]


def _day(i: int) -> date:
    return D0 + timedelta(days=i)


def _bars(first: int, closes: list) -> dict:
    return {datetime(*_day(first + k).timetuple()[:3], 23): v for k, v in enumerate(closes)}


def _metrics(**actuals):
    out = {n: {"actual": 1.0, "note": "", "not_evaluable_reason": None, "detail": {}} for n in ROWS}
    out["max_drawdown_pct_max"]["actual"] = 5.0
    out["sharpe_min"]["actual"] = 2.0
    out["avg_daily_return_min"]["actual"] = 0.001
    out["trade_count_min"]["actual"] = 200
    out["cost_edge_ratio_min"]["actual"] = 5.0
    out["calmar_min"]["actual"] = 2.0
    for k, v in actuals.items():
        out[k]["actual"] = v
    return out


def _fake_chain(total_return: float, days: int = 365, start_level=None) -> dict:
    """A minimal chain for _calmar_row: only daily_levels, n_counted_calendar_days, start_level."""
    chain = {"daily_levels": [(D0, 1.0), (_day(days - 1), 1.0 + total_return)],
             "n_counted_calendar_days": days}
    if start_level is not None:
        chain["start_level"] = start_level
    return chain


def _calmar(total_return: float, dd_pct: float, days: int = 365) -> dict:
    """The metrics entry _calmar_row writes for a fake chain."""
    out = {}

    def _row(name, actual=None, note="", reason=None, detail=None):
        out[name] = {"actual": None if reason else actual, "note": note or (reason or ""),
                     "not_evaluable_reason": reason, "detail": detail or {}}

    rpr._calmar_row(_row, _fake_chain(total_return, days), {"max_drawdown_pct": dd_pct},
                    "SPAN", {"first_day": "x"})
    return out["calmar_min"]


def _grade(metrics, bars=CALMAR_BARS, dsr=0.99):
    results, overall, reasons = rpr._grade_profit_bars_v2(bars, dsr=dsr, dsr_note="t",
                                                          metrics=metrics)
    return {r["name"]: r for r in results}, overall, reasons


# -- the value, by hand --------------------------------------------------------------------

def test_calmar_value_on_a_synthetic_chained_curve_by_hand():
    """One coin, 365 counted days (so the annualisation exponent is exactly 1): level 1.0, up to
    1.3, down to 1.17 (drawdown 1 - 1.17/1.3 = 10%), back to 1.3. R = 0.30, annualised 0.30,
    Calmar = 0.30 / 0.10 = 3.0."""
    closes = [1000.0] * 100 + [1300.0] * 100 + [1170.0] * 100 + [1300.0] * 65
    assert len(closes) == 365
    wins = {"w0": {"X": _bars(0, closes)}}
    bounds = {"w0": (_day(0), _day(364))}
    chain = pw.chain_windows(wins, ["X"], bounds, start_values={"w0": {"X": 1000.0}})
    assert chain["n_counted_calendar_days"] == 365
    dd = pw.whole_test_max_drawdown(chain)
    assert dd["max_drawdown_pct"] == pytest.approx(10.0, rel=1e-9)
    out = {}

    def _row(name, actual=None, note="", reason=None, detail=None):
        out[name] = {"actual": actual, "note": note, "reason": reason, "detail": detail or {}}

    rpr._calmar_row(_row, chain, dd, "SPAN", {})
    row = out["calmar_min"]
    assert row["reason"] is None
    assert row["actual"] == pytest.approx(3.0, rel=1e-9)
    d = row["detail"]
    assert d["total_return"] == pytest.approx(0.30, rel=1e-9)
    assert d["annualised_return"] == pytest.approx(0.30, rel=1e-9)
    assert d["counted_days"] == 365 and d["max_drawdown_pct"] == pytest.approx(10.0)
    assert "365" in d["formula"]
    # the same total return as the buy-and-hold comparison's strategy_total_return
    bh = pw.chained_buy_and_hold(chain, {"w0": {"X": _bars(0, closes)}}, {"X": 0.0}, {"X": 0.0})
    assert d["total_return"] == pytest.approx(bh["strategy_total_return"], rel=1e-12)


def test_annualisation_is_compound_over_the_counted_days():
    # R = 0.21 over 100 counted days: (1.21)^(365/100) - 1; drawdown 20 % -> /0.20
    row = _calmar(0.21, 20.0, days=100)
    ann = 1.21 ** 3.65 - 1.0
    assert row["detail"]["annualised_return"] == pytest.approx(ann, rel=1e-12)
    assert row["actual"] == pytest.approx(ann / 0.20, rel=1e-12)
    assert row["detail"]["counted_days"] == 100


def test_counted_days_not_the_calendar_span_across_a_planned_gap():
    """Two 100-day windows 200 days apart: the chain counts 200 days, not the 400-day span."""
    w = lambda first: _bars(first, [1000.0] * 100)  # noqa: E731
    chain = pw.chain_windows({"a": {"X": w(0)}, "b": {"X": w(300)}}, ["X"],
                             {"a": (_day(0), _day(99)), "b": (_day(300), _day(399))},
                             start_values={"a": {"X": 1000.0}, "b": {"X": 1000.0}})
    assert chain["n_calendar_days"] == 400 and chain["n_counted_calendar_days"] == 200
    out = {}
    rpr._calmar_row(lambda name, actual=None, note="", reason=None, detail=None:
                    out.update(row={"actual": actual, "reason": reason, "detail": detail or {}}),
                    chain, {"max_drawdown_pct": 5.0}, "S", {})
    assert out["row"]["detail"]["counted_days"] == 200


def test_a_curve_that_ends_below_one_with_a_positive_mean_daily_return_fails():
    """Up 50 %, down 40 % (mean daily return +5 % over 2 days) ends at 0.9: total return < 0."""
    w0 = _bars(0, [1000.0, 1500.0, 900.0])
    chain = pw.chain_windows({"w0": {"X": w0}}, ["X"], {"w0": (_day(0), _day(2))},
                             start_values={"w0": {"X": 1000.0}})
    rets = [r for _d, r in chain["daily_returns"]]
    assert sum(rets) / len(rets) > 0 and chain["daily_levels"][-1][1] < 1.0
    out = {}
    rpr._calmar_row(lambda name, actual=None, note="", reason=None, detail=None:
                    out.update(row={"actual": actual, "reason": reason, "detail": detail or {}}),
                    chain, pw.whole_test_max_drawdown(chain), "S", {})
    assert out["row"]["detail"]["total_return"] < 0 and out["row"]["actual"] < 0


# -- the comparator ------------------------------------------------------------------------

def test_strict_greater_than_at_the_boundary():
    # R = 0.375 (binary-exact), 365 days -> annualised 0.375 exactly; drawdown 50 % -> 0.75
    at = _calmar(0.375, 50.0)
    assert at["actual"] == 0.75
    rows, overall, _r = _grade(_metrics(calmar_min=at["actual"]))
    assert rows["calmar_min"]["result"] == "FAIL" and rows["calmar_min"]["comparator"] == ">"
    above = _calmar(0.376, 50.0)
    assert above["actual"] > 0.75
    rows, overall, _r = _grade(_metrics(calmar_min=above["actual"]))
    assert rows["calmar_min"]["result"] == "PASS" and overall == "PASS"


def test_negative_total_return_fails_with_that_reason():
    row = _calmar(-0.10, 15.0)
    assert row["actual"] < 0 and "negative total return" in row["note"]
    assert row["detail"]["total_return"] == pytest.approx(-0.10)
    rows, overall, reasons = _grade(_metrics(calmar_min=row["actual"]))
    assert rows["calmar_min"]["result"] == "FAIL" and overall == "FAIL"
    assert any(r.startswith("calmar_min: FAIL") for r in reasons)


def test_the_calmar_row_carries_its_record():
    row = _calmar(0.30, 10.0)
    rows, _o, _r = _grade(_metrics(calmar_min=row["actual"]))
    entry = rows["calmar_min"]
    assert entry["threshold"] == 0.75 and entry["actual"] == pytest.approx(3.0)
    assert entry["basis"] == ("portfolio_equal_weight_whole_test_chained_annualised_return_over_"
                              "drawdown")


# -- the edges -----------------------------------------------------------------------------

def test_zero_drawdown_with_a_positive_return_is_not_evaluable_no_division():
    row = _calmar(0.30, 0.0)
    assert row["actual"] is None and "no drawdown" in row["not_evaluable_reason"]
    assert row["detail"]["no_drawdown"] is True
    rows, overall, _r = _grade(_metrics(calmar_min=None))
    assert rows["calmar_min"]["result"] == "NOT_EVALUABLE" and overall == "FAIL"


@pytest.mark.parametrize("total", [0.0, -0.05])
def test_zero_drawdown_without_a_positive_return_reads_zero_and_fails(total):
    row = _calmar(total, 0.0)
    assert row["actual"] == 0.0 and row["detail"]["no_drawdown"] is True
    rows, _o, _r = _grade(_metrics(calmar_min=row["actual"]))
    assert rows["calmar_min"]["result"] == "FAIL"


def test_an_overflowing_annualisation_is_not_evaluable():
    row = _calmar(50.0, 10.0, days=2)  # 51^(182.5)
    assert row["actual"] is None and "overflows" in row["not_evaluable_reason"]


def test_start_level_is_the_first_level_when_day1_returns_are_chained():
    chain = _fake_chain(0.0, start_level=1.0)
    chain["daily_levels"] = [(D0, 1.1), (_day(364), 1.375)]  # D-116: day-1 return in the level
    out = {}
    rpr._calmar_row(lambda name, actual=None, note="", reason=None, detail=None:
                    out.update(row={"actual": actual, "detail": detail or {}}),
                    chain, {"max_drawdown_pct": 50.0}, "S", {})
    assert out["row"]["detail"]["total_return"] == pytest.approx(0.375)


# -- the drawdown is advisory --------------------------------------------------------------

def test_a_25_percent_drawdown_no_longer_fails_the_verdict_on_its_own():
    rows, overall, reasons = _grade(_metrics(max_drawdown_pct_max=25.0))
    dd = rows["max_drawdown_pct_max"]
    assert dd["result"] == "FAIL" and dd["advisory"] is True and dd["actual"] == 25.0
    assert dd["threshold"] == 20.0 and dd["comparator"] == "<="  # computed and printed as before
    assert overall == "PASS"  # the Calmar row (2.0 > 0.75) decides
    assert any("max_drawdown_pct_max: FAIL" in r and "D-188" in r for r in reasons)


def test_the_calmar_row_decides_when_the_drawdown_is_small():
    rows, overall, _r = _grade(_metrics(max_drawdown_pct_max=5.0, calmar_min=0.5))
    assert rows["max_drawdown_pct_max"]["result"] == "PASS"
    assert rows["calmar_min"]["result"] == "FAIL" and overall == "FAIL"


def test_without_calmar_min_the_drawdown_still_blocks_as_before():
    """A bars file without calmar_min (no row): grading is exactly the pre-D-188 grading."""
    m = _metrics(max_drawdown_pct_max=25.0)
    rows, overall, _r = _grade(m, bars=t62.V2_BARS)
    assert "calmar_min" not in rows
    assert rows["max_drawdown_pct_max"]["result"] == "FAIL"
    assert "advisory" not in rows["max_drawdown_pct_max"] and overall == "FAIL"


def test_row_order_calmar_follows_the_drawdown():
    results, _o, _r = rpr._grade_profit_bars_v2(CALMAR_BARS, dsr=0.99, dsr_note="t",
                                                metrics=_metrics())
    names = [r["name"] for r in results]
    assert names.index("calmar_min") == names.index("max_drawdown_pct_max") + 1


def test_the_deflated_sharpe_row_is_unchanged():
    rows, overall, _r = _grade(_metrics(), dsr=0.1)
    assert rows["deflated_sharpe_threshold"]["result"] == "FAIL"
    assert "advisory" not in rows["deflated_sharpe_threshold"] and overall == "FAIL"
    rows, overall, _r = _grade(_metrics(), dsr=None)
    assert rows["deflated_sharpe_threshold"]["advisory"] is True and overall == "PASS"
    assert CALMAR_BARS["deflated_sharpe_threshold"] == t62.V2_BARS["deflated_sharpe_threshold"]


def test_an_advisory_not_evaluable_drawdown_does_not_block_either():
    m = _metrics()
    m["max_drawdown_pct_max"].update(actual=None, not_evaluable_reason="x")
    rows, overall, _r = _grade(m)
    assert rows["max_drawdown_pct_max"]["result"] == "NOT_EVALUABLE"
    assert rows["max_drawdown_pct_max"]["advisory"] is True and overall == "PASS"


def test_the_grid_cell_and_the_memory_ignore_an_advisory_drawdown_fail(tmp_path):
    rows, overall, _r = _grade(_metrics(max_drawdown_pct_max=25.0))
    cell = vce._evaluate_profit_bars_cell(
        {"id": "pb"}, "base", lambda vid: {"result": overall, "bars": list(rows.values())})
    assert cell["result"] == "PASS"
    cell = vce._evaluate_profit_bars_cell(
        {"id": "pb"}, "base",
        lambda vid: {"result": "FAIL", "bars": list(_grade(_metrics(calmar_min=0.1))[0].values())})
    assert cell["result"] == "FAIL"


# -- partial coverage ----------------------------------------------------------------------

def test_a_held_partial_variant_cannot_pass_on_an_advisory_drawdown_alone():
    """Where the D-047 normalisation cannot be applied, calmar_min is held NOT_EVALUABLE with the
    drawdown row (the drawdown is advisory now, so it no longer holds the variant by itself)."""
    results, overall, _r = rpr._grade_profit_bars_v2(CALMAR_BARS, dsr=0.99, dsr_note="t",
                                                     metrics=_metrics())
    assert overall == "PASS"
    held, h_overall, _hr = rpr._hold_rows_not_evaluable(results, rpr._D047_HELD_BARS, "partial",
                                                        bars=CALMAR_BARS)
    by = {r["name"]: r for r in held}
    assert by["calmar_min"]["result"] == "NOT_EVALUABLE"
    assert by["max_drawdown_pct_max"]["result"] == "NOT_EVALUABLE" and h_overall == "FAIL"


def test_the_ruin_path_fails_the_calmar_row(monkeypatch, tmp_path):
    from portfolio_daily import PortfolioRuined

    def boom(run_dir, pr):
        raise PortfolioRuined("ruin", path="p.csv", timestamp="2020-01-02", equity=-5.0,
                              drawdown_pct=120.0)

    monkeypatch.setattr(rpr, "_whole_test_chain", boom)
    monkeypatch.setattr(rpr, "_v2_trade_records", lambda run_dir, pr: (None, "no records"))
    m = rpr._whole_test_profit_metrics(tmp_path, {"results": []}, CALMAR_BARS)
    assert m["calmar_min"]["actual"] == pytest.approx(-100.0 / 120.0)
    assert m["calmar_min"]["note"].startswith("RUIN: ")
    results, overall, _r = rpr._grade_profit_bars_v2(CALMAR_BARS, dsr=0.99, dsr_note="t", metrics=m)
    rows = {r["name"]: r for r in results}
    assert rows["calmar_min"]["result"] == "FAIL" and overall == "FAIL"
    assert rows["max_drawdown_pct_max"]["advisory"] is True


# -- the loader ----------------------------------------------------------------------------

def test_loader_accepts_the_committed_file_with_calmar_and_unsigned():
    real = SR_ROOT / "config" / "profitability_bars.yaml"
    for v2 in (False, True):
        doc = rpr._load_profitability_bars(real, v2=v2)
        assert doc["max_drawdown_pct_max"] == 20.0 and doc["deflated_sharpe_threshold"] == 0.5
        # the file changed after the 2026-10-14 signature: unsigned until the operator signs
        assert doc["ratified_by"] is None and doc["ratified_at"] is None
    assert rpr._load_profitability_bars(real, v2=True)["calmar_min"] == 0.75


def test_loader_calmar_min_is_optional_and_range_checked(tmp_path):
    def load(doc):
        p = tmp_path / "bars.yaml"
        p.write_text(yaml.safe_dump(doc), encoding="utf-8")
        return rpr._load_profitability_bars(p, v2=True)

    assert "calmar_min" not in load(t62.V2_BARS)          # absent = no row
    assert load({**t62.V2_BARS, "calmar_min": None})["calmar_min"] is None
    assert load({**t62.V2_BARS, "calmar_min": 0.75})["calmar_min"] == 0.75
    for bad in (0.0, -1.0, 1000.0, True, "0.75", float("nan")):
        with pytest.raises(rpr.ProfitabilityBarsSchemaError, match="calmar_min"):
            load({**t62.V2_BARS, "calmar_min": bad})


def test_legacy_path_ignores_calmar_min(tmp_path):
    p = tmp_path / "bars.yaml"
    p.write_text(yaml.safe_dump({**t62.V1_BARS, "calmar_min": -5}), encoding="utf-8")
    assert rpr._load_profitability_bars(p, v2=False)["calmar_min"] == -5  # never read, never graded


def test_an_off_calmar_bar_has_no_row_and_the_metrics_hold_none():
    assert rpr._bar_is_off(t62.V2_BARS, "calmar_min") is True
    assert rpr._bar_is_off({**t62.V2_BARS, "calmar_min": None}, "calmar_min") is True
    assert rpr._bar_is_off(CALMAR_BARS, "calmar_min") is False
    rows, _o, _r = _grade(_metrics(), bars=t62.V2_BARS)
    assert "calmar_min" not in rows


def test_math_is_finite_for_every_graded_actual():
    for total, dd in ((0.3, 10.0), (-0.2, 30.0), (0.0, 5.0)):
        a = _calmar(total, dd)["actual"]
        assert a is not None and math.isfinite(a)
