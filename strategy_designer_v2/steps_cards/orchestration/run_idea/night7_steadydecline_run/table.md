# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_calm-fall-depth-continues | - | plan | inconclusive (+1.43) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1_calm-fall-continuation-all-coins; 7.g: 0 ideas, 3 discoveries (2 explorations) | 0.87 | 5.5 |
| 033-01_close-near-low-rebounds | - | plan | confirmed (+2.64) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.d: 033-01.d1_wide-day-low-close-rebound, 033-01.d2_low-close-rebound-long-side; 7.g: 033-01.g1_wide-day-low-close-rebound, 033-01.g2_agitated-close-near-low-rebound | 1.03 | 5.7 |
| 034-01_agitated-low-close-rebounds | - | plan | confirmed (+2.95) | not profitable enough (failed: Mean daily return, on days in a position, Calmar) | - | 7.d: 034-01.d1_wide-range-low-close-rebound, 034-01.d2_falling-agitated-low-close-rebound; 7.g: 034-01.g1_wide-day-close-location-reversal, 034-01.g2_falling-agitated-low-close-rebound | 1.05 | 6.0 |
| 035-01_wide-low-close-rebounds | - | plan | confirmed (+3.27) | not profitable enough (failed: Calmar) | - | 7.d: 035-01.d1_agitated-wide-day-low-close-rebound, 035-01.d2_unusual-wide-day-low-close-rebound; 7.g: 035-01.g1_wide-low-close-three-day-rebound, 035-01.g3_extreme-wide-low-close-rebound | 1.07 | 5.8 |
| 036-01_fall-vs-swing-next-day-rebound | - | plan | inconclusive (+2.75) | not profitable enough (failed: Calmar) | - | 7.b: 036-01.b1_outsized-fall-rebound-all-coins; 7.g: 036-01.g1_raw-fall-depth-next-day-rebound, 036-01.g2_agitated-market-fall-rebound | 1.01 | 5.2 |
| 037-01_wide-day-fall-next-day-rebound | - | missing-components | - | - | - | - | 0.09 | 0.6 |
| 032-02_calm-fall-below-high-continues | - | plan | inconclusive (+1.22) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 032-02.b1_calm-fall-depth-more-coins; 7.g: 032-02.g1_calm-decline-fourteen-day-continuation | 0.87 | 5.3 |

## Consumption
7 ideas, 5.99 USD, 34.0 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.52 | 2.9 |
| step4_backtest | 0.00 | 12.4 |
| step5_verdict | 1.01 | 3.7 |
| step6_check | 0.00 | 0.3 |
| chart_files | 0.00 | 0.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 1.17 | 4.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.77 | 2.5 |
| step7_7.g | 2.52 | 8.0 |
| similarity_check | 0.00 | 0.2 |
