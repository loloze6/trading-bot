---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the RSI reaches a high extreme (a strongly one-sided run of gains) -> adapted: the "extreme" threshold becomes a graded reading. The forecast uses 50 - RSI(14), keeps only the overbought side, and passes it through a smooth dead zone (signed_power, exponent 2). The position therefore stays small at mildly high RSI and grows steeply as RSI nears its extremes. "After the RSI reaches" becomes "while the RSI is high".
- Comparison: behaviour after extreme readings versus after neutral readings (from the brief) -> kept: neutral readings give a forecast near 0, so the criterion compares what follows the largest short positions with what follows near-zero forecasts.
- Outcome: price falls over the following bars, giving back part of the run -> adapted: there is no holding period. The short is held only while RSI stays high, and the fall is measured as the forward 5-bar return after each bar.
- Verdict transfer: yes: the forecast is short in proportion to how overbought the RSI is and flat when RSI is neutral or low, so the comparison and the forward return measure exactly whether high RSI extremes are followed by falls.
Forecast: The forecast uses RSIPullbackComponent with period 14, the Wilder convention. Its raw value is (50 - RSI) x 0.4: negative when RSI is above 50, positive below. - It is standardised over the 60 previous values (min_periods 20), which puts it on the forecast scale, about 10 for an average distance of RSI from 50. - It is clipped at a maximum of 0, so only the overbought side remains and the forecast is never positive. - signed_power with exponent 2 and pivot 10 damps moderate readings towards 0 and amplifies large ones. A standardised -5 becomes -2.5, -10 stays -10, and -20 becomes -40. The combined forecast is clipped at -20. - The forecast is 0 whenever RSI is at or below 50. It grows more negative, continuously and faster than linearly, as RSI rises towards an extreme. A bigger short is taken the more overbought the coin is. - There is no regime condition: the detector is ungated.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's forward 5-bar close-to-close return is measured after two groups of bars, pooled over the 3 coins and 6 windows: - extreme bars: bars whose forecast is at most -10, that is, RSI clearly overbought; - neutral bars: bars whose forecast is 0, that is, RSI at or below 50 (none of the idea's situation). The measure is the mean forward return after extreme bars minus the mean after neutral bars. Taking the difference removes the market's own drift, the same way it would against simply holding the coin. Returns are taken on non-overlapping 5-bar blocks, so that overlapping returns are counted once: within a run of qualifying bars, only every 5th bar counts. The result is judged before costs.
- Supporting check: The sign of the main difference is computed per coin. It must be negative for at least 2 of the 3 coins, so that one coin does not carry the result.
- Confirm: Both of the following hold: - The pooled difference (extreme minus neutral) is negative, with a t-statistic of -2.0 or lower on the non-overlapping blocks. - It is negative for at least 2 of the 3 coins. That is, price falls more, or rises less, in the 5 bars after high RSI extremes than after neutral readings.
- Reject: Either of the following holds: - The pooled difference is zero or positive, which means continuation or no effect after high extremes. - The pooled difference is negative with a t-statistic above -1.0, and the difference is negative for at most 1 of the 3 coins.
- Inconclusive: Any other result is inconclusive. This includes: - a negative difference with a t-statistic between -2.0 and -1.0; - a t-statistic of -2.0 or lower with only 1 coin agreeing; - fewer than 30 non-overlapping extreme-bar blocks pooled across the coins, or fewer than 30 neutral blocks.
