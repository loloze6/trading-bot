# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 017-05_settlement-move-reverses-after | - | plan | confirmed (+5.12) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day, 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses, 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours; 7.g: 017-05_settlement-move-reverses-after.g1_one-day-large-move-reversal, 017-05_settlement-move-reverses-after.g2_reversal-in-volatility-bursts, 017-05_settlement-move-reverses-after.g3_us-open-move-reversal, 017-05_settlement-move-reverses-after.g4_intraday-move-reverses-next-day | 1.22 | 10.4 |
| 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods | 017-02_presettle-rise-after-downtrend | plan | confirmed (+13.77) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours, 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls, 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours; 7.g: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.g1_daily-fade-in-volatility-spikes, 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.g2_late-evening-utc-drift | 1.03 | 14.9 |
| 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility | 017-01_presettle-drop-after-uptrend | plan | confirmed (+12.28) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.d: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day, 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily; 7.g: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.g1_volatile-day-move-reversal | 1.20 | 15.5 |

## Consumption
3 ideas, 3.45 USD, 40.9 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.22 | 1.3 |
| step4_backtest | 0.00 | 23.4 |
| step5_verdict | 0.49 | 2.0 |
| step6_check | 0.00 | 2.3 |
| chart_files | 0.00 | 0.5 |
| similarity_check | 0.00 | 0.4 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.g | 1.20 | 5.1 |
| step7_7.d | 1.55 | 5.9 |
