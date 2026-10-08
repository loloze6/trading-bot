"""D-091 (E-075 PR-5a, CUL-424): the trade-level claim-test family (D-086) reaches the
pipeline under orchestrator.analyst.enabled (off by default).

Before this, only a caller passing `trade_tests=True` accepted a trade test, and no pipeline
caller did. So a trade-efficiency analyst's claim was refused at decide-next and at step
1a's card check, never measured in the child, and `not_measurable` at fold confirmation.
Under the flag every one of those places accepts and measures it; flag off, every call is
exactly as before.
"""
from __future__ import annotations

import ast
import copy
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import claim_measure as cmeas  # noqa: E402
import decide_next as dn  # noqa: E402
import explore_confirm as ec  # noqa: E402
import fold_confirm as fc  # noqa: E402
import reader_findings as rfi  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

import test_e077_pr2_confirm as base  # noqa: E402  (fold-B fixtures: _build, _confirm, ...)

COINS = ("BTCUSD", "ETHUSD", "XRPUSD")
TRADE_TEST = {"name": "longs_beat_shorts",
              "selector": {"kind": "trade", "where": [{"field": "side", "op": "==", "value": "long"}]},
              "outcome": {"kind": "trade_net_return"}, "baseline": {"kind": "other_trades"},
              "statistic": "mean_diff", "direction": "greater", "floor": {"min_events": 4}}
EMPTY = {"vehicle": [], "combines_as": "execution_rule", "fold_observed": "A"}


def _claim(kind="execution_behaviour", test=None):
    return {"statement": "Long lots of this strategy earn more than its short lots.",
            "kind": kind, "tests": [copy.deepcopy(test or TRADE_TEST)],
            "pass_if": "long lots above the others", "fail_if": "not above",
            "rationale": "the strategy's longs ride the drift"}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# the flag and the one keyword helper
# ---------------------------------------------------------------------------

def test_the_flag_reader():
    on = {"orchestrator": {"analyst": {"enabled": True}, "folds": {"enabled": True}}}
    assert rpr._analyst_enabled({}) is False
    assert rpr._analyst_enabled(on) is True
    for bad in ("true", None, 1):
        with pytest.raises(ValueError, match="orchestrator.analyst.enabled"):
            rpr._analyst_enabled({"orchestrator": {"analyst": {"enabled": bad}}})


def test_the_flag_requires_folds():
    """Review of #358: without folds a trade claim of a plain kind would be routed in-run by
    E-072 and fail there; the analyst's claims are confirmed on folds only."""
    with pytest.raises(ValueError, match="requires orchestrator.folds.enabled=true"):
        rpr._analyst_enabled({"orchestrator": {"analyst": {"enabled": True}}})
    assert rpr._analyst_enabled({"orchestrator": {"analyst": {"enabled": False}}}) is False


@pytest.mark.parametrize("folds,analyst,want", [
    (False, False, {}), (True, False, {"folds": True}), (False, True, {"trade_tests": True}),
    (True, True, {"folds": True, "trade_tests": True})])
def test_the_claim_check_keywords(monkeypatch, folds, analyst, want):
    monkeypatch.setattr(rpr, "_folds_enabled", lambda *a: folds)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: analyst)
    assert rpr._claim_check_kw() == want


def test_every_claim_check_of_the_orchestrator_takes_the_keywords():
    """Static: each check_claim / side_finding_review / reading_structure /
    side_finding_merges call in run_phase1_research passes **_claim_check_kw(), so the
    1a card checks, the claim measurement's check and the reading checks all see the flag."""
    tree = ast.parse((SR_ROOT / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8"))
    names = {"check_claim", "side_finding_review", "reading_structure", "side_finding_merges"}
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Attribute) and n.func.attr in names]
    assert len(calls) == 9
    for c in calls:
        star = [k.value for k in c.keywords if k.arg is None]
        assert any(isinstance(v, ast.Call) and getattr(v.func, "id", None) == "_claim_check_kw"
                   for v in star), ast.unparse(c)
    direct = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
              and getattr(n.func, "id", None) == "_claim_check_folds"]
    assert len(direct) == 1                                  # only inside _claim_check_kw


# ---------------------------------------------------------------------------
# the checks: reading, merges, decide-next, E-072's route
# ---------------------------------------------------------------------------

def test_side_finding_review_accepts_a_trade_claim_only_with_the_family():
    item = {"claim": _claim()}
    on = rfi.side_finding_review(item, prior={}, own=set(), run_id="r", folds=True, trade_tests=True)
    assert on["errors"] == [] and len(on["spec_hashes"]) == 1
    off = rfi.side_finding_review(item, prior={}, own=set(), run_id="r", folds=True)
    assert off["errors"] and "trade" in off["errors"][0]


def test_merges_and_structure_see_a_trade_claim_only_with_the_family():
    def reading(cat):
        rid = f"{cat}-run_x"
        return {"schema_version": 3, "reading_id": rid, "model_id": "m",
                "rubric_version": f"{cat}-reading-v1", "explanation": "e", "evidence": ["x=1"],
                "side_findings": [{"proposal_id": f"{rid}-1", "claim": _claim(),
                                   "evidence": ["x=1"], "scores": base._scores(), **EMPTY}]}
    readings = {c: reading(c) for c in ("forecast_power", "trade_efficiency")}
    assert len(rfi.side_finding_merges(readings, folds=True, trade_tests=True)) == 1
    assert rfi.side_finding_merges(readings, folds=True) == []
    doc = readings["trade_efficiency"]
    assert rfi.reading_structure(doc, folds=True, trade_tests=True)[0][2] != ()
    assert rfi.reading_structure(doc, folds=True)[0][2] == ()


def _side_item(pid, claim):
    return {"proposal_id": pid, "kind": "side_finding", "claim": claim,
            "evidence": ["slices.overall.x=1"], "scores": base._scores(), "model_id": "m",
            "rubric_version": "profitability-reading-v1", "config_change": [], **EMPTY}


@pytest.mark.parametrize("on", [False, True])
def test_decide_next_takes_a_trade_claim_only_under_the_flag(on):
    import test_e077_folds as tf
    inputs, pid = tf._scenario("run_074", "ROOT", {"run_074": tf.FOLD_A})
    inputs["runs"]["run_074"]["proposals"] = [{"category": "profitability",
                                               "proposal": _side_item(pid, _claim())}]
    if on:
        inputs["trade_tests"] = True
    cand = tf._cand(tf._decide(inputs, "run_074"), pid)
    refused = [r for r in cand["gates"]["feasibility"]["reasons"] if r.startswith("next_test_refused")]
    assert (refused == []) is on
    assert cand["eligible"] is on


def test_load_inputs_carries_the_family_only_when_asked(tmp_path):
    (tmp_path / "campaign_record").mkdir()
    off = dn.load_inputs(tmp_path, {"queue": []}, categories=["profitability"])
    on = dn.load_inputs(tmp_path, {"queue": []}, categories=["profitability"], trade_tests=True)
    assert "trade_tests" not in off and on["trade_tests"] is True
    assert {k: v for k, v in on.items() if k != "trade_tests"} == off


def test_e072_routes_a_trade_claim_as_pending_under_both_flags():
    item = {"claim": _claim()}
    assert ec.finding_route(item, folds=True, trade_tests=True)[0] == ec.PENDING
    assert ec.finding_route(item, folds=True)[0] == ec.NOT_MEASURABLE
    assert ec.finding_spec_hashes(item, folds=True, trade_tests=True) != []


# ---------------------------------------------------------------------------
# the child run's own claim measurement
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("on", [False, True])
def test_the_childs_claim_measurement_passes_the_family_only_under_the_flag(on, monkeypatch,
                                                                           tmp_path):
    run_dir = tmp_path / "run_child"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "H", "claim": _claim(kind="conditional_behaviour")}),
        encoding="utf-8")
    seen = []

    class Stop(Exception):
        pass

    def spy(run_dir, vid, tests, eras, holdout_start, **kw):
        seen.append(kw)
        raise Stop()
    monkeypatch.setattr(cmeas, "measure_variant", spy)
    monkeypatch.setattr(rpr, "_claim_measure_module", lambda: cmeas)
    monkeypatch.setattr(rpr, "_claim_check_exempt", lambda *a: None)
    monkeypatch.setattr(rpr, "_claim_measure_variants", lambda *a, **k: (["base"], {}))
    monkeypatch.setattr(rpr, "_folds_enabled", lambda *a: False)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: on)
    if not on:
        # flag off the card's trade test is refused at the card check: nothing is measured
        monkeypatch.setattr(rpr, "save_yaml", lambda *a, **k: None)
        monkeypatch.setattr(cmeas, "record_measured", lambda *a, **k: None)
        rpr._measure_claim_tests(run_dir, "run_child")
        assert seen == []
        return
    with pytest.raises(Stop):
        rpr._measure_claim_tests(run_dir, "run_child")
    assert seen == [{"trade_tests": True}]


# ---------------------------------------------------------------------------
# fold confirmation on the child's trades
# ---------------------------------------------------------------------------

def _trades_for(block, sign, seed):
    """Daily lots over one block: 8 longs and 8 shorts; longs net +sign*0.8%, shorts
    -sign*0.8%, plus noise (0.2%)."""
    days = pd.date_range(block["start"], block["end"], freq="1D", tz="UTC")
    rng = np.random.default_rng(seed)
    out = []
    for k in range(16):
        e, x = 2 + 6 * k, 4 + 6 * k
        if x >= len(days):
            break
        side = "LONG" if k % 2 == 0 else "SHORT"
        net = (0.8 if side == "LONG" else -0.8) * sign + rng.normal(0.0, 0.2)
        out.append({"trade_id": f"{block['label']}-{k}", "side": side,
                    "entry_time": days[e].strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "exit_time": days[x].strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "exit_forecast": 0.0, "entry_regime": "unknown",
                    "net_profit_loss_percent": float(net)})
    return out


def _build_trades(tmp_path, signs, symbols=("BTCUSD",)):
    root, child = base._build(tmp_path, claim=_claim(), envelope=EMPTY, symbols=symbols,
                              config_period=1)
    path = child / "artifacts" / "research_brief.yaml"
    brief = yaml.safe_load(path.read_text(encoding="utf-8"))
    brief["candidate"]["start_config"] = base._config(1)
    path.write_text(yaml.safe_dump(brief), encoding="utf-8")
    for si, sym in enumerate(symbols):
        for wi, block in enumerate(base.BLOCKS):
            rid = f"base_{sym}_{block['label']}"
            (child / "variants" / "base" / "results" / rid / "trades.json").write_text(
                json.dumps(_trades_for(block, signs[wi], 1000 + 50 * si + wi)), encoding="utf-8")
    return root, child


def _signs(n_pos):
    return [1.0] * n_pos + [-1.0] * (6 - n_pos)


def test_a_trade_claim_is_confirmed_on_the_fold_under_the_flag(tmp_path):
    root, child = _build_trades(tmp_path, _signs(6))
    row = base._confirm(root, child, trade_tests=True)
    assert row["status"] == fc.CONFIRMED, row["reason"]
    assert row["agreement"] == {"longs_beat_shorts": {"0": "6 of 6"}}
    assert row["_comparisons"] and row["vehicle"] == []


def test_a_trade_claim_with_four_of_six_windows_is_not_confirmed(tmp_path):
    root, child = _build_trades(tmp_path, _signs(4))
    row = base._confirm(root, child, trade_tests=True)
    assert row["status"] == fc.NOT_CONFIRMED
    assert row["agreement"] == {"longs_beat_shorts": {"0": "4 of 6"}}


def test_flag_off_a_trade_claim_is_not_measurable_as_before(tmp_path):
    root, child = _build_trades(tmp_path, _signs(6))
    row = base._confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "check_claim" in row["reason"]


def test_three_coins_of_trades_are_pooled_per_window(tmp_path):
    root, child = _build_trades(tmp_path, _signs(5), symbols=COINS)
    row = base._confirm(root, child, trade_tests=True)
    assert row["status"] == fc.CONFIRMED, row["reason"]
    assert row["window_basis"] == "coins_pooled_per_window"
    h = row["tests"]["longs_beat_shorts"]["horizons"]["0"]
    assert (h["windows_claimed_sign"], h["windows_with_value"]) == (5, 6)
    assert sorted(h["per_window"]) == sorted(base.LABELS)


def test_a_bar_test_beside_a_trade_test_is_measured_on_the_bars(tmp_path):
    """measure_on_fold splits the claim: the bar test through measure_on_windows, the
    trade test on the trade windows."""
    root, child = _build_trades(tmp_path, _signs(6))
    bar_test = base._claim()["tests"][0]
    res, measured = fc.measure_on_fold(child, "base", [bar_test, TRADE_TEST], base.LABELS,
                                       base.ERAS, base.HOLDOUT, trade_tests=True)
    assert res["up_day_follow"]["status"] == cmeas.MEASURED
    assert res["longs_beat_shorts"]["status"] == cmeas.MEASURED
    assert list(res["longs_beat_shorts"]["horizons"]) == [0]
    assert len(measured) == 6
    # flag off: exactly measure_on_windows' result for the same tests
    off, m_off = fc.measure_on_fold(child, "base", [bar_test, TRADE_TEST], base.LABELS,
                                    base.ERAS, base.HOLDOUT)
    assert (off, m_off) == ec.measure_on_windows(child, "base", [bar_test, TRADE_TEST],
                                                 base.LABELS, base.ERAS, base.HOLDOUT)
    assert off["longs_beat_shorts"]["status"] == cmeas.NOT_MEASURED


def test_a_custom_measure_hook_is_called_as_before_with_the_flag_off(tmp_path):
    root, child = _build_trades(tmp_path, _signs(6))
    seen = []

    def hook(run_dir, vid, tests, labels, eras, holdout_start, **kw):
        seen.append(kw)
        return {}, []
    base._confirm(root, child, measure=hook, trade_tests=True)
    assert seen == [{"trade_tests": True}]                    # flag on: the hook gets it
    base._confirm(root, child, measure=hook)
    assert seen == [{"trade_tests": True}]   # flag off the trade claim is refused before measuring
    root2, child2 = base._build(tmp_path / "bars")            # a bar claim, flag off
    base._confirm(root2, child2, measure=hook)
    assert seen[-1] == {}                                     # called exactly as before


@pytest.mark.parametrize("on", [False, True])
def test_the_orchestrator_passes_the_family_to_fold_confirmation_only_under_the_flag(on,
                                                                                   monkeypatch,
                                                                                   tmp_path):
    seen = []

    def fake(*a, **kw):
        seen.append({k: v for k, v in kw.items() if k == "trade_tests"})
        return None
    monkeypatch.setattr(fc, "confirm_on_fold", fake)
    monkeypatch.setattr(rpr, "_folds_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: on)
    monkeypatch.setattr(rpr, "_claim_measure_variants", lambda *a, **k: ([], {}))
    rpr._confirm_on_fold_after_backtests(tmp_path, "run_x")
    assert seen == [{"trade_tests": True} if on else {}]



# ---------------------------------------------------------------------------
# review of #358: the trade claim's hash, the coins' cost records, the untested wiring
# ---------------------------------------------------------------------------

def test_a_trade_tests_hash_is_recorded_not_none():
    """claim_findings._tests_of and claim_measure.unmeasured_tests hash a trade test like
    check_claim does (before: None, so a measured trade claim read as `stale`)."""
    import claim_findings as cf
    want = cc_hash = cmeas.test_spec(TRADE_TEST, True)[1]
    assert cc_hash
    (row,) = cf._tests_of(_claim())
    assert row["spec_hash"] == want
    assert cmeas.unmeasured_tests([TRADE_TEST], "x")["longs_beat_shorts"]["spec_hash"] == want
    bar = base._claim()["tests"][0]
    assert cf._tests_of({"tests": [bar]})[0]["spec_hash"] == cmeas.test_spec(bar)[1]


def _diag(child, symbols, per_coin):
    """trade_diagnostics.json of the base variant: every lot of every coin-window with the
    all-costs fields, carrying `symbol` and `window` as run_protocol writes them."""
    recs = []
    for sym in symbols:
        for block in base.BLOCKS:
            rid = f"base_{sym}_{block['label']}"
            trades = json.loads((child / "variants" / "base" / "results" / rid / "trades.json")
                                .read_text(encoding="utf-8"))
            for t in trades[:per_coin.get(sym, len(trades))]:
                recs.append({"trade_id": t["trade_id"], "symbol": sym, "window": block["label"],
                             "gross_return_before_costs": 1.0, "cost_paid_all": 10.0})
    (child / "variants" / "base" / "trade_diagnostics.json").write_text(
        json.dumps({"trades": recs}), encoding="utf-8")


def _rename_trades(child, symbols):
    """Give each coin's lots distinct ids (the fixture reuses ids across coins)."""
    for sym in symbols:
        for block in base.BLOCKS:
            path = child / "variants" / "base" / "results" / f"base_{sym}_{block['label']}" / "trades.json"
            trades = json.loads(path.read_text(encoding="utf-8"))
            for t in trades:
                t["trade_id"] = f"{sym}-{t['trade_id']}"
            path.write_text(json.dumps(trades), encoding="utf-8")


def test_several_coins_keep_their_own_all_costs_records(tmp_path):
    """Before: the records were grouped by window only, so with two coins a coin-window got
    both coins' records, the pairing failed and that window fell back to the net basis."""
    import claim_tests as ct
    coins = ("BTCUSD", "ETHUSD")
    root, child = _build_trades(tmp_path, _signs(6), symbols=coins)
    _rename_trades(child, coins)
    _diag(child, coins, {})
    tws = ct.load_variant_trade_windows(child, "base")
    assert {tw.basis for tw in tws} == {"all_costs"}
    row = base._confirm(root, child, trade_tests=True)
    assert row["status"] != fc.NOT_MEASURABLE, row["reason"]


def test_one_coins_records_are_used_whatever_their_symbol_spelling(tmp_path):
    import claim_tests as ct
    root, child = _build_trades(tmp_path, _signs(6))
    _diag(child, ("BTCUSD",), {})
    path = child / "variants" / "base" / "trade_diagnostics.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    for r in doc["trades"]:
        r["symbol"] = "BTC/USD"                                 # another spelling: one coin
    path.write_text(json.dumps(doc), encoding="utf-8")
    assert {tw.basis for tw in ct.load_variant_trade_windows(child, "base")} == {"all_costs"}


@pytest.mark.parametrize("on", [False, True])
def test_the_in_run_record_gets_the_family_only_under_the_flag(on, monkeypatch, tmp_path):
    seen = []

    class Stop(Exception):
        pass

    def spy(*a, **kw):
        seen.append({k: v for k, v in kw.items() if k == "trade_tests"})
        raise Stop()
    monkeypatch.setattr(ec, "confirm_findings", spy)
    monkeypatch.setattr(rpr, "_explore_confirm_module", lambda: ec)
    monkeypatch.setattr(ec, "load_split", lambda arts: {"exploration": [], "confirmation": []})
    monkeypatch.setattr(rpr, "_folds_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: on)
    monkeypatch.setattr(rpr, "_load_holdout_range", lambda: (base.HOLDOUT, None))
    (tmp_path / "artifacts" / "proposals").mkdir(parents=True)
    try:
        rpr._record_confirmations("run_x", tmp_path)
    except Stop:
        pass
    assert seen == [{"trade_tests": True} if on else {}]


def test_confirm_findings_routes_a_trade_claim_pending_only_with_the_family(tmp_path):
    doc = {"schema_version": 3, "reading_id": "trade_efficiency-run_x", "model_id": "m",
           "rubric_version": "trade_efficiency-reading-v1", "explanation": "e",
           "evidence": ["x=1"],
           "side_findings": [{"proposal_id": "trade_efficiency-run_x-1", "claim": _claim(),
                              "evidence": ["x=1"], "scores": base._scores(), **EMPTY}]}
    split = {"exploration": [], "confirmation": []}
    kw = dict(base_variant="base", eras=base.ERAS, holdout_start=base.HOLDOUT, folds=True)
    (rec,) = ec.confirm_findings(tmp_path, "run_x", {"trade_efficiency": doc}, split,
                                 trade_tests=True, **kw)
    assert rec["status"] == ec.PENDING and rec["finding_spec_hashes"]
    (rec,) = ec.confirm_findings(tmp_path, "run_x", {"trade_efficiency": doc}, split, **kw)
    assert rec["status"] == ec.NOT_MEASURABLE


def _analyst_guarded(tree):
    """Every `trade_tests` keyword, and every dict literal with a "trade_tests" key, sits
    inside a conditional expression whose test calls *_analyst_enabled()."""
    parents = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node

    def is_flag_call(t):
        return (isinstance(t, ast.Call) and not t.args and not t.keywords
                and (getattr(t.func, "id", "") == "_analyst_enabled"
                     or getattr(t.func, "attr", "") == "_analyst_enabled"))

    def guarded(node):
        # the node must sit in the BODY (the "if true" branch) of a conditional expression
        # whose condition is exactly a call of _analyst_enabled() (review round 2 of #358)
        child = node
        while child in parents:
            parent = parents[child]
            if isinstance(parent, ast.IfExp) and parent.body is child and is_flag_call(parent.test):
                return True
            child = parent
        return False
    bad = []
    for node in ast.walk(tree):
        hit = ((isinstance(node, ast.keyword) and node.arg == "trade_tests")
               or (isinstance(node, ast.Dict) and any(isinstance(k, ast.Constant)
                                                      and k.value == "trade_tests" for k in node.keys)))
        if hit and not guarded(node):
            bad.append(ast.unparse(node) if not isinstance(node, ast.keyword) else node.arg)
    return bad


def test_every_orchestrator_trade_tests_sits_behind_the_flag():
    """Review of #358: a static guard, not a regex. In workflow/ every `trade_tests` keyword
    or dict key is inside `... if _analyst_enabled() else ...`; and run_campaign's decide-next
    inputs carry it (the call site the behavioural tests cannot reach)."""
    for name in ("run_phase1_research.py", "run_campaign.py"):
        tree = ast.parse((SR_ROOT / "workflow" / name).read_text(encoding="utf-8"))
        assert _analyst_guarded(tree) == [], name
    camp = ast.parse((SR_ROOT / "workflow" / "run_campaign.py").read_text(encoding="utf-8"))
    calls = [n for n in ast.walk(camp) if isinstance(n, ast.Call)
             and getattr(n.func, "attr", "") == "load_inputs"]
    assert len(calls) == 1
    assert "trade_tests" in ast.unparse(calls[0]) and "_analyst_enabled" in ast.unparse(calls[0])
    # the guard is not vacuous: an unconditional keyword is reported
    assert _analyst_guarded(ast.parse("f(x, trade_tests=True)")) == ["trade_tests"]
    assert _analyst_guarded(ast.parse('f(**{"trade_tests": True})')) != []
    for bypass in ('f(**({"trade_tests": True} if not _analyst_enabled() else {}))',
                   'f(**({} if _analyst_enabled() else {"trade_tests": True}))',
                   'f(**({"trade_tests": True} if _analyst_enabled() or x else {}))'):
        assert _analyst_guarded(ast.parse(bypass)) != [], bypass
    assert _analyst_guarded(ast.parse(
        'f(**({"trade_tests": True} if orch._analyst_enabled() else {}))')) == []



def test_two_coins_spelled_differently_keep_their_own_records(tmp_path):
    """Review round 2 of #358: trade_diagnostics.json may write BTC/USD where
    protocol_result.yaml writes BTCUSD; the coins are compared without punctuation."""
    import claim_tests as ct
    coins = ("BTCUSD", "ETHUSD")
    root, child = _build_trades(tmp_path, _signs(6), symbols=coins)
    _rename_trades(child, coins)
    _diag(child, coins, {})
    path = child / "variants" / "base" / "trade_diagnostics.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    for r in doc["trades"]:
        r["symbol"] = r["symbol"][:3] + "/" + r["symbol"][3:].lower()
    path.write_text(json.dumps(doc), encoding="utf-8")
    assert {tw.basis for tw in ct.load_variant_trade_windows(child, "base")} == {"all_costs"}
    assert ct._coin_key("btc/usd") == ct._coin_key("BTCUSD") == "BTCUSD"
