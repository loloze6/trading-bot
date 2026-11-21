# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 020-04_support-breakdown-continues-down | - | missing-components | - | - | - | - | 0.04 | 0.3 |
| 020-01_resistance-retest-turns-down | - | plan | inconclusive (-0.17) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance; 7.d: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high, 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues, 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high; 7.g: 020-01_resistance-retest-turns-down.g1_strong-up-day-keeps-rising | 1.64 | 6.4 |
| 020-02_support-retest-bounces-up | - | plan | rejected (-2.10) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling; 7.d: 020-02_support-retest-bounces-up.d1_support-bounce-in-uptrends, 020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend; 7.g: 020-02_support-retest-bounces-up.g1_saturday-rise-after-strong-week | 1.50 | 6.5 |
| 020-03_resistance-breakout-continues-up | - | plan | inconclusive (+1.20) | not profitable enough (failed: Calmar) | - | 7.b: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins, 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run; 7.d: 020-03_resistance-breakout-continues-up.d1_held-breakout-keeps-rising, 020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend; 7.g: 020-03_resistance-breakout-continues-up.g1_sharp-daily-fall-rebounds, 020-03_resistance-breakout-continues-up.g2_sharp-fall-near-highs-rebounds | 1.38 | 6.6 |

## Consumption
4 ideas, 4.57 USD, 19.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.77 | 2.8 |
| step4_backtest | 0.00 | 3.7 |
| step5_verdict | 0.43 | 1.8 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.c | 0.40 | 1.3 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.d | 1.20 | 4.0 |
| step7_7.b | 0.70 | 2.3 |
| step7_7.g | 1.07 | 3.8 |
