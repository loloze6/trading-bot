# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 061-01_falling-calm-scaled-rise-fade | - | plan | no effect (-1.44) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 061-01.c1_falling-calm-scaled-fall-rebound, 061-01.c2_falling-calm-rise-continuation | 0.71 | 8.3 |
| 064-01_falling-calm-up-day-fades | - | plan | no effect (+0.45) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 064-01.c1_calm-decline-big-rise-follows-through, 064-01.c2_calm-decline-bounce-extends-week | 0.56 | 7.6 |

## Consumption
2 ideas, 1.27 USD, 15.9 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.22 | 1.4 |
| step4_backtest | 0.00 | 11.1 |
| step5_verdict | 0.35 | 1.3 |
| step6_check | 0.00 | 0.0 |
| chart_files | 0.00 | 0.0 |
| step7_7.g | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.70 | 2.0 |
