---
idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: be08f97ea86e
---
Fidelity:
- Situation: the 30-day net move is small against the 30-day high-low range, the close is below that range's middle, and the coin fell over the past 10 days, larger falls counting more -> kept. A regime holds the flat-and-below-middle condition, using a net-move-to-range ratio of 0.5 or less (convention) and the close below the high-low midpoint. The size of the 10-day fall is graded.
- Comparison: a larger 10-day fall against a smaller one -> kept: the position grows with the size of the fall.
- Outcome: the coin falls over the next 5 days, falling more after larger falls -> kept: a short held 5 bars.
- Verdict transfer: yes: the test measures the stated condition, the stated graded driver and the stated 5-day fall, so its verdict is the idea's verdict.
Forecast: The forecast is active only when the 30-bar net move is at most half of the 30-bar high-low range and the close is below that range's midpoint. The midpoint is (highest high + lowest low) / 2 over the same 30 bars. When active, the forecast is the 10-bar percent return, standardised against its last 60 values and clipped at 0 from above. It is negative and grows in size with the depth of the 10-bar fall, and it is 0 when the coin rose. On every other bar it is 0. It is never positive.
Config: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Take the bars at positions 0, 5, 10, ... of each window where the regime is mean_reversion. On those bars, regress the coin's next-5-bar return, minus its mean 5-bar return over all windows, on the forecast. Report the slope's t.
- Supporting check: Take the cases, the grid bars with forecast ≤ -2. Their mean next-5-bar return minus drift, in the short direction, must be above 0.
- Confirm: The slope's t is at least 2 (more negative forecasts are followed by lower returns) and the supporting check passes.
- Reject: The slope's t is at most -2 (larger falls are followed by relative rises).
- Inconclusive: The idea is neither confirmed nor rejected when the slope's t is between -2 and 2. It is also inconclusive when t ≥ 2 but the check fails, or when fewer than 30 grid bars with forecast < 0 exist across coins and windows.
