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

## Consumption
6 ideas, 6.78 USD, 57.6 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.61 | 3.9 |
| step4_backtest | 0.00 | 34.3 |
| step5_verdict | 1.16 | 4.4 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 1.94 | 5.7 |
| step7_7.g | 3.07 | 8.8 |
