---
idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days, after a 20-day fall -> adapted: a regime selects bars whose close crosses a 90-day swing-high close level while the 20-day return is below 0, and "several times" becomes graded by weighting with the level's touch count.
- Comparison: a deeper 20-day fall against a shallower one -> kept: the short position grows with the depth of the 20-day fall.
- Outcome: the price falls over the next 10 days, more after deeper falls -> kept: a short held for 10 bars, larger after deeper falls.
- Verdict transfer: yes: the bars, the level, the fall, the side and the horizon are the idea's own, and the only change is that "several" is graded instead of a cut-off.
Forecast: The regime is `mean_reversion` only on a bar where two things hold. First, `ResistanceBreakTouchCountComponent` (period 90, side 2, band 2.0, cross_period 1) is above 0: the close has just crossed a level of past turn-down closes. Second, the 20-bar price change (`PriceEvolutionComponent`, period 20) is below 0. On every other bar the forecast is 0. On a selected bar, the forecast is the equal-weight mean of two parts: - the 20-bar change, standardised (window 60, min_periods 20) and clipped at most 0; - the break reading (touches x percent above the level), standardised (window 90, min_periods 22), then negated and clipped at most 0. The forecast is never positive. Its size grows with the depth of the 20-day fall and with how often the broken level held.
Config: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The cases are short signals (a bet on the short side), read once per 10-bar grid cell of each window. For each case, take the coin's 10-bar return from the signal's close, minus the coin's normal 10-bar drift over all windows, on the short side. Take the mean over all coins and cases, with the t of that mean.
- Supporting check: Split the cases at the median of the absolute forecast at entry. The larger-forecast half (deeper falls) has a larger mean drift-removed short-side move than the smaller half (difference above 0).
- Confirm: The mean short-side unusual move is above 0 with t >= 2, over at least 20 cases, and the supporting check passes.
- Reject: The mean short-side unusual move has t <= -2 over at least 20 cases, meaning the price rises after these breaks beyond its normal drift.
- Inconclusive: Any t between -2 and 2, fewer than 20 non-overlapping cases, or t >= 2 with the supporting check failing.
