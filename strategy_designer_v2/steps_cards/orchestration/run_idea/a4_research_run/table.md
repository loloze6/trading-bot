# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 060-01_falling-agitated-high-close-fade | - | plan | inconclusive (+0.78) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 060-01.b1_falling-agitated-high-close-fade-wider; 7.g: no ideas: The only pattern that clears chance after this many angles is the next-day rebound after the weakest days in falling agitated markets (F3), which the profile map already holds with 16 strategies; the tested idea's own fade is not graded (F1, F2), and the down-day high-close fade (F4) is too thin and ungraded to stand out. | 0.85 | 13.7 |
| 060-01.b1_falling-agitated-high-close-fade-wider | 060-01_falling-agitated-high-close-fade | plan | inconclusive (+1.01) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The theme's effect is not in the data: no more daily data is available, the next-day fade after an upper-range close is ungraded or inverted in the strongest cases (F1), it is about as present outside the falling-agitated profile (F2), and it fades across years and coins (F3) with no horizon where it shows (F4), so no amendment on the theme has a finding to rest on.; 7.g: 060-01.b1.g1_quiet-day-next-fade | 0.84 | 13.8 |
| 060-01.b1.g1_quiet-day-next-fade | 060-01.b1_falling-agitated-high-close-fade-wider | plan | inconclusive (-1.26) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 060-01.b1.g1.b1_falling-agitated-flat-day-fade; 7.g: no ideas: Across about ten angles (scaled move, close location, range, 5-day and 30-day returns, swing ratio, weekday, coin), no pattern reaches a day-pooled |t| of 2.5. Those near 2 are either not graded (F4, F5), already held in the map (the agitated big-fall and wide-range rebounds behind F2 and F3, the falling-agitated high-close fade in F6), or smaller than the 0.32 % cost of a trade (F1). | 1.86 | 10.2 |

## Consumption
3 ideas, 3.55 USD, 37.7 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.21 | 2.4 |
| step4_backtest | 0.00 | 27.8 |
| step5_verdict | 0.50 | 1.8 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 0.73 | 2.4 |
| step7_7.g | 1.11 | 3.2 |
