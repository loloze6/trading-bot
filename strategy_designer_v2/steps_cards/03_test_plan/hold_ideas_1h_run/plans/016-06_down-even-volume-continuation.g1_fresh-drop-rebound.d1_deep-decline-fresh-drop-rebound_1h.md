---
idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin fell over the past 3 days, with a 1-day fall and a 3-day fall of some depth -> adapted: "fallen over 3 days" is a regime (72-bar return below 0), and both fall sizes are graded and summed.
- Comparison: larger 1-day fall and deeper 3-day fall against smaller ones; mild 3-day declines refused -> adapted: the rebound bet grows with each fall's size, and the 3-day part is damped smoothly when mild.
- Outcome: the price rises over the next 3 days, more after larger falls -> kept: forward 72-bar return.
- Verdict transfer: yes: the forecast is long in proportion to both falls only while the 3-day fall holds, so its payoff over 72 bars tests exactly the claimed rebound.
Forecast: The regime turns on only while the 72-bar return is negative; otherwise the forecast is flat. In the regime, the forecast is the equal-weight mean of two parts, each standardised, negated and clipped at 0, so the forecast is never short. - The first part is the 72-bar fall: PriceEvolution(72), standardised over 73 bars. A signed_power with exponent 2 damps mild declines towards 0. - The second part is the fresh 24-bar fall: PriceEvolution(24), standardised over 60 bars. It is 0 when the last day rose. The forecast is 0 when neither part shows a fall. It grows as the 3-day fall deepens, and it grows as the 1-day drop gets larger.
Config: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: The OLS slope of the forward 72-bar return minus the coin's mean 72-bar return (all windows together) on the forecast. Samples are the non-overlapping 72-bar grid bars where the forecast is above 0, pooled over coins and windows.
- Supporting check: On the same grid, the cases in the top third of forecast have a mean excess 72-bar return above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: A t between -2 and 2, or a confirming t with a failed check. At least 100 independent grid cases with a positive forecast are needed; fewer is inconclusive.
