---
idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: at a funding settlement time, the 2-hour pre-move runs against the 24-hour trend -> kept: a regime fires on the bar closing at 00/08/16 UTC when the 2h return × the 24h return is below 0.
- Comparison: the move after against the 2-hour pre-move, sized by the 24-hour trend's strength -> kept: the position points against the pre-move (with the 24h trend) and grows with the 24h return.
- Outcome: the 2 hours after settlement move back, opposite the pre-move, more when the trend is stronger -> kept: a 2-bar hold, signed with the 24h trend.
- Verdict transfer: yes: the forecast bets exactly the stated retracement over the stated 2 hours, at settlement only, sized by the stated trend.
Forecast: The forecast is non-zero only on the hourly bar whose close is a funding settlement (the coming bar starts at 00:00, 08:00 or 16:00 UTC). It also needs the 2-hour return (close[t]/close[t-2]) and the 24-hour return (close[t]/close[t-24]) to have opposite signs, so that their product (MomentumDivergence 3/25) is below 0. On those bars the forecast is the 24-hour return (PriceEvolution, period 24), standardised against its own past 60 values. It is long after a 24h rise with a 2h dip into settlement, and short after a 24h fall with a 2h bounce. Its size grows with the strength of the 24-hour trend, and it is 0 on every other bar. Each bet is held for 2 bars.
Config: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Use the cases: bars in regime mean_reversion with a non-zero forecast. Settlement bars are 8 bars apart, so each case counts once. On each case, compute forecast/10 × (close[t+2]/close[t] − 1 − the coin's mean 2-bar return over all its windows). Take the t of the mean of this product over all coins and windows.
- Supporting check: The Pearson correlation between the case's forecast and its excess 2-bar return (as above) is above 0.
- Confirm: The main-measure mean is positive with t ≥ 2 over at least 200 cases, and the correlation is above 0.
- Reject: The main-measure mean is negative with t ≤ -2 over at least 200 cases.
- Inconclusive: These results neither confirm nor reject: - a t between -2 and 2; - a t ≥ 2 with a correlation at or below 0; - fewer than 200 cases.
