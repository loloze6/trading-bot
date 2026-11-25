---
idea: 033-02_upside-break-continues-rising
brief: 033_range-position-predicts-drift
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a daily close above the 20-day high -> kept: a regime rule fires only when the close is above the highest high of the prior 20 bars.
- Comparison: how far the close sits above that high -> kept: inside the regime, the forecast is the percent distance of the close above the prior 20-day high.
- Outcome: the price rises over the next 5 days, more for larger breaks -> kept: the position is long only, held 5 bars, and sized by the break's size.
- Verdict transfer: yes: the test measures this exact situation, the same strength and the same 5-day rise, so both a confirm and a reject apply to the idea.
Forecast: The forecast uses `DistanceFromHighComponent` with period 20, source "high", exclude_current 1 and form "percent". This is (close − highest high of the prior 20 bars) / that high × 100. The regime detector sends a bar to "trending" only when this distance is above 0, which means the close broke above the 20-day high. Every other bar is flat. Inside the regime the same distance is standardised over its past 60 values and clipped at 0. The forecast is therefore positive and grows with how far the close sits above the prior high. It is zero whenever there is no breakout. The book never goes short.
Config: 033-02_upside-break-continues-rising_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move per case. A case is a long bet, that is, a rise of the forecast of at least 2 points, read once per 5-bar grid cell. The unusual move is the coin's 5-bar return from the signal's close minus the coin's normal 5-bar drift over all windows. Its t is computed with the cases of one day pooled.
- Supporting check: Graded size. The mean unusual move of cases with a forecast above the cases' median, minus that of cases at or below the median, is above 0.
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The mean unusual move is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a confirming t whose graded-size check fails. Fewer than 30 distinct case days is also inconclusive.
