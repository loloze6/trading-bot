# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_flat-range-upside-break-fades | - | plan | inconclusive (-1.97) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1_flat-range-upside-breaks-continue; 7.g: 032-01.g1_next-day-rebound-after-falls | 2.04 | 5.8 |
| 032-02_flat-range-downside-break-recovers | - | plan | inconclusive (-0.55) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 032-02.b1_flat-range-upside-break-continues; 7.g: 032-02.g1_top-of-range-close-continues | 1.24 | 5.8 |
| 032-01.b1_flat-range-upside-breaks-continue | 032-01_flat-range-upside-break-fades | plan | inconclusive (+1.57) | not profitable enough (failed: Calmar) | - | 7.b: 032-01.b1.b1_flat-range-breaks-more-coins, 032-01.b1.b2_tight-range-breaks-rise-fast; 7.g: 032-01.b1.g1_flat-coin-twenty-day-momentum, 032-01.b1.g2_range-position-predicts-drift, 032-01.b1.g3_one-day-move-reverses-next-day | 1.10 | 5.8 |
| 032-02.b1_flat-range-upside-break-continues | 032-02_flat-range-downside-break-recovers | plan | inconclusive (+2.17) | profitable enough | - | 7.b: 032-02.b1.b1_flat-range-upside-break-continues; 7.e: 032-02.b1.e1_quiet-breakouts-continue-longer, 032-02.b1.e2_tight-range-breakouts-continue; 7.g: 032-02.b1.g1_range-position-predicts-continuation, 032-02.b1.g2_top-of-range-keeps-rising | 1.60 | 7.1 |
| 032-02.b1.e1_quiet-breakouts-continue-longer | 032-02.b1_flat-range-upside-break-continues | plan | inconclusive (+2.00) | profitable enough | - | 7.b: 032-02.b1.e1.b1_quiet-breakouts-more-coins, 032-02.b1.e1.b2_unextended-breakouts-keep-rising; 7.e: 032-02.b1.e1.e1_tight-range-breakouts-continue, 032-02.b1.e1.e2_unextended-breakouts-keep-rising; 7.g: 032-02.b1.e1.g1_next-day-rebound-after-shocks, 032-02.b1.e1.g2_big-up-days-keep-rising | 1.55 | 7.4 |

## Consumption
5 ideas, 7.53 USD, 31.9 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.39 | 4.5 |
| step4_backtest | 0.00 | 7.9 |
| step5_verdict | 0.91 | 3.5 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.e | 0.82 | 2.5 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.g | 2.41 | 7.3 |
| step7_7.b | 2.00 | 6.0 |
