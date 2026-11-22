# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 027-01_panic-range-multiple-rebound | - | missing-components | - | - | - | - | 0.07 | 0.5 |
| 027-02_panic-fall-depth-rebound | - | plan | inconclusive (+0.49) | not profitable enough (failed: Mean daily return, Calmar) | - | 7.b: no ideas: The tested grading, a deeper fall followed by a larger rebound, is absent at every horizon from 1 to 21 days (F1, F2), so narrowing it to a shorter horizon or a part of the data would not make it show; the panic premium appears only as a flat level over 1 to 3 days (F3, F4), with no grade that carries it (F6), and that is the clear answer.; 7.d: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends, 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues, 027-02_panic-fall-depth-rebound.d3_moderate-shake-outs-also-rebound; 7.g: 027-02_panic-fall-depth-rebound.g1_mild-panic-fall-rebound, 027-02_panic-fall-depth-rebound.g2_deep-panic-fall-continuation | 1.42 | 8.0 |
| 027-03_panic-rebound-in-downtrend | - | plan | inconclusive (+0.99) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar, Trades per day) | - | 7.b: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins, 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days; 7.d: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium, 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound; 7.g: 027-03_panic-rebound-in-downtrend.g1_one-day-wide-range-fall-rebound, 027-03_panic-rebound-in-downtrend.g2_panic-premium-within-three-days, 027-03_panic-rebound-in-downtrend.g3_one-day-wide-range-rally-fade | 1.31 | 8.0 |
| 027-04_panic-delayed-recovery-drift | - | missing-components | - | - | - | - | 0.10 | 0.7 |
| 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins | 027-03_panic-rebound-in-downtrend | plan | rejected (-5.29) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | - | 7.c: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins.c1_panic-rebound-in-uptrends, 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins.c2_downtrend-dips-keep-falling, 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins.c3_downtrend-panic-short-rebound; 7.d: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins.d1_one-day-panic-rebound, 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins.d2_deep-panic-after-decline, 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins.d3_capitulation-one-day-rebound; 7.g: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins.g1_volatility-expansion-precedes-gains, 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins.g2_short-panic-rebound-in-uptrends | 1.65 | 13.2 |
| 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days | 027-03_panic-rebound-in-downtrend | plan | inconclusive (+5.04) | not profitable enough (failed: Mean daily return, Calmar) | - | 7.b: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend; 7.d: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.d1_one-day-panic-premium-broad, 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.d2_absorbed-panic-rebound; 7.g: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.g1_range-expansion-predicts-rebound, 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.g2_wide-range-falls-rebound-graded, 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.g3_next-day-rebound-after-falls | 1.48 | 8.0 |
| 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend | 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days | plan | mismatch | not profitable enough (failed: Mean daily return) | - | 7.d: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend.d1_mild-panic-in-uptrend, 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend.d2_shallow-dip-week-rebound; 7.g: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend.g1_wide-range-falls-rebound, 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend.g2_wide-range-dip-in-uptrend, 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend.g3_late-utc-evening-bid, 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend.g4_post-midnight-utc-weakness | 1.02 | 7.1 |
| 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends | 027-02_panic-fall-depth-rebound | plan | inconclusive (+1.26) | not profitable enough (failed: Mean daily return, Trades per day) | - | 7.b: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins; 7.d: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.d1_panic-width-rebound-any-trend, 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.d2_one-week-panic-width-rebound; 7.g: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.g1_afternoon-utc-volatility-scaled-rise | 1.61 | 9.2 |

## Consumption
8 ideas, 8.66 USD, 54.5 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.01 | 7.5 |
| step4_backtest | 0.00 | 19.6 |
| step5_verdict | 1.09 | 4.5 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.2 |
| step7_7.c | 0.43 | 1.3 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 2.32 | 7.9 |
| step7_7.b | 1.34 | 4.7 |
| step7_7.g | 2.47 | 8.6 |
