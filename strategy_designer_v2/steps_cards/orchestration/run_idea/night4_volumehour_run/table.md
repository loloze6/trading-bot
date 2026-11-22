# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 028-01_volume-surge-up-continuation | - | plan | inconclusive (+0.14) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The tested measure is essentially zero (t 0.14 on 8827 cases, F1), the plan already used all folds for BTC and ETH, and no coin, year, horizon, forecast strength or volume level shows the effect consistently (F2–F7), so the clear answer is that volume-confirmed up-hours in BTC and ETH do not continue over the next two to six hours.; 7.d: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound, 028-01_volume-surge-up-continuation.d2_volume-surge-after-quiet-day; 7.g: 028-01_volume-surge-up-continuation.g1_evening-rebound-after-daily-fall, 028-01_volume-surge-up-continuation.g2_daily-move-reverses-next-day | 1.29 | 7.7 |
| 028-02_volume-surge-down-continuation | - | plan | inconclusive (-1.13) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong; 7.d: 028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds, 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward; 7.g: 028-02_volume-surge-down-continuation.g1_one-day-move-reverses-next-day, 028-02_volume-surge-down-continuation.g2_deep-daily-fall-rebounds | 4.86 | 21.0 |
| 028-03_low-volume-up-fade | - | plan | inconclusive (+1.21) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider, 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade; 7.d: 028-03_low-volume-up-fade.d1_high-volume-drop-rebounds, 028-03_low-volume-up-fade.d2_volume-surge-rises-continue; 7.g: 028-03_low-volume-up-fade.g1_evening-rebound-after-down-days | 1.30 | 7.3 |
| 028-04_low-volume-down-fade | - | plan | inconclusive (+1.40) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers; 7.d: 028-04_low-volume-down-fade.d1_quiet-dip-in-rising-day, 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade; 7.g: no ideas: Across the moves, volume, regime, volatility, weekday, hour, horizon and book angles I examined, no graded pattern stands out above what roughly 70 cells of chance would produce. The one cell that does (Thursday, t −3.6) is a calendar condition, not a graded situation. | 1.25 | 7.1 |
| 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong | 028-02_volume-surge-down-continuation | plan | inconclusive (+0.93) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins, 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong; 7.d: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.d1_volume-surge-within-uptrend, 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.d2_seven-day-momentum-continues-daily, 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.d3_extreme-volume-up-hour-continuation; 7.g: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.g1_one-day-moves-reverse-next-day, 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.g2_evening-utc-hours-drift-up | 1.53 | 7.5 |
| 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider | 028-03_low-volume-up-fade | plan | confirmed (+2.14) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider.d1_post-midnight-quiet-rise-fade, 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider.d2_quiet-rise-fade-no-uptrend, 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider.d3_thinner-volume-larger-fade; 7.g: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider.g1_turbulent-day-fall-rebound, 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider.g2_turbulence-scales-fall-rebounds | 1.02 | 10.0 |
| 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers | 028-04_low-volume-down-fade | plan | confirmed (+4.59) | profitable enough | unseen_2016_2017: does not hold; unseen_2026: no data | 7.g: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers.g1_late-utc-evening-rise | 0.61 | 5.9 |

## Consumption
7 ideas, 11.86 USD, 66.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.58 | 4.0 |
| step4_backtest | 0.00 | 19.0 |
| step5_verdict | 1.03 | 4.1 |
| step6_check | 0.00 | 0.5 |
| chart_files | 0.00 | 0.3 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 5.48 | 20.4 |
| step7_7.g | 2.57 | 9.0 |
| step7_7.d | 2.21 | 7.8 |
| unseen_test | 0.00 | 1.3 |
