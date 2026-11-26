# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 058-01_agitated-decline-rally-giveback | - | plan | inconclusive (+0.49) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-01.b1_rally-giveback-all-coins; 7.g: 058-01.g2_agitated-decline-one-day-rise-fades | 1.14 | 6.9 |
| 058-01.b1_rally-giveback-all-coins | 058-01_agitated-decline-rally-giveback | plan | inconclusive (+1.74) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-01.b1.b1_rally-giveback-over-fifteen-days; 7.g: no ideas: Across the 10 angles examined (scaled rises over 3, 5 and 10 days, range, close location, weekday, trend and agitation profiles, years, coins, trades), no pattern stood out beyond what that many looks produce by chance. The best ones are a borderline momentum outside the profile (t about 2, F3, F4) and a weekday effect that is overstated and already held (F5). The brief's graded give-back is absent inside its profile (F1). | 1.03 | 11.6 |
| 058-01.b1.b1_rally-giveback-over-fifteen-days | 058-01.b1_rally-giveback-all-coins | plan | inconclusive (+1.21) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-01.b1.b1.b1_rally-giveback-over-twenty-days, 058-01.b1.b1.b2_large-rallies-fail-within-week; 7.g: 058-01.b1.b1.g1_rally-giveback-over-three-days | 1.00 | 11.7 |
| 058-01.g2_agitated-decline-one-day-rise-fades | 058-01_agitated-decline-rally-giveback | plan | inconclusive (+0.73) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-01.g2.b1_one-day-rise-fades-wider; 7.g: 058-01.g2.g1_agitated-decline-upper-wick-fade | 1.20 | 7.1 |
| 058-01.g2.b1_one-day-rise-fades-wider | 058-01.g2_agitated-decline-one-day-rise-fades | plan | confirmed (-4.09) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 058-01.g2.b1.d1_raw-sized-one-day-rise-fade, 058-01.g2.b1.d2_deep-decline-one-day-rise-fade, 058-01.g2.b1.d3_one-day-rise-fades-over-5-days; 7.g: 058-01.g2.b1.g1_three-day-rise-fades-falling | 1.12 | 12.1 |
| 058-01.g2.b1.d1_raw-sized-one-day-rise-fade | 058-01.g2.b1_one-day-rise-fades-wider | plan | inconclusive (+0.97) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The result is on the predicted side but small (F1), and no more data is available. The grading the idea claims shows only weakly on raw swings at the 3-day horizon (slope t 1.92, rises above one swing t 1.51 on 24 days; F3). It reverses at 1 and 2 days (F4) and is not concentrated in any coin, window or year (F5). No part of the data shows the effect clearly enough for an amended idea to give a clear answer.; 7.g: 0 ideas, 2 discoveries (2 explorations) | 1.06 | 11.7 |
| 058-01.g2.b1.d2_deep-decline-one-day-rise-fade | 058-01.g2.b1_one-day-rise-fades-wider | plan | inconclusive (+1.34) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-01.g2.b1.d2.b1_next-day-fade-of-rises, 058-01.g2.b1.d2.b2_multi-day-rally-give-back; 7.g: 0 ideas, 1 discoveries (3 explorations) | 1.30 | 12.6 |
| 058-01.g2.b1.d3_one-day-rise-fades-over-5-days | 058-01.g2.b1_one-day-rise-fades-wider | plan | inconclusive (+1.16) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-01.g2.b1.d3.b1_one-day-rise-fades-next-day, 058-01.g2.b1.d3.b2_large-one-day-rises-fade; 7.g: 0 ideas, 2 discoveries (3 explorations) | 1.26 | 12.1 |
| 058-01.g2.b1.g1_three-day-rise-fades-falling | 058-01.g2.b1_one-day-rise-fades-wider | plan | inconclusive (+1.46) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The test already used every coin and fold available on daily bars. In the visible folds the give-back is neither graded with the rise's size (the largest rises keep rising over 5 days, t -2.03) nor present on any coin, period or horizon with t of 2 or more on a usable number of cases, so the theme's effect is not in the data.; 7.g: 058-01.g2.b1.g1.g1_extreme-rally-fade-falling-agitated | 1.09 | 11.9 |
| 058-01.b1.b1.b1_rally-giveback-over-twenty-days | 058-01.b1.b1_rally-giveback-over-fifteen-days | plan | inconclusive (-2.92) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The give-back after rallies in falling, agitated markets points the predicted way but rests on one window (w18) and is not graded at any horizon (F2–F4). No more daily data exists to sharpen it (F6), and no condition, side or horizon isolates it clearly, so no amended idea on the theme is worth testing.; 7.g: 058-01.b1.b1.b1.g1_rally-giveback-within-five-days | 4.29 | 25.6 |

## Consumption
10 ideas, 14.49 USD, 123.3 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.76 | 4.6 |
| step4_backtest | 0.00 | 71.0 |
| step5_verdict | 1.92 | 7.0 |
| step6_check | 0.00 | 0.4 |
| chart_files | 0.00 | 0.2 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.d | 0.45 | 1.4 |
| step7_7.b | 6.53 | 23.7 |
| step7_7.g | 4.82 | 15.0 |
| similarity_check | 0.00 | 0.1 |
