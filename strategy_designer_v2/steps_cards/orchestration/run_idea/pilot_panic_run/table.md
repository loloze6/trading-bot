# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 054-01_deep-reclaimed-low-pierce-rebound | - | plan | inconclusive (+0.92) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 054-01.b1_reclaimed-low-all-coins; 7.g: 054-01.g1_rising-market-reclaimed-low-fades | 2.78 | 6.7 |
| 054-02_strong-close-reclaim-rebound | - | plan | inconclusive (+0.62) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 054-02.b1_reclaim-rebound-all-coins, 054-02.b2_low-close-reclaim-rebound; 7.g: 054-02.g1_choppy-reclaimed-low-falls | 1.34 | 8.1 |
| 054-03_deep-pierce-reclaim-continuation | - | plan | inconclusive (-0.91) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 054-03.b1_rising-market-reclaimed-low-continuation, 054-03.b2_choppy-market-reclaimed-low-continuation; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.24 | 7.1 |
| 054-04_weak-reclaim-low-continuation | - | plan | inconclusive (-1.20) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 054-04.b1_reclaimed-low-after-rise; 7.g: 054-04.g1_strong-reclaim-monthly-low-fails | 1.24 | 7.4 |

## Consumption
4 ideas, 6.60 USD, 29.3 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 2.52 | 6.3 |
| step4_backtest | 0.00 | 9.8 |
| step5_verdict | 0.83 | 3.3 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 1.46 | 4.3 |
| step7_7.g | 1.79 | 5.5 |
