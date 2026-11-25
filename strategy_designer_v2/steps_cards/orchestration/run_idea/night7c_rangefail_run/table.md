# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_flat-range-upside-break-fades | - | plan | inconclusive (-1.97) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1_flat-range-upside-breaks-continue; 7.g: 032-01.g1_next-day-rebound-after-falls | 2.04 | 5.8 |
| 032-02_flat-range-downside-break-recovers | - | plan | inconclusive (-0.55) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 032-02.b1_flat-range-upside-break-continues; 7.g: 032-02.g1_top-of-range-close-continues | 1.24 | 5.8 |

## Consumption
2 ideas, 3.28 USD, 11.6 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.96 | 1.6 |
| step4_backtest | 0.00 | 3.2 |
| step5_verdict | 0.39 | 1.5 |
| step6_check | 0.00 | 0.0 |
| chart_files | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.g | 0.99 | 2.7 |
| step7_7.b | 0.94 | 2.5 |
