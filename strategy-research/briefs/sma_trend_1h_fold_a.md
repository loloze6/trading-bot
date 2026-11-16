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
strategy_domain: "SMA trend"

# The idea: what you think happens in this market and why; nothing about how the pipeline runs.
# Copy the idea word for word, in the words of the person who gave it to you: do not paraphrase, shorten or strengthen it (a hedged "would allow" must not become "generates").
research_goal: >
  the difference between price and sma with a combination of short term and long SMA can predict price evolution on BTC on 1h fold A

# The exchange this idea trades on.
venue: "kraken"

# The product on that exchange (a venue and product pair listed in config/venue_tradability.yaml).
product: "perp"

# The coin(s) to test, in BASEQUOTE form; write the same list again under machine_constraints.protocol.symbols below.
market_universe: ["BTCUSDT"]

# The bar size; write the same value again under machine_constraints.protocol.timeframe below.
timeframe: "1h"

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
# constraints:
#   - |
#     Build EXACTLY this strategy config (JSON)
#     <FILL IN: the strategy config as JSON>
#   - |
#     Use EXACTLY this block manifest (JSON)
#     <FILL IN: the block manifest as JSON>

# Scope for now: copy this block unchanged into every brief. Step 1a reads it as part of the brief.
scope: |
  Scope for now (2026-10-14).
  Kraken only: in scope by the operator's focus (D-130), not a capability limit; other venues' caches exist (e.g. Binance 4h files in trading-bot/local_data/) but are out of scope.
  One coin per variant: in scope. Each variant backtests one coin; an asset variant runs the same idea on a coin of another category. Not in scope: several coins inside one variant (a basket or a cross-coin ranking), because step 5a refuses a multi-coin variant (tools/variant_coin.py:725, rule G4 at :681-682) and tools/run_protocol.py backtests each coin alone (:2609, :2617).
  Price bars only, from the Kraken caches: in scope (trading-bot/local_data/kraken_<COIN>USD_<1h or 1d>.csv; the cache name carries the venue prefix, trading-bot/data/fetchers/ccxt_fetcher.py:123). Not in scope: any other feed. Funding is dropped for Kraken (tools/venue_resolver.py:134); it is kept only on the default venue, binance (tools/venue_resolver.py:57, the default path returning at :101-102); no order book, liquidation, cross-venue, on-chain or options feed exists (config/available_feeds.yaml:35-50); no open-interest fetcher exists (config/venue_data_capability.yaml:528-530 says available true and reachable_through_this_codebase false; :536-537 says no OI fetcher exists). Fear-and-greed is out of scope by the operator's decision of 2026-10-14 (wired: config/available_feeds.yaml:26), not by a capability limit.
  Perp priced on spot bars, funding not charged: in scope. A Kraken perp brief is backtested on Kraken spot prices with Kraken futures fees. Not in scope: real perp prices and funding payments, because config/venue_data_capability.yaml:472-481 declares the spot price proxy, tools/venue_resolver.py:117-137 writes price_proxy True and funding_modelled False into the protocol, and tools/run_protocol.py:2476-2480 prints it on every run.
  Hourly or daily bars: in scope (1h and 1d are the only Kraken caches on disk, 19 coins each). Not in scope: 4h, 15m or any other bar size, because no Kraken cache exists for them, a coarser bar is built from the hourly cache only through the opt-in trading.fetch_interval_seconds (docs/DATA_AVAILABILITY.md:25-38) that no brief field sets, and Kraken's live fetch returns only the 720 most recent candles (config/venue_data_capability.yaml:394-397).
  Claims expressible in the claim-test slots: in scope. Selector: all, event, regime, regime_change, calendar, quantile (tools/claim_tests.py:579-581). Outcome: fwd_return, fwd_volatility, fwd_max_drawdown, trend_ends (:631-632). Baseline: complement, placebo, other_selector (:682-683). Statistic: mean_diff, rank_ic, hit_rate, decay_curve (:748-749). Not in scope: a claim that needs a value outside these lists, because check_spec refuses it before any data is read (:881).
  The operator updates this when focus or capabilities change, recorded in DECISION_LOG.md.

machine_constraints:
  protocol:
    # The same coin(s) as market_universe above.
    symbols: ["BTCUSDT"]
    # The same bar size as timeframe above.
    timeframe: "1h"
    # Windows: start and end (end is the last included day, never the 1st of a month) cut into blocks of window_months months (1, 2, 3, 4, 6 or 12).
    # With window_months above 1, start must fall on a block boundary (January, May or September for 4; January or July for 6), else the protocol generation refuses it at launch (run_phase1_research.py:11642-11646).
    # Windows must lie inside the research period (config/campaign_data_policy.yaml, key backward_extension.BTCUSDT_1h; tools/research_folds.py:113): never the sealed holdout, and 2024-2025 only as fold D's exact blocks; the simplest is a fold (A, B, C or D) from config/folds.yaml, otherwise launch refuses the protocol before any spend (run_campaign.py:3847-3853).
    start: "2022-01-01"
    end: "2023-12-31"
    window_months: 4
    # OPTIONAL: instead of cutting start to end yourself, take a fold (A, B, C or D) from config/folds.yaml by uncommenting the next line.
    # Fold D is used only when orchestrator.folds is on (tools/research_folds.py:397-403; workflow/run_phase1_research.py:11720-11724).
    # With a fold, start and end are still read (run_phase1_research.py:11771-11772); window_months is not used (its only reader is the no-fold branch, run_phase1_research.py:11715).
    fold: A
---

# SMA trend on BTC 1h, fold A

Prose below the closing `---` is for human readers only -- the orchestrator
never reads it. Use this space for the idea's motivation, links, and any
context that does not belong in a field.

Sources copied (brief writer, 2026-10-23):
1. `strategy-research/tools/forecast_rules.py:55-60`, RULE_SENTENCE (the D-149 standardised-forecast rule). Its string pieces are joined into one line.
2. `strategy-research/workflow_artifacts/skills/strategy-config-authoring/SKILL.md:184-188`, the "standardise window:" text.
3. The same file, `SKILL.md:189-195`, the volatility-targeting (D-176) bullet. I changed "365 daily / 8760 hourly" to "365 daily / 8760".
4. `strategy-research/docs/STRATEGY_DESIGN_GUIDE.md:27`, the step 5 fill-timing sentence: "The bot trades toward the target allocation, filling at that bar's close."

## Ratification (direction, 2026-10-23; people only, the orchestrator does not read this)
PURPOSE. Tests the operator's claim, as written in research_goal, on BTC 1h over fold A, as a candidate block under the roadmap's accumulation of proven ideas. The registry holds daily blocks only; a pass registers the first 1h block. Composition is within one timeframe (tools/composition.py:10-13), so overlap with the daily block is not this run's question and residual_ic here is the candidate's own all-bars IC (tools/residual_ic.py:24-26).
Pre-registered outcomes (the review opens by naming which one happened):
A. validated (every criterion on every variant) and base passes every bar: the block registers with base's config as the first 1h block; refold next on a drawn fold (D-123).
B. validated on the criteria, base fails one or more bars: equity and exposure read first, the one change a practitioner would make named; no block.
C. refuted by a criterion: the review decides whether the brief stays open for another card (the R2 rule) or closes.
D. data gate or engineering fault: report; relaunch after the fix on the operator's word.
E. a 1b or 5a refusal: a fix, not a result; relaunch on the operator's word.
