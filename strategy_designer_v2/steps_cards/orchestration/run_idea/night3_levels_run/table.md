# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 020-01_resistance-retest-turns-down | - | plan | inconclusive (-0.17) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance; 7.d: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high, 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues, 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high; 7.g: 020-01_resistance-retest-turns-down.g1_strong-up-day-keeps-rising | 1.64 | 6.4 |
| 020-02_support-retest-bounces-up | - | plan | rejected (-2.10) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling; 7.d: 020-02_support-retest-bounces-up.d1_support-bounce-in-uptrends, 020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend; 7.g: 020-02_support-retest-bounces-up.g1_saturday-rise-after-strong-week | 1.50 | 6.5 |
| 020-03_resistance-breakout-continues-up | - | plan | inconclusive (+1.20) | not profitable enough (failed: Calmar) | - | 7.b: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins, 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run; 7.d: 020-03_resistance-breakout-continues-up.d1_held-breakout-keeps-rising, 020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend; 7.g: 020-03_resistance-breakout-continues-up.g1_sharp-daily-fall-rebounds, 020-03_resistance-breakout-continues-up.g2_sharp-fall-near-highs-rebounds | 1.38 | 6.6 |
| 020-04_support-breakdown-continues-down | - | plan | inconclusive (+0.73) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The small fall after a support break is the coins' own downtrend: an ordinary bar below the 50-day average falls about as much (difference t 0.56). The break has no grading of its own (rho 0.003, larger half below smaller), so a rerun on more coins would stay inconclusive. Even if confirmed, its 0.20 % per case only matches a 0.19 % trade cost and its total move is negative, so no amended version is supported.; 7.d: 020-04_support-breakdown-continues-down.d1_support-break-after-mild-decline, 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds; 7.g: 020-04_support-breakdown-continues-down.g1_deep-support-break-rebounds | 1.29 | 6.4 |
| 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance | 020-01_resistance-retest-turns-down | plan | inconclusive (+0.62) | not profitable enough (failed: Calmar) | - | 7.b: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins; 7.d: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d1_resistance-break-with-rising-trend, 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d2_resistance-break-near-highs, 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend; 7.g: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.g1_one-day-rebound-after-shocks | 1.43 | 6.9 |
| 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling | 020-02_support-retest-bounces-up | plan | inconclusive (+0.53) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins, 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall; 7.d: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend, 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows; 7.g: no ideas: After about 40 comparisons, nothing beyond the forecast's own weak echo of the known near-highs drift (F1, F2) is clearly more than chance: high-volatility momentum (F4) rests on one half of the windows and one coin, and the weekday gap (F5) is unstable across years and is not a graded situation. | 1.27 | 5.9 |

## Consumption
6 ideas, 8.51 USD, 38.7 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.98 | 4.4 |
| step4_backtest | 0.00 | 7.7 |
| step5_verdict | 0.86 | 3.5 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.c | 0.40 | 1.3 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.d | 2.26 | 7.7 |
| step7_7.b | 1.82 | 6.0 |
| step7_7.g | 2.19 | 7.8 |
