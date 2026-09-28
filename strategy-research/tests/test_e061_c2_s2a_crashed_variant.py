"""
E-061 C2 S2a -- a variant without a graded result can never validate an idea
(D-015; C2_S1_FINDINGS.md C2.4, guesses G11 and G15), plus the review round's
fixes. The joined-up case lives in test_e061_end_to_end_wiring.py
(test_c2_4_one_crashed_variant_never_validates).

Design (review round): the grid's `variants` / `grid` hold GRADED columns only; a
variant refused or failed in protocol_execution is listed ONLY in the top-level
`failed_variants` {vid: reason}, the reason prefixed `refused:` (no data touched,
no trial row) or `backtest_failed:` (a spent look); every other variant of the idea
without a graded column in this run (REPEAT skip, data-gate decline, 5a refusal) is
in `untested_variants`. Either one non-empty makes the idea at best inconclusive; a
genuine FAIL still refutes (D-014).

  1. The grid (tools/verdict_criteria_evaluator.py::evaluate_grid) and the one
     shared validator (check_failed_variants / grid_failed_variants).
  2. The variant loop (run_phase1_research.run_tool_worker, protocol_execution):
     crash / refusal prefixes, the re-run bypass (failed_attempt persisted in
     index.yaml), the repeat-gate case (whole idea in one run), a base whose
     trial write failed never feeds the singular artifacts.
  3. Branch 3 (_profit_bars_backtest_candidates): a failed variant is NOT_TESTED
     (crashed: its backtest_failed trial_id; refused: null); malformed input
     raises; D-021 -- the graded survivors of an inconclusive idea are still graded.
  4. Campaign memory (tools/campaign_memory.py): crashed -> `failed`, refused ->
     `not_tested`; corrupt failed_variants raises; decide_next / novelty.
"""
import asyncio
import json
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
import campaign_memory as cm  # noqa: E402
import decide_next as dn  # noqa: E402
import novelty as nov  # noqa: E402
import protocol_refusal  # noqa: E402

from test_grid_evaluation import (  # noqa: E402
    _protocol_result, _windows_for_reducer, _menu_shaped_pre_reg)
from test_e033_slice4a_variant_loop import _set_flag, _summary_for  # noqa: E402
from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402
from test_profit_bars_every_backtest import (  # noqa: E402
    FULL_ON, VARIANT_LOOP_ON, RUN_ID, _variant_run, _write_bars, _grid, _memory,
    _set_orchestrator, _SCHEMA)

CRASH = "backtest_failed: run_protocol.py non-zero exit (1)"
REFUSED = "refused: run_protocol.py refused before any backtest (no data touched): x"
PASS_CRIT = {"id": "c1", "metric": "net_return_pct", "source": "window", "reducer": "median",
             "comparator": ">", "threshold": 0.0, "floor": {"min_windows": 1}}
VIDS = ("asset_v2", "base", "design_v2")


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _good():
    return _protocol_result(_windows_for_reducer([1.0, 2.0, 3.0]))


def _bad():
    return _protocol_result(_windows_for_reducer([-1.0, -2.0, -3.0]))


# ---------------------------------------------------------------------------
# 1. The grid and the shared validator
# ---------------------------------------------------------------------------

def test_two_passing_survivors_and_one_crashed_variant_is_inconclusive():
    pre = _menu_shaped_pre_reg([PASS_CRIT])
    survivors = vce.evaluate_grid({"base": _good(), "design": _good()}, pre, {}, {})
    assert survivors["idea_status"] == "validated"  # the survivors alone would validate
    res = vce.evaluate_grid({"base": _good(), "design": _good()}, pre, {}, {},
                            failed_variants={"asset": CRASH})
    assert res["idea_status"] == "inconclusive"
    assert res["variants"] == ["base", "design"]  # graded columns only
    assert res["grid"] == survivors["grid"]       # no column, no cell for the failed one
    assert res["failed_variants"] == {"asset": CRASH}
    assert "failed their backtest" in res["reason"] and "D-015" in res["reason"]
    assert "refused" not in res["reason"]


def test_a_refused_variant_is_worded_as_a_refusal():
    res = vce.evaluate_grid({"base": _good()}, _menu_shaped_pre_reg([PASS_CRIT]), {}, {},
                            failed_variants={"asset": REFUSED, "design": CRASH})
    assert res["idea_status"] == "inconclusive"
    assert "['asset'] were refused before any backtest (no data touched" in res["reason"]
    assert "['design'] failed their backtest" in res["reason"]


def test_a_genuine_fail_on_a_survivor_still_refutes():
    """D-014: FAIL dominates a variant without a graded result."""
    pre = _menu_shaped_pre_reg([PASS_CRIT])
    res = vce.evaluate_grid({"base": _bad()}, pre, {}, {}, failed_variants={"asset": CRASH},
                            untested_variants={"design": "repeat: exact match"})
    assert res["idea_status"] == "refuted"
    assert res["variants"] == ["base"]


def test_no_grader_runs_for_a_failed_variant(monkeypatch):
    graded, profit = [], []
    real = vce._evaluate_grid_cell

    def _spy(crit, pr, eras, composition_runs=False):
        graded.append(id(pr))
        return real(crit, pr, eras, composition_runs=composition_runs)
    monkeypatch.setattr(vce, "_evaluate_grid_cell", _spy)
    pre = _menu_shaped_pre_reg([PASS_CRIT, {"id": "profit_bars", "source": "profit_bars",
                                            "reducer": "all_pass"}])

    def _grader(vid):
        profit.append(vid)
        return {"result": "PASS", "bars": [{"name": "sharpe_min", "result": "PASS"}],
                "reasons": []}
    res = vce.evaluate_grid({"base": _good()}, pre, {}, {}, composition_runs=True,
                            profit_bars_grader=_grader, failed_variants={"asset": CRASH})
    assert len(graded) == 1 and profit == ["base"]
    assert all("asset" not in row for row in res["grid"].values())
    assert res["idea_status"] == "inconclusive"


def test_an_untested_variant_keeps_the_idea_inconclusive():
    """Card D: unanimity is judged within one run -- a variant of the idea
    with no graded column here (a REPEAT skip) blocks `validated`."""
    pre = _menu_shaped_pre_reg([PASS_CRIT])
    res = vce.evaluate_grid({"asset": _good()}, pre, {}, {},
                            untested_variants={"base": "repeat: exact match of run_1:base",
                                               "design": "repeat: exact match of run_1:design"})
    assert res["idea_status"] == "inconclusive"
    assert res["variants"] == ["asset"] and "failed_variants" not in res
    assert sorted(res["untested_variants"]) == ["base", "design"]
    assert "all its variants are graded in one run" in res["reason"]


@pytest.mark.parametrize("kw", [{"failed_variants": None}, {"failed_variants": {}},
                                {"untested_variants": None}, {"untested_variants": {}}])
def test_no_failed_or_untested_variant_is_byte_identical(kw):
    pre = _menu_shaped_pre_reg([PASS_CRIT])
    today = vce.evaluate_grid({"base": _good(), "design": _bad()}, pre, {}, {})
    got = vce.evaluate_grid({"base": _good(), "design": _bad()}, pre, {}, {}, **kw)
    assert yaml.safe_dump(got) == yaml.safe_dump(today)
    assert "failed_variants" not in got and "untested_variants" not in got


@pytest.mark.parametrize("failed,match", [
    ({"base": CRASH}, "both graded"),
    ({"asset": ""}, "non-empty strings"),
    ({"asset": None}, "non-empty strings"),
    ({"asset": "run_protocol.py crashed"}, "must start with one of"),
    (["asset"], "non-empty"),
    ([], "non-empty"),
    ("", "non-empty"),
])
def test_malformed_failed_variants_raise(failed, match):
    with pytest.raises(ValueError, match=match):
        vce.evaluate_grid({"base": _good()}, _menu_shaped_pre_reg([PASS_CRIT]), {}, {},
                          failed_variants=failed)


def test_untested_overlapping_a_graded_or_failed_variant_raises():
    pre = _menu_shaped_pre_reg([PASS_CRIT])
    for untested in ({"base": "x"}, {"asset": "x"}):
        with pytest.raises(ValueError, match="both graded"):
            vce.evaluate_grid({"base": _good()}, pre, {}, {}, failed_variants={"asset": CRASH},
                              untested_variants=untested)


@pytest.mark.parametrize("value", [[], "", None, {}, ["asset"]])
def test_grid_failed_variants_refuses_a_present_but_empty_value(value):
    """The shared reader: absent -> {}; present -> must be a real mapping."""
    assert vce.grid_failed_variants({"variants": ["base"]}) == {}
    with pytest.raises(ValueError, match="non-empty"):
        vce.grid_failed_variants({"variants": ["base"], "failed_variants": value})


# ---------------------------------------------------------------------------
# 2. The variant loop
# ---------------------------------------------------------------------------

def _write_index(run_dir: Path, variants: dict | None = None) -> None:
    """The three-variant idea (base / design / asset), all validated unless
    `variants` overrides an entry."""
    vdir = run_dir / "artifacts" / "variants"
    index = {}
    for vid in VIDS:
        (vdir / vid).mkdir(parents=True, exist_ok=True)
        (vdir / vid / "strategy_config.json").write_text(json.dumps({"variant": vid}),
                                                          encoding="utf-8")
        index[vid] = {"status": "validated",
                      "config_path": f"artifacts/variants/{vid}/strategy_config.json"}
    index.update(variants or {})
    rpr.save_yaml(vdir / "index.yaml", {"variants": index})


def _setup_run(run_id: str, variants: dict | None = None) -> Path:
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True},
                         "variant_loop": {"enabled": True},
                         "grid_evaluation": {"enabled": True}})
    _write_protocol(rpr.ROOT, f"{run_id}.json")
    run_dir = _minimal_run(rpr.ROOT, run_id)
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, {"protocol_ref": f"protocols/{run_id}.json"})
    _write_index(run_dir, variants)
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml",
                  _menu_shaped_pre_reg([{**PASS_CRIT, "metric": "sharpe"}]))
    return run_dir


def _attempt(monkeypatch, run_id: str, *, crash=(), refuse=()):
    """One protocol_execution attempt: variants in `crash` exit non-zero after
    touching data, variants in `refuse` exit EXIT_NO_DATA_TOUCHED with the token;
    every other variant succeeds with a passing summary tagged by its id."""
    def _run(cmd, *a, **k):
        vid = Path(cmd[2]).parent.name
        out = Path(cmd[cmd.index("--out-dir") + 1])
        out.mkdir(parents=True, exist_ok=True)

        class _R:
            returncode, stdout, stderr = 0, "", ""
        if vid in refuse:
            _R.returncode = protocol_refusal.EXIT_NO_DATA_TOUCHED
            _R.stderr = f"{protocol_refusal.NO_DATA_TOUCHED_TOKEN}: x -- refusing.\n"
            return _R()
        if vid in crash:
            _R.returncode, _R.stderr = 1, "boom"
            return _R()
        summary = _summary_for(vid)
        summary["results"] = _windows_for_reducer([1.0, 2.0, 3.0])
        for r in summary["results"]:
            r["core"]["sharpe"] = 1.0
        (out / "protocol_summary.json").write_text(json.dumps(summary), encoding="utf-8")
        return _R()
    monkeypatch.setattr(rpr.subprocess, "run", _run)
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))


def _grid_of(run_dir):
    return rpr.load_yaml(run_dir / "artifacts" / "grid_evaluation.yaml")


def _index_of(run_dir):
    return rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"]


def _rows(run_id):
    return sorted((t["trial_id"], t["source"]) for t in rpr.load_campaign_state()["trial_sharpes"]
                  if t["trial_id"].startswith(f"{run_id}:"))


def test_variant_loop_records_the_crashed_variant_in_failed_variants_only(monkeypatch):
    run_dir = _setup_run("run_941")
    _attempt(monkeypatch, "run_941", crash={"design_v2"})
    grid = _grid_of(run_dir)
    assert grid["failed_variants"] == {"design_v2": CRASH}
    assert grid["variants"] == ["asset_v2", "base"]
    assert all("design_v2" not in row for row in grid["grid"].values())
    assert grid["idea_status"] == "inconclusive" and "untested_variants" not in grid
    assert rpr.load_yaml(run_dir / "artifacts" / "idea_status.yaml")["idea_status"] == "inconclusive"
    assert _rows("run_941") == [("run_941:asset_v2", "backtest"), ("run_941:base", "backtest"),
                                ("run_941:design_v2", "backtest_failed")]
    idx = _index_of(run_dir)
    assert idx["design_v2"]["failed_attempt"] == CRASH and idx["design_v2"]["status"] == "validated"
    assert "failed_attempt" not in idx["base"]


def test_variant_loop_keeps_a_refusal_apart_from_a_crash(monkeypatch):
    run_dir = _setup_run("run_943")
    _attempt(monkeypatch, "run_943", crash={"design_v2"}, refuse={"asset_v2"})
    grid = _grid_of(run_dir)
    assert grid["failed_variants"]["asset_v2"].startswith("refused: run_protocol.py refused")
    assert grid["failed_variants"]["design_v2"] == CRASH
    assert grid["variants"] == ["base"]
    assert "['asset_v2'] were refused before any backtest" in grid["reason"]
    assert "['design_v2'] failed their backtest" in grid["reason"]
    # no trial row for the refusal, one backtest_failed row for the crash
    assert _rows("run_943") == [("run_943:base", "backtest"),
                                ("run_943:design_v2", "backtest_failed")]
    idx = _index_of(run_dir)
    assert idx["asset_v2"]["status"] == "not_tested"
    assert idx["asset_v2"]["failed_attempt"] == grid["failed_variants"]["asset_v2"]


def test_variant_loop_without_a_failure_validates_and_writes_no_extra_key(monkeypatch):
    run_dir = _setup_run("run_942")
    index_before = (run_dir / "artifacts" / "variants" / "index.yaml").read_bytes()
    _attempt(monkeypatch, "run_942")
    grid = _grid_of(run_dir)
    assert "failed_variants" not in grid and "untested_variants" not in grid
    assert grid["idea_status"] == "validated"
    assert (run_dir / "artifacts" / "variants" / "index.yaml").read_bytes() == index_before


def test_rerun_keeps_a_variant_refused_on_an_earlier_attempt(monkeypatch):
    """The reviewer's scenario: attempt 1 -- asset refused, base and design crash
    (all failed, protocol_execution raises); resume -- base and design succeed.
    The refused asset is not re-run (not_tested) yet must stay counted: the idea
    is NOT validated."""
    run_dir = _setup_run("run_944")
    with pytest.raises(RuntimeError, match="all 3 validated variant"):
        _attempt(monkeypatch, "run_944", crash={"base", "design_v2"}, refuse={"asset_v2"})
    idx = _index_of(run_dir)
    assert idx["asset_v2"]["failed_attempt"].startswith("refused:")
    assert idx["base"]["failed_attempt"] == idx["design_v2"]["failed_attempt"] == CRASH

    _attempt(monkeypatch, "run_944")  # resume: only base and design are validated
    grid = _grid_of(run_dir)
    assert grid["variants"] == ["base", "design_v2"]
    assert list(grid["failed_variants"]) == ["asset_v2"]
    assert grid["failed_variants"]["asset_v2"].startswith("refused:")
    assert grid["idea_status"] == "inconclusive"
    idx = _index_of(run_dir)
    assert "failed_attempt" not in idx["base"] and "failed_attempt" not in idx["design_v2"]
    assert idx["asset_v2"]["failed_attempt"].startswith("refused:")
    # the attempt-1 looks stay counted next to the attempt-2 backtests
    assert _rows("run_944") == [("run_944:base", "backtest"), ("run_944:base", "backtest_failed"),
                                ("run_944:design_v2", "backtest"),
                                ("run_944:design_v2", "backtest_failed")]


def test_rerun_that_regrades_the_crashed_variant_clears_it(monkeypatch):
    run_dir = _setup_run("run_945")
    _attempt(monkeypatch, "run_945", crash={"asset_v2"})
    assert _grid_of(run_dir)["idea_status"] == "inconclusive"
    _attempt(monkeypatch, "run_945")  # the crashed variant is re-run and succeeds
    grid = _grid_of(run_dir)
    assert "failed_variants" not in grid and grid["idea_status"] == "validated"
    assert all("failed_attempt" not in v for v in _index_of(run_dir).values())


def test_repeat_skipped_variants_keep_the_idea_inconclusive(monkeypatch):
    """Run 1's asset crashed; run 2 re-runs only the asset (base and design are
    exact REPEATs of run 1, skipped by the gate) and it PASSes. The earlier
    graded results live in the memory, but unanimity is judged within one run:
    run 2 stays inconclusive."""
    run_1 = _setup_run("run_946")
    _attempt(monkeypatch, "run_946", crash={"asset_v2"})
    assert _grid_of(run_1)["idea_status"] == "inconclusive"
    repeat = {vid: {"status": "not_tested",
                    "config_path": f"artifacts/variants/{vid}/strategy_config.json",
                    "reason": f"{rpr._REPEAT_REASON_PREFIX} exact match of tested run_946:{vid}"}
              for vid in ("base", "design_v2")}
    run_2 = _setup_run("run_947", repeat)
    _attempt(monkeypatch, "run_947")
    grid = _grid_of(run_2)
    assert grid["variants"] == ["asset_v2"]
    assert all(row["asset_v2"]["result"] == "PASS" for row in grid["grid"].values())
    assert grid["idea_status"] == "inconclusive"
    assert "failed_variants" not in grid
    assert sorted(grid["untested_variants"]) == ["base", "design_v2"]
    assert grid["untested_variants"]["base"].startswith(rpr._REPEAT_REASON_PREFIX)


def test_a_base_whose_trial_write_failed_never_feeds_the_singular_artifacts(monkeypatch):
    run_dir = _setup_run("run_948")
    real_record = rpr._record_backtest_trial

    def _record(run_id, summary, config_path, *, trial_id):
        if trial_id.endswith(":base"):
            raise OSError("ledger unwritable")
        return real_record(run_id, summary, config_path, trial_id=trial_id)
    monkeypatch.setattr(rpr, "_record_backtest_trial", _record)
    seen = []
    real_c7 = vce.evaluate_pass_rule_criteria

    def _c7(summary, *a, **k):
        seen.append(summary["config_sha256"])
        return real_c7(summary, *a, **k)
    monkeypatch.setattr(vce, "evaluate_pass_rule_criteria", _c7)
    _attempt(monkeypatch, "run_948")
    grid = _grid_of(run_dir)
    assert grid["failed_variants"] == {
        "base": "backtest_failed: the backtest completed but its trial write raised OSError"}
    assert grid["variants"] == ["asset_v2", "design_v2"]
    # C7 and the singular bridge file (read by the category reports) come from
    # the first GRADED variant, never from base
    assert seen == ["sha-asset_v2"]
    singular = rpr.load_yaml(run_dir / "artifacts" / "protocol_result.yaml")
    assert singular["config_sha256"] == "sha-asset_v2"
    assert ("run_948:base", "backtest_failed") in _rows("run_948")


# ---------------------------------------------------------------------------
# 3. Branch 3 and 4. memory
# ---------------------------------------------------------------------------

def _failed_run(stale_good: bool = False, refused_asset: bool = False) -> Path:
    """`base` graded (all PASS); `broken` crashed (validated, a backtest_failed
    row) -- listed in failed_variants, never a column, with a stale passing
    protocol_result.yaml left on disk when stale_good; with refused_asset,
    `asset` was refused before any backtest (not_tested, no trial row)."""
    run_dir = _variant_run({"base": True}, stale={"good": True} if stale_good else None)
    arts = run_dir / "artifacts"
    failed = {"broken": CRASH}
    if refused_asset:
        index = rpr.load_yaml(arts / "variants" / "index.yaml")
        index["variants"]["asset"] = {"status": "not_tested", "reason": REFUSED[len("refused: "):],
                                      "config_path": "artifacts/variants/asset/strategy_config.json",
                                      "failed_attempt": REFUSED}
        rpr.save_yaml(arts / "variants" / "index.yaml", index)
        failed["asset"] = REFUSED
    grid = _grid(["base"], "validated")
    grid.update(failed_variants=failed, idea_status="inconclusive",
                reason="every criterion PASSed on every graded variant, but not every variant "
                       "was graded; " + vce._failed_variants_reason(failed))
    rpr.save_yaml(arts / "grid_evaluation.yaml", grid)
    rpr.save_yaml(arts / "idea_status.yaml", rpr._build_idea_status_artifact(grid, RUN_ID))
    return run_dir


def test_branch3_crashed_variant_is_not_tested_with_its_trial_id():
    _set_orchestrator({**FULL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _failed_run(stale_good=True)
    assert (run_dir / "artifacts" / "variants" / "broken" / "protocol_result.yaml").exists()
    cands = rpr._profit_bars_backtest_candidates(run_dir, RUN_ID)
    b = cands["broken"]
    assert b["result"] == "NOT_TESTED" and b["protocol_result"] is None
    assert b["trial_id"] == f"{RUN_ID}:broken"  # its real backtest_failed row
    assert b["reason"].startswith("backtest failed (") and CRASH in b["reason"]
    ev = rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    assert ev["variants"]["broken"]["result"] == "NOT_TESTED" and ev["variants"]["broken"]["bars"] == []
    assert ev["variants"]["broken"]["trial_id"] == f"{RUN_ID}:broken"
    assert "broken" not in ev["passing"]


def test_branch3_refused_variant_is_not_tested_without_a_trial_id():
    _set_orchestrator({**FULL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _failed_run(refused_asset=True)
    a = rpr._profit_bars_backtest_candidates(run_dir, RUN_ID)["asset"]
    assert a["result"] == "NOT_TESTED" and a["trial_id"] is None
    assert a["reason"].startswith("refused before any backtest, no data touched")


def test_branch3_grades_the_survivors_of_an_inconclusive_idea():
    """D-021: grid status is not a holdout precondition -- base passes every bar
    although the idea is inconclusive (a crashed variant), and branch 3 says so."""
    _set_orchestrator({**FULL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _failed_run()
    assert rpr.load_yaml(run_dir / "artifacts" / "idea_status.yaml")["idea_status"] == "inconclusive"
    ev = rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    assert ev["variants"]["base"]["result"] == "PASS"
    assert ev["passing"] == ["base"] and ev["result"] == "PASS"


@pytest.mark.parametrize("value,match", [
    ({"ghost": CRASH}, "not in"),
    ({"base": CRASH}, "both graded"),
    ({"broken": "crashed"}, "must start with one of"),
    ([], "non-empty"), ("", "non-empty"), (None, "non-empty"),
])
def test_branch3_refuses_a_malformed_failed_variants(value, match):
    _set_orchestrator({**FULL_ON, **VARIANT_LOOP_ON})
    run_dir = _failed_run()
    path = run_dir / "artifacts" / "grid_evaluation.yaml"
    grid = rpr.load_yaml(path)
    grid["failed_variants"] = value
    rpr.save_yaml(path, grid)
    with pytest.raises(ValueError, match=match):
        rpr._profit_bars_backtest_candidates(run_dir, RUN_ID)


def test_memory_records_crashed_as_failed_and_refused_as_not_tested():
    _set_orchestrator({**FULL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _failed_run(stale_good=True, refused_asset=True)
    rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    rpr._run_regroup_record_stage(RUN_ID, run_dir, profit_bars_evaluated=True)
    doc = _memory()
    e = doc["runs"][RUN_ID]
    assert e["idea_status"] == "inconclusive"
    assert e["variants"]["broken"]["status"] == "failed"
    assert e["variants"]["broken"]["reason"] == CRASH
    assert e["variants"]["broken"]["trial_id"] == f"{RUN_ID}:broken"  # its backtest_failed row
    assert e["variants"]["asset"]["status"] == "not_tested"
    assert e["variants"]["asset"]["reason"] == REFUSED and e["variants"]["asset"]["trial_id"] is None
    assert e["variants"]["base"]["status"] == "tested"
    assert e["grid"]["variants"] == ["base"]
    assert all(set(row) == {"base"} for row in e["grid"]["cells"].values())
    assert e["profit_bars"]["variants"]["broken"]["result"] == "NOT_TESTED"
    assert e["registry"] == {"skipped": cm.REGISTRY_SKIPPED_NOT_VALIDATED}
    jsonschema.Draft202012Validator(_SCHEMA).validate(doc)
    # the downstream readers of that status: novelty never sees it as tested
    assert [(r, v) for r, v, _e, _v in nov._tested_variants(doc)] == [(RUN_ID, "base")]


def test_decide_next_sees_a_crashed_base_as_not_tested():
    _set_orchestrator({**FULL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _variant_run({"design": True})
    arts = run_dir / "artifacts"
    index = rpr.load_yaml(arts / "variants" / "index.yaml")
    index["variants"]["base"] = {"status": "validated",
                                 "config_path": "artifacts/variants/base/strategy_config.json"}
    rpr.save_yaml(arts / "variants" / "index.yaml", index)
    grid = _grid(["design"], "validated")
    grid.update(failed_variants={"base": CRASH}, idea_status="inconclusive", reason="crashed base")
    rpr.save_yaml(arts / "grid_evaluation.yaml", grid)
    rpr.save_yaml(arts / "idea_status.yaml", rpr._build_idea_status_artifact(grid, RUN_ID))
    rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    rpr._run_regroup_record_stage(RUN_ID, run_dir, profit_bars_evaluated=True)
    e = _memory()["runs"][RUN_ID]
    vid, base = dn._base_variant(e)
    assert vid == "base" and base["status"] == "failed"  # -> source_base_variant_not_tested


@pytest.mark.parametrize("value,match", [
    ({"ghost": CRASH}, "not in the index"),
    ({"base": CRASH}, "both graded"),
    ({"broken": "crashed"}, "must start with one of"),
    ([], "non-empty"), ("", "non-empty"), (None, "non-empty"),
])
def test_memory_refuses_a_corrupt_failed_variants(value, match):
    _set_orchestrator({**FULL_ON, **VARIANT_LOOP_ON})
    run_dir = _failed_run()
    path = run_dir / "artifacts" / "grid_evaluation.yaml"
    grid = rpr.load_yaml(path)
    grid["failed_variants"] = value
    rpr.save_yaml(path, grid)
    with pytest.raises(cm.CampaignMemoryError, match=match):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
