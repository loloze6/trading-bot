# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 031-02_down-streak-length-reversal | - | plan | inconclusive (-1.27) | not profitable enough (failed: Calmar) | - | 7.b: 031-02.b1_sharp-daily-fall-rebounds; 7.g: no ideas: The streak length, the past returns, the volatility, the range, the weekday, the year and the book's extreme days all leave no pattern that stands out. Across about 60 groupings the best t's are 2.0 to 2.7, isolated and not graded (F3–F6). The book's profit is the coins' drift held 96 % of the time (F1, F2), not a new effect. | 1.02 | 5.7 |
| 031-02.b1_sharp-daily-fall-rebounds | 031-02_down-streak-length-reversal | plan | confirmed (+2.28) | not profitable enough (failed: Calmar) | - | 7.d: 031-02.b1.d1_sharp-fall-rebounds-in-turbulence, 031-02.b1.d2_rebound-graded-by-turbulence; 7.g: 031-02.b1.g1_long-up-streaks-keep-rising, 031-02.b1.g2_volatile-falls-rebound-harder | 1.06 | 5.8 |
| 031-02.b1.d1_sharp-fall-rebounds-in-turbulence | 031-02.b1_sharp-daily-fall-rebounds | plan | confirmed (+2.06) | profitable enough | unseen_2016_2017: holds; unseen_2026: does not hold | 7.g: 031-02.b1.d1.g1_dip-rebound-grows-with-turbulence, 031-02.b1.d1.g2_long-up-runs-keep-rising | 0.61 | 4.7 |
| 031-02.b1.d2_rebound-graded-by-turbulence | 031-02.b1_sharp-daily-fall-rebounds | missing-components | - | - | - | - | 0.08 | 0.5 |
| 031-02.b1.g1_long-up-streaks-keep-rising | 031-02.b1_sharp-daily-fall-rebounds | missing-components | - | - | - | - | 0.05 | 0.2 |
| 031-02.b1.g2_volatile-falls-rebound-harder | 031-02.b1_sharp-daily-fall-rebounds | plan | inconclusive (+1.47) | not profitable enough (failed: Calmar) | - | 7.b: 031-02.b1.g2.b1_volatile-falls-more-coins, 031-02.b1.g2.b2_unusually-large-falls-rebound, 031-02.b1.g2.b3_next-day-rebound-after-falls; 7.g: 031-02.b1.g2.g1_strong-rises-keep-running | 1.19 | 5.4 |
| 031-02.b1.g2.b1_volatile-falls-more-coins | 031-02.b1.g2_volatile-falls-rebound-harder | plan | inconclusive (+1.33) | not profitable enough (failed: Calmar) | - | 7.b: 031-02.b1.g2.b1.b1_volatile-falls-next-day-rebound, 031-02.b1.g2.b1.b2_deep-fall-next-day-rebound; 7.g: no ideas: Across about seventy cells of forecast, streak, past-return, volatility, weekday, year and book-tail splits, no pattern stands out from chance once that many looks are counted. The best candidate, 20-day continuation over 10 days (F4), drops to a |t| of about 1 on most grid offsets and flips sign between years. The book's profit is the coins' own rise held at about 0.43 (F1), which leaves no new effect to propose. | 1.26 | 10.0 |
| 031-01_up-streak-length-reversal | - | plan | inconclusive (+1.08) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 031-01.b1_up-streak-reversal-more-coins, 031-01.b2_long-up-streaks-continue; 7.g: 031-01.g1_volatility-scaled-down-day-rebound, 031-01.g2_next-day-rebound-after-falls | 1.90 | 6.4 |
| 031-03_up-streak-length-continuation | - | plan | inconclusive (+1.43) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 031-03.b1_up-streak-continuation-more-coins; 7.g: 031-03.g1_large-up-day-continuation, 031-03.g2_fast-large-up-day-drift | 0.85 | 5.9 |
| 031-04_down-streak-length-continuation | - | plan | inconclusive (-0.18) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The test's result is zero (t -0.18) rather than short of the bar, and no coin, year, trend regime, horizon or streak length shows a graded down-streak continuation (F1–F6). So the clear answer is that, in these coins' daily bars, down streaks are not followed by further falls, and the one stray up-streak cell (F7) is too isolated to support an idea.; 7.g: 031-04.g1_one-day-volatility-scaled-reversal, 031-04.g2_run-depth-short-horizon-reversal | 0.84 | 6.1 |
| 031-01.b1_up-streak-reversal-more-coins | 031-01_up-streak-length-reversal | plan | inconclusive (+0.87) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The test already used every coin and all four folds, so no more daily data is available. The effect is not clearly present in any one part of the data and graded with streak length there (F2, F4, F6, F7). The only significant reading is a 1-day reversal after a single up close (F3, F5), which does not grow with the streak, so no graded idea rests on it.; 7.g: no ideas: Across roughly 90 groupings over 3 rounds (streak length and sign, run size, day's move, 5- and 20-day returns, volatility regime, weekday, year, coin and forecast quartile), the one |t| above 2 (-2.52) was ungraded and sat between neighbours of the opposite sign, which is what chance produces among that many looks. The book's loss is simply the cost of being short a rising market (F1), so no pattern stands out enough to support an idea. | 1.05 | 10.9 |
| 031-03.b1_up-streak-continuation-more-coins | 031-03_up-streak-length-continuation | plan | inconclusive (+0.54) | not profitable enough (failed: Calmar) | - | 7.b: 031-03.b1.b1_up-streak-continuation-in-uptrend; 7.g: no ideas: Across about fifteen angles (streak length on both sides, past returns, volatility, daily range absolute and relative, move size by sign, weekday, year, the book's extreme days), the strongest pattern is that a wide range relative to the coin's last 20 days precedes a higher 5-day move, but its pooled t is only 1.81. After that many looks it cannot be told apart from chance, so no finding supports a new idea. | 1.07 | 10.6 |

## Consumption
12 ideas, 10.99 USD, 72.2 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.83 | 6.3 |
| step4_backtest | 0.00 | 36.1 |
| step5_verdict | 1.72 | 6.1 |
| step6_check | 0.00 | 0.6 |
| chart_files | 0.00 | 0.2 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.45 | 1.6 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 2.65 | 8.0 |
| step7_7.g | 4.34 | 12.2 |
| similarity_check | 0.00 | 0.1 |
| unseen_test | 0.00 | 0.9 |
