---
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.6402 USD
---
## Findings
- **F1:** The tested book's edge grows with the coin's 20-day volatility. On its active days, the next-day directional move net of drift is +0.01 % in the lowest volatility third (t −0.15, 781 cases), +0.38 % in the middle third (t 2.74, 781) and +0.60 % in the top third (t 3.58, 781), which is 5.5 times the 0.11 % round-trip cost. The long side has no edge at all in calm markets: its strength is −0.066 (t −1.07, 437) in the low third against +0.123 (t 2.48, 317) in the high third.
- **F2:** Volatility also decides what follows the moves the idea does not trade. Among 1-day falls of more than one usual move while the close is below its 50-day average, the correlation between the coin's volatility rank and the next-day rebound is 0.18 (t 3.86, 424 cases). In the lowest volatility third those falls keep falling (strength −0.40, t −1.96, 136 cases); in the top third they rebound (+0.18, t 2.07, 154).
- **F3:** Among 1-day rises of more than one usual move while the close is above its 50-day average, the correlation between volatility rank and the next-day give-back is 0.14 (t 3.19, 506 cases). In the lowest volatility third those rises keep going up the next day (give-back strength −0.31, t −2.59, 184 cases).
- **F4:** Below the 50-day average, the next-day fall grows with the size of the day's rise. Rises of 0.3 to 1 usual move are followed by −0.42 % (t −2.47, 525 cases), rises of 1 to 2 by −0.64 % (t −2.67, 206) and rises above 2 by −1.02 % (t −1.75, 50). The short side's give-back is still there on non-overlapping 5-day stretches: +1.38 % in its direction (t 2.23, 236 cases), against +0.61 % for the long side (t 0.93, 251).
- **F5:** Below the 50-day average, the more a coin has risen over the past 20 days, the more it falls over the next 3 days. On non-overlapping 3-day stretches the strength is −0.006 in the lowest 20-day-return third (t −0.09, 267 cases) and −0.178 in the top third (t −2.19, 265). This is the weakest pattern here, given how many angles were examined.
- **F6:** The long side fails in falling years. Its next-day directional move is −1.21 % in 2018 (t −1.90, 66 cases) and −1.14 % in 2022 (t −2.73, 82), against +0.42 % in 2023 (t 3.02, 221). Patterns by weekday are within the range of chance once the 14 groups examined are counted.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend.g1_volatility-graded-counter-trend-fade` (from F1, F2, F3): The larger a coin's 1-day move against its 50-day average, measured in its 20-day usual moves, and the higher its 20-day volatility stands against its own past, the more of that move it gives back over the next 1 day.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend.g2_turbulent-downtrend-down-day-rebound` (from F2): The larger a coin's vol-scaled 1-day fall while its close is below its 50-day average, and the higher its 20-day volatility against its own past, the more it rises over the next 1 day.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend.g3_downtrend-rally-five-day-fade` (from F4): The larger a coin's vol-scaled 1-day rise while its close is below its 50-day average, the more it falls over the next 5 days.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend.g4_calm-uptrend-up-day-continuation` (from F3, F1): The lower a coin's 20-day volatility against its own past, the more its vol-scaled 1-day rise while its close is above its 50-day average continues over the next 1 day.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend.g5_downtrend-bounce-three-day-fade` (from F5): The larger a coin's 20-day return while its close is below its 50-day average, the more it falls over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
