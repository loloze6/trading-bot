---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Use the 14-bar Wilder RSI on daily closes, read as momentum: the raw value is (RSI − 50) × 0.4. Divide it by the mean absolute value of its previous 60 readings and multiply by 10, capped at ±20. Then apply a graded dead zone, signed_power with exponent 2 and pivot 10, so readings near 50 shrink toward 0 and readings far above 50 grow sharply. Finally clip at 0, because the idea concerns only high extremes. The forecast is zero whenever RSI ≤ 50. Above 50 it is positive, and it grows smoothly and faster than linearly as RSI rises, so the largest long positions occur at the highest RSI readings (70 and above). It is never negative.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Confirm: The horizon is 5 bars, and the main measure uses the recorded rsi_mom raw value. Take bars where RSI ≥ 70 (raw ≤ −8) and bars where RSI is neutral at 40–60 (raw between −4 and +4). Compute the forward 5-bar close-to-close return after each, minus the coin's unconditional mean 5-bar return over the same windows. Sample only non-overlapping 5-bar blocks, so each return counts once. The idea is confirmed if, pooled over the three coins and six windows, mean excess return after RSI ≥ 70 exceeds that after neutral readings by a t-statistic ≥ 2.0. The supporting check requires the same sign of difference in at least 2 of the 3 coins.
Reject: The idea is rejected if the pooled difference (high-extreme minus neutral, excess 5-bar return) is ≤ 0. It is also rejected if the difference is positive but below 2.0 in t and negative in at least 2 of the 3 coins. A significantly negative difference (t ≤ −2.0) rejects continuation and points to reversal.
Inconclusive: The result is inconclusive if the difference is positive but has t between 0 and 2.0 with at least 2 of 3 coins positive. It is also inconclusive if fewer than 30 non-overlapping RSI ≥ 70 observations exist in the pooled sample.
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50", with a long position that grows smoothly with RSI and is largest at extremes, instead of a trade triggered by crossing a threshold. The RSI scale is measured against its own recent 60 bars rather than fixed levels. The low-extreme side of the brief is not traded.
