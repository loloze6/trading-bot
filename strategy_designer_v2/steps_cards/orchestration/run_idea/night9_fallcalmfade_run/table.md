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

## Consumption
11 ideas, 8.26 USD, 52.9 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 2.20 | 8.8 |
| step4_backtest | 0.00 | 24.1 |
| step5_verdict | 1.09 | 4.2 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 1.07 | 3.2 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 1.37 | 4.1 |
| step7_7.g | 2.53 | 8.0 |
| similarity_check | 0.00 | 0.2 |
