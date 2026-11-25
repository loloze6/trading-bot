# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_calm-fall-depth-continues | - | plan | inconclusive (+1.43) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1_calm-fall-continuation-all-coins; 7.g: 0 ideas, 3 discoveries (2 explorations) | 0.87 | 5.5 |
| 033-01_close-near-low-rebounds | - | plan | confirmed (+2.64) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.d: 033-01.d1_wide-day-low-close-rebound, 033-01.d2_low-close-rebound-long-side; 7.g: 033-01.g1_wide-day-low-close-rebound, 033-01.g2_agitated-close-near-low-rebound | 1.03 | 5.7 |
| 034-01_agitated-low-close-rebounds | - | plan | confirmed (+2.95) | not profitable enough (failed: Mean daily return, on days in a position, Calmar) | - | 7.d: 034-01.d1_wide-range-low-close-rebound, 034-01.d2_falling-agitated-low-close-rebound; 7.g: 034-01.g1_wide-day-close-location-reversal, 034-01.g2_falling-agitated-low-close-rebound | 1.05 | 6.0 |
| 035-01_wide-low-close-rebounds | - | plan | confirmed (+3.27) | not profitable enough (failed: Calmar) | - | 7.d: 035-01.d1_agitated-wide-day-low-close-rebound, 035-01.d2_unusual-wide-day-low-close-rebound; 7.g: 035-01.g1_wide-low-close-three-day-rebound, 035-01.g3_extreme-wide-low-close-rebound | 1.07 | 5.8 |
| 036-01_fall-vs-swing-next-day-rebound | - | plan | inconclusive (+2.75) | not profitable enough (failed: Calmar) | - | 7.b: 036-01.b1_outsized-fall-rebound-all-coins; 7.g: 036-01.g1_raw-fall-depth-next-day-rebound, 036-01.g2_agitated-market-fall-rebound | 1.01 | 5.2 |
| 032-02_calm-fall-below-high-continues | - | plan | inconclusive (+1.22) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 032-02.b1_calm-fall-depth-more-coins; 7.g: 032-02.g1_calm-decline-fourteen-day-continuation | 0.87 | 5.3 |
| 038-01_agitated-fall-next-day-rebound | - | plan | confirmed (+2.77) | profitable enough | unseen_2016_2017: holds; unseen_2026: does not hold | 7.g: 038-01.g1_agitated-big-falls-rebound | 0.83 | 6.5 |
| 033-02_close-near-high-gives-back | - | plan | confirmed (-2.61) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 033-02.d1_high-close-fades-in-selloffs, 033-02.d2_high-close-fades-after-declines, 033-02.d3_wide-day-high-close-gives-back; 7.g: 033-02.g1_wide-low-close-rebounds, 033-02.g2_agitated-wide-low-close, 033-02.g3_low-close-two-day-rebound | 1.01 | 5.8 |
| 034-02_agitated-high-close-gives-back | - | plan | inconclusive (+1.02) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 034-02.b1_agitated-high-close-all-coins; 7.g: 034-02.g1_falling-agitated-low-close-rebound, 034-02.g2_deep-fall-low-close-rebounds | 1.15 | 6.9 |
| 037-01_wide-day-fall-next-day-rebound | - | plan | confirmed (+2.37) | not profitable enough (failed: Calmar) | - | 7.d: 037-01.d1_wide-falls-rebound-when-agitated, 037-01.d2_only-extreme-wide-falls-rebound, 037-01.d3_wide-fall-after-multi-day-decline; 7.g: 037-01.g1_wide-fall-rebound-agitated, 037-01.g2_wide-fall-low-close | 1.89 | 6.7 |
| 039-01_agitated-swing-fall-low-close-rebound | - | plan | confirmed (+3.86) | not profitable enough (failed: Calmar) | - | 7.d: 039-01.d1_falling-agitated-forced-selling-rebound, 039-01.d2_multi-day-slide-low-close-rebound; 7.g: 039-01.g1_extreme-agitated-fall-rebound, 039-01.g2_agitated-low-close-two-day-rebound | 1.03 | 6.3 |

## Consumption
11 ideas, 11.82 USD, 65.7 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.70 | 5.4 |
| step4_backtest | 0.00 | 23.7 |
| step5_verdict | 1.85 | 6.9 |
| step6_check | 0.00 | 0.5 |
| chart_files | 0.00 | 0.2 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 2.34 | 8.2 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 1.23 | 4.0 |
| step7_7.g | 4.71 | 15.0 |
| similarity_check | 0.00 | 0.5 |
| unseen_test | 0.00 | 1.2 |
