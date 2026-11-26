# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 058-01_agitated-rise-stretch-giveback | - | plan | inconclusive (+0.39) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The theme's effect is not in the data. In rising agitated markets a close far above its 20-day average is followed by a further rise beyond drift, not a giveback (F2), and no graded fall shows at any horizon, coin or distance band (F1, F3, F4, F5).; 7.g: 0 ideas, 2 discoveries (3 explorations) | 1.09 | 6.5 |
| 058-03_calm-rise-stretch-continuation | - | plan | inconclusive (+1.49) | profitable enough | - | 7.b: 058-03.b1_calm-rise-continuation-all-coins; 7.e: 058-03.e1_calm-rise-stretch-ten-days, 058-03.e2_choppy-market-distance-continuation; 7.g: 0 ideas, 2 discoveries (3 explorations) | 1.47 | 7.3 |
| 058-03.e1_calm-rise-stretch-ten-days | 058-03_calm-rise-stretch-continuation | plan | confirmed (+2.32) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: 058-03.e1.g1_choppy-stretch-continues-ten-days | 0.73 | 6.2 |
| 058-03.e2_choppy-market-distance-continuation | 058-03_calm-rise-stretch-continuation | plan | inconclusive (+0.72) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-03.e2.b1_choppy-distance-continuation-more-coins; 7.g: 0 ideas, 1 discoveries (3 explorations) | 0.98 | 5.3 |
| 058-03.b1_calm-rise-continuation-all-coins | 058-03_calm-rise-stretch-continuation | plan | confirmed (+2.06) | not profitable enough (failed: Calmar) | - | 7.d: 058-03.b1.d1_calm-rise-moderate-stretch, 058-03.b1.d2_calm-rise-longer-hold; 7.g: 0 ideas, 2 discoveries (2 explorations) | 1.37 | 12.0 |
| 058-03.e2.b1_choppy-distance-continuation-more-coins | 058-03.e2_choppy-market-distance-continuation | plan | inconclusive (+0.97) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 058-03.e2.b1.b1_choppy-distance-continuation-recent-swings; 7.g: 0 ideas, 2 discoveries (3 explorations) | 1.30 | 11.2 |
| 059-01_swing-scaled-rise-continues | - | plan | inconclusive (+2.08) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 059-01.b1_calm-swing-scaled-move-continues; 7.g: 059-01.g1_calm-swing-scaled-move-continues, 059-01.g2_calmer-scaled-move-carries-further | 1.06 | 5.4 |
| 059-01.b1_calm-swing-scaled-move-continues | 059-01_swing-scaled-rise-continues | plan | inconclusive (+1.41) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 059-01.b1.b1_calm-scaled-move-more-coins; 7.g: 059-01.b1.g1_choppy-calm-scaled-continuation, 059-01.b1.g2_calm-week-move-continues | 0.98 | 5.9 |
| 060-01_falling-agitated-high-close-fade | - | plan | confirmed (-2.46) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 060-01.d1_wide-day-high-close-next-day-fade; 7.g: 060-01.g1_wide-day-high-close-fade | 1.06 | 6.3 |
| 058-02_agitated-rise-swing-scaled-giveback | - | plan | inconclusive (-0.79) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The theme's effect is not in the data: a coin far above its 20-day average in a rising agitated market kept rising over the next 1 to 10 days, in every coin and every year with enough cases, with no graded giveback (F1–F4). The only gradient, continuation in calm and choppy markets, is too weak and too mixed across coins to make a clear idea (F5, F6).; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.81 | 6.6 |
| 060-01.d1_wide-day-high-close-next-day-fade | 060-01_falling-agitated-high-close-fade | plan | inconclusive (-1.78) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 060-01.d1.b1_wide-day-upper-close-next-day-fade, 060-01.d1.b2_wide-up-day-high-close-fade; 7.g: no ideas: The only pattern that stands out once same-day cases are counted together is the wide-day low-close rebound (F1), which the portfolio already holds; the tested high-close fade, its grading, and the weekday, volatility and rising-trend angles stay under t 2 or repeat held books (F2–F6). | 1.03 | 6.4 |
| 060-01.g1_wide-day-high-close-fade | 060-01_falling-agitated-high-close-fade | plan | confirmed (+2.50) | not profitable enough (failed: Calmar, Trades per day) | - | 7.d: 060-01.g1.d1_wider-than-usual-high-close-fade, 060-01.g1.d2_wide-day-close-location-graded-fade; 7.g: 060-01.g1.g1_graded-width-high-close-fade | 1.11 | 7.1 |
| 060-01.g1.d1_wider-than-usual-high-close-fade | 060-01.g1_wide-day-high-close-fade | plan | inconclusive (+1.89) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 060-01.g1.d1.b1_wide-high-close-fade-more-coins; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.10 | 7.0 |
| 060-01.g1.d2_wide-day-close-location-graded-fade | 060-01.g1_wide-day-high-close-fade | plan | confirmed (+2.23) | not profitable enough (failed: Calmar) | - | 7.d: 060-01.g1.d2.d1_own-range-close-height-fade, 060-01.g1.d2.d2_wider-squeeze-day-fades-harder; 7.g: 060-01.g1.d2.g1_up-day-high-close-fade | 1.13 | 7.2 |
| 060-01.g1.d2.d1_own-range-close-height-fade | 060-01.g1.d2_wide-day-close-location-graded-fade | plan | confirmed (+2.23) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: 060-01.g1.d2.d1.g3_wide-high-close-fade | 0.90 | 7.4 |
| 060-01.g1.d2.d2_wider-squeeze-day-fades-harder | 060-01.g1.d2_wide-day-close-location-graded-fade | plan | inconclusive (+1.83) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 060-01.g1.d2.d2.b1_wider-squeeze-fade-more-coins; 7.g: 060-01.g1.d2.d2.g1_agitated-downtrend-up-day-fades, 060-01.g1.d2.d2.g2_calm-downtrend-fall-continuation | 1.00 | 6.6 |
| 060-01.g1.g1_graded-width-high-close-fade | 060-01.g1_wide-day-high-close-fade | plan | inconclusive (+1.83) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 060-01.g1.g1.b1_graded-width-fade-all-coins; 7.g: 060-01.g1.g1.g1_agitated-downtrend-up-day-fade, 060-01.g1.g1.g2_swing-graded-downtrend-rally-fade | 0.88 | 6.0 |
| 068-01_falling-agitated-lone-rise-fade | - | plan | no verdict | not checked | - | 7.g: no ideas: The backtest record is empty (0 coin-window tables in bars, trades and days, and no verdict, check or size), so no pattern could be measured and no finding supports an idea; the backtest should be rerun before this line reads it again. | 0.34 | 3.8 |

## Consumption
18 ideas, 19.34 USD, 124.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 2.31 | 9.0 |
| step4_backtest | 0.00 | 57.0 |
| step5_verdict | 2.79 | 10.0 |
| step6_check | 0.00 | 0.5 |
| chart_files | 0.00 | 0.2 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 2.00 | 6.4 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.46 | 1.2 |
| step7_7.b | 3.38 | 10.8 |
| step7_7.g | 8.39 | 26.4 |
| similarity_check | 0.00 | 0.4 |
| unseen_test | 0.00 | 2.3 |
