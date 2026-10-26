"""D-193: the optional test key `signal` (default "forecast"), run_101's finding that the analyst
could see each component's sub-forecast columns in bars.csv but could not test them.

Declared tool change, no flag (D-143 precedent). Covers: the default leaves every hash, block, log
entry and measured number byte-identical to before the key existed (golden values were computed
with the code of master cdb5a424); a component column changes the forecast array abs_forecast,
forecast_sign_change, rank_ic and the selectors read; the allowed values come from the data
dictionary's Unit column; refusals ("no component <id> in this variant", a column that is not of
unit forecast, a trade test, a vehicle that removes the component); the key survives the pasted
test block (claim card, claim_measure, claim_findings, the card schema) and the analyst's derived
columns honour it; the prompt line for the card's horizon_bars. Synthetic data only (2020 dates).
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import analyst_queries as aq  # noqa: E402
import analyst_session as asm  # noqa: E402
import claim_card as cc  # noqa: E402
import claim_findings as cf  # noqa: E402
import claim_measure as cm  # noqa: E402
import claim_tests as ct  # noqa: E402

import test_e075_pr5_analyst as q5  # noqa: E402

T0 = 1577836800            # 2020-01-01 00:00 UTC
HOUR = 3600
N = 130
HOLDOUT = "2021-01-01"
C1_POST = "debug_info.components.c1.post_pipeline_value"
C1_WC = "debug_info.components.c1.weighted_contribution"
C1_WN = "debug_info.components.c1.weight_normalized"
C9_POST = "debug_info.components.c9.post_pipeline_value"
WINDOWS = [("R1", "AAA", "w0", 0, 11), ("R2", "AAA", "w1", 24 * 31, 12)]

COLS = ["timestamp", "open", "high", "low", "close", "volume", "forecast", "regime",
        C1_POST, C1_WC, C1_WN, "debug_info.forecast_delta"]


def stamp(t):
    return np.datetime64(int(t), "s").astype(str).replace("T", " ")


def make_run(root: Path, vid="base") -> Path:
    """A synthetic run: two hourly windows of one coin. The component columns are independent
    of `forecast`, so a test on one cannot give the other's number."""
    root = Path(root)
    results = []
    for rid, sym, win, off, seed in WINDOWS:
        rng = np.random.default_rng(seed)
        c = 100.0 * np.exp(np.cumsum(0.004 * rng.standard_normal(N)))
        fc = np.round(6.0 * rng.standard_normal(N), 4)
        post = np.round(7.0 * rng.standard_normal(N), 4)
        ts = T0 + off * HOUR + np.arange(N) * HOUR
        regime = np.where(np.arange(N) % 3 == 0, "trending", "chop")
        res = root / "variants" / vid / "results" / rid
        res.mkdir(parents=True)
        lines = [",".join(COLS)]
        for i in range(N):
            lines.append(",".join(str(v) for v in (
                stamp(ts[i]), c[i], c[i] * 1.002, c[i] * 0.998, c[i], 10 + (i % 7), fc[i],
                regime[i], post[i], round(0.5 * post[i], 6), 0.5, round(fc[i] / 3, 6))))
        (res / "bars.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
        results.append({"run_id": rid, "symbol": sym, "window": win})
    art = root / "artifacts" / "variants" / vid
    art.mkdir(parents=True)
    (art / "protocol_result.yaml").write_text(yaml.safe_dump({"results": results}),
                                              encoding="utf-8")
    return root


@pytest.fixture()
def run(tmp_path):
    return make_run(tmp_path / "run_001")


def engine(run, **kw):
    kw.setdefault("holdout_start", HOLDOUT)
    kw.setdefault("comparison_budget", 10 ** 9)
    kw.setdefault("log_path", Path(run).parent / (Path(run).name + "_log.yaml"))
    return aq.QueryEngine(run, **kw)


def bars(run, rid="R1"):
    return Path(run) / "variants" / "base" / "results" / rid / "bars.csv"


def column(run, name, rid="R1"):
    import csv
    with open(bars(run, rid), newline="", encoding="utf-8") as f:
        return np.array([float(r[name]) for r in csv.DictReader(f)])


COND = {"kind": "event", "field": "forecast", "op": ">=", "value": 3.0}
TEST = {"selector": COND, "outcome": {"kind": "fwd_return", "horizons": [1, 3]},
        "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "greater",
        "floor": {"min_events": 5}}


def windows_of(run):
    return ct.load_variant_bars(Path(run), "base")


def _canon_hash(test):
    """The spec hash as it was computed before D-193: the same canonical JSON over the nine
    fields the TestSpec then had (no `signal` key)."""
    d = {"selector": test["selector"], "outcome": dict(test["outcome"], horizons=sorted(
        test["outcome"]["horizons"])), "baseline": test["baseline"],
        "statistic": test["statistic"], "direction": test["direction"], "floor": test["floor"],
        "alpha": 0.05, "consistency": None, "significance": dict(ct.DEFAULT_SIGNIFICANCE)}
    return hashlib.sha256(json.dumps(ct._canon(d), sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# 1. Default unused: byte-identical
# ---------------------------------------------------------------------------

# computed with the code of master cdb5a424 on the fixture above (conditional_effect on COND,
# horizons [1, 3], by=None, the default floor), before this change
GOLDEN_RESULT_SHA256 = "1b2d013ccb3c27df6495cdccfae7d796fd11f8b2ed31dfacb2ac9b1bc3e5c894"
GOLDEN_SPEC_HASH = "4c67e97c8c8d4c281512bbb9a46fc5c168684ae1eb923e33664ef0e2d0940cb2"


def test_the_default_signal_is_not_part_of_a_tests_identity():
    base = ct.TestSpec.from_dict(dict(TEST))
    assert base.signal == "forecast"
    assert ct.spec_hash(base) == _canon_hash(TEST)
    assert ct.spec_hash(ct.TestSpec.from_dict(dict(TEST, signal="forecast"))) == _canon_hash(TEST)
    other = ct.TestSpec.from_dict(dict(TEST, signal=C1_POST))
    assert ct.spec_hash(other) != _canon_hash(TEST)
    assert ct.spec_hash(ct.TestSpec.from_dict(dict(TEST, signal=C1_WC))) != ct.spec_hash(other)


def test_a_call_without_signal_logs_and_answers_exactly_as_before(run, tmp_path):
    e1 = engine(run, log_path=tmp_path / "l1.yaml")
    r1 = e1.conditional_effect(COND, horizons=[1, 3], floor=TEST["floor"])
    e2 = engine(run, log_path=tmp_path / "l2.yaml")
    r2 = e2.conditional_effect(COND, horizons=[1, 3], floor=TEST["floor"], signal="forecast")
    e3 = engine(run, log_path=tmp_path / "l3.yaml")
    r3 = e3.conditional_effect(COND, horizons=[1, 3], floor=TEST["floor"], signal=None)
    for r in (r1, r2, r3):
        assert r["status"] == "ok"
        assert "signal" not in r["result"]["test"]
        assert r["result"]["spec_hash"] == GOLDEN_SPEC_HASH
    entries = [e.log.entries()[0] for e in (e1, e2, e3)]
    for ent in entries:
        assert "signal" not in ent["params"]
        assert ent["result_sha256"] == GOLDEN_RESULT_SHA256
    assert entries[0] == entries[1] == entries[2]


def test_describe_and_distribution_without_signal_log_no_signal_key(run, tmp_path):
    e = engine(run, log_path=tmp_path / "l.yaml")
    d = e.describe("abs_forecast")
    e.distribution("forecast_sign_change", signal="forecast")
    assert "signal" not in d["result"]
    for ent in e.log.entries():
        assert "signal" not in ent["params"] and "signal" not in ent["result"]


def test_default_windows_and_effect_sizes_are_unchanged(run):
    w = ct.read_bars_csv(bars(run), "AAA", "w0")
    assert w.forecast_column == "forecast"
    np.testing.assert_array_equal(w.forecast, column(run, "forecast"))
    ws = windows_of(run)
    spec = ct.TestSpec.from_dict(dict(TEST))
    explicit = ct.TestSpec.from_dict(dict(TEST, signal="forecast"))
    a = ct.effect_sizes(ws, spec)[1]
    b = ct.effect_sizes(ws, explicit)[1]
    assert a == b


# ---------------------------------------------------------------------------
# 2. The signal is the forecast array every selector and statistic reads
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("sig", [C1_POST, C1_WC])
def test_the_window_reads_the_signal_column_as_its_forecast(run, sig):
    w = ct.read_bars_csv(bars(run), "AAA", "w0", signal=sig)
    np.testing.assert_array_equal(w.forecast, column(run, sig))
    assert w.forecast_column == sig
    # the derived bar-t functions inherit it unchanged
    np.testing.assert_array_equal(ct.abs_forecast(w), np.abs(column(run, sig)))
    sc = ct.forecast_sign_change(w)
    f = column(run, sig)
    want = (f[1:] * f[:-1] < 0).astype(float)
    np.testing.assert_array_equal(sc[1:], want)
    assert np.isnan(sc[0])
    assert not np.array_equal(w.forecast, column(run, "forecast"))


@pytest.mark.parametrize("statistic,baseline", [("rank_ic", None),
                                                ("mean_diff", {"kind": "complement"})])
def test_effect_sizes_with_a_signal_equal_reading_the_windows_with_it(run, statistic, baseline):
    ws = windows_of(run)
    ws_sig = [ct.read_bars_csv(bars(run, rid), sym, win, signal=C1_POST)
              for rid, sym, win, _o, _s in WINDOWS]
    test = dict(TEST, statistic=statistic, baseline=baseline,
                selector={"kind": "event", "field": "abs_forecast", "op": ">=", "value": 5.0})
    got = ct.effect_sizes(ws, ct.TestSpec.from_dict(dict(test, signal=C1_POST)))[1]
    want = ct.effect_sizes(ws_sig, ct.TestSpec.from_dict(test))[1]
    default = ct.effect_sizes(ws, ct.TestSpec.from_dict(test))[1]
    assert got == want
    assert got != default


def test_a_selector_on_the_forecast_field_reads_the_signal(run):
    ws = windows_of(run)
    spec = ct.TestSpec.from_dict(dict(TEST, signal=C1_POST))
    per = ct.effect_sizes(ws, spec)[0]
    for p, (rid, *_rest) in zip(per, WINDOWS):
        np.testing.assert_array_equal(p["fc"], column(run, C1_POST, rid))
        np.testing.assert_array_equal(p["mask"], column(run, C1_POST, rid) >= 3.0)


def test_forecast_sign_change_selector_uses_the_signal(run):
    ws = windows_of(run)
    test = dict(TEST, selector={"kind": "event", "field": "forecast_sign_change", "op": ">=",
                                "value": 1.0})
    per = ct.effect_sizes(ws, ct.TestSpec.from_dict(dict(test, signal=C1_WC)))[0]
    f = column(run, C1_WC)
    np.testing.assert_array_equal(per[0]["mask"][1:], f[1:] * f[:-1] < 0)


def test_a_verdict_under_method_b_on_another_signal_is_refused(run):
    ws = windows_of(run)
    spec = ct.TestSpec.from_dict(dict(TEST, signal=C1_POST))
    with pytest.raises(ValueError, match="builds its null from"):
        ct._graded({}, *ct.effect_sizes(ws, spec), ws, spec, None)


# ---------------------------------------------------------------------------
# 3. Allowed values come from the data dictionary
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("sig", ["forecast", C1_POST, C1_WC, "debug_info.components.zz.post_pipeline_value"])
def test_forecast_unit_columns_are_allowed(sig):
    assert ct.signal_errors(sig) == []
    assert ct.check_spec(ct.TestSpec.from_dict(dict(TEST, signal=sig))) == []


@pytest.mark.parametrize("sig", [C1_WN, "close", "regime", "no_such_column", "", None, 3,
                                 "debug_info.components.c1.last_history_value"])
def test_other_columns_are_refused(sig):
    errs = ct.check_spec(ct.TestSpec.from_dict(dict(TEST, signal=sig)))
    assert errs and all(e.startswith("signal:") for e in errs)


def test_the_allowed_values_are_read_from_the_dictionary_not_a_list(monkeypatch):
    rows = list(aq.load_bars_dictionary()) + [
        {"field": "debug_info.novel_score", "meaning": "x", "unit": "forecast", "when": "close",
         "role": "feature", "pattern": None}]
    monkeypatch.setitem(ct._DICTIONARY_CACHE, "rows", rows)
    assert ct.signal_errors("debug_info.novel_score") == []
    rows[-1] = dict(rows[-1], unit="score")
    assert ct.signal_errors("debug_info.novel_score")


def test_a_forecast_unit_column_known_only_after_the_bar_is_refused(monkeypatch):
    rows = list(aq.load_bars_dictionary()) + [
        {"field": "debug_info.hindsight", "meaning": "x", "unit": "forecast", "when": "after",
         "role": "outcome", "pattern": None}]
    monkeypatch.setitem(ct._DICTIONARY_CACHE, "rows", rows)
    assert ct.signal_errors("debug_info.hindsight")


def test_a_trade_test_takes_no_signal():
    trade = {"selector": {"kind": "trade", "where": [{"field": "side", "op": "==",
                                                      "value": "long"}]},
             "outcome": {"kind": "trade_net_return"}, "baseline": {"kind": "other_trades"},
             "statistic": "mean_diff", "direction": "greater", "floor": {"min_events": 5}}
    assert ct.check_spec(ct.TestSpec.from_dict(trade), trade_tests=True) == []
    errs = ct.check_spec(ct.TestSpec.from_dict(dict(trade, signal=C1_POST)), trade_tests=True)
    assert errs and "only a bar test takes a signal" in errs[0]


# ---------------------------------------------------------------------------
# 4. An absent component is refused with the exact text
# ---------------------------------------------------------------------------

def test_the_engine_refuses_an_absent_component_with_the_exact_text(run):
    e = engine(run)
    r = e.conditional_effect(COND, horizons=[1], signal=C9_POST)
    assert r["status"] == "refused"
    assert r["reason"] == "no component c9 in this variant"
    d = e.describe("abs_forecast", signal=C9_POST)
    assert d["status"] == "refused" and d["reason"] == "no component c9 in this variant"
    # the refused calls are in the log, with the signal they named
    assert [x["params"]["signal"] for x in e.log.entries()] == [C9_POST, C9_POST]


def test_the_window_reader_refuses_an_absent_component_with_the_exact_text(run):
    with pytest.raises(ValueError) as exc:
        ct.read_bars_csv(bars(run), "AAA", "w0", signal=C9_POST)
    assert str(exc.value) == "no component c9 in this variant"
    w = ct.read_bars_csv(bars(run), "AAA", "w0")
    with pytest.raises(ValueError, match="no component c9 in this variant"):
        ct.window_with_signal(w, C9_POST)


def test_the_engine_refuses_a_signal_that_is_not_a_forecast_column(run):
    r = engine(run).conditional_effect(COND, horizons=[1], signal=C1_WN)
    assert r["status"] == "refused" and "signal:" in r["reason"]


# ---------------------------------------------------------------------------
# 5. The claim card refuses a component its own vehicle removes
# ---------------------------------------------------------------------------

def claim_with(signal, **over):
    t = {"name": "t1", **TEST, "signal": signal}
    c = {"statement": "s", "kind": "conditional_behaviour", "tests": [t], "pass_if": "p",
         "fail_if": "f", "rationale": "r"}
    c.update(over)
    return c


BASE_CONFIG = {"strategies": {"regimes": {"r": {"components": [
    {"id": "c1", "weight": 1.0}, {"id": "c2", "weight": 1.0}]}}}}


def test_the_claim_card_accepts_a_valid_signal_and_refuses_an_invalid_one():
    ok = cc.check_claim(claim_with(C1_POST))
    assert ok.errors == [] and ok.tests[0]["verdict_possible"] is True
    assert ok.tests[0]["spec_hash"] == ct.spec_hash(ct.TestSpec.from_dict(
        dict(TEST, signal=C1_POST)))
    default = cc.check_claim(claim_with("forecast"))
    assert default.tests[0]["spec_hash"] == _canon_hash(TEST)
    bad = cc.check_claim(claim_with(C1_WN))
    assert bad.errors and "signal:" in bad.errors[0]
    plain = {k: v for k, v in claim_with("forecast")["tests"][0].items() if k != "signal"}
    assert cc.check_claim(claim_with("forecast", tests=[plain])).errors == []


def test_a_vehicle_that_zeroes_the_weight_removes_the_component():
    vehicle = [{"component_id": "c1", "field": "weight", "before": 1.0, "after": 0}]
    errs = cc.vehicle_signal_errors(claim_with(C1_POST), vehicle)
    assert len(errs) == 1 and "claim.tests[0].signal" in errs[0] and "'c1'" in errs[0]
    assert "removes" in errs[0]
    # a component the vehicle keeps, a signal on `forecast`, and a different change: no error
    assert cc.vehicle_signal_errors(claim_with(C1_POST), [
        {"component_id": "c2", "field": "weight", "before": 1.0, "after": 0}]) == []
    assert cc.vehicle_signal_errors(claim_with(C1_POST), [
        {"component_id": "c1", "field": "weight", "before": 1.0, "after": 2.0}]) == []
    assert cc.vehicle_signal_errors(claim_with("forecast"), vehicle) == []


def test_a_config_vehicle_that_drops_the_component_removes_it():
    kept = {"strategies": {"regimes": {"r": {"components": [{"id": "c2", "weight": 1.0}]}}}}
    vehicle = {"kind": "config", "config": kept}
    errs = cc.vehicle_signal_errors(claim_with(C1_WC), vehicle, BASE_CONFIG)
    assert len(errs) == 1 and "'c1'" in errs[0]
    assert cc.vehicle_signal_errors(claim_with("debug_info.components.c2.post_pipeline_value"),
                                    vehicle, BASE_CONFIG) == []
    zero = {"kind": "config", "config": {"strategies": {"regimes": {"r": {"components": [
        {"id": "c1", "weight": 0}, {"id": "c2", "weight": 1.0}]}}}}}
    assert cc.vehicle_signal_errors(claim_with(C1_POST), zero)       # no base config needed
    assert cc.vehicle_signal_errors(claim_with(C1_POST), vehicle) == []   # absent: needs the base


def test_the_analyst_answer_check_applies_the_claim_card_refusal():
    vehicle = [{"component_id": "c1", "field": "weight", "before": 1.0, "after": 0}]
    claim = {"tests": [{"name": "t", **TEST, "signal": C1_POST}]}
    text = q5._claim_answer(claim=claim, vehicle=vehicle)
    errors = q5._check(text)
    assert [e for e in errors if "which this claim's own vehicle removes" in e]
    text = q5._claim_answer(claim=claim, vehicle=[{"component_id": "c2", "field": "weight",
                                                   "before": 1.0, "after": 0}])
    assert not [e for e in q5._check(text) if "vehicle removes" in e]


# ---------------------------------------------------------------------------
# 6. The key survives the pasted test block
# ---------------------------------------------------------------------------

def test_the_pasted_block_carries_the_signal_and_a_child_re_runs_it_on_the_same_column(run):
    e = engine(run)
    r = e.conditional_effect(COND, horizons=[1, 3], floor=TEST["floor"], signal=C1_POST)
    assert r["status"] == "ok", r
    res = r["result"]
    block = res["test"]
    assert block["signal"] == C1_POST
    assert res["compiles_as_claim"] is True
    assert block["name"] == "cond_" + res["spec_hash"][:10]
    assert res["spec_hash"] != GOLDEN_SPEC_HASH
    # the card tool, the child's measurement and the findings record all read the same key
    errs, h, possible = cc._check_test(block, "test", True)
    assert errs == [] and h == res["spec_hash"] and possible
    spec, h2 = cm.test_spec(block, True)
    assert spec.signal == C1_POST and h2 == res["spec_hash"]
    measured = cm.measure_test(windows_of(run), block, None)
    assert measured["status"] == cm.MEASURED
    for hz, cell in res["horizons"].items():
        assert measured["horizons"][int(hz)]["value"] == pytest.approx(cell["effect"], abs=1e-7)
    (t,) = cf._tests_of({"tests": [block]})
    assert t["spec"]["signal"] == C1_POST and t["spec_hash"] == res["spec_hash"]
    # and the answer's own signal-less block is the same shape as before
    plain = e.conditional_effect(COND, horizons=[1, 3], floor=TEST["floor"])["result"]["test"]
    (tp,) = cf._tests_of({"tests": [plain]})
    assert "signal" not in tp["spec"]


def test_the_signal_changes_the_measured_number(run):
    e = engine(run)
    a = e.conditional_effect(COND, horizons=[1, 3], floor=TEST["floor"])["result"]["horizons"]
    b = e.conditional_effect(COND, horizons=[1, 3], floor=TEST["floor"], signal=C1_POST)["result"]["horizons"]
    assert a != b


def test_the_card_schema_allows_the_optional_signal():
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((SR_ROOT / "workflow_artifacts/schemas/hypothesis_card.schema.json")
                        .read_text(encoding="utf-8"))
    sub = {"$ref": "#/$defs/claim_test", "$defs": schema["$defs"]}
    base = {"name": "t", **TEST}
    jsonschema.validate(base, sub)
    jsonschema.validate(dict(base, signal=C1_POST), sub)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(dict(base, signal=5), sub)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(dict(base, signall="x"), sub)


def test_the_memory_view_and_digests_show_the_signal_only_when_written():
    import analyst_memory_view as amv
    with_sig = amv._specs([{"spec_hash": "h", "spec": dict(TEST, signal=C1_POST)}])
    without = amv._specs([{"spec_hash": "h", "spec": dict(TEST)}])
    assert with_sig[0]["signal"] == C1_POST and "signal" not in without[0]


# ---------------------------------------------------------------------------
# 7. The analyst's derived columns take the key
# ---------------------------------------------------------------------------

def test_describe_and_distribution_of_a_derived_column_honour_the_signal(run):
    e = engine(run)
    f = np.concatenate([column(run, C1_POST, rid) for rid, *_r in WINDOWS])
    d = e.describe("abs_forecast", signal=C1_POST)
    assert d["status"] == "ok" and d["result"]["signal"] == C1_POST
    assert d["result"]["groups"]["all"]["mean"] == pytest.approx(float(np.abs(f).mean()), abs=1e-6)
    plain = e.describe("abs_forecast")["result"]["groups"]["all"]["mean"]
    assert plain != d["result"]["groups"]["all"]["mean"]
    s = e.describe("forecast_sign_change", signal=C1_WC)
    sc = []
    for rid, *_r in WINDOWS:
        g = column(run, C1_WC, rid)
        sc += [x for x in (g[1:] * g[:-1] < 0).astype(float)]
    assert s["result"]["groups"]["all"]["mean"] == pytest.approx(float(np.mean(sc)), abs=1e-6)
    dist = e.distribution("abs_forecast", signal=C1_POST, bins=5)
    assert dist["status"] == "ok" and dist["result"]["signal"] == C1_POST
    assert sum(dist["result"]["groups"]["all"]) == len(f)


def test_a_signal_on_a_column_that_is_not_derived_from_the_forecast_is_refused(run):
    r = engine(run).describe("close", signal=C1_POST)
    assert r["status"] == "refused" and "signal applies to" in r["reason"]


# ---------------------------------------------------------------------------
# 8. The analyst prompt: the card's horizon_bars, information only
# ---------------------------------------------------------------------------

def _context(run, card):
    arts = Path(run) / "artifacts"
    if card is not None:
        (arts / "hypothesis_card.yaml").write_text(card, encoding="utf-8")
    return asm.run_context(Path(run), "artifacts/base_config.json", "A")


def test_the_prompt_names_the_cards_horizon_bars(run):
    text = _context(run, yaml.safe_dump({"statement": {"predicts": "x",
                                                       "predicts_kind": "return_direction",
                                                       "horizon_bars": 24}}))
    assert "Hypothesis horizon: 24 bars" in text
    assert text.count("Hypothesis horizon") == 1


@pytest.mark.parametrize("card", [None, "claim: {}\n", yaml.safe_dump({"statement": {"predicts": "x"}}),
                                  yaml.safe_dump({"statement": {"horizon_bars": "soon"}}),
                                  yaml.safe_dump({"statement": {"horizon_bars": True}}),
                                  yaml.safe_dump({"statement": {"horizon_bars": 0}}),
                                  ": : not yaml [", "- a list\n"])
def test_no_horizon_line_when_the_card_has_none_and_nothing_else_changes(run, card):
    baseline = _context(run, None)
    text = _context(run, card)
    assert "Hypothesis horizon" not in text
    assert text == baseline


def test_the_skill_names_the_horizon_comparison_and_the_signal_key():
    skill = (SR_ROOT / "workflow_artifacts/skills/analyst/SKILL.md").read_text(encoding="utf-8")
    flat = " ".join(skill.split())
    assert "`median_holding_bars`" in flat and "Hypothesis horizon" in flat
    assert "information only, with no bar, gate or refusal" in flat
    assert "optional `signal`, default `forecast`" in flat
    assert "debug_info.components.<id>.post_pipeline_value" in flat
    assert "debug_info.components.<id>.weighted_contribution" in flat
