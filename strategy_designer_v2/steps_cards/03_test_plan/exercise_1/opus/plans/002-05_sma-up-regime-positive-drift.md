---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Config: 002-05_sma-up-regime-positive-drift_config.json
Confirm: The test confirms the idea if, before costs, BTC's mean next-day return on bars with a positive forecast (the up-cross stretches) beats its mean next-day return over all bars. The strategy's return per unit of average exposure must also beat buy-and-hold, and next-day returns should not shrink as the forecast grows.
Reject: The test rejects the idea if, on positive-forecast bars, the mean next-day return is no higher than the unconditional mean and the strategy's return per unit of exposure does not beat buy-and-hold. It also rejects the idea if returns fall as the spread widens, which would mean the cross marks exhaustion rather than a trend.
Deviation: The idea's on/off state ("between an up-cross of SMA50 over SMA200 and the next down-cross") becomes "long in proportion to how far SMA50 sits above SMA200, flat when it is below". Days just after a cross get a small position and days deep in the stretch get a large one, so the test weights the middle and late part of each stretch, not the stretch evenly. The 50/200 periods are the conventional golden-cross choice, because the source gives no lengths. The comparison is against the unconditional mean and buy-and-hold, not against randomly placed stretches of equal length.
