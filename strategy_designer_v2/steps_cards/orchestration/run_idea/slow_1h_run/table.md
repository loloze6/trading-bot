# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 016-01_up-grind-price-continuation | - | missing-components | - | - | - | - | 0.05 | 0.3 |
| 016-02_down-grind-price-continuation | - | missing-components | - | - | - | - | 0.04 | 0.3 |
| 016-03_up-jump-price-reversal | - | missing-components | - | - | - | - | 0.04 | 0.3 |
| 016-04_down-jump-price-reversal | - | missing-components | - | - | - | - | 0.05 | 0.3 |
| 016-05_up-even-volume-continuation | - | missing-components | - | - | - | - | 0.08 | 0.6 |
| 016-06_down-even-volume-continuation | - | plan | inconclusive (+0.94) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 016-06_down-even-volume-continuation.b1_three-day-fall-size-rebound, 016-06_down-even-volume-continuation.b2_smooth-falls-keep-falling; 7.d: 016-06_down-even-volume-continuation.d1_even-volume-gentle-falls, 016-06_down-even-volume-continuation.d2_gentle-falls-keep-falling; 7.g: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound, 016-06_down-even-volume-continuation.g2_smooth-climb-continuation | 1.31 | 25.7 |
| 016-07_up-volume-burst-reversal | - | missing-components | - | - | - | - | 0.36 | 0.3 |
| 016-08_down-volume-burst-reversal | - | missing-components | - | - | - | - | 0.04 | 0.3 |
| 016-06_down-even-volume-continuation.g1_fresh-drop-rebound | 016-06_down-even-volume-continuation | plan | confirmed (+2.75) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold; 7.g: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.g1_one-day-fresh-drop-rebound, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.g2_smooth-up-grind-continuation | 0.92 | 18.6 |
| 016-06_down-even-volume-continuation.g2_smooth-climb-continuation | 016-06_down-even-volume-continuation | plan | inconclusive (+1.25) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation.b1_smooth-climbs-keep-rising, 016-06_down-even-volume-continuation.g2_smooth-climb-continuation.b2_smooth-climb-more-coins; 7.d: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation.d1_slow-raw-smooth-climb-continuation, 016-06_down-even-volume-continuation.g2_smooth-climb-continuation.d2_choppy-big-climb-reverses; 7.g: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation.g1_absolute-smoothness-climb-continuation, 016-06_down-even-volume-continuation.g2_smooth-climb-continuation.g2_deep-drop-three-day-rebound, 016-06_down-even-volume-continuation.g2_smooth-climb-continuation.g3_violent-decline-rebound | 1.24 | 19.5 |

## Consumption
10 ideas, 4.12 USD, 66.2 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.91 | 4.3 |
| step4_backtest | 0.00 | 48.8 |
| step5_verdict | 0.37 | 1.6 |
| step6_check | 0.00 | 0.7 |
| chart_files | 0.00 | 0.4 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.d | 1.07 | 4.1 |
| step7_7.b | 0.67 | 2.4 |
| step7_7.g | 1.10 | 4.0 |
