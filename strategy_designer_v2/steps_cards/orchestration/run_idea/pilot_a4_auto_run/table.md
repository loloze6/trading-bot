# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 061-01_falling-calm-scaled-rise-fade | - | plan | no effect (-1.44) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 061-01.c1_falling-calm-scaled-fall-rebound, 061-01.c2_falling-calm-rise-continuation | 0.71 | 8.3 |
| 064-01_falling-calm-up-day-fades | - | plan | no effect (+0.45) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 064-01.c1_calm-decline-big-rise-follows-through, 064-01.c2_calm-decline-bounce-extends-week | 0.56 | 7.6 |
| 086-01_heavy-volume-up-day-continuation | - | plan | no effect (+0.82) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.c: no ideas: The theme's effect is not in the data. In falling calm markets, heavy-volume up days are followed by no more rise than light-volume ones at 1 to 10 days (F1, F6), and volume does not grade the later move (F2). The only positive result comes from DOGE in two 2021 windows, while BTC and XMR kept falling after up days of every kind (F3, F4, F5). That leaves no long-side variation on this theme a trader could act on. | 0.66 | 8.1 |
| 050-02_falling-calm-scaled-week-rise-continuation | - | plan | inconclusive (+1.50) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 050-02.b1_calm-downtrend-week-rise-continuation-more-coins | 0.48 | 7.5 |
| 060-02_falling-calm-low-to-close-fade | - | missing-components | - | - | - | - | 0.10 | 0.6 |
| 086-02_volume-weighted-up-move-continuation | - | plan | no effect (+0.51) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.c: 086-02.c1_calm-decline-five-day-continuation, 086-02.c2_calm-decline-ten-day-continuation | 0.68 | 7.9 |
| 050-03_falling-calm-range-scaled-week-fall | - | plan | no effect (+0.19) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 050-03.c1_calm-downtrend-scaled-rise-continues, 050-03.c2_weekly-scaled-rise-longer-carry | 0.62 | 7.8 |
| 050-04_falling-calm-range-scaled-week-rise | - | plan | inconclusive (+1.26) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 050-04.b1_range-scaled-week-rise-all-coins; 7.g: no ideas: The only graded pattern is the 14-day rise carrying on over the next week in falling calm markets, and on the long side it rests on 23 cases and 19 days, with t near 2, mostly from one window; after about forty angles tested, it does not stand out from chance. | 0.83 | 7.9 |
| 077-01_falling-calm-deep-close-drift | - | plan | no effect (+0.61) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 077-01.c1_falling-calm-recovery-continues; 7.g: 077-01.g1_falling-calm-rebound-continuation, 077-01.g2_calm-decline-five-day-momentum | 1.13 | 8.9 |

## Consumption
9 ideas, 5.75 USD, 64.7 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.80 | 4.7 |
| step4_backtest | 0.00 | 43.9 |
| step5_verdict | 1.40 | 5.3 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.g | 0.74 | 2.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 0.43 | 1.5 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 2.38 | 7.0 |
