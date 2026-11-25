# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 058-01_rising-calm-dip-rebound | - | plan | inconclusive (+0.33) | not profitable enough (failed: Calmar) | - | 7.b: no ideas: The theme's effect is not in the data. In rising calm markets deeper few-day dips are followed by smaller moves, not larger recoveries (F1, F2), at every horizon from 1 to 10 days (F3). The opposite sign also shifts from year to year (F4), and no other profile shows a clear graded rebound that would justify narrowing the idea (F5, F6).; 7.g: 0 ideas, 2 discoveries (2 explorations) | 0.99 | 6.4 |
| 058-02_rising-calm-below-recent-high | - | plan | inconclusive (-1.67) | not profitable enough (failed: Calmar) | - | 7.b: 058-02.b1_rising-calm-deep-dips-extend; 7.g: 058-02.g1_choppy-agitated-dip-continues | 1.01 | 6.7 |
| 058-02.b1_rising-calm-deep-dips-extend | 058-02_rising-calm-below-recent-high | plan | inconclusive (+0.61) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-02.b1.b1_deep-calm-uptrend-dips-extend; 7.g: 058-02.b1.g1_rising-calm-high-distance-continuation | 0.98 | 6.2 |
| 058-02.b1.b1_deep-calm-uptrend-dips-extend | 058-02.b1_rising-calm-deep-dips-extend | plan | inconclusive (+0.61) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-02.b1.b1.b1_calm-uptrend-dips-bounce-briefly, 058-02.b1.b1.b2_calm-uptrend-dip-next-day-rebound; 7.g: 058-02.b1.b1.g1_calm-uptrend-one-day-dip-rebound, 058-02.b1.b1.g2_calm-uptrend-dip-three-day-rebound | 1.10 | 12.1 |
| 058-02.g1_choppy-agitated-dip-continues | 058-02_rising-calm-below-recent-high | plan | inconclusive (+0.32) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-02.g1.b1_rising-market-dip-continues, 058-02.g1.b2_dip-below-high-continues; 7.g: 058-02.g1.g1_rising-calm-dip-continues | 1.00 | 6.8 |

## Consumption
5 ideas, 5.08 USD, 38.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.36 | 2.2 |
| step4_backtest | 0.00 | 19.2 |
| step5_verdict | 0.83 | 3.0 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 1.84 | 6.5 |
| step7_7.g | 2.04 | 7.0 |
