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

## Consumption
6 ideas, 7.61 USD, 40.2 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 3.22 | 5.3 |
| step4_backtest | 0.00 | 19.4 |
| step5_verdict | 0.81 | 2.7 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 1.59 | 5.6 |
| step7_7.g | 1.99 | 7.0 |
