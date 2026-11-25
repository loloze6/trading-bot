# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_choppy-weekly-rise-reverses | - | plan | inconclusive (-0.99) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1_agitated-trend-weekly-reversal; 7.g: 032-01.g1_large-daily-fall-rebounds, 032-01.g2_agitated-fall-next-day-rebound | 1.19 | 6.6 |
| 032-02_choppy-weekly-fall-rebounds | - | plan | inconclusive (+1.01) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 032-02.b1_choppy-weekly-falls-keep-falling; 7.g: 032-02.g1_deep-daily-fall-rebounds, 032-02.g2_agitated-daily-fall-rebound | 1.02 | 6.3 |
| 032-01.b1_agitated-trend-weekly-reversal | 032-01_choppy-weekly-rise-reverses | plan | inconclusive (-1.03) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1.b1_large-weekly-rise-continues; 7.g: 032-01.b1.g1_calm-chop-weekly-continuation, 032-01.b1.g2_weekly-move-continuation-graded | 1.01 | 5.5 |
| 032-02.b1_choppy-weekly-falls-keep-falling | 032-02_choppy-weekly-fall-rebounds | plan | inconclusive (+1.41) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-02.b1.b1_choppy-falls-more-coins, 032-02.b1.b2_weekly-falls-after-directionless-months; 7.g: 032-02.b1.g1_sharp-daily-drop-rebounds, 032-02.b1.g2_calm-chop-weekly-continuation | 1.09 | 5.9 |
| 032-01.b1.b1_large-weekly-rise-continues | 032-01.b1_agitated-trend-weekly-reversal | plan | inconclusive (+1.94) | profitable enough | - | 7.b: 032-01.b1.b1.b1_large-weekly-rise-continues-more-coins, 032-01.b1.b1.b2_scaled-weekly-move-continues; 7.e: 032-01.b1.b1.e1_large-weekly-fall-continues, 032-01.b1.b1.e2_choppy-market-weekly-move-continues, 032-01.b1.b1.e3_weekly-rise-within-rising-month, 032-01.b1.b1.e4_calm-month-weekly-breakout-continues; 7.g: 032-01.b1.b1.g1_large-down-day-next-day-rebound, 032-01.b1.b1.g2_agitated-down-day-rebound-grows, 032-01.b1.b1.g3_dip-in-rising-week-rebounds | 1.24 | 6.4 |
| 032-01.b1.b1.e1_large-weekly-fall-continues | 032-01.b1.b1_large-weekly-rise-continues | plan | inconclusive (-1.10) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1.b1.e1.b1_choppy-large-weekly-rise-continues; 7.g: 032-01.b1.b1.e1.g1_sharp-daily-fall-rebounds, 032-01.b1.b1.e1.g2_agitated-daily-fall-reversal | 1.24 | 6.1 |
| 032-01.b1.b1.e2_choppy-market-weekly-move-continues | 032-01.b1.b1_large-weekly-rise-continues | plan | confirmed (+3.56) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.d: 032-01.b1.b1.e2.d1_raw-scaled-weekly-continuation, 032-01.b1.b1.e2.d2_chop-continuation-with-month; 7.g: 032-01.b1.b1.e2.g1_calm-market-weekly-move-continues, 032-01.b1.b1.e2.g2_agitated-market-daily-move-reverses | 1.17 | 6.1 |
| 032-01.b1.b1.e2.d1_raw-scaled-weekly-continuation | 032-01.b1.b1.e2_choppy-market-weekly-move-continues | plan | confirmed (+2.14) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.d: 032-01.b1.b1.e2.d1.d1_chop-continuation-with-monthly-lean, 032-01.b1.b1.e2.d1.d2_continuation-held-only-in-chop, 032-01.b1.b1.e2.d1.d3_aligned-continuation-inside-chop; 7.g: no ideas: Beyond the tested idea's own choppy-regime continuation (F1, F2), I looked at efficiency-ratio levels, volatility ranks, coins, years, weekdays, daily shocks, trade sides and the book's extreme days, and every other pattern (F4, F5, F6) falls under t 2 once days are clustered or holds on only two of six coins, so none stands out from chance across that many angles. | 1.26 | 6.3 |
| 032-01.b1.b1.e2.d2_chop-continuation-with-month | 032-01.b1.b1.e2_choppy-market-weekly-move-continues | plan | confirmed (+3.90) | not profitable enough (failed: Calmar) | - | 7.d: 032-01.b1.b1.e2.d2.d1_chop-continuation-while-chop-lasts, 032-01.b1.b1.e2.d2.d2_strong-case-chop-continuation; 7.g: 032-01.b1.b1.e2.d2.g1_contracted-swings-monthly-continuation, 032-01.b1.b1.e2.d2.g2_chop-week-plus-month-continuation | 1.00 | 5.6 |
| 032-03_reversal-grows-with-choppiness | - | plan | inconclusive (-2.00) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-03.b1_choppy-weekly-rise-continues, 032-03.b2_quiet-coin-weekly-move-continues; 7.g: 032-03.g1_next-day-rebound-after-shocks, 032-03.g2_calm-regime-weekly-continuation | 1.80 | 5.9 |
| 032-01.b1.b1.e2.d1.d1_chop-continuation-with-monthly-lean | 032-01.b1.b1.e2.d1_raw-scaled-weekly-continuation | plan | confirmed (+2.75) | not profitable enough (failed: Calmar) | - | 7.d: 032-01.b1.b1.e2.d1.d1.d1_chop-continuation-while-aligned, 032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean; 7.g: 032-01.b1.b1.e2.d1.d1.g1_agitated-large-fall-next-day-bounce | 1.40 | 6.6 |
| 032-01.b1.b1.e2.d1.d2_continuation-held-only-in-chop | 032-01.b1.b1.e2.d1_raw-scaled-weekly-continuation | plan | confirmed (+3.56) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.d: 032-01.b1.b1.e2.d1.d2.d1_chop-continuation-along-30-day-drift; 7.g: 032-01.b1.b1.e2.d1.d2.g1_scaled-daily-fall-rebounds, 032-01.b1.b1.e2.d1.d2.g2_close-at-low-next-day-bounce, 032-01.b1.b1.e2.d1.d2.g3_monthly-drift-persists-in-chop, 032-01.b1.b1.e2.d1.d2.g4_trending-market-weekly-fall-reverses | 1.06 | 5.8 |

## Consumption
12 ideas, 14.49 USD, 73.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.89 | 7.3 |
| step4_backtest | 0.00 | 23.2 |
| step5_verdict | 2.07 | 7.8 |
| step6_check | 0.00 | 0.5 |
| chart_files | 0.00 | 0.2 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 2.50 | 8.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.38 | 1.4 |
| step7_7.g | 5.06 | 15.9 |
| step7_7.b | 2.59 | 8.5 |
| similarity_check | 0.00 | 0.3 |
