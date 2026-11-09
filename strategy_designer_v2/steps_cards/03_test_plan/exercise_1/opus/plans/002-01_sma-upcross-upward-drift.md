---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Config: 002-01_sma-upcross-upward-drift_config.json
Confirm: The mean next-bar return of BTC on bars where the forecast is above 0 (SMA50 above SMA200) is higher than its mean return over all bars, before costs. The strategy's return per unit of average exposure also beats buy-and-hold over the same period. Within those long bars, next-bar returns rise with the size of the forecast, so that the top third of forecasts earns more than the bottom third.
Reject: The mean next-bar return while the forecast is above 0 is no higher than the unconditional mean, or the return per unit of exposure does not beat buy-and-hold. It is also rejected if returns fall as the forecast grows, with the largest spreads followed by reversals, which would mean the cross marks exhaustion and not the start of a trend.
Deviation: "After the short average crosses above the long one" becomes "while SMA50 is above SMA200, long in proportion to the percent gap between them". This changes the test in four ways. The position is small right at the cross and grows as the gap widens, so the test weights the established part of the trend more than the bars just after the cross. The idea gives no periods, so 50/200, the conventional daily golden cross, is assumed. Only the upward cross is tested: the forecast is clipped at 0, so there is no short side after a downward cross. Results are read on all bars above the cross, not on fixed windows after each cross event.
