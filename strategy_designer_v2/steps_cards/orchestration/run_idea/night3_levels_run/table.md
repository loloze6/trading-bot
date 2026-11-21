# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 020-03_resistance-breakout-continues-up | - | missing-components | - | - | - | - | 0.04 | 0.3 |
| 020-04_support-breakdown-continues-down | - | missing-components | - | - | - | - | 0.04 | 0.3 |
| 020-01_resistance-retest-turns-down | - | plan | inconclusive (-0.17) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance; 7.d: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high, 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues, 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high; 7.g: 020-01_resistance-retest-turns-down.g1_strong-up-day-keeps-rising | 1.64 | 6.4 |
| 020-02_support-retest-bounces-up | - | plan | rejected (-2.10) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling; 7.d: 020-02_support-retest-bounces-up.d1_support-bounce-in-uptrends, 020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend; 7.g: 020-02_support-retest-bounces-up.g1_saturday-rise-after-strong-week | 1.50 | 6.5 |

## Consumption
4 ideas, 3.23 USD, 13.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.69 | 2.2 |
| step4_backtest | 0.00 | 2.3 |
| step5_verdict | 0.29 | 1.2 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.c | 0.40 | 1.2 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.d | 0.81 | 2.6 |
| step7_7.b | 0.35 | 1.2 |
| step7_7.g | 0.69 | 2.5 |
