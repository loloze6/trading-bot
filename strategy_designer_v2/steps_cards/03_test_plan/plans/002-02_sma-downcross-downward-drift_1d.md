---
idea: 002-02_sma-downcross-downward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: The 50-day and 200-day simple moving averages of the close (the usual daily cross pair, since the brief gives no settings). The spread is (SMA50 − SMA200) / SMA200 × 100. It is standardised against its own previous 200 values (target 10, cap 20) and keeps only its negative side. The forecast is zero while SMA50 is at or above SMA200. Once SMA50 is below SMA200 the forecast is negative (short), and it grows in size as SMA50 falls further below SMA200, up to −20.
Config: 002-02_sma-downcross-downward-drift_1d_config.json
Confirm: Horizon 20 bars. Use one 20-bar block every 20 bars, so overlapping returns count once, and keep the blocks that start with the forecast non-zero. In each block, take BTC's 20-bar forward return minus the mean 20-bar return of its window, and multiply it by −forecast/10. The idea is confirmed if: - there are at least 10 such active blocks across the 6 windows; - the mean of this product is positive with a t-statistic of at least 2.0, before costs; - as a supporting check, more than 55% of active blocks have a negative excess forward return.
Reject: The idea is rejected if there are at least 10 active blocks and the mean product is zero or negative (t-statistic of 0 or below). It is also rejected if 50% or fewer of active blocks have a negative excess forward return. Either result means price does not fall more often or further than at random points, or it reverses after the cross.
Inconclusive: Fewer than 10 non-overlapping active blocks, which is possible because 50/200 crosses are rare in six 122-day windows. Also inconclusive: a positive mean product with a t-statistic between 0 and 2.0.
Deviation: "After a downward cross" becomes "while SMA50 is below SMA200". The position is sized by how far below it is, not by how recent the cross is. Bars long after the cross count as much as bars just after it, and the position fades as the spread narrows rather than at a fixed number of bars after the event.
