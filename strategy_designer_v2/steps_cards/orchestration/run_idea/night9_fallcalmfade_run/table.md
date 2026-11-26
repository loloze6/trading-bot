# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 070-01_calm-decline-run-break-fade | - | plan | inconclusive (+0.98) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 070-01.b1_calm-decline-fade-more-coins; 7.g: 070-01.g1_calm-decline-long-run-break | 1.14 | 8.0 |
| 070-01.b1_calm-decline-fade-more-coins | 070-01_calm-decline-run-break-fade | plan | inconclusive (+0.24) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 070-01.b1.b1_calm-decline-depth-fade; 7.g: 070-01.b1.g1_calm-decline-depth-fade, 070-01.b1.g2_falling-market-depth-fade | 1.17 | 13.9 |
| 070-01.b1.b1_calm-decline-depth-fade | 070-01.b1_calm-decline-fade-more-coins | missing-components | - | - | - | - | 0.07 | 0.4 |
| 074-01_falling-market-run-break-fade | - | plan | inconclusive (+3.54) | not profitable enough (failed: Calmar) | - | 7.b: 074-01.b1_falling-deep-run-break-fade; 7.g: 074-01.g1_falling-agitated-scaled-run-break-fade | 1.04 | 6.5 |
| 070-01.g1_calm-decline-long-run-break | 070-01_calm-decline-run-break-fade | missing-components | - | - | - | - | 0.09 | 0.6 |
| 074-01.g1_falling-agitated-scaled-run-break-fade | 074-01_falling-market-run-break-fade | missing-components | - | - | - | - | 0.07 | 0.4 |
| 064-01_calm-decline-big-rise-fades | - | plan | inconclusive (-1.42) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: no ideas: The fade the theme claims is not in the data: large scaled rises in falling calm markets were followed by a rise, not a fall (-2.25 % short-direction, t -1.42, 62 cases). The giveback does not grow with the rise's size (correlation +0.038, or -0.245 on the forecast). The opposite move is too unstable across sampling, coins and years (F2, F3) to support an idea on another side.; 7.g: 064-01.g1_calm-decline-up-day-fade | 1.02 | 7.4 |
| 070-01.b1.g1_calm-decline-depth-fade | 070-01.b1_calm-decline-fade-more-coins | missing-components | - | - | - | - | 0.15 | 0.9 |
| 070-01.b1.g2_falling-market-depth-fade | 070-01.b1_calm-decline-fade-more-coins | missing-components | - | - | - | - | 0.07 | 0.4 |
| 074-01.b1_falling-deep-run-break-fade | 074-01_falling-market-run-break-fade | plan | confirmed (+3.54) | not profitable enough (failed: Calmar) | - | 7.d: 074-01.b1.d1_run-break-fade-widening-swing, 074-01.b1.d2_run-break-fade-steep-slide, 074-01.b1.d3_agitated-falling-run-break-fade; 7.g: 074-01.b1.g1_convex-deep-run-fade, 074-01.b1.g2_calm-downtrend-relief-fade | 2.01 | 7.0 |
| 074-01.b1.d1_run-break-fade-widening-swing | 074-01.b1_falling-deep-run-break-fade | plan | confirmed (+2.88) | not profitable enough (failed: Calmar) | - | 7.d: 074-01.b1.d1.d1_run-break-fade-after-sharp-leg, 074-01.b1.d1.d2_depth-graded-run-break-fade; 7.g: 074-01.b1.d1.g1_falling-market-rally-break-rebound | 1.42 | 7.6 |
| 074-01.b1.d2_run-break-fade-steep-slide | 074-01.b1_falling-deep-run-break-fade | plan | confirmed (+3.54) | profitable enough | unseen_2016_2017: does not hold; unseen_2026: does not hold | 7.g: 074-01.b1.d2.g1_up-run-break-dip-rebound | 0.98 | 6.9 |
| 074-01.b1.d3_agitated-falling-run-break-fade | 074-01.b1_falling-deep-run-break-fade | plan | confirmed (+2.84) | not profitable enough (failed: Calmar) | - | 7.d: 074-01.b1.d3.d1_deep-run-break-fade-falling, 074-01.b1.d3.d2_agitated-deep-run-fade; 7.g: 074-01.b1.d3.g1_calm-falling-run-break-fade, 074-01.b1.d3.g2_falling-run-depth-two-day-fade | 1.50 | 8.2 |
| 074-01.b1.d1.d1_run-break-fade-after-sharp-leg | 074-01.b1.d1_run-break-fade-widening-swing | plan | confirmed (+3.57) | profitable enough | unseen_2016_2017: holds; unseen_2026: does not hold | 7.g: 074-01.b1.d1.d1.g1_falling-market-dip-relief-fade | 0.78 | 6.4 |
| 074-01.b1.d1.d2_depth-graded-run-break-fade | 074-01.b1.d1_run-break-fade-widening-swing | plan | confirmed (+3.54) | not profitable enough (failed: Calmar) | - | 7.d: 074-01.b1.d1.d2.d1_five-day-fall-graded-relief-fade; 7.g: 074-01.b1.d1.d2.g1_heavy-volume-relief-fade | 1.10 | 6.6 |
| 074-01.b1.g1_convex-deep-run-fade | 074-01.b1_falling-deep-run-break-fade | plan | confirmed (+4.26) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: no ideas: Every pattern that stands out repeats the tested idea (F1 to F4, already in the map as 074-01.b1.g1, falling short) or long rebounds the map already holds (F6). What remains is an ungraded weekday split (F5) or choppy-market fades too weak to tell from chance (F7), after looking at run length, depth, up-day size, close position, agitation, trend, weekday, window and large moves. | 0.80 | 6.7 |

## Consumption
16 ideas, 13.44 USD, 87.7 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 2.81 | 12.6 |
| step4_backtest | 0.00 | 37.3 |
| step5_verdict | 1.95 | 7.5 |
| step6_check | 0.00 | 0.3 |
| chart_files | 0.00 | 0.2 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 2.07 | 6.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 1.37 | 4.1 |
| step7_7.g | 5.25 | 15.3 |
| similarity_check | 0.00 | 0.6 |
| unseen_test | 0.00 | 3.7 |
