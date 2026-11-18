# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|
| 012-04_flush-depth-retracement-size | - | missing-components | - | - | - | 0.05 | 0.3 |
| 012-01_liquidation-flush-rebound | - | plan | inconclusive (+2.11) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar, Trades per bar) | 7.b: 012-01_liquidation-flush-rebound.b1_volume-graded-rebound-after-falls, 012-01_liquidation-flush-rebound.b2_liquidation-flush-rebound-wider; 7.d: 012-01_liquidation-flush-rebound.d1_delayed-flush-rebound-days-two-three, 012-01_liquidation-flush-rebound.d2_heavy-volume-fall-rebound; 7.g: 012-01_liquidation-flush-rebound.g1_volume-graded-fall-rebound | 1.94 | 8.3 |
| 012-02_volume-burst-fall-reversal | - | plan | confirmed (+2.48) | not profitable enough (failed: Mean daily return, Calmar) | 7.d: 012-02_volume-burst-fall-reversal.d1_one-day-volume-flush-rebound, 012-02_volume-burst-fall-reversal.d2_volume-flush-in-uptrend; 7.g: 012-02_volume-burst-fall-reversal.g1_volume-burst-fall-next-day-rebound, 012-02_volume-burst-fall-reversal.g2_five-day-move-weekly-continuation, 012-02_volume-burst-fall-reversal.g3_volume-backed-five-day-continuation | 1.15 | 6.6 |
| 012-03_lower-wick-flush-recovery | - | plan | inconclusive (+0.77) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | 7.b: 012-03_lower-wick-flush-recovery.b1_lower-wick-rebound-more-coins, 012-03_lower-wick-flush-recovery.b2_flush-closing-low-next-day-rebound, 012-03_lower-wick-flush-recovery.b3_volume-burst-fall-rebound; 7.d: 012-03_lower-wick-flush-recovery.d1_close-at-low-flush-rebound, 012-03_lower-wick-flush-recovery.d2_flush-rebound-after-deep-falls, 012-03_lower-wick-flush-recovery.d3_capitulation-depth-predicts-rebound; 7.g: 012-03_lower-wick-flush-recovery.g1_volume-graded-down-day-rebound | 1.41 | 7.8 |

## Consumption
4 ideas, 4.55 USD, 23.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.86 | 3.9 |
| step4_backtest | 0.00 | 7.0 |
| step5_verdict | 0.43 | 1.9 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 1.04 | 3.4 |
| step7_7.b | 0.69 | 2.1 |
| step7_7.g | 1.54 | 4.5 |
