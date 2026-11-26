# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 060-01_falling-calm-wide-high-close-fade | - | plan | inconclusive (+1.00) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 060-01.b1_falling-calm-high-close-fade; 7.g: no ideas: The patterns that are clearly there (F2, F3, F4) repeat strategies the profile map already holds. The remaining ones (F1, F5) do not stand out from chance once one counts the roughly 150 cuts examined across width, close location, today's return, trend, agitation, weekday, year, coin and window; F1's grading also reverses under a different swing ranking. | 1.11 | 12.6 |
| 060-01.b1_falling-calm-high-close-fade | 060-01_falling-calm-wide-high-close-fade | plan | inconclusive (+1.00) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 060-01.b1.b1_falling-calm-pinned-high-fade; 7.g: 060-01.b1.g1_falling-calm-rise-size-fade | 1.53 | 13.6 |

## Consumption
2 ideas, 2.64 USD, 26.2 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.20 | 1.2 |
| step4_backtest | 0.00 | 17.1 |
| step5_verdict | 0.60 | 2.2 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 0.75 | 2.2 |
| step7_7.g | 1.10 | 3.5 |
