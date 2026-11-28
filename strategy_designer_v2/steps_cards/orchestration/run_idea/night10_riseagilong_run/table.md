# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 086-01_first-up-after-long-down-run | - | plan | no effect (-0.16) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.c: 086-01.c1_forceful-turn-day-continues, 086-01.c2_shallow-pullback-turn-continues | 0.77 | 6.8 |
| 086-02_first-up-after-deep-down-run | - | plan | no effect (-0.16) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.c: 086-02.c1_forceful-break-day-continues; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.21 | 7.9 |
| 087-01_agitated-rise-scaled-burst-continues | - | plan | inconclusive (+1.36) | not profitable enough (failed: Sharpe minus holding's Sharpe, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 087-01.b1_scaled-burst-continues-more-coins; 7.g: 087-01.g1_raw-swing-unit-push-continuation | 0.92 | 7.2 |
| 087-02_agitated-push-off-low-continues | - | missing-components | - | - | - | - | 0.09 | 0.5 |
| 086-01.c1_forceful-turn-day-continues | 086-01_first-up-after-long-down-run | plan | no effect (-0.28) | not profitable enough (failed: Sharpe minus holding's Sharpe, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-01.c1.c1_buy-within-long-down-run; 7.g: 0 ideas, 1 discoveries (3 explorations) | 1.33 | 8.2 |
| 041-01.b1_rising-agitated-rise-continues | 041-01_agitated-scaled-rise-next-day-continues | plan | no effect (+0.02) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 041-01.b1.c1_rising-agitated-fall-rebound-four-days, 041-01.b1.c2_rising-agitated-rise-continues-three-days; 7.g: no ideas: In rising agitated markets, the only pattern near significance is a 3-day scaled-rise continuation (t 2.11). It vanishes on the other two 3-day grids (t 0.36, 0.42), it was found among about 60 tests, and it repeats the rising-market continuation ideas the map already holds in that cell (034-01.e1, 034-02, 033-03.b2). So no finding supports a new idea for this research. | 1.31 | 7.6 |
| 086-02.c1_forceful-break-day-continues | 086-02_first-up-after-deep-down-run | plan | no effect (-0.13) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.c: 086-02.c1.c1_shallow-pullback-break-continues; 7.g: no ideas: In rising agitated markets, neither the turning day's force nor the run's length or depth grades the following rise, and longer runs even point the other way (F2–F4). The only pattern near significance, nearness to the 20-day high, does not stand out after the angles searched and is already held (F5). The rest looks like chance or is off the box (F6, F7). We looked at the forecast's terciles, run length and depth, close location, 5- and 20-day returns, distance to the 20- and 60-day highs and the 20-day low, volume, day range, 60-day return, weekday, coin, year, the 3-, 5- and 10-day horizons, and the book's extreme days. | 4.45 | 21.0 |

## Consumption
7 ideas, 10.07 USD, 59.3 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.70 | 4.3 |
| step4_backtest | 0.00 | 22.7 |
| step5_verdict | 1.11 | 4.3 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.g | 2.40 | 6.5 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 0.22 | 0.7 |
| step7_7.c | 5.64 | 20.5 |
