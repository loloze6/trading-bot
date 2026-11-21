---
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a fall over the last 24 hours made of many similar-sized hourly losses -> kept: LossShareBeyondLargest (24 bars, k 1) on net 24-hour falls only.
- Comparison: rather than in one large hour -> kept: 1 minus the largest hourly loss's share of all the 24 hourly losses.
- Outcome: it rises over the next 2 days -> kept: long, held 48 bars.
- Verdict transfer: yes: the forecast grows exactly with how evenly a 24-hour fall was spread over its hours, and it is long for 2 days.
Forecast: The forecast uses one indicator, LossShareBeyondLargestComponent, over 24 bars with k 1. For the last 24 hourly returns it computes S = 1 - (largest hourly loss / sum of all hourly losses), signed by the 24-hour net return. It is negative over a net fall. It is standardised over 60 bars (min_periods 20) and clipped at 0 from above, so net rises give 0, and then negated. The forecast is therefore 0 when the coin did not fall over 24 hours, and positive (long) after a net fall. It is small when one hour carried most of the losses and grows toward about +20 as the losses spread evenly over many hours. It is never short.
Config: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: Use a non-overlapping 48-bar grid in each window, pooled over coins and windows. Regress each grid bar's 48-bar forward return, minus the coin's normal 48-bar drift over all windows, on its forecast. The measure is the t of the slope.
- Supporting check: Take grid bars with a net 24-hour fall (forecast > 0). Split them at their median forecast. The upper (grind) half's mean excess 48-bar return minus the lower (jump) half's must be > 0 (Welch's t).
- Confirm: The slope t is >= 2, with at least 300 positive-forecast grid cases, and the supporting check difference is above 0.
- Reject: The slope t is <= -2, with at least 300 positive-forecast grid cases.
- Inconclusive: The slope t is between -2 and 2, or the slope t is >= 2 but the supporting check fails, or there are fewer than 300 positive-forecast grid cases.
