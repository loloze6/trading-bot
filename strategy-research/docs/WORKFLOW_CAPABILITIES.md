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
- A background campaign process (`RUNBOOK.md` §1c) and an interactive session touching the same state files (`campaign_queue.yaml`, `campaign_knowledge_base.yaml`, `config/detector_wishlist.yaml`) is a real conflict, not a hypothetical one — see `docs/analysis-reports/INCIDENT_20260710.md`; treat any disagreement as requiring recomputation from source artifacts, never a guess.

### New component code
- If a hypothesis requires an indicator not in STRATEGY_CONFIG_REFERENCE.md's catalog,
  the pipeline MUST emit a component_gap pause and a component_proposal.md.
- Human reviews the proposal, writes the component following STRATEGY_EXTENDING.md,
  and resumes via human_resolution.yaml.
- DO NOT invent component class names that don't exist. Always check the catalog first.
  If unsure whether a variant is achievable via config, check the "Variants via config"
  section of the relevant component entry.

### Holdout execution
- The holdout window is `holdout_range` in config/campaign_data_policy.yaml (a closed
  range; never restate its dates) and requires explicit --holdout --i-understand flags.
  run_protocol.py takes the range from the policy only (CUL-339): a protocol `holdout`
  block that disagrees with it (e.g. `end: null`) is refused before any data is fetched.
  Omit the block, or copy the policy range exactly.
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
| **Hypothesis needs a timeframe with no `<SYMBOL>_<TF>.csv` on disk (4h, 30m, ...)** | **No fetch needed.** `CandleBuilder` (`data/data_manager.py:326`) aggregates ANY finer cached interval up to the target on the BACKTEST path, not only the live path — its own `add_row()` is documented as "Backtest path: ingest one historical DataFrame row". Set the protocol's `timeframe` and the engine builds those bars from the 1h (or 5m/1m) cache. **Verified 2026-08-27:** 48 x 1h BTCUSDT rows fed to `CandleBuilder(interval_seconds=14400)` produced 11 completed 4h candles with open/high/close matching the source rows exactly. Fetching a `_4h.csv` is redundant whenever a finer cache already spans the window — this exact mistake was made on 2026-08-27 and the redundant fetch reverted. |
| Hypothesis needs funding rate or Fear & Greed data | `aux_feeds: ["funding_rate"]` or `["fear_greed"]` + the matching existing component — no new code (run_044's original false component_gap on this exact point, 2026-07-04, is the cautionary example) |
