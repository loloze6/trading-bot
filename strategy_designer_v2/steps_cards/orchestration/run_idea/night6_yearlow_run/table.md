# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 031-01_near-yearly-low-keeps-falling | - | plan | inconclusive (+1.70) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 031-01.b1_near-yearly-low-falls-all-coins; 7.g: 031-01.g1_weekly-gains-carry-into-saturday | 1.08 | 6.0 |
| 031-02_near-yearly-low-bounces | - | plan | inconclusive (-1.70) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 031-02.b1_failed-rally-near-yearly-low; 7.g: 031-02.g1_weekend-continues-the-week-s-move | 1.12 | 6.1 |
| 031-03_yearly-low-break-extends | - | plan | inconclusive (+0.01) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 031-03.b1_deep-yearly-low-break-rebounds; 7.g: no ideas: The data gives no stable pattern to build on. The breaks are few (24 grid cases on 13 days), the hints of a post-break bounce (F1, F2, F6) and of a falling break day continuing (F4) all have t below 2, and none of the bar-wide angles I examined (F5) stands out from chance after that many looks. | 1.09 | 6.8 |
| 031-04_yearly-low-break-reverses | - | plan | not observable (+1.41) | not profitable enough (failed: Calmar, Trades per day) | - | 7.a: 031-04.a1_yearly-low-break-all-coins; 7.g: no ideas: Across momentum over 5 to 30 days, range position, volatility, weekday, year and the regime's cases, no pattern stood out beyond chance: the best graded slope had a day-clustered t of 1.43 and flipped sign across years, and the two notable weekdays are the expected extremes of many comparisons. | 1.04 | 6.1 |

## Consumption
4 ideas, 4.32 USD, 25.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.43 | 2.9 |
| step4_backtest | 0.00 | 9.9 |
| step5_verdict | 0.68 | 2.5 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.38 | 1.1 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 1.04 | 3.4 |
| step7_7.g | 1.79 | 5.1 |
