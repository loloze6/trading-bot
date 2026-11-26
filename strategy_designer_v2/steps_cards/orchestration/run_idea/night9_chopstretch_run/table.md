# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 067-01_choppy-up-stretch-keeps-rising | - | plan | inconclusive (+0.73) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 067-01.b1_choppy-down-stretch-keeps-falling; 7.g: 0 ideas, 2 discoveries (2 explorations) | 1.18 | 6.5 |
| 067-01.b1_choppy-down-stretch-keeps-falling | 067-01_choppy-up-stretch-keeps-rising | plan | inconclusive (-0.56) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 067-01.b1.b1_choppy-stretch-carries-both-ways; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.05 | 6.5 |
| 067-01.b1.b1_choppy-stretch-carries-both-ways | 067-01.b1_choppy-down-stretch-keeps-falling | plan | inconclusive (+0.91) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 067-01.b1.b1.b1_choppy-downside-stretch-keeps-falling, 067-01.b1.b1.b2_choppy-stretch-carry-all-coins; 7.g: 067-01.b1.b1.g1_choppy-downside-stretch-keeps-falling | 1.01 | 6.2 |
| 074-01_agitated-stretch-below-rebounds | - | plan | inconclusive (+1.03) | not profitable enough (failed: Calmar) | - | 7.b: 074-01.b1_agitated-stretch-all-coins; 7.g: 0 ideas, 2 discoveries (2 explorations) | 0.84 | 6.6 |

## Consumption
4 ideas, 4.09 USD, 25.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.27 | 1.3 |
| step4_backtest | 0.00 | 12.0 |
| step5_verdict | 0.69 | 2.5 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 1.41 | 4.4 |
| step7_7.g | 1.72 | 5.4 |
