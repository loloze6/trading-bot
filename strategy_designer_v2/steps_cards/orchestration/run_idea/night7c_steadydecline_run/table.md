# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_calm-decline-depth-continues | - | plan | inconclusive (+0.35) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The tested effect is zero (F1) and no part of the data shows it clearly: depth does not grade the outcome (F3), the coins and windows contradict each other (F4), no horizon reaches t 2 (F5), and the quiet-range hint stays below t 2 and disappears when graded (F6). An amended idea would rest on noise.; 7.g: 032-01.g1_sharp-daily-fall-rebounds, 032-01.g2_high-volume-selloff-day-rebounds | 1.20 | 6.4 |
| 032-02_low-range-decline-continues-more | - | plan | inconclusive (-0.73) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The tested effect is zero rather than short of the bar: an unusual move of +0.10 % with t 0.22, and a slope t of -0.73. No coin, window, depth or horizon shows calm declines falling more in a way that holds up (F1–F6), so neither more data nor a narrowed version is supported.; 7.g: 032-02.g1_uptrend-near-high-continues, 032-02.g2_calm-uptrend-keeps-rising | 0.94 | 5.8 |
| 032-03_low-volume-decline-continues-more | - | plan | inconclusive (+0.48) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-03.b1_thin-volume-decline-more-coins, 032-03.b2_deep-calm-decline-continues; 7.g: 032-03.g1_position-in-28-day-range | 0.96 | 6.2 |
| 032-04_calm-decline-rally-sold | - | plan | mismatch | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.g: 032-04.g1_calm-uptrend-day-follow-through | 0.65 | 4.5 |
| 032-03.b1_thin-volume-decline-more-coins | 032-03_low-volume-decline-continues-more | plan | inconclusive (+1.25) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-03.b1.b1_thin-volume-decline-all-coins, 032-03.b1.b2_violent-decline-rebounds; 7.g: no ideas: Across about 60 groupings and slopes (depth of the decline, volume and range ratios over several spans, calm against panic, volatility, past returns, weekday, year), no pattern exceeded a t of about 2.6, which is what chance gives among that many looks. The one consistent shape, moderate declines continuing while deep ones do not, was chosen after seeing the data and was never tested on its own. | 1.09 | 8.9 |

## Consumption
5 ideas, 4.84 USD, 31.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.49 | 3.1 |
| step4_backtest | 0.00 | 14.0 |
| step5_verdict | 0.85 | 3.1 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.g | 1.89 | 6.0 |
| step7_7.b | 1.60 | 5.2 |
