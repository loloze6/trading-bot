---
idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a fall over the 2 hours before the 00:00 and 16:00 UTC settlements -> kept: a clock regime selects the two settlement bars, and a graded 2-bar fall is measured there.
- Comparison: the fall against the coin's usual 2-hour move -> kept: the 2-bar return is divided by the mean absolute 2-bar return over 720 bars.
- Outcome: a rise over the 8 hours after the settlement, larger for a larger fall -> kept: the long bet is held for 8 bars, and its size grows with the fall.
- Verdict transfer: yes: the config buys exactly the stated fall at exactly the two settlements and holds the bet for the stated 8 hours.
Forecast: The forecast is computed only on the bar whose close is a 00:00 or 16:00 UTC settlement, that is, when the coming bar starts at hour 0 or 16. Every other bar is in a null regime and has forecast 0. On a settlement bar, the indicator is the return over the last 2 bars divided by the coin's mean absolute 2-bar return over the last 720 bars, so a fall is counted in usual 2-hour moves. This value is standardised against its own past 500 values, sign-flipped, and clipped at 0. A rise therefore gives 0. A fall gives a long position that grows in proportion to its size against the usual move, about +10 for a typical-sized fall and capped at +20. The forecast is never negative, and the book holds each bet for the 8 bars up to the next settlement.
Config: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours_1h_config.json
Criterion:
- Horizon: 8 bars
- Main measure: Cases are settlement bars (regime mean_reversion) with forecast ≥ 2. Settlements are at least 8 bars apart, so the cases do not overlap. For each case, take the coin's 8-bar return from that close minus the coin's normal 8-bar drift (the mean over all windows). The measure is the forecast-weighted mean of this excess return over all coins and windows, with the t of the weighted mean.
- Supporting check: Split the cases at the median forecast. The mean 8-bar excess return of the upper half minus that of the lower half must be above 0 (Welch's t reported).
- Confirm: The forecast-weighted mean excess return is above 0 with t ≥ 2, before costs, and the upper-half minus lower-half difference is above 0.
- Reject: The forecast-weighted mean excess return is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming main measure with a failed supporting check is also inconclusive. So is a sample of fewer than 100 cases across all coins and windows.
