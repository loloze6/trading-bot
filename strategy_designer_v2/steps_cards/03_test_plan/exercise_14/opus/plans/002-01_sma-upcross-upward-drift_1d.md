---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a short moving average of price has just crossed above a long moving average -> adapted: "after the cross" becomes "while the short SMA stays above the long SMA". This is the state that begins at the upward cross and ends at the cross back, which the brief says ends the trend. The on/off cross event becomes graded by the percent spread between the two SMAs. Settings are the daily-bar convention, SMA 50 over SMA 200.
- Comparison: price after random points -> kept: forward returns from active bars are compared with forward returns from all bars of the same windows, which is the same as simply holding the coin.
- Outcome: price keeps rising over the following bars, more often and further -> kept: the up-share and the mean of forward returns after active bars, long side only.
- Verdict transfer: yes: the forecast is non-zero exactly over the bars that follow an upward cross until the trend ends, so the direction and size of later returns on those bars, compared with all bars, confirm or reject the idea as stated.
Forecast: The percent spread of the 50-bar SMA over the 200-bar SMA of the close is computed as (SMA50 − SMA200) / SMA200 × 100. It is standardised against its own past 200 values, with window 200 and min_periods 50, so that an average spread reads about 10. It is capped at 20, then clipped at 0 from below. The forecast is zero while the short average is below the long one, which is before an upward cross or after a downward one. It is positive from the moment the 50-SMA crosses above the 200-SMA. It grows smoothly as the short average pulls further above the long one, to at most +20, which is a 200% long position. It is never negative.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Take the BTC close-to-close return over the next 20 bars, starting at bars where the forecast is above 0. Use non-overlapping blocks: after a case is counted, the next one starts no earlier than 20 bars later. Compare these returns with 20-bar returns from non-overlapping blocks across all bars of the same six windows, which is buy-and-hold from random points. Two numbers are measured: the excess in mean 20-bar return, and the excess in the share of blocks that end up. Both are measured before costs.
- Supporting check: Over all active bars, the Spearman rank correlation between the forecast size and the following 20-bar return, counted on non-overlapping blocks. It should be positive if a larger spread means a more established trend.
- Confirm: Both of the following hold: - The mean 20-bar return after active bars exceeds the all-bars mean by at least +2 percentage points, with a one-sided t-statistic of at least 1.5 on non-overlapping blocks. - The up-share after active bars exceeds the all-bars up-share by at least 10 percentage points.
- Reject: Any one of the following: - The excess mean 20-bar return is at or below 0. - The up-share after active bars is at or below the all-bars up-share. - The mean 20-bar return after active bars is negative in absolute terms, meaning moves after upward crosses reverse.
- Inconclusive: These results neither confirm nor reject: - The excess mean is positive but below +2 points. - The t-statistic is below 1.5. - The up-share edge is between 0 and 10 points. Any result is also inconclusive if fewer than 10 non-overlapping active 20-bar blocks exist across the six windows, which is likely if the 50/200 state is rarely on.
