# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 054-01_deep-reclaimed-low-pierce-rebound | - | plan | inconclusive (+0.92) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 054-01.b1_reclaimed-low-all-coins; 7.g: 054-01.g1_rising-market-reclaimed-low-fades | 2.78 | 6.7 |
| 054-02_strong-close-reclaim-rebound | - | plan | inconclusive (+0.62) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 054-02.b1_reclaim-rebound-all-coins, 054-02.b2_low-close-reclaim-rebound; 7.g: 054-02.g1_choppy-reclaimed-low-falls | 1.34 | 8.1 |
| 054-03_deep-pierce-reclaim-continuation | - | plan | inconclusive (-0.91) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 054-03.b1_rising-market-reclaimed-low-continuation, 054-03.b2_choppy-market-reclaimed-low-continuation; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.24 | 7.1 |
| 054-04_weak-reclaim-low-continuation | - | plan | inconclusive (-1.20) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 054-04.b1_reclaimed-low-after-rise; 7.g: 054-04.g1_strong-reclaim-monthly-low-fails | 1.24 | 7.4 |
| 054-01.b1_reclaimed-low-all-coins | 054-01_deep-reclaimed-low-pierce-rebound | plan | inconclusive (+1.29) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 054-01.b1.b1_weak-close-reclaim-rebounds, 054-01.b1.b2_reclaimed-low-fails-rising; 7.g: 0 ideas, 1 discoveries (3 explorations) | 1.39 | 12.2 |
| 054-02.b1_reclaim-rebound-all-coins | 054-02_strong-close-reclaim-rebound | plan | inconclusive (+0.81) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 054-02.b1.b1_reclaim-rebound-after-deep-fall; 7.g: 054-02.b1.g1_strong-reclaim-fails-falling | 1.43 | 13.2 |
| 054-03.b1_rising-market-reclaimed-low-continuation | 054-03_deep-pierce-reclaim-continuation | plan | inconclusive (+1.11) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 054-03.b1.b1_reclaimed-low-uptrend-continuation; 7.g: no ideas: The only patterns that stand out are already held in the profile map: the late-week gain (045-01) and the continuation near the 30-day high (034-01.b1, 033-03.b2). The brief's reclaimed-low situation is not graded and rests on one window, so no new idea is supported. | 1.06 | 6.1 |

## Consumption
7 ideas, 10.48 USD, 60.9 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 2.85 | 8.4 |
| step4_backtest | 0.00 | 27.6 |
| step5_verdict | 1.49 | 6.0 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 2.64 | 8.2 |
| step7_7.g | 3.50 | 10.4 |
