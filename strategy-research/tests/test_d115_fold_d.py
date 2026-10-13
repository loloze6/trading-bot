"""D-115 (operator decision 2026-10-13): no validation stage; fold D = the six contiguous
4-month blocks of 2024-2025, defined in config/folds.yaml but OUTSIDE the automatic fold
order (decide-next still assigns A, then B, then C, then folds_exhausted, never D). The
validation guard lets through windows that are exactly fold D's blocks, wherever it runs.
A brief carrying `fold: "D"` is generated only under orchestrator.folds.enabled; flag off
it is refused exactly as on master.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "tests"))
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import run_protocol as rp  # noqa: E402
import research_folds as rf  # noqa: E402
import test_e077_folds as t77  # noqa: E402  (the decide-next scenario helpers)
from protocol_refusal import EXIT_NO_DATA_TOUCHED  # noqa: E402
from test_k3_protocol_pinning import _minimal_run  # noqa: E402

REAL_POLICY = SR_ROOT / "config" / "campaign_data_policy.yaml"
REAL_FOLDS = SR_ROOT / "config" / "folds.yaml"
DOC = rf.load_folds(REAL_FOLDS, policy_path=REAL_POLICY)
FOLD_D_WINDOWS = rf.fold_windows(DOC, "D")
MASTER_REFUSAL = "fold 'D' is not one of ['A', 'B', 'C']"  # check_fold_id's message on master


@pytest.fixture(autouse=True)
def _folds_file_in_the_sandbox():
    dest = rpr.ROOT / "config" / "folds.yaml"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REAL_FOLDS, dest)


@pytest.fixture
def folds_flag(monkeypatch, tmp_path):
    def _set(value):
        p = tmp_path / "campaign_config.yaml"
        p.write_text(yaml.safe_dump({"orchestrator": {"folds": {"enabled": value}}}), encoding="utf-8")
        monkeypatch.setattr(rf, "CAMPAIGN_CONFIG_PATH", p)
    return _set


def _fold_d_constraints():
    return {"protocol": {"symbols": ["BTCUSDT"], "timeframe": "1h", "start": "2024-01-01",
                         "end": "2025-12-31", "window_months": 4, "fold": "D",
                         "promotion": t77.PROMOTION}}


# -- the folds file ----------------------------------------------------------------------

def test_fold_d_is_six_contiguous_blocks_of_2024_2025_outside_the_automatic_order():
    assert DOC["order"] == ["A", "B", "C"]
    assert [w["label"] for w in FOLD_D_WINDOWS] == ["2024-01", "2024-05", "2024-09",
                                                    "2025-01", "2025-05", "2025-09"]
    spans = [(w["test"]["start"], w["test"]["end"]) for w in FOLD_D_WINDOWS]
    assert spans[0][0] == "2024-01-01" and spans[-1][1] == "2025-12-31"
    v_start, v_end = rf.policy_ranges(REAL_POLICY)["validation"]
    assert (v_start, v_end) == ("2024-01-01", "2025-12-31")
    for (_s, e), (s2, _e2) in zip(spans, spans[1:]):
        assert (rf.date.fromisoformat(e) + rf.timedelta(days=1)).isoformat() == s2  # contiguous


def _write(tmp_path, doc):
    p = tmp_path / "folds.yaml"
    p.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return p


def test_load_folds_refuses_a_fold_d_block_outside_2024_2025(tmp_path):
    doc = yaml.safe_load(REAL_FOLDS.read_text(encoding="utf-8"))
    doc["folds"]["D"][0] = {"label": "2017-09", "start": "2017-09-01", "end": "2017-12-31"}
    with pytest.raises(rf.FoldsError, match="fold D block 2017-09 .* outside the validation period"):
        rf.load_folds(_write(tmp_path, doc), policy_path=REAL_POLICY)


def test_load_folds_refuses_a_fold_d_block_inside_the_holdout_of_a_policy(tmp_path):
    """A synthetic holdout over fold D's last block (no sealed date written here)."""
    policy = yaml.safe_load(REAL_POLICY.read_text(encoding="utf-8"))
    policy["holdout_range"] = ["2025-10-01", "2025-11-30"]
    pp = tmp_path / "policy.yaml"
    pp.write_text(yaml.safe_dump(policy), encoding="utf-8")
    with pytest.raises(rf.FoldsError, match="fold D block 2025-09 .* overlaps the holdout"):
        rf.load_folds(REAL_FOLDS, policy_path=pp)


def test_load_folds_needs_the_fold_d_key_and_keeps_order_a_b_c(tmp_path):
    doc = yaml.safe_load(REAL_FOLDS.read_text(encoding="utf-8"))
    no_d = {**doc, "folds": {k: v for k, v in doc["folds"].items() if k != "D"}}
    with pytest.raises(rf.FoldsError, match="exactly the keys"):
        rf.load_folds(_write(tmp_path, no_d), policy_path=REAL_POLICY)
    with pytest.raises(rf.FoldsError, match="order must be exactly"):
        rf.load_folds(_write(tmp_path, {**doc, "order": ["A", "B", "C", "D"]}), policy_path=REAL_POLICY)


# -- decide-next: fold order unchanged -----------------------------------------------------

def test_a_lineage_that_used_a_b_c_is_still_exhausted_never_fold_d():
    inputs, pid = t77._scenario("run_081", "ROOT__x-run_074-1__y-run_080-1",
                                {"run_081": t77.FOLD_C, "run_080": t77.FOLD_B,
                                 "run_074": t77.FOLD_A})
    cand = t77._cand(t77._decide(inputs, "run_081"), pid)
    assert cand["fold_assignment"]["fold"] is None
    assert cand["gates"]["feasibility"]["result"] == "INFEASIBLE"
    assert any(r.startswith("folds_exhausted") for r in cand["gates"]["feasibility"]["reasons"])


def test_a_2024_run_still_uses_no_fold():
    """folds_used_by reads the automatic order only, so a 2024 window counts for no fold."""
    assert rf.folds_used_by(DOC, [("2024-02-01", "2024-02-28")]) == []


# -- the generator and the pre-flight ------------------------------------------------------

@pytest.mark.parametrize("pre_flight", [False, True])
def test_flag_off_a_fold_d_brief_is_refused_exactly_as_on_master(pre_flight):
    mc = _fold_d_constraints()
    with pytest.raises(rf.FoldsError) as exc:
        if pre_flight:
            camp._expected_generated_protocol(mc["protocol"], "run_940", promotion_retired=False,
                                              folds_enabled=False)
        else:
            rpr._ensure_protocol_from_constraints(_minimal_run(rpr.ROOT, "run_940"), "run_940", mc)
    assert str(exc.value) == MASTER_REFUSAL


def test_the_fold_d_check_adds_no_flag_read_for_a_non_d_brief():
    calls = []
    mc = {"protocol": {**_fold_d_constraints()["protocol"], "fold": "B", "start": "2018-05-01",
                       "end": "2021-12-31"}}
    rpr._ensure_protocol_from_constraints(_minimal_run(rpr.ROOT, "run_941"), "run_941", mc,
                                          folds_enabled=lambda: calls.append(1) or False)
    assert calls == [1]  # once, by the guard after G7, exactly as on master; none for the fold check


def test_flag_on_a_fold_d_brief_generates_fold_d_and_the_pre_flight_agrees():
    mc = _fold_d_constraints()
    run_dir = _minimal_run(rpr.ROOT, "run_942")
    path = rpr._ensure_protocol_from_constraints(run_dir, "run_942", mc, folds_enabled=True)
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["windows"] == FOLD_D_WINDOWS and "fold" not in doc  # no new protocol key
    ctx = yaml.safe_load((run_dir / "artifacts" / "run_context.yaml").read_text(encoding="utf-8"))
    assert ctx["fold"] == "D"
    expected = camp._expected_generated_protocol(mc["protocol"], "run_942", promotion_retired=False,
                                                 folds_enabled=True)
    assert expected["windows"] == doc["windows"]
    assert camp._validation_overlap_in(path, True) is None
    assert rf.fold_of_constraints(mc) == "D"  # recorded on the memory entry and trial rows


def test_a_pinned_file_of_fold_d_blocks_passes_and_a_1_month_2024_tile_does_not():
    ok = rpr.ROOT / "protocols" / "d_blocks.json"
    ok.parent.mkdir(parents=True, exist_ok=True)
    ok.write_text(json.dumps({"windows": FOLD_D_WINDOWS}), encoding="utf-8")
    assert camp._validation_overlap_in(ok, True) is None
    bad = rpr.ROOT / "protocols" / "tile.json"
    bad.write_text(json.dumps({"windows": [{"label": "2024-01", "test": {
        "start": "2024-01-01", "end": "2024-01-31"}}]}), encoding="utf-8")
    assert "not one of fold D's blocks" in camp._validation_overlap_in(bad, True)


# -- tools/run_protocol.py -----------------------------------------------------------------

def test_run_protocol_lets_fold_d_blocks_through_and_refuses_anything_else_in_2024_2025(
        folds_flag, capsys):
    folds_flag(True)
    assert rp._refuse_validation_period_windows({"windows": FOLD_D_WINDOWS}) is None
    shifted = [{"label": "2024-01", "test": {"start": "2024-01-02", "end": "2024-04-30"}}]
    relabelled = [{"label": "x", "test": dict(FOLD_D_WINDOWS[0]["test"])}]
    for windows in (shifted, relabelled):
        with pytest.raises(SystemExit) as exc:
            rp._refuse_validation_period_windows({"windows": windows})
        assert exc.value.code == EXIT_NO_DATA_TOUCHED
        assert "not one of fold D's blocks" in capsys.readouterr().err


# -- the guard itself ------------------------------------------------------------------------

def test_the_guard_reads_fold_d_only_when_a_window_is_in_2024_2025():
    v = ("2024-01-01", "2025-12-31")
    calls = []

    def loader():
        calls.append(1)
        return FOLD_D_WINDOWS
    rf.assert_windows_clear_of_validation(rf.fold_windows(DOC, "A"), v, loader)
    assert calls == []
    rf.assert_windows_clear_of_validation(FOLD_D_WINDOWS, v, loader)
    assert calls == [1]  # read once, not per window
    with pytest.raises(rf.ValidationBoundaryBreach):
        rf.assert_windows_clear_of_validation(FOLD_D_WINDOWS, v)  # nothing allowed by default
