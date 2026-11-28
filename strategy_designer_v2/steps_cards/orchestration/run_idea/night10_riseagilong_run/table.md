# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 086-01_first-up-after-long-down-run | - | plan | no effect (-0.16) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.c: 086-01.c1_forceful-turn-day-continues, 086-01.c2_shallow-pullback-turn-continues | 0.77 | 6.8 |
| 086-02_first-up-after-deep-down-run | - | plan | no effect (-0.16) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.c: 086-02.c1_forceful-break-day-continues; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.21 | 7.9 |
| 087-01_agitated-rise-scaled-burst-continues | - | plan | inconclusive (+1.36) | not profitable enough (failed: Sharpe minus holding's Sharpe, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 087-01.b1_scaled-burst-continues-more-coins; 7.g: 087-01.g1_raw-swing-unit-push-continuation | 0.92 | 7.2 |

## Consumption
3 ideas, 2.90 USD, 21.9 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.37 | 2.4 |
| step4_backtest | 0.00 | 11.3 |
| step5_verdict | 0.58 | 2.3 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.g | 0.90 | 2.6 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 0.22 | 0.7 |
| step7_7.c | 0.84 | 2.5 |
