# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 017-05_settlement-move-reverses-after | - | plan | confirmed (+5.12) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day, 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses, 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours; 7.g: 017-05_settlement-move-reverses-after.g1_one-day-large-move-reversal, 017-05_settlement-move-reverses-after.g2_reversal-in-volatility-bursts, 017-05_settlement-move-reverses-after.g3_us-open-move-reversal, 017-05_settlement-move-reverses-after.g4_intraday-move-reverses-next-day | 1.22 | 10.4 |

## Consumption
1 ideas, 1.22 USD, 10.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.08 | 0.5 |
| step4_backtest | 0.00 | 5.3 |
| step5_verdict | 0.16 | 0.6 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| similarity_check | 0.00 | 0.1 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.g | 0.42 | 1.5 |
| step7_7.d | 0.57 | 2.1 |
