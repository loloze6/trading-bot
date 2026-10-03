"""E-068 slice 3 (CUL-393): the claim card's tests MEASURED after the backtests.

Covers:
  1. tools/claim_measure: effect sizes on a planted effect and on no effect,
     window signs ("k of n") per variant and per coin, the plain description,
     regime selectors measured, never a p-value or a verdict;
  2. no lookahead: windows never chained, no signal recompute, no cache read,
     a bar at or after the holdout start refused;
  3. statuses: measured / not_measured with a reason (card gap, bars missing,
     error, no graded variant), every test counted;
  4. run_phase1_research wiring: flag-off byte identity, flag-on files and
     coverage, idea_status/grid untouched, files cleared on a re-run, and an
     error at each step never escapes (information only);
  5. the offline tool's calibration lock now compares the outcome kind, the
     selector and the number of fakes.

No LLM, no backtest, no market data. tests/conftest.py sandboxes rpr.ROOT.
"""
import copy
import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import claim_card as cc  # noqa: E402
import claim_measure as cm  # noqa: E402
import claim_tests as ct  # noqa: E402

from test_e068_claim_tests import (DON, EVENT, FAST, make_windows, passed_summary,  # noqa: E402
                                   spec)
from test_k3_protocol_pinning import _minimal_run  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402

ON = {"config_direct_authoring": {"enabled": True}, "claim_tests": {"enabled": True}}
FAR = "2099-01-01"          # a holdout start after every synthetic bar

UP = {"name": "high_forecast",
      "selector": {"kind": "event", "field": "forecast", "op": ">=", "value": 8},
      "outcome": {"kind": "fwd_return", "horizons": [1, 2]},
      "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "greater",
      "floor": {"min_events": 20}}
REGIME_T = {"name": "trend_label",
            "selector": {"kind": "regime", "value": "trend"},
            "outcome": {"kind": "fwd_return", "horizons": [1]},
            "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "greater",
            "floor": {"min_events": 10}}
IC_T = {"name": "ic", "selector": {"kind": "all"},
        "outcome": {"kind": "fwd_return", "horizons": [1]},
        "statistic": "rank_ic", "direction": "greater", "floor": {"min_blocks": 5}}
CARD = {"hypothesis_id": "H-S3", "criteria": []}


def _claim(tests) -> dict:
    return {"statement": "High forecasts are followed by higher returns.",
            "kind": "direction_forecast", "tests": copy.deepcopy(tests),
            "pass_if": "higher at every horizon", "fail_if": "lower at any horizon",
            "rationale": "the signal ranks the next bars"}


def _planted(seed=1, n=200, n_windows=4):
    """Bars after a forecast >= 8 drift up by 1% (the planted effect)."""
    return make_windows(seed, n=n, n_windows=n_windows,
                        plant=lambda t, fc, ts: (0.01 if fc >= 8 else 0.0, 1.0))


def _keys(doc) -> set:
    out = set()
    if isinstance(doc, dict):
        for k, v in doc.items():
            out.add(str(k))
            out |= _keys(v)
    elif isinstance(doc, list):
        for v in doc:
            out |= _keys(v)
    return out


def _no_verdict(doc) -> None:
    keys = _keys(doc)
    assert not keys & {"p_value", "p_value_opposite", "verdict", "calibration_file"}, keys
    text = yaml.safe_dump(doc)
    assert "supported" not in text and "refuted" not in text and "inconclusive" not in text


# ---------------------------------------------------------------------------
# 1. claim_measure: effect sizes only
# ---------------------------------------------------------------------------

def test_planted_effect_is_measured_with_window_signs_and_a_description():
    ws = _planted()
    res = cm.measure_test(ws, UP, None)
    assert res["status"] == cm.MEASURED and res["label"] == "measured, not proven"
    for h in (1, 2):
        r = res["horizons"][h]
        assert r["value"] > 0.005                       # ~1% drift per bar after an event
        assert r["windows_with_claimed_sign"] == r["windows_with_a_value"] == 4
        assert r["n_windows"] == 4 and r["n_events"] >= 20
    text = "\n".join(res["description"])
    assert "measured, not proven" in text and "claimed sign in 4 of 4 windows" in text
    assert "No p-value and no verdict" in text
    assert res["spec_hash"] == cc.check_claim(_claim([UP])).tests[0]["spec_hash"]
    _no_verdict(res)


def test_no_effect_is_measured_small_and_mixed():
    ws = make_windows(2, n=200, n_windows=6)
    res = cm.measure_test(ws, UP, None)
    r = res["horizons"][1]
    assert res["status"] == cm.MEASURED and abs(r["value"]) < 0.005
    assert 0 < r["windows_with_claimed_sign"] < 6       # signs flip between windows
    _no_verdict(res)


def test_a_zero_or_undefined_window_never_counts_as_the_claimed_sign():
    cells = [{"oriented": 0.0}, {"oriented": 0.1}, {"oriented": None}, {"oriented": -0.1}]
    assert cm._claimed(cells) == (1, 3)          # 1 of 3 windows with a value


def test_per_coin_rows_split_the_variant():
    ws = _planted(3, n_windows=4)
    for w, sym in zip(ws, ("AAAUSD", "AAAUSD", "BBBUSD", "BBBUSD")):
        w.symbol = sym
    r = cm.measure_test(ws, UP, None)["horizons"][1]
    assert sorted(r["per_coin"]) == ["AAAUSD", "BBBUSD"]
    assert sum(c["n_events"] for c in r["per_coin"].values()) == r["n_events"]
    assert all(c["n_windows"] == 2 for c in r["per_coin"].values())
    only_a = cm.measure_test([w for w in ws if w.symbol == "AAAUSD"], UP, None)["horizons"][1]
    assert r["per_coin"]["AAAUSD"]["value"] == pytest.approx(only_a["value"])
    assert "  BBBUSD: effect" in "\n".join(cm.measure_test(ws, UP, None)["description"])


def test_regime_selector_and_rank_ic_are_measured():
    ws = make_windows(4, n=120, n_windows=3)
    assert ct.check_spec(cm.test_spec(REGIME_T)[0])          # refused for a verdict ...
    reg = cm.measure_test(ws, REGIME_T, None)                # ... measured here
    assert reg["status"] == cm.MEASURED and reg["horizons"][1]["n_events"] > 0
    ic = cm.measure_test(ws, IC_T, None)
    assert ic["status"] == cm.MEASURED and "no baseline" in ic["description"][0]


def test_floor_shortfall_is_reported_not_judged():
    t = dict(UP, floor={"min_events": 10**6})
    res = cm.measure_test(make_windows(5, n=80, n_windows=2), t, None)
    assert res["status"] == cm.MEASURED and res["floor_not_met"]
    assert "Below the card's floor" in "\n".join(res["description"])


def test_eras_are_reported_when_given():
    ws = make_windows(6, n=80, n_windows=2)
    eras = [{"era_id": "early", "range": ["2019-01-01", "2020-06-30"]},
            {"era_id": "late", "range": ["2020-07-01", "2021-12-31"]}]
    r = cm.measure_test(ws, UP, eras)["horizons"][1]
    assert set(r["per_era"]) <= {"early", "late"} and r["n_eras_with_events"] >= 1


def test_measurement_equals_the_engine_effect_sizes():
    """The numbers are slice 1's own effect sizes (run_test, not calibrated)."""
    ws = _planted(7)
    s = ct.TestSpec.from_dict({k: v for k, v in UP.items() if k != "name"})
    engine = ct.run_test(ws, s, calibrated=False)["horizons"]
    mine = cm.measure_test(ws, UP, None)["horizons"]
    for h in (1, 2):
        for k in ("value", "oriented", "n_events", "per_window"):
            assert mine[h][k] == engine[h][k]


# ---------------------------------------------------------------------------
# 2. no lookahead
# ---------------------------------------------------------------------------

def test_windows_are_never_chained_and_later_windows_change_nothing():
    ws = _planted(8, n_windows=3)
    alone = cm.measure_test(ws[:1], UP, None)["horizons"][1]["per_window"]
    together = cm.measure_test(ws, UP, None)["horizons"][1]["per_window"]
    label = ws[0].label
    assert together[label] == alone[label]


def test_a_selection_uses_bar_t_only():
    """Changing every bar AFTER t never changes whether t is selected, nor its
    events up to t - h_max (their outcomes end at or before t)."""
    ws = make_windows(9, n=120, n_windows=1)
    w = ws[0]
    cut = 60
    fut = copy.deepcopy(w)
    fut.forecast[cut + 1:] = -fut.forecast[cut + 1:]
    fut.close[cut + 1:] = fut.close[cut + 1:] * 1.5
    m1, _ = ct.SELECTORS["event"](w, UP["selector"])
    m2, _ = ct.SELECTORS["event"](fut, UP["selector"])
    assert np.array_equal(m1[:cut + 1], m2[:cut + 1])
    y1, y2 = ct.out_fwd_return(w, 2), ct.out_fwd_return(fut, 2)
    assert np.array_equal(y1[:cut - 1], y2[:cut - 1])


def test_no_signal_recompute_and_no_cache_read(monkeypatch, tmp_path):
    run = _run_with_variants(tmp_path / "runs", "run_x", {"base": _planted(10, n_windows=2)})
    monkeypatch.setattr(ct, "compute_signal", lambda *a, **k: pytest.fail("no recompute"))
    monkeypatch.setattr(ct, "read_warmup", lambda *a, **k: pytest.fail("no cache read"))
    doc = cm.measure_variant(run, "base", [UP], None, FAR)
    assert doc["status"] == cm.MEASURED


def test_a_bar_at_the_holdout_start_is_never_measured(tmp_path):
    ws = make_windows(11, n=60, n_windows=2)
    run = _run_with_variants(tmp_path / "runs", "run_x", {"base": ws})
    last = pd.Timestamp(int(ws[-1].ts[-1]), unit="s").strftime("%Y-%m-%d")
    doc = cm.measure_variant(run, "base", [UP], None, last)        # the last bar's own day
    assert doc["status"] == cm.NOT_MEASURED and doc["reason"] == cm.ERROR
    assert "holdout" in doc["detail"] and doc["tests"] == {}
    day_after = (pd.Timestamp(last) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    assert cm.measure_variant(run, "base", [UP], None, day_after)["status"] == cm.MEASURED


# ---------------------------------------------------------------------------
# 3. statuses and counting
# ---------------------------------------------------------------------------

def _write_bars(d: Path, w) -> None:
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "bars.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["timestamp", "close", "forecast", "regime"])
        for t in range(len(w.ts)):
            wr.writerow([pd.Timestamp(int(w.ts[t]), unit="s").strftime("%Y-%m-%d %H:%M:%S"),
                         repr(float(w.close[t])), repr(float(w.forecast[t])), w.regime[t]])


def _run_with_variants(runs_root: Path, run_id: str, variants: dict) -> Path:
    """A run directory as the variant loop leaves it: per variant
    artifacts/variants/<vid>/protocol_result.yaml naming each window's
    variants/<vid>/results/<rid>/bars.csv."""
    run = Path(runs_root) / run_id
    for vid, ws in variants.items():
        results = []
        for i, w in enumerate(ws):
            rid = f"{vid}_r{i}"
            _write_bars(run / "variants" / vid / "results" / rid, w)
            results.append({"symbol": w.symbol, "window": w.window, "run_id": rid})
        vdir = run / "artifacts" / "variants" / vid
        vdir.mkdir(parents=True, exist_ok=True)
        (vdir / "protocol_result.yaml").write_text(yaml.safe_dump({"results": results}),
                                                   encoding="utf-8")
    return run


def test_variant_bars_missing_and_a_bad_test_are_recorded(tmp_path):
    run = _run_with_variants(tmp_path / "runs", "run_x", {"base": _planted(12, n_windows=2)})
    bad = dict(UP, name="bad", selector={"kind": "moon_phase"})
    doc = cm.measure_variant(run, "base", [UP, bad], None, FAR)
    assert doc["status"] == cm.MEASURED
    assert doc["tests"]["bad"]["status"] == cm.NOT_MEASURED
    assert doc["tests"]["bad"]["reason"] == cm.ERROR
    assert len(doc["bars"]) == 2 and all(len(b["sha256"]) == 64 for b in doc["bars"])
    assert all(b["path"].startswith("variants/base/results/") for b in doc["bars"])
    next((run / "variants" / "base" / "results").glob("*/bars.csv")).unlink()
    gone = cm.measure_variant(run, "base", [UP], None, FAR)
    assert gone["status"] == cm.NOT_MEASURED and gone["reason"] == cm.BARS_MISSING


@pytest.mark.parametrize("card_status,variants,want", [
    ({"usable": False, "reason": "no_claim", "detail": "x"}, {}, ("not_measured", "no_claim")),
    ({"usable": False, "reason": "tests_none", "detail": "x"}, {}, ("not_measured", "tests_none")),
    ({"usable": True}, {}, ("not_measured", "no_graded_variants")),
    ({"usable": True}, {"a": {"status": "not_measured", "reason": "bars_missing", "tests": {}}},
     ("not_measured", "bars_missing")),
    ({"usable": True}, {"a": {"status": "not_measured", "reason": "bars_missing", "tests": {}},
                        "b": {"status": "not_measured", "reason": "error", "tests": {}}},
     ("not_measured", "error")),
], ids=["no_claim", "tests_none", "no_variants", "bars_missing", "error"])
def test_run_status_is_measured_or_not_measured_with_a_reason(card_status, variants, want):
    doc = cm.run_doc("run_1", card_status, variants)
    assert (doc["claim_status"], doc["reason"]) == want
    assert doc["information_only"] is True and doc["n_tests_measured"] == 0


def test_every_test_is_counted_and_recorded_next_to_slice_2s_row(tmp_path):
    variants = {"a": {"status": "measured", "tests": {
        "t1": {"status": "measured", "spec_hash": "h1"},
        "t2": {"status": "not_measured", "reason": "error"}}},
        "b": {"status": "measured", "tests": {"t1": {"status": "measured", "spec_hash": "h1"}}}}
    doc = cm.run_doc("run_1", {"usable": True}, variants)
    assert doc["claim_status"] == "measured"
    assert doc["n_tests_measured"] == 2 and doc["n_tests_not_measured"] == 1
    assert {(c["variant"], c["test"]) for c in doc["tests"]} == {("a", "t1"), ("a", "t2"),
                                                                ("b", "t1")}
    cc.record_coverage(tmp_path, "run_1", {"usable": True, "reason": None})
    cc.record_coverage(tmp_path, "run_2", {"usable": False, "reason": "tests_none"})
    before = "\n".join(cc.coverage_summary_lines(tmp_path))
    assert "measured" not in before
    cm.record_measured(tmp_path, "run_1", doc)
    row = yaml.safe_load((tmp_path / cc.COVERAGE_REL).read_text(encoding="utf-8"))["runs"]["run_1"]
    assert row["usable"] is True and row["measured"]["n_tests_measured"] == 2
    after = cc.coverage_summary_lines(tmp_path)
    assert "\n".join(after[:len(before.splitlines())]) == before        # slice 2 lines unchanged
    assert after[-1] == ("- Claim tests measured after the backtests (effect sizes, measured, "
                         "not proven): 2 test(s) in 1 run(s) (run_1); runs not measured: 0")
    cm.record_measured(tmp_path, "run_3", cm.error_doc("run_3", ValueError("x")))
    last = cc.coverage_summary_lines(tmp_path)
    assert last[-1].endswith("runs not measured: 1")
    assert "None:" not in "\n".join(last)                     # a measured-only row is no card gap


# ---------------------------------------------------------------------------
# 4. run_phase1_research wiring
# ---------------------------------------------------------------------------

def _fixture_run(run_id: str, claim=None, variants=None) -> Path:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    _run_with_variants(rpr.ROOT / "runs", run_id,
                       variants if variants is not None else {"base": _planted(13, n_windows=2)})
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml",
                  dict(CARD, **({"claim": claim} if claim is not None else {})))
    rpr.save_yaml(run_dir / "artifacts" / "idea_status.yaml", {"idea_status": "refuted"})
    rpr.save_yaml(run_dir / "artifacts" / "grid_evaluation.yaml", {"result": "FAIL"})
    return run_dir


def _tree(root: Path) -> dict:
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


@pytest.mark.parametrize("orch", [None, {"config_direct_authoring": {"enabled": True}},
                                  {"config_direct_authoring": {"enabled": True},
                                   "claim_tests": {"enabled": False}}],
                         ids=["no_config", "cda_only", "explicit_off"])
def test_flag_off_reads_and_writes_nothing(orch, monkeypatch):
    _set_orchestrator(orch)
    run_dir = _fixture_run("run_960", claim=_claim([UP]))
    stale = run_dir / "artifacts" / "claim_status.yaml"
    stale.write_text("stale\n", encoding="utf-8")
    before = _tree(rpr.ROOT)
    monkeypatch.setattr(rpr, "_claim_measure_module", lambda: pytest.fail("flag off"))
    monkeypatch.setattr(rpr, "load_yaml", lambda *a, **k: pytest.fail("nothing read"))
    rpr._measure_claim_tests_after_backtests(run_dir, "run_960")
    assert _tree(rpr.ROOT) == before


def test_flag_on_writes_measured_files_and_counts_them():
    _set_orchestrator(ON)
    run_dir = _fixture_run("run_961", claim=_claim([UP, REGIME_T]),
                           variants={"base": _planted(14, n_windows=2),
                                     "other": _planted(15, n_windows=2)})
    keep = {n: (run_dir / "artifacts" / n).read_bytes()
            for n in ("idea_status.yaml", "grid_evaluation.yaml", "hypothesis_card.yaml")}
    rpr._measure_claim_tests_after_backtests(run_dir, "run_961")
    for n, b in keep.items():                                   # never read into the grid
        assert (run_dir / "artifacts" / n).read_bytes() == b
    st = rpr.load_yaml(run_dir / "artifacts" / "claim_status.yaml")
    assert st["claim_status"] == "measured" and st["n_tests_measured"] == 4
    assert st["variants"]["base"]["file"] == "variants/base/claim_test.yaml"
    v = rpr.load_yaml(run_dir / "artifacts" / "variants" / "base" / "claim_test.yaml")
    assert v["status"] == "measured" and set(v["tests"]) == {"high_forecast", "trend_label"}
    assert v["tests"]["high_forecast"]["horizons"][1]["value"] > 0
    _no_verdict(st)
    _no_verdict(v)
    cov = rpr.load_yaml(rpr.ROOT / cc.COVERAGE_REL)["runs"]["run_961"]["measured"]
    assert cov["claim_status"] == "measured" and cov["n_tests_measured"] == 4


@pytest.mark.parametrize("claim,reason", [(None, "no_claim"),
                                          ("tests_none", "tests_none"),
                                          ({"broken": True}, "invalid_claim")])
def test_flag_on_card_gaps_are_not_measured_with_the_reason(claim, reason):
    _set_orchestrator(ON)
    if claim == "tests_none":
        claim = dict(_claim([UP]), tests="none", missing_block="fwd_return_of")
    run_dir = _fixture_run("run_962", claim=claim)
    rpr._measure_claim_tests_after_backtests(run_dir, "run_962")
    st = rpr.load_yaml(run_dir / "artifacts" / "claim_status.yaml")
    assert st["claim_status"] == "not_measured" and st["reason"] == reason
    assert not list((run_dir / "artifacts" / "variants").glob("*/claim_test.yaml"))


def _boom(*a, **k):
    raise RuntimeError("injected")


@pytest.mark.parametrize("target", [
    "card_read", "check_claim", "holdout_range", "eras", "graded_variants", "load_bars",
    "effect_sizes", "variant_write", "run_doc", "coverage_write"])
def test_an_error_at_each_step_never_escapes(target, monkeypatch):
    _set_orchestrator(ON)
    run_dir = _fixture_run("run_963", claim=_claim([UP]))
    import protocol_resolution as pres
    real_save = rpr.save_yaml
    patches = {
        "card_read": (rpr, "load_yaml", _boom),
        "check_claim": (cc, "check_claim", _boom),
        "holdout_range": (rpr, "_load_holdout_range", _boom),
        "eras": (pres, "load_policy_eras", _boom),
        "graded_variants": (ct, "graded_variants", _boom),
        "load_bars": (ct, "load_variant_bars", _boom),
        "effect_sizes": (ct, "effect_sizes", _boom),
        "variant_write": (rpr, "save_yaml", lambda p, d, *a, **k: _boom()
                          if Path(p).name == cm.VARIANT_FILE else real_save(p, d, *a, **k)),
        "run_doc": (cm, "run_doc", _boom),
        "coverage_write": (cm, "record_measured", _boom),
    }
    mod, name, fn = patches[target]
    monkeypatch.setattr(mod, name, fn)
    rpr._measure_claim_tests_after_backtests(run_dir, "run_963")       # never raises
    st = rpr.load_yaml(run_dir / "artifacts" / "claim_status.yaml") \
        if target != "card_read" else yaml.safe_load(
            (run_dir / "artifacts" / "claim_status.yaml").read_text(encoding="utf-8"))
    assert st["claim_status"] == "not_measured" and st["reason"] == "error"
    assert "injected" in st["detail"]


def test_the_safety_net_itself_never_raises(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _fixture_run("run_964", claim=_claim([UP]))
    monkeypatch.setattr(ct, "graded_variants", _boom)
    monkeypatch.setattr(rpr, "save_yaml", _boom)
    monkeypatch.setattr(cm, "record_measured", _boom)
    rpr._measure_claim_tests_after_backtests(run_dir, "run_964")
    monkeypatch.setattr(rpr, "_claim_measure_module", _boom)
    rpr._measure_claim_tests_after_backtests(run_dir, "run_964")


def test_previous_attempt_files_are_cleared_only_with_the_flag_on():
    run_dir = _fixture_run("run_965", claim=_claim([UP]))
    files = [run_dir / "artifacts" / "claim_status.yaml",
             run_dir / "artifacts" / "variants" / "base" / "claim_test.yaml"]
    for p in files:
        p.write_text("stale\n", encoding="utf-8")
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    rpr._clear_claim_measure_files(run_dir)
    assert all(p.exists() for p in files)
    _set_orchestrator(ON)
    rpr._clear_claim_measure_files(run_dir)
    assert not any(p.exists() for p in files)
    assert (run_dir / "artifacts" / "idea_status.yaml").exists()


def test_the_two_seams_are_wired_after_the_backtests():
    """The clear runs at protocol_execution entry (tool worker); the measurement
    runs in run_loop after protocol_execution, never inside the grid."""
    import inspect
    worker = inspect.getsource(rpr.run_tool_worker)
    assert 'if stage_name == "protocol_execution":\n        _clear_claim_measure_files(RUN_DIR)' \
        in worker
    loop = inspect.getsource(rpr.run_loop)
    assert ('if current_stage == "protocol_execution":\n'
            '                _measure_claim_tests_after_backtests(RUN_DIR, run_id)') in loop
    grid = inspect.getsource(rpr._build_idea_status_artifact)
    assert "claim" not in grid


# ---------------------------------------------------------------------------
# 5. the offline tool's calibration lock (kept in this slice)
# ---------------------------------------------------------------------------

def test_calibration_lock_compares_outcome_selector_and_number_of_fakes(tmp_path):
    ws = make_windows(16, n=60, n_windows=1)
    s = spec(EVENT)

    def found(**kw):
        p = tmp_path / "c.yaml"
        p.write_text(yaml.safe_dump(passed_summary(DON, "mean_diff", **kw)))
        return ct.calibration_for(ct.passed_calibrations([p]), s, ws)

    assert found() is not None
    assert found(outcome="fwd_max_drawdown") is None
    assert found(outcome=None) is None                       # unstated: matches nothing
    assert found(selector="regime") is None
    assert found(selector=None) is None
    assert found(selector=dict(EVENT)) is not None           # a whole selector, equal
    assert found(selector=dict(EVENT, value=-12)) is None    # a whole selector, other value
    assert found(n_null=FAST["n_resamples"] + 1) is None
    assert found(n_null=None) is not None                    # helper default = the spec's N


def test_the_published_run065_gate_no_longer_unlocks_its_1000_fakes_grade():
    """REGRADE_run065.md: the grade drew 1,000 fakes, the gate 199 (and stated
    no outcome kind). Under the stricter lock it would read 'not calibrated'."""
    e068 = SR_ROOT / "engineering" / "roadmap" / "E-068"
    summary = e068 / "calibration_a5" / "summary_block_permutation_v1_onesided.yaml"
    doc = yaml.safe_load((e068 / "regrade_specs" / "run_065_breakout_continuation.yaml")
                         .read_text(encoding="utf-8"))
    t = ct.TestSpec.from_dict(doc["tests"][0])
    assert t.significance["n_resamples"] == 1000
    passed = ct.passed_calibrations([summary])
    assert len(passed) == 1 and passed[0]["scope"]["n_null"] == 199
    ws = make_windows(17, n=60, n_windows=1)
    for w in ws:
        w.signal = passed[0]["scope"]["signal"]
    assert ct.calibration_for(passed, t, ws) is None
