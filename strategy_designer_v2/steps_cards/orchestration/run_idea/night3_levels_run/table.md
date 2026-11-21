# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 020-02_support-retest-bounces-up | - | missing-components | - | - | - | - | 0.04 | 0.3 |
| 020-03_resistance-breakout-continues-up | - | missing-components | - | - | - | - | 0.04 | 0.3 |
| 020-04_support-breakdown-continues-down | - | missing-components | - | - | - | - | 0.04 | 0.3 |
| 020-01_resistance-retest-turns-down | - | plan | inconclusive (-0.17) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance; 7.d: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high, 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues, 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high; 7.g: 020-01_resistance-retest-turns-down.g1_strong-up-day-keeps-rising | 1.64 | 6.4 |

## Consumption
4 ideas, 1.77 USD, 7.3 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.62 | 1.7 |
| step4_backtest | 0.00 | 1.4 |
| step5_verdict | 0.15 | 0.6 |
| step6_check | 0.00 | 0.0 |
| chart_files | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.d | 0.31 | 1.1 |
| step7_7.b | 0.35 | 1.2 |
| step7_7.g | 0.34 | 1.2 |
