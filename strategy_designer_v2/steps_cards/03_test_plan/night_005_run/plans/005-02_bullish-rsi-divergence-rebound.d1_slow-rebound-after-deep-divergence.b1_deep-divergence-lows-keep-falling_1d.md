---
idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the close makes a new 30-day low while the 14-day RSI is above its reading at the previous low in that window -> kept: a regime rule fires when the close is below the prior 30-bar low and the RSI change since the prior low is above 0.
- Comparison: the RSI now against the RSI at the previous low in the window -> kept: `RsiChangeFromPriorLowComponent` (14, lookback 30) is above 0.
- Outcome: the price keeps falling over the next 20 days, and falls more the deeper the 30-day decline -> adapted: holding period dropped; a short sized by the 30-day decline is held while the divergence low lasts and is judged on 20-bar forward returns.
- Verdict transfer: yes: the test measures the idea's event, side and size relation directly, and only drops the 20-day hold.
Forecast: Two measures decide when the forecast is not zero. The first is the close's distance below the lowest close of the prior 30 bars. The second is the 14-day RSI now minus the RSI at the lowest close of bars t-30 to t-4. When the close is below the prior 30-bar low and that RSI change is above 0, the bar is a divergence low, and the forecast is the 30-bar return standardised over its past 60 values and clipped at 0. That return is negative at a new low, so the forecast is short, and the short grows with the depth of the 30-day decline. On every other bar the forecast is 0 (flat). It is never positive.
Config: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The excess 20-bar return after event bars. Event bars are bars with regime `trending` and forecast < 0, keeping only the first event bar in any 20-bar span within a window. The excess return is the coin's return over the next 20 bars minus the coin's mean 20-bar return on the non-overlapping grid over all windows. The statistic is the ordinary t of the mean, pooled over coins.
- Supporting check: Across the same event bars, the slope of the excess 20-bar return on the absolute forecast (the depth) is below 0.
- Confirm: The mean excess return is negative with t <= -2 over at least 20 events, and the depth slope is below 0.
- Reject: The mean excess return is positive with t >= +2 over at least 20 events.
- Inconclusive: Any t between -2 and +2, or a confirming t with a depth slope of 0 or above. Fewer than 20 independent events is inconclusive whatever the t.
