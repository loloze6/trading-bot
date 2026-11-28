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

## Consumption
10 ideas, 8.85 USD, 66.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.90 | 4.9 |
| step4_backtest | 0.00 | 36.2 |
| step5_verdict | 1.81 | 6.8 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.g | 2.16 | 6.2 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.67 | 1.8 |
| step7_7.b | 1.67 | 4.9 |
| step7_7.c | 1.63 | 4.8 |
| similarity_check | 0.00 | 0.1 |
