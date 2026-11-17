---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets
line: 7.g patterns
backtest: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 30-day volatility is low relative to its own recent history, the larger its 7-day return measured against its 30-day volatility, the higher its return over the next 7 days.
Consequence: In calm markets, follow the coin's last week's move in proportion to its size, rather than the RSI-share reading.
Why:
- F1: In the calm regime (30-day volatility rank at or below its median), the coin's 7-day return scaled by its 30-day volatility predicts its next 7-day return: slope t 2.81 on 347 non-overlapping cases. The effect is similar for 3-day and 14-day lookbacks (t 2.86 and 2.96) and for a 3-day horizon (t 3.07, n 813). It holds in each coin separately (BTC t 1.94, n 171; ETH t 2.04, n 176) and stays positive on all seven grid offsets (t 1.10 to 2.85).
- F2: The same 7-day continuation is absent in the high-volatility regime (t -0.50, n 324), and the calm-minus-volatile slope difference has t 2.14. However, the calm-regime effect is uneven across years: 2018 has t 2.86 (n 51), while 2019, 2021 and 2023 have negative slopes (t -1.11, -0.50, -1.39). It is therefore weaker evidence than its pooled t suggests.
- F4: The tested signal, the share of the past 30 days with RSI above 50, carries no information on the 14-day grid in either regime (calm t 0.43, n 101; volatile t -0.33, n 91; BTC calm t -0.10, ETH calm t 0.59). The coin's own 30-day return predicts no better (calm t -0.22).
