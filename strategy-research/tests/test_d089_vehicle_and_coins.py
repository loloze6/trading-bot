"""D-089 (operator, 2026-10-08): two decisions under orchestrator.folds.enabled.

(a) A claim of kind execution_behaviour may change nothing: `vehicle: []` -- the child
    re-runs today's strategy on the next fold and the strategy's own behaviour there is the
    test. Every other kind still needs a non-empty vehicle.
(b) Several coins, option C: in each window the coins are pooled into one value first, then
    "all but one window" is applied over the fold's windows (3 coins x 6 windows: 5 of 6
    pooled windows confirm, 4 of 6 do not). One coin is measured exactly as before.

Fixtures are the E-077 PR-2 test's (real bars written to disk, read by the real measurement).
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import numpy as np
import pytest

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import claim_card as cc  # noqa: E402
import claim_measure as cmeas  # noqa: E402
import claim_tests as ct  # noqa: E402
import decide_next as dn  # noqa: E402
import explore_confirm as ec  # noqa: E402
import fold_confirm as fc  # noqa: E402
import reader_findings as rfi  # noqa: E402
import reader_proposals as rp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

import test_e077_pr2_confirm as base  # noqa: E402  (fixtures: _build, _claim, _reading, ...)
from test_e077_pr2_confirm import (CAT, CHANGE, LABELS, _build,  # noqa: E402
                                   _claim, _confirm, _reading)

COINS = ("BTCUSD", "ETHUSD", "XRPUSD")
EMPTY = {"vehicle": [], "combines_as": "execution_rule", "fold_observed": "A"}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _check_model(claim, **envelope):
    rp.check_reading(_reading(claim, **envelope), CAT, "reading", from_model=True, envelope=True)


# ---------------------------------------------------------------------------
# (a) an empty vehicle: execution_behaviour only
# ---------------------------------------------------------------------------

def test_the_kinds_allowed_an_empty_vehicle_are_the_folds_kinds():
    assert rp.EMPTY_VEHICLE_KINDS == cc.FOLDS_CLAIM_KINDS == ("execution_behaviour",)


def test_an_empty_vehicle_is_accepted_for_execution_behaviour():
    _check_model(_claim(kind="execution_behaviour"), **EMPTY)


@pytest.mark.parametrize("kind", ["event_behaviour", "direction_forecast", "cost_turnover"])
def test_an_empty_vehicle_is_refused_for_every_other_kind(kind):
    with pytest.raises(rp.ProposalError, match=r"vehicle: an empty vehicle .* allowed only for a "
                                               r"claim of kind \['execution_behaviour'\]"):
        _check_model(_claim(kind=kind), **EMPTY)
    # the same claim with a real vehicle is accepted, as before
    _check_model(_claim(kind=kind), **dict(EMPTY, vehicle=copy.deepcopy(CHANGE)))


def test_a_missing_vehicle_is_still_refused_and_names_the_empty_form():
    env = {k: v for k, v in EMPTY.items() if k != "vehicle"}
    with pytest.raises(rp.ProposalError, match=r"`vehicle` is required .*`vehicle: \[\]` only"):
        _check_model(_claim(kind="execution_behaviour"), **env)


def test_a_file_with_an_empty_vehicle_loads_and_reaches_decide_next_as_no_change():
    doc = _reading(_claim(kind="execution_behaviour"), **EMPTY)
    rp.check_reading(doc, CAT, "file")                                   # a file, as it stands
    (item,) = rp.flatten_reading(doc)
    assert item["config_change"] == [] and item["vehicle"] == []
    start = dn.side_finding_start(item, {"base_config": {"a": 1}, "manifest": {"m": 1}})
    assert start == {"config": {"a": 1}, "manifest": {"m": 1}, "ops": [], "reason": None}
    with pytest.raises(rp.ProposalError, match="allowed only for a claim of kind"):
        rp.check_reading(_reading(_claim(kind="event_behaviour"), **EMPTY), CAT, "file")


def test_side_finding_review_accepts_execution_behaviour_only_with_folds():
    item = {"claim": _claim(kind="execution_behaviour")}
    assert rfi.side_finding_review(item, prior={}, own=set(), run_id="r", folds=True)["errors"] == []
    flag_off = rfi.side_finding_review(item, prior={}, own=set(), run_id="r")
    assert flag_off["errors"] and "execution_behaviour" in flag_off["errors"][0]


def test_decide_next_passes_folds_to_the_review_only_under_the_flag(monkeypatch):
    seen = []

    def spy(p, **kw):
        seen.append({k: v for k, v in kw.items() if k == "folds"})
        return {"errors": [], "tests_none": False, "missing_block": None, "spec_hashes": [],
                "warnings": []}
    monkeypatch.setattr(rfi, "side_finding_review", spy)
    dn._side_finding_review("r", {}, {"claim": {}}, {"memory": {}})
    dn._side_finding_review("r", {}, {"claim": {}}, {"memory": {}, "folds": {"doc": {}}})
    assert seen == [{}, {"folds": True}]


@pytest.mark.parametrize("flag_on", [False, True])
def test_the_orchestrators_reading_review_passes_folds_only_under_the_flag(flag_on, monkeypatch):
    seen = []

    def spy(item, **kw):
        seen.append({k: v for k, v in kw.items() if k == "folds"})
        return {"errors": [], "tests_none": False, "missing_block": None, "spec_hashes": [],
                "warnings": []}
    monkeypatch.setattr(rfi, "side_finding_review", spy)
    monkeypatch.setattr(rpr, "_reader_findings_module", lambda: rfi)
    monkeypatch.setattr(rpr, "_folds_enabled", lambda: flag_on)
    rpr._reading_content_errors({"side_findings": [{"claim": {}}]}, CAT, Path("nowhere"))
    assert seen == [{"folds": True} if flag_on else {}]


def test_a_claim_with_an_empty_vehicle_is_measured_on_the_unchanged_strategy(tmp_path):
    root, child = _build(tmp_path, claim=_claim(kind="execution_behaviour"), envelope=EMPTY,
                         config_period=1)                   # the source config, unchanged
    row = _confirm(root, child)
    assert row["status"] == fc.CONFIRMED, row["reason"]
    assert row["vehicle"] == [] and "vehicle_missing" not in row
    assert row["vehicle_variant"] == "base"


# ---------------------------------------------------------------------------
# (b) several coins: pooled per window first (option C)
# ---------------------------------------------------------------------------

def _signs(n_pos):
    return tuple([1.0] * n_pos + [-1.0] * (6 - n_pos))


def test_three_coins_five_of_six_pooled_windows_confirm(tmp_path):
    root, child = _build(tmp_path, symbols=COINS, signs=_signs(5))
    row = _confirm(root, child)
    assert row["status"] == fc.CONFIRMED, row["reason"]
    assert row["window_basis"] == "coins_pooled_per_window"
    h = row["tests"]["up_day_follow"]["horizons"]["1"]
    assert h["windows_with_value"] == 6 and h["windows_claimed_sign"] == 5
    assert sorted(h["per_window"]) == sorted(LABELS)                     # windows, not cells
    assert row["agreement"] == {"up_day_follow": {"1": "5 of 6"}}
    # under the old cell count this fold would need 17 of 18 cells: it has at most 15
    assert len(row["windows_measured"]) == 18


def test_three_coins_four_of_six_pooled_windows_do_not_confirm(tmp_path):
    root, child = _build(tmp_path, symbols=COINS, signs=_signs(4))
    row = _confirm(root, child)
    assert row["status"] == fc.NOT_CONFIRMED
    assert row["agreement"] == {"up_day_follow": {"1": "4 of 6"}}


def test_a_window_is_pooled_over_its_coins_not_voted(tmp_path):
    """In each window one coin is against, two are for: pooled, every window holds."""
    root, child = _build(tmp_path, symbols=COINS)
    against = COINS[2]
    for wi, block in enumerate(base.BLOCKS):             # the third coin plants the reverse
        rid = f"base_{against}_{block['label']}"
        base._bars(child / "variants" / "base" / "results" / rid / "bars.csv", block, -1.0,
                   500 + wi)
    measured_by_cell = {}

    def measure(run_dir, vid, tests, labels, eras, holdout_start):
        res, measured = fc.measure_on_fold(run_dir, vid, tests, labels, eras, holdout_start)
        measured_by_cell.update(res["up_day_follow"]["horizons"][1]["per_window"])
        return res, measured
    row = _confirm(root, child, measure=measure)
    assert row["status"] == fc.CONFIRMED, row["reason"]
    assert len(measured_by_cell) == 18                      # the cells are still recorded
    against_cells = [c["oriented"] for k, c in measured_by_cell.items() if k.startswith(against)]
    assert all(v < 0 for v in against_cells)                # a vote per cell: 12 of 18, refuted
    assert row["tests"]["up_day_follow"]["horizons"]["1"]["windows_with_value"] == 6


def test_pooled_per_window_is_the_statistic_over_the_coins_events(tmp_path):
    root, child = _build(tmp_path, symbols=COINS)
    ws = ct.load_variant_bars(child, "base")
    spec, _h = cmeas.test_spec(_claim()["tests"][0])
    per, _out, _hz, _rng = ct.effect_sizes(ws, spec, None)
    cells = fc.pooled_per_window(per, spec, 1)
    assert list(cells) == LABELS
    for win in LABELS:
        sub = [p for p in per if p["w"].window == win]
        y = np.concatenate([p["ys"][1] for p in sub])
        m = np.concatenate([p["mask"] for p in sub])
        wr = np.concatenate([p["wref"] for p in sub])
        ok = np.isfinite(y)
        hand = y[m & ok].mean() - np.average(y[ok], weights=wr[ok])        # mean_diff, by hand
        assert cells[win]["value"] == pytest.approx(hand, rel=1e-12)
        assert cells[win]["coins"] == list(COINS)


def test_one_coin_is_measured_exactly_as_before(tmp_path):
    """The default measurement of one coin is the pre-D-089 one (measure_on_windows): the
    same row, field for field, and no pooled cells."""
    for signs in (_signs(6), _signs(5), _signs(4)):
        d = tmp_path / str(len([s for s in signs if s > 0]))
        root, child = _build(d, signs=signs)
        new = _confirm(root, child)
        old = _confirm(root, child, measure=ec.measure_on_windows)
        assert new == old
        assert "window_basis" not in new
        res, _m = fc.measure_on_fold(child, "base", [_claim()["tests"][0]], LABELS, base.ERAS,
                                     base.HOLDOUT)
        assert all(fc.POOLED_KEY not in x for x in res["up_day_follow"]["horizons"].values())


def test_one_coins_pooled_window_equals_its_cell(tmp_path):
    root, child = _build(tmp_path)
    ws = ct.load_variant_bars(child, "base")
    spec, _h = cmeas.test_spec(_claim()["tests"][0])
    per, out, _hz, _rng = ct.effect_sizes(ws, spec, None)
    cells = fc.pooled_per_window(per, spec, 1)
    for p in per:
        assert cells[p["w"].window]["oriented"] == out[1]["per_window"][p["w"].label]["oriented"]


def test_several_coins_without_pooled_values_are_never_graded_per_cell():
    r = {"name": "t", "status": cmeas.MEASURED, "spec_hash": "h", "horizons": {1: {
        "value": 0.1, "oriented": 0.1, "n_events": 9,
        "per_window": {f"{c}/{w}": {"value": 0.1, "oriented": 0.1} for c in COINS for w in LABELS}}}}
    g = fc.grade_test(r)
    assert g["status"] == fc.NOT_MEASURABLE and fc.POOLED_KEY in g["reason"]
    r["horizons"][1][fc.POOLED_KEY] = {w: {"value": 0.1, "oriented": 0.1} for w in LABELS}
    assert fc.grade_test(r)["status"] == fc.CONFIRMED
