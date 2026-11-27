# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 086-01_first-down-day-streak-length | - | plan | no effect (-1.74) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-01.c1_first-dip-falls-over-week | 1.67 | 8.2 |
| 086-02_first-down-day-run-size | - | plan | no effect (-1.17) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-02.c1_first-dip-depth-continues, 086-02.c2_deep-down-day-continues; 7.g: no ideas: Across the forecast, streak length, dip size, horizons from 1 to 10 days, nine bar features, weekdays and windows, no pattern in rising agitated markets on the short side stands out from chance. The only ordering, a weaker fall after longer runs, is the opposite of the theme's effect and not significant, so the theme's effect is not in the data. | 1.16 | 8.9 |

## Consumption
2 ideas, 2.83 USD, 17.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.11 | 1.7 |
| step4_backtest | 0.00 | 10.2 |
| step5_verdict | 0.40 | 1.6 |
| step6_check | 0.00 | 0.0 |
| chart_files | 0.00 | 0.0 |
| step7_7.g | 0.45 | 1.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.c | 0.87 | 2.5 |
