---
idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: the daily close stands above its highest close of the previous 90 days, by some distance -> adapted: "after a close beyond" becomes "while the close is beyond"; the percent distance above the prior 90-day closing high, graded and clipped at 0.
- Comparison: further beyond against less far beyond -> kept: the position grows with the percent distance.
- Outcome: the coin rises more over the next 20 days -> kept: each bet is held 20 daily bars.
- Verdict transfer: yes: the test gains when the close is above the prior 90-day high, in proportion to the distance, over 20 days, which is the idea's own claim.
Forecast: The component is DistanceFromHighComponent with period 90, source close, exclude_current 1 and form percent. On each bar it gives (close − highest close of the previous 90 bars) / that high × 100. Standardise scales it against its own past 91 values, with min_periods 23. A clip at 0 then keeps only the part above the high. The forecast is 0 whenever the close is at or below the prior 90-day closing high. It is positive, and grows in proportion to the distance, while the close stands above that high. It is never negative.
Config: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The sample is the non-overlapping 20-bar grid of each window, using only grid bars with forecast > 0. On each, take post_pipeline_value of beyond_high × (the coin's 20-bar forward return − the coin's mean 20-bar return over all windows). The measure is the ordinary t of the mean of that product.
- Supporting check: Among those positive-forecast grid bars, take the mean drift-adjusted 20-bar return of the upper half by forecast minus that of the lower half. The check passes when this difference is above 0.
- Confirm: The main-measure t is 2 or more, with at least 30 cases, and the supporting check passes.
- Reject: The main-measure t is −2 or less, with at least 30 cases.
- Inconclusive: A t between −2 and 2, or a t of 2 or more with the supporting check failing, is inconclusive. Fewer than 30 positive-forecast grid cases across all coins and windows is also inconclusive.
