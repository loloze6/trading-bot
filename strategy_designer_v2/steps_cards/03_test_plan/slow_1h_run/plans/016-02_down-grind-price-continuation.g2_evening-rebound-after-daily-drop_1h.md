---
idea: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's fall over the past 24 hours, measured against its own volatility -> kept
- Comparison: none beyond "the more"; the larger the fall, the larger the rise -> kept
- Outcome: the price rises over the two hours from 21:00 to 23:00 UTC that follow -> adapted: "after X" made "while X", so the 22:00 bar re-reads the 24-hour fall one hour later
- Verdict transfer: yes: the test is the idea's own graded fall measure, sized into the idea's own two-hour slot, so a confirm or a reject carries over to the idea.
Forecast: The forecast is active only when the coming bar starts at 21:00 or 22:00 UTC. It is a regime chosen by the hour of day, because that slot is part of the idea. Inside it, the measure is the 24-bar return divided by the usual move (`VolatilityScaledReturnComponent`, period 24, vol_period 20), negated so that a fall reads positive. It is standardised over 60 bars and clipped at 0. The forecast is positive and grows with the size of the fall in usual moves. It is 0 when the coin did not fall, and 0 on every other hour of the day. It is long only, as the idea only claims a rise after a fall.
Config: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The decision bar is each day's bar stamped 20:00 UTC, which closes at 21:00; that gives one non-overlapping case per day, coin and window. On these bars, regress the coin's 2-bar return (close[t+2] / close[t] - 1) minus the coin's mean 2-bar return over all windows on the recorded forecast. Report the slope's t.
- Supporting check: On decision bars whose forecast is above the median of the positive forecasts, the mean excess 2-bar return (as above) is above 0.
- Confirm: The slope is positive with t >= 2, and the supporting check passes.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any slope with -2 < t < 2, or t >= 2 with a failed supporting check. At least 300 decision bars with a positive forecast are needed; with fewer, the result is inconclusive.
