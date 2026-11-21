# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 021-01_above-rising-cloud-continues-up | - | plan | inconclusive (+1.30) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | - | 7.b: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins; 7.d: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues, 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades; 7.g: 021-01_above-rising-cloud-continues-up.g1_one-day-rebound-after-falls, 021-01_above-rising-cloud-continues-up.g2_week-long-continuation-after-surges | 1.73 | 6.4 |
| 021-02_below-falling-cloud-continues-down | - | plan | inconclusive (+0.69) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues; 7.d: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud, 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud, 021-02_below-falling-cloud-continues-down.d3_fast-cloud-fall-rebounds; 7.g: 021-02_below-falling-cloud-continues-down.g1_range-position-predicts-week, 021-02_below-falling-cloud-continues-down.g2_sharp-daily-drops-rebound, 021-02_below-falling-cloud-continues-down.g3_monthly-momentum-continues | 1.60 | 6.9 |
| 021-03_thin-cloud-upward-breakout | - | missing-components | - | - | - | - | 0.12 | 0.9 |
| 021-04_thin-cloud-downward-breakdown | - | missing-components | - | - | - | - | 0.19 | 1.4 |
| 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins | 021-01_above-rising-cloud-continues-up | plan | inconclusive (+1.75) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | - | 7.b: no ideas: The above-rising-cloud effect comes from a few large 2021 moves in small, volatile coins (F1, F3, F4), not from a steady pattern. It is not graded by the cloud's slope (F2), its trimmed t is 0.99, and its strength is about a third of a real idea's (F5). No condition, side or horizon in this data isolates a graded effect, and no more data is available (F6), so the clear answer is that a coin trading above a rising cloud does not reliably keep rising beyond its usual drift.; 7.d: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins.d1_lasting-stay-above-cloud, 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins.d2_off-cloud-fallers-keep-lagging; 7.g: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins.g1_26-day-momentum-continues-26-days, 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins.g2_scaled-momentum-over-ten-days | 1.67 | 11.2 |

## Consumption
5 ideas, 5.30 USD, 26.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.99 | 4.3 |
| step4_backtest | 0.00 | 8.0 |
| step5_verdict | 0.47 | 1.8 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 1.18 | 3.5 |
| step7_7.g | 1.23 | 4.0 |
| step7_7.d | 1.43 | 4.9 |
