---
name: verdict-interpreter
description: Reads backtest findings against hypothesis-specific success criteria and produces
either a refined research brief for the next iteration or a final research decision.
---

# Verdict Interpreter

## Mission
Translate structured backtest findings into a concrete next action:
a refined brief that fixes the identified failure, or a final decision to kill or promote.

## Required inputs
- `protocol_result.yaml`       (backtest findings + hypothesis_verdict criteria_results + diagnostics —
                                every run always executes a full backtest, E-039)
- `pass_rule_evaluation.yaml`  (K2, 2026-07-13 — REQUIRED. Machine-authored verdict from the
                                pre-registered, structured pass rule in pre_registration.yaml —
                                see "MACHINE-AUTHORED VERDICT" section below. When its `result` is
                                `PASS` or `FAIL`, its `hypothesis_verdict`/`lineage_routing` fields
                                are COPY-THROUGH, not independently re-decided. When its `result` is
                                `legacy_not_evaluable` or `SPEC_ERROR` — including every run's
                                pre_registration.yaml before K2, e.g. run_057's own — this file
                                carries no binding verdict and you decide exactly as before K2.)
- `validation_protocol.yaml`   (descriptive context ONLY as of K2 — its own decision_rules/
                                required_evidence are NOT decision-bearing; see below)
- `backtest_spec.yaml`         (config_rationale: what config choices mapped to which claims)
- `research_brief.yaml`        (original research question and constraints)
- `campaign_state.yaml`        (cross-run altitude history; what has been tried and at which altitude)
- `trade_diagnostics.json`     (Step 03 — optional; present when trades occurred. Read summary block.)
- `post_backtest_routes`       (E-039/CUL-264, 2026-09-11 — optional, injected directly into this
                                stage's own handoff, not a separate file. Present only when a real
                                backtest ran and produced measured trade/window data. See the
                                dedicated section below — read it, it is evidence, NOT a decision.)

## MACHINE-AUTHORED VERDICT (K2, 2026-07-13)

`pass_rule_evaluation.yaml` (written by `tools/verdict_criteria_evaluator.py` during
`protocol_execution`, before this stage runs) is the DECISION authority whenever it
carries one. Your job shifted: explain WHY, cite it, and supply the qualitative fields
no formula can produce (`root_cause`, `config_to_failure_map`, `trade_attribution`) —
not re-decide `hypothesis_verdict`/`lineage_routing` independently when it already has.

- `result: PASS` or `FAIL` — copy `hypothesis_verdict` and `lineage_routing` from it
  VERBATIM into `verdict_interpretation.yaml` (B4 copy-through discipline — do not
  paraphrase, do not re-derive). If your own diagnostic reading (Rules 1-6 below)
  disagrees with its verdict, do NOT silently overwrite it either direction — write
  your disagreement into `altitude_justification` and set a `human_pause` per the
  standing disagreement rule (see RUNBOOK.md's pause table); a stage output that
  contradicts `pass_rule_evaluation.yaml` without flagging it is a conformance
  violation, not a judgment call.
- `result: legacy_not_evaluable` or `SPEC_ERROR`, or absent `hypothesis_verdict`/
  `lineage_routing` with `discretion: stage` set — no binding verdict exists for this
  run (a legacy pre_registration.yaml, or a pre-registered branch that explicitly opted
  into stage discretion). Decide `hypothesis_verdict`/`lineage_routing` yourself, using
  Rules 1-6 below, exactly as this skill worked before K2.
- Check `branches_failed` (not just `statement_branch_matched`) when writing
  `criteria_summary` — every failing branch is recorded, never hidden, even though only
  the first (id-order) selects the routing decision.

Rule 6 and the other five diagnostic rules below are UNCHANGED by K2 — they still drive
`root_cause`/`altitude_justification`'s qualitative content on every run; only the
PASS/FAIL/routing decision itself moves to the machine when a structured pass rule exists.

## Post-backtest route (E-039/CUL-264, 2026-09-11) — evidence, NOT a second decision authority

If this run's handoff carries `post_backtest_routes`, it is a REAL, measured
go/no-go computed mechanically from this run's actual backtest (real trades
where available, CUL-272; otherwise a real correlation/cost estimate,
CUL-264) — never a guess, and never the removed A8.6 pre-flight (that gate
estimated an activation rate before any backtest ran at all; this is
computed *after*, from real numbers).

**This is explicitly NOT like `pass_rule_evaluation.yaml` above.** It does
not bind your `hypothesis_verdict`/`lineage_routing` the way a `PASS`/`FAIL`
machine verdict does. Treat each window's `route` exactly like any other
diagnostic (`forecast_return_corr`, `cost_drag_pct`) — supporting evidence
you weigh alongside everything else, never a label you copy through
verbatim or a check you can skip your own analysis because of:

- A `kill_no_ic`/`kill_cost_hurdle`/`refine_*` route is a real, computed
  signal worth taking seriously — but still requires your own root-cause
  reasoning (Rules 1-6 below), same as any other bad diagnostic number.
- `inconclusive_insufficient_data` means the sample was too small to trust
  the route's own math (too few effective observations or trades) — treat
  this as **informationless**, not as a soft kill signal. Do not let a small
  sample masquerade as a negative result.
- If several windows disagree (one `kill_no_ic`, another clean), that
  disagreement is itself evidence — say so, do not silently average it away.

## Required outputs
- `verdict_interpretation.yaml`   (structured findings summary — always required)
- `findings_carryover.yaml`       (required when lineage_routing = refine, pivot OR escalate)
- EXACTLY ONE of the following:
  - `proposed_brief.yaml`         (if lineage_routing = refine or pivot)
  - `escalation_request.yaml`     (if lineage_routing = escalate)
  - `research_decision.yaml`      (if lineage_routing = terminate or hypothesis_verdict = promote)

## Output requirements
`verdict_interpretation.yaml` must include:
- hypothesis_id
- protocol_verdict          # from protocol_result.yaml hypothesis_verdict.verdict (legacy field,
                            # retained as a mirror — see hypothesis_verdict/lineage_routing below)
- hypothesis_verdict        # K2/A8: kill | refine | promote — is the MECHANISM dead? Copy-through
                            # from pass_rule_evaluation.yaml when it has a binding verdict (see
                            # MACHINE-AUTHORED VERDICT above); otherwise your own diagnostic judgment.
- lineage_routing           # K2/A8: terminate | refine | pivot | escalate — what does the CAMPAIGN
                            # do next? A SEPARATE question from hypothesis_verdict (run_057's own
                            # incident: mechanism dead + pivot routing were forced into one slot).
                            # Same copy-through/independent-judgment split as hypothesis_verdict.
- status                    # LEGACY mirror field, derived: status = lineage_routing when it's
                            # refine/pivot/escalate; status = kill when hypothesis_verdict == kill
                            # regardless of routing; status = promote when hypothesis_verdict ==
                            # promote. Kept so older tooling/logs reading a single-word summary
                            # never breaks — hypothesis_verdict/lineage_routing are authoritative,
                            # status is derived FROM them, never the reverse.
- criteria_summary          # list: each criterion → PASS/FAIL/UNTESTED + actual value. When
                            # pass_rule_evaluation.yaml has a binding verdict, this must be
                            # consistent with its criteria_results/branches_failed, not a
                            # separately-invented set.
- primary_failure_mode      # the single most likely explanation for failure
- config_to_failure_map     # which specific config choice contributed to the primary failure
- untested_criteria         # list of criteria that could not be evaluated
- proposed_change_dimension # one word identifying what is being changed (e.g. er_threshold,
                            # smooth_period, signal_component, regime_mode). Used to detect
                            # consecutive same-dimension changes across runs.
- hypothesis_family         # short label for the signal family (e.g. rsi_mean_reversion,
                            # keltner_breakout). Used for circuit-breaker family tracking.
- altitude_justification    # one sentence citing the specific diagnostic value that drove
                            # the altitude choice (required; do not omit).
- root_cause                # IMPROVEMENT 01: structured causal explanation (see section below).
                            # Required for all non-promote verdicts.
- trade_attribution         # Step 03: required when trade_diagnostics.json is available
                            # (see STEP 03 — Trade Attribution section below).

`proposed_brief.yaml` (when lineage_routing = refine):
- must be a valid research_brief.yaml (same schema as input brief)
- must change EXACTLY ONE aspect of the hypothesis from the previous brief
- must state explicitly in a `change_from_previous` field what changed and why
- must NOT change the core research question unless the primary_failure_mode indicates
  the hypothesis itself is wrong (not just the implementation)
- C9 (K2, 2026-07-13): this content is checked against campaign_knowledge_base.yaml for an
  exhausted/forbidden family BEFORE the orchestrator scaffolds the next run
  (`_route_refine`) — do not name a family the KB already marks exhausted with no open
  reactivation_condition; that pauses the pipeline rather than proceeding.

`proposed_brief.yaml` (when lineage_routing = pivot):
- must represent a STRUCTURALLY DIFFERENT hypothesis (different signal family or regime mode)
- must carry forward lessons from the failed hypothesis via `findings_carryover` field
- must explain in `change_from_previous` WHY the previous family was exhausted
- C9 (K2, 2026-07-13): `_route_pivot` itself does not read proposed_brief.yaml (the next
  run's hypothesis is formalized later, by hypothesis_generation) — but it DOES scan
  `primary_failure_mode`/`config_to_failure_map`/`root_cause`/`findings_carryover.yaml`'s
  own prose for a KB-exhausted family before scaffolding. Naming an exhausted family
  (e.g. a Keltner variant) anywhere in that prose pauses the pipeline the same way.

## REQUIRED OUTPUT — findings_carryover.yaml

`findings_carryover.yaml` is MANDATORY whenever status is refine, pivot, or escalate.
You MUST produce this file in the **same response** as proposed_brief.yaml or escalation_request.yaml.
Do not emit proposed_brief.yaml or escalation_request.yaml without also emitting findings_carryover.yaml.

## CRITICAL — do not claim untested variants as explored space

`expanded_hypothesis_card.yaml` (if present) may list multiple variants (V1, V2, V3...).
Only the variant that actually appears in `protocol_result.yaml` was executed — typically
V1 only. Before writing any statement in `what_not_to_try` that references a specific
parameter value, configuration, or variant, verify that value appears in
`protocol_result.yaml` or `backtest_spec.yaml` (the config that actually ran), NOT just in
`expanded_hypothesis_card.yaml` (proposals that may never have run).

FORBIDDEN: writing "[parameter] already tried/tested/exhausted" for any value that only
appears in `expanded_hypothesis_card.yaml`'s untested variants (V2 onward, when only V1
executed). This is a false claim that permanently and incorrectly forecloses real search
space for all future runs reading this carryover.

If you want to note that a variant was proposed but not tested, use this framing instead:
"V2 (ATR=1.8) was proposed by innovation_expansion but not executed — still untested,
available for future exploration" — this is accurate and distinct from claiming it failed.

`findings_carryover.yaml` must include:
- hypothesis_id
- what_failed: list of criteria that FAILed
- diagnostic_rule_applied: "Rule N: <one-line description of the matched condition>"
- diagnostic_snapshot: {forecast_return_corr, cost_drag_pct, gross_pnl, uninformative_regimes}
- what_not_to_try: list of approaches ruled out by the diagnostics — ONLY cite parameter
  values or configs that appear in protocol_result.yaml (actually executed). Do NOT cite
  expanded_hypothesis_card.yaml variant proposals as tested. See CRITICAL section above.
- next_altitude: refine | pivot | escalate (the decision taken)
- parameter_bracket: (optional — populate ONLY when the bracketing condition is met; omit otherwise)
    dimension: <the parameter dimension being tuned, e.g. min_score>
    too_tight_value: <value that produced too few trades / over-filtered>
    too_loose_value: <value that produced too many trades / under-filtered>
    last_tried_value: <the value used in the run that produced THIS carryover>
    direction_history: [<ordered list of outcomes, e.g. tight, loose>]

Bracket population rule: when status is refine AND the same dimension has been tried in
BOTH directions across runs (one producing too few trades, one too many), populate
parameter_bracket with the bracket bounds derived from the two bounding runs.

Bracket consumption rule: when parameter_bracket is present in the INCOMING
findings_carryover.yaml (from the previous run), the next proposed value for that
dimension MUST be the midpoint of too_tight_value and too_loose_value. Do not step
further in either direction. Compute midpoint explicitly and state it in
proposed_brief.yaml change_from_previous.

`escalation_request.yaml` (when status = escalate):
- target: "new_component" | "instrument" | "timeframe"
- reason: which diagnostic value(s) drove this decision
- proposed_capability: brief description of what is needed
  (e.g. "FundingRateComponent: crypto-specific signal not in current catalog")

`research_decision.yaml` (when status = kill or promote):
- hypothesis_id
- decision: kill | promote
- rationale: which criteria drove the decision
- findings_archive: key metrics across all windows for the record

YAML formatting rule — applies to ALL string values in all artifacts:
- Any string value containing a colon (:) MUST use block scalar syntax (| or >) or be
  quoted with single or double quotes.
- List items (- items) that contain colons MUST be quoted: `- "key: value"` not `- key: value`
- This rule applies even inside nested mappings and multi-line values.
- Violation causes a YAML parse error that halts the pipeline.

## IMPROVEMENT 01 — Structured Root Cause (replaces free-text root_cause)

For every verdict that is NOT `promote`, populate a `root_cause` block:

```yaml
root_cause:
  mechanism_failure: <enum value — see table below>
  supporting_evidence: <must cite specific field names from protocol_result.yaml or trade_diagnostics.json>
  confidence: <high | medium | low>
```

### mechanism_failure enum — choose the FIRST matching value

| Diagnostic trigger | mechanism_failure to assign | Notes |
|---|---|---|
| `weak_signal` rule fires (corr < 0.03) | `already_priced_in`, `no_informational_content_this_venue`, or `edge_arbitraged_away` | Distinguish using `edge_source.category` from hypothesis_card: if category = `persistent_behavioral_bias` on a mature venue, prefer `already_priced_in`; if the signal is asset-specific, `no_informational_content_this_venue`; if a once-structural edge has degraded, `edge_arbitraged_away` |
| `cost_drag` rule fires (cost_drag > 80%) | `signal_real_but_subscale_vs_costs` | FIRST confirm `forecast_return_corr > 0` — if correlation is also negative, the root cause is `already_priced_in`, not cost drag. Cost drag only applies when the signal direction is correct. |
| `signal_inversion` rule fires (corr < -0.03) | `entry_exit_execution_gap` or `already_priced_in` | Check trade_diagnostics.json MAE/MFE first. If losers have large favorable post-exit moves (`post_exit_return_20bars > 0`) on a winning entry direction, root cause is `entry_exit_execution_gap`. Otherwise `already_priced_in`. |
| `regime_uninformative` rule fires | `regime_misattribution` or `lag_mismatch_to_regime_persistence` | MUST consult `regime_detector_report.yaml` (Improvement 02). If detector_confidence is low/medium → `regime_misattribution`. If detector_confidence is high AND regime label is valid but forward_return_mean near zero → `lag_mismatch_to_regime_persistence`. |
| `parameter_exhausted` (same parameter tried 2×) | `edge_arbitraged_away` or `insufficient_sample_inconclusive` | If total trade count ≥ 30, prefer `edge_arbitraged_away`. If total trade count < 30, prefer `insufficient_sample_inconclusive`. |
| Trade attribution `primary_weakness = holding_sizing` | `signal_real_but_subscale_vs_costs` OR `entry_exit_execution_gap` | Check: is per_trade_expectancy negative because of outsized losses (→ `entry_exit_execution_gap`) or because gross edge is too small (→ `signal_real_but_subscale_vs_costs`)? |
| Trade attribution `primary_weakness = entry` or `exit` | `entry_exit_execution_gap` | Execution problem; do not discard signal. |
| Trade attribution `primary_weakness = signal_direction` | `already_priced_in` | Signal itself is wrong. |
| Indicator does not suit this asset's flow dynamics | `indicator_incompatible_with_asset_flow` | Applies when an indicator designed for equities (e.g., MACD) shows consistent misalignment with crypto perpetual behavior; note in campaign_knowledge_base. |
| Diagnostics show `active_n_bars=0` combined with a nonzero `component_error_count`/`component_error_sample` (protocol_result.yaml, if a full backtest ran despite errors), OR any other clear engine/config-level fault (not a signal-quality or sample-size question) | `component_execution_error` | F6 (2026-07-04). This is an engineering failure, not a research finding — do NOT map it to `already_priced_in`, `insufficient_sample_inconclusive`, or any other signal-quality/power category. `status` should still be set descriptively (e.g. `refine`), but see the prescribed action below: the orchestrator's circuit breaker treats this mechanism_failure as an absolute stop regardless of `status` — it will never be silently upgraded into pivot/escalate/kill. |

### mechanism_failure → prescribed action

| mechanism_failure | Prescribed next action | Notes |
|---|---|---|
| `already_priced_in` | pivot to a different `edge_source.category` | Do NOT retry price_volume_only variants within the same category |
| `lag_mismatch_to_regime_persistence` | refine (altitude 1) — adjust lookback/threshold | Parameter problem, not signal problem |
| `no_informational_content_this_venue` | **Wishlist note only** — record "this mechanism requires a venue with property X" in findings_carryover.yaml notes. Do NOT generate an executable escalation_request until multi-venue infrastructure exists (A1.4). Route as `pivot` to a different mechanism/asset class, not `escalate`. | Until cross-venue feeds exist, "different venue" is not an executable target |
| `signal_real_but_subscale_vs_costs` | refine — raise `threshold_filter min_abs` (fewer, higher-conviction trades → longer avg holding → better edge/cost ratio). **Do NOT prescribe "lower-fee venue" as an escalation target** — multi-venue execution does not exist (A1.4). If cost hurdle is structurally unbeatable on current venues, route as `pivot` to a different signal class, not `escalate`. | Do NOT pivot signal; direction is correct. Venue prescription is wishlist-only. |
| `indicator_incompatible_with_asset_flow` | pivot family entirely; exclude this indicator category for this asset going forward | Feed to campaign_knowledge_base (Improvement 05) |
| `component_execution_error` | STOP — do not spawn a new run, do not record a trial or KB finding, do not mark the family failed. Human fixes the component/config, then re-runs fresh. | F6: the orchestrator enforces this as an absolute circuit-breaker override — see ORCHESTRATOR NOTE below |
| `entry_exit_execution_gap` | refine at execution layer only — do NOT discard the signal | Per Improvement 03; altitude 1 only |
| `regime_misattribution` | STOP — do not spawn new run; route to regime-auditor for investigation | See ORCHESTRATOR NOTE below |
| `edge_arbitraged_away` | pivot category; record in campaign_knowledge_base as known-competed mechanism | |
| `insufficient_sample_inconclusive` | do NOT kill; flag for extended protocol or more windows before final verdict | |

### ORCHESTRATOR NOTE — `regime_misattribution` routing

When `root_cause.mechanism_failure = regime_misattribution`:
- The orchestrator will pause the pipeline and route to regime-auditor before spawning any next run.
- Your job: set `status = refine` (not kill/pivot) and cite the detector confidence value and the
  regime label in `altitude_justification`.
- Do NOT escalate or kill on regime_misattribution — regime attribution is an instrumentation
  problem, not a hypothesis-level failure. Fix the measurement before re-evaluating the signal.
- Per A2.3 standing policy: if the regime auditor confirms the detector is unusable, the 
  orchestrator will switch to ungated-only generation for this symbol/timeframe. Your verdict
  should recommend ungated reformulation of the hypothesis.

### `supporting_evidence` format rule

Must cite at least one field name from `protocol_result.yaml` or `trade_diagnostics.json`:
```yaml
# GOOD
supporting_evidence: "forecast_return_corr=0.012 (p=0.71); n_trades_total=47; 
  cost_drag_pct=31% — signal direction roughly right but correlation indistinguishable 
  from zero across 22 windows."

# BAD — restates verdict without citing a field
supporting_evidence: "The signal does not predict returns well."
```

## Altitude decision logic

Decide `status` from `diagnostics` (in protocol_result.yaml) + `campaign_state.yaml`, in this order:

1. Read `campaign_state.yaml`: how many times each altitude has been used, what was changed.

2. If the primary FAIL is a parameter problem AND fewer than 2 parameter dimensions have been tried
   on DIFFERENT dimensions for this hypothesis → `refine` (altitude 1).

3. If 2+ parameter dimensions have been changed for this hypothesis with no improvement on the primary
   FAIL → hypothesis is parameter-exhausted. Climb to altitude 2: `pivot`.
   Apply Diagnostic interpretation rules (see section below) to choose the pivot intelligently.

4. If 2+ hypotheses in the same family have been pivoted through and all fail on the same root cause
   → family is exhausted. Climb to altitude 3: `escalate`.
   Apply Diagnostic interpretation rules (see section below) to choose the escalation target.
   When recommending escalate with target=instrument: read coin_universe.yaml and propose
   a specific symbol from the category whose strategy_affinity matches the current
   hypothesis's signal type. E.g. if the signal is momentum/trending, propose a coin from
   smart_contract_infra (strategy_affinity: [trending, breakout]) not from memecoin.

5. Only `kill` if: escalate has already tried the reasonable instrument set AND candidate component
   types for this research question, and all failed. Killing is answering the research question
   negatively — valid, but it must come AFTER search-space expansion.

## Required prerequisite reading
Read workflow_artifacts/skills/quant-fundamentals/SKILL.md before applying any rule below. If a rule's stated
mechanism conflicts with an identity in quant-fundamentals, quant-fundamentals is
authoritative — note the conflict in your output rather than silently following the rule
as originally written.

## Diagnostic interpretation rules
Apply these rules IN ORDER to the `diagnostics` block in `protocol_result.yaml`
before choosing an altitude. Each rule maps a numeric condition to a root cause,
which then drives the altitude choice.

RULE 1 — Cost drag dominates (trade-level dilution or duration problem):
  IF median_cost_drag_pct > 80% AND median_gross_pnl > 0:
    Root cause: the signal earns gross PnL but per-trade fees consume it.
    NOTE: cost_drag_pct = total_fees / |gross_pnl|. Fees and gross_pnl scale
    together under any position-size or leverage change, so cost_drag_pct is
    mathematically invariant to sizing. "Sizing problem" is not a valid diagnosis
    here. Do NOT propose leverage reductions, position-size changes, or framing
    this as a "sizing model" issue — they cannot affect this ratio by construction.
    Two candidate causes (cannot always be distinguished with current metrics):
    (a) Low-conviction trade dilution: many trades with small |price_return| drag
        down the aggregate. forecast magnitude distribution is the diagnostic.
        Fix: raise threshold_filter min_abs to cut low-conviction entries.
    (b) Short trade duration: positions close before price moves enough to offset
        fees. avg_trade_duration_bars would be the diagnostic, but this field does
        not yet exist in metrics.json (STEP_02 pending). If cause (b) is suspected
        (e.g. threshold_filter is already ≥ 15.0 and cost_drag persists), note
        in findings_carryover.yaml that the root cause is provisional — cause (b)
        cannot be ruled out until avg_trade_duration_bars is available.
    Do NOT pivot to a different signal — the signal works.
    Correct action at altitude 1: raise threshold_filter min_abs.
    Correct action at altitude 2 (pivot): keep the same signal; switch to a
    less-frequent entry rule (e.g. wider bands, higher min_score). Do NOT write
    a pivot brief that changes the signal family — that wastes a run.

RULE 2 — Signal has no directional edge:
  IF abs(median_forecast_return_corr) < 0.03 OR pvalue > 0.10:
    Root cause: the signal does not predict price direction.
    Correct action: pivot (altitude 2) to a structurally different signal.
    In proposed_brief.yaml, change the signal component (not just parameters).

RULE 3 — Signal is inverted:
  IF median_forecast_return_corr < -0.03 AND pvalue < 0.10:
    Root cause: the signal predicts the opposite of what the strategy bets.
    Correct action: pivot (altitude 2) to the reverse signal (e.g. long on RSI > 50
    instead of < 50, or short breakout instead of long breakout).
    This is a cheap pivot — same component, reversed logic.

RULE 4 — Regime is uninformative:
  IF all regimes in uninformative_regimes include the active strategy's regime:
    FIRST check n_bars for the active regime in regime_validity
    (available in protocol_result.yaml results[*].regime_validity[regime].n_bars).
    Compute the median n_bars for that regime across all 22 windows.
    IF median n_bars < 20:
      The near-zero forward_return_mean is likely noise from an insufficient sample,
      not evidence that the regime label is unpredictive. Do NOT conclude the regime
      is uninformative. Route to Rule 5 instead (regime fires too rarely → sample
      problem → relax thresholds).
    IF median n_bars >= 20:
      Root cause: the regime classifier does not identify a coherent market state.
      The forward_return_mean in that regime is near zero (< 0.0001) with enough
      bars to be reliable — the regime label itself is not predictive at this timescale.
      Correct action: pivot (altitude 2) to a different regime definition
      (e.g. score mode instead of threshold_rules, or different component thresholds).
      Document which regime was uninformative, its n_bars, and its forward_return_mean
      in findings_carryover.

RULE 5 — Signal works but regime is too rare (sample problem):
  IF win_rate_vs_sharpe == "win_rate PASS + sharpe FAIL"
  AND median_forecast_return_corr > 0.03
  AND median_cost_drag_pct < 80%:
    Root cause: signal has edge (win_rate, corr positive) but the regime fires too rarely
    for Sharpe to be statistically meaningful. Variance dominates.
    Correct action at altitude 1: relax regime thresholds to increase regime frequency
    (if not already tried). If already tried (check campaign_state), correct action at
    altitude 2: switch to a regime that fires more often (e.g. unknown/default, or a
    score-mode regime with a lower min_score).

RULE 6 — No diagnostic signal (all metrics null):
  IF median_forecast_return_corr is null AND median_gross_pnl is null:
    FIRST distinguish cause using per_symbol_summary in protocol_result.yaml.
    Check min_trade_count for every symbol in per_symbol_summary.

    CASE A — Pre-Phase-A / instrumentation failure:
      IF any symbol has min_trade_count > 0:
        Root cause: trades occurred but Phase-A instrumentation was absent (old run).
        Correct action: refine with the same brief. Do NOT count this run in
        parameter-dimension history or failed_families. Flag in findings_carryover.

    CASE B — Regime starvation (all symbols have min_trade_count = 0):
      Root cause: regime thresholds are set above the market's actual ER/VR
      distribution — the regime fired on zero bars across ALL 22 walk-forward
      windows. The signal never engaged. This IS informative: it tells you the
      threshold is too tight, not that the signal lacks edge.
      Count this run in parameter-dimension history (it is a data point).
      Correct action: INCREMENTAL threshold relaxation only. This is NOT permission
      to apply Rule 5's full prescription. Cautionary precedent: run_034 relaxed
      the ER threshold aggressively (0.50 → 0.35), causing corr to collapse from
      0.2145 → 0.014 and cost_drag to spike to 413%. Over-relaxation is as bad as
      over-tightening.
      - If parameter_bracket is present in findings_carryover.yaml for the regime
        threshold dimension: use the midpoint rule exactly (do not step further in
        either direction). Compute the midpoint explicitly and state it in
        proposed_brief.yaml change_from_previous.
      - If no bracket exists: relax by the minimum plausible step only (e.g. ER
        threshold: subtract 0.05, NOT 0.15+). Set parameter_bracket with
        too_tight_value = current threshold; too_loose_value = TBD (to be filled
        once over-trading is observed). Document the open bracket in
        findings_carryover.yaml so the next run can close it.
      Do NOT escalate timeframe or pivot signal — starvation is a threshold
      calibration problem, not a signal quality or timeframe problem.

PRIORITY: apply rules in order 1→6. The FIRST matching rule determines root cause and
altitude. Do not apply multiple rules to the same run. If no rule matches, default to
Rule 2 (no directional edge → pivot to different signal).

After applying a rule, populate `altitude_justification` in verdict_interpretation.yaml
with the EXACT diagnostic values that triggered the rule:
  altitude_justification: "Rule 1: cost_drag_pct=142.82% > 80%, gross_pnl=+21.94 > 0"

## Checklist
- Check TWO independent trade-count gates before treating corr or Sharpe as conclusive.
  These are separate checks — passing one does not satisfy the other.

  GATE B-CUMULATIVE: sum trade counts across ALL walk-forward windows and symbols
  (sum protocol_result.yaml results[*].trade_count). If the total is < 15: label the
  run "directional signal only, not validated" in verdict_interpretation.yaml
  primary_failure_mode. This catches extreme small-sample runs (e.g. a 3-trade lucky
  streak on a single window). Threshold is PROVISIONAL (set 2026-06-30) — see
  quant-fundamentals/SKILL.md Gate B for the basis and update protocol.

  GATE B-PER-WINDOW: note that a run with 11 windows at 2–3 trades each clears the
  cumulative floor (e.g. 44 total) while every individual window's Sharpe is computed
  from 2–3 trades — individually unreliable. Per-window thinness is enforced via the
  min_trade_count criterion in validation_protocol.yaml (a separate existing gate).
  Do not treat a cumulative pass as a substitute for a per-window pass. If
  min_trade_count appears in criteria_results as FAIL, honour it as a genuine failure
  independent of the cumulative total.
- Read criteria_results from protocol_result.yaml first. Do not re-derive the verdict.
- Read diagnostics block from protocol_result.yaml. Cite the specific value driving your altitude choice.
- Read campaign_state.yaml: recent_parameter_dimensions, failed_families, instruments_tried.
- Identify the primary_failure_mode by mapping FAIL criteria to failure_modes in validation_protocol.yaml.
- Map the failure to a specific config choice in backtest_spec.yaml config_rationale.
- For refine: change only the config element linked to the primary failure. Do not redesign.
- For pivot: produce a structurally different proposed_brief + findings_carryover.yaml.
- For escalate: produce escalation_request.yaml; do NOT produce proposed_brief.yaml.
- For kill: confirm at least 2 independent FAIL criteria before killing. If only 1 FAILs,
  recommend refine with a targeted fix.
- UNTESTED criteria are not failures. Do not kill based on untested criteria.
- Always populate `altitude_justification` with the specific diagnostic value used.

## Forbidden
- Do not change more than one hypothesis dimension in proposed_brief.yaml (refine case).
- Do not recommend new components or transforms not in STRATEGY_CONFIG_REFERENCE.md (refine case).
- Do not re-run or re-evaluate backtest numbers — accept protocol_result.yaml as truth.
- Do not promote unless ALL evaluable approve criteria pass.
- Do not promote if total trade count across all windows is < 15 (provisional floor —
  see quant-fundamentals/SKILL.md Gate B). A run below this threshold cannot be
  conclusively validated regardless of corr or Sharpe values.
- Do not promote if min_trade_count appears in criteria_results with result: FAIL.
  This is a hard block independent of the cumulative floor above: a run can have 69
  cumulative trades while still having windows with 0 trades, making per-window Sharpe
  uncomputable or degenerate in those windows. Both gates must pass independently.
- Do not refine the same parameter dimension twice consecutively.
- Do not kill before at least one escalate (instrument or component) has been attempted, UNLESS
  diagnostics prove the research question is definitively answered negatively (e.g.
  median_forecast_return_corr is significantly negative AND its reverse was already tested and failed).
- Do not pivot or escalate without citing the specific diagnostic value in altitude_justification.
- Do not emit both proposed_brief.yaml AND escalation_request.yaml — pick exactly one.
- Do NOT recommend pivot on a parameter dimension if a bracket exists in the incoming
  findings_carryover.yaml and the midpoint of that bracket has not yet been tested.
- Do not invent escalation targets. The ONLY permitted values for escalation_request.yaml
  target are: "instrument", "timeframe", "new_component". Any other value will crash the
  pipeline. Regime methodology changes (OR-gate, score-mode, different thresholds, new
  component type) are hypothesis-level changes — use status=pivot with a proposed_brief.yaml,
  not status=escalate. Brief constraints in the current run's research_brief.yaml are
  guidance for THAT run only; they do not prevent a pivot to a new brief that lifts those
  constraints.
- Do not output escalation_request.yaml or proposed_brief.yaml without also outputting findings_carryover.yaml in the same response.
- Do NOT read, cite, or otherwise consume `fragment_patterns.yaml` (2026-07-10).
  It is an ideation-only diagnostic artifact (basis: lifo_fragment,
  ideation_only) — ANY finding in it, including an apparently damning
  forecast-bin or duration/regime pattern, must never be used to relitigate,
  support, or override a verdict here. It is not in this skill's Required
  inputs for exactly this reason. If it is ever presented alongside the
  required inputs, ignore it for verdict purposes — it belongs to
  campaign_review's ideation stage, not here. See
  docs/VERIFICATION_DOCTRINE.md section 2 (the three-role model) for the
  model this enforces and test_fragment_patterns_firewall.py for the
  mechanical check.

## STEP 03 — Trade Attribution (required when trade_diagnostics.json is available)

Read `trade_diagnostics.json` summary block. Apply the decision table below to populate
`trade_attribution` in `verdict_interpretation.yaml`:

```yaml
trade_attribution:
  primary_weakness: <entry | exit | holding_sizing | signal_direction | none_healthy>
  evidence: <must cite specific trade_diagnostics_summary field values>
```

Decision table (apply first matching pattern):

| Pattern in `trade_diagnostics_summary` | `primary_weakness` |
|---|---|
| High `mfe`, low realized return AND `exit_efficiency_median` < 0.30 | `exit` — signal finds good moves, exits give them back |
| `entry_efficiency_median` < −0.10 | `entry` — entering late/early relative to signal degrades the edge |
| `pnl_concentration.pct_pnl_from_worst_decile_trades` > 80% (magnitude) AND `exit_reason_breakdown.signal_flip_pct` > 70% | `holding_sizing` — losses driven by uncapped adverse excursions; worst-decile trades dominate total PnL; no stop mechanism. Applies even when `stop_loss_pct = 0` — the absence of stops is the diagnosis. |
| `stop_loss_recovery_rate` > 0.50 AND `exit_reason_breakdown.stop_loss_pct` > 10% | `holding_sizing` — stops fired but trades would have recovered; stops are too tight |
| Poor `entry_efficiency_median`, poor `exit_efficiency_median`, AND `forecast_return_corr` < 0 | `signal_direction` — genuine signal problem, not execution |
| None of the above triggered | `none_healthy` |

Aggregate-median caveat: `exit_efficiency_median` is the median across ALL trades including
winners, which pulls it positive even when losers have deeply negative exit efficiency (e.g.,
Keltner 2025: overall median 0.44, loser-cohort median −1.46). The `pnl_concentration` pattern
catches this by looking at total PnL impact of the worst trades rather than per-trade efficiency.
Do not conclude `none_healthy` solely because `exit_efficiency_median` appears positive — check
`pct_pnl_from_worst_decile_trades` first.

Routing rule: when `primary_weakness` is `entry`, `exit`, or `holding_sizing`, the verdict
**must not** discard the underlying signal. These are execution-level problems (altitude 1
refine on execution logic), distinct from signal quality problems that warrant pivot.

A3.3 guard on `exit_efficiency`: this metric benchmarks realized returns against the best
possible exit in the holding window — an unattainable hindsight optimum. It is valid for
*relative comparison across variants and for trend detection within a family*. Do NOT
interpret `exit_efficiency_median = 0.35` as "35% of return was left on the table and is
achievable." Do not prescribe "capture the remaining X%" as a refinement target.

A3.5 regression fixture — `keltner_163`: the 163-trade Keltner ledger at
strategy-research/results/protocols/20260702T091324Z_18fad381/ has the following
settled canonical signature (post-reconciliation, 2026-07-02):

  2024 cohort (n=69): win_rate_net=50.7%, per_trade_expectancy_bps.mean=−26.2
  2025 cohort (n=94): win_rate_net=57.4%, per_trade_expectancy_bps.mean=−58.3

  NOTE: win_rate_net uses `profitable_net` (engine net-of-commission definition).
  Gross win rate (profit_loss_percent > 0) overstates by ~8–9 pp and is WRONG here.
  per_trade_expectancy_bps uses `net_portfolio_return_pct * 100` (portfolio-level net).
  Position-level gross bps understates expectancy magnitude by ~2× and is WRONG here.

  Named channel: `holding_sizing`
  Evidence string: "pct_pnl_from_worst_decile_trades=123% (2024) / 128% (2025), signal_flip_pct=95%,
  loser_median_mae grew 1.8%→2.7% (2024→2025); no stop mechanism; worst-decile trades
  wipe all gains. Winner avg (+62/+68 bps) stable; loser avg worsened −117→−228 bps."

  Any implementation of the trade attribution decision table must route the keltner_163
  fixture to `primary_weakness = holding_sizing` on the basis of `pct_pnl_from_worst_decile_trades`.
  If it routes to `none_healthy` or `signal_direction`, the aggregate-median caveat above
  has been ignored — re-check the decision table.

## IMPROVEMENT 02 — Regime Attribution Gate (mandatory for regime-gated hypotheses)

When the tested hypothesis is regime-gated (its config has a `regime_detector` block and
at least one strategy regime other than `unknown`), you MUST populate a `regime_attribution`
block in `verdict_interpretation.yaml`:

```yaml
regime_attribution:
  detector_confidence: <value from handoff field `regime_detector_confidence`, e.g. medium>
  signal_performs_in_intended_regime: <bool>   # from per_regime_metrics for the gated regime
  signal_performs_in_other_regimes: <bool>     # would it work ungated or in another regime?
  conclusion: <one of the four values below>
```

Apply this decision tree IN ORDER:

1. If `detector_confidence != high` for the tested symbol/timeframe:
   - Check the handoff field `ungated_escape_eligible`.
   - If `ungated_escape_eligible: true` (pooled IC ~ 0, see rationale):
     → conclusion = `signal_bad_everywhere` (ungated evidence overrides; cite the ungated
       metric values from `ungated_escape_rationale` in `altitude_justification`).
   - If `ungated_escape_eligible: false`:
     → conclusion = `inconclusive_low_detector_confidence`
     → status MUST be `refine` (route back to regime-auditor, not kill or pivot)
     → altitude_justification must state: "Regime detector confidence is [level] for
       [symbol_timeframe]; cannot conclude signal_bad_everywhere without trusted regime
       partition. Routed to regime re-validation."
     → **FORBIDDEN: setting conclusion = signal_bad_everywhere while detector_confidence
       != high and ungated_escape_eligible = false.**

2. If `detector_confidence = high`:
   - Check per_regime_metrics for the gated regime and for ungated/default:
   - If signal performs well ONLY in a DIFFERENT regime than gated:
     → conclusion = `signal_good_wrong_regime_gate`
     → status = `refine` (altitude 1: change which regime is active, not the signal)
   - If signal performs poorly in ALL regimes (including ungated):
     → conclusion = `signal_bad_everywhere`
     → status = `pivot` or `kill` per normal rules
   - If signal performs well in the gated regime:
     → conclusion = `signal_good_regime_gate_correct`
     → continue to normal promotion path

## A3.4 — Sparse-trader Sharpe gate (mandatory)

Before applying any Sharpe-based diagnostic rule, compute:
  `below_floor_pct = fraction of windows with trade_count < 5`

If `below_floor_pct > 0.50` (more than half the windows are sparse):
- Suspend all `median_sharpe`-based rules.
- Use `per_trade_expectancy_bps` (from `hypothesis_verdict.diagnostics`) as the primary
  performance statistic.
- State in `verdict_interpretation.yaml` which statistic was used and why.
- If `per_trade_expectancy_bps` mean ≤ 0 with |t_stat| > 1.5: treat as a kill/pivot signal.
- If `per_trade_expectancy_bps` is unavailable in the diagnostics block: note the gap
  and fall back to win_rate + cost_drag as the primary evidence.

## A2.3 — IC measurement scope

### IC scope for ungated escape (A2.1)

`median_forecast_return_corr` in the diagnostics block is IC computed **on gated bars only** — the bars where the strategy actually placed trades, which occur exclusively inside the active regime. For a strategy gated to TRENDING (~1% of bars), IC=0.2145 on those bars does NOT represent all-bars IC.

**`ungated_escape_eligible` is set directly by the regime-auditor skill's own judgment** (see `workflow_artifacts/skills/regime-auditor/SKILL.md`'s A2.1 rules) — there is no automatic re-resolution step downstream that recomputes it from a measured all-bars IC (E-039 step 5: the mechanism that used to do this, `signal_prescreen`'s own `_resolve_ungated_escape`, was removed with the rest of that stage, and nothing replaced it — see `engineering/roadmap/E-037/FINDINGS.md`'s E037-07 entry). Treat `ungated_escape_eligible` as the regime-auditor's stated conclusion, not as a field you can independently re-derive from IC: cite its own `ungated_escape_rationale` when applying the A2.1 escape.

If no regime-auditor run exists for this symbol/timeframe, treat `ungated_escape_eligible` as indeterminate and note that in `altitude_justification`.

## Context rule
Read only the five input artifacts plus the handoff `regime_detector_confidence` field.
Minimal context.
