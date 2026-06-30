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
- `protocol_result.yaml`       (backtest findings + hypothesis_verdict criteria_results + diagnostics)
- `validation_protocol.yaml`   (original hypothesis success criteria and failure modes)
- `backtest_spec.yaml`         (config_rationale: what config choices mapped to which claims)
- `research_brief.yaml`        (original research question and constraints)
- `campaign_state.yaml`        (cross-run altitude history; what has been tried and at which altitude)

## Required outputs
- `verdict_interpretation.yaml`   (structured findings summary — always required)
- `findings_carryover.yaml`       (required when status = refine, pivot OR escalate)
- EXACTLY ONE of the following:
  - `proposed_brief.yaml`         (if status = refine or pivot)
  - `escalation_request.yaml`     (if status = escalate)
  - `research_decision.yaml`      (if status = kill or promote)

## Output requirements
`verdict_interpretation.yaml` must include:
- hypothesis_id
- protocol_verdict          # from protocol_result.yaml hypothesis_verdict.verdict
- status                    # YOUR decision: promote | refine | pivot | escalate | kill
- criteria_summary          # list: each criterion → PASS/FAIL/UNTESTED + actual value
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

`proposed_brief.yaml` (when status = refine):
- must be a valid research_brief.yaml (same schema as input brief)
- must change EXACTLY ONE aspect of the hypothesis from the previous brief
- must state explicitly in a `change_from_previous` field what changed and why
- must NOT change the core research question unless the primary_failure_mode indicates
  the hypothesis itself is wrong (not just the implementation)

`proposed_brief.yaml` (when status = pivot):
- must represent a STRUCTURALLY DIFFERENT hypothesis (different signal family or regime mode)
- must carry forward lessons from the failed hypothesis via `findings_carryover` field
- must explain in `change_from_previous` WHY the previous family was exhausted

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
Read skills/quant-fundamentals/SKILL.md before applying any rule below. If a rule's stated
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

## Context rule
Read only the five input artifacts. Minimal context.
