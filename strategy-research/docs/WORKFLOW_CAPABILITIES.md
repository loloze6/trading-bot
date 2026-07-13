# WORKFLOW_CAPABILITIES.md
What the research pipeline can do autonomously vs what requires human action.
Read this before deciding whether to pause for human review.

## What the pipeline can do WITHOUT human action

### Strategy expression
- Any combination of existing components, transforms, regimes in STRATEGY_CONFIG_REFERENCE.md
- Variant patterns (sign-flip, scaling, parameter ranges) — see Variants section per component
- New regime modes (threshold_rules, score, score_product, different thresholds, veto combinations)
- Multi-component ensembles (weighted combination of signals in one regime)
- Any transform pipeline ordering allowed by STRATEGY_CONFIG_REFERENCE.md ordering rules
- Funding-rate or Fear & Greed signals via `aux_feeds` + `FundingRateMeanReversionComponent` /
  `FearGreedContrarianComponent` (STRATEGY_CONFIG_REFERENCE.md §4/§4a) — these already exist and
  have working reference configs (run_041, run_042). Do NOT emit component_gap for these.

### Research loop
- Generate, validate, and refine hypotheses autonomously (stages 1-4)
- Emit and schema-validate candidate configs (stage 5)
- Run 22-window walk-forward protocol across 2 symbols (stage 6, tool)
- Interpret diagnostic metrics and choose altitude (refine/pivot/escalate) (stage 7)
- Scaffold the next run with updated brief and findings_carryover (automatic)
- Climb from parameter tuning → hypothesis pivot → instrument escalation

### Instrument escalation
- Switch between symbols in the coin_universe.yaml (see ENHANCE_04_COIN_UNIVERSE)
- Run the same config on a different symbol and compare diagnostics

## What ALWAYS requires human action

### Concurrent writers (2026-07-10)
- A background campaign process (`RUNBOOK.md` §1c) and an interactive session touching the same state files (`campaign_queue.yaml`, `campaign_knowledge_base.yaml`, `config/detector_wishlist.yaml`) is a real conflict, not a hypothetical one — see `incident_20260710/INCIDENT.md`; treat any disagreement as requiring recomputation from source artifacts, never a guess.

### New component code
- If a hypothesis requires an indicator not in STRATEGY_CONFIG_REFERENCE.md's catalog,
  the pipeline MUST emit a component_gap pause and a component_proposal.md.
- Human reviews the proposal, writes the component following STRATEGY_EXTENDING.md,
  and resumes via human_resolution.yaml.
- DO NOT invent component class names that don't exist. Always check the catalog first.
  If unsure whether a variant is achievable via config, check the "Variants via config"
  section of the relevant component entry.

### Holdout execution
- The holdout window (2025-01-01 onward) requires explicit --holdout --i-understand flags.
- Never run holdout automatically. Always human-triggered.

### Capital deployment
- Paper trading gate and live deployment are human decisions.
- The pipeline ends at "promote + holdout passed." What happens after is human.

### Campaign restart after space_empty
- If the campaign terminates with status: space_empty (all reasonable instruments and
  components exhausted), a human defines the next research question.

## Common confusion — what looks like it needs human but doesn't

| Situation | Action |
|---|---|
| LLM invents a component name | Check "Variants via config" in STRATEGY_CONFIG_REFERENCE.md — the variant likely exists |
| Regime fires too rarely | Relax regime thresholds in config — no new code |
| Signal direction inverted | Negative scaling_factor or negate transform — no new code |
| Need multiplicative regime scoring (ER × VR) | Use `mode: "score_product"` with per-component `divisor` keys — no new code |
| Want bidirectional signal | long_only: false on RSIPullbackComponent — no new code |
| Want lower-band Keltner | scaling_factor: -20.0 — no new code |
| Want wider/tighter Keltner | atr_multiplier parameter — no new code |
| Want slower/faster EMA | fast_period, slow_period parameters — no new code |
| Hypothesis needs funding rate or Fear & Greed data | `aux_feeds: ["funding_rate"]` or `["fear_greed"]` + the matching existing component — no new code (run_044's original false component_gap on this exact point, 2026-07-04, is the cautionary example) |
