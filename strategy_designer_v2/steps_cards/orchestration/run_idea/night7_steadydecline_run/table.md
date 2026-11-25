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
| 038-02_agitated-fall-vs-swing-rebound | - | plan | confirmed (+4.80) | profitable enough | unseen_2016_2017: holds; unseen_2026: does not hold | 7.g: 038-02.g1_agitated-outsized-fall-rebounds, 038-02.g2_agitated-fall-three-day-rebound | 0.66 | 6.0 |
| 033-01.d1_wide-day-low-close-rebound | 033-01_close-near-low-rebounds | plan | confirmed (+3.36) | not profitable enough (failed: Calmar) | - | 7.d: 033-01.d1.d1_strong-low-close-rebound-only, 033-01.d1.d2_agitated-wide-day-low-close-rebound, 033-01.d1.d3_wide-day-high-close-next-day-fade; 7.g: 033-01.d1.g1_falling-agitated-low-close-rebound | 1.07 | 5.8 |
| 033-01.d2_low-close-rebound-long-side | 033-01_close-near-low-rebounds | plan | confirmed (+2.07) | not profitable enough (failed: Mean daily return, on days in a position, Calmar) | - | 7.d: 033-01.d2.d1_wide-range-low-close-rebound, 033-01.d2.d2_wide-range-low-close-two-day-rebound, 033-01.d2.d3_agitated-decline-low-close-rebound; 7.g: 033-01.d2.g1_give-back-below-high-rebounds, 033-01.d2.g2_agitated-low-close-rebound, 033-01.d2.g3_falling-market-low-close-rebound | 1.10 | 5.8 |
| 040-01_agitated-fall-size-next-day-rebound | - | plan | confirmed (+3.76) | not profitable enough (failed: Calmar) | - | 7.d: 040-01.d1_falling-agitated-fall-rebound; 7.g: 040-01.g1_falling-agitated-fall-rebound, 040-01.g2_heavy-volume-fall-next-day-rebound | 1.22 | 6.5 |
| 035-02_swing-wide-low-close-rebounds | - | plan | confirmed (+3.20) | not profitable enough (failed: Calmar) | - | 7.d: 035-02.d1_strong-flush-only-rebound, 035-02.d2_flush-in-recent-advance, 035-02.d3_sudden-flush-after-up-week; 7.g: 035-02.g1_agitated-wide-low-close-rebound, 035-02.g2_absolute-high-to-close-drop-rebound | 2.04 | 6.6 |
| 036-02_fall-vs-range-next-day-rebound | - | plan | inconclusive (+1.93) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 036-02.b1_outsized-fall-rebound-more-coins; 7.g: 036-02.g1_outsized-fall-weak-close, 036-02.g2_outsized-fall-after-decline, 036-02.g3_agitated-outsized-fall-rebound | 0.96 | 6.0 |
| 037-02_fall-range-beyond-loss-rebound | - | plan | confirmed (+3.30) | not profitable enough (failed: Calmar) | - | 7.d: 037-02.d1_wide-fall-rebound-outside-chop, 037-02.d2_falling-agitated-sweep-rebound, 037-02.d3_sweep-after-slide-rebounds; 7.g: 037-02.g1_forced-fall-rebound-when-agitated, 037-02.g2_deep-fall-wide-relative-range, 037-02.g3_deep-fall-closing-at-low | 1.19 | 7.8 |
| 039-02_agitated-range-fall-low-close-rebound | - | plan | confirmed (+2.76) | profitable enough | unseen_2016_2017: holds; unseen_2026: does not hold | 7.g: 039-02.g1_agitated-at-low-close-rebound, 039-02.g2_calm-market-short-momentum | 1.52 | 7.7 |
| 040-02_agitated-fall-vs-swing-rebound | - | plan | confirmed (+3.18) | not profitable enough (failed: Calmar) | - | 7.d: 040-02.d1_agitated-fall-after-weekly-decline, 040-02.d2_two-day-rebound-after-selling, 040-02.d3_largest-scaled-falls-rebound, 040-02.d4_falling-agitated-fall-rebound; 7.g: 040-02.g1_agitated-heavy-volume-fall-rebound, 040-02.g2_heavy-volume-fall-three-day-rebound | 1.08 | 7.0 |
| 034-01.d1_wide-range-low-close-rebound | 034-01_agitated-low-close-rebounds | plan | confirmed (+3.69) | profitable enough | unseen_2016_2017: does not hold; unseen_2026: does not hold | 7.g: 034-01.d1.g1_ordinary-rise-high-close-fade, 034-01.d1.g2_agitated-sharp-fall-low-close-rebound | 0.65 | 6.4 |

## Consumption
21 ideas, 23.30 USD, 131.3 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 4.37 | 12.6 |
| step4_backtest | 0.00 | 46.0 |
| step5_verdict | 3.45 | 12.7 |
| step6_check | 0.00 | 1.0 |
| chart_files | 0.00 | 0.4 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 4.90 | 17.6 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 1.45 | 4.8 |
| step7_7.g | 9.13 | 30.0 |
| similarity_check | 0.00 | 1.2 |
| unseen_test | 0.00 | 4.9 |
