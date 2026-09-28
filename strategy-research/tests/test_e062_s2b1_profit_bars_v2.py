"""
E-062 S2b-1 -- profit bars v2: flag, definitions and values
(engineering/roadmap/E-062/S1_FINDINGS.md Q5/Q7/Q8 "Wiring", G1-G9/G11 and the
S2a amendments; D-034..D-039).

Covers:
  1. orchestrator.profit_bars_v2.enabled: strict bool (quoted "false" refused),
     dependency on profit_bars_every_backtest, run_loop's pre-flight and
     run_campaign's launch pre-flight.
  2. The loader: the three v2 keys are required only under v2; an unquoted YAML
     date in ratified_at is accepted; the committed bars file loads both ways
     with the D-039 values and no signature.
  3. The seven v2 rows (name, basis, comparator), a full PASS, strict `>` at the
     boundary, and every NOT_EVALUABLE case of the wiring.
  4. bars_definitions: v2 in the evaluation; a spend refuses bars_changed when
     the evaluation's definitions differ from the flag now.
  5. Flag off: golden promote-path outputs unchanged with the flag written
     explicitly false, and the per-backtest evaluation identical with the flag
     absent or false.
"""
import json
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).parent / "fixtures" / "profit_bars_golden"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as rc  # noqa: E402
import golden_harness  # noqa: E402

from test_e058_s2a_regroup_record import (  # noqa: E402
    ALL_ON, RUN_ID, _seed, _set_orchestrator, _minimal_run_at)
from test_profit_bars_every_backtest import _seed_dsr_ledger  # noqa: E402

PB = {"profit_bars_file": {"enabled": True}, "profit_bars_every_backtest": {"enabled": True}}
FULL_ON = {**ALL_ON, **PB}
V2_ON = {**FULL_ON, "profit_bars_v2": {"enabled": True}}
GOLDEN_DIR = Path(__file__).parent / "fixtures" / "profit_bars_golden"

V1_BARS = {"sharpe_min": 1.0, "max_drawdown_pct_max": 20.0, "avg_daily_return_min": 0.0005,
           "trade_count_min": 100, "deflated_sharpe_threshold": 0.95,
           "target_instrument_set": ["BTCUSDT", "ETHUSDT"],
           "ratified_by": None, "ratified_at": None}
V2_KEYS = {"buy_and_hold_excess_return_min": 0.0, "cost_edge_ratio_min": 2.2,
           "cost_edge_min_trades": 100}
V2_BARS = {**V1_BARS, **V2_KEYS}

ROW_ORDER = ["sharpe_min", "deflated_sharpe_threshold", "max_drawdown_pct_max",
             "trade_count_min", "avg_daily_return_min", "buy_and_hold_excess_return_min",
             "cost_edge_ratio_min"]
EXPECTED_BASIS = {
    "sharpe_min": "portfolio_equal_weight_whole_test_chained_daily_sharpe",
    "deflated_sharpe_threshold": "deflated_sharpe_on_campaign_trial_ledger",
    "max_drawdown_pct_max": "portfolio_equal_weight_whole_test_chained",
    "trade_count_min": "per_coin_total_whole_test_excl_window_closes",
    "avg_daily_return_min": "portfolio_equal_weight_whole_test_chained_mean_daily_return",
    "buy_and_hold_excess_return_min": "portfolio_equal_weight_vs_buy_and_hold",
    "cost_edge_ratio_min": "pooled_trades_realized_edge_to_cost",
}
EXPECTED_COMPARATOR = {"sharpe_min": ">=", "deflated_sharpe_threshold": ">=",
                       "max_drawdown_pct_max": "<=", "trade_count_min": ">=",
                       "avg_daily_return_min": ">=", "buy_and_hold_excess_return_min": ">",
                       "cost_edge_ratio_min": ">"}
CHAIN_ROWS = ("max_drawdown_pct_max", "avg_daily_return_min", "sharpe_min",
              "buy_and_hold_excess_return_min")

W1 = ("w1", date(2020, 1, 1), date(2020, 2, 1))
W2 = ("w2", date(2020, 2, 1), date(2020, 3, 1))
SLIPPAGE = {"default": 1.5, "BTCUSDT": 1, "ETHUSDT": 1.5}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# Fixture builders
# ---------------------------------------------------------------------------

def _write_bars(doc: dict) -> Path:
    path = rpr.ROOT / "config" / "profitability_bars.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc), encoding="utf-8")
    return path


def _write_cost_model(fee: float = 7.5) -> None:
    path = rpr.ROOT / "config" / "cost_model.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump({"fee_rate_bps": {"default": fee}}), encoding="utf-8")


def _write_protocol(windows, name: str) -> Path:
    path = rpr.ROOT / "protocols" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"windows": [
        {"label": lab, "test": {"start": s.isoformat(), "end": e.isoformat()}}
        for lab, s, e in windows]}), encoding="utf-8")
    return path


def _default_strat(_label, k):
    return 0.002 + 0.001 * (-1) ** k


def _write_window(out_dir: Path, wid: str, first: date, last: date, *, label, strat, price,
                  manifest: bool = True) -> None:
    """portfolio_states.csv (a NOT_READY warm-up row, then an 11:00 bar at the
    previous close and a 23:00 close per day) and manifest.json for one window."""
    d = out_dir / "results" / wid
    d.mkdir(parents=True, exist_ok=True)
    lines = ["timestamp,regime,postRebalance_total_value,close",
             f"{first - timedelta(days=1)} 23:00:00,NOT_READY,999999.0,1.0"]
    eq, px = 10000.0, 100.0
    for k in range((last - first).days + 1):
        day = first + timedelta(days=k)
        lines.append(f"{day} 11:00:00,trend,{eq},{px}")
        if k > 0:
            eq *= 1.0 + strat(label, k)
            px *= 1.0 + price
        lines.append(f"{day} 23:00:00,trend,{eq},{px}")
    (d / "portfolio_states.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if manifest:
        (d / "manifest.json").write_text(json.dumps(
            {"config": {"cost_model": {"slippage_bps": SLIPPAGE}}}), encoding="utf-8")


def _trade(sym, win, reason, rr, cost):
    return {"symbol": sym, "window": win, "exit_reason": reason, "realized_return": rr,
            "cost_paid": cost}


def _build(out_dir: Path, *, coins=("BTCUSDT",), windows=(W1, W2), strat=_default_strat,
           price=-0.001, n_signal=59, n_eow=1, rr=0.45, cost=15.0, trades_file=True,
           protocol=True, protocol_windows=None, tail=1, manifest=True, n_per_coin=None) -> dict:
    """A protocol_result whose windows, equity/close files, manifests, trade
    records and protocol JSON all exist. Defaults clear every v2 bar."""
    out_dir.mkdir(parents=True, exist_ok=True)
    results, trades = [], []
    for sym in coins:
        ns = (n_per_coin or {}).get(sym, n_signal)
        for lab, s, e in windows:
            wid = f"{out_dir.name}-{sym}-{lab}"
            _write_window(out_dir, wid, s, e - timedelta(days=tail), label=lab, strat=strat,
                          price=price, manifest=manifest)
            results.append({"symbol": sym, "window": lab, "run_id": wid,
                            "core": {"trade_count": ns + n_eow, "sharpe": 1.0}})
            trades += [_trade(sym, lab, "signal_flip", rr, cost) for _ in range(ns)]
            trades += [_trade(sym, lab, "end_of_window", rr, cost) for _ in range(n_eow)]
    if trades_file and trades:
        (out_dir / "trade_diagnostics.json").write_text(
            json.dumps({"trades": trades, "summary": {}}), encoding="utf-8")
    pr = {"results": results,
          "per_symbol_summary": {s: {"median_sharpe": 1.5, "max_abs_drawdown_pct": 1.0,
                                     "min_trade_count": n_signal + n_eow} for s in coins}}
    if protocol:
        pr["protocol_file"] = str(_write_protocol(protocol_windows or windows,
                                                  f"{out_dir.name}_protocol.json"))
    return pr


def _metrics(pr, run_dir, bars=V2_BARS):
    _write_cost_model()
    return rpr._whole_test_profit_metrics(run_dir, pr, bars)


def _rows(pr, run_dir, dsr=0.99, bars=V2_BARS):
    results, overall, reasons = rpr._grade_profit_bars_v2(
        bars, dsr=dsr, dsr_note="test", metrics=_metrics(pr, run_dir, bars))
    return {r["name"]: r for r in results}, overall, reasons, results


def _v2_run(**build) -> Path:
    """A graded single run (variant loop off) whose protocol_result is _build's."""
    _set_orchestrator(V2_ON)
    _write_bars(V2_BARS)
    _write_cost_model()
    run_dir = _seed()
    pr = _build(run_dir, **build)
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", pr)
    _seed_dsr_ledger()
    return run_dir


def _pbe(run_dir: Path) -> dict:
    return yaml.safe_load((run_dir / "artifacts" / "profit_bars_evaluation.yaml")
                          .read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1. The flag
# ---------------------------------------------------------------------------

def test_flag_false_when_absent_or_off():
    _set_orchestrator(None)
    assert rpr._profit_bars_v2_enabled() is False
    _set_orchestrator(FULL_ON)
    assert rpr._profit_bars_v2_enabled() is False
    _set_orchestrator({**FULL_ON, "profit_bars_v2": {}})
    assert rpr._profit_bars_v2_enabled() is False
    _set_orchestrator({**FULL_ON, "profit_bars_v2": {"enabled": False}})
    assert rpr._profit_bars_v2_enabled() is False


def test_flag_true_with_its_dependency():
    _set_orchestrator(V2_ON)
    assert rpr._profit_bars_v2_enabled() is True


@pytest.mark.parametrize("bad", ["false", "true", None, 0, 1])
def test_flag_non_bool_is_refused(bad):
    _set_orchestrator({**FULL_ON, "profit_bars_v2": {"enabled": bad}})
    with pytest.raises(ValueError, match=r"orchestrator\.profit_bars_v2\.enabled=.* is not a "
                                         r"real boolean"):
        rpr._profit_bars_v2_enabled()
    refusal = rc._flag_preflight_refusal()
    assert refusal and f"orchestrator.profit_bars_v2.enabled={bad!r}" in refusal


def test_flag_on_without_profit_bars_every_backtest_raises():
    _set_orchestrator({**ALL_ON, "profit_bars_file": {"enabled": True},
                       "profit_bars_v2": {"enabled": True}})
    with pytest.raises(ValueError, match="requires orchestrator.profit_bars_every_backtest"):
        rpr._profit_bars_v2_enabled()
    assert "profit_bars_v2.enabled=true requires" in rc._flag_preflight_refusal()


def test_launch_preflight_reads_the_flag_on_a_consistent_set():
    _set_orchestrator(V2_ON)
    values, refusal = rc._flag_preflight()
    assert refusal is None and values["profit_bars_v2"] is True


def test_run_loop_preflight_fails_before_any_spend(monkeypatch):
    _set_orchestrator({"profit_bars_v2": {"enabled": True}})
    run_dir = _minimal_run_at(rpr.ROOT, RUN_ID, "protocol_execution")
    _seed(pending="protocol_execution")
    invoked = []

    async def _record(stage_name, run_id, retry_context=None):
        invoked.append(stage_name)
    monkeypatch.setattr(rpr, "async_invoke_agent", _record)
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert invoked == []
    assert state["status"] == "failed"
    assert "profit_bars_v2.enabled=true requires" in state["last_error"]
    assert state["pending_stage"] == "protocol_execution"


# ---------------------------------------------------------------------------
# 2. The loader
# ---------------------------------------------------------------------------

def test_v1_loader_does_not_need_the_v2_keys():
    doc = rpr._load_profitability_bars(_write_bars(V1_BARS))
    assert doc == V1_BARS


@pytest.mark.parametrize("key", sorted(V2_KEYS))
def test_v2_loader_refuses_a_missing_v2_key(key):
    path = _write_bars({k: v for k, v in V2_BARS.items() if k != key})
    assert rpr._load_profitability_bars(path)  # v1: fine
    with pytest.raises(rpr.ProfitabilityBarsSchemaError, match=key):
        rpr._load_profitability_bars(path, v2=True)


@pytest.mark.parametrize("key,bad", [("cost_edge_min_trades", 2.5),
                                     ("cost_edge_min_trades", True),
                                     ("cost_edge_min_trades", 0),
                                     ("cost_edge_ratio_min", "2.2"),
                                     ("buy_and_hold_excess_return_min", None)])
def test_v2_loader_refuses_a_bad_v2_value(key, bad):
    path = _write_bars({**V2_BARS, key: bad})
    with pytest.raises(rpr.ProfitabilityBarsSchemaError, match=key):
        rpr._load_profitability_bars(path, v2=True)


@pytest.mark.parametrize("raw,iso", [("2025-12-15", "2025-12-15"),
                                     ("2025-12-15T10:30:00", "2025-12-15T10:30:00"),
                                     ("'2025-12-15'", "2025-12-15")])
def test_unquoted_yaml_date_in_ratified_at_is_accepted(raw, iso):
    path = rpr.ROOT / "config" / "profitability_bars.yaml"
    text = yaml.safe_dump({**V2_BARS, "ratified_by": "operator"}).replace(
        "ratified_at: null", f"ratified_at: {raw}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    for v2 in (False, True):
        assert rpr._load_profitability_bars(path, v2=v2)["ratified_at"] == iso


def test_committed_bars_file_has_the_d039_values_and_no_signature():
    real = SR_ROOT / "config" / "profitability_bars.yaml"
    for v2 in (False, True):
        doc = rpr._load_profitability_bars(real, v2=v2)
        assert {k: doc[k] for k in V2_BARS if k != "target_instrument_set"} == \
            {k: v for k, v in V2_BARS.items() if k != "target_instrument_set"}
    header = real.read_text(encoding="utf-8")
    for basis in EXPECTED_BASIS.values():
        assert f"basis: {basis}\n" in header, basis
    assert "NOT RATIFIED" not in header and "PLACEHOLDER" not in header


def test_committed_menu_has_the_d039_values():
    menu = yaml.safe_load((SR_ROOT / "config" / "criterion_menu.yaml").read_text(encoding="utf-8"))
    cost = next(c for c in menu["criteria"] if c["id"] == "realized_edge_to_cost_ratio")
    assert (cost["comparator"], cost["threshold"], cost["floor"]["min_trades"]) == (">", 2.2, 100)
    ric = next(c for c in menu["code_added_criteria"] if c["id"] == "residual_ic")
    assert (ric["threshold"], ric["max_p_value"], ric["floor"]["min_n_eff"], ric["ratified"]) \
        == (0.02, 0.05, 30, False)


# ---------------------------------------------------------------------------
# 3. The seven v2 rows
# ---------------------------------------------------------------------------

def test_full_pass_seven_rows_with_basis_and_comparator(tmp_path):
    run_dir = tmp_path / "run"
    pr = _build(run_dir)
    rows, overall, reasons, ordered = _rows(pr, run_dir)
    assert [r["name"] for r in ordered] == ROW_ORDER
    assert {n: r["basis"] for n, r in rows.items()} == EXPECTED_BASIS
    assert {n: r["comparator"] for n, r in rows.items()} == EXPECTED_COMPARATOR
    assert overall == "PASS" and reasons == [], reasons
    # hand-checked values
    rets = [_default_strat("w", k) for k in range(1, 31)] + \
        [_default_strat("w", k) for k in range(1, 29)]
    assert rows["avg_daily_return_min"]["actual"] == pytest.approx(sum(rets) / len(rets), abs=1e-12)
    assert rows["avg_daily_return_min"]["detail"]["n_daily_returns"] == 58
    assert rows["max_drawdown_pct_max"]["actual"] == pytest.approx(0.0, abs=1e-12)
    assert rows["trade_count_min"]["actual"] == 118
    assert rows["trade_count_min"]["detail"]["per_coin"]["BTCUSDT"] == {
        "raw": 120, "end_of_window": 2, "excluding_end_of_window": 118}
    assert rows["cost_edge_ratio_min"]["actual"] == pytest.approx(3.0, abs=1e-12)
    bh = rows["buy_and_hold_excess_return_min"]["detail"]
    assert bh["buy_and_hold_gross_return"] < 0 < bh["strategy_total_return"]
    assert rows["buy_and_hold_excess_return_min"]["actual"] == pytest.approx(
        bh["strategy_total_return"] - bh["buy_and_hold_total_return"], abs=1e-15)
    assert bh["cost_per_side_bps"] == {"BTCUSDT": 8.5}  # 7.5 fee + 1 bp slippage


def test_drawdown_spans_windows_on_the_whole_test(tmp_path):
    """A 12% fall at the end of w1 and another at the start of w2: each window
    alone stays under 20%, the whole test (D-034) does not."""
    def strat(label, k):
        if label == "w1" and k >= 25:
            return -(1 - 0.88 ** (1 / 6))
        if label == "w2" and k <= 6:
            return -(1 - 0.88 ** (1 / 6))
        return 0.004
    run_dir = tmp_path / "run"
    rows, overall, _r, _o = _rows(_build(run_dir, strat=strat), run_dir)
    assert rows["max_drawdown_pct_max"]["actual"] == pytest.approx(100 * (1 - 0.88 ** 2), abs=1e-6)
    assert rows["max_drawdown_pct_max"]["result"] == "FAIL" and overall == "FAIL"


@pytest.mark.parametrize("name,threshold,actual,result", [
    ("cost_edge_ratio_min", 2.2, 2.2, "FAIL"),
    ("cost_edge_ratio_min", 2.2, 2.2000001, "PASS"),
    ("buy_and_hold_excess_return_min", 0.0, 0.0, "FAIL"),
    ("buy_and_hold_excess_return_min", 0.0, 1e-9, "PASS"),
    ("sharpe_min", 1.0, 1.0, "PASS"),
    ("max_drawdown_pct_max", 20.0, 20.0, "PASS"),
])
def test_comparators_at_the_boundary(name, threshold, actual, result):
    metrics = {n: {"actual": 1.0, "note": "", "not_evaluable_reason": None, "detail": {}}
               for n in ROW_ORDER if n != "deflated_sharpe_threshold"}
    metrics[name] = {"actual": actual, "note": "", "not_evaluable_reason": None, "detail": {}}
    rows, _o, _r = rpr._grade_profit_bars_v2({**V2_BARS, name: threshold}, dsr=0.99,
                                             dsr_note="t", metrics=metrics)
    assert {r["name"]: r for r in rows}[name]["result"] == result


def test_cost_ratio_exactly_2_2_from_records_fails(tmp_path):
    run_dir = tmp_path / "run"
    rows, _o, _r, _x = _rows(_build(run_dir, rr=0.33), run_dir)
    assert rows["cost_edge_ratio_min"]["actual"] == 2.2
    assert rows["cost_edge_ratio_min"]["result"] == "FAIL"


def test_buy_and_hold_wins_in_a_bull_market_with_a_flat_strategy(tmp_path):
    run_dir = tmp_path / "run"
    rows, overall, _r, _o = _rows(_build(run_dir, strat=lambda _l, _k: 0.0, price=0.003),
                                  run_dir)
    assert rows["buy_and_hold_excess_return_min"]["result"] == "FAIL"
    assert rows["buy_and_hold_excess_return_min"]["actual"] < 0
    assert rows["sharpe_min"]["result"] == "NOT_EVALUABLE"  # zero stdev
    assert overall == "FAIL"


def test_always_long_forced_closes_do_not_count(tmp_path):
    run_dir = tmp_path / "run"
    rows, _o, _r, _x = _rows(_build(run_dir, n_signal=0, n_eow=1), run_dir)
    tc = rows["trade_count_min"]
    assert tc["actual"] == 0 and tc["result"] == "FAIL"
    assert tc["detail"]["per_coin"]["BTCUSDT"] == {"raw": 2, "end_of_window": 2,
                                                    "excluding_end_of_window": 0}
    assert rows["cost_edge_ratio_min"]["result"] == "NOT_EVALUABLE"


def test_worst_coin_decides_the_trade_count(tmp_path):
    run_dir = tmp_path / "run"
    pr = _build(run_dir, coins=("BTCUSDT", "ETHUSDT"), n_per_coin={"BTCUSDT": 59, "ETHUSDT": 40})
    rows, _o, _r, _x = _rows(pr, run_dir)
    assert rows["trade_count_min"]["actual"] == 80
    assert rows["trade_count_min"]["detail"]["worst_coin"] == "ETHUSDT"
    assert rows["trade_count_min"]["result"] == "FAIL"


def test_no_trade_anywhere_reads_zero_without_a_file(tmp_path):
    run_dir = tmp_path / "run"
    pr = _build(run_dir, n_signal=0, n_eow=0)
    assert not (run_dir / "trade_diagnostics.json").exists()
    rows, _o, _r, _x = _rows(pr, run_dir)
    assert rows["trade_count_min"]["actual"] == 0 and rows["trade_count_min"]["result"] == "FAIL"
    assert rows["cost_edge_ratio_min"]["result"] == "NOT_EVALUABLE"


def _assert_not_evaluable(row, needle):
    assert row["result"] == "NOT_EVALUABLE" and row["actual"] is None
    assert needle in row["not_evaluable_reason"], row["not_evaluable_reason"]


def test_trades_without_their_file_are_not_evaluable(tmp_path):
    run_dir = tmp_path / "run"
    rows, _o, reasons, _x = _rows(_build(run_dir, trades_file=False), run_dir)
    _assert_not_evaluable(rows["trade_count_min"], "no trade_diagnostics.json")
    _assert_not_evaluable(rows["cost_edge_ratio_min"], "no trade_diagnostics.json")
    assert any(r.startswith("trade_count_min: NOT_EVALUABLE") for r in reasons)


def test_records_that_disagree_with_core_trade_count_are_not_evaluable(tmp_path):
    run_dir = tmp_path / "run"
    pr = _build(run_dir)
    pr["results"][0]["core"]["trade_count"] += 1
    rows, _o, _r, _x = _rows(pr, run_dir)
    _assert_not_evaluable(rows["trade_count_min"], "do not match core.trade_count")
    _assert_not_evaluable(rows["cost_edge_ratio_min"], "do not match core.trade_count")


def test_cost_floor_below_min_trades_is_not_evaluable(tmp_path):
    run_dir = tmp_path / "run"
    rows, _o, _r, _x = _rows(_build(run_dir, n_signal=49), run_dir)  # 98 non-forced
    _assert_not_evaluable(rows["cost_edge_ratio_min"], "fewer than min_trades=100")
    assert rows["trade_count_min"]["result"] == "FAIL"


def test_missing_cost_on_a_record_is_not_evaluable(tmp_path):
    run_dir = tmp_path / "run"
    pr = _build(run_dir)
    path = run_dir / "trade_diagnostics.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["trades"][0]["cost_paid"] = None
    path.write_text(json.dumps(doc), encoding="utf-8")
    rows, _o, _r, _x = _rows(pr, run_dir)
    _assert_not_evaluable(rows["cost_edge_ratio_min"], "lack a measured cost")


def test_missing_protocol_file_makes_the_chain_rows_not_evaluable(tmp_path):
    run_dir = tmp_path / "run"
    rows, _o, _r, _x = _rows(_build(run_dir, protocol=False), run_dir)
    for name in CHAIN_ROWS:
        _assert_not_evaluable(rows[name], "no protocol_file")
    assert rows["trade_count_min"]["result"] == "PASS"
    assert rows["cost_edge_ratio_min"]["result"] == "PASS"


def test_protocol_windows_differing_from_results_are_not_evaluable(tmp_path):
    run_dir = tmp_path / "run"
    w3 = ("w3", date(2020, 3, 1), date(2020, 4, 1))
    rows, _o, _r, _x = _rows(_build(run_dir, protocol_windows=(W1, W2, w3)), run_dir)
    for name in CHAIN_ROWS:
        _assert_not_evaluable(rows[name], "are not the results' windows")


def test_too_few_daily_returns_makes_only_the_sharpe_not_evaluable(tmp_path):
    run_dir = tmp_path / "run"
    short = (("w1", date(2020, 1, 1), date(2020, 1, 11)), ("w2", date(2020, 1, 11), date(2020, 1, 21)))
    rows, _o, _r, _x = _rows(_build(run_dir, windows=short), run_dir)
    _assert_not_evaluable(rows["sharpe_min"], "fewer than SHARPE_MIN_DAILY_RETURNS=30")
    assert rows["avg_daily_return_min"]["result"] == "PASS"
    assert rows["max_drawdown_pct_max"]["result"] == "PASS"


def test_engine_tail_beyond_the_limit_is_not_evaluable(tmp_path):
    run_dir = tmp_path / "run"
    rows, _o, _r, _x = _rows(_build(run_dir, tail=7), run_dir)
    for name in CHAIN_ROWS:
        _assert_not_evaluable(rows[name], "max_engine_tail_days")


def test_missing_manifest_makes_only_buy_and_hold_not_evaluable(tmp_path):
    run_dir = tmp_path / "run"
    rows, _o, _r, _x = _rows(_build(run_dir, manifest=False), run_dir)
    _assert_not_evaluable(rows["buy_and_hold_excess_return_min"], "no manifest.json")
    assert rows["sharpe_min"]["result"] == "PASS"


def test_a_run_charged_another_fee_is_not_evaluable_for_buy_and_hold(tmp_path):
    run_dir = tmp_path / "run"
    rows, _o, _r, _x = _rows(_build(run_dir, cost=20.0, rr=0.6), run_dir)
    _assert_not_evaluable(rows["buy_and_hold_excess_return_min"], "charged another commission")


def test_missing_dsr_is_not_evaluable(tmp_path):
    run_dir = tmp_path / "run"
    rows, overall, _r, _x = _rows(_build(run_dir), run_dir, dsr=None)
    _assert_not_evaluable(rows["deflated_sharpe_threshold"], "no deflated Sharpe")
    assert overall == "FAIL"


def test_variant_out_dir_is_found_under_variants(tmp_path):
    run_dir = tmp_path / "run"
    pr = _build(run_dir / "variants" / "design")
    rows, overall, _r, _x = _rows(pr, run_dir)
    assert overall == "PASS"
    assert "source variants/design/trade_diagnostics.json" in rows["trade_count_min"]["note"]


# ---------------------------------------------------------------------------
# 4. bars_definitions and the spend check
# ---------------------------------------------------------------------------

def test_evaluation_records_bars_definitions_v2():
    run_dir = _v2_run()
    ev = rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID, record_bars_sha=True)
    assert ev == _pbe(run_dir)
    assert ev["bars_definitions"] == "v2"
    rows = ev["variants"][RUN_ID]["bars"]
    assert [r["name"] for r in rows] == ROW_ORDER
    assert {r["name"]: r["basis"] for r in rows} == EXPECTED_BASIS
    assert ev["variants"][RUN_ID]["result"] == "PASS", ev["variants"][RUN_ID]["reasons"]
    assert ev["passing"] == [RUN_ID]
    assert rpr._evaluation_under_current_bars(ev)["cost_edge_ratio_min"] == 2.2
    text = (run_dir / "artifacts" / "profit_bars_evaluation.yaml").read_text(encoding="utf-8")
    assert "&id" not in text and "*id" not in text  # no YAML aliases between rows
    assert "source trade_diagnostics.json" in {r["name"]: r for r in rows}["trade_count_min"]["note"]


def test_v2_evaluation_needs_the_v2_keys():
    run_dir = _v2_run()
    _write_bars(V1_BARS)
    with pytest.raises(rpr.ProfitabilityBarsSchemaError, match="profit_bars_v2 is on"):
        rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)


def test_spend_refused_when_the_evaluation_is_v2_and_the_flag_is_off_now():
    run_dir = _v2_run()
    ev = rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID, record_bars_sha=True)
    _set_orchestrator(FULL_ON)
    with pytest.raises(rpr.HoldoutUnlockRefused) as exc:
        rpr._evaluation_under_current_bars(ev)
    assert exc.value.code == "bars_changed" and "'v2'" in exc.value.detail


def test_spend_refused_when_a_v1_evaluation_meets_the_v2_flag():
    _set_orchestrator(FULL_ON)
    _write_bars(V2_BARS)
    ev = {rpr.BARS_FILE_SHA_FIELD: rpr._bars_file_sha256()}  # graded v1, same bytes
    assert rpr._evaluation_under_current_bars(ev)["sharpe_min"] == 1.0  # flag off: fine
    _set_orchestrator(V2_ON)
    with pytest.raises(rpr.HoldoutUnlockRefused) as exc:
        rpr._evaluation_under_current_bars(ev)
    assert exc.value.code == "bars_changed" and "'v1'" in exc.value.detail


def test_spend_refused_when_the_flag_does_not_read():
    _set_orchestrator({**FULL_ON, "profit_bars_v2": {"enabled": "false"}})
    _write_bars(V2_BARS)
    with pytest.raises(rpr.HoldoutUnlockRefused) as exc:
        rpr._evaluation_under_current_bars({rpr.BARS_FILE_SHA_FIELD: rpr._bars_file_sha256()})
    assert exc.value.code == "bars_changed"


def test_partial_coverage_cap_still_applies_under_v2(monkeypatch):
    run_dir = _v2_run()
    real = rpr._profit_bars_backtest_candidates

    def _with_cap(rd, rid):
        out = real(rd, rid)
        out[RUN_ID]["partial_coverage"] = "graded on partial coverage (test)"
        return out
    monkeypatch.setattr(rpr, "_profit_bars_backtest_candidates", _with_cap)
    ev = rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    rows = {r["name"]: r for r in ev["variants"][RUN_ID]["bars"]}
    for name in rpr._variant_coin_module().D042_TIME_DEPENDENT_BARS:
        assert rows[name]["result"] == "NOT_EVALUABLE"
    assert ev["passing"] == [] and ev["result"] == "FAIL"


# ---------------------------------------------------------------------------
# 5. Flag off
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("scenario", sorted(golden_harness.scenarios()))
def test_golden_promote_path_unchanged_with_the_flag_written_false(scenario, monkeypatch):
    common = golden_harness._common()
    for sc in common["scenarios"].values():
        sc["orchestrator"] = {**sc["orchestrator"], "profit_bars_v2": {"enabled": False}}
    monkeypatch.setattr(golden_harness, "_common", lambda: common)
    out = golden_harness.run_scenario(rpr, scenario, Path(tempfile.mkdtemp()))
    expected = sorted(p.name for p in (GOLDEN_DIR / scenario).iterdir())
    assert sorted(out) == expected
    for fname in expected:
        assert out[fname] == (GOLDEN_DIR / scenario / fname).read_text(encoding="utf-8"), fname


@pytest.mark.parametrize("v2_section", [None, {"enabled": False}])
def test_per_backtest_evaluation_is_v1_with_the_flag_absent_or_false(v2_section):
    run_dir = _v2_run()
    orch = dict(FULL_ON)
    if v2_section is not None:
        orch["profit_bars_v2"] = v2_section
    _set_orchestrator(orch)
    _write_bars(V1_BARS)  # the v1 loader: no v2 key needed
    ev = rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    assert "bars_definitions" not in ev
    assert [r["name"] for r in ev["variants"][RUN_ID]["bars"]] == [
        "sharpe_min", "deflated_sharpe_threshold", "max_drawdown_pct_max", "trade_count_min",
        "avg_daily_return_min"]
    assert all("comparator" not in r and "detail" not in r
               for r in ev["variants"][RUN_ID]["bars"])


def test_flag_off_evaluation_bytes_identical_absent_vs_false():
    run_dir = _v2_run()
    texts = []
    for orch in (FULL_ON, {**FULL_ON, "profit_bars_v2": {"enabled": False}}):
        _set_orchestrator(orch)
        _write_bars(V1_BARS)
        rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
        text = (run_dir / "artifacts" / "profit_bars_evaluation.yaml").read_text(encoding="utf-8")
        texts.append("\n".join(line for line in text.splitlines()
                               if not line.startswith("generated_at:")))
    assert texts[0] == texts[1]
