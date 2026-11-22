---
idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: be08f97ea86e
---
Fidelity:
- Situation: the 30-day net move is small against the 30-day high-low range, the close sits below that range's middle, and the 10-day return is negative, larger when more negative -> kept: a rule needs NetMoveToRange(30, high-low) at or below 0.3 (a conventional "small") and the close below the 30-day high-low midpoint (Ichimoku spans of 30, displacement 0); the size of the short is the 10-day return.
- Comparison: the fall is moderate rather than extreme against its own recent 10-day moves -> kept: a veto sets the book flat when the 10-day return is 2 or more usual 10-day moves down (mean absolute 10-day move over 60 days).
- Outcome: the coin falls over the next 5 days -> kept: short, held 5 bars.
- Verdict transfer: yes: the same flat, below-middle, moderately falling bars are sized by the same return and judged on the same 5-day fall.
Forecast: Every bar is first checked by a veto. If the 10-day return, measured in usual 10-day moves over the last 60 days, is -2 or lower, the slide is extreme and the bar goes to a flat regime. Otherwise the bar is active only when both conditions hold: the 30-day net move is at most 0.3 of the 30-day high-low range, and the close is below that range's middle. On active bars the forecast is the 10-day percent return, standardised against its own last 60 values and clipped at 0. It is therefore short only, and it grows with the depth of the 10-day fall. On every other bar the forecast is 0.
Config: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On each window's non-overlapping 5-bar grid, take the bars with a forecast below 0 as cases. For each case, compute the coin's 5-bar return minus its mean 5-bar return over all windows, in the short direction. Report the t of the mean of these unusual moves.
- Supporting check: The half of the cases with the larger absolute forecast has a larger mean short-side unusual move than the smaller half (difference larger minus smaller above 0).
- Confirm: The main t is 2 or more over at least 30 cases, and the supporting difference is above 0.
- Reject: The main t is -2 or less over at least 30 cases.
- Inconclusive: A t between -2 and 2, a confirming t with a supporting difference at or below 0, or fewer than 30 cases in total.
