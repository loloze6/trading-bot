---
line: 7.b inconclusive
backtest: 010-02_rsi-below-midpoint-continues-down_1d
idea tested: 010-02_rsi-below-midpoint-continues-down
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2529 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts but short of the bar: a pooled 7-day slope t of 1.82 on 815 non-overlapping cases. Only BTC and ETH ran (BNB is absent), and both coins point the same way without reaching the bar on their own (BTC t 0.90 on 408 cases, ETH t 1.61 on 407 cases), so the test is short of cases rather than wrong in sign.
- **F2:** The effect is mixed over time and leans on one year. At 7 days the slope t by year is 2.87 in 2025 but between -0.98 and +0.59 in every other year, with 2022 to 2024 all negative. Without 2025 the pooled 7-day t falls to 1.16 on 713 cases, and only 42% of windows have a positive slope.
- **F3:** The same forecast is clearer at shorter horizons, where there are more independent cases. The pooled slope t is 2.65 at 1 day (5,794 cases) and 2.48 at 3 days (1,907 cases), against 1.82 at 7 days and 1.03 at 14 days. Without 2025 it is still 2.14 at 1 day (5,070 cases).
- **F4:** The extremes carry the effect, and both sides contribute.
- **F5:** The book's timing gain before costs is positive (0.00092 a day), and its Sharpe is 0.82, which beats holding by 0.18. The forecast's direction therefore earns, but its size is small relative to 7-day coin moves of about 11%.

## Ideas
- `010-02_rsi-below-midpoint-continues-down.b1_rsi-below-share-more-coins` (from F1, F2, F5): The larger the share of the past 14 days that a coin's 14-day RSI has spent below its midpoint, the larger the coin's fall over the next 7 days.
- `010-02_rsi-below-midpoint-continues-down.b2_rsi-below-share-next-day` (from F3, F4): The larger the share of the past 14 days that a coin's 14-day RSI has spent below its midpoint, the larger the coin's fall over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
