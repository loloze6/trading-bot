"""
D-150 -- Branch 3 records each variant's forecast shape (information only, never a
bar, never a gate, no flag). `_evaluate_profit_bars_every_backtest` adds a per-variant
key `forecast_shape` beside `bars`: {abs_mean_forecast, share_at_cap,
abs_mean_allocation, n_bars, n_windows}, read from the bars.csv of exactly the windows
graded. Synthetic runs only (no real run directory, no market data).
"""
import json
import sys
from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.usefixtures("reader_docs")

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).parent / "fixtures" / "profit_bars_golden"))

import run_phase1_research as rpr  # noqa: E402
import campaign_memory as cm  # noqa: E402
import test_profit_bars_every_backtest as tpb  # noqa: E402
from test_profit_bars_every_backtest import RUN_ID  # noqa: E402

_HDR = "timestamp,regime,forecast,postRebalance_current_allocation,postRebalance_total_value\n"
# Window label w1: forecasts +20, -20, 19.5, nan; allocations 0.5, -0.5, 0.25, (blank)
_W1 = [("20", "0.5"), ("-20", "-0.5"), ("19.5", "0.25"), ("nan", "")]
# Window label w2: forecasts 0, 10; allocations 1.0, -1.0
_W2 = [("0", "1.0"), ("10", "-1.0")]


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _write_bars_csv(folder: Path, rows) -> None:
    lines = [_HDR.rstrip("\n")]
    for i, (f, a) in enumerate(rows):
        regime = "NOT_READY" if i == 0 else "trend"   # warm-up rows ARE read (no drop)
        lines.append(f"2020-01-0{i + 1} 00:00:00,{regime},{f},{a},1000.0")
    (folder / "bars.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _setup(monkeypatch=None):
    tpb._set_orchestrator({**tpb.FULL_ON, **tpb.VARIANT_LOOP_ON})
    tpb._write_bars()
    run_dir = tpb._variant_run({"base": False, "design": True})
    for vid in ("base", "design"):
        root = run_dir / "variants" / vid / "results"
        for sym in ("BTCUSDT", "ETHUSDT"):
            _write_bars_csv(root / f"{vid}-{sym}-w1", _W1)
            _write_bars_csv(root / f"{vid}-{sym}-w2", _W2)
    return run_dir


def _evaluate(run_dir):
    return rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)


def _strip(ev):
    d = json.loads(json.dumps(ev, default=str))
    d.pop("generated_at")
    for v in d["variants"].values():
        v.pop("forecast_shape")        # the key itself is the only thing allowed to differ
    return d


def test_forecast_shape_hand_computed_over_the_graded_windows():
    run_dir = _setup()
    fs = _evaluate(run_dir)["variants"]["design"]["forecast_shape"]
    # |forecast| finite: w1 {20, 20, 19.5} x2 coins, w2 {0, 10} x2 coins -> sum 139 over 10
    # at the cap (>= 20 - 1e-9): the four 20s of 10 finite values
    # |allocation| finite: w1 {0.5, 0.5, 0.25} x2, w2 {1, 1} x2 -> sum 6.5 over 10
    assert fs == {"abs_mean_forecast": 13.9, "share_at_cap": 0.4, "abs_mean_allocation": 0.65,
                  "n_bars": 12, "n_windows": 4}


def test_a_stale_results_folder_not_in_protocol_result_is_ignored():
    run_dir = _setup()
    stale = run_dir / "variants" / "design" / "results" / "design-BTCUSDT-w1-OLD"
    stale.mkdir(parents=True)
    (stale / "portfolio_states.csv").write_text("timestamp,regime\n", encoding="utf-8")
    _write_bars_csv(stale, [("20", "9.0")] * 50)
    fs = _evaluate(run_dir)["variants"]["design"]["forecast_shape"]
    assert fs["n_bars"] == 12 and fs["n_windows"] == 4 and fs["abs_mean_forecast"] == 13.9


def test_missing_bars_csv_gives_none_and_grading_is_byte_identical(monkeypatch):
    run_dir = _setup()
    (run_dir / "variants" / "design" / "results" / "design-ETHUSDT-w2" / "bars.csv").unlink()
    ev = _evaluate(run_dir)
    assert ev["variants"]["design"]["forecast_shape"] is None
    assert ev["variants"]["base"]["forecast_shape"] is not None   # the other variant is unaffected
    monkeypatch.setattr(rpr, "_variant_forecast_shape", lambda run_dir, pr: None)
    ev_none = _evaluate(run_dir)
    assert _strip(ev) == _strip(ev_none)


@pytest.mark.parametrize("bad", ["columns", "unreadable_value"])
def test_unreadable_bars_csv_gives_none(bad):
    run_dir = _setup()
    p = run_dir / "variants" / "design" / "results" / "design-BTCUSDT-w1" / "bars.csv"
    if bad == "columns":
        p.write_text("timestamp,regime,forecast\n2020-01-01,trend,1.0\n", encoding="utf-8")
    else:
        p.write_text(_HDR + "2020-01-01 00:00:00,trend,abc,0.1,1.0\n", encoding="utf-8")
    ev = _evaluate(run_dir)
    assert ev["variants"]["design"]["forecast_shape"] is None
    assert ev["variants"]["design"]["result"] == "PASS"


def test_no_results_gives_none():
    assert rpr._variant_forecast_shape(Path("nowhere"), {"results": []}) is None
    assert rpr._variant_forecast_shape(Path("nowhere"), {}) is None


@pytest.mark.parametrize("results", [["x"], [{"run_id": 123}], {"run_id": "w"}, [None]])
def test_a_malformed_results_entry_gives_none(results):
    assert rpr._variant_forecast_shape(Path("nowhere"), {"results": results}) is None


def test_key_sits_beside_bars_and_is_in_no_bar_row_and_no_reason():
    run_dir = _setup()
    ev = _evaluate(run_dir)
    for vid, v in ev["variants"].items():
        assert "forecast_shape" in v
        assert "forecast_shape" not in {b for row in v["bars"] for b in row}
        blob = json.dumps({"bars": v["bars"], "reasons": v["reasons"]}, default=str)
        assert "forecast_shape" not in blob and "abs_mean_forecast" not in blob
    for vid in ("asset", "broken"):          # no protocol_result: the key is present and None
        assert ev["variants"][vid]["result"] == "NOT_TESTED"
        assert ev["variants"][vid]["forecast_shape"] is None
    assert ev["variants"]["design"]["forecast_shape"] is not None
    on_disk = yaml.safe_load((run_dir / "artifacts" / "profit_bars_evaluation.yaml")
                             .read_text(encoding="utf-8"))
    assert on_disk["variants"]["design"]["forecast_shape"] == ev["variants"]["design"]["forecast_shape"]


def test_result_and_passing_equal_a_run_with_the_helper_returning_none(monkeypatch):
    run_dir = _setup()
    ev = _evaluate(run_dir)
    monkeypatch.setattr(rpr, "_variant_forecast_shape", lambda run_dir, pr: None)
    ev_none = _evaluate(run_dir)
    assert ev["result"] == ev_none["result"] == "PASS" and ev["passing"] == ev_none["passing"]
    for vid in ev["variants"]:
        a, b = dict(ev["variants"][vid]), dict(ev_none["variants"][vid])
        a.pop("forecast_shape"), b.pop("forecast_shape")
        assert a == b


def test_campaign_memory_does_not_carry_forecast_shape_and_schema_is_unaffected():
    run_dir = _setup()
    _evaluate(run_dir)
    block = cm.profit_bars_block(run_dir, RUN_ID, {
        "base": {"status": "tested"}, "design": {"status": "tested"},
        "broken": {"status": "failed"}, "asset": {"status": "not_tested"}})
    for v in block["variants"].values():
        assert set(v) == {"result", "bars"}
    assert "forecast_shape" not in json.dumps(block)
