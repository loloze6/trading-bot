---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin's Saturday-to-Sunday close-to-close fall -> adapted: "after the fall" becomes "while on the Sunday bar", with the 1-bar return measured at Sunday's close.
- Comparison: larger fall, and higher past-20-day volatility, give a larger rise -> kept: the fall is multiplied by the 20-day volatility, measured against the coin's prior 168 days.
- Outcome: price rises over the next 3 days (Monday to Wednesday) -> kept: each bet is held for 3 daily bars.
- Verdict transfer: yes: the forecast bets only on Sunday falls, sized by fall times 20-day volatility, and is judged on the next 3 days' rise.
Forecast: A calendar regime is active only on Sunday's bar, the bar whose next bar is Monday. On that bar the component is Sunday's 1-day return times the 20-day volatility of daily returns, divided by the volatility of the 168 days before those 20. It is standardised against its own past 189 values, then negated and clipped at 0. The forecast is therefore positive only after a Sunday fall. It grows with the size of the fall and with recent volatility, and it is 0 after a Sunday rise and on every other day. Each bet is held through Wednesday by the holding period.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: A case is a Sunday bar with forecast > 0; these bars are 7 days apart, so the cases do not overlap. For each case, take forecast x (the coin's 3-bar return from Sunday's close, minus that coin's mean non-overlapping 3-bar return over all windows). The measure is the t of the mean of this product over all cases.
- Supporting check: Split the cases into thirds by forecast. The mean excess 3-bar return of the top third minus that of the bottom third must be above 0.
- Confirm: The main measure has t >= 2 and the top-minus-bottom-third difference is above 0.
- Reject: The main measure has t <= -2.
- Inconclusive: A t between -2 and 2, or t >= 2 with the top-minus-bottom-third difference at or below 0. Fewer than 100 cases is also inconclusive.
