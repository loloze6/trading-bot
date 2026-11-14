---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: RSI(14, Wilder) on daily closes, read as momentum. The raw component value is (50 − RSI) × 0.4. It is divided by its mean absolute value over the previous 60 bars and scaled to target 10 (cap ±20). The sign is then flipped, so the value is positive when RSI is above 50. Below 0 it is clipped to 0, which makes the forecast flat whenever RSI ≤ 50. Finally it is squared with sign kept (signed_power, exponent 2, pivot 10). The forecast is therefore 0 at RSI 50 and stays small near neutral readings. It grows with the square of RSI's distance above 50, so the largest long positions come at high extremes (RSI near or above 70). It is never negative.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Confirm: The test uses a 5-bar horizon, pooled over the 3 coins and 6 windows. Forward returns are taken from non-overlapping 5-bar blocks, so each return is counted once. Each block is classed by its starting bar. Extreme bars have recorded raw RSI value ≤ −8 (RSI ≥ 70). Neutral bars have raw value between −4 and +4 (RSI 40–60). The idea is confirmed if the mean forward 5-bar close-to-close return of extreme bars exceeds that of neutral bars with t ≥ 2, and the difference is positive in at least 2 of the 3 coins. Comparing against neutral bars of the same coin and period removes the market's own drift. Supporting check, before costs: the portfolio's total return beats buy-and-hold of the coin scaled by the strategy's average exposure, in at least 2 of 3 coins.
Reject: The idea is rejected if the extreme-minus-neutral difference in mean forward 5-bar return is zero or negative pooled. It is also rejected if the difference is positive in fewer than 2 of 3 coins. A difference with t ≤ −2 additionally points to reversal rather than continuation.
Inconclusive: A pooled difference that is positive but with t below 2, or that is confirmed pooled but positive in only 1 coin, neither confirms nor rejects the idea. The same holds if fewer than 20 non-overlapping extreme blocks exist across all coins and windows.
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, sized by the square of its distance from 50". Moderate readings above 50 therefore hold small long positions instead of none. The extreme-versus-neutral contrast is made in the evaluation, not in the position. Only the high-extreme (long) side is traded; low extremes stay flat.
