---
idea: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the 21:00 UTC bar, with the coin's 24-hour fall -> adapted: "from the 21:00 bar" becomes "while on the 21:00 and 22:00 bars", and the 24-bar fall is read at each of those bars.
- Comparison: a deeper 24-hour fall against a shallower one -> kept: the position grows with the depth of the 24-bar fall.
- Outcome: the return over the next 2 hours is positive, and larger after deeper falls -> kept: the 2-bar return after the 21:00 close, judged against holding the coin.
- Verdict transfer: yes: the test holds long from 21:00 to 23:00, sized by the 24-hour fall, so its result is the idea's result.
Forecast: The forecast is active only on bars stamped 21:00 and 22:00 UTC, where the next bar starts at hour 22 or 23. A rule on HourOfDayComponent selects these bars. Together they cover the two hours from the 21:00 close to 23:00. On those bars the forecast is the 24-bar percent change, standardised over the 60 bars before it, then negated and clipped at 0. It is positive after a 24-hour fall and grows with the depth of the fall, capped at 20. It is zero after a 24-hour rise and on every other hour of the day.
Config: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Use one case per day: the bar stamped 21:00 in each window. For each case, take the excess return, close[t+2]/close[t]-1 minus the coin's mean 2-bar return over all windows. The measure is the OLS slope of this excess return on that bar's forecast, with all coins and days pooled.
- Supporting check: On 21:00 bars with forecast > 0, the mean of the same excess 2-bar return is above 0.
- Confirm: The slope's t is at least 2, and the supporting mean's t is at least 2.
- Reject: The slope's t is -2 or lower, or the supporting mean's t is -2 or lower.
- Inconclusive: Any other result, for example a t between -2 and 2 on either measure, or a strong slope with a weak mean, is neither a confirm nor a reject. Fewer than 300 days with forecast > 0 across coins is also inconclusive.
