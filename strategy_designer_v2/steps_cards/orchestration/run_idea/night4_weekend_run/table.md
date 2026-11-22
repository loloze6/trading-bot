# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 026-01_weekend-rise-reverses-early-week | - | plan | inconclusive (-0.10) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The tested result is zero (t -0.10) and there is nothing to narrow it to. No horizon, side, size, coin, year or regime shows a steady reversal after a weekend gain that is graded with the gain (F2, F4, F5, F6). Weekend gains behave like midweek gains (F3), and the one significant pattern, the continuation of small weekend falls, shrinks as the fall grows (F7).; 7.d: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues, 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks; 7.g: 026-01_weekend-rise-reverses-early-week.g1_volatile-day-moves-reverse-next-day, 026-01_weekend-rise-reverses-early-week.g2_volatile-sell-off-next-day-rebound | 1.51 | 12.9 |
| 026-02_weekend-drop-reverses-early-week | - | plan | rejected (-2.18) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 026-02_weekend-drop-reverses-early-week.c1_sunday-rally-fades-early-week, 026-02_weekend-drop-reverses-early-week.c2_sunday-move-reverses-midweek, 026-02_weekend-drop-reverses-early-week.c3_saturday-move-continues-midweek; 7.d: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue, 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week, 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends; 7.g: 026-02_weekend-drop-reverses-early-week.g1_late-evening-rebound-after-falls, 026-02_weekend-drop-reverses-early-week.g2_late-evening-rise-after-turbulence, 026-02_weekend-drop-reverses-early-week.g3_midweek-rise-carries-into-weekend | 1.55 | 12.6 |
| 026-03_weekend-reversal-exceeds-weekday | - | plan | inconclusive (+0.84) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend; 7.d: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week, 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday, 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week; 7.g: 026-03_weekend-reversal-exceeds-weekday.g1_high-volatility-daily-move-reverses | 1.48 | 13.0 |
| 026-04_thinner-weekend-larger-reversal | - | missing-components | - | - | - | - | 0.08 | 0.7 |
| 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend | 026-03_weekend-reversal-exceeds-weekday | plan | confirmed (+3.03) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | - | 7.d: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend.d1_midweek-rises-carry-into-weekend, 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend.d2_trend-aligned-midweek-move-continues, 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend.d3_sharp-two-day-falls-rebound; 7.g: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend.g1_midweek-rises-run-into-weekend, 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend.g2_evening-rebound-after-day-s-fall | 0.97 | 10.8 |
| 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues | 026-01_weekend-rise-reverses-early-week | plan | confirmed (+3.13) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | - | 7.d: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues.d1_weekend-extends-weekly-trend, 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues.d2_calm-weekly-rise-continues; 7.g: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues.g1_late-evening-rebound-after-afternoon-fall, 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues.g2_turbulent-daily-moves-reverse, 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues.g3_calm-mid-week-move-continues | 1.05 | 19.5 |
| 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue | 026-02_weekend-drop-reverses-early-week | missing-components | - | - | - | - | 0.09 | 0.6 |

## Consumption
7 ideas, 6.72 USD, 70.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.64 | 4.5 |
| step4_backtest | 0.00 | 42.2 |
| step5_verdict | 0.84 | 3.6 |
| step6_check | 0.00 | 0.3 |
| chart_files | 0.00 | 0.5 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.57 | 1.8 |
| step7_7.b | 0.70 | 2.5 |
| step7_7.g | 1.98 | 7.4 |
| step7_7.d | 2.00 | 7.2 |
