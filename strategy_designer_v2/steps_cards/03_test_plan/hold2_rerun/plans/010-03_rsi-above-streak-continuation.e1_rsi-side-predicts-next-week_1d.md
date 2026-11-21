---
idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 70a362722b07
---
Fidelity:
- Situation: the coin's 14-day RSI at the close, and how far it sits above or below 50 -> kept
- Comparison: above 50 against below 50, sized by the distance from 50 -> kept
- Outcome: the return over the next 1 to 7 days is higher the further RSI is above 50, and lower the further it is below -> kept
- Verdict transfer: yes: the forecast is RSI minus 50, graded and signed, judged on the next 7 daily bars, as the idea states.
Forecast: The forecast is RSI(14) minus 50, built from RSIPullbackComponent (period 14, long_only false), which outputs (50 − RSI) × sf, then negated. It is standardised against its own last 60 values (min_periods 20) and has no regime gate. It is positive when RSI is above 50 and negative when RSI is below 50. Its size grows linearly with the distance from 50, it is zero at exactly 50, and it is capped at ±20.
Config: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: The sample is non-overlapping 7-bar cases (positions 0, 7, 14, … of each window, per coin). For each case, take the forecast at bar t divided by 10, times the coin's 7-bar return minus that coin's mean 7-bar return over all windows. The measure is the mean of this product across all cases, with the ordinary t of the mean. This is the forecast-weighted excess return, so the coin's own rise is not credited to the idea.
- Supporting check: On the same cases, the mean excess 7-bar return when the forecast is above 0, minus the mean when the forecast is below 0 (Welch t), has the same sign as the main measure.
- Confirm: The main measure is positive with t ≥ 2, and the supporting difference is positive.
- Reject: The main measure is negative with t ≤ −2, and the supporting difference is negative. That would mean returns run against the side RSI is on.
- Inconclusive: Any other result: |t| < 2, including a main measure near zero, or the main measure and the check disagreeing in sign. At least 300 independent cases are needed across the coins, or the result is inconclusive.
