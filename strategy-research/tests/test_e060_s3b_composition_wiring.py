"""
E-060 S3b -- composition wiring (delivery_plan_v26.md slice 7 items 7.2, 7.3,
7.5; engineering/roadmap/E-060/S1_FINDINGS.md guesses 9-12 and the operator
decisions of 2026-09-26), behind orchestrator.composition_runs.enabled.

Proven here, with fixtures only (the registry is empty on the real checkout,
no LLM runs, no real backtest, no market data, never the holdout):
  * flag off: R1 is the same recorded no-op, load_inputs reads nothing new,
    the DONE step passes no new kwarg, a profit_bars criterion is the
    SPEC_ERROR it always was, a patch brief is byte-identical;
  * R1 fires only when an exact timeframe holds >= 2 forecast blocks whose set
    has no composition yet, once per registry state per timeframe, behind a
    run in progress and operator entries, ahead of agent entries, candidates
    and R2;
  * the stand-alone daily-returns loader fails loud and matches the profit
    bars' equal-weight portfolio definition;
  * the variant configs, the manifest and compositions.yaml are written by
    code, and steps 1a / 1b / 2 author nothing (no LLM call);
  * the 5a manifest/weights check;
  * the profit_bars grid criterion is branch 3's own grading;
  * 7.5: a reader patch from a composition run is accepted with its
    composition manifest as the source;
  * a composite never registers as a block;
  * one end-to-end fixture run: registry change -> R1 -> composition run ->
    graded composite -> never a block -> R1 does not fire again.
"""
from __future__ import annotations

import copy
import json
import random
import re
import shutil
import statistics
import sys
from pathlib import Path

import pandas as pd
import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import decide_next as dn  # noqa: E402
import composition as comp  # noqa: E402
import composite_cache as cc  # noqa: E402
import block_registry as br  # noqa: E402
import campaign_memory as cm  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

from test_e060_s3a_composition import _registry, _rets_for  # noqa: E402
from test_e059_s2a_decide_next import (  # noqa: E402
    _one_source, _decide, _by_id, _memory_entry, _src, _write_flags, _ALL_ON)
from test_halt_quarantine_policy import (  # noqa: E402
    _entry, _save_queue_entries, _write_campaign_state, _write_fresh_scaffold,
    campaign_root,  # noqa: F401  (fixture)
)

REAL_MENU = yaml.safe_load((_SR / "config" / "criterion_menu.yaml").read_text(encoding="utf-8"))
OLD_R1 = {"registry_revision": 0, "last_composition_revision": None, "would_fire": False,
          "fired": False, "reason": "composition brief writer is slice 7"}
FLAT_COMP_ON = {**_ALL_ON, "profit_bars_file": True, "profit_bars_every_backtest": True,
                "verdict_routing_retired": True, "variant_loop": True, "composition_runs": True,
                "data_availability_gate": False}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _blk(bid, tf="1h", kind="forecast", sha=None, run=None):
    return {"block_id": bid, "kind": kind, "timeframe": tf,
            "timeframe_category": cc.timeframe_category(tf) if tf else None,
            "source_config_sha256": sha or ("s" * 63 + bid[-1]),
            "validated_by_run": run or f"run_{bid[-1]}"}


def _comp_inputs(blocks, revision=None):
    return {"registry": {"schema_version": 1, "revision": revision or len(blocks),
                         "blocks": blocks},
            "compositions": [], "sources": {}}


def _with_comp(inputs, blocks, revision=None):
    inputs["composition"] = _comp_inputs(blocks, revision)
    inputs["registry_revision"] = revision or len(blocks)
    return inputs


def _equity_csv(path: Path, days=40, seed=0, t0="2020-01-01", not_ready=5, bars=True):
    """portfolio_states.csv, plus (bars=True) a bars.csv next to it whose
    forecast leads the next bar's move (so a residual IC is measurable)."""
    rng = random.Random(seed)
    eq, lines = 10000.0, ["timestamp,regime,postRebalance_total_value"]
    close, blines = 100.0, ["timestamp,close,forecast"]
    for i, t in enumerate(pd.date_range(t0, periods=days * 24, freq="h")):
        eq *= 1.0 + rng.gauss(0.0, 0.002)
        lines.append(f"{t.isoformat()},{'NOT_READY' if i < not_ready else 'unknown'},{eq:.6f}")
        f = rng.gauss(0.0, 1.0)
        blines.append(f"{t.isoformat()},{close:.6f},{f:.6f}")
        close *= 1.0 + 0.002 * f + rng.gauss(0.0, 0.002)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if bars:
        (path.parent / "bars.csv").write_text("\n".join(blines) + "\n", encoding="utf-8")


def _validating_run(root: Path, block: dict, days=40, windows=("2020-01", "2020-03"),
                    symbols=("BTCUSDT", "ETHUSDT"), seed=0) -> dict:
    """The per-variant results of the run that validated `block` (base variant)."""
    run = block["validated_by_run"]
    results = []
    for w in windows:
        for k, s in enumerate(symbols):
            wrid = f"{run}_{s}_{w}"
            results.append({"symbol": s, "window": w, "run_id": wrid})
            _equity_csv(root / "runs" / run / "variants" / "base" / "results" / wrid /
                        "portfolio_states.csv", days=days, seed=seed * 100 + k * 10 + len(results),
                        t0=f"{w}-01")
    pr = {"results": results}
    path = root / "runs" / run / "artifacts" / "variants" / "base" / "protocol_result.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(pr), encoding="utf-8")
    # the residual-IC basis recorded at registration (S2): no composite yet
    (root / "runs" / run / "artifacts" / "residual_ic.yaml").write_text(yaml.safe_dump(
        {"timeframe": "1h", "timeframe_category": "low", "skipped": None,
         "composite": {"kind": "none", "cache_dir": None}, "variants": {}}), encoding="utf-8")
    return pr


def _written(tmp_path, window_starts=None, prior_ic=None, rets=None):
    """Code-written composition from the S3a fixture registry (per-window
    weights: window 1 equal, window 2 estimated -- review fix 5)."""
    from test_e060_s3a_composition import WINDOW_STARTS, _prior_ic_from_registry
    doc = _registry(tmp_path)
    out = tmp_path / "campaign_record" / "compositions" / "c1"
    m = comp.write_composition_variants(
        doc, "1h", out, root=tmp_path, daily_returns_by_block=rets or _rets_for(doc),
        window_starts=window_starts or WINDOW_STARTS,
        prior_ic=prior_ic or _prior_ic_from_registry, enabled=True)
    cfgs = {vid: json.loads((out / f"{vid}.json").read_text(encoding="utf-8"))
            for vid in ("base", "vol_scaled", "ic_weighted")}
    return doc, m, cfgs


# ---------------------------------------------------------------------------
# 1. Flag off: nothing new
# ---------------------------------------------------------------------------

def test_flag_off_r1_is_the_same_recorded_no_op():
    rec = _decide(_one_source([]))
    assert rec["rules"]["r1"] == OLD_R1
    inputs = _one_source([])
    inputs["registry_revision"] = 2
    assert _decide(inputs)["rules"]["r1"] == {**OLD_R1, "registry_revision": 2, "would_fire": True}


def test_flag_off_load_inputs_reads_no_composition(tmp_path, monkeypatch):
    monkeypatch.setattr(dn, "load_composition_inputs",
                        lambda *a, **k: pytest.fail("flag off must not read R1's inputs"))
    a = dn.load_inputs(tmp_path, {"queue": []}, categories=["profitability"])
    b = dn.load_inputs(tmp_path, {"queue": []}, categories=["profitability"],
                       composition_runs=False)
    assert "composition" not in a and a == b


def test_flag_off_profit_bars_criterion_is_the_old_spec_error():
    crit = {"id": "profit_bars", "metric": "profit_bars", "source": "profit_bars"}
    pre = {"pass_rule": {"criteria": [crit]}}
    grader = lambda vid: pytest.fail("flag off never grades")  # noqa: E731
    out = vce.evaluate_grid({"base": {"results": []}}, pre, {}, REAL_MENU,
                            profit_bars_grader=grader)
    assert out["result"] == "SPEC_ERROR"
    assert out["grid"]["profit_bars"]["base"] == vce.evaluate_grid(
        {"base": {"results": []}}, pre, {}, REAL_MENU)["grid"]["profit_bars"]["base"]


def test_flag_off_patch_brief_keys_keep_their_order():
    from test_e059_s2a_decide_next import _patch
    inputs = _one_source([_patch("profitability-run_061-1")])
    rec = _decide(inputs)
    _rel, text = dn.candidate_brief(rec, inputs, decision_ref="d.yaml")
    front = yaml.safe_load(re.match(r"\A---\n(.*?\n)---\n", text, re.S).group(1))
    assert list(front["candidate"]) == ["config", "manifest", "criteria_from", "source"]
    assert list(front["candidate"]["source"])[-4:] == [
        "resolved_patch", "base_config_ref", "expected_config_sha256", "expected_manifest_sha256"]
    assert "composition" not in front["candidate"]


def test_flag_off_done_step_passes_no_composition_kwarg(campaign_root, monkeypatch):
    from test_e059_s2a_decide_next import _stage_flag_on_source, _patch
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    seen = []
    real = dn.load_inputs
    monkeypatch.setattr(dn, "load_inputs", lambda *a, **k: seen.append(k) or real(*a, **k))
    _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")])
    assert camp.process_once() is True
    assert seen and "composition_runs" not in seen[0]
    root = campaign_root["root"]
    rec = yaml.safe_load((root / "runs" / "run_061" / "artifacts" / "decision_record.yaml")
                         .read_text(encoding="utf-8"))
    assert rec["rules"]["r1"] == OLD_R1
    assert not (root / "campaign_record" / "compositions").exists()
    assert not (root / "campaign_record" / "compositions.yaml").exists()


def test_composition_brief_with_the_flag_off_fails_loud_never_the_llm():
    run_dir = rpr.ROOT / "runs" / "run_780"
    (run_dir / "artifacts").mkdir(parents=True)
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml",
                  {"candidate": {"composition": {"manifest_ref": "x"}}})
    with pytest.raises(ValueError, match="composition_runs is off"):
        rpr._composition_mode(run_dir)
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", {"research_goal": "g"})
    assert rpr._composition_mode(run_dir) is False


# ---------------------------------------------------------------------------
# 2. R1: fires on a registry change with >= 2 same-timeframe blocks, once
# ---------------------------------------------------------------------------

def _r1(inputs):
    rec = _decide(inputs)
    return rec, rec["rules"]["r1"]


def test_r1_single_block_or_mixed_timeframes_never_fires():
    for blocks in ([_blk("A1")], [_blk("A1", "1h"), _blk("A2", "1d")]):
        rec, r1 = _r1(_with_comp(_one_source([]), blocks))
        assert r1["fired"] is False and r1["would_fire"] is False
        assert {r["status"] for r in r1["timeframes"]} == {"single_block"}
        assert "composition" not in (rec["picked"] or {})


def test_r1_fires_on_two_same_timeframe_blocks_ahead_of_candidates_and_r2():
    from test_e059_s2a_decide_next import _patch
    blocks = [_blk("A1"), _blk("A2", "60m")]  # same bar size in seconds
    rec, r1 = _r1(_with_comp(_one_source([_patch("profitability-run_061-1", conf=3)]), blocks))
    h = cc.composite_registry_hash(blocks)
    eid = f"composition-1h-{h}"
    assert r1["fired"] is True and r1["entry_id"] == eid and r1["registry_hash"] == h
    assert r1["priority"] == dn.AGENT_PRIORITY - 1
    assert rec["picked"] == {"composition": eid, "queue_entry_id": eid,
                             "brief_path": f"{dn.CANDIDATE_BRIEFS_DIR}/{eid}.md",
                             "timeframe": "1h", "registry_hash": h, "priority": 998,
                             "why": rec["picked"]["why"]}
    # the eligible reader candidate is still ranked and recorded, just not picked
    assert _by_id(rec)["profitability-run_061-1"]["rank"] == 1
    assert rec["rules"]["r2"]["fired"] is False and rec["stop"] is None


def test_r1_fires_once_per_registry_state_per_timeframe():
    blocks = [_blk("A1"), _blk("A2")]
    eid = dn.composition_entry_id("1h", cc.composite_registry_hash(blocks))
    queue = {"queue": [{"id": eid, "status": "done", "origin": "composition", "priority": 998}]}
    inputs = _with_comp(_one_source([]), blocks)
    inputs["queue"] = queue
    _rec, r1 = _r1(inputs)
    assert r1["fired"] is False and r1["timeframes"][0]["status"] == "fired_before"
    # a block on ANOTHER timeframe bumps the revision, not the 1h set: still no fire
    inputs = _with_comp(_one_source([]), blocks + [_blk("A3", "1d")], revision=3)
    inputs["queue"] = queue
    _rec, r1 = _r1(inputs)
    assert r1["fired"] is False and r1["registry_revision"] == 3
    # a third 1h block changes the 1h set: R1 fires again, under a new id
    inputs = _with_comp(_one_source([]), blocks + [_blk("A4")], revision=3)
    inputs["queue"] = queue
    _rec, r1 = _r1(inputs)
    assert r1["fired"] is True and r1["entry_id"] != eid


def test_r1_waits_behind_a_run_in_progress_and_operator_entries():
    blocks = [_blk("A1"), _blk("A2")]
    for entry, why in (({"id": "RUN", "status": "in_progress", "priority": 999}, "in progress"),
                       ({"id": "OP", "status": "ready", "priority": 1000}, "operator")):
        inputs = _with_comp(_one_source([]), blocks)
        inputs["queue"] = {"queue": [entry]}
        rec, r1 = _r1(inputs)
        assert r1["would_fire"] is True and r1["fired"] is False and why in r1["reason"]
        assert "composition" not in rec["picked"]


def test_r1_goes_ahead_of_ready_agent_entries_whatever_their_priority():
    blocks = [_blk("A1"), _blk("A2")]
    inputs = _with_comp(_one_source([]), blocks)
    inputs["queue"] = {"queue": [{"id": "AG", "status": "ready", "origin": "reader", "priority": 5},
                                 {"id": "R2", "status": "ready", "origin": "brief"}]}
    rec, r1 = _r1(inputs)
    assert r1["fired"] is True and r1["priority"] == 4
    sim = inputs["queue"]["queue"] + [{"id": r1["entry_id"], "status": "ready", "priority": 4}]
    assert dn.select_entry_rule(sim)["id"] == rec["picked"]["composition"]


def test_r1_reports_blocks_without_a_timeframe():
    legacy = _blk("A9")
    legacy.pop("timeframe")
    _rec, r1 = _r1(_with_comp(_one_source([]), [_blk("A1"), _blk("A2"), legacy]))
    assert r1["fired"] is True
    assert [e["block_id"] for e in r1["excluded_blocks"]] == ["A9"]


def test_r1_records_match_the_schema():
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((_SR / "workflow_artifacts" / "schemas" / "decision_record.schema.json")
                        .read_text(encoding="utf-8"))
    v = jsonschema.Draft202012Validator(schema)
    for blocks, queue in (([_blk("A1"), _blk("A2")], []),
                          ([_blk("A1")], []),
                          ([_blk("A1"), _blk("A2")], [{"id": "OP", "status": "ready",
                                                       "priority": 1}])):
        inputs = _with_comp(_one_source([]), blocks)
        inputs["queue"] = {"queue": queue}
        v.validate(_decide(inputs))


# ---------------------------------------------------------------------------
# 3. The stand-alone daily-returns loader (review fix 9: one shared helper)
# ---------------------------------------------------------------------------

def test_loader_reads_the_validating_run_and_matches_the_profit_bars_portfolio(tmp_path):
    doc = _registry(tmp_path)
    block = doc["blocks"][0]
    pr = _validating_run(tmp_path, block)
    rets = comp.load_block_daily_returns(block, root=tmp_path)
    assert len(rets) == 2 * 39  # 2 windows x (40 common days - 1)
    assert all(isinstance(d, type(pd.Timestamp("2020-01-01").date())) for d, _r in rets)
    run_dir = tmp_path / "runs" / block["validated_by_run"]
    avg = rpr._portfolio_profit_metrics(run_dir, pr)["avg_daily_return"][0]
    assert round(statistics.mean(r for _d, r in rets), 8) == avg


def test_one_daily_returns_helper_shared_by_profit_bars_and_composition():
    """Review fix 9: no second copy of the readers or the coverage floor."""
    import portfolio_daily as pd_
    assert rpr._window_equity_bars is pd_.window_equity_bars
    assert rpr._find_window_equity_file is pd_.find_window_equity_file
    assert rpr._daily_closes is pd_.daily_closes
    assert rpr.PORTFOLIO_MIN_COMMON_DAY_COVERAGE is pd_.PORTFOLIO_MIN_COMMON_DAY_COVERAGE
    assert not hasattr(comp, "PORTFOLIO_MIN_COMMON_DAY_COVERAGE")
    src = (_SR / "tools" / "composition.py").read_text(encoding="utf-8")
    assert '"variants" / vid / "results"' not in src and "portfolio_states.csv\"" not in src


@pytest.mark.parametrize("break_it, needle", [
    ("no_protocol_result", "protocol_result.yaml is missing"),
    ("no_equity", "no portfolio_states.csv"),
    ("short", "at least 30"),
    ("bad_ref", "is not"),
    ("changed_config", "changed after it was validated"),
    ("other_run", "was validated by"),
    ("coin_gap", "the coin set differs"),
])
def test_loader_fails_loud(tmp_path, break_it, needle):
    doc = _registry(tmp_path)
    block = doc["blocks"][0]
    run = block["validated_by_run"]
    _validating_run(tmp_path, block, days=(10 if break_it == "short" else 40),
                    windows=(("2020-01",) if break_it == "short" else ("2020-01", "2020-03")))
    base = tmp_path / "runs" / run
    if break_it == "no_protocol_result":
        (base / "artifacts" / "variants" / "base" / "protocol_result.yaml").unlink()
    elif break_it == "no_equity":
        next((base / "variants" / "base" / "results").glob("*/portfolio_states.csv")).unlink()
    elif break_it == "bad_ref":
        block = dict(block, source_config_ref=f"runs/{run}/artifacts/candidate_strategy_config.json")
    elif break_it == "changed_config":
        block = dict(block, source_config_sha256="0" * 64)
    elif break_it == "other_run":
        block = dict(block, validated_by_run="run_111")
    elif break_it == "coin_gap":
        path = base / "artifacts" / "variants" / "base" / "protocol_result.yaml"
        pr = yaml.safe_load(path.read_text(encoding="utf-8"))
        pr["results"] = pr["results"][:-1]
        path.write_text(yaml.safe_dump(pr), encoding="utf-8")
    with pytest.raises(comp.CompositionError, match=needle):
        comp.load_block_daily_returns(block, root=tmp_path)


# ---------------------------------------------------------------------------
# 3b. No lookahead in the weights (review fix 5)
# ---------------------------------------------------------------------------

def _perturbed_after(rets, cut):
    """The same series with every return dated on/after `cut` replaced."""
    import random as _r
    rng = _r.Random(7)
    return {b: [(d, r if d < cut else rng.gauss(0.0, 0.5)) for d, r in v] for b, v in rets.items()}


def test_vol_weights_of_a_window_ignore_data_inside_and_after_it(tmp_path):
    doc = _registry(tmp_path)
    rets = _rets_for(doc)  # 60 daily returns from 2020-01-01
    blocks = doc["blocks"]
    starts = ["2020-01-01", "2020-02-15", "2020-03-15"]
    cut = pd.Timestamp("2020-02-15").date()
    a = comp.window_weight_schedule("vol_scaled", blocks, starts, daily_returns_by_block=rets)
    b = comp.window_weight_schedule("vol_scaled", blocks, starts,
                                    daily_returns_by_block=_perturbed_after(rets, cut))
    # windows starting on/before the cut: identical -- data inside/after never used
    assert a[:2] == b[:2]
    assert a[2] != b[2]  # a later window does see the changed (now past) data
    # the first window has no prior data: equal weights, recorded as not estimated
    assert a[0]["basis"]["estimated"] is False and a[0]["weights"] == comp.equal_weights(
        [x["block_id"] for x in blocks])
    assert a[1]["basis"]["estimated"] is True and a[1]["basis"]["data_before"] == "2020-02-15"
    assert a[1]["basis"]["n_daily_returns"] == {x["block_id"]: 45 for x in blocks}


def test_ic_weights_ask_only_for_data_before_each_window(tmp_path):
    doc = _registry(tmp_path)
    asked = []

    def prior_ic(block, d):
        asked.append((block["block_id"], d))
        return {"value": 0.02 if block["block_id"].startswith("H-0") else 0.01, "n_eff": 40}
    sched = comp.window_weight_schedule("ic_weighted", doc["blocks"], ["2020-03-15", "2020-01-01"],
                                        prior_ic=prior_ic)
    assert [e["from"] for e in sched] == ["2020-01-01", "2020-03-15"]
    assert sorted({d for _b, d in asked}) == [pd.Timestamp("2020-01-01").date(),
                                               pd.Timestamp("2020-03-15").date()]
    assert sched[0]["weights"]["H-0:run_900"] == pytest.approx(2 / 3)


def test_prior_residual_ic_uses_only_bars_realised_before_the_window(tmp_path):
    doc = _registry(tmp_path)
    block = doc["blocks"][0]
    _validating_run(tmp_path, block, windows=("2020-01", "2020-03"))
    before = pd.Timestamp("2020-02-20").date()
    a = comp.load_block_prior_residual_ic(block, before, root=tmp_path, timeframe="1h")
    # rewrite every bar of the LATER window: the measurement before it cannot move
    for p in (tmp_path / "runs" / block["validated_by_run"] / "variants" / "base" /
              "results").glob("*2020-03/bars.csv"):
        df = pd.read_csv(p)
        df["forecast"] = -df["forecast"] * 3.0
        df.to_csv(p, index=False)
    b = comp.load_block_prior_residual_ic(block, before, root=tmp_path, timeframe="1h")
    assert a == b and a["n_bars"] > 0
    full = comp.load_block_prior_residual_ic(block, pd.Timestamp("2020-06-01").date(),
                                             root=tmp_path, timeframe="1h")
    assert full["n_bars"] > a["n_bars"]


def test_engine_config_carries_the_window_schedule_and_equal_static_weights(tmp_path):
    _doc, m, cfgs = _written(tmp_path)
    reg = _reg(cfgs["vol_scaled"])
    assert {b["weight"] for b in reg["blocks"]} == {0.5}
    assert [e["from"] for e in reg["weight_schedule"]] == ["2020-01-01", "2020-03-15"]
    assert "weight_schedule" not in _reg(cfgs["base"])
    for e in m["variants"]["vol_scaled"]["weight_schedule"]:
        assert "estimated" in e["basis"]


# ---------------------------------------------------------------------------
# 4. Code-written variants + the 5a check
# ---------------------------------------------------------------------------

def test_variant_patches_rebuild_the_code_written_configs_exactly(tmp_path):
    import json_pointer as jp
    _doc, m, cfgs = _written(tmp_path)
    patches = comp.variant_patches_from_manifest(m)
    assert [v["variant_id"] for v in patches["variants"]] == ["base", "vol_scaled", "ic_weighted"]
    for v in patches["variants"]:
        built = jp.apply_json_pointer_patch(cfgs["base"], v["patch"])
        assert dn.config_sha256(built) == m["variants"][v["variant_id"]]["config_sha256"]
        assert all(p["path"].endswith(("/weight", "/weight_schedule")) for p in v["patch"])


def test_5a_check_passes_each_variant_on_its_own_scheme_only(tmp_path):
    doc, m, cfgs = _written(tmp_path)
    for vid, cfg in cfgs.items():
        comp.check_composition_config(cfg, m, vid, root=tmp_path, registry_doc=doc)
    with pytest.raises(comp.CompositionError, match="weight_schedule"):
        comp.check_composition_config(cfgs["base"], m, "vol_scaled", root=tmp_path,
                                      registry_doc=doc)


def _reg(cfg):
    return cfg["strategies"]["regimes"]["unknown"]


@pytest.mark.parametrize("mutate, needle", [
    (lambda c: _reg(c)["blocks"][0].__setitem__("weight", _reg(c)["blocks"][0]["weight"] * 1.01),
     "weights differ"),
    (lambda c: _reg(c)["blocks"].pop(1), "not the manifest's"),
    (lambda c: _reg(c)["components"].append(dict(_reg(c)["components"][0], id="stray")),
     "owned by exactly one"),
    (lambda c: _reg(c)["blocks"][0]["source"]["regime_detector"].__setitem__(
        "default_regime", "chop"), "gated/timed as its source"),
    (lambda c: _reg(c)["blocks"][1]["source"].__setitem__("warmup", 1), "gated/timed"),
    (lambda c: _reg(c)["components"][0].__setitem__("lookback", 7), "lookback"),
    (lambda c: _reg(c)["components"][0].__setitem__(
        "class", "strategies.strategy_components.X"), "class"),
    (lambda c: _reg(c).__setitem__("block_standardisation", {"target": 5.0}),
     "block_standardisation"),
    (lambda c: c["regime_detector"].__setitem__("default_regime", "chop"), "ungated"),
    (lambda c: c["strategies"]["regimes"].__setitem__("chop", {"components": []}), "carry"),
    (lambda c: _reg(c)["blocks"][0].__setitem__("weight", -0.5), "positive finite"),
    # review fix 7: the scaffolding
    (lambda c: c.__setitem__("aux_feeds", ["funding_rate"]), "aux_feeds"),
    (lambda c: c["strategies"].__setitem__("warmup", 51), "outside its scaffolding"),
    (lambda c: c["strategies"].__setitem__("min_allocation_change", 0.3), "min_allocation_change"),
    (lambda c: c.__setitem__("significance_methodology", "x"), "outside its scaffolding"),
    (lambda c: _reg(c).__setitem__("weight_schedule",
                                   [{"from": "2020-01-01", "weights": {"b0": 1.0, "b1": 1.0}}]),
     "weight_schedule"),
])
def test_5a_check_fails_loud(tmp_path, mutate, needle):
    doc, m, cfgs = _written(tmp_path)
    cfg = copy.deepcopy(cfgs["base"])
    mutate(cfg)
    with pytest.raises(comp.CompositionError, match=needle):
        comp.check_composition_config(cfg, m, "base", root=tmp_path, registry_doc=doc)


def test_5a_check_refuses_a_manifest_whose_pointers_do_not_match_its_components(tmp_path):
    """Review fix 7: a missing config_paths entry raises instead of zip()
    silently checking fewer pointers."""
    doc, m, cfgs = _written(tmp_path)
    m2 = copy.deepcopy(m)
    m2["blocks"][0]["config_paths"] = []
    with pytest.raises(comp.CompositionError, match="one to one"):
        comp.check_composition_config(cfgs["base"], m2, "base", root=tmp_path, registry_doc=doc)


def test_5a_check_refuses_a_block_missing_from_the_registry(tmp_path):
    doc, m, cfgs = _written(tmp_path)
    doc = dict(doc, blocks=doc["blocks"][:1])
    with pytest.raises(comp.CompositionError, match="not in the block registry"):
        comp.check_composition_config(cfgs["base"], m, "base", root=tmp_path, registry_doc=doc)


def test_5a_check_allows_a_reader_patch_to_a_component_parameter(tmp_path):
    """7.5: a patch changing a component's params keeps the block gated and
    pinned as its source -- the manifest check passes; the brief's config sha
    pins the exact config."""
    doc, m, cfgs = _written(tmp_path)
    cfg = copy.deepcopy(cfgs["base"])
    _reg(cfg)["components"][0]["params"]["period"] += 1
    comp.check_composition_config(cfg, m, "base", root=tmp_path, registry_doc=doc)


def test_5a_builds_each_blocks_source_once_per_process(tmp_path, monkeypatch):
    """Review fix 8: three variants x two blocks -> two source builds."""
    doc, m, cfgs = _written(tmp_path)
    comp._ASSEMBLED.clear()
    calls = []
    real = comp._assemble_block
    monkeypatch.setattr(comp, "_assemble_block", lambda *a: calls.append(a[1]) or real(*a))
    for vid, cfg in cfgs.items():
        comp.check_composition_config(cfg, m, vid, root=tmp_path, registry_doc=doc)
    assert sorted(calls) == ["b0", "b1"]


# ---------------------------------------------------------------------------
# 5. profit_bars grading in the grid
# ---------------------------------------------------------------------------

def _bars(*results):
    return [{"name": f"bar{i}", "result": r} for i, r in enumerate(results)]


def test_profit_bars_cell_is_the_graders_result():
    crit = rpr._code_added_criterion(REAL_MENU, "profit_bars")
    pre = {"pass_rule": {"criteria": [crit]}}
    graded = {"base": {"result": "PASS", "bars": _bars("PASS", "PASS"), "reasons": []},
              "vol_scaled": {"result": "FAIL", "bars": _bars("FAIL", "PASS"),
                             "reasons": ["sharpe_min: FAIL"]}}
    out = vce.evaluate_grid({v: {"results": []} for v in graded}, pre, {}, REAL_MENU,
                            composition_runs=True, profit_bars_grader=lambda v: graded[v])
    assert out["result"] == "GRID_EVALUATED" and out["idea_status"] == "refuted"
    assert out["grid"]["profit_bars"]["base"]["result"] == "PASS"
    assert out["grid"]["profit_bars"]["vol_scaled"]["reason"] == "sharpe_min: FAIL"
    out = vce.evaluate_grid({"base": {}}, pre, {}, REAL_MENU, composition_runs=True,
                            profit_bars_grader=lambda v: graded["base"])
    assert out["idea_status"] == "validated"
    for grader in (lambda v: {"result": "NOT_EVALUABLE"}, None,
                   lambda v: {"result": "PASS", "bars": _bars("PASS", "FAIL")}):
        out = vce.evaluate_grid({"base": {}}, pre, {}, REAL_MENU, composition_runs=True,
                                profit_bars_grader=grader)
        assert out["result"] == "SPEC_ERROR" and out["idea_status"] is None


def test_not_evaluable_bar_is_inconclusive_never_fail():
    """Review fix 1: a missing input (NOT_EVALUABLE) is not a measured failure."""
    crit = rpr._code_added_criterion(REAL_MENU, "profit_bars")
    pre = {"pass_rule": {"criteria": [crit]}}
    g = {"result": "FAIL", "bars": _bars("PASS", "NOT_EVALUABLE"), "reasons": ["dsr: NOT_EVALUABLE"]}
    out = vce.evaluate_grid({"base": {}}, pre, {}, REAL_MENU, composition_runs=True,
                            profit_bars_grader=lambda v: g)
    assert out["grid"]["profit_bars"]["base"]["result"] == "INCONCLUSIVE"
    assert out["idea_status"] == "inconclusive"
    g2 = {"result": "FAIL", "bars": _bars("FAIL", "NOT_EVALUABLE"), "reasons": []}
    out = vce.evaluate_grid({"base": {}}, pre, {}, REAL_MENU, composition_runs=True,
                            profit_bars_grader=lambda v: g2)
    assert out["grid"]["profit_bars"]["base"]["result"] == "FAIL"


def test_grid_grader_and_branch_3_share_the_invalidation_rule(monkeypatch):
    """Review fix 4: an invalidated trial is never graded by either -- the
    grid cell is INCONCLUSIVE, branch 3's candidate INVALIDATED."""
    run_id = "run_790"
    run_dir = rpr.ROOT / "runs" / run_id
    (run_dir / "artifacts" / "variants" / "base").mkdir(parents=True)
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "base" / "protocol_result.yaml",
                  {"results": [], "per_symbol_summary": {}})
    rpr.save_yaml(run_dir / "artifacts" / "grid_evaluation.yaml", {"variants": ["base"]})
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml",
                  {"variants": {"base": {"status": "validated"}}})
    monkeypatch.setattr(rpr, "_invalidated_trial_ids", lambda: {f"{run_id}:base"})
    monkeypatch.setattr(rpr, "_load_profitability_bars", lambda *a: {})
    monkeypatch.setattr(rpr, "_promotion_dsr_context", lambda: {})
    monkeypatch.setattr(rpr, "_variant_loop_enabled", lambda: True)
    graded = rpr._profit_bars_grid_grader(run_dir, run_id)("base")
    assert graded["result"] == "INVALIDATED"
    b3 = rpr._profit_bars_backtest_candidates(run_dir, run_id)["base"]
    assert b3["result"] == "INVALIDATED"
    crit = rpr._code_added_criterion(REAL_MENU, "profit_bars")
    out = vce.evaluate_grid({"base": {}}, {"pass_rule": {"criteria": [crit]}}, {}, REAL_MENU,
                            composition_runs=True, profit_bars_grader=lambda v: graded)
    assert out["grid"]["profit_bars"]["base"]["result"] == "INCONCLUSIVE"


# ---------------------------------------------------------------------------
# 6. 7.5 -- a reader patch from a composition run (review fixes 3 and 6)
# ---------------------------------------------------------------------------

def _composition_source(tmp_path, field="params.period", delta=2):
    from test_e059_s2a_decide_next import _patch
    doc, m, cfgs = _written(tmp_path)
    before = _reg(cfgs["base"])["components"][0]
    for part in field.split("."):
        before = before[part]
    p = _patch("profitability-run_061-1", component_id="b0__sig", field=field,
               before=before, after=before + delta)
    inputs = _one_source([p], config=cfgs["base"], manifest=None)
    inputs["runs"]["run_061"]["composition_manifest"] = m
    inputs["runs"]["run_061"]["composition_check"] = dn._composition_checker(tmp_path, doc, m)
    return inputs, m, cfgs


def test_patch_on_a_composition_is_feasible_with_its_composition_manifest(tmp_path):
    inputs, m, cfgs = _composition_source(tmp_path)
    rec = _decide(inputs)
    c = _by_id(rec)["profitability-run_061-1"]
    assert c["eligible"] is True and c["gates"]["feasibility"]["result"] == "FEASIBLE"
    _rel, text = dn.candidate_brief(rec, inputs, decision_ref="d.yaml")
    front = yaml.safe_load(re.match(r"\A---\n(.*?\n)---\n", text, re.S).group(1))
    cand = front["candidate"]
    assert "manifest" not in cand and "expected_manifest_sha256" not in cand["source"]
    assert cand["composition"]["manifest_ref"] == "runs/run_061/artifacts/composition_manifest.yaml"
    assert cand["composition"]["manifest_sha256"] == dn.config_sha256(m)
    assert cand["composition"]["registry_hash"] == m["registry_hash"]
    assert cand["source"]["source_kind"] == "composition"
    assert cand["source"]["expected_config_sha256"] == dn.config_sha256(cand["config"])
    assert _reg(cand["config"])["components"][0]["params"]["period"] == \
        _reg(cfgs["base"])["components"][0]["params"]["period"] + 2


@pytest.mark.parametrize("field, delta", [("lookback", 5), ("weight", 1.0)])
def test_patch_that_breaks_the_composition_check_is_infeasible(tmp_path, field, delta):
    """Review fix 3: the same check as 1b/5a, not a pointer check."""
    inputs, _m, _c = _composition_source(tmp_path, field=field, delta=delta)
    c = _by_id(_decide(inputs))["profitability-run_061-1"]
    reasons = c["gates"]["feasibility"]["reasons"]
    if field == "weight":  # a component weight inside a block is its part weight: allowed
        assert c["eligible"] is True, reasons
    else:
        assert c["eligible"] is False
        assert any(r.startswith("composition_check_failed") and "lookback" in r for r in reasons)


def test_flag_off_a_composite_patch_is_infeasible_never_a_crash(campaign_root):
    """Review fix 6: with the flag off decide-next never reads a composition
    manifest -- the patch is source_manifest_missing."""
    from test_e059_s2a_decide_next import _stage_flag_on_source, _patch
    run_dir = _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")])
    (run_dir / "artifacts" / "block_manifest.yaml").unlink()
    (run_dir / "artifacts" / "composition_manifest.yaml").write_text(
        yaml.safe_dump({"kind": "composition"}), encoding="utf-8")
    root = campaign_root["root"]
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    inputs = dn.load_inputs(root, queue, categories=["profitability"], known_classes=None)
    assert "composition_manifest" not in inputs["runs"]["run_061"]
    c = _by_id(_decide(inputs))["profitability-run_061-1"]
    assert c["eligible"] is False
    assert c["gates"]["feasibility"]["reasons"][0].startswith("source_manifest_missing")


def test_a_run_with_neither_manifest_is_still_source_manifest_missing(tmp_path):
    from test_e059_s2a_decide_next import _patch
    c = _by_id(_decide(_one_source([_patch("profitability-run_061-1")], manifest=None)))
    assert c["profitability-run_061-1"]["gates"]["feasibility"]["reasons"][0].startswith(
        "source_manifest_missing")


def test_a_failed_7_5_run_is_composition_failed_whatever_its_origin(campaign_root, monkeypatch):
    """Review fix 3: a reader patch on a composite (origin reader) that fails
    at 1b/5a pauses as composition_failed, never quarantined."""
    root = campaign_root["root"]
    _write_flags(root, **FLAT_COMP_ON)
    cfg = yaml.safe_load((root / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    cfg["orchestrator"]["halt_policy"] = {"quarantine_enabled": True}
    (root / "config" / "campaign_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_071", status="failed",
                                    pending_stage="backtest_specification",
                                    last_error="5a: weights differ")
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml",
                  {"candidate": {"composition": {"manifest_ref": "x"}}})
    e = dict(_entry("run_071", "profitability-run_061-1"), origin="reader", source="agent")
    _save_queue_entries(campaign_root["queue_path"], [e])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_071"], trial_sharpes=[])
    assert camp.process_once() is False
    after = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"][0]
    assert after["status"] == "paused:composition_failed"
    assert "QUARANTINE" not in (root / "campaign_log.md").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 6b. R1: inconclusive re-fire and preparation failures (review fixes 1, 2)
# ---------------------------------------------------------------------------

def _inconclusive_setup(not_eval, graded_basis, now_basis, attempts=1):
    blocks = [_blk("A1"), _blk("A2")]
    base = dn.composition_entry_id("1h", cc.composite_registry_hash(blocks))
    ids = [dn.composition_attempt_id(base, n) for n in range(1, attempts + 1)]
    inputs = _with_comp(_one_source([]), blocks)
    inputs["queue"] = {"queue": [{"id": i, "status": "done", "outcome": "inconclusive",
                                  "origin": "composition", "run_ids": ["run_x"]} for i in ids]}
    inputs["composition"]["inconclusive"] = {ids[-1]: {"not_evaluable": not_eval,
                                                       "dsr_basis": graded_basis}}
    inputs["composition"]["dsr_basis"] = now_basis
    return inputs, base


def test_inconclusive_for_want_of_trials_refires_once_the_ledger_has_them():
    inputs, base = _inconclusive_setup(["deflated_sharpe_threshold"],
                                       {"n_dsr_total": 1, "n_trials": 1},
                                       {"n_dsr_total": 5, "n_trials": 4})
    rec, r1 = _r1(inputs)
    assert r1["fired"] is True and r1["entry_id"] == f"{base}-a2"
    assert "ledger now has" in r1["timeframes"][0]["reason"]
    assert rec["picked"]["composition"] == f"{base}-a2"


@pytest.mark.parametrize("not_eval, graded, now", [
    (["deflated_sharpe_threshold"], {"n_dsr_total": 1, "n_trials": 1},
     {"n_dsr_total": 1, "n_trials": 1}),                      # ledger unchanged: wait
    (["avg_daily_return_min"], {"n_dsr_total": 1, "n_trials": 1},
     {"n_dsr_total": 9, "n_trials": 9}),                      # a property of its own data
    (["deflated_sharpe_threshold"], {"n_dsr_total": 5, "n_trials": 5},
     {"n_dsr_total": 9, "n_trials": 9}),                      # trials were not what was missing
])
def test_inconclusive_never_refires_on_unchanged_inputs(not_eval, graded, now):
    inputs, _base = _inconclusive_setup(not_eval, graded, now)
    _rec, r1 = _r1(inputs)
    assert r1["fired"] is False and r1["timeframes"][0]["status"] == "fired_before"
    assert r1["timeframes"][0]["reason"]


def test_a_refired_attempt_is_itself_never_rerun_while_outstanding():
    inputs, base = _inconclusive_setup(["deflated_sharpe_threshold"],
                                       {"n_dsr_total": 1, "n_trials": 1},
                                       {"n_dsr_total": 5, "n_trials": 5}, attempts=2)
    inputs["queue"]["queue"][-1]["status"] = "ready"
    _rec, r1 = _r1(inputs)
    assert r1["fired"] is False and r1["timeframes"][0]["status"] == "fired_before"


def test_an_unresolved_failure_row_marks_the_block_set_as_fired():
    blocks = [_blk("A1"), _blk("A2")]
    h = cc.composite_registry_hash(blocks)
    inputs = _with_comp(_one_source([]), blocks)
    inputs["composition"]["failures"] = [{"registry_hash": h, "entry_id": "x", "reason": "r",
                                          "resolved": False}]
    _rec, r1 = _r1(inputs)
    assert r1["fired"] is False and r1["timeframes"][0]["status"] == "failed_before"
    inputs["composition"]["failures"][0]["resolved"] = True
    _rec, r1 = _r1(inputs)
    assert r1["fired"] is True
    # a new block-set revision fires regardless of an old failure
    inputs["composition"]["failures"][0]["resolved"] = False
    inputs = _with_comp(inputs, blocks + [_blk("A3")], revision=3)
    inputs["composition"]["failures"] = [{"registry_hash": h, "entry_id": "x", "reason": "r",
                                          "resolved": False}]
    _rec, r1 = _r1(inputs)
    assert r1["fired"] is True


def test_record_composition_failure_is_locked_append_only(tmp_path):
    path = tmp_path / "campaign_record" / "compositions.yaml"
    row = comp.record_composition_failure(path, registry_hash="h", timeframe="1h",
                                          entry_id="e1", reason="boom", enabled=True)
    assert row["resolved"] is False
    comp.record_composition_failure(path, registry_hash="h", timeframe="1h", entry_id="e1",
                                    reason="again", enabled=True)
    rows = comp.load_composition_failures(path)
    assert [r["reason"] for r in rows] == ["boom"]
    assert cc.load_compositions(path) == []
    with pytest.raises(comp.CompositionError, match="composition_runs is off"):
        comp.record_composition_failure(path, registry_hash="h", timeframe="1h", entry_id="e2",
                                        reason="x", enabled=False)


# ---------------------------------------------------------------------------
# 6c. One definition of each shared name (review fix 10)
# ---------------------------------------------------------------------------

def test_single_constants():
    import composition_names as names
    assert comp.MANIFEST_FILENAME is names.MANIFEST_FILENAME
    assert dn.COMPOSITION_MANIFEST_FILE is names.MANIFEST_FILENAME
    assert rpr._COMPOSITION_MANIFEST_FILE is names.MANIFEST_FILENAME
    assert dn.ORIGIN_COMPOSITION is names.ORIGIN_COMPOSITION
    assert camp.COMPOSITION_ORIGIN is names.ORIGIN_COMPOSITION
    assert rpr._residual_ic_menu_entry(REAL_MENU) == rpr._code_added_criterion(REAL_MENU,
                                                                               "residual_ic")


# ---------------------------------------------------------------------------
# 7. A composite never registers as a block
# ---------------------------------------------------------------------------

def test_composite_never_registers_as_a_block(tmp_path, capsys):
    path = tmp_path / "campaign_record" / "block_registry.yaml"
    entry = {"run_id": "run_800", "legacy": False, "idea_status": "validated",
             "engineering_fault": None}
    out = br.record_run(path, tmp_path / "runs" / "run_800", entry, root=tmp_path,
                        composition_runs=True, composition_run=True)
    assert out == {"skipped": cm.REGISTRY_SKIPPED_COMPOSITION} == {"skipped": "composition"}
    assert not path.exists() and "no_manifest" not in capsys.readouterr().out


# ---------------------------------------------------------------------------
# 8. End to end: registry change -> R1 -> composition run -> graded composite
# ---------------------------------------------------------------------------

HANDOFFS = ("research_brief_to_hypothesis.yaml", "hypothesis_to_strategy_config_authoring.yaml",
            "hypothesis_to_innovation_expansion.yaml", "validation_to_backtest_specification.yaml",
            "backtest_spec_to_data_availability_gate.yaml", "backtest_spec_to_protocol_execution.yaml")


def _stage_campaign(campaign_root):
    """Two validated 1h forecast blocks (registry revision 2, their validating
    runs' results on disk), and a just-finished refuted run_061 whose DONE
    step triggers decide-next."""
    root = campaign_root["root"]
    _write_flags(root, **FLAT_COMP_ON)
    for name in ("criterion_menu.yaml", "profitability_bars.yaml"):
        shutil.copy(_SR / "config" / name, root / "config" / name)
    # two composite windows: the first has no prior block data (equal weights),
    # the second starts after the blocks' validating windows (estimated weights)
    proto = {"symbols": ["BTCUSDT", "ETHUSDT"], "timeframe": "1h",
             "windows": [{"label": "2020-01", "test": {"start": "2020-01-01", "end": "2020-02-09"}},
                         {"label": "2020-05", "test": {"start": "2020-05-01", "end": "2020-06-09"}}]}
    (root / "protocols").mkdir(exist_ok=True)
    (root / "protocols" / "p1h.json").write_text(json.dumps(proto), encoding="utf-8")
    doc = _registry(root)
    (root / "campaign_record").mkdir(exist_ok=True)
    (root / "campaign_record" / "block_registry.yaml").write_text(yaml.safe_dump(doc),
                                                                  encoding="utf-8")
    memory = {"schema_version": 1, "legacy_note": "", "runs": {}}
    for k, block in enumerate(doc["blocks"]):
        run = block["validated_by_run"]
        _validating_run(root, block, seed=k)
        arts = root / "runs" / run / "artifacts"
        (arts / "pre_registration.yaml").write_text(yaml.safe_dump(
            {"machine_constraints": {"protocol_ref": "protocols/p1h.json"}}), encoding="utf-8")
        (arts / "research_brief.yaml").write_text(yaml.safe_dump(
            {"strategy_domain": "crypto", "market_universe": "BTCUSDT,ETHUSDT", "timeframe": "1h",
             "research_goal": "g", "venue": "binance", "product": "perp"}), encoding="utf-8")
        memory["runs"][run] = _memory_entry(run, hyp=block["hypothesis_id"],
                                            protocol_ref="protocols/p1h.json",
                                            idea_status="validated")
    memory["runs"]["run_061"] = _memory_entry("run_061")
    (root / "campaign_record" / "campaign_memory.yaml").write_text(yaml.safe_dump(memory),
                                                                    encoding="utf-8")
    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_061", status="completed",
                                    pending_stage="completed_refuted")
    (run_dir / "artifacts" / "idea_status.yaml").write_text(yaml.safe_dump(
        {"run_id": "run_061", "idea_status": "refuted", "result": "FAIL", "reason": "r"}),
        encoding="utf-8")
    _save_queue_entries(campaign_root["queue_path"], [_entry("run_061")])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_061"], trial_sharpes=[])
    return doc


def _fake_subprocess(calls):
    """validate_config.py -> ok; run_protocol.py -> a 1-window, 2-coin result
    with per-window equity and bars files (fixture data, not a backtest)."""
    def run(cmd, *a, **k):
        class _R:
            returncode, stdout, stderr = 0, "", ""
        cmd = [str(c) for c in cmd]
        calls.append(cmd)
        if cmd[1].endswith("run_protocol.py"):
            out_dir = Path(cmd[cmd.index("--out-dir") + 1])
            vid = out_dir.name
            results = []
            for k, s in enumerate(("BTCUSDT", "ETHUSDT")):
                wrid = f"w_{vid}_{s}"
                _equity_csv(out_dir / "results" / wrid / "portfolio_states.csv", seed=k + len(vid))
                results.append({"symbol": s, "window": "2020-01", "run_id": wrid,
                                "core": {"trade_count": 40, "sharpe": 0.1}})
            summary = {"results": results, "verdict": "kill", "protocol_file": cmd[3],
                       "per_symbol_summary": {s: {"median_sharpe": 0.1, "max_abs_drawdown_pct": 5.0,
                                                  "min_trade_count": 40}
                                              for s in ("BTCUSDT", "ETHUSDT")},
                       "hypothesis_verdict": {"verdict": "refine", "diagnostics": {}}}
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "protocol_summary.json").write_text(json.dumps(summary), encoding="utf-8")
        return _R()
    return run


def test_end_to_end_registry_change_to_graded_composite(campaign_root, monkeypatch):
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    root = campaign_root["root"]
    doc = _stage_campaign(campaign_root)

    # --- step 1: run_061 finishes -> decide-next -> R1 ---------------------
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    assert camp.process_once() is True
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]
    done, new = queue
    h = cc.composite_registry_hash(doc["blocks"])
    eid = f"composition-1h-{h}"
    assert done["outcome"] == "refuted"
    assert new["id"] == eid and new["origin"] == "composition" and new["status"] == "ready"
    assert new["priority"] == 998 and new["source"] == "agent"
    record = yaml.safe_load((root / "runs" / "run_061" / "artifacts" / "decision_record.yaml")
                            .read_text(encoding="utf-8"))
    assert record["rules"]["r1"]["fired"] is True and record["picked"]["composition"] == eid
    cdir = root / "campaign_record" / "compositions" / eid
    assert sorted(p.name for p in cdir.iterdir()) == [
        "base.json", "composition_manifest.yaml", "ic_weighted.json", "vol_scaled.json"]
    manifest = yaml.safe_load((cdir / "composition_manifest.yaml").read_text(encoding="utf-8"))
    # vol_scaled: window 1 (no prior data) equal; window 2 = 1/sigma of each
    # block's stand-alone daily returns dated before 2020-05-01 (all of them here)
    first, second = manifest["variants"]["vol_scaled"]["weight_schedule"]
    assert first["from"] == "2020-01-01" and first["basis"]["estimated"] is False
    assert set(first["weights"].values()) == {0.5}
    sig = {b["block_id"]: statistics.stdev(r for _d, r in comp.load_block_daily_returns(b, root=root))
           for b in doc["blocks"]}
    inv = {b: 1 / s for b, s in sig.items()}
    assert second["from"] == "2020-05-01" and second["basis"]["estimated"] is True
    assert second["weights"] == {b: pytest.approx(v / sum(inv.values()), rel=1e-12)
                                 for b, v in inv.items()}
    ic_first, ic_second = manifest["variants"]["ic_weighted"]["weight_schedule"]
    assert ic_first["basis"]["estimated"] is False  # nothing measured before window 1
    comps = yaml.safe_load((root / "campaign_record" / "compositions.yaml").read_text(
        encoding="utf-8"))["compositions"]
    assert [c["registry_hash"] for c in comps] == [h]
    assert cc.resolve_current_composite(doc, comps, "1h")["kind"] == "composition"
    brief = camp._parse_brief_frontmatter(root / new["brief_path"])
    assert brief["candidate"]["source"]["origin"] == "composition"
    assert "pass_rule" not in brief["machine_constraints"]

    # --- step 2: the composition run; 1a / 1b / step 2 never call an LLM ---
    # (the fixture protocol results are not full protocol_result documents,
    # so artifact validation goes back to warn-only; the card is checked
    # against its schema explicitly below)
    monkeypatch.delenv("WORKFLOW_ARTIFACT_VALIDATION")
    monkeypatch.setattr(rpr, "run_loop", RUN_LOOP)
    async def _no_llm(stage, *a, **k):
        pytest.fail(f"LLM stage invoked: {stage}")
    monkeypatch.setattr(rpr, "run_claude_worker", _no_llm)
    monkeypatch.setattr(rpr, "run_gemini_worker", _no_llm)
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))
    calls = []
    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess(calls))
    readers = []

    def _readers(run_id, run_dir, attempt):
        """The first composition run's profitability reader proposes one
        patch (7.5): a component parameter of block b0."""
        readers.append(run_id)
        if len(readers) == 1:
            from test_e059_s2a_decide_next import _patch
            spec = json.loads((run_dir / "artifacts" / "variants" / "base" /
                               "strategy_config.json").read_text(encoding="utf-8"))
            period = _reg(spec)["components"][0]["params"]["period"]
            (run_dir / "artifacts" / "proposals").mkdir(exist_ok=True)
            (run_dir / "artifacts" / "proposals" / "profitability.yaml").write_text(yaml.safe_dump(
                [_patch(f"profitability-{run_id}-1", component_id="b0__sig",
                        field="params.period", before=period, after=period + 2)]),
                encoding="utf-8")
    monkeypatch.setattr(rpr, "_run_specialist_readers_stage", _readers)
    monkeypatch.setattr(rpr, "_refresh_regime_detector_report_for_readers", lambda *a: None)
    import build_reports
    # E-061 C2 S2d: the variant-loop call site now also passes
    # variants=/failed_variants=/untested_variants= -- accept and ignore them,
    # this stub only exists to skip real report building against fixture
    # protocol results that aren't full protocol_result documents.
    monkeypatch.setattr(build_reports, "build_reports",
                         lambda run_dir, write=True, **kwargs: {})

    def _scaffold(run_id):
        run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], run_id,
                                        pending_stage="hypothesis_generation")
        for name in HANDOFFS:
            (run_dir / "handoffs" / name).write_text(yaml.safe_dump(
                {"required_inputs": [], "deliverables": []}), encoding="utf-8")
    monkeypatch.setattr(camp, "setup_run", _scaffold)

    keep_going = camp.process_once()
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]
    entry = next(e for e in queue if e["id"] == eid)
    run_id = entry["run_ids"][0]
    run_dir = root / "runs" / run_id
    arts = run_dir / "artifacts"
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state.get("last_error") is None, state.get("last_error")

    # 1a: the code-written card and the profit bars as the only criterion
    card = yaml.safe_load((arts / "hypothesis_card.yaml").read_text(encoding="utf-8"))
    assert card["hypothesis_id"] == f"COMPOSITION-1h-{h}" and card["pass_through"] is True
    jsonschema = pytest.importorskip("jsonschema")
    jsonschema.Draft7Validator(json.loads((_SR / "workflow_artifacts" / "schemas" /
                                           "hypothesis_card.schema.json").read_text(
        encoding="utf-8"))).validate(card)
    pre = yaml.safe_load((arts / "pre_registration.yaml").read_text(encoding="utf-8"))
    assert [c["id"] for c in pre["pass_rule"]["criteria"]] == ["profit_bars"]
    assert "pass_rule_pending" not in pre
    # 1b: the code-written base, the manifest, no block manifest
    spec = yaml.safe_load((arts / "backtest_spec.yaml").read_text(encoding="utf-8"))
    assert dn.config_sha256(spec["config"]) == manifest["variants"]["base"]["config_sha256"]
    assert yaml.safe_load((arts / "composition_manifest.yaml").read_text(encoding="utf-8")) == manifest
    assert not (arts / "block_manifest.yaml").exists()
    # step 2 + 5a: the three code-written variants, byte for byte
    for vid in ("base", "vol_scaled", "ic_weighted"):
        cfg = json.loads((arts / "variants" / vid / "strategy_config.json").read_text(encoding="utf-8"))
        assert dn.config_sha256(cfg) == manifest["variants"][vid]["config_sha256"]
    # backtests: exactly one trial row per variant, nothing else
    rows = yaml.safe_load(campaign_root["campaign_state_path"].read_text(encoding="utf-8"))["trial_sharpes"]
    assert sorted(r["trial_id"] for r in rows) == [f"{run_id}:{v}" for v in
                                                    ("base", "ic_weighted", "vol_scaled")]
    # the grid grades profit_bars with branch 3's own function: same answer per variant
    grid = yaml.safe_load((arts / "grid_evaluation.yaml").read_text(encoding="utf-8"))
    pbe = yaml.safe_load((arts / "profit_bars_evaluation.yaml").read_text(encoding="utf-8"))
    assert grid["criteria"] == ["profit_bars"]
    for vid in ("base", "vol_scaled", "ic_weighted"):
        assert grid["grid"]["profit_bars"][vid]["result"] == pbe["variants"][vid]["result"]
        assert grid["grid"]["profit_bars"][vid]["bars"] == pbe["variants"][vid]["bars"]
        assert pbe["variants"][vid]["kind"] == "composite"
    ric = yaml.safe_load((arts / "residual_ic.yaml").read_text(encoding="utf-8"))
    assert ric["skipped"] == "composition run"
    # the readers ran; regroup recorded the run and registered no block
    assert readers == [run_id]
    mem = yaml.safe_load((root / "campaign_record" / "campaign_memory.yaml").read_text(encoding="utf-8"))
    assert mem["runs"][run_id]["registry"] == {"skipped": "composition"}
    assert br.load_registry(root / "campaign_record" / "block_registry.yaml") == doc
    # the idea status came from the grid only; the run ended through decide-next
    idea = yaml.safe_load((arts / "idea_status.yaml").read_text(encoding="utf-8"))
    assert idea["idea_status"] == grid["idea_status"]
    # Branch 3 passes nothing; each grid cell reads the same bars: FAIL when a
    # bar FAILs, INCONCLUSIVE when one is NOT_EVALUABLE (review fix 1).
    assert pbe["passing"] == []
    for vid in ("base", "vol_scaled", "ic_weighted"):
        res = [b["result"] for b in pbe["variants"][vid]["bars"]]
        want = "FAIL" if "FAIL" in res else ("INCONCLUSIVE" if "NOT_EVALUABLE" in res else "PASS")
        assert grid["grid"]["profit_bars"][vid]["result"] == want
        assert grid["grid"]["profit_bars"][vid]["weight_schedule"] == \
            manifest["variants"][vid]["weight_schedule"]
    assert entry["status"] == "done" and entry["outcome"] == grid["idea_status"]
    rec2 = yaml.safe_load((run_dir / "artifacts" / "decision_record.yaml").read_text(
        encoding="utf-8"))
    # R1 never fires twice for the same registry state and the same inputs
    assert rec2["rules"]["r1"]["fired"] is False
    assert rec2["rules"]["r1"]["timeframes"][0]["status"] == "fired_before"

    # --- step 3 (7.5): the reader's patch on the composite is accepted with
    # the composition manifest as its source, and runs as a composition too --
    pid = f"profitability-{run_id}-1"
    assert rec2["picked"]["candidate_id"] == pid
    child_entry = next(e for e in yaml.safe_load(campaign_root["queue_path"].read_text(
        encoding="utf-8"))["queue"] if e["id"] == pid)
    assert child_entry["origin"] == "reader" and child_entry["status"] == "ready"
    camp.process_once()
    child_entry = next(e for e in yaml.safe_load(campaign_root["queue_path"].read_text(
        encoding="utf-8"))["queue"] if e["id"] == pid)
    child = child_entry["run_ids"][0]
    carts = root / "runs" / child / "artifacts"
    cstate = yaml.safe_load((root / "runs" / child / "pipeline_state.yaml").read_text(
        encoding="utf-8"))
    assert cstate.get("last_error") is None, cstate.get("last_error")
    ccard = yaml.safe_load((carts / "hypothesis_card.yaml").read_text(encoding="utf-8"))
    assert ccard["hypothesis_id"] == f"COMPOSITION-1h-{h}__{pid}"
    assert [c["id"] for c in yaml.safe_load((carts / "pre_registration.yaml").read_text(
        encoding="utf-8"))["pass_rule"]["criteria"]] == ["profit_bars"]
    patched = json.loads((carts / "variants" / "base" / "strategy_config.json").read_text(
        encoding="utf-8"))
    assert _reg(patched)["components"][0]["params"]["period"] == period_after(manifest, root)
    assert dn.config_sha256(patched) != manifest["variants"]["base"]["config_sha256"]
    for vid in ("vol_scaled", "ic_weighted"):  # the schemes' weights on the patched composite
        v = json.loads((carts / "variants" / vid / "strategy_config.json").read_text(
            encoding="utf-8"))
        assert {b["id"]: b["weight"] for b in _reg(v)["blocks"]} == {
            mb["config_block_id"]: manifest["variants"][vid]["weights"][mb["block_id"]]
            for mb in manifest["blocks"]}
    assert not (carts / "block_manifest.yaml").exists()
    mem = yaml.safe_load((root / "campaign_record" / "campaign_memory.yaml").read_text(
        encoding="utf-8"))
    assert mem["runs"][child]["registry"] == {"skipped": "composition"}
    assert br.load_registry(root / "campaign_record" / "block_registry.yaml") == doc
    assert readers == [run_id, child]
    # nothing touched the sealed store
    assert not any("holdout_sealed" in " ".join(c) for c in calls)


def period_after(manifest, root):
    """The patched period: the source block's validated period + 2."""
    base = json.loads((root / manifest["variants"]["base"]["config_ref"]).read_text(
        encoding="utf-8"))
    return _reg(base)["components"][0]["params"]["period"] + 2


RUN_LOOP = rpr.run_loop  # the real one (step 1 stubs it)


def test_r1_preparation_failure_is_a_classified_pause_and_the_campaign_continues(
        campaign_root, monkeypatch):
    """Review fix 2: a block's stand-alone returns are missing -> no raw
    traceback; a failure row, a paused composition entry and a halt_history
    record; the decision is made again without it (here: a reader candidate
    is picked) and R1 never re-fires that block set."""
    from test_e059_s2a_decide_next import _patch
    root = campaign_root["root"]
    doc = _stage_campaign(campaign_root)
    run0 = doc["blocks"][0]["validated_by_run"]
    (root / "runs" / run0 / "artifacts" / "variants" / "base" / "protocol_result.yaml").unlink()
    # run_061 also has a reader proposal, so there is something else to run
    arts = root / "runs" / "run_061" / "artifacts"
    (arts / "proposals").mkdir()
    (arts / "proposals" / "profitability.yaml").write_text(yaml.safe_dump(
        [_patch("profitability-run_061-1")]), encoding="utf-8")
    src = _src([])
    for name, d in (("block_manifest.yaml", {"block": {"kind": "forecast", "config_paths": [
                        "/strategies/regimes/unknown/components/0"]},
                        "scaffolding": ["/regime_detector"], "rationale": "r"}),
                    ("pre_registration.yaml", src["pre_registration"]),
                    ("research_brief.yaml", src["research_brief"]),
                    ("hypothesis_card.yaml", src["card"])):
        (arts / name).write_text(yaml.safe_dump(d), encoding="utf-8")
    from test_e059_s2a_decide_next import _base_config
    (arts / "variants" / "base").mkdir(parents=True)
    (arts / "variants" / "base" / "strategy_config.json").write_text(
        json.dumps(_base_config()), encoding="utf-8")
    mem_path = root / "campaign_record" / "campaign_memory.yaml"
    mem = yaml.safe_load(mem_path.read_text(encoding="utf-8"))
    mem["runs"]["run_061"] = _memory_entry("run_061", proposal_ids=["profitability-run_061-1"])
    mem_path.write_text(yaml.safe_dump(mem), encoding="utf-8")
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)

    assert camp.process_once() is True  # no traceback, the campaign continues
    h = cc.composite_registry_hash(doc["blocks"])
    eid = f"composition-1h-{h}"
    queue = {e["id"]: e for e in yaml.safe_load(
        campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]}
    assert queue[eid]["status"] == "paused:composition_failed"
    assert queue[eid]["origin"] == "composition" and queue[eid]["run_ids"] == []
    assert queue["profitability-run_061-1"]["status"] == "ready"
    rows = comp.load_composition_failures(root / "campaign_record" / "compositions.yaml")
    assert [r["registry_hash"] for r in rows] == [h] and "protocol_result.yaml" in rows[0]["reason"]
    state = yaml.safe_load((root / "runs" / "run_061" / "pipeline_state.yaml").read_text(
        encoding="utf-8"))
    assert state["halt_history"][-1]["reason"] == "composition_failed"
    rec = yaml.safe_load((arts / "decision_record.yaml").read_text(encoding="utf-8"))
    assert rec["picked"]["candidate_id"] == "profitability-run_061-1"
    assert rec["rules"]["r1"]["timeframes"][0]["status"] == "failed_before"
    assert "HALT — composition_failed" in (root / "campaign_log.md").read_text(encoding="utf-8")


def test_a_crashed_composition_run_pauses_and_is_never_quarantined(campaign_root, monkeypatch):
    root = campaign_root["root"]
    _write_flags(root, **FLAT_COMP_ON)
    cfg = yaml.safe_load((root / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    cfg["orchestrator"]["halt_policy"] = {"quarantine_enabled": True}
    (root / "config" / "campaign_config.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_070", status="failed",
                          pending_stage="protocol_execution", last_error="boom")
    e = dict(_entry("run_070", "composition-1h-abc"), origin="composition", source="agent")
    _save_queue_entries(campaign_root["queue_path"], [e])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_070"], trial_sharpes=[])
    assert camp.process_once() is False
    after = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"][0]
    assert after["status"] == "paused:composition_failed" and after.get("outcome") is None
    log = (root / "campaign_log.md").read_text(encoding="utf-8")
    assert "HALT — composition_failed: unhandled_exception: boom" in log
    assert "QUARANTINE" not in log
