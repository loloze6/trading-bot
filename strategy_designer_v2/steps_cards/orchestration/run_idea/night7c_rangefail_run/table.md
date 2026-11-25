# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_flat-range-upside-break-fades | - | plan | inconclusive (-1.97) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1_flat-range-upside-breaks-continue; 7.g: 032-01.g1_next-day-rebound-after-falls | 2.04 | 5.8 |
| 032-02_flat-range-downside-break-recovers | - | plan | inconclusive (-0.55) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 032-02.b1_flat-range-upside-break-continues; 7.g: 032-02.g1_top-of-range-close-continues | 1.24 | 5.8 |
| 032-01.b1_flat-range-upside-breaks-continue | 032-01_flat-range-upside-break-fades | plan | inconclusive (+1.57) | not profitable enough (failed: Calmar) | - | 7.b: 032-01.b1.b1_flat-range-breaks-more-coins, 032-01.b1.b2_tight-range-breaks-rise-fast; 7.g: 032-01.b1.g1_flat-coin-twenty-day-momentum, 032-01.b1.g2_range-position-predicts-drift, 032-01.b1.g3_one-day-move-reverses-next-day | 1.10 | 5.8 |
| 032-02.b1_flat-range-upside-break-continues | 032-02_flat-range-downside-break-recovers | plan | inconclusive (+2.17) | profitable enough | - | 7.b: 032-02.b1.b1_flat-range-upside-break-continues; 7.e: 032-02.b1.e1_quiet-breakouts-continue-longer, 032-02.b1.e2_tight-range-breakouts-continue; 7.g: 032-02.b1.g1_range-position-predicts-continuation, 032-02.b1.g2_top-of-range-keeps-rising | 1.60 | 7.1 |
| 032-02.b1.e1_quiet-breakouts-continue-longer | 032-02.b1_flat-range-upside-break-continues | plan | inconclusive (+2.00) | profitable enough | - | 7.b: 032-02.b1.e1.b1_quiet-breakouts-more-coins, 032-02.b1.e1.b2_unextended-breakouts-keep-rising; 7.e: 032-02.b1.e1.e1_tight-range-breakouts-continue, 032-02.b1.e1.e2_unextended-breakouts-keep-rising; 7.g: 032-02.b1.e1.g1_next-day-rebound-after-shocks, 032-02.b1.e1.g2_big-up-days-keep-rising | 1.55 | 7.4 |
| 032-02.b1.e2_tight-range-breakouts-continue | 032-02.b1_flat-range-upside-break-continues | plan | confirmed (+2.59) | not profitable enough (failed: Calmar) | - | 7.d: 032-02.b1.e2.d1_raw-tightness-graded-breakouts, 032-02.b1.e2.d2_tight-breakouts-held-longer, 032-02.b1.e2.d3_failed-breakouts-give-nothing; 7.g: 032-02.b1.e2.g1_choppy-coin-twenty-day-momentum | 1.19 | 6.1 |
| 032-01.b1.b1_flat-range-breaks-more-coins | 032-01.b1_flat-range-upside-breaks-continue | plan | inconclusive (+2.53) | profitable enough | - | 7.b: 032-01.b1.b1.b1_compressed-range-breakouts-continue, 032-01.b1.b1.b2_tight-range-breaks-ten-days; 7.e: 032-01.b1.b1.e1_tight-range-breakout-ten-days, 032-01.b1.b1.e2_small-breaks-follow-through; 7.g: 032-01.b1.b1.g1_20-day-range-position-continues, 032-01.b1.b1.g2_flat-range-top-continues-briefly | 1.59 | 11.2 |
| 032-01.b1.b1.e1_tight-range-breakout-ten-days | 032-01.b1.b1_flat-range-breaks-more-coins | plan | confirmed (+3.42) | not profitable enough (failed: Calmar) | - | 7.d: 032-01.b1.b1.e1.d1_narrow-range-breakout-continuation, 032-01.b1.b1.e1.d2_breakout-held-above-level; 7.g: 032-01.b1.b1.e1.g1_tight-range-downside-break-continues | 1.36 | 10.3 |
| 032-02.b1.e1.e1_tight-range-breakouts-continue | 032-02.b1.e1_quiet-breakouts-continue-longer | plan | inconclusive (-0.57) | profitable enough | - | 7.b: 032-02.b1.e1.e1.b1_absolute-tight-range-breakouts-continue, 032-02.b1.e1.e1.b2_quiet-approach-breakouts-continue; 7.e: 032-02.b1.e1.e1.e1_tight-range-breaks-rise-faster, 032-02.b1.e1.e1.e2_compressed-ranges-precede-rises, 032-02.b1.e1.e1.e3_two-month-momentum-continues; 7.g: 032-02.b1.e1.e1.g1_nearness-to-high-momentum, 032-02.b1.e1.e1.g2_two-month-high-proximity-drift | 2.18 | 6.9 |
| 032-01.b1.b1.e2_small-breaks-follow-through | 032-01.b1.b1_flat-range-breaks-more-coins | missing-components | - | - | - | - | 0.09 | 0.6 |
| 032-02.b1.e1.e2_unextended-breakouts-keep-rising | 032-02.b1.e1_quiet-breakouts-continue-longer | plan | inconclusive (-0.53) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar, Trades per day) | - | 7.b: 032-02.b1.e1.e2.b1_narrow-clear-breakouts-keep-rising; 7.g: 032-02.b1.e1.e2.g1_top-of-range-closes-keep-rising, 032-02.b1.e1.e2.g2_nearness-to-high-predicts-gains | 1.15 | 6.1 |

## Consumption
11 ideas, 15.09 USD, 73.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 2.99 | 10.6 |
| step4_backtest | 0.00 | 23.6 |
| step5_verdict | 1.87 | 7.2 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.d | 0.91 | 3.0 |
| step7_7.e | 1.61 | 5.1 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.g | 4.59 | 13.7 |
| step7_7.b | 3.12 | 9.6 |
| similarity_check | 0.00 | 0.1 |
