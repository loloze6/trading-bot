# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 017-02_presettle-rise-after-downtrend | - | missing-components | - | - | - | - | 0.05 | 0.3 |
| 017-03_postsettle-recovery-after-uptrend | - | missing-components | - | - | - | - | 0.12 | 0.8 |
| 017-04_postsettle-decline-after-downtrend | - | missing-components | - | - | - | - | 0.06 | 0.4 |
| 017-05_settlement-move-reverses-after | - | missing-components | - | - | - | - | 0.13 | 1.0 |
| 017-06_settlement-volume-rises-with-trend | - | untestable | - | - | - | - | 0.04 | 0.3 |
| 017-01_presettle-drop-after-uptrend | - | plan | inconclusive (+0.85) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 017-01_presettle-drop-after-uptrend.b1_pre-16-00-settlement-drop, 017-01_presettle-drop-after-uptrend.b2_weekday-us-open-uptrend-fade; 7.d: 017-01_presettle-drop-after-uptrend.d1_08-00-settlement-uptrend-fade, 017-01_presettle-drop-after-uptrend.d2_morning-reversal-of-3-day-rise; 7.g: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend, 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility | 1.34 | 15.1 |

## Consumption
6 ideas, 1.74 USD, 17.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.52 | 3.5 |
| step4_backtest | 0.00 | 9.2 |
| step5_verdict | 0.15 | 0.7 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.32 | 1.3 |
| step7_7.g | 0.37 | 1.4 |
| step7_7.b | 0.37 | 1.5 |
