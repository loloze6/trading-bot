"""
D-196 -- three warn-only schema drifts seen on run_101, and the base variant's whole-test
book on the tried_ideas row.

  1. hypothesis_card `target_market` as a list validates (schema was string-only).
  2. backtest_spec without `hypothesis_id` validates (schema required it; no skill asks for it).
  3. decision_record candidate `angle` / `floor_lowered` validate (closed candidate schema).
  4. base_book: the five figures are COPIED from artifacts/profit_bars_evaluation.yaml
     (synthetic values a recompute could not produce), missing figures are null, a run
     without a base variant has no block, an old entry loads and its tried_ideas row is
     unchanged, and the view passes the figures through.

Everything is built synthetically under the per-test sandbox (tests/conftest.py).
"""
import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import campaign_memory as cm  # noqa: E402
from workflow_artifact_validation import validate_workflow_artifact  # noqa: E402

SCHEMAS = SR_ROOT / "workflow_artifacts" / "schemas"


def _schema(name: str) -> dict:
    return json.loads((SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))


@pytest.fixture
def strict(monkeypatch):
    """Schema violations raise instead of warning."""
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")


# ---------------------------------------------------------------------------
# 1-3. the three schema drifts (a run_101-shaped record validates)
# ---------------------------------------------------------------------------

def test_hypothesis_card_target_market_list_validates(strict):
    card = {"hypothesis_id": "H", "timeframe": "1h", "target_market": ["BTCUSDT"]}
    validate_workflow_artifact("hypothesis_card.yaml", card)
    validate_workflow_artifact("hypothesis_card.yaml", {**card, "target_market": ["BTCUSDT", "ETHUSDT"]})
    validate_workflow_artifact("hypothesis_card.yaml", {**card, "target_market": "BTCUSDT, ETHUSDT"})


@pytest.mark.parametrize("bad", [5, {"asset": "BTCUSDT"}, [1, 2], [["BTCUSDT"]]])
def test_hypothesis_card_target_market_still_rejects_other_shapes(strict, bad):
    import jsonschema
    card = {"hypothesis_id": "H", "timeframe": "1h", "target_market": bad}
    with pytest.raises(jsonschema.ValidationError):
        validate_workflow_artifact("hypothesis_card.yaml", card)


def test_backtest_spec_without_hypothesis_id_validates(strict):
    import jsonschema
    spec = {"status": "spec_ready", "config": {"regime_detector": {}, "strategies": {}},
            "config_rationale": [{"hypothesis_claim": "c", "config_choice": "x"}],
            "component_gap": None}
    validate_workflow_artifact("backtest_spec.yaml", spec)
    validate_workflow_artifact("backtest_spec.yaml", {**spec, "hypothesis_id": "H"})
    # the other required fields still are
    for key in ("status", "config", "config_rationale"):
        broken = {k: v for k, v in spec.items() if k != key}
        with pytest.raises(jsonschema.ValidationError):
            validate_workflow_artifact("backtest_spec.yaml", broken)


def _candidate() -> dict:
    return {
        "candidate_id": "forecast_power-run_078-1", "origin": "reader", "kind": "side_finding",
        "category": "forecast_power", "source_run": "run_078", "parent_hypothesis_id": "P",
        "hypothesis_id": "P__forecast_power-run_078-1",
        "proposal_ref": "runs/run_078/artifacts/proposals/forecast_power.yaml#forecast_power-run_078-1",
        "collapsed_sources": [],
        "scores": {"confidence_real": 2, "distance_to_profitable": 2, "mechanism_plausibility": 2,
                   "model_id": "m", "rubric_version": "v"},
        "resolved_config_sha256": None,
        "gates": {"novelty": {"exact_match": "NOVEL", "matched_runs": [],
                              "digest_advisory": {"outcome": "novel", "family": None,
                                                  "family_confidence": None, "run_ids": []}},
                  "feasibility": {"result": "FEASIBLE", "reasons": []}},
        "eligible": True,
        "cost": {"backtests": 3, "seconds_estimate": 184, "basis": "b"},
        "rank": 2,
    }


def _check_candidate(cand: dict) -> None:
    import jsonschema
    schema = _schema("decision_record")
    jsonschema.Draft202012Validator(
        {"$ref": "#/$defs/candidate", "$defs": schema["$defs"]}).validate(cand)


def test_decision_record_candidate_angle_and_floor_lowered_validate():
    import jsonschema
    base = _candidate()
    _check_candidate(base)                                       # unchanged shape still valid
    _check_candidate({**base, "angle": "regime"})                # the run_101 candidate
    _check_candidate({**base, "angle": "sizing"})
    one = {"from": 0.2, "to": 0.1, "after": "q3", "reason": "r"}
    _check_candidate({**base, "floor_lowered": one})
    _check_candidate({**base, "floor_lowered": [one, {**one, "test": "q4"}]})
    with pytest.raises(jsonschema.ValidationError):
        _check_candidate({**base, "angle": "carry"})             # only the writer's two values
    with pytest.raises(jsonschema.ValidationError):
        _check_candidate({**base, "something_else": 1})          # the schema is still closed


def test_the_writer_side_values_are_what_the_schema_accepts():
    """decide_next writes reader_proposals' angle values; the schema enum must match them."""
    import reader_proposals as rp
    enum = _schema("decision_record")["$defs"]["candidate"]["properties"]["angle"]["enum"]
    assert sorted(enum) == sorted(rp.ANGLES)


# ---------------------------------------------------------------------------
# 4. base_book on the memory entry and the tried_ideas row
# ---------------------------------------------------------------------------

BASE = {  # values a recompute from any bars could not produce
    "sharpe": -0.4242, "max_dd": 33.3333, "shape_alloc": 0.1234567, "econ_alloc": 0.9999,
    "turnover": 7.7777, "median": 11.5,
}


def _variant_doc(vid: str, tested: bool, *, base_figures: bool, economics: bool = True) -> dict:
    if not tested:
        return {"kind": "variant", "trial_id": f"run_980:{vid}", "result": "NOT_TESTED",
                "reason": "not tested", "bars": [], "reasons": []}
    bars = [{"name": "sharpe_min", "threshold": 0.0, "actual": BASE["sharpe"], "result": "FAIL"},
            {"name": "max_drawdown_pct_max", "threshold": 20.0, "actual": BASE["max_dd"],
             "result": "FAIL", "advisory": True},
            {"name": "trade_frequency_min", "threshold": 0.01, "actual": 0.3, "result": "PASS"}]
    doc = {"kind": "variant", "trial_id": f"run_980:{vid}", "result": "FAIL", "reason": None,
           "bars": bars, "reasons": []}
    if base_figures:
        doc["forecast_shape"] = {"abs_mean_forecast": 5.0, "share_at_cap": 0.01,
                                 "abs_mean_allocation": BASE["shape_alloc"], "n_bars": 10, "n_windows": 2}
        if economics:
            doc["window_economics"] = {"windows": {}, "total": {
                "mean_abs_allocation": BASE["econ_alloc"], "turnover_annualised": BASE["turnover"],
                "median_holding_bars": BASE["median"], "trades": 5}}
    return doc


def _write_evaluation(run_dir: Path, entry: dict, *, drop_base: bool = False,
                      economics: bool = True, shape: bool = True) -> None:
    graded = {}
    for vid, v in entry["variants"].items():
        graded[vid] = _variant_doc(vid, v["status"] == "tested", base_figures=(vid == "base"),
                                   economics=economics)
    if not shape:
        graded["base"].pop("forecast_shape", None)
    if drop_base:                      # an evaluation with no `base` variant at all
        graded.pop("base")
    doc = {"run_id": "run_980", "generated_at": "t", "scope": cm.PROFIT_BARS_SCOPE_EVERY_BACKTEST,
           "bars_definitions": "v2", "variants": graded, "passing": [], "result": "FAIL"}
    (run_dir / "artifacts" / "profit_bars_evaluation.yaml").write_text(
        yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _seed_entry_inputs():
    import test_e058_s2a_regroup_record as t58
    t58._set_orchestrator(t58.ALL_ON)
    run_dir = t58._seed(idea_status="refuted", variant_loop=True)
    kw = dict(trial_sharpes=rpr.load_campaign_state()["trial_sharpes"],
              categories=rpr._reader_categories(), protocol_root=rpr.ROOT, recorded_at="t")
    plain = cm.build_memory_entry(run_dir, t58.RUN_ID, **kw)
    return run_dir, kw, plain


def test_entry_carries_the_five_figures_read_from_the_evaluation():
    run_dir, kw, plain = _seed_entry_inputs()
    assert "base_book" not in plain                                   # flag off: as before
    _write_evaluation(run_dir, plain)
    entry = cm.build_memory_entry(run_dir, "run_980", profit_bars_evaluated=True, **kw)
    assert entry["base_book"] == {
        "sharpe": BASE["sharpe"], "max_drawdown_pct": BASE["max_dd"],
        "mean_abs_allocation": BASE["shape_alloc"],      # forecast_shape first, not window_economics
        "turnover_annualised": BASE["turnover"], "median_holding_bars": BASE["median"]}
    # nothing else on the entry moved
    assert {k: v for k, v in entry.items() if k not in ("base_book", "profit_bars", "profit_bars_reason")} \
        == {k: v for k, v in plain.items() if k not in ("profit_bars", "profit_bars_reason")}
    # the entry validates against the memory schema (closed entry, new optional key)
    import jsonschema
    schema = _schema("campaign_memory")
    jsonschema.Draft202012Validator({"$ref": "#/$defs/entry", "$defs": schema["$defs"]}).validate(entry)


def test_missing_figures_are_null_and_allocation_falls_back_to_window_economics():
    run_dir, kw, plain = _seed_entry_inputs()
    _write_evaluation(run_dir, plain, economics=False)                # analyst flag off
    book = cm.build_memory_entry(run_dir, "run_980", profit_bars_evaluated=True, **kw)["base_book"]
    assert book == {"sharpe": BASE["sharpe"], "max_drawdown_pct": BASE["max_dd"],
                    "mean_abs_allocation": BASE["shape_alloc"],
                    "turnover_annualised": None, "median_holding_bars": None}
    _write_evaluation(run_dir, plain, shape=False)                    # no forecast_shape
    book = cm.build_memory_entry(run_dir, "run_980", profit_bars_evaluated=True, **kw)["base_book"]
    assert book["mean_abs_allocation"] == BASE["econ_alloc"]
    _write_evaluation(run_dir, plain, economics=False, shape=False)
    book = cm.build_memory_entry(run_dir, "run_980", profit_bars_evaluated=True, **kw)["base_book"]
    assert book["mean_abs_allocation"] is None


def test_no_base_variant_in_the_evaluation_means_no_block():
    run_dir, kw, plain = _seed_entry_inputs()
    _write_evaluation(run_dir, plain, drop_base=True)
    assert cm.base_book_block(run_dir, "run_980") is None
    # a base variant that was not tested: the block exists, every figure null
    graded = yaml.safe_load((run_dir / "artifacts" / "profit_bars_evaluation.yaml").read_text(encoding="utf-8"))
    graded["variants"]["base"] = _variant_doc("base", False, base_figures=False)
    (run_dir / "artifacts" / "profit_bars_evaluation.yaml").write_text(
        yaml.safe_dump(graded, sort_keys=False), encoding="utf-8")
    assert cm.base_book_block(run_dir, "run_980") == {k: None for k in cm.BASE_BOOK_FIELDS}


@pytest.mark.parametrize("bad", [True, "0.3", float("nan"), float("inf"), None, [1]])
def test_record_number_takes_only_finite_real_numbers(bad):
    assert cm._record_number(bad) is None
    assert cm._record_number(0) == 0 and cm._record_number(-1.5) == -1.5


def test_memory_with_old_and_new_entries_loads_and_the_view_passes_the_figures_through(tmp_path):
    run_dir, kw, plain = _seed_entry_inputs()
    _write_evaluation(run_dir, plain)
    new = cm.build_memory_entry(run_dir, "run_980", profit_bars_evaluated=True, **kw)
    old = copy.deepcopy(plain)
    old["run_id"], old["recorded_at"] = "run_979", "2020-01-01T00:00:00+00:00"
    path = tmp_path / "campaign_memory.yaml"
    cm.upsert_memory(path, old)
    cm.upsert_memory(path, new)
    memory = cm.load_memory(path)                                     # strict loader accepts both
    rows = {r["run_id"]: r for r in cm.tried_ideas(memory, root=rpr.ROOT)["runs"]}
    keys = ["base_sharpe", "base_max_drawdown_pct", "base_mean_abs_allocation",
            "base_turnover_annualised", "base_median_holding_bars"]
    assert [rows["run_980"][k] for k in keys] == [
        BASE["sharpe"], BASE["max_dd"], BASE["shape_alloc"], BASE["turnover"], BASE["median"]]
    row_keys = list(rows["run_980"])
    assert row_keys[row_keys.index("variants_tested") + 1:][:5] == keys
    # the old entry: no key at all, row exactly as before
    assert not any(k in rows["run_979"] for k in keys)
    assert list(rows["run_979"]) == ["run_id", "hypothesis_id", "symbols", "timeframe",
                                     "idea_status", "variants_tested"]


def test_view_row_with_a_null_figure_keeps_the_key_with_null():
    runs = {"run_a": {"run_id": "run_a", "hypothesis_id": "H", "recorded_at": "2021-01-01",
                      "idea_status": "refuted", "timeframe": "1h", "variants": {},
                      "base_book": {"sharpe": 0.5, "max_drawdown_pct": None,
                                    "mean_abs_allocation": None, "turnover_annualised": None,
                                    "median_holding_bars": None}}}
    (row,) = cm.tried_ideas({"runs": runs}, root=rpr.ROOT)["runs"]
    assert row["base_sharpe"] == 0.5
    assert row["base_max_drawdown_pct"] is None and row["base_median_holding_bars"] is None


def test_view_ignores_a_malformed_base_book():
    runs = {"run_a": {"run_id": "run_a", "hypothesis_id": "H", "recorded_at": "2021-01-01",
                      "idea_status": "refuted", "timeframe": "1h", "variants": {},
                      "base_book": "not a mapping"}}
    (row,) = cm.tried_ideas({"runs": runs}, root=rpr.ROOT)["runs"]
    assert "base_sharpe" not in row


def test_tried_ideas_note_names_the_new_fields():
    for name in ("base_sharpe", "base_max_drawdown_pct", "base_mean_abs_allocation",
                 "base_turnover_annualised", "base_median_holding_bars"):
        assert name in cm.TRIED_IDEAS_NOTE
