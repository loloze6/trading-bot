---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the stretch between an upward cross of the short simple average over the long one and the next downward cross, which is the state "short SMA above long SMA" -> adapted: "after an up-cross, until the down-cross" becomes "while the 50-day SMA is above the 200-day SMA". The on/off state becomes graded by the size of the spread, and the forecast is 0 whenever the short average is below the long one.
- Comparison: random stretches of the same length -> adapted: the forward returns from on-state bars are compared with the forward returns from all bars in the same windows, which is simply holding the coin. Random stretches are an unconditional sample of the coin's path, so this is the same baseline.
- Outcome: price rises more often and further during the up-cross stretch -> kept: the forward BTC return and the share of up moves, measured from on-state bars.
- Verdict transfer: yes: the long position exists exactly while the up-cross stretch lasts, so on-state returns that beat or fail to beat unconditional returns confirm or reject the idea directly.
Forecast: One component, the percent spread between the 50-day and 200-day simple moving averages, computed as (SMA50 − SMA200) / SMA200. It is standardised against its own past 200 values (min_periods 50). That puts it on the forecast scale, with about 10 at an average-sized spread, capped at 20. It is then clipped at 0 from below. - The forecast is positive only while SMA50 is above SMA200, which is the stretch between an up-cross and the next down-cross. - It grows as the short average pulls further above the long one. - It is 0 from the down-cross until the next up-cross. - It is never negative. - The 50/200 pair is the most common daily convention, because the brief gives no lengths.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The mean 20-bar forward BTC close-to-close return from bars where the forecast is above 0, minus the mean 20-bar forward return from all bars. Both are sampled on non-overlapping 20-bar blocks, so overlapping returns are counted once. Results are pooled over the 6 windows and judged before costs against holding the coin.
- Supporting check: The share of on-state 20-bar blocks with a positive return, compared with the share of positive blocks among all blocks.
- Confirm: All three must hold: - The on-state mean 20-bar return exceeds the all-blocks mean by at least 2 percentage points. - A Welch t-statistic of the on-state blocks against the off-state blocks is at least 2. - The on-state share of positive blocks is at least 10 points above the unconditional share.
- Reject: Either of these: - The on-state mean 20-bar return is at or below the all-blocks mean. - The on-state mean 20-bar return is negative, meaning moves after up-crosses reverse.
- Inconclusive: These cases neither confirm nor reject: - A positive excess below 2 points. - A t-statistic below 2. - A hit-rate gap below 10 points. - Fewer than 10 non-overlapping on-state blocks. - Fewer than 5 off-state blocks. - Fewer than 3 distinct up-cross stretches across the 6 windows.
