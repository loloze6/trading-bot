---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin fell over the weekend, as its Saturday-to-Sunday close-to-close return -> kept: the Sunday bar's one-bar return, read at Sunday's close only, through a calendar regime.
- Comparison: the larger the weekend fall, the larger the rise -> kept: the long position grows with the size of the fall, measured in the coin's usual daily moves.
- Outcome: the price rises over the next 3 days (Monday to Wednesday), long -> kept: the position is bought at Sunday's close and held 3 daily bars.
- Verdict transfer: yes: the test measures exactly the Sunday fall, the 3-day rise after it and the link between their sizes, so either result carries to the idea.
Forecast: The regime is active only on the Sunday bar, whose next bar is a Monday (WeekdayComponent reads 0). On that bar the forecast is the Sunday one-bar return in percent (PriceEvolutionComponent, period 1), standardised over its last 60 daily values (min_periods 20), negated, and clipped at 0. The forecast is positive and grows linearly with the size of the Sunday fall in usual daily moves, up to the cap of 20. It is 0 when Sunday rose or was flat. On every other bar the regime is null and the forecast is 0. The 3-bar holding period carries each Sunday bet through Wednesday's close.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The cases are the Sunday bars with a forecast of 2 or more; Sundays are 7 bars apart, so their 3-bar returns never overlap. Per case, take the coin's 3-bar return from Sunday's close (close[t+3]/close[t]-1, inside the window) minus the coin's mean 3-bar return over all its windows. Measure the mean of (forecast/10) x that excess return across cases, with its t of the mean.
- Supporting check: Split the cases at the median forecast. The mean excess 3-bar return of the larger-fall half minus that of the smaller-fall half must be above 0.
- Confirm: The main measure's t is 2 or more, with at least 100 cases, and the supporting check passes.
- Reject: The main measure's t is -2 or less, with at least 100 cases.
- Inconclusive: Any t between -2 and 2, or a t of 2 or more with the supporting check failing. Fewer than 100 cases is also inconclusive, whatever the t.
