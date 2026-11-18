# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|
| 006-01_compression-precedes-larger-move | - | untestable | - | - | - | 0.03 | 0.2 |
| 006-02_longer-squeeze-bigger-move | - | untestable | - | - | - | 0.04 | 0.3 |
| 006-03_post-squeeze-volatility-overshoot | - | untestable | - | - | - | 0.04 | 0.2 |
| 006-04_upside-squeeze-break-continuation | - | plan | inconclusive (-1.46) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | 7.b: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation; 7.d: 006-04_upside-squeeze-break-continuation.d1_momentum-break-ten-day-continuation, 006-04_upside-squeeze-break-continuation.d2_breakout-bar-ten-day-drift; 7.g: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise, 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound | 1.21 | 5.8 |
| 006-05_downside-squeeze-break-continuation | - | missing-components | - | - | - | 0.12 | 0.9 |

## Consumption
5 ideas, 1.43 USD, 7.3 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.35 | 2.5 |
| step4_backtest | 0.00 | 1.2 |
| step5_verdict | 0.11 | 0.4 |
| step6_check | 0.00 | 0.0 |
| chart_files | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.30 | 1.0 |
| step7_7.g | 0.32 | 1.1 |
| step7_7.d | 0.34 | 1.1 |
