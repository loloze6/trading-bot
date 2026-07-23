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

C7-EXT-R (2026-07-22, remediation of the independent audit in
docs/session_reports/20260722_c7ext_audit.md) repairs G6, which the audit
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
# in docs/venue_survey_20260719.md (Binance / Kraken / Bybit perps).
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
