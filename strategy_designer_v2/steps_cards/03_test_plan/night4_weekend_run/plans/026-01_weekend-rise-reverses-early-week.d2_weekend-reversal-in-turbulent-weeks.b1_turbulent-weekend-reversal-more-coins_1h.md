---
idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: the price rises from Saturday 00:00 UTC to Monday 00:00 UTC -> kept: the 48-bar return read at the bar that closes at Monday 00:00 (the next bar is weekday 0, hour 0), graded by its size.
- Comparison: only while 30-day hourly volatility is high against its own last 6 months -> kept: a regime rule requires the ratio of the 720-bar return volatility to its 4320-bar mean to be at least 1.
- Outcome: the price falls over Monday and Tuesday, more after a larger weekend gain -> kept: a short is sized by the weekend gain and held 48 bars.
- Verdict transfer: yes: the config bets exactly on falls after weekend rises in high-volatility weeks, sized by the gain, over the idea's own two days.
Forecast: The forecast is non-zero only on the bar whose close is Monday 00:00 UTC, and only when the 30-day volatility of hourly returns is at least its 6-month mean. On that bar it is minus the 48-bar (weekend) percent return, standardised against the past 60 values of the rolling 48-bar return. It is clipped at 0, so it is short after a weekend rise, larger for a larger rise, and 0 after a weekend fall. The bet is held 48 bars, through Monday and Tuesday. On every other bar the regime is null and the forecast is 0.
Config: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: A case is each short bet, a forecast of -2 or lower on a Monday 00:00 bar. For each case, take the coin's 48-bar return from that bar's close, minus the coin's normal 48-bar drift over all its windows, signed in the short direction. The measure is the mean of this unusual move, with its t over the cases, before costs.
- Supporting check: Across the cases, the correlation between abs(forecast) and the unusual move is above 0 (larger weekend gains are followed by larger falls).
- Confirm: The mean unusual move in the short direction is positive with t >= 2, and the supporting correlation is above 0.
- Reject: The mean unusual move in the short direction is negative with t <= -2 (weekend rises carry on in high-volatility weeks).
- Inconclusive: A t between -2 and 2, or a confirming t with a correlation at or below 0. Any result with fewer than 300 cases over all coins and windows is also inconclusive.
