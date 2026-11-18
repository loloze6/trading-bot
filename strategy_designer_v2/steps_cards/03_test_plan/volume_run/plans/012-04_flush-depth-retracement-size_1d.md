---
idea: 012-04_flush-depth-retracement-size
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4a01343a8148
---
Fidelity:
- Situation: a sharp fall on a volume burst with a long lower wick -> adapted: all three conditions form a regime rule. The graded open-to-low drop is the signal while the rule holds.
- Comparison: a larger open-to-low drop against a smaller one, among such bars -> kept
- Outcome: price rises over the next 3 days -> adapted: "after the flush" becomes "while the flush bar holds", and the 3-day hold is dropped. The 3-bar rise is measured on the record.
- Verdict transfer: yes: the test measures how the drop size on flush bars relates to the 3-bar rise, which is the idea's own claim.
Forecast: On every bar the detector checks three conditions: - the bar's return is at most -2 usual moves (VolatilityScaledReturn, 1 bar, 20-bar volatility); - volume is at least twice its mean over the prior 20 bars; - the lower wick is at least 0.3 of the bar's range. When all three hold, the bar is in the mean_reversion regime. The forecast there is the bar's open-to-low drop in percent, standardised against its last 60 values with target 5 (so a flush of two to four typical drops reads about 10 to 20, not the cap). It is clipped at 0, so it is long only. The forecast grows with the depth of the drop. On every other bar the forecast is 0.
Config: 012-04_flush-depth-retracement-size_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The cases are the flush bars (regime mean_reversion, forecast > 0). If two flush bars fall within 3 bars of each other in the same window, only the earlier one is kept. On these cases, regress the excess 3-bar return on the forecast and read the t of the slope. The excess 3-bar return is close[t+3]/close[t]-1 minus the coin's mean 3-bar return over all windows, measured inside the window only.
- Supporting check: The mean excess 3-bar return of the flush bars is above 0.
- Confirm: The slope is positive with t ≥ 2 and the supporting check passes.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: A slope t between -2 and 2 is inconclusive, as is a confirming slope whose mean excess return is not above 0. Fewer than 30 kept flush bars across all coins and windows is also inconclusive.
