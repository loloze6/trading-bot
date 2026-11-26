# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 064-01_choppy-large-up-day-continuation | - | plan | inconclusive (-0.20) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: no ideas: The theme's effect is not in the data. The test's result is zero (strength -0.024, t -0.20), and no horizon, jump size, coin, period or agitation level shows the continuation clearly (best t 1.14 on 44 cases). Neither more data nor a narrower idea is warranted (F1–F5).; 7.g: no ideas: Across the forecast, the close position, the trend, the agitation, the weekday, the grid offsets and the down side, nothing beat chance robustly. The one pattern above t 2 on overlapping days is large up-day continuation in rising markets (F5), and the profile map already holds it in rising calm and rising agitated. | 1.09 | 12.0 |
| 067-01_choppy-strong-month-rise-continues | - | plan | inconclusive (+0.86) | not profitable enough (failed: Calmar) | - | 7.b: 067-01.b1_choppy-weak-month-keeps-falling; 7.g: 067-01.g1_choppy-month-fall-continues, 067-01.g2_calm-chop-scaled-fall-continues | 1.01 | 10.9 |
| 067-01.b1_choppy-weak-month-keeps-falling | 067-01_choppy-strong-month-rise-continues | plan | confirmed (+2.08) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 067-01.b1.d1_agitated-chop-weak-month-falls; 7.g: 067-01.b1.g1_choppy-agitated-month-fall-continues | 1.22 | 12.0 |
| 067-01.b1.d1_agitated-chop-weak-month-falls | 067-01.b1_choppy-weak-month-keeps-falling | plan | inconclusive (+1.09) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The fall after a weak month in a choppy, agitated market appears only in one crash window (w16) and reverses without it (F2, F3). No horizon, depth of fall or period shows it in a graded way (F4, F5), and no more data exists to retest it (F1), so the theme's effect is not in the data.; 7.g: 067-01.b1.d1.g1_daily-close-height-week-continuation | 0.98 | 11.8 |
| 067-01.b1.g1_choppy-agitated-month-fall-continues | 067-01.b1_choppy-weak-month-keeps-falling | plan | inconclusive (+1.09) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 067-01.b1.g1.b1_choppy-month-fall-continues, 067-01.b1.g1.b2_choppy-calm-fall-continues; 7.g: 067-01.b1.g1.g1_choppy-calm-month-continuation, 067-01.b1.g1.g2_choppy-month-fall-continues | 1.05 | 11.6 |

## Consumption
5 ideas, 5.34 USD, 58.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.40 | 2.0 |
| step4_backtest | 0.00 | 40.8 |
| step5_verdict | 0.93 | 3.1 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.d | 0.52 | 1.5 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 1.26 | 4.0 |
| step7_7.g | 2.23 | 6.4 |
| similarity_check | 0.00 | 0.1 |
