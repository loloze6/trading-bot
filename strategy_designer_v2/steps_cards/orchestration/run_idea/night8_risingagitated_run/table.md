# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 058-01_agitated-rise-stretch-giveback | - | plan | inconclusive (+0.39) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The theme's effect is not in the data. In rising agitated markets a close far above its 20-day average is followed by a further rise beyond drift, not a giveback (F2), and no graded fall shows at any horizon, coin or distance band (F1, F3, F4, F5).; 7.g: 0 ideas, 2 discoveries (3 explorations) | 1.09 | 6.5 |
| 058-02_agitated-rise-swing-scaled-giveback | - | missing-components | - | - | - | - | 0.07 | 0.4 |
| 058-03_calm-rise-stretch-continuation | - | plan | inconclusive (+1.49) | profitable enough | - | 7.b: 058-03.b1_calm-rise-continuation-all-coins; 7.e: 058-03.e1_calm-rise-stretch-ten-days, 058-03.e2_choppy-market-distance-continuation; 7.g: 0 ideas, 2 discoveries (3 explorations) | 1.47 | 7.3 |
| 058-03.e1_calm-rise-stretch-ten-days | 058-03_calm-rise-stretch-continuation | plan | confirmed (+2.32) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: 058-03.e1.g1_choppy-stretch-continues-ten-days | 0.73 | 6.2 |
| 058-03.e2_choppy-market-distance-continuation | 058-03_calm-rise-stretch-continuation | plan | inconclusive (+0.72) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-03.e2.b1_choppy-distance-continuation-more-coins; 7.g: 0 ideas, 1 discoveries (3 explorations) | 0.98 | 5.3 |
| 058-03.b1_calm-rise-continuation-all-coins | 058-03_calm-rise-stretch-continuation | plan | confirmed (+2.06) | not profitable enough (failed: Calmar) | - | 7.d: 058-03.b1.d1_calm-rise-moderate-stretch, 058-03.b1.d2_calm-rise-longer-hold; 7.g: 0 ideas, 2 discoveries (2 explorations) | 1.37 | 12.0 |
| 058-03.e2.b1_choppy-distance-continuation-more-coins | 058-03.e2_choppy-market-distance-continuation | plan | inconclusive (+0.97) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 058-03.e2.b1.b1_choppy-distance-continuation-recent-swings; 7.g: 0 ideas, 2 discoveries (3 explorations) | 1.30 | 11.2 |

## Consumption
7 ideas, 7.01 USD, 48.9 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.46 | 2.6 |
| step4_backtest | 0.00 | 24.4 |
| step5_verdict | 0.99 | 3.4 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.70 | 1.9 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.46 | 1.2 |
| step7_7.b | 1.09 | 3.6 |
| step7_7.g | 3.31 | 10.3 |
| similarity_check | 0.00 | 0.1 |
| unseen_test | 0.00 | 1.1 |
