# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|
| 005-01_bearish-rsi-divergence-giveback | - | missing-components | - | - | - | 0.04 | 0.3 |
| 005-02_bullish-rsi-divergence-rebound | - | plan | inconclusive (-1.35) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | 7.b: no ideas: The divergence result is on the opposite side of the idea, its size does not grade the following return (F2), and no coin, year, trend, volatility regime or horizon shows a clear rebound that new lows without a divergence lack (F3, F4), so no amended idea has support.; 7.d: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence, 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling; 7.g: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal | 1.71 | 5.9 |
| 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal | 005-02_bullish-rsi-divergence-rebound | plan | confirmed (+3.80) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | 7.d: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.d1_fade-rises-only-in-downtrends, 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.d2_volatile-sharp-fall-rebound; 7.g: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation, 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly | 1.02 | 5.0 |
| 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation | 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal | missing-components | - | - | - | 0.07 | 0.5 |
| 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly | 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal | plan | confirmed (+3.50) | profitable enough | 7.g: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound, 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g2_volatile-rise-slow-giveback | 0.69 | 3.7 |
| 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence | 005-02_bullish-rsi-divergence-rebound | plan | inconclusive (-1.56) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | 7.b: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling; 7.d: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.d1_divergence-five-day-bounce, 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.d2_divergence-low-continues-falling; 7.g: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal | 1.26 | 5.5 |
| 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal | 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence | plan | confirmed (+3.66) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | 7.d: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.d1_counter-trend-volatile-day-reversal, 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.d2_volatility-expansion-graded-one-day-reversal; 7.g: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal, 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g2_volatile-down-day-rebound, 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g3_calm-spell-three-day-continuation | 0.87 | 4.4 |
| 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling | 005-02_bullish-rsi-divergence-rebound | plan | inconclusive (-0.81) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | 7.b: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.b1_shallow-new-lows-more-coins; 7.d: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.d1_shallow-lows-near-trend, 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.d2_sharp-drops-rebound-instead, 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.d3_near-highs-keep-rising; 7.g: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal | 1.11 | 5.6 |

## Consumption
8 ideas, 6.77 USD, 30.9 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.01 | 5.0 |
| step4_backtest | 0.00 | 6.3 |
| step5_verdict | 0.75 | 3.5 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 0.67 | 2.1 |
| step7_7.d | 1.68 | 5.8 |
| step7_7.g | 2.66 | 8.1 |
