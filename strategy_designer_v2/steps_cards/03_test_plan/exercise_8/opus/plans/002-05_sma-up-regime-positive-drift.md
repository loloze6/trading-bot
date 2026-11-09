---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: The 50-day and 200-day simple moving averages of the close, the most common pair on daily bars (golden and death cross). Take the spread (SMA50 - SMA200) / SMA200 in percent. Divide it by the mean absolute spread of the 200 bars before it and multiply by 10, capped at 20. Then clip it at 0. The forecast is positive while the 50-day average sits above the 200-day average, which is the stretch from an upward cross to the next downward cross. Its size grows with how far the short average has pulled above the long one. It is zero while the short average is below the long one, because the idea makes no claim about those stretches. It is never negative.
Config: 002-05_sma-up-regime-positive-drift_config.json
Confirm: Pool all six windows and use a 1-bar horizon, counting each daily return once. The mean next-bar BTC close-to-close return on bars with forecast > 0 must exceed the mean next-bar return over all tested bars by a t-statistic of at least 2.0, before costs. The supporting check is that the share of up bars among forecast > 0 bars is higher than the share of up bars over all tested bars.
Reject: The mean next-bar return on forecast > 0 bars is at or below the all-bar mean, or the strategy's equity does no better than buy-and-hold scaled to the same average exposure. A t-statistic of -2.0 or lower would also show that moves after up-crosses tend to reverse.
Inconclusive: The difference is positive but its t-statistic is below 2.0, or fewer than 100 tested bars have forecast > 0.
Deviation: The idea treats the up-cross stretch as one on/off state. The config instead sizes the position by the width of the SMA50/SMA200 spread, so it tests "while the short average is above the long one, and more so the wider the gap". It does not test an equal bet from each cross. Periods 50/200 are a convention, because the brief gives none. Only the long side of the cross is tested.
