"""
K2 kernel (C7): machine-checkable pass-rule evaluator.

Reads a run's already-computed protocol_result.yaml (per_symbol_summary,
trade_diagnostics_summary -- both computed by tools/run_protocol.py from
real bars.csv/trades.json, never recomputed here) and pre_registration.yaml's
structured pass_rule.criteria/outcomes (B11/C7 schema), and resolves the
pre-registered verdict deterministically -- no keyword matching, no prose
parsing, no LLM involvement. Replaces tools/run_protocol.py's
evaluate_against_decision_rules() as the DECISION authority; that function's
prose-criteria output (validation_protocol.yaml-derived) remains
informational only from here on (see design note section 6).

See docs/design/K2_verdict_machinery_design_20260713.md sections 6 and 8.
"""
from __future__ import annotations

_VALID_COMPARATORS = (">=", ">", "<=", "<", "==")


def _apply_comparator(op: str, actual: float, threshold: float) -> bool:
    if op == ">=":
        return actual >= threshold
    if op == ">":
        return actual > threshold
    if op == "<=":
        return actual <= threshold
    if op == "<":
        return actual < threshold
    if op == "==":
        return actual == threshold
    raise ValueError(f"unknown comparator {op!r}")


def _lookup_metric_value(protocol_result: dict, criterion: dict, symbol: str | None):
    """Reads an already-computed statistic from protocol_result.yaml.
    Per-symbol criteria (symbol is not None) read
    per_symbol_summary[symbol][metric]; pooled criteria read
    trade_diagnostics_summary[metric][statistic], falling back to
    hypothesis_verdict.diagnostics[metric] (both shapes are present,
    identically, in a real run_protocol.py output -- confirmed against
    run_057's own protocol_result.yaml)."""
    metric = criterion["metric"]
    if symbol is not None:
        per_symbol_summary = protocol_result.get("per_symbol_summary") or {}
        return (per_symbol_summary.get(symbol) or {}).get(metric)

    statistic = criterion.get("statistic")
    tds = protocol_result.get("trade_diagnostics_summary") or {}
    if metric in tds:
        val = tds[metric]
        if isinstance(val, dict) and statistic:
            return val.get(statistic)
        return val
    hv_diag = (protocol_result.get("hypothesis_verdict") or {}).get("diagnostics") or {}
    if metric in hv_diag:
        val = hv_diag[metric]
        if isinstance(val, dict) and statistic:
            return val.get(statistic)
        return val
    return None


def _evaluate_one_criterion(criterion: dict, protocol_result: dict) -> dict:
    metric = criterion.get("metric")
    comparator = criterion.get("comparator")
    if not metric or comparator not in _VALID_COMPARATORS:
        return {"id": criterion.get("id"), "result": "SPEC_ERROR",
                "reason": f"criterion missing metric or invalid comparator {comparator!r}"}

    per_symbol_threshold = criterion.get("per_symbol_threshold")
    null_handling = criterion.get("null_handling")

    if per_symbol_threshold:
        per_symbol_results = {}
        overall = "PASS"
        for symbol, threshold in per_symbol_threshold.items():
            value = _lookup_metric_value(protocol_result, criterion, symbol)
            if value is None:
                if null_handling == "fails_threshold":
                    # A3.4: a null aggregate (e.g. every window below the trade
                    # floor) is a DEFINED outcome the pre-registered rule itself
                    # anticipates -- it can never satisfy a ">=" floor, so it
                    # resolves to a real, reasoned FAIL, never UNTESTED. This is
                    # the exact fix for run_057's own BTCUSDT gap (design note
                    # section 3): the value is present-and-null, not absent.
                    per_symbol_results[symbol] = {
                        "value": None, "threshold": threshold, "result": "FAIL",
                        "reason": (f"{symbol} {metric} is null (A3.4: all windows below "
                                   f"the trade floor) -- a null aggregate cannot satisfy "
                                   f"{comparator} {threshold}, resolved as FAIL per the "
                                   f"pre-registered null_handling policy"),
                    }
                    overall = "FAIL"
                else:
                    per_symbol_results[symbol] = {
                        "value": None, "threshold": threshold, "result": "SPEC_ERROR",
                        "reason": (f"{symbol} {metric} is null and this criterion has no "
                                   f"null_handling policy -- pre_registration.yaml is "
                                   f"missing a required field for this criterion"),
                    }
                    if overall != "FAIL":
                        overall = "SPEC_ERROR"
                continue
            met = _apply_comparator(comparator, value, threshold)
            result = "PASS" if met else "FAIL"
            per_symbol_results[symbol] = {"value": value, "threshold": threshold, "result": result}
            if result == "FAIL":
                overall = "FAIL"
        return {"id": criterion.get("id"), "result": overall, "per_symbol": per_symbol_results}

    threshold = criterion.get("threshold")
    value = _lookup_metric_value(protocol_result, criterion, None)
    if value is None:
        if null_handling == "fails_threshold":
            return {"id": criterion.get("id"), "result": "FAIL", "value": None,
                    "threshold": threshold,
                    "reason": f"{metric} is null -- cannot satisfy {comparator} {threshold}"}
        return {"id": criterion.get("id"), "result": "SPEC_ERROR", "value": None,
                "reason": f"{metric} is null and this criterion has no null_handling policy"}
    met = _apply_comparator(comparator, value, threshold)
    return {"id": criterion.get("id"), "result": "PASS" if met else "FAIL",
            "value": value, "threshold": threshold}


def evaluate_pass_rule_criteria(protocol_result: dict, pre_registration: dict) -> dict:
    """
    Evaluates a run's protocol_result.yaml against pre_registration.yaml's
    structured pass_rule (B11/C7 schema). Returns a dict written verbatim
    into runs/<id>/artifacts/pass_rule_evaluation.yaml by the caller.

    R3 (K2 Phase B operator ruling): if pass_rule is a plain string (the
    LEGACY schema -- every run's pre_registration.yaml before this kernel,
    including run_057's own, per the design note's section 3) this function
    NEVER raises -- it returns an explicit, named 'legacy_not_evaluable'
    result so a caller can route the run to the LLM stage's own judgment
    exactly as before, rather than crashing the pipeline.
    """
    pass_rule = pre_registration.get("pass_rule")
    if pass_rule is None:
        return {"result": "legacy_not_evaluable",
                "reason": "pre_registration.yaml has no pass_rule field at all"}
    if isinstance(pass_rule, str):
        return {"result": "legacy_not_evaluable",
                "reason": ("pass_rule is a plain string (pre-K2 legacy schema), not the "
                           "structured {statement, criteria, outcomes} shape -- this run's "
                           "verdict is not machine-evaluable; falls through to the LLM "
                           "stage's own judgment, unchanged from pre-K2 behavior")}
    if not isinstance(pass_rule, dict):
        return {"result": "legacy_not_evaluable",
                "reason": f"pass_rule is neither a string nor a dict (got {type(pass_rule).__name__})"}

    criteria = pass_rule.get("criteria") or []
    outcomes = pass_rule.get("outcomes") or []
    if not criteria or not outcomes:
        return {"result": "legacy_not_evaluable",
                "reason": ("pass_rule is dict-shaped but missing criteria or outcomes -- "
                           "not a conformant K2 structured pass rule")}

    # A3 (K2 Phase B operator amendment): NAME-level window_set_ref check
    # only. Content-hash pinning (verifying the actual window set's
    # bytes/hash, not just its file name, matches what was pre-registered)
    # is B3/B10 scope (K3), not this kernel -- a name mismatch refuses
    # evaluation; a matching name is NOT verified byte-for-byte against
    # protocol_result.yaml's actual window contents here.
    window_set_ref = pass_rule.get("window_set_ref")
    protocol_file = protocol_result.get("protocol_file")
    if window_set_ref and protocol_file:
        ref_name = str(window_set_ref).replace("\\", "/").rsplit("/", 1)[-1]
        actual_name = str(protocol_file).replace("\\", "/").rsplit("/", 1)[-1]
        if ref_name != actual_name:
            return {"result": "SPEC_ERROR",
                    "reason": (f"window_set_ref={window_set_ref!r} (pre-registered) != "
                               f"protocol_file={protocol_file!r} (actually executed) -- "
                               f"refusing to evaluate a pass rule against a mismatched "
                               f"protocol/window set (name-level check only; K3/B3+B10 "
                               f"adds content-hash pinning)")}

    criteria_results = [_evaluate_one_criterion(c, protocol_result) for c in criteria]

    fail_ids = [r["id"] for r in criteria_results if r["result"] == "FAIL"]
    spec_error_ids = [r["id"] for r in criteria_results if r["result"] == "SPEC_ERROR"]

    if spec_error_ids and not fail_ids:
        return {
            "result": "SPEC_ERROR",
            "criteria_results": criteria_results,
            "reason": (f"criteria {spec_error_ids} could not be evaluated (missing "
                       f"null_handling or unresolvable metric) -- pre_registration.yaml "
                       f"needs correction"),
        }

    outcomes_by_branch = {o["branch"]: o for o in outcomes}
    # branches_failed (operator amendment A1): every failing branch, never
    # hidden, even though id-order resolution below picks only the first.
    branches_failed = [f"FAIL-{fid}" for fid in fail_ids]

    if not fail_ids:
        pass_branch = outcomes_by_branch.get("PASS")
        if pass_branch is None:
            return {"result": "legacy_not_evaluable", "criteria_results": criteria_results,
                     "branches_failed": [],
                     "reason": "all criteria PASS but pre_registration.yaml's outcomes has no 'PASS' branch"}
        return {
            "result": "PASS",
            "criteria_results": criteria_results,
            "branches_failed": [],
            "statement_branch_matched": "PASS",
            "hypothesis_verdict": pass_branch.get("hypothesis_verdict"),
            "lineage_routing": pass_branch.get("lineage_routing"),
        }

    # A1: id-order resolution -- the FIRST failing criterion (in the
    # criteria list's own order) selects the matched branch. This is a
    # real, order-sensitive decision, documented explicitly (not implicit)
    # via the warning below when it matters.
    statement_branch_matched = branches_failed[0]
    matched_outcome = outcomes_by_branch.get(statement_branch_matched)
    if matched_outcome is None:
        return {"result": "legacy_not_evaluable", "criteria_results": criteria_results,
                "branches_failed": branches_failed,
                "reason": (f"criterion {fail_ids[0]!r} FAILed but pre_registration.yaml's "
                           f"outcomes has no {statement_branch_matched!r} branch -- B11 "
                           f"lint should have caught this at materialization time")}

    result = {
        "result": "FAIL",
        "criteria_results": criteria_results,
        "branches_failed": branches_failed,
        "statement_branch_matched": statement_branch_matched,
        "hypothesis_verdict": matched_outcome.get("hypothesis_verdict"),
        "lineage_routing": matched_outcome.get("lineage_routing"),
    }

    if matched_outcome.get("discretion") == "stage":
        # B11's opt-in escape hatch: this branch has no fixed pair -- the
        # LLM stage decides, from A8's vocabulary only (never free text).
        result["discretion"] = "stage"
        result["hypothesis_verdict"] = None
        result["lineage_routing"] = None

    # A1 (operator amendment): multiple FAIL branches with DIFFERING verdict
    # pairs is a WARNING -- order is deciding the outcome, and the brief's
    # author must know that at registration time.
    if len(fail_ids) > 1:
        distinct_pairs = {
            (outcomes_by_branch[b].get("hypothesis_verdict"), outcomes_by_branch[b].get("lineage_routing"))
            for b in branches_failed if b in outcomes_by_branch
        }
        if len(distinct_pairs) > 1:
            result["warning"] = (
                f"multiple FAIL branches ({branches_failed}) carry DIFFERING "
                f"hypothesis_verdict/lineage_routing pairs; id-order resolution selected "
                f"{statement_branch_matched!r} -- confirm this ordering is intentional"
            )

    return result
