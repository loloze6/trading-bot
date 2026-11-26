# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 072-01_choppy-deep-close-continuation | - | plan | inconclusive (+0.10) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 072-01.b1_choppy-deep-close-five-day; 7.g: 0 ideas, 1 discoveries (3 explorations) | 1.17 | 6.6 |
| 074-01_falling-wide-up-day-fade | - | plan | inconclusive (+1.28) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 074-01.b1_falling-wide-up-fade-more-coins; 7.g: 074-01.g1_falling-agitated-wide-up-fade | 0.90 | 6.0 |
| 074-01.b1_falling-wide-up-fade-more-coins | 074-01_falling-wide-up-day-fade | plan | inconclusive (+2.10) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 074-01.b1.b1_falling-wide-up-day-high-close-fade; 7.g: 0 ideas, 1 discoveries (3 explorations) | 1.29 | 12.8 |
| 074-01.b1.b1_falling-wide-up-day-high-close-fade | 074-01.b1_falling-wide-up-fade-more-coins | plan | inconclusive (+1.37) | not profitable enough (failed: Sharpe minus holding's Sharpe, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 074-01.b1.b1.b1_falling-widest-up-day-fade, 074-01.b1.b1.b2_agitated-downtrend-wide-day-fade; 7.g: 074-01.b1.b1.g1_falling-wide-up-day-width-fade | 1.24 | 13.5 |
| 072-01.b1_choppy-deep-close-five-day | 072-01_choppy-deep-close-continuation | plan | inconclusive (+1.08) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 072-01.b1.b1_choppy-deep-close-more-coins; 7.g: 072-01.b1.g1_choppy-convex-deep-close-fall, 072-01.b1.g2_choppy-agitated-deep-close-fall | 0.82 | 5.4 |
| 074-01.b1.b1.b1_falling-widest-up-day-fade | 074-01.b1.b1_falling-wide-up-day-high-close-fade | plan | inconclusive (+1.18) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 074-01.b1.b1.b1.b1_falling-wide-high-close-fade; 7.g: 074-01.b1.b1.b1.g1_falling-wide-high-close-fade | 1.36 | 13.3 |
| 074-01.b1.b1.b2_agitated-downtrend-wide-day-fade | 074-01.b1.b1_falling-wide-up-day-high-close-fade | plan | inconclusive (+1.97) | not profitable enough (failed: Calmar) | - | 7.b: 074-01.b1.b1.b2.b1_agitated-downtrend-range-multiple-fade; 7.g: no ideas: The tested fade shows its sign only in falling agitated markets (F1, F4) and has no width grading (F2). The only strong graded pattern, the wide-down-day rebound in falling agitated markets (F5), is already held by many proven strategies in that cell. The other angles (weekday, choppy agitated up days, close position) did not stand out beyond chance after testing this many angles (F6). | 1.33 | 15.9 |
| 074-01.g1_falling-agitated-wide-up-fade | 074-01_falling-wide-up-day-fade | plan | confirmed (+3.12) | not profitable enough (failed: Calmar) | - | 7.d: 074-01.g1.d1_wide-close-high-bounce-fade; 7.g: 074-01.g1.g1_falling-wide-up-day-fade, 074-01.g1.g2_recent-fall-wide-bounce-fade | 1.17 | 8.2 |
| 074-01.g1.d1_wide-close-high-bounce-fade | 074-01.g1_falling-agitated-wide-up-fade | plan | confirmed (+3.32) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: no ideas: The only patterns that stand out are the tested fade itself (F1–F3) and the falling agitated down-day rebound (F5), which the profile map already holds 16 times; the second-day give-back (F4, t 2.23) does not stand out after this many angles, and weekdays (F6) show nothing. | 0.77 | 8.3 |

## Consumption
9 ideas, 10.06 USD, 90.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.96 | 6.2 |
| step4_backtest | 0.00 | 53.4 |
| step5_verdict | 1.72 | 6.6 |
| step6_check | 0.00 | 0.3 |
| chart_files | 0.00 | 0.2 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.42 | 1.4 |
| step7_7.b | 2.35 | 6.9 |
| step7_7.g | 4.61 | 13.3 |
| similarity_check | 0.00 | 0.2 |
| unseen_test | 0.00 | 1.6 |
