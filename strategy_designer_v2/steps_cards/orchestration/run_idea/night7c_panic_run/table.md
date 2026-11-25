# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_volatile-decline-low-cascade | - | plan | not observable | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.a: 032-01.a1_volatile-decline-low-all-coins; 7.g: 032-01.g1_monthly-high-proximity-momentum, 032-01.g2_volatility-scaled-weekly-momentum | 1.09 | 6.0 |
| 032-02_volatile-decline-low-rebound | - | plan | inconclusive (+0.75) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 032-02.b1_volatile-decline-low-rebound-more-coins, 032-02.b2_volatile-low-next-day-rebound; 7.g: 032-02.g1_near-monthly-high-continuation, 032-02.g2_calm-breakout-continuation | 1.06 | 5.5 |
| 032-03_deep-fall-low-exhaustion-rebound | - | plan | inconclusive (+0.56) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 032-03.b1_deep-low-rebound-all-coins, 032-03.b2_deep-low-three-day-rebound, 032-03.b3_shallow-fall-low-breakdown; 7.g: 032-03.g1_near-monthly-high-continuation, 032-03.g2_long-lower-wick-weakness, 032-03.g3_wide-day-fall-next-day-rebound | 1.00 | 5.7 |
| 032-02.b1_volatile-decline-low-rebound-more-coins | 032-02_volatile-decline-low-rebound | plan | inconclusive (-0.21) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar, Trades per day) | - | 7.b: 032-02.b1.b1_volatile-low-one-day-rebound; 7.g: 032-02.b1.g1_twenty-day-high-breakout-continuation, 032-02.b1.g2_wide-range-breakout-continuation | 1.09 | 8.7 |
| 032-03.b1_deep-low-rebound-all-coins | 032-03_deep-fall-low-exhaustion-rebound | plan | inconclusive (+0.64) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 032-03.b1.b1_three-day-rebound-after-volatile-low, 032-03.b1.b2_capitulation-day-short-bounce; 7.g: 032-03.b1.g1_closeness-to-monthly-high | 1.07 | 9.5 |
| 032-02.b2_volatile-low-next-day-rebound | 032-02_volatile-decline-low-rebound | plan | confirmed (+2.13) | not profitable enough (failed: Trades per day) | - | 7.d: 032-02.b2.d1_volatile-ten-day-low-rebound, 032-02.b2.d2_graded-monthly-low-rebound, 032-02.b2.d3_falling-coin-short-low-bounce; 7.g: 032-02.b2.g1_close-location-next-day-reversal, 032-02.b2.g2_volatile-close-near-low-rebound, 032-02.b2.g3_stretched-breakout-next-day-fade, 032-02.b2.g4_volatile-big-drop-next-day-rebound | 1.19 | 6.3 |
| 032-02.b2.d3_falling-coin-short-low-bounce | 032-02.b2_volatile-low-next-day-rebound | plan | inconclusive (+1.18) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 032-02.b2.d3.b1_falling-coin-low-bounce-all-coins; 7.g: 032-02.b2.d3.g1_volatile-decline-one-day-reversal, 032-02.b2.d3.g2_standardised-down-day-bounce | 0.94 | 4.7 |
| 032-02.b2.g1_close-location-next-day-reversal | 032-02.b2_volatile-low-next-day-rebound | plan | confirmed (+4.76) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.d: 032-02.b2.g1.d1_close-location-on-wide-days, 032-02.b2.g1.d2_long-reversal-after-wide-days, 032-02.b2.g1.d3_short-fade-in-falling-month; 7.g: 032-02.b2.g1.g1_close-distance-from-midpoint, 032-02.b2.g1.g2_wide-day-close-reversal, 032-02.b2.g1.g3_next-day-rebound-after-shocks, 032-02.b2.g1.g4_five-day-range-continuation | 1.07 | 5.9 |
| 032-02.b2.d1_volatile-ten-day-low-rebound | 032-02.b2_volatile-low-next-day-rebound | plan | inconclusive (+2.48) | not profitable enough (failed: Calmar) | - | 7.b: 032-02.b2.d1.b1_volatile-ten-day-low-rebound-wider; 7.g: 032-02.b2.d1.g1_wide-day-weak-close-rebound | 1.98 | 6.2 |
| 032-02.b2.d2_graded-monthly-low-rebound | 032-02.b2_volatile-low-next-day-rebound | missing-components | - | - | - | - | 0.27 | 2.0 |
| 032-02.b2.g1.d1_close-location-on-wide-days | 032-02.b2.g1_close-location-next-day-reversal | missing-components | - | - | - | - | 0.06 | 0.4 |
| 032-02.b2.g1.d2_long-reversal-after-wide-days | 032-02.b2.g1_close-location-next-day-reversal | plan | inconclusive (+1.19) | not profitable enough (failed: Calmar) | - | 7.b: 032-02.b2.g1.d2.b1_wide-day-low-close-rebound-more-coins, 032-02.b2.g1.d2.b2_rebound-after-wide-days-in-decline; 7.g: 032-02.b2.g1.d2.g1_five-day-momentum-continues-briefly, 032-02.b2.g1.d2.g2_monthly-trend-carries-over-days | 1.01 | 5.5 |
| 032-02.b2.g1.d3_short-fade-in-falling-month | 032-02.b2.g1_close-location-next-day-reversal | plan | inconclusive (+1.16) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-02.b2.g1.d3.b1_short-fade-more-coins, 032-02.b2.g1.d3.b2_high-close-fades-wide-steeper; 7.g: 032-02.b2.g1.d3.g1_falling-month-one-day-close-reversal, 032-02.b2.g1.d3.g2_falling-month-daily-return-reversal, 032-02.b2.g1.d3.g3_near-high-five-day-continuation | 1.09 | 6.0 |
| 032-02.b2.g2_volatile-close-near-low-rebound | 032-02.b2_volatile-low-next-day-rebound | plan | confirmed (+2.45) | not profitable enough (failed: Calmar) | - | 7.d: 032-02.b2.g2.d1_near-low-rebound-in-falling-months, 032-02.b2.g2.d2_below-midrange-close-rebound, 032-02.b2.g2.d3_rebound-scaled-by-range-widening; 7.g: 032-02.b2.g2.g1_volatile-large-fall-next-day-rebound | 1.04 | 5.3 |
| 032-02.b2.g2.d1_near-low-rebound-in-falling-months | 032-02.b2.g2_volatile-close-near-low-rebound | plan | inconclusive (+1.30) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 032-02.b2.g2.d1.b1_near-low-rebound-more-coins, 032-02.b2.g2.d1.b2_near-high-close-fades; 7.g: 032-02.b2.g2.d1.g1_near-low-close-rebounds-anywhere, 032-02.b2.g2.d1.g2_volatility-scaled-one-day-fall-reversal, 032-02.b2.g2.d1.g3_down-day-close-at-low-rebounds | 1.00 | 5.3 |
| 032-02.b2.g2.d2_below-midrange-close-rebound | 032-02.b2.g2_volatile-close-near-low-rebound | plan | inconclusive (+1.97) | not profitable enough (failed: Mean daily return, on days in a position) | - | 7.b: 032-02.b2.g2.d2.b1_below-midrange-rebound-all-coins, 032-02.b2.g2.d2.b2_close-location-in-wide-ranges; 7.g: 032-02.b2.g2.d2.g1_large-daily-fall-rebounds, 032-02.b2.g2.d2.g2_volatile-regime-daily-fall-rebound | 0.92 | 5.2 |
| 032-02.b2.g2.d3_rebound-scaled-by-range-widening | 032-02.b2.g2_volatile-close-near-low-rebound | plan | mismatch | not profitable enough (failed: Calmar) | - | 7.g: 032-02.b2.g2.d3.g1_volatility-scaled-down-day-rebound, 032-02.b2.g2.d3.g2_calm-after-turbulence-daily-drift | 1.03 | 6.4 |

## Consumption
17 ideas, 16.91 USD, 94.6 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 2.83 | 13.9 |
| step4_backtest | 0.00 | 32.9 |
| step5_verdict | 2.67 | 10.3 |
| step6_check | 0.00 | 0.7 |
| chart_files | 0.00 | 0.2 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 1.18 | 4.2 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 3.46 | 11.1 |
| step7_7.g | 6.36 | 19.7 |
| step7_7.a | 0.41 | 1.3 |
| similarity_check | 0.00 | 0.2 |
