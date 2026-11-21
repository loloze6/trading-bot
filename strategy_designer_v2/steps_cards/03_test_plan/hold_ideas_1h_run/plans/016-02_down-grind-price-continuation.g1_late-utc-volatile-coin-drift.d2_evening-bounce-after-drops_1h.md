---
idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's close at 21:00 UTC after a 24-hour fall, measured in units of its 7-day hourly volatility -> adapted: a regime selects the bar whose coming hour is 21 (closing at 21:00), and the size of the vol-scaled 24-bar fall is graded with no threshold.
- Comparison: the larger the fall, the larger the rise; no trade when the coin has not fallen -> kept: the position grows with the fall and is zero when the 24-bar return is not negative.
- Outcome: the coin rises over the two hours after 21:00 -> kept: the book holds the long for 2 bars.
- Verdict transfer: yes: the test measures the 2-hour rise after 21:00 against the size of the vol-scaled 24-hour fall, as the idea states.
Forecast: Only on the bar closing at 21:00 UTC (the coming bar's hour is 21), the forecast reads the 24-bar return divided by the 168-bar (7-day) standard deviation of hourly returns times sqrt(24). It standardises this reading against its own past 168 values, negates it so that a fall reads positive, and clips it at 0. The forecast is positive and grows with the depth of the vol-scaled 24-hour fall. It is 0 when the coin has not fallen and on every other hour. It is never negative.
Config: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The forecast-weighted mean of the excess 2-bar return at bars with forecast > 0. The excess return is close[t+2]/close[t] - 1, inside the window, minus the coin's mean 2-bar return over all windows. Each 21:00 bar is one case, and the cases do not overlap.
- Supporting check: The mean excess 2-bar return of the cases in the upper half of the forecast, minus that of the lower half, is positive (Welch t > 0).
- Confirm: The weighted mean excess return is positive with t >= 2, and the upper-half-minus-lower-half difference is positive.
- Reject: The weighted mean excess return is negative with t <= -2.
- Inconclusive: A t between -2 and 2, or t >= 2 when the upper-minus-lower difference is not positive. The minimum is 300 cases with forecast > 0, counted across all coins and windows.
