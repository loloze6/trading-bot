# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_choppy-weekly-rise-reverses | - | plan | inconclusive (-0.99) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1_agitated-trend-weekly-reversal; 7.g: 032-01.g1_large-daily-fall-rebounds, 032-01.g2_agitated-fall-next-day-rebound | 1.19 | 6.6 |
| 032-02_choppy-weekly-fall-rebounds | - | plan | inconclusive (+1.01) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 032-02.b1_choppy-weekly-falls-keep-falling; 7.g: 032-02.g1_deep-daily-fall-rebounds, 032-02.g2_agitated-daily-fall-rebound | 1.02 | 6.3 |
| 032-03_reversal-grows-with-choppiness | - | missing-components | - | - | - | - | 0.08 | 0.5 |
| 032-01.b1_agitated-trend-weekly-reversal | 032-01_choppy-weekly-rise-reverses | plan | inconclusive (-1.03) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1.b1_large-weekly-rise-continues; 7.g: 032-01.b1.g1_calm-chop-weekly-continuation, 032-01.b1.g2_weekly-move-continuation-graded | 1.01 | 5.5 |
| 032-02.b1_choppy-weekly-falls-keep-falling | 032-02_choppy-weekly-fall-rebounds | plan | inconclusive (+1.41) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-02.b1.b1_choppy-falls-more-coins, 032-02.b1.b2_weekly-falls-after-directionless-months; 7.g: 032-02.b1.g1_sharp-daily-drop-rebounds, 032-02.b1.g2_calm-chop-weekly-continuation | 1.09 | 5.9 |
| 032-01.b1.b1_large-weekly-rise-continues | 032-01.b1_agitated-trend-weekly-reversal | plan | inconclusive (+1.94) | profitable enough | - | 7.b: 032-01.b1.b1.b1_large-weekly-rise-continues-more-coins, 032-01.b1.b1.b2_scaled-weekly-move-continues; 7.e: 032-01.b1.b1.e1_large-weekly-fall-continues, 032-01.b1.b1.e2_choppy-market-weekly-move-continues, 032-01.b1.b1.e3_weekly-rise-within-rising-month, 032-01.b1.b1.e4_calm-month-weekly-breakout-continues; 7.g: 032-01.b1.b1.g1_large-down-day-next-day-rebound, 032-01.b1.b1.g2_agitated-down-day-rebound-grows, 032-01.b1.b1.g3_dip-in-rising-week-rebounds | 1.24 | 6.4 |
| 032-01.b1.b1.e1_large-weekly-fall-continues | 032-01.b1.b1_large-weekly-rise-continues | plan | inconclusive (-1.10) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1.b1.e1.b1_choppy-large-weekly-rise-continues; 7.g: 032-01.b1.b1.e1.g1_sharp-daily-fall-rebounds, 032-01.b1.b1.e1.g2_agitated-daily-fall-reversal | 1.24 | 6.1 |

## Consumption
7 ideas, 6.87 USD, 37.3 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.68 | 4.5 |
| step4_backtest | 0.00 | 12.2 |
| step5_verdict | 1.04 | 3.8 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.38 | 1.3 |
| step7_7.g | 2.52 | 7.8 |
| step7_7.b | 2.25 | 7.3 |
