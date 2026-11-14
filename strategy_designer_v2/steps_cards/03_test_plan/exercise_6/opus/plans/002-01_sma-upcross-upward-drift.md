---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: Take the percent spread between the 50-day and 200-day simple moving averages of the close, (SMA50 − SMA200) / SMA200 × 100. The brief gives no lengths, so I used the most common daily-bar convention, the 50/200 "golden cross". Standardise the spread against its own previous 200 values (window 200, min_periods 50), so a typical spread maps to about 10, capped at 20. Then clip it at 0 from below. The forecast is zero while SMA50 is at or below SMA200. It turns positive the moment SMA50 crosses above SMA200, starting from zero with no jump. It grows in proportion to how far SMA50 has pulled above SMA200, up to +20 (200% long). It never goes short, because the idea is only about the upward cross.
Config: 002-01_sma-upcross-upward-drift_config.json
Confirm: The horizon is 20 bars. Sample one bar every 20 bars, so overlapping returns are counted once, and pool the samples across the 6 windows. The idea is confirmed if two things hold: - Main measure: on sampled bars with forecast > 0, the forecast-weighted mean forward 20-bar return of BTC beats the mean forward 20-bar return of all sampled bars (the buy-and-hold baseline) by at least 1.0 percentage point. This must hold in at least 4 of the 6 windows that have active bars. - Supporting check: the share of active samples with a positive forward 20-bar return is higher than the same share over all samples.
Reject: The idea is rejected if the forecast-weighted forward 20-bar return on active bars is at or below the all-bars baseline in the pooled sample. It is also rejected if that return is negative, which would mean moves after upward crosses reverse.
Inconclusive: The result is inconclusive in any of these cases: - The pooled excess is positive but below 1.0 percentage point. - The excess is positive pooled but holds in fewer than 4 of the windows with active bars. - Fewer than 10 non-overlapping active samples exist across all windows.
Deviation: The idea says "after an upward cross". The config tests "while SMA50 is above SMA200, more strongly the wider the gap". The position starts near zero right at the cross and is largest later in an established uptrend, not just after the cross event.
