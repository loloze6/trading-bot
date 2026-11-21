# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 019-01_narrow-range-larger-move | - | untestable | - | - | - | - | 0.04 | 0.2 |
| 019-02_narrow-range-wider-span | - | untestable | - | - | - | - | 0.04 | 0.3 |
| 019-03_upward-breakout-quiet-continuation | - | plan | inconclusive (+1.28) | not profitable enough (failed: Calmar) | - | 7.b: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins, 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week; 7.d: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week, 019-03_upward-breakout-quiet-continuation.d2_breakout-with-rising-week; 7.g: 019-03_upward-breakout-quiet-continuation.g1_volatility-expansion-lifts-returns, 019-03_upward-breakout-quiet-continuation.g2_quiet-ranges-precede-weakness | 1.72 | 7.0 |
| 019-04_downward-breakout-quiet-continuation | - | plan | rejected (-4.49) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.c: no answer; 7.d: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend, 019-04_downward-breakout-quiet-continuation.d2_wide-dip-rebound-uptrend; 7.g: 019-04_downward-breakout-quiet-continuation.g1_wide-range-precedes-rise, 019-04_downward-breakout-quiet-continuation.g2_volatility-expansion-precedes-rise | 1.17 | 6.5 |
| 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins | 019-03_upward-breakout-quiet-continuation | plan | inconclusive (+1.35) | profitable enough | - | 7.b: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins, 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues; 7.e: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation, 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails; 7.g: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.g1_sharp-fall-three-day-rebound, 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.g2_failed-downside-break-rebound | 1.76 | 12.0 |

## Consumption
5 ideas, 4.73 USD, 25.9 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.77 | 2.7 |
| step4_backtest | 0.00 | 9.7 |
| step5_verdict | 0.46 | 1.8 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.10 | 0.4 |
| step7_7.e | 0.49 | 1.6 |
| step7_7.d | 0.69 | 2.3 |
| step7_7.b | 0.77 | 2.5 |
| step7_7.g | 1.44 | 4.7 |
