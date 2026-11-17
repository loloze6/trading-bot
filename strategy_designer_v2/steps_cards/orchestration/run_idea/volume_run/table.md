# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|
| 012-01_liquidation-flush-rebound | - | missing-components | - | - | - | 0.28 | 0.3 |
| 012-02_volume-burst-fall-reversal | - | plan | inconclusive (+1.59) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | 7.b: 012-02_volume-burst-fall-reversal.b1_volume-flush-next-day-rebound, 012-02_volume-burst-fall-reversal.b2_volume-burst-fall-reversal-broadened; 7.d: 012-02_volume-burst-fall-reversal.d1_one-day-volume-burst-rebound, 012-02_volume-burst-fall-reversal.d2_close-at-low-next-day-rebound, 012-02_volume-burst-fall-reversal.d3_volume-burst-dip-in-uptrend; 7.g: 012-02_volume-burst-fall-reversal.g1_heavy-volume-down-day-rebound, 012-02_volume-burst-fall-reversal.g2_calm-market-volume-flush-rebound | 1.45 | 6.1 |

## Consumption
2 ideas, 1.74 USD, 6.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.37 | 0.9 |
| step4_backtest | 0.00 | 1.3 |
| step5_verdict | 0.14 | 0.7 |
| step6_check | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.33 | 0.9 |
| step7_7.d | 0.35 | 1.1 |
| step7_7.g | 0.55 | 1.5 |
