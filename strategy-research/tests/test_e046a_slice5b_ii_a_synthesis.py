"""
E-046a Slice 5b-ii-A: mechanical verdict synthesis
(workflow/run_phase1_research.py::_synthesize_verdict, schema
workflow_artifacts/schemas/verdict_synthesis.schema.json).

Spec: engineering/roadmap/E-046a/S1_FINDINGS_5B_II.md §5 plus its
"Decision (operator, 2026-09-23)" section (new artifact/schema, static
S_max >= 6). Every fixture here is hand-built in tmp_path -- no real run
directory is read or written, no LLM is involved.

Covers:
  1. Case B scoring: all-5-empty -> kill; single strong proposal -> refine with the
     right proposed_change_dimension; 0 < S_max < 6 -> refine low-confidence;
     S_max == 0 -> kill; the S_max=6 boundary; deterministic tie-break.
  2. Case A: a binding pass_rule_evaluation.yaml is carried through verbatim
     (every authority-table pair), even against strong contrary proposals;
     discretion: stage / legacy_not_evaluable / SPEC_ERROR / absent fall to Case B.
  3. Safety checks (component_execution_error, regime_misattribution) fire
     regardless of proposals and of a binding verdict, and never read proposals.
  4. VERDICT_BLOCKED pauses rather than issuing a verdict.
  5. Fail-closed on unknown enum/discretion/result values and malformed inputs,
     including every malformed-proposal-file shape.
  6. Output validates against the new schema; smuggled undeclared fields are
     rejected at every object level.
  7. Purity (no files written) and legacy-carryover compatibility of `rationale`.
"""
import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

jsonschema = pytest.importorskip("jsonschema")

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(WORKFLOW_PATH))
sys.path.insert(0, str(TOOLS_PATH))

import run_phase1_research as rpr  # noqa: E402
import build_reports  # noqa: E402

SCHEMA_PATH = (Path(__file__).parent.parent / "workflow_artifacts" / "schemas"
               / "verdict_synthesis.schema.json")
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
VALIDATOR = jsonschema.Draft202012Validator(SCHEMA)
FAMILY = "test_family"
CATEGORIES = list(build_reports.REPORT_CATEGORIES)


# ---------------------------------------------------------------------------
# fixture builders
# ---------------------------------------------------------------------------

def _protocol_result(component_error_count=0, uninformative=(), n_bars=50):
    results = []
    for sym in ("BTCUSDT", "ETHUSDT"):
        for w in ("w1", "w2"):
            results.append({
                "symbol": sym, "window": w, "run_id": f"{sym}_{w}",
                "core": {"trade_count": 30},
                "regime_validity": {r: {"n_bars": n_bars, "informative": False} for r in uninformative},
                "component_errors": {"count": component_error_count, "samples": []},
            })
    return {
        "results": results,
        "hypothesis_verdict": {
            "verdict": "refine",
            "diagnostics": {
                "median_forecast_return_corr": 0.0412,
                "median_cost_drag_pct": 142.82,
                "median_gross_pnl": -3.5,
                "uninformative_regimes": list(uninformative),
            },
        },
    }


def _detector_report(confidence="high"):
    return {"per_symbol_per_timeframe": [
        {"symbol": s, "timeframe": "1h", "confidence": confidence, "metrics": {}}
        for s in ("BTCUSDT", "ETHUSDT")
    ]}


def _proposal(cat, n=1, scores=(2, 2, 2), kind="patch", field="transforms[2].params.min_abs"):
    p = {
        "proposal_id": f"{cat}-run_test-{n}",
        "kind": kind,
        "evidence": [f"slices.overall.diagnostics.x={n}"],
        "scores": dict(zip(("confidence_real", "distance_to_profitable",
                            "mechanism_plausibility"), scores)),
        "model_id": "test-model",
        "rubric_version": f"{cat}-reader-v1",
    }
    if kind == "patch":
        p["patch"] = [{"component_id": "keltner", "field": field, "before": 15.0, "after": 20.0}]
    else:
        p["block"] = {"kind": "forecast", "config_paths": ["strategies.regimes.unknown.components"],
                      "scaffolding": ["x"], "rationale": "y"}
    return p


def _make_run(tmp_path, *, protocol=None, pass_rule=None, proposals=None, raw_proposals=None):
    """proposals: {category: list} written as YAML; categories not named are
    left absent. raw_proposals: {filename: text} written verbatim."""
    art = tmp_path / "run" / "artifacts"
    art.mkdir(parents=True)
    (art / "hypothesis_card.yaml").write_text(yaml.safe_dump({"hypothesis_id": "H-TEST-1"}), encoding="utf-8")
    (art / "protocol_result.yaml").write_text(
        yaml.safe_dump(protocol if protocol is not None else _protocol_result()), encoding="utf-8")
    if pass_rule is not None:
        (art / "pass_rule_evaluation.yaml").write_text(yaml.safe_dump(pass_rule), encoding="utf-8")
    if proposals is not None or raw_proposals is not None:
        (art / "proposals").mkdir()
    for cat, items in (proposals or {}).items():
        (art / "proposals" / f"{cat}.yaml").write_text(yaml.safe_dump(items), encoding="utf-8")
    for name, text in (raw_proposals or {}).items():
        (art / "proposals" / name).write_text(text, encoding="utf-8")
    return tmp_path / "run"


def _synth(run_dir, report="default"):
    return rpr._synthesize_verdict(run_dir, FAMILY, _detector_report() if report == "default" else report)


def _assert_valid(out):
    errors = sorted(VALIDATOR.iter_errors(out), key=str)
    assert not errors, [e.message for e in errors]


def _binding(result, hv, lr, **extra):
    d = {"result": result, "hypothesis_verdict": hv, "lineage_routing": lr,
         "statement_branch_matched": "PASS" if result == "PASS" else "FAIL-a",
         "branches_failed": [] if result == "PASS" else ["FAIL-a"],
         "criteria_results": [{"id": "a", "result": result}]}
    d.update(extra)
    return d


# ---------------------------------------------------------------------------
# 0. the constant
# ---------------------------------------------------------------------------

def test_threshold_constant_is_static_six():
    assert rpr.SYNTHESIS_REFINE_MIN_S_MAX == 6
    assert rpr.VERDICT_SYNTHESIS_FILENAME == "verdict_synthesis.yaml"


# ---------------------------------------------------------------------------
# 1. Case B scoring
# ---------------------------------------------------------------------------

def test_all_five_empty_kills(tmp_path):
    # mix of explicit `[]` files and absent files -- both contribute nothing.
    run = _make_run(tmp_path, proposals={"profitability": [], "regime_power": [],
                                         "component_attribution": []})
    out = _synth(run)
    _assert_valid(out)
    assert out["decided_by"] == "scored_proposals"
    assert (out["hypothesis_verdict"], out["lineage_routing"]) == ("kill", "terminate")
    assert out["scoring"]["s_max"] is None and out["scoring"]["winner"] is None
    assert out["scoring"]["proposal_counts"] == {c: 0 for c in CATEGORIES}
    assert out["proposed_change_dimension"] is None


def test_no_proposals_dir_at_all_kills(tmp_path):
    out = _synth(_make_run(tmp_path))
    assert (out["hypothesis_verdict"], out["lineage_routing"]) == ("kill", "terminate")


def test_single_high_scoring_proposal_refines_with_its_dimension(tmp_path):
    run = _make_run(tmp_path, proposals={
        "profitability": [_proposal("profitability", scores=(3, 2, 2))],
        "forecast_power": [],
    })
    out = _synth(run)
    _assert_valid(out)
    assert (out["hypothesis_verdict"], out["lineage_routing"]) == ("refine", "refine")
    assert out["scoring"]["s_max"] == 7
    assert out["scoring"]["low_confidence"] is False
    assert out["scoring"]["winner"]["category"] == "profitability"
    assert out["proposed_change_dimension"] == "transforms[2].params.min_abs"


def test_below_threshold_refines_low_confidence(tmp_path):
    run = _make_run(tmp_path, proposals={"trade_efficiency": [_proposal("trade_efficiency", scores=(2, 1, 2))]})
    out = _synth(run)
    _assert_valid(out)
    assert (out["hypothesis_verdict"], out["lineage_routing"]) == ("refine", "refine")
    assert out["scoring"]["s_max"] == 5
    assert out["scoring"]["low_confidence"] is True
    assert "low confidence" in out["rationale"]


@pytest.mark.parametrize("scores,low", [((2, 2, 2), False), ((3, 2, 0), True), ((3, 3, 0), False)])
def test_threshold_boundary(tmp_path, scores, low):
    run = _make_run(tmp_path, proposals={"profitability": [_proposal("profitability", scores=scores)]})
    assert _synth(run)["scoring"]["low_confidence"] is low


def test_all_zero_scores_kill_not_refine(tmp_path):
    run = _make_run(tmp_path, proposals={
        "profitability": [_proposal("profitability", scores=(0, 0, 0))],
        "regime_power": [_proposal("regime_power", scores=(0, 0, 0))],
    })
    out = _synth(run)
    _assert_valid(out)
    assert (out["hypothesis_verdict"], out["lineage_routing"]) == ("kill", "terminate")
    assert out["scoring"]["s_max"] == 0
    assert out["scoring"]["low_confidence"] is False
    assert out["proposed_change_dimension"] is None


def test_best_proposal_across_categories_wins_and_ties_are_recorded(tmp_path):
    run = _make_run(tmp_path, proposals={
        "component_attribution": [_proposal("component_attribution", scores=(3, 3, 1), field="weight")],
        "forecast_power": [_proposal("forecast_power", 1, scores=(1, 1, 1)),
                           _proposal("forecast_power", 2, scores=(2, 3, 2), field="scaling_factor")],
        "profitability": [_proposal("profitability", scores=(1, 0, 0))],
    })
    out = _synth(run)
    # 7 in forecast_power and 7 in component_attribution: category order decides.
    assert out["scoring"]["s_max"] == 7
    assert out["scoring"]["winner"]["proposal_id"] == "forecast_power-run_test-2"
    assert out["scoring"]["tied_proposal_ids"] == ["forecast_power-run_test-2",
                                                   "component_attribution-run_test-1"]
    assert out["proposed_change_dimension"] == "scaling_factor"
    assert out["scoring"]["proposal_counts"]["forecast_power"] == 2


def test_new_block_dimension(tmp_path):
    run = _make_run(tmp_path, proposals={"forecast_power": [_proposal("forecast_power", kind="new_block", scores=(3, 3, 3))]})
    out = _synth(run)
    _assert_valid(out)
    assert out["proposed_change_dimension"] == "new_block:forecast:strategies.regimes.unknown.components"


def test_multi_field_patch_dimension_is_sorted_and_deduped(tmp_path):
    p = _proposal("profitability", scores=(3, 3, 3))
    p["patch"] = [{"field": "b"}, {"field": "a"}, {"field": "b"}]
    out = _synth(_make_run(tmp_path, proposals={"profitability": [p]}))
    assert out["proposed_change_dimension"] == "a+b"


# ---------------------------------------------------------------------------
# 2. Case A -- binding pass rule carried through verbatim
# ---------------------------------------------------------------------------

_STRONG = {"profitability": [_proposal("profitability", scores=(3, 3, 3), field="min_abs")]}


@pytest.mark.parametrize("result,hv,lr", [
    ("PASS", "promote", None),
    ("FAIL", "kill", "terminate"),
    ("FAIL", "kill", "pivot"),
    ("FAIL", "kill", "escalate"),
    ("FAIL", "refine", "refine"),
])
@pytest.mark.parametrize("discretion_shape", ["key_absent", "explicit_null"])
def test_binding_pass_rule_carried_through_verbatim(tmp_path, result, hv, lr, discretion_shape):
    extra = {} if discretion_shape == "key_absent" else {"discretion": None}
    run = _make_run(tmp_path, pass_rule=_binding(result, hv, lr, **extra), proposals=_STRONG)
    out = _synth(run)
    _assert_valid(out)
    assert out["decided_by"] == "binding_pass_rule"
    assert out["pass_rule"]["binding"] is True
    assert (out["hypothesis_verdict"], out["lineage_routing"]) == (hv, lr)
    # proposals never override the route, but a binding refine still gets its dimension
    assert out["proposed_change_dimension"] == ("min_abs" if lr == "refine" else None)
    assert out["criteria_summary"] == [{"criterion": "a", "result": result}]


@pytest.mark.parametrize("result", ["PASS", "FAIL", "SPEC_ERROR", "legacy_not_evaluable", "VERDICT_BLOCKED"])
@pytest.mark.parametrize("discretion", [None, "stage"])
@pytest.mark.parametrize("hv,lr", [(None, None), ("kill", None), (None, "terminate"), ("kill", "pivot"),
                                   ("promote", None)])
def test_pass_rule_is_binding_agrees_with_resolve_verdict_fields(result, discretion, hv, lr):
    """CODE-REVIEW REGRESSION: the binding predicate used to be inferred by
    probing _resolve_verdict_fields with a sentinel interp. It is now an
    explicit helper; this pins it to _resolve_verdict_fields's own binding
    branch so the two cannot drift."""
    pre = {"result": result, "discretion": discretion, "hypothesis_verdict": hv, "lineage_routing": lr}
    sentinel = object()
    got = rpr._resolve_verdict_fields({"hypothesis_verdict": sentinel, "lineage_routing": sentinel},
                                      "", "", pre_eval=pre)
    assert rpr._pass_rule_is_binding(pre) == (got[0] is not sentinel)
    assert rpr._pass_rule_is_binding(None) is False


@pytest.mark.parametrize("pass_rule", [
    None,  # file absent
    {"result": "FAIL", "discretion": "stage", "hypothesis_verdict": None, "lineage_routing": None,
     "statement_branch_matched": "FAIL-a", "branches_failed": ["FAIL-a"],
     "criteria_results": [{"id": "a", "result": "FAIL"}]},
    {"result": "legacy_not_evaluable", "reason": "string pass_rule"},
    {"result": "SPEC_ERROR", "reason": "x", "criteria_results": [{"id": "a", "result": "SPEC_ERROR"}]},
], ids=["absent", "discretion_stage", "legacy_not_evaluable", "spec_error"])
def test_non_binding_cases_fall_to_scoring(tmp_path, pass_rule):
    run = _make_run(tmp_path, pass_rule=pass_rule, proposals=_STRONG)
    out = _synth(run)
    _assert_valid(out)
    assert out["decided_by"] == "scored_proposals"
    assert out["pass_rule"]["binding"] is False
    assert (out["hypothesis_verdict"], out["lineage_routing"]) == ("refine", "refine")


def test_discretion_stage_overrides_a_pair_left_on_the_evaluation(tmp_path):
    """Even if a stage-discretion evaluation still carried a pair, it is not binding."""
    pr = _binding("FAIL", "kill", "terminate", discretion="stage")
    out = _synth(_make_run(tmp_path, pass_rule=pr, proposals=_STRONG))
    assert out["decided_by"] == "scored_proposals"
    assert out["lineage_routing"] == "refine"


# ---------------------------------------------------------------------------
# 3. safety checks
# ---------------------------------------------------------------------------

_GARBAGE_PROPOSALS = {"profitability.yaml": "this: [is: not, valid"}


@pytest.mark.parametrize("pass_rule", [None, _binding("PASS", "promote", None)])
def test_component_execution_error_pauses_regardless(tmp_path, pass_rule):
    run = _make_run(tmp_path, protocol=_protocol_result(component_error_count=3),
                    pass_rule=pass_rule, raw_proposals=_GARBAGE_PROPOSALS)
    out = _synth(run)  # garbage proposals never read -> no raise
    _assert_valid(out)
    assert out["decided_by"] == "safety_pause"
    assert out["pause"]["reason"] == "component_execution_error"
    assert out["pause"]["pipeline_flag"] == "component_execution_error_flagged"
    assert out["hypothesis_verdict"] is None and out["lineage_routing"] is None
    assert out["scoring"] is None
    assert any("component_errors.count=3" in e for e in out["pause"]["evidence"])


def test_component_errors_absent_is_no_evidence(tmp_path):
    pr = _protocol_result()
    for r in pr["results"]:
        del r["component_errors"]
    assert _synth(_make_run(tmp_path, protocol=pr))["decided_by"] == "scored_proposals"


@pytest.mark.parametrize("report", [_detector_report("medium"), _detector_report("low"), None],
                         ids=["medium", "low", "report_unavailable"])
@pytest.mark.parametrize("pass_rule", [None, _binding("PASS", "promote", None)])
def test_regime_misattribution_pauses_regardless(tmp_path, report, pass_rule):
    run = _make_run(tmp_path, protocol=_protocol_result(uninformative=("trending",)),
                    pass_rule=pass_rule, raw_proposals=_GARBAGE_PROPOSALS)
    out = _synth(run, report=report)
    _assert_valid(out)
    assert out["decided_by"] == "safety_pause"
    assert out["pause"]["reason"] == "regime_misattribution"
    assert out["pause"]["pipeline_flag"] == "regime_misattribution_flagged"


def test_regime_misattribution_needs_unconfirmed_detector(tmp_path):
    run = _make_run(tmp_path, protocol=_protocol_result(uninformative=("trending",)))
    assert _synth(run, report=_detector_report("high"))["decided_by"] == "scored_proposals"


def test_regime_misattribution_missing_symbol_in_report_is_unconfirmed(tmp_path):
    run = _make_run(tmp_path, protocol=_protocol_result(uninformative=("trending",)))
    report = _detector_report("high")
    report["per_symbol_per_timeframe"] = report["per_symbol_per_timeframe"][:1]  # ETHUSDT missing
    assert _synth(run, report=report)["pause"]["reason"] == "regime_misattribution"


def test_rule4_small_sample_is_not_uninformative(tmp_path):
    run = _make_run(tmp_path, protocol=_protocol_result(uninformative=("trending",), n_bars=10))
    assert _synth(run, report=_detector_report("low"))["decided_by"] == "scored_proposals"


def test_component_error_checked_before_regime(tmp_path):
    run = _make_run(tmp_path, protocol=_protocol_result(component_error_count=1, uninformative=("trending",)))
    assert _synth(run, report=None)["pause"]["reason"] == "component_execution_error"


# ---------------------------------------------------------------------------
# 4. VERDICT_BLOCKED
# ---------------------------------------------------------------------------

def test_verdict_blocked_pauses_instead_of_scoring(tmp_path):
    pr = {"result": "VERDICT_BLOCKED", "blocked_by": ["G1"], "reason": "funding not modeled"}
    out = _synth(_make_run(tmp_path, pass_rule=pr, proposals=_STRONG))
    _assert_valid(out)
    assert out["decided_by"] == "verdict_blocked"
    assert out["pause"]["reason"] == "verdict_blocked"
    assert out["hypothesis_verdict"] is None and out["scoring"] is None


# ---------------------------------------------------------------------------
# 5. fail closed
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("pass_rule", [
    {"result": "MAYBE"},
    {"result": "pass", "hypothesis_verdict": "promote", "lineage_routing": None},  # wrong case
    _binding("FAIL", "kill", "terminate", discretion="llm"),
    _binding("FAIL", "kill", "terminate", criteria_results=[{"id": "a", "result": "WEIRD"}]),
    _binding("FAIL", "kill", "terminate", criteria_results=[{"result": "FAIL"}]),
    _binding("PASS", "promote", "terminate"),         # pair outside the authority table
    _binding("FAIL", "abandon", "terminate"),         # unknown hypothesis_verdict
    _binding("FAIL", "kill", "retry"),                # unknown lineage_routing
    _binding("PASS", None, None),                     # binding result with no pair
    _binding("FAIL", "kill", "terminate", branches_failed="FAIL-a"),
    ["not", "a", "mapping"],
], ids=["unknown_result", "lowercase_result", "unknown_discretion", "unknown_criterion_result",
        "criterion_without_id", "incoherent_pair", "unknown_hv", "unknown_lr",
        "binding_without_pair", "branches_failed_not_list", "not_mapping"])
def test_unknown_or_malformed_pass_rule_fails_closed(tmp_path, pass_rule):
    run = _make_run(tmp_path, pass_rule=pass_rule, proposals=_STRONG)
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(run)


def test_unknown_pass_rule_value_not_masked_by_a_safety_pause(tmp_path):
    run = _make_run(tmp_path, protocol=_protocol_result(component_error_count=2),
                    pass_rule={"result": "MAYBE"})
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(run)


@pytest.mark.parametrize("mutate", [
    lambda pr: pr["results"][0].__setitem__("component_errors", {"count": "3"}),
    lambda pr: pr["results"][0].__setitem__("component_errors", {"count": -1}),
    lambda pr: pr["results"][0].__setitem__("component_errors", {"count": True}),
    lambda pr: pr["results"][0].__setitem__("component_errors", 5),
    lambda pr: pr.__setitem__("results", {"a": 1}),
    lambda pr: pr.pop("results"),
    lambda pr: pr["hypothesis_verdict"]["diagnostics"].__setitem__("uninformative_regimes", "trending"),
    lambda pr: pr["hypothesis_verdict"]["diagnostics"].__setitem__("median_cost_drag_pct", "142"),
    lambda pr: pr["hypothesis_verdict"]["diagnostics"].__setitem__("median_gross_pnl", float("nan")),
    lambda pr: pr["hypothesis_verdict"].__setitem__("diagnostics", "n/a"),
], ids=["count_str", "count_negative", "count_bool", "component_errors_not_mapping",
        "results_not_list", "results_missing", "uninformative_not_list", "diag_str", "diag_nan",
        "diagnostics_not_mapping"])
def test_malformed_protocol_result_fails_closed(tmp_path, mutate):
    pr = _protocol_result()
    mutate(pr)
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(_make_run(tmp_path, protocol=pr))


def test_unknown_detector_confidence_fails_closed(tmp_path):
    run = _make_run(tmp_path, protocol=_protocol_result(uninformative=("trending",)))
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(run, report=_detector_report("very_high"))


def test_missing_required_inputs_and_family(tmp_path):
    run = _make_run(tmp_path)
    with pytest.raises(rpr.VerdictSynthesisError):
        rpr._synthesize_verdict(run, "  ", _detector_report())
    (run / "artifacts" / "hypothesis_card.yaml").unlink()
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(run)


def _bad(mutator):
    p = _proposal("profitability", scores=(3, 3, 3))
    mutator(p)
    return yaml.safe_dump([p])


@pytest.mark.parametrize("files", [
    {"profitability.yaml": "- proposal_id: [unclosed"},                        # unparseable
    {"profitability.yaml": ""},                                                 # empty / null doc
    {"profitability.yaml": yaml.safe_dump({"proposal_id": "x"})},              # mapping not list
    {"profitability.yaml": yaml.safe_dump(["just a string"])},                 # entry not mapping
    {"profitability.yaml": _bad(lambda p: p["scores"].__setitem__("confidence_real", 4))},
    {"profitability.yaml": _bad(lambda p: p["scores"].__setitem__("confidence_real", True))},
    {"profitability.yaml": _bad(lambda p: p["scores"].__setitem__("confidence_real", 2.0))},
    {"profitability.yaml": _bad(lambda p: p["scores"].pop("mechanism_plausibility"))},
    {"profitability.yaml": _bad(lambda p: p["scores"].__setitem__("extra", 1))},
    {"profitability.yaml": _bad(lambda p: p.__setitem__("proposal_id", "regime_power-run_test-1"))},
    {"profitability.yaml": _bad(lambda p: p.__setitem__("kind", "tweak"))},
    {"profitability.yaml": _bad(lambda p: p.__setitem__("block", {"kind": "forecast"}))},
    {"profitability.yaml": _bad(lambda p: p.__setitem__("patch", []))},
    {"profitability.yaml": _bad(lambda p: p.__setitem__("patch", [{"component_id": "k", "after": 1}]))},
    {"profitability.yaml": _bad(lambda p: p.__setitem__("evidence", []))},
    {"profitability.yaml": _bad(lambda p: p.__setitem__("hypothesis_verdict", "promote"))},
    {"profitability.yaml": _bad(lambda p: p.pop("model_id"))},
    {"profitability.yaml": yaml.safe_dump([_proposal("profitability"), _proposal("profitability")])},
    {"profitability.yaml": "[]", "profitability_v2.yaml": "[]"},                # unexpected file
    {"profitability.yml": "[]"},                                                # wrong extension
], ids=["unparseable", "empty_file", "mapping", "entry_not_mapping", "score_out_of_range",
        "score_bool", "score_float", "score_missing", "score_extra", "foreign_category_id",
        "unknown_kind", "patch_and_block", "empty_patch", "patch_item_without_field",
        "empty_evidence", "smuggled_routing_field", "missing_model_id", "duplicate_id",
        "unexpected_file", "wrong_extension"])
def test_malformed_proposal_file_fails_loud(tmp_path, files):
    run = _make_run(tmp_path, raw_proposals=files)
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(run)


def test_malformed_losing_proposal_still_fails_loud(tmp_path):
    """A malformed proposal must not be silently skipped just because it would not win."""
    bad = _proposal("regime_power", scores=(0, 0, 0))
    bad["patch"] = [{"component_id": "k"}]  # no field
    run = _make_run(tmp_path, proposals={"profitability": [_proposal("profitability", scores=(3, 3, 3))],
                                         "regime_power": [bad]})
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(run)


def test_malformed_proposal_fails_loud_even_under_binding_pass_rule(tmp_path):
    run = _make_run(tmp_path, pass_rule=_binding("FAIL", "kill", "terminate"),
                    raw_proposals={"profitability.yaml": "{}"})
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(run)


# ---------------------------------------------------------------------------
# 6. schema
# ---------------------------------------------------------------------------

def test_schema_is_itself_valid_and_closed_everywhere():
    jsonschema.Draft202012Validator.check_schema(SCHEMA)

    def walk(node, where):
        if isinstance(node, dict):
            if node.get("type") == "object" and "properties" in node:
                assert node.get("additionalProperties") is False, f"{where} lacks additionalProperties: false"
            for k, v in node.items():
                walk(v, f"{where}/{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{where}[{i}]")
    walk(SCHEMA, "#")


def _sample_outputs(tmp_path):
    outs = []
    outs.append(_synth(_make_run(tmp_path / "a", proposals=_STRONG)))
    outs.append(_synth(_make_run(tmp_path / "b", protocol=_protocol_result(component_error_count=1))))
    outs.append(_synth(_make_run(tmp_path / "c", pass_rule=_binding("FAIL", "kill", "pivot"), proposals=_STRONG)))
    return outs


@pytest.mark.parametrize("path", [
    (), ("pass_rule",), ("diagnostic_snapshot",), ("scoring",), ("scoring", "winner"),
    ("scoring", "winner", "scores"), ("scoring", "proposal_counts"), ("criteria_summary", 0),
], ids=lambda p: "/".join(map(str, p)) or "top")
def test_smuggled_field_rejected_at_every_level(tmp_path, path):
    out = _sample_outputs(tmp_path)[0]
    out["criteria_summary"] = [{"criterion": "a", "result": "FAIL"}]
    _assert_valid(out)
    bad = copy.deepcopy(out)
    node = bad
    for key in path:
        node = node[key]
    node["smuggled"] = "x"
    assert list(VALIDATOR.iter_errors(bad)), f"smuggled field at {path} was accepted"


def test_smuggled_field_in_pause_rejected(tmp_path):
    out = _sample_outputs(tmp_path)[1]
    _assert_valid(out)
    bad = copy.deepcopy(out)
    bad["pause"]["smuggled"] = 1
    assert list(VALIDATOR.iter_errors(bad))


@pytest.mark.parametrize("mutate", [
    lambda o: o.__setitem__("hypothesis_verdict", "refine"),        # paused but carries a verdict
    lambda o: o.__setitem__("decided_by", "scored_proposals"),      # pause with non-pause decider
    lambda o: o["pause"].__setitem__("reason", "verdict_blocked"),  # safety_pause w/ wrong reason
])
def test_schema_conditionals_on_paused_output(tmp_path, mutate):
    out = _sample_outputs(tmp_path)[1]
    bad = copy.deepcopy(out)
    mutate(bad)
    assert list(VALIDATOR.iter_errors(bad))


@pytest.mark.parametrize("mutate", [
    lambda o: o.__setitem__("lineage_routing", "terminate"),      # promote/terminate-style incoherence
    lambda o: o["pass_rule"].__setitem__("binding", True),         # scored but claims binding
    lambda o: o.__setitem__("pause", {"reason": "verdict_blocked", "pipeline_flag": "verdict_blocked_flagged",
                                      "evidence": ["x"]}),
])
def test_schema_conditionals_on_verdict_output(tmp_path, mutate):
    out = _sample_outputs(tmp_path)[0]   # scored refine/refine
    bad = copy.deepcopy(out)
    mutate(bad)
    assert list(VALIDATOR.iter_errors(bad))


def test_schema_binding_path_must_claim_binding(tmp_path):
    out = _sample_outputs(tmp_path)[2]   # binding kill/pivot
    _assert_valid(out)
    bad = copy.deepcopy(out)
    bad["pass_rule"]["binding"] = False
    assert list(VALIDATOR.iter_errors(bad))


# ---------------------------------------------------------------------------
# 7. purity + legacy-consumer compatibility
# ---------------------------------------------------------------------------

def test_synthesis_writes_nothing(tmp_path):
    run = _make_run(tmp_path, pass_rule=_binding("FAIL", "refine", "refine"), proposals=_STRONG)
    before = sorted((p.relative_to(run), p.stat().st_mtime_ns) for p in run.rglob("*"))
    _synth(run)
    after = sorted((p.relative_to(run), p.stat().st_mtime_ns) for p in run.rglob("*"))
    assert before == after


def test_rationale_parses_through_legacy_carryover_regexes(tmp_path):
    """5b-ii-B will feed these fields to _auto_generate_findings_carryover; its
    regex scrape of altitude_justification must recover the exact numbers."""
    run = _make_run(tmp_path, proposals=_STRONG)
    out = _synth(run)
    interp = {
        "hypothesis_id": out["hypothesis_id"],
        "altitude_justification": out["rationale"],
        "criteria_summary": out["criteria_summary"],
        "proposed_change_dimension": out["proposed_change_dimension"],
        "hypothesis_family": out["hypothesis_family"],
    }
    rpr._auto_generate_findings_carryover(run, interp, out["lineage_routing"])
    carry = yaml.safe_load((run / "artifacts" / "findings_carryover.yaml").read_text(encoding="utf-8"))
    assert carry["diagnostic_snapshot"] == {"forecast_return_corr": 0.0412,
                                            "cost_drag_pct": 142.82, "gross_pnl": -3.5}
    assert carry["diagnostic_rule_applied"].startswith("scored_proposals")
    assert "min_abs" in carry["what_not_to_try"][0]


# ---------------------------------------------------------------------------
# CODE-REVIEW REGRESSIONS (2026-09-23 review of b9e0da6d)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("label", ["NOT_READY", " not_ready "])
def test_warmup_label_never_triggers_regime_misattribution(tmp_path, label):
    """build_regime_validity groups warmup bars too, so NOT_READY shows up in
    uninformative_regimes in real runs (runs 014-023, ~119 bars). It is not a
    detector regime and must not pause the run."""
    run = _make_run(tmp_path, protocol=_protocol_result(uninformative=(label,), n_bars=119))
    out = _synth(run, report=_detector_report("low"))
    assert out["decided_by"] != "safety_pause"
    _assert_valid(out)


def test_warmup_label_does_not_shield_a_real_uninformative_regime(tmp_path):
    run = _make_run(tmp_path, protocol=_protocol_result(uninformative=("NOT_READY", "trending"), n_bars=119))
    out = _synth(run, report=_detector_report("low"))
    assert out["decided_by"] == "safety_pause"
    assert out["pause"]["reason"] == "regime_misattribution"
    assert not any("NOT_READY" in e for e in out["pause"]["evidence"])


@pytest.mark.parametrize("bad", [float("nan"), float("inf")])
def test_non_finite_n_bars_fails_loud(tmp_path, bad):
    """A NaN median made `>= 20` False and silently dropped the RULE 4 regime."""
    run = _make_run(tmp_path, protocol=_protocol_result(uninformative=("trending",), n_bars=bad))
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(run, report=_detector_report("low"))


@pytest.mark.parametrize("report", [
    {"per_symbol_per_timeframe": [{"symbol": "BTCUSDT", "timeframe": "1h", "confidence": "bogus"}]},
    [1, 2],
    {"per_symbol_per_timeframe": "nope"},
])
def test_malformed_detector_report_fails_loud_even_without_rule4(tmp_path, report):
    run = _make_run(tmp_path)  # no uninformative regime -> RULE 4 never fires
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(run, report=report)


def test_unknown_binding_pair_is_not_hidden_behind_a_safety_pause(tmp_path):
    run = _make_run(tmp_path, protocol=_protocol_result(component_error_count=1),
                    pass_rule=_binding("FAIL", "abandon", "retry"))
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(run)


def test_unknown_pair_is_not_hidden_behind_verdict_blocked(tmp_path):
    run = _make_run(tmp_path, pass_rule={"result": "VERDICT_BLOCKED", "hypothesis_verdict": "abandon",
                                         "lineage_routing": None, "blocked_by": ["G5"]})
    # VERDICT_BLOCKED is not binding, so the pair is not carried; it must still
    # not be accepted as a valid verdict on the blocked path.
    out = _synth(run)
    assert out["decided_by"] == "verdict_blocked"
    assert out["hypothesis_verdict"] is None


def test_fail_result_with_promote_verdict_fails_loud(tmp_path):
    """A mis-registered FAIL branch carrying promote would spend the holdout."""
    run = _make_run(tmp_path, pass_rule=_binding("FAIL", "promote", None))
    with pytest.raises(rpr.VerdictSynthesisError, match="FAIL"):
        _synth(run)


@pytest.mark.parametrize("field,value", [("result", ["PASS"]), ("hypothesis_verdict", ["kill"]),
                                         ("lineage_routing", {"a": 1}), ("discretion", ["stage"])])
def test_unhashable_pass_rule_values_raise_synthesis_error_not_typeerror(tmp_path, field, value):
    pr = _binding("FAIL", "kill", "terminate")
    pr[field] = value
    run = _make_run(tmp_path, pass_rule=pr)
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(run)


def test_binding_refine_without_proposals_gets_unspecified_dimension(tmp_path):
    """dim=None would make the circuit breaker's `dim in recent_dims` never
    match, so repeated unexplained refines would never trip it."""
    run = _make_run(tmp_path, pass_rule=_binding("FAIL", "refine", "refine"))
    out = _synth(run)
    assert out["decided_by"] == "binding_pass_rule"
    assert out["proposed_change_dimension"] == rpr.SYNTHESIS_UNSPECIFIED_DIMENSION
    _assert_valid(out)


def test_binding_refine_ignores_a_zero_score_winner_for_the_dimension(tmp_path):
    run = _make_run(tmp_path, pass_rule=_binding("FAIL", "refine", "refine"),
                    proposals={"profitability": [_proposal("profitability", scores=(0, 0, 0))]})
    out = _synth(run)
    assert out["proposed_change_dimension"] == rpr.SYNTHESIS_UNSPECIFIED_DIMENSION


def test_binding_refine_uses_an_evidence_bearing_winner_for_the_dimension(tmp_path):
    run = _make_run(tmp_path, pass_rule=_binding("FAIL", "refine", "refine"),
                    proposals={"profitability": [_proposal("profitability", scores=(1, 0, 0), field="weight")]})
    assert _synth(run)["proposed_change_dimension"] == "weight"


@pytest.mark.parametrize("litter", [".DS_Store", "profitability.yaml~", "notes.txt"])
def test_os_and_editor_litter_in_proposals_dir_is_ignored(tmp_path, litter):
    run = _make_run(tmp_path, raw_proposals={"profitability.yaml": "[]", litter: "junk"})
    assert _synth(run)["decided_by"] == "scored_proposals"


@pytest.mark.parametrize("pid", ["profitability-", "profitability-run_1", "profitability-run_1-x"])
def test_proposal_id_must_match_full_schema_pattern(tmp_path, pid):
    run = _make_run(tmp_path, raw_proposals={
        "profitability.yaml": _bad(lambda p: p.__setitem__("proposal_id", pid))})
    with pytest.raises(rpr.VerdictSynthesisError):
        _synth(run)


@pytest.mark.parametrize("mutate", [
    lambda o: o.__setitem__("proposed_change_dimension", "weight"),        # terminate + dimension
    lambda o: o.__setitem__("pass_rule", {**o["pass_rule"], "result": "VERDICT_BLOCKED"}),  # binding w/o PASS/FAIL
])
def test_schema_rejects_inconsistent_outputs(tmp_path, mutate):
    run = _make_run(tmp_path, pass_rule=_binding("FAIL", "kill", "terminate"))
    out = _synth(run)
    _assert_valid(out)
    bad = copy.deepcopy(out)
    mutate(bad)
    assert list(VALIDATOR.iter_errors(bad)), "schema accepted an inconsistent output"


def test_schema_rejects_refine_without_dimension(tmp_path):
    run = _make_run(tmp_path, proposals={"profitability": [_proposal("profitability")]})
    out = _synth(run)
    assert out["lineage_routing"] == "refine"
    bad = copy.deepcopy(out)
    bad["proposed_change_dimension"] = None
    assert list(VALIDATOR.iter_errors(bad))


def test_schema_rejects_fail_plus_promote(tmp_path):
    run = _make_run(tmp_path, pass_rule=_binding("PASS", "promote", None))
    out = _synth(run)
    bad = copy.deepcopy(out)
    bad["pass_rule"]["result"] = "FAIL"
    assert list(VALIDATOR.iter_errors(bad))
