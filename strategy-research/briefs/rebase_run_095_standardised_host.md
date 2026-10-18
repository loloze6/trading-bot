---
# research_brief_new_pipeline.md -- step 0, idea intake.
#
# 1. Copy this file to strategy-research/briefs/<your_brief_name>.md.
# 2. Replace every "<FILL IN...>" below. Registration refuses a copy that still
#    carries that text anywhere in this block.
# 3. Register it: python workflow/run_campaign.py register --brief
#    briefs/<your_brief_name>.md --priority <n> --notes "<n>"
#    (RUNBOOK.md section 1a-bis lists the checks to run before any LLM spend).
#
# Add no `promotion` block: the grid and the profit bars decide (D-043).
# Prose below the closing '---' is for people only; the orchestrator never reads it.

# A one- or two-word label for the kind of idea (registration needs it).
strategy_domain: "short_horizon_reversal"

# The idea: what you think happens in this market and why; nothing about how the pipeline runs.
# Copy the idea word for word, in the words of the person who gave it to you: do not paraphrase, shorten or strengthen it (a hedged "would allow" must not become "generates").
research_goal: >
  Re-expression of run_095's host, the negated one-day price move on BTC, with its forecast standardised (D-148, D-149) instead of scaling_factor 20 and a clip at 20, on fold D, the fold run_095 ran on. On run_095's windows 27 to 46 percent of bars sat at the clip, so the position size said little about the move's size. The signal, the coin, the venue and the fold are unchanged; only the scale is. A new lineage: no claim from runs 094 to 096 carries over.

  run_094's thesis, unchanged: Large overnight gaps (>1% of prior close) from news/futures fixing overshoot market equilibrium; gap-fills recover within 1-3 days producing predictable mean-reversion returns.

# The exchange this idea trades on.
venue: "kraken"

# The product on that exchange (a venue and product pair listed in config/venue_tradability.yaml).
product: "perp"

# The coin(s) to test, in BASEQUOTE form; write the same list again under machine_constraints.protocol.symbols below.
market_universe: ["BTCUSDT"]

# The bar size; write the same value again under machine_constraints.protocol.timeframe below.
timeframe: "1d"

# Data the idea needs beyond price bars, or none.
available_data: none

# OPTIONAL: your own criteria, as ids from config/criterion_menu.yaml (D-121, needs orchestrator.brief_criteria).
# To use it, delete the criteria_from line below and add:
# evaluation:
#   pass_rule:
#     criteria:
#       - id: whole_test_sharpe_positive
# Left as it is, step 1a picks the criteria from the menu.
criteria_from: hypothesis_generation

# OPTIONAL: a seeded config and block manifest, built exactly as given (D-110, D-112; needs orchestrator.exact_config_1b).
# Each is one entry of a constraints list: the entry's first line is the fixed sentence below, the JSON follows on the next lines.
constraints:
  - "Funding is not modelled on this venue: do not use the funding_rate feed."
  - |
    Build EXACTLY this strategy config (JSON)
    {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"}, "strategies": {"regimes": {"unknown": {"components": [{"id": "gap_reversion", "class": "strategies.strategy_components.PriceEvolutionComponent", "params": {"period": 1, "scaling_factor": 1.0}, "weight": 1.0, "transforms": [{"op": "standardise", "params": {"window": 60, "min_periods": 30, "target": 10, "cap": 20}}, {"op": "negate"}]}]}, "trending": null, "mean_reversion": null, "chop": null}}}
  - |
    Use EXACTLY this block manifest (JSON)
    {"block": {"kind": "forecast", "config_paths": ["/strategies/regimes/unknown/components/0"]}, "scaffolding": ["/regime_detector", "/strategies/regimes/trending", "/strategies/regimes/mean_reversion", "/strategies/regimes/chop"], "rationale": "The negated one-bar price evolution, standardised, is the signal under test; the ungated detector and the null regimes are engine scaffolding."}

# Scope for now: copy this block unchanged into every brief. Step 1a reads it as part of the brief.
scope: |
  Scope for now (2026-10-14).
  Kraken only: in scope by the operator's focus (D-130), not a capability limit; other venues' caches exist (e.g. Binance 4h files in trading-bot/local_data/) but are out of scope.
  One coin per variant: in scope. Each variant backtests one coin; an asset variant runs the same idea on a coin of another category. Not in scope: several coins inside one variant (a basket or a cross-coin ranking), because step 5a refuses a multi-coin variant (tools/variant_coin.py:725, rule G4 at :681-682) and tools/run_protocol.py backtests each coin alone (:2609, :2617).
  Price bars only, from the Kraken caches: in scope (trading-bot/local_data/kraken_<COIN>USD_<1h or 1d>.csv; the cache name carries the venue prefix, trading-bot/data/fetchers/ccxt_fetcher.py:123). Not in scope: any other feed. Funding is dropped for Kraken (tools/venue_resolver.py:134); it is kept only on the default venue, binance (tools/venue_resolver.py:57, the default path returning at :101-102); no order book, liquidation, cross-venue, on-chain or options feed exists (config/available_feeds.yaml:35-50); no open-interest fetcher exists (config/venue_data_capability.yaml:528-530 says available true and reachable_through_this_codebase false; :536-537 says no OI fetcher exists). Fear-and-greed is out of scope by the operator's decision of 2026-10-14 (wired: config/available_feeds.yaml:26), not by a capability limit.
  Perp priced on spot bars, funding not charged: in scope. A Kraken perp brief is backtested on Kraken spot prices with Kraken futures fees. Not in scope: real perp prices and funding payments, because config/venue_data_capability.yaml:472-481 declares the spot price proxy, tools/venue_resolver.py:117-137 writes price_proxy True and funding_modelled False into the protocol, and tools/run_protocol.py:2476-2480 prints it on every run.
  Hourly or daily bars: in scope (1h and 1d are the only Kraken caches on disk, 19 coins each). Not in scope: 4h, 15m or any other bar size, because no Kraken cache exists for them, a coarser bar is built from the hourly cache only through the opt-in trading.fetch_interval_seconds (docs/DATA_AVAILABILITY.md:25-38) that no brief field sets, and Kraken's live fetch returns only the 720 most recent candles (config/venue_data_capability.yaml:394-397).
  Claims expressible in the claim-test slots: in scope. Selector: all, event, regime, regime_change, calendar, quantile (tools/claim_tests.py:583-585). Outcome: fwd_return, fwd_volatility, fwd_max_drawdown, trend_ends (:635-636). Baseline: complement, placebo, other_selector (:686-687). Statistic: mean_diff, rank_ic, hit_rate, decay_curve (:752-753). Not in scope: a claim that needs a value outside these lists, because check_spec refuses it before any data is read (:888).
  The operator updates this when focus or capabilities change, recorded in DECISION_LOG.md.

machine_constraints:
  protocol:
    # The same coin(s) as market_universe above.
    symbols: ["BTCUSDT"]
    # The same bar size as timeframe above.
    timeframe: "1d"
    # Fold D, the fold run_095 ran on (config/folds.yaml).
    fold: D
    start: "2024-01-01"
    end: "2025-12-31"
    window_months: 4
---

# Re-base of the run_095 host with a standardised forecast (D-149)

run_095's host (the negated one-day BTC move, scaling_factor 20, clip at 20) is refused after 1b under
D-149; this brief re-expresses it with `standardise` as the scale step, on the same fold, as a new
lineage. Built by the operator's ruling of 2026-10-18.
