# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 022-04_signal-weights-carry-forward | - | missing-components | - | - | - | - | 0.05 | 0.4 |
| 022-01_learned-combined-signal-score | - | plan | inconclusive (-1.83) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls; 7.d: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score, 022-01_learned-combined-signal-score.d2_four-week-momentum-alone, 022-01_learned-combined-signal-score.d3_large-day-precedes-rise; 7.g: no ideas: Across the 25 signal quintiles, the weekday-by-coin, by-year and by-volatility tables, the persistence check and the large-move bins, nothing is graded and stands out from chance. The one strong pattern, the weekday effect in F5, is a fixed calendar condition that is neither graded nor stable across years and volatility levels, so it cannot be written as a graded idea. | 1.81 | 9.9 |
| 022-02_combination-beats-best-single | - | plan | inconclusive (+0.21) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days; 7.d: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends, 022-02_combination-beats-best-single.d2_28-day-momentum-5-day-horizon, 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility; 7.g: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week, 022-02_combination-beats-best-single.g2_saturday-drift-scaled-by-week | 1.46 | 12.2 |
| 022-03_combined-extremes-larger-moves | - | plan | inconclusive (-1.01) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days; 7.d: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue; 7.g: 022-03_combined-extremes-larger-moves.g1_large-up-days-keep-rising, 022-03_combined-extremes-larger-moves.g2_violent-days-precede-gains | 1.62 | 16.7 |

## Consumption
4 ideas, 4.94 USD, 39.2 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.80 | 3.0 |
| step4_backtest | 0.00 | 22.5 |
| step5_verdict | 0.41 | 1.5 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 1.10 | 3.9 |
| step7_7.g | 1.48 | 4.5 |
| step7_7.b | 1.15 | 3.6 |
