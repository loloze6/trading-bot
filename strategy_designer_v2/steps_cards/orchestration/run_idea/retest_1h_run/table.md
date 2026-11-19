# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation | 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample | plan | inconclusive (+4.74) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.b1_rsi-continuation-wider-coin-set, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.b2_graded-high-rsi-continuation; 7.d: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.d1_week-averaged-rsi-strength-continuation, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.d2_slow-rsi-strength-in-uptrends; 7.g: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.g1_one-day-drop-rebound, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.g2_ten-day-return-continuation | 1.53 | 35.7 |
| 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation | 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample | plan | confirmed (+3.40) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.d1_smoothed-rsi-uptrend-continuation, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.d2_upper-rsi-uptrend-continuation; 7.g: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.g1_volatility-burst-daily-reversal, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.g2_calm-market-daily-continuation | 1.09 | 25.2 |
| 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins | 002-01_sma-golden-cross-upward-drift | plan | confirmed (+7.19) | profitable enough | unseen_2016_2017: holds; unseen_2026: does not hold | 7.g: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins.g1_five-day-momentum-inside-uptrends, 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins.g2_large-move-next-day-rebound-drift | 0.61 | 53.8 |
| 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs | 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs | plan | inconclusive (+2.18) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs.b1_near-high-momentum-more-coins, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs.b2_near-high-one-day-giveback; 7.d: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs.d1_weekly-proximity-momentum-uptrend, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs.d2_twenty-day-high-proximity-momentum; 7.g: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs.g1_one-day-fall-rebound, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs.g2_weekly-fall-reversal, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs.g3_near-high-momentum-daily-bars | 1.67 | 20.3 |

## Consumption
4 ideas, 4.90 USD, 135.0 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.95 | 2.4 |
| step4_backtest | 0.00 | 110.3 |
| step5_verdict | 0.57 | 2.9 |
| step6_check | 0.00 | 1.4 |
| chart_files | 0.00 | 0.6 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 0.66 | 2.4 |
| step7_7.d | 1.02 | 3.8 |
| step7_7.g | 1.70 | 6.4 |
| unseen_test | 0.00 | 4.8 |
