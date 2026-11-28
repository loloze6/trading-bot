# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 061-01_falling-calm-scaled-rise-fade | - | plan | no effect (-0.28) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.c: 061-01.c1_falling-calm-decline-continues, 061-01.c2_low-close-keeps-sliding | 0.84 | 7.2 |
| 064-01_falling-calm-up-day-fades | - | plan | no effect (-0.69) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 064-01.c1_feeble-bounces-fail-in-calm-declines | 0.62 | 6.5 |
| 070-01_falling-calm-run-break-fade | - | plan | no effect (-0.18) | not profitable enough (failed: Sharpe minus holding's Sharpe, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 070-01.c1_deep-run-bounce-fades, 070-01.c2_weak-bounce-gives-back | 0.66 | 6.8 |
| 086-01_down-day-volume-share-drift | - | missing-components | - | - | - | - | 0.06 | 0.3 |

## Consumption
4 ideas, 2.18 USD, 20.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.36 | 2.1 |
| step4_backtest | 0.00 | 12.2 |
| step5_verdict | 0.55 | 2.2 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.g | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.c | 1.27 | 4.1 |
