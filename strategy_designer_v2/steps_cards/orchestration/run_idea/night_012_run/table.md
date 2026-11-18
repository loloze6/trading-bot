# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|
| 012-02_volume-burst-fall-reversal | - | missing-components | - | - | - | 0.04 | 0.3 |
| 012-03_lower-wick-flush-recovery | - | missing-components | - | - | - | 0.09 | 0.6 |
| 012-04_flush-depth-retracement-size | - | missing-components | - | - | - | 0.05 | 0.3 |
| 012-01_liquidation-flush-rebound | - | plan | inconclusive (+2.11) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar, Trades per bar) | 7.b: 012-01_liquidation-flush-rebound.b1_volume-graded-rebound-after-falls, 012-01_liquidation-flush-rebound.b2_liquidation-flush-rebound-wider; 7.d: 012-01_liquidation-flush-rebound.d1_delayed-flush-rebound-days-two-three, 012-01_liquidation-flush-rebound.d2_heavy-volume-fall-rebound; 7.g: 012-01_liquidation-flush-rebound.g1_volume-graded-fall-rebound | 1.94 | 8.3 |

## Consumption
4 ideas, 2.12 USD, 9.5 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.70 | 2.8 |
| step4_backtest | 0.00 | 2.6 |
| step5_verdict | 0.16 | 0.7 |
| step6_check | 0.00 | 0.0 |
| chart_files | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.35 | 1.0 |
| step7_7.b | 0.37 | 1.0 |
| step7_7.g | 0.55 | 1.4 |
