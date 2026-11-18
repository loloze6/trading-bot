---
idea: 012-03_lower-wick-flush-recovery
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 70a362722b07
---
Fidelity:
- Situation: a bar that falls sharply on a volume burst -> kept: the bar's return is at most -2 usual moves (20-bar) and its volume is at least 2x its prior 20-bar mean (conventional cut-offs).
- Comparison: a longer lower wick below the close, as a share of the high-to-low range -> kept: (close - low) / (high - low) on the flush bar, graded.
- Outcome: a larger price rise over the next 3 days -> adapted: holding period dropped; the position is held only on the flush bar, and the 3-bar rise is read from the recorded closes.
- Verdict transfer: yes: the same bars and wick are measured, and the 3-bar rise is scored directly on them.
Forecast: The regime detector marks a bar "mean_reversion" when both conditions hold: - its one-bar return is at most -2 usual moves (VolatilityScaledReturnComponent, period 1, vol_period 20); - its volume is at least 2x the mean of the prior 20 volumes (VolumeRatioComponent, period 20, exclude_current 1). On every other bar the forecast is 0 (flat). On a flush bar the forecast is the close's location in the bar's range, (close - low) / (high - low) from CloseLocationInRangeComponent "low", standardised against its past 60 values. It is long only, about 0 for a close at the low and up to 20 (capped) for a close near the high. It grows linearly with the lower wick.
Config: 012-03_lower-wick-flush-recovery_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Use the flush bars (regime "mean_reversion"), keeping per coin and window only bars at least 3 bars after the previously kept one. On these bars, take the OLS slope t of the excess 3-bar return on the wick value (wick `post_pipeline_value`), pooled over coins. The excess 3-bar return is close[t+3]/close[t] - 1 minus the coin's mean 3-bar return over all windows.
- Supporting check: The mean excess 3-bar return of the flush bars whose wick is above the median of flush bars is above 0.
- Confirm: The slope t is 2 or more and the supporting check passes.
- Reject: The slope t is -2 or less.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. A slope t of 2 or more with a check that fails is also inconclusive. So is any result with fewer than 30 independent flush bars.
