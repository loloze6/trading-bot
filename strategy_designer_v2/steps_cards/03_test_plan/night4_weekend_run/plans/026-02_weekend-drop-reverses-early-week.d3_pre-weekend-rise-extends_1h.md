---
idea: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 08ec5a873928
---
Fidelity:
- Situation: the coin rose over the two days before Friday 00:00 UTC -> adapted: measured once, at the close of the bar that ends at Friday 00:00, as the 48-bar return graded by size (rises only).
- Comparison: a larger two-day rise against a smaller one -> kept: the position grows with the 48-bar rise.
- Outcome: the price keeps rising over Friday and Saturday -> kept: the bet is held 48 bars, long.
- Verdict transfer: yes: the test bets only at Friday 00:00, only on rises, sized by the rise, and holds it over Friday and Saturday, as the idea states.
Forecast: The regime detector selects one bar a week per coin: the bar whose coming bar starts Friday 00:00 UTC (weekday 4, hour 0). On that bar only, the forecast is the 48-bar percent return (Wednesday 00:00 to Friday 00:00), standardised against its own past 60 values. It is clipped at 0, so it is positive and grows with the size of the two-day rise. It is zero after a two-day fall and on every other bar. The bet is held for 48 bars.
Config: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The cases are the Friday 00:00 bars with a forecast above 0, one per coin per week, so the cases do not overlap. For each case, take the coin's 48-bar return from that close minus the coin's mean 48-bar return over all its windows. Regress this excess return on the forecast across all cases, and read the t of the slope.
- Supporting check: Over the same cases, the forecast-weighted mean of the excess 48-bar return is above 0.
- Confirm: The slope's t is 2 or more, and the forecast-weighted mean excess return is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2 is inconclusive. So is a t of 2 or more with a forecast-weighted mean of 0 or below. At least 100 cases are required across coins and windows; with fewer, the result is inconclusive.
