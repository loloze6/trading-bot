"""
C5.7a (DELIVERY_REVIEW.md C11): the three artifact schemas that were never
added -- ``grid_evaluation``, ``idea_status``, ``variant_patches`` under
workflow_artifacts/schemas/.

They are wired the way every other schema in that directory is: by file stem,
through tools/workflow_artifact_validation.validate_workflow_artifact, which
run_phase1_research.save_yaml / load_yaml already call (warn-only by default,
blocking under WORKFLOW_ARTIFACT_VALIDATION=raise). Nothing in production code
changed -- dropping the schema file in is the whole wiring -- so the default
path can only ever gain a log warning, never a different result. What this file
proves is that the warning never fires for anything the writers really write:

  * REAL WRITERS, the E-061 end-to-end harness (tests/test_e061_end_to_end_
    wiring.py): the campaign runs the real setup_run, the real stages and the
    real save_yaml with only the model and the tool subprocesses stubbed. Every
    grid_evaluation / idea_status / variant_patches document that passes through
    save_yaml / load_yaml in those runs (recorded at the validation hook, so the
    intermediate rewrites and the retry attempts count too), and every such file
    left on disk, is validated. Six scenarios: the joined-up two-run campaign
    (validated + refuted grids), a crashed variant (failed_variants), a
    partial-coverage asset (partial_coverage_variants), a data-gate-declined
    asset (untested_variants), the Step-2 shape retry (two variant_patches
    outputs), and a generated protocol.
  * REAL WRITERS, called directly: vce.evaluate_grid on synthetic protocol
    results for every cell path (window reducers, sign_consistent_by_era,
    pooled, per_symbol_all, floor INCONCLUSIVE, SPEC_ERROR, profit_bars cells
    graded by the real _grade_profit_bars / _grade_profit_bars_v2 rows) and the
    failed / untested / partial-coverage keys; rpr._build_idea_status_artifact
    on each of those; tools/composition.variant_patches_from_manifest.
  * A FROZEN CORPUS (tests/fixtures/c5_7a/writer_corpus.json): the distinct
    document shapes the real writers produced across every existing test that
    touches these artifacts (37 files run with a recorder on the validation
    hook), kept so the composition-only cells (residual_ic, profit_bars v1 and
    v2, weight_schedule) stay covered without re-running those suites.

and that each schema rejects a malformed document for every required key and
enum, plus the whole-document rules JSON Schema cannot state (grid keys equal
criteria x variants, idea_status rolled up from the cells).
"""
from __future__ import annotations

import copy
import json
import logging
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
import workflow_artifact_validation as wav  # noqa: E402
import composition as comp  # noqa: E402
import test_e061_end_to_end_wiring as e061  # noqa: E402
from test_e061_end_to_end_wiring import harness  # noqa: E402,F401  (fixture)

jsonschema = pytest.importorskip("jsonschema")

_SCHEMAS = _SR / "workflow_artifacts" / "schemas"
_CORPUS = Path(__file__).resolve().parent / "fixtures" / "c5_7a" / "writer_corpus.json"
STEMS = ("grid_evaluation", "idea_status", "variant_patches")


# ---------------------------------------------------------------------------
# helpers: validate exactly the way the production hook does
# ---------------------------------------------------------------------------

def _schema(stem: str) -> dict:
    return json.loads((_SCHEMAS / f"{stem}.schema.json").read_text(encoding="utf-8"))


def _errors(stem: str, doc) -> list:
    # wav._make_validator is what validate_workflow_artifact builds (registry of
    # every sibling schema, validator class picked from the schema's $schema).
    return sorted(wav._make_validator(jsonschema, _schema(stem)).iter_errors(doc),
                  key=lambda e: list(e.absolute_path))


def _assert_valid(stem: str, doc, where: str = "") -> None:
    errs = _errors(stem, doc)
    assert not errs, f"{stem} {where}: {errs[0].message} @ {list(errs[0].absolute_path)}"


def _assert_invalid(stem: str, doc, why: str = "") -> None:
    assert _errors(stem, doc), f"{stem}: expected a violation ({why}) but the document validated"


# ---------------------------------------------------------------------------
# whole-document rules JSON Schema cannot state
# ---------------------------------------------------------------------------

def check_grid_rules(grid: dict) -> None:
    variants, criteria = grid["variants"], grid["criteria"]
    assert set(grid["grid"]) == set(criteria), "grid rows are not the criteria"
    for cid, row in grid["grid"].items():
        assert set(row) == set(variants), f"criterion {cid}: cells are not the graded variants"
    failed = grid.get("failed_variants", {})
    untested = grid.get("untested_variants", {})
    partial = grid.get("partial_coverage_variants", {})
    assert not set(failed) & set(variants), "a failed variant is also a graded column"
    assert not set(untested) & (set(variants) | set(failed)), "an untested variant is also graded/failed"
    assert set(partial) <= set(variants), "partial coverage names a variant that is not a column"
    results = [c["result"] for row in grid["grid"].values() for c in row.values()]
    if grid["result"] == "SPEC_ERROR":
        assert "SPEC_ERROR" in results and grid["idea_status"] is None
        return
    assert "SPEC_ERROR" not in results
    if "FAIL" in results:
        want = "refuted"
    elif "INCONCLUSIVE" in results or failed or untested or partial:
        want = "inconclusive"
    else:
        want = "validated"
    assert grid["idea_status"] == want, (grid["idea_status"], want)


def check_status_matches_grid(status: dict, grid: dict) -> None:
    assert status["idea_status"] == grid["idea_status"]
    assert status["reason"] == grid["reason"]
    assert status["grid_evaluation_ref"] == f"runs/{status['run_id']}/artifacts/grid_evaluation.yaml"


def check_variant_patches_rules(doc: dict) -> None:
    ids = [v["variant_id"] for v in doc["variants"]]
    assert len(ids) == len(set(ids)), "duplicate variant_id (5a raises on it)"


# ---------------------------------------------------------------------------
# 1. the wiring: same stem-keyed hook as every schema in the directory
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("stem", STEMS)
def test_schema_is_a_valid_schema_found_by_the_production_hook(stem):
    schema = _schema(stem)
    jsonschema.validators.validator_for(schema).check_schema(schema)
    assert wav._SCHEMAS_DIR / f"{stem}.schema.json" == _SCHEMAS / f"{stem}.schema.json"
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"  # the directory's draft


def test_default_mode_only_warns_and_raise_mode_blocks_the_write(tmp_path, monkeypatch, caplog):
    bad = {"run_id": "run_001", "idea_status": "maybe"}
    path = tmp_path / "idea_status.yaml"
    monkeypatch.delenv("WORKFLOW_ARTIFACT_VALIDATION", raising=False)
    with caplog.at_level(logging.WARNING, logger=wav.logger.name):
        rpr.save_yaml(path, bad)  # default: warn, never raise, the write still happens
    assert path.exists() and "workflow artifact validation failed" in caplog.text
    path.unlink()
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    with pytest.raises(jsonschema.ValidationError):
        rpr.save_yaml(path, bad)
    assert not path.exists(), "raise mode must block the write"


# ---------------------------------------------------------------------------
# 2. real writers called directly
# ---------------------------------------------------------------------------

def _window(symbol, label, **core):
    c = {"sharpe": 1.0, "net_return_pct": 1.0, "trade_count": 10, "max_drawdown_pct": -5.0,
         "win_rate": 0.5}
    c.update(core)
    return {"symbol": symbol, "window": label, "core": c}


def _protocol_result(windows, tds=None, pooled=None):
    return {"results": windows, "trade_diagnostics_summary": tds or {},
            "per_symbol_summary": {}, "hypothesis_verdict": {"diagnostics": pooled or {}}}


def _pr(values, symbol="BTCUSDT", start="2020"):
    return _protocol_result([_window(symbol, f"{start}-{i + 1:02d}", net_return_pct=v)
                             for i, v in enumerate(values)])


def _crit(cid="c1", **kw):
    base = {"id": cid, "metric": "net_return_pct", "source": "window", "reducer": "median",
            "comparator": ">", "threshold": 0.0, "floor": {"min_windows": 3, "min_trades": 10}}
    return {**base, **kw}


def _grid(pr_by_variant, criteria, **kw):
    g = vce.evaluate_grid(pr_by_variant, {"pass_rule": {"criteria": criteria}}, {}, {}, **kw)
    g["evaluated_at"] = "<evaluated_at placeholder>"  # the caller's wall-clock stamp
    return g


def _profit_grader(rows_by_variant):
    def grader(vid):
        rows, overall = rows_by_variant[vid]
        return {"result": overall, "bars": rows,
                "reasons": [f"{r['name']}: {r['result']}" for r in rows if r["result"] != "PASS"]}
    return grader


_BARS = {"sharpe_min": 0.5, "deflated_sharpe_threshold": 0.95, "max_drawdown_pct_max": 30.0,
         "trade_count_min": 100, "avg_daily_return_min": 0.0005,
         "buy_and_hold_excess_return_min": 0.0, "cost_edge_ratio_min": 2.2}


def _v1_rows(actuals: dict, portfolio=False):
    pss = {"BTCUSDT": {"max_abs_drawdown_pct": actuals.get("dd", 10.0),
                        "min_trade_count": actuals.get("tc", 150)}}
    portfolio_arg = ({"max_drawdown_pct": (actuals.get("dd"), "equal-weight worst window"),
                      "avg_daily_return": (actuals.get("adr"), "equal-weight mean"),
                      "not_evaluable_reason": "no equity files"} if portfolio else None)
    return rpr._grade_profit_bars(_BARS, sharpe=actuals.get("sharpe"), sharpe_note="s",
                                  dsr=actuals.get("dsr"), dsr_note="d", pss=pss,
                                  portfolio=portfolio_arg)


def _v2_rows(actuals: dict):
    def m(name):
        a = actuals.get(name)
        return {"actual": a, "note": f"{name} note", "detail": {"k": 1} if a is not None else {},
                "not_evaluable_reason": None if a is not None else "no value"}
    metrics = {n: m(n) for n in ("sharpe_min", "max_drawdown_pct_max", "trade_count_min",
                                 "avg_daily_return_min", "buy_and_hold_excess_return_min",
                                 "cost_edge_ratio_min")}
    return rpr._grade_profit_bars_v2(_BARS, dsr=actuals.get("dsr"), dsr_note="d", metrics=metrics)


def _direct_grids() -> dict:
    """{name: grid document} -- every cell path of evaluate_grid."""
    out = {}
    good, bad = _pr([1, 2, 3, 4, 5]), _pr([-1, -2, -3, -4, -5])
    out["all_pass"] = _grid({"v1": good, "v2": good}, [_crit("a"), _crit("b", reducer="min", threshold=0.5)])
    out["one_fail_refutes"] = _grid({"v1": good, "v2": bad}, [_crit("a")])
    out["floor_inconclusive"] = _grid({"v1": _pr([1, 2])}, [_crit("a")])
    out["single_column_run_id"] = _grid({"run_007": good}, [_crit("a")])
    out["scalar_reducers"] = _grid({"v1": good}, [
        _crit(r, reducer=r) for r in ("median", "mean", "min", "max")]
        + [_crit("frac", reducer="fraction_above", reducer_arg=0.0, comparator=">=", threshold=0.5)])
    out["sign_consistent_pass"] = _grid({"v1": _pr([1, 2, 0.5])},
                                        [_crit("sce", reducer="sign_consistent_by_era", floor={"min_windows": 1})])
    out["sign_consistent_fail"] = _grid({"v1": _protocol_result([
        _window("BTCUSDT", "2020-01", net_return_pct=1.0), _window("BTCUSDT", "2020-02", net_return_pct=2.0),
        _window("BTCUSDT", "2024-03", net_return_pct=-1.0), _window("BTCUSDT", "2024-04", net_return_pct=-2.0)])},
        [_crit("sce", reducer="sign_consistent_by_era", floor={"min_windows": 1})])
    out["sign_consistent_no_era"] = _grid({"v1": _protocol_result([_window("BTCUSDT", "2001-01", net_return_pct=1.0)])},
                                          [_crit("sce", reducer="sign_consistent_by_era", floor={"min_windows": 1})])
    out["fraction_above_no_arg_spec_error"] = _grid({"v1": good}, [_crit("f", reducer="fraction_above")])
    out["bad_comparator_spec_error"] = _grid({"v1": good}, [_crit("a", comparator="~")])
    out["bad_source_spec_error"] = _grid({"v1": good}, [_crit("a", source="nope")])
    two = _protocol_result([_window("BTCUSDT", "2020-01"), _window("BTCUSDT", "2020-02"),
                            _window("BTCUSDT", "2020-03"), _window("ETHUSDT", "2020-01"),
                            _window("ETHUSDT", "2020-02"), _window("ETHUSDT", "2020-03", net_return_pct=-9.0)])
    out["per_symbol_all"] = _grid({"v1": two}, [_crit("ps", symbol_reducer="per_symbol_all", reducer="min")])
    out["per_symbol_all_no_symbol"] = _grid({"v1": _protocol_result([{"window": "2020-01", "core": {"net_return_pct": 1.0}}] * 3)},
                                            [_crit("ps", symbol_reducer="per_symbol_all")])
    pooled = _protocol_result([_window("BTCUSDT", f"2020-{i:02d}") for i in range(1, 6)],
                              pooled={"realized_edge_to_cost_ratio": 3.0})
    out["pooled"] = _grid({"v1": pooled}, [{"id": "p", "metric": "realized_edge_to_cost_ratio", "source": "pooled",
                                             "comparator": ">", "threshold": 2.2, "floor": {"min_windows": 5}}])
    out["pooled_none_inconclusive"] = _grid({"v1": _protocol_result([_window("BTCUSDT", "2020-01")] * 5)},
                                            [{"id": "p", "metric": "missing_metric", "source": "pooled",
                                              "comparator": ">", "threshold": 1.0, "floor": {"min_windows": 1}}])
    out["failed_untested_partial"] = _grid(
        {"base": good, "design": good}, [_crit("a")],
        failed_variants={"asset": "backtest_failed: non-zero exit", "asset2": "refused: no coin"},
        untested_variants={"asset3": "data gate declined"},
        partial_coverage_variants={"design": "ran 4 of 6 windows"})
    out["only_failed"] = _grid({"base": good}, [_crit("a")], failed_variants={"x": "refused: y"})
    out["only_untested"] = _grid({"base": good}, [_crit("a")], untested_variants={"x": "repeat"})
    out["only_partial"] = _grid({"base": good}, [_crit("a")], partial_coverage_variants={"base": "4 of 6"})
    out["fail_beats_failed"] = _grid({"base": bad}, [_crit("a")], failed_variants={"x": "backtest_failed: y"})
    # composition runs: profit_bars cells graded by the real bar graders (v1, v1 portfolio, v2)
    pb = {"source": "profit_bars", "id": "profit_bars", "metric": "profit_bars"}
    ok_v1 = _v1_rows({"sharpe": 1.0, "dsr": 0.99, "dd": 10.0, "tc": 150, "adr": 0.001}, portfolio=True)
    ok_v2 = _v2_rows({"sharpe_min": 1.0, "dsr": 0.99, "max_drawdown_pct_max": 10.0, "trade_count_min": 150,
                      "avg_daily_return_min": 0.001, "buy_and_hold_excess_return_min": 0.1,
                      "cost_edge_ratio_min": 3.0})
    ne_v1 = _v1_rows({"sharpe": 1.0, "dsr": None, "dd": 10.0, "tc": 150})
    fail_v2 = _v2_rows({"sharpe_min": 0.1, "dsr": None, "max_drawdown_pct_max": 50.0, "trade_count_min": 10})
    inv = ([], "INVALIDATED")
    g = _profit_grader({"pass_v1": (ok_v1[0], ok_v1[1]),
                        "pass_v2": (ok_v2[0], ok_v2[1]), "ne_v1": (ne_v1[0], ne_v1[1]),
                        "fail_v2": (fail_v2[0], fail_v2[1]), "inv": inv})
    for name, ids in {"profit_bars_pass": ["pass_v1", "pass_v2"], "profit_bars_mixed": ["pass_v1", "ne_v1"],
                      "profit_bars_fail_v2": ["fail_v2", "pass_v2"], "profit_bars_invalidated": ["inv", "pass_v1"]}.items():
        out[name] = _grid({i: good for i in ids}, [pb], composition_runs=True, profit_bars_grader=g)
    sched_grader = lambda vid: {**g(vid), "weight_schedule": [{"from": "2020-01", "weights": {"b1": 0.5, "b2": 0.5}}]}  # noqa: E731
    out["profit_bars_weight_schedule"] = _grid({"pass_v1": good}, [pb], composition_runs=True,
                                               profit_bars_grader=sched_grader)
    return out


def test_direct_grids_cover_every_cell_result_and_validate():
    grids = _direct_grids()
    seen = {c["result"] for g in grids.values() for row in g["grid"].values() for c in row.values()}
    assert seen >= {"PASS", "FAIL", "INCONCLUSIVE", "SPEC_ERROR"}
    assert {g["idea_status"] for g in grids.values()} == {"validated", "refuted", "inconclusive", None}
    assert {g["result"] for g in grids.values()} == {"GRID_EVALUATED", "SPEC_ERROR"}
    assert any("per_symbol" in c for g in grids.values() for row in g["grid"].values() for c in row.values())
    assert any("bars" in c and c["bars"] for g in grids.values() for row in g["grid"].values() for c in row.values())
    assert any("weight_schedule" in c for g in grids.values() for row in g["grid"].values() for c in row.values())
    bar_keys = {k for g in grids.values() for row in g["grid"].values() for c in row.values()
                for b in c.get("bars", []) for k in b}
    assert {"basis", "comparator", "not_evaluable_reason", "note", "detail"} <= bar_keys  # v1 + v2 rows
    for name, g in grids.items():
        # through yaml, as save_yaml writes it and load_yaml reads it back
        rt = yaml.safe_load(yaml.safe_dump(g, sort_keys=False))
        _assert_valid("grid_evaluation", rt, name)
        check_grid_rules(rt)
        if g["idea_status"] is not None:
            status = rpr._build_idea_status_artifact(g, "run_009")
            rts = yaml.safe_load(yaml.safe_dump(status, sort_keys=False))
            _assert_valid("idea_status", rts, name)
            check_status_matches_grid(rts, rt)
        else:
            with pytest.raises(ValueError):  # the builder refuses a SPEC_ERROR grid: no artifact exists
                rpr._build_idea_status_artifact(g, "run_009")


def test_composition_variant_patches_validate():
    manifest = {"kind": "composition", "schema_version": comp.SCHEMA_VERSION, "registry_hash": "abc",
                "blocks": [{"block_id": "b1", "config_block_id": "blk_a",
                            "config_paths": ["/x/0"], "component_ids": ["c0"]},
                           {"block_id": "b2", "config_block_id": "blk_b",
                            "config_paths": ["/x/1"], "component_ids": ["c1"]}],
                "variants": {"base": {"weights": {"b1": 0.5, "b2": 0.5}},
                             "vol_scaled": {"weights": {"b1": 0.6, "b2": 0.4}},
                             "ic_weighted": {"weights": {"b1": 0.7, "b2": 0.3},
                                             "weight_schedule": [{"from": "2020-01", "weights": {"b1": 0.7, "b2": 0.3}}]}}}
    doc = comp.variant_patches_from_manifest(manifest)
    rt = yaml.safe_load(yaml.safe_dump(doc, sort_keys=False))
    _assert_valid("variant_patches", rt)
    check_variant_patches_rules(rt)
    assert [v["variant_id"] for v in rt["variants"]] == ["base", "vol_scaled", "ic_weighted"]


# ---------------------------------------------------------------------------
# 3. real writers through the E-061 end-to-end harness
# ---------------------------------------------------------------------------

@pytest.fixture
def recorded(monkeypatch):
    """Every (stem, path, deep copy of the document) that save_yaml / load_yaml hand
    to the validation hook while a scenario runs."""
    rec = []
    real = rpr.validate_workflow_artifact

    def hook(path, data):
        if Path(path).stem in STEMS:
            rec.append((Path(path).stem, str(path), copy.deepcopy(data)))
        return real(path, data)

    monkeypatch.setattr(rpr, "validate_workflow_artifact", hook)
    return rec


_SCENARIOS = {
    "test_end_to_end_two_runs_with_the_real_run_setup": {"grid": 2, "failed": False},
    "test_c2_4_one_crashed_variant_never_validates": {"grid": 1, "failed": True},
    "test_c2_s2b_partial_coverage_asset_is_untested_and_blocks_nothing": {"grid": 1, "untested": True},
    "test_c2_s2b_layer2_declined_asset_blocks_nothing": {"grid": 1, "untested": True},
    "test_c2_5_invalid_shape_retries_once_then_the_run_proceeds": {"grid": 1, "patches_min": 2},
    "test_c5_6_generated_protocol_without_promotion_completes": {"grid": 1},
}


@pytest.mark.slow
@pytest.mark.parametrize("scenario", list(_SCENARIOS))
def test_real_run_artifacts_validate(scenario, harness, recorded, caplog, monkeypatch):  # noqa: F811
    expect = _SCENARIOS[scenario]
    # blocking mode: a document the schemas refuse would raise inside save_yaml/load_yaml
    # and the run would not complete (the scenario's own assertions would fail)
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    with caplog.at_level(logging.WARNING, logger=wav.logger.name):
        getattr(e061, scenario)(harness)

    # no validation warning for the three stems anywhere in the run
    ours = [r.getMessage() for r in caplog.records
            if r.name == wav.logger.name and any(f"/{s}." in r.getMessage() or f"\\{s}." in r.getMessage()
                                                 for s in STEMS)]
    assert ours == [], ours[:1]

    by_stem = {s: [d for st, _p, d in recorded if st == s] for s in STEMS}
    on_disk = {s: [] for s in STEMS}
    for s in STEMS:
        for f in harness.root.glob(f"runs/*/**/{s}.yaml"):
            on_disk[s].append(yaml.safe_load(f.read_text(encoding="utf-8")))
    for s in STEMS:
        assert by_stem[s] and on_disk[s], f"{scenario}: no {s} passed the hook / reached disk"
        for i, doc in enumerate(by_stem[s] + on_disk[s]):
            _assert_valid(s, doc, f"{scenario}[{i}]")
    for doc in by_stem["grid_evaluation"] + on_disk["grid_evaluation"]:
        check_grid_rules(doc)
    for doc in by_stem["variant_patches"] + on_disk["variant_patches"]:
        check_variant_patches_rules(doc)
    # every idea_status file matches the grid file next to it
    for f in harness.root.glob("runs/*/artifacts/idea_status.yaml"):
        status = yaml.safe_load(f.read_text(encoding="utf-8"))
        grid = yaml.safe_load((f.parent / "grid_evaluation.yaml").read_text(encoding="utf-8"))
        check_status_matches_grid(status, grid)

    disk_grids = on_disk["grid_evaluation"]
    assert len(disk_grids) >= expect["grid"]
    if expect.get("failed"):
        assert any("failed_variants" in g for g in disk_grids)
    if expect.get("untested"):
        assert any("untested_variants" in g for g in disk_grids)
    assert len(by_stem["variant_patches"]) >= expect.get("patches_min", 1)
    # per-coin variants: the harness writes kind + symbol on every entry
    assert any(v.get("kind") and v.get("symbol") for d in on_disk["variant_patches"] for v in d["variants"])


# ---------------------------------------------------------------------------
# 4. the frozen corpus of real writer output (all existing tests)
# ---------------------------------------------------------------------------

def _corpus() -> list:
    return json.loads(_CORPUS.read_text(encoding="utf-8"))


def test_frozen_writer_corpus_validates():
    corpus = _corpus()
    by_stem = {s: [e for e in corpus if e["stem"] == s] for s in STEMS}
    assert all(len(v) >= 3 for v in by_stem.values()), {k: len(v) for k, v in by_stem.items()}
    for e in corpus:
        _assert_valid(e["stem"], e["doc"], e["source"])
        if e["stem"] == "grid_evaluation":
            check_grid_rules(e["doc"])
        elif e["stem"] == "variant_patches":
            check_variant_patches_rules(e["doc"])
    # the composition-only cell paths are represented
    cells = [c for e in by_stem["grid_evaluation"] for row in e["doc"]["grid"].values() for c in row.values()]
    assert any("p_value_one_sided" in c for c in cells), "no residual_ic cell in the corpus"
    assert any(c.get("source") == "profit_bars" and c.get("bars") for c in cells)
    assert any("weight_schedule" in c for c in cells)


# ---------------------------------------------------------------------------
# 5. every required key / enum is enforced (hand-written malformed documents)
# ---------------------------------------------------------------------------

def _valid_grid() -> dict:
    g = _direct_grids()
    return copy.deepcopy(g["failed_untested_partial"])


def _valid_status() -> dict:
    return rpr._build_idea_status_artifact(_direct_grids()["all_pass"], "run_001")


def _valid_patches() -> dict:
    return {"base_config_ref": "artifacts/backtest_spec.yaml", "variants": [
        {"variant_id": "base", "kind": "base", "symbol": "BTCUSDT", "patch": [], "rationale": "r"},
        {"variant_id": "fast", "kind": "design", "symbol": "BTCUSDT",
         "patch": [{"path": "/strategies/warmup", "value": 10}], "rationale": "r"},
        {"variant_id": "xrp", "kind": "asset", "symbol": "XRPUSDT", "patch": [], "rationale": "r"}]}


_VALID = {"grid_evaluation": _valid_grid, "idea_status": _valid_status, "variant_patches": _valid_patches}


@pytest.mark.parametrize("stem", STEMS)
def test_hand_written_valid_documents_validate(stem):
    _assert_valid(stem, _VALID[stem]())


@pytest.mark.parametrize("stem", STEMS)
def test_every_top_level_required_key_is_enforced(stem):
    for key in _schema(stem)["required"]:
        doc = _VALID[stem]()
        del doc[key]
        _assert_invalid(stem, doc, f"missing {key}")


def _set(path, value):
    def mut(doc):
        node = doc
        for p in path[:-1]:
            node = node[p]
        node[path[-1]] = value
    return mut


def _del(path):
    def mut(doc):
        node = doc
        for p in path[:-1]:
            node = node[p]
        del node[path[-1]]
    return mut


_GRID_BAD = {
    "result_enum": _set(["result"], "DONE"),
    "idea_status_enum": _set(["idea_status"], "promising"),
    "spec_error_needs_null_status": _set(["result"], "SPEC_ERROR"),
    "evaluated_grid_needs_a_status": _set(["idea_status"], None),
    "criteria_not_list": _set(["criteria"], "a"),
    "criteria_empty": _set(["criteria"], []),
    "criteria_duplicate": _set(["criteria"], ["a", "a"]),
    "variants_empty": _set(["variants"], []),
    "variants_non_string": _set(["variants"], [1]),
    "grid_empty": _set(["grid"], {}),
    "grid_row_not_object": _set(["grid", "a"], []),
    "reason_empty": _set(["reason"], ""),
    "evaluated_at_type": _set(["evaluated_at"], 123),
    "unknown_top_level_key": _set(["extra"], 1),
    "failed_variants_bad_prefix": _set(["failed_variants"], {"x": "crashed"}),
    "failed_variants_empty": _set(["failed_variants"], {}),
    "failed_variants_not_mapping": _set(["failed_variants"], ["x"]),
    "untested_variants_empty_reason": _set(["untested_variants"], {"x": ""}),
    "untested_variants_empty": _set(["untested_variants"], {}),
    "partial_variants_empty": _set(["partial_coverage_variants"], {}),
    "cell_result_enum": _set(["grid", "a", "base", "result"], "MAYBE"),
    "cell_missing_result": _del(["grid", "a", "base", "result"]),
    "cell_unknown_key": _set(["grid", "a", "base", "surprise"], 1),
    "cell_comparator_enum": _set(["grid", "a", "base", "comparator"], "~"),
    "cell_value_type": _set(["grid", "a", "base", "value"], "high"),
    "cell_n_windows_type": _set(["grid", "a", "base", "n_windows"], 1.5),
    "cell_n_windows_negative": _set(["grid", "a", "base", "n_windows"], -1),
    "cell_source_const": _set(["grid", "a", "base", "source"], "window"),
    "cell_per_symbol_nested": _set(["grid", "a", "base", "per_symbol"],
                                   {"BTCUSDT": {"result": "PASS", "per_symbol": {}}}),
    "cell_per_symbol_empty": _set(["grid", "a", "base", "per_symbol"], {}),
    "cell_bars_row_missing_name": _set(["grid", "a", "base", "bars"],
                                       [{"threshold": 1, "actual": 1, "result": "PASS"}]),
    "cell_bars_row_result_enum": _set(["grid", "a", "base", "bars"],
                                      [{"name": "n", "threshold": 1, "actual": 1, "result": "OK"}]),
    "cell_bars_row_missing_actual": _set(["grid", "a", "base", "bars"],
                                         [{"name": "n", "threshold": 1, "result": "PASS"}]),
    "cell_bars_row_unknown_key": _set(["grid", "a", "base", "bars"],
                                      [{"name": "n", "threshold": 1, "actual": 1, "result": "PASS", "x": 1}]),
    "cell_bars_row_comparator_enum": _set(["grid", "a", "base", "bars"],
                                          [{"name": "n", "threshold": 1, "actual": 1, "result": "PASS",
                                            "comparator": "=="}]),
}


@pytest.mark.parametrize("name", list(_GRID_BAD))
def test_grid_evaluation_rejects(name):
    doc = _valid_grid()
    _GRID_BAD[name](doc)
    _assert_invalid("grid_evaluation", doc, name)


def test_grid_evaluation_spec_error_needs_null_status_but_accepts_it():
    doc = _valid_grid()
    doc["result"], doc["idea_status"] = "SPEC_ERROR", None
    _assert_valid("grid_evaluation", doc)


_STATUS_BAD = {
    "run_id_empty": _set(["run_id"], ""),
    "idea_status_enum": _set(["idea_status"], "maybe"),
    "idea_status_none": _set(["idea_status"], None),
    "result_enum": _set(["result"], "SPEC_ERROR"),
    "hypothesis_verdict_enum": _set(["hypothesis_verdict"], "refine"),
    "lineage_routing_enum": _set(["lineage_routing"], "pivot"),
    "ref_shape": _set(["grid_evaluation_ref"], "artifacts/grid_evaluation.yaml"),
    "ref_wrong_file": _set(["grid_evaluation_ref"], "runs/run_001/artifacts/idea_status.yaml"),
    "reason_type": _set(["reason"], 3),
    "unknown_key": _set(["extra"], 1),
    # validated is PASS / promote / null: any other triple is refused
    "validated_but_FAIL": _set(["result"], "FAIL"),
    "validated_but_kill": _set(["hypothesis_verdict"], "kill"),
    "validated_but_terminate": _set(["lineage_routing"], "terminate"),
}


@pytest.mark.parametrize("name", list(_STATUS_BAD))
def test_idea_status_rejects(name):
    doc = _valid_status()
    assert doc["idea_status"] == "validated"
    _STATUS_BAD[name](doc)
    _assert_invalid("idea_status", doc, name)


@pytest.mark.parametrize("idea_status,triple", [
    ("validated", ("PASS", "promote", None)),
    ("refuted", ("FAIL", "kill", "terminate")),
    ("inconclusive", ("INCONCLUSIVE", "human_pause", "inconclusive_grid")),
])
def test_idea_status_routing_triples_are_pinned_to_the_status(idea_status, triple):
    assert rpr._GRID_IDEA_STATUS_ROUTING[idea_status] == triple  # the schema copies the code's table
    doc = {"run_id": "run_1", "idea_status": idea_status, "result": triple[0],
           "hypothesis_verdict": triple[1], "lineage_routing": triple[2],
           "grid_evaluation_ref": "runs/run_1/artifacts/grid_evaluation.yaml", "reason": None}
    _assert_valid("idea_status", doc)
    for other, t in rpr._GRID_IDEA_STATUS_ROUTING.items():
        if other != idea_status:
            for i, key in enumerate(("result", "hypothesis_verdict", "lineage_routing")):
                bad = {**doc, key: t[i]}
                _assert_invalid("idea_status", bad, f"{idea_status} carrying {other}'s {key}")


_PATCHES_BAD = {
    "variants_missing": _del(["variants"]),
    "variants_empty": _set(["variants"], []),
    "variants_not_list": _set(["variants"], {"base": {}}),
    "entry_not_mapping": _set(["variants", 1], "fast"),
    "variant_id_missing": _del(["variants", 1, "variant_id"]),
    "variant_id_empty": _set(["variants", 1, "variant_id"], ""),
    "variant_id_unsafe_path": _set(["variants", 1, "variant_id"], "../../escape"),
    "variant_id_slash": _set(["variants", 1, "variant_id"], "design/v2"),
    "variant_id_space": _set(["variants", 1, "variant_id"], "fast one"),
    "kind_enum": _set(["variants", 1, "kind"], "hybrid"),
    "symbol_list_is_multi_coin": _set(["variants", 2, "symbol"], ["XRPUSDT", "ETHUSDT"]),
    "symbol_empty": _set(["variants", 2, "symbol"], ""),
    "symbols_key_is_multi_coin": _set(["variants", 2, "symbols"], ["XRPUSDT"]),
    "patch_not_list": _set(["variants", 1, "patch"], {"path": "/a", "value": 1}),
    "patch_op_not_mapping": _set(["variants", 1, "patch"], [21]),
    "patch_op_missing_path": _set(["variants", 1, "patch"], [{"value": 1}]),
    "patch_op_missing_value": _set(["variants", 1, "patch"], [{"path": "/a"}]),
    "patch_path_not_pointer": _set(["variants", 1, "patch"], [{"path": "a/b", "value": 1}]),
    "patch_path_empty": _set(["variants", 1, "patch"], [{"path": "", "value": 1}]),
    "patch_path_root_only": _set(["variants", 1, "patch"], [{"path": "/", "value": 1}]),
    "patch_path_not_string": _set(["variants", 1, "patch"], [{"path": 3, "value": 1}]),
    "rationale_type": _set(["variants", 1, "rationale"], ["r"]),
    "base_config_ref_type": _set(["base_config_ref"], 1),
}


@pytest.mark.parametrize("name", list(_PATCHES_BAD))
def test_variant_patches_rejects(name):
    doc = _valid_patches()
    _PATCHES_BAD[name](doc)
    _assert_invalid("variant_patches", doc, name)


@pytest.mark.parametrize("name,mut", [
    ("patch_missing_or_null_is_read_as_empty", _del(["variants", 0, "patch"])),
    ("patch_null", _set(["variants", 0, "patch"], None)),
    ("legacy_coinless_entries", lambda d: [v.pop(k, None) for v in d["variants"] for k in ("kind", "symbol")]),
    ("symbol_null", _set(["variants", 0, "symbol"], None)),
    ("no_rationale", _del(["variants", 0, "rationale"])),
    ("no_base_config_ref", _del(["base_config_ref"])),
    ("code_written_top_level_keys", lambda d: d.update(generated_by="tools/composition.py",
                                                       composition_registry_hash="h")),
    ("unread_extra_keys_tolerated", lambda d: d["variants"][0].update(title="x")),
    ("patch_value_any_json", _set(["variants", 1, "patch"], [{"path": "/a/b", "value": {"x": [1, None]}},
                                                             {"path": "/c", "value": None}])),
])
def test_variant_patches_permissive_choices_the_code_accepts(name, mut):
    doc = _valid_patches()
    mut(doc)
    _assert_valid("variant_patches", doc, name)
