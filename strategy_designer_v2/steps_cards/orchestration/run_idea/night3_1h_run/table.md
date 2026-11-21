# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 018-01_hourly-breakout-gain-before-close | - | untestable | - | - | - | - | 0.05 | 0.3 |
| 018-02_hourly-breakout-multiday-continuation | - | missing-components | - | - | - | - | 0.05 | 0.4 |
| 018-03_hourly-surge-gain-before-close | - | untestable | - | - | - | - | 0.06 | 0.5 |
| 018-04_hourly-surge-multiday-continuation | - | plan | inconclusive (-0.06) | not profitable enough (failed: Calmar) | - | 7.b: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise; 7.d: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high, 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades, 018-04_hourly-surge-multiday-continuation.d3_nearness-to-monthly-high; 7.g: 018-04_hourly-surge-multiday-continuation.g1_deep-daily-fall-rebounds, 018-04_hourly-surge-multiday-continuation.g2_top-of-range-continues | 1.36 | 11.7 |

## Consumption
4 ideas, 1.53 USD, 12.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.25 | 1.8 |
| step4_backtest | 0.00 | 6.1 |
| step5_verdict | 0.13 | 0.6 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.34 | 1.2 |
| step7_7.d | 0.36 | 1.4 |
| step7_7.g | 0.44 | 1.6 |
