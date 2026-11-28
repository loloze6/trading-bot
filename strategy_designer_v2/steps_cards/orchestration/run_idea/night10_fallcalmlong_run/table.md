# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 086-01_heavy-volume-up-day-continuation | - | plan | no effect (+0.42) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-01.c1_heavy-volume-off-low-absorption, 086-01.c2_heavy-up-day-extends-rebound | 0.74 | 6.6 |
| 050-02_falling-calm-scaled-week-rise-continuation | - | plan | inconclusive (+1.89) | not profitable enough (failed: Calmar) | - | 7.b: 050-02.b1_calm-downtrend-week-rise-more-coins, 050-02.b2_calm-downtrend-week-rise-five-days | 0.68 | 5.8 |
| 086-02_repeated-heavy-volume-buying-days | - | plan | no effect (-0.94) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-02.c1_light-volume-up-day-follow-through, 086-02.c2_quiet-three-day-rise-continuation | 0.74 | 6.4 |
| 050-04_falling-calm-range-scaled-week-rise | - | plan | inconclusive (+1.83) | not profitable enough (failed: Calmar) | - | 7.b: 050-04.b1_range-scaled-week-rise-more-coins; 7.g: no ideas: In falling calm markets the only graded pattern (F1, F4) separates down weeks from up weeks rather than growing with the rise, and it has no fifth with t ≥ 2 and flips sign between 2018–2019 and 2020–2021 (F2, F5). Its nearness-to-high form is already held (035-01.b1), and no other angle looked at (F6) stands out from chance, so no long idea rests on these findings. | 0.84 | 6.5 |
| 086-01.c1_heavy-volume-off-low-absorption | 086-01_heavy-volume-up-day-continuation | plan | no effect (-0.71) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-01.c1.c1_light-volume-up-day-continues, 086-01.c1.c2_heavy-volume-down-day-rebounds; 7.g: 0 ideas, 2 discoveries (2 explorations) | 1.07 | 7.5 |
| 050-02.b1_calm-downtrend-week-rise-more-coins | 050-02_falling-calm-scaled-week-rise-continuation | plan | confirmed (+2.15) | not profitable enough (failed: Calmar) | - | 7.d: 050-02.b1.d1_large-scaled-rise-longer-hold, 050-02.b1.d2_scaled-rise-strong-case, 050-02.b1.d3_rise-with-room-below-high; 7.g: no ideas: Across about fifteen variables and three horizons, the only long-side gradient in falling calm markets is the tested scaled 7-day rise itself (F1), and its look-alike, the range place, repeats it (F2). The strong patterns point short (F3, F5), outside the long-only box, and what limits the book is how concentrated its gains are (F4), which no new situation addresses. | 1.31 | 7.6 |
| 050-02.b1.d1_large-scaled-rise-longer-hold | 050-02.b1_calm-downtrend-week-rise-more-coins | plan | inconclusive (+1.20) | not profitable enough (failed: Calmar) | - | 7.b: 050-02.b1.d1.b1_scaled-rise-carry-more-coins | 0.62 | 5.6 |
| 050-02.b1.d2_scaled-rise-strong-case | 050-02.b1_calm-downtrend-week-rise-more-coins | plan | inconclusive (+2.39) | not profitable enough (failed: Calmar) | - | 7.b: 050-02.b1.d2.b1_scaled-rise-week-carry, 050-02.b1.d2.b2_scaled-rise-more-coins | 0.60 | 5.6 |
| 050-02.b1.d3_rise-with-room-below-high | 050-02.b1_calm-downtrend-week-rise-more-coins | plan | no effect (+0.67) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 050-02.b1.d3.c1_scaled-weekly-rise-short-carry, 050-02.b1.d3.c2_scaled-three-day-rise-carries; 7.g: 050-02.b1.d3.g1_calm-downtrend-two-week-scaled-rise | 1.07 | 7.1 |
| 050-04.b1_range-scaled-week-rise-more-coins | 050-04_falling-calm-range-scaled-week-rise | plan | inconclusive (+1.83) | not profitable enough (failed: Calmar) | - | 7.b: no ideas: The small positive carry-on after a calm-downtrend weekly rise is already measured on all the data available (F1). It does not grow with the size of the rise (F2, F3), and it is not concentrated in a horizon, coin, year or kind of signal day (F4, F5), so no amendment would give a clear answer.; 7.g: no ideas: In falling calm markets the long side shows no graded carry-on from the scaled weekly rise (F2, F3). The one long pattern that stands out, nearness to the recent high, is not separable from the tested measure, is unstable by year and coin, and is already held by 035-01.b1 (F4, F5). Nothing else among the angles examined stands out from chance (F6). | 1.20 | 7.3 |
| 089-01_calm-decline-up-volume-share | - | plan | no effect (-1.14) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 089-01.c1_calm-decline-down-volume-exhaustion | 1.68 | 6.3 |
| 089-02_calm-decline-up-down-volume-ratio | - | missing-components | - | - | - | - | 0.05 | 0.3 |
| 089-03_calm-decline-thinning-down-volume | - | missing-components | - | - | - | - | 0.06 | 0.3 |
| 089-04_calm-decline-up-volume-lasting | - | plan | no effect (-1.08) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.c: 089-04.c1_heavy-up-day-volume-rebounds, 089-04.c2_swelling-volume-in-calm-decline; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.03 | 7.0 |
| 050-02.b2_calm-downtrend-week-rise-five-days | 050-02_falling-calm-scaled-week-rise-continuation | plan | no effect (-0.21) | not profitable enough (failed: Calmar) | - | 7.c: 050-02.b2.c1_calm-downtrend-fortnight-rise-carries; 7.g: 050-02.b2.g1_calm-downtrend-climb-off-low | 1.27 | 7.1 |
| 086-02.c1_light-volume-up-day-follow-through | 086-02_repeated-heavy-volume-buying-days | plan | no effect (+0.41) | not profitable enough (failed: Calmar) | - | 7.c: 086-02.c1.c1_light-up-day-shallow-fall, 086-02.c1.c2_up-day-after-shallow-fall; 7.g: no ideas: I looked at the forecast, volume on up and down days, prior 5- and 10-day returns, range, close position, weekday, coin and window. Every long-side pattern in falling calm markets (F2–F4) changes sign or vanishes when the 5-day grid is shifted or all bars are used, so none can be told from chance across this many angles. | 1.04 | 7.2 |
| 089-01.c1_calm-decline-down-volume-exhaustion | 089-01_calm-decline-up-volume-share | missing-components | - | - | - | - | 0.06 | 0.3 |
| 089-04.c1_heavy-up-day-volume-rebounds | 089-04_calm-decline-up-volume-lasting | missing-components | - | - | - | - | 0.06 | 0.3 |
| 086-01.c2_heavy-up-day-extends-rebound | 086-01_heavy-volume-up-day-continuation | plan | no effect (+0.68) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.c: 086-01.c2.c1_quiet-up-day-extends-rebound, 086-01.c2.c2_strong-rebound-up-day-continues; 7.g: no ideas: In falling calm markets the brief's heavy-volume effect is absent, and at 3 to 5 days it points the wrong way (F2, F3). The only graded pattern, prior 5-day momentum at 3 to 5 days (F4), flips at 10 days and does not survive the roughly 36 feature-and-horizon angles examined (F5). No pattern stands out enough to justify a new long idea in this box. | 1.04 | 7.1 |

## Consumption
19 ideas, 15.15 USD, 101.9 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 2.48 | 8.7 |
| step4_backtest | 0.00 | 53.8 |
| step5_verdict | 2.70 | 10.1 |
| step6_check | 0.00 | 0.3 |
| chart_files | 0.00 | 0.2 |
| step7_7.g | 3.92 | 11.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.67 | 1.8 |
| step7_7.b | 1.67 | 4.9 |
| step7_7.c | 3.70 | 10.8 |
| similarity_check | 0.00 | 0.1 |
