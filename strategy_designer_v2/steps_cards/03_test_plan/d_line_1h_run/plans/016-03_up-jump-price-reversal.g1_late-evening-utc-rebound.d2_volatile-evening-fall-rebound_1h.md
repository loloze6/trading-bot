---
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin fell over the 24 hours up to the 20:00 UTC close -> adapted: the 24-bar fall is made graded and read on the bar closing at 20:00 UTC.
- Comparison: only while 10-day hourly volatility is high, with a larger rise the higher it is -> adapted: "high" is a regime condition on the 240-bar volatility rank, and the fall is sized in percent against its own long past, which grows with volatility.
- Outcome: the coin rises over the next 24 hours -> adapted: the 24-hour holding period is dropped, and the rise is read 24 bars after each 20:00 forecast.
- Verdict transfer: yes: the test bets long on the 20:00 fall only in high-volatility regimes, and grades the bet by a fall size that grows with volatility, which is what the idea claims.
Forecast: The regime is active only when both hold: - the coming bar starts at 20:00 UTC (the current bar closes at 20:00); - the 240-bar (10-day) hourly volatility ranks at or above the middle of its last 720 bars. In that regime the forecast comes from the 24-bar price change in percent, negated so that a fall reads positive. It is standardised against the mean absolute size of its own last 500 values and clipped at 0. It is therefore positive and grows with the size of the fall, and a percent fall is larger when volatility is high. It is 0 when the coin rose over the 24 hours, and 0 (flat) on every other hour and in calm markets. It is never negative.
Config: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The cases are the bars with forecast > 0 (at most one per day, so their 24-bar returns do not overlap). For each case, take the 24-bar forward return close[t+24]/close[t]-1 minus the coin's mean 24-bar return over all windows. Report the forecast-weighted mean of this excess return, pooled over coins and windows, with its t-statistic.
- Supporting check: Split the cases by forecast into thirds. The mean excess 24-bar return of the top third minus that of the bottom third must be above 0.
- Confirm: The forecast-weighted mean excess return is positive with t ≥ 2, and the top-minus-bottom-third difference is above 0.
- Reject: The forecast-weighted mean excess return is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2. Also inconclusive: t ≥ 2 while the top-minus-bottom-third difference is not above 0. Neither a confirm nor a reject is possible with fewer than 100 pooled cases.
