# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week | 026-03_weekend-reversal-exceeds-weekday | plan | confirmed (+4.57) | not profitable enough (failed: Calmar) | - | 7.d: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets, 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue; 7.g: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.g1_sunday-move-reverses-early-week, 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.g2_saturday-minus-sunday-spread | 1.85 | 10.6 |
| 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue | 026-04_thinner-weekend-larger-reversal | missing-components | - | - | - | - | 0.09 | 0.6 |
| 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets | 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week | plan | confirmed (+4.14) | not profitable enough (failed: Calmar) | - | 7.d: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend, 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d2_calm-up-saturday-continues-higher; 7.g: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.g1_sunday-reversal-in-volatile-markets, 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.g2_saturday-continues-sunday-reverses, 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.g3_evening-rebound-after-daily-falls | 1.51 | 27.6 |
| 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue | 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week | plan | inconclusive (+0.80) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week; 7.g: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.g1_volatile-one-day-moves-reverse, 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.g2_deep-daily-falls-rebound, 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.g3_late-evening-utc-drift | 1.07 | 9.3 |
| 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week | 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue | plan | confirmed (+2.56) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.d: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d1_sunday-reversal-grows-with-volatility, 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday, 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d3_sunday-rises-fade-in-turbulence; 7.g: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.g1_volatility-scaled-daily-reversal, 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.g2_sunday-reversal-in-volatility, 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.g3_late-evening-rise-after-falls | 1.12 | 9.8 |

## Consumption
5 ideas, 5.65 USD, 58.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.20 | 4.0 |
| step4_backtest | 0.00 | 37.4 |
| step5_verdict | 0.67 | 2.5 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.3 |
| similarity_check | 0.00 | 0.4 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 0.36 | 1.3 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 1.39 | 5.1 |
| step7_7.g | 2.03 | 6.9 |
