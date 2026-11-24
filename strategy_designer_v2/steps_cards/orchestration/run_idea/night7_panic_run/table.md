# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_monthly-low-break-cascade | - | plan | inconclusive (-1.97) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1_monthly-low-exhaustion-rebound; 7.g: 032-01.g1_monthly-low-exhaustion-rebound, 032-01.g2_monthly-low-closing-off-lows | 1.78 | 6.4 |
| 033-01_rising-market-sharp-drop-rebound | - | plan | inconclusive (+1.11) | not profitable enough (failed: Calmar) | - | 7.b: 033-01.b1_rising-market-dip-rebound-more-coins; 7.g: 033-01.g1_calm-uptrend-dip-rebound | 1.00 | 5.0 |
| 034-01_falling-market-rally-fade | - | plan | inconclusive (+0.05) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 034-01.b1_agitated-downtrend-rally-fade, 034-01.b2_next-day-agitated-rally-fade; 7.g: 0 ideas, 2 discoveries (2 explorations) | 1.21 | 5.7 |

## Consumption
3 ideas, 4.00 USD, 17.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.98 | 1.4 |
| step4_backtest | 0.00 | 6.2 |
| step5_verdict | 0.56 | 2.2 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 1.12 | 3.2 |
| step7_7.g | 1.35 | 4.0 |
