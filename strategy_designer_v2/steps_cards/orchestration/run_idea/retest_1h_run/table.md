# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation | 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample | plan | inconclusive (+4.74) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.b1_rsi-continuation-wider-coin-set, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.b2_graded-high-rsi-continuation; 7.d: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.d1_week-averaged-rsi-strength-continuation, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.d2_slow-rsi-strength-in-uptrends; 7.g: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.g1_one-day-drop-rebound, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.g2_ten-day-return-continuation | 1.53 | 35.7 |
| 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation | 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample | plan | confirmed (+3.40) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.d1_smoothed-rsi-uptrend-continuation, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.d2_upper-rsi-uptrend-continuation; 7.g: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.g1_volatility-burst-daily-reversal, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.g2_calm-market-daily-continuation | 1.09 | 25.2 |
| 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins | 002-01_sma-golden-cross-upward-drift | plan | confirmed (+7.19) | profitable enough | unseen_2016_2017: holds; unseen_2026: does not hold | 7.g: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins.g1_five-day-momentum-inside-uptrends, 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins.g2_large-move-next-day-rebound-drift | 0.61 | 53.8 |

## Consumption
3 ideas, 3.23 USD, 114.6 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.54 | 1.7 |
| step4_backtest | 0.00 | 95.7 |
| step5_verdict | 0.43 | 2.1 |
| step6_check | 0.00 | 1.1 |
| chart_files | 0.00 | 0.5 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 0.32 | 1.2 |
| step7_7.d | 0.61 | 2.4 |
| step7_7.g | 1.34 | 5.1 |
| unseen_test | 0.00 | 4.8 |
