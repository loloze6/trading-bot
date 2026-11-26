# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 070-01_calm-decline-run-break-fade | - | plan | inconclusive (+0.98) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 070-01.b1_calm-decline-fade-more-coins; 7.g: 070-01.g1_calm-decline-long-run-break | 1.14 | 8.0 |
| 070-01.b1_calm-decline-fade-more-coins | 070-01_calm-decline-run-break-fade | plan | inconclusive (+0.24) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 070-01.b1.b1_calm-decline-depth-fade; 7.g: 070-01.b1.g1_calm-decline-depth-fade, 070-01.b1.g2_falling-market-depth-fade | 1.17 | 13.9 |
| 070-01.b1.b1_calm-decline-depth-fade | 070-01.b1_calm-decline-fade-more-coins | missing-components | - | - | - | - | 0.07 | 0.4 |
| 074-01_falling-market-run-break-fade | - | plan | inconclusive (+3.54) | not profitable enough (failed: Calmar) | - | 7.b: 074-01.b1_falling-deep-run-break-fade; 7.g: 074-01.g1_falling-agitated-scaled-run-break-fade | 1.04 | 6.5 |
| 074-01.b1_falling-deep-run-break-fade | 074-01_falling-market-run-break-fade | missing-components | - | - | - | - | 0.08 | 0.5 |
| 070-01.g1_calm-decline-long-run-break | 070-01_calm-decline-run-break-fade | missing-components | - | - | - | - | 0.09 | 0.6 |
| 074-01.g1_falling-agitated-scaled-run-break-fade | 074-01_falling-market-run-break-fade | missing-components | - | - | - | - | 0.07 | 0.4 |

## Consumption
7 ideas, 3.67 USD, 30.2 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.79 | 5.1 |
| step4_backtest | 0.00 | 15.8 |
| step5_verdict | 0.57 | 2.1 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 1.01 | 2.9 |
| step7_7.g | 1.31 | 4.2 |
