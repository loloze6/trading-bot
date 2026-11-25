# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_choppy-agitated-weekly-rise-reverts | - | plan | inconclusive (-1.30) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The theme's effect is not in the data. The tested result points the wrong way (F1), and inside the choppy agitated profile larger weekly rises are not followed by larger falls at any horizon (F2, F4). The only fall seen follows rises and falls alike (F3), and the reversal is no stronger in the profile than outside it (F5), so no amended idea on the theme has a finding to rest on.; 7.g: 032-01.g1_choppy-market-weekly-reversal | 0.96 | 5.5 |
| 033-01_scaled-daily-fall-next-day-rebound | - | plan | confirmed (+2.63) | not profitable enough (failed: Calmar) | - | 7.d: 033-01.d1_agitated-outsized-fall-rebound, 033-01.d2_falling-agitated-fall-rebound; 7.g: 033-01.g1_heavy-volume-outsized-fall-rebound, 033-01.g2_agitated-market-scaled-fall-rebound | 1.12 | 5.4 |
| 032-02_choppy-agitated-weekly-fall-reverts | - | plan | inconclusive (-0.54) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 032-02.b1_choppy-agitated-weekly-rise-fades; 7.g: 0 ideas, 3 discoveries (2 explorations) | 1.00 | 5.6 |
| 034-01_agitated-scaled-fall-next-day-rebound | - | plan | inconclusive (+1.89) | not profitable enough (failed: Calmar) | - | 7.b: 034-01.b1_agitated-fall-rebound-more-coins, 034-01.b2_falling-agitated-fall-rebound; 7.g: 034-01.g1_agitated-extreme-fall-convex-rebound, 034-01.g2_agitated-deep-fall-two-day-rebound, 034-01.g3_agitated-three-day-fall-rebound, 034-01.g4_scaled-fall-rebound-every-market | 1.05 | 6.1 |
| 035-01_falling-agitated-scaled-fall-rebound | - | plan | confirmed (+2.62) | profitable enough | unseen_2016_2017: holds; unseen_2026: does not hold | 7.g: 035-01.g1_second-down-day-rebound, 035-01.g2_scaled-fall-two-day-rebound | 0.65 | 5.7 |
| 036-01_agitated-scaled-fall-three-day-rebound | - | plan | inconclusive (+0.72) | not profitable enough (failed: Calmar) | - | 7.b: no ideas: The theme's effect is not in the data. The three-day rise does not grow with the scaled fall in any trend (F1). It is not larger in agitated than in calm markets (F3). What rebound exists lands on the next day and is not built over the two days after (F4, F5). More data could not lift a t of 0.72 (F2).; 7.g: 036-01.g1_falling-agitated-scaled-fall-rebound | 0.98 | 5.6 |
| 037-01_agitated-ordinary-rise-next-day-giveback | - | plan | confirmed (+2.20) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 037-01.d1_falling-agitated-rise-giveback; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.03 | 6.0 |
| 038-01_calm-scaled-weekly-rise-continues | - | plan | inconclusive (+1.46) | not profitable enough (failed: Calmar) | - | 7.b: 038-01.b1_calm-scaled-rise-more-coins, 038-01.b2_calm-scaled-move-continues-both-ways; 7.g: 038-01.g1_calm-scaled-fall-continues, 038-01.g2_calm-short-burst-follows-through, 038-01.g3_calm-monthly-scaled-trend-continues | 0.83 | 5.3 |
| 039-01_agitated-low-close-next-day-rebound | - | plan | confirmed (+2.96) | not profitable enough (failed: Mean daily return, on days in a position, Calmar) | - | 7.d: 039-01.d1_falling-agitated-low-close-rebound, 039-01.d2_wide-range-low-close-rebound; 7.g: 039-01.g1_wide-day-low-close-rebound, 039-01.g2_price-distance-below-mid-range | 1.01 | 6.5 |
| 040-01_agitated-daily-fall-next-day-rebound | - | plan | confirmed (+2.18) | not profitable enough (failed: Calmar) | - | 7.d: 040-01.d1_agitated-outsized-fall-rebound, 040-01.d2_agitated-second-down-day-rebound; 7.g: 040-01.g1_heavy-volume-agitated-fall-rebound | 1.00 | 6.1 |
| 036-02_agitated-scaled-fall-delayed-rebound | - | plan | inconclusive (+1.21) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 036-02.b1_delayed-rebound-more-coins; 7.g: 036-02.g1_agitated-fall-next-day-rebound, 036-02.g2_agitated-scaled-fall-bounce | 0.99 | 6.2 |

## Consumption
11 ideas, 10.61 USD, 64.0 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.81 | 4.5 |
| step4_backtest | 0.00 | 26.1 |
| step5_verdict | 1.80 | 6.4 |
| step6_check | 0.00 | 0.4 |
| chart_files | 0.00 | 0.2 |
| step7_7.d | 1.59 | 5.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 1.95 | 6.0 |
| step7_7.g | 4.46 | 14.0 |
| similarity_check | 0.00 | 0.3 |
| unseen_test | 0.00 | 1.1 |
