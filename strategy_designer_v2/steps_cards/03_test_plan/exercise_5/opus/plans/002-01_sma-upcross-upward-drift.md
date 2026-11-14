---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: Use one indicator, the spread between the 50-day and 200-day simple moving averages of the close: (SMA50 − SMA200) / SMA200 × 100. These are the conventional daily golden-cross settings, since neither the brief nor the source gives periods. The spread is standardised against its own previous 200 values (current spread × 10 / mean absolute spread of the past 200 bars, capped at ±20). It is then clipped at 0 from below. - When it is positive: whenever SMA50 is above SMA200, that is, after an upward cross that has not yet been undone. It grows continuously as SMA50 pulls further above SMA200. An average-sized spread gives +10, or 100% long. - When it is zero: whenever SMA50 is at or below SMA200, or before warm-up is complete. - When it is negative: never. The idea concerns only the upward cross.
Config: 002-01_sma-upcross-upward-drift_config.json
Confirm: Use a horizon of 20 bars. In each window, sample bars 0, 20, 40, 60, 80 and 100, so the 20-bar forward returns do not overlap. That gives about 36 samples across the 6 windows. The idea is confirmed if two things hold, judged before costs: - Main measure: on samples where the forecast is above 0, the mean 20-bar forward log return of BTC exceeds the mean over all samples (that is, simply holding the coin) by a positive amount, with a t-statistic of at least 2. - Supporting check: the share of positive forward returns on those samples is higher than the share over all samples.
Reject: The idea is rejected if either of these holds: - The excess mean forward return on samples with a positive forecast is zero or negative, with at least 8 such samples. - That excess is negative with a t-statistic of −2 or below, which would show reversal after crosses.
Inconclusive: The result is inconclusive in any of these cases: - Fewer than 8 samples have a positive forecast. - The excess is positive but its t-statistic is below 2. - The excess comes entirely from a single window. - The excess is positive but the supporting hit-rate check fails.
Deviation: The idea says "after an upward cross"; the config tests "while SMA50 is above SMA200". The position is sized by how far apart the averages are, not by how recent the cross is. So the position is smallest right after the cross and largest later in the trend. The periods 50/200 are a convention, not taken from the source.
