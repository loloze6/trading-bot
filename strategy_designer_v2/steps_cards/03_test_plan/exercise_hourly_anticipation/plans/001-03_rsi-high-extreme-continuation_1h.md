---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a high extreme -> adapted: the threshold becomes a graded RSI excess above 50, with extremes amplified by signed_power.
- Comparison: rise after extreme versus after neutral readings -> kept: neutral RSI gives a forecast near 0, and the criterion contrasts the largest positions with those bars.
- Outcome: price keeps rising over the following bars -> adapted: "after X" becomes "while X", and the fixed holding period is dropped.
- Verdict transfer: yes: the forecast is long in proportion to RSI strength above 50 and zero at or below it, so forward returns after its largest values versus near-zero values test exactly the idea's claim.
Forecast: Use the 14-bar Wilder RSI from RSIPullbackComponent, which outputs (50 − RSI) × sf. Standardise it over its past 60 values, then negate it so that RSI above 50 is positive. Apply signed_power with exponent 2 (pivot 10), so mild readings near 50 stay near 0 and extreme high readings grow quadratically. Finally, clip at 0 so the forecast is long-only: zero whenever RSI ≤ 50, and larger the further RSI sits above its usual range, up to the cap of 20.
Config: 001-03_rsi-high-extreme-continuation_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The coin's forward 24-bar close-to-close return after "extreme" bars minus the same return after "neutral" bars. - Extreme bars are those where the forecast is in its top decile of nonzero values. - Neutral bars are those where the forecast is below 1 and RSI is between 40 and 60. - Both returns are taken net of the coin's unconditional mean 24-bar return in the same window, so the market's own drift is not credited. - Samples are thinned to non-overlapping 24-bar blocks, one case per block.
- Supporting check: The portfolio's gross return per unit of average exposure exceeds buy-and-hold's return times the same average exposure, in at least 2 of the 3 coins.
- Confirm: The pooled extreme-minus-neutral difference is positive with t ≥ 2 on non-overlapping cases, and it is positive in at least 2 of 3 coins and in at least 4 of the 6 windows.
- Reject: The pooled difference is ≤ 0, or it is negative in at least 2 of 3 coins. A difference with t ≤ −2 additionally points to reversal.
- Inconclusive: A positive pooled difference with t < 2, or a positive pooled difference that is not confirmed by coins and windows. Any coin with fewer than 30 non-overlapping extreme cases, or fewer than 100 pooled, is inconclusive.
