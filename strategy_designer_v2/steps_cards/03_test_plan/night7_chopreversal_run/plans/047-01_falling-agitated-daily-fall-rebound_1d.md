---
idea: 047-01_falling-agitated-daily-fall-rebound
brief: 047_falling-agitated-two-way-daily-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 0e977cd77240
---
Fidelity:
- Situation: a coin's one-day percent fall, larger or smaller -> adapted: the one-day close-to-close fall, graded by its size in the coin's usual daily moves, and 0 on up days.
- Comparison: a larger fall against a smaller fall, inside a falling, agitated market -> kept: the profile is added by code, and the position grows with the fall.
- Outcome: a larger rise over the next day -> kept: a long held for 1 daily bar.
- Verdict transfer: yes: the book is long only after down days in the profile, sized by the fall, so a next-day rise that grows with the fall confirms the idea and its absence rejects it.
Forecast: The forecast is the coin's one-day percent return (`PriceEvolutionComponent`, `period` 1). It is standardised against the mean absolute size of its last 60 daily returns, then negated and clipped at 0. It is 0 on up days and flat days. On down days it is positive and grows in proportion to the day's fall: a usual-sized fall gives about +10, and a fall twice the usual size or more gives the cap of +20. It is never negative. The code keeps the book flat outside the falling, agitated profile.
Config: 047-01_falling-agitated-daily-fall-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On recorded bars with forecast > 0, regress the coin's next-day excess return on the forecast and read the slope. The excess return is close[t+1]/close[t] - 1 minus the coin's mean daily return over all windows. The slope's t uses standard errors clustered by day.
- Supporting check: The forecast-weighted mean of the next-day excess return on those bars is above 0.
- Confirm: The slope's t is 2 or more, and the weighted mean excess return is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any slope t between -2 and 2 is inconclusive, as is a confirming slope whose check fails. Fewer than 100 down-day cases, or cases falling on fewer than 50 distinct days, is also inconclusive.
