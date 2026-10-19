"""PR-B (analyst tools, 2026-10-19): window_economics, trade_gross_return / trade_cost_pct and the
derived bar columns abs_forecast, allocation_abs, forecast_sign_change.

  1. tools/window_economics.py on hand-computed fixtures: every field of a window, of `total`,
     direction changes with zeros, NOT_READY rows out, empty trades, gross 0, the refusals.
  2. The query: zero comparisons, the 12-cell cap, the logged refusal, the digest; the engine's
     object is the stored object (run_phase1_research._variant_window_economics).
  3. trade_slice: trade_gross_return counts as a comparison, trade_cost_pct does not; values
     are trades.json's; a lot-count mismatch is refused.
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

def write_window(folder: Path, rows, trades):
    """rows: (regime, total_portfolio_value, previous_allocation, postRebalance_current_allocation),
    one per hourly bar from 2020-01-01 00:00; trades: list of trade dicts (or None: no file)."""
    folder.mkdir(parents=True, exist_ok=True)
    lines = [BARS_HDR]
    for i, (regime, tpv, prev, post) in enumerate(rows):
        lines.append(f"2020-01-01 {i:02d}:00:00,{regime},{tpv},{prev},{post}")
    (folder / "bars.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if trades is not None:
        (folder / "trades.json").write_text(json.dumps(trades), encoding="utf-8")


def lot(gross, fees, net, minutes):
    return {"profit_loss_absolute": gross, "total_commission": fees,
            "net_profit_loss_absolute": net, "duration_minutes": minutes}


# W1: V0 = 1000 (the first row, a NOT_READY one). Ready rows 1..7:
#   post 0.5 0.5 0 -0.4 0 0.3 0.3   prev 0 0.5 0.5 0 -0.4 0 0.3
#   turnover .5+0+.5+.4+.4+.3+0 = 2.1 ; signs + + (0) - (0) + + -> 2 flips
#   mean |a| = 2.0 / 7 ; max .5 ; lots 30/-10/20 gross, 1/.5/1.5 fees, 29/-10.5/18.5 net
#   -> gross 4.0, fees 0.3, net 3.7 (% of 1000) ; holding 2, 1, 5 bars (hourly) -> median 2
W1_ROWS = [("NOT_READY", 1000, 0, 0), ("trend", 1000, 0.0, 0.5), ("trend", 1010, 0.5, 0.5),
           ("trend", 1020, 0.5, 0.0), ("trend", 1020, 0.0, -0.4), ("trend", 1030, -0.4, 0.0),
           ("trend", 1030, 0.0, 0.3), ("trend", 1040, 0.3, 0.3)]
W1_TRADES = [lot(30.0, 1.0, 29.0, 120.0), lot(-10.0, 0.5, -10.5, 60.0), lot(20.0, 1.5, 18.5, 300.0)]
# W2: V0 = 2000. Ready rows 0..3 (a padded lower-case not_ready row 4 with |alloc| 0.9 is out):
#   post -.2 -.2 0 .4   prev 0 -.2 -.2 0 -> turnover .2+0+.2+.4 = .8 ; signs - - (0) + -> 1 flip
#   mean |a| = .8/4 = .2 ; max .4 ; lots 40+... gross -20+60 = 40 -> 2.0, fees 2+4 -> .3, net 34 -> 1.7
#   holding 1, 3 bars
W2_ROWS = [("trend", 2000, 0.0, -0.2), ("trend", 2000, -0.2, -0.2), ("trend", 2010, -0.2, 0.0),
           ("trend", 2010, 0.0, 0.4), (" not_ready ", 2020, 0.9, 0.9)]
W2_TRADES = [lot(-20.0, 2.0, -22.0, 60.0), lot(60.0, 4.0, 56.0, 180.0)]


@pytest.fixture()
def wins(tmp_path):
    write_window(tmp_path / "a", W1_ROWS, W1_TRADES)
    write_window(tmp_path / "b", W2_ROWS, W2_TRADES)
    return [("AAA", "w0", tmp_path / "a"), ("BBB", "w1", tmp_path / "b")]


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
    assert a == {"n_bars": 7, "trades": 3, "turnover": approx(2.1), "direction_changes": 2,
                 "mean_abs_allocation": approx(2.0 / 7), "max_abs_allocation": 0.5,
                 "gross_pct": approx(4.0), "fees_pct": approx(0.3), "net_pct": approx(3.7),
                 "cost_drag_pct": approx(7.5), "median_holding_bars": 2.0}
    assert b == {"n_bars": 4, "trades": 2, "turnover": approx(0.8), "direction_changes": 1,
                 "mean_abs_allocation": approx(0.2), "max_abs_allocation": 0.4,
                 "gross_pct": approx(2.0), "fees_pct": approx(0.3), "net_pct": approx(1.7),
                 "cost_drag_pct": approx(15.0), "median_holding_bars": 2.0}
    # total: counts, turnover and the *_pct summed (each window its own account), bars pooled,
    # cost drag from the summed *_pct, holding over the 5 lots pooled (2,1,5,1,3 -> 2)
    assert tot == {"n_bars": 11, "trades": 5, "turnover": approx(2.9), "direction_changes": 3,
                   "mean_abs_allocation": approx(2.8 / 11), "max_abs_allocation": 0.5,
                   "gross_pct": approx(6.0), "fees_pct": approx(0.6), "net_pct": approx(5.4),
                   "cost_drag_pct": approx(10.0), "median_holding_bars": 2.0}


def test_net_is_gross_minus_fees_in_dollars_not_a_sum_of_lot_percents(wins):
    c = we.window_economics(wins)["windows"]["AAA/w0"]
    assert c["net_pct"] == approx(c["gross_pct"] - c["fees_pct"])
    # the basis is the window's starting account (1000), whatever the lots' own sizes
    assert c["gross_pct"] == approx(100 * sum(t["profit_loss_absolute"] for t in W1_TRADES) / 1000)


def test_turnover_is_the_function_the_run_artifact_uses(wins):
    from performance.bar_equity import turnover
    df = pd.read_csv(wins[0][2] / "bars.csv")
    df = df[df["regime"] != "NOT_READY"]
    got = we.window_economics(wins[:1])["windows"]["AAA/w0"]["turnover"]
    assert got == approx(turnover(df["postRebalance_current_allocation"], df["previous_allocation"]))


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
        cell = we.window_economics([("X", name, tmp_path / name)])["windows"][f"X/{name}"]
        assert cell["direction_changes"] == want, name


def test_not_ready_rows_are_excluded_from_every_bar_field(wins):
    # W2's row 4 (" not_ready ", |alloc| 0.9) would give max 0.9, 5 bars, turnover +0.0
    b = we.window_economics(wins)["windows"]["BBB/w1"]
    assert b["n_bars"] == 4 and b["max_abs_allocation"] == 0.4
    # ... and W1's NOT_READY first row still supplies V0 (the account at the window's start)
    assert we.window_economics(wins[:1])["windows"]["AAA/w0"]["gross_pct"] == approx(4.0)


def test_a_window_without_lots_has_no_cost_drag_and_no_holding(tmp_path):
    write_window(tmp_path / "e", W2_ROWS, [])
    c = we.window_economics([("X", "w", tmp_path / "e")])["windows"]["X/w"]
    assert (c["trades"], c["gross_pct"], c["fees_pct"], c["net_pct"]) == (0, 0.0, 0.0, 0.0)
    assert c["cost_drag_pct"] is None and c["median_holding_bars"] is None
    assert c["n_bars"] == 4 and c["turnover"] == approx(0.8)


def test_zero_gross_gives_no_cost_drag_but_keeps_the_rest(tmp_path):
    write_window(tmp_path / "z", W2_ROWS, [lot(10.0, 1.0, 9.0, 60.0), lot(-10.0, 1.0, -11.0, 120.0)])
    c = we.window_economics([("X", "w", tmp_path / "z")])["windows"]["X/w"]
    assert c["gross_pct"] == 0.0 and c["cost_drag_pct"] is None
    assert c["fees_pct"] == approx(0.1) and c["net_pct"] == approx(-0.1)
    assert c["median_holding_bars"] == 1.5


def test_the_step_is_the_median_bar_spacing_not_a_fixed_hour(tmp_path):
    f = tmp_path / "d"
    f.mkdir()
    # a daily window: 1440 minutes is one bar
    (f / "bars.csv").write_text(BARS_HDR + "\n" + "\n".join(
        f"2020-01-0{d} 00:00:00,trend,1000,0,0.1" for d in range(1, 5)) + "\n", encoding="utf-8")
    (f / "trades.json").write_text(json.dumps([lot(1.0, 0.1, 0.9, 2880.0)]), encoding="utf-8")
    assert we.window_economics([("X", "d", f)])["windows"]["X/d"]["median_holding_bars"] == 2.0


def test_the_inputs_are_not_modified_and_the_result_is_deterministic(wins):
    before = [(p / "bars.csv").read_bytes() + (p / "trades.json").read_bytes()
              for _s, _w, p in wins]
    a, b = we.window_economics(wins), we.window_economics(copy.deepcopy(wins))
    assert a == b
    assert before == [(p / "bars.csv").read_bytes() + (p / "trades.json").read_bytes()
                      for _s, _w, p in wins]


def test_a_duplicate_label_raises(wins):
    with pytest.raises(ValueError, match="given twice"):
        we.window_economics([wins[0], ("AAA", "w0", wins[1][2])])


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
        we.window_economics([("X", "w", f)])


@pytest.mark.parametrize("bad", ["x", None, True, float("nan")])
def test_a_non_numeric_trade_field_raises(tmp_path, bad):
    t = lot(1.0, 0.1, 0.9, 60.0)
    t["total_commission"] = bad
    write_window(tmp_path / "t", W2_ROWS, [t])
    # NaN is written by json.dumps as NaN and read back as a float nan
    with pytest.raises(ValueError, match="no numeric total_commission"):
        we.window_economics([("X", "w", tmp_path / "t")])


def test_a_trade_row_that_is_not_a_mapping_raises(tmp_path):
    write_window(tmp_path / "t", W2_ROWS, [[1, 2]])
    with pytest.raises(ValueError, match="not a mapping"):
        we.window_economics([("X", "w", tmp_path / "t")])


def test_missing_files_and_degenerate_windows_raise(tmp_path):
    write_window(tmp_path / "nt", W2_ROWS, None)
    with pytest.raises(OSError):
        we.window_economics([("X", "w", tmp_path / "nt")])
    with pytest.raises(OSError):
        we.window_economics([("X", "w", tmp_path / "nowhere")])
    write_window(tmp_path / "one", W2_ROWS[:1], [])
    with pytest.raises(ValueError, match="fewer than 2 bars"):
        we.window_economics([("X", "w", tmp_path / "one")])
    write_window(tmp_path / "v0", [("trend", 0, 0.0, 0.1)] * 3, [])
    with pytest.raises(ValueError, match="not positive"):
        we.window_economics([("X", "w", tmp_path / "v0")])
    write_window(tmp_path / "nan", [("trend", 1000, 0.0, "")] * 3, [])
    with pytest.raises(ValueError, match="NaN allocation"):
        we.window_economics([("X", "w", tmp_path / "nan")])


# ---------------------------------------------------------------------------
# a saved-run-shaped fixture (tests/test_e075_pr4_queries.make_run) with the economics fields
# ---------------------------------------------------------------------------

def enrich(run):
    """Add the trades.json fields the economics read, hand-made per lot k = 0..7:
    gross $ 10(k+1), fee $1, net $10(k+1)-1, duration HOLDS[k] bars of an hour,
    profit_loss_percent (k+1)-4, total_commission_percent 0.1+0.01k."""
    for p in sorted(Path(run).glob("variants/base/results/*/trades.json")):
        trades = json.loads(p.read_text(encoding="utf-8"))
        for k, t in enumerate(trades):
            t.update(profit_loss_absolute=10.0 * (k + 1), total_commission=1.0,
                     net_profit_loss_absolute=10.0 * (k + 1) - 1.0,
                     duration_minutes=HOLDS[k] * 60.0,
                     profit_loss_percent=float(k + 1) - 4.0,
                     total_commission_percent=0.1 + 0.01 * k)
        p.write_text(json.dumps(trades), encoding="utf-8")


@pytest.fixture()
def run(tmp_path):
    root = make_run(tmp_path / "run_001")
    enrich(root)
    return root


def _window_dirs(run):
    return [(s, w, Path(run) / "variants" / "base" / "results" / rid)
            for rid, s, w, _o, _sd in pr4.WINDOWS]


# ---------------------------------------------------------------------------
# 2. the query
# ---------------------------------------------------------------------------

def test_the_query_returns_the_hand_numbers_of_the_saved_run(run):
    res = engine(run).window_economics()
    assert res["status"] == "ok"
    out = res["result"]
    assert list(out["windows"]) == ["AAA/w0", "AAA/w1", "BBB/w0"]
    for cell in out["windows"].values():
        # 8 lots; V0 = 1000 (the first row); gross 10*(1..8) = 360, fees 8, net 352
        assert cell["trades"] == 8 and cell["n_bars"] == N
        assert cell["gross_pct"] == approx(36.0) and cell["fees_pct"] == approx(0.8)
        assert cell["net_pct"] == approx(35.2)
        assert cell["cost_drag_pct"] == approx(0.8 / 36.0 * 100)
        assert cell["median_holding_bars"] == 4.5        # 2 3 3 4 5 5 7 9
        # the exits alternate +0.3 / -0.3 over 8 lots: 7 flips, mean |a| = 8 * 0.3 / N
        assert cell["direction_changes"] == 7 and cell["max_abs_allocation"] == 0.3
        assert cell["mean_abs_allocation"] == approx(8 * 0.3 / N)
    # turnover: independent numpy over the file's own two columns
    for (sym, win, folder) in _window_dirs(run):
        df = pd.read_csv(folder / "bars.csv")
        want = float(np.abs(df["postRebalance_current_allocation"].to_numpy()
                            - df["previous_allocation"].to_numpy()).sum())
        assert out["windows"][f"{sym}/{win}"]["turnover"] == approx(want)
    t = out["total"]
    assert t["trades"] == 24 and t["n_bars"] == 3 * N and t["direction_changes"] == 21
    assert t["gross_pct"] == approx(108.0) and t["net_pct"] == approx(105.6)
    assert t["median_holding_bars"] == 4.5


def test_the_query_is_the_module_function_over_the_same_folders(run):
    got = engine(run).window_economics()["result"]
    want = json.loads(json.dumps(we.window_economics(_window_dirs(run))))
    assert got == want


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


def test_twelve_cells_are_not_over_the_cell_cap(tmp_path, monkeypatch):
    wins = [(f"rw{i}", f"S{i}", "w0", 0, 40 + i) for i in range(12)]
    monkeypatch.setattr(pr4, "WINDOWS", wins)
    root = make_run(tmp_path / "run_12")
    enrich(root)
    res = engine(root).window_economics()
    # 12 cells and the total fit the cell cap and the 4000-character cap (about 3000 here)
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
    root = make_run(tmp_path / "raw")                 # trades.json without the dollar fields
    eng = engine(root)
    res = eng.window_economics()
    assert res["status"] == "refused" and "economics cannot be read" in res["reason"]
    assert "profit_loss_absolute" in res["reason"]
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


def test_trade_gross_return_values_are_trades_json_and_count_as_comparisons(run):
    eng = engine(run)
    res = eng.trade_slice([], [{"field": "trade_gross_return", "stat": "mean"},
                               {"field": "trade_gross_return", "stat": "share_positive"},
                               {"field": "trade_gross_return", "stat": "median"}])
    assert res["status"] == "ok"
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
    res = eng.trade_slice([], [{"field": "trade_gross_return", "stat": "mean"}])
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
    for i, (_s, _w, folder) in enumerate(folders):
        df = pd.read_csv(folder / "bars.csv")
        assert np.allclose(np.asarray(fa[i], dtype=float), np.abs(df["forecast"].to_numpy()),
                           rtol=1e-12, atol=0)
        assert np.allclose(np.asarray(aa[i], dtype=float),
                           np.abs(df["postRebalance_current_allocation"].to_numpy()),
                           rtol=1e-12, atol=0)
    assert (np.asarray(aa[0]) == 0.3).sum() == 8              # the eight exit bars
    g = eng.describe("abs_forecast")["result"]["groups"]["all"]
    allf = np.concatenate([np.abs(pd.read_csv(f / "bars.csv")["forecast"].to_numpy())
                           for _s, _w, f in folders])
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
    for _s, _w, folder in _window_dirs(run):
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
    write_window(folder, rows, [lot(20.0 + k, 2.0, 18.0 + k, 120.0), lot(-5.0, 1.0, -6.0, 60.0)])


@pytest.fixture()
def stub_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _graded_run():
    tpb._set_orchestrator({**tpb.FULL_ON, **tpb.VARIANT_LOOP_ON})
    tpb._write_bars()
    run_dir = tpb._variant_run({"base": False, "design": True})
    k = 0
    for vid in ("base", "design"):
        for sym in ("BTCUSDT", "ETHUSDT"):
            for w in ("w1", "w2"):
                _bars_for(_window_folder(run_dir, vid, sym, w), k)
                k += 1
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
    assert c["median_holding_bars"] == 1.5
    for vid in ("asset", "broken"):                  # no protocol_result: the key is None
        assert on["variants"][vid]["result"] == "NOT_TESTED"
        assert on["variants"][vid]["window_economics"] is None


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
    for _s, _w, folder in _window_dirs(run):
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
