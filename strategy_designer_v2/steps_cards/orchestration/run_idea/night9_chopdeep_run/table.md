# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 072-01_choppy-deep-close-continuation | - | plan | inconclusive (+0.10) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 072-01.b1_choppy-deep-close-five-day; 7.g: 0 ideas, 1 discoveries (3 explorations) | 1.17 | 6.6 |
| 074-01_falling-wide-up-day-fade | - | plan | inconclusive (+1.28) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 074-01.b1_falling-wide-up-fade-more-coins; 7.g: 074-01.g1_falling-agitated-wide-up-fade | 0.90 | 6.0 |
| 074-01.b1_falling-wide-up-fade-more-coins | 074-01_falling-wide-up-day-fade | plan | inconclusive (+2.10) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 074-01.b1.b1_falling-wide-up-day-high-close-fade; 7.g: 0 ideas, 1 discoveries (3 explorations) | 1.29 | 12.8 |

## Consumption
3 ideas, 3.37 USD, 25.5 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.29 | 1.8 |
| step4_backtest | 0.00 | 13.7 |
| step5_verdict | 0.59 | 2.3 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 0.91 | 2.7 |
| step7_7.g | 1.58 | 4.7 |
