---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin fell over the weekend, Saturday close to Sunday close, larger fall stronger -> kept: the Sunday bar's 1-bar fall, graded, active only when the coming bar is a Monday.
- Comparison: the rise is larger the further the coin fell over its past 20 days, and none after a 20-day rise -> kept: the weekend fall is multiplied by the 20-day fall, and the product is 0 when the 20 days rose.
- Outcome: the coin rises over the next 3 days, Monday to Wednesday -> kept: the bet is placed at Sunday's close and held 3 daily bars.
- Verdict transfer: yes: the same weekend return, the same 20-day condition and the same 3-day rise are tested, so a confirm or a reject carries over to the idea.
Forecast: On the bar whose coming bar is a Monday (the Sunday bar), the forecast is the Sunday 1-day fall times the 20-day fall, both clipped at 0. It is standardised over its past 60 daily values (min 20). It is positive only when the Sunday close is below Saturday's and also below the close 20 days earlier. It grows with the size of either fall, and is 0 after a weekend rise or a 20-day rise. On every other weekday the regime is flat, and the 3-bar holding period keeps the Sunday bet through Monday to Wednesday. It is long only.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The cases are Sunday bars with forecast > 0, one per week, so their 3-day returns do not overlap. For each case, take close[t+3]/close[t]-1 inside the window, minus the coin's mean 3-day return over all its windows (holding the coin). The measure is the mean of this excess return over all cases, with its t.
- Supporting check: Across the cases, the least-squares slope of the excess 3-day return on the forecast is positive, so a larger forecast is followed by a larger excess rise.
- Confirm: The mean excess 3-day return is positive with t ≥ 2 on at least 100 cases, and the supporting slope is above 0.
- Reject: The mean excess 3-day return is negative with t ≤ -2 on at least 100 cases.
- Inconclusive: The idea is neither confirmed nor rejected in three situations: - t falls between -2 and 2; - t is 2 or more but the slope is 0 or below; - there are fewer than 100 cases.
