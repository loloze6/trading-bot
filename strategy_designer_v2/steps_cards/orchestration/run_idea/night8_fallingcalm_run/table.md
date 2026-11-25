# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 058-01_calm-downtrend-depth-continues | - | plan | inconclusive (+0.37) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 058-01.b1_calm-downtrend-all-coins, 058-01.b2_quiet-volume-calm-fall-continues; 7.g: 058-01.g1_thin-volume-deep-fall-continues, 058-01.g2_volume-drying-decline-continues | 0.99 | 6.6 |
| 058-02_quiet-volume-fall-continues | - | plan | inconclusive (-0.55) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 058-02.b1_quiet-calm-fall-more-coins; 7.g: 058-02.g1_choppy-agitated-deep-fall-continues | 1.04 | 7.6 |
| 058-03_heavy-volume-fall-exhausts | - | plan | inconclusive (-0.98) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The test's result is on the side the idea rules out. No coin, period, horizon or depth of fall shows the heavy-volume exhaustion clearly (F1, F3, F4, F5), and the brief's own continuation is absent too (F6), so the theme's effect is not in the data.; 7.g: 058-03.g1_calm-downtrend-weekly-continuation | 0.80 | 6.2 |

## Consumption
3 ideas, 2.83 USD, 20.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.25 | 1.6 |
| step4_backtest | 0.00 | 9.5 |
| step5_verdict | 0.49 | 1.8 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 0.91 | 3.4 |
| step7_7.g | 1.19 | 4.0 |
