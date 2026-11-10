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
- Situation: the stretch from an upward cross of the short SMA over the long SMA until the next downward cross, that is, the short average above the long one -> adapted: "after the up-cross, until the down-cross" becomes "while the short SMA is above the long SMA". The on/off state is made graded by the size of the spread (SMA50 − SMA200) / SMA200. The spread is 0 at the cross and grows as the averages separate. Short-average-below stretches give zero, because the idea speaks only of up-cross stretches.
- Comparison: random stretches of the same length -> adapted: the coin's own return over all tested bars of the same windows, measured in equal-length non-overlapping blocks. This is the expected return and hit rate of a random stretch of that length.
- Outcome: price rises more often and further over the stretch (upward) -> kept: forward coin returns while the stretch is active, measured as a hit rate and as an average size.
- Verdict transfer: yes: the main measure uses every bar where the short SMA is above the long SMA, whatever the spread size, so a confirm or reject on it is a confirm or reject of the idea as stated. The spread grading is only checked separately.
Forecast: One indicator, the SMA-pair spread (SMA50 − SMA200) / SMA200 in percent. This is the most common daily-bar convention, the "golden cross", and the brief gives no lengths. The spread is standardised against its own previous 200 values (min 50), so a typical spread maps to about 10, and the result is capped at 20. It is then clipped at 0 below. The forecast is positive while SMA50 is above SMA200, so from the up-cross until the down-cross. It grows smoothly from 0 at the cross as the short average pulls further above the long one. It is exactly 0 while SMA50 is at or below SMA200, so the position is flat outside the idea's stretches. It never goes short.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The coin's 20-bar forward close-to-close return over non-overlapping 20-bar blocks. - The blocks start on bars where the forecast is > 0 and are taken consecutively within each window, so overlapping returns are counted once. - These are compared with the same non-overlapping 20-bar blocks taken over all bars of the six windows, which is the buy-and-hold random-stretch baseline. - The two quantities reported are the difference in mean block return and the difference in share of positive blocks. Both are before costs.
- Supporting check: Is the spread size itself informative? Within in-stretch bars, compare the mean next-bar coin return when the forecast is above its in-stretch median with the mean when it is below. This is reported, but it does not decide the verdict.
- Confirm: Both of the following hold, with at least the minimum counts below: - The in-stretch blocks' mean 20-bar return exceeds the all-bars blocks' mean by at least 3 percentage points, with a one-sided t ≥ 2.0 (Welch) on the block returns. - The in-stretch share of positive blocks exceeds the all-bars share by at least 10 percentage points.
- Reject: Either of the following, with at least the minimum counts below: - The in-stretch mean 20-bar return is at or below the all-bars mean. - The in-stretch share of positive blocks is at or below the all-bars share. A negative excess with t ≤ −2.0 additionally shows reversal after up-crosses, the brief's second failure case.
- Inconclusive: - A positive excess smaller than 3 points, or with t < 2.0, or with only one of the two differences meeting its bar. - Too few cases: fewer than 10 non-overlapping in-stretch 20-bar blocks, or fewer than 3 distinct up-cross-to-down-cross stretches (or stretches already active at a window's start) across the six windows. - Fewer than 25 all-bars blocks.
