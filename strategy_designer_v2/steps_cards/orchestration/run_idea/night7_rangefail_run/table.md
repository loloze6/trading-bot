# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_choppy-upside-break-fades | - | plan | inconclusive (-0.70) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: no ideas: In choppy markets, closes beyond the 20-day range do not fade in these data. They continue at every horizon from 3 days on, with no grading by overshoot and no difference from trending markets, and the few fading groups are scattered and small (F2–F5), so the theme's effect is not in the data.; 7.g: 032-01.g2_choppy-upside-breaks-continue | 0.86 | 4.7 |

## Consumption
1 ideas, 0.86 USD, 4.7 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.08 | 0.5 |
| step4_backtest | 0.00 | 1.7 |
| step5_verdict | 0.18 | 0.6 |
| step6_check | 0.00 | 0.0 |
| chart_files | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.21 | 0.6 |
| step7_7.g | 0.39 | 1.2 |
