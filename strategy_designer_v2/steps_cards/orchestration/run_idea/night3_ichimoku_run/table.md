# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 021-03_thin-cloud-upward-breakout | - | missing-components | - | - | - | - | 0.04 | 0.3 |
| 021-04_thin-cloud-downward-breakdown | - | missing-components | - | - | - | - | 0.10 | 0.7 |
| 021-01_above-rising-cloud-continues-up | - | plan | inconclusive (+1.30) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | - | 7.b: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins; 7.d: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues, 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades; 7.g: 021-01_above-rising-cloud-continues-up.g1_one-day-rebound-after-falls, 021-01_above-rising-cloud-continues-up.g2_week-long-continuation-after-surges | 1.73 | 6.4 |
| 021-02_below-falling-cloud-continues-down | - | plan | inconclusive (+0.69) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues; 7.d: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud, 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud, 021-02_below-falling-cloud-continues-down.d3_fast-cloud-fall-rebounds; 7.g: 021-02_below-falling-cloud-continues-down.g1_range-position-predicts-week, 021-02_below-falling-cloud-continues-down.g2_sharp-daily-drops-rebound, 021-02_below-falling-cloud-continues-down.g3_monthly-momentum-continues | 1.60 | 6.9 |

## Consumption
4 ideas, 3.47 USD, 14.3 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.75 | 2.5 |
| step4_backtest | 0.00 | 2.5 |
| step5_verdict | 0.29 | 1.2 |
| step6_check | 0.00 | 0.0 |
| chart_files | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 0.78 | 2.4 |
| step7_7.g | 0.75 | 2.5 |
| step7_7.d | 0.90 | 3.1 |
