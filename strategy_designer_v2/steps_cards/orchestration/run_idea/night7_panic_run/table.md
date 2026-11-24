# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_monthly-low-break-cascade | - | plan | inconclusive (-1.97) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 032-01.b1_monthly-low-exhaustion-rebound; 7.g: 032-01.g1_monthly-low-exhaustion-rebound, 032-01.g2_monthly-low-closing-off-lows | 1.78 | 6.4 |
| 033-01_rising-market-sharp-drop-rebound | - | plan | inconclusive (+1.11) | not profitable enough (failed: Calmar) | - | 7.b: 033-01.b1_rising-market-dip-rebound-more-coins; 7.g: 033-01.g1_calm-uptrend-dip-rebound | 1.00 | 5.0 |
| 034-01_falling-market-rally-fade | - | plan | inconclusive (+0.05) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 034-01.b1_agitated-downtrend-rally-fade, 034-01.b2_next-day-agitated-rally-fade; 7.g: 0 ideas, 2 discoveries (2 explorations) | 1.21 | 5.7 |
| 035-01_rising-market-quieting-swings-rise | - | plan | inconclusive (+0.61) | not profitable enough (failed: Calmar) | - | 7.b: 035-01.b1_quieting-swings-more-coins; 7.g: 0 ideas, 1 discoveries (2 explorations) | 0.85 | 4.7 |
| 036-01_scaled-rally-week-continuation | - | plan | inconclusive (-0.67) | not profitable enough (failed: Calmar) | - | 7.b: 036-01.b1_calm-market-rally-two-week-continuation; 7.g: 036-01.g1_scaled-two-week-rally-continues, 036-01.g2_scaled-weekly-rally-continues | 1.03 | 5.4 |
| 037-01_falling-market-wide-day-decline | - | missing-components | - | - | - | - | 0.06 | 0.3 |

## Consumption
6 ideas, 5.94 USD, 27.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.23 | 2.9 |
| step4_backtest | 0.00 | 9.5 |
| step5_verdict | 0.88 | 3.3 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 1.69 | 5.2 |
| step7_7.g | 2.14 | 6.3 |
