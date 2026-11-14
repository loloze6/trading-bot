---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: 2017 to 2024
---
Idea: In BTC, ETH and BNB daily bars, when RSI(14) is above 70, the coin's return over the next 5 bars is lower than its average 5-bar return over the same coin and window.
Consequence: A trader would take profits on longs, or decline new ones, in a coin whose daily RSI is above 70, expecting the following week to lag holding.
Why:
- F4: The RSI(14), recovered as 50 minus the component's raw value, never exceeded 58.0 in the window (95th percentile 55.2, median 47.5). It was above 55 on 8.3% of bars and never above 60 or 70. A high-extreme RSI in the usual sense never occurred in this period.
- F5: Because the forecast is standardised over its past 60 values, the −10 threshold was hit at mild absolute RSI levels. On those 15 bars the implied RSI averaged 55.6 (range 54.0–58.0), against 45.8 on the 81 zero-forecast bars. The "extreme" cases here are extremes relative to a bearish 2022 stretch, not RSI extremes.
- F7: The case-to-case spread is large relative to the effect. The 5-bar forward return has an sd of 7.3% across all bars and the excess return 5.7% on extreme bars. At an effect of −2.3%, about 23 independent cases are needed for |t| = 2. A sample with that many extreme cases needs roughly 8–10 times the current extreme frequency in bar-count terms: several coins, several windows or years, or a shorter bar size where 14-bar RSI runs recur more often.
