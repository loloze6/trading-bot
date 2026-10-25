---
strategy_domain: risk timing from price-only volatility and drawdown forecasts
market_universe:
- BTCUSDT
timeframe: 1d
venue: kraken
product: perp
available_data: Kraken daily caches kraken_BTCUSD_1d.csv, 2013-10-06 to 2025-12-31,
  price bars only, funding not modelled
research_goal: Does a price-only forecast built from BTCUSDT daily bars predict forward
  realised volatility and forward maximum drawdown over the next 1 to 20 days better
  than the unconditional baseline? Use the full Kraken daily history from 2013, because
  the daily_signal_power_floor KB finding requires 2018 or later data for daily-frequency
  tests. Test only fwd_volatility and fwd_max_drawdown outcomes with claim-test slots
  already in the brief scope, with no trade-level or basket claims. The aim is to
  find an exposure-scaling input that can be reduced ahead of drawdowns, not a next-bar
  directional entry.
criteria_from: hypothesis_generation
machine_constraints:
  protocol:
    symbols:
    - BTCUSDT
    timeframe: 1h
    start: '2022-01-01'
    end: '2023-12-31'
    window_months: 4
    fold: A
---

# Reframe from campaign review (run_100)

Written by the orchestrator from runs/run_100/artifacts/campaign_review.yaml (recommendation: reframe; E-059 slice 6c S2b). Registered as a `ready` queue entry with origin campaign_review; decide-next picks the next run. Its criteria are written at step 1a from config/criterion_menu.yaml (criteria_from); its protocol pin is run_100's.
