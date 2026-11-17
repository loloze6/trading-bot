# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|
| 010-04_rsi-below-streak-continuation | - | missing-components | - | - | - | 0.04 | 0.3 |
| 010-05_rsi-above-share-reversal | - | missing-components | - | - | - | 0.04 | 0.3 |
| 010-06_rsi-below-share-reversal | - | missing-components | - | - | - | 0.04 | 0.3 |
| 010-07_rsi-above-streak-reversal | - | missing-components | - | - | - | 0.04 | 0.3 |
| 010-08_rsi-below-streak-reversal | - | missing-components | - | - | - | 0.04 | 0.2 |
| 010-01_rsi-above-share-continuation | - | plan | inconclusive (+1.65) | not profitable enough (failed: Calmar) | 7.b: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins; 7.d: 010-01_rsi-above-share-continuation.d1_rsi-above-share-long-side, 010-01_rsi-above-share-continuation.d2_rsi-share-with-trend-agreement; 7.g: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets | 1.45 | 5.6 |
| 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins | 010-01_rsi-above-share-continuation | plan | inconclusive (-0.30) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, Calmar) | 7.b: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.b1_downtrend-rsi-below-share-rebound; 7.d: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.d1_rsi-stretch-exhausts-within-trend, 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.d2_distance-above-100-day-average; 7.g: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.g1_next-day-rebound-after-sharp-falls, 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.g2_seven-day-return-continuation | 1.39 | 6.8 |
| 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets | 010-01_rsi-above-share-continuation | plan | inconclusive (+0.00) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | 7.b: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets.b1_calm-market-rsi-level-continuation; 7.d: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets.d1_rsi-share-agreeing-with-momentum, 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets.d2_thirty-day-return-continuation; 7.g: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets.g1_calm-market-short-term-continuation, 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets.g2_volatile-market-next-day-reversal | 1.22 | 5.5 |
| 010-02_rsi-below-share-continuation | - | plan | inconclusive (+1.59) | not profitable enough (failed: Calmar) | 7.b: 010-02_rsi-below-share-continuation.b1_rsi-below-share-continuation-broader; 7.d: 010-02_rsi-below-share-continuation.d1_rsi-share-confirmed-by-trend, 010-02_rsi-below-share-continuation.d2_rsi-share-in-calm-markets; 7.g: 010-02_rsi-below-share-continuation.g1_one-day-volatility-scaled-reversal | 1.52 | 5.8 |
| 010-03_rsi-above-streak-continuation | - | plan | inconclusive (+1.48) | profitable enough | 7.b: 010-03_rsi-above-streak-continuation.b1_rsi-above-streak-six-coins, 010-03_rsi-above-streak-continuation.b2_rsi-above-streak-one-week-continuation; 7.e: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week, 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down; 7.g: no ideas: I looked at the streak, RSI level, past returns, volatility, range, weekday and the book's extreme days. No pattern stands out from chance given that many looks: the strongest is momentum at t ≈ 2.3–2.4 on overlapping tests, and it is present only in the later half of the windows. | 0.98 | 5.2 |

## Consumption
10 ideas, 6.76 USD, 30.3 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.17 | 3.9 |
| step4_backtest | 0.00 | 7.3 |
| step5_verdict | 0.59 | 2.8 |
| step6_check | 0.00 | 0.1 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.30 | 0.9 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 1.35 | 4.3 |
| step7_7.g | 1.88 | 5.9 |
| step7_7.d | 1.47 | 4.9 |
