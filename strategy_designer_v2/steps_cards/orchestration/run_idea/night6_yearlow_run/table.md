# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 031-01_near-yearly-low-keeps-falling | - | plan | inconclusive (+1.70) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 031-01.b1_near-yearly-low-falls-all-coins; 7.g: 031-01.g1_weekly-gains-carry-into-saturday | 1.08 | 6.0 |
| 031-02_near-yearly-low-bounces | - | plan | inconclusive (-1.70) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 031-02.b1_failed-rally-near-yearly-low; 7.g: 031-02.g1_weekend-continues-the-week-s-move | 1.12 | 6.1 |
| 031-03_yearly-low-break-extends | - | plan | inconclusive (+0.01) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 031-03.b1_deep-yearly-low-break-rebounds; 7.g: no ideas: The data gives no stable pattern to build on. The breaks are few (24 grid cases on 13 days), the hints of a post-break bounce (F1, F2, F6) and of a falling break day continuing (F4) all have t below 2, and none of the bar-wide angles I examined (F5) stands out from chance after that many looks. | 1.09 | 6.8 |
| 031-04_yearly-low-break-reverses | - | plan | not observable (+1.41) | not profitable enough (failed: Calmar, Trades per day) | - | 7.a: 031-04.a1_yearly-low-break-all-coins; 7.g: no ideas: Across momentum over 5 to 30 days, range position, volatility, weekday, year and the regime's cases, no pattern stood out beyond chance: the best graded slope had a day-clustered t of 1.43 and flipped sign across years, and the two notable weekdays are the expected extremes of many comparisons. | 1.04 | 6.1 |
| 031-01.b1_near-yearly-low-falls-all-coins | 031-01_near-yearly-low-keeps-falling | plan | inconclusive (+1.07) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The slope is on the idea's side but small at every horizon (F1), the test already used all available coins and folds, and the effect is not graded in proximity (F2–F4) and appears in no stable coin, year or horizon subset, only in market-phase swings that flip sign (F5, F6), so no amended idea has a finding to rest on.; 7.g: no ideas: The one pattern that stands out against the many angles looked at is the Saturday rise (F3), and it is an on/off calendar condition with no graded situation. Every graded situation examined (nearness to the yearly low, large down days, past returns, volatility, distance from recent lows) was non-monotone or could not be told from chance (F1, F2, F4, F5). | 1.09 | 10.5 |

## Consumption
5 ideas, 5.41 USD, 35.6 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.51 | 3.3 |
| step4_backtest | 0.00 | 17.0 |
| step5_verdict | 0.86 | 3.0 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.38 | 1.1 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 1.42 | 4.4 |
| step7_7.g | 2.25 | 6.5 |
