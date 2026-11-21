---
idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the daily close's distance below its highest close of the past 90 days -> kept: the percent distance of the close below its 90-bar closing high, graded.
- Comparison: closer to the high against farther from it -> kept: the distance is centred on its own usual size, so nearer than usual reads long and farther reads short.
- Outcome: a higher return over the next 5 days -> kept: each bet is held 5 daily bars and judged on the 5-bar return against holding the coin.
- Verdict transfer: yes: the forecast is the idea's own nearness measure, graded, and is judged on the idea's own 5-day return.
Forecast: The forecast starts from the percent distance of the close below its highest close of the last 90 daily bars, current bar included. This distance is 0 at a new high and negative below it. It is standardised over 90 bars, so it averages about -10. A constant of +10, standardised, is added at equal weight, which gives (x + 10) / 2. The forecast is about +5 at a new 90-day high and positive whenever the close is nearer the high than usual. It is 0 at the usual distance, and negative, growing to about -5, as the close sits twice its usual distance below the high or farther. The size grows continuously with nearness, and there is no regime.
Config: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the coin's 5-bar forward return, minus its normal drift over all windows, on the forecast at the bar. Bars are taken on each window's non-overlapping 5-bar grid and pooled over coins and windows, before costs. The measure is the t of that slope.
- Supporting check: The book's timing gain is positive before costs: its mean daily return minus its gain from the market's own rise.
- Confirm: The slope's t is 2 or more over at least 1000 independent grid cases, and the supporting check passes.
- Reject: The slope's t is -2 or less over at least 1000 independent grid cases.
- Inconclusive: A t between -2 and 2, fewer than 1000 grid cases, or a confirming slope whose timing gain is not positive.
