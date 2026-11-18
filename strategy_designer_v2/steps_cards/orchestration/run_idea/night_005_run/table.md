# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|
| 005-01_bearish-rsi-divergence-giveback | - | missing-components | - | - | - | 0.04 | 0.3 |
| 005-02_bullish-rsi-divergence-rebound | - | plan | inconclusive (-1.35) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | 7.b: no ideas: The divergence result is on the opposite side of the idea, its size does not grade the following return (F2), and no coin, year, trend, volatility regime or horizon shows a clear rebound that new lows without a divergence lack (F3, F4), so no amended idea has support.; 7.d: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence, 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling; 7.g: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal | 1.71 | 5.9 |
| 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal | 005-02_bullish-rsi-divergence-rebound | plan | confirmed (+3.80) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | 7.d: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.d1_fade-rises-only-in-downtrends, 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.d2_volatile-sharp-fall-rebound; 7.g: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation, 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly | 1.02 | 5.0 |
| 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation | 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal | missing-components | - | - | - | 0.07 | 0.5 |

## Consumption
4 ideas, 2.84 USD, 11.7 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.65 | 2.4 |
| step4_backtest | 0.00 | 2.2 |
| step5_verdict | 0.25 | 1.2 |
| step6_check | 0.00 | 0.0 |
| chart_files | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 0.30 | 0.8 |
| step7_7.d | 0.67 | 2.2 |
| step7_7.g | 0.97 | 2.9 |
