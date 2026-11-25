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

## Consumption
11 ideas, 12.88 USD, 79.3 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.61 | 4.6 |
| step4_backtest | 0.00 | 37.1 |
| step5_verdict | 1.77 | 6.2 |
| step6_check | 0.00 | 0.4 |
| chart_files | 0.00 | 0.2 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 1.09 | 3.2 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.46 | 1.2 |
| step7_7.b | 2.62 | 8.4 |
| step7_7.g | 5.32 | 16.7 |
| similarity_check | 0.00 | 0.2 |
| unseen_test | 0.00 | 1.1 |
