# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 060-01_falling-calm-wide-high-close-fade | - | plan | inconclusive (+1.00) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 060-01.b1_falling-calm-high-close-fade; 7.g: no ideas: The patterns that are clearly there (F2, F3, F4) repeat strategies the profile map already holds. The remaining ones (F1, F5) do not stand out from chance once one counts the roughly 150 cuts examined across width, close location, today's return, trend, agitation, weekday, year, coin and window; F1's grading also reverses under a different swing ranking. | 1.11 | 12.6 |
| 060-01.b1_falling-calm-high-close-fade | 060-01_falling-calm-wide-high-close-fade | plan | inconclusive (+1.00) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 060-01.b1.b1_falling-calm-pinned-high-fade; 7.g: 060-01.b1.g1_falling-calm-rise-size-fade | 1.53 | 13.6 |
| 074-01_rising-calm-wide-low-close-rebound | - | plan | inconclusive (+1.93) | not profitable enough (failed: Calmar) | - | 7.b: 074-01.b1_low-close-nearness-rebound, 074-01.b2_three-day-low-close-rebound; 7.g: 074-01.g1_rising-calm-low-close-three-days | 1.11 | 13.0 |
| 074-01.b1_low-close-nearness-rebound | 074-01_rising-calm-wide-low-close-rebound | plan | confirmed (+2.31) | not profitable enough (failed: Trades per day) | - | 7.d: 074-01.b1.d1_wide-lower-close-calm-rebound; 7.g: 074-01.b1.g1_width-times-low-close-rebound | 1.14 | 12.9 |
| 074-01.b1.d1_wide-lower-close-calm-rebound | 074-01.b1_low-close-nearness-rebound | plan | inconclusive (+1.71) | not profitable enough (failed: Calmar) | - | 7.b: 074-01.b1.d1.b1_wide-day-nearer-low-rebounds, 074-01.b1.d1.b2_low-close-three-day-rebound; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.08 | 12.4 |

## Consumption
5 ideas, 5.97 USD, 64.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.52 | 3.1 |
| step4_backtest | 0.00 | 44.0 |
| step5_verdict | 1.17 | 4.2 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.41 | 1.2 |
| step7_7.b | 1.50 | 4.2 |
| step7_7.g | 2.37 | 7.4 |
| similarity_check | 0.00 | 0.1 |
