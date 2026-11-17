# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|
| 012-01_liquidation-flush-rebound | - | missing-components | - | - | - | 0.28 | 0.3 |
| 012-02_volume-burst-fall-reversal | - | plan | inconclusive (+1.59) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | 7.b: 012-02_volume-burst-fall-reversal.b1_volume-flush-next-day-rebound, 012-02_volume-burst-fall-reversal.b2_volume-burst-fall-reversal-broadened; 7.d: 012-02_volume-burst-fall-reversal.d1_one-day-volume-burst-rebound, 012-02_volume-burst-fall-reversal.d2_close-at-low-next-day-rebound, 012-02_volume-burst-fall-reversal.d3_volume-burst-dip-in-uptrend; 7.g: 012-02_volume-burst-fall-reversal.g1_heavy-volume-down-day-rebound, 012-02_volume-burst-fall-reversal.g2_calm-market-volume-flush-rebound | 1.45 | 6.1 |
| 012-03_lower-wick-flush-recovery | - | missing-components | - | - | - | 0.04 | 0.3 |
| 012-04_flush-depth-retracement-size | - | missing-components | - | - | - | 0.04 | 0.3 |
| 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g2_rising-volume-precedes-gains | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month | missing-components | - | - | - | 0.04 | 0.3 |
| 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends | plan | inconclusive (+1.96) | not profitable enough (failed: Calmar) | 7.b: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.b1_volume-surge-more-coins, 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.b2_heavy-volume-on-up-days, 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.b3_direction-signed-volume-surge; 7.d: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.d1_volume-surge-in-uptrends, 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.d2_volume-surge-on-up-days, 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.d3_volume-surge-near-high; 7.g: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.g1_volatility-scaled-daily-move-continues, 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.g2_thin-volume-precedes-weakness | 1.18 | 5.4 |
| 013-04_heavy-volume-below-high-breakout | - | missing-components | - | - | - | 0.06 | 0.4 |
| 013-06_breakout-volume-drives-continuation | - | plan | inconclusive (+1.66) | not profitable enough (failed: Mean daily return, Calmar) | 7.b: 013-06_breakout-volume-drives-continuation.b1_breakout-volume-more-coins; 7.d: 013-06_breakout-volume-drives-continuation.d1_high-volume-breakout-late-follow-through, 013-06_breakout-volume-drives-continuation.d2_extreme-volume-breakout-continuation; 7.g: 013-06_breakout-volume-drives-continuation.g1_heavy-volume-selloff-next-day-rebound, 013-06_breakout-volume-drives-continuation.g2_volatility-scaled-fall-reverses | 1.03 | 8.1 |
| 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week | plan | confirmed (+4.17) | not profitable enough (failed: Mean daily return, Calmar) | 7.d: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume.d1_near-high-volume-in-uptrends, 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume.d2_near-high-is-long-only; 7.g: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume.g1_next-day-rebound-after-selloffs, 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume.g2_close-in-range-predicts-week, 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume.g3_strong-day-on-volume-continues | 0.91 | 4.7 |
| 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side | plan | confirmed (+2.75) | profitable enough | 7.g: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through.g1_range-expansion-precedes-gains, 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through.g2_weekly-return-momentum-continues | 0.53 | 3.4 |

## Consumption
10 ideas, 5.57 USD, 29.2 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.83 | 4.1 |
| step4_backtest | 0.00 | 8.9 |
| step5_verdict | 0.63 | 3.1 |
| step6_check | 0.00 | 0.2 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.83 | 2.7 |
| step7_7.d | 1.33 | 4.4 |
| step7_7.g | 1.95 | 5.9 |
