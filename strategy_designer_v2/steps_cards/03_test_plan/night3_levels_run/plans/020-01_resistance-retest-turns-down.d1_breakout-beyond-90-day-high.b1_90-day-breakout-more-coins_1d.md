---
idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.b1_90-day-breakout-more-coins
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: e48527ec0eac
---
Fidelity:
- Situation: the daily close stands above its highest close of the previous 90 days, by some distance -> kept
- Comparison: the further above that prior 90-day high, the larger the rise -> kept
- Outcome: the coin rises over the next 5 days -> kept
- Verdict transfer: yes: the forecast is the percent distance above the prior 90-day closing high, long only, held 5 days.
Forecast: The forecast uses one indicator: the close's percent distance from the highest close of the 90 bars before today, with today excluded (DistanceFromHighComponent, period 90, source close, exclude_current 1, form percent). It is standardised over its past 90 values (min_periods 22) and then clipped at 0. The forecast is 0 whenever the close is at or below the prior 90-day high. It is positive only when the close stands above that high, and it grows in proportion to how far above. It is never negative, so the idea takes no short against a breakout.
Config: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.b1_90-day-breakout-more-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window and keep the bars with forecast > 0. For each such case, take the coin's 5-bar return minus the coin's mean 5-bar return over all its windows. The measure is the mean of forecast x that excess return, pooled over coins, with its ordinary t.
- Supporting check: Split the cases at the median forecast. The mean excess 5-bar return of the upper half minus that of the lower half must be greater than 0.
- Confirm: Main measure t >= 2, and the upper-half minus lower-half difference is greater than 0.
- Reject: Main measure t <= -2.
- Inconclusive: The idea is inconclusive in three cases: - -2 < t < 2; - t >= 2 but the upper-half minus lower-half difference is <= 0; - fewer than 30 independent cases on the grid.
