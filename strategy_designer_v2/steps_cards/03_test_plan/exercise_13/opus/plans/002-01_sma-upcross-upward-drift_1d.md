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
- Situation: the short moving average has just crossed above the long moving average -> adapted: "after the cross" becomes "while the 50-day SMA is above the 200-day SMA". The on/off cross becomes a graded measure: the percent spread of SMA50 over SMA200, kept only when positive.
- Comparison: price after random points -> adapted: random points are represented by all bars of the same windows, which is what simply holding BTC earns. Returns while the spread is positive are judged against the unconditional return of holding the coin.
- Outcome: price keeps rising over the following bars, more often and further than after random points -> kept: the forward 20-bar return of BTC, its sign (more often) and its size (further), measured after in-state bars.
- Verdict transfer: yes: if bars with SMA50 above SMA200 are followed by more frequent and larger rises than all bars, the cross-started uptrend persists; if they are not, or if they reverse, the idea fails as the brief states.
Forecast: One component, EMASpreadComponent with average "sma", fast 50 and slow 200 (the daily golden-cross convention). It computes (SMA50 − SMA200) / SMA200 × 100. - It is standardised against its own past 200 values (min_periods 50), so a typical spread gives about 10, which is a 100% long position, capped at 20. - It is then clipped at 0, so the forecast is long-only. - The forecast is zero while SMA50 is below SMA200 (before an upward cross, or after a downward cross ends the trend). - It is positive from the upward cross onward and grows continuously as the short average pulls further above the long one. - It never goes short, because the idea concerns only the upward cross.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: - Split each window into consecutive, non-overlapping 20-bar blocks, so overlapping returns are counted once. - Label a block "in-state" when the forecast is greater than 0 at its first bar. - For each in-state block, take BTC's close-to-close return over the block, before costs. - The measure is the mean of these in-state returns minus the mean 20-bar return over all blocks in all six windows (the buy-and-hold baseline, i.e. random points).
- Supporting check: Compare two hit rates: the share of in-state blocks with a positive 20-bar return, and the share of all blocks with a positive 20-bar return. Also check the dose-response: in-state blocks with a forecast at or above the in-state median should show a mean forward return at least as high as the blocks below it.
- Confirm: All three must hold: - The in-state mean 20-bar return exceeds the all-block mean by more than 0, with a one-sided t-statistic of at least 2.0 on the non-overlapping block returns. - The in-state hit rate exceeds the all-block hit rate. - The excess is positive in at least 4 of the windows that contain in-state blocks.
- Reject: Either of these: - The in-state mean excess return is 0 or below and the in-state hit rate is no higher than the all-block rate. - The excess is negative with a t-statistic of −2.0 or lower, meaning moves reverse after crosses.
- Inconclusive: - Any result in between, such as a positive excess with a t-statistic below 2.0, or a mean and a hit rate that disagree. - The test is also inconclusive if there are fewer than 12 non-overlapping in-state blocks, or fewer than 6 out-of-state blocks. - The six windows give about 36 blocks in total.
