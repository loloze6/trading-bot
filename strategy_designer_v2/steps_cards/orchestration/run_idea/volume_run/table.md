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

## Consumption
7 ideas, 3.10 USD, 13.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.61 | 2.6 |
| step4_backtest | 0.00 | 2.4 |
| step5_verdict | 0.25 | 1.1 |
| step6_check | 0.00 | 0.1 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.64 | 2.0 |
| step7_7.d | 0.71 | 2.3 |
| step7_7.g | 0.89 | 2.6 |
