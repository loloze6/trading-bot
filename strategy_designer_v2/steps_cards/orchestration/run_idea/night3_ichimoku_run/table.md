# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 021-01_above-rising-cloud-continues-up | - | plan | inconclusive (+1.30) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | - | 7.b: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins; 7.d: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues, 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades; 7.g: 021-01_above-rising-cloud-continues-up.g1_one-day-rebound-after-falls, 021-01_above-rising-cloud-continues-up.g2_week-long-continuation-after-surges | 1.73 | 6.4 |
| 021-02_below-falling-cloud-continues-down | - | plan | inconclusive (+0.69) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues; 7.d: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud, 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud, 021-02_below-falling-cloud-continues-down.d3_fast-cloud-fall-rebounds; 7.g: 021-02_below-falling-cloud-continues-down.g1_range-position-predicts-week, 021-02_below-falling-cloud-continues-down.g2_sharp-daily-drops-rebound, 021-02_below-falling-cloud-continues-down.g3_monthly-momentum-continues | 1.60 | 6.9 |
| 021-03_thin-cloud-upward-breakout | - | missing-components | - | - | - | - | 0.12 | 0.9 |
| 021-04_thin-cloud-downward-breakdown | - | missing-components | - | - | - | - | 0.19 | 1.4 |
| 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins | 021-01_above-rising-cloud-continues-up | plan | inconclusive (+1.75) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | - | 7.b: no ideas: The above-rising-cloud effect comes from a few large 2021 moves in small, volatile coins (F1, F3, F4), not from a steady pattern. It is not graded by the cloud's slope (F2), its trimmed t is 0.99, and its strength is about a third of a real idea's (F5). No condition, side or horizon in this data isolates a graded effect, and no more data is available (F6), so the clear answer is that a coin trading above a rising cloud does not reliably keep rising beyond its usual drift.; 7.d: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins.d1_lasting-stay-above-cloud, 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins.d2_off-cloud-fallers-keep-lagging; 7.g: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins.g1_26-day-momentum-continues-26-days, 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins.g2_scaled-momentum-over-ten-days | 1.67 | 11.2 |
| 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues | 021-02_below-falling-cloud-continues-down | missing-components | - | - | - | - | 0.09 | 0.7 |
| 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues | 021-01_above-rising-cloud-continues-up | plan | inconclusive (-1.26) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | - | 7.b: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise; 7.d: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.d1_above-cloud-stretched-above-average, 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.d2_above-thin-cloud-continues, 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.d3_26-day-momentum-continues; 7.g: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.g1_sharp-daily-fall-rebounds-next-day, 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.g2_last-week-s-move-continues-monthly | 4.65 | 20.7 |
| 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise | 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues | missing-components | - | - | - | - | 0.07 | 0.6 |

## Consumption
8 ideas, 10.12 USD, 48.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.24 | 6.2 |
| step4_backtest | 0.00 | 10.1 |
| step5_verdict | 0.64 | 2.6 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 1.54 | 4.8 |
| step7_7.g | 1.63 | 5.4 |
| step7_7.d | 5.07 | 19.5 |
