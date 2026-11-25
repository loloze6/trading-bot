# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_volatile-decline-low-cascade | - | plan | not observable | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.a: 032-01.a1_volatile-decline-low-all-coins; 7.g: 032-01.g1_monthly-high-proximity-momentum, 032-01.g2_volatility-scaled-weekly-momentum | 1.09 | 6.0 |
| 032-02_volatile-decline-low-rebound | - | plan | inconclusive (+0.75) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 032-02.b1_volatile-decline-low-rebound-more-coins, 032-02.b2_volatile-low-next-day-rebound; 7.g: 032-02.g1_near-monthly-high-continuation, 032-02.g2_calm-breakout-continuation | 1.06 | 5.5 |
| 032-03_deep-fall-low-exhaustion-rebound | - | plan | inconclusive (+0.56) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 032-03.b1_deep-low-rebound-all-coins, 032-03.b2_deep-low-three-day-rebound, 032-03.b3_shallow-fall-low-breakdown; 7.g: 032-03.g1_near-monthly-high-continuation, 032-03.g2_long-lower-wick-weakness, 032-03.g3_wide-day-fall-next-day-rebound | 1.00 | 5.7 |
| 032-02.b1_volatile-decline-low-rebound-more-coins | 032-02_volatile-decline-low-rebound | plan | inconclusive (-0.21) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar, Trades per day) | - | 7.b: 032-02.b1.b1_volatile-low-one-day-rebound; 7.g: 032-02.b1.g1_twenty-day-high-breakout-continuation, 032-02.b1.g2_wide-range-breakout-continuation | 1.09 | 8.7 |
| 032-03.b1_deep-low-rebound-all-coins | 032-03_deep-fall-low-exhaustion-rebound | plan | inconclusive (+0.64) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 032-03.b1.b1_three-day-rebound-after-volatile-low, 032-03.b1.b2_capitulation-day-short-bounce; 7.g: 032-03.b1.g1_closeness-to-monthly-high | 1.07 | 9.5 |

## Consumption
5 ideas, 5.31 USD, 35.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.46 | 2.8 |
| step4_backtest | 0.00 | 16.9 |
| step5_verdict | 0.98 | 3.8 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 1.54 | 4.6 |
| step7_7.g | 1.93 | 5.8 |
| step7_7.a | 0.41 | 1.3 |
