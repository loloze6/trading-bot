# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 058-01_calm-range-top-drifts-down | - | missing-components | - | - | - | - | 1.82 | 1.7 |
| 058-02_calm-range-bottom-drifts-up | - | plan | inconclusive (-0.34) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-02.b1_calm-range-bottom-keeps-falling, 058-02.b2_calm-range-position-continues; 7.g: 058-02.g1_calm-range-bottom-keeps-falling | 2.01 | 8.4 |
| 058-02.b1_calm-range-bottom-keeps-falling | 058-02_calm-range-bottom-drifts-up | plan | inconclusive (-0.68) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-02.b1.b1_calm-range-position-continues, 058-02.b1.b2_choppy-range-position-continues; 7.g: 058-02.b1.g1_falling-market-rally-fades | 0.97 | 6.6 |
| 058-02.b2_calm-range-position-continues | 058-02_calm-range-bottom-drifts-up | plan | inconclusive (+0.73) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 058-02.b2.b1_calm-range-continuation-more-coins; 7.g: no ideas: Every pattern that stands out after this many angles repeats an idea the map already holds. Calm range-position continuation is 035-01.b1, range-top continuation everywhere is 034-01.b1 and 033-03.b2, falling-agitated rebound is already held 12 times, and the late-week gain is 045-01. What remains (the Wednesday dip, the 20-day-return shape) does not survive a day-clustered or graded reading. | 0.84 | 6.3 |
| 058-02.b2.b1_calm-range-continuation-more-coins | 058-02.b2_calm-range-position-continues | plan | inconclusive (+0.87) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: no ideas: The effect is not stronger where the idea places it (F4), it appears in one year only (F2), on neither side consistently (F3), it is not graded by nearness to the edge (F5) and it is not clearer at another horizon (F6), so no condition, side or horizon would give a clear answer, and the test already used all the data available (F7).; 7.g: 058-02.b2.b1.g1_choppy-range-position-continuation | 1.01 | 11.5 |
| 058-02.b1.b2_choppy-range-position-continues | 058-02.b1_calm-range-bottom-keeps-falling | plan | inconclusive (+0.87) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-02.b1.b2.b1_choppy-range-position-more-coins; 7.g: 058-02.b1.b2.g2_choppy-calm-range-position-continues | 0.95 | 5.8 |
| 058-02.b1.b2.b1_choppy-range-position-more-coins | 058-02.b1.b2_choppy-range-position-continues | plan | inconclusive (+0.79) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 058-02.b1.b2.b1.b1_choppy-calm-range-position, 058-02.b1.b2.b1.b2_calm-market-range-position; 7.g: 058-02.b1.b2.b1.g1_choppy-calm-range-position-continuation, 058-02.b1.b2.b1.g2_falling-calm-range-low-continuation | 1.08 | 11.4 |
| 058-02.b1.b2.b1.b2_calm-market-range-position | 058-02.b1.b2.b1_choppy-range-position-more-coins | plan | inconclusive (+1.70) | profitable enough | - | 7.b: 058-02.b1.b2.b1.b2.b1_calm-rising-range-position, 058-02.b1.b2.b1.b2.b2_calm-range-edge-continuation; 7.e: 058-02.b1.b2.b1.b2.e1_choppy-calm-range-continuation, 058-02.b1.b2.b1.b2.e2_calm-nearness-to-high-short-horizon; 7.g: 058-02.b1.b2.b1.b2.g1_falling-calm-range-low-continuation, 058-02.b1.b2.b1.b2.g2_quietness-scaled-range-continuation | 1.29 | 12.9 |
| 058-02.b1.b2.b1.b2.e2_calm-nearness-to-high-short-horizon | 058-02.b1.b2.b1.b2_calm-market-range-position | plan | confirmed (+3.96) | not profitable enough (failed: Calmar) | - | 7.d: 058-02.b1.b2.b1.b2.e2.d1_rising-calm-near-high-continuation, 058-02.b1.b2.b1.b2.e2.d2_falling-calm-far-from-high-decline; 7.g: 058-02.b1.b2.b1.b2.e2.g1_choppy-calm-high-continuation, 058-02.b1.b2.b1.b2.e2.g2_falling-calm-low-continuation | 1.29 | 12.5 |

## Consumption
9 ideas, 11.27 USD, 77.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 3.42 | 6.3 |
| step4_backtest | 0.00 | 43.6 |
| step5_verdict | 1.37 | 4.6 |
| step6_check | 0.00 | 0.3 |
| chart_files | 0.00 | 0.1 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.40 | 1.3 |
| step7_7.d | 0.61 | 2.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 2.23 | 7.8 |
| step7_7.g | 3.24 | 10.9 |
| similarity_check | 0.00 | 0.1 |
