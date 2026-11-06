# Night of 2026-11-06: what ran, what passed, what it cost

Generated 2026-11-06 06:14 UTC by `night_2026-11-06/make_readme.py` from the records. Numbers only. The operator delegated the night: briefs by the delegate, runs by the pipeline, no holdout spent, no git until morning.

## Totals

| runs | claims judged | judge passes | engine runs | engine passes | model cost USD |
|---|---|---|---|---|---|
| 55 | 548 | 23 (4.2%) | 29 | 9 | 20.65 |

The judge's pass rate sits near the 5% noise floor of its own rule (the claim's number on the fold, same sign in 5 of 6 windows). A judge pass is an event mean on one fold; the engine's bar is the book: net positive in 5 of 6 windows, median window Sharpe at least 1.0, worst window drawdown at most 20%, at full size or at a fixed 20% volatility target.

## Every run

| run | fold | claims | judge passes | engine (per symbol) | cost USD |
|---|---|---|---|---|---|
| _replications/breakout_spike_continues_inside_spike_reverts | ? | 1 | 0 | spike_continues_inside_spike_reverts_LTCUSD: fail (full, net -28%, Sharpe -0.42, dd 0.3174); spike_continues_inside_spike_reverts_ETHUSD: fail (full, net +13%, Sharpe 0.19, dd 0.2987) | 0.00 |
| _replications/donchian_72h_breakout | ? | 1 | 0 | - | 0.00 |
| _replications/friday_long_net_profit | ? | 1 | friday_long_net_profit | long_net_profit_XMRUSD: fail (full, net +66%, Sharpe 0.42, dd 0.1408); long_net_profit_XRPUSD: refused; long_net_profit_ADAUSD: refused | 0.00 |
| _replications/gated_cross_pays_net | ? | 1 | 0 | - | 0.00 |
| _replications/low_vol_regime_momentum | ? | 1 | 0 | vol_regime_momentum_ETHUSD: refused; vol_regime_momentum_LTCUSD: refused | 0.00 |
| _replications/volume_burst_stretch_pullback_bar_continues | ? | 1 | 0 | burst_stretch_pullback_bar_continues_ETHUSD: pass (vol_target, net +29%, Sharpe 1.21, dd 0.0629) | 0.00 |
| _replications/volume_burst_stretch_pullback_bar_continues_2 | ? | 1 | 0 | burst_stretch_pullback_bar_continues_BTCUSD: pass (vol_target, net +37%, Sharpe 1.78, dd 0.073) | 0.00 |
| fake_01_btc_overreaction/001 | A | 11 | breakout_spike_continues_inside_spike_reverts | breakout_spike_continues_inside_spike_reverts_BTCUSD: pass (full_size, net +56%, Sharpe 1.03, dd 0.1544) | 0.34 |
| fake_02_eth_vol_regime_trend/001 | A | 10 | 0 | - | 0.29 |
| fake_03_time_of_week/001 | A | 10 | volume_surprise_vs_clock | - | 0.40 |
| n01_session_vol_regime_book_1h/001 | B | 10 | 0 | - | 0.45 |
| n02_alt_daily_trend_other_categories_1d/001 | C | 12 | long_horizon_exhaustion | - | 0.43 |
| n03_eth_hourly_stretch_reversion_1h/001 | B | 12 | asia_hours_stretch_fade, weekend_stretch_continuation | asia_hours_stretch_fade_ETHUSD: fail (full, net +27%, Sharpe 0.33, dd 0.251); weekend_stretch_continuation_ETHUSD: fail (full, net +24%, Sharpe 0.51, dd 0.0986) | 0.61 |
| n04_btc_daily_vol_timing_1d/001 | C | 12 | low_vol_regime_momentum | low_vol_regime_momentum_BTCUSD: pass (vol_target, net +102%, Sharpe 2.1, dd 0.1054) | 0.43 |
| n05_retail_coins_hourly_flow_1h/001 | A | 12 | 0 | - | 0.44 |
| n06_range_break_continuation_other_coins_1h/001 | B | 10 | 0 | - | 0.28 |
| n06_range_break_continuation_other_coins_1h/002 | A | 14 | trend_aligned_24h_break | trend_aligned_24h_break_SOLUSD: fail (full, net +46%, Sharpe -0.19, dd 0.4517); trend_aligned_24h_break_LINKUSD: fail (full, net -15%, Sharpe 0.08, dd 0.4231) | 0.49 |
| n07_calendar_daily_three_coins_1d/001 | B | 11 | friday_long_net_profit | friday_long_net_profit_LTCUSD: fail (full, net +131%, Sharpe 1.11, dd 0.1611); friday_long_net_profit_ETHUSD: pass (full, net +116%, Sharpe 1.81, dd 0.156); friday_long_net_profit_BTCUSD: fail (full, net +33%, Sharpe 0.69, dd 0.0845) | 0.52 |
| n08_opening_range_breakout_eth_1h/001 | C | 13 | or_close_location_drift, break_aligned_with_prior_day, or_location_with_prior_day | or_location_with_prior_day_ETHUSD: fail (full, net +97%, Sharpe 0.78, dd 0.4988); break_aligned_with_prior_day_ETHUSD: fail (full, net -43%, Sharpe -0.28, dd 0.5383) | 0.58 |
| n09_long_horizon_reversal_book_1d/001 | A | 9 | 0 | - | 0.37 |
| n10_hourly_trend_with_vol_gate_1h/001 | C | 13 | donchian_72h_breakout | donchian_72h_breakout_ETHUSD: pass (vol_target, net +66%, Sharpe 1.58, dd 0.0898); donchian_72h_breakout_BTCUSD: pass (vol_target, net +32%, Sharpe 1.16, dd 0.1592) | 0.51 |
| n11_daily_gate_hourly_entry_1h/001 | A | 12 | 0 | - | 0.62 |
| n12_short_horizon_daily_reversion_1d/001 | B | 10 | 0 | - | 0.32 |
| n12_short_horizon_daily_reversion_1d/002 | A | 10 | 0 | - | 0.46 |
| n13_quiet_period_then_move_btc_1h/001 | C | 14 | long_quiet_stays_quiet | - | 0.47 |
| n14_dollar_volume_regime_memecoins_1d/001 | A | 10 | 0 | - | 0.26 |
| n15_eth_hourly_momentum_horizons_1h/001 | A | 12 | mom_24h_short_reversal | - | 0.34 |
| n16_day_of_week_other_coins_1d/001 | A | 10 | weekend_low_volatility | - | 0.26 |
| n17_vol_channel_breakout_daily_1d/001 | B | 13 | 0 | - | 0.49 |
| n18_payment_coins_hourly_shock_1h/001 | A | 11 | volume_backed_shock_more_volatile_after | - | 0.40 |
| n19_altcoin_daily_momentum_1d/001 | A | 11 | 0 | - | 0.25 |
| n20_compression_breakout_alts_daily_1d/001 | A | 11 | 0 | - | 0.35 |
| n21_candle_patterns_daily_1d/001 | C | 9 | 0 | - | 0.47 |
| n22_friday_effect_hourly_resolution_1h/001 | B | 14 | 0 | - | 0.46 |
| n23_weekday_gated_trend_hourly_1h/001 | C | 12 | gated_cross_pays_net | gated_cross_pays_net_ETHUSD: fail (full, net +54%, Sharpe 0.55, dd 0.3769); gated_cross_pays_net_BTCUSD: pass (vol_target, net +8%, Sharpe 1.31, dd 0.1433) | 0.60 |
| n24_hourly_donchian_other_coins_1h/001 | A | 12 | 0 | - | 0.45 |
| n25_low_vol_momentum_other_coins_1d/001 | A | 11 | 0 | - | 0.43 |
| n26_session_reversal_hourly_1h/001 | C | 10 | 0 | - | 0.43 |
| n27_drawdown_state_daily_1d/001 | B | 11 | 0 | - | 0.40 |
| n28_hourly_stretch_reversion_older_coins_1h/001 | C | 13 | volume_burst_stretch_pullback_bar_continues | volume_burst_stretch_pullback_bar_continues_XRPUSD: pass (vol_target, net +32%, Sharpe 1.8, dd 0.0558); volume_burst_stretch_pullback_bar_continues_LTCUSD: fail (full, net +79%, Sharpe 1.26, dd 0.2722) | 0.45 |
| n29_hourly_autocorrelation_regimes_1h/001 | B | 11 | lag24_same_hour_echo | - | 0.40 |
| n30_round_numbers_hourly_1h/001 | B | 13 | 0 | - | 0.67 |
| n31_weekly_reversal_daily_1d/001 | A | 12 | 0 | - | 0.44 |
| n32_vol_term_structure_hourly_1h/001 | A | 11 | expansion_persists_in_size | - | 0.32 |
| n33_volume_price_divergence_daily_1d/001 | A | 9 | 0 | - | 0.28 |
| n34_hour_of_day_drift_hourly_1h/001 | C | 10 | europe_open_distribution_weekday_07_10 | europe_open_distribution_weekday_07_10_ETHUSD: fail (full, net +0%, Sharpe 0.49, dd 0.2901); europe_open_distribution_weekday_07_10_BTCUSD: fail (full, net -14%, Sharpe -0.02, dd 0.2438); europe_open_distribution_weekday_07_10_LTCUSD: fail (full, net -48%, Sharpe -0.56, dd 0.3089) | 0.56 |
| n35_privacy_coins_hourly_shock_1h/001 | A | 12 | 0 | - | 0.40 |
| n36_ltc_xmr_hourly_weekday_1h/001 | A | 11 | weekend_quiet_regime | - | 0.37 |
| n37_zec_ltc_hourly_trend_1h/001 | A | 11 | 0 | - | 0.37 |
| n38_daily_range_cycles_1d/001 | C | 11 | 0 | - | 0.38 |
| n39_daily_typical_price_anchor_1d/001 | B | 12 | 0 | - | 0.48 |
| n40_multi_day_volume_climax_1d/001 | C | 11 | 0 | - | 0.43 |
| real_01_daily_breadth_fold_a/001 | A | 12 | 0 | - | 0.46 |
| real_01b_daily_breadth_ltc/001 | B | 10 | 0 | - | 0.47 |
| real_01b_daily_breadth_ltc/002 | C | 10 | 0 | - | 0.57 |

## Engine passes (a book that passed the profit bar on its fold, at either size)

- volume_burst_stretch_pullback_bar_continues on ETHUSD (1h, fold C), _replications/volume_burst_stretch_pullback_bar_continues, passed as vol_target: net +28.8%, median window Sharpe 1.21, worst window drawdown 6.3%, trades 199
- volume_burst_stretch_pullback_bar_continues on BTCUSD (1h, fold C), _replications/volume_burst_stretch_pullback_bar_continues_2, passed as vol_target: net +36.7%, median window Sharpe 1.78, worst window drawdown 7.3%, trades 205
- breakout_spike_continues_inside_spike_reverts on BTCUSD (1h, fold A), fake_01_btc_overreaction/001, passed as full_size: net +55.6%, median window Sharpe 1.03, worst window drawdown 15.4%, trades 193
- low_vol_regime_momentum on BTCUSD (1d, fold C), n04_btc_daily_vol_timing_1d/001, passed as vol_target: net +102.2%, median window Sharpe 2.1, worst window drawdown 10.5%, trades 43
- friday_long_net_profit on ETHUSD (1d, fold B), n07_calendar_daily_three_coins_1d/001, passed as full size: net +116.4%, median window Sharpe 1.81, worst window drawdown 15.6%, trades 106
- donchian_72h_breakout on ETHUSD (1h, fold C), n10_hourly_trend_with_vol_gate_1h/001, passed as vol_target: net +66.1%, median window Sharpe 1.58, worst window drawdown 9.0%, trades 213
- donchian_72h_breakout on BTCUSD (1h, fold C), n10_hourly_trend_with_vol_gate_1h/001, passed as vol_target: net +32.0%, median window Sharpe 1.16, worst window drawdown 15.9%, trades 241
- gated_cross_pays_net on BTCUSD (1h, fold C), n23_weekday_gated_trend_hourly_1h/001, passed as vol_target: net +8.4%, median window Sharpe 1.31, worst window drawdown 14.3%, trades 120
- volume_burst_stretch_pullback_bar_continues on XRPUSD (1h, fold C), n28_hourly_stretch_reversion_older_coins_1h/001, passed as vol_target: net +32.2%, median window Sharpe 1.8, worst window drawdown 5.6%, trades 177

## Replications (same claim code, other coins, same fold, no model call)

| claim | fold | symbol | judge | engine |
|---|---|---|---|---|
| breakout_spike_continues_inside_spike_reverts | A | ETHUSD | pass (effect +0.0064, 5 of 6) | fail |
| breakout_spike_continues_inside_spike_reverts | A | LTCUSD | pass (effect +0.0072, 5 of 6) | fail |
| breakout_spike_continues_inside_spike_reverts | A | XRPUSD | fail (effect +0.0003, 4 of 6) | - |
| breakout_spike_continues_inside_spike_reverts | A | ADAUSD | fail (effect +0.0049, 4 of 6) | - |
| donchian_72h_breakout | C | LTCUSD | fail (effect +0.0029, 4 of 6) | - |
| donchian_72h_breakout | C | XRPUSD | fail (effect +0.0094, 4 of 6) | - |
| friday_long_net_profit | B | XRPUSD | pass (effect +0.0111, 5 of 6) | refused: engine refused: AssertionError: warmup_prefetch: strategy not ready after 347 pr |
| friday_long_net_profit | B | ADAUSD | pass (effect +0.0187, 5 of 6) | refused: engine refused: RuntimeError: No historical data for ADAUSD over <date>..<date>  |
| friday_long_net_profit | B | XMRUSD | pass (effect +0.0076, 5 of 6) | fail |
| gated_cross_pays_net | C | LTCUSD | fail (effect +0.0137, 4 of 6) | - |
| gated_cross_pays_net | C | XRPUSD | fail (effect -0.0040, 4 of 6) | - |
| low_vol_regime_momentum | C | ETHUSD | pass (effect +0.0412, 5 of 6) | refused: engine refused: AssertionError: warmup_prefetch: strategy not ready after 873 pr |
| low_vol_regime_momentum | C | LTCUSD | pass (effect +0.0196, 5 of 6) | refused: engine refused: AssertionError: warmup_prefetch: strategy not ready after 898 pr |
| low_vol_regime_momentum | C | XRPUSD | fail (effect +0.0070, 3 of 6) | - |
| volume_burst_stretch_pullback_bar_continues | C | ETHUSD | pass (effect +0.0057, 5 of 6) | pass (vol_target, Sharpe 1.21) |
| volume_burst_stretch_pullback_bar_continues | C | ADAUSD | fail (effect +0.0062, 4 of 6) | - |
| volume_burst_stretch_pullback_bar_continues | C | BTCUSD | pass (effect +0.0053, 5 of 6) | pass (vol_target, Sharpe 1.78) |
| volume_burst_stretch_pullback_bar_continues | C | LINKUSD | fail (effect +0.0098, 3 of 6) | - |

## Lite book check on every judge-passed return claim (information; close-to-close, full size, 0.15% cost)

56 judge-passed books checked, 8 pass the same bar in the lite check: breakout_spike_continues_inside_spike_reverts on BTCUSD (Sharpe 1.04), month_start_inflow on ADAUSD (Sharpe 1.25), friday_long_net_profit on ETHUSD (Sharpe 1.81), friday_long_net_profit on LTCUSD (Sharpe 1.73), friday_long_after_down_week on ETHUSD (Sharpe 1.72), trend_gate_breakout_long on ETHUSD (Sharpe 1.82), near_high_gate_breakout_long on ETHUSD (Sharpe 1.64), friday_post_us_close_net_profit on LTCUSD (Sharpe 1.08)

## Looks per brief (claims tried; at a 5% noise rate expect one false pass per twenty)

fake_01_btc_overreaction: 21, fake_02_eth_vol_regime_trend: 19, fake_03_time_of_week: 22, real_01_daily_breadth_fold_a: 12, n01_session_vol_regime_book_1h: 10, n02_alt_daily_trend_other_categories_1d: 12, n04_btc_daily_vol_timing_1d: 12, n03_eth_hourly_stretch_reversion_1h: 12, n05_retail_coins_hourly_flow_1h: 12, n06_range_break_continuation_other_coins_1h: 14, n07_calendar_daily_three_coins_1d: 11, n08_opening_range_breakout_eth_1h: 13, n09_long_horizon_reversal_book_1d: 9, n10_hourly_trend_with_vol_gate_1h: 13, n11_daily_gate_hourly_entry_1h: 12, n12_short_horizon_daily_reversion_1d: 20, n13_quiet_period_then_move_btc_1h: 14, n15_eth_hourly_momentum_horizons_1h: 12, n14_dollar_volume_regime_memecoins_1d: 10, n16_day_of_week_other_coins_1d: 10, n17_vol_channel_breakout_daily_1d: 13, n18_payment_coins_hourly_shock_1h: 11, n19_altcoin_daily_momentum_1d: 11, n20_compression_breakout_alts_daily_1d: 11, n21_candle_patterns_daily_1d: 9, n22_friday_effect_hourly_resolution_1h: 14, n23_weekday_gated_trend_hourly_1h: 12, n24_hourly_donchian_other_coins_1h: 12, n25_low_vol_momentum_other_coins_1d: 11, n26_session_reversal_hourly_1h: 10, n27_drawdown_state_daily_1d: 11, n28_hourly_stretch_reversion_older_coins_1h: 13, n29_hourly_autocorrelation_regimes_1h: 11, real_01b_daily_breadth_ltc: 32, n30_round_numbers_hourly_1h: 13, n31_weekly_reversal_daily_1d: 12, n32_vol_term_structure_hourly_1h: 11, n34_hour_of_day_drift_hourly_1h: 10, n33_volume_price_divergence_daily_1d: 9, n35_privacy_coins_hourly_shock_1h: 12, n36_ltc_xmr_hourly_weekday_1h: 11, n37_zec_ltc_hourly_trend_1h: 11, n38_daily_range_cycles_1d: 11, n39_daily_typical_price_anchor_1d: 12, n40_multi_day_volume_climax_1d: 11

## Defects the runs revealed and the fixes (from STEPBACK.md, in order)

- Batch 7 is generalisation: each mechanism that passed the engine on one coin and fold is asked again on other coins, with its "already tried" line taken from the record. That is the campaign-review question ("is it the coin or the mechanism?"), delegated for the night. No holdout, no second fold for the same coin.
- The operator's own brief is run on the two folds it has not seen; it is the campaign's core job, and a run on another fold is a new run with new ideas, not a confirmation of a claim. One fresh brief.
- One prompt fix asked by three runs (a flat next claim refused by the judge): the analyst prompt now shows the nested skeleton. No reading of results.
- Batch 7 asked a question the pipeline could not yet answer exactly: is a passing mechanism the coin's or the mechanism's? New ideas on other coins are not a replication. `steps/replicate.py` runs the same claim code on other symbols, same fold, no model call, judge then engine. Queued for the five engine-passing claims.
- The operator's brief could not run on folds B and C with ADA (no history). LTC, named clean in the brief, takes its place in a variant brief; the twelve tried claims are carried over so none is repeated. The choice of coin is the delegate's and is written down.
- The replications answered the batch-7 question with code, not ideas: none of the five engine-passing books passes the engine on another coin; two hold at the judge level on ETH and LTC. Recorded, not read further. One defect fixed (a claim from an analyst round lives in claims_rN.yaml).
- The operator's brief answered no on all three research folds (BTC with ADA on A, with LTC on B and C). Ten judge passes failed the engine tonight; the lite book check, which matched the engine on the BTC candidate, is run on every judge-passed book as information, so the morning file can show which passes carry a book and the pipeline can later skip the engine where the lite check already says no.
- The Friday claim replicated at the judge level on XRP, ADA and XMR (now six coins at the judge, one at the engine); the engine could not run it on XRP and ADA for fold B history and failed on XMR. Recorded. One hygiene fix: engine refusal messages carried window dates into tracked files; scrubbed and prevented, night logs ignored by git.
- Consistency of the record: three books passed the engine before the two-size policy existed; the policy is applied to them now, code only, same claims, same folds. One more replication of the claim that passed the engine on two coins.
- Batch 13 applied the two-size policy to the early engine passes and replicated the volume-burst claim on BTC (engine pass at the volatility target; it now holds on XRP, ETH, BTC and fails on LTC). Recorded, not read further. Batch 14 is five briefs on domains the record has not touched.
- Batch 14: n31 none, n32 one volatility filter on both coins, n33 refused by the coverage check (my fold choice for the privacy coins, again fold B; re-queued on fold A), n34 running. No defect in the pipeline this round; one in my brief routing, which the check caught for free.
- n34 gave a judge pass on three coins with a tiny effect and an engine fail on both coins tested: the two judges disagree again, recorded. Batch 16 is the last of the night: three briefs on the coins the record has barely touched at hourly resolution, on fold A where they have history.
- Fifty-two runs, 514 claims, 23 judge passes, 9 engine passes, 19.36 USD, nine defects fixed in the pipeline, each named with its run. The morning file is generated from the records. Nothing was read as a trader; no next brief was proposed to the operator.
- The last three briefs found nothing. Fifty-five runs, 548 claims, 23 judge passes, 9 engine passes, 20.65 USD. The morning file and the analysis are regenerated. From here the loop only checks in; it launches no run unless a check-in finds a reason.

## Open asks (recorded, not built)

- Daily claims with year-long windows cannot reach the engine on folds whose first window starts near the start of a coin's cache (the engine's warm-up wants twice the claim's history): refused, not scored.
- A validated filter waits for a book; the shelf holds filters that no book has used.
- A significance floor for the judge is the operator's ruling; the t-statistic is recorded next to each effect since 01:35.
- The holdout path is not built; nothing touched the sealed store.

## Files

`records/query.py` (this table), `records/shelf.yaml`, `records/claims_tried.yaml`, `records/trials.yaml`, `records/lite_books.yaml`, `runs/<brief>/<n>/` (claims, verdicts, analyses, engine folders), `runs/_replications/`, `STEPBACK.md`, `CHANGES.md`.
