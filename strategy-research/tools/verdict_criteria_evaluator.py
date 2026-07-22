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

C7-EXT (2026-07-22, XS_momentum ungated-verdict incident) adds seven gates on
top of the K2 kernel. See the VERDICT PRECONDITIONS section below and ledger
entry C7-EXT in PIPELINE_IMPROVEMENTS_20260712_v4.md for the four-link defect
chain each gate closes.
"""
from __future__ import annotations

_VALID_COMPARATORS = (">=", ">", "<=", "<", "==")

# C7-EXT: the four verdict PRECONDITIONS (G1-G4). Enumerated for callers/tests.
VERDICT_PRECONDITION_IDS = (
    "cost_model_completeness",   # G1
    "distribution_stats",        # G2
    "deployable_today",          # G3
    "robustness_mechanism",      # G4
)

# Default perp funding interval, in hours. Overridable per-brief via
# research_brief["funding_interval_hours"]. 8h is the convention on every venue
# in docs/venue_survey_20260719.md (Binance / Kraken / Bybit perps).
_DEFAULT_FUNDING_INTERVAL_HOURS = 8.0

# G6: a KB/queue verdict field is admissible ONLY with evaluator provenance.
_VERDICT_FIELDS = ("verdict_c7", "hypothesis_verdict", "verdict")


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


# ---------------------------------------------------------------------------
# VERDICT PRECONDITIONS -- C7-EXT (2026-07-22)
#
# The XS_momentum incident: a verdict ("REFINE") was issued for a hypothesis
# with NO pre-registered pass_rule at all, produced off the orchestrator by a
# research-path tool, and each of the four checks below was missing without
# anything in the machinery noticing.
#
# G5 is the structural fix: these preconditions evaluate INDEPENDENTLY of
# whether a pass_rule exists, and DOMINATE the result. An unmet precondition
# yields `VERDICT_BLOCKED` -- not PASS, not FAIL, and specifically NOT
# `legacy_not_evaluable`, which was the hole: `legacy_not_evaluable` routes a
# rule-less run to stage discretion, and stage discretion has no idea these
# checks exist. A blocked verdict is not a failed hypothesis; it is a
# hypothesis whose evidence is not yet admissible for ANY verdict.
# ---------------------------------------------------------------------------


def _blocked(gate_id: str, reason: str, remedy: str) -> dict:
    return {"id": gate_id, "result": "BLOCKED", "reason": reason, "remedy": remedy}


def _met(gate_id: str, reason: str) -> dict:
    return {"id": gate_id, "result": "MET", "reason": reason}


def _bar_hours(research_brief: dict) -> float:
    tf = str(research_brief.get("timeframe") or "1h").strip().lower()
    try:
        if tf.endswith("h"):
            return float(tf[:-1])
        if tf.endswith("m"):
            return float(tf[:-1]) / 60.0
        if tf.endswith("d"):
            return float(tf[:-1]) * 24.0
    except ValueError:
        pass
    return 1.0


def _holding_period_hours(protocol_result: dict, research_brief: dict):
    """Best-available holding-period estimate, in hours. Returns None when no
    field resolves -- which G1 treats as BLOCKED, never as 'short enough': an
    unmeasured holding period cannot demonstrate that positions close inside
    the funding interval."""
    diag = (protocol_result.get("hypothesis_verdict") or {}).get("diagnostics") or {}
    tds = protocol_result.get("trade_diagnostics_summary") or {}
    for src in (diag, tds, protocol_result):
        for key in ("median_holding_hours", "avg_holding_hours",
                    "median_holding_period_hours"):
            val = src.get(key)
            if isinstance(val, (int, float)):
                return float(val)
        for key in ("avg_trade_duration_bars", "median_trade_duration_bars"):
            val = src.get(key)
            if isinstance(val, (int, float)):
                return float(val) * _bar_hours(research_brief)
    # A rebalance cadence upper-bounds a fully-rebalanced book's holding period
    # (a daily-rebalanced position is held ~24h).
    reb = research_brief.get("rebalance_hours")
    if isinstance(reb, (int, float)):
        return float(reb)
    return None


def _gate_cost_model_completeness(protocol_result: dict, pre_registration: dict,
                                  research_brief: dict) -> dict:
    """G1 -- cost-model completeness. If product is a perp AND the holding
    period exceeds the funding interval, funding must be MODELED or explicitly
    BOUNDED with a cited magnitude. Otherwise the verdict is BLOCKED, not
    passed. XS_momentum: perp product, daily rebalance (24h) against an 8h
    funding interval, funding not modeled -- three funding accruals per
    holding period went uncosted and the verdict issued anyway."""
    gid = "cost_model_completeness"
    product = str(research_brief.get("product") or "").strip().lower()
    if product not in ("perp", "perpetual", "perpetual_future", "swap"):
        return _met(gid, f"product={product!r} is not a perp -- funding does not apply")

    interval = research_brief.get("funding_interval_hours") or _DEFAULT_FUNDING_INTERVAL_HOURS
    holding = _holding_period_hours(protocol_result, research_brief)
    if holding is None:
        return _blocked(
            gid,
            "product is a perp but no holding-period statistic resolved from "
            "protocol_result.yaml (median/avg holding hours, trade duration bars) "
            "nor a rebalance cadence from the brief -- cannot establish that "
            "positions close inside the funding interval",
            "record a holding-period statistic, or model/bound funding unconditionally",
        )
    if holding <= interval:
        return _met(gid, f"perp holding period {holding}h <= funding interval "
                         f"{interval}h -- positions close before funding accrues")

    cm = (pre_registration.get("cost_model_completeness")
          or protocol_result.get("cost_model_completeness") or {})
    funding = cm.get("funding") or {}
    treatment = str(funding.get("treatment") or "").strip().lower()
    if treatment == "modeled":
        return _met(gid, f"perp holding period {holding}h > funding interval "
                         f"{interval}h and funding treatment=modeled")
    if treatment == "bounded":
        bound = funding.get("bound_bps_per_interval")
        citation = funding.get("citation")
        if not isinstance(bound, (int, float)) or not citation:
            return _blocked(
                gid,
                f"funding treatment=bounded but the bound is incomplete "
                f"(bound_bps_per_interval={bound!r}, citation={citation!r}) -- an "
                f"uncited or absent magnitude is not a bound",
                "supply bound_bps_per_interval AND a citation for it",
            )
        return _met(gid, f"perp holding period {holding}h > funding interval "
                         f"{interval}h; funding bounded at {bound} bps/interval "
                         f"({citation})")
    return _blocked(
        gid,
        f"product=perp with holding period {holding}h > funding interval "
        f"{interval}h, but cost_model_completeness.funding.treatment is "
        f"{treatment!r} -- funding is neither modeled nor explicitly bounded, so "
        f"the reported net figures omit a cost the strategy actually pays",
        "set funding.treatment to 'modeled', or to 'bounded' with "
        "bound_bps_per_interval + citation",
    )


def _gate_distribution_stats(protocol_result: dict) -> dict:
    """G2 -- distribution statistics are mandatory alongside any Sharpe. A
    Sharpe reported alone is a second-moment summary standing in for a
    distribution it cannot describe; it cannot distinguish a smooth edge from
    a short-volatility payoff."""
    gid = "distribution_stats"
    diag = (protocol_result.get("hypothesis_verdict") or {}).get("diagnostics") or {}
    tds = protocol_result.get("trade_diagnostics_summary") or {}
    sources = (diag, tds, protocol_result)

    def _present(names):
        return any(src.get(n) is not None for src in sources for n in names)

    if not _present(("median_sharpe", "sharpe", "net_sharpe", "sharpe_ratio",
                     "net_sharpe_full_sample")):
        return _met(gid, "no Sharpe reported -- distribution stats not required")

    missing = []
    if not _present(("skew", "skewness", "return_skew")):
        missing.append("skew")
    if not _present(("kurtosis", "excess_kurtosis", "return_kurtosis")):
        missing.append("kurtosis")
    if not _present(("worst_period_return_pct", "tail_ratio", "cvar_95",
                     "worst_month_return_pct", "var_95")):
        missing.append("a tail statistic (worst_period_return_pct / cvar_95 / tail_ratio)")
    if missing:
        return _blocked(
            gid,
            f"a Sharpe is reported but these distribution statistics are absent: "
            f"{', '.join(missing)} -- Sharpe alone cannot distinguish a smooth edge "
            f"from a short-volatility payoff",
            "report skew, kurtosis, and at least one tail statistic alongside every Sharpe",
        )
    return _met(gid, "skew, kurtosis and a tail statistic accompany the reported Sharpe")


def _gate_deployable_today(protocol_result: dict) -> dict:
    """G3 -- a 'deployable-today' figure (most recent FULL year, at CURRENT
    costs) is mandatory on every verdict. XS_momentum's headline 1.325 was
    dominated by 2017/2020; its most recent full year was 0.07. Both are true;
    only one is deployable, and only the headline reached the verdict."""
    gid = "deployable_today"
    dt = protocol_result.get("deployable_today")
    if not isinstance(dt, dict):
        return _blocked(
            gid,
            "protocol_result.yaml has no `deployable_today` block -- the verdict "
            "rests on full-sample statistics with no statement of what the "
            "strategy earned in the most recent full year at today's costs",
            "add deployable_today: {year, net_sharpe, net_return_pct, cost_basis}",
        )
    missing = [k for k in ("year", "net_sharpe", "cost_basis") if dt.get(k) is None]
    if missing:
        return _blocked(
            gid,
            f"`deployable_today` is present but missing required field(s): "
            f"{', '.join(missing)}",
            "populate year (most recent FULL year), net_sharpe, and cost_basis "
            "(the current-cost schedule used)",
        )
    return _met(gid, f"deployable_today: {dt.get('year')} net_sharpe="
                     f"{dt.get('net_sharpe')} at cost_basis={dt.get('cost_basis')!r}")


def _gate_robustness_mechanism(protocol_result: dict) -> dict:
    """G4 -- any robustness check flagged anomalous requires a WRITTEN
    mechanism explanation before the verdict stands. XS_momentum's lag test
    had net Sharpe RISING with execution delay (1.33 -> 1.42 -> 1.51); that
    was read as 'no lookahead' and passed over. An unexplained anomaly that
    happens to point the convenient direction is the most dangerous kind."""
    gid = "robustness_mechanism"
    checks = protocol_result.get("robustness_checks") or []
    if isinstance(checks, dict):
        checks = [dict(v, id=k) for k, v in checks.items() if isinstance(v, dict)]
    unexplained = []
    for chk in checks:
        if not isinstance(chk, dict):
            continue
        if not chk.get("anomalous"):
            continue
        expl = chk.get("mechanism_explanation")
        if not (isinstance(expl, str) and expl.strip()):
            unexplained.append(chk.get("id") or chk.get("name") or "<unnamed>")
    if unexplained:
        return _blocked(
            gid,
            f"robustness check(s) {unexplained} are flagged anomalous with no "
            f"`mechanism_explanation` -- an unexplained anomaly is an open "
            f"question about the result's validity, not a footnote to it",
            "write a mechanism_explanation for each anomalous check, or clear the flag",
        )
    return _met(gid, f"{len(checks)} robustness check(s); no unexplained anomalies")


def evaluate_verdict_preconditions(protocol_result: dict, pre_registration: dict,
                                   research_brief: dict | None = None) -> list[dict]:
    """G1-G4, evaluated in VERDICT_PRECONDITION_IDS order. Callable standalone
    so a research-path run -- which has no orchestrator, and was exactly how
    XS_momentum escaped -- can still be checked against them."""
    brief = research_brief or {}
    return [
        _gate_cost_model_completeness(protocol_result, pre_registration, brief),
        _gate_distribution_stats(protocol_result),
        _gate_deployable_today(protocol_result),
        _gate_robustness_mechanism(protocol_result),
    ]


# ---------------------------------------------------------------------------
# G6 -- verdict provenance. No verdict may enter campaign_knowledge_base.yaml
# or campaign_queue.yaml except through this evaluator. A run that did not
# pass through it is structurally ungated, and a verdict field on such an
# entry is rejected rather than recorded. This is the link that let a
# research-path tool (panel_backtester.py) write `verdict_c7: refine` into
# the KB with no pass rule, no evaluator call, and no run directory.
# ---------------------------------------------------------------------------

class UngatedVerdictError(ValueError):
    """Raised when a KB/queue entry carries a verdict without evaluator
    provenance. Deliberately fatal: the KB is the campaign's memory, and a
    verdict written into it without a gate is indistinguishable, later, from
    one that earned its way there."""


def validate_verdict_provenance(entry: dict, entry_ref: str = "<entry>") -> dict:
    """G6. Returns the entry unchanged when admissible; raises
    UngatedVerdictError otherwise.

    A verdict field is admissible ONLY when the entry cites a
    `pass_rule_evaluation_ref` (the pass_rule_evaluation.yaml this evaluator
    wrote) AND that evaluation resolved to a binding result. An entry with no
    such provenance must instead record `verdict_status: ungated` and keep its
    measurements -- measurements are real information; they are simply not a
    verdict."""
    present = [f for f in _VERDICT_FIELDS if entry.get(f) is not None]
    ref = entry.get("pass_rule_evaluation_ref")
    status = str(entry.get("verdict_status") or "").strip().lower()

    if not present:
        return entry

    # Checked before the provenance test: an entry that declares itself ungated
    # and then carries a verdict anyway is self-contradictory, and saying so is
    # more useful than the generic missing-provenance message it would
    # otherwise fall through to.
    if status == "ungated":
        raise UngatedVerdictError(
            f"{entry_ref} declares `verdict_status: ungated` yet also carries "
            f"verdict field(s) {present} -- contradictory. An ungated run has "
            f"measurements, not a verdict."
        )
    if not ref:
        raise UngatedVerdictError(
            f"{entry_ref} carries verdict field(s) {present} but no "
            f"`pass_rule_evaluation_ref` -- this run did not pass through the "
            f"verdict evaluator and is structurally ungated. Record "
            f"`verdict_status: ungated` and keep the measurements; a verdict "
            f"field is not admissible here."
        )
    return entry


def evaluate_pass_rule_criteria(protocol_result: dict, pre_registration: dict,
                                research_brief: dict | None = None) -> dict:
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

    G5 (C7-EXT): the four verdict preconditions are evaluated FIRST and
    DOMINATE. They run whether or not a pass_rule exists, and an unmet one
    short-circuits to VERDICT_BLOCKED before any `legacy_not_evaluable` return
    can hand the run to stage discretion.
    """
    precondition_results = evaluate_verdict_preconditions(
        protocol_result, pre_registration, research_brief)
    blocked = [g for g in precondition_results if g["result"] == "BLOCKED"]
    if blocked:
        return {
            "result": "VERDICT_BLOCKED",
            "preconditions": precondition_results,
            "blocked_by": [g["id"] for g in blocked],
            "reason": (
                "verdict precondition(s) "
                + ", ".join(f"{g['id']} ({g['reason']})" for g in blocked)
                + " -- no verdict of any kind (PASS, FAIL, or stage-discretion) may "
                  "be issued on this run until they are met. This is NOT a failed "
                  "hypothesis; it is inadmissible evidence."
            ),
        }

    # Preconditions all MET -- resolve the pass rule exactly as K2 did, then
    # stamp the precondition results onto the artifact so a later reader can
    # see they were checked rather than assume it.
    result = _resolve_pass_rule(protocol_result, pre_registration)
    result["preconditions"] = precondition_results
    return result


def _resolve_pass_rule(protocol_result: dict, pre_registration: dict) -> dict:
    """The unchanged K2 pass-rule resolution. Split out by C7-EXT so that G5's
    precondition gate sits strictly in front of every one of its exits --
    including the `legacy_not_evaluable` ones."""
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
