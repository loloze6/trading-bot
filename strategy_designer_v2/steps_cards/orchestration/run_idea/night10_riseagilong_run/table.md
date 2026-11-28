# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 086-01_first-up-after-long-down-run | - | plan | no effect (-0.16) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.c: 086-01.c1_forceful-turn-day-continues, 086-01.c2_shallow-pullback-turn-continues | 0.77 | 6.8 |
| 086-02_first-up-after-deep-down-run | - | plan | no effect (-0.16) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.c: 086-02.c1_forceful-break-day-continues; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.21 | 7.9 |

## Consumption
2 ideas, 1.98 USD, 14.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.26 | 1.8 |
| step4_backtest | 0.00 | 7.6 |
| step5_verdict | 0.40 | 1.6 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.g | 0.49 | 1.2 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 0.00 | 0.0 |
| step7_7.c | 0.84 | 2.5 |
