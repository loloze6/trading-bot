# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_monthly-low-break-cascade | - | plan | inconclusive (-1.97) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1_monthly-low-exhaustion-rebound; 7.g: 032-01.g1_monthly-low-exhaustion-rebound, 032-01.g2_monthly-low-closing-off-lows | 1.78 | 6.4 |
| 033-01_rising-market-sharp-drop-rebound | - | plan | inconclusive (+1.11) | not profitable enough (failed: Calmar) | - | 7.b: 033-01.b1_rising-market-dip-rebound-more-coins; 7.g: 033-01.g1_calm-uptrend-dip-rebound | 1.00 | 5.0 |

## Consumption
2 ideas, 2.79 USD, 11.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.91 | 1.0 |
| step4_backtest | 0.00 | 4.4 |
| step5_verdict | 0.37 | 1.5 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.56 | 1.6 |
| step7_7.g | 0.95 | 2.8 |
