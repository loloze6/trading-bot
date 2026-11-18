---
idea: 012-03_lower-wick-flush-recovery
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4a01343a8148
---
Fidelity:
- Situation: a bar that falls sharply on a volume burst -> kept: a regime rule, fall of 2 or more usual moves with volume at least twice its prior 20-bar mean.
- Comparison: a longer lower wick below the close, as a share of the bar's range -> kept: the lower wick over the high-to-low range, graded.
- Outcome: a larger price rise over the next 3 days -> adapted: holding period dropped, and the 3-bar rise is read from prices after each flush bar.
- Verdict transfer: yes: the test checks whether, among sharp high-volume falls, the 3-day rebound grows with the wick share, which is the idea's claim.
Forecast: The forecast is non-zero only on bars where two conditions hold. The first is that the one-bar return is -2 or less in units of its 20-bar standard deviation. The second is that volume is at least 2 times the median of the prior 20 bars' volume. On those bars the forecast is long, set by the lower wick (min(open, close) − low) as a share of the bar's range. That share is standardised against its own past 60 values, so an average wick gives about +10, no wick gives 0, and a long wick gives up to +20. On all other bars the forecast is 0. It is never negative.
Config: 012-03_lower-wick-flush-recovery_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: On flush bars (regime mean_reversion), the slope of a regression of excess 3-bar return on the forecast. Excess return is close[t+3]/close[t] − 1 minus the coin's mean 3-bar return over all windows. Events are taken within windows, and an event within 3 bars after a kept event is dropped so returns do not overlap.
- Supporting check: The forecast-weighted mean excess 3-bar return over the same events is above 0.
- Confirm: The slope's t-statistic is 2 or more and the forecast-weighted mean excess return is above 0, with at least 30 independent events.
- Reject: The slope's t-statistic is −2 or less, with at least 30 independent events.
- Inconclusive: A slope t between −2 and 2. A slope t of 2 or more with a non-positive weighted mean. Any result from fewer than 30 independent events.
