---
idea: 025-02_deeper-fall-bigger-giveback
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: 90-day return negative and a one-day rise of several usual daily moves -> kept: a regime rule selects bars with a negative 90-bar return and a 1-bar return of at least 2 usual moves (20-bar volatility).
- Comparison: the deeper the 90-day fall, the larger the next fall -> kept: inside that regime the short grows with the depth of the 90-bar fall.
- Outcome: the price falls over the next 5 days -> kept: a short held for 5 bars after the rise bar.
- Verdict transfer: yes: the test asks directly whether deeper prior falls give larger 5-day falls after sharp one-day rises.
Forecast: The forecast is non-zero only on a bar where both conditions hold: the 90-bar return is below 0, and that bar's return is at least 2 usual daily moves (the one-bar return over the 20-bar standard deviation of daily returns). On those bars the forecast is the 90-bar percent return, standardised against its own last 90 values and clipped at 0, so it is never long. It is more negative, so a larger short, the deeper the 90-day fall. It reaches -10 at the usual size of the 90-bar move and is capped at -20. On every other bar it is 0. Each short is held for 5 bars.
Config: 025-02_deeper-fall-bigger-giveback_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: A case is a short bet (a fall of the forecast of at least 2 points), read once per cell of the 5-bar grid of each window. For each case, take the coin's 5-bar forward return minus its normal 5-bar drift over all windows. Regress that on the case's forecast, pooling all coins; the measure is the slope's t.
- Supporting check: The mean unusual move of the cases in the short direction (the drift-adjusted 5-bar return, sign flipped) is above 0.
- Confirm: The slope is positive with t ≥ 2: a more negative forecast, meaning a deeper fall, comes with a more negative 5-bar return. The supporting check must also pass.
- Reject: The slope is negative with t ≤ -2: deeper falls are followed by smaller falls or by rises.
- Inconclusive: A slope t between -2 and 2, or a confirming slope with a mean unusual move of 0 or below. Fewer than 30 cases is also inconclusive, whatever the result.
