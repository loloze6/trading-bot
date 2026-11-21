---
idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 0974d5467d9f
---
Fidelity:
- Situation: a 4h bar closes above the highest high of the preceding two-day (12-bar) stretch -> adapted: the on/off breakout is made graded, as the size of the close above that high (0 when there is no breakout).
- Comparison: the stretch's narrowness against the 30-day (180-bar) average 4h range, and the 7-day (42-bar) average range against the 60-day (360-bar) average -> kept: the two ratios B/S and L/Q multiply the breakout size.
- Outcome: the coin rises over the next three days (18 bars), more so the narrower and quieter the setup -> kept: each bet is held 18 bars, and the gain is read against holding the coin.
- Verdict transfer: yes: the component computes the idea's breakout, its narrowness weight and its quiet-week weight on each coin's own bars, and each bet is held for the idea's 3-day horizon.
Forecast: The forecast uses one indicator, NarrowRangeBreakoutRangeRatio, with period 12, base_period 180, ratio_long_period 360 and ratio_short_period 42. Its raw value is the close's break above the prior 12-bar high, in percent of the close. That value is multiplied by the 180-bar mean bar range over the 12-bar stretch's range. It is multiplied again by the 360-bar mean bar range over the 42-bar mean bar range. The result is standardised against its own past 360 values (min_periods 90). The forecast is zero when the close is not above the prior 12-bar high, and never negative. It is positive on a breakout and grows with the size of the break, with how narrow the stretch was, and with how quiet the past week was against the past 60 days. It is capped at 20.
Config: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The cases are the bets: a rise of the forecast of at least 2 points, read once per 18-bar grid cell of each window, pooled over the coins and windows. For each case, take the coin's return over the next 18 bars minus its normal 18-bar drift (holding the coin), before costs. The measure is the mean of that excess return, with its ordinary t.
- Supporting check: Split the cases at the median entry forecast. The Welch t of the high-forecast half's mean excess return minus the low-forecast half's must be above 0. This tests that narrower and quieter setups rise more.
- Confirm: The idea is confirmed when the mean excess return has t >= 2 over at least 100 cases, and the supporting check's Welch t is above 0.
- Reject: The idea is rejected when the mean excess return has t <= -2 over at least 100 cases.
- Inconclusive: The result is inconclusive when t is between -2 and 2, or when t >= 2 but the high-forecast half does not beat the low-forecast half. It is also inconclusive with fewer than 100 cases in total.
