---
idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: at a funding settlement, the 2-hour move into it runs against the 24-hour trend -> kept: a regime rule fires when the coming bar starts at 00:00, 08:00 or 16:00 UTC and the 2-bar return times the 24-bar return is below 0.
- Comparison: the stronger the 24-hour trend, the larger the move back -> kept: the position size is the 24-bar return, standardised against its own past.
- Outcome: the next 8 hours run opposite the pre-move, which here is the trend's direction -> kept: the bet is held for 8 bars from the settlement close.
- Verdict transfer: yes: the test measures the idea's own condition, sizing, direction and 8-hour hold.
Forecast: The forecast is non-zero only on the bar that closes at a settlement time (the coming bar starts at 00:00, 08:00 or 16:00 UTC), and only when the 2-bar return and the 24-bar return have opposite signs. The detector reads both conditions. `MomentumDivergenceComponent` (short_period 3, long_period 25) gives the product of the 2-bar and 24-bar returns, which is below 0 when they disagree. On those bars the forecast is the 24-bar percent return (`PriceEvolutionComponent`, period 24), standardised over its last 60 values (min 20). It is long after a 24-hour rise and short after a 24-hour fall, which is against the pre-move. Its size grows with the trend's strength, about ±10 for a usual trend and capped at ±20. On every other bar the forecast is 0, and the holding period carries the bet through the 8 hours to the next settlement.
Config: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins_1h_config.json
Criterion:
- Horizon: 8 bars
- Main measure: The cases are the settlement bars in regime mean_reversion with a non-zero forecast; they are 8 bars apart, so they do not overlap. For each case, take forecast/10 × (the coin's 8-bar return from that close minus the coin's mean 8-bar return over all windows). Compute the mean over all cases and coins, and its t.
- Supporting check: Split the cases by |forecast| into the top half and the bottom half. The drift-adjusted 8-bar return in the forecast's direction must be higher in the top half than in the bottom half (difference > 0).
- Confirm: The main measure's mean is > 0 with t ≥ 2, and the supporting check's difference is > 0.
- Reject: The main measure's mean is < 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with the supporting check failing. Fewer than 200 cases is also inconclusive.
