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
| 038-02_calm-scaled-weekly-fall-continues | - | plan | inconclusive (+1.53) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 038-02.b1_calm-scaled-fall-more-coins; 7.g: 038-02.g1_calm-scaled-three-day-continuation, 038-02.g2_calm-scaled-rise-continues, 038-02.g3_calm-scaled-monthly-trend-continues | 0.94 | 5.9 |
| 039-02_agitated-high-close-next-day-giveback | - | plan | confirmed (+2.96) | not profitable enough (failed: Mean daily return, on days in a position, Calmar) | - | 7.d: 039-02.d1_wide-range-low-close-next-day-rebound, 039-02.d2_falling-market-low-close-rebound, 039-02.d3_choppy-market-high-close-giveback; 7.g: 039-02.g2_downtrend-low-close-next-day-rebound, 039-02.g3_wide-day-close-location-reversal | 1.08 | 6.6 |
| 041-01_agitated-scaled-rise-next-day-continues | - | plan | inconclusive (-1.11) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 041-01.b1_rising-agitated-rise-continues, 041-01.b2_falling-agitated-rise-given-back; 7.g: 041-01.g1_falling-agitated-fall-rebound | 1.14 | 6.3 |
| 040-02_agitated-daily-rise-next-day-giveback | - | plan | inconclusive (+1.33) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 040-02.b1_falling-agitated-fall-rebound, 040-02.b2_agitated-daily-fall-rebound; 7.g: 040-02.g1_falling-agitated-fall-rebound | 0.92 | 5.8 |
| 037-01.d1_falling-agitated-rise-giveback | 037-01_agitated-ordinary-rise-next-day-giveback | plan | inconclusive (+1.60) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 037-01.d1.b1_falling-agitated-rise-giveback-more-coins; 7.g: 037-01.d1.g2_agitation-scaled-ordinary-rise-giveback | 1.03 | 6.3 |
| 042-01_falling-agitated-low-close-rebound | - | plan | confirmed (+2.98) | not profitable enough (failed: Calmar) | - | 7.d: 042-01.d1_lower-half-close-rebound, 042-01.d2_down-day-low-close-rebound; 7.g: 042-01.g1_deep-close-in-usual-ranges, 042-01.g2_wide-low-close-rebounds | 1.03 | 6.4 |
| 043-01_falling-agitated-intraday-drop-rebound | - | plan | confirmed (+3.04) | profitable enough | unseen_2016_2017: holds; unseen_2026: does not hold | 7.g: 043-01.g1_falling-agitated-day-move-reversal | 1.43 | 6.3 |
| 039-01.d1_falling-agitated-low-close-rebound | 039-01_agitated-low-close-next-day-rebound | plan | mismatch | not profitable enough (failed: Mean daily return, on days in a position, Calmar) | - | 7.g: 039-01.d1.g1_wide-day-low-close-rebound, 039-01.d1.g2_falling-wide-day-low-close-rebound | 0.60 | 4.9 |
| 039-02.d1_wide-range-low-close-next-day-rebound | 039-02_agitated-high-close-next-day-giveback | plan | confirmed (+2.61) | profitable enough | unseen_2016_2017: holds; unseen_2026: does not hold | 7.g: 039-02.d1.g2_down-day-low-close-next-day-rebound | 0.64 | 6.2 |
| 044-02_agitated-down-day-range-rebound | - | plan | confirmed (+3.21) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: 044-02.g1_agitated-wide-fall-run-rebound | 0.74 | 7.3 |
| 045-01_agitated-wide-low-close-rebound | - | plan | confirmed (+3.83) | profitable enough | unseen_2016_2017: does not hold; unseen_2026: does not hold | 7.g: 045-01.g1_falling-agitated-low-close-rebound, 045-01.g2_agitated-high-close-next-day-fade | 0.63 | 6.2 |
| 046-01_calm-scaled-rise-second-day-continues | - | plan | inconclusive (+1.88) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 046-01.b1_calm-rise-second-day-all-coins; 7.g: 0 ideas, 1 discoveries (2 explorations) | 4.18 | 19.0 |
| 047-01_falling-agitated-daily-fall-rebound | - | plan | confirmed (+2.77) | profitable enough | unseen_2016_2017: holds; unseen_2026: does not hold | 7.g: 047-01.g1_agitated-wide-up-day-next-day-fade, 047-01.g2_agitated-wide-down-day-rebound | 0.78 | 6.4 |
| 045-02_agitated-wide-high-close-giveback | - | plan | no verdict | not checked | - | 7.g: no ideas: The backtest record for 045-02_agitated-wide-high-close-giveback reached this line with 0 coins, 0 windows, 0 bars, 0 trades and 0 days, so no pattern could be measured and no idea can rest on a finding. The backtest should be re-run or its record reloaded before this line reads it again. | 0.34 | 3.4 |
| 046-02_calm-scaled-rise-two-day-continues | - | plan | inconclusive (+0.39) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 046-02.b1_calm-rise-second-day-follow-through; 7.g: 046-02.g2_calm-rise-second-day-follow-through | 1.09 | 5.9 |
| 044-01_agitated-wide-range-fall-rebound | - | plan | confirmed (+2.16) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: 044-01.g1_falling-agitated-wide-fall-rebound | 2.40 | 7.0 |
| 048-01_falling-agitated-wide-rise-giveback | - | missing-components | - | - | - | - | 0.08 | 0.5 |

## Consumption
28 ideas, 29.68 USD, 174.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 4.48 | 12.9 |
| step4_backtest | 0.00 | 67.2 |
| step5_verdict | 4.26 | 15.5 |
| step6_check | 0.00 | 0.9 |
| chart_files | 0.00 | 0.4 |
| step7_7.d | 2.35 | 7.6 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 7.34 | 26.0 |
| step7_7.g | 11.26 | 35.0 |
| similarity_check | 0.00 | 0.9 |
| unseen_test | 0.00 | 7.8 |
