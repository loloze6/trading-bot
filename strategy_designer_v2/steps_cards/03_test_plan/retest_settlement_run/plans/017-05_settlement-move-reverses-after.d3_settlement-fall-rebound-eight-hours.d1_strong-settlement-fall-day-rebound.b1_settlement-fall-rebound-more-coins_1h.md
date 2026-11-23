---
idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a fall over the 2 hours before the 00:00 or 16:00 UTC settlement -> kept: the 2-bar return at the close of the bar ending at settlement, active only at those two clock times.
- Comparison: the fall's size against the coin's usual 2-hour move -> kept: the 2-bar return divided by the mean absolute 2-bar return over 720 bars.
- Outcome: a rise over the next 24 hours that grows with the fall, carried mostly by the largest falls -> kept: a long position held 24 bars, sized by the fall in usual moves, damped toward 0 for small falls.
- Verdict transfer: yes: the test buys the settlement falls in proportion to their depth in usual moves and holds each bet for the idea's 24 hours.
Forecast: A regime rule makes the forecast non-zero only on the two settlement bars of each day. These are the bars whose next bar starts at 00:00 or 16:00 UTC. On those bars the forecast uses the 2-bar return divided by the mean absolute 2-bar return of the last 720 bars, which is the fall in usual 2-hour moves. This value is standardised over its past 500 values (min 120), negated, and clipped at 0, so it is long only and positive only after a fall. It then goes through signed_power with exponent 3 and pivot 20, the strongest graded dead zone. A fall of one usual move gives about 2.5. A fall of two usual moves or more gives about 20. Small falls stay near 0. The forecast is 0 on every other bar and after rises. Each bet is held for 24 bars.
Config: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Cases are the settlement bars whose forecast is 2 or more (the bets), at most one per non-overlapping 24-bar grid cell of each window. For each case, take the coin's return from that bar's close over 24 bars, minus the coin's mean 24-bar return over all windows. The measure is the mean of this unusual move across cases, with its t of the mean, before costs.
- Supporting check: The mean unusual 24-bar move of the cases must exceed that of the settlement bars with a smaller fall (forecast above 0 but below 2), as a positive Welch difference (cases minus small falls).
- Confirm: The idea is confirmed when the mean unusual move of the cases is positive with t ≥ 2, and the supporting difference is above 0.
- Reject: The idea is rejected when the mean unusual move of the cases is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more is also inconclusive when the supporting difference is 0 or below. Fewer than 30 independent cases in total is inconclusive whatever the t.
