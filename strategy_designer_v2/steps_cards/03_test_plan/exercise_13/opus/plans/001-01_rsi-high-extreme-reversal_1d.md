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
- Situation: the 14-bar RSI reaches a high extreme on BTC, ETH or BNB -> adapted: the "reaches an extreme" threshold becomes a graded short that grows as RSI rises above 50. The signed_power transform damps readings near 50 towards zero and amplifies readings far above it, so the position is concentrated at extremes without a cliff. "After the index reaches" becomes "while the index is high".
- Comparison: behaviour after extreme readings against behaviour after neutral readings (from the brief) -> kept: the criterion compares forward returns after high-extreme bars with forward returns after neutral bars. Both groups are taken from the recorded RSI value. Neutral readings give a near-zero forecast.
- Outcome: price falls over the following bars, giving back part of the run -> kept: the forward close-to-close return over 5 daily bars after the bar, expected negative relative to neutral bars.
- Verdict transfer: yes: the test measures whether returns after high RSI readings are lower than after neutral ones, with the position growing with the extremity, which is exactly the claim. A confirm or reject transfers to the idea.
Forecast: The forecast is built from RSIPullbackComponent with period 14, whose raw value is (50 − RSI) × 0.4. This value is negative when RSI is above 50. - It is standardised against its own previous 60 values, with min_periods 20, so an average reading is about 10 in size. - It is then passed through signed_power with exponent 2 and pivot 10. A standardised −5 becomes −2.5, −10 stays −10, and −15 becomes −22.5. Moderate readings are damped and extreme ones amplified, smoothly. - It is then clipped at a maximum of 0, so only the high-RSI side the idea speaks about takes positions. The forecast is zero whenever RSI is at or below 50. It is negative (short) when RSI is above 50, growing roughly with the square of the standardised distance above 50, and reaching the −20 cap (200% short) at the most extreme readings. It is never positive.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: - Extreme bars: bars whose forecast is −10 or lower (the largest short positions, roughly RSI well above its usual excursion). - Neutral bars: bars whose recorded raw RSI value is between −4 and +4 (RSI between 40 and 60). - Measure: the mean 5-bar forward return of the coin (close to close) after extreme bars, minus the same mean after neutral bars. - Counting: overlapping returns are counted once. Within a run of consecutive extreme bars, only the first bar and then every 5th bar are kept; neutral bars are sampled every 5th bar. - Drift: subtracting the neutral-bar return removes the coin's own drift, so buy-and-hold's rise is not credited. - Pooling: results are pooled across the 3 coins and 18 windows, and also reported per coin.
- Supporting check: the 5-bar return of the strategy's portfolio on bars where the forecast is nonzero, minus the return of holding the coin over the same bars. Results are grouped into terciles of position size. If the idea holds, this excess should rise with the size of the short.
- Confirm: All three of the following hold: - The pooled extreme-minus-neutral difference is −1.0 percentage point or lower. - The t-statistic on the non-overlapping cases is −2.0 or lower. - The difference has the same negative sign in at least 2 of the 3 coins.
- Reject: Either of the following holds, with at least the minimum count of cases: - The pooled difference is 0 or higher (extreme readings are followed by returns no lower than neutral). - The difference is positive with a t-statistic of +2.0 or higher, which would indicate continuation, the opposite of the idea.
- Inconclusive: - A negative difference that misses the confirm thresholds (smaller than 1.0 percentage point in size, or a t-statistic between −2.0 and 0). - Coins disagreeing in sign (fewer than 2 of 3 negative). - Fewer than 30 non-overlapping extreme cases pooled, or fewer than 30 non-overlapping neutral cases.
