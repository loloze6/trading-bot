# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 086-01_first-down-day-streak-length | - | plan | no effect (-1.74) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-01.c1_first-dip-falls-over-week | 1.67 | 8.2 |
| 086-02_first-down-day-run-size | - | plan | no effect (-1.17) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-02.c1_first-dip-depth-continues, 086-02.c2_deep-down-day-continues; 7.g: no ideas: Across the forecast, streak length, dip size, horizons from 1 to 10 days, nine bar features, weekdays and windows, no pattern in rising agitated markets on the short side stands out from chance. The only ordering, a weaker fall after longer runs, is the opposite of the theme's effect and not significant, so the theme's effect is not in the data. | 1.16 | 8.9 |
| 086-01.c1_first-dip-falls-over-week | 086-01_first-down-day-streak-length | plan | no effect (-0.89) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-01.c1.c1_deep-first-dip-continues; 7.g: no ideas: Across about 45 feature-horizon-grid tests in rising agitated markets, the only patterns reach |t| near 2.5 and either reverse when the 7-day grid start is moved (close position in range, day's return) or are not graded and vanish beyond one day (up-streak length), so none stands out from chance. | 1.10 | 9.5 |
| 041-01.b1_rising-agitated-rise-continues | 041-01_agitated-scaled-rise-next-day-continues | plan | inconclusive (+1.86) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 041-01.b1.b1_rise-continuation-more-coins; 7.g: no ideas: Inside the rising agitated profile, none of the angles examined shows a graded effect that stands out from chance on the short side. The angles were the day's scaled move, multi-day stretch, close location, range, wicks, volume, distance to recent highs, weekday and the book's own days. The largest t is 2.26 among about 50 tests, its sign is wrong for a short, and the profile's negative drift cannot be told from 0 (ZEC t -1.39). | 1.01 | 8.3 |
| 086-02.c1_first-dip-depth-continues | 086-02_first-down-day-run-size | plan | no effect (-0.56) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-02.c1.c1_first-dip-falls-ten-days, 086-02.c1.c2_delayed-first-dip-continuation; 7.g: no ideas: After many angles, no pattern in rising agitated markets on the short side survives a change of sampling grid or shows a graded order: the down-run continuation (F4) and the low-close result (F6) vanish on other grid offsets. The brief's effect of a first dip after an up run continuing lower, graded by the run or by the dip, is not in these bars (F1–F3). | 1.03 | 8.7 |
| 086-02.c2_deep-down-day-continues | 086-02_first-down-day-run-size | plan | no effect (-0.10) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-02.c2.c1_large-run-first-dip-falls; 7.g: 086-02.c2.g2_deep-down-day-five-days | 1.01 | 8.7 |

## Consumption
6 ideas, 6.98 USD, 52.3 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.49 | 4.1 |
| step4_backtest | 0.00 | 30.9 |
| step5_verdict | 1.13 | 4.5 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.g | 1.89 | 5.2 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.43 | 1.2 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.c | 2.03 | 6.1 |
