# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 029-02_breakout-volume-trapped-decline | - | missing-components | - | - | - | - | 0.07 | 0.5 |
| 029-03_close-below-breakout-bar-low | - | missing-components | - | - | - | - | 0.05 | 0.3 |
| 029-04_breakout-extension-failure-decline | - | missing-components | - | - | - | - | 0.14 | 0.9 |
| 029-05_failed-breakout-multiday-drift | - | missing-components | - | - | - | - | 0.09 | 0.6 |
| 029-01_failed-breakout-depth-decline | - | plan | inconclusive (-0.29) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline; 7.d: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls, 029-01_failed-breakout-depth-decline.d2_quiet-market-failed-breakout-falls, 029-01_failed-breakout-depth-decline.d3_marginal-breakout-failure-falls; 7.g: 029-01_failed-breakout-depth-decline.g1_breakout-size-continues-higher | 6.09 | 20.3 |

## Consumption
5 ideas, 6.44 USD, 22.7 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.68 | 3.4 |
| step4_backtest | 0.00 | 1.3 |
| step5_verdict | 0.18 | 0.7 |
| step6_check | 0.00 | 0.0 |
| chart_files | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 0.35 | 1.1 |
| step7_7.g | 0.53 | 1.6 |
| step7_7.d | 3.71 | 14.6 |
