---
idea: 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 9111077ea370
---
Fidelity:
- Situation: an unbroken streak of rising 4h bars whose gain is large against the coin's typical 4h move over 30 days -> adapted: "after the streak" becomes "while the streak lasts", and "large" becomes graded by the streak's gain in mean absolute one-bar moves over 180 bars.
- Comparison: only while the price is below its 30-day average, more so the further below -> kept: the percent depth below the 180-bar SMA, which is 0 at or above it.
- Outcome: the coin falls over the next three days, more after larger gains and deeper discounts -> kept: a short held for 18 bars, sized by gain times depth.
- Verdict transfer: yes: the component is exactly the streak gain in usual moves times the depth below the 30-day average, held over the idea's 3-day horizon.
Forecast: One component, UpStreakGainTimesDepthBelowAverageComponent (window 180, max_bars 180, ma_period 180: 30 days of 4h bars). It multiplies the current up-streak's gain, counted in mean absolute one-bar moves over 180 bars, by the close's percent depth below its 180-bar SMA. It is standardised over its own past 181 values (min_periods 45), negated to make it a short, then passed through signed_power (exponent 3, pivot 20) as the strongest graded dead zone. The forecast is never positive. It is 0 when bar t did not close up or the close is at or above the 30-day average. It grows more negative, smoothly, as the streak's gain and the discount to the average grow, and small readings are damped towards 0.
Config: 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The cases are short bets (a fall of the forecast of at least 2 points from its highest level since the last bet), read once per 18-bar grid cell of each window. For each case, take the coin's 18-bar return from the signal bar's close minus the coin's normal 18-bar drift over all windows, signed for the short. Measure the mean of this unusual move and its t over the cases, pooled over coins and windows, before costs.
- Supporting check: The mean unusual move of the cases with the larger absolute forecast (above the median) minus that of the smaller ones must be above 0.
- Confirm: The mean unusual move is positive (the coin falls more than its drift) with t >= 2 over at least 30 independent cases, and the supporting check is above 0.
- Reject: The mean unusual move is negative (the coin rises more than its drift after the signal) with t <= -2 over at least 30 independent cases.
- Inconclusive: Any t between -2 and 2, a confirming t whose supporting check is not above 0, or fewer than 30 independent cases.
