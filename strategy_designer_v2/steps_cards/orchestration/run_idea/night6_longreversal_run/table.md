# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 031-01_extreme-rise-partly-reverses | - | plan | inconclusive (-1.02) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The result sits on the continuation side but cannot be told from zero, and it rests on a few large outliers (F1). No coin, period, recent path, horizon or forecast size shows the predicted reversal (F2–F4), so there is no part of the data to narrow the idea to and no continuation effect large enough to propose instead.; 7.g: 031-01.g1_sharp-drop-next-day-bounce | 0.99 | 6.0 |
| 031-02_extreme-fall-partly-rebounds | - | plan | inconclusive (+0.01) | not profitable enough (failed: Calmar) | - | 7.b: 031-02.b1_deep-fall-still-falling-rebounds, 031-02.b2_graded-deep-and-recent-fall; 7.g: no ideas: Over about 30 angles (eleven features at two horizons, slopes at three horizons, coins, years, volatility halves, weekdays and trades), no pattern stood out beyond chance. The best candidate, 14-day continuation over the next 7 days, has a day-clustered t of only 1.45 and flips sign across coins and years, and the Saturday effect (t 2.2) is one of seven weekdays tested. | 0.99 | 6.5 |
| 031-03_fading-volume-after-rise-reverses | - | plan | inconclusive (-0.46) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 031-03.b1_short-horizon-continuation-after-moves; 7.g: 031-03.g1_volume-surge-leads-two-week-drift, 031-03.g2_one-week-momentum-continues | 0.98 | 6.6 |
| 031-04_fading-volume-after-fall-rebounds | - | plan | mismatch | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.g: no ideas: The book never entered its regime because the 122-bar windows cannot warm up a 365-day volatility (F1). Across the past-move, volume, volatility, range, distance-from-high, one-day-return and weekday angles I looked at, no pattern stood out beyond chance given the number of tests (F2–F6), so no finding supports a new idea. | 0.76 | 5.5 |
| 031-02.b1_deep-fall-still-falling-rebounds | 031-02_extreme-fall-partly-rebounds | plan | inconclusive (+1.22) | not profitable enough (failed: Calmar) | - | 7.b: 031-02.b1.b1_deepest-falls-rebound-most, 031-02.b1.b2_levelled-off-deep-falls-rebound; 7.g: 031-02.b1.g1_strong-month-continues-next-week | 1.20 | 10.8 |
| 031-03.b1_short-horizon-continuation-after-moves | 031-03_fading-volume-after-rise-reverses | plan | inconclusive (+0.65) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 031-03.b1.b1_20-day-continuation-all-coins; 7.g: no ideas: Across the forecast, the 5-, 20- and 60-day moves, volatility levels, volatility ratios, weekdays, the day after large moves, coins, years, halves and the book's sides, no pattern stood out from chance once same-day cases were taken together and the many angles weighed (F2–F7). The book's only steady gain was the coins' own rise on its long bars (F1), which is holding the coins, not a new idea. | 1.11 | 5.2 |
| 031-02.b2_graded-deep-and-recent-fall | 031-02_extreme-fall-partly-rebounds | plan | not observable (+0.01) | not profitable enough (failed: Calmar) | - | 7.a: 031-02.b2.a1_deep-fall-rebound-nineteen-coins; 7.g: 031-02.b2.g1_short-horizon-scaled-trend-continuation, 031-02.b2.g2_quiet-market-trend-continuation | 1.23 | 7.1 |
| 031-02.b1.b1_deepest-falls-rebound-most | 031-02.b1_deep-fall-still-falling-rebounds | plan | inconclusive (+0.99) | not profitable enough (failed: Calmar) | - | 7.b: 031-02.b1.b1.b1_steadied-falls-rebound-most; 7.g: 031-02.b1.b1.g1_90-day-run-ups-keep-rising | 1.30 | 10.6 |
| 031-03.b1.b1_20-day-continuation-all-coins | 031-03.b1_short-horizon-continuation-after-moves | plan | inconclusive (+1.52) | not profitable enough (failed: Calmar) | - | 7.b: 031-03.b1.b1.b1_aligned-20-day-continuation; 7.g: 031-03.b1.b1.g1_volatility-scaled-monthly-continuation, 031-03.b1.b1.g2_direction-not-size-turbulent-coins, 031-03.b1.b1.g3_long-side-volatile-continuation | 1.08 | 10.3 |
| 031-02.b1.b2_levelled-off-deep-falls-rebound | 031-02.b1_deep-fall-still-falling-rebounds | plan | mismatch | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.g: no ideas: Across the regime, forecast, trades, momentum at 7 to 90 days, 1-day reversal, volatility level and weekday, nothing stands out from chance once cases are grouped by day and the number of angles is counted, so none supports a new idea. | 0.93 | 9.1 |
| 031-02.b2.a1_deep-fall-rebound-nineteen-coins | 031-02.b2_graded-deep-and-recent-fall | plan | inconclusive (-0.20) | not profitable enough (failed: Calmar) | - | 7.b: 031-02.b2.a1.b1_depth-graded-ninety-day-fall-rebound, 031-02.b2.a1.b2_deep-fall-rebound-45-days; 7.g: no ideas: The only pattern that stands out after this many angles is a Saturday rise (F1, F2), which is a fixed calendar condition with no grading. Everything graded (forecast parts, past returns, volatility, recent week inside the regime; F3–F5) cannot be told from chance, so no graded, one-direction idea is supported. | 1.16 | 11.4 |
| 031-02.b1.b1.b1_steadied-falls-rebound-most | 031-02.b1.b1_deepest-falls-rebound-most | plan | inconclusive (-1.33) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 031-02.b1.b1.b1.b1_monthly-losers-keep-falling; 7.g: 031-02.b1.b1.b1.g1_monthly-trend-carries-next-week | 1.08 | 9.3 |

## Consumption
12 ideas, 12.81 USD, 98.3 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.09 | 6.6 |
| step4_backtest | 0.00 | 54.7 |
| step5_verdict | 2.31 | 8.3 |
| step6_check | 0.00 | 0.4 |
| chart_files | 0.00 | 0.2 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.31 | 1.0 |
| step7_7.b | 3.39 | 10.2 |
| step7_7.g | 5.71 | 16.8 |
