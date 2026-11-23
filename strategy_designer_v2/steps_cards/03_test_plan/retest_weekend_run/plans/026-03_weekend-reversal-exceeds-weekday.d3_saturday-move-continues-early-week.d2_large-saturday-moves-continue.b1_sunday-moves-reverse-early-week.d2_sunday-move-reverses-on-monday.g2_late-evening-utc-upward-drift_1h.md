---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: fc27df6a23f8
---
Fidelity:
- Situation: the two hours from 21:00 to 23:00 UTC -> kept: an hour-of-day regime selects the bars stamped 21:00 and 22:00.
- Comparison: return above the coin's normal hourly drift, larger the higher its 30-day hourly volatility -> kept: the drift is the benchmark in the criterion, and the 720-bar volatility sizes the position.
- Outcome: the coin rises more than usual from 21:00 to 23:00, and more so when volatility is high -> kept: the position is long over those 2 bars and sized by volatility.
- Verdict transfer: yes: the test holds exactly that stretch, long, with a size set by the stated volatility, and judges it against the coin's drift.
Forecast: A regime on `HourOfDayComponent` is active when the coming bar is stamped 21:00 or 22:00 UTC, so a position opens at the 20:00 bar's close and is held to 23:00. In every other hour the forecast is 0. Inside the regime the forecast is the 30-day (720-bar) hourly volatility from `VolatilityFromStdDevComponent`, standardised over its past 500 values. It is always positive (long only), about +10 when volatility is at its usual level, and larger up to the cap of 20 when volatility is higher. Its size therefore grows with the coin's 30-day volatility.
Config: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: A case is one coin-day, entered at the close of the bar stamped 20:00. For each case, take the 2-bar return to the 22:00 bar's close minus the coin's mean 2-bar return over all its windows (non-overlapping grid). Average these excess returns weighted by the position held, before costs, and compute the t of that weighted mean.
- Supporting check: The cases with an above-median position (higher volatility) have a larger mean excess return than the cases below the median (difference above 0).
- Confirm: The position-weighted mean excess return is above 0 with t >= 2, and the supporting check passes.
- Reject: The position-weighted mean excess return is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming t whose supporting check fails. At least 200 cases are needed (about 17,000 are expected); with fewer, the result is inconclusive.
