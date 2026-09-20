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

See engineering/improvements/done/design_and_docs/K2_verdict_machinery_design_20260713.md sections 6 and 8.

C7-EXT (2026-07-22, XS_momentum ungated-verdict incident) adds seven gates on
top of the K2 kernel. See the VERDICT PRECONDITIONS section below and ledger
entry C7-EXT in engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md for the four-link defect
chain each gate closes.

C7-EXT-R (2026-07-22, remediation of the independent audit in
engineering/sessions/session_reports/20260722_c7ext_audit.md) repairs G6, which the audit
demonstrated was bypassable in the exact shape of the incident it was written
to close. See the G6 section below.

WHAT THESE GATES ARE, STATED PLAINLY: G1-G4 are PRESENCE checks, not content
checks. They establish that a required figure was REPORTED; they do not and
cannot establish that it was reported carefully. The audit demonstrated that
`skew: 0, kurtosis: 0, var_95: 0`, `cost_basis: ""`, and
`mechanism_explanation: "."` all clear their respective gates. They catch
OMISSION, not carelessness. Do not read a MET precondition as a quality
warrant. Carry-forwards D-2 (G4 detects no anomalies; it only demands prose for
self-declared ones) and D-7 (G1's product allowlist is exact-match on a
free-text brief field; G2/G3 accept placeholder and wrong-typed values) are
OPEN and recorded as such in the ledger.
"""
from __future__ import annotations

import statistics
import sys
from pathlib import Path

# tools/ may not be on sys.path when this module is imported by path rather than
# by name (several callers do exactly that), so make the sibling import robust
# rather than dependent on the caller having set the path up first.
_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

import record_schema as _record_schema  # noqa: E402

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
# in docs/analysis-reports/venue_survey_20260719.md (Binance / Kraken / Bybit perps).
_DEFAULT_FUNDING_INTERVAL_HOURS = 8.0

# G6: a KB/queue verdict field is admissible ONLY with evaluator provenance.
_VERDICT_FIELDS = ("verdict_c7", "hypothesis_verdict", "verdict")

# C7-EXT-R2 (2026-07-23): the name-matching approach is GONE, and deliberately so.
#
# Round 1 gated three names. Round 2 replaced them with "any key containing the
# substring 'verdict'" and called it "New name, same gate". The re-audit defeated
# that in minutes with `status: kill`, `disposition: kill`, `urteil: kill`, and by
# nesting a verdict one level down or inside a list. Enumerating forbidden names
# is an unbounded guess, and broadening the guess is the same move, not a
# different one.
#
# What replaces it is a CLOSED SCHEMA (tools/record_schema.py): a record may hold
# only enumerated fields with declared value shapes, and a bare verdict token is
# refused as a VALUE anywhere except the one designated field. `_VERDICT_FIELDS`
# survives only because those three names are real legacy shapes worth naming in
# an error message -- the schema would reject them as unknown fields regardless,
# and does so even if this tuple is emptied.

# C7-EXT-R / D-4. The audit's decisive finding: the three names above are NOT
# the field the campaign records verdicts in. Both campaign_knowledge_base.yaml
# and config/campaign_queue.yaml record them in `outcome`, and
# _write_kb_findings_entry emits exactly that -- so G6 was a structural no-op on
# every entry the orchestrator itself writes.
#
# `outcome` cannot simply be added to _VERDICT_FIELDS, because not every outcome
# is a verdict. `invalidated_artifact` and `blocked_feed_unavailable` are
# ENGINEERING states -- they assert nothing about the hypothesis and require no
# gate. A verdict is a claim about whether the hypothesis is true, and only
# those need provenance.
_VERDICT_BEARING_OUTCOME_PREFIXES = ("kill", "promote", "refine")
_VERDICT_BEARING_OUTCOMES = frozenset({
    "no_edge_observed",
    "era_conditional_instability",
    "completed_rejected",
})
# Process/engineering states, and honest self-declarations of non-verdict. These
# are admissible with no provenance BECAUSE they claim nothing about the
# hypothesis. `ungated_*` and `measurement_only_*` are the vocabulary a corrected
# record uses (XS_momentum's own corrected outcome is one of them).
_NON_VERDICT_OUTCOME_PREFIXES = ("ungated", "measurement_only", "blocked", "unusable",
                                 "paused", "in_progress")
_NON_VERDICT_OUTCOMES = frozenset({
    "invalidated_artifact",
    "inconclusive",
    # config/campaign_queue.yaml reuses `outcome` for WHERE A LINEAGE GOT TO as
    # well as for what it concluded. A stage name or a lineage-continuation
    # marker asserts nothing about the hypothesis and needs no gate; only a
    # terminal scientific claim does. `completed_rejected` is deliberately NOT in
    # this set -- it is a claim, and it is how the campaign's one genuinely gated
    # verdict (run_059) is recorded.
    "hypothesis_generation", "innovation_expansion", "validation",
    "backtest_specification", "signal_prescreen", "protocol_execution",
    "verdict_interpreter", "refinement_planner", "holdout_evaluation",
    "campaign_review",
    "completed_reframed", "completed_escalated", "completed_refined",
    "done", "ready", "pending", "superseded", "not_launched",
    # E-030 S2a. Registered here DELIBERATELY, as the same kind of act the
    # `outcome_is_verdict_bearing` docstring describes: an unrecognised outcome
    # defaults to verdict-bearing, so without this line _save_queue would refuse
    # every quarantine write with UngatedVerdictError -- turning a quarantine into
    # a crash, which is strictly worse than the halt it replaces.
    #
    # It belongs in THIS set, next to `invalidated_artifact`, for the same reason
    # that one does: it records that the RUN failed for engineering reasons and
    # that NO scientific claim is being made. That is exactly what the S1 taxonomy's
    # R8 requires of a quarantine -- "quarantine must never write a scientific
    # outcome" -- and it is why quarantine writes this value rather than
    # `completed_rejected`, which IS a claim and is deliberately absent from this
    # set. A quarantined entry therefore needs no pass_rule_evaluation_ref, and
    # honest_verdict_count() correctly does not count it.
    "quarantined_engineering_failure",
})

# An entry may honestly declare that it holds no gated verdict. This is not a
# loophole -- it is the entire point. The defect was that an ungated verdict was
# INDISTINGUISHABLE from a gated one; requiring the distinction to be stated is
# the fix. A reader can now tell them apart, and `honest_verdict_count()` counts
# only the gated ones.
_UNGATED_DECLARATIONS = frozenset({"ungated", "stage_discretion", "void"})

# A pass_rule_evaluation.yaml only confers provenance if it actually RESOLVED a
# verdict. VERDICT_BLOCKED / legacy_not_evaluable / SPEC_ERROR are the evaluator
# declining to decide; citing one as provenance is citing a non-decision.
_BINDING_EVALUATION_RESULTS = frozenset({"PASS", "FAIL"})


def outcome_is_verdict_bearing(outcome) -> bool:
    """True when `outcome` asserts something about whether the hypothesis is
    true, and therefore requires evaluator provenance under G6.

    Unrecognised outcomes are treated as VERDICT-BEARING. That default is
    deliberate: a new outcome string nobody classified is exactly the shape the
    XS_momentum incident arrived in, and the safe failure mode is to demand
    provenance and be told 'this one does not need it' rather than to wave it
    through silently."""
    if outcome is None:
        return False
    text = str(outcome).strip().lower()
    if not text:
        return False
    if text in _NON_VERDICT_OUTCOMES or text.startswith(_NON_VERDICT_OUTCOME_PREFIXES):
        return False
    # Everything else -- the classified verdict outcomes AND anything
    # unrecognised -- requires provenance. See the default-deny note above.
    return True


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


def lint_pass_rule_structure(pass_rule) -> list[str]:
    """CUL-267: registration-time structural lint over a pass_rule's
    `criteria` list, moving a class of `_evaluate_one_criterion` SPEC_ERROR
    from EVALUATION time (discovered only after a real backtest already ran)
    to REGISTRATION time (a bad criterion is refused when the brief is
    written).

    What this CANNOT check: whether `criterion["metric"]` actually resolves
    via `_lookup_metric_value` -- that set is DATA-dependent (per_symbol_summary's
    keys when `symbol` is given; trade_diagnostics_summary's / hypothesis_verdict.
    diagnostics's keys when pooled), only knowable once a real protocol_result.yaml
    exists. A registration-time lint has no protocol_result.yaml yet.

    What this DOES check -- the structural half of the same failure modes
    `_evaluate_one_criterion` guards against:
      - `metric` is a non-empty string (an empty/absent metric can never
        resolve, regardless of data);
      - `comparator` is one of `_VALID_COMPARATORS`;
      - unless `per_symbol_threshold` is set, `null_handling` is
        `"fails_threshold"` -- the only value `_evaluate_one_criterion`
        recognizes to avoid SPEC_ERROR when the metric resolves to None
        (see its non-per-symbol branch). `per_symbol_threshold` criteria are
        exempted here because a null result there is per-symbol and
        data-dependent (some symbols may simply never resolve null); the
        existing B11 total-mapping lint already requires a null_handling
        value be PRESENT for that shape.

    Mirrors `_lint_pass_rule_total_mapping`'s own legacy-shape tolerance: a
    `pass_rule` that is `None` or a plain string is the pre-K2 legacy schema
    and is NOT linted here -- it resolves to `legacy_not_evaluable` at
    evaluation time (R3), unchanged by this ticket.

    Returns a list of violation strings; empty means the criteria are
    structurally clean and no criterion in this pass_rule can hit the three
    SPEC_ERROR causes this lint targets."""
    violations: list[str] = []
    if pass_rule is None or isinstance(pass_rule, str):
        return violations  # legacy shape -- nothing to lint (same as B11's own lint)
    if not isinstance(pass_rule, dict):
        violations.append(f"pass_rule is neither a string nor a dict (got {type(pass_rule).__name__})")
        return violations

    criteria = pass_rule.get("criteria") or []
    for idx, criterion in enumerate(criteria):
        if not isinstance(criterion, dict):
            violations.append(f"criteria[{idx}] is not a mapping (got {type(criterion).__name__})")
            continue
        cid = criterion.get("id") or f"criteria[{idx}]"

        metric = criterion.get("metric")
        if not (isinstance(metric, str) and metric.strip()):
            violations.append(
                f"criterion {cid!r}: metric is missing or empty ({metric!r}) -- "
                f"_evaluate_one_criterion would return SPEC_ERROR for this at evaluation "
                f"time; refusing at registration instead"
            )

        comparator = criterion.get("comparator")
        if comparator not in _VALID_COMPARATORS:
            violations.append(
                f"criterion {cid!r}: comparator={comparator!r} is not one of "
                f"{_VALID_COMPARATORS} -- _evaluate_one_criterion would return SPEC_ERROR "
                f"for this at evaluation time; refusing at registration instead"
            )

        # CODE-REVIEW FIX (2026-09-20): this used to skip the null_handling check
        # entirely whenever per_symbol_threshold was set. That was wrong --
        # _evaluate_one_criterion's per_symbol_threshold branch reads the SAME
        # criterion-level null_handling field and applies the SAME
        # `== "fails_threshold"` check per symbol (see that function: the
        # per-symbol loop's null branch is byte-identical in condition to the
        # pooled branch below it). A per-symbol criterion with a missing or
        # wrong null_handling still reaches SPEC_ERROR the moment any one
        # symbol's metric resolves null -- exactly the post-backtest discovery
        # this lint exists to move to registration time. The check now applies
        # unconditionally, per-symbol or pooled, matching the evaluator exactly.
        null_handling = criterion.get("null_handling")
        if null_handling != "fails_threshold":
            violations.append(
                f"criterion {cid!r}: null_handling={null_handling!r} is not "
                f"'fails_threshold' (the only value _evaluate_one_criterion "
                f"recognizes to avoid SPEC_ERROR when this metric resolves null, "
                f"for both per-symbol and pooled criteria) -- "
                f"refusing at registration instead of deferring to a SPEC_ERROR "
                f"discovered after a real backtest runs"
            )

    return violations


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


def _default_root() -> Path:
    """strategy-research/, the root the KB and queue live under."""
    return Path(__file__).resolve().parent.parent


def _entry_run_ids(entry: dict) -> list:
    ids = []
    for key in ("evidence_runs", "run_ids"):
        val = entry.get(key)
        if isinstance(val, list):
            ids.extend(str(v) for v in val if v)
        elif val:
            ids.append(str(val))
    if entry.get("run_id"):
        ids.append(str(entry["run_id"]))
    return ids


def resolve_evaluation_ref(ref, entry: dict, root=None) -> tuple:
    """C7-EXT-R / D-4. Resolves a `pass_rule_evaluation_ref` to a real artifact.

    The audit showed the previous check accepted ANY truthy string --
    `"does/not/exist.yaml"` conferred provenance. Provenance that is never
    resolved is not provenance; it is a spelling.

    Three things must hold, and all three are checkable:
      1. the path EXISTS on disk;
      2. it BELONGS to this entry -- it lies under runs/<one of this entry's own
         run ids>/, so an entry cannot borrow another run's evaluation;
      3. the evaluation RESOLVED a verdict (result PASS or FAIL). VERDICT_BLOCKED,
         legacy_not_evaluable and SPEC_ERROR are the evaluator DECLINING to
         decide -- citing one as provenance cites a non-decision.

    Returns (ok: bool, detail: str)."""
    if not ref or not isinstance(ref, str):
        return False, f"pass_rule_evaluation_ref is absent or not a string ({ref!r})"

    base = Path(root) if root is not None else _default_root()
    candidate = Path(ref)
    path = candidate if candidate.is_absolute() else base / ref
    if not path.exists():
        return False, (f"pass_rule_evaluation_ref={ref!r} does not exist "
                       f"(resolved to {path}) -- a path that resolves to nothing "
                       f"is not provenance")

    # C7-EXT-R2: containment is checked on the RESOLVED path, and only after it is
    # resolved. The previous version substring-matched the UNRESOLVED string, so
    #     runs/run_999_FAKE/../run_059/artifacts/pass_rule_evaluation.yaml
    # with evidence_runs: ["run_999_FAKE"] passed the ownership test (the literal
    # text does contain "/runs/run_999_FAKE/") while open() followed the ".." to
    # run_059's real FAIL. A fabricated hypothesis citing a run that never
    # executed borrowed a genuine result from an unrelated one.
    resolved = path.resolve()
    run_ids = _entry_run_ids(entry)
    if not run_ids:
        # C7-EXT-R2, found while implementing (not in the re-audit): with no run
        # ids the ownership check used to be SKIPPED, so an entry naming no run at
        # all could cite any evaluation in the tree. An entry that claims a verdict
        # must say which run earned it.
        return False, (f"pass_rule_evaluation_ref={ref!r} is cited by an entry that "
                       f"names no run (evidence_runs/run_ids/run_id all absent) -- "
                       f"ownership cannot be established, so the citation confers "
                       f"nothing")
    owning_dirs = [(base / "runs" / rid).resolve() for rid in run_ids]
    if not any(resolved == owner or owner in resolved.parents for owner in owning_dirs):
        return False, (f"pass_rule_evaluation_ref={ref!r} resolves to {resolved}, which "
                       f"does not lie under any of this entry's own runs {run_ids} -- an "
                       f"entry may not borrow another run's evaluation as its provenance")

    try:
        import yaml
        with open(path, "r", encoding="utf-8") as fh:
            evaluation = yaml.safe_load(fh) or {}
    except Exception as exc:  # unreadable/unparseable is a failed resolution
        return False, f"pass_rule_evaluation_ref={ref!r} could not be parsed: {exc}"

    if not isinstance(evaluation, dict):
        return False, f"pass_rule_evaluation_ref={ref!r} did not parse to a mapping"

    result = str(evaluation.get("result") or "").strip().upper()
    if result not in _BINDING_EVALUATION_RESULTS:
        return False, (f"pass_rule_evaluation_ref={ref!r} has result={result!r}, which "
                       f"is not a resolved verdict (expected one of "
                       f"{sorted(_BINDING_EVALUATION_RESULTS)}) -- the evaluator "
                       f"declined to decide, so there is no verdict to cite")
    return True, f"{ref} (result={result})"


def validate_verdict_provenance(entry: dict, entry_ref: str = "<entry>",
                                root=None, schema=None) -> dict:
    """G6. Returns the entry unchanged when admissible; raises
    UngatedVerdictError otherwise.

    TWO GATES, IN ORDER (C7-EXT-R2, 2026-07-23):

      1. CLOSED SCHEMA -- tools/record_schema.py. The record may contain only
         enumerated fields with declared value shapes, and no string anywhere in
         it, at any depth, may be a bare verdict token except in the one
         designated field. This replaces three rounds of failed name-matching;
         see record_schema.py's header for why enumerating forbidden names could
         never have worked.

      2. PROVENANCE on that one designated field, `outcome`.

    ADMISSIBLE means one of:
      - the entry cites a pass_rule_evaluation_ref that RESOLVES -- exists,
        RESOLVED-path-contained within a run this entry actually names, and
        recorded a binding PASS/FAIL; or
      - the entry honestly declares it holds no gated verdict, via
        `verdict_status: ungated` (or stage_discretion / void).

    The second branch is not a loophole. The defect this closes is that an
    ungated verdict was INDISTINGUISHABLE from a gated one. Forcing the record
    to say which it is restores the distinction; honest_verdict_count() then
    counts only the first kind.

    `schema` selects the record type; it defaults to the KB finding schema
    because that is the stricter of the two."""
    try:
        _record_schema.validate_record_schema(
            entry, schema if schema is not None else _record_schema.KB_FINDING_SCHEMA,
            entry_ref)
    except _record_schema.RecordSchemaError as exc:
        # Re-raised as UngatedVerdictError so every existing call site -- the KB
        # writer, the queue writer, the standalone lint -- refuses on a schema
        # violation without needing to learn a second exception type.
        raise UngatedVerdictError(str(exc)) from exc

    strict_fields = sorted(f for f in _VERDICT_FIELDS if entry.get(f) is not None)
    outcome = entry.get("outcome")
    outcome_gated = outcome_is_verdict_bearing(outcome)
    ref = entry.get("pass_rule_evaluation_ref")
    status = str(entry.get("verdict_status") or "").strip().lower()
    declared_ungated = status in _UNGATED_DECLARATIONS

    if not strict_fields and not outcome_gated:
        return entry

    # A strict verdict field alongside a self-declaration of ungated is
    # contradictory, and saying so is more useful than the generic
    # missing-provenance message it would otherwise fall through to. Note this
    # applies to the strict fields ONLY: `outcome` plus `verdict_status: ungated`
    # is the CORRECT shape for a corrected record, not a contradiction.
    if strict_fields and declared_ungated:
        raise UngatedVerdictError(
            f"{entry_ref} declares `verdict_status: {status}` yet also carries "
            f"verdict field(s) {strict_fields} -- contradictory. An ungated run has "
            f"measurements, not a verdict."
        )

    if declared_ungated:
        return entry

    if not ref:
        what = (f"verdict field(s) {strict_fields}" if strict_fields
                else f"verdict-bearing `outcome: {outcome}`")
        raise UngatedVerdictError(
            f"{entry_ref} carries {what} but no `pass_rule_evaluation_ref` -- this "
            f"run did not pass through the verdict evaluator and is structurally "
            f"ungated. Either cite a real pass_rule_evaluation.yaml, or record "
            f"`verdict_status: ungated` and keep the measurements; a verdict is "
            f"not admissible here."
        )

    ok, detail = resolve_evaluation_ref(ref, entry, root)
    if not ok:
        raise UngatedVerdictError(
            f"{entry_ref} cites a pass_rule_evaluation_ref that does not confer "
            f"provenance: {detail}."
        )
    return entry


def honest_verdict_count(kb: dict, queue: dict, root=None) -> list:
    """C7-EXT-R / D-5. The gated-verdict roll, computed from EVIDENCE rather
    than from a string match.

    The superseded test counted queue entries whose `outcome` string equalled
    "completed_rejected", which tests nothing about gatedness: H-041-C-v2 was
    rejected by an LLM validation stage before its pass_rule ever ran, and was
    counted anyway. A verdict is gated iff the evaluator actually ran and
    resolved it -- which is exactly the artifact resolve_evaluation_ref checks.

    Returns a sorted list of hypothesis_ids holding an admissible gated verdict."""
    gated = set()
    for entry in list((kb or {}).get("findings") or []) + list((queue or {}).get("queue") or []):
        if not isinstance(entry, dict):
            continue
        if not (outcome_is_verdict_bearing(entry.get("outcome"))
                or any(entry.get(f) is not None for f in _VERDICT_FIELDS)):
            continue
        ok, _ = resolve_evaluation_ref(entry.get("pass_rule_evaluation_ref"), entry, root)
        if ok:
            gated.add(str(entry.get("hypothesis_id") or entry.get("id")))
    return sorted(gated)


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


def _find_pass_rule(pre_registration: dict):
    """C7-EXT-R / D-6. A pre-registered pass_rule may sit at the top level of
    pre_registration.yaml OR nested under `machine_constraints`.

    This is not a cosmetic tolerance. run_057's pass_rule is nested
    (runs/run_057/artifacts/pre_registration.yaml: machine_constraints.pass_rule)
    and the top-level-only lookup therefore resolved it to None. No
    pass_rule_evaluation.yaml was ever written for run_057, and a `kill` was
    recorded into both the KB and the queue regardless.

    HONEST LIMIT OF THIS FIX: finding run_057's rule does not make it
    machine-evaluable. It is a legacy PROSE STRING, so it still resolves to
    `legacy_not_evaluable` -- correctly. The fix changes the diagnosis from "no
    rule was registered" to the accurate "a rule was registered, in a shape this
    kernel cannot evaluate, and the verdict was human-adjudicated throughout".
    That distinction is the whole point for the archive: run_057 was never
    mechanically gated, and its record must say so rather than implying a gate
    ran. Future runs registering a nested STRUCTURED rule are now evaluated
    rather than silently dropped.

    Top level wins when both exist -- a brief that states the rule in both places
    is malformed, and preferring the canonical location keeps the resolution
    deterministic rather than silently favouring the nested copy."""
    top = pre_registration.get("pass_rule")
    if top is not None:
        return top
    machine_constraints = pre_registration.get("machine_constraints")
    if isinstance(machine_constraints, dict):
        return machine_constraints.get("pass_rule")
    return None


def _resolve_pass_rule(protocol_result: dict, pre_registration: dict) -> dict:
    """The unchanged K2 pass-rule resolution. Split out by C7-EXT so that G5's
    precondition gate sits strictly in front of every one of its exits --
    including the `legacy_not_evaluable` ones."""
    pass_rule = _find_pass_rule(pre_registration)
    if pass_rule is None:
        return {"result": "legacy_not_evaluable",
                "reason": ("pre_registration.yaml has no pass_rule field at all -- "
                           "checked both the top level and machine_constraints "
                           "(C7-EXT-R/D-6)")}
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


# ---------------------------------------------------------------------------
# E-046b S2 -- the grid (engineering_roadmap.html card C). evaluate_grid()
# lives BESIDE evaluate_pass_rule_criteria() above -- it never replaces it.
# A legacy (non-menu-shaped) pass_rule keeps going through that function
# exactly as before; this is new, additive machinery for a differently
# shaped pass_rule.criteria list (entries carrying `source`/`reducer`
# fields). See strategy-research/engineering/roadmap/E-046b/S1_FINDINGS.md
# for the full characterization this implements, including the
# operator-confirmed FAIL-dominates-INCONCLUSIVE tie-break and the
# independently-verified `_era_id_for_timestamp` None-comparison bug this
# module's own era resolver proactively guards against.
# ---------------------------------------------------------------------------

_VALID_GRID_SOURCES = ("window", "pooled")
_VALID_GRID_REDUCERS = ("median", "mean", "min", "max", "fraction_above", "sign_consistent_by_era")


def _era_id_for_timestamp(ts, eras: list) -> str:
    """Grid's own copy -- deliberately NOT importing run_protocol.py (that
    module launches subprocesses and carries import-time weight this
    evaluator otherwise avoids).

    PROACTIVE FIX (not yet hit in the corpus) of the bug
    S1_FINDINGS.md documents in run_protocol.py's identically-named
    function: `campaign_data_policy.yaml`'s last era
    (era_2026_h2_forward_recorded) has an open-ended upper bound,
    `range: [2026-07-26, null]`. The original `lo <= d <= hi` raises
    TypeError the moment a timestamp reaches that far without matching an
    earlier era (`str <= None` is unorderable in Python 3). Here, `hi is
    None` is treated as +inf -- any date >= lo matches -- and `hi` is never
    compared to `d` directly when it is None."""
    import pandas as pd
    d = pd.Timestamp(ts).strftime("%Y-%m-%d")
    for era in eras:
        lo, hi = era["range"]
        if hi is None:
            if lo <= d:
                return era["era_id"]
            continue
        if lo <= d <= hi:
            return era["era_id"]
    return "era_unmapped"


def _load_campaign_data_policy_eras() -> list:
    """Local copy of run_protocol.py::_load_campaign_data_policy, scoped to
    just the `eras` list this module needs -- same "small,
    strategy-research-specific config reader, not general statistics"
    rationale that function's own docstring gives for not centralizing it."""
    import yaml as _yaml
    path = Path(__file__).resolve().parent.parent / "config" / "campaign_data_policy.yaml"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        doc = _yaml.safe_load(f) or {}
    return doc.get("eras") or []


def _window_label_to_timestamp(window_label):
    """protocol_result.yaml's results[*]['window'] is a 'YYYY-MM' label
    (confirmed directly against run_054's and run_059's real artifacts, not
    assumed) -- not a full timestamp. Anchors on the first day of that
    month. Returns None (never raises) for a label this doesn't recognize,
    so a caller can skip that window rather than crash on an unexpected
    window-naming convention."""
    import pandas as pd
    if not window_label:
        return None
    text = str(window_label).strip()
    try:
        if len(text) == 7 and text[4] == "-":  # 'YYYY-MM'
            return pd.Timestamp(text + "-01")
        return pd.Timestamp(text)
    except (ValueError, TypeError):
        return None


def _numeric_values(values):
    return [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]


def _reduce_median(values, _arg=None):
    vals = _numeric_values(values)
    return statistics.median(vals) if vals else None


def _reduce_mean(values, _arg=None):
    vals = _numeric_values(values)
    return statistics.mean(vals) if vals else None


def _reduce_min(values, _arg=None):
    vals = _numeric_values(values)
    return min(vals) if vals else None


def _reduce_max(values, _arg=None):
    vals = _numeric_values(values)
    return max(vals) if vals else None


def _reduce_fraction_above(values, arg):
    vals = _numeric_values(values)
    if not vals:
        return None
    if arg is None:
        raise ValueError("reducer=fraction_above requires a numeric reducer_arg (the "
                          "threshold values are counted above) -- none was given")
    return sum(1 for v in vals if v > arg) / len(vals)


_SCALAR_REDUCERS = {
    "median": _reduce_median,
    "mean": _reduce_mean,
    "min": _reduce_min,
    "max": _reduce_max,
    "fraction_above": _reduce_fraction_above,
}


def _reduce_sign_consistent_by_era(value_window_pairs, eras: list):
    """S1_FINDINGS.md §3 pseudocode: group (value, window) pairs by era via
    the window's own timestamp, take each era's median sign, and PASS iff
    every REPRESENTED era's sign agrees and is nonzero (a zero median is
    ambiguous, never a pass).

    Returns (passed: bool | None, detail: dict). `passed is None` means "not
    computable" (no window resolved both a numeric value and a recognizable
    era) -- the caller must treat that as INCONCLUSIVE, never as a silent
    pass or fail."""
    from collections import defaultdict
    by_era = defaultdict(list)
    for value, window_label in value_window_pairs:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            continue
        ts = _window_label_to_timestamp(window_label)
        if ts is None:
            continue
        by_era[_era_id_for_timestamp(ts, eras)].append(value)

    if not by_era:
        return None, {"era_medians": {}, "era_signs": {},
                       "reason": "no window resolved both a numeric value and a recognizable era"}

    era_medians = {eid: statistics.median(vals) for eid, vals in by_era.items()}
    era_signs = {eid: (1 if med > 0 else (-1 if med < 0 else 0)) for eid, med in era_medians.items()}
    detail = {"era_medians": era_medians, "era_signs": era_signs}

    signs = set(era_signs.values())
    if 0 in signs:
        return False, {**detail, "reason": "at least one represented era's median is exactly "
                                            "zero -- ambiguous, not a passing sign"}
    if len(signs) > 1:
        return False, {**detail, "reason": f"represented eras disagree in sign: {era_signs}"}
    return True, detail


def _check_floor(n_windows: int, n_trades: int, floor: dict | None):
    """Gates the reducer's/lookup's OWN input count before any comparator
    runs (S1_FINDINGS.md §3). Returns (ok: bool, reason: str | None).

    `min_n_eff` deliberately RAISES rather than being silently treated as
    satisfied or as zero -- S1_FINDINGS.md's 'Not determined' section found
    no field anywhere in the addressable protocol_result.yaml corpus
    (core / per_symbol_summary / trade_diagnostics_summary /
    hypothesis_verdict.diagnostics) that resolves an effective-sample-size
    statistic. A criterion that declares this floor cannot be honestly
    evaluated yet."""
    floor = floor or {}
    if floor.get("min_n_eff") is not None:
        raise NotImplementedError(
            f"floor.min_n_eff={floor['min_n_eff']!r} is not computable in this slice -- no "
            f"field named n_eff (or an equivalent effective-sample-size statistic) exists "
            f"anywhere in the addressable protocol_result.yaml corpus (S1_FINDINGS.md's 'Not "
            f"determined' section). Refusing to silently treat this floor as satisfied or as "
            f"zero -- remove min_n_eff from this criterion's floor, or wire a real n_eff "
            f"source before using it."
        )
    min_windows = floor.get("min_windows")
    if min_windows is not None and n_windows < min_windows:
        return False, f"n_windows={n_windows} < floor.min_windows={min_windows}"
    min_trades = floor.get("min_trades")
    if min_trades is not None and n_trades < min_trades:
        return False, f"n_trades={n_trades} < floor.min_trades={min_trades}"
    return True, None


def _window_core_triples(protocol_result: dict, metric: str, symbol: str | None):
    """[(core[metric], window_label, core['trade_count'])] over
    protocol_result['results'], optionally filtered to one symbol. This is
    the NEW capability _lookup_metric_value doesn't have -- it never reads
    per-window `core` at all (S1_FINDINGS.md §1)."""
    out = []
    for entry in protocol_result.get("results") or []:
        if not isinstance(entry, dict):
            continue
        if symbol is not None and entry.get("symbol") != symbol:
            continue
        core = entry.get("core") or {}
        out.append((core.get(metric), entry.get("window"), core.get("trade_count")))
    return out


def _evaluate_grid_cell_for_symbol(criterion: dict, protocol_result: dict, eras: list,
                                    symbol: str | None) -> dict:
    """One (criterion, variant[, symbol]) cell -- the mechanical core, no
    symbol_reducer branching (that lives one level up in
    _evaluate_grid_cell)."""
    cid = criterion.get("id")
    metric = criterion.get("metric")
    source = criterion.get("source")
    comparator = criterion.get("comparator")
    threshold = criterion.get("threshold")
    floor = criterion.get("floor")

    if not metric:
        return {"result": "SPEC_ERROR", "reason": f"criterion {cid!r} has no metric"}
    if source not in _VALID_GRID_SOURCES:
        return {"result": "SPEC_ERROR",
                "reason": f"criterion {cid!r}: source={source!r} not one of {_VALID_GRID_SOURCES}"}

    if source == "window":
        reducer = criterion.get("reducer")
        if reducer not in _VALID_GRID_REDUCERS:
            return {"result": "SPEC_ERROR",
                    "reason": f"criterion {cid!r}: reducer={reducer!r} not one of {_VALID_GRID_REDUCERS}"}
        triples = _window_core_triples(protocol_result, metric, symbol)
        non_none = [(v, w, tc) for v, w, tc in triples if isinstance(v, (int, float)) and not isinstance(v, bool)]
        n_windows = len(non_none)
        n_trades = sum((tc or 0) for _, _, tc in non_none)
        floor_ok, floor_reason = _check_floor(n_windows, n_trades, floor)
        if not floor_ok:
            return {"result": "INCONCLUSIVE", "n_windows": n_windows, "n_trades": n_trades,
                    "reason": floor_reason}

        if reducer == "sign_consistent_by_era":
            passed, detail = _reduce_sign_consistent_by_era([(v, w) for v, w, _ in non_none], eras)
            if passed is None:
                return {"result": "INCONCLUSIVE", "n_windows": n_windows, "n_trades": n_trades,
                        "reason": detail.get("reason"), "detail": detail}
            return {"result": "PASS" if passed else "FAIL", "n_windows": n_windows,
                    "n_trades": n_trades, "detail": detail}

        try:
            value = _SCALAR_REDUCERS[reducer]([v for v, _, _ in non_none], criterion.get("reducer_arg"))
        except ValueError as exc:
            return {"result": "SPEC_ERROR", "reason": str(exc)}
        if value is None:
            return {"result": "INCONCLUSIVE", "n_windows": n_windows, "n_trades": n_trades,
                    "reason": f"{reducer}({metric}) resolved to None over {n_windows} window(s)"}
        if comparator not in _VALID_COMPARATORS:
            return {"result": "SPEC_ERROR",
                    "reason": f"criterion {cid!r}: comparator={comparator!r} not one of {_VALID_COMPARATORS}"}
        met = _apply_comparator(comparator, value, threshold)
        return {"result": "PASS" if met else "FAIL", "value": value, "threshold": threshold,
                "n_windows": n_windows, "n_trades": n_trades}

    # source == "pooled": reuses the existing three-source lookup
    # (per_symbol_summary / trade_diagnostics_summary /
    # hypothesis_verdict.diagnostics) -- the value is already aggregated, no
    # reducer applies. Floor counts ALL windows backing that aggregate (every
    # window in scope, not filtered to a non-None metric -- the pre-
    # aggregation in run_protocol.py owns its own internal filtering, e.g.
    # realized_edge_to_cost_ratio only pools records with a measured
    # cost_paid).
    value = _lookup_metric_value(protocol_result, criterion, symbol)
    entries = [e for e in (protocol_result.get("results") or [])
               if isinstance(e, dict) and (symbol is None or e.get("symbol") == symbol)]
    n_windows = len(entries)
    n_trades = sum(((e.get("core") or {}).get("trade_count") or 0) for e in entries)
    floor_ok, floor_reason = _check_floor(n_windows, n_trades, floor)
    if not floor_ok:
        return {"result": "INCONCLUSIVE", "n_windows": n_windows, "n_trades": n_trades,
                "reason": floor_reason}
    if value is None:
        return {"result": "INCONCLUSIVE", "n_windows": n_windows, "n_trades": n_trades,
                "reason": f"pooled metric {metric!r} resolved to None in this protocol_result "
                          f"(e.g. a pre-CUL-300 artifact for realized_edge_to_cost_ratio)"}
    if comparator not in _VALID_COMPARATORS:
        return {"result": "SPEC_ERROR",
                "reason": f"criterion {cid!r}: comparator={comparator!r} not one of {_VALID_COMPARATORS}"}
    met = _apply_comparator(comparator, value, threshold)
    return {"result": "PASS" if met else "FAIL", "value": value, "threshold": threshold,
            "n_windows": n_windows, "n_trades": n_trades}


def _dominant_cell_result(results: list) -> str:
    """SPEC_ERROR > FAIL > INCONCLUSIVE > PASS. Used to roll multiple
    per-symbol cells (symbol_reducer=per_symbol_all) up into one cell result
    -- the same dominance ordering evaluate_grid uses at the idea level
    below, reused rather than re-implemented (a SPEC_ERROR is a criterion
    that could not even be evaluated, more serious than a measured FAIL;
    never silently folded into 'FAIL')."""
    if not results:
        raise ValueError("_dominant_cell_result called with an empty list")
    if "SPEC_ERROR" in results:
        return "SPEC_ERROR"
    if "FAIL" in results:
        return "FAIL"
    if "INCONCLUSIVE" in results:
        return "INCONCLUSIVE"
    return "PASS"


def _evaluate_grid_cell(criterion: dict, protocol_result: dict, eras: list) -> dict:
    """One (criterion, variant) cell, handling `symbol_reducer`.

    `null` (default) and `pooled` are both evaluated with no symbol filter.
    Card C's own text: "The default is one symbol per variant" -- assuming a
    variant whose protocol_result already contains exactly one symbol's
    windows. Measured directly against the real corpus (run_054, run_059):
    EVERY current protocol_result.yaml backtests BOTH BTCUSDT and ETHUSDT
    inside one run (S1_FINDINGS.md's per_symbol_summary keys). S2 does not
    build a symbol-partitioned variant registry (that is later scope), so on
    today's real data `symbol_reducer: null` pools naively across whatever
    symbols are present -- identical to `pooled`. Documented here, not
    silently guessed."""
    symbol_reducer = criterion.get("symbol_reducer")
    if symbol_reducer not in (None, "per_symbol_all", "pooled"):
        return {"result": "SPEC_ERROR",
                "reason": f"criterion {criterion.get('id')!r}: symbol_reducer={symbol_reducer!r} "
                          f"not one of null/per_symbol_all/pooled"}

    if symbol_reducer == "per_symbol_all":
        symbols = sorted({
            e.get("symbol") for e in (protocol_result.get("results") or [])
            if isinstance(e, dict) and e.get("symbol")
        })
        if not symbols:
            return {"result": "INCONCLUSIVE",
                    "reason": "symbol_reducer=per_symbol_all but no window in this "
                              "protocol_result carries a symbol field"}
        per_symbol = {sym: _evaluate_grid_cell_for_symbol(criterion, protocol_result, eras, sym)
                      for sym in symbols}
        return {"result": _dominant_cell_result([c["result"] for c in per_symbol.values()]),
                "per_symbol": per_symbol}

    return _evaluate_grid_cell_for_symbol(criterion, protocol_result, eras, symbol=None)


def _menu_entries_by_id(menu) -> dict:
    if menu is None:
        return {}
    if isinstance(menu, dict):
        entries = menu.get("criteria") or []
    elif isinstance(menu, list):
        entries = menu
    else:
        raise TypeError(f"menu must be a dict ({{'criteria': [...]}}) or a list, got {type(menu).__name__}")
    return {e["id"]: e for e in entries if isinstance(e, dict) and e.get("id")}


def _is_menu_shaped_pass_rule(pass_rule) -> bool:
    """True iff `pass_rule` is dict-shaped AND at least one criterion entry
    carries a `source` or `reducer` field -- this slice's detection rule for
    'grid-shaped', distinct from K2's legacy metric/comparator/threshold/
    per_symbol_threshold shape. Checks for the NEW fields' PRESENCE, not the
    old ones' absence, so a criterion could in principle carry both during a
    transition without breaking detection."""
    if not isinstance(pass_rule, dict):
        return False
    criteria = pass_rule.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        return False
    return any(isinstance(c, dict) and ("source" in c or "reducer" in c) for c in criteria)


def _resolve_grid_criteria(pre_registration: dict, menu) -> list:
    """Merges each pass_rule.criteria entry against its matching `menu` entry
    (by `id`) -- criterion-supplied fields win, `menu` backfills anything the
    criterion doesn't specify. A fully self-contained criterion needs no
    menu entry at all (same anchor-table pattern as hypothesis-design/
    SKILL.md §A8.6's plausible_ic_upper: pick from the table, override with a
    stated reason, or skip it if the criterion is already complete)."""
    pass_rule = _find_pass_rule(pre_registration or {})
    if not _is_menu_shaped_pass_rule(pass_rule):
        return []
    menu_by_id = _menu_entries_by_id(menu)
    resolved = []
    for raw in pass_rule["criteria"]:
        if not isinstance(raw, dict):
            continue
        cid = raw.get("id")
        base = dict(menu_by_id.get(cid) or {})
        merged = {**base, **{k: v for k, v in raw.items() if v is not None}}
        if not merged.get("id"):
            merged["id"] = cid
        resolved.append(merged)
    return resolved


def evaluate_grid(protocol_results_by_variant: dict, pre_registration: dict,
                   research_brief: dict | None, menu) -> dict:
    """
    E-046b S2: the grid (engineering_roadmap.html card C) -- criteria x
    variants, every cell mechanical, unanimity across variants. No LLM
    verdict, no averaging across variants, no re-thresholding per variant.

    `protocol_results_by_variant`: {variant_id: protocol_result_dict} -- one
    column per variant. A single-entry dict is a valid 1-column grid: a
    variant registry does not exist yet (S1_FINDINGS.md §7 / delivery_plan_v26.md
    slice 2's own framing: "buildable before variants exist -- a grid with
    one column is still a grid, and the same code later takes three").

    `pre_registration`: must resolve a pass_rule whose criteria carry
    `source`/`reducer` fields (menu-shaped, see `_is_menu_shaped_pass_rule`)
    -- either fully self-contained or naming only `id` (+ overrides) to be
    merged against `menu`. A non-menu-shaped (or absent) pass_rule resolves
    zero criteria here and RAISES (see below) -- callers must route a legacy
    pass_rule through `evaluate_pass_rule_criteria` instead, never here.

    `research_brief`: accepted for signature parity with
    `evaluate_pass_rule_criteria` and for a future criterion type that needs
    brief context -- none of the v1 menu entries (`config/criterion_menu.yaml`)
    do, so it is currently unused. Kept as an explicit parameter rather than
    silently dropped, so a later criterion type does not force a signature
    change.

    `menu`: `config/criterion_menu.yaml`'s loaded document (a dict with a
    `criteria` list, or a bare list) -- used only to backfill criterion
    fields not already given directly in `pre_registration`.

    Returns {"result": "GRID_EVALUATED" | "SPEC_ERROR", "criteria": [id, ...],
    "variants": [variant_id, ...], "grid": {criterion_id: {variant_id:
    cell_dict}}, "idea_status": "validated"|"refuted"|"inconclusive"|None,
    "reason": str}.

    Idea-level status (card C, OPERATOR-CONFIRMED tie-break,
    S1_FINDINGS.md's appended 2026-09-20 decision): ANY cell that genuinely
    FAILs with sufficient data -> REFUTED, regardless of other cells being
    INCONCLUSIVE. Else ANY INCONCLUSIVE cell (with no FAIL present) ->
    INCONCLUSIVE. Else -> VALIDATED. A cell that could not even be evaluated
    (SPEC_ERROR) short-circuits the whole grid to a top-level SPEC_ERROR
    result with `idea_status: None` BEFORE the unanimity rollup runs -- a
    malformed criterion cannot honestly produce any idea status, mirroring
    `_resolve_pass_rule`'s own SPEC_ERROR precedent above.
    """
    if not isinstance(protocol_results_by_variant, dict) or not protocol_results_by_variant:
        raise ValueError("protocol_results_by_variant must be a non-empty {variant_id: "
                          "protocol_result} dict -- evaluate_grid always needs at least one column")

    criteria_defs = _resolve_grid_criteria(pre_registration, menu)
    if not criteria_defs:
        raise ValueError(
            "pre_registration's pass_rule resolved zero menu-shaped criteria (none of its "
            "criteria carry `source`/`reducer` fields, directly or via `menu`) -- evaluate_grid "
            "is for menu-shaped pass rules only; route a legacy pass_rule through "
            "evaluate_pass_rule_criteria instead"
        )

    eras = _load_campaign_data_policy_eras()
    variant_ids = list(protocol_results_by_variant.keys())

    grid: dict = {}
    spec_errors = []
    for crit in criteria_defs:
        cid = crit.get("id")
        if not cid:
            raise ValueError(f"a resolved grid criterion has no id: {crit!r}")
        row = {}
        for variant_id in variant_ids:
            cell = _evaluate_grid_cell(crit, protocol_results_by_variant[variant_id], eras)
            row[variant_id] = cell
            if cell["result"] == "SPEC_ERROR":
                spec_errors.append({"criterion_id": cid, "variant_id": variant_id,
                                     "reason": cell.get("reason")})
        grid[cid] = row

    if spec_errors:
        return {
            "result": "SPEC_ERROR",
            "criteria": [c.get("id") for c in criteria_defs],
            "variants": variant_ids,
            "grid": grid,
            "idea_status": None,
            "reason": f"{len(spec_errors)} cell(s) could not be evaluated: {spec_errors}",
        }

    all_cell_results = [cell["result"] for row in grid.values() for cell in row.values()]
    if any(r == "FAIL" for r in all_cell_results):
        idea_status = "refuted"
        reason = "at least one criterion FAILed with sufficient data on at least one variant"
    elif any(r == "INCONCLUSIVE" for r in all_cell_results):
        idea_status = "inconclusive"
        reason = "no criterion FAILed, but at least one cell lacked sufficient data to judge"
    else:
        idea_status = "validated"
        reason = "every criterion PASSed on every variant"

    return {
        "result": "GRID_EVALUATED",
        "criteria": [c.get("id") for c in criteria_defs],
        "variants": variant_ids,
        "grid": grid,
        "idea_status": idea_status,
        "reason": reason,
    }
