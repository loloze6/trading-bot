---
line: 7.g patterns
backtest: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins_1d
idea tested: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3306 USD
---
## Findings
- **F1:** The coin's own one-day move reverses the next day: across all six coins, the next-day excess return is +0.88% after a fall of 2 or more 30-day standard deviations (t 3.09, n 430) and +0.51% after a fall of 1 to 2 (t 3.45, n 1280), against +0.04% after one of 1 to 2 up (n 1391); the slope of the next-day excess return on the scaled move has t -4.76.
- **F2:** This rebound after falls of 1 or more standard deviations is positive in all six coins (XMR +1.03% t 3.64, ZEC +0.80% t 2.20, XRP +0.74% t 1.97, BTC +0.32% t 1.26) and in 7 of 8 years (2021 +1.56% t 3.42, 2020 +1.40% t 2.90, 2023 +0.56% t 2.43; 2025 -0.11% t -0.33).
- **F3:** Over the next 14 days, the coin's past 7-day return carries forward, not reverses: pooled slope t 3.42 (1008 non-overlapping cases), 2.97 when the past return is scaled by volatility and 2.95 when winsorised; the top past-7-day quintile earns +4.1% excess against -4.6% in the bottom quintile.
- **F4:** That 7-day continuation is positive in 5 of 6 coins (ZEC t 2.41, ETH 1.85, BTC 1.64; LTC 0.00) but rests mostly on 2025 (t 5.14); 2018 to 2023 range from t -0.49 to 0.93, so it is weaker evidence than F1.
- **F5:** The tested RSI-share forecast predicts nothing: slope t -0.30 on the forecast and -0.73 on the raw share (1152 cases); its quintiles' 14-day excess returns run from -0.69% to +0.71% with no order; per coin it splits, from XRP t -2.85 to BTC t +1.15.
- **F6:** The book's small gain is not from riding the market: mean gain 0.000363 per day against a market part of -0.000024, with a mean position of -0.017 and 45% of bars long; it lost in 2023 (-0.00092) and 2024 (-0.00026).
- **F7:** Saturday's excess return is +0.34% (t 4.09, n 2484), positive in all six coins and in 6 of 8 years, but it comes from a weekday scan of seven days and is a calendar effect with no grading.

## Ideas
- `010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.g1_next-day-rebound-after-sharp-falls` (from F1, F2): The larger a coin's one-day fall, measured against its own daily volatility over the past 30 days, the higher its return over the next 1 day.
- `010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.g2_seven-day-return-continuation` (from F3, F4, F5): The higher a coin's return over the past 7 days, the higher its return over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
