---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g1_volatile-market-falls-rebound-next-day
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: fc27df6a23f8
---
Fidelity:
- Situation: a coin's 24-hour fall, in usual 30-day daily moves, with high 30-day hourly volatility -> adapted: "after a fall" made "while the 24h return is a fall", graded by its size times the 30-day hourly volatility.
- Comparison: the rise against the coin's normal drift, with rises followed by no comparable fall -> kept: drift is removed in the criterion, and the post-rise move is checked separately.
- Outcome: the price rises over the next 24 hours, more after larger falls and in more volatile months -> kept: a long held for 24 bars, sized by the forecast.
- Verdict transfer: yes: the forecast is exactly the idea's fall-times-volatility reading, long only, judged over its own 24h horizon against drift.
Forecast: One component, MeanAbsScaledReturnTimesVolatilityComponent (period 24, window 720, vol_period 720, no cap). It is the 24-bar return in multiples of the 30-day mean absolute 24-bar return, times the 30-day standard deviation of hourly returns. The forecast standardises it over its past 500 values, negates it, and clips it at 0. It is positive only while the coin is down over 24 hours. It grows linearly with the depth of the fall in usual daily moves and with the 30-day hourly volatility. It is zero after flat or rising stretches, so the strategy never goes short.
Config: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g1_volatile-market-falls-rebound-next-day_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The sample is the bars at positions 0, 24, 48, ... of each window, for every coin. On each of them, compute (forecast / 10) x (close[t+24] / close[t] − 1 − the coin's mean 24-bar return over all windows). The measure is the mean of this value and its t, before costs.
- Supporting check: Take the same grid bars where the component's last_history_value is positive and in that coin's top fifth of positive values. Their mean drift-adjusted 24-bar return must not be negative with a t of −2 or less, which is the idea's "no comparable fall after rises".
- Confirm: The main measure's t is at least 2, and the supporting check passes.
- Reject: The main measure's t is at most −2, or the post-rise mean has a t of at most −2 (rises are reversed too).
- Inconclusive: Any other result, including a main t between −2 and 2 or an estimate near zero. At least 200 grid bars with forecast > 0 are needed across coins and windows; below that the test is inconclusive.
