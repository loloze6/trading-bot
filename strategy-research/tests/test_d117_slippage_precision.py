"""D-117 (CUL-431's slippage rounding defect): trade_diagnostics' all-costs fields
(slippage_paid, cost_paid_all, gross_return_before_costs; written only under CUL-414's
--cost-bar-all-costs) read each leg's close at full precision from portfolio_states.csv,
not from bars.csv, which the engine writes rounded to 6 decimals. A declared change in
output only where rounding changed a close; byte-identical elsewhere.

The run_081 check reads run artifacts that are not in git: it runs where they exist
(D113_RUNS_ROOT, or this checkout) and skips elsewhere.
"""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import portfolio_daily as pdv1  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
import run_protocol as rp  # noqa: E402

SLIP = 7.5  # bps one way


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _fills(side, ref_in, ref_out):
    s = SLIP / 1e4
    return (ref_in * (1 + s), ref_out * (1 - s)) if side == "LONG" else (ref_in * (1 - s), ref_out * (1 + s))


def _write(run_dir: Path, closes, *, states=True):
    """bars.csv rounded to 6 decimals (as write_bars_csv does), portfolio_states.csv at full
    precision, and two trades filled at the full-precision closes."""
    run_dir.mkdir()
    ts = [f"2020-01-0{i + 1}" for i in range(len(closes))]
    with open(run_dir / "bars.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["timestamp", "open", "high", "low", "close"])
        w.writeheader()
        for t, c in zip(ts, closes):
            r = round(c, 6)
            w.writerow({"timestamp": t, "open": r, "high": r, "low": r, "close": r})
    if states:
        with open(run_dir / "portfolio_states.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["timestamp", "regime", "close"])
            w.writeheader()
            for t, c in zip(ts, closes):
                w.writerow({"timestamp": t, "regime": "trend", "close": repr(c)})
    trades = []
    for tid, side, i_in, i_out in (("t1", "LONG", 0, 2), ("t2", "SHORT", 3, 4)):
        e, x = _fills(side, closes[i_in], closes[i_out])
        trades.append({"trade_id": tid, "symbol": "DOGEUSD", "side": side, "entry_price": e,
                       "exit_price": x, "entry_time": f"{ts[i_in]}T00:00:00",
                       "exit_time": f"{ts[i_out]}T00:00:00", "duration_minutes": 1440.0,
                       "profit_loss_percent": 0.0, "net_portfolio_profit_loss_percent": 0.0,
                       "profitable_net": False, "exit_forecast": 0.0,
                       "total_commission_percent": 0.1})
    (run_dir / "trades.json").write_text(json.dumps(trades), encoding="utf-8")


CLOSES = [0.0612345678, 0.0623456789, 0.0634567891, 0.0645678912, 0.0656789123]
ARGS = ("DOGEUSD", "w1", "2020-01-05", None)


def test_slippage_paid_is_the_configured_slippage_at_full_precision(tmp_path):
    run_dir = tmp_path / "run"
    _write(run_dir, CLOSES)
    recs = rp._compute_trade_records_for_window(run_dir, *ARGS, commission_bps=5.0,
                                                cost_bar_all_costs=True)
    for r in recs:
        assert r["slippage_paid"] == pytest.approx(2 * SLIP, abs=1e-6)
        assert r["cost_paid_all"] == pytest.approx(r["cost_paid"] + 2 * SLIP, abs=1e-6)


def test_without_portfolio_states_the_rounded_closes_are_used_as_before(tmp_path):
    run_dir = tmp_path / "run"
    _write(run_dir, CLOSES, states=False)
    recs = rp._compute_trade_records_for_window(run_dir, *ARGS, commission_bps=5.0,
                                                cost_bar_all_costs=True)
    bars = rp._load_bars(run_dir)
    for r in recs:
        side = "LONG" if r["direction"] == "long" else "SHORT"
        assert r == {**r, **rp._all_costs_fields(side, r["entry_price"], r["exit_price"], bars,
                                                 r["entry_idx"], r["exit_idx"], r["cost_paid"])}
    # the rounding is visible on these prices: off by more than 1e-3 bps
    assert any(abs(r["slippage_paid"] - 2 * SLIP) > 1e-3 for r in recs)


def test_every_other_field_and_the_flag_off_records_are_unchanged(tmp_path):
    with_states, without = tmp_path / "a", tmp_path / "b"
    _write(with_states, CLOSES)
    _write(without, CLOSES, states=False)
    for flag in (False, True):
        a = rp._compute_trade_records_for_window(with_states, *ARGS, commission_bps=5.0,
                                                 cost_bar_all_costs=flag)
        b = rp._compute_trade_records_for_window(without, *ARGS, commission_bps=5.0,
                                                 cost_bar_all_costs=flag)
        drop = {"gross_return_before_costs", "slippage_paid", "cost_paid_all"}
        assert [{k: v for k, v in r.items() if k not in drop} for r in a] == \
            [{k: v for k, v in r.items() if k not in drop} for r in b]
        if not flag:
            assert json.dumps(a) == json.dumps(b)  # flag off: byte-identical


def test_prices_with_six_decimals_or_fewer_give_identical_records(tmp_path):
    closes = [43123.5, 43555.25, 44001.0, 43890.125, 43500.0]
    a, b = tmp_path / "a", tmp_path / "b"
    _write(a, closes)
    _write(b, closes, states=False)
    ra = rp._compute_trade_records_for_window(a, *ARGS, commission_bps=5.0, cost_bar_all_costs=True)
    rb = rp._compute_trade_records_for_window(b, *ARGS, commission_bps=5.0, cost_bar_all_costs=True)
    assert json.dumps(ra) == json.dumps(rb)


def test_full_precision_closes_reader(tmp_path):
    p = tmp_path / "portfolio_states.csv"
    p.write_text("timestamp,regime,close\n2020-01-01,trend,0.1231\n2020-01-01,trend,0.9999\n"
                 "2020-01-02,trend,\n2020-01-03,trend,-1\n2020-01-04,trend,0.5\n", encoding="utf-8")
    assert rp._full_precision_closes(tmp_path) == {"2020-01-01": 0.1231, "2020-01-04": 0.5}
    assert rp._full_precision_closes(tmp_path / "none") == {}


_RUNS_ROOT = Path(os.environ.get("D113_RUNS_ROOT") or SR_ROOT)
RUN_081 = _RUNS_ROOT / "runs" / "run_081"


@pytest.mark.skipif(not (RUN_081 / "trade_diagnostics.json").exists(),
                    reason="run_081's artifacts are not in this checkout (set D113_RUNS_ROOT)")
def test_run_081_slippage_is_now_exact_on_every_lot():
    """CUL-431 measured up to 0.107 bps of rounding error on run_081 (DOGE); with
    full-precision closes every lot's slippage_paid is the configured slippage, both legs."""
    pr = yaml.safe_load((RUN_081 / "artifacts" / "protocol_result.yaml").read_text(encoding="utf-8"))
    n = 0
    for r in pr["results"]:
        path = pdv1.find_window_equity_file(RUN_081, r["run_id"])
        cm = json.loads((path.parent / "manifest.json").read_text(encoding="utf-8"))["config"]["cost_model"]
        slip_bps = cm["slippage_bps"].get(r["symbol"], cm["slippage_bps"]["default"])
        recs = rp._compute_trade_records_for_window(path.parent, r["symbol"], r["window"],
                                                    "2023-12-31", None, commission_bps=5.0,
                                                    cost_bar_all_costs=True)
        for rec in recs:
            assert rec["slippage_paid"] == pytest.approx(2 * slip_bps, abs=1e-6), (r["symbol"], rec)
            n += 1
    assert n == 257


def test_bars_missing_from_portfolio_states_keep_the_rounded_close_and_warn(tmp_path, capsys):
    """Review of #407: a partial file is used where it has the bar, the bars.csv close
    elsewhere, and the fallback is said on stderr (never silent)."""
    run_dir = tmp_path / "run"
    _write(run_dir, CLOSES)
    rows = (run_dir / "portfolio_states.csv").read_text(encoding="utf-8").splitlines()
    (run_dir / "portfolio_states.csv").write_text("\n".join(r for r in rows if "2020-01-05" not in r)
                                                  + "\n", encoding="utf-8")
    recs = rp._compute_trade_records_for_window(run_dir, *ARGS, commission_bps=5.0,
                                                cost_bar_all_costs=True)
    err = capsys.readouterr().err
    assert "no close for 1 of 5" in err and "DOGEUSD w1" in err
    t1, t2 = recs                  # t1 legs (01, 03) are in the file; t2 exits on 05
    assert t1["slippage_paid"] == pytest.approx(2 * SLIP, abs=1e-6)
    bars = rp._load_bars(run_dir)
    assert t2["slippage_paid"] == rp._all_costs_fields(
        "SHORT", t2["entry_price"], t2["exit_price"],
        rp._bars_with_full_precision_closes(bars, rp._full_precision_closes(run_dir)),
        t2["entry_idx"], t2["exit_idx"], t2["cost_paid"])["slippage_paid"]
    assert abs(t2["slippage_paid"] - 2 * SLIP) > 1e-4  # the exit leg used the rounded close
