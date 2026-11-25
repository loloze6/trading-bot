# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 058-01_calm-downtrend-depth-continues | - | plan | inconclusive (+0.37) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 058-01.b1_calm-downtrend-all-coins, 058-01.b2_quiet-volume-calm-fall-continues; 7.g: 058-01.g1_thin-volume-deep-fall-continues, 058-01.g2_volume-drying-decline-continues | 0.99 | 6.6 |
| 058-02_quiet-volume-fall-continues | - | plan | inconclusive (-0.55) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 058-02.b1_quiet-calm-fall-more-coins; 7.g: 058-02.g1_choppy-agitated-deep-fall-continues | 1.04 | 7.6 |
| 058-03_heavy-volume-fall-exhausts | - | plan | inconclusive (-0.98) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The test's result is on the side the idea rules out. No coin, period, horizon or depth of fall shows the heavy-volume exhaustion clearly (F1, F3, F4, F5), and the brief's own continuation is absent too (F6), so the theme's effect is not in the data.; 7.g: 058-03.g1_calm-downtrend-weekly-continuation | 0.80 | 6.2 |
| 058-01.b1_calm-downtrend-all-coins | 058-01_calm-downtrend-depth-continues | plan | inconclusive (-0.61) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: no ideas: The theme's effect is not in the data. The test already used every coin and fold available. Within the falling-calm profile, a deeper 30-day fall is not followed by more falling at 5, 10 or 20 days (F1, F2, F6), and the continuation is no stronger there than outside it (F3). Even the brief's quiet-volume condition shows only a sign with t -0.91 (F4), and the residual changes sign by year and coin (F5).; 7.g: 058-01.b1.g1_calm-downtrend-recent-fall-continues | 1.04 | 12.5 |

## Consumption
4 ideas, 3.87 USD, 33.0 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.32 | 2.0 |
| step4_backtest | 0.00 | 18.4 |
| step5_verdict | 0.68 | 2.4 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 1.27 | 4.6 |
| step7_7.g | 1.60 | 5.4 |
