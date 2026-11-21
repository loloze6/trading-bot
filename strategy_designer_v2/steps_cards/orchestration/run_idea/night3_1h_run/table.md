# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 018-01_hourly-breakout-gain-before-close | - | untestable | - | - | - | - | 0.05 | 0.3 |
| 018-02_hourly-breakout-multiday-continuation | - | missing-components | - | - | - | - | 0.05 | 0.4 |
| 018-03_hourly-surge-gain-before-close | - | untestable | - | - | - | - | 0.06 | 0.5 |
| 018-04_hourly-surge-multiday-continuation | - | plan | inconclusive (-0.06) | not profitable enough (failed: Calmar) | - | 7.b: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise; 7.d: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high, 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades, 018-04_hourly-surge-multiday-continuation.d3_nearness-to-monthly-high; 7.g: 018-04_hourly-surge-multiday-continuation.g1_deep-daily-fall-rebounds, 018-04_hourly-surge-multiday-continuation.g2_top-of-range-continues | 1.36 | 11.7 |
| 018-05_hourly-plunge-loss-before-close | - | plan | inconclusive (-0.45) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds; 7.d: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds, 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge; 7.g: 018-05_hourly-plunge-loss-before-close.g1_rebound-after-outsized-daily-plunge, 018-05_hourly-plunge-loss-before-close.g2_outsized-weekly-rise-continues | 1.34 | 11.9 |
| 018-06_hourly-plunge-multiday-continuation | - | plan | inconclusive (+0.04) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound; 7.d: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound, 018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound, 018-06_hourly-plunge-multiday-continuation.d3_deep-drawdown-bounce-fades; 7.g: 018-06_hourly-plunge-multiday-continuation.g1_hourly-plunge-two-day-rebound | 1.38 | 11.3 |

## Consumption
6 ideas, 4.24 USD, 36.0 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.46 | 3.4 |
| step4_backtest | 0.00 | 18.3 |
| step5_verdict | 0.40 | 1.8 |
| step6_check | 0.00 | 0.3 |
| chart_files | 0.00 | 0.3 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 1.06 | 3.7 |
| step7_7.d | 1.11 | 4.0 |
| step7_7.g | 1.21 | 4.1 |
