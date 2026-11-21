# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 022-02_combination-beats-best-single | - | missing-components | - | - | - | - | 0.05 | 0.3 |
| 022-03_combined-extremes-larger-moves | - | missing-components | - | - | - | - | 0.04 | 0.3 |
| 022-04_signal-weights-carry-forward | - | missing-components | - | - | - | - | 0.05 | 0.4 |
| 022-01_learned-combined-signal-score | - | plan | inconclusive (-1.83) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls; 7.d: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score, 022-01_learned-combined-signal-score.d2_four-week-momentum-alone, 022-01_learned-combined-signal-score.d3_large-day-precedes-rise; 7.g: no ideas: Across the 25 signal quintiles, the weekday-by-coin, by-year and by-volatility tables, the persistence check and the large-move bins, nothing is graded and stands out from chance. The one strong pattern, the weekday effect in F5, is a fixed calendar condition that is neither graded nor stable across years and volatility levels, so it cannot be written as a graded idea. | 1.81 | 9.9 |

## Consumption
4 ideas, 1.95 USD, 10.9 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.62 | 1.8 |
| step4_backtest | 0.00 | 4.5 |
| step5_verdict | 0.12 | 0.4 |
| step6_check | 0.00 | 0.0 |
| chart_files | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.35 | 1.3 |
| step7_7.g | 0.37 | 1.3 |
| step7_7.b | 0.49 | 1.6 |
