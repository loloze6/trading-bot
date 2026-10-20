"""D-162 (vehicle-format V2-2 + V3, one PR): a config vehicle is routed.

  decide_next   side_finding_start starts the child from the vehicle's config with the
                source manifest as config_vehicle.derived_manifest relabels it; the candidate
                is re-checked on every pass (manifest, the ungated twin's block paths,
                requires_op:/requires_component:, exact_config_1b_off); the brief carries the
                config and its manifest as D-110's exact constraints; a slim vehicle copy
                (Q4); component_request_rows (V2b).
  run_campaign  passes known_ops (lazily) and exact_config_1b, and appends the rows once per
                (kind, name).
  1b            copies the vehicle's config (D-110), refuses a piece that is still missing,
                and still refuses a patch pass-through.
  step 2        a regime gate's design variant is its ungated twin, written by code.
  reader_findings / fold_confirm / explore_confirm   the merge key, the whole-config
                comparison, the PENDING route.
  PREFILLED_CLAIM.md / analyst SKILL.md   the texts.

No LLM, no backtest, no market data.
"""
from __future__ import annotations

import ast
import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import block_manifest as bm  # noqa: E402
import campaign_review_retired as crr  # noqa: E402
import config_vehicle as cv  # noqa: E402
import decide_next as dn  # noqa: E402
import explore_confirm as ec  # noqa: E402
import fold_confirm as fc  # noqa: E402
import forecast_rules as fr  # noqa: E402
import json_pointer as jp  # noqa: E402
import reader_findings as rfi  # noqa: E402
import reader_proposals as rp  # noqa: E402
import run_campaign as camp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

import test_e077_pr2_confirm as e077  # noqa: E402
from test_d051_d053_forecast_rules import CONFIG, MANIFEST, SC  # noqa: E402
from test_e068_5_readers_v3 import _claim, _scores  # noqa: E402
from test_e072_explore_confirm import _pure_claim  # noqa: E402
from test_exact_config_1b import ON, _run  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
from test_halt_quarantine_policy import campaign_root  # noqa: E402,F401  (fixture)

RUN, CAT = "run_070", "trade_efficiency"
TB = cv.TBOT_ROOT
NEW_OP = "kalman_smooth"                                   # not in TRANSFORM_OPS_REGISTRY
NEW_CLASS = SC + "KalmanTrendComponent"                    # not in strategy_components.py
STANDARDISE = {"op": "standardise", "params": {"window": 20, "min_periods": 5}}
RULE = {"regime": "trending", "any_of": [[{"id": "er", "op": "gte", "value": 0.4}]]}
VETO = {"id": "er", "transforms": [], "rules": [{"op": "lt", "value": 0.1}], "result": "chop",
        "consecutive_bars": 2}
CHANGE = [{"component_id": "rsi", "field": "params.period", "before": 14, "after": 21}]
ELIGIBLE = "the vehicle's config, copied by code at 1b (D-110); step 3's data gate stays binding"
EXACT_OFF = ("exact_config_1b_off: a config vehicle is built only by D-110's exact-config 1b "
             "(the config and its block manifest copied by code), and "
             "orchestrator.exact_config_1b is off")


def _gated(rules=(RULE,), vetoes=(VETO,)) -> dict:
    """CONFIG's strategy moved unknown -> trending, traded only when the gate says so."""
    cfg = copy.deepcopy(CONFIG)
    regimes = cfg["strategies"]["regimes"]
    regimes["trending"], regimes["unknown"] = regimes["unknown"], None
    cfg["regime_detector"]["rules"] = copy.deepcopy(list(rules))
    cfg["regime_detector"]["vetoes"] = copy.deepcopy(list(vetoes))
    return cfg


def _with_op(cfg, op=NEW_OP) -> dict:
    cfg = copy.deepcopy(cfg)
    (regime,) = cv._trading_regimes(cfg)
    cfg["strategies"]["regimes"][regime]["components"][0]["transforms"] = [
        STANDARDISE, {"op": op, "params": {"q": 0.01}}, {"op": "clip", "params": {"min": -20, "max": 20}}]
    return cfg


def _with_class(cfg, cls=NEW_CLASS) -> dict:
    cfg = copy.deepcopy(cfg)
    (regime,) = cv._trading_regimes(cfg)
    cfg["strategies"]["regimes"][regime]["components"].append(
        {"id": "kalman", "class": cls, "params": {"period": 20}, "weight": 1.0,
         "transforms": [STANDARDISE]})
    return cfg


def _req(kind="op", name=NEW_OP, spec="a one-dimensional Kalman filter of the value") -> dict:
    return {"kind": kind, "name": name, "spec": spec, "example": f"{{name: {name}}}"}


def _vehicle(config, **extra) -> dict:
    return {"kind": "config", "config": copy.deepcopy(config), **extra}


def _side(vehicle=None, combines_as="regime_gate", n=1, claim=None, **extra) -> dict:
    p = {"proposal_id": f"{CAT}-{RUN}-{n}", "kind": rp.SIDE_FINDING, "claim": claim or _claim(),
         "evidence": ["variants.base.slices.overall.y=2"], "scores": _scores(), "model_id": "m",
         "rubric_version": f"{CAT}-reading-v1", **extra}
    if vehicle is not None:
        p.update(vehicle=vehicle, combines_as=combines_as, fold_observed="A")
    return p


def _memory_entry() -> dict:
    return {"run_id": RUN, "hypothesis_id": "H-070", "timeframe": "1h",
            "variants": {"base": {"status": "tested", "symbols": ["BTCUSD"], "n_windows": 6,
                                  "config_ref": f"runs/{RUN}/artifacts/variants/base/"
                                                f"strategy_config.json"}}}


def _src(*proposals, manifest=None) -> dict:
    return {"proposals": [{"category": CAT, "proposal": p} for p in proposals],
            "base_variant": "base", "base_config": copy.deepcopy(CONFIG),
            "base_config_ref": f"runs/{RUN}/artifacts/variants/base/strategy_config.json",
            "manifest": copy.deepcopy(MANIFEST if manifest is None else manifest),
            "pre_registration": {"machine_constraints": {"protocol_ref": "protocols/p.json"}},
            "research_brief": {"strategy_domain": "d", "market_universe": "u", "timeframe": "1h",
                               "venue": "kraken", "product": "perp"},
            "card": None, "card_text": None}


def _old_inputs(src) -> dict:
    return {"memory": {"runs": {RUN: _memory_entry()}}, "queue": {"queue": []},
            "existing_candidate_briefs": [], "known_classes": dn.known_component_classes(TB),
            "feed_set": None, "digest": None, "protocol_specs": {}, "runs": {RUN: src}}


def _inputs(src, **over) -> dict:
    out = {**_old_inputs(src), "known_ops": dn.known_ops(TB), "exact_config_1b": True}
    out.update(over)
    return {k: v for k, v in out.items() if v is not _DROP}


_DROP = object()


def _cand(p, src=None, **over) -> dict:
    src = src or _src(p)
    return dn._candidate(RUN, _memory_entry(), src, CAT, p, _inputs(src, **over), {})


def _reasons(cand) -> list:
    return cand["gates"]["feasibility"]["reasons"]


def _front(p, src=None, inputs=None) -> dict:
    src = src or _src(p)
    inputs = inputs or _inputs(src)
    cand = dn._candidate(RUN, _memory_entry(), src, CAT, p, inputs, {})
    record = {"picked": {"candidate_id": cand["candidate_id"], "brief_path": "x/y.md"},
              "candidates": [cand]}
    _rel, text = dn.candidate_brief(record, inputs, decision_ref="d")
    return yaml.safe_load(text.split("---\n")[1])


# ---------------------------------------------------------------------------
# decide_next: the pieces
# ---------------------------------------------------------------------------

def test_the_prefix_copies_equal_the_orchestrators_and_decide_next_never_imports_it():
    assert dn.BRIEF_EXACT_CONFIG_PREFIX == rpr.BRIEF_EXACT_CONFIG_PREFIX
    assert dn.BRIEF_EXACT_MANIFEST_PREFIX == rpr.BRIEF_EXACT_MANIFEST_PREFIX
    tree = ast.parse(Path(dn.__file__).read_text(encoding="utf-8"))
    names = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    names |= {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
    assert "run_phase1_research" not in names and "run_campaign" not in names


def test_known_ops_is_the_registry_read_with_ast(tmp_path):
    vc = cv._validate_config_module(TB)
    assert dn.known_ops(TB) == sorted(vc.TRANSFORM_OPS_REGISTRY)
    (tmp_path / "strategies").mkdir()
    reg = tmp_path / "strategies" / "registry.py"
    reg.write_text("import nothing_importable\nX = {'a': 1}\nTRANSFORM_OPS_REGISTRY = {'b': 2}\n",
                   encoding="utf-8")
    assert dn.known_ops(tmp_path) == ["b"]                          # never imported
    for bad in ("TRANSFORM_OPS_REGISTRY = dict(a=1)\n", "TRANSFORM_OPS_REGISTRY = {}\n",
                "OTHER = {'a': 1}\n", "TRANSFORM_OPS_REGISTRY: dict = {1: 2}\n"):
        reg.write_text(bad, encoding="utf-8")
        with pytest.raises(dn.DecideNextError, match="TRANSFORM_OPS_REGISTRY"):
            dn.known_ops(tmp_path)


def test_side_finding_start_of_a_config_vehicle():
    gate = _gated()
    p = _side(_vehicle(gate))
    start = dn.side_finding_start(p, _src())
    derived = cv.derived_manifest(MANIFEST, CONFIG, gate, "regime_gate")
    assert start == {"config": gate, "manifest": derived, "ops": [], "reason": None,
                     "config_vehicle": True}
    assert derived["block"]["config_paths"] == ["/strategies/regimes/trending/components/0"]
    start["config"]["x"] = 1                                     # a copy
    assert "x" not in p["vehicle"]["config"]
    # forecast_block: no relabel, the source manifest as it is
    fb = dn.side_finding_start(_side(_vehicle(CONFIG), "forecast_block"), _src())
    assert fb["manifest"] == MANIFEST and fb["config_vehicle"] is True


def test_a_config_vehicle_on_a_composite_or_without_a_source_config_is_a_reason():
    p = _side(_vehicle(_gated()))
    comp = dn.side_finding_start(p, {**_src(), "composition_manifest": {"members": []}})
    assert comp["config"] is None and comp["reason"].startswith("config_change_on_composition")
    for drop in ("base_config", "manifest"):
        start = dn.side_finding_start(p, {**_src(), drop: None})
        assert start["config"] is None and start["reason"].startswith("source_config_missing")


def test_patch_and_plain_findings_are_byte_identical_with_the_new_inputs():
    """Every new branch is keyed on a mapping vehicle: a plain finding, a config_change and
    a patch-list vehicle give the same start, candidate and brief with or without the new
    inputs (known_ops, exact_config_1b)."""
    for p in (_side(), _side(config_change=copy.deepcopy(CHANGE)),
              _side(copy.deepcopy(CHANGE), combines_as="forecast_block")):
        if isinstance(p.get("vehicle"), list):
            p["config_change"] = p["vehicle"]                      # as flatten_reading does
        src = _src(p)
        start = dn.side_finding_start(p, src)
        assert "config_vehicle" not in start
        old_in, new_in = _old_inputs(src), _inputs(src)
        old = dn._candidate(RUN, _memory_entry(), src, CAT, p, old_in, {})
        new = dn._candidate(RUN, _memory_entry(), src, CAT, p, new_in, {})
        assert old == new and old["eligible"] is True
        assert _front(p, src, old_in) == _front(p, src, new_in)
        assert "constraints" not in _front(p, src, new_in)


# ---------------------------------------------------------------------------
# decide_next: the candidate
# ---------------------------------------------------------------------------

def test_a_config_vehicle_with_every_piece_and_the_flag_is_eligible():
    gate = _gated()
    cand = _cand(_side(_vehicle(gate)))
    assert cand["eligible"] is True and cand["gates"]["feasibility"]["result"] == "UNKNOWN"
    assert _reasons(cand) == [ELIGIBLE]
    assert cand["resolved_config_sha256"] == dn.config_sha256(gate)
    assert cand["gates"]["novelty"]["exact_match"] == "NOVEL"
    # the same config already run on the same key: a repeat, as for a config change
    key = dn.novelty_key(dn.config_sha256(gate), ["BTCUSD"], _memory_entry(), {})
    src = _src(_side(_vehicle(gate)))
    again = dn._candidate(RUN, _memory_entry(), src, CAT, _side(_vehicle(gate)), _inputs(src),
                          {key: ["run_060"]})
    assert again["gates"]["novelty"]["exact_match"] == "REPEAT" and again["eligible"] is False


def test_a_missing_op_is_requires_op():
    cand = _cand(_side(_vehicle(_with_op(_gated()), requires=[_req()])))
    assert cand["eligible"] is False
    assert _reasons(cand) == [f"requires_op:{NEW_OP} -- not in TRANSFORM_OPS_REGISTRY "
                              f"(strategies.registry) yet; eligible as it stands once it is"]


def test_a_missing_component_is_requires_component_not_unknown_component_class():
    cand = _cand(_side(_vehicle(_with_class(_gated()),
                                requires=[_req("component", NEW_CLASS)])))
    assert cand["eligible"] is False
    assert _reasons(cand) == [f"requires_component:{NEW_CLASS} -- not defined in "
                              f"strategies.strategy_components yet; eligible as it stands once "
                              f"it is"]
    assert not any("unknown_component_class" in r for r in _reasons(cand))


def test_no_known_sets_supplied_names_every_piece():
    cand = _cand(_side(_vehicle(_gated())), known_ops=None, known_classes=None)
    ops, classes = cv.used_pieces(_gated())
    assert _reasons(cand) == (
        [f"requires_op:{o} -- no known op set was supplied" for o in sorted(ops)]
        + [f"requires_component:{c} -- no known class set was supplied" for c in sorted(classes)])


def test_exact_config_1b_off_is_infeasible():
    for over in ({"exact_config_1b": _DROP}, {"exact_config_1b": False}):
        cand = _cand(_side(_vehicle(_gated())), **over)
        assert cand["eligible"] is False and _reasons(cand) == [EXACT_OFF]


def test_a_manifest_that_does_not_fit_is_manifest_unresolved():
    cfg = copy.deepcopy(CONFIG)
    del cfg["strategies"]["warmup"]                          # a scaffolding path gone
    (reason,) = _reasons(_cand(_side(_vehicle(cfg), "forecast_block")))
    assert reason.startswith("manifest_unresolved: the source run's block manifest, as the "
                             "child runs it (config_vehicle.derived_manifest): manifest path(s) "
                             "['/strategies/warmup'] do not resolve"), reason


def test_the_ungated_twin_must_resolve_the_block_paths():
    manifest = {"block": {"kind": "forecast", "config_paths": [
        "/strategies/regimes/unknown/components/0", "/regime_detector/rules/0"]},
        "scaffolding": ["/strategies/warmup"], "rationale": "the gated block"}
    p = _side(_vehicle(_gated()))
    (reason,) = _reasons(_cand(p, _src(p, manifest=manifest)))
    assert reason == ("manifest_unresolved: the ungated twin (D-052, the run's design variant) "
                      "does not resolve the block path(s) ['/regime_detector/rules/0']")
    # a regime_gate config with no gate form (a file written before D-160): no twin
    (reason,) = _reasons(_cand(_side(_vehicle(CONFIG))))
    assert reason.startswith("manifest_unresolved: the ungated twin (D-052, the run's design "
                             "variant) cannot be derived: config.regime_detector: combines_as "
                             "regime_gate needs the gate")


def test_q6_a_regime_claim_kind_stays_regime_block_needs_composition():
    claim = dict(_claim(), kind="regime_classifier")
    cand = _cand(_side(_vehicle(_gated()), claim=claim))
    assert cand["eligible"] is False
    assert any(r.startswith("regime_block_needs_composition") for r in _reasons(cand))


def test_eligibility_flips_with_no_rewrite_once_the_piece_exists():
    p = _side(_vehicle(_with_class(_with_op(_gated())),
                       requires=[_req(), _req("component", NEW_CLASS)]))
    before = copy.deepcopy(p)
    assert _cand(p)["eligible"] is False
    only_op = _cand(p, known_ops=dn.known_ops(TB) + [NEW_OP])
    assert [r.split(" -- ")[0] for r in _reasons(only_op)] == [f"requires_component:{NEW_CLASS}"]
    both = _cand(p, known_ops=dn.known_ops(TB) + [NEW_OP],
                 known_classes=dn.known_component_classes(TB) + [NEW_CLASS])
    assert both["eligible"] is True and _reasons(both) == [ELIGIBLE]
    assert p == before                                         # nothing rewritten


# ---------------------------------------------------------------------------
# V2b: component_requests.yaml, once per name
# ---------------------------------------------------------------------------

def _decide(*proposals, **over):
    src = _src(*proposals)
    inputs = _inputs(src, **over)
    return inputs, dn.decide(inputs, now="2026-10-20T00:00:00+00:00",
                             trigger={"after_run": RUN, "after_entry": "E"})


def test_component_request_rows_once_per_name_first_spec_kept(tmp_path):
    first = _side(_vehicle(_with_op(_gated()), requires=[_req(spec="spec one")]), n=1)
    second = _side(_vehicle(_with_class(_with_op(_gated())),
                            requires=[_req(spec="spec two"), _req("component", NEW_CLASS)]), n=2)
    plain = _side(n=3)
    inputs, record = _decide(first, second, plain)
    rows = dn.component_request_rows(record, inputs)
    assert [(r["kind"], r["name"], r["spec"]) for r in rows] == [
        ("op", NEW_OP, "spec one"), ("op", NEW_OP, "spec two"), ("component", NEW_CLASS,
                                                                 "a one-dimensional Kalman "
                                                                 "filter of the value")]
    assert rows[0] == {"kind": "op", "name": NEW_OP, "spec": "spec one",
                       "example": f"{{name: {NEW_OP}}}", "stage": "decide_next", "run_id": RUN,
                       "proposal_ref": f"runs/{RUN}/artifacts/proposals/{CAT}.yaml#{CAT}-{RUN}-1",
                       "reason": f"requires_op:{NEW_OP}"}
    path = tmp_path / "component_requests.yaml"
    path.write_text(yaml.safe_dump({"requests": [{"run_id": "run_001", "kind": "deviation",
                                                  "reason": "deviation: x"}]}), encoding="utf-8")
    for _pass in range(2):                                     # every decide pass appends
        crr.append_component_requests(path, rows, key=dn.component_request_key)
    got = yaml.safe_load(path.read_text(encoding="utf-8"))["requests"]
    assert [(r["kind"], r.get("name"), r.get("spec")) for r in got] == [
        ("deviation", None, None), ("op", NEW_OP, "spec one"),
        ("component", NEW_CLASS, "a one-dimensional Kalman filter of the value")]


def test_no_rows_once_the_piece_exists_or_for_a_patch():
    p = _side(_vehicle(_with_op(_gated()), requires=[_req()]))
    inputs, record = _decide(p, known_ops=dn.known_ops(TB) + [NEW_OP])
    assert dn.component_request_rows(record, inputs) == []
    inputs, record = _decide(_side(config_change=copy.deepcopy(CHANGE)))
    assert dn.component_request_rows(record, inputs) == []


def test_run_campaign_passes_known_ops_lazily_and_exact_config_1b_only_when_on(
        campaign_root, monkeypatch):
    seen = []

    class _Stop(Exception):
        pass

    def _capture(root, queue, **kw):
        seen.append(kw)
        raise _Stop
    monkeypatch.setattr(dn, "load_inputs", _capture)
    entry = {"id": "E", "status": "done", "outcome": "refuted", "run_ids": ["run_1"]}
    for on in (False, True):
        monkeypatch.setattr(rpr, "_exact_config_1b_enabled", lambda cfg=None, on=on: on)
        with pytest.raises(_Stop):
            camp._finish_lineage_with_decision({"queue": [entry]}, entry, "run_1")
    assert all(callable(kw["known_ops"]) for kw in seen)
    assert seen[0]["known_ops"]() == dn.known_ops(camp._TRADING_BOT_ROOT)
    assert "exact_config_1b" not in seen[0] and seen[1]["exact_config_1b"] is True


def test_run_campaign_appends_the_rows_after_the_decision(campaign_root, monkeypatch):
    p = _side(_vehicle(_with_op(_gated()), requires=[_req()]))
    src = _src(p)
    monkeypatch.setattr(dn, "load_inputs", lambda root, queue, **kw: _inputs(src))
    entry = {"id": "E", "status": "done", "outcome": "refuted", "verdict_status": "ungated",
             "run_ids": [RUN]}
    campaign_root["queue_path"].write_text(yaml.safe_dump({"queue": [entry]}), encoding="utf-8")
    (campaign_root["runs_dir"] / RUN / "artifacts").mkdir(parents=True)
    for _pass in range(2):
        camp._finish_lineage_with_decision({"queue": [dict(entry)]}, dict(entry), RUN)
    path = campaign_root["root"] / crr.COMPONENT_REQUESTS_REL
    got = yaml.safe_load(path.read_text(encoding="utf-8"))["requests"]
    assert [(r["kind"], r["name"], r["stage"]) for r in got] == [("op", NEW_OP, "decide_next")]


# ---------------------------------------------------------------------------
# the brief (V2d, Q4)
# ---------------------------------------------------------------------------

def _brief_dir(tmp_path, front) -> Path:
    run_dir = tmp_path / "run_x"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "research_brief.yaml").write_text(
        yaml.safe_dump(front, sort_keys=False), encoding="utf-8")
    return run_dir


def test_the_brief_carries_the_exact_config_and_manifest_and_round_trips(tmp_path):
    gate = _with_op(_gated())
    p = _side(_vehicle(gate, requires=[_req()]))
    front = _front(p)
    derived = cv.derived_manifest(MANIFEST, CONFIG, gate, "regime_gate")
    cand, source = front["candidate"], front["candidate"]["source"]
    assert cand["start_config"] == gate and cand["start_manifest"] == derived
    assert "config" not in cand and "manifest" not in cand
    assert "expected_config_sha256" not in source and "resolved_patch" not in source
    assert source["start_config_sha256"] == dn.config_sha256(gate)
    assert source["proposal"]["vehicle"] == {"kind": "config",
                                             "config_sha256": dn.config_sha256(gate),
                                             "requires": [_req()],
                                             "config_ref": "candidate.start_config"}
    assert source["proposal"]["combines_as"] == "regime_gate"
    assert [c.split("\n", 1)[0] for c in front["constraints"]] == [
        f"{dn.BRIEF_EXACT_CONFIG_PREFIX}: the config vehicle of {CAT}-{RUN}-1 (a side finding "
        f"of {RUN}), unchanged (D-162).",
        f"{dn.BRIEF_EXACT_MANIFEST_PREFIX}: {RUN}'s block manifest, as "
        f"config_vehicle.derived_manifest gives it for this config (D-161)."]
    assert "relabelled to the vehicle's trading regime" in front["research_goal"]
    assert "Its ungated twin" in front["research_goal"]
    run_dir = _brief_dir(tmp_path, front)
    assert rpr._brief_exact_config(run_dir) == gate                 # the orchestrator's parsers
    assert rpr._brief_exact_manifest(run_dir) == derived
    assert rpr._is_pass_through_candidate(run_dir / "artifacts") is False
    assert rpr._brief_config_vehicle(run_dir) == (source["proposal"]["vehicle"], "regime_gate")


def test_a_forecast_block_vehicle_brief_names_no_twin():
    cfg = copy.deepcopy(CONFIG)
    cfg["strategies"]["regimes"]["unknown"]["components"][0]["params"]["period"] = 21
    front = _front(_side(_vehicle(cfg), "forecast_block"))
    assert "twin" not in front["research_goal"] and "relabelled" not in front["research_goal"]
    assert front["candidate"]["source"]["proposal"]["vehicle"] == {
        "kind": "config", "config_sha256": dn.config_sha256(cfg),
        "config_ref": "candidate.start_config"}


# ---------------------------------------------------------------------------
# step 1b (V3a, V3b)
# ---------------------------------------------------------------------------

def _1b_run(run_id, front) -> Path:
    run_dir = _run(run_id, no_brief=True)
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", front)
    return run_dir


def test_1b_copies_the_config_vehicle_by_code():
    _set_orchestrator(ON)
    gate = _gated()
    run_dir = _1b_run("run_981", _front(_side(_vehicle(gate))))
    assert rpr._exact_config_1b_mode(run_dir) is True
    rpr._exact_config_1b(run_dir, "run_981")
    arts = run_dir / "artifacts"
    assert rpr.load_yaml(arts / "backtest_spec.yaml")["config"] == gate
    assert rpr.load_yaml(arts / bm.MANIFEST_FILENAME) == cv.derived_manifest(
        MANIFEST, CONFIG, gate, "regime_gate")


def test_1b_refuses_a_piece_that_is_still_missing():
    _set_orchestrator(ON)
    p = _side(_vehicle(_with_class(_with_op(_gated())),
                       requires=[_req(), _req("component", NEW_CLASS)]))
    run_dir = _1b_run("run_982", _front(p))
    with pytest.raises(RuntimeError) as exc:
        rpr._exact_config_1b(run_dir, "run_982")
    assert str(exc.value) == (
        f"[D-110] exact-config 1b refused: the brief's config vehicle (D-162) uses op "
        f"'{NEW_OP}', component '{NEW_CLASS}', which does not exist yet; 1b never builds a "
        f"missing piece (its spec is in campaign_record/component_requests.yaml)")
    for name in ("backtest_spec.yaml", "decision.yaml", bm.MANIFEST_FILENAME):
        assert not (run_dir / "artifacts" / name).exists()


def test_1b_still_refuses_a_patch_pass_through_and_reads_no_piece_for_another_brief():
    _set_orchestrator(ON)
    run_dir = _run("run_983")                               # D-110's own exact-config brief
    brief = rpr.load_yaml(run_dir / "artifacts" / "research_brief.yaml")
    assert rpr._config_vehicle_missing_pieces(run_dir, _with_op(_gated())) == []
    brief["candidate"] = {"source": {"expected_config_sha256": "a" * 64}}
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", brief)
    with pytest.raises(RuntimeError, match=r"\[D-110\] exact-config 1b refused: a decide_next "
                                           r"pass-through candidate carries its own config"):
        rpr._exact_config_1b(run_dir, "run_983")


# ---------------------------------------------------------------------------
# step 2: the ungated twin is the design variant, by code
# ---------------------------------------------------------------------------

LOOP_ON = {**ON, "variant_loop": {"enabled": True}}
STEP2 = [{"variant_id": "base", "kind": "base", "patch": []},
         {"variant_id": "model_design", "kind": "design",
          "patch": [{"path": "/strategies/warmup", "value": 60}]},
         {"variant_id": "other_design", "kind": "design",
          "patch": [{"path": "/strategies/warmup", "value": 70}]},
         {"variant_id": "eth", "kind": "asset", "symbol": "ETHUSDT", "patch": []}]


def test_the_twin_mode_needs_the_loop_the_exact_route_and_a_regime_gate_vehicle():
    gate_front = _front(_side(_vehicle(_gated())))
    fb_front = _front(_side(_vehicle(CONFIG), "forecast_block"))
    _set_orchestrator(LOOP_ON)
    assert rpr._ungated_twin_variant_mode(_1b_run("run_984", gate_front)) is True
    assert rpr._ungated_twin_variant_mode(_1b_run("run_985", fb_front)) is False
    assert rpr._ungated_twin_variant_mode(_run("run_986")) is False      # no config vehicle
    _set_orchestrator(ON)                                                # loop off
    assert rpr._ungated_twin_variant_mode(_1b_run("run_987", gate_front)) is False
    _set_orchestrator({**LOOP_ON, "exact_config_1b": {"enabled": False}})
    assert rpr._ungated_twin_variant_mode(_1b_run("run_988", gate_front)) is False


def test_the_twin_replaces_every_design_variant_and_its_manifest_resolves():
    _set_orchestrator(LOOP_ON)
    gate = _gated()
    run_dir = _1b_run("run_989", _front(_side(_vehicle(gate))))
    rpr._exact_config_1b(run_dir, "run_989")
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "variant_patches.yaml", {"base_config_ref": "x", "variants": STEP2})
    rpr._set_ungated_twin_variant(run_dir, "run_989")
    rpr._set_ungated_twin_variant(run_dir, "run_989")                    # idempotent
    doc = rpr.load_yaml(arts / "variant_patches.yaml")
    assert doc["base_config_ref"] == "x"
    assert [(v["variant_id"], v["kind"]) for v in doc["variants"]] == [
        ("base", "base"), (rpr.UNGATED_TWIN_VARIANT_ID, "design"), ("eth", "asset")]
    twin_entry = doc["variants"][1]
    assert "symbol" not in twin_entry and twin_entry["patch"]
    twin = jp.apply_json_pointer_patch(gate, twin_entry["patch"])
    assert twin == cv.ungated_twin(gate)                     # the config IS the twin
    assert twin["regime_detector"]["default_regime"] == "trending"
    assert "vetoes" not in twin["regime_detector"] and twin["regime_detector"]["rules"] == []
    derived = rpr.load_yaml(arts / bm.MANIFEST_FILENAME)
    assert derived["block"]["config_paths"] == ["/strategies/regimes/trending/components/0"]
    assert jp.manifest_missing_paths(twin, derived) == []          # 5a's per-variant check
    assert fr.class_mismatch(gate, twin) == []
    assert fr.strategies_violations(twin, fr.on_off_classes()) == []


def test_the_twin_is_written_where_step_2_is_routed_before_any_shape_check():
    src = Path(rpr.__file__).read_text(encoding="utf-8")
    branch = src[src.index('elif current_stage == "innovation_expansion":'):]
    branch = branch[:branch.index("elif current_stage == \"backtest_specification\"")]
    assert branch.index("_set_ungated_twin_variant(RUN_DIR, run_id)") < branch.index(
        "_route_variant_shape_check(RUN_DIR, run_id)")
    assert "if _ungated_twin_variant_mode(RUN_DIR):" in branch


# ---------------------------------------------------------------------------
# reader_findings, fold_confirm, explore_confirm
# ---------------------------------------------------------------------------

def _item(vehicle=None, **extra) -> dict:
    p = _side(vehicle, **extra)
    if isinstance(p.get("vehicle"), list):
        p["config_change"] = p["vehicle"]
    return p


def test_the_merge_key_is_the_canonical_config():
    a, b = _item(_vehicle(_gated())), _item(_vehicle(json.loads(json.dumps(_gated()))))
    other = _item(_vehicle(_with_op(_gated())))
    ka, kb, ko = rfi._merge_key(a), rfi._merge_key(b), rfi._merge_key(other)
    assert ka == kb and ka != ko
    assert ka[2] == "config:" + json.dumps(_gated(), sort_keys=True, default=str)
    patch = _item(copy.deepcopy(CHANGE), combines_as="forecast_block")
    assert rfi._merge_key(patch)[2] == json.dumps(sorted(
        json.dumps(c, sort_keys=True, default=str) for c in CHANGE), default=str)
    assert rfi._merge_key(_side())[2] is None


def _cv_envelope(config) -> dict:
    return {"vehicle": _vehicle(config), "combines_as": "forecast_block", "fold_observed": "A"}


def test_fold_confirm_compares_a_config_vehicle_whole(tmp_path):
    root, child = e077._build(tmp_path, envelope=_cv_envelope(e077._config(2)), config_period=2)
    row = e077._confirm(root, child)
    assert row["status"] == fc.CONFIRMED, row["reason"]
    assert "vehicle_missing" not in row
    assert row["vehicle"] == {"kind": "config", "config_sha256": dn.config_sha256(e077._config(2)),
                              "config_ref": f"runs/{e077.CHILD}/artifacts/research_brief.yaml"
                                            f"#candidate.start_config"}


def test_fold_confirm_names_what_the_measured_config_lacks(tmp_path):
    root, child = e077._build(tmp_path, envelope=_cv_envelope(e077._config(2)), config_period=99)
    row = e077._confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "tests" not in row
    assert row["reason"] == (
        "vehicle_not_in_measured_config: variant 'base' does not carry the claim's vehicle: "
        "/strategies/regimes/trend/components/0/params/period: the vehicle has 2, the measured "
        "config has 99")
    assert len(row["vehicle_missing"]) == 1
    wider = {**e077._config(2), **{k: 1 for k in ("a", "b", "c", "d")}}
    root, child = e077._build(tmp_path / "wide", envelope=_cv_envelope(wider), config_period=2)
    row = e077._confirm(root, child)
    assert len(row["vehicle_missing"]) == 4 and row["reason"].endswith(
        "/c: the vehicle has 1, the measured config has None; (+1 more)"), row["reason"]
    assert fc.config_vehicle_missing(e077._config(2), _vehicle(e077._config(2))) == []
    many = {f"k{i}": i for i in range(5)}
    lacks = fc.config_vehicle_missing({}, _vehicle(many))
    assert len(lacks) == 5 and lacks[0] == "/k0: the vehicle has 0, the measured config has None"


def test_explore_confirm_routes_a_config_vehicle_like_a_config_change():
    reads_forecast = copy.deepcopy(_pure_claim())
    reads_forecast["tests"][0]["selector"] = {"kind": "event", "field": "forecast",
                                              "op": ">", "value": 0.0}
    cfg_vehicle = _vehicle(CONFIG)
    assert ec.finding_route({"claim": reads_forecast})[0] == ec.IN_RUN
    assert ec.finding_route({"claim": reads_forecast, "vehicle": cfg_vehicle})[0] == ec.PENDING
    assert ec.finding_route({"claim": reads_forecast, "config_change": CHANGE}) == \
        ec.finding_route({"claim": reads_forecast, "vehicle": cfg_vehicle})
    assert ec.finding_route({"claim": _pure_claim(), "vehicle": cfg_vehicle})[0] == ec.IN_RUN
    assert ec.finding_route({"claim": _pure_claim(), "vehicle": cfg_vehicle},
                            folds=True)[0] == ec.PENDING


# ---------------------------------------------------------------------------
# the texts (V3c, V3d)
# ---------------------------------------------------------------------------

PREFILLED_SENTENCE = (
    "Exception: when the brief's config changes only the regime detector (a gate on the source "
    "run's unchanged strategies), the claim is about that gate: in signal_concept describe the "
    "gate's condition and the source run's block it gates; keep the strategies as the source "
    "run's; the ungated twin (the same config without the gate) is the design variant, and code "
    "derives it, so do not write it.")


def _flat(path) -> str:
    return " ".join((SR_ROOT / path).read_text(encoding="utf-8").split())


def test_prefilled_claim_carries_the_approved_sentence_after_the_block_bullet():
    text = _flat("workflow_artifacts/skills/hypothesis-design/PREFILLED_CLAIM.md")
    assert PREFILLED_SENTENCE in text
    assert text.index("**The block is the source run's.**") < text.index(PREFILLED_SENTENCE)


def test_the_analyst_skill_advertises_the_config_form_and_requires():
    text = _flat("workflow_artifacts/skills/analyst/SKILL.md")
    for phrase in ("`vehicle: {kind: config, config: <the complete strategy config>}`",
                   "`combines_as: regime_gate`", "Code derives the ungated twin",
                   "`requires: [{kind: op, name: kalman_smooth,",
                   "(a component: `kind: component`, `name` its full class path "
                   "`strategies.strategy_components.<ClassName>`",
                   "The checker cannot know whether a new op you list is a history op",
                   "an existing history op placed after it is refused (V5)",
                   "except a piece the config form lists in `requires`"):
        assert phrase in text, phrase
