# Improvement 04 — Indicator Knowledge Library

## Gap

`hypothesis-design` selects a signal concept from scratch every run with no reference to prior knowledge about indicator behavior. There is no artifact encoding well-established properties of indicator classes — typical lag, regime affinity, crowding/arbitrage risk, data requirements. As a result indicator choice functions as a random draw from the model's training distribution rather than an informed decision, and the pipeline re-discovers (empirically, expensively) facts that are already well known — e.g., that trend-following indicators structurally underperform in ranging regimes.

This improvement adds a reference library the generation-side skills must consult, seeded with well-established domain knowledge and then enriched over time with this campaign's own empirical results (via Improvement 05).

## New artifact: `indicator_library.yaml`

Root-level, campaign-independent (this is domain knowledge, not run-specific), version-controlled like a schema.

```yaml
indicators:
  - id: string                     # e.g. "rsi_mean_reversion"
    category: string                # e.g. "oscillator", "trend_following", "volume_flow", "order_book_imbalance"
    known_regime_affinity:
      trending: enum[favorable, unfavorable, neutral]
      ranging: enum[favorable, unfavorable, neutral]
      high_vol: enum[favorable, unfavorable, neutral]
    typical_lag_bars: string        # qualitative or approximate range, e.g. "low (0-2 bars)"
    crowding_risk: enum[low, medium, high]   # how widely known/arbitraged this indicator class is
    data_requirements: enum[ohlcv_only, order_book, funding_open_interest, liquidation, cross_exchange]
    edge_source_compatibility: list[enum]    # which categories from Improvement 01's taxonomy this indicator class can plausibly support
    campaign_empirical_results:      # populated over time, pulled from campaign_knowledge_base.yaml (Improvement 05)
      - symbol_timeframe: string
        regime_tested: string
        outcome: enum[promising, failed, inconclusive]
        run_id: string
    notes: string
```

Seed this file with a starting set covering the major indicator classes already in use or likely to be proposed (moving averages / trend, oscillators / mean-reversion, volume-based, order-book-based, volatility-based). The seed content is domain knowledge (e.g., "RSI-style mean reversion is `unfavorable` in `trending` regime" is a textbook fact) — an implementation agent with market-knowledge access should populate this, not leave it empty pending backtests.

## Skill constraint changes — `hypothesis-design`

Before finalizing `signal_concept`, the skill must:
1. Look up the proposed indicator (or nearest category) in `indicator_library.yaml`.
2. Check `known_regime_affinity` against the hypothesis's proposed `target_market` regime conditions — if the pairing is `unfavorable`, the skill must either justify why this run expects an exception, or choose a different indicator/regime pairing.
3. Check `campaign_empirical_results` for this campaign — if this indicator category has already been tested and failed under the same symbol/timeframe/regime combination, the skill must not propose it again without a materially different `edge_source.specific_mechanism` (cross-reference Improvement 01) than what was already tried.
4. Prefer indicators whose `data_requirements != ohlcv_only` when `crowding_risk = high` for the OHLCV-only alternative — i.e., don't default to the most crowded indicator class when a less crowded one with compatible `edge_source_compatibility` exists.

## Skill constraint changes — `innovation-expansion`

When generating variants, consult the library to ensure variant diversity is real (different `category` and `data_requirements`), not just cosmetic (same category, reversed sign). Add a check: if all proposed variants map to the same `indicator_library` category, the expansion is rejected and must be redone.

## Maintenance

- `indicator_library.yaml` is updated automatically after every run: `campaign-review` (or a lightweight post-run hook) writes back to `campaign_empirical_results` using the run's `verdict_interpretation.yaml` and `root_cause.mechanism_failure` (Improvement 01). This is the same underlying data as `campaign_knowledge_base.yaml` (Improvement 05) — treat `indicator_library.yaml` as an indicator-indexed *view* over the knowledge base, not a separately maintained parallel store, to avoid drift.

## Schema/orchestrator changes

- `schemas/indicator_library.schema.json` — new.
- `workflow/run_phase1_research.py` — load `indicator_library.yaml` into the handoff context for `hypothesis_generation` and `innovation_expansion` stages.
- Add a lightweight post-run hook (or extend `campaign-review`) that writes empirical results back to the library.

## Acceptance criteria

1. `indicator_library.yaml` exists with at least the major indicator categories seeded with `known_regime_affinity`, `crowding_risk`, and `edge_source_compatibility` populated from domain knowledge (not left blank).
2. `hypothesis_generation` handoff includes the library; a spot-check of a generated hypothesis card shows its indicator choice is consistent with (or explicitly justifies deviation from) the library's regime affinity for that category.
3. Re-proposing an indicator category already marked `failed` for the same symbol/timeframe/regime in `campaign_empirical_results` is blocked unless a materially new `edge_source.specific_mechanism` is given.
4. After N runs, `campaign_empirical_results` entries are non-empty and traceable to specific `run_id`s.
