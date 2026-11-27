# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 060-01_falling-calm-wide-high-close-fade | - | plan | inconclusive (+1.00) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 060-01.b1_falling-calm-high-close-fade; 7.g: no ideas: The patterns that are clearly there (F2, F3, F4) repeat strategies the profile map already holds. The remaining ones (F1, F5) do not stand out from chance once one counts the roughly 150 cuts examined across width, close location, today's return, trend, agitation, weekday, year, coin and window; F1's grading also reverses under a different swing ranking. | 1.11 | 12.6 |
| 060-01.b1_falling-calm-high-close-fade | 060-01_falling-calm-wide-high-close-fade | plan | inconclusive (+1.00) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 060-01.b1.b1_falling-calm-pinned-high-fade; 7.g: 060-01.b1.g1_falling-calm-rise-size-fade | 1.53 | 13.6 |
| 074-01_rising-calm-wide-low-close-rebound | - | plan | inconclusive (+1.93) | not profitable enough (failed: Calmar) | - | 7.b: 074-01.b1_low-close-nearness-rebound, 074-01.b2_three-day-low-close-rebound; 7.g: 074-01.g1_rising-calm-low-close-three-days | 1.11 | 13.0 |
| 074-01.b1_low-close-nearness-rebound | 074-01_rising-calm-wide-low-close-rebound | plan | confirmed (+2.31) | not profitable enough (failed: Trades per day) | - | 7.d: 074-01.b1.d1_wide-lower-close-calm-rebound; 7.g: 074-01.b1.g1_width-times-low-close-rebound | 1.14 | 12.9 |
| 074-01.b1.d1_wide-lower-close-calm-rebound | 074-01.b1_low-close-nearness-rebound | plan | inconclusive (+1.71) | not profitable enough (failed: Calmar) | - | 7.b: 074-01.b1.d1.b1_wide-day-nearer-low-rebounds, 074-01.b1.d1.b2_low-close-three-day-rebound; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.08 | 12.4 |
| 074-01.b1.g1_width-times-low-close-rebound | 074-01.b1_low-close-nearness-rebound | plan | inconclusive (+2.23) | not profitable enough (failed: Calmar, Trades per day) | - | 7.b: 074-01.b1.g1.b1_graded-wide-low-close-rebound; 7.g: no ideas: The tested idea's effect is confined to rising calm (F1), but its grading does not hold (F2). The other patterns that stand out either repeat the source brief (F3) or repeat rebounds the map already holds (F4). Nothing else stood out across profiles, the sign and size of the last day's move, volatility quartiles or weekdays (F5), so no new, ungraded-free idea is supported. | 1.08 | 13.0 |
| 074-01.b2_three-day-low-close-rebound | 074-01_rising-calm-wide-low-close-rebound | plan | inconclusive (+1.14) | not profitable enough (failed: Calmar) | - | 7.b: no ideas: The rebound is strong and present on every coin, year and sub-regime visible in folds B and C (F1, F2), yet it nets to about zero over all four folds. No condition read from a coin's bars at the close separates where it holds from where it reverses (F2, F4, F5), and the test already used all the data available (F6), so neither a narrower idea nor more data would give a clearer answer.; 7.g: 074-01.b2.g1_rising-calm-width-graded-rebound | 1.41 | 13.4 |
| 074-01.b1.d1.b1_wide-day-nearer-low-rebounds | 074-01.b1.d1_wide-lower-close-calm-rebound | plan | inconclusive (+1.71) | not profitable enough (failed: Calmar) | - | 7.b: 074-01.b1.d1.b1.b1_wide-low-close-three-day-rebound, 074-01.b1.d1.b1.b2_wide-day-pinned-low-rebound; 7.g: 074-01.b1.d1.b1.g1_wide-low-close-three-day-rebound, 074-01.b1.d1.b1.g2_rising-calm-wide-day-continuation | 1.11 | 12.7 |
| 075-01_heavy-volume-next-day-rise | - | plan | confirmed (+3.05) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.d: 075-01.d1_heavy-volume-down-day-rebound, 075-01.d2_heavy-volume-fall-two-day-rebound, 075-01.d3_heavy-volume-deep-fall-rebound; 7.g: 075-01.g1_heavy-volume-down-day-rebound, 075-01.g2_light-volume-up-day-fade | 1.02 | 12.0 |
| 075-01.d1_heavy-volume-down-day-rebound | 075-01_heavy-volume-next-day-rise | plan | confirmed (+5.81) | not profitable enough (failed: Calmar) | - | 7.d: 075-01.d1.d1_heavy-volume-deep-fall-rebound; 7.g: 075-01.d1.g2_heavy-volume-after-fall-rebound | 1.15 | 11.8 |
| 075-01.d2_heavy-volume-fall-two-day-rebound | 075-01_heavy-volume-next-day-rise | plan | confirmed (+2.47) | not profitable enough (failed: Calmar) | - | 7.d: 075-01.d2.d1_extreme-volume-down-day-rebound, 075-01.d2.d2_rising-market-heavy-volume-dip-rebound, 075-01.d2.d3_heavy-volume-fall-five-day-rebound; 7.g: 075-01.d2.g1_rising-market-heavy-volume-dip | 1.12 | 12.6 |
| 061-01_falling-calm-rally-fade | - | plan | inconclusive (-0.60) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: the theme's effect is not in the data. Inside falling calm markets a sharp rise is followed by no larger fall than a flat or small-fall day (F2), the fade does not grow with the rise (F3), and it appears only in some years and windows, with opposite signs elsewhere (F4). No condition, side or horizon isolates it (F5).; 7.g: no ideas: The tested rally fade is only the falling calm market's own next-day drift (F1, F2). The one pattern that stands out, the graded next-day rebound after scaled falls and low closes outside falling calm (F3, F4), is already held in the map's agitated and falling agitated long cells (038-01, 047-01, 051-01, 045-01, 039-02). Nothing else stands out among the angles examined (F5). | 1.06 | 12.1 |
| 060-02_falling-calm-close-above-low-fade | - | plan | mismatch | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.g: 0 ideas, 1 discoveries (3 explorations) | 0.96 | 12.6 |

## Consumption
13 ideas, 14.88 USD, 164.6 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.33 | 7.8 |
| step4_backtest | 0.00 | 112.6 |
| step5_verdict | 2.70 | 9.7 |
| step6_check | 0.00 | 0.7 |
| chart_files | 0.00 | 0.3 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 1.71 | 5.5 |
| step7_7.b | 3.22 | 9.4 |
| step7_7.g | 5.92 | 18.2 |
| similarity_check | 0.00 | 0.3 |
