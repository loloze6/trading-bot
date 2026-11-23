---
idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: at a funding settlement time, the 2-hour move into it runs against the coin's 24-hour trend -> kept
- Comparison: the pre-move judged against the 24-hour trend's direction, with size set by the trend's strength -> kept
- Outcome: over the 8 hours after settlement the price runs opposite to the pre-move, and moves more when the trend is stronger -> kept
- Verdict transfer: yes: the book bets only at the bar closing on each settlement, only when the pre-move opposes the trend, sizes the bet by the trend and holds it 8 hours, which is exactly the idea's claim.
Forecast: The regime detector selects only the bar whose close is a funding settlement (00:00, 08:00 or 16:00 UTC), read by HoursToSettlementComponent = 8 for the coming bar. On that bar: - If the 2-bar return is below 0 and the 24-bar return is above 0, the regime is "trending". - If the 2-bar return is above 0 and the 24-bar return is below 0, the regime is "mean_reversion". - Every other bar is "unknown" or "chop", which are flat. In both active regimes the forecast is the 24-bar return (PriceEvolutionComponent, period 24), standardised over its past 60 values (target 10, cap 20). - It is positive (long) after a pre-dip against an uptrend. - It is negative (short) after a pre-rally against a downtrend. - Its size grows continuously with the strength of the 24-hour trend. - It is zero at every other time. The bet made at settlement is held for the 8 bars to the next settlement.
Config: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses_1h_config.json
Criterion:
- Horizon: 8 bars
- Main measure: The cases are settlement bars where the regime is trending or mean_reversion and |forecast| is at least 2. For each case, take the coin's 8-bar return from that bar's close minus the coin's normal 8-bar drift, multiplied by the sign of the forecast. The measure is the t of the mean of these values across all coins and windows. - The coin's normal 8-bar drift is the mean return on the non-overlapping 8-bar grid over all windows. - Settlements are 8 bars apart, so the cases do not overlap.
- Supporting check: Across the cases, the slope of the signed excess 8-bar return on |forecast| is above 0.
- Confirm: The idea is confirmed only when both of these hold: - The mean signed excess return has t ≥ 2. - The slope on |forecast| is positive.
- Reject: The mean signed excess return has t ≤ -2.
- Inconclusive: Any of these results neither confirms nor rejects: - t between -2 and 2. - t ≥ 2 but with a slope of 0 or below. - Fewer than 100 cases in total.
