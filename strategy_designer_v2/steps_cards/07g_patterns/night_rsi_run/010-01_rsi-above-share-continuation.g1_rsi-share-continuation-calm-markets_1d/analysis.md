---
line: 7.g patterns
backtest: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets_1d
idea tested: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3676 USD
---
## Findings
- **F1:** In the calm regime (30-day volatility rank at or below its median), the coin's 7-day return scaled by its 30-day volatility predicts its next 7-day return: slope t 2.81 on 347 non-overlapping cases. The effect is similar for 3-day and 14-day lookbacks (t 2.86 and 2.96) and for a 3-day horizon (t 3.07, n 813). It holds in each coin separately (BTC t 1.94, n 171; ETH t 2.04, n 176) and stays positive on all seven grid offsets (t 1.10 to 2.85).
- **F2:** The same 7-day continuation is absent in the high-volatility regime (t -0.50, n 324), and the calm-minus-volatile slope difference has t 2.14. However, the calm-regime effect is uneven across years: 2018 has t 2.86 (n 51), while 2019, 2021 and 2023 have negative slopes (t -1.11, -0.50, -1.39). It is therefore weaker evidence than its pooled t suggests.
- **F3:** In the high-volatility regime, a coin's daily move scaled by its 30-day volatility reverses the next day. The bottom quintile of moves is followed by +0.63% (t 2.62, n 456) and the top quintile by -0.37% (t -2.14, n 472), falling steadily across the quintiles. In the calm regime the quintiles show no order (t -0.24 to 0.49), and pooled over all bars the slope t is -3.21 on 4834 one-day cases.
- **F4:** The tested signal, the share of the past 30 days with RSI above 50, carries no information on the 14-day grid in either regime (calm t 0.43, n 101; volatile t -0.33, n 91; BTC calm t -0.10, ETH calm t 0.59). The coin's own 30-day return predicts no better (calm t -0.22).
- **F5:** The book ran with only BTC and ETH, with no BNB data. Its mean daily return was 0.049% (BTC) and 0.053% (ETH), against 0.118% and 0.137% from holding the coins. Its 10% worst days (-2.9%) and 10% best days (+3.4%) came on coin days that averaged +0.24% and +0.37%. The book's extremes therefore come from its position sign more than from the coin's direction.
- **F6:** Other angles showed nothing that stands out after this many looks. Next 7-day returns by volatility quintile range from -1.1% to +0.7% with no order. Weekdays show only one t beyond 2 (Wednesday -0.39%, t -2.38) out of seven.

## Ideas
- `010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets.g1_calm-market-short-term-continuation` (from F1, F2, F4): When a coin's 30-day volatility is low relative to its own recent history, the larger its 7-day return measured against its 30-day volatility, the higher its return over the next 7 days.
- `010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets.g2_volatile-market-next-day-reversal` (from F3): When a coin's 30-day volatility is high relative to its own recent history, the larger its last day's return measured against its 30-day volatility, the lower its return over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
