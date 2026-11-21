---
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: how far the coin has fallen over its last 24 hours, graded ("the more") -> kept
- Comparison: none
- Outcome: the coin rises over the next 24 hours, more after a larger fall -> kept
- Verdict transfer: yes: the forecast is the size of the 24-hour fall itself, held for 24 hours, so its forward gains confirm or reject the claim directly.
Forecast: The forecast starts from the coin's 24-bar percent return, `PriceEvolutionComponent` with period 24. It is standardised over its last 60 values (min_periods 20) and negated, so a fall reads positive. It is then clipped at 0, because the idea speaks only of falls. The forecast is zero after a 24-hour rise. It is positive after a 24-hour fall and grows continuously with the depth of that fall. It is about +10 for a fall of the usual size and capped at +20. The forecast never goes negative.
Config: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The measure uses the non-overlapping 24-bar grid of each window and the grid bars with forecast > 0. Each case's value is (forecast / 10) x (the coin's 24-bar forward return minus its normal 24-bar drift over all windows). The ordinary t of the mean of these values is taken over all cases.
- Supporting check: Cases are split at the median forecast. The mean excess 24-bar forward return of the upper half minus that of the lower half must be greater than 0.
- Confirm: The idea is confirmed when the main measure's t is 2 or more and the supporting check's difference is positive.
- Reject: The idea is rejected when the main measure's t is -2 or less.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more is also inconclusive when the upper-half minus lower-half difference is 0 or below. At least 200 grid cases with forecast > 0 are required, or the result is inconclusive.
