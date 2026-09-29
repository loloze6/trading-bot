"""
E-062 S2b-2b -- flag wiring of the whole-test DSR (D-041 / D-046;
engineering/roadmap/E-062/S2B2_FINDINGS.md Q1 P1/C1-C6, Q2, Q5, Q6, Q7 row
S2b-2b, G1/G6/G7/G10/G11/G12).

Covers:
  1. P1: the ledger row's `whole_test` block (flag on only; not_evaluable /
     error caught into the block, the row still written and counted in N);
     run_tool_worker's call site; flag off: no key.
  2. The loader key dsr_min_same_basis_trials (required under v2, >= 2) and
     the committed value 10.
  3. The v2 DSR row: basis string, a sparse candidate gets a real DSR, the
     ledger's Sharpe is the bar's Sharpe, below-floor K uses sigma_null end to
     end, K at the floor uses the cross-trial spread, N equal flag on/off.
  4. Review item (a): the overlay is read through ONE path constant; dsr_basis
     records its presence and sha256 (absent recorded as absent).
  5. Review item (b): lockstep of the candidate's own ledger row (values,
     status, error block, missing block) and a dedup collapse onto an earlier
     block-less row raises instead of silently dropping it from K.
  6. The spend: recomputes on the whole-test basis; refuses a sharpe_basis
     mismatch and a DSR under the threshold; a small K is not a refusal.
  7. Review item (c): under D-046 the DSR row is NOT_EVALUABLE only together
     with sharpe_min (the candidate's own data) or at N < 2, so decide_next's
     R1 already classifies such an attempt `fired_before`; nothing waits on K.
  8. Flag off: dsr_basis keeps its two keys and the overlay is never read.
"""
import ast
import asyncio
import hashlib
import json
import math
import sys
from pathlib import Path
from statistics import NormalDist

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import decide_next  # noqa: E402
import deflate_sharpe  # noqa: E402
import portfolio_whole_test as pwt  # noqa: E402

from test_e058_s2a_regroup_record import RUN_ID, _seed, _set_orchestrator  # noqa: E402
from test_profit_bars_every_backtest import _seed_dsr_ledger  # noqa: E402
from test_e062_s2b1_profit_bars_v2 import (  # noqa: E402
    FULL_ON, V1_BARS, V2_BARS, V2_ON, _attach_whole_test, _build, _pbe, _v2_run,
    _write_bars, _write_cost_model)
from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402

DSR_BASIS = "deflated_sharpe_whole_test_daily_on_campaign_trial_ledger"
SHA = "a" * 64
_ND = NormalDist(0, 1)


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _state() -> dict:
    return rpr.load_yaml(rpr.CAMPAIGN_STATE_PATH)


def _own_row(trial_id=RUN_ID) -> dict:
    return next(r for r in _state()["trial_sharpes"]
                if r["trial_id"] == trial_id and r["source"] == "backtest")


def _edit_rows(fn) -> None:
    state = _state()
    fn(state["trial_sharpes"])
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, state)


def _evaluate(run_dir=None, **kw) -> dict:
    return rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID, **kw)


def _dsr_row(ev: dict, cid=RUN_ID) -> dict:
    return {r["name"]: r for r in ev["variants"][cid]["bars"]}["deflated_sharpe_threshold"]


def _rows(ev: dict, cid=RUN_ID) -> dict:
    return {r["name"]: r for r in ev["variants"][cid]["bars"]}


def _block(sr: float, t: int = 400) -> dict:
    return {"basis": pwt.WHOLE_TEST_BASIS, "status": "ok", "reason": None, "sr_daily": sr,
            "n_daily_returns": t, "skew": 0.0, "kurtosis": 3.0}


def _add_same_basis_rows(n: int, start: int = 700) -> None:
    """n more backtest rows from other runs, each with an ok whole_test block."""
    _edit_rows(lambda rows: rows.extend(
        {"trial_id": f"run_{start + i}", "source": "backtest", "statistic_valid": "sharpe",
         "sharpe": 0.1, "forecast_hash": f"fh-sb-{start + i}",
         "whole_test": _block(-0.05 + 0.01 * i)} for i in range(n)))


def _overlay_entry(trial_id: str, sr: float) -> dict:
    return {"trial_id": trial_id, "source": "backtest", **_block(sr, t=2695),
            "inputs_sha256": {"protocol_result": SHA, "portfolio_states": {"w1.csv": SHA}},
            "code_sha256": {"portfolio_whole_test.py": SHA}}


def _hand_dsr(sr, t, skew, kurt, sr0):
    return _ND.cdf((sr - sr0) * math.sqrt(t - 1)
                   / math.sqrt(1 - skew * sr + ((kurt - 1) / 4) * sr * sr))


def _z(n):
    g = 0.5772156649
    return (1 - g) * _ND.inv_cdf(1 - 1 / n) + g * _ND.inv_cdf(1 - 1 / (math.e * n))


# ---------------------------------------------------------------------------
# 1. P1 -- the ledger row's whole_test block
# ---------------------------------------------------------------------------

def test_whole_test_trial_kw_is_empty_with_the_flag_off_and_a_block_with_it_on(tmp_path):
    run_dir = tmp_path / "run"
    pr = _build(run_dir)
    for orch in (None, FULL_ON, {**FULL_ON, "profit_bars_v2": {"enabled": False}}):
        _set_orchestrator(orch)
        assert rpr._whole_test_trial_kw(run_dir, pr) == {}
    _set_orchestrator(V2_ON)
    kw = rpr._whole_test_trial_kw(run_dir, pr)
    assert set(kw) == {"whole_test"}
    block = kw["whole_test"]
    st = pwt.whole_test_sharpe_stats(rpr._whole_test_chain(run_dir, pr)[0]["daily_returns"])
    assert block == {"basis": pwt.WHOLE_TEST_BASIS, "status": "ok", "reason": None,
                     "sr_daily": st["sr_daily"], "n_daily_returns": st["T"], "skew": st["skew"],
                     "kurtosis": st["kurtosis_raw"]}


def test_ledger_block_not_evaluable_and_error_are_caught_and_the_row_still_counts(tmp_path,
                                                                                  monkeypatch):
    """G10: NOT_EVALUABLE -> status not_evaluable, any other error -> status
    error; neither raises, the row is written, N counts it and K does not."""
    run_dir = tmp_path / "run"
    ne = rpr._whole_test_ledger_block(run_dir, _build(run_dir, protocol=False))
    assert ne["status"] == "not_evaluable" and "no protocol_file" in ne["reason"]
    assert [ne[k] for k in ("sr_daily", "n_daily_returns", "skew", "kurtosis")] == [None] * 4

    def _boom(*_a, **_k):
        raise RuntimeError("disk gone")
    with monkeypatch.context() as m:
        m.setattr(rpr, "_whole_test_chain", _boom)
        err = rpr._whole_test_ledger_block(run_dir, {})
    assert err["status"] == "error" and err["reason"] == "RuntimeError: disk gone"

    cfgs = [tmp_path / "cfg1.json", tmp_path / "cfg2.json"]
    for i, cfg in enumerate(cfgs):
        cfg.write_text(json.dumps({"i": i}), encoding="utf-8")  # two distinct trials
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, {"campaign_id": "t", "runs": [], "trial_sharpes": []})
    rpr._record_backtest_trial("run_001", {"per_symbol_summary": {}}, cfgs[0], whole_test=ne)
    rpr._record_backtest_trial("run_002", {"per_symbol_summary": {}}, cfgs[1], whole_test=err)
    rows = _state()["trial_sharpes"]
    assert [r["whole_test"]["status"] for r in rows] == ["not_evaluable", "error"]
    ctx = rpr._whole_test_dsr_context()
    assert ctx["n_dsr_total"] == 2 and ctx["sample"]["K"] == 0


def test_record_backtest_trial_without_the_keyword_writes_the_legacy_row(tmp_path):
    cfg = tmp_path / "cfg.json"
    cfg.write_text("{}", encoding="utf-8")
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, {"campaign_id": "t", "runs": [], "trial_sharpes": []})
    rpr._record_backtest_trial("run_001", {"per_symbol_summary": {}}, cfg)
    assert set(_state()["trial_sharpes"][0]) == {
        "trial_id", "source", "sharpe", "expectancy_bps", "n_trades", "statistic_valid",
        "below_floor_pct", "forecast_hash"}


def _run_protocol_execution(monkeypatch, run_id: str, v2: bool) -> Path:
    """run_tool_worker("protocol_execution") on the single-config path with a
    faked run_protocol that writes real window equity files (a sparse
    candidate: below_floor_pct 80). The v2 flag is patched at its reader --
    the full flag set would also switch on the grid / readers stages, which
    need artifacts this test does not build."""
    if v2:
        monkeypatch.setattr(rpr, "_profit_bars_v2_enabled", lambda cfg=None: True)
    root = rpr.ROOT
    _write_protocol(root, f"{run_id}.json")
    run_dir = _minimal_run(root, run_id)
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, {"protocol_ref": f"protocols/{run_id}.json"})

    def _fake(cmd, *args, **kwargs):
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        pr = _build(out_dir)
        pr["hypothesis_verdict"] = {"verdict": "refine",
                                    "diagnostics": {"below_floor_pct": 80.0}}
        (out_dir / "protocol_summary.json").write_text(json.dumps(pr), encoding="utf-8")

        class _Ok:
            returncode, stdout, stderr = 0, "", ""
        return _Ok()
    monkeypatch.setattr(rpr.subprocess, "run", _fake)
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))
    return run_dir


def test_run_tool_worker_writes_the_block_only_with_the_flag(monkeypatch):
    run_dir = _run_protocol_execution(monkeypatch, "run_931", v2=False)
    row = _own_row("run_931")
    assert "whole_test" not in row and row["statistic_valid"] == "expectancy"
    _run_protocol_execution(monkeypatch, "run_932", v2=True)
    row = _own_row("run_932")
    assert row["statistic_valid"] == "expectancy"  # legacy fields still written
    pr = rpr.load_yaml(rpr.ROOT / "runs" / "run_932" / "artifacts" / "protocol_result.yaml")
    assert row["whole_test"] == rpr._whole_test_ledger_block(rpr.ROOT / "runs" / "run_932", pr)
    assert row["whole_test"]["status"] == "ok"
    assert run_dir.exists()


# ---------------------------------------------------------------------------
# 2. The loader key
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad", [1, 0, -3, True, 10.0, "10", None])
def test_v2_loader_refuses_a_bad_floor(bad):
    path = _write_bars({**V2_BARS, "dsr_min_same_basis_trials": bad})
    with pytest.raises(rpr.ProfitabilityBarsSchemaError, match="dsr_min_same_basis_trials"):
        rpr._load_profitability_bars(path, v2=True)
    assert rpr._load_profitability_bars(path)["sharpe_min"] == 1.0  # v1 ignores it


def test_committed_bars_file_carries_the_floor_and_the_new_basis():
    real = SR_ROOT / "config" / "profitability_bars.yaml"
    assert rpr._load_profitability_bars(real, v2=True)["dsr_min_same_basis_trials"] == 10
    doc = yaml.safe_load(real.read_text(encoding="utf-8"))
    # Signed by the operator 2026-09-29 (E-062 SIGNING_CHECKLIST.md).
    assert doc["ratified_by"] and str(doc["ratified_at"]) == "2026-09-29"
    assert f"basis: {DSR_BASIS}\n" in real.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 3. The v2 DSR row
# ---------------------------------------------------------------------------

def _sparse_v2_run(**build) -> Path:
    """A graded single run whose candidate is sparse (below_floor_pct 80 on its
    protocol_result and statistic_valid expectancy on its ledger row)."""
    run_dir = _v2_run(**build)
    path = run_dir / "artifacts" / "protocol_result.yaml"
    pr = rpr.load_yaml(path)
    pr["hypothesis_verdict"] = {"verdict": "refine", "diagnostics": {
        "below_floor_pct": 80.0, "per_trade_expectancy_bps": {"mean": 5.0, "se": 1.0}}}
    rpr.save_yaml(path, pr)

    def _sparse(rows):
        for r in rows:
            if r["trial_id"] == RUN_ID and r["source"] == "backtest":
                r.update(statistic_valid="expectancy", below_floor_pct=80.0)
    _edit_rows(_sparse)
    return run_dir


def test_sparse_candidate_gets_a_real_dsr():
    run_dir = _sparse_v2_run()
    pr = rpr.load_yaml(run_dir / "artifacts" / "protocol_result.yaml")
    legacy = rpr._promotion_dsr_context()["dsr_candidate"](pr)
    assert legacy[1] is True and legacy[4]["deflated_sharpe_ratio"] is None  # legacy: sparse
    ev = _evaluate(run_dir)
    row = _dsr_row(ev)
    assert row["basis"] == DSR_BASIS and row["comparator"] == ">="
    assert isinstance(row["actual"], float) and row["result"] in ("PASS", "FAIL")
    assert row["detail"]["status"] == "ok" and "expectancy" not in row["note"]


def test_ledger_sharpe_is_the_bar_sharpe():
    run_dir = _v2_run()
    ev = _evaluate(run_dir)
    block = _own_row()["whole_test"]
    rows = _rows(ev)
    assert block["sr_daily"] * math.sqrt(pwt.SHARPE_DAYS_PER_YEAR) == rows["sharpe_min"]["actual"]
    assert rows["deflated_sharpe_threshold"]["detail"]["sr_daily"] == block["sr_daily"]
    assert rows["deflated_sharpe_threshold"]["detail"]["T"] == block["n_daily_returns"]


def test_below_floor_k_uses_sigma_null_end_to_end():
    run_dir = _v2_run()
    ev = _evaluate(run_dir)
    d = _dsr_row(ev)["detail"]
    block = _own_row()["whole_test"]
    assert d["K"] == 1 == ev["dsr_basis"]["n_same_basis"] < ev["dsr_basis"]["min_same_basis"] == 10
    assert d["sigma_source"] == "null" and d["mean_same_basis"] is None
    t = block["n_daily_returns"]
    assert d["sigma_null"] == 1 / math.sqrt(t - 1)
    assert d["sr0"] == pytest.approx(d["sigma_null"] * _z(d["N"]), abs=1e-15)
    assert _dsr_row(ev)["actual"] == pytest.approx(
        _hand_dsr(block["sr_daily"], t, block["skew"], block["kurtosis"], d["sr0"]), abs=1e-12)


def test_k_at_the_floor_uses_the_cross_trial_spread():
    run_dir = _v2_run()
    _add_same_basis_rows(9)  # + the candidate = 10 = the floor
    ev = _evaluate(run_dir)
    d = _dsr_row(ev)["detail"]
    assert d["K"] == 10 and d["mean_same_basis"] is not None
    srs = [r["whole_test"]["sr_daily"] for r in _state()["trial_sharpes"] if "whole_test" in r]
    sigma_k = math.sqrt(sum((x - sum(srs) / 10) ** 2 for x in srs) / 9)
    assert d["sigma_cross"] == pytest.approx(sigma_k, rel=1e-12)
    want = max(sum(srs) / 10, 0.0) + max(sigma_k, d["sigma_null"]) * _z(d["N"])
    assert d["sr0"] == pytest.approx(want, rel=1e-12)


def test_n_is_equal_with_the_flag_on_and_off():
    run_dir = _v2_run()
    _add_same_basis_rows(3)
    on = _evaluate(run_dir)
    _set_orchestrator(FULL_ON)
    _write_bars(V1_BARS)
    off = _evaluate(run_dir)
    assert on["dsr_basis"]["n_dsr_total"] == off["dsr_basis"]["n_dsr_total"] == \
        _dsr_row(on)["detail"]["N"]
    assert on["dsr_basis"]["n_trials"] == off["dsr_basis"]["n_trials"]


def test_n_of_the_sample_and_of_the_pipeline_must_agree():
    _v2_run()
    ctx = rpr._promotion_dsr_context()
    assert rpr._whole_test_dsr_context(ctx)["n_dsr_total"] == ctx["n_dsr_total"]
    with pytest.raises(ValueError, match="the two dedup implementations disagree"):
        rpr._whole_test_dsr_context({**ctx, "n_dsr_total": ctx["n_dsr_total"] + 1})


# ---------------------------------------------------------------------------
# 4. Review item (a): the overlay
# ---------------------------------------------------------------------------

def test_overlay_is_read_through_one_path_constant_only():
    src = (SR_ROOT / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    literals = [n for n in ast.walk(tree) if isinstance(n, ast.Constant)
                and isinstance(n.value, str) and "trial_sharpe_basis_recompute" in n.value]
    assert len(literals) == 1  # the constant's own assignment
    loads = [n for n in ast.walk(tree) if isinstance(n, ast.Name)
             and n.id == "TRIAL_SHARPE_BASIS_OVERLAY_PATH" and isinstance(n.ctx, ast.Load)]
    assert len(loads) == 1  # read once, in _load_trial_sharpe_basis_overlay
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
              and n.name == "_load_trial_sharpe_basis_overlay")
    assert any(isinstance(n, ast.Name) and n.id == "TRIAL_SHARPE_BASIS_OVERLAY_PATH"
               for n in ast.walk(fn))
    for other in (SR_ROOT / "workflow").glob("*.py"):
        if other.name != "run_phase1_research.py":
            assert "trial_sharpe_basis_recompute" not in other.read_text(encoding="utf-8")


def test_overlay_absent_is_recorded_as_absent_and_present_with_its_sha():
    run_dir = _v2_run()
    assert not rpr.TRIAL_SHARPE_BASIS_OVERLAY_PATH.exists()
    absent = _evaluate(run_dir)
    assert absent["dsr_basis"]["basis_overlay"] == {"present": False, "sha256": None}
    assert absent["dsr_basis"]["sharpe_basis"] == pwt.WHOLE_TEST_BASIS

    # a legacy block-less row (run_800, _seed_dsr_ledger) recomputed in the overlay
    rpr.TRIAL_SHARPE_BASIS_OVERLAY_PATH.write_text(
        yaml.safe_dump({"entries": [_overlay_entry("run_800", 0.03)]}, sort_keys=False),
        encoding="utf-8")
    present = _evaluate(run_dir)
    sha = hashlib.sha256(rpr.TRIAL_SHARPE_BASIS_OVERLAY_PATH.read_bytes()).hexdigest()
    assert present["dsr_basis"]["basis_overlay"] == {"present": True, "sha256": sha}
    assert present["dsr_basis"]["n_same_basis"] == absent["dsr_basis"]["n_same_basis"] + 1
    assert present["dsr_basis"]["n_dsr_total"] == absent["dsr_basis"]["n_dsr_total"]  # N fixed
    assert _dsr_row(present)["detail"]["K"] == 2


def test_malformed_overlay_fails_loud_under_v2_and_is_never_read_flag_off():
    run_dir = _v2_run()
    rpr.TRIAL_SHARPE_BASIS_OVERLAY_PATH.write_text(
        yaml.safe_dump({"entries": [{**_overlay_entry("run_800", 0.03), "at": "x"}]}),
        encoding="utf-8")
    with pytest.raises(ValueError, match="basis overlay entry 0"):
        _evaluate(run_dir)
    _set_orchestrator(FULL_ON)
    _write_bars(V1_BARS)
    ev = _evaluate(run_dir)
    assert ev["dsr_basis"] == {"n_dsr_total": ev["dsr_basis"]["n_dsr_total"],
                               "n_trials": ev["dsr_basis"]["n_trials"]}
    assert _dsr_row(ev)["basis"] == "deflated_sharpe_on_campaign_trial_ledger"


# ---------------------------------------------------------------------------
# 5. Review item (b): lockstep of the candidate's own row
# ---------------------------------------------------------------------------

def _assert_dsr_not_evaluable(ev, needle: str, cid=RUN_ID) -> dict:
    """The candidate's DSR row reads NOT_EVALUABLE with `needle` in its reason,
    never a number; its OTHER bars are still graded (the stage does not fail)."""
    row = _dsr_row(ev, cid)
    assert row["result"] == "NOT_EVALUABLE" and row["actual"] is None, row
    assert needle in row["not_evaluable_reason"], row["not_evaluable_reason"]
    assert row["detail"]["dsr"] is None and row["detail"]["status"] == "not_evaluable"
    return row


def test_candidate_ledger_value_differing_from_the_graded_value_is_not_evaluable():
    run_dir = _v2_run()
    _edit_rows(lambda rows: _own_in(rows)["whole_test"].update(
        sr_daily=_own_in(rows)["whole_test"]["sr_daily"] + 1e-12))
    ev = _evaluate(run_dir)  # a resume after code/data changed: must not raise
    _assert_dsr_not_evaluable(ev, "ledger_stats_mismatch")
    assert "['sr_daily']" in _dsr_row(ev)["not_evaluable_reason"]
    assert _rows(ev)["sharpe_min"]["actual"] is not None  # the other bars are graded


def test_matching_ledger_stats_still_grade_in_lockstep():
    run_dir = _v2_run()
    row = _dsr_row(_evaluate(run_dir))
    assert row["result"] != "NOT_EVALUABLE" and isinstance(row["actual"], float)


def test_malformed_ledger_block_still_raises():
    run_dir = _v2_run()
    _edit_rows(lambda rows: _own_in(rows)["whole_test"].pop("skew"))
    with pytest.raises(ValueError):
        _evaluate(run_dir)


def _own_in(rows, trial_id=RUN_ID):
    return next(r for r in rows if r["trial_id"] == trial_id and r["source"] == "backtest")


def test_candidate_row_without_a_block_raises():
    run_dir = _v2_run()
    _edit_rows(lambda rows: _own_in(rows).pop("whole_test"))
    with pytest.raises(ValueError, match="has no whole_test block"):
        _evaluate(run_dir)


def test_candidate_status_mismatch_is_not_evaluable():
    run_dir = _v2_run()
    _edit_rows(lambda rows: _own_in(rows).update(whole_test={
        "basis": pwt.WHOLE_TEST_BASIS, "status": "not_evaluable", "reason": "x",
        "sr_daily": None, "n_daily_returns": None, "skew": None, "kurtosis": None}))
    ev = _evaluate(run_dir)
    _assert_dsr_not_evaluable(ev, "ledger_stats_mismatch")
    assert "['status']" in _dsr_row(ev)["not_evaluable_reason"]


def test_candidate_error_block_is_not_evaluable_with_the_blocks_reason():
    """A transient OSError when P1 read the CSV: the ledger row says error. A
    normal run can hit it -- it must not raise out of grading (every --resume
    would re-spend and hit it again)."""
    run_dir = _v2_run()
    _edit_rows(lambda rows: _own_in(rows).update(whole_test={
        "basis": pwt.WHOLE_TEST_BASIS, "status": "error", "reason": "OSError: gone",
        "sr_daily": None, "n_daily_returns": None, "skew": None, "kurtosis": None}))
    ev = _evaluate(run_dir)
    _assert_dsr_not_evaluable(ev, "OSError: gone")
    assert _rows(ev)["sharpe_min"]["actual"] is not None
    assert ev["dsr_basis"]["n_same_basis"] == 0  # the errored row is not in K ...
    assert ev["dsr_basis"]["n_dsr_total"] == rpr._promotion_dsr_context()["n_dsr_total"]  # ... N is


def test_dedup_collapse_onto_an_earlier_blockless_row_is_not_evaluable_and_named():
    """An earlier backtest row with the candidate's forecast_hash and source
    (no block) survives dedup; the candidate's own row collapses onto it (a
    retest of the same config on another protocol). Its DSR reads NOT_EVALUABLE
    naming the earlier trial -- not a raise, and not a DSR graded on a sample
    that silently lacks the candidate."""
    run_dir = _v2_run()
    _edit_rows(lambda rows: rows.insert(0, {
        "trial_id": "run_100", "source": "backtest", "statistic_valid": "sharpe",
        "sharpe": 0.2, "forecast_hash": _own_in(rows)["forecast_hash"]}))
    wctx = rpr._whole_test_dsr_context()
    assert all(x["trial_id"] != RUN_ID for x in wctx["sample"]["rows"])  # the silent drop
    ev = _evaluate(run_dir)
    row = _assert_dsr_not_evaluable(ev, "dedup_collapse")
    assert "'run_100'" in row["not_evaluable_reason"]
    assert _rows(ev)["sharpe_min"]["actual"] is not None


def test_dedup_collapse_onto_an_earlier_ok_block_row_is_not_evaluable_and_k_unchanged():
    """The earlier row carries an ok block, so it IS in the sample (K counts it
    once); the candidate is not. NOT_EVALUABLE, K/N as the ledger says."""
    run_dir = _v2_run()
    fh = _own_in(_state()["trial_sharpes"])["forecast_hash"]
    _edit_rows(lambda rows: rows.insert(0, {
        "trial_id": "run_100", "source": "backtest", "statistic_valid": "sharpe",
        "sharpe": 0.2, "forecast_hash": fh, "whole_test": _block(0.04)}))
    ev = _evaluate(run_dir)
    row = _assert_dsr_not_evaluable(ev, "dedup_collapse")
    assert "'run_100'" in row["not_evaluable_reason"]
    assert row["detail"]["K"] == ev["dsr_basis"]["n_same_basis"] == 1
    assert row["detail"]["N"] == ev["dsr_basis"]["n_dsr_total"]


def _two_variant_run() -> Path:
    """Two graded per-coin variants (base, design) of one run, each with its own
    ledger row (trial ids `<run>:base`, `<run>:design`) and whole_test block."""
    from test_profit_bars_every_backtest import VARIANT_LOOP_ON
    _set_orchestrator({**V2_ON, **VARIANT_LOOP_ON})
    _write_bars(V2_BARS)
    _write_cost_model()
    run_dir = _seed(variant_loop=True)
    arts = run_dir / "artifacts"
    vids = ["base", "design"]
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {
        v: {"status": "validated", "config_path": f"artifacts/variants/{v}/strategy_config.json"}
        for v in vids}})
    prs = {}
    for v in vids:
        prs[f"{RUN_ID}:{v}"] = _build(run_dir / "variants" / v)
        rpr.save_yaml(arts / "variants" / v / "protocol_result.yaml", prs[f"{RUN_ID}:{v}"])
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, {"campaign_id": "t", "runs": [], "trial_sharpes": [
        {"trial_id": f"{RUN_ID}:{v}", "source": "backtest", "sharpe": 0.3,
         "forecast_hash": f"fh-{v}"} for v in vids]})
    _seed_dsr_ledger()
    _attach_whole_test(run_dir, prs)
    return run_dir


def test_one_variants_dsr_not_evaluable_leaves_the_other_variants_graded_normally():
    """Two canonically identical variants (same forecast_hash): the later one
    collapses onto the earlier under dedup. ITS DSR is NOT_EVALUABLE naming the
    earlier trial; the other variant is graded exactly as it is without the
    collision, and the stage does not raise."""
    run_dir = _two_variant_run()
    clean = _evaluate(run_dir)
    assert _dsr_row(clean, "base")["result"] != "NOT_EVALUABLE"
    assert _dsr_row(clean, "design")["result"] != "NOT_EVALUABLE"

    _edit_rows(lambda rows: _own_in(rows, f"{RUN_ID}:design").update(
        forecast_hash=_own_in(rows, f"{RUN_ID}:base")["forecast_hash"]))
    ev = _evaluate(run_dir)
    row = _assert_dsr_not_evaluable(ev, "dedup_collapse", "design")
    assert f"'{RUN_ID}:base'" in row["not_evaluable_reason"]
    base = _dsr_row(ev, "base")
    assert base["result"] != "NOT_EVALUABLE" and isinstance(base["actual"], float)
    assert base["detail"]["K"] == 1 and ev["dsr_basis"]["n_same_basis"] == 1
    # the surviving variant's other bars are untouched by the collision
    assert {k: v for k, v in _rows(ev, "base").items() if k != "deflated_sharpe_threshold"} == {
        k: v for k, v in _rows(clean, "base").items() if k != "deflated_sharpe_threshold"}


def test_not_evaluable_candidate_reads_not_evaluable_in_lockstep(tmp_path):
    run_dir = _v2_run(protocol=False)
    assert _own_row()["whole_test"]["status"] == "not_evaluable"
    row = _dsr_row(_evaluate(run_dir))
    assert row["result"] == "NOT_EVALUABLE" and row["actual"] is None
    assert "no protocol_file" in row["not_evaluable_reason"]


# ---------------------------------------------------------------------------
# 6. The spend
# ---------------------------------------------------------------------------

def _entry(ev):
    return ev["variants"][RUN_ID]


def test_spend_recomputes_on_the_whole_test_basis():
    run_dir = _v2_run()
    ev = _evaluate(run_dir, record_bars_sha=True)
    bars = rpr._evaluation_under_current_bars(ev)
    got = rpr._dsr_on_current_ledger(run_dir, RUN_ID, _entry(ev), bars, ev)
    assert got["deflated_sharpe_ratio"] == _dsr_row(ev)["actual"]
    assert got["sharpe_basis"] == pwt.WHOLE_TEST_BASIS
    assert got["n_same_basis"] == 1 < bars["dsr_min_same_basis_trials"]  # small K: no refusal
    assert got["basis_overlay"] == {"present": False, "sha256": None}


@pytest.mark.parametrize("basis", [None, "deflated_sharpe_on_campaign_trial_ledger",
                                   "whole_test_daily_equal_weight_v0"])
def test_spend_refuses_a_sharpe_basis_mismatch(basis):
    run_dir = _v2_run()
    ev = _evaluate(run_dir, record_bars_sha=True)
    bars = rpr._evaluation_under_current_bars(ev)
    if basis is None:
        ev["dsr_basis"].pop("sharpe_basis")
    else:
        ev["dsr_basis"]["sharpe_basis"] = basis
    with pytest.raises(rpr.HoldoutUnlockRefused) as exc:
        rpr._dsr_on_current_ledger(run_dir, RUN_ID, _entry(ev), bars, ev)
    assert exc.value.code == "dsr_fails_current_ledger" and "sharpe_basis" in exc.value.detail


def test_spend_refuses_a_dsr_under_the_threshold_and_a_broken_lockstep():
    run_dir = _v2_run()
    ev = _evaluate(run_dir, record_bars_sha=True)
    bars = rpr._evaluation_under_current_bars(ev)
    with pytest.raises(rpr.HoldoutUnlockRefused) as exc:
        rpr._dsr_on_current_ledger(run_dir, RUN_ID, _entry(ev),
                                   {**bars, "deflated_sharpe_threshold": 1.01}, ev)
    assert exc.value.code == "dsr_fails_current_ledger"
    _edit_rows(lambda rows: _own_in(rows)["whole_test"].update(skew=0.5))
    with pytest.raises(rpr.HoldoutUnlockRefused) as exc:
        rpr._dsr_on_current_ledger(run_dir, RUN_ID, _entry(ev), bars, ev)
    # a moved ledger row is a NOT_EVALUABLE DSR (no number), refused with its reason
    assert exc.value.code == "dsr_fails_current_ledger"
    assert "ledger_stats_mismatch" in exc.value.detail


def test_spend_turns_a_malformed_yaml_overlay_into_the_classified_refusal():
    run_dir = _v2_run()
    ev = _evaluate(run_dir, record_bars_sha=True)
    bars = rpr._evaluation_under_current_bars(ev)
    rpr.TRIAL_SHARPE_BASIS_OVERLAY_PATH.write_text("entries: [unclosed\n  - {", encoding="utf-8")
    with pytest.raises(rpr.HoldoutUnlockRefused) as exc:
        rpr._dsr_on_current_ledger(run_dir, RUN_ID, _entry(ev), bars, ev)
    assert exc.value.code == "dsr_fails_current_ledger"
    assert "cannot be reproduced" in exc.value.detail


# ---------------------------------------------------------------------------
# 7. Review item (c): decide_next's R1 re-fire needs no K rule
# ---------------------------------------------------------------------------

def _classify(ev, ledger_basis):
    base = "comp-1"
    not_eval = sorted({b["name"] for v in ev["variants"].values() for b in v["bars"]
                       if b["result"] == "NOT_EVALUABLE"})
    comp_inputs = {"failures": [], "dsr_basis": ledger_basis,
                   "inconclusive": {base: {"not_evaluable": not_eval,
                                           "dsr_basis": ev["dsr_basis"]}}}
    entries = [{"id": base, "status": "done", "outcome": "inconclusive"}]
    return decide_next._classify_block_set(base, "h", entries, comp_inputs), not_eval


def test_dsr_not_evaluable_only_with_the_candidates_own_sharpe_so_r1_does_not_refire():
    run_dir = _v2_run(protocol=False)
    ev = _evaluate(run_dir)
    (status, _eid, _why), not_eval = _classify(ev, {"n_dsr_total": 50, "n_trials": 50})
    assert {"deflated_sharpe_threshold", "sharpe_min"} <= set(not_eval)
    assert status == "fired_before"


def test_whole_test_dsr_only_not_evaluable_is_fired_before_not_a_missing_input():
    """Review fix 4: a whole-test evaluation (dsr_basis carries sharpe_basis)
    that is inconclusive on the DSR alone (here a dedup collapse) is
    `fired_before` whatever the legacy n_trials count says -- the legacy
    _dsr_computable rule (n_trials >= 2 at grading, ledger now has more) must
    not re-fire it."""
    run_dir = _v2_run()
    _edit_rows(lambda rows: rows.insert(0, {
        "trial_id": "run_100", "source": "backtest", "statistic_valid": "sharpe",
        "sharpe": 0.2, "forecast_hash": _own_in(rows)["forecast_hash"]}))
    ev = _evaluate(run_dir)
    assert _dsr_row(ev)["result"] == "NOT_EVALUABLE"
    ev["dsr_basis"] = {**ev["dsr_basis"], "n_trials": 1}  # the legacy count below its floor
    (status, _eid, why), not_eval = _classify(ev, {"n_dsr_total": 50, "n_trials": 50})
    assert not_eval == ["deflated_sharpe_threshold"]
    assert status == "fired_before" and "whole-test" in why
    # the legacy basis (no sharpe_basis) is unchanged: it re-fires when the ledger grew
    legacy = {k: v for k, v in ev["dsr_basis"].items() if k != "sharpe_basis"}
    (status, _eid, _why), _ = _classify({**ev, "dsr_basis": legacy},
                                        {"n_dsr_total": 50, "n_trials": 50})
    assert status == "eligible"


def test_small_k_never_makes_the_dsr_not_evaluable():
    run_dir = _v2_run()
    ev = _evaluate(run_dir)
    assert ev["dsr_basis"]["n_same_basis"] < ev["dsr_basis"]["min_same_basis"]
    assert _dsr_row(ev)["result"] != "NOT_EVALUABLE"


# ---------------------------------------------------------------------------
# 8. The composition grid's grader follows branch 3
# ---------------------------------------------------------------------------

def test_grid_grader_grades_the_whole_test_dsr_like_branch_3():
    from test_profit_bars_every_backtest import VARIANT_LOOP_ON
    _set_orchestrator({**V2_ON, **VARIANT_LOOP_ON})
    _write_bars(V2_BARS)
    _write_cost_model()
    run_dir = _seed(variant_loop=True)
    arts = run_dir / "artifacts"
    vids = ["base", "design"]
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {
        v: {"status": "validated", "config_path": f"artifacts/variants/{v}/strategy_config.json"}
        for v in vids}})
    prs = {}
    for v in vids:
        prs[f"{RUN_ID}:{v}"] = _build(run_dir / "variants" / v)
        rpr.save_yaml(arts / "variants" / v / "protocol_result.yaml", prs[f"{RUN_ID}:{v}"])
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, {"campaign_id": "t", "runs": [], "trial_sharpes": [
        {"trial_id": f"{RUN_ID}:{v}", "source": "backtest", "sharpe": 0.3,
         "forecast_hash": f"fh-{v}"} for v in vids]})
    _seed_dsr_ledger()
    _attach_whole_test(run_dir, prs)
    cell = rpr._profit_bars_grid_grader(run_dir, RUN_ID)("base")
    dsr = {r["name"]: r for r in cell["bars"]}["deflated_sharpe_threshold"]
    ev = _evaluate(run_dir)
    assert dsr["basis"] == DSR_BASIS and dsr == _dsr_row(ev, "base")
    assert ev == _pbe(run_dir)
