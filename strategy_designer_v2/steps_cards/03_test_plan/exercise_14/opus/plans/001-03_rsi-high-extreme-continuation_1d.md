---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the RSI reaches a high extreme -> adapted: graded rather than a threshold. The position grows with how far the 14-bar RSI sits above 50. A squared dead zone keeps readings just above 50 small and lets extreme readings carry the largest positions. "After the RSI reaches an extreme" becomes "while the RSI is high".
- Comparison: the move after neutral readings -> kept: neutral readings (RSI near 50) give a forecast near zero. The test compares what follows the largest positions with what follows near-zero ones, and also with the coin's average move over all bars.
- Outcome: the price keeps rising over the following bars -> adapted: no holding period is set. The return is read over the next 5 bars while the position follows the RSI, and only the upward side is traded.
- Verdict transfer: yes: the forecast is the RSI's high-side strength, so a forward return that rises after large forecasts relative to neutral bars and to holding is exactly the idea's claim, and its absence rejects it.
Forecast: Use the 14-bar RSI on daily bars as RSIPullbackComponent, whose raw value is (50 − RSI) × 0.4. Standardise it against its own 60 previous values (target 10, cap 20), then negate it so it is positive when the RSI is above 50. Clip it at 0 to make it long-only, since the idea is about high extremes only. Finally apply signed_power with exponent 2 and pivot 10. The forecast is 0 when the RSI is 50 or below and small just above 50. Around the RSI's typical distance from 50 it is about +10, a 100% long position. At extreme readings it rises steeply and is capped at +20 (200% long). It is never negative.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's 5-bar forward return after "extreme" bars minus its 5-bar forward return over all bars, which is the return of simply holding the coin. Extreme bars are those with forecast ≥ 10. The comparison is made per coin and then pooled across the 3 coins and 6 windows. Only non-overlapping 5-bar blocks are counted: within a run of consecutive extreme bars, a case is taken only every 5th bar.
- Supporting check: Compare the forward return after extreme bars with the forward return after neutral bars, those with forecast between 0 and 2. The idea needs extreme > neutral as well as extreme > holding.
- Confirm: The pooled excess 5-bar forward return after extreme bars is > 0 with a t-statistic ≥ 2.0 on the non-overlapping cases. The excess is also positive in at least 2 of the 3 coins, and the supporting check shows extreme > neutral when pooled.
- Reject: The pooled excess 5-bar forward return after extreme bars is ≤ 0 and is ≤ 0 in at least 2 of the 3 coins. A significantly negative pooled excess (t ≤ −2) also rejects; it would point to reversal instead of continuation.
- Inconclusive: The pooled excess is positive but t < 2.0, or the coins disagree (only 1 of 3 positive while the pooled excess is positive), or extreme ≤ neutral despite a positive excess over holding. At least 40 non-overlapping extreme cases are needed pooled, with at least 10 per coin. Below that the result is inconclusive whatever its sign.
