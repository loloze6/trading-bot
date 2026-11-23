---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 17ade308c2e6
---
Fidelity:
- Situation: a day's volume heavy against its prior 20-day average, with the close low in the day's high-low range -> kept: the volume over its prior 20-day mean times the close's distance from the high as a share of the range.
- Comparison: only while the 20-day volatility is high against its history, larger the higher it is -> kept: a regime rule on the 20-day volatility over its 60-day mean, and that ratio also scales the forecast.
- Outcome: the coin rises over the next day -> kept: a long position, 1 daily bar.
- Verdict transfer: yes: every part is measured as stated, so a confirm or reject of this forecast's next-day gains is a verdict on the idea.
Forecast: The forecast comes from one component, VolumeWeightedCloseLocationVolatilityRatioComponent, with volume_period 20, vol_period 20 and vol_lookback 60. Its raw value is the product of three factors: - (high − close) / (high − low) of the day; - the day's volume over its prior 20-day mean; - the 20-day return volatility over its 60-day mean. The raw value is standardised over 80 bars, with min_periods 20. It is never negative, so the forecast is long or flat. It grows with heavier volume, a lower close and higher volatility. It is active only on days whose 20-day volatility is at or above its 60-day mean. On all other days the forecast is 0 (flat).
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Use the regime-active bars of all coins and windows, pooled. Regress the coin's next-day return minus its mean daily return over all windows on the bar's forecast, and take the slope's t.
- Supporting check: The book's timing gain must be above 0. That gain is its mean daily return minus the part explained by the position times the coin's mean daily return.
- Confirm: The slope t is 2 or more, on at least 300 active bars, and the timing gain is above 0.
- Reject: The slope t is −2 or less, on at least 300 active bars.
- Inconclusive: Inconclusive covers three cases: - a slope t between −2 and 2; - a t of 2 or more with a timing gain at or below 0; - fewer than 300 regime-active bars pooled.
