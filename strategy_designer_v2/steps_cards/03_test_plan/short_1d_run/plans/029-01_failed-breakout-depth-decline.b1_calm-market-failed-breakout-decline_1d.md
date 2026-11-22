---
idea: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 5f0a6e1d2346
---
Fidelity:
- Situation: a daily close above the prior 20-day high, then a close back below that old high within 3 days -> adapted: on/off made graded and "after" made "while": FailedBreakoutDepthInUsualMoves (20, 3) is positive while the close sits below the old high, after a breakout 1 to 3 bars earlier, and grows with the depth below it.
- Comparison: only while the 20-day volatility of daily returns is low, and the lower it is, the larger the fall -> adapted: the on/off "low" condition is made graded by dividing the depth by the 20-day return volatility, so the reading grows as volatility falls.
- Outcome: the coin falls over the next 5 days -> kept: short, with each bet held 5 bars.
- Verdict transfer: yes: the forecast is short only on failed breakouts and is larger when 20-day volatility is lower, so falls over 5 bars confirm the idea and their absence rejects it.
Forecast: FailedBreakoutDepthInUsualMovesComponent (period 20, fail_window 3, vol_period 20, exclude_current 1, lag 0) is the depth of today's close below the prior 20-day closing high, measured only when that high was broken 1 to 3 bars ago. The depth is divided by the standard deviation of the last 20 daily returns. It is 0 when there is no failed breakout and positive while one holds. It grows with the depth and as volatility gets lower. It is standardised over the 60 values before the bar (min_periods 20), then negated. The forecast is therefore 0 away from failed breakouts and negative during one (short only), larger in size the deeper the failure and the calmer the coin.
Config: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are short bets: a fall of the forecast of at least 2 points below its highest level since its last bet, read once per 5-bar grid cell of each window. For each case, take the coin's 5-bar return from the signal bar's close, minus the coin's mean 5-bar return over all its windows, with the sign flipped so that a fall is positive. The measure is the mean of this unusual move over all cases, with its t.
- Supporting check: Split the cases at the median of |forecast| (deeper failure in calmer markets above the median). The mean unusual move of the top half minus that of the bottom half must be above 0.
- Confirm: The mean unusual move in the short direction is above 0 with t >= 2, and the supporting check passes.
- Reject: The mean unusual move in the short direction is below 0 with t <= -2, meaning the coin rose more than usual after these cases.
- Inconclusive: Any t between -2 and 2, or a confirming t with a failed supporting check. Fewer than 30 independent cases over all coins and windows is inconclusive whatever the t.
