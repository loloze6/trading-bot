"""PR-B (analyst tools, 2026-10-19): window_economics, trade_gross_return / trade_cost_pct and the
derived bar columns abs_forecast, allocation_abs, forecast_sign_change.

  1. tools/window_economics.py on hand-computed fixtures: every field of a window, of `total`,
     direction changes with zeros, NOT_READY rows out, empty trades, gross 0, the refusals;
     the figures READ from the core block / metrics.json are used verbatim (lots perturbed:
     unchanged) and are None, never recomputed, where the run did not record them.
  2. The query: zero comparisons, the 12-cell cap, the logged refusal, the digest; the engine's
     object is the stored object (run_phase1_research._variant_window_economics).
  3. trade_slice: trade_gross_return counts as a comparison, trade_cost_pct does not;
     trade_gross_return is the TradeWindow's, on the window's return basis (PR-C S1: the claim
     outcome's per-lot numbers; trades.json's profit_loss_percent / 100 on the fallback basis),
     trade_cost_pct is trades.json's; a lot-count mismatch is refused.
  4. The derived columns: forecast_sign_change with zeros, NaN at the first bar and after a
     missing t-1 stamp, no future bar read; list_columns lists them; grouped describe charges.
  5. profit_bars_evaluation.yaml: flag off -> no key and byte-identical; flag on -> the key
     after forecast_shape, None where the variant or its files are missing.
  6. The tool is registered (schemas, help, the SDK tool list).

Synthetic data only (2020 dates, hand-made numbers): no run copy, no market data, no model call.
"""
import copy
import hashlib
import json
import math
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "fixtures" / "profit_bars_golden"))

import analyst_queries as aq  # noqa: E402
import analyst_session as asm  # noqa: E402
import claim_card as cc  # noqa: E402
import window_economics as we  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
import test_e075_pr4_queries as pr4  # noqa: E402
import test_profit_bars_every_backtest as tpb  # noqa: E402
from test_e075_pr4_queries import HOLDS, N, engine, log_of, make_run  # noqa: E402

CELL_KEYS = set(we.CELL_KEYS)
BARS_HDR = "timestamp,regime,total_portfolio_value,previous_allocation,postRebalance_current_allocation"


# ---------------------------------------------------------------------------
# fixtures: two hand-made windows
# ---------------------------------------------------------------------------

def write_window(folder: Path, rows, trades, turnover=None):
    """rows: (regime, total_portfolio_value, previous_allocation, postRebalance_current_allocation),
    one per hourly bar from 2020-01-01 00:00; trades: list of trade dicts (or None: no file);
    turnover: written as metrics.json bar_equity.turnover (None: no metrics.json)."""
    folder.mkdir(parents=True, exist_ok=True)
    lines = [BARS_HDR]
    for i, (regime, tpv, prev, post) in enumerate(rows):
        lines.append(f"2020-01-01 {i:02d}:00:00,{regime},{tpv},{prev},{post}")
    (folder / "bars.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if trades is not None:
        (folder / "trades.json").write_text(json.dumps(trades), encoding="utf-8")
    if turnover is not None:
        (folder / "metrics.json").write_text(
            json.dumps({"core": {}, "bar_equity": {"turnover": turnover}}), encoding="utf-8")


def lot(gross, fees, net, minutes):
    return {"profit_loss_absolute": gross, "total_commission": fees,
            "net_profit_loss_absolute": net, "duration_minutes": minutes}


def core_of(trade_count, gross, fees, net, cost_drag, avg_dur):
    """A protocol_result `core` block: only the keys window_economics reads (dollars, bars)."""
    return {"trade_count": trade_count, "gross_pnl": gross, "fees_paid": fees, "net_pnl": net,
            "cost_drag_pct": cost_drag, "avg_trade_duration_bars": avg_dur}


# W1: V0 = 1000 (the first row, a NOT_READY one). Ready rows 1..7:
#   post 0.5 0.5 0 -0.4 0 0.3 0.3   prev 0 0.5 0.5 0 -0.4 0 0.3
#   turnover .5+0+.5+.4+.4+.3+0 = 2.1 ; signs + + (0) - (0) + + -> 2 flips
#   mean |a| = 2.0 / 7 ; max .5 ; lots 30/-10/20 gross, 1/.5/1.5 fees, 29/-10.5/18.5 net
#   -> gross 4.0, fees 0.3, net 3.7 (% of 1000) ; holding 2, 1, 5 bars (hourly) -> median 2
W1_ROWS = [("NOT_READY", 1000, 0, 0), ("trend", 1000, 0.0, 0.5), ("trend", 1010, 0.5, 0.5),
           ("trend", 1020, 0.5, 0.0), ("trend", 1020, 0.0, -0.4), ("trend", 1030, -0.4, 0.0),
           ("trend", 1030, 0.0, 0.3), ("trend", 1040, 0.3, 0.3)]
W1_TRADES = [lot(30.0, 1.0, 29.0, 120.0), lot(-10.0, 0.5, -10.5, 60.0), lot(20.0, 1.5, 18.5, 300.0)]
#   the run's own core block (hand-typed as the run would write it, NOT summed from the lots here):
#   trade_count 3, gross $40, fees $3, net $37, cost drag 7.5 %, mean duration 8/3 = 2.67 bars;
#   metrics.json bar_equity.turnover 2.1
W1_CORE = core_of(3, 40.0, 3.0, 37.0, 7.5, 2.67)
W1_TURNOVER = 2.1
# W2: V0 = 2000. Ready rows 0..3 (a padded lower-case not_ready row 4 with |alloc| 0.9 is out):
#   post -.2 -.2 0 .4   prev 0 -.2 -.2 0 -> turnover .2+0+.2+.4 = .8 ; signs - - (0) + -> 1 flip
#   mean |a| = .8/4 = .2 ; max .4 ; lots 40+... gross -20+60 = 40 -> 2.0, fees 2+4 -> .3, net 34 -> 1.7
#   holding 1, 3 bars
W2_ROWS = [("trend", 2000, 0.0, -0.2), ("trend", 2000, -0.2, -0.2), ("trend", 2010, -0.2, 0.0),
           ("trend", 2010, 0.0, 0.4), (" not_ready ", 2020, 0.9, 0.9)]
W2_TRADES = [lot(-20.0, 2.0, -22.0, 60.0), lot(60.0, 4.0, 56.0, 180.0)]
#   core: trade_count 2, gross $40, fees $6, net $34, cost drag 15 %, mean duration 2.0 bars;
#   bar_equity.turnover 0.8
W2_CORE = core_of(2, 40.0, 6.0, 34.0, 15.0, 2.0)
W2_TURNOVER = 0.8


@pytest.fixture()
def wins(tmp_path):
    write_window(tmp_path / "a", W1_ROWS, W1_TRADES, W1_TURNOVER)
    write_window(tmp_path / "b", W2_ROWS, W2_TRADES, W2_TURNOVER)
    return [("AAA", "w0", tmp_path / "a", W1_CORE), ("BBB", "w1", tmp_path / "b", W2_CORE)]


def approx(v):
    return pytest.approx(v, rel=1e-6, abs=1e-9)


# ---------------------------------------------------------------------------
# 1. tools/window_economics.py
# ---------------------------------------------------------------------------

def test_every_field_of_each_cell_and_of_the_total_is_the_hand_number(wins):
    out = we.window_economics(wins)
    assert list(out["windows"]) == ["AAA/w0", "BBB/w1"]
    a, b, tot = out["windows"]["AAA/w0"], out["windows"]["BBB/w1"], out["total"]
    assert set(a) == set(b) == set(tot) == CELL_KEYS
    # D-168 derived fields: fees_pct x 365 / n_bars, gross_pct / trades, fees_pct / trades,
    # turnover x 365 / n_bars (W1: 0.3 x 365 / 7, 4.0 / 3, 0.3 / 3, 2.1 x 365 / 7)
    assert a == {"n_bars": 7, "trades": 3, "turnover": approx(2.1), "direction_changes": 2,
                 "mean_abs_allocation": approx(2.0 / 7), "max_abs_allocation": 0.5,
                 "gross_pct": approx(4.0), "fees_pct": approx(0.3), "net_pct": approx(3.7),
                 "cost_drag_pct": approx(7.5), "avg_trade_duration_bars": approx(2.67),
                 "median_holding_bars": 2.0,
                 "fees_pct_annualised": approx(0.3 * 365 / 7), "gross_per_lot_pct": approx(4.0 / 3),
                 "fees_per_lot_pct": approx(0.1), "turnover_annualised": approx(2.1 * 365 / 7),
                 "cost_drag_note": None}
    assert b == {"n_bars": 4, "trades": 2, "turnover": approx(0.8), "direction_changes": 1,
                 "mean_abs_allocation": approx(0.2), "max_abs_allocation": 0.4,
                 "gross_pct": approx(2.0), "fees_pct": approx(0.3), "net_pct": approx(1.7),
                 "cost_drag_pct": approx(15.0), "avg_trade_duration_bars": approx(2.0),
                 "median_holding_bars": 2.0,
                 "fees_pct_annualised": approx(0.3 * 365 / 4), "gross_per_lot_pct": approx(1.0),
                 "fees_per_lot_pct": approx(0.15), "turnover_annualised": approx(0.8 * 365 / 4),
                 "cost_drag_note": None}
    # total: counts, turnover and the *_pct summed (each window its own account), bars pooled,
    # cost drag from the SUMMED READ DOLLARS ((80 - 71) / 80 = 11.25, not the 10.0 of the
    # summed percents: the two windows have different starting accounts), the average duration
    # weighted by trade count ((3 * 2.67 + 2 * 2.0) / 5), holding over the 5 lots pooled
    # (2,1,5,1,3 -> 2)
    assert tot == {"n_bars": 11, "trades": 5, "turnover": approx(2.9), "direction_changes": 3,
                   "mean_abs_allocation": approx(2.8 / 11), "max_abs_allocation": 0.5,
                   "gross_pct": approx(6.0), "fees_pct": approx(0.6), "net_pct": approx(5.4),
                   "cost_drag_pct": approx(11.25), "avg_trade_duration_bars": approx(2.402),
                   "median_holding_bars": 2.0,
                   # total: summed percents / trades / turnover over the pooled 11 bars
                   "fees_pct_annualised": approx(0.6 * 365 / 11),
                   "gross_per_lot_pct": approx(6.0 / 5), "fees_per_lot_pct": approx(0.6 / 5),
                   "turnover_annualised": approx(2.9 * 365 / 11), "cost_drag_note": None}


#: D-168: the twelve fields that existed before, as the pre-change code returned them for the
#: two fixture windows (8-significant-digit floats, exact: no approx), in their original order
LEGACY_KEYS = ["n_bars", "trades", "turnover", "direction_changes", "mean_abs_allocation",
               "max_abs_allocation", "gross_pct", "fees_pct", "net_pct", "cost_drag_pct",
               "avg_trade_duration_bars", "median_holding_bars"]
LEGACY_GOLDEN = {
    "AAA/w0": [7, 3, 2.1, 2, 0.28571429, 0.5, 4.0, 0.3, 3.7, 7.5, 2.67, 2.0],
    "BBB/w1": [4, 2, 0.8, 1, 0.2, 0.4, 2.0, 0.3, 1.7, 15.0, 2.0, 2.0],
    "total": [11, 5, 2.9, 3, 0.25454545, 0.5, 6.0, 0.6, 5.4, 11.25, 2.402, 2.0],
}


def test_every_pre_existing_field_is_byte_identical_and_keeps_its_place(wins):
    out = we.window_economics(wins)
    cells = {**out["windows"], "total": out["total"]}
    for label, golden in LEGACY_GOLDEN.items():
        cell = cells[label]
        assert list(cell)[:len(LEGACY_KEYS)] == LEGACY_KEYS, label      # same keys, same order
        assert json.dumps([cell[k] for k in LEGACY_KEYS]) == json.dumps(golden), label
        # the new keys come after, in their own order
        assert list(cell)[len(LEGACY_KEYS):] == [
            "fees_pct_annualised", "gross_per_lot_pct", "fees_per_lot_pct",
            "turnover_annualised", "cost_drag_note"], label


# gross near zero: W2's bars with V0 = 2000, gross $2 (0.1 %), fees $6 (0.3 %): 0.1 < 5 x 0.3
NEAR_ZERO_CORE = core_of(2, 2.0, 6.0, -4.0, 300.0, 2.0)


def test_cost_drag_is_withheld_with_the_note_when_gross_is_near_zero(tmp_path):
    write_window(tmp_path / "n", W2_ROWS, W2_TRADES, W2_TURNOVER)
    c = we.window_economics([("X", "w", tmp_path / "n", NEAR_ZERO_CORE)])
    cell, tot = c["windows"]["X/w"], c["total"]
    for x in (cell, tot):
        assert x["cost_drag_pct"] is None
        assert x["cost_drag_note"] == "gross near zero: a signal finding, not a cost finding"
    # the other fields are what they are with the run's cost drag of 300 % in the core
    assert cell["gross_pct"] == approx(0.1) and cell["fees_pct"] == approx(0.3)
    assert cell["net_pct"] == approx(-0.2) and cell["trades"] == 2
    assert cell["fees_pct_annualised"] == approx(0.3 * 365 / 4)
    assert cell["gross_per_lot_pct"] == approx(0.05) and cell["fees_per_lot_pct"] == approx(0.15)
    assert cell["turnover_annualised"] == approx(0.8 * 365 / 4)


def test_cost_drag_is_reported_at_five_times_fees_and_above_negative_gross_too(tmp_path):
    write_window(tmp_path / "n", W2_ROWS, W2_TRADES, W2_TURNOVER)
    # V0 2000: fees $4 -> 0.2 %, gross $20 -> 1.0 % = 5 x 0.2 %: the boundary is reported
    at = core_of(2, 20.0, 4.0, 16.0, 20.0, 2.0)
    c = we.window_economics([("X", "w", tmp_path / "n", at)])["windows"]["X/w"]
    assert c["cost_drag_pct"] == 20.0 and c["cost_drag_note"] is None
    # just under: $19.9 -> 0.995 % < 1.0 %
    under = core_of(2, 19.9, 4.0, 15.9, 20.1, 2.0)
    c = we.window_economics([("X", "w", tmp_path / "n", under)])["windows"]["X/w"]
    assert c["cost_drag_pct"] is None and c["cost_drag_note"] is not None
    # the test is on the absolute gross: a large loss with small fees is a cost reading
    loss = core_of(2, -40.0, 4.0, -44.0, 10.0, 2.0)
    c = we.window_economics([("X", "w", tmp_path / "n", loss)])["windows"]["X/w"]
    assert c["cost_drag_pct"] == 10.0 and c["cost_drag_note"] is None


def test_the_null_rule_leaves_cells_without_a_gross_or_fees_figure_as_the_run_recorded(tmp_path):
    write_window(tmp_path / "n", W2_ROWS, W2_TRADES)             # no metrics.json
    c = we.window_economics([("X", "w", tmp_path / "n", None)])["windows"]["X/w"]
    assert c["cost_drag_pct"] is None and c["cost_drag_note"] is None
    assert c["fees_pct_annualised"] is None and c["gross_per_lot_pct"] is None
    assert c["fees_per_lot_pct"] is None and c["turnover_annualised"] is None
    part = {k: v for k, v in W2_CORE.items() if k != "fees_paid"}
    c = we.window_economics([("X", "w", tmp_path / "n", part)])["windows"]["X/w"]
    assert c["cost_drag_pct"] == 15.0 and c["cost_drag_note"] is None


def test_a_window_without_lots_has_no_per_lot_figures_and_a_zero_gross_zero_fees_cell_reports(tmp_path):
    write_window(tmp_path / "e", W2_ROWS, [], W2_TURNOVER)
    core = core_of(0, 0.0, 0.0, 0.0, None, None)
    c = we.window_economics([("X", "w", tmp_path / "e", core)])["windows"]["X/w"]
    assert c["gross_per_lot_pct"] is None and c["fees_per_lot_pct"] is None
    assert c["fees_pct_annualised"] == 0.0 and c["turnover_annualised"] == approx(0.8 * 365 / 4)
    assert c["cost_drag_pct"] is None and c["cost_drag_note"] is None     # 0 >= 0: not withheld


def test_the_total_is_gated_on_its_own_summed_percents(wins, tmp_path):
    """One window carries a real cost reading, the other a near-zero gross: each cell is gated
    on its own figures, the total on the summed percents (4.0 + 0.1 = 4.1 against 5 x 0.6 =
    3.0: reported, from the summed dollars (42 - 33) / 42). Two near-zero windows give a
    withheld total (0.2 against 5 x 0.6)."""
    write_window(tmp_path / "n", W2_ROWS, W2_TRADES, W2_TURNOVER)
    out = we.window_economics([wins[0], ("X", "w", tmp_path / "n", NEAR_ZERO_CORE)])
    assert out["windows"]["AAA/w0"]["cost_drag_pct"] == approx(7.5)
    assert out["windows"]["X/w"]["cost_drag_pct"] is None
    assert out["total"]["gross_pct"] == approx(4.1) and out["total"]["fees_pct"] == approx(0.6)
    assert out["total"]["cost_drag_pct"] == approx(9.0 / 42.0 * 100)
    assert out["total"]["cost_drag_note"] is None
    out2 = we.window_economics([("X", "w", tmp_path / "n", NEAR_ZERO_CORE),
                                ("Y", "w", tmp_path / "n", NEAR_ZERO_CORE)])
    assert out2["total"]["gross_pct"] == approx(0.2) and out2["total"]["fees_pct"] == approx(0.6)
    assert out2["total"]["cost_drag_pct"] is None and out2["total"]["cost_drag_note"]


def test_the_read_figures_are_the_core_dollars_converted_by_the_starting_account(wins):
    """gross / fees / net are core.gross_pnl / fees_paid / net_pnl, as a percent of V0 (the
    first bars.csv row's total_portfolio_value: 1000 and 2000) and nothing else."""
    cells = we.window_economics(wins)["windows"]
    for (sym, win, _f, core), v0 in zip(wins, (1000.0, 2000.0)):
        c = cells[f"{sym}/{win}"]
        assert c["gross_pct"] == approx(100 * core["gross_pnl"] / v0)
        assert c["fees_pct"] == approx(100 * core["fees_paid"] / v0)
        assert c["net_pct"] == approx(100 * core["net_pnl"] / v0)
        assert c["trades"] == core["trade_count"]
        assert c["cost_drag_pct"] == core["cost_drag_pct"]
        assert c["avg_trade_duration_bars"] == core["avg_trade_duration_bars"]
        assert c["net_pct"] == approx(c["gross_pct"] - c["fees_pct"])


def test_the_read_figures_are_used_verbatim_not_summed_from_the_lots(wins, tmp_path):
    """Perturb every lot of trades.json (dollars, commissions, count): gross / fees / net, the
    trade count, cost drag and the average duration do not move, because they are not summed
    from the lots. Only median_holding_bars (computed from the lots' durations) responds."""
    base = we.window_economics(wins)
    for _s, _w, folder, _c in wins:
        p = folder / "trades.json"
        lots = json.loads(p.read_text(encoding="utf-8"))
        for t in lots:
            t.update(profit_loss_absolute=t["profit_loss_absolute"] * 7 + 123.0,
                     total_commission=t["total_commission"] * 11 + 5.0,
                     net_profit_loss_absolute=-999.0, duration_minutes=60.0 * 17)
        p.write_text(json.dumps(lots + [lots[0]]), encoding="utf-8")        # and one lot more
    moved = we.window_economics(wins)
    read_keys = ("trades", "turnover", "gross_pct", "fees_pct", "net_pct", "cost_drag_pct",
                 "avg_trade_duration_bars")
    for label in list(base["windows"]) + ["total"]:
        b = base["total"] if label == "total" else base["windows"][label]
        m = moved["total"] if label == "total" else moved["windows"][label]
        assert {k: m[k] for k in read_keys} == {k: b[k] for k in read_keys}, label
        assert m["median_holding_bars"] == 17.0 != b["median_holding_bars"], label
    # an inconsistent core is not "fixed" by the dollars of the lots or by its own identities:
    # cost_drag_pct is the run's, whatever (gross - net) / |gross| would give
    odd = [(s, w, f, dict(c, cost_drag_pct=99.0)) for s, w, f, c in wins]
    assert we.window_economics(odd)["windows"]["AAA/w0"]["cost_drag_pct"] == 99.0


def test_turnover_is_metrics_json_bar_equity_verbatim_not_recomputed(wins):
    # the bars of W1 give 2.1 if recomputed; the run's recorded value is what is read
    (wins[0][2] / "metrics.json").write_text(
        json.dumps({"bar_equity": {"turnover": 9.99}}), encoding="utf-8")
    cells = we.window_economics(wins)
    assert cells["windows"]["AAA/w0"]["turnover"] == 9.99
    assert cells["total"]["turnover"] == approx(9.99 + 0.8)


def test_figures_the_run_did_not_record_are_none_and_never_recomputed(tmp_path):
    """No core block (an older run) and no metrics.json: every read figure is None, the
    computed ones are still there; the total is None for a sum with a missing term."""
    write_window(tmp_path / "old", W1_ROWS, W1_TRADES)                # no metrics.json
    write_window(tmp_path / "new", W2_ROWS, W2_TRADES, W2_TURNOVER)
    out = we.window_economics([("OLD", "w", tmp_path / "old", None),
                               ("NEW", "w", tmp_path / "new", W2_CORE)])
    old, new, tot = out["windows"]["OLD/w"], out["windows"]["NEW/w"], out["total"]
    for k in ("trades", "turnover", "gross_pct", "fees_pct", "net_pct", "cost_drag_pct",
              "avg_trade_duration_bars"):
        assert old[k] is None, k
        assert tot[k] is None, k
    assert old["n_bars"] == 7 and old["direction_changes"] == 2 and old["median_holding_bars"] == 2.0
    assert new["gross_pct"] == approx(2.0) and new["turnover"] == approx(0.8)
    assert tot["n_bars"] == 11 and tot["direction_changes"] == 3
    # a core block that lacks one key (and a non-mapping core) is None for that key only
    part = {k: v for k, v in W2_CORE.items() if k != "fees_paid"}
    c = we.window_economics([("P", "w", tmp_path / "new", part)])["windows"]["P/w"]
    assert c["fees_pct"] is None and c["gross_pct"] == approx(2.0)
    assert we.window_economics([("P", "w", tmp_path / "new", "junk")])["windows"]["P/w"][
        "gross_pct"] is None


@pytest.mark.parametrize("key", ["gross_pnl", "fees_paid", "net_pnl", "trade_count",
                                 "cost_drag_pct", "avg_trade_duration_bars"])
@pytest.mark.parametrize("bad", ["x", True, float("nan")])
def test_a_present_but_non_numeric_core_figure_raises(tmp_path, key, bad):
    write_window(tmp_path / "w", W2_ROWS, W2_TRADES, W2_TURNOVER)
    with pytest.raises(ValueError, match=f"{key} is not a finite number"):
        we.window_economics([("X", "w", tmp_path / "w", dict(W2_CORE, **{key: bad}))])


def test_result_cores_are_keyed_by_run_id():
    pr = {"results": [{"run_id": "a", "core": {"gross_pnl": 1.0}}, {"core": {"gross_pnl": 2.0}},
                      {"run_id": "b"}, {"run_id": "c", "core": "junk"}, "x"]}
    assert we.result_cores(pr) == {"a": {"gross_pnl": 1.0}, "b": None, "c": None}
    assert we.result_cores(None) == {} and we.result_cores({}) == {}


@pytest.mark.parametrize("alloc,flips", [
    ([1, 0, -1], 1),                 # + 0 - : a flip through flat
    ([1, 0, 1], 0),                  # + 0 + : none
    ([1, -1, 1], 2),
    ([0, 0, 0], 0),
    ([0, 0.5, 0, 0, -0.5, 0], 1),
    ([1e-6, -0.5, 0.5], 1),          # |a| <= 1e-6 is flat: no sign, so only -0.5 -> 0.5 flips
    ([2e-6, -0.5], 1),               # just above the epsilon is a sign
    ([0.5], 0),
    ([], 0),
])
def test_direction_changes_skip_flat_stretches(alloc, flips):
    assert we.direction_changes(np.array(alloc, dtype=float)) == flips


def test_direction_changes_with_zeros_in_a_window_file(tmp_path):
    for name, post, want in (("flipthroughflat", [0.5, 0.0, -0.5], 1),
                             ("sameside", [0.5, 0.0, 0.5], 0)):
        rows = [("trend", 1000, 0.0, post[0])] + [("trend", 1000, post[i - 1], post[i])
                                                   for i in range(1, len(post))]
        write_window(tmp_path / name, rows, [])
        cell = we.window_economics([("X", name, tmp_path / name, None)])["windows"][f"X/{name}"]
        assert cell["direction_changes"] == want, name


def test_not_ready_rows_are_excluded_from_every_bar_field(wins):
    # W2's row 4 (" not_ready ", |alloc| 0.9) would give max 0.9, 5 bars, turnover +0.0
    b = we.window_economics(wins)["windows"]["BBB/w1"]
    assert b["n_bars"] == 4 and b["max_abs_allocation"] == 0.4
    # ... and W1's NOT_READY first row still supplies V0 (the account at the window's start)
    assert we.window_economics(wins[:1])["windows"]["AAA/w0"]["gross_pct"] == approx(4.0)


def test_a_window_without_lots_has_no_cost_drag_no_duration_and_no_holding(tmp_path):
    # what the run writes for a window without trades: counts and dollars 0, no ratio, no mean
    write_window(tmp_path / "e", W2_ROWS, [], W2_TURNOVER)
    core = core_of(0, 0.0, 0.0, 0.0, None, None)
    c = we.window_economics([("X", "w", tmp_path / "e", core)])["windows"]["X/w"]
    assert (c["trades"], c["gross_pct"], c["fees_pct"], c["net_pct"]) == (0, 0.0, 0.0, 0.0)
    assert c["cost_drag_pct"] is None and c["median_holding_bars"] is None
    assert c["avg_trade_duration_bars"] is None
    assert c["n_bars"] == 4 and c["turnover"] == approx(0.8)
    tot = we.window_economics([("X", "w", tmp_path / "e", core)])["total"]
    assert tot["trades"] == 0 and tot["avg_trade_duration_bars"] is None


def test_zero_gross_gives_the_runs_no_cost_drag_but_keeps_the_rest(tmp_path):
    write_window(tmp_path / "z", W2_ROWS, [lot(10.0, 1.0, 9.0, 60.0), lot(-10.0, 1.0, -11.0, 120.0)])
    core = core_of(2, 0.0, 2.0, -2.0, None, 1.5)
    c = we.window_economics([("X", "w", tmp_path / "z", core)])["windows"]["X/w"]
    assert c["gross_pct"] == 0.0 and c["cost_drag_pct"] is None
    assert c["fees_pct"] == approx(0.1) and c["net_pct"] == approx(-0.1)
    assert c["median_holding_bars"] == 1.5 and c["avg_trade_duration_bars"] == 1.5
    assert c["turnover"] is None                       # no metrics.json: not recomputed
    assert we.window_economics([("X", "w", tmp_path / "z", core)])["total"]["cost_drag_pct"] is None


def test_the_step_is_the_median_bar_spacing_not_a_fixed_hour(tmp_path):
    f = tmp_path / "d"
    f.mkdir()
    # a daily window: 1440 minutes is one bar
    (f / "bars.csv").write_text(BARS_HDR + "\n" + "\n".join(
        f"2020-01-0{d} 00:00:00,trend,1000,0,0.1" for d in range(1, 5)) + "\n", encoding="utf-8")
    (f / "trades.json").write_text(json.dumps([lot(1.0, 0.1, 0.9, 2880.0)]), encoding="utf-8")
    assert we.window_economics([("X", "d", f, None)])["windows"]["X/d"][
        "median_holding_bars"] == 2.0


def test_the_inputs_are_not_modified_and_the_result_is_deterministic(wins):
    def snap():
        return [(p / "bars.csv").read_bytes() + (p / "trades.json").read_bytes()
                + (p / "metrics.json").read_bytes() for _s, _w, p, _c in wins]
    before, cores = snap(), copy.deepcopy([c for *_x, c in wins])
    a, b = we.window_economics(wins), we.window_economics(copy.deepcopy(wins))
    assert a == b
    assert before == snap() and cores == [c for *_x, c in wins]


def test_the_windows_must_be_four_tuples_with_the_core(wins):
    with pytest.raises(ValueError):
        we.window_economics([wins[0][:3]])


def test_a_duplicate_label_raises(wins):
    with pytest.raises(ValueError, match="given twice"):
        we.window_economics([wins[0], ("AAA", "w0", wins[1][2], None)])


def test_no_window_raises():
    with pytest.raises(ValueError, match="no window"):
        we.window_economics([])


def test_a_missing_column_raises(tmp_path):
    f = tmp_path / "m"
    f.mkdir()
    (f / "bars.csv").write_text("timestamp,regime,total_portfolio_value,previous_allocation\n"
                                "2020-01-01 00:00:00,trend,1000,0\n"
                                "2020-01-01 01:00:00,trend,1000,0\n", encoding="utf-8")
    (f / "trades.json").write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="missing column.*postRebalance_current_allocation"):
        we.window_economics([("X", "w", f, None)])


@pytest.mark.parametrize("bad", ["x", None, True, float("nan")])
def test_a_non_numeric_lot_duration_raises(tmp_path, bad):
    t = lot(1.0, 0.1, 0.9, 60.0)
    t["duration_minutes"] = bad
    write_window(tmp_path / "t", W2_ROWS, [t])
    # NaN is written by json.dumps as NaN and read back as a float nan
    with pytest.raises(ValueError, match="no numeric duration_minutes"):
        we.window_economics([("X", "w", tmp_path / "t", None)])


def test_the_lots_dollar_fields_are_not_read_so_their_absence_is_not_an_error(tmp_path):
    write_window(tmp_path / "t", W2_ROWS, [{"duration_minutes": 60.0}], W2_TURNOVER)
    c = we.window_economics([("X", "w", tmp_path / "t", W2_CORE)])["windows"]["X/w"]
    assert c["gross_pct"] == approx(2.0) and c["median_holding_bars"] == 1.0


def test_a_trade_row_that_is_not_a_mapping_raises(tmp_path):
    write_window(tmp_path / "t", W2_ROWS, [[1, 2]])
    with pytest.raises(ValueError, match="not a mapping"):
        we.window_economics([("X", "w", tmp_path / "t", None)])


def test_missing_files_and_degenerate_windows_raise(tmp_path):
    write_window(tmp_path / "nt", W2_ROWS, None)
    with pytest.raises(OSError):
        we.window_economics([("X", "w", tmp_path / "nt", None)])
    with pytest.raises(OSError):
        we.window_economics([("X", "w", tmp_path / "nowhere", None)])
    write_window(tmp_path / "one", W2_ROWS[:1], [])
    with pytest.raises(ValueError, match="fewer than 2 bars"):
        we.window_economics([("X", "w", tmp_path / "one", None)])
    write_window(tmp_path / "v0", [("trend", 0, 0.0, 0.1)] * 3, [])
    with pytest.raises(ValueError, match="not positive"):
        we.window_economics([("X", "w", tmp_path / "v0", None)])
    write_window(tmp_path / "nan", [("trend", 1000, 0.0, "")] * 3, [])
    with pytest.raises(ValueError, match="NaN allocation"):
        we.window_economics([("X", "w", tmp_path / "nan", None)])


# ---------------------------------------------------------------------------
# a saved-run-shaped fixture (tests/test_e075_pr4_queries.make_run) with the economics fields
# ---------------------------------------------------------------------------

def saved_core(i):
    """The core block the saved-run fixture gives its i-th window (hand-typed as a run would
    write it; the figures differ per window so a mis-paired window is caught): 8 lots, gross
    $(360 + 100 i), fees $(8 + i), net = gross - fees, cost drag fees / gross, rounded to 4
    places as run_artifact.build_core does, mean duration sum(HOLDS) / 8 = 4.75 bars."""
    gross, fees = 360.0 + 100.0 * i, 8.0 + i
    return core_of(8, gross, fees, gross - fees, round(fees / gross * 100, 4), 4.75)


def enrich(run):
    """Add the trades.json fields the lots' own tools read, hand-made per lot k = 0..7:
    gross $ 10(k+1), fee $1, net $10(k+1)-1, duration HOLDS[k] bars of an hour,
    profit_loss_percent (k+1)-4, total_commission_percent 0.1+0.01k; and what the economics
    READ: each window's `core` block in the variant's protocol_result.yaml (saved_core) and
    its metrics.json bar_equity.turnover (an independent numpy sum over the file's own two
    allocation columns, rounded to 6 places as the run rounds it)."""
    for p in sorted(Path(run).glob("variants/base/results/*/trades.json")):
        trades = json.loads(p.read_text(encoding="utf-8"))
        for k, t in enumerate(trades):
            t.update(profit_loss_absolute=10.0 * (k + 1), total_commission=1.0,
                     net_profit_loss_absolute=10.0 * (k + 1) - 1.0,
                     duration_minutes=HOLDS[k] * 60.0,
                     profit_loss_percent=float(k + 1) - 4.0,
                     total_commission_percent=0.1 + 0.01 * k)
        p.write_text(json.dumps(trades), encoding="utf-8")
    pr_path = Path(run) / "artifacts" / "variants" / "base" / "protocol_result.yaml"
    pr = yaml.safe_load(pr_path.read_text(encoding="utf-8"))
    for i, entry in enumerate(pr["results"]):
        entry["core"] = saved_core(i)
        df = pd.read_csv(Path(run) / "variants" / "base" / "results" / entry["run_id"] / "bars.csv")
        turn = float(np.abs(df["postRebalance_current_allocation"].to_numpy()
                            - df["previous_allocation"].to_numpy()).sum())
        (Path(run) / "variants" / "base" / "results" / entry["run_id"] / "metrics.json"
         ).write_text(json.dumps({"core": entry["core"], "bar_equity": {"turnover": round(turn, 6)}}),
                      encoding="utf-8")
    pr_path.write_text(yaml.safe_dump(pr), encoding="utf-8")


@pytest.fixture()
def run(tmp_path):
    root = make_run(tmp_path / "run_001")
    enrich(root)
    return root


def _window_dirs(run):
    """(symbol, window, folder, core) of the saved run's windows, the core from its
    protocol_result.yaml as the query reads it."""
    pr = yaml.safe_load((Path(run) / "artifacts" / "variants" / "base" / "protocol_result.yaml")
                        .read_text(encoding="utf-8"))
    cores = we.result_cores(pr)
    return [(s, w, Path(run) / "variants" / "base" / "results" / rid, cores[rid])
            for (rid, s, w, _o, _sd) in pr4.WINDOWS]


# ---------------------------------------------------------------------------
# 2. the query
# ---------------------------------------------------------------------------

def test_the_query_returns_the_hand_numbers_of_the_saved_run(run):
    res = engine(run).window_economics()
    assert res["status"] == "ok"
    out = res["result"]
    assert list(out["windows"]) == ["AAA/w0", "AAA/w1", "BBB/w0"]
    for i, cell in enumerate(out["windows"].values()):
        # the window's own core block (saved_core(i)); V0 = 1000 (the first row): gross
        # $(360 + 100 i) -> (36 + 10 i) %, fees $(8 + i) -> (0.8 + 0.1 i) %, net = their difference
        c = saved_core(i)
        assert cell["trades"] == 8 and cell["n_bars"] == N
        assert cell["gross_pct"] == approx(36.0 + 10.0 * i)
        assert cell["fees_pct"] == approx(0.8 + 0.1 * i)
        assert cell["net_pct"] == approx(35.2 + 9.9 * i)
        assert cell["cost_drag_pct"] == c["cost_drag_pct"]
        assert cell["avg_trade_duration_bars"] == 4.75
        assert cell["median_holding_bars"] == 4.5        # 2 3 3 4 5 5 7 9
        # the exits alternate +0.3 / -0.3 over 8 lots: 7 flips, mean |a| = 8 * 0.3 / N
        assert cell["direction_changes"] == 7 and cell["max_abs_allocation"] == 0.3
        assert cell["mean_abs_allocation"] == approx(8 * 0.3 / N)
    # turnover: metrics.json's bar_equity.turnover, written by enrich from an independent numpy
    # sum over the file's own two columns
    for (sym, win, folder, _core) in _window_dirs(run):
        df = pd.read_csv(folder / "bars.csv")
        want = float(np.abs(df["postRebalance_current_allocation"].to_numpy()
                            - df["previous_allocation"].to_numpy()).sum())
        assert out["windows"][f"{sym}/{win}"]["turnover"] == approx(want)
    t = out["total"]
    assert t["trades"] == 24 and t["n_bars"] == 3 * N and t["direction_changes"] == 21
    assert t["gross_pct"] == approx(36.0 * 3 + 30.0) and t["net_pct"] == approx(35.2 * 3 + 29.7)
    # cost drag from the summed dollars: fees 8 + 9 + 10 = 27 over gross 360 + 460 + 560 = 1380
    assert t["cost_drag_pct"] == approx(27.0 / 1380.0 * 100)
    assert t["avg_trade_duration_bars"] == approx(4.75)
    assert t["median_holding_bars"] == 4.5


def test_the_query_is_the_module_function_over_the_same_folders(run):
    got = engine(run).window_economics()["result"]
    want = json.loads(json.dumps(we.window_economics(_window_dirs(run))))
    assert got == want


def _edit_results(run, fn):
    pr_path = Path(run) / "artifacts" / "variants" / "base" / "protocol_result.yaml"
    pr = yaml.safe_load(pr_path.read_text(encoding="utf-8"))
    fn(pr["results"])
    pr_path.write_text(yaml.safe_dump(pr), encoding="utf-8")


def test_the_query_pairs_each_window_with_its_core_by_run_id_whatever_the_result_order(
        tmp_path):
    base = make_run(tmp_path / "run_a")
    enrich(base)
    want = engine(base).window_economics()["result"]
    # the same run with protocol_result.yaml's results[] in another order: the windows are
    # loaded in that order, each must still read its own core (saved_core(i) differs per window)
    other = make_run(tmp_path / "run_b")
    enrich(other)
    _edit_results(other, lambda rs: rs.reverse())
    got = engine(other).window_economics()["result"]
    assert got["windows"] == want["windows"]
    assert list(got["windows"]) == list(reversed(list(want["windows"])))
    for k in ("trades", "n_bars", "direction_changes"):
        assert got["total"][k] == want["total"][k]
    for k in ("gross_pct", "fees_pct", "net_pct", "cost_drag_pct"):
        assert got["total"][k] == approx(want["total"][k])


def test_a_window_without_a_core_reads_none_never_another_windows_core(run):
    _edit_results(run, lambda rs: rs[1].pop("core"))
    res = engine(run).window_economics()
    assert res["status"] == "ok", res.get("reason")
    cells = res["result"]["windows"]
    for k in ("trades", "gross_pct", "fees_pct", "net_pct", "cost_drag_pct",
              "avg_trade_duration_bars"):
        assert cells["AAA/w1"][k] is None
        assert res["result"]["total"][k] is None
    for label, i in (("AAA/w0", 0), ("BBB/w0", 2)):
        assert cells[label]["gross_pct"] == approx(36.0 + 10.0 * i)
        assert cells[label]["trades"] == 8
    assert cells["AAA/w1"]["median_holding_bars"] == 4.5      # computed fields stay


def test_the_query_counts_zero_comparisons_and_leaves_the_total_alone(run):
    eng = engine(run)
    sel = {"kind": "event", "field": "forecast", "op": ">=", "value": 3.0}
    spent = eng.conditional_effect(sel, [1, 2])["cumulative_comparisons"]
    assert spent == 2
    r = eng.window_economics()
    assert (r["n_comparisons"], r["cumulative_comparisons"]) == (0, spent)
    assert log_of(eng)[-1]["n_comparisons"] == 0
    assert eng.window_economics()["cumulative_comparisons"] == spent
    # ... and it is never refused for the budget, even a spent one
    spent_eng = engine(run, comparison_budget=1)
    assert spent_eng.window_economics()["status"] == "ok"


def test_the_query_log_entry_has_a_digest_and_the_hash_of_its_result(run):
    eng = engine(run)
    res = eng.window_economics()
    e = log_of(eng)[-1]
    assert e["function"] == "window_economics" and e["status"] == "ok"
    t = res["result"]["total"]
    assert e["digest"] == (f"3 window(s); trades={t['trades']} turnover={t['turnover']} "
                           f"gross_pct={t['gross_pct']} net_pct={t['net_pct']}")
    assert e["result"] == res["result"]
    assert e["result_sha256"] == hashlib.sha256(aq._canon_json(res["result"]).encode()).hexdigest()
    assert e["params"] == {"variant": "base"} and e["n_comparisons"] == 0


def test_more_cells_than_the_cap_is_refused_and_logged(tmp_path, monkeypatch):
    wins = [(f"rw{i}", f"S{i}", "w0", 0, 40 + i) for i in range(13)]
    monkeypatch.setattr(pr4, "WINDOWS", wins)
    root = make_run(tmp_path / "run_big")
    enrich(root)
    assert aq.MAX_GROUPS == 12
    eng = engine(root)
    res = eng.window_economics()
    assert res["status"] == "refused" and "13 (coin, window) cells" in res["reason"]
    assert "cap of 12" in res["reason"] and res["n_comparisons"] == 0
    assert "result" not in res
    e = log_of(eng)[-1]
    assert e["function"] == "window_economics" and e["status"] == "refused"
    assert e["reason"] == res["reason"] and "result" not in e


def test_twelve_cells_are_not_over_the_cell_cap_or_the_character_cap(tmp_path, monkeypatch):
    # D-168: the derived fields take about 170 characters per cell; MAX_RESULT_CHARS is 6500 so
    # 12 cells and the total fit both the cell cap and the character cap.
    wins = [(f"rw{i}", f"S{i}", "w0", 0, 40 + i) for i in range(12)]
    monkeypatch.setattr(pr4, "WINDOWS", wins)
    root = make_run(tmp_path / "run_12")
    enrich(root)
    res = engine(root).window_economics()
    assert res["status"] == "ok", res.get("reason")
    assert len(res["result"]["windows"]) == 12
    assert len(aq._canon_json(res["result"])) <= aq.MAX_RESULT_CHARS


def test_the_cell_cap_follows_the_engine_constant(run, monkeypatch):
    monkeypatch.setattr(aq, "MAX_GROUPS", 2)
    res = engine(run).window_economics()
    assert res["status"] == "refused" and "3 (coin, window) cells" in res["reason"]
    assert "cap of 2" in res["reason"]


def test_a_result_over_the_character_cap_is_refused_and_logged(run, monkeypatch):
    eng = engine(run)
    monkeypatch.setattr(aq, "MAX_RESULT_CHARS", 150)
    res = eng.window_economics()
    assert res["status"] == "refused" and "over the 150 cap" in res["reason"]
    assert res["n_comparisons"] == 0 and log_of(eng)[-1]["status"] == "refused"


def test_unreadable_economics_are_a_logged_refusal(tmp_path):
    root = make_run(tmp_path / "raw")                 # trades.json without the lots' durations
    eng = engine(root)
    res = eng.window_economics()
    assert res["status"] == "refused" and "economics cannot be read" in res["reason"]
    assert "duration_minutes" in res["reason"]
    assert log_of(eng)[-1]["status"] == "refused"


def test_a_window_at_or_after_the_holdout_start_is_refused(run):
    # the fixture's windows run from 2020-01-01 (w0) and 2020-02-01 (w1), 130 hourly bars each
    eng = engine(run, holdout_start="2020-01-05")
    res = eng.window_economics()
    assert res["status"] == "refused" and "holdout" in res["reason"]
    assert "result" not in res and res["n_comparisons"] == 0
    e = log_of(eng)[-1]
    assert e["function"] == "window_economics" and e["status"] == "refused"
    assert engine(run, holdout_start="2020-03-01").window_economics()["status"] == "ok"


def test_missing_trades_and_foreign_variants_are_refused(tmp_path, run):
    nt = engine(make_run(tmp_path / "nt", trades=False))
    r = nt.window_economics()
    assert r["status"] == "refused" and "trades cannot be read" in r["reason"]
    eng = engine(run)
    assert eng.window_economics(variant="../other")["status"] == "refused"
    assert eng.window_economics(variant="nope")["status"] == "refused"


# ---------------------------------------------------------------------------
# 3. trade_slice: trade_gross_return, trade_cost_pct
# ---------------------------------------------------------------------------

def test_the_new_fields_are_in_the_closed_aggregates():
    assert "trade_gross_return" in aq.AGG_FIELDS and "trade_cost_pct" in aq.AGG_FIELDS
    assert "trade_gross_return" in aq._OUTCOME_AGG_FIELDS
    assert "trade_cost_pct" not in aq._OUTCOME_AGG_FIELDS


@pytest.mark.parametrize("field", ["abs_forecast", "forecast_sign_change"])
def test_after_pr_c_the_forecast_fields_and_the_gross_outcome_are_claim_names(field, run):
    """PR-C BOUNDARY, pinned (it was: none of PR-B's new names is a claim name). Now: event
    conditions on abs_forecast and forecast_sign_change are accepted by conditional_effect and
    charged as usual (one comparison per horizon); {kind: trade_gross_return} is a valid claim
    outcome; allocation_abs as a selector field and a trade_cost_pct filter field stay refused."""
    eng = engine(run)
    res = eng.conditional_effect({"kind": "event", "field": field, "op": ">=", "value": 0.0},
                                 [1, 2], "fwd_return", {"kind": "complement"})
    assert res["status"] == "ok", res.get("reason")
    assert res["n_comparisons"] == 2 and res["cumulative_comparisons"] == 2   # charged as usual
    assert res["result"]["compiles_as_claim"] is True

    def claim(test):
        return {"statement": "s", "kind": "conditional_behaviour", "tests": [test],
                "pass_if": "p", "fail_if": "f", "rationale": "r"}

    assert cc.check_claim(claim(res["result"]["test"])).errors == []          # and the claim passes

    # still refused: the allocation held after the bar is not a selector field
    res = eng.conditional_effect({"kind": "event", "field": "allocation_abs", "op": ">=",
                                  "value": 0.0}, [1, 2], "fwd_return", {"kind": "complement"})
    assert res["status"] == "refused"
    assert res["n_comparisons"] == 0 and res["cumulative_comparisons"] == 2   # nothing charged

    base = {"name": "t1", "selector": {"kind": "trade", "where": [
                {"field": "exit_cause", "op": "==", "value": "flip"}]},
            "outcome": {"kind": "trade_net_return"}, "baseline": {"kind": "other_trades"},
            "statistic": "mean_diff", "direction": "greater", "floor": {"min_events": 50}}
    # positive controls: the closed trade names, trade_gross_return now among them
    assert cc.check_claim(claim(base), trade_tests=True).errors == []
    good_outcome = dict(base, outcome={"kind": "trade_gross_return"})
    res = cc.check_claim(claim(good_outcome), trade_tests=True)
    assert res.errors == [] and len(res.tests) == 1, res.errors
    # a trade filter field that is not in the closed list is still refused
    bad_filter = dict(base, selector={"kind": "trade", "where": [
        {"field": "trade_cost_pct", "op": ">=", "value": 0.1}]})
    res = cc.check_claim(claim(bad_filter), trade_tests=True)
    assert res.errors and res.tests == [], res.errors


def test_trade_gross_return_values_are_trades_json_and_count_as_comparisons(run):
    eng = engine(run)
    res = eng.trade_slice([], [{"field": "trade_gross_return", "stat": "mean"},
                               {"field": "trade_gross_return", "stat": "share_positive"},
                               {"field": "trade_gross_return", "stat": "median"}])
    assert res["status"] == "ok"
    assert res["result"]["return_basis"] == ["net_of_fees_and_slippage"]   # no diagnostics file
    cell = res["result"]["groups"]["all"]
    # lots k = 0..7 of 3 windows: profit_loss_percent (k+1)-4 -> -3..4 -> /100
    assert cell["n_trades"] == 24
    assert cell["trade_gross_return_mean"] == approx(0.005)
    assert cell["trade_gross_return_median"] == approx(0.005)            # (0.00 + 0.01) / 2
    assert cell["trade_gross_return_share_positive"] == 0.5               # k+1 >= 5: four of eight
    # one group x three aggregates of an outcome
    assert (res["n_comparisons"], res["cumulative_comparisons"]) == (3, 3)
    res = eng.trade_slice([], [{"field": "trade_gross_return", "stat": "mean"}], by="direction")
    g = res["result"]["groups"]
    assert g["long"]["trade_gross_return_mean"] == approx(0.0)           # k even: -3 -1 1 3
    assert g["short"]["trade_gross_return_mean"] == approx(0.01)         # k odd: -2 0 2 4
    assert (res["n_comparisons"], res["cumulative_comparisons"]) == (2, 5)
    # a count relates nothing
    res = eng.trade_slice([], [{"field": "trade_gross_return", "stat": "count"}])
    assert res["n_comparisons"] == 0 and res["result"]["groups"]["all"]["trade_gross_return_count"] == 24


def test_trade_cost_pct_is_the_commission_rate_and_counts_nothing(run):
    eng = engine(run)
    res = eng.trade_slice([], [{"field": "trade_cost_pct", "stat": "mean"},
                               {"field": "trade_cost_pct", "stat": "median"},
                               {"field": "trade_cost_pct", "stat": "share_positive"}], by="direction")
    assert res["status"] == "ok" and res["n_comparisons"] == 0
    g = res["result"]["groups"]
    # total_commission_percent 0.1 + 0.01k: k even 0.1 0.12 0.14 0.16, k odd 0.11 0.13 0.15 0.17
    assert g["long"]["trade_cost_pct_mean"] == approx(0.13)
    assert g["short"]["trade_cost_pct_mean"] == approx(0.14)
    assert g["long"]["trade_cost_pct_share_positive"] == 1.0
    assert eng.trade_slice([], [{"field": "trade_cost_pct", "stat": "mean"}])[
        "cumulative_comparisons"] == 0


def test_the_new_fields_follow_the_filter_and_the_lot_order_of_trades_json(run):
    eng = engine(run)
    flt = [{"field": "side", "op": "==", "value": "short"}]
    cell = eng.trade_slice(flt, [{"field": "trade_gross_return", "stat": "mean"},
                                 {"field": "trade_cost_pct", "stat": "mean"}])["result"][
        "groups"]["all"]
    assert cell["n_trades"] == 12
    assert cell["trade_gross_return_mean"] == approx(0.01)
    assert cell["trade_cost_pct_mean"] == approx(0.14)
    # the lots of every trades.json in the opposite order (a fresh engine): each lot keeps its own
    # side, gross return and cost, so the short lots' numbers are the same
    for p in Path(run).glob("variants/base/results/*/trades.json"):
        lots = json.loads(p.read_text(encoding="utf-8"))
        p.write_text(json.dumps(lots[::-1]), encoding="utf-8")
    again = engine(run).trade_slice(flt, [{"field": "trade_gross_return", "stat": "mean"}])
    assert again["status"] == "ok"
    assert again["result"]["groups"]["all"]["trade_gross_return_mean"] == approx(0.01)


def test_a_lot_count_that_no_longer_matches_trades_json_is_refused(run):
    eng = engine(run)
    assert eng.trade_slice([], [{"field": "holding_bars", "stat": "mean"}])["status"] == "ok"
    p = next(Path(run).glob("variants/base/results/*/trades.json"))
    lots = json.loads(p.read_text(encoding="utf-8"))
    p.write_text(json.dumps(lots + [lots[0]]), encoding="utf-8")        # 9 lots against 8 loaded
    # trade_cost_pct is the field still read from trades.json beside the loaded lots (PR-C S1:
    # trade_gross_return reads the loaded TradeWindow itself)
    res = eng.trade_slice([], [{"field": "trade_cost_pct", "stat": "mean"}])
    assert res["status"] == "refused" and "does not match its loaded lots" in res["reason"]
    assert res["n_comparisons"] == 0 and log_of(eng)[-1]["status"] == "refused"


def test_a_lot_without_the_percent_field_is_nan_and_leaves_the_group_to_the_others(run):
    for p in Path(run).glob("variants/base/results/*/trades.json"):
        lots = json.loads(p.read_text(encoding="utf-8"))
        del lots[0]["profit_loss_percent"]
        p.write_text(json.dumps(lots), encoding="utf-8")
    cell = engine(run).trade_slice([], [{"field": "trade_gross_return", "stat": "mean"}])[
        "result"]["groups"]["all"]
    assert cell["n_trades"] == 24
    assert cell["trade_gross_return_mean"] == approx(np.mean([(k + 1 - 4) / 100 for k in range(1, 8)]))


def _all_costs(run):
    """The variant's trade_diagnostics.json (CUL-414 all-costs records) for every lot of the
    fixture, hand-made: window i (pr4.WINDOWS order), lot k: gross_return_before_costs
    0.5(k+1) - 1 + 0.1 i (%), cost_paid_all 10 + k (bps). Its gross differs from trades.json's
    profit_loss_percent (k+1) - 4, so the source of the number is visible."""
    recs = []
    for i, (rid, sym, win, _off, _seed) in enumerate(pr4.WINDOWS):
        for k in range(len(HOLDS)):
            recs.append({"trade_id": f"{rid}-{k}", "window": win, "symbol": sym,
                         "gross_return_before_costs": 0.5 * (k + 1) - 1.0 + 0.1 * i,
                         "cost_paid_all": 10.0 + k})
    (Path(run) / "variants" / "base" / "trade_diagnostics.json").write_text(
        json.dumps({"trades": recs}), encoding="utf-8")


def test_trade_gross_return_is_the_claim_outcomes_number_on_the_windows_basis(run):
    """S1 (operator ruling 2026-10-19): trade_slice's trade_gross_return reads the loaded
    TradeWindow's gross_return, the same per-lot number as the claim outcome
    {kind: trade_gross_return}; return_basis names the basis. On the all_costs basis that is
    gross_return_before_costs / 100, not trades.json's profit_loss_percent / 100."""
    import claim_tests as ct
    _all_costs(run)
    eng = engine(run)
    res = eng.trade_slice([], [{"field": "trade_gross_return", "stat": "mean"},
                               {"field": "trade_cost_pct", "stat": "mean"}])
    assert res["status"] == "ok"
    assert res["result"]["return_basis"] == ["all_costs"]
    cell = res["result"]["groups"]["all"]
    twins = ct.load_variant_trade_windows(run, "base")
    assert [tw.basis for tw in twins] == ["all_costs"] * 3
    claim_vals = np.concatenate([ct.trade_outcome(tw, "trade_gross_return", 0) for tw in twins])
    assert len(claim_vals) == cell["n_trades"] == 24
    # mean over k of 0.5(k+1) - 1 is 1.25 %, plus 0.1 i averaged over i = 0, 1, 2: 1.35 %
    assert cell["trade_gross_return_mean"] == approx(float(claim_vals.mean()))
    assert cell["trade_gross_return_mean"] == approx(0.0135)
    assert cell["trade_gross_return_mean"] != approx(0.005)            # not trades.json's 0.005
    assert cell["trade_cost_pct_mean"] == approx(0.135)                # still trades.json's rate
    # by direction, under a filter: the same numbers as the claim outcome's lots
    flt = [{"field": "side", "op": "==", "value": "short"}]
    g = eng.trade_slice(flt, [{"field": "trade_gross_return", "stat": "median"}],
                        by="window")["result"]["groups"]
    for tw in twins:
        short = ct.trade_outcome(tw, "trade_gross_return", 0)[tw.side == "short"]
        assert g[tw.label]["trade_gross_return_median"] == approx(float(np.median(short)))


# ---------------------------------------------------------------------------
# 4. derived bar columns
# ---------------------------------------------------------------------------

FIRST = [3.0, -2.0, 0.0, 4.0, -1.0, 0.0, 0.0, 5.0, -5.0, 2.0]


def _set_forecast(run, first=FIRST, rest=1.0):
    """Window 1's forecasts: FIRST, then `rest`. Returns its bars.csv path."""
    p = Path(run) / "variants" / "base" / "results" / "R1" / "bars.csv"
    df = pd.read_csv(p)
    df["forecast"] = float(rest)
    df.loc[: len(first) - 1, "forecast"] = first
    df.to_csv(p, index=False)
    return p


def test_forecast_sign_change_with_zero_forecasts_and_a_nan_first_bar(run):
    _set_forecast(run)
    v = engine(run)._column_values("base", "forecast_sign_change")[0]
    v = np.asarray(v, dtype=float)
    assert len(v) == N and math.isnan(v[0])
    # 3 -> -2 flips; -2 -> 0 and 0 -> 4 do not (a zero has no sign); 4 -> -1 flips; -1 -> 0,
    # 0 -> 0, 0 -> 5 do not; 5 -> -5 and -5 -> 2 flip; 2 -> 1 and on, none
    assert v[1:10].tolist() == [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0]
    assert v[10:].tolist() == [0.0] * (N - 10)


def test_forecast_sign_change_is_nan_after_a_missing_previous_stamp(run):
    p = _set_forecast(run, first=[1.0, -1.0] * 8)
    df = pd.read_csv(p)
    df = df.drop(index=12).reset_index(drop=True)          # the bar stamped 12:00 is gone
    df.to_csv(p, index=False)
    v = np.asarray(engine(run)._column_values("base", "forecast_sign_change")[0], dtype=float)
    assert len(v) == N - 1
    # rows 0..11 as before (alternating signs -> 1 from the second), row 12 is the old bar 13:
    # its t-1 stamp (12:00) is missing -> NaN, row 13 (old 14) has its t-1 present again
    assert math.isnan(v[0]) and v[1:12].tolist() == [1.0] * 11
    assert math.isnan(v[12])
    assert v[13] == 1.0


def test_forecast_sign_change_is_nan_when_a_forecast_is_not_finite(run):
    p = _set_forecast(run, first=[1.0, float("nan"), -1.0, 2.0])
    v = np.asarray(engine(run)._column_values("base", "forecast_sign_change")[0], dtype=float)
    assert math.isnan(v[1]) and math.isnan(v[2])            # nan at t, nan at t-1
    assert v[3] == 1.0 and p.exists()


def test_forecast_sign_change_reads_no_future_bar(run):
    p = _set_forecast(run, first=[1.0, -1.0, 2.0, -2.0] * 20)
    base = np.asarray(engine(run)._column_values("base", "forecast_sign_change")[0], dtype=float)
    df = pd.read_csv(p)
    df.loc[61:, "forecast"] = -df.loc[61:, "forecast"] * 7 + 3.0     # bar t+1 = 61 and later changed
    df.to_csv(p, index=False)
    new = np.asarray(engine(run)._column_values("base", "forecast_sign_change")[0], dtype=float)
    # bars 0..60 depend on bars <= 60 only: unchanged (including bar 60, whose t+1 was perturbed)
    assert np.array_equal(base[:61], new[:61], equal_nan=True)
    assert not np.array_equal(base[61:], new[61:], equal_nan=True)     # the perturbation was real


def test_abs_forecast_and_allocation_abs_are_bar_t_absolute_values(run):
    _set_forecast(run)
    eng = engine(run)
    folders = _window_dirs(run)
    fa = eng._column_values("base", "abs_forecast")
    aa = eng._column_values("base", "allocation_abs")
    for i, (_s, _w, folder, _c) in enumerate(folders):
        df = pd.read_csv(folder / "bars.csv")
        assert np.allclose(np.asarray(fa[i], dtype=float), np.abs(df["forecast"].to_numpy()),
                           rtol=1e-12, atol=0)
        assert np.allclose(np.asarray(aa[i], dtype=float),
                           np.abs(df["postRebalance_current_allocation"].to_numpy()),
                           rtol=1e-12, atol=0)
    assert (np.asarray(aa[0]) == 0.3).sum() == 8              # the eight exit bars
    g = eng.describe("abs_forecast")["result"]["groups"]["all"]
    allf = np.concatenate([np.abs(pd.read_csv(f / "bars.csv")["forecast"].to_numpy())
                           for _s, _w, f, _c in folders])
    assert g["n"] == len(allf) and g["mean"] == aq.r8(allf.mean())


def test_list_columns_lists_the_derived_columns(run):
    out = engine(run).list_columns()["result"]
    derived = out["derived_columns"]
    for name in ("abs_forecast", "forecast_sign_change", "allocation_abs"):
        assert name in derived
    assert any(d.startswith("past_return_<n>") for d in derived)
    assert any(d.startswith("trailing_vol_<n>") for d in derived)
    assert len(aq._canon_json(out)) <= aq.MAX_RESULT_CHARS
    assert set(aq.DERIVED_COLUMNS) == {"past_return", "trailing_vol", "abs_forecast",
                                       "forecast_sign_change", "allocation_abs"}


@pytest.mark.parametrize("col", ["abs_forecast", "allocation_abs", "forecast_sign_change"])
def test_describe_of_the_new_columns_by_hour_weekday_regime_still_charges(run, col):
    eng = engine(run)
    for by in ("hour", "weekday", "regime"):
        r = eng.describe(col, by=by)
        assert r["status"] == "ok", (col, by, r.get("reason"))
        assert r["n_comparisons"] == len(r["result"]["groups"]) >= 1, (col, by)
    assert eng.describe(col)["n_comparisons"] == 0
    assert eng.describe(col, by="window")["n_comparisons"] == 0
    assert eng.distribution(col, by="hour", bins=3)["n_comparisons"] > 0


def test_a_derived_column_with_no_value_in_the_run_is_refused(run):
    for _s, _w, folder, _c in _window_dirs(run):
        df = pd.read_csv(folder / "bars.csv")
        df["forecast"] = float("nan")
        df.to_csv(folder / "bars.csv", index=False)
    r = engine(run).describe("forecast_sign_change")
    assert r["status"] == "refused" and "no numeric value" in r["reason"]


# ---------------------------------------------------------------------------
# 5. profit_bars_evaluation.yaml
# ---------------------------------------------------------------------------

class _FrozenDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2020, 6, 1, 12, 0, 0, tzinfo=tz)


def _window_folder(run_dir, vid, sym, w):
    return run_dir / "variants" / vid / "results" / f"{vid}-{sym}-{w}"


def _bars_for(folder, k):
    """A 6-bar window; its numbers depend on k (the window's index) so cells differ."""
    rows = [("NOT_READY", 1000, 0.0, 0.0)] + [
        ("trend", 1000 + 5 * i, a, b) for i, (a, b) in enumerate(
            [(0.0, 0.5), (0.5, 0.5), (0.5, -0.25), (-0.25, 0.0), (0.0, 0.2)])]
    write_window(folder, rows, [lot(20.0 + k, 2.0, 18.0 + k, 120.0), lot(-5.0, 1.0, -6.0, 60.0)],
                 turnover=1.7)


def _graded_core(k):
    """The core block of window k: what the run would have recorded for _bars_for(k)'s two
    lots (gross 20 + k and -5 -> 15 + k, fees 3, net 12 + k, mean duration 1.5 bars)."""
    gross = 15.0 + k
    return core_of(2, gross, 3.0, gross - 3.0, round(3.0 / gross * 100, 4), 1.5)


@pytest.fixture()
def stub_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _graded_run():
    tpb._set_orchestrator({**tpb.FULL_ON, **tpb.VARIANT_LOOP_ON})
    tpb._write_bars()
    run_dir = tpb._variant_run({"base": False, "design": True})
    k = 0
    for vid in ("base", "design"):
        pr_path = run_dir / "artifacts" / "variants" / vid / "protocol_result.yaml"
        pr = rpr.load_yaml(pr_path)
        for sym in ("BTCUSDT", "ETHUSDT"):
            for w in ("w1", "w2"):
                _bars_for(_window_folder(run_dir, vid, sym, w), k)
                (entry,) = [r for r in pr["results"] if (r["symbol"], r["window"]) == (sym, w)]
                entry["core"] = {**entry["core"], **_graded_core(k)}
                k += 1
        rpr.save_yaml(pr_path, pr)
    return run_dir


def _evaluate(run_dir, monkeypatch, flag):
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda cfg=None: flag)
    monkeypatch.setattr(rpr, "datetime", _FrozenDatetime)
    ev = rpr._evaluate_profit_bars_every_backtest(run_dir, tpb.RUN_ID)
    return ev, (run_dir / "artifacts" / "profit_bars_evaluation.yaml").read_bytes()


def _without_economics(d):
    d = json.loads(json.dumps(d, default=str))
    for v in d["variants"].values():
        v.pop("window_economics", None)
    return d


@pytest.mark.usefixtures("reader_docs", "stub_python")
def test_flag_off_has_no_key_and_the_file_is_byte_identical(monkeypatch):
    run_dir = _graded_run()
    ev, raw = _evaluate(run_dir, monkeypatch, False)
    assert all("window_economics" not in v for v in ev["variants"].values())
    assert b"window_economics" not in raw
    # a second off run, the economics helper forbidden to run: the same bytes
    monkeypatch.setattr(rpr, "_variant_window_economics",
                        lambda *a, **k: pytest.fail("window_economics ran with the flag off"))
    ev2, raw2 = _evaluate(run_dir, monkeypatch, False)
    assert raw2 == raw and _without_economics(ev2) == _without_economics(ev)


@pytest.mark.usefixtures("reader_docs", "stub_python")
def test_flag_on_adds_only_the_key_after_forecast_shape(monkeypatch):
    run_dir = _graded_run()
    off, raw_off = _evaluate(run_dir, monkeypatch, False)
    on, raw_on = _evaluate(run_dir, monkeypatch, True)
    for vid, v in on["variants"].items():
        assert "window_economics" in v, vid
        keys = list(v)
        assert keys.index("window_economics") == keys.index("forecast_shape") + 1, vid
    # nothing else differs: result, passing, bars, reasons, forecast_shape all as flag off
    assert _without_economics(on) == _without_economics(off)
    disk_on = yaml.safe_load(raw_on)
    disk_off = yaml.safe_load(raw_off)
    assert _without_economics(disk_on) == _without_economics(disk_off)
    assert "window_economics" in disk_on["variants"]["design"]


@pytest.mark.usefixtures("reader_docs", "stub_python")
def test_flag_on_graded_variants_carry_the_economics_and_the_others_none(monkeypatch):
    run_dir = _graded_run()
    on, _raw = _evaluate(run_dir, monkeypatch, True)
    for vid in ("base", "design"):
        we_ = on["variants"][vid]["window_economics"]
        assert list(we_["windows"]) == ["BTCUSDT/w1", "BTCUSDT/w2", "ETHUSDT/w1", "ETHUSDT/w2"]
        assert set(we_["total"]) == CELL_KEYS
        assert we_["total"]["trades"] == 8 and we_["total"]["n_bars"] == 20
    # hand numbers of one cell (base, BTCUSDT/w1, k = 0): V0 1000; lots 20/-5 gross -> 1.5%,
    # fees 3 -> 0.3%, net 18-6 = 12 -> 1.2% ; turnover .5+0+.75+.25+.2 = 1.7
    c = on["variants"]["base"]["window_economics"]["windows"]["BTCUSDT/w1"]
    assert c["trades"] == 2 and c["gross_pct"] == approx(1.5) and c["fees_pct"] == approx(0.3)
    assert c["net_pct"] == approx(1.2) and c["turnover"] == approx(1.7)
    assert c["direction_changes"] == 2 and c["cost_drag_pct"] == approx(20.0)
    assert c["median_holding_bars"] == 1.5 and c["avg_trade_duration_bars"] == 1.5
    # the next window of the variant carries its OWN core (k = 1: gross $16 -> 1.6 %)
    c1 = on["variants"]["base"]["window_economics"]["windows"]["BTCUSDT/w2"]
    assert c1["gross_pct"] == approx(1.6) and c1["net_pct"] == approx(1.3)
    for vid in ("asset", "broken"):                  # no protocol_result: the key is None
        assert on["variants"][vid]["result"] == "NOT_TESTED"
        assert on["variants"][vid]["window_economics"] is None


@pytest.mark.usefixtures("reader_docs", "stub_python")
def test_flag_on_a_variant_without_core_blocks_has_none_read_figures_and_grading_is_unchanged(
        monkeypatch):
    run_dir = _graded_run()
    pr_path = run_dir / "artifacts" / "variants" / "design" / "protocol_result.yaml"
    pr = rpr.load_yaml(pr_path)
    for r in pr["results"]:                           # an older run: only the grader's figure
        r["core"] = {"sharpe": r["core"]["sharpe"]}
    rpr.save_yaml(pr_path, pr)
    off, _ = _evaluate(run_dir, monkeypatch, False)
    on, _ = _evaluate(run_dir, monkeypatch, True)
    t = on["variants"]["design"]["window_economics"]["total"]
    for k in ("trades", "gross_pct", "fees_pct", "net_pct", "cost_drag_pct",
              "avg_trade_duration_bars"):
        assert t[k] is None, k
    assert t["turnover"] == approx(4 * 1.7) and t["n_bars"] == 20      # metrics.json is read
    assert on["variants"]["base"]["window_economics"]["total"]["gross_pct"] is not None
    assert on["result"] == off["result"] and on["passing"] == off["passing"]


@pytest.mark.usefixtures("reader_docs", "stub_python")
@pytest.mark.parametrize("what", ["bars", "trades", "equity_file", "column"])
def test_flag_on_missing_or_unreadable_files_give_none_and_grading_is_unchanged(monkeypatch, what):
    run_dir = _graded_run()
    folder = _window_folder(run_dir, "design", "ETHUSDT", "w2")
    if what == "bars":
        (folder / "bars.csv").unlink()
    elif what == "trades":
        (folder / "trades.json").unlink()
    elif what == "equity_file":
        (folder / "portfolio_states.csv").unlink()
    else:
        (folder / "bars.csv").write_text("timestamp,regime\n2020-01-01 00:00:00,trend\n",
                                         encoding="utf-8")
    off, _ = _evaluate(run_dir, monkeypatch, False)          # the same damaged run, flag off
    on, _ = _evaluate(run_dir, monkeypatch, True)
    assert on["variants"]["design"]["window_economics"] is None
    assert on["variants"]["base"]["window_economics"] is not None
    assert on["result"] == off["result"] and on["passing"] == off["passing"]


def test_the_stored_object_is_the_one_the_query_returns(run):
    # a stub equity file in every window of the saved-run fixture, so the helper finds each folder
    for _s, _w, folder, _c in _window_dirs(run):
        (folder / "portfolio_states.csv").write_text("timestamp,regime\n", encoding="utf-8")
    pr = yaml.safe_load((Path(run) / "artifacts" / "variants" / "base" / "protocol_result.yaml")
                        .read_text(encoding="utf-8"))
    stored = rpr._variant_window_economics(Path(run), pr)
    queried = engine(run).window_economics()["result"]
    assert stored is not None
    assert json.loads(json.dumps(stored)) == queried


def test_the_helper_returns_none_instead_of_raising(tmp_path):
    assert rpr._variant_window_economics(tmp_path, {"results": []}) is None
    assert rpr._variant_window_economics(tmp_path, {}) is None
    assert rpr._variant_window_economics(tmp_path, None) is None
    assert rpr._variant_window_economics(tmp_path, {"results": ["x"]}) is None
    assert rpr._variant_window_economics(tmp_path, {"results": [{"run_id": "nope", "symbol": "A",
                                                                 "window": "w"}]}) is None


# ---------------------------------------------------------------------------
# 6. registration
# ---------------------------------------------------------------------------

def test_the_tool_is_registered_in_the_session_and_the_workflow():
    assert "window_economics" in asm.TOOL_NAMES
    assert "mcp__analyst__window_economics" in asm.ALLOWED_TOOLS and len(asm.ALLOWED_TOOLS) == 7
    assert "window_economics" in rpr._ANALYST_TOOL_SCHEMAS
    assert "window_economics" in rpr._ANALYST_TOOL_HELP
    assert set(rpr._ANALYST_TOOL_SCHEMAS) == set(rpr._ANALYST_TOOL_HELP) == set(asm.TOOL_NAMES)
    props, required = rpr._ANALYST_TOOL_SCHEMAS["window_economics"]
    assert props == {"variant": {"type": "string"}} and required == []
    assert hasattr(aq.QueryEngine, "window_economics")


def test_the_sdk_tool_list_has_a_wrapper_per_tool():
    tools = rpr._analyst_tools(object())
    assert [t.name for t in tools] == list(asm.TOOL_NAMES) and len(tools) == 7


def test_the_data_dictionary_describes_the_new_tool_and_fields():
    text = (SR_ROOT / "docs" / "DATA_DICTIONARY.md").read_text(encoding="utf-8")
    for needle in ("window_economics", "trade_gross_return", "trade_cost_pct", "abs_forecast",
                   "allocation_abs", "forecast_sign_change", "median_holding_bars",
                   "direction_changes", "cost_drag_pct"):
        assert needle in text, needle
    for key in we.CELL_KEYS:
        assert f"`{key}`" in text, key
