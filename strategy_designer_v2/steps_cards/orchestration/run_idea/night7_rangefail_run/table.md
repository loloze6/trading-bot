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
| 033-01.b1_range-position-more-coins | 033-01_range-position-drift-follows | plan | inconclusive (+1.39) | not profitable enough (failed: Calmar) | - | 7.b: 033-01.b1.b1_range-position-calm-market, 033-01.b1.b2_range-position-three-days; 7.g: 033-01.b1.g1_upper-range-strength-keeps-rising, 033-01.b1.g2_range-position-in-rising-markets | 1.14 | 9.7 |
| 033-03.b1_upper-range-drifts-higher | 033-03_downside-break-continues-falling | plan | inconclusive (+1.53) | not profitable enough (failed: Calmar) | - | 7.b: 033-03.b1.b1_range-position-more-coins; 7.g: 033-03.b1.g1_calm-range-position-drift, 033-03.b1.g2_rising-market-range-drift | 1.10 | 5.3 |
| 033-03.b2_rising-market-range-top-continuation | 033-03_downside-break-continues-falling | plan | confirmed (+3.08) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: 033-03.b2.g1_calm-market-range-position-drift, 033-03.b2.g2_rising-range-top-long-drift | 0.64 | 5.0 |
| 033-01.b2_beyond-range-close-drift | 033-01_range-position-drift-follows | missing-components | - | - | - | - | 1.07 | 2.2 |
| 033-02.d1_upside-break-five-day-hold | 033-02_upside-break-continues-rising | plan | confirmed (+2.05) | not profitable enough (failed: Calmar) | - | 7.d: 033-02.d1.d1_rising-market-upside-break-hold, 033-02.d1.d2_narrow-range-upside-break-hold, 033-02.d1.d3_agitated-upside-break-hold; 7.g: 033-02.d1.g1_calm-range-position-drift, 033-02.d1.g2_calm-market-upside-break | 1.15 | 6.1 |
| 033-02.d2_fresh-upside-break-rises | 033-02_upside-break-continues-rising | missing-components | - | - | - | - | 0.07 | 0.4 |
| 032-02.b1.b1_choppy-downside-break-rebound | 032-02.b1_choppy-downside-break-one-day-rebound | plan | inconclusive (+1.90) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 032-02.b1.b1.b1_agitated-choppy-break-rebound, 032-02.b1.b1.b2_sharp-fall-break-one-day-rebound; 7.g: 032-02.b1.b1.g1_rising-market-breakout-continuation | 1.08 | 9.0 |

## Consumption
13 ideas, 12.62 USD, 69.0 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 2.35 | 9.6 |
| step4_backtest | 0.00 | 25.4 |
| step5_verdict | 1.90 | 6.8 |
| step6_check | 0.00 | 0.4 |
| chart_files | 0.00 | 0.2 |
| step7_7.d | 1.03 | 3.5 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 2.62 | 7.9 |
| step7_7.g | 4.73 | 14.1 |
| similarity_check | 0.00 | 0.2 |
| unseen_test | 0.00 | 0.9 |
