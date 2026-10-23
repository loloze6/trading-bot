---
# Child brief of run_098: the long side of the Donchian 250 position, BTC, fold B (draft for operator ratification).
# Built from workflow_artifacts/templates/research_brief_new_pipeline.md and the precedent briefs/rebase_run_095_standardised_host.md.
# Register only after the operator ratifies it. The queued card and the queue entry are separate drafts.
# Prose below the closing '---' is for people only; the orchestrator never reads it.

strategy_domain: "daily_breadth"
market_universe: [BTCUSDT]
timeframe: "1d"
venue: "kraken"
product: "perp"
research_goal: >
  PURPOSE. The roadmap's accumulation thesis (engineering/engineering_roadmap.html, the
  registry of validated blocks and the hypothesis-blind profit bars; D-130): the campaign
  grows by confirming or refuting claims and registering the blocks that validate, so a
  finding from one run is carried as a pre-registered test, never as belief. run_098 (the
  Donchian 250 position of the close, standardised, long and short, BTC, fold B) was refuted
  on its own bars: its forecast information coefficient was negative and its whole-test
  drawdown was 41.6 percent. Its analyst re-run found the line this run answers: the long
  side earns and the short side loses. The short lots lost (mean net return per short lot
  -0.034, entered into the bounce after a breakdown), and the strong-long entries earned
  (+0.022 gross per lot at an entry forecast of 10 or more). This run asks whether that line is a
  strategy: the same host, long-only, with the host's sizing at a common target volatility,
  on the same fold. The block rule is the one lane 1 used: a pass registers the block on
  fold B, and the refold on a fold it has not seen comes after.

  The idea, with run_098's own parent line: the daily close's position in its trailing
  250-day high-low range (a graded Donchian position) predicts BTC's next daily returns;
  taken only on the long side, standardised per D-166, and sized to 20 percent a year
  volatility, it earns more than Kraken perp costs on spot prices on fold B (six 4-month
  blocks of 2018-2021). Who pays: holders and shorts who anchor on the range's high and
  cover into breakdowns; why it may survive costs: a daily signal trades rarely.
constraints:
  - "Criteria: this brief carries none (criteria_from: hypothesis_generation); the queued card carries criteria: forecast_ic_median, and code adds residual_ic to the grid (composition mode), as for run_098. The verdict is every criterion on every variant: one FAIL refutes (verdict_criteria_evaluator.py:2214-2232); the block's config is base's (block_registry.py:225-241). Branch 3, as signed in config/profitability_bars.yaml, is read for the bars. Reading note for forecast_ic_median: after the clip at zero about half of the forecast is exactly 0 (every bar whose close is in the lower half of its 250-bar range), so the IC carries ties."
  - |
    Build EXACTLY this strategy config (JSON)
    {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"}, "strategies": {"regimes": {"unknown": {"components": [{"id": "anchor_position", "class": "strategies.strategy_components.DonchianBreakoutComponent", "params": {"period": 250, "scaling_factor": 1.0}, "weight": 1.0, "transforms": [{"op": "standardise", "params": {"window": 250, "min_periods": 62}}, {"op": "clip", "params": {"min": 0, "max": 20}}, {"op": "vol_target", "params": {"window": 60, "target_annual_vol": 0.2, "periods_per_year": 365}}, {"op": "clip", "params": {"min": 0, "max": 20}}]}]}, "trending": null, "mean_reversion": null, "chop": null}}}
  - |
    Use EXACTLY this block manifest (JSON)
    {"block": {"kind": "forecast", "config_paths": ["/strategies/regimes/unknown/components/0"]}, "scaffolding": ["/regime_detector", "/strategies/regimes/trending", "/strategies/regimes/mean_reversion", "/strategies/regimes/chop"], "rationale": "The Donchian 250 position of the close, standardised, limited to long only and vol-targeted, is the signal under test; the ungated detector and the null regimes are engine scaffolding."}
  - "In words: the position of the close in its trailing 250-bar high-low range, from -1 (at the low) to +1 (at the high); standardised (window 250, min_periods 62, target 10 and cap 20 by the op's defaults, D-148, D-149, D-166); limited to 0..20 (long or flat); then volatility targeting to 20 percent a year over 60 daily closes (365 periods a year); then limited to 0..20 again. Allocation is forecast / 10."
  - "config_rationale (statements for the record; step 1b is written by code in this run under D-110, so backtest_spec.yaml's own config_rationale field is filled by code): (1) the standardise window follows D-166: the larger of 60 and the component's longest lookback (250), at most 500, with min_periods a quarter of the window (62); (2) long-only is the tested vehicle, from run_098's analyst re-run (the re-run records PR-11 wrote: strategy-research/runs/run_098/artifacts/analyst_rerun/forecast.yaml and trade_efficiency.yaml, cited by D-171); (3) the sizing is host convention at a common target volatility, not the tested mechanism; (4) fills at the signal bar's close (D-164), with no delay clause."
  - "Readiness: this config's required_bars is 312 (250 Donchian bars plus 62 standardise min_periods); the data gates (D-169) count a window as covered only when the coin has 2 x required_bars = 624 daily bars before the window's start."
  - "Coins: the base and the design variant run on BTC; the asset variant runs on LTC. BTC (Kraken, daily cache from 2013) and LTC (first Kraken bar 2013-10-24) have the 624 bars before every fold-B window. ADA (first bar 2018-09-28) has 624 bars before only two of the six windows (2021-01 and 2021-09) and LINK (first bar 2019-09-25) before only one (2021-09), under D-169's 624 bars and D-042's 60 percent of windows; they are out because this run is BTC plus LTC."
  - "Variants (one coin each): the base on BTC; one design variant on BTC, the same config with the vol_target op removed (one transform change, D-053): the transforms list is replaced by standardise (window 250, min_periods 62), clip (min 0, max 20), clip (min 0, max 20), written as one patch that replaces the list at /strategies/regimes/unknown/components/0/transforms; one asset variant: LTCUSDT (altcoin_l1_verified_kraken category), empty patch."
  - |
    Pre-registered outcomes (written before the run; the review opens by naming which one happened):
    A. idea validated (criteria pass on base, design and LTC) and base passes every bar: the block registers with base's config; refold next.
    B. validated; base passes the scale-free bars (Sharpe > 0, deflated Sharpe >= 0.5, excess over buy-and-hold > 0, leave-one-block-out > 0, trade frequency >= 1%) and fails drawdown or the daily-return bar: the sizing target is the next lever. Both bars scale with the target; at 0.2 they need a Sharpe between 0.9 and 1.1 together, the held signed-bars question. B is the expected outcome unless the Sharpe reaches that.
    C. refuted on BTC base by the criteria: the long edge was the fold's drift; the family closes on fold B.
    C2. refuted only by LTC (criteria pass on BTC, fail on LTC): the mechanism is not cross-asset; the family closes on fold B; BTC-only is not re-run.
    C3. refuted only by the design variant (the unsized form fails a criterion that the sized base passes): the ordering came from the volatility scaling, not from the position; base's bars are read as information; no block.
    C4. refuted by residual_ic alone (forecast_ic_median passes on every variant): the long side of the range position duplicates the active lane 1 block on fold B; no block; the family closes as redundant, not as refuted on edge.
    D. base fails only the trade-frequency bar: read the pair; if the design variant alone fails it, the 250-bar standardise is the cause; if both fail it, the 0.2 band is.
    E. engineering fault, including the anomaly where only the unsized design variant passes every bar: report, no block.
  - "Claim tests and the lenses: the card's claim has two tests, information only (claim_tests.py:92): the vehicle's own forecast claim (rank IC of the long-only forecast with the 5- and 20-bar returns) and half (a) (after a forecast of 8 or more, the 5-bar return is lower than on the other bars, complement baseline, floor 50 events). No question is handed to the analyst lenses; they stay independent. Negate is refused as a vehicle: the strong-long entries earn (+0.022 gross per lot at entry >= 10). The bounce after forecast <= -10 is an observation (D-171), not tested here. The trial-ledger row is written as for every run."
  - "Out of scope, not even sized: funding carry, cross-sectional momentum (cross-coin ranking), cost engineering. A variant is one coin; a multi-coin variant is refused."
  - "No lookahead: a bar's decision uses data timestamped at or before that bar's close. The position, the standardise mean (past values only, registry.py:96-115) and the vol_target window (closes up to the current bar, registry.py:37-52) all end at the signal bar's close."
available_data:
  - "Kraken daily OHLCV caches trading-bot/local_data/kraken_BTCUSD_1d.csv and kraken_LTCUSD_1d.csv. The data-availability gate grades each window."
  - "Costs: Kraken perp fees and slippage from config/cost_model.yaml, applied to spot prices (venue kraken, product perp)."

criteria_from: hypothesis_generation

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
    symbols: ["BTCUSDT"]
    timeframe: "1d"
    fold: "B"
    start: "2018-05-01"
    end: "2021-12-31"
    window_months: 4
---

# Child of run_098: long-only Donchian 250 position, vol-targeted, BTC, fold B

Prose below the closing `---` is for human readers only; the orchestrator never reads it.

Parent: run_098 (daily breadth, fold B, refuted). This brief tests the line its analyst
re-run found (the long side earns, the short side loses) as a strategy on the same fold,
with the block rule of lane 1: a pass registers the block on fold B and the refold comes
after. Fold B is the fold run_098 ran on, kept on purpose by the operator's direction of
2026-10-21; a pass here is therefore not independent evidence, and the refold carries that
weight.
