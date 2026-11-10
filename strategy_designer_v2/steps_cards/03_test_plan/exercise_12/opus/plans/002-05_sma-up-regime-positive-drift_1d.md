---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: Uses the 50-day and 200-day simple moving averages of the daily close, the conventional daily "golden cross / death cross" pair. The raw value is the spread (SMA50 − SMA200) / SMA200 × 100. It is standardised against its own last 200 values, so a spread of typical size gives about +10 (100% long) and the forecast is capped at +20. Negative values are clipped to 0. The forecast is therefore positive, and grows with how far SMA50 sits above SMA200, on every bar from an upward cross until the next downward cross. It is exactly 0 (flat) from a downward cross until the next upward cross. It is never short.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Confirm: The horizon is 1 bar (next-day close-to-close return; each bar is counted once, with no overlap), pooled over the 6 windows, before costs. Two results together confirm the idea. First, the mean next-day return of BTC on bars with forecast > 0 exceeds the mean next-day return on all bars (buy-and-hold) by a t-statistic ≥ 2. Second, the supporting check holds: the share of up days on forecast > 0 bars beats the share on all bars, and is ≥ 52%.
Reject: The idea is rejected if the mean next-day return on forecast > 0 bars is at or below the all-bar mean. It is also rejected if the share of up days on forecast > 0 bars is no higher than on all bars. Either result means the up-cross stretches do no better than random stretches, or they reverse.
Inconclusive: Three results neither confirm nor reject. The excess mean return is positive but its t-statistic is below 2. The two measures disagree in sign. Fewer than 100 bars across all 6 windows carry forecast > 0, or fewer than 100 bars carry forecast = 0, too few for a fair comparison.
Deviation: The holding is not a fixed position from cross to cross. Its size grows with the width of the SMA50 − SMA200 gap: it is small just after a cross and larger as the gap widens. The criterion still judges the whole stretch where the forecast is positive. Only the long (upward-cross) stretch is tested. The brief's alternative trigger, "price crosses the long average", is not tested.
