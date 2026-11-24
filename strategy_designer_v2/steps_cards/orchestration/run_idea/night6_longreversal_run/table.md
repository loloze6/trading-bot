# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 031-01_extreme-rise-partly-reverses | - | plan | inconclusive (-1.02) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The result sits on the continuation side but cannot be told from zero, and it rests on a few large outliers (F1). No coin, period, recent path, horizon or forecast size shows the predicted reversal (F2–F4), so there is no part of the data to narrow the idea to and no continuation effect large enough to propose instead.; 7.g: 031-01.g1_sharp-drop-next-day-bounce | 0.99 | 6.0 |
| 031-02_extreme-fall-partly-rebounds | - | plan | inconclusive (+0.01) | not profitable enough (failed: Calmar) | - | 7.b: 031-02.b1_deep-fall-still-falling-rebounds, 031-02.b2_graded-deep-and-recent-fall; 7.g: no ideas: Over about 30 angles (eleven features at two horizons, slopes at three horizons, coins, years, volatility halves, weekdays and trades), no pattern stood out beyond chance. The best candidate, 14-day continuation over the next 7 days, has a day-clustered t of only 1.45 and flips sign across coins and years, and the Saturday effect (t 2.2) is one of seven weekdays tested. | 0.99 | 6.5 |
| 031-03_fading-volume-after-rise-reverses | - | plan | inconclusive (-0.46) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 031-03.b1_short-horizon-continuation-after-moves; 7.g: 031-03.g1_volume-surge-leads-two-week-drift, 031-03.g2_one-week-momentum-continues | 0.98 | 6.6 |
| 031-04_fading-volume-after-fall-rebounds | - | plan | mismatch | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.g: no ideas: The book never entered its regime because the 122-bar windows cannot warm up a 365-day volatility (F1). Across the past-move, volume, volatility, range, distance-from-high, one-day-return and weekday angles I looked at, no pattern stood out beyond chance given the number of tests (F2–F6), so no finding supports a new idea. | 0.76 | 5.5 |

## Consumption
4 ideas, 3.73 USD, 24.6 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.37 | 2.2 |
| step4_backtest | 0.00 | 11.3 |
| step5_verdict | 0.85 | 3.1 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 1.04 | 3.2 |
| step7_7.g | 1.47 | 4.6 |
