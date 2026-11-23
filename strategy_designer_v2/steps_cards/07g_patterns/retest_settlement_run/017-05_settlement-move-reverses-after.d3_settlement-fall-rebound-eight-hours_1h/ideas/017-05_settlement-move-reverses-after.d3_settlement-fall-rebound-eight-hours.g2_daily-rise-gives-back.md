---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the next 24 hours runs opposite to a rise over the coin's past 24 hours: the larger that 24-hour rise against the coin's usual 24-hour move, the larger the fall that follows. The fall is larger when the coin's past 30-day hourly volatility is high.
Consequence: A trader sells or shorts a coin after an unusually large 24-hour run-up in a volatile market for one day, and refuses to chase such a run-up with a long.
Why:
- F5: A 24h rise is also followed by a 24h move below drift, so the effect runs on both sides. The top quintile of 24h moves gives an excess of −0.33 % (t −3.5) and a total of −0.19 %. In high volatility it gives an excess of −0.73 % (t −3.3) and a total of −0.59 %. The middle quintiles sit between −0.06 % and −0.17 %, so the grading is clear only at the extremes.
- F3: The rebound is concentrated where volatility is high. By the coin's 30-day hourly volatility tercile, the slope t is +0.24, −2.66 and −9.28. In the high-volatility tercile, the bottom quintile of 24h moves (933 cases) is followed by an excess of +1.45 % (t 5.7) and a total of +1.59 %, about 8 times the cost.
- F2: The 24h-fall rebound holds in every coin and across time. The per-coin slope t runs from −2.60 (LTC) to −4.47 (XMR). The slope is negative in 7 of 8 years, from t −0.84 (2022) to −5.66 (2021), and positive only in 2024 (t +0.93). Averaged across coins at each time, its signal profit still has t 3.90 over 6691 independent times.
