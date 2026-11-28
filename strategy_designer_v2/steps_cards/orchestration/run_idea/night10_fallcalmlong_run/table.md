# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 086-01_heavy-volume-up-day-continuation | - | plan | no effect (+0.42) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-01.c1_heavy-volume-off-low-absorption, 086-01.c2_heavy-up-day-extends-rebound | 0.74 | 6.6 |
| 050-02_falling-calm-scaled-week-rise-continuation | - | plan | inconclusive (+1.89) | not profitable enough (failed: Calmar) | - | 7.b: 050-02.b1_calm-downtrend-week-rise-more-coins, 050-02.b2_calm-downtrend-week-rise-five-days | 0.68 | 5.8 |

## Consumption
2 ideas, 1.41 USD, 12.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.17 | 0.9 |
| step4_backtest | 0.00 | 7.5 |
| step5_verdict | 0.39 | 1.6 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.g | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 0.41 | 1.0 |
| step7_7.c | 0.44 | 1.3 |
