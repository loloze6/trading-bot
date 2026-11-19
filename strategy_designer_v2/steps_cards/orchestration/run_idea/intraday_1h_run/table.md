# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 017-05_settlement-move-reverses-after | - | missing-components | - | - | - | - | 0.13 | 1.0 |
| 017-06_settlement-volume-rises-with-trend | - | untestable | - | - | - | - | 0.04 | 0.3 |
| 017-01_presettle-drop-after-uptrend | - | plan | inconclusive (+0.85) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 017-01_presettle-drop-after-uptrend.b1_pre-16-00-settlement-drop, 017-01_presettle-drop-after-uptrend.b2_weekday-us-open-uptrend-fade; 7.d: 017-01_presettle-drop-after-uptrend.d1_08-00-settlement-uptrend-fade, 017-01_presettle-drop-after-uptrend.d2_morning-reversal-of-3-day-rise; 7.g: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend, 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility | 1.34 | 15.1 |
| 017-03_postsettle-recovery-after-uptrend | - | plan | inconclusive (+1.39) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 017-03_postsettle-recovery-after-uptrend.b1_post-settlement-recovery-more-coins, 017-03_postsettle-recovery-after-uptrend.b2_16-00-settlement-recovery-after-rise, 017-03_postsettle-recovery-after-uptrend.b3_post-settlement-recovery-8-hours; 7.d: 017-03_postsettle-recovery-after-uptrend.d1_16-00-settlement-eight-hour-recovery, 017-03_postsettle-recovery-after-uptrend.d2_08-00-settlement-uptrend-giveback; 7.g: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal, 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal, 017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation, 017-03_postsettle-recovery-after-uptrend.g4_midday-trend-giveback | 1.61 | 15.7 |
| 017-04_postsettle-decline-after-downtrend | - | plan | rejected (-5.89) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours, 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls; 7.d: no ideas: The after-settlement decline the book bets on is real but too small to pay. It is about 4 to 6 bp over 2 hours against roughly 10 bp of fee per trade (F1, F2). Its only larger form, after 00:00 UTC over 6 hours, loses its grading by the 3-day fall (F4) and has faded since 2023 (F5). Its clock pattern also appears at non-settlement hours (F6). So no amendment of this idea, and no idea the findings support, would lift the book's gain above its fees.; 7.g: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls, 017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls, 017-04_postsettle-decline-after-downtrend.g3_afternoon-continuation-of-3-day-trend | 1.53 | 16.0 |
| 017-02_presettle-rise-after-downtrend | - | plan | inconclusive (+1.30) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 017-02_presettle-rise-after-downtrend.b1_pre-settlement-rise-more-coins, 017-02_presettle-rise-after-downtrend.b2_deep-fall-pre-settlement-rebound; 7.d: 017-02_presettle-rise-after-downtrend.d1_deep-fall-rebound-over-a-day, 017-02_presettle-rise-after-downtrend.d2_pre-midnight-settlement-trend-continuation; 7.g: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall, 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods, 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal | 1.35 | 14.9 |

## Consumption
6 ideas, 6.01 USD, 62.9 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.75 | 5.1 |
| step4_backtest | 0.00 | 37.0 |
| step5_verdict | 0.57 | 2.6 |
| step6_check | 0.00 | 0.6 |
| chart_files | 0.00 | 0.4 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.39 | 1.5 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 1.65 | 6.0 |
| step7_7.g | 1.54 | 5.6 |
| step7_7.b | 1.11 | 4.1 |
