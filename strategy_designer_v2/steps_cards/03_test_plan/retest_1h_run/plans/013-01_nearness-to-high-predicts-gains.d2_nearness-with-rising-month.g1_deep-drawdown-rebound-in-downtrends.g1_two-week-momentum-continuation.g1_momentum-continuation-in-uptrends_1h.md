---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's 14-day rise, larger meaning stronger -> kept: the 336-bar percent return, graded and kept long-only, as the idea speaks of rises.
- Comparison: only among coins whose 60-day return is positive, larger rise against higher return -> kept: a regime on the coin's own 1440-bar return above 0, with the relation read across that coin's bars over time.
- Outcome: a higher return over the next 7 days, upward -> kept: the forward 168-bar return.
- Verdict transfer: yes: the test measures within each coin whether a larger 14-day rise, in an up 60-day trend, is followed by a larger 7-day return, which is the idea's per-coin claim.
Forecast: The regime is "trending" while the coin's 1440-bar (60-day) return is above 0. On all other bars the regime is "unknown" and the forecast is flat. In the trending regime the forecast is the coin's 336-bar (14-day) percent return, scaled by the mean size of its last 336 values (target 10, capped at ±20) and clipped at 0. It is positive and grows with the size of the 14-day rise, and it is 0 when the coin fell over 14 days. It is never negative.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1h_config.json
Criterion:
- Horizon: 168 bars
- Main measure: The sample is the non-overlapping 168-bar grid of each window, using only bars whose regime is trending. On it, regress the forward 168-bar return minus the coin's mean 168-bar return over all windows on the forecast, pooled across coins. The measure is the t of that slope.
- Supporting check: The slope is positive in at least 4 of the 6 coins.
- Confirm: The slope t is at least 2 and the supporting check passes.
- Reject: The slope t is at most -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, and so is t ≥ 2 when the coin check fails. The test needs at least 100 independent trending grid bars in total, with at least 30 of them carrying a forecast above 0; with fewer it is inconclusive.
