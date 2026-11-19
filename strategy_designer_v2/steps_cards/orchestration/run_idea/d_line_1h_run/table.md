# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound | 016-06_down-even-volume-continuation.g1_fresh-drop-rebound | plan | confirmed (+3.16) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.d1_deep-relative-fall-rebound, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.d2_slow-rebound-after-deep-falls; 7.g: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.g1_grind-up-rise-continues, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.g2_choppy-fall-keeps-falling, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.g3_only-extreme-falls-rebound | 1.32 | 15.5 |
| 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold | 016-06_down-even-volume-continuation.g1_fresh-drop-rebound | plan | inconclusive (+2.75) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.b1_one-day-rebound-after-drop; 7.d: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.d1_daily-set-three-day-drop-rebound, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.d2_deep-drop-only-rebound, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.d3_three-day-fall-depth-rebound; 7.g: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.g1_one-day-fresh-drop-rebound, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.g2_volatility-graded-daily-reversal, 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.g3_calm-day-move-continuation | 1.28 | 17.1 |
| 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising | 016-03_up-jump-price-reversal | plan | inconclusive (-0.65) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.b1_three-day-rise-size-continues, 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.b2_deep-three-day-falls-rebound; 7.d: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.d1_slow-grind-keeps-rising, 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.d2_efficient-rises-keep-rising; 7.g: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.g1_volatile-one-day-fall-rebound, 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.g2_three-day-fall-rebound, 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.g3_efficient-rises-keep-rising | 1.25 | 15.5 |

## Consumption
3 ideas, 3.85 USD, 48.2 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.55 | 1.5 |
| step4_backtest | 0.00 | 32.8 |
| step5_verdict | 0.37 | 1.6 |
| step6_check | 0.00 | 0.7 |
| chart_files | 0.00 | 0.4 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.71 | 2.6 |
| step7_7.d | 1.03 | 4.0 |
| step7_7.g | 1.18 | 4.5 |
