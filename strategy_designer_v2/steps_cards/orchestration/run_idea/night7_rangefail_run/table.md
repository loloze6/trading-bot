# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_choppy-upside-break-fades | - | plan | inconclusive (-0.70) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: no ideas: In choppy markets, closes beyond the 20-day range do not fade in these data. They continue at every horizon from 3 days on, with no grading by overshoot and no difference from trending markets, and the few fading groups are scattered and small (F2–F5), so the theme's effect is not in the data.; 7.g: 032-01.g2_choppy-upside-breaks-continue | 0.86 | 4.7 |
| 033-01_range-position-drift-follows | - | plan | inconclusive (+3.17) | not profitable enough (failed: Calmar) | - | 7.b: 033-01.b1_range-position-more-coins, 033-01.b2_beyond-range-close-drift; 7.g: 033-01.g1_calm-range-position-drift | 1.02 | 5.2 |
| 032-02_choppy-downside-break-rebounds | - | plan | inconclusive (-1.27) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 032-02.b1_choppy-downside-break-one-day-rebound; 7.g: 032-02.g1_flat-base-upside-breaks-continue, 032-02.g2_tight-range-breakouts-run-further | 1.24 | 5.4 |
| 033-02_upside-break-continues-rising | - | plan | confirmed (+2.05) | not profitable enough (failed: Calmar) | - | 7.d: 033-02.d1_upside-break-five-day-hold, 033-02.d2_fresh-upside-break-rises; 7.g: 033-02.g1_upside-break-ten-day-rise, 033-02.g2_calm-market-range-drift, 033-02.g3_agitated-downside-break-continues | 1.32 | 6.3 |
| 033-03_downside-break-continues-falling | - | plan | inconclusive (+0.67) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 033-03.b1_upper-range-drifts-higher, 033-03.b2_rising-market-range-top-continuation; 7.g: 033-03.g1_calm-range-position-drift, 033-03.g2_calm-upside-break-continues | 1.06 | 5.2 |
| 032-02.b1_choppy-downside-break-one-day-rebound | 032-02_choppy-downside-break-rebounds | plan | inconclusive (+1.98) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar, Trades per day) | - | 7.b: 032-02.b1.b1_choppy-downside-break-rebound; 7.g: 032-02.b1.g1_downside-range-break-rebounds, 032-02.b1.g2_agitated-downside-break-rebound | 0.87 | 4.6 |

## Consumption
6 ideas, 6.37 USD, 31.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.57 | 3.4 |
| step4_backtest | 0.00 | 9.5 |
| step5_verdict | 1.01 | 3.6 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.d | 0.59 | 1.9 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 1.50 | 4.7 |
| step7_7.g | 2.70 | 7.9 |
| similarity_check | 0.00 | 0.1 |
