---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d3_weekend-fall-in-turbulence
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the coin fell over the weekend, from Saturday's close to Sunday's close -> kept: the Sunday bar's one-bar return, read on the Sunday bar only, with the long side kept for falls.
- Comparison: a larger rise when 20-day volatility stands higher against 60-day volatility -> kept: the fall is multiplied by the 20-day over 60-day return standard deviation.
- Outcome: the coin rises over the next 3 days (Monday to Wednesday), more after a larger fall -> kept: each bet is held 3 daily bars from Sunday's close.
- Verdict transfer: yes: the forecast is the weekend fall times the volatility ratio, taken only at Sunday's close and held Monday to Wednesday, so its 3-day result is the idea's own.
Forecast: The forecast is computed only on Sunday bars. The detector's weekday clock selects the bar whose coming bar is a Monday. On every other bar the regime is flat, and the holding period carries Sunday's bet through Wednesday. On a Sunday the component is the Sunday bar's return in percent times the volatility ratio. The ratio is the standard deviation of the last 20 daily returns over that of the last 60, both ending on Sunday. The value is standardised against its own past 61 values, negated, and clipped at 0. The forecast is therefore positive after a weekend fall and 0 after a weekend rise or a flat weekend. It grows in proportion to the depth of the fall and to how far 20-day volatility stands above 60-day volatility. It is never negative.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d3_weekend-fall-in-turbulence_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The cases are Sunday bars with forecast > 0. On each case, take the coin's 3-bar return close[t+3]/close[t]-1 inside its window and subtract the coin's mean non-overlapping 3-bar return over all its windows. Pool all coins and regress this excess return on the forecast. The measure is the slope and its t. The cases are one per week, so they never overlap.
- Supporting check: The mean excess 3-bar return over all cases is above 0.
- Confirm: The slope of excess return on the forecast has t >= 2, and the mean excess return over the cases is positive.
- Reject: The slope has t <= -2, meaning larger volatility-weighted weekend falls are followed by smaller or more negative excess 3-day returns.
- Inconclusive: Any slope t between -2 and 2 is inconclusive, as is a positive slope with a mean excess return at or below 0. A count below 200 cases is also inconclusive.
