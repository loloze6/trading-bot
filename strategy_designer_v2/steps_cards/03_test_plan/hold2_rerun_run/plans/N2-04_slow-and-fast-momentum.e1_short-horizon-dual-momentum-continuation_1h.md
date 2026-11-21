---
idea: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's 60-day and 20-day returns are both positive -> adapted: the on/off condition is the regime, and the position inside it is graded by the size of the two returns.
- Comparison: higher than the coin's average daily return -> kept.
- Outcome: the next few days' returns are higher (continuation up), rather than over the following 20 days -> kept: the next few days are measured at 3 days (72 bars); the 20-day contrast is not the claim under test.
- Verdict transfer: yes: the test measures whether returns over the next 3 days, while both returns are up, beat the coin's average 3-day return.
Forecast: The regime detector computes the 1440-bar (60-day) and 480-bar (20-day) percent returns. When both are above 0, the bar is "trending". On every other bar the regime is null, so the forecast is 0 and the book is flat. In the trending regime, each of the two returns is standardised against its own past 500 values (min_periods 120) and clipped at 0. The forecast is their equal-weight mean, which is always positive there. It grows as either return gets larger against its usual size, up to the cap of 20, and it never goes short.
Config: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: The coin's 72-bar forward return, minus the coin's mean 72-bar return over all its windows (holding). It is measured on the non-overlapping 72-bar grid of each window, at grid bars where forecast > 0, pooled over coins, with the t of the mean.
- Supporting check: Over the trending bars, the book's mean daily timing gain (the book's daily return minus the gain from the market's own rise) is above 0.
- Confirm: The mean excess 72-bar return has t >= 2 over at least 100 cases, and the supporting check passes.
- Reject: The mean excess 72-bar return has t <= -2 over at least 100 cases.
- Inconclusive: A t between -2 and 2 is inconclusive. So is t >= 2 with a timing gain of 0 or below, or fewer than 100 non-overlapping in-situation cases.
