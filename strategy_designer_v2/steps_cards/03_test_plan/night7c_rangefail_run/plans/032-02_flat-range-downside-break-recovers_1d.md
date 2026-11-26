---
idea: 032-02_flat-range-downside-break-recovers
brief: 032_choppy-market-breakouts-fail
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 051b3422f169
---
Fidelity:
- Situation: a coin gone nowhere over 60 days closes below its prior 60-day low -> kept: a regime holds the position only when the 60-day efficiency ratio is at or below 0.3 (the convention for choppy) and the close is under the prior 60-day low; elsewhere the book is flat.
- Comparison: the further the close sits below the old low, the larger the share recovered -> adapted: the position is graded by the close's percent depth under the prior 60-day low.
- Outcome: price rises back toward the range over the next 10 days -> kept: a long held for 10 daily bars.
- Verdict transfer: yes: the test measures the same trendless breakdown, its depth, the long 10-day outcome and its scaling with depth.
Forecast: The regime detector selects mean_reversion when two things hold. The first is that the 60-bar Kaufman efficiency ratio (smoothed over 5) is at or below 0.3. The second is that the close is below the lowest low of the prior 60 bars, with bar t excluded. On every other bar the forecast is 0. Inside the regime, the forecast is long and graded. It uses the close's signed percent distance from the prior 60-day low. That distance is standardised against its own past 60 values, then negated, so a deeper close below the old low gives a larger long. It is clipped at 0, so it is never short.
Config: 032-02_flat-range-downside-break-recovers_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: For each case, take the coin's 10-bar return from the close of the signal bar, minus the coin's mean 10-bar return over all windows. A case is a long bet, read once per non-overlapping 10-bar grid cell of each window. The measure is the mean of these excess returns, with its day-clustered t.
- Supporting check: The share of the overshoot recovered must grow with the depth of the close below the old low. The share is the excess 10-bar return divided by the depth, where the depth is minus `depth.last_history_value` / 100. The check passes when the slope of the share on the depth has t ≥ 2.
- Confirm: The mean excess return is positive with t ≥ 2 over at least 30 cases, and the supporting slope is positive with t ≥ 2.
- Reject: The mean excess return has t ≤ -2 (breakdowns keep going), or the slope of the share on the depth has t ≤ -2 (bigger breaks are recovered less).
- Inconclusive: Any other result is inconclusive: a main t between -2 and 2, or a main confirm with a slope t between -2 and 2. Fewer than 30 cases is also inconclusive, whatever the t.
