"""
E-077 PR-2 (CUL-421, D-087) -- the claim record and confirmation on the child run's
fold, behind orchestrator.folds.enabled (off by default; no new flag).

Proven here, all with synthetic inputs (no LLM, no backtest, no market data, no
cache, no holdout bar; every date is in 2018-2021):
  1. The claim record: kind `execution_behaviour` is accepted by check_claim(folds=True)
     only (flag off: CLAIM_TESTS.md, the card schema and the refusal text are as before);
     today's readers' side findings are not accepted under the flag (no retry, no vehicle
     shape echoed); the proposal ENVELOPE (`vehicle`,
     `combines_as`, `fold_observed`) is validated where reader proposals are: a model's
     answer under the flag MUST carry a vehicle, a bad `combines_as` / `fold_observed`
     / a vehicle that does not resolve / both vehicle and config_change are refused; the
     vehicle reaches decide-next as the finding's config change.
  2. THE NOISE RULE on handcrafted measurements (the exact boundary): 6 of 6 and 5 of 6
     windows confirm, 4 of 6 does not, too few of the fold's windows with a value is not
     measurable (R5: an empty window counts against; a floor not met is not measurable),
     no events is not measurable, a negative pooled sign at ANY horizon is not confirmed,
     every test of a claim must pass.
  3. confirm_on_fold end to end on a fixture child run with planted per-window effects
     (bars written to disk, read by the real measurement): a planted effect confirms, a
     null does not, 5 of 6 confirms, 4 of 6 does not, a coin with 3 windows of bars is
     not measurable, a selector that matches nothing is not measurable, a changed spec
     is not comparable, `tests: none` and an unreadable source are not measurable, and a
     run not built from a side finding gives no row.
  4. The ledger: one row per measurement, no duplicate on resume, the look counted
     once, the row survives an E-072 rewrite of the file, refuted and not-measurable
     rows are kept; the campaign summary has one line per status, fold-labelled.
  5. Under the folds flag explore_confirm's in-run route and its weak follow-up
     resolution are unreachable; flag off is exactly as before.

No cost appears in any row.
"""
from __future__ import annotations

import copy
import csv
import json
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import explore_confirm as ec  # noqa: E402
import fold_confirm as fc  # noqa: E402
import claim_card as cc  # noqa: E402
import claim_measure as cmeas  # noqa: E402
import reader_proposals as rp  # noqa: E402
import research_folds as rf  # noqa: E402
import protocol_resolution as pres  # noqa: E402

from _reader_test_helpers import RUN_ID, _set_orchestrator  # noqa: E402

REAL_POLICY = SR_ROOT / "config" / "campaign_data_policy.yaml"
REAL_FOLDS = SR_ROOT / "config" / "folds.yaml"
DOC = rf.load_folds(REAL_FOLDS, policy_path=REAL_POLICY)
FOLD = "B"
BLOCKS = DOC["folds"][FOLD]
LABELS = [b["label"] for b in BLOCKS]
ERAS = pres.load_policy_eras(REAL_POLICY)
HOLDOUT = rf.policy_ranges(REAL_POLICY)["holdout"][0]
FOLDS_ON = {"folds": {"enabled": True}}

SRC, CHILD, CAT = "run_src", "run_child", "trade_efficiency"
PID = f"{CAT}-{SRC}-1"
CHANGE = [{"component_id": "shock_reversal", "field": "params.period", "before": 1, "after": 2}]


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------

def _claim(kind="execution_behaviour", value=0.0, horizons=(1,), floor=10, name="up_day_follow") -> dict:
    return {"statement": "After an up day the strategy's next bar goes the same way.",
            "kind": kind,
            "tests": [{"name": name,
                       "selector": {"kind": "event", "field": "past_return", "bars": 1,
                                    "op": ">", "value": value},
                       "outcome": {"kind": "fwd_return", "horizons": list(horizons)},
                       "baseline": {"kind": "complement"}, "statistic": "mean_diff",
                       "direction": "greater", "floor": {"min_events": floor}}],
            "pass_if": "effect above zero", "fail_if": "effect at or below zero",
            "rationale": "seen on the run that inspired it"}


def _scores() -> dict:
    return {"confidence_real": 2, "distance_to_profitable": 2, "mechanism_plausibility": 2}


def _reading(claim, **envelope) -> dict:
    rid = f"{CAT}-{SRC}"
    side = {"proposal_id": PID, "claim": claim, "evidence": ["variants.base.slices.overall.y=2"],
            "scores": _scores()}
    side.update(envelope)
    return {"schema_version": 3, "reading_id": rid, "model_id": "m",
            "rubric_version": f"{CAT}-reading-v1", "explanation": "Exits came late.",
            "evidence": ["variants.base.slices.overall.x=1"], "side_findings": [side]}


def _save(path: Path, doc) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _bars(path: Path, block: dict, sign: float, seed: int) -> None:
    """Daily bars over the block: r[t+1] = 0.006 * sign * sign(r[t]) + noise(0.01). A sign of
    +1 plants 'an up day is followed by an up day' (mean_diff > 0, about 6 standard errors);
    -1 plants the reverse; 0 is pure noise."""
    import pandas as pd
    ts = pd.date_range(block["start"], block["end"], freq="1D", tz="UTC")
    n = len(ts)
    rng = np.random.default_rng(seed)
    r = np.zeros(n)
    r[0] = 0.01
    for t in range(n - 1):
        r[t + 1] = 0.006 * sign * np.sign(r[t]) + rng.normal(0.0, 0.01)
    close = 100.0 * np.cumprod(1.0 + r)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "high", "low", "close", "forecast", "regime"])
        for t in range(n):
            w.writerow([ts[t].strftime("%Y-%m-%dT%H:%M:%SZ"), f"{close[t] * 1.01:.6f}",
                        f"{close[t] * 0.99:.6f}", f"{close[t]:.6f}", f"{r[t] * 100:.6f}", "unknown"])


def _build(tmp_path: Path, *, signs=(1.0,) * 6, symbols=("BTCUSD",), bar_windows=None,
           claim=None, card_claim="same", source_claim=True, fold=FOLD, with_bars=True,
           envelope=None, extra_source=None, protocol_blocks=None, seed0=0,
           config_period=2) -> tuple:
    """(campaign root, child run dir). The source run holds a v3 reading with one side
    finding; the child's brief names it, its card carries `card_claim`, and its base
    variant has bars on `bar_windows` (default: every block) with the planted `signs`."""
    root = tmp_path / "camp"
    claim = claim or _claim()
    env = {"vehicle": copy.deepcopy(CHANGE), "combines_as": "execution_rule",
           "fold_observed": "A"} if envelope is None else envelope
    if source_claim:
        _save(root / "runs" / SRC / "artifacts" / "proposals" / f"{CAT}.yaml",
              _reading(claim, **env) if extra_source is None else extra_source)
    arts = root / "runs" / CHILD / "artifacts"
    _save(arts / "research_brief.yaml", {"candidate": {"source": {
        "proposal_ref": f"runs/{SRC}/artifacts/proposals/{CAT}.yaml#{PID}"}}})
    pre = {"machine_constraints": {"protocol": ({"fold": fold} if fold else {})}}
    _save(arts / "pre_registration.yaml", pre)
    _save(arts / "hypothesis_card.yaml", {"hypothesis_id": "H-1",
                                          "claim": claim if card_claim == "same" else card_claim})
    blocks = BLOCKS if protocol_blocks is None else protocol_blocks
    (arts / "variants").mkdir(parents=True, exist_ok=True)
    (arts / "variants" / "run_protocol.json").write_text(json.dumps({
        "symbols": list(symbols), "timeframe": "1d",
        "windows": [{"label": b["label"], "test": {"start": b["start"], "end": b["end"]}}
                    for b in blocks]}), encoding="utf-8")
    results = []
    use = set(range(len(BLOCKS))) if bar_windows is None else set(bar_windows)
    for si, sym in enumerate(symbols):
        for wi, block in enumerate(BLOCKS):
            if wi not in use:
                continue
            rid = f"base_{sym}_{block['label']}"
            results.append({"symbol": sym, "window": block["label"], "run_id": rid,
                            "core": {"sharpe": 0.1}})
            if with_bars:
                _bars(root / "runs" / CHILD / "variants" / "base" / "results" / rid / "bars.csv",
                      block, signs[wi % len(signs)], seed0 + 100 * si + wi)
    _save(arts / "variants" / "base" / "protocol_result.yaml", {"results": results})
    if config_period is not None:       # the strategy config the base variant was backtested on
        _write_variant_config(arts, "base", config_period)
    return root, root / "runs" / CHILD


def _config(period) -> dict:
    """A strategy config with the component of CHANGE: params.period == `period`."""
    return {"regime_detector": {"components": []},
            "strategies": {"regimes": {"trend": {"components": [
                {"id": "shock_reversal", "class": "ShockReversal",
                 "params": {"period": period}, "weight": 1.0}]}}}}


def _write_variant_config(arts: Path, vid: str, period) -> None:
    d = arts / "variants" / vid
    d.mkdir(parents=True, exist_ok=True)
    (d / "strategy_config.json").write_text(json.dumps(_config(period)), encoding="utf-8")


def _confirm(root, child, **kw):
    return fc.confirm_on_fold(child, CHILD, root=root, folds_doc=DOC, eras=ERAS,
                              holdout_start=HOLDOUT, **kw)


def _measured(oriented_by_h: dict, *, windows=None, status=cmeas.MEASURED, name="up_day_follow",
              pooled=None, floor_not_met=None) -> dict:
    """A claim_measure.measure_test-shaped result: {horizon: [per-window oriented values]}.
    `pooled` {horizon: value} overrides the pooled oriented value (default: the windows' mean).
    `floor_not_met` is claim_measure's own list of floor entries (R5); a list shorter than the
    fold leaves the later windows ABSENT from the measurement (no bars there). Each cell carries
    n_events 11 (claim_tests' per-window count, R5; the pooled n_events is their sum) and the
    result the claim's own `floor`, as claim_measure.measure_test returns them."""
    if status != cmeas.MEASURED:
        return {"name": name, "status": status, "reason": "x", "spec_hash": "h"}
    hz = {}
    for h, vals in oriented_by_h.items():
        pw = {f"BTCUSD/{LABELS[i % len(LABELS)]}{'' if i < len(LABELS) else i}":
              {"value": v, "oriented": v, "n_events": 11} for i, v in enumerate(vals)}
        defined = [v for v in vals if v is not None]
        p = (pooled or {}).get(h, float(np.mean(defined)) if defined else None)
        hz[h] = {"value": p, "oriented": p, "n_events": 11 * len(vals), "per_window": pw}
    out = {"name": name, "status": cmeas.MEASURED, "spec_hash": "h", "horizons": hz,
           "floor": {"min_events": 100}}
    if floor_not_met is not None:
        out["floor_not_met"] = list(floor_not_met)
    return out


def _fake(results_by_test: dict):
    def _measure(run_dir, vid, tests, labels, eras, holdout_start):
        return results_by_test, list(labels)
    return _measure


# ---------------------------------------------------------------------------
# 1. The claim record
# ---------------------------------------------------------------------------

def test_execution_behaviour_is_a_claim_kind_only_under_the_folds_flag():
    assert "execution_behaviour" not in cc.CLAIM_KINDS             # the original closed list
    assert cc.FOLDS_CLAIM_KINDS == ("execution_behaviour",)
    res = cc.check_claim(_claim(), folds=True)
    assert res.errors == [] and len(res.tests) == 1
    none = dict(_claim(), tests="none", missing_block="the trade-level exit-cause family")
    res = cc.check_claim(none, folds=True)
    assert res.errors == [] and res.tests_none
    assert "execution_behaviour" not in cc.KIND_BLOCK     # never a block: no kind-vs-block warning
    assert cc.check_claim(_claim(kind="vibes"), folds=True).errors     # still a closed list
    # flag off (the default): refused, and the message is exactly the one a made-up kind gets
    off = cc.check_claim(_claim())
    assert off.errors == [f"claim.kind: 'execution_behaviour' is not one of {list(cc.CLAIM_KINDS)}"]
    assert cc.check_claim(_claim(kind="vibes")).errors == [
        f"claim.kind: 'vibes' is not one of {list(cc.CLAIM_KINDS)}"]
    assert cc.check_claim(_claim(), folds=False).errors == off.errors


def test_flag_off_every_prompt_input_that_names_the_kinds_is_as_before():
    """CLAIM_TESTS.md (model input of step 1a and the readers) and the card schema's kind
    enum do not mention the new kind; its guide is a separate file shown to no prompt."""
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas"
                         / "hypothesis_card.schema.json").read_text(encoding="utf-8"))
    assert tuple(schema["properties"]["claim"]["properties"]["kind"]["enum"]) == cc.CLAIM_KINDS
    skills = SR_ROOT / "workflow_artifacts" / "skills" / "hypothesis-design"
    assert "execution_behaviour" not in (skills / "CLAIM_TESTS.md").read_text(encoding="utf-8")
    assert "| `execution_behaviour` |" in (skills / "CLAIM_TESTS_EXECUTION.md").read_text(encoding="utf-8")
    # no prompt reads the separate guide
    src = (SR_ROOT / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    assert "CLAIM_TESTS_EXECUTION" not in src


def test_the_folds_flag_reaches_every_claim_check_of_the_orchestrator(monkeypatch):
    _orch(FOLDS_ON, monkeypatch)
    assert rpr._claim_check_folds() == {"folds": True}
    monkeypatch.setattr(rpr, "_folds_enabled", lambda cfg=None: False)
    assert rpr._claim_check_folds() == {}
    item = {"claim": _claim()}
    assert ec.finding_route(item)[0] == ec.NOT_MEASURABLE             # flag off: refused
    assert ec.finding_route(item, folds=True)[0] == ec.PENDING
    assert ec.finding_spec_hashes(item) == [] and len(ec.finding_spec_hashes(item, folds=True)) == 1


def test_the_envelope_never_sits_inside_the_claim():
    claim = dict(_claim(), vehicle=CHANGE)
    assert any("unknown keys" in e for e in cc.check_claim(claim).errors)


def _check(side_extra, *, envelope, from_model=True, claim=None):
    doc = _reading(claim or _claim(), **side_extra)
    rp.check_reading(doc, CAT, "reading", from_model=from_model, envelope=envelope)


def test_under_the_flag_a_model_must_write_a_vehicle():
    good = {"vehicle": CHANGE, "combines_as": "execution_rule", "fold_observed": "A"}
    _check(good, envelope=True)                                    # accepted
    with pytest.raises(rp.ProposalError, match="`vehicle` is required"):
        _check({}, envelope=True)
    with pytest.raises(rp.ProposalError, match="`vehicle` is required"):
        _check({"combines_as": "knowledge_only"}, envelope=True)


def test_each_envelope_key_is_checked():
    with pytest.raises(rp.ProposalError, match="combines_as='forecast'"):
        _check({"vehicle": CHANGE, "combines_as": "forecast"}, envelope=True)
    for ok in rp.COMBINES_AS:
        _check({"vehicle": CHANGE, "combines_as": ok}, envelope=True)
    assert rp.COMBINES_AS == ("forecast_block", "regime_gate", "execution_rule", "knowledge_only")
    _check({"vehicle": CHANGE, "fold_observed": "D"}, envelope=True)   # D-123: D is drawn too
    with pytest.raises(rp.ProposalError, match="fold_observed='E'"):
        _check({"vehicle": CHANGE, "fold_observed": "E"}, envelope=True)
    # D-089 (a): an empty vehicle only for execution_behaviour (accepted there, see
    # test_d089_vehicle_and_coins.py); any other kind is refused
    with pytest.raises(rp.ProposalError, match="vehicle"):
        _check({"vehicle": []}, envelope=True, claim=_claim(kind="event_behaviour"))
    with pytest.raises(rp.ProposalError, match="vehicle"):
        _check({"vehicle": [{"component_id": "c"}]}, envelope=True)
    with pytest.raises(rp.ProposalError, match="OR `config_change`"):
        _check({"vehicle": CHANGE, "config_change": CHANGE}, envelope=True)


def test_without_the_flag_a_models_envelope_is_refused_as_before():
    with pytest.raises(rp.ProposalError, match="a side finding is exactly"):
        _check({"vehicle": CHANGE}, envelope=False)
    with pytest.raises(rp.ProposalError, match="a side finding is exactly"):
        _check({"combines_as": "knowledge_only"}, envelope=False)
    _check({}, envelope=False)                                     # no vehicle needed, as before
    _check({"config_change": CHANGE}, envelope=False)


def test_a_file_already_written_loads_with_or_without_the_flag():
    doc = _reading(_claim(), vehicle=CHANGE, combines_as="regime_gate", fold_observed="B")
    rp.check_reading(doc, CAT, "reading")                           # from_model False: a file
    rp.check_reading(_reading(_claim()), CAT, "reading")            # an old file, no envelope


def test_the_vehicle_reaches_decide_next_as_the_findings_config_change(tmp_path):
    _save(tmp_path / "proposals" / f"{CAT}.yaml",
          _reading(_claim(), vehicle=CHANGE, combines_as="execution_rule", fold_observed="A"))
    items = rp.load_proposals(tmp_path / "proposals", [CAT])[CAT]
    assert len(items) == 1
    item = items[0]
    assert item["config_change"] == CHANGE and item["vehicle"] == CHANGE
    assert item["combines_as"] == "execution_rule" and item["fold_observed"] == "A"
    plain = rp.flatten_reading(_reading(_claim()))[0]
    assert not (set(plain) & rp.ENVELOPE_KEYS)                      # no envelope: no new key


# D-198: the orchestrator's reader answer validation (`_validate_reading_output`), the readers'
# side-finding refusal under folds and the reader worker are deleted with the readers; the
# envelope shape checks above (reader_proposals.check_reading) stay.


# ---------------------------------------------------------------------------
# 2. THE NOISE RULE, on handcrafted measurements (the exact boundary)
# ---------------------------------------------------------------------------

POS, NEG = 0.02, -0.02


def _grade(oriented_by_h, **kw):
    return fc.grade_test(_measured(oriented_by_h, **kw))


def test_the_constants_are_the_rule():
    assert fc.MIN_WINDOWS == 4 and fc.WINDOWS_ALLOWED_AGAINST == 1
    assert "NOISE RULE" in fc.RULE_TEXT and "no cost" in fc.RULE_TEXT


def test_six_of_six_and_five_of_six_confirm_four_of_six_does_not():
    assert _grade({1: [POS] * 6})["status"] == fc.CONFIRMED
    g = _grade({1: [POS] * 5 + [NEG]}, pooled={1: 0.01})
    assert g["status"] == fc.CONFIRMED
    assert g["horizons"]["1"]["windows_claimed_sign"] == 5 and g["horizons"]["1"]["windows_with_value"] == 6
    g = _grade({1: [POS] * 4 + [NEG] * 2}, pooled={1: 0.01})
    assert g["status"] == fc.NOT_CONFIRMED and "4 of 6" in g["reason"]
    assert _grade({1: [POS] * 3 + [NEG] * 3}, pooled={1: 0.01})["status"] == fc.NOT_CONFIRMED


def test_the_pooled_sign_must_hold_even_when_the_windows_do():
    g = _grade({1: [POS] * 6}, pooled={1: -0.001})
    assert g["status"] == fc.NOT_CONFIRMED and g["horizons"]["1"]["pooled_sign_held"] is False
    assert _grade({1: [POS] * 6}, pooled={1: 0.0})["status"] == fc.NOT_CONFIRMED   # > 0, strictly
    # a window at exactly zero is not the claimed sign
    assert _grade({1: [POS] * 4 + [0.0, 0.0]}, pooled={1: 0.01})["status"] == fc.NOT_CONFIRMED
    assert _grade({1: [POS] * 5 + [0.0]}, pooled={1: 0.01})["status"] == fc.CONFIRMED


def test_every_horizon_must_hold_both_parts():
    both = {1: [POS] * 6, 2: [POS] * 6}
    assert _grade(both)["status"] == fc.CONFIRMED
    assert _grade(both, pooled={1: 0.02, 2: -0.01})["status"] == fc.NOT_CONFIRMED
    windows_fail = {1: [POS] * 6, 2: [POS] * 4 + [NEG] * 2}
    g = _grade(windows_fail, pooled={1: 0.02, 2: 0.01})
    assert g["status"] == fc.NOT_CONFIRMED and "h=2" in g["reason"]


def test_too_few_of_the_folds_windows_with_a_value_is_not_measurable():
    # R5: a window with no value counts against, so a fold of 6 needs 5 windows with a value
    g = _grade({1: [POS] * 3})
    assert g["status"] == fc.NOT_MEASURABLE and "too few of the fold's windows with a value" in g["reason"]
    assert "4 needed" in g["reason"]                  # 3 cells measured: the MIN_WINDOWS backstop
    assert _grade({1: [POS] * 4})["status"] == fc.CONFIRMED          # a fold of 4 windows, all with a value
    assert _grade({1: [POS, POS, POS, None, None, None]})["status"] == fc.NOT_MEASURABLE
    # 4 of 6 windows with a value: the empty windows count against, so it cannot be graded
    assert _grade({1: [POS, POS, POS, POS, None, None]})["status"] == fc.NOT_MEASURABLE
    assert _grade({1: [POS, POS, POS, POS, POS, None]})["status"] == fc.CONFIRMED
    # one horizon too short to grade makes the whole test not measurable
    assert _grade({1: [POS] * 6, 2: [POS] * 3 + [None] * 3})["status"] == fc.NOT_MEASURABLE


def test_a_refutation_at_a_judged_horizon_is_not_confirmed_even_if_another_horizon_is_short():
    g = _grade({1: [NEG] * 6, 24: [POS] * 3 + [None] * 3}, pooled={1: -0.02, 24: 0.02})
    assert g["status"] == fc.NOT_CONFIRMED and "h=1" in g["reason"] and "h=24" not in g["reason"]
    # windows fail at h=1 (4 of 6) with a short h=24: still a refutation
    g = _grade({1: [POS] * 4 + [NEG] * 2, 24: [POS] * 3 + [None] * 3}, pooled={1: 0.01, 24: 0.02})
    assert g["status"] == fc.NOT_CONFIRMED
    # every judged horizon holds and one is short: not measurable (cannot confirm)
    g = _grade({1: [POS] * 6, 24: [POS] * 3 + [None] * 3})
    assert g["status"] == fc.NOT_MEASURABLE and "too few" in g["reason"] and "5 needed" in g["reason"]
    # a short horizon with the wrong sign is not itself judged
    g = _grade({1: [POS] * 6, 24: [NEG] * 3 + [None] * 3}, pooled={1: 0.02, 24: -0.02})
    assert g["status"] == fc.NOT_MEASURABLE
    assert fc.combine({"t": g})[0] == fc.NOT_MEASURABLE


# --- R5 (operator ruling 2026-10-19, report #495 item 1): the claim's floor, and the count over
# --- the fold's windows (an empty window counts against). Synthetic shapes only.

FOLD_WINDOWS = list(LABELS)                 # the fold's six windows, as confirm_on_fold passes them
FLOOR = ["events=100 at h=1 (have 60)"]     # claim_measure's own floor_not_met entry


def _grade_fold(oriented_by_h, **kw):
    return fc.grade_test(_measured(oriented_by_h, **kw), FOLD_WINDOWS)


def test_r5_a_floor_not_met_is_not_measurable_and_never_confirmed():
    g = _grade_fold({1: [POS] * 6}, floor_not_met=FLOOR)
    assert g["status"] == fc.NOT_MEASURABLE and g["reason"].startswith("floor not met")
    assert FLOOR[0] in g["reason"]
    # even a clean 0 of 6 refutation: the floor is read first, so it is not a refutation
    g = _grade_fold({1: [NEG] * 6}, pooled={1: -0.02}, floor_not_met=FLOOR)
    assert g["status"] == fc.NOT_MEASURABLE and g["reason"].startswith("floor not met")
    # a floor entry at ANY horizon: h=24 short of the floor while h=1 refutes
    g = _grade_fold({1: [NEG] * 6, 24: [POS] * 6}, pooled={1: -0.02, 24: 0.02},
                    floor_not_met=["events=100 at h=24 (have 60)"])
    assert g["status"] == fc.NOT_MEASURABLE and g["reason"].startswith("floor not met")
    # without fold_windows too
    g = fc.grade_test(_measured({1: [POS] * 6}, floor_not_met=FLOOR))
    assert g["status"] == fc.NOT_MEASURABLE and g["reason"].startswith("floor not met")
    # no entry (an empty list, or no key at all) is no floor problem
    assert _grade_fold({1: [POS] * 6}, floor_not_met=[])["status"] == fc.CONFIRMED
    assert _grade_fold({1: [POS] * 6})["status"] == fc.CONFIRMED


def test_r5_a_floor_not_met_is_not_measurable_in_a_combined_claim():
    no = fc.grade_test(_measured({1: [POS] * 6}, floor_not_met=FLOOR), FOLD_WINDOWS)
    ok = _grade_fold({1: [POS] * 6})
    assert fc.combine({"a": ok, "b": no})[0] == fc.NOT_MEASURABLE


def test_r5_five_measured_all_positive_with_one_window_absent_confirms():
    g = _grade_fold({1: [POS] * 5})                       # the 6th window has no cell at all
    assert g["status"] == fc.CONFIRMED
    h = g["horizons"]["1"]
    assert (h["windows_claimed_sign"], h["windows_with_value"], h["windows_in_fold"]) == (5, 5, 6)
    assert h["windows_against"] == 1 and h["windows_without_value"] == [FOLD_WINDOWS[5]]


def test_r5_pooled_bare_window_keys_with_one_window_absent_count_against():
    # the multi-coin shape: per-window cells pooled over the coins, keyed by the bare window
    # label (no "<symbol>/" prefix); the sixth window has no cell at all
    res = _measured({1: [POS] * 5})
    hz = res["horizons"][1]
    hz["per_window"] = {f"{s}/{w}": {"value": POS, "oriented": POS}
                        for s in ("BTCUSD", "ETHUSD") for w in FOLD_WINDOWS[:5]}
    hz[fc.POOLED_KEY] = {w: {"value": POS, "oriented": POS} for w in FOLD_WINDOWS[:5]}
    g = fc.grade_test(res, FOLD_WINDOWS)
    assert g["status"] == fc.CONFIRMED
    h = g["horizons"]["1"]
    assert h["windows_without_value"] == [FOLD_WINDOWS[5]]
    assert (h["windows_in_fold"], h["windows_with_value"], h["windows_against"]) == (6, 5, 1)
    assert f"{h['windows_claimed_sign']} of {h['windows_in_fold']}" == "5 of 6"


def test_r5_four_positive_one_negative_one_absent_is_a_real_refutation():
    g = _grade_fold({1: [POS] * 4 + [NEG]}, pooled={1: 0.01})
    assert g["status"] == fc.NOT_CONFIRMED and "4 of 6" in g["reason"]
    assert "1 without a value" in g["reason"]


def test_r5_five_positive_one_absent_with_a_negative_pooled_value_is_not_confirmed():
    g = _grade_fold({1: [POS] * 5}, pooled={1: -0.001})
    assert g["status"] == fc.NOT_CONFIRMED and g["horizons"]["1"]["pooled_sign_held"] is False


def test_r5_four_positive_one_none_one_absent_is_not_measurable():
    # two windows without a value (a cell holding None, and a window with no cell): 4 of 6
    # with a value, 5 needed -> too few to grade, not a refutation
    g = _grade_fold({1: [POS] * 4 + [None]})
    assert g["status"] == fc.NOT_MEASURABLE and "too few" in g["reason"] and "5 needed" in g["reason"]
    h = g["horizons"]["1"]
    assert h["windows_with_value"] == 4 and len(h["windows_without_value"]) == 2
    # an all-empty-but-one fold is the same
    assert _grade_fold({1: [POS]})["status"] == fc.NOT_MEASURABLE


def test_r5_one_none_cell_counts_against_exactly_like_a_wrong_sign():
    assert _grade_fold({1: [POS] * 5 + [None]})["status"] == fc.CONFIRMED
    assert _grade_fold({1: [POS] * 5 + [NEG]}, pooled={1: 0.01})["status"] == fc.CONFIRMED
    # a None plus a wrong sign = two against, with 5 values: judged, and refuted
    g = _grade_fold({1: [POS] * 4 + [NEG, None]}, pooled={1: 0.01})
    assert g["status"] == fc.NOT_CONFIRMED


def test_r5_the_count_runs_over_the_measured_windows_without_fold_windows():
    # no fold_windows (None or empty): the windows the measurement carries
    res = _measured({1: [POS] * 5})
    assert fc.grade_test(res)["horizons"]["1"]["windows_in_fold"] == 5
    assert fc.grade_test(res, None)["status"] == fc.CONFIRMED
    assert fc.grade_test(res, [])["horizons"]["1"]["windows_in_fold"] == 5
    # ... and a None cell still counts against there
    g = fc.grade_test(_measured({1: [POS] * 4 + [None, None]}))
    assert g["status"] == fc.NOT_MEASURABLE
    assert g["horizons"]["1"]["windows_in_fold"] == 6


def test_r5_a_judged_horizon_that_refutes_stands_while_another_horizon_is_short():
    g = _grade_fold({1: [POS] * 4 + [NEG], 24: [POS] * 3},
                    pooled={1: 0.01, 24: 0.02})
    assert g["status"] == fc.NOT_CONFIRMED and "h=1" in g["reason"] and "h=24" not in g["reason"]
    # a pooled-negative judged horizon likewise
    g = _grade_fold({1: [POS] * 5, 24: [POS] * 3}, pooled={1: -0.01, 24: 0.02})
    assert g["status"] == fc.NOT_CONFIRMED
    # every judged horizon holds and the other is short: not measurable
    g = _grade_fold({1: [POS] * 5, 24: [POS] * 3}, pooled={1: 0.01, 24: 0.02})
    assert g["status"] == fc.NOT_MEASURABLE and "h=24" in g["reason"] and "too few" in g["reason"]


@pytest.mark.parametrize("shape", [
    {1: [POS] * 5 + [NEG]},                                         # one horizon, the last window against
    {1: [NEG] + [POS] * 5},                                         # the first window against
    {1: [POS] * 5 + [NEG], 3: [POS, NEG] + [POS] * 4},              # two horizons, one against at each
    {1: [POS] * 6, 3: [POS] * 3 + [NEG] + [POS] * 2},               # one horizon unanimous, one 5 of 6
])
def test_r5_the_shape_of_the_three_recorded_confirmations_still_confirms(shape):
    # 5 of 6 (or 6 of 6) at every horizon, no window empty, the claim's floor met
    pooled = {h: 0.01 for h in shape}
    g = _grade_fold(shape, pooled=pooled, floor_not_met=[])
    assert g["status"] == fc.CONFIRMED
    for x in g["horizons"].values():
        assert x["windows_in_fold"] == 6 and x["windows_with_value"] == 6
        assert x["windows_without_value"] == []
    assert fc.combine({"t": g})[0] == fc.CONFIRMED


def test_no_events_and_an_error_are_not_measurable_never_confirmed():
    g = fc.grade_test({"status": cmeas.NO_EVENTS, "horizons": {}})
    assert g["status"] == fc.NOT_MEASURABLE and "no events" in g["reason"]
    g = fc.grade_test({"status": cmeas.NOT_MEASURED, "reason": "error", "detail": "boom"})
    assert g["status"] == fc.NOT_MEASURABLE and "boom" in g["reason"]
    g = _grade({1: [None] * 6})
    assert g["status"] == fc.NOT_MEASURABLE and "no horizon" in g["reason"]


def test_a_claim_is_confirmed_only_if_every_test_is():
    ok = {"status": fc.CONFIRMED, "reason": "ok"}
    no = {"status": fc.NOT_CONFIRMED, "reason": "fails"}
    nm = {"status": fc.NOT_MEASURABLE, "reason": "short"}
    assert fc.combine({"a": ok, "b": ok})[0] == fc.CONFIRMED
    assert fc.combine({"a": ok, "b": no})[0] == fc.NOT_CONFIRMED
    assert fc.combine({"a": no, "b": nm})[0] == fc.NOT_CONFIRMED     # a measured failure refutes
    assert fc.combine({"a": ok, "b": nm})[0] == fc.NOT_MEASURABLE
    assert fc.combine({})[0] == fc.NOT_MEASURABLE


def test_the_chance_rate_the_docs_quote():
    from math import comb
    p5 = sum(comb(6, k) for k in (5, 6)) / 64
    assert round(p5, 3) == 0.109          # "about 11% per fold" under a symmetric null
    assert round(1 / 64, 3) == 0.016      # 6 of 6
    assert "11%" in fc.RULE_TEXT


# ---------------------------------------------------------------------------
# 3. confirm_on_fold, end to end on planted bars
# ---------------------------------------------------------------------------

def test_a_planted_effect_is_confirmed_on_the_childs_fold(tmp_path):
    root, child = _build(tmp_path)
    row = _confirm(root, child)
    assert row["status"] == fc.CONFIRMED, row["reason"]
    assert row["basis"] == fc.BASIS_CHILD_RUN and row["fold"] == FOLD
    assert row["finding_id"] == PID and row["source_run"] == SRC and row["run_id"] == CHILD
    assert row["vehicle"] == CHANGE and row["combines_as"] == "execution_rule"
    assert row["fold_observed"] == "A"                              # observed on A, measured on B
    assert row["vehicle_variant"] == "base" and row["base_variant"] == "base"
    t = row["tests"]["up_day_follow"]["horizons"]["1"]
    assert t["windows_claimed_sign"] == 6 and t["windows_with_value"] == 6 and t["oriented"] > 0
    assert row["agreement"] == {"up_day_follow": {"1": "6 of 6"}}
    assert row["effect"]["up_day_follow"]["1"] == t["effect"]
    assert sorted(w.split("/")[1] for w in row["windows_measured"]) == sorted(LABELS)
    assert row["_comparisons"] == [{"test": "up_day_follow",
                                    "spec_hash": row["spec_hashes"][0], "n_comparisons": 1}]
    assert row["confirmation_set"] == ec.set_key([dict(b) for b in BLOCKS])


def test_no_cost_appears_in_a_row(tmp_path):
    root, child = _build(tmp_path)
    text = yaml.safe_dump(_confirm(root, child)).lower()
    for word in ("cost", "slippage", "fee", "bps", "net_return", "profit"):
        assert word not in text.replace("no cost comparison", ""), word


def test_a_null_effect_is_not_confirmed(tmp_path):
    root, child = _build(tmp_path, signs=(0.0,), seed0=11)
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_CONFIRMED, row["reason"]
    assert "noise rule fails" in row["reason"]
    assert row["tests"]["up_day_follow"]["horizons"]["1"]["windows_claimed_sign"] < 5


def test_the_planted_signs_are_what_the_measurement_sees(tmp_path):
    """The fixture itself: a planted sign is the sign of its window."""
    signs = (1.0, -1.0, 1.0, -1.0, 1.0, -1.0)
    root, child = _build(tmp_path, signs=signs)
    row = _confirm(root, child)
    per_window = row["tests"]["up_day_follow"]["horizons"]["1"]["per_window"]
    got = [per_window[f"BTCUSD/{b['label']}"] > 0 for b in BLOCKS]
    assert got == [s > 0 for s in signs]


def test_five_of_six_confirms_and_four_of_six_does_not(tmp_path):
    root, child = _build(tmp_path, signs=(1.0, 1.0, 1.0, 1.0, 1.0, -1.0))
    row = _confirm(root, child)
    h = row["tests"]["up_day_follow"]["horizons"]["1"]
    assert (h["windows_claimed_sign"], h["windows_with_value"]) == (5, 6)
    assert h["oriented"] > 0 and row["status"] == fc.CONFIRMED
    root, child = _build(tmp_path / "b", signs=(1.0, 1.0, 1.0, 1.0, -1.0, -1.0))
    row = _confirm(root, child)
    h = row["tests"]["up_day_follow"]["horizons"]["1"]
    assert (h["windows_claimed_sign"], h["windows_with_value"]) == (4, 6)
    assert h["oriented"] > 0 and row["status"] == fc.NOT_CONFIRMED   # the sign held; the rule did not


def test_a_coin_with_bars_in_three_of_the_folds_windows_is_not_measurable(tmp_path):
    root, child = _build(tmp_path, bar_windows=(3, 4, 5))
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "too few" in row["reason"]
    assert row["tests"]["up_day_follow"]["horizons"]["1"]["windows_with_value"] == 3
    root, child = _build(tmp_path / "four", bar_windows=(2, 3, 4, 5))
    assert _confirm(root, child)["status"] == fc.NOT_MEASURABLE     # R5: four of the fold's six is too few
    root, child = _build(tmp_path / "five", bar_windows=(1, 2, 3, 4, 5))
    row = _confirm(root, child)
    assert row["status"] == fc.CONFIRMED          # five of six: the empty one counts as the one against
    # the agreement is "k of F": F is the fold's windows, not the windows with a value
    assert row["agreement"]["up_day_follow"]["1"] == "5 of 6"
    h = row["tests"]["up_day_follow"]["horizons"]["1"]
    assert (h["windows_with_value"], h["windows_in_fold"], h["windows_against"]) == (5, 6, 1)
    assert h["windows_without_value"] == [BLOCKS[0]["label"]]


# --- R5, operator 2026-10-19: a claim graded not_measurable keeps what was measured ----------

def _kept(row, expect_floor, windows):
    """What every measured row keeps, whatever its status: the claim's floor in the test entry,
    and per window the selected events with an outcome (same cells as per_window, summing to the
    pooled n_events), all plain YAML-able ints."""
    t = row["tests"]["up_day_follow"]
    assert t["floor"] == expect_floor
    h = t["horizons"]["1"]
    epw = h["events_per_window"]
    assert set(epw) == {f"BTCUSD/{w}" for w in windows} == set(h["per_window"])
    assert all(type(n) is int and n > 0 for n in epw.values()), epw
    assert sum(epw.values()) == h["n_events"]
    yaml.safe_dump(row)
    return h


def test_r5_a_floor_not_met_row_keeps_the_events_and_the_floor(tmp_path):
    root, child = _build(tmp_path, with_bars=False)
    res = {"up_day_follow": _measured({1: [POS] * 6}, floor_not_met=FLOOR)}
    row = _confirm(root, child, measure=_fake(res))
    assert row["status"] == fc.NOT_MEASURABLE and "floor not met" in row["reason"]
    h = _kept(row, {"min_events": 100}, LABELS)
    assert h["events_per_window"] == {f"BTCUSD/{w}": 11 for w in LABELS}
    # the effect and agreement a not_measurable row already carried are still there
    assert row["agreement"] == {"up_day_follow": {"1": "6 of 6"}}
    # the entry's floor is a copy, not the measurement's own dict
    assert row["tests"]["up_day_follow"]["floor"] is not res["up_day_follow"]["floor"]
    # graded alone, the horizon keeps its events too
    g = fc.grade_test(res["up_day_follow"], LABELS)
    assert g["horizons"]["1"]["events_per_window"] == h["events_per_window"]


def test_r5_a_floor_not_met_on_real_bars_keeps_the_events_and_the_floor(tmp_path):
    root, child = _build(tmp_path, claim=_claim(floor=10 ** 6))
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "floor not met" in row["reason"]
    _kept(row, {"min_events": 10 ** 6}, LABELS)


@pytest.mark.parametrize("bar_windows", [(3, 4, 5), (2, 3, 4, 5)])
def test_r5_a_too_few_windows_row_keeps_the_events_and_the_floor(tmp_path, bar_windows):
    root, child = _build(tmp_path, bar_windows=bar_windows)
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "too few" in row["reason"]
    h = _kept(row, {"min_events": 10}, [LABELS[i] for i in bar_windows])
    assert h["windows_with_value"] == len(bar_windows)
    assert len(h["events_per_window"]) == len(bar_windows)           # the absent windows: no cell


def test_r5_a_too_few_windows_row_with_an_injected_measure(tmp_path):
    root, child = _build(tmp_path, with_bars=False)
    res = {"up_day_follow": _measured({1: [POS] * 3})}               # bars in 3 of the fold's 6
    row = _confirm(root, child, measure=_fake(res))
    assert row["status"] == fc.NOT_MEASURABLE and "too few" in row["reason"]
    h = _kept(row, {"min_events": 100}, LABELS[:3])
    assert h["n_events"] == 33


def test_r5_a_confirmed_row_keeps_them_too(tmp_path):
    root, child = _build(tmp_path)
    row = _confirm(root, child)
    assert row["status"] == fc.CONFIRMED
    _kept(row, {"min_events": 10}, LABELS)


def test_r5_an_early_exit_before_measurement_keeps_status_and_reason_only(tmp_path):
    root, child = _build(tmp_path, with_bars=False)
    # a result claim_measure did not measure (an error, mixed return bases): status + reason only
    for status, why in ((cmeas.NOT_MEASURED, "x"), (cmeas.NOT_MEASURED, cmeas.MIXED_BASES)):
        res = _measured({}, status=status)
        res["reason"] = why
        row = _confirm(root, child, measure=_fake({"up_day_follow": res}))
        assert row["status"] == fc.NOT_MEASURABLE and row["reason"] == f"up_day_follow: not measured: {why}"
        entry = row["tests"]["up_day_follow"]
        assert set(entry) == {"spec_hash", "status", "reason"}, entry
        assert not row.get("agreement") and not row.get("effect")
    # a claim with no test at all, a measurement that raises, a changed spec: no test entry
    claim = dict(_claim(), tests="none", missing_block="trade-level exit cause")
    r2, c2 = _build(tmp_path / "none", claim=claim, card_claim=claim)
    row = _confirm(r2, c2)
    assert row["status"] == fc.NOT_MEASURABLE and "tests" not in row
    row = _confirm(root, child, measure=lambda *a: (_ for _ in ()).throw(OSError("bars.csv")))
    assert row["status"] == fc.NOT_MEASURABLE and "tests" not in row
    r3, c3 = _build(tmp_path / "changed", card_claim=_claim(value=0.001))
    row = _confirm(r3, c3)
    assert row["status"] == fc.NOT_COMPARABLE and "tests" not in row
    assert "events_per_window" not in json.dumps(row) and "min_events" not in json.dumps(row)


def test_a_selector_that_matches_nothing_is_not_measurable_and_still_a_look(tmp_path):
    claim = _claim(value=5.0)                                      # no bar is up 500%
    root, child = _build(tmp_path, claim=claim)
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "no events" in row["reason"]
    assert "up_day_follow" in row["reason"]
    assert row["_comparisons"] and row["_comparisons"][0]["test"] == "up_day_follow"


def test_a_changed_spec_is_not_comparable_and_nothing_is_measured(tmp_path):
    root, child = _build(tmp_path, card_claim=_claim(value=0.001))
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_COMPARABLE and "not comparable" in row["reason"]
    assert row["own_spec_hashes"] != row["spec_hashes"]
    assert "tests" not in row and "_comparisons" not in row        # no measurement, no look
    # a card with no usable claim test is not the claim either
    root, child = _build(tmp_path / "nocard", card_claim={"statement": "x"})
    assert _confirm(root, child)["status"] == fc.NOT_COMPARABLE


def test_tests_none_is_not_measurable_knowledge(tmp_path):
    claim = dict(_claim(), tests="none", missing_block="trade-level exit cause")
    root, child = _build(tmp_path, claim=claim, card_claim=claim)
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "tests: none" in row["reason"]
    assert row["vehicle"] == CHANGE                                 # the record keeps the envelope


def test_an_unreadable_or_missing_source_is_a_row_not_a_crash(tmp_path):
    root, child = _build(tmp_path, source_claim=False)
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "not in the source run's proposals" in row["reason"]
    root, child = _build(tmp_path / "x", extra_source={"not": "a reading"})
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "cannot be read" in row["reason"]


def test_a_run_not_built_from_a_side_finding_gives_no_row(tmp_path):
    root, child = _build(tmp_path)
    (child / "artifacts" / "research_brief.yaml").write_text("candidate: {}\n", encoding="utf-8")
    assert _confirm(root, child) is None
    # a patch (a legacy v2 list) is not a claim either
    root, child = _build(tmp_path / "p", extra_source=[{
        "proposal_id": PID, "kind": "patch", "evidence": ["e"], "scores": _scores(),
        "model_id": "m", "rubric_version": "trade_efficiency-reader-v2",
        "patch": [{"component_id": "c", "field": "f", "before": 1, "after": 2}]}])
    assert _confirm(root, child) is None


def test_a_child_without_a_fold_or_on_other_windows_is_not_measured(tmp_path):
    root, child = _build(tmp_path, fold=None)
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "no fold" in row["reason"] and row["fold"] is None
    # the pre-registration says fold B but the protocol ran other windows
    other = DOC["folds"]["C"]
    root, child = _build(tmp_path / "w", protocol_blocks=other)
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "not exactly fold B" in row["reason"]


def test_the_vehicle_must_be_in_the_measured_config(tmp_path):
    root, child = _build(tmp_path)                       # base config carries period == 2 (the vehicle)
    assert _confirm(root, child)["status"] == fc.CONFIRMED
    # step 1b reverted the vehicle (period back to its `before` value): not measurable, named
    _write_variant_config(child / "artifacts", "base", 1)
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "tests" not in row
    assert row["reason"].startswith("vehicle_not_in_measured_config")
    assert "shock_reversal.params.period" in row["reason"] and "has 1" in row["reason"]
    assert len(row["vehicle_missing"]) == 1 and row["vehicle_variant"] == "base"
    # a missing component, a missing field and an unreadable config are not measurable either
    cfg = child / "artifacts" / "variants" / "base" / "strategy_config.json"
    cfg.write_text(json.dumps({"strategies": {"regimes": {}}}), encoding="utf-8")
    assert "0 components" in _confirm(root, child)["reason"]
    cfg.write_text(json.dumps(_config(2)).replace('"period": 2', '"other": 2'), encoding="utf-8")
    assert "does not resolve" in _confirm(root, child)["reason"]
    cfg.write_text("not json", encoding="utf-8")
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "cannot be read" in row["reason"]
    cfg.unlink()
    assert _confirm(root, child)["reason"].startswith("vehicle_not_in_measured_config")


def test_every_vehicle_change_is_checked_and_all_the_missing_are_listed():
    two = CHANGE + [{"component_id": "shock_reversal", "field": "params.threshold",
                     "before": 0.5, "after": 0.9}]
    assert fc.vehicle_missing(_config(2), CHANGE) == []
    miss = fc.vehicle_missing(_config(2), two)
    assert len(miss) == 1 and "params.threshold" in miss[0]
    assert len(fc.vehicle_missing(_config(1), two)) == 2
    assert fc.vehicle_missing(_config(2), []) == []                   # an empty vehicle: nothing to check


def test_the_vehicle_is_read_from_the_named_vehicle_variant(tmp_path):
    import shutil
    root, child = _build(tmp_path)
    arts = child / "artifacts"
    # a second graded variant `alt` that carries the vehicle while `base` does not
    _write_variant_config(arts, "base", 1)
    shutil.copytree(arts / "variants" / "base", arts / "variants" / "alt")
    _write_variant_config(arts, "alt", 2)
    assert _confirm(root, child)["reason"].startswith("vehicle_not_in_measured_config")
    row = _confirm(root, child, vehicle_variant="alt",
                   measure=_fake({"up_day_follow": _measured({1: [POS] * 6})}))
    assert row["status"] == fc.CONFIRMED and row["vehicle_variant"] == "alt"


def test_the_orchestrator_passes_the_vehicle_variant_through(tmp_path, monkeypatch):
    seen = {}

    def _fake_confirm(*a, **kw):
        seen.update(kw)
    monkeypatch.setattr(rpr, "_folds_enabled", lambda cfg=None: True)
    monkeypatch.setattr(fc, "confirm_on_fold", _fake_confirm)
    monkeypatch.setattr(rpr, "_claim_measure_variants", lambda *a, **k: ([], {}))
    rpr._confirm_on_fold_after_backtests(tmp_path, "run_x", "alt")
    assert seen["vehicle_variant"] == "alt"
    rpr._confirm_on_fold_after_backtests(tmp_path, "run_x")
    assert seen["vehicle_variant"] is None


def test_a_vehicle_variant_that_was_not_backtested_this_attempt_is_not_measured(tmp_path):
    root, child = _build(tmp_path)
    row = _confirm(root, child, fresh_variants=[])
    assert row["status"] == fc.NOT_MEASURABLE and "was not backtested in this attempt" in row["reason"]
    assert _confirm(root, child, fresh_variants=["base"])["status"] == fc.CONFIRMED


def test_the_measurement_is_the_generic_one_and_trade_tests_plug_in_through_it(tmp_path):
    root, child = _build(tmp_path, with_bars=False)
    calls = []

    def custom(run_dir, vid, tests, labels, eras, holdout_start):
        calls.append((vid, [t["name"] for t in tests], list(labels), holdout_start))
        return {"up_day_follow": _measured({1: [POS] * 6})}, list(labels)

    row = _confirm(root, child, measure=custom)
    assert row["status"] == fc.CONFIRMED
    assert calls == [("base", ["up_day_follow"], LABELS, HOLDOUT)]    # vehicle variant, fold's blocks
    row = _confirm(root, child, measure=custom, vehicle_variant="base", base_variant="base")
    assert row["vehicle_variant"] == "base"


def test_a_measure_that_raises_is_a_row(tmp_path):
    root, child = _build(tmp_path, with_bars=False)

    def boom(*a):
        raise FileNotFoundError("bars.csv")

    row = _confirm(root, child, measure=boom)
    assert row["status"] == fc.NOT_MEASURABLE and "bars.csv" in row["reason"]


def test_a_bar_at_the_holdout_start_is_refused(tmp_path):
    """The fold's windows never reach the holdout, and the generic measurement still refuses
    any bar at or after the start it is given."""
    root, child = _build(tmp_path)
    assert all(b["end"] < HOLDOUT for b in BLOCKS)
    row = fc.confirm_on_fold(child, CHILD, root=root, folds_doc=DOC, eras=ERAS,
                             holdout_start="2019-01-01")           # bars of 2019-05.. reach it
    assert row["status"] == fc.NOT_MEASURABLE and "holdout start" in row["reason"]


# ---------------------------------------------------------------------------
# 4. The ledger
# ---------------------------------------------------------------------------

def test_one_row_per_measurement_and_no_duplicate_on_resume(tmp_path):
    root, child = _build(tmp_path)
    ledger_root = tmp_path / "ledger"
    first = ec.record_fold_confirmation(ledger_root, _confirm(root, child))
    again = ec.record_fold_confirmation(ledger_root, _confirm(root, child))   # a resume / re-run
    doc = ec.load_ledger(ledger_root)
    assert list(doc["fold_confirmations"]) == [f"{PID}@{CHILD}"]
    row = doc["fold_confirmations"][f"{PID}@{CHILD}"]
    assert row["status"] == fc.CONFIRMED and row["fold"] == FOLD and row["basis"] == "child_run"
    assert row["agreement"] == {"up_day_follow": {"1": "6 of 6"}}
    assert "_comparisons" not in row
    # the look is counted once, on the fold's windows
    assert len(doc["looks"]) == 1 and doc["looks"][0]["run_id"] == CHILD
    key = ec.set_key([dict(b) for b in BLOCKS])
    assert doc["by_set"] == {key: {"n_looks": 1, "n_comparisons": 1}}
    assert first["looks"] == again["looks"] == {"confirmation_set": key, "n_looks_on_set": 1,
                                               "n_comparisons_on_set": 1}
    assert doc["findings"] == {}                                   # kept apart from E-072's findings


def test_refuted_and_not_measurable_claims_stay_as_rows(tmp_path):
    ledger_root = tmp_path / "ledger"
    for n, (kw, status) in enumerate([({}, fc.CONFIRMED), ({"signs": (0.0,), "seed0": 11}, fc.NOT_CONFIRMED),
                                      ({"bar_windows": (3, 4, 5)}, fc.NOT_MEASURABLE)]):
        root, child = _build(tmp_path / f"r{n}", **kw)
        row = _confirm(root, child)
        row = dict(row, run_id=f"run_c{n}")
        assert row["status"] == status
        ec.record_fold_confirmation(ledger_root, row)
    rows = ec.fold_rows(ec.load_ledger(ledger_root))
    assert sorted(r["status"] for r in rows) == sorted([fc.CONFIRMED, fc.NOT_CONFIRMED, fc.NOT_MEASURABLE])
    assert all(r["reason"] for r in rows)


def test_a_row_without_its_ids_is_refused(tmp_path):
    with pytest.raises(ValueError, match="needs run_id"):
        ec.record_fold_confirmation(tmp_path, {"status": "confirmed"})


def test_an_e072_rewrite_of_the_file_keeps_the_fold_rows(tmp_path):
    root, child = _build(tmp_path)
    ledger_root = tmp_path / "ledger"
    ec.record_fold_confirmation(ledger_root, _confirm(root, child))
    ec.record(ledger_root, "run_other", [{"finding_id": "z", "source_run": "run_other",
                                          "confirmation_sign_retained": ec.PENDING,
                                          "status": ec.PENDING}])
    doc = ec.load_ledger(ledger_root)
    assert list(doc["fold_confirmations"]) == [f"{PID}@{CHILD}"] and "z" in doc["findings"]
    assert len(doc["looks"]) == 1


def test_a_ledger_without_fold_rows_is_written_exactly_as_before(tmp_path):
    ec.record(tmp_path, "run_1", [{"finding_id": "a", "source_run": "run_1",
                                   "confirmation_sign_retained": True}])
    assert "fold_confirmations" not in ec.load_ledger(tmp_path)
    assert ec.fold_summary_lines(ec.load_ledger(tmp_path)) == []


def test_the_campaign_summary_has_one_line_per_status_fold_labelled(tmp_path):
    ledger_root = tmp_path / "ledger"
    assert ec.summary_lines(ledger_root) == []                      # no ledger: no lines
    for n, (fold, status) in enumerate([("B", fc.CONFIRMED), ("B", fc.CONFIRMED), ("C", fc.NOT_CONFIRMED),
                                        ("B", fc.NOT_MEASURABLE)]):
        ec.record_fold_confirmation(ledger_root, {
            "run_id": f"run_c{n}", "finding_id": f"f{n}", "status": status, "fold": fold,
            "confirmation_set": f"set_{fold}"})
    text = "\n".join(ec.summary_lines(ledger_root))
    assert "## Claims measured on a child run's fold (E-077" in text
    assert "- Confirmed: 2 (fold B 2)" in text
    assert "- Not confirmed: 1 (fold C 1)" in text
    assert "- Not measurable: 1 (fold B 1)" in text
    assert "Not comparable" not in text                              # shown only when there is one
    assert "noise rule" in text and "11%" in text
    ec.record_fold_confirmation(ledger_root, {"run_id": "run_c9", "finding_id": "f9",
                                              "status": fc.NOT_COMPARABLE, "fold": "B"})
    assert "- Not comparable: 1 (fold B 1)" in "\n".join(ec.summary_lines(ledger_root))


def test_a_pending_finding_with_a_fold_row_is_not_counted_pending(tmp_path):
    ledger_root = tmp_path / "ledger"
    ec.record(ledger_root, "run_src", [
        {"finding_id": "pend", "source_run": "run_src", "confirmation_sign_retained": ec.PENDING},
        {"finding_id": "other", "source_run": "run_src", "confirmation_sign_retained": ec.PENDING}])
    text = "\n".join(ec.summary_lines(ledger_root))
    assert "Side findings: 2 (" in text and "pending 2" in text
    ec.record_fold_confirmation(ledger_root, {"run_id": "run_c", "finding_id": "pend",
                                              "status": fc.CONFIRMED, "fold": "B"})
    text = "\n".join(ec.summary_lines(ledger_root))
    assert "Side findings: 1 (" in text and "pending 1" in text


def test_the_campaign_summary_regenerates_with_the_fold_lines(tmp_path):
    import run_campaign as camp
    ec.record_fold_confirmation(rpr.ROOT, {"run_id": "run_c", "finding_id": "f", "status": fc.CONFIRMED,
                                           "fold": "B", "confirmation_set": "s"})
    camp._regenerate_summary({"version": "1.0", "queue": []})
    text = camp.CAMPAIGN_SUMMARY_PATH.read_text(encoding="utf-8")
    assert "- Confirmed: 1 (fold B 1)" in text


# ---------------------------------------------------------------------------
# 5. The orchestrator wiring and the flag
# ---------------------------------------------------------------------------

def _into_sandbox(tmp_path, monkeypatch, flags, **kw):
    """The fixture child under the sandboxed ROOT (rpr.ROOT), as a stage would see it."""
    import shutil
    _set_orchestrator(flags)
    monkeypatch.chdir(SR_ROOT)
    root, child = _build(tmp_path, **kw)
    dest = rpr.ROOT / "runs" / CHILD
    shutil.copytree(child, dest, dirs_exist_ok=True)
    shutil.copytree(root / "runs" / SRC, rpr.ROOT / "runs" / SRC, dirs_exist_ok=True)
    return dest


def _fresh(dest: Path) -> None:
    """The backtest result is newer than the attempt's start (as it is when the stage runs)."""
    import os
    import time
    later = time.time_ns() + 10**9
    for p in (dest / "artifacts" / "variants").glob("*/protocol_result.yaml"):
        os.utime(p, ns=(later, later))


def test_flag_on_the_stage_writes_the_row_and_the_artifact(tmp_path, monkeypatch):
    dest = _into_sandbox(tmp_path, monkeypatch, FOLDS_ON)
    rpr._clear_fold_confirmation(dest)                              # the attempt starts
    _fresh(dest)
    rpr._confirm_on_fold_after_backtests(dest, CHILD)
    art = yaml.safe_load((dest / "artifacts" / fc.ROW_ARTIFACT).read_text(encoding="utf-8"))
    assert art["status"] == fc.CONFIRMED and art["fold"] == FOLD
    doc = ec.load_ledger(rpr.ROOT)
    assert list(doc["fold_confirmations"]) == [f"{PID}@{CHILD}"]
    rpr._confirm_on_fold_after_backtests(dest, CHILD)               # a resume
    doc = ec.load_ledger(rpr.ROOT)
    assert list(doc["fold_confirmations"]) == [f"{PID}@{CHILD}"] and len(doc["looks"]) == 1
    # a re-run of protocol_execution clears the artifact, not the ledger row
    rpr._clear_fold_confirmation(dest)
    assert not (dest / "artifacts" / fc.ROW_ARTIFACT).exists()
    assert list(ec.load_ledger(rpr.ROOT)["fold_confirmations"]) == [f"{PID}@{CHILD}"]


def test_a_stale_backtest_is_not_measured(tmp_path, monkeypatch):
    """No recorded attempt start (or a result older than the attempt): nothing is measured."""
    dest = _into_sandbox(tmp_path, monkeypatch, FOLDS_ON)
    rpr._FOLD_CONFIRM_ATTEMPT_START.pop(str(dest.resolve()), None)
    rpr._confirm_on_fold_after_backtests(dest, CHILD)
    art = yaml.safe_load((dest / "artifacts" / fc.ROW_ARTIFACT).read_text(encoding="utf-8"))
    assert art["status"] == fc.NOT_MEASURABLE and "not backtested in this attempt" in art["reason"]


def test_flag_off_the_stage_does_nothing(tmp_path, monkeypatch):
    dest = _into_sandbox(tmp_path, monkeypatch, {})
    rpr._clear_fold_confirmation(dest)
    rpr._confirm_on_fold_after_backtests(dest, CHILD)
    assert not (dest / "artifacts" / fc.ROW_ARTIFACT).exists()
    assert not (rpr.ROOT / ec.LEDGER_REL).exists()
    assert str(dest.resolve()) not in rpr._FOLD_CONFIRM_ATTEMPT_START


def test_a_failure_in_the_confirmation_never_stops_the_run(tmp_path, monkeypatch, capsys):
    dest = _into_sandbox(tmp_path, monkeypatch, FOLDS_ON)
    rpr._clear_fold_confirmation(dest)
    monkeypatch.setattr(ec, "record_fold_confirmation",
                        lambda *a, **k: (_ for _ in ()).throw(OSError("disk full")))
    rpr._confirm_on_fold_after_backtests(dest, CHILD)               # must not raise
    assert "could not be recorded" in capsys.readouterr().out
    art = yaml.safe_load((dest / "artifacts" / fc.ROW_ARTIFACT).read_text(encoding="utf-8"))
    assert art["status"] == "error" and "disk full" in art["detail"]


def test_the_stage_is_called_after_the_claim_measurement_in_the_run_loop():
    src = (SR_ROOT / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    a = src.index("_measure_claim_tests_after_backtests(RUN_DIR, run_id)")
    b = src.index("_confirm_on_fold_after_backtests(RUN_DIR, run_id)")
    assert 0 < a < b and b - a < 600
    assert "_clear_fold_confirmation(RUN_DIR)" in src


def test_routes_in_run_does_not_exist_under_the_folds_flag():
    pure = {"claim": _claim(kind="event_behaviour")}
    assert ec.finding_route(pure)[0] == ec.IN_RUN                   # flag off: as before
    assert ec.finding_route(pure, folds=True) == (ec.PENDING, ec.FOLD_PENDING_REASON)
    block = {"claim": dict(_claim(), kind="direction_forecast")}
    assert ec.finding_route(block, folds=True)[0] == ec.PENDING
    # refused claims and `tests: none` route as before
    none = {"claim": dict(_claim(), tests="none", missing_block="x")}
    assert ec.finding_route(none, folds=True)[0] == ec.NOT_MEASURABLE
    assert ec.finding_route({"claim": {"kind": "vibes"}}, folds=True)[0] == ec.NOT_MEASURABLE


def _orch(flags_extra, monkeypatch):
    from _reader_test_helpers import V3_ON, _run070_shaped
    return _run070_shaped(monkeypatch, {**V3_ON, **flags_extra})


# D-198: the in-run confirmation stage tests (`_record_confirmations` after the readers, the weak
# follow-up resolution) went with the readers and the explore_confirm flag.


def test_flag_off_the_e072_ledger_and_summary_are_byte_identical(tmp_path):
    """record() now shares helpers with the fold rows; its file must not change by one byte
    when there are no fold rows."""
    rec = {"finding_id": "a", "source_run": "run_1", "confirmation_sign_retained": True,
           "confirmation_set": "S", "_comparisons": [{"test": "t", "spec_hash": "h", "n_comparisons": 2}]}
    ec.record(tmp_path, "run_1", [rec])
    doc = yaml.safe_load((tmp_path / ec.LEDGER_REL).read_text(encoding="utf-8"))
    assert list(doc) == ["schema_version", "note", "bar", "findings", "looks", "by_set"]
    assert doc["by_set"] == {"S": {"n_looks": 1, "n_comparisons": 2}}
    assert doc["findings"]["a"]["looks"] == {"confirmation_set": "S", "n_looks_on_set": 1,
                                             "n_comparisons_on_set": 2}
    lines = ec.summary_lines(tmp_path)
    assert lines[1] == "## Side findings on unseen windows (E-072; information only, not proven)"
    assert not any("E-077" in x for x in lines)


def test_the_folds_flag_stays_off_in_the_shipped_config():
    cfg = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["folds"]["enabled"] is False
    assert "fold_confirm" not in json.dumps(cfg)                    # no second flag
