"""D-186 (direction 2026-10-24, PR-4): step 1a code and config -- IC at horizons, residual IC
exempt without a block, the card statement schema.

Two flags, both off by default:
  orchestrator.forecast_ic_horizons       the `forecast_ic_median` menu entry takes a card `horizon`
                                          (1, 6, 24, 72, 168); the grid reads the matching window
                                          core field; residual_ic.py ranks against the h-bar forward
                                          return; run_protocol gets --forecast-ic-horizons.
  orchestrator.residual_ic_requires_block an idea on a timeframe with no forecast block is exempt
                                          from residual IC ("no forecast block on this timeframe").

Every test with a flag off pins byte-identity with the behaviour before D-186. All synthetic: no
LLM, no backtest, no trial row, no holdout. (build_core itself is tested in
trading-bot/tests/test_build_core_ic_horizons.py.)
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR / "tests"))
sys.path.insert(0, str(SR / "workflow"))
sys.path.insert(0, str(SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
import composite_cache as cc  # noqa: E402
import residual_ic as ric  # noqa: E402
from _reader_test_helpers import _set_orchestrator  # noqa: E402
from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402
from test_e060_s2_residual_ic import (  # noqa: E402
    _block, _protocol, _registry_file, _seal, _summary, _variant_results, Z_CAND, Z_COMP,
)

RAW_MENU = yaml.safe_load((SR / "config" / "criterion_menu.yaml").read_text(encoding="utf-8"))
CID = "forecast_ic_median"
METRIC = "forecast_return_corr_all_bars"
HORIZONS = [1, 6, 24, 72, 168]
ON = {"forecast_ic_horizons": {"enabled": True}}
BLOCK_ON = {"residual_ic_requires_block": {"enabled": True}}

# The entry exactly as it read under D-134, before this row (basis aside): the flag-off menu
# must give this, key for key and in this order.
OLD_ENTRY_KEYS = ["id", "metric", "source", "reducer", "comparator", "threshold",
                  "card_overridable", "scale_free", "symbol_reducer", "floor", "basis"]
OLD_ENTRY = {"id": CID, "metric": METRIC, "source": "window", "reducer": "median", "comparator": ">",
             "threshold": 0.02, "card_overridable": [], "scale_free": True, "symbol_reducer": None,
             "floor": {"min_windows": 5}}


def _entry(menu):
    return next(e for e in menu["criteria"] if e["id"] == CID)


def _menu_into_sandbox():
    (rpr.ROOT / "config").mkdir(parents=True, exist_ok=True)
    (rpr.ROOT / "config" / "criterion_menu.yaml").write_text(
        (SR / "config" / "criterion_menu.yaml").read_text(encoding="utf-8"), encoding="utf-8")


def _card(**crit):
    return {"hypothesis_id": "H-1", "criteria": [{"id": CID, **crit}]}


# ---------------------------------------------------------------------------------------------
# 1. the flags
# ---------------------------------------------------------------------------------------------

@pytest.mark.parametrize("reader,name", [(rpr._forecast_ic_horizons_enabled, "forecast_ic_horizons"),
                                         (rpr._residual_ic_requires_block_enabled,
                                          "residual_ic_requires_block")])
def test_flag_reader_false_absent_true_present_and_strict(reader, name):
    _set_orchestrator(None)
    assert reader() is False                                    # no config file
    _set_orchestrator({})
    assert reader() is False                                    # no section
    _set_orchestrator({name: {"enabled": True}})
    assert reader() is True
    _set_orchestrator({name: {"enabled": "true"}})
    with pytest.raises(ValueError):
        reader()                                                # a quoted string is refused


def test_shipped_defaults_are_off_and_registered():
    cfg = yaml.safe_load((SR / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    for name in ("forecast_ic_horizons", "residual_ic_requires_block"):
        assert cfg["orchestrator"][name] == {"enabled": False}
    reg = {f.get("config_key"): f for f in yaml.safe_load(
        (SR / "config" / "feature_flag_register.yaml").read_text(encoding="utf-8"))["flags"]}
    for name in ("forecast_ic_horizons", "residual_ic_requires_block"):
        e = reg[f"orchestrator.{name}.enabled"]
        assert e["state"] == "off_incomplete" and "D-186" in e["blocked_on"]
        assert e["reader"] == f"run_phase1_research._{name}_enabled"


def test_both_readers_are_in_the_launch_preflight():
    readers = camp._flag_readers()
    assert readers["forecast_ic_horizons"] is rpr._forecast_ic_horizons_enabled
    assert readers["residual_ic_requires_block"] is rpr._residual_ic_requires_block_enabled


def test_run_protocol_gets_the_argument_only_under_the_flag():
    _set_orchestrator(None)
    assert rpr._forecast_ic_horizons_args() == []
    _set_orchestrator(ON)
    assert rpr._forecast_ic_horizons_args() == ["--forecast-ic-horizons"]
    src = (SR / "tools" / "run_protocol.py").read_text(encoding="utf-8")
    assert '"--forecast-ic-horizons"' in src and "set_forecast_ic_horizons(" in src


# ---------------------------------------------------------------------------------------------
# 2. the menu entry and its flag-off strip
# ---------------------------------------------------------------------------------------------

def test_the_menu_entry_declares_the_horizon():
    e = _entry(RAW_MENU)
    assert e["card_overridable"] == ["horizon"]
    assert e["horizon"] == 1 and e["horizon_allowed"] == HORIZONS
    assert e["metric"] == METRIC and e["threshold"] == 0.02       # nothing else moved


def test_flag_off_menu_is_the_pre_d186_entry_key_for_key():
    off = _entry(vce.menu_without_horizon(RAW_MENU))
    assert list(off) == OLD_ENTRY_KEYS
    assert {k: v for k, v in off.items() if k != "basis"} == OLD_ENTRY
    assert off["basis"] == _entry(RAW_MENU)["basis"]


def test_menu_without_horizon_does_not_mutate_and_leaves_other_entries_alone():
    before = copy.deepcopy(RAW_MENU)
    off = vce.menu_without_horizon(RAW_MENU)
    assert RAW_MENU == before
    others_raw = [e for e in RAW_MENU["criteria"] if e["id"] != CID]
    others_off = [e for e in off["criteria"] if e["id"] != CID]
    assert others_raw == others_off
    assert off["code_added_criteria"] == RAW_MENU["code_added_criteria"]
    nothing = {"criteria": others_raw}
    assert vce.menu_without_horizon(nothing) is nothing           # nothing to strip: same object


def test_the_loader_strips_with_the_flag_off_and_keeps_with_it_on():
    _menu_into_sandbox()
    _set_orchestrator(None)
    assert _entry(rpr._load_criterion_menu()) == _entry(vce.menu_without_horizon(RAW_MENU))
    _set_orchestrator(ON)
    assert _entry(rpr._load_criterion_menu()) == _entry(RAW_MENU)
    (rpr.ROOT / "config" / "criterion_menu.yaml").unlink()
    assert rpr._load_criterion_menu() == {}                       # absent file, as before


def test_flag_off_resolved_criterion_is_byte_identical_to_before():
    _menu_into_sandbox()
    _set_orchestrator(None)
    menu = rpr._load_criterion_menu()
    (res,) = vce.resolve_criteria_against_menu([{"id": CID}], menu)
    assert "horizon" not in res and "horizon_allowed" not in res
    assert {k: v for k, v in res.items() if k != "basis"} == OLD_ENTRY
    # the card path (meta keys dropped) gives the registered pass_rule of D-134
    pr = rpr._pass_rule_from_card(_card(), menu, "card")
    assert pr == {"criteria": [{k: v for k, v in OLD_ENTRY.items() if k != "card_overridable"}]}
    assert json.dumps(pr, sort_keys=False) == json.dumps(
        {"criteria": [{k: v for k, v in OLD_ENTRY.items() if k != "card_overridable"}]})


def test_flag_off_a_cards_horizon_is_refused_as_an_unknown_key():
    _menu_into_sandbox()
    _set_orchestrator(None)
    menu = rpr._load_criterion_menu()
    with pytest.raises(ValueError, match="does not let a criterion override"):
        rpr._pass_rule_from_card(_card(horizon=24), menu, "card")
    # restating the menu's value of a key that is not there is still an override
    with pytest.raises(ValueError):
        rpr._pass_rule_from_card(_card(horizon=1), menu, "card")


def test_flag_on_a_card_may_set_each_allowed_horizon():
    _menu_into_sandbox()
    _set_orchestrator(ON)
    menu = rpr._load_criterion_menu()
    for h in HORIZONS:
        (crit,) = rpr._pass_rule_from_card(_card(horizon=h), menu, "card")["criteria"]
        assert crit["horizon"] == h and crit["metric"] == METRIC and crit["threshold"] == 0.02
        assert "horizon_allowed" not in crit and "card_overridable" not in crit


def test_flag_on_the_default_horizon_is_written_as_1():
    _menu_into_sandbox()
    _set_orchestrator(ON)
    (crit,) = rpr._pass_rule_from_card(_card(), rpr._load_criterion_menu(), "card")["criteria"]
    assert crit["horizon"] == 1


@pytest.mark.parametrize("bad", [2, 0, -6, 25, 169, "6", "24", 6.0, True, [6], {"h": 6}])
def test_flag_on_any_other_horizon_value_is_refused(bad):
    _menu_into_sandbox()
    _set_orchestrator(ON)
    with pytest.raises(ValueError, match="allowed horizons"):
        rpr._pass_rule_from_card(_card(horizon=bad), rpr._load_criterion_menu(), "card")


def test_flag_on_no_other_field_became_overridable():
    _menu_into_sandbox()
    _set_orchestrator(ON)
    menu = rpr._load_criterion_menu()
    for key, val in (("threshold", 0.05), ("metric", "sharpe"), ("comparator", ">="),
                     ("floor", {"min_windows": 1})):
        with pytest.raises(ValueError):
            rpr._pass_rule_from_card(_card(**{key: val}), menu, "card")


def test_the_brief_lint_follows_the_flag():
    rule = {"criteria": [{"id": CID, "horizon": 24}]}
    on = vce.lint_menu_shaped_pass_rule(rule, RAW_MENU)
    assert on == []
    off = vce.lint_menu_shaped_pass_rule(rule, vce.menu_without_horizon(RAW_MENU))
    assert off and "does not let a criterion override" in off[0]
    bad = vce.lint_menu_shaped_pass_rule({"criteria": [{"id": CID, "horizon": 7}]}, RAW_MENU)
    assert bad and "allowed horizons" in bad[0]


# ---------------------------------------------------------------------------------------------
# 3. the grid reads the matching field
# ---------------------------------------------------------------------------------------------

def _pr(per_window: list[dict]):
    return {"results": [{"symbol": "ETHUSDT", "window": f"2021-{i + 1:02d}",
                         "core": {"trade_count": 7, **core}} for i, core in enumerate(per_window)],
            "trade_diagnostics_summary": {}, "per_symbol_summary": {},
            "hypothesis_verdict": {"diagnostics": {}}}


def _grid(per_window, menu, criterion=None):
    rule = {"pass_rule": {"criteria": vce.resolve_criteria_against_menu([criterion or {"id": CID}], menu)}}
    return vce.evaluate_grid({"v1": _pr(per_window)}, rule, {}, menu)["grid"][CID]["v1"]


def _windows(n=6, **fields):
    return [{METRIC: 0.0, **{k: v for k, v in fields.items()}} for _ in range(n)]


def test_horizon_reads_its_own_field_not_the_one_bar_field():
    cores = [{METRIC: 0.0, "forecast_return_corr_all_bars_h24": 0.05, "forecast_return_corr_all_bars_h6": -0.1}
             for _ in range(6)]
    assert _grid(cores, RAW_MENU, {"id": CID, "horizon": 24})["result"] == "PASS"
    assert _grid(cores, RAW_MENU, {"id": CID, "horizon": 24})["value"] == 0.05
    assert _grid(cores, RAW_MENU, {"id": CID, "horizon": 6})["result"] == "FAIL"
    assert _grid(cores, RAW_MENU, {"id": CID, "horizon": 1})["result"] == "FAIL"   # METRIC is 0.0
    assert _grid(cores, RAW_MENU)["result"] == "FAIL"             # default horizon 1


def test_horizon_one_reads_exactly_what_the_flag_off_grid_reads():
    cores = [{METRIC: v, "forecast_return_corr_all_bars_h1": v + 9.0}
             for v in (0.01, 0.03, 0.05, 0.04, 0.06, 0.02)]
    off = _grid(cores, vce.menu_without_horizon(RAW_MENU))
    on = _grid(cores, RAW_MENU, {"id": CID, "horizon": 1})
    assert on["value"] == off["value"] and on["result"] == off["result"]
    on_default = _grid(cores, RAW_MENU)
    assert on_default["value"] == off["value"]


def test_a_window_without_the_horizon_field_is_left_out_and_under_the_floor_is_inconclusive():
    cores = [{METRIC: 0.9, "forecast_return_corr_all_bars_h24": 0.05} for _ in range(4)] + \
            [{METRIC: 0.9} for _ in range(2)]                     # a window run without the flag
    cell = _grid(cores, RAW_MENU, {"id": CID, "horizon": 24})
    assert cell["result"] == "INCONCLUSIVE" and cell["n_windows"] == 4
    none_windows = [{METRIC: 0.9, "forecast_return_corr_all_bars_h24": None} for _ in range(6)]
    assert _grid(none_windows, RAW_MENU, {"id": CID, "horizon": 24})["result"] == "INCONCLUSIVE"


def test_a_malformed_horizon_in_a_registered_rule_is_a_spec_error_not_a_crash():
    for bad in ("24", 24.0, True, 0, -1):
        cell = _grid(_windows(), RAW_MENU, {"id": CID, "horizon": bad})
        assert cell["result"] == "SPEC_ERROR" and "horizon" in cell["reason"]


def test_horizon_metric_unit():
    assert vce.horizon_metric({}, "m") == ("m", None)
    assert vce.horizon_metric({"horizon": None}, "m") == ("m", None)
    assert vce.horizon_metric({"horizon": 1}, "m") == ("m", None)
    assert vce.horizon_metric({"horizon": 72}, "m") == ("m_h72", None)
    assert vce.horizon_metric({"horizon": "72"}, "m")[1]


def test_a_criterion_with_no_horizon_key_is_graded_as_before_in_every_old_shape():
    # the flag-off resolved criterion (no horizon key) reads the base field
    cores = [{METRIC: 0.05, "forecast_return_corr_all_bars_h24": -1.0} for _ in range(6)]
    assert _grid(cores, vce.menu_without_horizon(RAW_MENU))["result"] == "PASS"


# ---------------------------------------------------------------------------------------------
# 4. the residual IC at a horizon
# ---------------------------------------------------------------------------------------------

def _two_window_result(tmp_path, n=40):
    import random
    import pandas as pd
    rng = random.Random(7)
    entries = []
    closes_by = {}
    for w, t0 in (("w1", "2020-01-01"), ("w2", "2020-03-01")):
        closes, c = [], 100.0
        for _ in range(n):
            closes.append(c)
            c *= 1.0 + rng.gauss(0.0, 0.01)
        d = tmp_path / f"wr_{w}"
        d.mkdir(parents=True)
        pd.DataFrame({"timestamp": pd.date_range(t0, periods=n, freq="h"),
                      "close": closes, "forecast": [rng.gauss(0, 1) for _ in range(n)]}
                     ).to_csv(d / "bars.csv", index=False)
        entries.append({"symbol": "BTCUSDT", "window": w, "run_id": f"wr_{w}", "core": {}})
        closes_by[w] = closes
    return {"results": entries}, closes_by


@pytest.mark.parametrize("h", [1, 6, 24])
def test_records_at_horizon_h_are_the_h_bar_forward_returns_within_each_window(tmp_path, h):
    n = 40
    pr, closes_by = _two_window_result(tmp_path, n)
    records, steps = ric.symbol_records_from_protocol_result(pr, tmp_path, horizon=h)
    recs = records["BTCUSDT"]
    assert len(recs) == 2 * (n - h)                              # h tail bars of EACH window dropped
    expected = []
    for w in ("w1", "w2"):
        c = closes_by[w]
        expected += [(c[i + h] - c[i]) / c[i] * 10000.0 for i in range(n - h)]
    assert [r["next_return_bps"] for r in recs] == pytest.approx(expected)
    assert steps["BTCUSDT"] is not None


def test_horizon_one_is_byte_identical_to_the_call_without_it(tmp_path):
    pr, _ = _two_window_result(tmp_path)
    a = ric.symbol_records_from_protocol_result(pr, tmp_path)
    b = ric.symbol_records_from_protocol_result(pr, tmp_path, horizon=1)
    assert a == b


def test_a_pair_never_crosses_a_window_boundary(tmp_path):
    n = 40
    pr, closes_by = _two_window_result(tmp_path, n)
    recs = ric.symbol_records_from_protocol_result(pr, tmp_path, horizon=24)[0]["BTCUSDT"]
    # w2's first closes were not used as w1's forward returns: w1 contributes only its first 16
    w1_ts = {r["timestamp"] for r in recs if r["timestamp"].month == 1}
    assert len(w1_ts) == n - 24


def test_a_hole_inside_the_span_drops_the_record(tmp_path):
    import pandas as pd
    d = tmp_path / "wr_h"
    d.mkdir()
    ts = list(pd.date_range("2020-01-01", periods=30, freq="h"))
    del ts[10]                                                    # a missing hour
    pd.DataFrame({"timestamp": ts, "close": [100 + i for i in range(29)],
                  "forecast": [float(i % 5) for i in range(29)]}).to_csv(d / "bars.csv", index=False)
    pr = {"results": [{"symbol": "BTCUSDT", "window": "w", "run_id": "wr_h", "core": {}}]}
    h = 6
    recs = ric.symbol_records_from_protocol_result(pr, tmp_path, horizon=h)[0]["BTCUSDT"]
    kept_rows = [i for i in range(29 - h) if not (i < 10 <= i + h)]
    assert len(recs) == len(kept_rows) < 29 - h


@pytest.mark.parametrize("bad", [0, -1, "6", 6.0, True, None])
def test_residual_ic_refuses_a_bad_horizon(tmp_path, bad):
    pr, _ = _two_window_result(tmp_path)
    with pytest.raises(ValueError, match="horizon"):
        ric.symbol_records_from_protocol_result(pr, tmp_path, horizon=bad)


def test_residual_ic_by_variant_at_a_horizon(tmp_path):
    """Composite none (no block): the candidate's own all-bar rank IC against the h-bar return,
    n_bars shrinks by h, n_eff counts blocks of at least h bars."""
    proto = _write_protocol(rpr.ROOT, "p1h.json", _protocol())
    reg = _registry_file([])
    run_dir = rpr.ROOT / "runs" / "run_900"
    n = 900
    results = _variant_results(run_dir, {"base": Z_CAND[:n]})
    summaries = {"base": _summary("wr_base")}
    kw = dict(root=rpr.ROOT, protocol_path=proto, registry_path=reg,
              compositions_path=rpr.ROOT / "campaign_record" / "compositions.yaml",
              holdout_range=_seal())
    d1 = cc.residual_ic_by_variant(summaries, results, **kw)["variants"]["base"]
    d1b = cc.residual_ic_by_variant(summaries, results, horizon=1, **kw)["variants"]["base"]
    assert d1 == d1b and d1["n_bars"] == n - 1                    # horizon 1: today's output
    d72 = cc.residual_ic_by_variant(summaries, results, horizon=72, **kw)["variants"]["base"]
    assert d72["n_bars"] == n - 72
    assert d1["n_eff"] == (n - 1) // 24 and d72["n_eff"] == (n - 72) // 72
    assert d72["value"] != d1["value"]
    # by hand: Spearman of the forecast with the 72-bar return over bars 0..n-73
    import pandas as pd
    from performance.signal_statistics import spearman_correlation
    bars = pd.read_csv(results["base"] / "wr_base" / "bars.csv")
    c = bars["close"].tolist()
    rets = [(c[i + 72] - c[i]) / c[i] * 10000.0 for i in range(n - 72)]
    assert d72["value"] == round(spearman_correlation(Z_CAND[:n - 72], rets), 6)


def test_residual_ic_horizon_comes_from_the_pass_rule_criterion_only():
    rule = lambda crits: {"pass_rule": {"criteria": crits}}
    assert rpr._residual_ic_horizon({}) == 1
    assert rpr._residual_ic_horizon(rule([{"id": "x"}])) == 1
    assert rpr._residual_ic_horizon(rule([{"id": CID}])) == 1
    assert rpr._residual_ic_horizon(rule([{"id": CID, "horizon": 24}])) == 24
    assert rpr._residual_ic_horizon(
        {"machine_constraints": {"pass_rule": {"criteria": [{"id": CID, "horizon": 6}]}}}) == 6
    assert rpr._residual_ic_horizon(rule([{"id": CID, "horizon": "24"}])) == 1      # not an int
    assert rpr._residual_ic_horizon(rule([{"id": CID, "horizon": True}])) == 1
    assert rpr._residual_ic_horizon(rule([{"id": "other", "horizon": 24}])) == 1    # another id
    assert rpr._residual_ic_horizon(rule([{"id": CID, "horizon": 6},
                                          {"id": CID, "horizon": 24}])) == 1       # ambiguous


def _grid_inputs(tmp_path, monkeypatch, horizon_seen, flags):
    """_residual_ic_grid_inputs with residual_ic_by_variant stubbed: which horizon reaches it?"""
    _set_orchestrator(flags)
    proto = _write_protocol(rpr.ROOT, "p1h.json", _protocol())
    run_dir = _minimal_run(rpr.ROOT, "run_901")

    def fake(summaries, dirs, **kw):
        horizon_seen.append(kw.get("horizon", "absent"))
        return {"timeframe": "1h", "timeframe_category": "low", "skipped": None,
                "composite": {"kind": "none"}, "variants": {v: {"value": 0.0} for v in summaries}}
    monkeypatch.setattr(cc, "residual_ic_by_variant", fake)
    pre = {"pass_rule": {"criteria": [{"id": CID, "horizon": 24}]}}
    rpr._residual_ic_grid_inputs({"base": _summary("wr_base")}, run_dir, proto, "py", pre)


def test_grid_inputs_pass_the_horizon_only_under_the_flag(tmp_path, monkeypatch):
    seen = []
    _grid_inputs(tmp_path, monkeypatch, seen, None)
    assert seen == ["absent"]                                     # flag off: the call as before
    seen.clear()
    _grid_inputs(tmp_path, monkeypatch, seen, ON)
    assert seen == [24]
    seen.clear()
    _set_orchestrator(ON)
    monkeypatch.setattr(rpr, "_residual_ic_horizon", lambda pre: 1)
    _grid_inputs(tmp_path, monkeypatch, seen, ON)
    assert seen == ["absent"]                                     # horizon 1: the call as before


# ---------------------------------------------------------------------------------------------
# 5. residual IC needs a block on the timeframe
# ---------------------------------------------------------------------------------------------

def _run_with_timeframe(tf="1h", run_id="run_950"):
    run_dir = _minimal_run(rpr.ROOT, run_id)
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml",
                  {"machine_constraints": {"protocol": {"timeframe": tf, "symbols": ["BTCUSDT"]}}})
    return run_dir


def test_flag_off_an_idea_without_a_block_is_not_exempt_as_before():
    _set_orchestrator(None)
    run_dir = _run_with_timeframe()
    assert rpr._residual_ic_exempt_reason(run_dir) is None
    assert rpr._residual_ic_exempt_reason(run_dir, timeframe="1h") is None


def test_flag_on_no_block_on_the_timeframe_is_exempt_with_the_reason():
    _set_orchestrator(BLOCK_ON)
    run_dir = _run_with_timeframe("1h")
    assert rpr._residual_ic_exempt_reason(run_dir) == "no forecast block on this timeframe"
    assert rpr.RESIDUAL_IC_NO_BLOCK_REASON == "no forecast block on this timeframe"


def test_flag_on_a_block_on_the_timeframe_keeps_it_required():
    _set_orchestrator(BLOCK_ON)
    _registry_file([_block("H1:run_700", tf="1h")])
    assert rpr._residual_ic_exempt_reason(_run_with_timeframe("1h")) is None


def test_flag_on_a_block_on_another_timeframe_does_not_count():
    _set_orchestrator(BLOCK_ON)
    _registry_file([_block("H1:run_700", tf="4h")])
    assert rpr._residual_ic_exempt_reason(_run_with_timeframe("1h")) == RESIDUAL_NO_BLOCK
    assert rpr._residual_ic_exempt_reason(_run_with_timeframe("4h", "run_951")) is None


def test_flag_on_a_regime_block_on_the_timeframe_is_not_a_forecast_block():
    _set_orchestrator(BLOCK_ON)
    _registry_file([_block("H1:run_700", tf="1h", kind="regime")])
    assert rpr._residual_ic_exempt_reason(_run_with_timeframe("1h")) == RESIDUAL_NO_BLOCK


def test_existing_exemptions_win_over_the_new_one():
    _set_orchestrator(BLOCK_ON)
    run_dir = _run_with_timeframe("1h")
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml",
                  {"candidate": {"source": {"proposal": {"block": {"kind": "regime"}}}}})
    assert rpr._residual_ic_exempt_reason(run_dir) == "regime block"
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml",
                  {"candidate": {"source": {"origin": "composition"}}})
    assert rpr._residual_ic_exempt_reason(run_dir) == "composition run"


def test_flag_on_an_undeterminable_timeframe_keeps_todays_answer():
    _set_orchestrator(BLOCK_ON)
    run_dir = _minimal_run(rpr.ROOT, "run_952")                   # no pre-registration, no context
    assert rpr._residual_ic_exempt_reason(run_dir) is None


def test_flag_on_the_protocol_constraint_without_a_timeframe_defaults_to_1h():
    _set_orchestrator(BLOCK_ON)
    run_dir = _minimal_run(rpr.ROOT, "run_953")
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml",
                  {"machine_constraints": {"protocol": {"symbols": ["BTCUSDT"]}}})
    _registry_file([_block("H1:run_700", tf="1h")])
    assert rpr._residual_ic_exempt_reason(run_dir) is None
    _registry_file([_block("H1:run_700", tf="4h")])
    assert rpr._residual_ic_exempt_reason(run_dir) == RESIDUAL_NO_BLOCK


def test_flag_on_a_pinned_protocol_gives_the_timeframe():
    _set_orchestrator(BLOCK_ON)
    proto = _protocol()
    proto["timeframe"] = "4h"
    _write_protocol(rpr.ROOT, "p4h.json", proto)
    run_dir = _minimal_run(rpr.ROOT, "run_954")
    rpr.save_yaml(run_dir / "artifacts" / "run_context.yaml",
                  {"run_type": "protocol_ref_pinned", "protocol": "p4h.json"})
    _registry_file([_block("H1:run_700", tf="1h")])
    assert rpr._residual_ic_exempt_reason(run_dir) == RESIDUAL_NO_BLOCK       # no 4h block
    _registry_file([_block("H1:run_700", tf="4h")])
    assert rpr._residual_ic_exempt_reason(run_dir) is None


def test_an_explicit_timeframe_wins_over_the_run_files():
    _set_orchestrator(BLOCK_ON)
    _registry_file([_block("H1:run_700", tf="4h")])
    run_dir = _run_with_timeframe("1h")
    assert rpr._residual_ic_exempt_reason(run_dir, timeframe="4h") is None
    assert rpr._residual_ic_exempt_reason(run_dir, timeframe="1h") == RESIDUAL_NO_BLOCK


def test_the_lookup_is_the_composite_resolvers_own_none_kind():
    _set_orchestrator(BLOCK_ON)
    _registry_file([_block("H1:run_700", tf="1h"), _block("H2:run_701", tf="1h")])   # two, no composition
    assert cc.resolve_current_composite(
        __import__("block_registry").load_active_registry(rpr._block_registry_path()), [], "1h"
    )["kind"] == "stale"
    # stale is "blocks exist": not exempt (the grid reports STALE as before)
    assert rpr._residual_ic_exempt_reason(_run_with_timeframe("1h")) is None


def test_grid_inputs_exempt_a_no_block_run_and_remove_the_criterion(monkeypatch):
    _set_orchestrator(BLOCK_ON)
    _menu_into_sandbox()
    proto = _write_protocol(rpr.ROOT, "p1h.json", _protocol())
    run_dir = _minimal_run(rpr.ROOT, "run_955")
    pre = {"pass_rule": {"criteria": [{"id": CID}, {"id": "residual_ic"}]}}
    out, grid_pre = rpr._residual_ic_grid_inputs({"base": _summary("wr_base")}, run_dir, proto, "py", pre)
    assert [c["id"] for c in grid_pre["pass_rule"]["criteria"]] == [CID]
    doc = rpr.load_yaml(run_dir / "artifacts" / "residual_ic.yaml")
    assert doc["skipped"] == "no forecast block on this timeframe"


def test_flag_off_the_same_run_is_not_skipped(monkeypatch):
    _set_orchestrator(None)
    proto = _write_protocol(rpr.ROOT, "p1h.json", _protocol())
    run_dir = _minimal_run(rpr.ROOT, "run_956")
    seen = {}

    def fake(summaries, dirs, **kw):
        seen.update(kw)
        return {"timeframe": "1h", "timeframe_category": "low", "skipped": kw.get("exempt_reason"),
                "composite": {"kind": "none"}, "variants": {v: {"value": 0.0} for v in summaries}}
    monkeypatch.setattr(cc, "residual_ic_by_variant", fake)
    pre = {"pass_rule": {"criteria": [{"id": CID}, {"id": "residual_ic"}]}}
    rpr._residual_ic_grid_inputs({"base": _summary("wr_base")}, run_dir, proto, "py", pre)
    assert seen["exempt_reason"] is None and "horizon" not in seen


# ---------------------------------------------------------------------------------------------
# 6. the card schema
# ---------------------------------------------------------------------------------------------

jsonschema = pytest.importorskip("jsonschema")
SCHEMA = json.loads((SR / "workflow_artifacts" / "schemas" / "hypothesis_card.schema.json")
                    .read_text(encoding="utf-8"))

OLD_REQUIRED = ["hypothesis_id", "thesis", "rationale", "edge_source", "signal_concept",
                "target_market", "timeframe", "assumptions", "expected_failure_modes"]
OLD_SHAPE = {
    "hypothesis_id": "H-1", "thesis": "t", "rationale": "r",
    "edge_source": {"category": "persistent_behavioral_bias", "specific_mechanism": "m",
                    "why_not_arbitraged": "w", "evidence_type": "price_volume_only",
                    "measurable_proxy": "p"},
    "signal_concept": "s", "target_market": "BTCUSDT", "timeframe": "1h",
    "assumptions": ["a"], "expected_failure_modes": ["x", "y", "z"],
}
NEW_SHAPE = {
    "hypothesis_id": "H-2", "timeframe": "1h",
    "idea_quantities": ["momentum over 24 bars", {"name": "volume", "why": "crowding"}],
    "not_expressible": ["order-book imbalance"],
    "statement": {"predicts": "the next day's return", "predicts_kind": "return_direction",
                  "horizon_bars": 24, "condition": "always",
                  "if_pass": "keep", "if_fail": "drop"},
    "criteria": [{"id": CID, "horizon": 24}],
    "criteria_rationale": "IC at the day horizon answers the statement",
}


def _valid(card):
    jsonschema.validate(card, SCHEMA)


def test_the_old_shape_card_is_still_valid():
    _valid(OLD_SHAPE)


def test_a_new_shape_card_is_valid():
    _valid(NEW_SHAPE)


def test_old_and_new_fields_together_are_valid():
    _valid({**OLD_SHAPE, **{k: v for k, v in NEW_SHAPE.items() if k not in ("hypothesis_id", "timeframe")}})


def test_required_before_and_after():
    assert SCHEMA["else"]["required"] == ["hypothesis_id", "timeframe"]
    assert set(OLD_REQUIRED) - set(SCHEMA["else"]["required"]) == {
        "thesis", "rationale", "edge_source", "signal_concept", "target_market", "assumptions",
        "expected_failure_modes"}
    for key in OLD_REQUIRED:                                      # no property was removed
        assert key in SCHEMA["properties"]
    for key in ("idea_quantities", "not_expressible", "statement", "criteria_rationale"):
        assert key in SCHEMA["properties"] and key not in SCHEMA["else"]["required"]


@pytest.mark.parametrize("missing", ["hypothesis_id", "timeframe"])
def test_identity_and_bar_size_stay_required(missing):
    card = {k: v for k, v in NEW_SHAPE.items() if k != missing}
    with pytest.raises(jsonschema.ValidationError):
        _valid(card)


@pytest.mark.parametrize("statement", [
    {"horizon_bars": 0}, {"horizon_bars": "24"}, {"horizon_bars": 2.5}, {"horizon_bars": True},
    {"horizon_bars": -1},
    {"predicts": 3, "predicts_kind": "return_direction"}, {"unknown": "x"},
])
def test_statement_is_checked(statement):
    with pytest.raises(jsonschema.ValidationError):
        _valid({**NEW_SHAPE, "statement": {"predicts": "x", "predicts_kind": "market_state", **statement}})


def test_statement_requires_predicts_and_predicts_kind_only():  # D-192
    with pytest.raises(jsonschema.ValidationError):
        _valid({**NEW_SHAPE, "statement": {}})
    with pytest.raises(jsonschema.ValidationError):
        _valid({**NEW_SHAPE, "statement": {"predicts": "x"}})
    _valid({**NEW_SHAPE, "statement": {"predicts": "x", "predicts_kind": "market_state"}})


@pytest.mark.parametrize("field,val", [("idea_quantities", "x"), ("not_expressible", {"a": 1}),
                                       ("criteria_rationale", ["x"])])
def test_new_field_types(field, val):
    with pytest.raises(jsonschema.ValidationError):
        _valid({**NEW_SHAPE, field: val})


def test_a_stray_field_is_still_refused():
    with pytest.raises(jsonschema.ValidationError):
        _valid({**NEW_SHAPE, "horizon": 24})


def test_the_composition_branch_is_unchanged():
    comp = {"hypothesis_id": "H-3", "thesis": "t", "timeframe": "1h",
            "composition": {"registry_hash": "h", "timeframe": "1h", "block_ids": [], "manifest_ref": "m"},
            "criteria": [], "pass_through": True, "source": "s"}
    _valid(comp)
    with pytest.raises(jsonschema.ValidationError):
        _valid({k: v for k, v in comp.items() if k != "thesis"})


def test_no_code_derives_a_criterion_or_horizon_from_the_statement():
    """The statement is information only (direction 2026-10-24: no criterion derivation by code).
    D-192 (PR-8): the one reader is `_criterion_consistency_warnings`, which only warns; the rest of
    run_phase1_research.py (the text from that function to its writer excluded) still never reads it."""
    for rel in ("workflow/run_phase1_research.py", "workflow/run_campaign.py",
                "tools/verdict_criteria_evaluator.py", "tools/residual_ic.py",
                "tools/composite_cache.py", "tools/decide_next.py"):
        text = (SR / rel).read_text(encoding="utf-8")
        if rel == "workflow/run_phase1_research.py":  # D-192: the one reader is the warning-only check
            head, rest = text.split("def _criterion_consistency_warnings", 1)
            text = head + rest.split("def _write_criterion_consistency", 1)[1]
        assert not any(w in text for w in ("horizon_bars", "idea_quantities", "criteria_rationale", "not_expressible")), rel


RESIDUAL_NO_BLOCK = "no forecast block on this timeframe"


# ---------------------------------------------------------------------------------------------
# 8. review round (PR #537): the flag-off step 1a prompt is byte-identical, the run_protocol
#    default is cleared, the pooled h>1 span step is robust to a hole in the first pair
# ---------------------------------------------------------------------------------------------

MENU_PATH = SR / "config" / "criterion_menu.yaml"
# The menu exactly as master 6257c9f3 had it, before D-186. NOTE: re-pin this fixture together
# with ANY later menu edit made outside the `# D-186 BEGIN` .. `# D-186 END` brackets -- the
# flag-off prompt text must equal it byte for byte.
MENU_PRE_D186 = (SR / "tests" / "fixtures" / "d186" / "criterion_menu_pre_d186.yaml"
                 ).read_text(encoding="utf-8")
MENU_REQ_PATH = "../../config/criterion_menu.yaml"


def _raw_menu_text():
    return MENU_PATH.read_text(encoding="utf-8")


def test_flag_off_menu_prompt_text_is_the_pre_d186_menu_byte_for_byte():
    assert rpr._menu_text_for_prompt(_raw_menu_text(), False) == MENU_PRE_D186


def test_flag_off_menu_prompt_text_has_no_horizon_token_and_no_marker():
    off = rpr._menu_text_for_prompt(_raw_menu_text(), False)
    assert "horizon" not in off.lower()
    assert "D-186" not in off
    assert "card_overridable: []" in off and "card_overridable: [horizon]" not in off


def test_flag_on_menu_prompt_text_is_the_raw_file():
    raw = _raw_menu_text()
    assert rpr._menu_text_for_prompt(raw, True) == raw
    assert "# D-186 BEGIN" in raw and "card_overridable: [horizon]" in raw


def test_menu_markers_are_comments_the_loaded_menu_is_unaffected():
    raw = _raw_menu_text()
    on = yaml.safe_load(raw)
    assert on == RAW_MENU
    assert _entry(on)["card_overridable"] == ["horizon"] and _entry(on)["horizon_allowed"] == HORIZONS
    # the flag-off prompt text loads to exactly what the flag-off loader hands every consumer
    assert yaml.safe_load(rpr._menu_text_for_prompt(raw, False)) == vce.menu_without_horizon(on)
    assert yaml.safe_load(MENU_PRE_D186) == vce.menu_without_horizon(on)


def test_menu_brackets_are_balanced_and_a_half_open_one_raises():
    raw = _raw_menu_text()
    lines = [ln.strip() for ln in raw.splitlines()]
    assert lines.count("# D-186 BEGIN") == lines.count("# D-186 END") >= 2
    with pytest.raises(ValueError):
        rpr._menu_text_for_prompt("a: 1\n    # D-186 BEGIN\nb: 2\n", False)


def test_menu_off_lines_keep_their_indent_and_line_ending():
    text = "x: 1\r\n  # D-186 BEGIN\r\n  drop: 1\r\n  # D-186 OFF: keep: 2\r\n  # D-186 END\r\ny: 3\r\n"
    assert rpr._menu_text_for_prompt(text, False) == "x: 1\r\n  keep: 2\r\ny: 3\r\n"


def test_only_the_menu_input_is_filtered():
    raw = _raw_menu_text()
    _set_orchestrator(None)
    assert rpr._prompt_input_content(MENU_REQ_PATH, raw) == MENU_PRE_D186
    assert rpr._prompt_input_content("..\..\config\criterion_menu.yaml", raw) == MENU_PRE_D186
    assert rpr._prompt_input_content("artifacts/research_brief.yaml", raw) == raw
    _set_orchestrator(ON)
    assert rpr._prompt_input_content(MENU_REQ_PATH, raw) == raw


def _menu_handoff():
    return {"required_inputs": [{"path": MENU_REQ_PATH, "reason": "menu"}], "optional_inputs": []}


def _menu_run_dir():
    _menu_into_sandbox()
    run_dir = rpr.ROOT / "runs" / "run_d186"
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    return run_dir


def _menu_section(text):
    return f"--- CONTENT OF {MENU_REQ_PATH} ---\n{text}\n"


def _gemini_prompt(monkeypatch, run_dir):
    import asyncio
    seen = {}

    class _Stop(Exception):
        pass

    class _Models:
        async def generate_content(self, **kw):
            seen["contents"] = kw["contents"]
            raise _Stop

    class _Client:
        class aio:  # noqa: N801
            models = _Models()

    monkeypatch.setattr(rpr, "_get_client", lambda: _Client())
    with pytest.raises(_Stop):
        asyncio.run(rpr.run_gemini_worker("hypothesis_generation", _menu_handoff(), run_dir))
    return seen["contents"]


def test_both_prompt_assemblers_inline_the_pre_d186_menu_with_the_flag_off(monkeypatch):
    _set_orchestrator(None)
    run_dir = _menu_run_dir()
    claude_prompt = rpr._build_stage_prompt("hypothesis_generation", _menu_handoff(), run_dir)
    gemini_prompt = _gemini_prompt(monkeypatch, run_dir)
    for prompt in (claude_prompt, gemini_prompt):
        assert _menu_section(MENU_PRE_D186) in prompt
        assert "D-186" not in prompt.split("--- CONTENT OF")[1].split("YAML FORMATTING")[0]
        assert "horizon" not in _menu_section(MENU_PRE_D186)


def test_both_prompt_assemblers_inline_the_raw_menu_with_the_flag_on(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _menu_run_dir()
    raw = _raw_menu_text()
    assert _menu_section(raw) in rpr._build_stage_prompt("hypothesis_generation", _menu_handoff(), run_dir)
    assert _menu_section(raw) in _gemini_prompt(monkeypatch, run_dir)


def test_run_protocol_main_clears_the_forecast_ic_default_on_a_flag_off_call(monkeypatch):
    """An in-process flag-on call followed by a flag-off call leaves the default None (the
    --holdout-without---i-understand refusal exits right after the default is set)."""
    import run_protocol as rp
    from reporting import run_artifact as ra
    monkeypatch.setattr(ra, "_forecast_ic_horizons_default", None)
    for argv, expected in ((["--forecast-ic-horizons"], tuple(ra.FORECAST_IC_HORIZONS)), ([], None)):
        monkeypatch.setattr(sys, "argv", ["run_protocol.py", "cfg.json", "proto.json", "--holdout"] + argv)
        with pytest.raises(SystemExit):
            rp.main()
        assert ra._forecast_ic_horizons_default == expected


def _pooled_rows(tmp_path, timestamps):
    import pandas as pd
    d = tmp_path / "wr_p"
    d.mkdir()
    n = len(timestamps)
    pd.DataFrame({"timestamp": timestamps, "close": [100.0 + i for i in range(n)],
                  "forecast": [float(i % 5) for i in range(n)]}).to_csv(d / "bars.csv", index=False)
    return [{"symbol": "BTCUSDT", "window": "w", "run_id": "wr_p"}]


def test_pooled_h_gt_1_first_pair_spanning_a_hole_still_builds_records(tmp_path):
    import pandas as pd
    import run_protocol as rp
    ts = list(pd.date_range("2020-01-01", periods=40, freq="h"))
    del ts[1:3]                                   # first pair (index 0, 1) spans a 3-hour hole
    rows = _pooled_rows(tmp_path, ts)
    n, h = len(ts), 6
    records, first_pair_step, _ = rp._assemble_pooled_symbol_records(rows, tmp_path, horizon=h)
    assert first_pair_step == pd.Timedelta(hours=3)          # returned value untouched (h=1 path)
    kept = [i for i in range(n - h) if ts[i + h] - ts[i] == pd.Timedelta(hours=h)]
    assert len(records) == len(kept) > 0
    assert [r["timestamp"] for r in records] == [ts[i] for i in kept]


def test_pooled_h1_path_is_untouched(tmp_path):
    import pandas as pd
    import run_protocol as rp
    ts = list(pd.date_range("2020-01-01", periods=30, freq="h"))
    del ts[1:3]
    rows = _pooled_rows(tmp_path, ts)
    a = rp._assemble_pooled_symbol_records(rows, tmp_path)
    b = rp._assemble_pooled_symbol_records(rows, tmp_path, horizon=1)
    assert a == b and len(a[0]) == len(ts) - 1 and a[1] == pd.Timedelta(hours=3)
