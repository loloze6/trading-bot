# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|
| 012-01_liquidation-flush-rebound | - | plan | inconclusive (+2.11) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar, Trades per bar) | 7.b: 012-01_liquidation-flush-rebound.b1_volume-graded-rebound-after-falls, 012-01_liquidation-flush-rebound.b2_liquidation-flush-rebound-wider; 7.d: 012-01_liquidation-flush-rebound.d1_delayed-flush-rebound-days-two-three, 012-01_liquidation-flush-rebound.d2_heavy-volume-fall-rebound; 7.g: 012-01_liquidation-flush-rebound.g1_volume-graded-fall-rebound | 1.94 | 8.3 |
| 012-02_volume-burst-fall-reversal | - | plan | confirmed (+2.48) | not profitable enough (failed: Mean daily return, Calmar) | 7.d: 012-02_volume-burst-fall-reversal.d1_one-day-volume-flush-rebound, 012-02_volume-burst-fall-reversal.d2_volume-flush-in-uptrend; 7.g: 012-02_volume-burst-fall-reversal.g1_volume-burst-fall-next-day-rebound, 012-02_volume-burst-fall-reversal.g2_five-day-move-weekly-continuation, 012-02_volume-burst-fall-reversal.g3_volume-backed-five-day-continuation | 1.15 | 6.6 |
| 012-03_lower-wick-flush-recovery | - | plan | inconclusive (+0.77) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | 7.b: 012-03_lower-wick-flush-recovery.b1_lower-wick-rebound-more-coins, 012-03_lower-wick-flush-recovery.b2_flush-closing-low-next-day-rebound, 012-03_lower-wick-flush-recovery.b3_volume-burst-fall-rebound; 7.d: 012-03_lower-wick-flush-recovery.d1_close-at-low-flush-rebound, 012-03_lower-wick-flush-recovery.d2_flush-rebound-after-deep-falls, 012-03_lower-wick-flush-recovery.d3_capitulation-depth-predicts-rebound; 7.g: 012-03_lower-wick-flush-recovery.g1_volume-graded-down-day-rebound | 1.41 | 7.8 |
| 012-04_flush-depth-retracement-size | - | plan | inconclusive (-0.72) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar, Trades per bar) | 7.b: 012-04_flush-depth-retracement-size.b1_deep-sharp-fall-3-day-rebound; 7.d: 012-04_flush-depth-retracement-size.d1_deep-heavy-volume-fall-rebound, 012-04_flush-depth-retracement-size.d2_close-at-low-next-day-bounce; 7.g: 012-04_flush-depth-retracement-size.g1_heavy-volume-down-day-rebound, 012-04_flush-depth-retracement-size.g2_volume-graded-multi-day-selloff-reversal | 1.46 | 7.5 |

## Consumption
4 ideas, 5.97 USD, 30.2 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.95 | 4.6 |
| step4_backtest | 0.00 | 9.4 |
| step5_verdict | 0.57 | 2.6 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 1.53 | 4.8 |
| step7_7.b | 1.04 | 3.2 |
| step7_7.g | 1.88 | 5.5 |
