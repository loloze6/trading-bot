---
idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 3d6ac1c822df
---
Fidelity:
- Situation: a 4h bar closes below the lowest low of the preceding two-day (12-bar) stretch, while the coin's 30-day (180-bar) return is positive -> kept: both are regime rules on the close's distance below the prior 12-bar low and on the 180-bar return.
- Comparison: how narrow that 12-bar stretch was against the coin's 30-day (180-bar) average 4h bar range -> adapted: "narrower than usual" is made graded, so the short grows as the stretch narrows and is zero when it is no narrower than usual.
- Outcome: the coin falls over the next three days (18 bars), more after a narrower stretch -> kept: a short held for 18 bars, sized by narrowness.
- Verdict transfer: yes: the test shorts exactly these breaks in rising months, sized by narrowness against the 30-day mean bar range, over three days, so its result is the idea's result.
Forecast: The forecast is computed only on a bar where two conditions hold together. The close must be below the lowest low of the prior 12 bars, current bar excluded. The 180-bar return must be positive. On every other bar the forecast is flat. On a qualifying bar, the forecast measures how narrow the stretch was. It reads the prior 12-bar stretch's high-low span divided by the mean 4h bar range over the last 180 bars, then standardises that over its own past 180 values (about 10 on average). It caps the result at 10 and subtracts a constant 10 at equal weight. The forecast is (min(width, 10) - 10) / 2. That gives 0 for a stretch no narrower than usual, down to -5 (a 50 percent short) as the stretch shrinks toward nothing. It is never positive.
Config: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Each case is a short bet: a fall of the forecast of at least 2 points, read once per non-overlapping 18-bar grid cell of each window. For each case, take the coin's 18-bar return from the signal bar's close, subtract the coin's normal 18-bar drift over all windows, and count a fall as positive. The measure is the mean of that unusual move over all cases, with its t of the mean. It is judged before costs.
- Supporting check: The cases in the narrower half (forecast at or below the median case forecast) must have a mean short-side unusual move above that of the wider half (Welch difference narrower minus wider greater than 0).
- Confirm: The mean short-side unusual move is above 0 with t >= 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean short-side unusual move is below 0 with t <= -2 over at least 30 cases, meaning the coin rose more than its drift after these breaks.
- Inconclusive: Any t between -2 and 2, a confirming t whose supporting check fails, or fewer than 30 cases.
