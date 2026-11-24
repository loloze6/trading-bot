---
idea: 032-01_flat-range-upside-break-fades
brief: 032_choppy-market-breakouts-fail
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 051b3422f169
---
Fidelity:
- Situation: a coin gone nowhere over 60 days closes above its prior 60-day high -> adapted: "gone nowhere" is the Kaufman efficiency ratio over 60 bars at or below 0.3 (the convention for choppy), and "close above the prior 60-day high" is a regime rule, both held "while" true.
- Comparison: the close against the prior 60-day high, and the overshoot's size -> kept: the percent distance of the close above the highest high of the prior 60 bars grades the short.
- Outcome: a fall back toward the range over the next 10 days, larger for bigger overshoots -> kept: a short held 10 bars, sized by the overshoot.
- Verdict transfer: yes: the test shorts only trendless 60-day breakouts, sized by the overshoot, and measures the 10-day fall that follows.
Forecast: Two conditions select the regime. The first is the 60-bar efficiency ratio (smoothing 5) at or below 0.3. The second is a close above the highest high of the 60 bars before it. When both hold, the forecast is the percent distance of the close above that prior high. That distance is standardised against its own past 60 values, clipped at 0 and negated. On every other bar the forecast is 0. The forecast is never positive. It is negative only on a trendless breakout, and its size grows linearly with how far the close sits above the old high.
Config: 032-01_flat-range-upside-break-fades_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The cases are short bets, read once per 10-bar grid cell. For each case, take the coin's 10-bar return from the signal bar's close, minus the coin's normal 10-bar drift over all windows, signed for the short side (a fall is positive). The measure is the mean of these unusual moves, with t computed over days (cases on the same day summed into one).
- Supporting check: The least-squares slope of the case's short-side unusual move on the case's raw overshoot (`last_history_value` of "overshoot") must be positive.
- Confirm: The mean short-side unusual move has t ≥ 2, and the supporting slope is above 0.
- Reject: The mean short-side unusual move has t ≤ -2, meaning the breakouts keep rising beyond the coin's drift.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t ≥ 2 with a slope at or below 0. Fewer than 30 cases (or fewer than 30 distinct days) is inconclusive whatever the t.
