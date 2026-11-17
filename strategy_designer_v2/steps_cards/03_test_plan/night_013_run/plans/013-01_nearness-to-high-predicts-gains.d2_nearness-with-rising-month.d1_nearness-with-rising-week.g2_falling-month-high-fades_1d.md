---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: a coin's 30-day return is negative -> kept: a regime rule on the 30-bar price change below 0 activates the signal.
- Comparison: the closer the daily close sits to its highest close of the past 52 weeks -> kept: graded by the percent distance below the 364-bar highest close.
- Outcome: lower return over the next 7 days -> kept: the 7-bar forward return should fall as the close nears the high.
- Verdict transfer: yes: within falling-month bars the forecast grows only with the distance below the 52-week high, so its link to the 7-bar return is the idea's claim.
Forecast: The forecast is active only on bars where the 30-bar price change is below 0; on other bars it is 0. On active bars it reads DistanceFromHigh (period 364). This is the percent the close sits below its highest close of the last 364 bars, and is 0 at the high. The distance is standardised over its own past 364 values (min_periods 91) and negated. The forecast is therefore 0 when the close is at the 52-week high. It grows positive, graded, the further below the high the close sits, capped at 20. A larger forecast is a larger long. This expresses "closer to the high, lower 7-day return" as "further below the high, higher return".
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Use the non-overlapping 7-bar grid of each window, keeping grid bars whose regime is mean_reversion. Regress the coin's 7-bar forward return minus that coin's mean 7-bar return over all windows on the bar's forecast, pooled over coins. Report the slope's t.
- Supporting check: On the same cases, compare the mean excess 7-bar return of the third with the smallest forecast (nearest the high) against the third with the largest forecast. The nearest third minus the farthest third must be below 0.
- Confirm: The slope's t is 2 or more (positive) and the supporting check passes, with at least 100 cases.
- Reject: The slope's t is -2 or less: being further below the high is followed by lower returns, and being nearer the high by higher returns.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A confirming t whose supporting check fails is also inconclusive. So is any result on fewer than 100 independent cases.
