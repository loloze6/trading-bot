---
idea: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: be08f97ea86e
---
Fidelity:
- Situation: the 30-day net move is small against the 30-day high-low range, and the close is below that range's middle -> adapted: both stay on/off conditions in a regime rule, read while they hold.
- Comparison: the size of the rise over the past 10 days, where a larger rise should mean a larger next move -> kept: the 10-bar price change, long side only, sets the position size.
- Outcome: the coin rises over the next 5 days, more after a larger 10-day rise -> kept: positions are held for 5 bars.
- Verdict transfer: yes: the regime measures exactly the idea's flat-and-below-middle state, and the forecast grows with exactly its 10-day rise.
Forecast: Two conditions are checked on every bar. The first is the 30-bar net move divided by the 30-bar high-low range (NetMoveToRangeRatio, period 30, high_low). The second is the close's percent distance from the middle of the 30-bar high-low range, built from Ichimoku spans with all periods 30 and displacement 0. When the ratio is 0.3 or less and the close is below the middle, the bar is mean_reversion. On those bars the forecast is the 10-bar percent price change, standardised over 60 bars and clipped at 0. It is positive and grows with the size of the 10-day rise. It is 0 when the coin fell over the 10 days, and 0 on every other bar.
Config: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On the non-overlapping 5-bar grid of each window, take the bars with forecast > 0. Regress each bar's next-5-bar return, minus the coin's mean 5-bar return over all windows, on the forecast. Report the slope's t, pooled over coins.
- Supporting check: The mean drift-removed 5-bar return over those same cases is above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: A t between -2 and 2, or a t of 2 or more with a mean that fails the check. Fewer than 30 grid cases with forecast > 0 is also inconclusive.
