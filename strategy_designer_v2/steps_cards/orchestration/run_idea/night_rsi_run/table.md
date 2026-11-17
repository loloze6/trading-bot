# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|
| 010-06_rsi-below-share-reversal | - | missing-components | - | - | - | 0.04 | 0.3 |
| 010-07_rsi-above-streak-reversal | - | missing-components | - | - | - | 0.04 | 0.3 |
| 010-08_rsi-below-streak-reversal | - | missing-components | - | - | - | 0.04 | 0.2 |
| 010-01_rsi-above-share-continuation | - | plan | inconclusive (+1.65) | not profitable enough (failed: Calmar) | 7.b: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins; 7.d: 010-01_rsi-above-share-continuation.d1_rsi-above-share-long-side, 010-01_rsi-above-share-continuation.d2_rsi-share-with-trend-agreement; 7.g: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets | 1.45 | 5.6 |
| 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins | 010-01_rsi-above-share-continuation | plan | inconclusive (-0.30) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | 7.b: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.b1_downtrend-rsi-below-share-rebound; 7.d: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.d1_rsi-stretch-exhausts-within-trend, 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.d2_distance-above-100-day-average; 7.g: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.g1_next-day-rebound-after-sharp-falls, 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.g2_seven-day-return-continuation | 1.39 | 6.8 |
| 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets | 010-01_rsi-above-share-continuation | plan | inconclusive (+0.00) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | 7.b: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets.b1_calm-market-rsi-level-continuation; 7.d: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets.d1_rsi-share-agreeing-with-momentum, 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets.d2_thirty-day-return-continuation; 7.g: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets.g1_calm-market-short-term-continuation, 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets.g2_volatile-market-next-day-reversal | 1.22 | 5.5 |
| 010-02_rsi-below-share-continuation | - | plan | inconclusive (+1.59) | not profitable enough (failed: Calmar) | 7.b: 010-02_rsi-below-share-continuation.b1_rsi-below-share-continuation-broader; 7.d: 010-02_rsi-below-share-continuation.d1_rsi-share-confirmed-by-trend, 010-02_rsi-below-share-continuation.d2_rsi-share-in-calm-markets; 7.g: 010-02_rsi-below-share-continuation.g1_one-day-volatility-scaled-reversal | 1.52 | 5.8 |
| 010-03_rsi-above-streak-continuation | - | plan | inconclusive (+1.48) | profitable enough | 7.b: 010-03_rsi-above-streak-continuation.b1_rsi-above-streak-six-coins, 010-03_rsi-above-streak-continuation.b2_rsi-above-streak-one-week-continuation; 7.e: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week, 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down; 7.g: no ideas: I looked at the streak, RSI level, past returns, volatility, range, weekday and the book's extreme days. No pattern stands out from chance given that many looks: the strongest is momentum at t ≈ 2.3–2.4 on overlapping tests, and it is present only in the later half of the windows. | 0.98 | 5.2 |
| 010-04_rsi-below-streak-continuation | - | plan | inconclusive (+1.28) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | 7.b: 010-04_rsi-below-streak-continuation.b1_rsi-level-predicts-week-ahead, 010-04_rsi-below-streak-continuation.b2_rsi-depth-below-midpoint; 7.d: 010-04_rsi-below-streak-continuation.d1_rsi-streak-shallow-decline-only, 010-04_rsi-below-streak-continuation.d2_deep-discount-rebounds; 7.g: 010-04_rsi-below-streak-continuation.g1_rsi-above-50-short-horizon-continuation | 1.10 | 5.8 |
| 010-05_rsi-above-share-reversal | - | plan | inconclusive (-1.43) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | 7.b: no ideas: The result runs weakly against the predicted reversal (t -1.43), is not graded by the share, and flips sign across years and volatility regimes (F1–F5). No part of the data shows the reversal clearly enough to narrow the idea to it, and more data on the same idea would only sharpen an effect on the wrong side.; 7.d: 010-05_rsi-above-share-reversal.d1_rsi-share-reversal-in-downtrends, 010-05_rsi-above-share-reversal.d2_rsi-dominance-continues-in-uptrends; 7.g: 010-05_rsi-above-share-reversal.g1_high-volatility-one-day-reversal | 1.20 | 5.9 |

## Consumption
10 ideas, 8.97 USD, 41.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.28 | 4.7 |
| step4_backtest | 0.00 | 9.9 |
| step5_verdict | 0.83 | 4.0 |
| step6_check | 0.00 | 0.1 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.30 | 0.9 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 1.90 | 6.2 |
| step7_7.g | 2.61 | 8.4 |
| step7_7.d | 2.06 | 7.1 |
