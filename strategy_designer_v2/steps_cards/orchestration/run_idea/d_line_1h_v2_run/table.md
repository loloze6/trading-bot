# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound | 016-06_down-even-volume-continuation.g1_fresh-drop-rebound | plan | confirmed (+2.63) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.d1_rebound-inside-monthly-uptrend, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.d2_rebound-after-volatile-drops, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.d3_dip-in-rising-month; 7.g: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.g1_one-day-fall-next-day-rebound, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.g2_one-day-rise-next-day-giveback | 1.35 | 12.5 |
| 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold | 016-06_down-even-volume-continuation.g1_fresh-drop-rebound | plan | inconclusive (+3.93) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.b1_one-day-graded-drop-rebound; 7.d: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.d1_high-volume-drop-rebound, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.d2_violent-drop-rebound-only, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.d3_deep-three-day-fall-rebound, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.d4_down-day-volume-sets-direction; 7.g: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.g1_high-volatility-one-day-reversal, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.g2_calm-market-three-day-continuation | 1.31 | 13.7 |
| 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising | 016-03_up-jump-price-reversal | plan | inconclusive (+1.50) | profitable enough | - | 7.b: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.b1_grinding-rises-more-coins, 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.b2_grinding-falls-keep-falling; 7.e: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.e1_share-of-up-hours-continuation, 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.e2_grind-continuation-in-uptrends; 7.g: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.g1_late-utc-volatility-scaled-drift, 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.g2_efficient-rises-keep-rising | 1.12 | 12.7 |

## Consumption
3 ideas, 3.78 USD, 38.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.56 | 1.5 |
| step4_backtest | 0.00 | 26.2 |
| step5_verdict | 0.39 | 1.6 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.3 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.37 | 1.3 |
| step7_7.b | 0.42 | 1.4 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.74 | 2.4 |
| step7_7.g | 1.29 | 4.1 |
