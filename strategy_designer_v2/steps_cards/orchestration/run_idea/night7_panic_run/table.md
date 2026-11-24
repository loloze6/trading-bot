# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_monthly-low-break-cascade | - | plan | inconclusive (-1.97) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1_monthly-low-exhaustion-rebound; 7.g: 032-01.g1_monthly-low-exhaustion-rebound, 032-01.g2_monthly-low-closing-off-lows | 1.78 | 6.4 |

## Consumption
1 ideas, 1.78 USD, 6.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.83 | 0.6 |
| step4_backtest | 0.00 | 2.7 |
| step5_verdict | 0.21 | 0.9 |
| step6_check | 0.00 | 0.0 |
| chart_files | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.35 | 0.9 |
| step7_7.g | 0.39 | 1.2 |
