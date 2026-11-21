# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 021-02_below-falling-cloud-continues-down | - | missing-components | - | - | - | - | 0.05 | 0.3 |
| 021-03_thin-cloud-upward-breakout | - | missing-components | - | - | - | - | 0.04 | 0.3 |
| 021-04_thin-cloud-downward-breakdown | - | missing-components | - | - | - | - | 0.10 | 0.7 |
| 021-01_above-rising-cloud-continues-up | - | plan | inconclusive (+1.30) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | - | 7.b: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins; 7.d: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues, 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades; 7.g: 021-01_above-rising-cloud-continues-up.g1_one-day-rebound-after-falls, 021-01_above-rising-cloud-continues-up.g2_week-long-continuation-after-surges | 1.73 | 6.4 |

## Consumption
4 ideas, 1.92 USD, 7.7 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.68 | 2.1 |
| step4_backtest | 0.00 | 1.2 |
| step5_verdict | 0.15 | 0.6 |
| step6_check | 0.00 | 0.0 |
| chart_files | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 0.31 | 1.0 |
| step7_7.g | 0.36 | 1.1 |
| step7_7.d | 0.43 | 1.7 |
