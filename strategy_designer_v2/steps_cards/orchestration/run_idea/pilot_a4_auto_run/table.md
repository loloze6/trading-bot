# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 061-01_falling-calm-scaled-rise-fade | - | plan | no effect (-1.44) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 061-01.c1_falling-calm-scaled-fall-rebound, 061-01.c2_falling-calm-rise-continuation | 0.71 | 8.3 |
| 064-01_falling-calm-up-day-fades | - | plan | no effect (+0.45) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 064-01.c1_calm-decline-big-rise-follows-through, 064-01.c2_calm-decline-bounce-extends-week | 0.56 | 7.6 |
| 086-01_heavy-volume-up-day-continuation | - | plan | no effect (+0.82) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.c: no ideas: The theme's effect is not in the data. In falling calm markets, heavy-volume up days are followed by no more rise than light-volume ones at 1 to 10 days (F1, F6), and volume does not grade the later move (F2). The only positive result comes from DOGE in two 2021 windows, while BTC and XMR kept falling after up days of every kind (F3, F4, F5). That leaves no long-side variation on this theme a trader could act on. | 0.66 | 8.1 |
| 050-02_falling-calm-scaled-week-rise-continuation | - | plan | inconclusive (+1.50) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 050-02.b1_calm-downtrend-week-rise-continuation-more-coins | 0.48 | 7.5 |

## Consumption
4 ideas, 2.40 USD, 31.5 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.39 | 2.4 |
| step4_backtest | 0.00 | 22.3 |
| step5_verdict | 0.73 | 2.8 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.g | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 0.21 | 0.8 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 1.07 | 3.1 |
