# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation | 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample | plan | inconclusive (+4.74) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.b1_rsi-continuation-wider-coin-set, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.b2_graded-high-rsi-continuation; 7.d: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.d1_week-averaged-rsi-strength-continuation, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.d2_slow-rsi-strength-in-uptrends; 7.g: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.g1_one-day-drop-rebound, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.g2_ten-day-return-continuation | 1.53 | 35.7 |
| 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation | 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample | plan | confirmed (+3.40) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.d1_smoothed-rsi-uptrend-continuation, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.d2_upper-rsi-uptrend-continuation; 7.g: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.g1_volatility-burst-daily-reversal, 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.g2_calm-market-daily-continuation | 1.09 | 25.2 |

## Consumption
2 ideas, 2.62 USD, 60.9 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.47 | 1.2 |
| step4_backtest | 0.00 | 50.0 |
| step5_verdict | 0.28 | 1.4 |
| step6_check | 0.00 | 0.9 |
| chart_files | 0.00 | 0.3 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 0.32 | 1.2 |
| step7_7.d | 0.61 | 2.4 |
| step7_7.g | 0.94 | 3.5 |
