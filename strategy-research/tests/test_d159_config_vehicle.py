"""D-159 (vehicle-format V1a-V1c, operator plan 2026-10-20): the config form of a vehicle.

  vehicle: {kind: config, config: <complete strategy config>[, requires: [{kind, name, spec,
  example}]]}

1. Lands unused: reader_proposals.CONFIG_VEHICLE_ROUTED is False, so a mapping vehicle is
   refused exactly as before (the patch-list message), from a model and in a written file,
   in the readers' check and in the analyst stage. Patch vehicles and D-151 are unchanged
   with the form on or off.
2. The shape (check_config_vehicle), with config_vehicle=True.
3. flatten_reading: a config vehicle is never handed on as a patch `config_change`.
4. The content (tools/config_vehicle.py): requires (absent today, used, every absent piece
   listed), validate_config with only V3/V12 lines of listed names exempt, D-051/D-149.
5. The wiring: run_phase1_research._reading_content_errors and the analyst's retry loop.

No LLM, no backtest, no market data.
"""
from __future__ import annotations

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

import config_vehicle as cv  # noqa: E402
import reader_proposals as rp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

from test_d051_d053_forecast_rules import CONFIG, MANIFEST, SC  # noqa: E402
from test_e077_pr2_confirm import CAT, CHANGE, _claim, _reading, _save  # noqa: E402
from test_e075_pr5_analyst import _flags, _good_claim, _install, run, RUN_ID  # noqa: E402,F401
import analyst_session as asm  # noqa: E402

ENV = {"combines_as": "forecast_block", "fold_observed": "A"}
NEW_OP = "kalman_smooth"                                   # not in TRANSFORM_OPS_REGISTRY
NEW_CLASS = SC + "KalmanTrendComponent"                    # not in strategy_components.py
STANDARDISE = {"op": "standardise", "params": {"window": 20, "min_periods": 5}}
OLD_MESSAGE = ("vehicle: must be a non-empty list of changes (omit it when the finding needs "
               "no config change)")


def _vehicle(config=None, **extra) -> dict:
    return {"kind": "config", "config": copy.deepcopy(CONFIG if config is None else config),
            **extra}


def _req(kind="op", name=NEW_OP, spec="a one-dimensional Kalman filter of the value",
         example="{op: kalman_smooth, params: {q: 0.01}}") -> dict:
    return {"kind": kind, "name": name, "spec": spec, "example": example}


def _check_model(vehicle, **kw):
    rp.check_reading(_reading(_claim(), vehicle=vehicle, **ENV), CAT, "reading",
                     from_model=True, envelope=True, **kw)


def _with_op(op=NEW_OP) -> dict:
    cfg = copy.deepcopy(CONFIG)
    comp = cfg["strategies"]["regimes"]["unknown"]["components"][0]
    comp["transforms"] = [STANDARDISE, {"op": op, "params": {"q": 0.01}},
                          {"op": "clip", "params": {"min": -20, "max": 20}}]
    return cfg


def _with_class(cls=NEW_CLASS) -> dict:
    cfg = copy.deepcopy(CONFIG)
    cfg["strategies"]["regimes"]["unknown"]["components"].append(
        {"id": "kalman", "class": cls, "params": {"period": 20}, "weight": 1.0,
         "transforms": [STANDARDISE]})
    return cfg


def _errors(vehicle) -> list:
    return cv.config_vehicle_errors(vehicle, "v")


# ---------------------------------------------------------------------------
# 1. lands unused: refused exactly as before
# ---------------------------------------------------------------------------

def test_the_form_is_off_until_v2_routes_it():
    assert rp.CONFIG_VEHICLE_ROUTED is False


@pytest.mark.parametrize("kw", [{}, {"config_vehicle": None}, {"config_vehicle": False}])
def test_off_a_config_vehicle_from_a_model_gets_the_old_patch_list_refusal(kw):
    with pytest.raises(rp.ProposalError) as exc:
        _check_model(_vehicle(), **kw)
    assert str(exc.value) == f"reading.side_findings[0].{OLD_MESSAGE}"


def test_off_a_written_file_with_a_config_vehicle_fails_to_load_loudly(tmp_path):
    _save(tmp_path / "proposals" / f"{CAT}.yaml", _reading(_claim(), vehicle=_vehicle(), **ENV))
    for load in (rp.load_proposals, rp.load_readings):
        with pytest.raises(rp.ProposalError) as exc:
            load(tmp_path / "proposals", [CAT])
        assert str(exc.value).endswith(f"side_findings[0].{OLD_MESSAGE}"), str(exc.value)


@pytest.mark.parametrize("on", [False, True])
def test_patch_vehicles_and_d151_are_unchanged_with_the_form_on_or_off(on, tmp_path):
    _check_model(copy.deepcopy(CHANGE), config_vehicle=on)                  # accepted
    with pytest.raises(rp.ProposalError, match=r"an empty vehicle is refused for every claim"):
        _check_model([], config_vehicle=on)
    with pytest.raises(rp.ProposalError, match=r"`vehicle` is required"):
        rp.check_reading(_reading(_claim(), **ENV), CAT, "reading", from_model=True,
                         envelope=True, config_vehicle=on)
    with pytest.raises(rp.ProposalError, match=r"vehicle\[0\] must be exactly"):
        _check_model([{"component_id": "x"}], config_vehicle=on)
    # a written `vehicle: []` still loads flagged (D-151); the flattened items are unchanged
    _save(tmp_path / "proposals" / f"{CAT}.yaml", _reading(_claim(), vehicle=[], **ENV))
    (item,) = rp.load_proposals(tmp_path / "proposals", [CAT])[CAT]
    assert item["legacy_no_vehicle"] is True and item["vehicle"] == [] and item["config_change"] == []
    flat = rp.flatten_reading(_reading(_claim(), vehicle=copy.deepcopy(CHANGE), **ENV))[0]
    assert flat["config_change"] == CHANGE and flat["vehicle"] == CHANGE


def test_vehicle_and_config_change_together_are_still_refused():
    side = _reading(_claim(), vehicle=_vehicle(), config_change=copy.deepcopy(CHANGE), **ENV)
    with pytest.raises(rp.ProposalError, match="write `vehicle` OR `config_change`"):
        rp.check_reading(side, CAT, "reading", from_model=True, envelope=True,
                         config_vehicle=True)


# ---------------------------------------------------------------------------
# 2. the shape (on)
# ---------------------------------------------------------------------------

def test_on_the_config_form_is_accepted_with_and_without_requires():
    _check_model(_vehicle(), config_vehicle=True)
    _check_model(_vehicle(_with_op(), requires=[_req()]), config_vehicle=True)
    _check_model(_vehicle(_with_class(), requires=[_req("component", NEW_CLASS,
                                                       example={"class": NEW_CLASS})]),
                 config_vehicle=True)


def test_on_the_flag_constant_turns_it_on_for_every_caller(monkeypatch, tmp_path):
    monkeypatch.setattr(rp, "CONFIG_VEHICLE_ROUTED", True)
    _check_model(_vehicle())
    _save(tmp_path / "proposals" / f"{CAT}.yaml", _reading(_claim(), vehicle=_vehicle(), **ENV))
    (item,) = rp.load_proposals(tmp_path / "proposals", [CAT])[CAT]
    assert item["vehicle"] == _vehicle() and "config_change" not in item
    assert "legacy_no_vehicle" not in item
    # forced on, a written file is shape-checked as the config form (not the patch list)
    _save(tmp_path / "proposals" / f"{CAT}.yaml",
          _reading(_claim(), vehicle=dict(_vehicle(), kind="patch"), **ENV))
    with pytest.raises(rp.ProposalError, match=r"vehicle.kind='patch' must be 'config'"):
        rp.load_proposals(tmp_path / "proposals", [CAT])


@pytest.mark.parametrize("vehicle,needle", [
    ({"kind": "config"}, "the config form is exactly"),
    ({"config": CONFIG}, "the config form is exactly"),
    (dict(_vehicle(), extra=1), "the config form is exactly"),
    (dict(_vehicle(), kind="patch"), r"vehicle.kind='patch' must be 'config'"),
    (dict(_vehicle(), config={}), "vehicle.config must be the complete strategy config"),
    (dict(_vehicle(), config=[1]), "vehicle.config must be the complete strategy config"),
    (dict(_vehicle(), requires=[]), r"vehicle.requires must be a non-empty list \(omit it"),
    (dict(_vehicle(), requires={"kind": "op"}), "vehicle.requires must be a non-empty list"),
    (dict(_vehicle(), requires=[{"kind": "op", "name": NEW_OP}]),
     r"requires\[0\] must be exactly \{kind, name, spec, example\}"),
    (dict(_vehicle(), requires=[_req(kind="feed")]), r"requires\[0\].kind='feed' must be one of"),
    (dict(_vehicle(), requires=[_req(name=" kalman_smooth")]), r"requires\[0\].name must be"),
    (dict(_vehicle(), requires=[_req(name="")]), r"requires\[0\].name must be"),
    (dict(_vehicle(), requires=[_req(spec=" ")]), r"requires\[0\].spec must be"),
    (dict(_vehicle(), requires=[_req(example="")]), r"requires\[0\].example must be"),
    (dict(_vehicle(), requires=[_req(example=None)]), r"requires\[0\].example must be"),
    (dict(_vehicle(), requires=[_req(), _req()]), r"requires\[1\]: op 'kalman_smooth' is listed twice"),
])
@pytest.mark.parametrize("how", ["kwarg", "constant"])
def test_on_each_shape_refusal(vehicle, needle, how, monkeypatch):
    if how == "constant":                       # the constant forced on, no kwarg
        monkeypatch.setattr(rp, "CONFIG_VEHICLE_ROUTED", True)
        kw = {}
    else:
        kw = {"config_vehicle": True}
    with pytest.raises(rp.ProposalError, match=needle):
        _check_model(vehicle, **kw)


# ---------------------------------------------------------------------------
# 3. flatten_reading
# ---------------------------------------------------------------------------

def test_a_config_vehicle_is_never_flattened_into_a_patch_config_change():
    (item,) = rp.flatten_reading(_reading(_claim(), vehicle=_vehicle(), **ENV))
    assert "config_change" not in item
    assert item["vehicle"] == _vehicle() and item["combines_as"] == "forecast_block"


# ---------------------------------------------------------------------------
# 4. the content
# ---------------------------------------------------------------------------

def test_a_valid_complete_config_passes():
    assert _errors(_vehicle()) == []


def test_validate_config_violations_are_refusals():
    cfg = copy.deepcopy(CONFIG)
    cfg["regime_detector"]["vetoes"] = [{"id": "nope", "result": "chop"}]
    errs = _errors(_vehicle(cfg))
    assert errs == ["v.config: VIOLATION V2 regime_detector.vetoes[0].id: 'nope' not declared "
                    "in regime_detector.components"]


def test_a_config_validate_config_cannot_read_is_a_refusal_not_a_crash():
    cfg = copy.deepcopy(CONFIG)
    del cfg["regime_detector"]["components"][0]["id"]
    (err,) = _errors(_vehicle(cfg))
    assert err.startswith("v.config: validate_config cannot check it (KeyError")


def test_d149_and_d051_apply():
    cfg = copy.deepcopy(CONFIG)
    cfg["strategies"]["regimes"]["unknown"]["components"][0]["transforms"] = [
        {"op": "scale", "params": {"factor": 10.0}}]
    (err,) = _errors(_vehicle(cfg))
    assert err.startswith("v.config: D-149: strategies.regimes.unknown.components[0]")
    cfg = _with_op("threshold_filter")
    assert any(e.startswith("v.config: D-051: dead-zone op 'threshold_filter'")
               for e in _errors(_vehicle(cfg)))


def test_a_missing_op_must_be_listed_and_once_listed_only_its_v3_line_is_exempt():
    errs = _errors(_vehicle(_with_op()))
    assert errs == [
        "v.config: op 'kalman_smooth' does not exist today (not in TRANSFORM_OPS_REGISTRY) and "
        "is not listed in requires: use an existing op, or list it as {kind: op, name: "
        "kalman_smooth, spec, example}",
        "v.config: VIOLATION V3 strategies.regimes.unknown.components[0].transforms[1].op: "
        "'kalman_smooth' not in TRANSFORM_OPS_REGISTRY"]
    assert _errors(_vehicle(_with_op(), requires=[_req()])) == []


def test_a_missing_component_must_be_listed_and_once_listed_only_its_v12_line_is_exempt():
    errs = _errors(_vehicle(_with_class()))
    assert len(errs) == 2
    assert errs[0] == (f"v.config: component class {NEW_CLASS!r} does not exist today and is "
                       f"not listed in requires: use an existing component, or list it as "
                       f"{{kind: component, name: {NEW_CLASS}, spec, example}}")
    assert errs[1].startswith(f"v.config: VIOLATION V12 strategies.regimes.unknown.components[1]"
                              f".class: cannot load {NEW_CLASS!r}")
    assert _errors(_vehicle(_with_class(), requires=[_req("component", NEW_CLASS)])) == []


def test_the_exemption_covers_v3_and_v12_only_never_another_rule():
    # the listed op is placed where V5 refuses it (a history op after it): V5 stays
    cfg = _with_op()
    cfg["strategies"]["regimes"]["unknown"]["components"][0]["transforms"] = [
        {"op": NEW_OP}, STANDARDISE]
    errs = _errors(_vehicle(cfg, requires=[_req()]))
    assert any(" V5 " in e for e in errs) and not any(" V3 " in e for e in errs)
    # a listed class is still under D-149
    cfg = _with_class()
    cfg["strategies"]["regimes"]["unknown"]["components"][1]["transforms"] = []
    errs = _errors(_vehicle(cfg, requires=[_req("component", NEW_CLASS)]))
    assert errs and all("D-149" in e for e in errs)


def test_an_unlisted_v3_line_is_not_exempted_by_another_listed_op():
    cfg = _with_op()
    cfg["strategies"]["regimes"]["unknown"]["components"][0]["transforms"].insert(
        1, {"op": "other_new_op"})
    errs = _errors(_vehicle(cfg, requires=[_req()]))
    assert any("'other_new_op' not in TRANSFORM_OPS_REGISTRY" in e for e in errs)
    assert not any("'kalman_smooth' not in TRANSFORM_OPS_REGISTRY" in e for e in errs)


@pytest.mark.parametrize("req,needle", [
    (_req(name="standardise"), "op 'standardise' exists today (TRANSFORM_OPS_REGISTRY); remove it"),
    (_req(name="unused_op"), "op 'unused_op' is not used by the config"),
    (_req("component", SC + "RSIPullbackComponent"), "exists today; remove it from requires"),
    (_req("component", "KalmanTrendComponent"), "must be a dotted class path in "
                                                "strategies.strategy_components"),
    (_req("component", "strategies.other_module.KalmanTrendComponent"), "must be a dotted class path"),
    (_req("component", SC + "UnusedNewComponent"), "is not used by the config"),
])
def test_each_requires_refusal(req, needle):
    errs = _errors(_vehicle(requires=[req]))
    assert len(errs) == 1 and errs[0].startswith("v.requires[0]: ") and needle in errs[0], errs


def _spy_validate(monkeypatch) -> list:
    calls = []
    vc = cv._validate_config_module(cv.TBOT_ROOT)
    real = vc.validate
    monkeypatch.setattr(vc, "validate", lambda config: calls.append(1) or real(config))
    return calls


def test_a_class_in_another_module_is_never_exemptable(monkeypatch):
    calls = _spy_validate(monkeypatch)
    bad = "strategies.no_such_module.KalmanTrendComponent"
    errs = _errors(_vehicle(_with_class(bad), requires=[_req("component", bad)]))
    assert errs == [f"v.requires[0]: component {bad!r} must be a dotted class path in "
                    f"strategies.strategy_components (as the config's `class` writes it, "
                    f"strategies.strategy_components.<ClassName>)"]
    assert calls == []                      # validate_config (V12 imports) never ran


@pytest.mark.parametrize("bad", ["json.JSONDecoder",
                                 "strategies.strategy_engine.ConfigDrivenStrategyEngine",
                                 "KalmanTrendComponent"])
def test_an_unlisted_class_outside_the_component_module_is_refused_and_never_imported(
        bad, monkeypatch):
    calls = _spy_validate(monkeypatch)
    errs = _errors(_vehicle(_with_class(bad)))
    assert errs == [f"v.config: component class {bad!r} must be a dotted class path in "
                    f"strategies.strategy_components (as the config's `class` writes it, "
                    f"strategies.strategy_components.<ClassName>)"]
    assert calls == []                      # no model-chosen module imported at reading time
    assert _errors(_vehicle()) == [] and calls == [1]       # the spy does see a normal call


MALFORMED_OP = [{"op": ["x"]}]                             # TypeError: unhashable list


def _malformed() -> dict:
    cfg = copy.deepcopy(CONFIG)
    cfg["strategies"]["regimes"]["unknown"]["components"][0]["transforms"] = copy.deepcopy(
        MALFORMED_OP)
    return cfg


def test_a_config_forecast_rules_cannot_read_is_a_refusal_not_a_crash(monkeypatch):
    import forecast_rules as fr
    with pytest.raises(TypeError):                         # the probe does crash forecast_rules
        fr.strategies_violations(_malformed(), fr.on_off_classes())
    vc = cv._validate_config_module(cv.TBOT_ROOT)
    monkeypatch.setattr(vc, "validate", lambda config: [])  # so forecast_rules is reached
    (err,) = _errors(_vehicle(_malformed()))
    assert err.startswith("v.config: forecast_rules cannot check it (TypeError"), err


def test_a_malformed_op_is_a_refusal_with_the_real_checkers():
    (err,) = _errors(_vehicle(_malformed()))
    assert err.startswith("v.config: ") and " cannot check it (TypeError" in err, err


def test_pieces_inside_a_block_source_detector_count_as_used():
    cfg = {"x": [{"blocks": [{"source": {"regime_detector": {"components": [
        {"class": NEW_CLASS, "transforms": [{"op": NEW_OP}]}]}}}]}]}
    assert cv.used_pieces(cfg) == ({NEW_OP}, {NEW_CLASS})


def test_used_pieces_ends_on_a_self_referential_structure():
    cfg = {"class": NEW_CLASS, "transforms": [{"op": NEW_OP}]}
    loop = [cfg]
    loop.append(loop)
    cfg["self"], cfg["loop"] = cfg, loop
    assert cv.used_pieces(cfg) == ({NEW_OP}, {NEW_CLASS})
    alias = yaml.safe_load("a: &x\n  class: " + NEW_CLASS + "\n  me: *x\n")
    assert alias["a"]["me"] is alias["a"]                  # a real YAML self-alias
    assert cv.used_pieces(alias) == (set(), {NEW_CLASS})


# ---------------------------------------------------------------------------
# 5. the wiring
# ---------------------------------------------------------------------------

def _doc(vehicle) -> dict:
    return _reading(_claim(), vehicle=vehicle, **ENV)


def _source_run(run_dir) -> None:
    """D-161: CONFIG and its MANIFEST as the source run's base config and block manifest
    (a config vehicle is also checked against its source run, which needs a manifest)."""
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text(
        json.dumps(CONFIG), encoding="utf-8")
    (run_dir / "artifacts" / "block_manifest.yaml").write_text(yaml.safe_dump(MANIFEST),
                                                               encoding="utf-8")


def test_the_content_check_runs_the_config_vehicle_check_and_never_resolve_patch(monkeypatch,
                                                                                  tmp_path):
    calls = []
    monkeypatch.setattr(rpr._decide_next_tools(), "resolve_patch",
                        lambda *a, **k: calls.append(a) or ([], {}, None))
    monkeypatch.setattr(rpr, "_claim_check_kw", lambda: {"folds": True})
    _source_run(tmp_path)
    cfg = copy.deepcopy(CONFIG)
    cfg["strategies"]["regimes"]["unknown"]["components"][0]["transforms"] = []
    errs = rpr._reading_content_errors(_doc(_vehicle(cfg)), CAT, tmp_path)
    assert [e for e in errs if e.startswith("side_findings[0].vehicle.config: D-149: ")], errs
    assert rpr._reading_content_errors(_doc(_vehicle()), CAT, tmp_path) == []
    assert calls == []                      # nothing resolved as a patch


def _run_analyst(run_dir):
    dest = rpr.run_analyst_worker("trade_efficiency", RUN_ID, run_dir)
    record = yaml.safe_load((run_dir / asm.record_rel("trade_efficiency")).read_text(
        encoding="utf-8"))
    return dest, record


def test_the_analyst_off_refuses_a_config_vehicle_with_the_old_message(run, monkeypatch):
    async def script(call):
        return await _good_claim(call, extra={"vehicle": _vehicle()})
    _install(monkeypatch, script)
    _dest, record = _run_analyst(run)
    errs = record["attempts"][0]["errors"]
    assert f"analyst reading.side_findings[0].{OLD_MESSAGE}" in errs, errs
    assert record["attempts"][-1]["status"] == "refused"


def test_the_analyst_on_hears_the_content_refusal_and_retries(run, monkeypatch):
    monkeypatch.setattr(rp, "CONFIG_VEHICLE_ROUTED", True)
    _source_run(run)
    cfg = _with_op()                                         # the new op, not listed
    answers = iter([_vehicle(cfg), _vehicle(cfg, requires=[_req()])])

    async def script(call):
        return await _good_claim(call, extra={"vehicle": next(answers)})
    _install(monkeypatch, script)
    dest, record = _run_analyst(run)
    first, second = record["attempts"]
    assert first["status"] == "refused" and any(
        e.startswith("side_findings[0].vehicle.config: op 'kalman_smooth' does not exist today")
        for e in first["errors"]), first["errors"]
    assert second["status"] == "accepted", second["errors"]
    written = yaml.safe_load(dest.read_text(encoding="utf-8"))
    assert written["side_findings"][0]["vehicle"]["requires"] == [_req()]


def test_the_analyst_on_refuses_a_malformed_op_and_retries_instead_of_crashing(run,
                                                                              monkeypatch):
    monkeypatch.setattr(rp, "CONFIG_VEHICLE_ROUTED", True)
    _source_run(run)
    answers = iter([_vehicle(_malformed()), _vehicle()])

    async def script(call):
        return await _good_claim(call, extra={"vehicle": next(answers)})
    _install(monkeypatch, script)
    _dest, record = _run_analyst(run)
    first, second = record["attempts"]
    assert first["status"] == "refused" and any(
        e.startswith("side_findings[0].vehicle.config: ") and " cannot check it (TypeError" in e
        for e in first["errors"]), first["errors"]
    assert second["status"] == "accepted", second["errors"]
