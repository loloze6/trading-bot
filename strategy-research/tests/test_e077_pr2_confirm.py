"""
E-077 PR-2 (CUL-421, D-087) -- the claim record and confirmation on the child run's
fold, behind orchestrator.folds.enabled (off by default; no new flag).

Proven here, all with synthetic inputs (no LLM, no backtest, no market data, no
cache, no holdout bar; every date is in 2018-2021):
  1. The claim record: kind `execution_behaviour` is accepted by check_claim (and by
     the card schema and CLAIM_TESTS.md); the proposal ENVELOPE (`vehicle`,
     `combines_as`, `fold_observed`) is validated where reader proposals are: a model's
     answer under the flag MUST carry a vehicle, a bad `combines_as` / `fold_observed`
     / a vehicle that does not resolve / both vehicle and config_change are refused; the
     vehicle reaches decide-next as the finding's config change.
  2. THE NOISE RULE on handcrafted measurements (the exact boundary): 6 of 6 and 5 of 6
     windows confirm, 4 of 6 does not, 3 windows with a value is not measurable, no
     events is not measurable, a negative pooled sign at ANY horizon is not confirmed,
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

from test_e046a_slice5b_ii_b_readers_stage import RUN_ID, _set_orchestrator  # noqa: E402

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
           envelope=None, extra_source=None, protocol_blocks=None, seed0=0) -> tuple:
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
    return root, root / "runs" / CHILD


def _confirm(root, child, **kw):
    return fc.confirm_on_fold(child, CHILD, root=root, folds_doc=DOC, eras=ERAS,
                              holdout_start=HOLDOUT, **kw)


def _measured(oriented_by_h: dict, *, windows=None, status=cmeas.MEASURED, name="up_day_follow",
              pooled=None) -> dict:
    """A claim_measure.measure_test-shaped result: {horizon: [per-window oriented values]}.
    `pooled` {horizon: value} overrides the pooled oriented value (default: the windows' mean)."""
    if status != cmeas.MEASURED:
        return {"name": name, "status": status, "reason": "x", "spec_hash": "h"}
    hz = {}
    for h, vals in oriented_by_h.items():
        pw = {f"BTCUSD/{LABELS[i % len(LABELS)]}{'' if i < len(LABELS) else i}":
              {"value": v, "oriented": v} for i, v in enumerate(vals)}
        defined = [v for v in vals if v is not None]
        p = (pooled or {}).get(h, float(np.mean(defined)) if defined else None)
        hz[h] = {"value": p, "oriented": p, "n_events": 99, "per_window": pw}
    return {"name": name, "status": cmeas.MEASURED, "spec_hash": "h", "horizons": hz}


def _fake(results_by_test: dict):
    def _measure(run_dir, vid, tests, labels, eras, holdout_start):
        return results_by_test, list(labels)
    return _measure


# ---------------------------------------------------------------------------
# 1. The claim record
# ---------------------------------------------------------------------------

def test_execution_behaviour_is_a_claim_kind_and_a_finding_only():
    assert "execution_behaviour" in cc.CLAIM_KINDS
    res = cc.check_claim(_claim())
    assert res.errors == [] and len(res.tests) == 1
    none = dict(_claim(), tests="none", missing_block="the trade-level exit-cause family")
    res = cc.check_claim(none)
    assert res.errors == [] and res.tests_none
    assert "execution_behaviour" not in cc.KIND_BLOCK     # never a block: no kind-vs-block warning
    assert cc.check_claim(_claim(kind="vibes")).errors     # still a closed list


def test_the_card_schema_and_the_guide_list_the_new_kind():
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas"
                         / "hypothesis_card.schema.json").read_text(encoding="utf-8"))
    assert tuple(schema["properties"]["claim"]["properties"]["kind"]["enum"]) == cc.CLAIM_KINDS
    guide = (SR_ROOT / "workflow_artifacts" / "skills" / "hypothesis-design"
             / "CLAIM_TESTS.md").read_text(encoding="utf-8")
    assert "| `execution_behaviour` |" in guide


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
    with pytest.raises(rp.ProposalError, match="fold_observed='D'"):
        _check({"vehicle": CHANGE, "fold_observed": "D"}, envelope=True)
    with pytest.raises(rp.ProposalError, match="vehicle"):
        _check({"vehicle": []}, envelope=True)
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


def _orch(flags_extra, monkeypatch):
    from test_e068_5_readers_v3 import V3_ON, _run070_shaped
    return _run070_shaped(monkeypatch, {**V3_ON, **flags_extra})


def _model_text(*, cat="trade_efficiency", run_id=RUN_ID, **envelope) -> str:
    from test_e068_5_readers_v3 import _claim as _c, _fenced, _scores as _s
    rid = f"{cat}-{run_id}"
    side = {"proposal_id": f"{rid}-1", "claim": _c(), "evidence": ["variants.base.slices.overall.y=2"],
            "scores": _s(), **envelope}
    return _fenced({"schema_version": 3, "reading_id": rid, "model_id": "m",
                    "rubric_version": f"{cat}-reading-v1", "explanation": "x",
                    "evidence": ["variants.base.slices.overall.x=1"], "side_findings": [side]})


def test_the_orchestrators_reading_check_applies_the_envelope_only_under_the_flag(monkeypatch):
    from test_e068_5_readers_v3 import _patch
    change = _patch()["patch"]                 # valid on run_070's config
    run_dir = _orch(FOLDS_ON, monkeypatch)
    ok = rpr._validate_reading_output(_model_text(vehicle=change, combines_as="execution_rule"),
                                      "trade_efficiency", run_dir)
    assert ok[1] is None, ok
    body, err = rpr._validate_reading_output(_model_text(), "trade_efficiency", run_dir)
    assert body is None and "`vehicle` is required" in err
    # a vehicle that does not resolve against the run's base config is refused like a config change
    bad = [dict(change[0], before=999)]
    body, err = rpr._validate_reading_output(_model_text(vehicle=bad), "trade_efficiency", run_dir)
    assert body is None and "side_findings[0].vehicle" in err
    # flag off: the same answer with a vehicle is refused as an undeclared key, as before
    run_dir = _orch({}, monkeypatch)
    body, err = rpr._validate_reading_output(_model_text(vehicle=change), "trade_efficiency", run_dir)
    assert body is None and "a side finding is exactly" in err
    assert rpr._validate_reading_output(_model_text(), "trade_efficiency", run_dir)[1] is None


def test_fold_observed_must_match_the_fold_the_run_ran_on(monkeypatch):
    from test_e068_5_readers_v3 import _patch
    change = _patch()["patch"]
    run_dir = _orch(FOLDS_ON, monkeypatch)
    _save(run_dir / "artifacts" / "pre_registration.yaml",
          {"machine_constraints": {"protocol": {"fold": "B"}}})
    body, err = rpr._validate_reading_output(_model_text(vehicle=change, fold_observed="A"),
                                             "trade_efficiency", run_dir)
    assert body is None and "fold_observed='A'" in err and "fold B" in err
    assert rpr._validate_reading_output(_model_text(vehicle=change, fold_observed="B"),
                                        "trade_efficiency", run_dir)[1] is None
    # a run with no registered fold (every run before the folds flag): only the shape check
    _save(run_dir / "artifacts" / "pre_registration.yaml", {"machine_constraints": {}})
    assert rpr._validate_reading_output(_model_text(vehicle=change, fold_observed="C"),
                                        "trade_efficiency", run_dir)[1] is None


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


def test_fewer_than_four_windows_with_a_value_is_not_measurable():
    g = _grade({1: [POS] * 3})
    assert g["status"] == fc.NOT_MEASURABLE and "fewer than 4" in g["reason"]
    assert _grade({1: [POS] * 4})["status"] == fc.CONFIRMED          # exactly 4 windows: measurable
    # a window with no value does not count as a window
    assert _grade({1: [POS, POS, POS, None, None, None]})["status"] == fc.NOT_MEASURABLE
    assert _grade({1: [POS, POS, POS, POS, None, None]})["status"] == fc.CONFIRMED
    # one horizon too short to grade makes the whole test not measurable
    assert _grade({1: [POS] * 6, 2: [POS] * 3 + [None] * 3})["status"] == fc.NOT_MEASURABLE


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


def test_a_coin_with_bars_in_three_windows_is_not_measurable(tmp_path):
    root, child = _build(tmp_path, bar_windows=(3, 4, 5))
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_MEASURABLE and "fewer than 4" in row["reason"]
    assert row["tests"]["up_day_follow"]["horizons"]["1"]["windows_with_value"] == 3
    root, child = _build(tmp_path / "four", bar_windows=(2, 3, 4, 5))
    assert _confirm(root, child)["status"] == fc.CONFIRMED          # four windows is enough


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
    pure = {"claim": _claim()}
    assert ec.finding_route(pure)[0] == ec.IN_RUN                   # flag off: as before
    assert ec.finding_route(pure, folds=True) == (ec.PENDING, ec.FOLD_PENDING_REASON)
    block = {"claim": dict(_claim(), kind="direction_forecast")}
    assert ec.finding_route(block, folds=True)[0] == ec.PENDING
    # refused claims and `tests: none` route as before
    none = {"claim": dict(_claim(), tests="none", missing_block="x")}
    assert ec.finding_route(none, folds=True)[0] == ec.NOT_MEASURABLE
    assert ec.finding_route({"claim": {"kind": "vibes"}}, folds=True)[0] == ec.NOT_MEASURABLE


def _e072_stage(monkeypatch, flags, run_id=RUN_ID, **kw):
    import test_e072_explore_confirm as t72
    run_dir = t72._ec_run(monkeypatch, flags=flags, run_id=run_id, **kw)
    t72._protocol_execution_part(run_dir, run_id)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", t72._readings_llm([], t72._sides()))
    return t72, run_dir


def _write_readings(run_dir: Path) -> None:
    """Two readings on disk (a pure finding and a block claim), as a reader stage leaves them.
    Written directly: under the folds flag a model's answer without a vehicle is refused, and
    the sandbox run's base config is a stub no vehicle could resolve against."""
    import test_e072_explore_confirm as t72
    from test_e068_5_readers_v3 import _reading as _rd
    for cat, sides in t72._sides().items():
        _save(run_dir / "artifacts" / "proposals" / f"{cat}.yaml", _rd(cat, sides=sides))


def test_under_the_folds_flag_no_finding_is_measured_in_run(monkeypatch):
    import test_e072_explore_confirm as t72
    t72_flags = {**t72.EC_ON, "folds": {"enabled": True}}
    t72, run_dir = _e072_stage(monkeypatch, t72_flags)
    _write_readings(run_dir)
    rpr._record_confirmations(RUN_ID, run_dir)
    doc = t72._confirmation(run_dir)
    pure = next(r for r in doc["side_findings"] if r["finding_id"] == f"trade_efficiency-{RUN_ID}-1")
    assert pure["route"] == ec.PENDING and pure["confirmation_sign_retained"] == ec.PENDING
    assert "tests" not in pure and "measured_in_run" not in pure
    ledger = ec.load_ledger(rpr.ROOT)
    assert ledger["looks"] == [] and ledger["by_set"] == {}         # nothing was looked at in-run


def test_flag_off_the_in_run_route_is_exactly_as_before(monkeypatch):
    import test_e072_explore_confirm as t72
    t72, run_dir = _e072_stage(monkeypatch, t72.EC_ON)
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    pure = next(r for r in t72._confirmation(run_dir)["side_findings"]
                if r["finding_id"] == f"trade_efficiency-{RUN_ID}-1")
    assert pure["route"] == ec.IN_RUN and pure["status"] == ec.MEASURED


def test_under_the_folds_flag_the_weak_follow_up_resolution_is_unreachable(monkeypatch):
    import test_e072_explore_confirm as t72
    flags = {**t72.EC_ON, "folds": {"enabled": True}}
    t72, run_dir = _e072_stage(monkeypatch, flags)
    _write_readings(run_dir)
    rpr._record_confirmations(RUN_ID, run_dir)
    pending = ec.load_ledger(rpr.ROOT)["findings"][f"forecast_power-{RUN_ID}-1"]
    assert pending["confirmation_sign_retained"] == ec.PENDING
    called = []
    monkeypatch.setattr(ec, "resolve_pending", lambda *a, **k: called.append(1))
    child = t72._child_run(monkeypatch, "run_991")
    _set_orchestrator(flags)                                        # _child_run reset the flags
    t72._protocol_execution_part(child, "run_991")
    rpr._record_confirmations("run_991", child)
    assert called == []                                         # never called under the flag
    rec = ec.load_ledger(rpr.ROOT)["findings"][f"forecast_power-{RUN_ID}-1"]
    assert rec["confirmation_sign_retained"] == ec.PENDING and "measured_in_run" not in rec
    assert t72._confirmation(child)["resolved_pending"] == []


def test_flag_off_the_follow_up_resolution_still_works(monkeypatch):
    import test_e072_explore_confirm as t72
    t72, run_dir = _e072_stage(monkeypatch, t72.EC_ON)
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    child = t72._child_run(monkeypatch, "run_991")
    t72._protocol_execution_part(child, "run_991")
    monkeypatch.setattr(rpr, "_invoke_reader_llm", t72._readings_llm([]))
    rpr._run_specialist_readers_stage("run_991", child)
    rec = ec.load_ledger(rpr.ROOT)["findings"][f"forecast_power-{RUN_ID}-1"]
    assert rec["measured_in_run"] == "run_991" and rec["weak"] is True


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
