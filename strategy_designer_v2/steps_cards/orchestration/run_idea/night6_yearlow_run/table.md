# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 031-01_near-yearly-low-keeps-falling | - | plan | inconclusive (+1.70) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 031-01.b1_near-yearly-low-falls-all-coins; 7.g: 031-01.g1_weekly-gains-carry-into-saturday | 1.08 | 6.0 |
| 031-02_near-yearly-low-bounces | - | plan | inconclusive (-1.70) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 031-02.b1_failed-rally-near-yearly-low; 7.g: 031-02.g1_weekend-continues-the-week-s-move | 1.12 | 6.1 |

## Consumption
2 ideas, 2.19 USD, 12.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.15 | 0.8 |
| step4_backtest | 0.00 | 5.0 |
| step5_verdict | 0.30 | 1.0 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 0.68 | 2.2 |
| step7_7.g | 1.06 | 2.9 |
