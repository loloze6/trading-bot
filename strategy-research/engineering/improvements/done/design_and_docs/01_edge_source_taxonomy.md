# Improvement 01 — Edge-Source Taxonomy & Causal Root-Cause Diagnostics

## Gap

`hypothesis-design` and `innovation-expansion` currently generate signal variants from a **form template** (reverse / behavioral / regime-specific / alternative-data), not from a theory of *why* a signal should have positive expected value. Nothing requires a hypothesis to state a structural reason the market would pay for this signal. As a result, most generated hypotheses are permutations of price/volume indicators — different shapes of the same non-edge.

Symmetrically, on the interpretation side, `verdict-interpreter`'s 5 diagnostic rules are threshold pattern-matches (`forecast_return_corr < 0.03` → pivot) with no requirement to explain the failure mechanistically. `root_cause` is a free-text field that is easy to fill vaguely. This means `pivot` verdicts spawn new hypotheses with no accumulated reason to expect them to differ from what just failed.

This improvement closes both ends: hypotheses must **declare** a mechanism before a signal formula is written, and verdicts must **check** the outcome against that declared mechanism, not just against a metric threshold.

## Part A — Edge-source taxonomy (generation side)

### New required field in `hypothesis_card.yaml`

Add:

```yaml
edge_source:
  category: enum[information_asymmetry, structural_forced_flow, liquidity_provision, cross_venue_dislocation]
  specific_mechanism: string   # 1-2 sentences: what specifically creates this edge
  why_not_arbitraged: string   # why hasn't this already been competed away
  evidence_type: enum[price_volume_only, order_book, funding_open_interest, liquidation_data, cross_exchange, other_external]
```

Definitions to embed in the `hypothesis-design` skill prompt:

- **information_asymmetry** — someone (informed traders, insiders, faster data consumers) knows something before price fully reflects it, and the signal proxies for that knowledge.
- **structural_forced_flow** — flows that happen because of mechanical/contractual reasons, not opinion: liquidation cascades, funding rate settlement, options gamma hedging, index rebalancing, margin calls.
- **liquidity_provision** — edge from being paid to provide immediacy (spread capture, market-making), not from directional prediction.
- **cross_venue_dislocation** — temporary price divergence between related instruments/venues (perp-spot basis, lead-lag between exchanges) that a signal exploits before it closes.

### Skill constraint changes — `hypothesis-design`

Add a **hard constraint**: the skill must not proceed to `signal_concept` until `edge_source` is fully populated. If `evidence_type = price_volume_only`, the skill must additionally justify in `why_not_arbitraged` why a pure price/volume signal would still have edge (this is intentionally a high bar — it should push the model toward `order_book`, `funding_open_interest`, `liquidation_data`, or `cross_exchange` evidence types by default).

### Skill constraint changes — `innovation-expansion`

Current requirement: at least one reverse, one behavioral, one regime-specific variant. Add: **at least one variant per family must use a non-`price_volume_only` evidence_type.** If the `expanded_hypothesis_card.alternative_data_candidates` field would otherwise be empty or deprioritized, this makes it mandatory for at least one variant.

## Part B — Causal root-cause taxonomy (interpretation side)

### Replace free-text `root_cause` in `verdict_interpretation.yaml` with a structured field

```yaml
root_cause:
  mechanism_failure: enum[
    already_priced_in,
    lag_mismatch_to_regime_persistence,
    no_informational_content_this_venue,
    signal_real_but_subscale_vs_costs,
    indicator_incompatible_with_asset_flow,
    entry_exit_execution_gap,        # cross-reference to Improvement 03
    regime_misattribution,            # cross-reference to Improvement 02
    edge_arbitraged_away,
    insufficient_sample_inconclusive
  ]
  supporting_evidence: string   # must cite specific diagnostic_metrics / trade_diagnostics fields, not restate the verdict
  confidence: enum[high, medium, low]
```

### New / modified diagnostic rules in `verdict-interpreter`

Keep the existing 5 rules as **triggers**, but require each triggered rule to resolve to one of the `mechanism_failure` enum values above using the evidence available (including the new Improvement 02 regime report and Improvement 03 trade diagnostics — this skill cannot be finalized until those two land). Concretely:

| Existing rule trigger | Must resolve to (using new evidence) |
|---|---|
| `weak_signal` (`forecast_return_corr < 0.03`) | `already_priced_in`, `no_informational_content_this_venue`, or `edge_arbitraged_away` — distinguish using `edge_source.category` and asset liquidity/maturity, not the correlation number alone |
| `cost_drag` | `signal_real_but_subscale_vs_costs` — confirm signal direction is correct (positive `forecast_return_corr`) before accepting this, otherwise it's actually `weak_signal` |
| `signal_inversion` | check trade-level MAE/MFE (Improvement 03) before concluding true inversion vs. `entry_exit_execution_gap` producing an apparent inversion |
| `regime_uninformative` | must consult `regime_detector_report.yaml` (Improvement 02) — if detector confidence is low, resolve to `regime_misattribution`, not `lag_mismatch_to_regime_persistence` |
| `parameter_exhausted` | `edge_arbitraged_away` or `insufficient_sample_inconclusive` depending on sample size at exhaustion |

### Prescribed action must follow from mechanism, not from the rule alone

Add a mapping table to the skill:

| mechanism_failure | Prescribed action |
|---|---|
| `already_priced_in` | pivot to a different `edge_source.category`, do not retry `price_volume_only` variants |
| `lag_mismatch_to_regime_persistence` | refine (parameter altitude 1) — adjust lookback/threshold |
| `no_informational_content_this_venue` | escalate to a venue/asset with the structural property this mechanism requires |
| `signal_real_but_subscale_vs_costs` | refine — raise trade filter, or escalate to a lower-fee venue/instrument |
| `indicator_incompatible_with_asset_flow` | pivot family entirely, exclude this indicator category for this asset going forward (feeds Improvement 04/05) |
| `entry_exit_execution_gap` | refine at the execution layer only — do not discard the signal (see Improvement 03) |
| `regime_misattribution` | halt hypothesis-level conclusions; route to regime detector fix (see Improvement 02) before re-evaluating |
| `edge_arbitraged_away` | pivot category, note in knowledge base as a "known-competed" mechanism for this asset (feeds Improvement 05) |
| `insufficient_sample_inconclusive` | do not kill; flag for extended protocol / more windows before final verdict |

## Orchestrator changes

- `workflow/run_phase1_research.py`: routing after `verdict_interpreter` must branch on `root_cause.mechanism_failure`, not just `verdict`. If `mechanism_failure = regime_misattribution`, force a route to the regime-auditor stage (Improvement 02) before any new run is spawned.
- `workflow_artifacts/schemas/hypothesis_card.schema.json` and `workflow_artifacts/schemas/verdict_interpretation.schema.json`: add required fields above; validation must reject a hypothesis card missing `edge_source` or a verdict missing structured `root_cause`.

## Acceptance criteria

1. No `hypothesis_card.yaml` can pass schema validation without a populated `edge_source` block.
2. At least one variant per `expanded_hypothesis_card.yaml` has `evidence_type != price_volume_only`.
3. Every `verdict_interpretation.yaml` with verdict `refine`/`pivot`/`escalate`/`kill` has a `mechanism_failure` enum value and non-empty `supporting_evidence` that references a specific metric field (spot-check: evidence string must contain a field name from `protocol_result.yaml` or `trade_diagnostics.json`).
4. A `regime_misattribution` mechanism_failure always routes to regime-auditor before spawning a new run (verifiable in orchestrator logs / `pipeline_state.audit_log`).
