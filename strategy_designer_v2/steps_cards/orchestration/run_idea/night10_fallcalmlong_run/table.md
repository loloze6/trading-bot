# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 086-01_heavy-volume-up-day-continuation | - | plan | no effect (+0.42) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-01.c1_heavy-volume-off-low-absorption, 086-01.c2_heavy-up-day-extends-rebound | 0.74 | 6.6 |
| 050-02_falling-calm-scaled-week-rise-continuation | - | plan | inconclusive (+1.89) | not profitable enough (failed: Calmar) | - | 7.b: 050-02.b1_calm-downtrend-week-rise-more-coins, 050-02.b2_calm-downtrend-week-rise-five-days | 0.68 | 5.8 |
| 086-02_repeated-heavy-volume-buying-days | - | plan | no effect (-0.94) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-02.c1_light-volume-up-day-follow-through, 086-02.c2_quiet-three-day-rise-continuation | 0.74 | 6.4 |
| 050-04_falling-calm-range-scaled-week-rise | - | plan | inconclusive (+1.83) | not profitable enough (failed: Calmar) | - | 7.b: 050-04.b1_range-scaled-week-rise-more-coins; 7.g: no ideas: In falling calm markets the only graded pattern (F1, F4) separates down weeks from up weeks rather than growing with the rise, and it has no fifth with t ≥ 2 and flips sign between 2018–2019 and 2020–2021 (F2, F5). Its nearness-to-high form is already held (035-01.b1), and no other angle looked at (F6) stands out from chance, so no long idea rests on these findings. | 0.84 | 6.5 |
| 086-01.c1_heavy-volume-off-low-absorption | 086-01_heavy-volume-up-day-continuation | plan | no effect (-0.71) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-01.c1.c1_light-volume-up-day-continues, 086-01.c1.c2_heavy-volume-down-day-rebounds; 7.g: 0 ideas, 2 discoveries (2 explorations) | 1.07 | 7.5 |

## Consumption
5 ideas, 4.06 USD, 32.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.49 | 2.7 |
| step4_backtest | 0.00 | 18.5 |
| step5_verdict | 0.92 | 3.5 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.g | 0.77 | 2.3 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 0.63 | 1.8 |
| step7_7.c | 1.25 | 3.7 |
